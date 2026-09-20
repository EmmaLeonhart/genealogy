"""Name every tracked file approaching GitHub's 100 MB hard limit, and say what can grow it.

    python scripts/check-file-sizes.py            # list, always exit 0
    python scripts/check-file-sizes.py --strict   # exit 1 on a file near the limit

**What it costs to not have this.** GitHub declines a push containing a file over 100 MB at
the pre-receive hook, so on 2026-09-19 `pipeline.yml` did **68 minutes of work and had every
push rejected, five attempts, every run** -- for four hours, silently. It was silent because
the job's `timeout-minutes` killed it mid-retry and GitHub reports a timeout kill as
`cancelled`, **the same word as the supersede-on-push cancellation**, which is what it was
read as. Two confident wrong diagnoses came out of that one word. Listing tracked files over
80 MB takes under three seconds; the alternative is finding out an hour into a run.

⛔ **A FILE OVER THE LIMIT BLOCKS EVERY PUSH, NOT JUST THE ONE THAT WROTE IT.** The
pre-receive hook rejects the push for what the repository CONTAINS. Measured here 2026-09-19
while building this check: **no workflow runs `refresh-live-values.py` and nothing in
`pipeline.yml` calls it**, so `garborg-live-items.json` -- the 100.32 MB file that took the
pipeline down -- was never regenerated in CI at all. It was refreshed and committed by a
session, and from then on it refused the pipeline's pushes, this repo's pushes, everyone's.
So the size alone is the failing condition, and `--strict` fails on it alone.

**What the `grown by` column is for, then.** It is not the failure decision; it is which KIND
of problem a file is. One a workflow rewrites crosses the limit unattended, between two runs,
with nobody watching -- that is a live fault. One nothing regenerates sits at whatever size
the last person left it -- `preservation/genealogy/dropbox/ITIS.ged` at 91.3 MB is the worked
example, and it is harmless in exactly that way. `CLAUDE.md` § *CHECK before raising an alarm*
is the whole column: it says which of the two you are looking at before anyone reacts.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORKFLOWS = REPO / ".github" / "workflows"

MB = 1024 * 1024

#: Report at and above this. Not a round number chosen for looks: `name-item-languages.csv`
#: sits at 83.1 MB and `tree-eccentricity.csv` at 84.3 MB, and the point of the list is to
#: hold the files that are one regeneration away from the limit, not to be empty.
WARN_MB = 80

#: `--strict` fails here. Below 100 because a file that reaches 100 has ALREADY taken the
#: next push with it, and the run that discovers that is the run that wasted an hour. Five
#: megabytes of margin is one regeneration of anything on this list.
FAIL_MB = 95

#: The limit itself, quoted in the failure line so nobody has to look it up.
HARD_MB = 100


def _writes_in():
    """`writes_in` from `build-repo-freshness.py`, which already judges a write by MODE.

    Imported rather than re-derived. That function's docstring records the bug that `open(`
    alone was counted as a write, so a plain read registered as an output; the fix is subtle,
    it is tested where it lives, and a second copy here would be a second thing to get wrong
    -- `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD*. The hyphen in the filename is
    why this is an `importlib` load and not an `import`.
    """
    path = REPO / "scripts" / "build-repo-freshness.py"
    spec = importlib.util.spec_from_file_location("_repo_freshness", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def writes(text: str) -> set[str]:
        found = mod.writes_in(text)
        for var, name in mod._ASSIGN_RE.findall(text):
            if _ATOMIC_RE(var).search(text):
                found.add(Path(name).name)
        return found

    return writes


def _ATOMIC_RE(var: str):
    """`os.replace(tmp, OUT)` -- write to a temp file, then swap it in.

    ⛔ **THIS IS THE REPO'S DOMINANT WRITE IDIOM AND `writes_in` CANNOT SEE IT.** It judges a
    write by the mode on the output name, and in this pattern the mode is on `tmp`; `OUT` is
    only ever the destination of a rename. Measured 2026-09-19: it is how
    `measure-eccentricity.py` writes `tree-eccentricity.csv` and how `refresh-live-values.py`
    writes its shards -- the 84.3 MB file and the 100.32 MB one, which is to say both of the
    files this check was written for. Without this rule the column reads `static` for them,
    which is the single most misleading thing it could say.
    """
    v = re.escape(var)
    #: Both spellings, because the repo uses both: `os.replace(tmp, OUT)` in
    #: `refresh-live-values.py`, `tmp.replace(OUT)` in `measure-eccentricity.py`. The
    #: single-argument `.replace(OUT)` is `Path.replace`; `str.replace` takes two, so the
    #: arity is what keeps this off ordinary string work.
    return re.compile(r"(?:os\.replace|os\.rename|shutil\.move)\([^)]*?,\s*" + v + r"\s*\)"
                      r"|\.replace\(\s*" + v + r"\s*\)")


def tracked_sizes():
    """`[(bytes, path)]` for every tracked file present on disk, largest first.

    **Absent is skipped, not zero.** `pipeline.yml` checks out sparsely -- no `/exports`, no
    `/wikidata` -- so most of the repo is simply not there when this runs in CI. A file the
    runner does not have is a file the runner cannot push over the limit.
    """
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True,
                         text=True, encoding="utf-8", errors="replace",
                         check=True).stdout
    rows = []
    for rel in out.splitlines():
        rel = rel.strip()
        if not rel:
            continue
        try:
            rows.append(((REPO / rel).stat().st_size, rel))
        except OSError:
            continue
    rows.sort(reverse=True)
    return rows


def writers():
    """`{filename: [(script, runs_in_ci), ...]}` -- who writes each generated file.

    ⛔ **THE SECOND HALF IS A DIRECT TEST AND IT STAYS DIRECT.** A transitive one was tried
    here first -- a script is in CI if something in CI calls it -- and the edge that made it
    worth having turned out not to exist: `build-garborg-day.py` names
    `refresh-live-values.py` six times and every one is prose telling a person to run it. A
    fixpoint over mentions pulled in `measure-eccentricity.py` as well, which would have
    reported `tree-eccentricity.csv` as a live CI fault when it is the opposite. Prose naming
    a script is how this repo is written, so a mention is not an edge.
    """
    writes_in = _writes_in()
    invoked = ""
    for wf in sorted(WORKFLOWS.glob("*.yml")):
        invoked += wf.read_text(encoding="utf-8", errors="replace")

    index: dict[str, list[tuple[str, bool]]] = {}
    for root in ("src", "scripts"):
        base = REPO / root
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            rel = str(p.relative_to(REPO)).replace("\\", "/")
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for name in writes_in(text):
                index.setdefault(name, []).append((rel, rel in invoked))
    return {k: sorted(set(v)) for k, v in index.items()}


def describe(rel: str, index) -> str:
    """The `grown by` cell: who rewrites this file, and whether CI is the one doing it."""
    gens = index.get(Path(rel).name, [])
    if not gens:
        return "static -- no generator writes it"
    ci = [s for s, in_ci in gens if in_ci]
    if ci:
        return "rewritten by CI: " + ", ".join(ci)
    return "grows only when a person runs " + ", ".join(s for s, _ in gens)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help=f"exit 1 on a tracked file at or over {FAIL_MB} MB")
    args = ap.parse_args()

    index = writers()
    rows = [(n, rel) for n, rel in tracked_sizes() if n >= WARN_MB * MB]

    if not rows:
        print(f"no tracked file is at or over {WARN_MB} MB")
        return 0

    print(f"{len(rows)} tracked files at or over {WARN_MB} MB "
          f"(GitHub refuses any push once one passes {HARD_MB} MB):")
    fatal = []
    for size, rel in rows:
        mb = size / MB
        print(f"  {mb:6.1f} MB  {rel}  ({describe(rel, index)})")
        if mb >= FAIL_MB:
            fatal.append((mb, rel))

    if not fatal:
        return 0
    for mb, rel in fatal:
        line = (f"{rel} is {mb:.1f} MB, within {HARD_MB - mb:.1f} MB of the "
                f"{HARD_MB} MB limit that refuses EVERY push to this repo")
        print(f"::error::{line}" if args.strict else f"WARNING: {line}")
    if args.strict:
        print("Shard it on a stable per-key rule, never a size-based split -- "
              "`SHARDS` in scripts/refresh-live-values.py is the worked example.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
