"""What each drifted Geni id named in each committed version of the tree (queue item: items whose Geni profile
turned into another person; Emma 2026-10-05: a versioning problem, FamilySearch decides).

Reads `reports/geni-identity-drift.csv` (kinds "different person" and "different given name ..."), then one
committed `reports/derived-labels.csv.gz` per day from git history (each tree rebuild committed one; all local),
and the creation label and date from `reports/garborg-qids.tsv`. Writes
`reports/geni-drift-versions-2026-10-08.csv`: per item, the name on each date, and the date it first changed.
Read-only; touches nothing on Wikidata.

    python scripts/session-2026-10-08/drift-versions.py
"""
import csv, gzip, io, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KINDS = ("different person", "different given name, shared surname or patronymic")
OUT = ROOT / "reports" / "geni-drift-versions-2026-10-08.csv"


def main():
    rows = [r for r in csv.DictReader(open(ROOT / "reports" / "geni-identity-drift.csv", encoding="utf-8"))
            if r["kind"] in KINDS]
    ids = {r["geni_id"] for r in rows}
    created = {}
    for r in csv.DictReader(open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8"), delimiter="\t"):
        if r["geni_id"] in ids:
            created[r["geni_id"]] = (r["created"], r["label"])
    log = subprocess.run(["git", "log", "--format=%h %ad", "--date=short", "--", "reports/derived-labels.csv.gz"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    per_day = {}
    for line in log:
        if line.strip():
            h, d = line.split()
            per_day.setdefault(d, h)          # newest commit of each day (log is newest first)
    days = sorted(per_day)
    names = {g: {} for g in ids}
    for d in days:
        blob = subprocess.run(["git", "show", f"{per_day[d]}:reports/derived-labels.csv.gz"], cwd=ROOT,
                              capture_output=True, check=True).stdout
        for r in csv.DictReader(io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(blob)), encoding="utf-8")):
            if r["geni_id"] in ids:
                names[r["geni_id"]][d] = r["label_mul"] or r["label_en"]
        print(d, sum(1 for g in ids if d in names[g]), "of", len(ids), flush=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "geni_id", "kind", "created", "label_at_creation", "first_changed", "history"])
        for r in sorted(rows, key=lambda r: r["qid"]):
            g = r["geni_id"]
            c_date, c_label = created.get(g, ("", r["label_at_creation"]))
            hist, prev, first = [], None, ""
            for d in days:
                n = names[g].get(d, "(absent)")
                if n != prev:
                    hist.append(f"{d}: {n}")
                    if prev is not None and not first and d >= (c_date or ""):
                        first = d
                    prev = n
            w.writerow([r["qid"], g, r["kind"], c_date, c_label, first, " | ".join(hist)])
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
