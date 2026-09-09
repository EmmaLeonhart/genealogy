"""Does Wikidata hold items for the eccentric clusters, and which pairs are solid enough to keep?

**Emma, 2026-09-05, on the first version of `reports/eccentric-clusters.md`:** *"your measurement
of there being qids is a bit flawed. Both Chinese lines likely have wiki data items even if no
connection. Pre dynastic Egypt definitely does… Axum certainly have qids lol… Third intermediate
period def has qids lol"*. Then: *"write these ones into that identification gedcom thing that
serves the dual purpose of entity resolution through adding dummy bios with the wikidata links"*.

**`P2600` counts a LINK, not an item.** That was the error in the first report: a cluster reading
`0` means nobody has joined those Geni profiles to Wikidata, and the report said *"every other
cluster is 0"* as though it were a fact about Wikidata's holdings. `CLAUDE.md` § *"Is X present?"*
is the standing rule — an absence names the store it is about.

So this asks Wikidata itself, and then **verifies every hit against the full item** rather than
trusting the search. Egress is blocked in the sandbox and ordinary in Actions, so it runs there:
`.github/workflows/check-cluster-items.yml`.

## The search is weak in BOTH directions, which is why nothing here is a verdict

- **`wbsearchentities` is a PREFIX search over labels and aliases.** Geni writes `Makeda Queen of
  Sheba`; Wikidata's label is `Queen of Sheba`, so the compound string matches nothing and the
  Axumite cluster first read **0 of 12** — the query format, not Wikidata.
  `namemodel.drop_title_tail` is the repo's own list, built for the `P735` emitters, and takes it
  to `Makeda`. Both forms are searched and the matching one is recorded.
- **A common name matches a living stranger.** The 李 Lee cluster first read *items exist* on
  `Dave Lee -> Q1691840 (British DJ and house music producer)`, `Alice Chung -> Q98293885
  (researcher)` and `Barbara Weil -> Q88846 Barbara Weiler (German politician)`, against
  Geni-**redacted** people who share a surname.
- **A hit can be a NAME ITEM rather than a person** — `Solomon -> Q18607853 (male given name)`.
  This repo creates name items, so that is the expected shape rather than a coincidence.

**There is therefore no `verdict` column and there must not be one.** A word summarising the
count asserted an identity in both directions at once. What is emitted is one row per candidate
carrying the evidence to judge it — and `CLAUDE.md` § *"Analyse this" means build a CSV* is what
that is: the census first, then a sample read by eye.

## What the evidence columns are, and why dates carry it

`instance_of_human` kills the name items, the settlements (`Namlit -> Q6961940`, *human
settlement in Myanmar*) and the genera (`Kapes -> Q6366576`, *genus of procolophonians*).

**The birth and death years on both sides do the rest**, and that is not a preference:
`reports/zipper-reliability.md` measures the `date` step at **0.0%** disagreement against
`solo`'s 11.8% and `name`'s 9.2%. `CLAUDE.md` § *1600-1900 is the band where NAMES LIE and YEARS
decide* is the same finding from the other side. Every cluster this touches is ancient, so a hit
whose dates are modern is a stranger however well the string matches.

**Nothing here writes a pair anywhere.** `scripts/build-qid-links-gedcom.py` holds an explicit
constant, by her design — *"Do not let it become an architecture"* — and its own docstring says
widening it *"is a decision, not a default"*. This file is the evidence that decision is made on.

Writes `reports/eccentric-cluster-candidates.tsv`.
"""
from __future__ import annotations

import collections
import csv
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from namemodel import drop_title_tail                       # noqa: E402 - after sys.path
sys.path.insert(0, str(ROOT / "src"))
from genimerge.wikidata import require_agent               # noqa: E402 - after sys.path

MEMBERS = ROOT / "reports" / "eccentric-cluster-members.tsv"
FACTS = ROOT / "reports" / "derived-facts.csv"
OUT = ROOT / "reports" / "eccentric-cluster-candidates.tsv"

