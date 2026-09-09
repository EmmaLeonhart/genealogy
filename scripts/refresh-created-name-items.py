"""The name items Emma has ALREADY created, so the generator stops re-creating them.

    python scripts/refresh-created-name-items.py

**The bug this closes, 2026-08-30.** `namemodel.store_name_item` resolves a token against
`out/wikidata/name-items-in-store.tsv.gz` — the offline Wikidata download. A name item created
**today** is not in that download, and the Garborg ledger tracks *people* (it is keyed on
`P2600`, which a name item does not have). So a token created in one run was invisible to the
next, and `CREATE` in QuickStatements always mints a new item rather than checking.

Emma ran the same regenerated file three times. The result, measured over all 581 items she has
created: **29 name items under 18 distinct labels, 10 of those labels created more than once** —
`Jonsdatter` three times. Another editor, `OBender12`, merged all eleven duplicates away and
stripped the `P734` links pointing at the losers.

It is not only patronymics: `Gennäs`, `Morlanda` and `Sør-Reime` are family names.

**Why the PEOPLE were safe and the name items were not.** A created person carries a `P2600`, so
`refresh-garborg-ledger.py` finds them in her contributions and the batch never re-proposes them.
A name item has no Geni id and no such anchor. Exactly one person slipped through — Anna
Andersdotter, `Q141199706` and `Q141199819`, same `P2600` ten minutes apart — and that is a
different fault from this one.

## What this reads

`Special:Contributions/日巫女` filtered to page **creations**, then `wbgetentities` in batches of
50 to keep only the items that are `instance of` a name class. Redirects are followed, so an item
already merged away resolves to its survivor and the survivor is what gets recorded — which is
the right answer, because that is the item a future run should link to.

Writes `reports/created-name-items.tsv`: `label`, `kind`, `qid`, `created`.
"""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import _http_fetch, require_agent  # noqa: E402

OUT = ROOT / "reports" / "created-name-items.tsv"
USER = "日巫女"

#: `P31` value -> the usage a person links to it with. Same table as `namemodel`.
KIND = {"Q101352": "family", "Q202444": "given", "Q12308941": "given",
        "Q11879590": "given", "Q3409032": "given", "Q110874": "patronymic"}


def created_pages(ua):
    out, cont = [], None
    for _ in range(40):
        url = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=usercontribs"
               "&ucuser=" + urllib.parse.quote(USER) +
               "&ucshow=new&uclimit=500&ucnamespace=0&ucprop=ids|title|timestamp")
        if cont:
            url += "&uccontinue=" + urllib.parse.quote(cont)
        data = json.loads(_http_fetch(url, headers=ua))
        out += [(c["title"], c["timestamp"])
                for c in data.get("query", {}).get("usercontribs", [])]
        cont = data.get("continue", {}).get("uccontinue")
        if not cont:
            break
        time.sleep(0.3)
    return out


def main():
    ua = {"User-Agent": require_agent()}
    pages = created_pages(ua)
    when = dict(pages)
    ids = [q for q, _t in pages]
    print(f"{len(ids)} items created by {USER}")

    rows, seen = [], set()
    for i in range(0, len(ids), 50):
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
               "&redirects=yes&props=labels|claims&languages=mul|en&ids="
               + "|".join(ids[i:i + 50]))
        data = json.loads(_http_fetch(url, headers=ua))
        for asked, item in (data.get("entities") or {}).items():
            if "missing" in item:
                continue
            p31 = {s["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                   for s in item.get("claims", {}).get("P31", [])}
            kinds = sorted({KIND[q] for q in p31 if q in KIND})
            if not kinds:
                continue
            labels = item.get("labels", {})
            label = (labels.get("mul") or labels.get("en") or {}).get("value", "")
            # The SURVIVOR, not the id we asked for: a merged duplicate resolves to the item
            # a future run should link to.
            qid = item.get("id", asked)
            for kind in kinds:
                if (label.casefold(), kind) in seen or not label:
                    continue
                seen.add((label.casefold(), kind))
                rows.append({"label": label, "kind": kind, "qid": qid,
                             "created": when.get(asked, "")[:10]})
        time.sleep(0.3)

    rows.sort(key=lambda r: (r["kind"], r["label"].casefold()))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["label", "kind", "qid", "created"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} distinct name items already created "
          f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
