# Reads the raw FamilySearch downloads into {fs_id: name, birth, death, parents, spouses, children}.
# Lists records only; decides nothing. Keyed on _FSFTID, never on the file's own counter.
import glob, json, re, collections
def parse(path):
    recs, fams, cur, tag1 = {}, {}, None, None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"(\d+) (@[^@]+@ )?(\S+) ?(.*)", line.rstrip("\n"))
        if not m: continue
        lvl, xref, tag, val = int(m.group(1)), (m.group(2) or "").strip(), m.group(3), m.group(4)
        if lvl == 0:
            cur = None
            if tag == "INDI": cur = recs.setdefault(xref, {"x": xref, "fams": [], "famc": []}); kind = "I"
            elif tag == "FAM": cur = fams.setdefault(xref, {"h": None, "w": None, "c": []}); kind = "F"
            continue
        if cur is None: continue
        if lvl == 1: tag1 = tag
        if kind == "I":
            if lvl == 1 and tag == "NAME" and "n" not in cur: cur["n"] = val.replace("/", "").strip()
            elif lvl == 1 and tag == "_FSFTID": cur["fs"] = val.strip()
            elif lvl == 1 and tag == "SEX": cur["sex"] = val.strip()
            elif lvl == 1 and tag == "FAMS": cur["fams"].append(val.strip())
            elif lvl == 1 and tag == "FAMC": cur["famc"].append(val.strip())
            elif lvl == 2 and tag == "DATE" and tag1 in ("BIRT", "DEAT"): cur.setdefault(tag1, val.strip())
        else:
            if lvl == 1 and tag == "HUSB": cur["h"] = val.strip()
            elif lvl == 1 and tag == "WIFE": cur["w"] = val.strip()
            elif lvl == 1 and tag == "CHIL": cur["c"].append(val.strip())
    out = {}
    for r in recs.values():
        if "fs" not in r: continue
        nm = lambda x: recs.get(x, {}).get("n", "")
        f = [nm(fams[x]["h"]) for x in r["famc"] if x in fams and fams[x]["h"]]
        m = [nm(fams[x]["w"]) for x in r["famc"] if x in fams and fams[x]["w"]]
        s = [nm(fams[x]["w"] if fams[x]["h"] == r["x"] else fams[x]["h"]) for x in r["fams"] if x in fams and (fams[x]["h"] or fams[x]["w"])]
        c = [nm(k) for x in r["fams"] if x in fams for k in fams[x]["c"]]
        out[r["fs"]] = {"n": r.get("n", ""), "b": r.get("BIRT", ""), "d": r.get("DEAT", ""), "f": f, "m": m, "s": s, "c": c[:6]}
    return out
allr = {}
for p in sorted(glob.glob("gedcom/familysearch/*.ged")):
    for k, v in parse(p).items(): allr.setdefault(k, v)
json.dump(allr, open("reports/session-2026-10-04/familysearch-records.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(allr), "FamilySearch persons")
