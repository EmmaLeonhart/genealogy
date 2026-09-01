"""Re-run stale generators in DEPENDENCY ORDER until the drift column stops moving.

    python scripts/refresh-drift.py --dry-run        # print the plan, run nothing
    python scripts/refresh-drift.py --max-age-hours 72

**Drift cascades, and that is what makes a hand-listed chain the wrong instrument.** On
2026-08-27 thirteen scripts were picked by eye and re-run; the count went 95 -> 80 rather than
95 -> 82, because refreshing a stage restales everything downstream of it. Three Bure topology
reports fell behind the roster that had just been rebuilt, `removal-batch-vintage.tsv` behind
the removal batch, `multi-geni-items.tsv` behind the shapes census. Each of those was a new row
that did not exist before the fix that caused it.

`build-repo-freshness` already knows every `generator -> input` edge. What it does not do is
order them, so this walks that graph instead of a list somebody typed.

## What it will and will not run

* **Only scripts that write something currently flagged.** A generator whose outputs are all
  current is never invoked.
* **Only offline scripts.** Anything naming `WikidataClient`, `full_entities`, `urllib.request`
  or `requests.` is skipped and reported. `CLAUDE.md` § *Never query Wikidata to check
  something* is not a thing to trust a topological sort with.
* **Only recent drift by default.** `--max-age-hours 72` keeps out the ~69 one-off analyses
  sitting 150-360h behind `out/merged.ged` -- the corpus grew under them and they are records of
  a day, not a to-do list. Pass a larger number deliberately.
* **A cycle is reported, never broken.** Two scripts each reading the other's output is a real
  thing to know about; picking an arbitrary order would hide it.

## Why it iterates

One pass in dependency order should be enough. It is run again anyway, up to `--rounds`, because
"should be" is how the last three defects in this area got shipped: the census is a heuristic
over path literals, and a generator it cannot see writes a file that then looks like it drifted
on its own. If round two still finds work, that gap is what it found.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
FRESHNESS = ROOT / "reports" / "repo-freshness.csv"

#: A script naming any of these talks to Wikidata and is never run from here.
NETWORK = ("WikidataClient", "full_entities", "urllib.request", "requests.")

AGE_RE = re.compile(r" is (\d+)h newer$")


def freshness_module():
    """`scripts/build-repo-freshness.py`, by path — the filename is hyphenated."""
    spec = importlib.util.spec_from_file_location(
        "_freshness", ROOT / "scripts" / "build-repo-freshness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


#: **`text=True` alone decodes as cp1252 on Windows and dies on the first Japanese name.**
#: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81` came out of a subprocess reader
#: thread on the first real run — not from the child, which was fine, but from this process
#: trying to read it. The reports are full of kana and Han, so this is the common case rather
#: than an edge one, and it is the same shape as `CLAUDE.md` § *Working on Windows here*.
RUN = dict(capture_output=True, text=True, encoding="utf-8", errors="replace")


#: Generators that REFUSE to run without a flag, and the flag they need.
#:
#: **Found 2026-09-01, and it had been failing silently every round.** `refresh-drift` invoked
#: `build-garborg-day.py` bare; that script answers *"this script only: --compose (the daily
#: algorithm) or --roster FILE"* and exits 1. So it failed in round 1, round 2 and round 3, its
#: outputs never came un-stale, and the run ended *"2 scripts still have stale outputs"* — a
#: refresher that could never refresh one of its own targets.
#:
#: The failure was visible in the log as `[FAIL] ... exit=1` and nothing acted on it, which is the
#: real lesson: the loop printed the error three times and carried on.
#:
#: **`--compose` and not `--roster`**, because `--compose` is the daily algorithm and the thing
#: whose outputs the drift graph is tracking. `--no-refresh` is deliberately NOT passed:
#: `CLAUDE.md` § *Regenerating QuickStatements ALWAYS regenerates the ledger* makes the ledger
#: refresh part of what running this script means.
NEWLINE = chr(10)

#: Generators that failed this run, so the summary can say why an output stayed stale.
failures = {}

REQUIRED_ARGS = {
    "scripts/build-garborg-day.py": ["--compose"],
}


def build_census() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build-repo-freshness.py")],
                   cwd=ROOT, check=True, **RUN)


def drift_rows(max_age: int) -> list[dict]:
    rows = []
    with open(FRESHNESS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            note = row.get("stale_against_input") or ""
            m = AGE_RE.search(note)
            if m and int(m.group(1)) <= max_age:
                rows.append(row)
    return rows


def offline(script_rel: str) -> bool:
    path = ROOT / script_rel
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return not any(marker in text for marker in NETWORK)


def plan(max_age: int):
    """`(order, skipped, cycles)` — the scripts to run, worst-first within a level."""
    mod = freshness_module()
    rows = drift_rows(max_age)
    if not rows:
        return [], [], []

    # generator -> the flagged outputs it is responsible for.
    #
    # **The `generator` column names any script that MENTIONS the file**, up to three of them,
    # so a reader lands there beside the real writer. Running a reader is not merely wasteful:
    # `build-synoptic-correspondence.py` reads `structural-walk-validation.tsv` and is a
    # ten-minute whole-corpus job that would be re-run for a file it does not produce. Confirm
    # with `writes_in` before believing the column.
    owns: dict[str, list[str]] = {}
    for row in rows:
        for script in (row.get("generator") or "").split(";"):
            script = script.replace("\\", "/").strip()
            if not script or not (ROOT / script).exists():
                continue
            text = (ROOT / script).read_text(encoding="utf-8", errors="replace")
            if Path(row["path"]).name in mod.writes_in(text):
                owns.setdefault(script, []).append(row["path"])

    skipped = [(s, "names a Wikidata client") for s in owns if not offline(s)]
    runnable = {s: o for s, o in owns.items() if offline(s)}

    # Which script produces which file, so an input can be traced to its producer.
    produces: dict[str, str] = {}
    for script in runnable:
        for name in mod.writes_in((ROOT / script).read_text(encoding="utf-8",
                                                            errors="replace")):
            for folder in ("reports", "out", "out/wikidata"):
                rel = f"{folder}/{name}"
                if (ROOT / rel).exists():
                    produces.setdefault(rel, script)
                    break

    # edge A -> B: B reads something A writes, so A runs first.
    after: dict[str, set[str]] = {s: set() for s in runnable}
    for script in runnable:
        for dep in mod.inputs_of(script):
            producer = produces.get(dep)
            if producer and producer != script and producer in runnable:
                after[script].add(producer)

    order, done = [], set()
    while True:
        ready = sorted(s for s in runnable
                       if s not in done and after[s] <= done)
        if not ready:
            break
        order.extend(ready)
        done.update(ready)
    cycles = sorted(set(runnable) - done)
    return [(s, runnable[s]) for s in order], skipped, cycles


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    # **A bare flag, checked.** `--check` was passed to another script here as though it were
    # one, was not, and the script silently did the real thing twice.
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and run nothing")
    ap.add_argument("--max-age-hours", type=int, default=72,
                    help="ignore drift older than this (default 72; the deep-history rows "
                         "are one-off analyses, not a to-do list)")
    ap.add_argument("--rounds", type=int, default=3,
                    help="re-plan and re-run this many times at most (default 3)")
    args = ap.parse_args()

    for round_no in range(1, args.rounds + 1):
        order, skipped, cycles = plan(args.max_age_hours)
        print(f"\n=== round {round_no}: {len(order)} scripts to run "
              f"(<= {args.max_age_hours}h drift) ===")
        for script, outputs in order:
            print(f"  {script}")
            for o in sorted(set(outputs))[:4]:
                print(f"      {o}")
        for script, why in skipped:
            print(f"  SKIP {script} — {why}")
        for script in cycles:
            print(f"  CYCLE {script} — reads something it also feeds; not ordered, not run")

        if not order:
            print("nothing left to re-run at this age threshold")
            return
        if args.dry_run:
            print("\n--dry-run: nothing was executed")
            return

        for script, _ in order:
            r = subprocess.run([sys.executable, str(ROOT / script)] + REQUIRED_ARGS.get(script, []),
                               cwd=ROOT, **RUN)
            tail = (r.stdout or r.stderr).strip().splitlines()
            print(f"  [{'ok ' if r.returncode == 0 else 'FAIL'}] {script}"
                  f"{'' if r.returncode == 0 else f' exit={r.returncode}'}"
                  f"{('  ' + tail[-1][:90]) if tail else ''}")
            if r.returncode != 0:
                failures[script] = (r.returncode, tail[-1][:120] if tail else '')
        build_census()

    order, _, _ = plan(args.max_age_hours)
    print(f"\nafter {args.rounds} rounds: {len(order)} scripts still have stale outputs")
    # **A generator that fails every round is the reason its outputs stay stale, and saying so
    # is the whole point.** Before 2026-09-01 the loop printed `[FAIL] ... exit=1` once per
    # round and the summary said only "2 scripts still have stale outputs", so a script that
    # could never succeed looked like one that was merely behind. Three identical failures went
    # past unremarked.
    if failures:
        print(f"{NEWLINE}{len(failures)} generator(s) FAILED, so their outputs cannot come "
              f"un-stale until that is fixed:")
        for script, (code, msg) in sorted(failures.items()):
            print(f"   exit={code}  {script}")
            if msg:
                print(f"            {msg}")


if __name__ == "__main__":
    main()
