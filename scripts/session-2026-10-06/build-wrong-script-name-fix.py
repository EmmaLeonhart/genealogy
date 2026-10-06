"""Fix batch for the wrong-script `P735` links on our items (queue item "Fix the wrong-script name links").

For every live link in `reports/name-links-wrong-script-live-2026-10-06.tsv` whose token is in
`reports/wrong-script-name-links.tsv`, and that the account added (or that came with our creation, no separate
edit, on an item the account created): remove the wrong item and add the Latin-script one, unless the item already holds it. Links added by
other editors are left alone, and protected items are skipped. Re-checks each item live first.
Writes `reports/wrong-script-name-fix-2026-10-06.qs`.

    python scripts/session-2026-10-06/build-wrong-script-name-fix.py
"""
import csv, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import wikidata_lockout  # noqa: E402

UA = {"User-Agent": "genealogy-audit (https://github.com/EmmaLeonhart/genealogy)"}
fix = {(r["token"], r["wrong_qid"]): r["qid"] for r in
       csv.DictReader(open(ROOT / "reports/wrong-script-name-links.tsv", encoding="utf-8"), delimiter="\t")}
links = [r for r in csv.DictReader(open(ROOT / "reports/name-links-wrong-script-live-2026-10-06.tsv",
                                        encoding="utf-8"), delimiter="\t")
         if (r["token"], r["linked_qid"]) in fix and r["property"] == "P735"]
def creator(qid):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "prop": "revisions", "titles": qid, "rvlimit": "1", "rvdir": "newer",
         "rvprop": "user", "format": "json"})
    data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
    return list(data["query"]["pages"].values())[0]["revisions"][0]["user"]


# No separate edit added the link: ours only when the account created the item (the link came with it).
mine = [r for r in links if r["added_by"] == "日巫女"
        or (r["added_by"] == "" and creator(r["item"]) == "日巫女")]
others = [r for r in links if r not in mine]

live = {}
items = sorted({r["item"] for r in mine})
for i in range(0, len(items), 50):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbgetentities", "ids": "|".join(items[i:i + 50]), "props": "claims", "format": "json"})
    data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
    for q, e in data.get("entities", {}).items():
        live[q] = {c["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                   for c in e.get("claims", {}).get("P735", [])}
    time.sleep(0.5)

out, skipped = [], []
for r in sorted(mine, key=lambda r: int(r["item"][1:])):
    q, wrong, right = r["item"], r["linked_qid"], fix[(r["token"], r["linked_qid"])]
    held = live.get(q, set())
    line = f"-{q}|P735|{wrong}"
    if wrong not in held:
        skipped.append((q, "wrong link no longer live"))
        continue
    if wikidata_lockout.touches_protected(line.replace("|", "\t")):
        skipped.append((q, "protected"))
        continue
    out.append(line)
    if right not in held:
        out.append(f"{q}|P735|{right}")
(ROOT / "reports/wrong-script-name-fix-2026-10-06.qs").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"{len(links)} live links on overlaid tokens: {len(mine)} ours, {len(others)} by other editors (left alone)")
print(f"{sum(1 for l in out if l.startswith('-'))} removals, {sum(1 for l in out if not l.startswith('-'))} additions; "
      f"skipped {len(skipped)}: {skipped[:5]}")
for r in others:
    print("  other editor:", r["item"], r["token"], r["added_by"], r["added_at"])
