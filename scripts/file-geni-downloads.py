"""Move what the geni collector extension downloaded into the repo.

`<a download>` strips path separators, so a content script cannot write into a subfolder --
every capture lands flat in `~/Downloads`. That is why filing is a separate step rather than a
tidy-up, and it is the same shape as the proven manual method, which ended
`mv /c/Users/Emma/Downloads/<id>-blood.html geni-paths/`.

    python scripts/file-geni-downloads.py [--downloads DIR] [--dry-run]

**A `.ged`/`.zip` is NEVER touched.** `CLAUDE.md` § *Never overwrite an existing `.ged`* makes
where an export goes her call, and § *Do not integrate as you go* keeps the zips in
`~/Downloads` until a whole batch is down. This script files path captures and the results TSV
and nothing else; it prints the exports it can see and leaves them alone.

**It refuses to overwrite.** A capture that already exists is a second reading of the same
target, which is a thing to look at rather than to silently replace.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PATHS = REPO / "geni-paths"
REPORTS = REPO / "reports"

CAPTURE = re.compile(r"^(?P<id>[0-9]+)-(?P<kind>blood|inlaw)\.(?P<ext>html|tsv)$", re.I)
#: Step 1 of the per-individual loop -- the immediate family scraped off the page. One file
#: per person, and they accumulate, so they get their own directory rather than joining the
#: path captures.
FAMILY = re.compile(r"^(?P<id>[0-9]+)-family\.tsv$", re.I)
RESULTS = re.compile(r"^geni-collector-results(?: \(\d+\))?\.tsv$", re.I)
EXPORTS = re.compile(r"^export-geni.*\.zip$", re.I)


def default_downloads() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser("~")) / "Downloads"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--downloads", default=str(default_downloads()))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = pathlib.Path(args.downloads)
    if not src.is_dir():
        print("no such directory: %s" % src, file=sys.stderr)
        return 1

    PATHS.mkdir(parents=True, exist_ok=True)
    moved = skipped = 0
    zips = []

    for f in sorted(src.iterdir()):
        if not f.is_file():
            continue
        if EXPORTS.match(f.name):
            zips.append(f.name)
            continue

        m = CAPTURE.match(f.name)
        if m:
            # A `.tsv` path file belongs beside the other generated paths, not with the pages.
            dest = (REPO / "paths" / ("isolate-geni-%s-%s.tsv" % (m.group("id"), m.group("kind").lower()))
                    if m.group("ext").lower() == "tsv"
                    else PATHS / f.name.lower())
        elif FAMILY.match(f.name):
            dest = REPO / "geni-families" / f.name.lower()
        elif RESULTS.match(f.name):
            dest = REPORTS / "geni-collector-results.tsv"
        else:
            continue

        if dest.exists() and not RESULTS.match(f.name):
            print("EXISTS, left alone: %s -> %s" % (f.name, dest.relative_to(REPO)))
            skipped += 1
            continue
        print("%s -> %s" % (f.name, dest.relative_to(REPO)))
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))
        moved += 1

    print("\n%d filed, %d left alone" % (moved, skipped))
    if zips:
        # Named, never moved: filing an export is hers, and a batch is filed all at once.
        print("%d export zip(s) in %s, NOT touched: %s"
              % (len(zips), src, ", ".join(zips[:5]) + (" ..." if len(zips) > 5 else "")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
