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

Writes `reports/wikidata-id-backfill.qs`. `--refilter` re-applies `guard` to that file alone.
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


def guard():
    """`excluded(qid, prop, value) -> reason or ""`: the lines this batch must never write.

    Found on the first build, 2026-10-02: a FamilySearch person rendered on a Geni xref carries a
    placeholder `FS…` id, which is not a Geni profile; and the ledger's entry-point rows name items
    the account never identified, Tanba and Izumo clan items among them, which are blocked.
    """
    import tanba_batch_block
    import wikidata_lockout
    blocked = set(tanba_batch_block.tanba_blocked_qids()) | set(wikidata_lockout.NEVER_EDIT)
    entry_points = set()
    with open(LEDGER, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            if (row.get("note") or "").startswith("entry point"):
                entry_points.add((row.get("qid") or "").strip())
    removed = set()
    for path in sorted((REPO / "reports").glob("*.qs")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.split(TAB)
            if len(parts) >= 3 and parts[0].startswith("-Q"):
                removed.add((parts[0][1:], parts[1], parts[2].strip('"')))
    for name in ("removed-statements.tsv", "suppressed-statements.tsv"):
        path = REPO / "reports" / name
        if path.exists():
            with open(path, encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh, delimiter=TAB):
                    removed.add((row["qid"], row["property"], row["value"]))

    def excluded(q, prop, val):
        if prop == "P2600" and not val.isdigit():
            return "P2600 value is a FamilySearch placeholder, not a Geni id"
        if q in blocked:
            return "item is blocked (Tanba or NEVER_EDIT)"
        if wikidata_lockout.touches_protected(f"{q}	{prop}	\"{val}\""):
            return "protected item or profile"
        if (q, prop, val) in removed:
            return "a removal of this exact statement is on record"
        if prop == "P2600" and q in entry_points:
            return "entry-point row of the ledger, not an identification"
        return ""
    return excluded


def fs_names():
    """`{FamilySearch id: NAME}` from the raw downloads in `gedcom/familysearch/`, first seen wins."""
    out = {}
    for path in sorted((REPO / "gedcom" / "familysearch").glob("*.ged")):
        name = None
        with open(path, encoding="utf-8-sig", errors="replace") as fh:
            for line in fh:
                if line.startswith("0 "):
                    name = None
                elif line.startswith("1 NAME ") and name is None:
                    name = line[7:].strip().replace("/", " ")
                elif line.startswith("1 _FSFTID ") and name:
                    out.setdefault(line[10:].strip(), " ".join(name.split()))
    return out


def _first(name):
    import unicodedata
    toks = [t for t in re.split(r"[\s,.'\"„“]+", name or "") if t]
    if not toks:
        return ""
    s = unicodedata.normalize("NFKD", toks[0].casefold())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def first_names_agree(a, b):
    """The 2026-10-01 removal test: the first given names agree (one a prefix of the other)."""
    x, y = _first(a), _first(b)
    if len(x) < 2 or len(y) < 2:
        return False
    return x == y or (min(len(x), len(y)) >= 3 and (x.startswith(y) or y.startswith(x)))


def name_check():
    """Drop every line whose source name and the item's live label disagree on the first name.

    Found on the first build, 2026-10-02: `Q618605` Höfða-Þórður Bjarnarson was given Geni
    `Sæmundur suðureyski` through a FamilySearch pairing the zipper made on a birth year alone
    (402 of the 654 `P2889` lines are such `date` pairings). The 2026-10-01 removals were exactly
    this case, so the same test runs before the batch: Geni's display name for `P2600`, the
    FamilySearch download's name for `P2889`, each against the item's `mul`/`en` label and aliases.
    An id with no name to compare is dropped too.
    """
    fsn = fs_names()
    lines = OUT.read_text(encoding="utf-8").split(NL)
    items = sorted({l.split(TAB)[0] for l in lines if l.startswith("Q")}, key=lambda q: int(q[1:]))
    labels = {}
    for k in range(0, len(items), 50):
        data = api_get({"action": "wbgetentities", "format": "json", "props": "labels|aliases",
                        "languages": "mul|en", "ids": "|".join(items[k:k + 50])}, AGENT)
        for q, ent in (data.get("entities") or {}).items():
            names = [v.get("value", "") for v in (ent.get("labels") or {}).values()]
            for al in (ent.get("aliases") or {}).values():
                names += [a.get("value", "") for a in al]
            labels[q] = names
    keep, counts, dropped = [], collections.Counter(), []
    for line in lines:
        parts = line.split(TAB)
        if len(parts) >= 3 and parts[0].startswith("Q"):
            q, prop, val = parts[0], parts[1], parts[2].strip('"')
            source = (parts[4].strip('"') if prop == "P2600" and len(parts) >= 5
                      else fsn.get(val, "") if prop == "P2889" else "")
            if not source:
                counts[f"{prop}: no source name to compare"] += 1
                dropped.append((q, prop, val, "", "; ".join(labels.get(q, []))))
                continue
            if not any(first_names_agree(source, n) for n in labels.get(q, [])):
                counts[f"{prop}: first name differs"] += 1
                dropped.append((q, prop, val, source, "; ".join(labels.get(q, []))))
                continue
        keep.append(line)
    OUT.write_text(NL.join(keep), encoding="utf-8", newline=NL)
    with open(REPO / "reports" / "id-backfill-name-dropped.tsv", "w", encoding="utf-8",
              newline=NL) as fh:
        fh.write(TAB.join(("qid", "property", "value", "source_name", "item_names")) + NL)
        for row in dropped:
            fh.write(TAB.join(row) + NL)
    for k, v in sorted(counts.items()):
        print(f"   dropped, {k}: {v:,}")
    print(f"{sum(1 for l in keep if l.startswith('Q')):,} lines left in {OUT.relative_to(REPO)}")


def refilter():
    """Apply `guard` to the written batch without reading Wikidata again."""
    excluded = guard()
    lines = OUT.read_text(encoding="utf-8").split(NL)
    keep, counts = [], collections.Counter()
    for line in lines:
        parts = line.split(TAB)
        if len(parts) >= 3 and parts[0].startswith("Q"):
            why = excluded(parts[0], parts[1], parts[2].strip('"'))
            if why:
                counts[why] += 1
                continue
        keep.append(line)
    OUT.write_text(NL.join(keep), encoding="utf-8", newline=NL)
    for k, v in sorted(counts.items()):
        print(f"   dropped, {k}: {v:,}")
    print(f"{sum(1 for l in keep if l.startswith('Q')):,} lines left in {OUT.relative_to(REPO)}")
    name_check()
    return 0


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
    excluded = guard()
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
                elif excluded(q, prop, val):
                    counts[excluded(q, prop, val)] += 1
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
    name_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(refilter() if "--refilter" in sys.argv else main())