API = "https://www.wikidata.org/w/api.php"
#: ⛔ THE USER-AGENT IS THE CONTACT ADDRESS AND NOTHING ELSE, and it is never written here.
#: Emma, 2026-08-18: *"no fucking github links in it either"* -- a repository URL in a constant
#: names her repositories to anyone reading the code, and so does a description of what the
#: project does. `tests/test_bot_identity.py::test_no_source_file_links_a_repository` scans every
#: file under `scripts/` and `src/genimerge/` for the host and fails the suite; this script
#: hardcoded one and is what turned CI red.
#: `genimerge.wikidata.require_agent()` reads BOT_CONTACT, falls back to the gitignored
#: `.bot-contact`, and fails with a clear message rather than sending an empty agent -- which
#: Wikimedia answers with a bare 403.

#: The cut to check. 100 is where the report's distinct populations separate.
CUT = 100

#: Seconds between requests. `CLAUDE.md` § *Querying Wikidata is ALLOWED* -- *"Be polite about
#: the rate"*. `wbsearchentities` takes one name per call, so the politeness is the gap;
#: `wbgetentities` takes fifty ids, so the items cost a fraction of the searches.
PAUSE = 0.25

HUMAN = "Q5"

NOT_A_NAME = re.compile(r"^\(|^NN\b|^Private$", re.I)
LATIN = re.compile(r"^[\W\d_]*[A-Za-z]")


def searchable(label: str) -> bool:
    """A label worth putting to `wbsearchentities`.

    Latin script, not a redaction marker, four characters or more. A Geni CJK label is usually a
    generational string -- `禄 (入闽始祖晋安郡王) 林 第1世闽南林氏衍派` -- that no Wikidata label
    resembles, so a miss would measure the label format rather than Wikidata's holdings. Those
    people are counted as `not-searchable`, which is an honest third answer and not a zero.
    """
    label = label.strip()
    return bool(label and not NOT_A_NAME.match(label) and LATIN.match(label) and len(label) >= 4)


def forms(label: str):
    """The strings worth searching for one person, best first: the label, then title-stripped."""
    label = label.strip()
    out = [label]
    stripped = drop_title_tail(label).strip()
    if stripped and stripped != label:
        out.append(stripped)
    return out


def _get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": require_agent()})
    try:
        with urllib.request.urlopen(req, timeout=45) as fh:
            return json.loads(fh.read().decode("utf-8"))
    except Exception as exc:                       # noqa: BLE001 - reported, never swallowed
        print(f"    ! {params.get('search') or params.get('ids')}: {exc}",
              file=sys.stderr, flush=True)
        return None


def search(term: str):
    got = _get({"action": "wbsearchentities", "search": term, "language": "en",
                "uselang": "en", "type": "item", "limit": "3", "format": "json"})
    return None if got is None else got.get("search", [])


def _year(claims, prop):
    """The year of the first `prop` time value, signed, or `''`.

    Wikidata writes `+0332-01-01T00:00:00Z` and `-0500-00-00T00:00:00Z`; the leading sign is the
    era and must survive, which is the same trap `genimerge.dates` records for Geni's `-73`.
    """
    for st in claims.get(prop, ()):
        value = (st.get("mainsnak", {}).get("datavalue") or {}).get("value") or {}
        t = value.get("time") or ""
        m = re.match(r"([+-])0*(\d+)-", t)
        if m:
            return ("-" if m.group(1) == "-" else "") + m.group(2)
    return ""


