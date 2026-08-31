"""Are the spine's people actually LINKED on Wikidata, or merely present?

    python scripts/check-spine-bonds.py

**Emma, 2026-08-29**, told the Charlemagne line had only two people with no item at all:
*"is it really only 2 people missing connecting Arne to Charlemagne? Look over this because
it doesn't feel right, but if so great, if it is the case check with the bonds"*.

Item existence and chain continuity are different questions and the first was the one being
answered. A step whose item exists but carries no `P22`/`P25`/`P40`/`P26` to its neighbour is
a hole in the chain exactly as much as a step with no item.

**One batched `wbgetentities` request per 50 items**, via `genimerge.wikidata.full_entities` --
the pattern `CLAUDE.md` sanctions for deciding what to emit, and never a per-item lookup.
`out/wikidata/relations.tsv` is the offline store and cannot answer this: it was downloaded
2026-08-25 and 20 of these items were created after it.

Writes `reports/spine-bonds.tsv` -- one row per consecutive pair, with the property that joins
them or the reason none does.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from bot_identity import agent as _bot_agent  # noqa: E402
from genimerge.wikidata import WikidataClient  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

#: Default to the two spine paths; any path file may be named on the command line instead.
#: **The one live spine.** These defaulted to `charlemagne-to-arne-garborg` and
#: `bergitte-to-emma`, two of the four lines Emma declared legacy on 2026-08-30 after verifying
#: them complete. Checking bonds on a finished line reports nothing and reads as a clean run.
PATHS = tuple(sys.argv[1:]) or ("paths/arne-garborg-to-johannes-bureus-geni.tsv",)
#: The five that join two people. `P3373` sibling is here because a spine step can be a
#: sibling hop -- the path's `relation_to_previous` column says which, and we do not assume.
BONDS = ("P22", "P25", "P40", "P26", "P3373")


def steps(rel):
    rows = [l.rstrip("\n") for l in (ROOT / rel).open(encoding="utf-8")
            if not l.startswith("#") and l.strip()]
    hdr = rows[0].split("\t")
    out = []
    for line in rows[1:]:
        f = dict(zip(hdr, line.split("\t")))
        m = re.search(r"geni:(\d+)", f.get("note", ""))
        out.append((f.get("step", ""), f.get("name", ""),
                    m.group(1) if m else "", f.get("relation_to_previous", "")))
    return out


def qid_map():
    """geni id -> QID, from the ledger first and the bulk P2600 store second."""
    m = {}
    for line in (ROOT / "out/wikidata/p2600-all.tsv").open(encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2 and p[1]:
            m.setdefault(p[1], p[0])
    led = ROOT / "reports/garborg-qids.tsv"
    for r in csv.DictReader(led.open(encoding="utf-8"), delimiter="\t"):
        g, q = (r.get("geni_id") or "").strip(), (r.get("qid") or "").strip()
        if g and q:
            m[g] = q          # the ledger is fresher and wins
    return m


def main():
    ids = qid_map()
    wanted, plan = set(), {}
    for rel in PATHS:
        st = steps(rel)
        plan[rel] = st
        for _, _, g, _ in st:
            if ids.get(g):
                wanted.add(ids[g])

    if not _bot_agent():
        sys.exit("BOT_CONTACT is not set; Wikimedia answers an empty User-Agent with a bare 403")
    client = WikidataClient(ROOT / "out" / "wikidata" / "livecache")
    items = {}
    order = sorted(wanted)
    for i in range(0, len(order), 50):
        items.update(client.full_entities(order[i:i + 50]))
    print(f"fetched {len(items)} items in {(len(order) + 49) // 50} request(s)")

    def links(qid):
        """{other qid: [properties]} for every bond this item states."""
        out = {}
        for p, claims in (items.get(qid, {}).get("claims") or {}).items():
            if p not in BONDS:
                continue
            for c in claims:
                dv = (c.get("mainsnak") or {}).get("datavalue") or {}
                v = dv.get("value") or {}
                if isinstance(v, dict) and v.get("id"):
                    out.setdefault(v["id"], []).append(p)
        return out

    rows, broken = [], {}
    for rel, st in plan.items():
        broken[rel] = []
        for a, b in zip(st, st[1:]):
            qa, qb = ids.get(a[2], ""), ids.get(b[2], "")
            if not qa or not qb:
                why = "no item: " + " and ".join(
                    n for n, q in ((a[1], qa), (b[1], qb)) if not q)
                rows.append((rel, a[0], b[0], a[1], b[1], qa, qb, "", "", why))
                broken[rel].append((a[0], b[0], why))
                continue
            fwd = links(qa).get(qb, [])
            rev = links(qb).get(qa, [])
            state = "linked" if (fwd or rev) else "NO BOND"
            rows.append((rel, a[0], b[0], a[1], b[1], qa, qb,
                         ",".join(fwd), ",".join(rev), state))
            if state == "NO BOND":
                broken[rel].append((a[0], b[0], f"{qa} and {qb} state nothing about each other"))

    out = ROOT / "reports/spine-bonds.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "step_a", "step_b", "name_a", "name_b",
                    "qid_a", "qid_b", "a_to_b", "b_to_a", "state"])
        w.writerows(rows)
    print(f"wrote {out} -- {len(rows)} consecutive pairs")
    for rel in PATHS:
        bad = broken[rel]
        tot = len(plan[rel]) - 1
        print(f"\n{rel}: {tot - len(bad)} of {tot} pairs bonded")
        for sa, sb, why in bad:
            print(f"    steps {sa}-{sb}: {why}")


if __name__ == "__main__":
    main()
