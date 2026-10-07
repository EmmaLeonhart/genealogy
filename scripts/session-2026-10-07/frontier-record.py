"""Append session verdicts for frontier cases to reports/session-2026-10-07/ancestor-frontier-verdicts.tsv.
Usage: python scripts/session-2026-10-07/frontier-record.py VERDICTS.json  ({"n": [[fs_id, verdict, reason], ...]})"""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
rows = [r for r in csv.DictReader(open(ROOT / "reports" / "owner-ancestor-frontier.csv", encoding="utf-8"))
        if r["fs_parent_candidates"]]
out = ROOT / "reports" / "session-2026-10-07" / "ancestor-frontier-verdicts.tsv"
new = not out.exists()
v = json.load(open(sys.argv[1], encoding="utf-8"))
with open(out, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    if new:
        w.writerow(["n", "geni_id", "name", "fs_id", "verdict", "reason"])
    for n, items in sorted(v.items(), key=lambda kv: int(kv[0])):
        r = rows[int(n)]
        cands = [c.strip() for c in r["fs_parent_candidates"].split(";")]
        for fs, verdict, reason in items:
            assert fs in cands, (n, fs, cands)
            w.writerow([n, r["geni_id"], r["name"], fs, verdict, reason])
print("recorded", sum(len(x) for x in v.values()), "verdicts for", len(v), "cases")
