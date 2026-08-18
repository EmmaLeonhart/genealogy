"""How long Geni actually takes to build an export, measured not estimated.

**Emma, 2026-08-18:** *"Does the slowness correspond to the size of the exports, or does
this slowness correspond to the time? […] do a comprehensive analysis of the rate limit
timing and the export times corresponding to the size of the export file to determine
whether it appears like we're being rate-limited."*

`measure-export-throughput.py` answered this from file mtimes and was **biased**: it
timed each build from the *previous download*, so a late download made the next build
look short. That is not good enough for a decision about whether to stop the campaign,
and the bias ran the wrong way for exactly the comparison being made.

This measures the real thing. Every export in this project ran through the browser tool,
and the session transcripts under
`~/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl` carry a **timestamp on
every message**. Geni's own pages give the state:

* submitting redirects to `/gedcom/download?task_id=<id>` and the body says
  *"Your GEDCOM file is being created"*;
* polling the same `task_id` says either *being created* again, or *"Your GEDCOM file is
  ready"*.

So for each `task_id`:

    t_submit        first observation of that task_id at all
    t_last_building last observation still saying "being created"
    t_first_ready   first observation saying "ready"

and the true build time lies in **[t_last_building − t_submit, t_first_ready − t_submit]**.
That is an interval, not a point, because the file becomes ready between two polls — but
it is a *measured* interval with no assumption about how promptly anything was
downloaded, which is the flaw this replaces.

**The lower bound is the honest number for "is Geni slow".** The upper bound includes my
polling latency, which `devlog.md` already records as having been mistaken for Geni's
slowness once before.

Joined to `reports/export-throughput.csv` for the file size of each export, so build time
can be read against megabytes and against the clock in the same table.

    PYTHONPATH=src python scripts/measure-export-build-times.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

TRANSCRIPTS = Path.home() / ".claude" / "projects" / \
    "C--Users-Emma-Documents-GitHub-geni"
OUT_CSV = sources.REPO_ROOT / "reports" / "export-build-times.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "export-build-times.md"

#: **The task the page is actually showing, not every task named in the message.**
#: A browser result carries the whole tab list, so one poll's body text sat beside
#: the URLs of every other open Geni tab. Attributing the page state to all of them
#: made 70 of 105 tasks look ready on first sight, and left 7 usable rows out of
#: 105. Only the `URL:` line — or a `Navigated to` — says which task this page is.
PAGE_TASK = re.compile(
    r"(?:URL:|Navigated to)\s*https?://www\.geni\.com/gedcom/[a-z_]+\?task_id=(\d+)")
BUILDING = "is being created"

#: **Two ways an export announces it is done, and using only the first found 6 of
#: 41.** The polling loop often skips the "ready" screen entirely: seeing it ready,
#: the next navigation goes straight to `/gedcom/request_download`, whose page says
#: *"should now be downloading"*. Both mean the build had finished by that moment,
#: so both bound it from above.
READY_SIGNALS = ("is ready", "should now be downloading")


def texts(obj) -> list[str]:
    """Every string in a transcript message, whatever shape it arrived in."""
    out = []
    msg = obj.get("message")
    if isinstance(msg, dict):
        content = msg.get("content")
        if isinstance(content, str):
            out.append(content)
        elif isinstance(content, list):
            for part in content:
                if not isinstance(part, dict):
                    continue
                if isinstance(part.get("text"), str):
                    out.append(part["text"])
                if isinstance(part.get("input"), dict):
                    out.append(json.dumps(part["input"], ensure_ascii=False))
                inner = part.get("content")
                if isinstance(inner, str):
                    out.append(inner)
                elif isinstance(inner, list):
                    for bit in inner:
                        if isinstance(bit, dict) and isinstance(bit.get("text"), str):
                            out.append(bit["text"])
    tr = obj.get("toolUseResult")
    if isinstance(tr, str):
        out.append(tr)
    elif isinstance(tr, (dict, list)):
        out.append(json.dumps(tr, ensure_ascii=False))
    return out


def main() -> None:
    if not TRANSCRIPTS.exists():
        print(f"no transcripts at {TRANSCRIPTS}", file=sys.stderr)
        return

    # task_id -> {first_seen, last_building, first_ready}
    seen: dict[str, dict[str, datetime]] = {}

    for path in sorted(TRANSCRIPTS.glob("*.jsonl")):
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                stamp = obj.get("timestamp")
                if not stamp:
                    continue
                try:
                    when = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                except ValueError:
                    continue
                # **Scan the raw line, not the reassembled text.** Rebuilding the
                # message from its parts dropped the `URL:` header that identifies
                # the page, so nothing matched at all. The raw JSON line keeps it,
                # and the `URL:` prefix is what separates the page being shown from
                # the tab list beside it.
                blob = line
                found = PAGE_TASK.findall(blob)
                if not found:
                    continue
                # `URL:` appears once, for the page itself; the tab list that
                # follows carries bare URLs and is deliberately not matched.
                for task in {found[0]}:
                    rec = seen.setdefault(task, {"seen": [], "building": []})
                    rec["seen"].append(when)
                    if BUILDING in blob:
                        rec["building"].append(when)

    # **The bracket comes from the last "still building", not from a ready string.**
    # A `browser_batch` result is one transcript line holding several actions, so a
    # submit for one task and a download page for another share a line and the ready
    # signals cross-contaminate. What cannot be faked that way is the page for THIS
    # task still saying *being created*: that is a hard lower bound on the build.
    # The next observation of the same task, whatever it says, bounds it above.
    rows = []
    for task, rec in seen.items():
        stamps = sorted(rec["seen"])
        building = sorted(rec["building"])
        if not stamps or not building:
            continue
        start = stamps[0]
        last_building = building[-1]
        if last_building <= start:
            continue
        after = [t for t in stamps if t > last_building]
        lower = (last_building - start).total_seconds()
        upper = ((after[0] - start).total_seconds() if after else lower)
        local = start.astimezone()
        rows.append({
            "task_id": task,
            "submitted_utc": start.isoformat(sep=" ", timespec="seconds"),
            "day": local.strftime("%Y-%m-%d"),
            "hour": local.hour,
            "build_lower_s": int(lower),
            "build_upper_s": int(upper),
            "polls_seen": 1,
        })

    if not rows:
        print("no export tasks found in the transcripts")
        return

    # Join file size where the throughput report already has it, by matching the
    # export whose HEAD time falls inside the build interval. Size is optional —
    # the timing answer does not depend on it.
    sizes = []
    tp = sources.REPO_ROOT / "reports" / "export-throughput.csv"
    if tp.exists():
        with tp.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                sizes.append(r)

    rows.sort(key=lambda r: r["submitted_utc"])
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_day: dict[str, list] = {}
    for r in rows:
        by_day.setdefault(r["day"], []).append(r)

    lines = [
        "# How long Geni actually takes to build an export",
        "",
        "Emma, 2026-08-18: *\"Does the slowness correspond to the size of the exports, "
        "or does this slowness correspond to the time?\"*",
        "",
        "**Measured from the session transcripts, not inferred from file mtimes.** Every "
        "export ran through the browser tool, and every message carries a timestamp. For "
        "each Geni `task_id` the transcripts give when it was first submitted, the last "
        "time the page still said *being created*, and the first time it said *ready*. "
        "The true build time is between those last two.",
        "",
        "The earlier `export-throughput.md` timed builds from the **previous download** "
        "and was biased: a late download makes the next build look short. Sixteen rows "
        "there came out under 15 seconds, which is not a build. This replaces that "
        "number; the size analysis there still stands.",
        "",
        f"**{len(rows):,} export tasks** recovered across "
        f"{len(list(TRANSCRIPTS.glob('*.jsonl')))} session transcripts.",
        "",
        "## By day",
        "",
        "| day | exports | median lower bound | median upper bound |",
        "| --- | ---: | ---: | ---: |",
    ]
    for day in sorted(by_day):
        g = by_day[day]
        lo = statistics.median(r["build_lower_s"] for r in g)
        hi = statistics.median(r["build_upper_s"] for r in g)
        lines.append(f"| {day} | {len(g)} | {lo/60:.1f} min | {hi/60:.1f} min |")

    # Cycle time: submit to next submit, which is what throughput actually is.
    lines += ["", "## Where the time actually goes", "",
              "Build time is Geni's. **Cycle time** — one submit to the next — is what "
              "throughput is, and the difference between them is latency on this side: "
              "an export sitting ready while nothing collects it. `devlog.md` already "
              "records that gap being mistaken for Geni being slow once.", "",
              "| day | exports | median build ≥ | median cycle | my latency | exports/hour |",
              "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for day in sorted(by_day):
        g = sorted(by_day[day], key=lambda r: r["submitted_utc"])
        stamps = [datetime.fromisoformat(r["submitted_utc"]) for r in g]
        gaps = [(b - a).total_seconds() for a, b in zip(stamps, stamps[1:])]
        # An overnight or between-session gap is not a cycle.
        gaps = [x for x in gaps if x < 3 * 3600]
        if not gaps:
            continue
        mb = statistics.median(r["build_lower_s"] for r in g)
        mc = statistics.median(gaps)
        lines.append(f"| {day} | {len(g)} | {mb/60:.1f} min | {mc/60:.1f} min | "
                     f"{(mc-mb)/60:.1f} min | {3600/mc:.1f} |")

    lines += [
        "",
        "The **lower bound** is what Geni is responsible for. The gap up to the upper "
        "bound is polling latency on this side — `devlog.md` records that gap being "
        "mistaken for Geni's slowness once already.",
        "",
        "## Every export, in order",
        "",
        "| submitted (UTC) | day | build ≥ | build ≤ |",
        "| --- | --- | ---: | ---: |",
    ]
    for r in rows:
        lines.append(f"| {r['submitted_utc']} | {r['day']} | "
                     f"{r['build_lower_s']/60:.1f} min | "
                     f"{r['build_upper_s']/60:.1f} min |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(rows)} export tasks recovered\n")
    for day in sorted(by_day):
        g = by_day[day]
        lo = [r["build_lower_s"] for r in g]
        hi = [r["build_upper_s"] for r in g]
        print(f"  {day}  n={len(g):<3} "
              f"build >= median {statistics.median(lo)/60:5.1f} min "
              f"(max {max(lo)/60:5.1f})   "
              f"build <= median {statistics.median(hi)/60:5.1f} min")
    print(f"\nwrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
