"""How many items this account created still carry the MARRIED name as their label (existing-item errors item).

Emma, 2026-10-01: the birth name is the label for everyone, the married name an alias; the pipeline's
`_label_corrections` backfills established items at `LABEL_EDIT_CAP` a run. `Q141539011` Valborg
Pedersdatter Ueland (born Sandsmark) was one still waiting. This counts the rest: an item whose live
`mul` label equals the Geni given name + `_MARNM`, where `SURN` differs. Read-only.

    python scripts/session-2026-10-07/married-labels-live.py
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "https://www.wikidata.org/w/api.php"
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
OUT = ROOT / "reports" / "married-labels-live-2026-10-07.csv"


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
    live = {}
    for i in range(0, len(qids), 50):
        d = get({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "labels|claims",
                 "languages": "mul", "format": "json"})
        for q, e in d.get("entities", {}).items():
            lab = ((e.get("labels") or {}).get("mul") or {}).get("value", "")
            geni = [(c["mainsnak"].get("datavalue") or {}).get("value")
                    for c in (e.get("claims") or {}).get("P2600", [])]
            if lab and geni and geni[0]:
                live[geni[0]] = (q, lab)
        time.sleep(0.5)
    rows = []
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            g = r["geni_id"]
            if g not in live or r["name_index"] not in ("0", ""):
                continue
            givn, surn, marnm = (" ".join((r.get(k) or "").split()) for k in ("givn", "surn", "marnm"))
            if not (givn and surn and marnm) or surn.casefold() == marnm.casefold():
                continue
            q, lab = live[g]
            if lab.casefold() == f"{givn} {marnm}".casefold():
                rows.append((q, g, lab, f"{givn} {surn}"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "geni_id", "live_label", "birth_name"])
        w.writerows(sorted(rows))
    print(len(live), "creations with a Geni id;", len(rows), "still under the married name ->", OUT.name)


if __name__ == "__main__":
    main()
