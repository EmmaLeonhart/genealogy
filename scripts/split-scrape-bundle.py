"""Split a bundled multi-page scrape into one <geni id>.html per person.

The browser saves many profiles in a single download (Chrome allows one
automatic download per tab, so bundling is how a batch beats one-tab-per-person).
Each page is preceded by a marker line:

    <<<GENI-PAGE 6000000012198494299>>>

    python scripts/split-scrape-bundle.py <bundle.html> [dest]

Writes into geni-scraping/ by default and refuses to overwrite a page already
held, matching scripts/sweep-scraped-pages.sh.
"""
from __future__ import annotations
import io, re, sys
from pathlib import Path

MARK = re.compile(r"<<<GENI-PAGE (\d+)>>>")

bundle = Path(sys.argv[1])
dest = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / "geni-scraping"
text = io.open(bundle, encoding="utf-8", errors="replace").read()

parts = MARK.split(text)
# parts = [preamble, id1, body1, id2, body2, ...]
wrote = skipped = 0
for i in range(1, len(parts) - 1, 2):
    gid, body = parts[i], parts[i + 1]
    out = dest / f"{gid}.html"
    if out.exists():
        skipped += 1
        continue
    io.open(out, "w", encoding="utf-8").write(body.strip())
    wrote += 1
print(f"split {wrote} new, {skipped} already held; geni-scraping now "
      f"{len(list(dest.glob('*.html')))}")
