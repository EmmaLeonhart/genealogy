"""One uncapped batch adding every Geni and FamilySearch id our data gives an item that lacks it.

    PYTHONPATH=src python scripts/build-id-backfill.py

Ruled 2026-10-02 (Emma): *"Ideally should get the id linked as soon as the relationship is linked
and right now everyone eligible for a geni or familysearch id to be added to them should have it
done in a rapid thing just the same as what we were doing earlier"* -- the earlier thing being
the `P2889` backfill of 2026-10-01 (`reports/wikidata-p2889-backfill.qs`).

**`P2889` FamilySearch person ID** goes on an item when its Geni id (the item's own `P2600`, or
the ledger's) is paired with a FamilySearch id by the zipper (`reports/familysearch-zipper-pairs.tsv`,
which since 2026-10-01 pairs no slot by position alone) or by the merged tree
(`derived-family-sources.csv`), and both readings agree.

**`P2600` Geni.com profile ID** goes on an item when the ledger names its Geni id, or when the
item's `P2889` is paired with a Geni id. It carries `P1810`, the name Geni displays, as every
`P2600` the pipeline writes does; a private or unknown-name marker gets no qualifier.

**Never written:** an id an item already states; an item that already holds a different id of
the same kind (that is a conflict for a person, not a gap); an id already on another item, which
would make a duplicate; and any pair Emma had removed (`reports/wikidata-p2889-removals.qs`).
The item's current claims are read live, just before the batch is written.

Writes `reports/wikidata-id-backfill.qs`.
"""

from __future__ import annotations

import collections
import csv
import gzip
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from live_name_items import _get as api_get  # noqa: E402

LEDGER = REPO / "reports" / "garborg-qids.tsv"
PAIRS = REPO / "reports" / "familysearch-zipper-pairs.tsv"
SOURCES = REPO / "reports" / "derived-family-sources.csv"
DISPLAY = REPO / "reports" / "display-names.csv"
P2600_ALL = REPO / "out" / "wikidata" / "p2600-all.tsv"
P2889_ALL = REPO / "out" / "wikidata" / "p2889-all.tsv"
REMOVALS = REPO / "reports" / "wikidata-p2889-removals.qs"
OUT = REPO / "reports" / "wikidata-id-backfill.qs"
AGENT = "geni-wikidata-id-backfill"
SPARQL = "https://query.wikidata.org/sparql"
TAB, NL = "\t", "\n"


def qs(value):
    return (value or "").replace('"', "").strip()


def roster(path):
    """`({id: {qid}}, {qid: {id}})` from a two-column roster."""
    by_id, by_q = collections.defaultdict(set), collections.defaultdict(set)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split(TAB)
            if len(parts) >= 2 and parts[0].startswith("Q"):
                by_id[parts[1]].add(parts[0])
                by_q[parts[0]].add(parts[1])
    return by_id, by_q


def live_p2889():
    """Every `P2889` on Wikidata now: the roster is a daily snapshot and the 2026-10-01 backfill
    landed after it."""
    query = "SELECT ?item ?id WHERE { ?item wdt:P2889 ?id }"
    url = SPARQL + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=300) as fh:
        rows = json.load(fh)["results"]["bindings"]
    by_id = collections.defaultdict(set)
    for r in rows:
        by_id[r["id"]["value"]].add(r["item"]["value"].rsplit("/", 1)[1])
    return by_id


def display_names():
    from labels import NARROW_MARKERS, WORDS_MEANING_UNKNOWN
    markers = NARROW_MARKERS | WORDS_MEANING_UNKNOWN
    out = {}
    path = DISPLAY if DISPLAY.exists() else None
    fh = (open(DISPLAY, encoding="utf-8", newline="") if path
          else io.TextIOWrapper(gzip.open(str(DISPLAY) + ".gz"), encoding="utf-8"))
    with fh:
        for row in csv.DictReader(fh):
            if row.get("name_index") not in ("0", ""):
                continue
            raw = row.get("display_name") or ""
            toks = re.sub(r"[-–]", " ", raw).split()
            if (not raw or "<private>" in raw.casefold() or raw.strip().casefold() == "private"
                    or any(t.casefold().strip(".,") in markers for t in toks)):
                continue
            out[row["geni_id"]] = raw
    return out


