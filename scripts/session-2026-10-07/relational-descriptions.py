"""Relationship-phrase descriptions on items this account created (queue item "Existing-item errors").

Emma, 2026-09-30: "get rid of all relational things from descriptions. It's Geni ID, its
occupation, or its birth to death." The creation path obeys that since then; items made before
it still carry `son of …`, `father of …`, `Jacob, son of …`. This lists every item the account
created, reads its `en` description, and for each relationship phrase writes the description the
creation ladder gives today (`build-garborg-day.life_description`, then the occupation, then
`Geni <id>`), computed by the day builder's own functions.

Writes `reports/relational-descriptions-2026-10-07.csv` and the batch
`reports/relational-descriptions-fix-2026-10-07.qs`. Sends nothing.

    python scripts/session-2026-10-07/relational-descriptions.py
"""
import csv
import importlib.util
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
API = "https://www.wikidata.org/w/api.php"
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
CSV_OUT = ROOT / "reports" / "relational-descriptions-2026-10-07.csv"
QS_OUT = ROOT / "reports" / "relational-descriptions-fix-2026-10-07.qs"
RELATIONAL = re.compile(r"\b(son|daughter|child|father|mother|parent|wife|husband|spouse|"
                        r"brother|sister|sibling|widow|widower)\s+of\b", re.I)


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(8):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception:
            time.sleep(15 * (i + 1))
    raise SystemExit("API failed: " + url)


def created():
    qids, cont = [], {}
    while True:
        d = get({"action": "query", "list": "usercontribs", "ucuser": "日巫女", "ucshow": "new",
                 "ucnamespace": 0, "uclimit": 500, "ucprop": "title", "format": "json", **cont})
        qids += [c["title"] for c in d["query"]["usercontribs"]]
        if "continue" not in d:
            return qids
        cont = {"uccontinue": d["continue"]["uccontinue"], "continue": d["continue"]["continue"]}


def main():
    qids = created()
    print(len(qids), "items created by the account", flush=True)
    hits = {}
    for i in range(0, len(qids), 50):
        d = get({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]),
                 "props": "descriptions|labels|claims", "languages": "en|mul", "format": "json"})
        for q, e in d.get("entities", {}).items():
            desc = ((e.get("descriptions") or {}).get("en") or {}).get("value", "")
            if desc and RELATIONAL.search(desc):
                geni = [(c["mainsnak"].get("datavalue") or {}).get("value")
                        for c in (e.get("claims") or {}).get("P2600", [])]
                label = ((e.get("labels") or {}).get("en") or (e.get("labels") or {}).get("mul") or {}).get("value", "")
                hits[q] = (desc, label, [g for g in geni if g])
        time.sleep(0.5)
    print(len(hits), "relational descriptions", flush=True)

    spec = importlib.util.spec_from_file_location("gday", ROOT / "scripts" / "build-garborg-day.py")
    G = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(G)
    want = {g for _d, _l, gs in hits.values() for g in gs}
    facts, places = {}, {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in want:
                facts[r["geni_id"]] = r
    with open(ROOT / "reports" / "derived-places.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in want:
                places[r["geni_id"]] = r

    rows, lines = [], ["# Replace relationship-phrase descriptions on items this account created (Emma 2026-09-30:",
                       "# Geni id, occupation, or birth to death). Ladder computed by build-garborg-day. Run with Run."]
    for q, (desc, label, geni) in sorted(hits.items()):
        g = geni[0] if geni else ""
        new, rung = "", ""
        f = facts.get(g)
        if f:
            new = G.life_description(f, places.get(g)) or ""
            rung = "life" if new else ""
            if not new:
                occ = ((f.get("occupations") or "").split(" | ")[0]).strip()
                if occ and occ.casefold() not in {"unknown", "ukjent", "okänd", "?", "nn"}:
                    en = G.occupation_of(occ)[1] or (occ if G.is_latin_text(occ) else "")
                    new = en[:G.DESC_MAX].rstrip(" -,")
                    rung = "occupation" if new else ""
        if not new and g:
            new, rung = f"Geni {g}", "geni"
        if new and new.casefold() == label.casefold():
            new, rung = (f"Geni {g}", "geni") if g else ("", "")
        rows.append((q, label, desc, g, rung, new))
        if new:
            lines.append(f'{q}\tDen\t"{G.qs(new)}"')
    with open(CSV_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "label", "description", "geni_id", "new_rung", "new_description"])
        w.writerows(rows)
    QS_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    import collections
    print(collections.Counter(r[4] for r in rows), "->", CSV_OUT.name, QS_OUT.name)


if __name__ == "__main__":
    main()
