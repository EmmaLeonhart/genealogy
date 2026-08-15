"""Who are the Wikidata people with no genealogy? A demographic census.

**Emma, 2026-08-15:** *"Can you look over the isolated wikidata individuals? I
want to analyze who they are. We did a bit of analysis but I want to basically
analyze them demographically."*

**Isolated means present as an item and absent as genealogy** — `CLAUDE.md`
§ *An item with no relationships is not a missing item*. The Samaritan high
priests are the worked example: on Geni, on Wikidata, attached to nothing. Her own
`Q140568870` is the same shape. The earlier pass established *that* they exist;
this asks *who they are*.

**Isolated is defined on five properties**: `P22` father, `P25` mother, `P40`
child, `P3373` sibling, `P26` spouse. An item stating none of them has no
genealogy. `P26` is included because a recorded marriage is a family relationship
even when no children are stated.

**THE LIMIT, and it is not a footnote.** The store is a **Geni-shaped slice** —
seeded from `P2600` holders and walked outward along those same five properties.
So an item whose relatives were simply never downloaded looks *identical* to one
that genuinely has no relatives. This census therefore reports two populations
separately and never merges them:

* **`stated-none`** — the item itself states no relationship. This is a fact about
  Wikidata.
* **`edge-of-slice`** — the item states relationships whose targets we do not
  hold. This is a fact about **our download**, not about Wikidata.

Only `stated-none` is isolation. Calling both isolated would measure our sampling
and report it as Wikidata's content, which is the § *"Is X present?"* failure.

Writes `reports/wikidata-isolates.md` and `.csv`.

    py scripts/measure-wikidata-isolates.py
"""

from __future__ import annotations

import csv
import glob
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge.matching import year_of  # noqa: E402

ITEMS = REPO / "wikidata" / "items"
LABELS = REPO / "reports" / "wikidata-labels.tsv"
OUT_MD = REPO / "reports" / "wikidata-isolates.md"
OUT_CSV = REPO / "reports" / "wikidata-isolates.csv"

FAMILY = ("P22", "P25", "P40", "P3373", "P26")
HUMAN, INSTANCE_OF = "Q5", "P31"
BIRTH, DEATH = "P569", "P570"
SEX, OCCUPATION, TITLE, COUNTRY = "P21", "P106", "P97", "P27"
GENI = "P2600"

SEX_LABEL = {"Q6581097": "male", "Q6581072": "female"}


def targets(entity: dict, prop: str) -> list[str]:
    out = []
    for claim in (entity.get("claims") or {}).get(prop, []):
        snak = claim.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict) and value.get("id"):
            out.append(value["id"])
    return out


def first_string(entity: dict, prop: str) -> str:
    for claim in (entity.get("claims") or {}).get(prop, []):
        snak = claim.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, str):
            return value
    return ""


def first_year(entity: dict, prop: str) -> int | None:
    for claim in (entity.get("claims") or {}).get(prop, []):
        snak = claim.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict):
            year = year_of(value.get("time"))
            if year is not None:
                return year
    return None


def century(year: int | None) -> str:
    if year is None:
        return "no date"
    if year < 0:
        return "BCE"
    return f"{(year // 100) * 100 + 1}s"


