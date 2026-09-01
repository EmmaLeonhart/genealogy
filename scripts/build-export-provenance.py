"""Which export did each person come from?

**The merge deliberately does not know.** `todo.md` §7 records it as a design property,
confirmed 2026-08-01: *"`Merger.add_source` keys on the xref and knows nothing about which
file it came from"*, which is what lets a new export be a file drop rather than a code
change. Nothing downstream carries a source column either — not `derived-labels.csv`, not
`derived-facts.csv`, not `derived-family.csv`.

**That is a gap under a live instruction.** queue.md's romanisation item says the culture
of a Han-only name — 陳 is *Chen*, *Chin* or *Jin* depending on whether the person is
Chinese, Japanese or Korean — is settled by *"the tree… via neighbours and **which exports
they came from**"*, never by the name. The neighbour half is available. The export half was
not, so the instruction could only ever have been half-followed.

This restores it without touching the merge. It reads the export files directly and
records, per Geni id, which files contain it — so provenance is derived where it is needed
rather than threaded through a merge that is better off not caring.

**An id in several exports is the normal case, not a conflict.** Exports overlap heavily by
design; the devlog measured 14.7% batch-internal redundancy. What matters for the culture
question is the *set* of files a person appears in, and especially a person who appears in
only one — that one seed says most about them.

    py scripts/build-export-provenance.py [--exports-dir DIR]

Writes `reports/export-provenance.csv` (geni_id, n_exports, exports) and a summary in
`reports/export-provenance.md`. Reads only; nothing is fetched and no record is modified.
"""

from __future__ import annotations

import collections
import csv
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPORTS = REPO / "exports"
OUT_CSV = REPO / "reports" / "export-provenance.csv"
OUT_MD = REPO / "reports" / "export-provenance.md"

#: `0 @I6000000001846508982@ INDI` — the individual record header, and the only line
#: this needs. Matching just this keeps a 1.2 GB pass cheap.
INDI = re.compile(r"^0 @I(\d+)@ INDI\s*$")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    exports_dir = EXPORTS
    if "--exports-dir" in sys.argv:
        exports_dir = Path(sys.argv[sys.argv.index("--exports-dir") + 1])

    files = sorted(p for p in exports_dir.rglob("*.ged"))
    if not files:
        print(f"no .ged under {exports_dir}")
        return 1
    print(f"{len(files)} export file(s) under {exports_dir}")

    where: dict[str, set[str]] = collections.defaultdict(set)
    t0 = time.time()
    for n, path in enumerate(files, 1):
        name = path.stem
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if line.startswith("0 @I"):
                        m = INDI.match(line.rstrip("\r\n"))
                        if m:
                            where[m.group(1)].add(name)
        except OSError as e:                                      # noqa: BLE001
            print(f"  skipped {path.name}: {e}", file=sys.stderr)
        if n % 50 == 0:
            print(f"  ...{n}/{len(files)} files, {len(where):,} people, "
                  f"{time.time() - t0:.0f}s", flush=True)

    counts = collections.Counter(len(v) for v in where.values())
    per_file = collections.Counter()
    only_here = collections.Counter()
    for gid, fs in where.items():
        for f in fs:
            per_file[f] += 1
        if len(fs) == 1:
            only_here[next(iter(fs))] += 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "n_exports", "exports"])
        for gid in sorted(where):
            fs = sorted(where[gid])
            w.writerow([gid, len(fs), " | ".join(fs)])

    uniq = sum(1 for v in where.values() if len(v) == 1)
    lines = [
        "# Which export each person came from", "",
        "Built by `scripts/build-export-provenance.py`, read-only over `exports/`.",
        "",
        "**The merge does not track this and should not** — `todo.md` §7 records that as "
        "the property which lets a new export be a file drop rather than a code change. "
        "This derives it where it is needed instead.",
        "",
        f"- export files read: **{len(files)}**",
        f"- distinct people: **{len(where):,}**",
        f"- appearing in exactly one export: **{uniq:,}** "
        f"({100 * uniq / max(len(where), 1):.1f}%)",
        "", "## How many exports each person appears in", "",
        "| exports | people |", "| ---: | ---: |",
    ]
    for k in sorted(counts):
        lines.append(f"| {k} | {counts[k]:,} |")
    lines += ["", "## The seeds that carry people nobody else has", "",
              "The column that matters for the culture question: a person present in "
              "**one** export is characterised by that seed.", "",
              "| export | people | of them unique to it |", "| --- | ---: | ---: |"]
    for f, n in per_file.most_common(30):
        lines.append(f"| `{f}` | {n:,} | {only_here.get(f, 0):,} |")
    lines += ["", "## What this is for", "",
              "queue.md's romanisation item: 陳 is *Chen*, *Chin* or *Jin* depending on "
              "whether the person is Chinese, Japanese or Korean, and Emma's rule is that "
              "**the tree settles it — via neighbours and which exports they came from — "
              "never the name.** The neighbour half was already available. This is the "
              "other half, and without it the instruction could only be half-followed."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nwrote {OUT_CSV} and {OUT_MD}")
    print(f"  {len(where):,} people across {len(files)} exports; "
          f"{uniq:,} appear in exactly one")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
