"""Census every tracked non-corpus artifact and say how stale it is.

Emma, 2026-08-15: *"it should also do work on figuring out what stuff in the
repository is outdated because there are certain things, like the missing
ancestors for example, that are kind of outdated."*

One row per tracked file under `reports/`, `docs/`, `out/`-adjacent root
markdown, and the root `*.md` set. Per file:

- `last_commit` / `days_stale` — when git last touched it.
- `claims_exports` — the largest "<N> exports" / "<N> GEDCOMs" figure the file
  states about the corpus, or blank. This is the checkable claim: the corpus is
  measured live, so a report claiming 145 when 203 are on disk is describing a
  tree that no longer exists.
- `generator` — the module or script that writes it, found by searching the
  source for the file's own name. A generated report that is stale is a re-run;
  a hand-written one that is stale is a decision.

The point is NOT to regenerate everything. A dated report (`ingest-2026-08-05`,
`audit-downloads-2026-08-06`) is a record of a day and is supposed to hold an
old number. The column says what a file claims; whether that is wrong is a
judgement, so the report ranks and the human decides.
"""
from __future__ import annotations

import csv
import datetime as dt
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TODAY = dt.date(2026, 8, 15)

#: "94 exports", "103 GEDCOMs". Two digits minimum -- "3 exports" is prose.
CLAIM_RE = re.compile(r"\b(\d{2,4})\s+(?:exports|GEDCOMs|gedcoms|\.ged files)\b")

#: A filename in a dated report is a record, not a claim about now.
DATED_RE = re.compile(r"20\d\d-\d\d-\d\d")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True,
                         text=True, check=True).stdout
    keep = []
    for line in out.splitlines():
        if line.startswith("exports/") or line.startswith("gedcom/"):
            continue
        if line.startswith(("reports/", "docs/")) or (
                "/" not in line and line.endswith(".md")):
            keep.append(line)
    return keep


def last_commit(path: str) -> str:
    r = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short",
                        "--", path], cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip()


def source_index() -> dict[str, str]:
    """Map a filename to the module/script that names it."""
    index: dict[str, list[str]] = {}
    for root in ("src", "scripts"):
        for p in (REPO / root).rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in re.finditer(r'["\']([\w./-]+\.(?:md|csv|tsv|json|html))["\']',
                                 text):
                index.setdefault(Path(m.group(1)).name, []).append(
                    str(p.relative_to(REPO)).replace("\\", "/"))
    return {k: ";".join(sorted(set(v))[:3]) for k, v in index.items()}


def main() -> None:
    live_exports = len(list((REPO / "exports").rglob("*.ged")))
    gens = source_index()
    rows = []
    for rel in tracked():
        p = REPO / rel
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        claims = [int(m.group(1)) for m in CLAIM_RE.finditer(text)]
        claim = max(claims) if claims else ""
        date = last_commit(rel)
        stale = ""
        if date:
            y, m, d = (int(x) for x in date.split("-"))
            stale = (TODAY - dt.date(y, m, d)).days
        rows.append({
            "path": rel,
            "last_commit": date,
            "days_stale": stale,
            "bytes": p.stat().st_size if p.exists() else 0,
            "claims_exports": claim,
            "behind_by": (live_exports - claim) if claim else "",
            "dated_name": "yes" if DATED_RE.search(Path(rel).name) else "",
            "generator": gens.get(Path(rel).name, ""),
        })

    rows.sort(key=lambda r: (-(r["behind_by"] or 0), -(r["days_stale"] or 0)))
    out = REPO / "reports" / "repo-freshness.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    behind = [r for r in rows if r["behind_by"] and not r["dated_name"]]
    print(f"corpus on disk: {live_exports} exports")
    print(f"{len(rows)} tracked artifacts -> {out}")
    print(f"{len(behind)} state a corpus size smaller than the live one "
          f"and are not dated snapshots:")
    for r in behind:
        print(f"  {r['behind_by']:>4} behind  {r['claims_exports']:>4} claimed  "
              f"{r['last_commit']}  {r['path']}")


if __name__ == "__main__":
    main()
