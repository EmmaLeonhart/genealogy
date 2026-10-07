"""Both sides of each open ancestor slot, for the session's case-by-case verdicts (queue item: zipper-merge Emma's
own ancestry). Reads `reports/owner-ancestor-frontier.csv` rows that have a FamilySearch parent candidate.

    python scripts/session-2026-10-07/frontier-show.py FROM TO

One line per case: n, the Geni ancestor (name, dates, spouses, children) || each FamilySearch candidate (same).
"""
import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))


def cases():
    rows = [r for r in csv.DictReader(open(ROOT / "reports" / "owner-ancestor-frontier.csv", encoding="utf-8"))
            if r["fs_parent_candidates"]]
    return rows


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    rows = cases()[a:b]
    gids = {r["geni_id"] for r in rows}
    fam, lab, facts = {}, {}, {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in gids:
                fam[r["geni_id"]] = r
    want = set(gids)
    for r in fam.values():
        for c in ("spouses", "children", "father", "mother"):
            want |= {x.strip() for x in (r.get(c) or "").split("|") if x.strip()}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in want:
                lab[r["geni_id"]] = r["label_mul"] or r["label_en"]
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in gids:
                facts[r["geni_id"]] = r
    spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
    fsday = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fsday)
    people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    by_fs = {}
    for key, rec in people.items():
        by_fs.setdefault(rec["fs_id"], key)

    def names(ids, n=3):
        return "/".join((lab.get(x, x) or x)[:24] for x in ids[:n])

    def fsname(k):
        return ((people.get(k) or {}).get("names") or [("?", "")])[0][0].replace("/", "").strip()[:26]

    for i, r in enumerate(rows, start=a):
        g = r["geni_id"]
        fr, fa = fam.get(g, {}), facts.get(g, {})
        sp = [x.strip() for x in (fr.get("spouses") or "").split("|") if x.strip()]
        ch = [x.strip() for x in (fr.get("children") or "").split("|") if x.strip()]
        left = (f"{r['name']} [{fa.get('birth_date_raw', '')}-{fa.get('death_date_raw', '')}] "
                f"s:{names(sp)} c:{names(ch)}")
        rights = []
        for fid in r["fs_parent_candidates"].split(";"):
            k = by_fs.get(fid.strip())
            if not k:
                rights.append(f"{fid}:(not in corpus)")
                continue
            rec = people[k]
            rights.append(f"{fid} {fsname(k)} [{rec.get('birth_date', '')}-{rec.get('death_date', '')}] "
                          f"s:{'/'.join(fsname(x) for x in sorted(spouses.get(k, ()))[:3])} "
                          f"c:{'/'.join(fsname(x) for x in sorted(children.get(k, ()))[:3])}")
        print(f"{i}: [{r['why_unpaired'][:22]}] child {r['paired_child_name'][:22]} || {left}  ||  "
              + "  ||  ".join(rights))


if __name__ == "__main__":
    main()
