"""Live labels with a doubled patronymic on items this account created (the "Duplicated patronymics" item).

Lists every item the account created (usercontribs, new pages), reads each one's live `mul`/`en`
label, and writes the ones where a patronymic stands twice in a row (`Marta Monsdatter
Monsdatter`) to `reports/doubled-patronymic-live-2026-10-07.csv`, with the label
`namemodel.drop_repeated_patronymic` gives. Read-only: nothing is sent.

    python scripts/session-2026-10-07/doubled-patronymic-live.py
"""
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from namemodel import drop_repeated_patronymic  # noqa: E402

API = "https://www.wikidata.org/w/api.php"
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
OUT = ROOT / "reports" / "doubled-patronymic-live-2026-10-07.csv"


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(8):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception:
            time.sleep(10 * (i + 1))
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
    print(len(qids), "items created by the account")
    rows = []
    for i in range(0, len(qids), 50):
        d = get({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "labels",
                 "languages": "mul|en", "format": "json"})
        for q, e in d.get("entities", {}).items():
            for lang, lab in (e.get("labels") or {}).items():
                fixed = drop_repeated_patronymic(lab["value"])
                if fixed != lab["value"]:
                    rows.append((q, lang, lab["value"], fixed))
        time.sleep(0.5)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "lang", "label", "without_the_repeat"])
        w.writerows(sorted(rows))
    print(len(rows), "labels,", len({r[0] for r in rows}), "items ->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
