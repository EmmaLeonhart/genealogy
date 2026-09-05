"""Does Wikidata actually HOLD items for the eccentric clusters? Ask it.

**Emma, 2026-09-05, on the first version of `reports/eccentric-clusters.md`:** *"your measurement
of there being qids is a bit flawed. Both Chinese lines likely have wiki data items even if no
connection. Pre dynastic Egypt definitely does… Axum certainly have qids lol… Third intermediate
period def has qids lol"*. And: *"Idk if you even bothered cross-checking wikidata p2600
properties linking to these lol"*.

**The `P2600` count was right and the sentence attached to it was wrong.** `P2600` *Geni.com
profile ID* counts a **link**: somebody having joined a Geni profile to a Wikidata item. A cluster
reading `0` is unlinked, and the report said *"every other cluster is 0"* as though that settled
whether Wikidata has the people. `CLAUDE.md` § *"Is X present?"* is the standing rule and this
broke it: an absence has to name the store it is about, and ours is a Geni-shaped slice.

**So this asks Wikidata itself**, by name, via `wbsearchentities`. Egress is blocked in the
sandbox and ordinary in Actions, so it runs there — `.github/workflows/check-cluster-items.yml`.

**⛔ A HIT IS A CANDIDATE, NEVER AN IDENTIFICATION, and this file must not become an input to a
merge.** `CLAUDE.md` deleted the `reconcile` name matcher for searching Wikidata *for* a name, and
that stays deleted. The difference is what the answer is used for: this one exists to replace the
sentence *"Wikidata does not have these people"* with a measurement, and it is read by a human.
Nothing joins on it. `Solomon King of Israel` matching `Q302` is a plausibility check on a
cluster, not a claim about that Geni profile.

**Only Latin-script labels are searched.** A Geni CJK label is usually a generational string —
`禄 (入闽始祖晋安郡王) 林 第1世闽南林氏衍派` — that no Wikidata label resembles, so a miss would
measure the label format rather than Wikidata's holdings. Those clusters get `not-searchable`,
which is an honest third answer and not a zero.

Writes `reports/eccentric-cluster-wikidata-check.tsv`.
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
MEMBERS = ROOT / "reports" / "eccentric-cluster-members.tsv"
OUT = ROOT / "reports" / "eccentric-cluster-wikidata-check.tsv"

API = "https://www.wikidata.org/w/api.php"
UA = ("genimerge/1.0 (https://github.com/EmmaLeonhart/genealogy; emma@topazcomputing.com)")

#: The cut to check. 100 is where the report's distinct populations separate: below it the
#: clusters merge back into the bulk, above it they only shrink.
CUT = 100

#: Names searched per cluster. A sample, not a census -- the question is whether the population
#: is on Wikidata at all, and twelve settles that without asking for a thousand requests.
SAMPLE = 12

#: Seconds between requests. `CLAUDE.md` § *Querying Wikidata is ALLOWED* -- *"Be polite about
#: the rate"*, and `wbsearchentities` takes one name per call, so the politeness is the gap.
PAUSE = 0.25

#: Geni's redaction markers and our own placeholder text: not names, so never searched.
NOT_A_NAME = re.compile(r"^\(|^NN\b|^Private$", re.I)

LATIN = re.compile(r"^[\W\d_]*[A-Za-z]")


def searchable(label: str) -> bool:
    """A label worth putting to `wbsearchentities`.

    Latin script, not a redaction marker, and more than a bare initial. A Geni generational
    string in Han characters is excluded on purpose: see the module docstring.
    """
    label = label.strip()
    if not label or NOT_A_NAME.match(label) or not LATIN.match(label):
        return False
    return len(label) >= 4


def search(term: str):
    """Top `wbsearchentities` hits for one term, or `None` if the request failed."""
    url = API + "?" + urllib.parse.urlencode({
        "action": "wbsearchentities", "search": term, "language": "en",
        "uselang": "en", "type": "item", "limit": "3", "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            return json.loads(fh.read().decode("utf-8")).get("search", [])
    except Exception as exc:                       # noqa: BLE001 - reported, never swallowed
        print(f"    ! {term!r}: {exc}", file=sys.stderr, flush=True)
        return None


def main() -> int:
    if not MEMBERS.exists():
        sys.exit(f"missing {MEMBERS.relative_to(ROOT)} -- run scripts/eccentric-clusters.py")

    by_cluster = collections.defaultdict(list)
    with open(MEMBERS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if int(row["cut"]) == CUT:
                by_cluster[int(row["rank"])].append(row)

    # `or "20"`, not a `get` default: an unset workflow input arrives as an EMPTY string,
    # not as an absent variable, so the default never fired and `int("")` killed the run.
    limit = int((os.environ.get("CLUSTERS") or "20").strip())
    ranks = sorted(by_cluster)[:limit]
    print(f"cut {CUT}: checking {len(ranks)} clusters of {len(by_cluster)}", flush=True)

    rows = []
    for rank in ranks:
        members = sorted(by_cluster[rank], key=lambda r: (-int(r["dist_charlemagne"]),
                                                          r["geni_id"]))
        pool = [m for m in members if searchable(m["label"])][:SAMPLE]
        print(f"  cluster {rank}: {len(members):,} people, {len(pool)} searchable names",
              flush=True)
        if not pool:
            rows.append({"cut": CUT, "rank": rank, "people": len(members),
                         "searched": 0, "with_hit": 0, "verdict": "not-searchable",
                         "examples": ""})
            continue
        hits, examples, failed = 0, [], 0
        for m in pool:
            found = search(m["label"])
            time.sleep(PAUSE)
            if found is None:
                failed += 1
                continue
            if found:
                hits += 1
                top = found[0]
                examples.append(f"{m['label']} -> {top['id']} {top.get('label', '')}"
                                f" ({top.get('description', '')})".strip())
        searched = len(pool) - failed
        verdict = ("request-failed" if searched == 0
                   else "items exist" if hits * 2 >= searched
                   else "some items" if hits else "no hit by name")
        print(f"    {hits}/{searched} named members match an item -- {verdict}", flush=True)
        rows.append({"cut": CUT, "rank": rank, "people": len(members),
                     "searched": searched, "with_hit": hits, "verdict": verdict,
                     # Sorted so the column is a pure function of its input.
                     "examples": " | ".join(sorted(examples)[:5])})

    fields = ["cut", "rank", "people", "searched", "with_hit", "verdict", "examples"]
    tmp = OUT.with_suffix(".tsv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        # Total sort key: (cut, rank) is unique per row.
        w.writerows(sorted(rows, key=lambda r: (r["cut"], r["rank"])))
    os.replace(tmp, OUT)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
