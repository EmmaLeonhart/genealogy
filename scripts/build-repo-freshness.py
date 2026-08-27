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
#: **Not a literal.** It was `dt.date(2026, 8, 15)`, so from the 16th onward every
#: `days_stale` in this census was understated by however long had passed -- twelve days by
#: 2026-08-27, and a report about staleness that is itself stale is the joke writing itself.
#: Same class as `--retrieved` defaulting to a typed-once date in
#: `build-structural-correspondence-batch.py`, fixed the same day.
TODAY = dt.date.today()

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
                # A script that merely NAMES the file is indexed here; whether it reads
                # rather than writes it is settled in `stale_against_inputs`, which skips a
                # generator whose own inputs include the file. One mechanism, not two.
                index.setdefault(Path(m.group(1)).name, []).append(
                    str(p.relative_to(REPO)).replace(chr(92)*2, '/'))
    return {k: ";".join(sorted(set(v))[:3]) for k, v in index.items()}


#: Below this, an output being older than its input is same-run ordering, not staleness.
MIN_DRIFT_HOURS = 1.0


#: `X = ... "name.csv" ...` — the constant a generator builds once at module level and then
#: opens. Almost nothing here writes the literal path a second time.
_ASSIGN_RE = re.compile(
    r'^[ \t]*([A-Za-z_]\w*)[ \t]*=[^\n]*?["\']([\w./-]+\.(?:md|csv|tsv|json|ged|qs|html))["\']',
    re.M)
#: A filename literal opened inline with an explicit write or append mode.
_DIRECT_WRITE_RE = re.compile(
    r'open\(\s*[^)]*?["\']([\w./-]+\.(?:md|csv|tsv|json|ged|qs|html))["\'][^)]*?,\s*["\'][wax]')


def writes_in(text: str) -> set[str]:
    """The filenames a script WRITES, judged by mode — not the ones it merely mentions.

    **`open(` alone was the bug.** The previous test counted any `open(...)` call containing a
    filename literal as a write, so `open(R / "emma-judgments.tsv", encoding="utf-8")` — a
    plain READ of a file Emma maintains by hand — registered as an output. That deleted it from
    the script's inputs, which in turn defeated the reader-is-not-a-generator skip in
    `stale_against_inputs`, and her hand verdicts were reported as 35h behind
    `reports/structural-correspondence.csv`, an input they do not have.

    A write is an inline `open("x.csv", "w")`, or a name bound to a path constant
    (`OUT = ROOT / "reports" / "x.tsv"`) later used as `OUT.open("w")`, `OUT.write_text(...)`,
    `OUT.write_bytes(...)` or `open(OUT, "w")`. A read-mode open of that same constant does not
    count, and that distinction is the entire fix.
    """
    found = {Path(m).name for m in _DIRECT_WRITE_RE.findall(text)}
    for var, name in _ASSIGN_RE.findall(text):
        v = re.escape(var)
        if (re.search(v + r'\.open\(\s*["\'][wax]', text)
                or re.search(v + r'\.write_(?:text|bytes)\(', text)
                or re.search(r'open\(\s*' + v + r'\s*,\s*["\'][wax]', text)):
            found.add(Path(name).name)
    return found


def inputs_of(script_rel: str) -> list[str]:
    """The `reports/` and `out/` files a generator READS.

    **Match bare filenames, not `reports/x.csv` literals.** This repo builds paths by
    joining -- `REPO / "reports" / "patronymic-items.csv"` -- so the joined string never
    appears in the source and a pattern looking for it finds only the minority of scripts
    that write the path in one piece. That is the same empty-join trap the rest of this repo
    keeps recording: the detector looked like it was working and was simply blind to most
    inputs.

    So: every `"<something>.csv|tsv|json|md|ged"` literal, resolved against `reports/` and
    `out/` by existence, minus whatever the script writes.
    """
    path = REPO / script_rel
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    named = set()
    for m in re.finditer(r'["\']([\w.-]+\.(?:md|csv|tsv|json|ged))["\']', text):
        for folder in ("reports", "out", "out/wikidata"):
            if (REPO / folder / m.group(1)).exists():
                named.add(f"{folder}/{m.group(1)}")
                break
    written = {f"{folder}/{name}"
               for folder in ("reports", "out", "out/wikidata")
               for name in writes_in(text)
               if (REPO / folder / name).exists()}
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
        deps = inputs_of(script)
        # **If the file is among the script's own inputs, that script READS it and is not
        # its generator.** `source_index` maps a name to any script that mentions it, so
        # `build-name-item-batch.py` -- which reads `patronymic-items.csv` as `PATRONYMICS`
        # -- was called its writer, and the file was then reported 8h behind
        # `name-classes.csv`, an input it does not have. Reusing `inputs_of` costs nothing
        # and needs no second heuristic.
        if rel in deps:
            continue
        for dep in deps:
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