def main() -> int:
    shards = sorted(glob.glob(str(ITEMS / "*.jsonl.gz")))
    print(f"streaming {len(shards):,} shards", flush=True)

    held: set[str] = set()
    people: dict[str, dict] = {}

    for n, shard in enumerate(shards, 1):
        with gzip.open(shard, "rt", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entity = json.loads(line)
                except json.JSONDecodeError:
                    continue
                qid = entity.get("id")
                if not qid:
                    continue
                held.add(qid)
                if HUMAN not in targets(entity, INSTANCE_OF):
                    continue
                rel = {p: targets(entity, p) for p in FAMILY}
                people[qid] = {
                    "rel": rel,
                    "birth": first_year(entity, BIRTH),
                    "death": first_year(entity, DEATH),
                    "sex": (targets(entity, SEX) or [""])[0],
                    "occupation": len(targets(entity, OCCUPATION)),
                    "title": len(targets(entity, TITLE)),
                    "country": len(targets(entity, COUNTRY)),
                    "geni": first_string(entity, GENI),
                    "labels": len(entity.get("labels") or {}),
                }
        if n % 300 == 0:
            print(f"  {n:,}/{len(shards):,} shards, {len(people):,} humans",
                  flush=True)

    print(f"\n{len(held):,} items, {len(people):,} of them human", flush=True)

    labels: dict[str, str] = {}
    with open(LABELS, encoding="utf-8") as handle:
        for line in handle:
            qid, _, label = line.rstrip("\n").partition("\t")
            if label:
                labels[qid] = label

    stated_none: list[str] = []
    edge: list[str] = []
    connected = 0
    for qid, rec in people.items():
        stated = [t for p in FAMILY for t in rec["rel"][p]]
        if not stated:
            stated_none.append(qid)
        elif not any(t in held for t in stated):
            edge.append(qid)
        else:
            connected += 1

    print(f"  stated-none  {len(stated_none):,}")
    print(f"  edge-of-slice {len(edge):,}")
    print(f"  connected     {connected:,}")

    rows = []
    for qid in stated_none:
        rec = people[qid]
        rows.append([qid, labels.get(qid, ""), century(rec["birth"]),
                     rec["birth"] if rec["birth"] is not None else "",
                     rec["death"] if rec["death"] is not None else "",
                     SEX_LABEL.get(rec["sex"], ""), rec["occupation"],
                     rec["title"], rec["country"], rec["geni"], rec["labels"]])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qid", "label", "century", "birth_year", "death_year",
                         "sex", "occupations", "titles", "countries",
                         "geni_id", "label_languages"])
        writer.writerows(rows)

    def tally(key) -> Counter:
        return Counter(key(people[q]) for q in stated_none)

    by_century = tally(lambda r: century(r["birth"]))
    by_sex = tally(lambda r: SEX_LABEL.get(r["sex"], "not stated"))
    dated = sum(1 for q in stated_none if people[q]["birth"] is not None)
    with_geni = sum(1 for q in stated_none if people[q]["geni"])
    with_occ = sum(1 for q in stated_none if people[q]["occupation"])
    with_title = sum(1 for q in stated_none if people[q]["title"])

    def order(key: str):
        if key == "BCE":
            return (0, 0)
        if key == "no date":
            return (2, 0)
        return (1, int(key.rstrip("s")))

    L: list[str] = []
    add = L.append
    add("# Who the isolated Wikidata people are")
    add("")
    add("**Emma, 2026-08-15:** *\"I want to basically analyze them demographically.\"*")
    add("")
    add("**Isolated = the item states no `P22`/`P25`/`P40`/`P3373`/`P26`.** Every one")
    add("is a row in `reports/wikidata-isolates.csv`.")
    add("")
    add("| | items |")
    add("| --- | ---: |")
    add(f"| humans in the store | {len(people):,} |")
    add(f"| **stated-none — no relationship at all** | **{len(stated_none):,}** |")
    add(f"| edge-of-slice — states relatives we do not hold | {len(edge):,} |")
    add(f"| connected | {connected:,} |")
    add("")
    add("**`edge-of-slice` is NOT isolation.** Those items state relationships whose")
    add("targets were never downloaded — a fact about our slice, not about Wikidata.")
    add("Merging the two would measure our own sampling and report it as Wikidata's")
    add("content, which is the § *\"Is X present?\"* failure this repo keeps making.")
    add("")
    add("## By century of birth")
    add("")
    add("| century | isolated | share |")
    add("| --- | ---: | ---: |")
    for key in sorted(by_century, key=order):
        n = by_century[key]
        add(f"| {key} | {n:,} | {100.0*n/max(len(stated_none),1):.1f}% |")
    add("")
    add(f"**Only {dated:,} of {len(stated_none):,} carry a birth date at all** "
        f"({100.0*dated/max(len(stated_none),1):.1f}%).")
    add("")
    add("## Sex, and what else they carry")
    add("")
    add("| | items | share |")
    add("| --- | ---: | ---: |")
    for key, n in by_sex.most_common():
        add(f"| {key} | {n:,} | {100.0*n/max(len(stated_none),1):.1f}% |")
    add(f"| carries an occupation `P106` | {with_occ:,} | "
        f"{100.0*with_occ/max(len(stated_none),1):.1f}% |")
    add(f"| carries a noble title `P97` | {with_title:,} | "
        f"{100.0*with_title/max(len(stated_none),1):.1f}% |")
    add(f"| **carries a Geni ID `P2600`** | **{with_geni:,}** | "
        f"{100.0*with_geni/max(len(stated_none),1):.1f}% |")
    add("")
    add("A `P2600` on an isolated item is the case `CLAUDE.md` describes: the person")
    add("is on Geni **and** on Wikidata, and what is missing is the genealogy.")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\nwrote {OUT_MD} and {OUT_CSV}")
    print(f"  dated {dated:,}  with Geni ID {with_geni:,}  "
          f"occupation {with_occ:,}  title {with_title:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
