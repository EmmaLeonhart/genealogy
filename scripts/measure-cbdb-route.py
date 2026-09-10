"""Is there a route into the CBDB people that does not go through Geni?

Emma, 2026-09-10, on `Zhu Jingze` 朱敬則 `Q8073795`: *"I found the route into cbdb stuff. These
people highly documented."* The Geni side is a dead end and that is settled — the profiles are
managed by `CBDB (China Biographical Database)`, carry no `Add Family` link and are not editable,
which is why 54,164 of them were parked at `2026-10-31`. The article she opened is the other
direction: an English Wikipedia biography naming the man's prefecture, his cousins, his
associates and his career, with a Wikidata link in its own header.

**Parking them and this route are not in conflict.** `last_attempted` governs what the *collector*
opens in a browser, and nothing here changes that. This asks a different question: how many of
them are reachable from the Wikidata side at all, and how many already carry the family
statements the campaign wants.

The four numbers, over the population `scripts/scan-cbdb-items.py` found:

    enwiki          a sitelink to English Wikipedia -- a documented person
    family          any of P22 father / P25 mother / P40 child / P3373 sibling ALREADY on the item
    addressable     an enwiki article and NO family statements yet -- the actual opportunity
    P2600           a Geni id, which is what puts them in the worklist in the first place

⛔ This MEASURES and writes a CSV. It changes nothing, edits nothing, and queues nothing --
`CLAUDE.md` § *"Analyse this" means: build a CSV of every instance*.
"""

from __future__ import annotations

import csv
import glob
import gzip
import json
import pathlib

OUT = pathlib.Path("reports/cbdb-route.tsv")
CBDB = pathlib.Path("reports/cbdb-items.tsv")
FAMILY = ("P22", "P25", "P40", "P3373")


def main() -> int:
    want = {}
    with CBDB.open(encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd)
        for row in rd:
            if row:
                want[row[0]] = row[1]          # qid -> geni_id ("" when absent)

    rows = []
    for shard in sorted(glob.glob("wikidata/items/items-*.jsonl.gz")):
        with gzip.open(shard, "rt", encoding="utf-8") as fh:
            for line in fh:
                # The prefilter is a plain substring: descriptions read "Tang dynasty person
                # CBDB = 27889", so cbdb sits MID-STRING. A '"cbdb' prefix matched 6 items of
                # 71,474 and looked like a finding.
                if 'cbdb' not in line.lower():
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                qid = o.get("id", "")
                if qid not in want:
                    continue
                claims = o.get("claims") or {}
                present = [p for p in FAMILY if claims.get(p)]
                sitelinks = o.get("sitelinks") or {}
                enwiki = "enwiki" in sitelinks
                zhwiki = "zhwiki" in sitelinks
                rows.append((
                    qid, want[qid],
                    ((o.get("labels") or {}).get("en") or {}).get("value", ""),
                    "yes" if enwiki else "no",
                    "yes" if zhwiki else "no",
                    ",".join(present),
                    str(len(sitelinks)),
                ))

    rows.sort()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("qid\tgeni_id\ten_label\tenwiki\tzhwiki\tfamily_properties\tsitelinks\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    n = len(rows)
    enwiki = sum(1 for r in rows if r[3] == "yes")
    zhwiki = sum(1 for r in rows if r[4] == "yes")
    anywiki = sum(1 for r in rows if r[3] == "yes" or r[4] == "yes")
    fam = sum(1 for r in rows if r[5])
    addressable = sum(1 for r in rows if (r[3] == "yes" or r[4] == "yes") and not r[5])
    geni = sum(1 for r in rows if r[1])
    print("cbdb items matched in the store: %d" % n)
    print("  with an English Wikipedia article : %6d  %4.1f%%" % (enwiki, 100.0 * enwiki / n))
    print("  with a Chinese Wikipedia article  : %6d  %4.1f%%" % (zhwiki, 100.0 * zhwiki / n))
    print("  with either                       : %6d  %4.1f%%" % (anywiki, 100.0 * anywiki / n))
    print("  ALREADY carrying P22/P25/P40/P3373: %6d  %4.1f%%" % (fam, 100.0 * fam / n))
    print("  ADDRESSABLE (an article, no family): %6d  %4.1f%%"
          % (addressable, 100.0 * addressable / n))
    print("  carrying a Geni id (P2600)        : %6d  %4.1f%%" % (geni, 100.0 * geni / n))
    print("-> %s" % OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
