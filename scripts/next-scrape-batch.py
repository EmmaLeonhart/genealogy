"""Print the next N Geni IDs to save, skipping anything already in geni-scraping/.

The saving itself runs in the browser: navigate to /people/x/<id>, then a Blob of
the page's own `outerHTML` is downloaded as `<id>.html`, so the markup never enters
the agent's context. `scripts/sweep-scraped-pages.sh` files the results.

    PYTHONPATH=src python scripts/next-scrape-batch.py [N]
"""
from __future__ import annotations
import csv, io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from genimerge import sources

REPO = sources.REPO_ROOT
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
have = {p.stem for p in (REPO / "geni-scraping").glob("*.html")}
rows = list(csv.DictReader(io.open(REPO / "reports" / "scrape-targets.csv",
                                   encoding="utf-8")))
todo = [r["geni_id"] for r in rows if r["geni_id"] not in have]
print(f"# {len(have)} saved, {len(todo)} to go", file=sys.stderr)
for g in todo[:n]:
    print(g)
