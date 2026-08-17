"""Convert every saved Geni page that has no path file yet.

Emma saves relationship-path pages into `paths_for_wikidata_isolates/` -- **not**
`geni_pages/`, which is the older store. This walks that directory, works out
which pages have never been turned into a `paths/*.tsv`, and runs
`genimerge path-from-html` over the ones that have not.

Run it whenever she says she has added links. It is idempotent: a page that
already has a path file is skipped, so re-running costs a directory listing.

**Matching is prefix-aware on purpose.** The existing path files were named by
slugging the page title and then truncating -- `isolate-geni-hartvig-sverdrup-
eckhoff-1855-1928-gausel-hetland-n-sta` is the whole name. A plain equality check
calls 31 already-converted pages new and would double-count their slots in the
chain-gap ranking.

Titles that are entirely CJK slug to nothing usable (`isolate-geni-259-210` for
Qin Shi Huang), so those get hand-written names from MANUAL.

    PYTHONPATH=src python scripts/convert-new-saved-pages.py [--dry-run]
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAGES = REPO / "paths_for_wikidata_isolates"
PATHS = REPO / "paths"

MANUAL = {
    "Geni - 【(嬴姓)】 ___ _政 (-259--210)": "isolate-geni-qin-shi-huang-259-210",
    "Geni - 【(山東濟寧)】 孫承諤 (1911-1991)": "isolate-geni-sun-cheng-e-1911-1991",
}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def target_name(stem: str) -> str:
    return MANUAL.get(stem) or ("isolate-" + slug(stem))


def already_converted(name: str, have: list[str]) -> bool:
    # existing names are truncated, so a prefix either way counts as a match
    return any(h == name or name.startswith(h) or h.startswith(name) for h in have)


def main() -> int:
    dry = "--dry-run" in sys.argv
    have = sorted(p.stem for p in PATHS.glob("*.tsv"))
    todo = [
        p for p in sorted(PAGES.glob("*.html"))
        if not already_converted(target_name(p.stem), have)
    ]
    print(f"{len(list(PAGES.glob('*.html')))} saved pages, {len(have)} path files, "
          f"{len(todo)} to convert")
    if dry:
        for p in todo:
            print("  would convert", p.name)
        return 0

    env = dict(os.environ, PYTHONPATH=str(REPO / "src"), PYTHONIOENCODING="utf-8")
    failed = 0
    for p in todo:
        out = PATHS / (target_name(p.stem) + ".tsv")
        r = subprocess.run(
            [sys.executable, "-m", "genimerge", "path-from-html", str(p), "-o", str(out)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
        )
        lines = (r.stdout or r.stderr).strip().splitlines()
        note = lines[-1][:70] if lines else ""
        if r.returncode:
            failed += 1
        print(f"{'ok  ' if not r.returncode else 'FAIL'} {out.name[:60]:<60} {note}")
    print(f"\nconverted {len(todo) - failed}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