def main() -> int:
    csv.field_size_limit(1 << 30)
    geni_by_id, geni_by_q = roster(P2600_ALL)
    print("reading every P2889 on Wikidata ...")
    fs_by_id = live_p2889()
    print(f"   {sum(len(v) for v in fs_by_id.values()):,} P2889 statements live")

    ledger = []
    with open(LEDGER, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            q, g = (row.get("qid") or "").strip(), (row.get("geni_id") or "").strip()
            if q.startswith("Q") and g.isdigit():
                ledger.append((q, g))

    # Geni <-> FamilySearch, kept only where every reading agrees.
    g2f, f2g = collections.defaultdict(set), collections.defaultdict(set)
    with open(PAIRS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            g2f[row["geni_id"]].add(row["fs_id"])
            f2g[row["fs_id"]].add(row["geni_id"])
    with open(SOURCES, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["relation"] == "fs_id":
                g2f[row["geni_id"]].add(row["relative"])
                f2g[row["relative"]].add(row["geni_id"])
    one_g2f = {g: next(iter(f)) for g, f in g2f.items()
               if len(f) == 1 and len(f2g[next(iter(f))]) == 1}
    one_f2g = {f: g for g, f in one_g2f.items()}

    removed = set()
    if REMOVALS.exists():
        for line in REMOVALS.read_text(encoding="utf-8").splitlines():
            parts = line.split(TAB)
            if len(parts) >= 3 and parts[0].startswith("-Q"):
                removed.add((parts[0][1:], parts[2].strip('"')))

    # Who is which Geni id: the ledger, then the roster where an id is on one item only.
    item_geni = collections.defaultdict(set)
    for q, g in ledger:
        item_geni[q].add(g)
    for g, qids in geni_by_id.items():
        if len(qids) == 1:
            item_geni[next(iter(qids))].add(g)

    want = collections.defaultdict(set)  # qid -> {(prop, id)}
    counts = collections.Counter()
    for q, genis in item_geni.items():
        for g in genis:
            f = one_g2f.get(g)
            if f:
                want[q].add(("P2889", f))
    for q, g in ledger:
        want[q].add(("P2600", g))
    for f, qids in fs_by_id.items():
        g = one_f2g.get(f)
        if g and len(qids) == 1:
            want[next(iter(qids))].add(("P2600", g))

    # Drop what the snapshots already settle, then read the rest live.
    for q in list(want):
        for prop, val in list(want[q]):
            holders = (geni_by_id if prop == "P2600" else fs_by_id).get(val, set())
            if q in holders:
                want[q].discard((prop, val))
                counts[f"{prop} already on the item"] += 1
            elif holders:
                want[q].discard((prop, val))
                counts[f"{prop} already on another item"] += 1
            elif prop == "P2889" and (q, val) in removed:
                want[q].discard((prop, val))
                counts["P2889 removed by Emma's order"] += 1
        if not want[q]:
            del want[q]
    print(f"{len(want):,} items to read live")

    names = display_names()
    lines = []
    ids = sorted(want, key=lambda q: int(q[1:]))
    for k in range(0, len(ids), 50):
        chunk = ids[k:k + 50]
        data = api_get({"action": "wbgetentities", "format": "json", "props": "claims",
                        "ids": "|".join(chunk)}, AGENT)
        for q, ent in (data.get("entities") or {}).items():
            if "missing" in ent or "redirects" in ent:
                counts["item missing or redirected"] += len(want.get(q, ()))
                continue
            claims = ent.get("claims") or {}
            have = {p: {((s.get("mainsnak") or {}).get("datavalue") or {}).get("value")
                        for s in claims.get(p, [])} for p in ("P2600", "P2889")}
            for prop, val in sorted(want.get(q, ())):
                if val in have[prop]:
                    counts[f"{prop} already on the item"] += 1
                elif prop == "P2889" and have[prop]:
                    counts["P2889 item holds a different FamilySearch id"] += 1
                else:
                    qual = ""
                    if prop == "P2600" and names.get(val):
                        qual = f'{TAB}P1810{TAB}"{qs(names[val])}"'
                    lines.append(f'{q}{TAB}{prop}{TAB}"{val}"{qual}')
                    counts[f"written {prop}"] += 1
        if k % 2000 == 0:
            print(f"   read {k + len(chunk):,} of {len(ids):,}")

    header = [
        "# Geni (P2600, with P1810) and FamilySearch (P2889) ids on every item our data identifies",
        "# and that lacks them. Uncapped. Emma, 2026-10-02. Read live before writing.",
    ]
    OUT.write_text(NL.join(header + lines) + NL, encoding="utf-8", newline=NL)
    for key, n in sorted(counts.items()):
        print(f"   {key}: {n:,}")
    print(f"{len(lines):,} lines -> {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
