"""The Ethiopian and Japanese emperor rosters, built from Wikidata.

    python scripts/build-emperor-rosters.py

**Emma, 2026-09-03**, asked how to source them: *"Build from Wikidata later."* Both are
entry-point groups dated 2027-01-01 in `reports/entry-point-groups.tsv` and both resolved to
**0** people, because nothing in the repo enumerates either.

**The roster is the holders of a POSITION, never a label match.** `queue.md` said it in the
item and `CLAUDE.md` § *A clan name is not a clan* is the general rule: the 52 tree labels
matching Ethiopia/Negus are the surname *Neguse*, which is what a name screen would catch.
So the query is `?p wdt:P39 wd:<position>` and nothing else decides membership.

**The two positions, confirmed with `wbsearchentities` rather than guessed** ---
`CLAUDE.md` § *Do not guess these*, and § *Always write the English label next to a property
or item ID*:

| position | label | description |
| --- | --- | --- |
| `Q10962705` | *Emperor of Ethiopia* | hereditary rulers of the Ethiopian Empire |
| `Q208233` | *Emperor of Japan* | head of state of Japan |

**The Geni join has THREE sources and the order is hers.** `CLAUDE.md` § *The Geni BIO
carries her own QID claims. Read them before any download* --- her own bio links are the
freshest statement of identity there is, so they are read first; then the live `P2600` on the
item; then the local `p2600-all.tsv` snapshot. The `geni_source` column records which one
answered, so a row can be traced rather than trusted.

**A blank `geni_ids` is not a failure.** The ledger is keyed on the Geni id, so an emperor
without one cannot become a ledger row --- but the QID is still the roster's answer to *who
are they*, and `group_qids()` keeps the pair either way. What a blank means is **we hold no
link**, never *no Geni profile exists*: `CLAUDE.md` § *"Is X present?"*.

Writes `reports/ethiopian-emperors.tsv` and `reports/japanese-emperors.tsv`.
"""
from __future__ import annotations

import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import WikidataClient  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]

#: `(group, position qid, position label, output file)`. The group names match
#: `reports/entry-point-groups.tsv` so the rows can be pointed at these files.
ROSTERS = [
    ("ethiopian-emperors", "Q10962705", "Emperor of Ethiopia", "ethiopian-emperors.tsv"),
    ("japanese-emperors", "Q208233", "Emperor of Japan", "japanese-emperors.tsv"),
]

QUERY = """SELECT ?p ?pLabel ?geni WHERE {
  ?p wdt:P39 wd:%s .
  OPTIONAL { ?p wdt:P2600 ?geni }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}"""


def _sort_key(qid: str) -> tuple[int, str]:
    """A TOTAL order --- `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*.

    Numeric so `Q99` sorts before `Q100`, with the raw string as the tiebreaker so two
    spellings of one number could never depend on insertion order.
    """
    try:
        return (int(qid[1:]), qid)
    except ValueError:
        return (1 << 62, qid)


def bio_links() -> dict[str, str]:
    """`qid -> geni id` from her own Geni *About Me* links, read out of the corpus."""
    path = ROOT / "out" / "bio-qids.tsv"
    out: dict[str, str] = {}
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            geni = (row.get("geni_id") or "").strip()
            if qid.startswith("Q") and geni.isdigit():
                out.setdefault(qid, geni)
    return out


def stored_p2600() -> dict[str, str]:
    """`qid -> geni id` from the local `p2600-all.tsv` snapshot.

    **The file has NO HEADER --- its first line is data.** Read with a header-consuming
    reader it silently ate `Q1000005` and fell through to positional indices that happened
    to be right, which is the § *check the separator before believing a distribution* failure
    in miniature: a parser that narrows its input and still prints a plausible number. Two
    bare columns, read as two bare columns.

    It also keeps DEPRECATED statements, unlike `wdt:` in the live query --- `CLAUDE.md`
    § *A second Geni ID on one Wikidata item is NOT a conflict* --- so it is consulted last
    rather than first.
    """
    path = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    out: dict[str, str] = {}
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 2:
                continue
            qid, geni = row[0].strip(), row[1].strip()
            if qid.startswith("Q") and geni.isdigit():
                out.setdefault(qid, geni)
    return out


def main() -> None:
    client = WikidataClient(cache_dir=ROOT / "out" / "wikidata" / "cache")
    bios, stored = bio_links(), stored_p2600()

    for group, position, position_label, filename in ROSTERS:
        rows = client.sparql(QUERY % position)
        people: dict[str, dict[str, str]] = {}
        for row in rows:
            qid = row["p"].rsplit("/", 1)[-1]
            entry = people.setdefault(qid, {"label": "", "live": ""})
            entry["label"] = entry["label"] or (row.get("pLabel") or "")
            if row.get("geni"):
                entry["live"] = entry["live"] or str(row["geni"]).strip()

        out_path = ROOT / "reports" / filename
        counts = {"bio": 0, "live": 0, "store": 0, "none": 0}
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerow(["qid", "label", "geni_ids", "geni_source", "position"])
            for qid in sorted(people, key=_sort_key):
                entry = people[qid]
                # Her bio links first, then the item's own statement, then the snapshot.
                if qid in bios:
                    geni, source = bios[qid], "bio"
                elif entry["live"]:
                    geni, source = entry["live"], "live"
                elif qid in stored:
                    geni, source = stored[qid], "store"
                else:
                    geni, source = "", ""
                counts[source or "none"] += 1
                writer.writerow([qid, entry["label"], geni, source, position])

        held = len(people) - counts["none"]
        print(
            f"{group}: {len(people)} holders of {position} ({position_label}), "
            f"{held} with a Geni id "
            f"(bio {counts['bio']}, live {counts['live']}, store {counts['store']}) "
            f"-> reports/{filename}"
        )


if __name__ == "__main__":
    main()
