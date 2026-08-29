"""Write each person's Wikidata QID into their bio, in the SYNOPTIC TREE.

    python scripts/inject-qid-into-bios.py [--in out/merged.ged] [--out out/synoptic.ged]

**Emma, 2026-08-29:** *"When the synoptic tree is merged we change all of their bios to links
to their qids so that the next step in with the wikidata union (which isn't really implemented
yet) they get joined with those wikidata items."* Asked where the link is written, she chose
**into the merged tree only** — Geni is never touched, no browser, nothing outward-facing.

## Why a `NOTE` and not something new

Geni already exports the About Me as a `NOTE` on the individual:

    1 NOTE {geni:about_me} https://wikidata.org/wiki/Special:EntityPage/Q135579415#…

and `scripts/build-geni-qid-links.py` already reads QIDs back *out* of that. So the bio is
where a Wikidata link on a Geni person lives, and writing there means the link is ordinary tree
content rather than a side file — which is the whole point, per `CLAUDE.md`: *"Forcing them into
this Synoptic tree like this makes it so that the Synoptic tree, when it starts being used as an
input, does use them properly, in the zipper merge thing."*

## The merge unions `NOTE`, so an injected link survives

`merge.ALWAYS_REPEATABLE` holds `NOTE`, deliberately and against the measured single-valued
detection. Repeatable paths with a value are matched **on that value**: an identical bio across
two exports collapses to one, a different one is kept alongside. So nothing here is overwritten
by a later export, and re-running this script is idempotent because the line it writes is
byte-identical to the one already there.

That is also why this writes its own `NOTE` line rather than appending to an existing bio:
editing the About Me text would create a *different* value, which the merge would then keep
**beside** the original instead of replacing it, and the person would end up with both.

## What it will not assert

**A Geni id with more than one candidate QID gets one `NOTE` per QID, not a choice.** 772 such
conflicts are in `reports/synoptic-conflicts.tsv`. Emitting both is honest and costs nothing —
`NOTE` is repeatable — while picking one would be an entity resolution this script has no
standing to make. `CLAUDE.md` § *A second Geni ID on one Wikidata item is NOT a conflict* is the
mirror case and settles the principle: multiplicity is recorded, not adjudicated.

**Nothing is removed.** The input's own `NOTE` lines, including Geni's About Me and any Wikidata
link Emma wrote there by hand, pass through untouched.

## Streaming, because the input is 1.6 GB

`out/merged.ged` is 1,683,614,450 bytes. Records are buffered one at a time — a `0`-level line
starts a record — and written straight back out, so peak memory is one individual.
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from genimerge.identity import geni_id_from_xref  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

#: The form the link takes. Plain `/wiki/<QID>` rather than Geni's
#: `Special:EntityPage/...#...` — that shape is what Geni's own renderer produced, not something
#: to imitate, and `build-geni-qid-links.py` matches the QID anywhere in the line.
LINK = "https://www.wikidata.org/wiki/{qid}"

#: `0 @I6000000087535357291@ INDI`
RECORD = re.compile(r"^0 (@[^@]+@) (\w+)")


def correspondence(path):
    """`{geni_id: [qid, ...]}` — every QID any source pairs with this person.

    Sorted and de-duplicated so the output is deterministic: the same tree in gives the same
    tree out, which is what makes re-running this cheap to verify.
    """
    out = collections.defaultdict(set)
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
            if g and q:
                out[g].add(q)
    return {g: sorted(qs) for g, qs in out.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="src", default="out/merged.ged")
    ap.add_argument("--out", dest="dst", default="out/synoptic.ged")
    ap.add_argument("--pairs", default="reports/synoptic-correspondence.tsv")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after N individuals; for checking the shape without a full pass")
    args = ap.parse_args()

    src, dst = ROOT / args.src, ROOT / args.dst
    if not src.exists():
        sys.exit(f"no such tree: {src}. Run `genimerge merge` first.")
    pairs = correspondence(ROOT / args.pairs)
    print(f"{len(pairs):,} Geni ids carry at least one QID")

    people = injected = already = multi = 0
    buf, xref, kind = [], None, None

    def flush(out):
        """Write one buffered record, adding the links this person is missing."""
        nonlocal injected, already, multi
        if kind == "INDI":
            geni = geni_id_from_xref(xref)
            qids = pairs.get(geni or "", ())
            if len(qids) > 1:
                multi += 1
            for qid in qids:
                line = f"1 NOTE {LINK.format(qid=qid)}"
                # Idempotent: the exact line we would write is already there. A *different*
                # line mentioning the same QID -- Geni's own About Me export, which Emma wrote
                # by hand -- is deliberately NOT treated as a match. Hers says a human asserted
                # it on Geni; ours says our correspondence pass derived it. Both are true and
                # the merge keeps both, because they are different values.
                if line in buf:
                    already += 1
                    continue
                buf.append(line)
                injected += 1
        out.write("\n".join(buf) + "\n")

    with src.open(encoding="utf-8", newline="") as fh, \
            dst.open("w", encoding="utf-8", newline="\n") as out:
        for raw in fh:
            line = raw.rstrip("\r\n")
            m = RECORD.match(line)
            if m or line.startswith("0 "):
                if buf:
                    flush(out)
                    if kind == "INDI":
                        people += 1
                        if args.limit and people >= args.limit:
                            buf = []
                            break
                buf = [line]
                xref, kind = (m.group(1), m.group(2)) if m else (None, line.split()[-1])
            else:
                buf.append(line)
        if buf:
            flush(out)
            people += kind == "INDI"

    print(f"{people:,} individuals read")
    print(f"{injected:,} NOTE links written")
    print(f"{already:,} already present -- re-running this is a no-op")
    print(f"{multi:,} people carry more than one QID; each gets one NOTE per QID, never a choice")
    print(f"wrote {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