def full_items(qids):
    """`{qid: {...}}` for every id, fifty at a time -- `wbgetentities` batches, so use it."""
    out = {}
    qids = sorted(set(qids))
    for i in range(0, len(qids), 50):
        batch = qids[i:i + 50]
        got = _get({"action": "wbgetentities", "ids": "|".join(batch),
                    "props": "labels|descriptions|claims", "languages": "en", "format": "json"})
        time.sleep(PAUSE)
        if got is None:
            continue
        for qid, item in (got.get("entities") or {}).items():
            claims = item.get("claims") or {}
            types = [(st.get("mainsnak", {}).get("datavalue") or {}).get("value", {}).get("id")
                     for st in claims.get("P31", ())]
            out[qid] = {
                "label": ((item.get("labels") or {}).get("en") or {}).get("value", ""),
                "description": ((item.get("descriptions") or {}).get("en") or {}).get("value", ""),
                "human": HUMAN in types,
                "instance_of": " ".join(t for t in types if t),
                "birth": _year(claims, "P569"),
                "death": _year(claims, "P570"),
                "p2600": " ".join(
                    (st.get("mainsnak", {}).get("datavalue") or {}).get("value", "")
                    for st in claims.get("P2600", ())),
            }
        print(f"  fetched {min(i + 50, len(qids))}/{len(qids)} items", flush=True)
    return out


def our_dates():
    """`{geni_id: (birth_year, death_year)}` from the derived facts."""
    out = {}
    with open(FACTS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            b, d = (row.get("birth_date_year") or "").strip(), (row.get("death_date_year") or "").strip()
            if b or d:
                out[row["geni_id"]] = (b, d)
    return out


def main() -> int:
    if not MEMBERS.exists():
        sys.exit(f"missing {MEMBERS.relative_to(ROOT)} -- run scripts/eccentric-clusters.py")

    by_cluster = collections.defaultdict(list)
    with open(MEMBERS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if int(row["cut"]) == CUT:
                by_cluster[int(row["rank"])].append(row)

    # `or "20"`, not a `get` default: an unset workflow input arrives as an EMPTY string, not as
    # an absent variable, so the default never fired and `int("")` killed a run.
    limit = int((os.environ.get("CLUSTERS") or "20").strip())
    per = int((os.environ.get("PER_CLUSTER") or "60").strip())
    ranks = sorted(by_cluster)[:limit]
    print(f"cut {CUT}: {len(ranks)} clusters of {len(by_cluster)}, up to {per} names each",
          flush=True)

    dates = our_dates()
    found = []
    for rank in ranks:
        members = sorted(by_cluster[rank],
                         key=lambda r: (-int(r["dist_charlemagne"]), r["geni_id"]))
        pool = [m for m in members if searchable(m["label"])][:per]
        print(f"  cluster {rank}: {len(members):,} people, {len(pool)} searchable", flush=True)
        for m in pool:
            for term in forms(m["label"]):
                got = search(term)
                time.sleep(PAUSE)
                if got is None:
                    break
                if got:
                    b, d = dates.get(m["geni_id"], ("", ""))
                    found.append({"cut": CUT, "rank": rank, "geni_id": m["geni_id"],
                                  "our_label": m["label"], "our_birth": b, "our_death": d,
                                  "dist": m["dist_charlemagne"], "searched": term,
                                  "qid": got[0]["id"]})
                    break

    print(f"{len(found)} candidates; fetching the full items", flush=True)
    items = full_items(r["qid"] for r in found)
    for r in found:
        it = items.get(r["qid"], {})
        r.update({"wd_label": it.get("label", ""), "wd_description": it.get("description", ""),
                  "instance_of_human": "yes" if it.get("human") else "no",
                  "instance_of": it.get("instance_of", ""),
                  "wd_birth": it.get("birth", ""), "wd_death": it.get("death", ""),
                  "wd_p2600": it.get("p2600", "")})

    fields = ["cut", "rank", "geni_id", "our_label", "our_birth", "our_death", "dist",
              "searched", "qid", "wd_label", "wd_description", "instance_of_human",
              "instance_of", "wd_birth", "wd_death", "wd_p2600"]
    tmp = OUT.with_suffix(".tsv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        # Total sort key: a person can appear once per cut, and the Geni id is the primary key.
        w.writerows(sorted(found, key=lambda r: (r["cut"], r["rank"], r["geni_id"])))
    os.replace(tmp, OUT)
    humans = sum(1 for r in found if r.get("instance_of_human") == "yes")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(found)} candidates, {humans} are humans")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
