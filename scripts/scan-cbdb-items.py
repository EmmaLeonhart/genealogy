"""Every Wikidata item in the offline store whose ENGLISH description mentions CBDB.

Emma, 2026-09-10: *"cbdb people can all get their date last edited set to October 31, 2026 so
that we don't need to deal with their bullshit. This means every wikidata item with 'cbdb' in
its English description"*.

The match is on `descriptions.en` only, case-insensitively, and the whole matched description is
written out beside the QID so the population can be read rather than trusted.
"""
import glob
import gzip
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path("reports/cbdb-items.tsv")


def main() -> int:
    shards = sorted(glob.glob("wikidata/items/items-*.jsonl.gz"))
    rows = []
    seen = 0
    for n, shard in enumerate(shards):
        with gzip.open(shard, "rt", encoding="utf-8") as fh:
            for line in fh:
                seen += 1
                if "cbdb" not in line.lower():
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                d = (o.get("descriptions") or {}).get("en") or {}
                val = d.get("value") or ""
                if "cbdb" not in val.lower():
                    continue
                label = ((o.get("labels") or {}).get("en") or {}).get("value", "")
                # P2600 is the Geni profile id; carry it so the worklist join needs no second pass
                geni = ""
                for st in (o.get("claims") or {}).get("P2600", []):
                    try:
                        geni = st["mainsnak"]["datavalue"]["value"]
                        break
                    except Exception:
                        pass
                rows.append((o.get("id", ""), geni, label, val))
        if n % 200 == 0:
            print("shard %d/%d  lines=%d  hits=%d" % (n, len(shards), seen, len(rows)), flush=True)
    rows.sort()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("qid\tgeni_id\ten_label\ten_description\n")
        for r in rows:
            fh.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    with_geni = sum(1 for r in rows if r[1])
    print("DONE lines=%d  cbdb_items=%d  with_P2600=%d -> %s"
          % (seen, len(rows), with_geni, OUT), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
