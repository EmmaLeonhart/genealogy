"""Genealogy 6, third pass: two Wikidata items in the store that are one person.

    python scripts/entity-resolution-store-duplicates.py [YYYY-MM-DD]

Reads every human (P31 Q5) in the local item store (wikidata/items/*.jsonl.gz) and pairs two items when all of these
hold: two different QIDs; the same name (mul or en label, case- and accent-folded); a birth year or a death year
known on both and equal, and no known year contradicting; and at least one shared relative in the same role (the same
QID as father on both, or mother, spouse or child). Where either item has a Chinese, Japanese or Korean label, both
must have the same one: romanization folds different characters into one spelling (the "Zhao Shi" daughters of
Emperor Huizong). The same role is what keeps a father and his namesake son apart:
the son's mother is the father's wife, a shared QID in two different roles. Same name and same years alone is not enough (a parish of Anna Andersdotters); the shared
relative is what makes it one family's person. Items whose Geni or FamilySearch ids disagree (each carries an id the
other does not, of the same property) are written but marked, since two ids can be two records of one person or two
people.

Writes reports/entity-resolution-store-duplicates-<date>.tsv (the evidence) and a .qs of MERGE lines (newer into
older, QuickStatements v1) for Emma to review and run. Nothing is sent from here.
"""
from __future__ import annotations

import collections
import csv
import datetime
import glob
import gzip
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
KIN = {"P22": "father", "P25": "mother", "P26": "spouse", "P40": "child"}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.casefold())
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).split())


def vals(claims, prop):
    out = []
    for c in claims.get(prop, []):
        dv = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(dv, dict) and "id" in dv:
            out.append(dv["id"])
        elif isinstance(dv, dict) and "time" in dv:
            try:
                out.append(int(dv["time"][:5].replace("+", "")) if dv["time"][0] == "+" else -int(dv["time"][1:5]))
            except ValueError:
                pass
        elif isinstance(dv, str):
            out.append(dv)
    return out


people = {}
by_key = collections.defaultdict(list)
shards = sorted(glob.glob(str(ROOT / "wikidata" / "items" / "*.jsonl.gz")))
for n, path in enumerate(shards, 1):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            cl = d.get("claims") or {}
            if "Q5" not in vals(cl, "P31"):
                continue
            lab = d.get("labels") or {}
            name = (lab.get("mul") or lab.get("en") or {}).get("value", "")
            if not name or fold(name) in ("nn", "private", "unknown"):
                continue
            q = d["id"]
            b, de = vals(cl, "P569"), vals(cl, "P570")
            rels = {(p, v) for p in KIN for v in vals(cl, p)}
            if q in people:
                continue
            cjk = next((lab[k]["value"] for k in ("zh", "zh-hant", "zh-hans", "ja", "ko") if k in lab), "")
            people[q] = {"name": name, "cjk": cjk, "b": b[0] if b else None, "d": de[0] if de else None, "rels": rels,
                         "geni": set(vals(cl, "P2600")), "fs": set(vals(cl, "P2889"))}
            by_key[fold(name)].append(q)
    if n % 250 == 0:
        print(f"  {n}/{len(shards)} shards, {len(people):,} people", flush=True)

pairs, seen = [], set()
for key, qs in by_key.items():
    if len(qs) < 2 or len(qs) > 200:
        continue
    for i, a in enumerate(qs):
        for b in qs[i + 1:]:
            A, B = people[a], people[b]
            if a == b:
                continue
            # pinyin and romaji fold different characters into one spelling: a Sinosphere name must match in script
            if (A["cjk"] or B["cjk"]) and A["cjk"] != B["cjk"]:
                continue
            # a year known on BOTH sides must agree; one side's birth against the other's death proves nothing
            if not ((A["b"] is not None and A["b"] == B["b"]) or (A["d"] is not None and A["d"] == B["d"])):
                continue
            if A["b"] is not None and B["b"] is not None and A["b"] != B["b"]:
                continue
            if A["d"] is not None and B["d"] is not None and A["d"] != B["d"]:
                continue
            shared = sorted({v for _, v in A["rels"] & B["rels"]} - {a, b})   # same relative in the same role
            if not shared:
                continue
            clash = bool(A["geni"] - B["geni"] and B["geni"] - A["geni"]) or bool(A["fs"] - B["fs"] and B["fs"] - A["fs"])
            old, new = sorted((a, b), key=lambda q: int(q[1:]))
            if (old, new) in seen:
                continue
            seen.add((old, new))
            pairs.append({"older": old, "newer": new, "name": A["name"], "born": A["b"] or B["b"] or "",
                          "died": A["d"] or B["d"] or "", "shared_relatives": " ".join(shared),
                          "geni_older": " ".join(sorted(people[old]["geni"])), "geni_newer": " ".join(sorted(people[new]["geni"])),
                          "fs_older": " ".join(sorted(people[old]["fs"])), "fs_newer": " ".join(sorted(people[new]["fs"])),
                          "ids_disagree": "yes" if clash else ""})

pairs.sort(key=lambda r: (int(r["older"][1:]), int(r["newer"][1:])))
rep = ROOT / "reports"
tsv = rep / f"entity-resolution-store-duplicates-{DAY}.tsv"
with open(tsv, "w", encoding="utf-8", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=list(pairs[0]) if pairs else ["older"], delimiter="\t")
    w.writeheader()
    w.writerows(pairs)
qs = ["# Genealogy 6, third pass: same name, same birth and death years, and a shared father/mother/spouse/child.",
      "# MERGE newer into older. Review before running; drop any line that is not one person.",
      "# Lines whose Geni or FamilySearch ids disagree are commented out: check them by hand first."]
for r in pairs:
    line = f"MERGE\t{r['newer']}\t{r['older']}"
    qs.append(("# ids disagree: " + line) if r["ids_disagree"] else line)
(rep / f"entity-resolution-store-duplicates-{DAY}.qs").write_text("\n".join(qs) + "\n", encoding="utf-8", newline="\n")
print(f"{len(people):,} people read from {len(shards):,} shards; {len(pairs):,} pairs "
      f"({sum(1 for r in pairs if r['ids_disagree'])} with disagreeing ids) -> {tsv.relative_to(ROOT)}")
