"""Read one drift case in full: the live item (labels, aliases, every statement with labels), our tree's current row for
its Geni id (name, sex, parents, spouses, children), and named FamilySearch records from our downloads (name, sex, dates,
parents, spouses, children). Read-only.

    python scripts/session-2026-10-08/drift-look.py QID GENI_ID [FSID ...]
"""
import csv, importlib.util, json, sys, urllib.request
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}


def get(ids):
    u = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&languages=mul|en&props=labels|aliases|claims|descriptions&ids=" + "|".join(ids)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))["entities"]


def lab(e):
    l = e.get("labels") or {}
    return (l.get("mul") or l.get("en") or {}).get("value", "")


def main():
    q, g, fsids = sys.argv[1], sys.argv[2], sys.argv[3:]
    e = get([q])[q]
    print(f"== {q} {lab(e)} | {e.get('descriptions', {}).get('en', {}).get('value')} | aliases",
          [a["value"] for a in e.get("aliases", {}).get("mul", [])])
    refs = []
    for p, cs in e["claims"].items():
        for c in cs:
            v = c["mainsnak"].get("datavalue", {}).get("value")
            if isinstance(v, dict) and "id" in v:
                refs.append(v["id"])
    names = {k: lab(v) for k, v in get(sorted(set(refs))[:50]).items()} if refs else {}
    for p, cs in e["claims"].items():
        out = []
        for c in cs:
            v = c["mainsnak"].get("datavalue", {}).get("value")
            out.append(f"{v['id']} {names.get(v['id'], '')}" if isinstance(v, dict) and "id" in v else
                       (v.get("time") if isinstance(v, dict) and "time" in v else v))
        print("  ", p, out)
    sp = lambda s: [x.strip() for x in (s or "").split("|") if x.strip()]
    fam = {}
    for r in csv.DictReader(open(ROOT / "reports" / "derived-family.csv", encoding="utf-8")):
        fam[r["geni_id"]] = r
    row = fam.get(g, {})
    want = {g} | set(sp(row.get("fathers"))) | set(sp(row.get("mothers"))) | set(sp(row.get("spouses"))) | set(sp(row.get("children")))
    labs, sex = {}, {}
    for r in csv.DictReader(open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8")):
        if r["geni_id"] in want:
            labs[r["geni_id"]] = r["label_mul"] or r["label_en"]
    for r in csv.DictReader(open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8")):
        if r["geni_id"] == g:
            sex[g] = (r.get("sex"), r.get("birth_date_raw"), r.get("death_date_raw"))
    n = lambda ids: [f"{x} {labs.get(x, '')}" for x in ids]
    print(f"== tree {g} {labs.get(g)} {sex.get(g)}")
    for k in ("fathers", "mothers", "spouses", "children"):
        print("  ", k, n(sp(row.get(k))))
    if fsids:
        spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
        fsday = importlib.util.module_from_spec(spec); spec.loader.exec_module(fsday)
        people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
        by = {}
        for k, rec in people.items():
            by.setdefault(rec["fs_id"], k)
        nm = lambda k: (((people.get(k) or {}).get("names") or [("", "")])[0][0].replace("/", "").strip() + " " +
                        (people.get(k) or {}).get("fs_id", "")) if k else ""
        for f in fsids:
            k = by.get(f)
            if not k:
                print("== FS", f, "not in our downloads"); continue
            rec = people[k]
            print(f"== FS {nm(k)} sex {rec.get('sex')} {rec.get('birth_date', '')} - {rec.get('death_date', '')}")
            print("   father", nm(father.get(k)), "| mother", nm(mother.get(k)))
            print("   spouses", [nm(x) for x in sorted(spouses.get(k, ()))])
            print("   children", [nm(x) for x in sorted(children.get(k, ()))])


if __name__ == "__main__":
    main()
