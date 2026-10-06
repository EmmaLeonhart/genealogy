"""Links from batch ebec37585 (reports/zipper-links-batch-ebec37585.csv) whose zipper pair is not among the 1,261
reviewed pairs (reports/session-2026-10-04/zipper-pairs-behind-wikidata-links.json), with their live state.
Writes reports/zipper-ebec-unreviewed-2026-10-06.csv."""
import csv, json, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-zipper-check/1.0 (emma@topazcomputing.com)"}
reviewed = json.dumps(json.load(open(ROOT / "reports/session-2026-10-04/zipper-pairs-behind-wikidata-links.json",
                                    encoding="utf-8")), ensure_ascii=False)
rows = [r for r in csv.DictReader(open(ROOT / "reports/zipper-links-batch-ebec37585.csv", encoding="utf-8"))
        if f'"{r["zipper_qid"]}"' not in reviewed]
ids = sorted({r["subject"] for r in rows} | {r["value"] for r in rows})
ents = {}
for i in range(0, len(ids), 50):
    u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|labels|info&ids="
         + "|".join(ids[i:i + 50]))
    ents.update(json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["entities"])
    time.sleep(1)
def label(q):
    l = ents.get(q, {}).get("labels", {})
    return (l.get("en") or l.get("mul") or l.get("ja") or {}).get("value", "")
out = []
for r in rows:
    e = ents.get(r["subject"], {})
    vals = [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
            for c in e.get("claims", {}).get(r["property"], [])]
    tgt = ents.get(r["value"], {})
    out.append({**r, "subject_now": e.get("id", ""), "value_now": tgt.get("id", ""),
                "value_label": label(r["value"]),
                "live": "yes" if r["value"] in vals or tgt.get("id") in vals else "no"})
with open(ROOT / "reports/zipper-ebec-unreviewed-2026-10-06.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out:
    print(" | ".join(o[k] for k in ("subject", "subject_label", "property", "value", "value_label", "band",
                                   "our_person", "their_person", "live", "subject_now", "value_now")))
