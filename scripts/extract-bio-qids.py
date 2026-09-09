"""The Geni-to-Wikidata correspondence Emma wrote into the Geni BIOS.

    python scripts/extract-bio-qids.py

**Emma, 2026-08-31, pointing at an Izumo join that had gone the long way round:** *"Yeah you use
the bio qids lol."*

**These are the freshest correspondence in the repo and nothing was reading them.** A Geni
profile's *About Me* can carry a `wikidata.org/wiki/Q…` link, and she puts them there. It shows
up in the export as text on the person's record, so **156 of the 600 exports carry at least
one**. That is a Geni-side statement of identity, made by her, captured at the moment each
export ran.

**Why this beats the obvious alternatives, both of which were tried first and were wrong:**

* `out/wikidata/p2600-all.tsv` is a **download from 2026-08-09**. Joining the 204 Izumo roster
  QIDs through it yields **2** Geni ids, because almost every one of those items got its `P2600`
  after that date. Stale, and the staleness is invisible -- 2 reads exactly like "these people
  are not linked".
* Scraping 19-digit ids out of `reports/izumo*.tsv` yields 210 and works, but it is reading
  whatever happens to be lying in old reports rather than a stated correspondence.
  `CLAUDE.md` § *Do not grab the first artifact that vaguely matches* is the objection.

**The parse is record-scoped, which is the whole difficulty.** A `wikidata.org` link is loose
text inside a `NOTE`/`_BIO`-style block, several lines below the `0 @I…@ INDI` that owns it, so
a file-wide `grep` gives QIDs attached to nobody. This walks the file tracking the current `0`
level record and attributes every link found to it.

**A person may carry more than one QID and that is not an error** -- `CLAUDE.md` § *A second
Geni ID on one Wikidata item is NOT a conflict* is the mirror of it. All pairs are emitted.

Writes **`out/bio-qids.tsv`, which is gitignored** -- Emma, 2026-09-06: *"it also
shouldn't exist lol because it's just garbage for agents to get confused about."* It sat in
`reports/` looking like one of the two curated Geni-to-Wikidata correspondences and is not
one: it is a machine extract of links already in Geni bios, read by the roster scripts.
`reports/correspondence-sources.md` is what that distinction is. Writes -- `geni_id`, `qid`, `exports`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.sources import find_exports  # noqa: E402

OUT = ROOT / "out" / "bio-qids.tsv"

#: `0 @I6000000001846508982@ INDI` -- the record that owns everything until the next `0` line.
INDI = re.compile(rb"^0 @I(\d+)@ INDI", re.M)
LEVEL0 = re.compile(rb"^0 ", re.M)
QID = re.compile(rb"wikidata\.org/(?:wiki|entity)/(Q\d+)", re.I)


def pairs_in(blob):
    """(geni_id, qid) for every Wikidata link, attributed to the record it sits in."""
    # Record boundaries: every level-0 line starts a new record.
    starts = [m.start() for m in LEVEL0.finditer(blob)] + [len(blob)]
    owner = None
    for i in range(len(starts) - 1):
        chunk = blob[starts[i]:starts[i + 1]]
        m = INDI.match(chunk)
        owner = m.group(1).decode() if m else None
        if owner is None:
            continue
        for q in QID.findall(chunk):
            yield owner, q.decode().upper()


def main():
    files = list(find_exports())
    print(f"scanning {len(files)} exports for bio Wikidata links ...", flush=True)

    seen = collections.defaultdict(set)
    for n, path in enumerate(files, 1):
        blob = path.read_bytes()
        if b"wikidata.org" not in blob:
            continue
        for gid, qid in pairs_in(blob):
            seen[(gid, qid)].add(path.name)
        if n % 150 == 0:
            print(f"  {n} exports", flush=True)

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["geni_id", "qid", "exports"])
        for (gid, qid), where in sorted(seen.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            w.writerow([gid, qid, len(where)])

    people = {g for g, _ in seen}
    qids = {q for _, q in seen}
    multi = sum(1 for g in people if len({q for gg, q in seen if gg == g}) > 1)
    print(f"\n{len(seen):,} distinct (person, item) pairs")
    print(f"{len(people):,} Geni profiles carry a Wikidata link in their bio")
    print(f"{len(qids):,} distinct Wikidata items named")
    print(f"{multi:,} profiles name more than one item")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
