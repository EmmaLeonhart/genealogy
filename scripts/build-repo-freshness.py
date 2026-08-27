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


#: Below this, an output being older than its input is same-run ordering, not staleness.
MIN_DRIFT_HOURS = 1.0


def inputs_of(script_rel: str) -> list[str]:
    """The `reports/` and `out/` files a generator READS, by the paths it names.

    Crude on purpose: every `reports/x` or `out/x` literal in the script, minus whatever it
    writes. A file it both reads and writes is not a dependency of itself.
    """
    path = REPO / script_rel
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    named = set(re.findall(r'["\']((?:reports|out)/[\w./-]+\.(?:md|csv|tsv|json|ged))["\']',
                           text))
    written = set(re.findall(r'(?:open|write_text|to_csv)\([^)]*?["\']'
                             r'((?:reports|out)/[\w./-]+)', text))
    return sorted(named - written)


def stale_against_inputs(rel: str, generators: str) -> str:
    """`"<input> is Nh newer"` when a generated file is older than something it reads.

    **This is the failure mode the repo actually has.** Three consecutive findings on
    2026-08-27 were drift between stages, not defects inside one: the structural walk was
    two days older than `reports/derived-family.csv`; `garborg-live-state.tsv` sat frozen at
    2026-08-24 while the ledger was rebuilt daily, making three-quarters of a batch
    duplicates; the correspondence batch was four days behind the walk. Each was found by
    hand, one at a time.

    Git-commit age -- what the rest of this file measures -- cannot see any of them: every
    one of those files was committed recently, just built from something older.
    """
    out = REPO / rel
    if not out.exists() or not generators:
        return ""
    newer = []
    for script in generators.split(";"):
        for dep in inputs_of(script):
            d = REPO / dep
            if d.exists() and d.stat().st_mtime > out.stat().st_mtime:
                hours = (d.stat().st_mtime - out.stat().st_mtime) / 3600
                # **Under an hour is one run, not drift.** Several outputs are written
                # minutes apart by the same script and would otherwise flag each other
                # forever -- and a column that cries wolf is one nobody reads.
                if hours >= MIN_DRIFT_HOURS:
                    newer.append((hours, dep))
    if not newer:
        return ""
    hours, dep = max(newer)
    return f"{dep} is {hours:.0f}h newer"


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
            "stale_against_input": stale_against_inputs(
                rel, gens.get(Path(rel).name, "")),
        })

    # Output-older-than-input first: it is the only column here that means something is
    # WRONG right now rather than merely old.
    rows.sort(key=lambda r: (not r["stale_against_input"],
                             -(r["behind_by"] or 0), -(r["days_stale"] or 0)))
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
