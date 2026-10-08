"""Part 2 of the Geni-drift item: what FamilySearch says each of the 58 drifted items is.

For each row of `reports/geni-drift-versions-2026-10-08.csv`: the live Wikidata item (mul/en label, every `P2889`
FamilySearch id, `P22`/`P25` labels), and for each `P2889` the FamilySearch person in our own downloads
(`gedcom/familysearch/`, read by `build-familysearch-day.read_corpus`): name, dates, father, mother. Writes
`reports/geni-drift-familysearch-2026-10-08.csv`. Read-only.

    python scripts/session-2026-10-08/drift-familysearch.py
"""
import csv, importlib.util, json, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
OUT = ROOT / "reports" / "geni-drift-familysearch-2026-10-08.csv"


def get(ids, props):
    u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&languages=mul|en&props=" + props
         + "&ids=" + "|".join(ids))
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))["entities"]
        except Exception:
            time.sleep(10 * (i + 1))
    raise SystemExit("API failed")


def lab(e):
    l = e.get("labels") or {}
    return (l.get("mul") or l.get("en") or {}).get("value", "")


def main():
    rows = list(csv.DictReader(open(ROOT / "reports" / "geni-drift-versions-2026-10-08.csv", encoding="utf-8")))
    ents = {}
    for i in range(0, len(rows), 50):
        ents.update(get([r["qid"] for r in rows[i:i + 50]], "labels|claims"))
    val = lambda e, p: [c["mainsnak"]["datavalue"]["value"] for c in (e.get("claims") or {}).get(p, [])
                        if "datavalue" in c["mainsnak"]]
    par = sorted({v["id"] for e in ents.values() for p in ("P22", "P25") for v in val(e, p)})
    plab = {}
    for i in range(0, len(par), 50):
        plab.update({k: lab(v) for k, v in get(par[i:i + 50], "labels").items()})
    spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
    fsday = importlib.util.module_from_spec(spec); spec.loader.exec_module(fsday)
    people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    by_fs = {}
    for k, rec in people.items():
        by_fs.setdefault(rec["fs_id"], k)
    nm = lambda k: ((people.get(k) or {}).get("names") or [("", "")])[0][0].replace("/", "").strip() if k else ""
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "label_live", "p22_live", "p25_live", "label_at_creation", "geni_history",
                    "fs_id", "fs_name", "fs_dates", "fs_father", "fs_mother"])
        for r in rows:
            e = ents.get(r["qid"], {})
            if "redirects" in e or "missing" in e or not e.get("claims"):
                w.writerow([r["qid"], "(redirect or missing)", "", "", r["label_at_creation"], r["history"],
                            "", "", "", "", ""]); continue
            base = [r["qid"], lab(e), "; ".join(plab.get(v["id"], v["id"]) for v in val(e, "P22")),
                    "; ".join(plab.get(v["id"], v["id"]) for v in val(e, "P25")), r["label_at_creation"], r["history"]]
            fsids = val(e, "P2889")
            if not fsids:
                w.writerow(base + ["", "(no P2889 on the item)", "", "", ""]); continue
            for fid in fsids:
                k = by_fs.get(fid)
                if not k:
                    w.writerow(base + [fid, "(not in our FamilySearch downloads)", "", "", ""]); continue
                rec = people[k]
                w.writerow(base + [fid, nm(k), f"{rec.get('birth_date', '')} - {rec.get('death_date', '')}",
                                   nm(father.get(k)), nm(mother.get(k))])
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
