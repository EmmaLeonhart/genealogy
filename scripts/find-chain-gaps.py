"""Who is missing from the relationship chains, ranked by how many slots they fill.

**This does not touch the merged tree, and that is the point.** Emma, 2026-08-17:
*"I didn't request that you rebuild the synoptic tree. You just did that on your own,
and I think that's kind of stupid… rebuilding the synoptic tree right now is just going
to create another tree that's going to become out of date pretty soon."*

She was right, and the cost was not only time: re-merging while she worked took the
machine to **0.3 GB free of 31.3 GB** and killed two background jobs. The chain question
never needed a merge. *Do we hold this person?* is answered by whether their Geni ID
appears as an `INDI` xref in any export, which is one pass over `exports/` and a set of
strings — **13 seconds against roughly five minutes and 4.5 GB**, and it cannot go stale
because it reads the corpus directly.

The merged tree is still the right instrument for questions about *structure* — who is
whose parent, which component somebody is in. It is the wrong one for presence.

### The ranking is slots, not midpointness — her call

Emma, 2026-08-17: *"can you force open the top 10 people for number of path slots they
fill? I was asking earlier for midpoints in path segments, but the issue with that is
that the midpoints for path segments were making some assumptions: an assumption of
relative equality of presence in slots, but I don't think this is true anymore."*

She is right about the assumption. Slot counts run from **10 down to 1** across the
missing people, so ranking by position-in-chain treated somebody blocking ten paths the
same as somebody blocking one. A **slot** is one appearance of one person on one saved
path, so a person on nine paths fills nine slots and closing them buys all nine.

**No already-opened filter.** Her rule, twice: the ranking drops a person by itself as
soon as an export covers them, so a filter can only exclude people who are *still* gaps.
`reports/midpoint-seeds-to-open.tsv` is overwritten every run and is the handoff for the
batch being opened now, never a history.

Writes `reports/chain-gaps.csv` (every missing person, every run) and
`reports/midpoint-seeds-to-open.tsv` (the top `--open` of them, with family-tree URLs —
**not** profile URLs, per `CLAUDE.md`).

    PYTHONPATH=src python scripts/find-chain-gaps.py --open 10
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

PATHS_DIR = REPO / "paths"
EXPORTS = REPO / "exports"
NAMES = REPO / "reports" / "path-bridge-targets.csv"
OUT_ALL = REPO / "reports" / "chain-gaps.csv"
OUT_OPEN = REPO / "reports" / "midpoint-seeds-to-open.tsv"

csv.field_size_limit(10 ** 7)

#: `0 @I6000000087535357291@ INDI` — the xref Geni writes, which `CLAUDE.md` records as
#: this repo's primary key. Read as bytes so a 30 MB export costs one read and no
#: decode; the IDs are ASCII digits whatever the rest of the file is.
INDI_XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)

#: Family-tree index, never the profile page. Emma, 2026-08-17: *"rather definitively
#: this kind of thing … is a better page to open up for them rather than the pages you
#: opened."* The profile shows one person; the index shows the neighbourhood she has to
#: work in to place a placeholder and run the export.
FAMILY_TREE_URL = "https://www.geni.com/family-tree/index/{}"

#: ---------------------------------------------------------------- ON HOLD
#: **Empty, and it should stay that way unless something is genuinely unreachable.**
#: Emma, 2026-08-17: *"put them on hold… I don't want you to throw them out in the sense
#: of just not using them at all, because I think we're able to get them. They just
#: require a slightly different strategy."*
#:
#: **Her bar, in her words:** *"the only situation where I'd be considering somebody to
#: be unreachable by our method would be if they have 32 ancestors, all of which have 32
#: ancestors, or if they themselves are a master profile and all of their ancestors are
#: master profiles."* Both are exhaustion conditions over a whole *walk*, not a property
#: of one screen.
#:
#: **What I did wrong, recorded because it is the failure mode she named.** I put James
#: IV, Margaret of Denmark, Francis II and Lorenzo II de' Medici here after looking at
#: the four generations the tree index renders, seeing a green `+N` badge on every box,
#: and calling the tree saturated. That is not a measurement of reachability — it is not
#: having walked deeper. `docs/export-seed-rules.md` § *When the whole visible tree is
#: saturated* says the next move is to follow those counts into a **smaller** ancestor
#: tree, preferring small odd numbers, and insert there. I skipped that step on all four.
#: Emma: *"you're dismissing them prematurely because it's very common that you dismiss
#: tasks prematurely… You just didn't push the depth far enough to actually do it."*
#:
#: **A master profile is not an unworkable person.** It cannot be edited from this
#: account, but the walk does not stop at it, and its neighbours are usually ordinary.
#:
#: **Never a heuristic.** Not an ancestor count on one screen, not a title in the name,
#: and **not "they have a Wikidata item"** — that last one was checked rather than
#: assumed and the number kills it: **1,109 of 6,758 absent chain people (16.4%)** carry
#: a `P2600` in `out/wikidata/p2600-all.tsv`, and they are mostly ordinary Nordic people
#: the loop handles well — Jens Jacobsen Bull, Gidsken Hermannsdatter Lange, Johanna
#: Bonnier, Anna Lorentzen. Holding on that would park 1,164 slots, most of them
#: workable.
#:
#: The QID is still carried into `reports/chain-gaps-on-hold.csv` when somebody is held,
#: because it is the handle for the different strategy: an item can be read offline from
#: the local store instead of exported from Geni.
ON_HOLD: dict[str, str] = {}

#: QID -> Geni ID dump from the bulk download; read to attach a Wikidata handle to the
#: held people. Absent file is fine, the column just comes out blank.
P2600_MAP = REPO / "out" / "wikidata" / "p2600-all.tsv"
OUT_HOLD = REPO / "reports" / "chain-gaps-on-hold.csv"


def wikidata_by_geni_id() -> dict[str, str]:
    """Geni ID -> QID, from the local store only. Never queries Wikidata."""
    out: dict[str, str] = {}
    if not P2600_MAP.exists():
        return out
    for line in P2600_MAP.read_text(encoding="utf-8").splitlines():
        parts = line.split("	")
        if len(parts) >= 2:
            out.setdefault(parts[1], parts[0])
    return out


def geni_ids_in_the_corpus() -> set[str]:
    """Every Geni ID that appears as an individual in any export."""
    files = sources.find_exports(EXPORTS)
    present: set[str] = set()
    for path in files:
        present.update(m.group(1).decode()
                       for m in INDI_XREF.finditer(path.read_bytes()))
    print(f"{len(files)} corpus exports, {len(present):,} distinct Geni IDs")
    return present


def chains() -> dict[str, set[str]]:
    """Geni ID -> the path files naming that person."""
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path in sorted(PATHS_DIR.glob("*.tsv")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("step"):
                continue
            for token in line.split("\t")[-1].split():
                if token.startswith("geni:"):
                    out[token[5:]].add(path.name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", type=int, default=10,
                    help="how many to write to the handoff file (default 10)")
    args = ap.parse_args()

    started = time.time()
    present = geni_ids_in_the_corpus()
    files_of = chains()

    absent = [g for g in files_of if g not in present]
    held = sorted((g for g in absent if g in ON_HOLD),
                  key=lambda g: -len(files_of[g]))
    absent = [g for g in absent if g not in ON_HOLD]
    absent.sort(key=lambda g: (-len(files_of[g]), g))
    slots = sum(len(files_of[g]) for g in absent)

    names: dict[str, str] = {}
    if NAMES.exists():
        with NAMES.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                names[row["geni_id"]] = row["name"]

    with OUT_ALL.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["slots", "geni_id", "name", "url", "paths"])
        for gid in absent:
            writer.writerow([len(files_of[gid]), gid, names.get(gid, ""),
                             FAMILY_TREE_URL.format(gid),
                             " | ".join(sorted(files_of[gid]))])

    shortlist = absent[:args.open]

    with OUT_OPEN.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["rank", "slots", "geni_id", "name", "url"])
        for rank, gid in enumerate(shortlist, start=1):
            writer.writerow([rank, len(files_of[gid]), gid, names.get(gid, ""),
                             FAMILY_TREE_URL.format(gid)])

    in_corpus = len(files_of) - len(absent) - len(held)
    print(f"chain people {len(files_of):,}   held {in_corpus:,}   gap {len(absent):,}")
    print(f"unfilled slots {slots:,}   ({time.time() - started:.0f}s, no merge)")
    qid_of = wikidata_by_geni_id()
    with OUT_HOLD.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["slots", "geni_id", "qid", "reason", "url", "paths"])
        for gid in held:
            writer.writerow([len(files_of[gid]), gid, qid_of.get(gid, ""),
                             ON_HOLD[gid], FAMILY_TREE_URL.format(gid),
                             " | ".join(sorted(files_of[gid]))])
    if held:
        print(f"\non hold, not ranked ({len(held)}, "
              f"{sum(len(files_of[g]) for g in held)} slots) -> {OUT_HOLD.name}:")
        for gid in held:
            print(f"  {len(files_of[gid]):>3} slots  {qid_of.get(gid, '--'):>10}  "
                  f"{ON_HOLD[gid]}")
    print(f"\nwrote {OUT_ALL.name} and {OUT_OPEN.name}\n")
    for rank, gid in enumerate(shortlist, start=1):
        print(f"  {rank:>2}. {len(files_of[gid]):>3} slots  "
              f"{names.get(gid, '?')[:40]:42} {gid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
