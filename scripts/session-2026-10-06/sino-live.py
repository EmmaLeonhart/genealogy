"""Live state of the Sinosphere name statements this account added (reports/sinosphere-name-statements.csv)
and of the unlabelled family-name items it created on 2026-10-04. Writes reports/sinosphere-name-live-2026-10-06.csv."""
import csv, json, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-sinosphere-check/1.0 (emma@topazcomputing.com)"}

def entities(ids):
    out = {}
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 50):
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|labels|info&ids="
               + "|".join(ids[i:i+50]))
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as r:
            out.update(json.load(r)["entities"])
        time.sleep(1)
    return out

rows = [r for r in csv.DictReader(open(ROOT / "reports/sinosphere-name-statements.csv", encoding="utf-8"))
        if r["source"] != "not ours"]
junk = sorted({r["value"] for r in rows if not r["value_en"] and not r["value_ja"]})
ents = entities([r["qid"] for r in rows] + junk)
out = []
for r in rows:
    e = ents.get(r["qid"], {})
    if "redirects" in e or e.get("redirects"):
        state = "redirect"
    claims = e.get("claims", {}).get(r["property"], [])
    hit = [c for c in claims if c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") == r["value"]]
    out.append({"qid": r["qid"], "ja": r["ja"], "property": r["property"], "value": r["value"],
                "value_en": r["value_en"], "value_ja": r["value_ja"], "source": r["source"],
                "live": "yes" if hit else "no", "statement_ids": " ".join(c["id"] for c in hit),
                "item_redirect_to": e.get("redirects", {}).get("to", "") if isinstance(e.get("redirects"), dict) else ""})
with open(ROOT / "reports/sinosphere-name-live-2026-10-06.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for q in junk:
    e = ents.get(q, {})
    print(q, "labels:", {k: v["value"] for k, v in e.get("labels", {}).items()},
          "claims:", {p: [c["mainsnak"].get("datavalue", {}).get("value") for c in cs] for p, cs in e.get("claims", {}).items()})
print(sum(o["live"] == "yes" for o in out), "of", len(out), "still live")
