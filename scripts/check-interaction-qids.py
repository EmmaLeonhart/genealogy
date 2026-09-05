"""For every item in Emma's interaction log: is it a redirect, and how old is it?

Answers the one question the log alone cannot: **which side of each merge was ours.**
`reports/created-name-items.tsv` records `Tunheim -> Q36927172` as an item created on
2026-08-27, but the log shows OBender12 merging *our* `Q141189029` into a `Q36927172`
that already existed. The ledger absorbed the redirect, so our own record of the event
now names the survivor and the duplicate has vanished from it.

The first revision timestamp settles it: an item created years before 2026-08-27 was not
created by us. `wbgetentities` carries no creation date, so that comes from
`prop=revisions&rvdir=newer&rvlimit=1`, and redirect status from `redirects=no`.

Live network, batched 50 ids a request --- `CLAUDE.md` § *Querying Wikidata is ALLOWED.
Be polite about the rate*.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge.wikidata import require_agent  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "reports" / "wikidata-interactions.csv"
OUT = ROOT / "reports" / "wikidata-interaction-qids.csv"
API = "https://www.wikidata.org/w/api.php"

EXTRA = ["Q141267933"]  # her own pointer: "this person had a weird error"


def get(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": require_agent()})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.loads(fh.read().decode("utf-8"))


def batched(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def main() -> int:
    qids: list[str] = []
    seen: set[str] = set()
    with LOG.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for q in [row["qid"], *row["other_qids"].split(";")]:
                if q and q not in seen:
                    seen.add(q)
                    qids.append(q)
    for q in EXTRA:
        if q not in seen:
            seen.add(q)
            qids.append(q)
    qids.sort(key=lambda q: int(q[1:]))

    info: dict[str, dict] = {q: {"qid": q} for q in qids}

    for batch in batched(qids, 50):
        data = get(
            {
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "props": "labels|descriptions|claims",
                "languages": "en|mul|ja|zh|ko",
                "redirects": "no",
                "format": "json",
                "formatversion": "2",
            }
        )
        for q, ent in (data.get("entities") or {}).items():
            rec = info.setdefault(q, {"qid": q})
            # `missing` arrives as an EMPTY STRING under formatversion=2, which is falsy
            # --- `ent.get("missing")` reports every redirect as present. With
            # `redirects=no` a redirected item is exactly what comes back this way, so
            # the whole redirect column read zero. Test for the key, never the value.
            if "missing" in ent:
                rec["missing"] = "1"
            labels = ent.get("labels") or {}
            rec["label_en"] = (labels.get("en") or {}).get("value", "")
            rec["label_mul"] = (labels.get("mul") or {}).get("value", "")
            claims = ent.get("claims") or {}
            rec["has_p2600"] = "1" if "P2600" in claims else "0"
            rec["has_p31"] = ";".join(
                sorted(
                    {
                        (c.get("mainsnak", {}).get("datavalue", {}).get("value", {}) or {}).get("id", "")
                        for c in claims.get("P31", [])
                    }
                    - {""}
                )
            )
            rec["n_claims"] = str(sum(len(v) for v in claims.values()))
        time.sleep(1)

    # First revision: the only thing that says who created the item.
    for batch in batched(qids, 20):
        data = get(
            {
                "action": "query",
                "prop": "revisions",
                "titles": "|".join(batch),
                "rvlimit": "1",
                "rvdir": "newer",
                "rvprop": "timestamp|user",
                "format": "json",
                "formatversion": "2",
            }
        )
        for page in (data.get("query") or {}).get("pages") or []:
            q = page.get("title", "")
            rec = info.setdefault(q, {"qid": q})
            revs = page.get("revisions") or []
            if revs:
                rec["created_at"] = revs[0].get("timestamp", "")
                rec["created_by"] = revs[0].get("user", "")
        time.sleep(1)

    fields = [
        "qid", "label_en", "label_mul", "created_at", "created_by",
        "redirect_to", "missing", "has_p2600", "has_p31", "n_claims",
    ]
    rows = [ {f: info[q].get(f, "") for f in fields} for q in qids ]
    tmp = OUT.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(OUT)
    print(f"{len(rows)} items -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
