"""Every Latin-script token in `reports/name-item-plan.csv` that links to an existing item, checked live:
the item's `mul` label, its `en` label and its writing system (`P282`). Writes the links whose item is not
Latin-script to `reports/name-links-wrong-script-2026-10-06.tsv` (queue item "Analyze the Daniel name links").

    python scripts/session-2026-10-06/name-links-script-check.py
"""
import csv, json, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-audit (https://github.com/EmmaLeonhart/genealogy)"}
LATIN_ALPHABET = "Q8229"


def script_of(s):
    for ch in s or "":
        if ch.isalpha():
            return unicodedata.name(ch, "?").split()[0]
    return ""


plan = [r for r in csv.DictReader(open(ROOT / "reports/name-item-plan.csv", encoding="utf-8"))
        if r["existing_qid"] and r["script"] == "Latin"]
qids = sorted({r["existing_qid"] for r in plan})
info = {}
for i in range(0, len(qids), 50):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "labels|claims",
         "languages": "mul|en", "format": "json"})
    for _ in range(3):
        try:
            data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
            break
        except Exception:                                            # noqa: BLE001
            time.sleep(5)
    for q, e in data.get("entities", {}).items():
        labels = e.get("labels", {})
        p282 = [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                for c in e.get("claims", {}).get("P282", [])]
        info[q] = (labels.get("mul", {}).get("value", ""), labels.get("en", {}).get("value", ""), p282,
                   (e.get("redirects") or {}).get("to", ""))
    time.sleep(0.5)

rows = []
for r in plan:
    mul, en, p282, redirect = info.get(r["existing_qid"], ("", "", [], ""))
    s = script_of(mul)
    if (mul and s != "LATIN") or (p282 and LATIN_ALPHABET not in p282):
        rows.append([r["token"], r["usage"], r["bearers"], r["existing_qid"], mul, en, s,
                     ",".join(filter(None, p282))])
rows.sort(key=lambda x: -int(x[2]))
out = ROOT / "reports" / "name-links-wrong-script-2026-10-06.tsv"
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("token\tusage\tbearers\tlinked_qid\tmul\ten\tmul_script\tP282\n")
    for x in rows:
        f.write("\t".join(map(str, x)) + "\n")
print(f"{len(plan)} Latin links over {len(qids)} items fetched ({len(info)} returned); "
      f"{len(rows)} link to a non-Latin item, {sum(int(x[2]) for x in rows)} bearers -> {out.name}")
