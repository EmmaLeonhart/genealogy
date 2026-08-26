"""Rebuild the ledger from Emma's Wikidata account, which is the only thing that knows.

    BOT_CONTACT=you@example.com python scripts/refresh-garborg-ledger.py

**Emma, 2026-08-25:** *"you fuckin look at wikidata exactly as I told you"*, then
*"just look at my fucki nprofile"*, then the URL, then *"fuckin use my account as a guide"* —
after a batch offered to create five people of whom three already had items.

`CLAUDE.md` already said this and the ledger was being maintained by hand anyway:
*"`reports/garborg-qids.tsv` is the ledger of who has one. It is filled from **Emma's Wikidata
contributions**, not from a bulk download — her instruction: 'You should be looking at my
contributions to see the new ones I've created.'"* Nothing automated it, so it drifted, and
**11 of her items were missing from it** when this was first run.

**Her account is `日巫女`.** `Special:Contributions` is the authority for what she has made;
`list=usercontribs` is one request per 500 edits.

## Two sources, because neither alone is enough

* **Her contributions** give everything she created or edited — 49 created, 59 touched. This is
  the guide she named.
* **A live `P2600` lookup** catches items she did *not* make. `Q138474188` *Hans Syvertsen
  Nyvold* is the worked example: it carries the Geni id of a Garborg-line person because
  **an IP added it by accident** (her words, 2026-08-25), so it appears in no contribution list
  of hers and would still have been duplicated. `scripts/build-garborg-day.py` runs that check
  as a pre-flight before every `CREATE`.

## What was wrong before, so it is not re-attempted

Three offline sources were being trusted and all three are snapshots taken before she started
creating: the hand-maintained ledger, `out/wikidata/p2600-all.tsv` from the bulk download, and
`out/wikidata/relations.tsv` behind the parent-`P40` duplicate guard.

**Git history is NOT a substitute and was briefly tried.** Emma: *"idk why the fuck you decided
it was gonna be okay to use git history."* She is right — `git log -S` over `reports/*.qs` records
what a batch **offered**, which is not what exists. An offer she declined would block a real
person forever, and an item she made by hand outside any batch would be invisible.

Merges into `reports/garborg-qids.tsv` rather than overwriting: rows already there keep their
`label` and `note` columns, which carry hand-written provenance.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
API = "https://www.wikidata.org/w/api.php"
ACCOUNT = "日巫女"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"


def agent():
    contact = os.environ.get("BOT_CONTACT", "").strip()
    if not contact:
        sys.exit("BOT_CONTACT is not set. Wikimedia answers an empty User-Agent with a bare "
                 "403, so this fails loudly rather than mysteriously.")
    return f"geni-merge/1.0 ({contact})"


def get(params, ua):
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=90) as fh:
        return json.load(fh)


def main():
    ua = agent()
    contribs, cont = [], None
    while True:
        p = {"action": "query", "list": "usercontribs", "ucuser": ACCOUNT,
             "uclimit": "500", "ucnamespace": "0",
             "ucprop": "title|timestamp|comment|flags", "format": "json"}
        if cont:
            p["uccontinue"] = cont
        data = get(p, ua)
        contribs += data["query"]["usercontribs"]
        cont = data.get("continue", {}).get("uccontinue")
        if not cont:
            break
    created = {c["title"] for c in contribs if "new" in c}
    touched = sorted({c["title"] for c in contribs})
    print(f"{len(contribs)} mainspace edits by {ACCOUNT}; "
          f"{len(created)} items created, {len(touched)} touched")

    # Every touched item, not only the created ones: she adds a P2600 to items other
    # people made, and that correspondence is just as load-bearing.
    found = {}
    for i in range(0, len(touched), 50):
        batch = touched[i:i + 50]
        data = get({"action": "wbgetentities", "ids": "|".join(batch),
                    "props": "claims|labels", "languages": "en|mul|no|nb",
                    "format": "json"}, ua)
        for qid, ent in data.get("entities", {}).items():
            if "missing" in ent:
                continue
            claims = ent.get("claims", {})
            gs = [st["mainsnak"].get("datavalue", {}).get("value")
                  for st in claims.get("P2600", []) if st.get("rank") != "deprecated"]
            labels = ent.get("labels", {})
            label = (labels.get("en") or labels.get("mul") or labels.get("no")
                     or labels.get("nb") or {}).get("value", "")
            for g in [g for g in gs if isinstance(g, str)]:
                found[g] = (qid, label, qid in created)

    rows = {}
    if LEDGER.exists():
        with open(LEDGER, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                rows[row["geni_id"]] = row

    added, changed = [], []
    for g, (qid, label, was_created) in sorted(found.items()):
        old = rows.get(g)
        if old is None:
            rows[g] = {"geni_id": g, "qid": qid, "label": label,
                       "created": "2026-08-25",
                       "note": f"from {ACCOUNT} contributions"
                               + ("" if was_created else " (P2600 added to an existing item)")}
            added.append((g, qid, label))
        elif old["qid"] != qid:
            changed.append((g, old["qid"], qid))

    with open(LEDGER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["geni_id", "qid", "label", "created", "note"],
                           delimiter="\t")
        w.writeheader()
        for g in sorted(rows):
            r = rows[g]
            w.writerow({k: r.get(k, "") for k in
                        ("geni_id", "qid", "label", "created", "note")})

    print(f"\n{len(added)} added to the ledger:")
    for g, qid, label in added:
        print(f"   {g}  {qid}  {label}")
    if changed:
        print(f"\n{len(changed)} DISAGREE with what the ledger held - not overwritten:")
        for g, a, b in changed:
            print(f"   {g}  ledger={a}  live={b}")
    print(f"\n{len(rows)} rows in {LEDGER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
