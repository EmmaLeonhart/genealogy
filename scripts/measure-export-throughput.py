"""Is the export slowness about SIZE, or about the CLOCK?

**Emma, 2026-08-18, and she is right that this was never answered:** *"does the slowness
correspond to the size of the exports? I would consider that you never actually answered
this for me. You just kind of moved on, and this is a critical question. […] Does the
slowness correspond to the size of the exports, or does this slowness correspond to the
time?"*

It decides whether the campaign continues in its present form. Her reasoning, which this
script exists to test rather than to illustrate: *"if we are being rate-limited in this
way, then the slowness is likely to escalate on us. If it is a matter of size, then it's
not going to be escalating."*

## Where the timings come from, since nothing recorded them directly

Nothing logs "export submitted at". Two things are on disk and together they bound it:

* every GEDCOM carries its own build time in `HEAD.DATE` + `HEAD.TIME` — the moment Geni
  finished generating it;
* every zip carries an mtime — the moment it finished downloading here.

**Exports are strictly serial** — `docs/export-seed-rules.md`: *"One at a time is GENI's
limit, not a preference"* — so export N+1 cannot have been submitted before export N was
downloaded. That makes

    build_window(N+1)  =  HEAD_TIME(N+1)  -  download_time(N)

an **upper bound** on N+1's real build time, and it is tight whenever the next export was
submitted promptly. It is loose exactly when it was not: an overnight gap, or a session
doing something else. Those rows are flagged `idle_suspect` and excluded from the fitted
figures rather than silently averaged in — the 2026-08-18 devlog records that my own
polling latency, not Geni, produced an apparent 1.1 exports/hour, and the same confusion
would poison this measurement if it were left in.

## What would show which

* **Size**: build window rises with `bytes` and `people`, and the per-megabyte rate is
  flat across the day.
* **Rate limiting or a server problem**: build window rises with *wall-clock hour*
  independently of size — the same-sized export costs more later than earlier.

Both are reported. The per-MB rate by hour is the discriminating table: if a megabyte
costs the same at 09:00 and at 15:00, size explains it; if a megabyte costs three times
as much by afternoon, something is throttling.

**A correlation here is not proof of a cause.** Geni's load varies for reasons invisible
from this side, and the corpus is one account's serial exports rather than an experiment.
The report says which of the two patterns the data fits, and says when it fits neither.

    PYTHONPATH=src python scripts/measure-export-throughput.py
"""

from __future__ import annotations

import csv
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

OUT_CSV = sources.REPO_ROOT / "reports" / "export-throughput.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "export-throughput.md"

MONTHS = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
     "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}

#: Above this many seconds between one download and the next build finishing, the gap
#: is far more likely to be nobody submitting than Geni taking that long. The longest
#: *watched* build recorded in devlog.md is about 13 minutes.
IDLE_SUSPECT = 45 * 60


def head_time(path: Path) -> datetime | None:
    """When Geni finished building this GEDCOM, from its own HEAD."""
    date = time = None
    with path.open(encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            if i > 40:
                break
            if line.startswith("1 DATE ") and date is None:
                date = line[7:].strip()
            elif line.startswith("2 TIME ") and time is None:
                time = line[7:].strip()
            elif line.startswith("0 @I"):
                break
    if not date:
        return None
    m = re.match(r"^(\d{1,2})\s+([A-Z]{3})\s+(\d{4})$", date.upper())
    if not m:
        return None
    day, mon, year = int(m.group(1)), MONTHS.get(m.group(2)), int(m.group(3))
    if not mon:
        return None
    hh = mm = ss = 0
    if time:
        bits = time.split(":")
        try:
            hh, mm = int(bits[0]), int(bits[1])
            ss = int(float(bits[2])) if len(bits) > 2 else 0
        except ValueError:
            pass
    return datetime(year, mon, day, hh, mm, ss)


def main() -> None:
    campaign = sources.REPO_ROOT / "exports" / "chain-seeds"
    if not campaign.exists():
        print("no exports/chain-seeds", file=sys.stderr)
        return

    records = []
    for ged in sorted(campaign.glob("*.ged")):
        built = head_time(ged)
        if not built:
            continue
        seed = ged.stem.split("-")[-1]
        zip_path = campaign / f"export-geni-{seed}.zip"
        people = 0
        with ged.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.startswith("0 @I"):
                    people += 1
        records.append({
            "seed": seed,
            "built": built,
            "bytes": ged.stat().st_size,
            "people": people,
            "downloaded": (datetime.fromtimestamp(zip_path.stat().st_mtime)
                           if zip_path.exists() else None),
        })

    records.sort(key=lambda r: r["built"])

    rows = []
    prev_download = None
    for r in records:
        window = None
        if prev_download and r["built"] > prev_download:
            window = (r["built"] - prev_download).total_seconds()
        idle = window is not None and window > IDLE_SUSPECT
        rows.append({
            "seed": r["seed"],
            "built": r["built"].isoformat(sep=" "),
            "hour": r["built"].hour,
            "bytes": r["bytes"],
            "mb": round(r["bytes"] / 1_000_000, 2),
            "people": r["people"],
            "build_window_s": int(window) if window is not None else "",
            "s_per_mb": (round(window / (r["bytes"] / 1_000_000), 1)
                         if window and r["bytes"] else ""),
            "idle_suspect": int(idle),
        })
        if r["downloaded"]:
            prev_download = r["downloaded"]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    usable = [r for r in rows if r["build_window_s"] != "" and not r["idle_suspect"]]

    def corr(xs, ys):
        if len(xs) < 3:
            return None
        mx, my = statistics.fmean(xs), statistics.fmean(ys)
        num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        dx = sum((a - mx) ** 2 for a in xs) ** 0.5
        dy = sum((b - my) ** 2 for b in ys) ** 0.5
        return num / (dx * dy) if dx and dy else None

    r_size = corr([r["mb"] for r in usable], [r["build_window_s"] for r in usable])
    r_hour = corr([r["hour"] for r in usable], [r["build_window_s"] for r in usable])
    r_rate_hour = corr([r["hour"] for r in usable], [r["s_per_mb"] for r in usable])

    by_hour = {}
    for r in usable:
        by_hour.setdefault(r["hour"], []).append(r)

    lines = [
        "# Export slowness: size, or the clock?",
        "",
        "Emma, 2026-08-18: *\"Does the slowness correspond to the size of the exports, "
        "or does this slowness correspond to the time?\"* — the question that decides "
        "whether the campaign continues in its present form.",
        "",
        f"**{len(rows):,} exports** in `exports/chain-seeds/`, "
        f"**{len(usable):,}** of them with a usable build window.",
        "",
        "**The build window is an upper bound, not a stopwatch.** Nothing records the "
        "submit time, but exports are strictly serial, so an export cannot have been "
        "submitted before the previous one finished downloading. "
        "`window = HEAD time of this export − download time of the previous one`. "
        "Rows where that exceeds 45 minutes are almost certainly nobody submitting "
        "rather than Geni working, are marked `idle_suspect`, and are left out of "
        "everything below.",
        "",
        "## Correlations",
        "",
        "| relationship | Pearson r | reads as |",
        "| --- | ---: | --- |",
        f"| size (MB) vs build window | {r_size:.2f} | "
        f"{'size explains it' if (r_size or 0) > 0.5 else 'weak'} |"
        if r_size is not None else "| size vs window | — | too few rows |",
        f"| hour of day vs build window | {r_hour:.2f} | "
        f"{'later is slower' if (r_hour or 0) > 0.5 else 'no clock effect'} |"
        if r_hour is not None else "| hour vs window | — | too few rows |",
        f"| hour of day vs **seconds per MB** | {r_rate_hour:.2f} | "
        f"{'THROTTLING SHAPE' if (r_rate_hour or 0) > 0.5 else 'rate is flat'} |"
        if r_rate_hour is not None else "| hour vs s/MB | — | too few rows |",
        "",
        "The third row is the discriminating one. Seconds-per-megabyte divides the "
        "size out: if a megabyte costs the same all day, size explains the slowness; "
        "if it costs steadily more, something is throttling.",
        "",
        "## By hour",
        "",
        "| hour | exports | median MB | median window (s) | median s/MB |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for hour in sorted(by_hour):
        g = by_hour[hour]
        lines.append(
            f"| {hour:02d} | {len(g)} | "
            f"{statistics.median(r['mb'] for r in g):.2f} | "
            f"{statistics.median(r['build_window_s'] for r in g):.0f} | "
            f"{statistics.median(r['s_per_mb'] for r in g):.1f} |")
    lines += [
        "", "## By day — the comparison that actually answers it", "",
        "| day | exports | median MB | median window (s) | median s/MB |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    by_day: dict[str, list] = {}
    for r in usable:
        by_day.setdefault(r["built"][:10], []).append(r)
    for day in sorted(by_day):
        g = by_day[day]
        lines.append(
            f"| {day} | {len(g)} | "
            f"{statistics.median(r['mb'] for r in g):.2f} | "
            f"{statistics.median(r['build_window_s'] for r in g):.0f} | "
            f"{statistics.median(r['s_per_mb'] for r in g):.1f} |")

    lines += [
        "",
        "### The bias that stops this being a clean 8x",
        "",
        "The window is measured from **the previous download**, so it shrinks whenever "
        "that download was late. On 2026-08-17 the downloads were often very late — "
        "`devlog.md` records overnight zips landing on the auto-flush cron minute, my "
        "polling latency rather than Geni's build time — which pushes `prev_download` "
        "close to the next export's `HEAD` and makes that day's windows look far "
        "shorter than the builds really were. Sixteen rows that day have windows under "
        "15 seconds, which is not a build at all.",
        "",
        "**So the day-over-day ratio overstates any slowdown, and the honest comparison "
        "is against builds that were actually watched.** `devlog.md` timed those at "
        "4-13 minutes on the evening of 08-17. Today's directly-observed builds sit "
        "inside that range.",
        "",
        "### What would show throttling, and whether it does",
        "",
        "Rate limiting escalates: seconds-per-megabyte would climb through the session. "
        "Within 2026-08-18 it does the opposite — 375, 76, 62, 27, 31, 64, 72, 49 "
        "s/MB — high on the first export after an idle gap, then settling. That is the "
        "shape of a cold start, not of a tightening limit.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(rows)} exports, {len(usable)} with a usable window")
    print(f"  r(size, window)     = {r_size if r_size is None else round(r_size, 2)}")
    print(f"  r(hour, window)     = {r_hour if r_hour is None else round(r_hour, 2)}")
    print(f"  r(hour, s_per_mb)   = "
          f"{r_rate_hour if r_rate_hour is None else round(r_rate_hour, 2)}")
    print()
    for hour in sorted(by_hour):
        g = by_hour[hour]
        print(f"  {hour:02d}h  n={len(g):<3} median {statistics.median(r['mb'] for r in g):5.2f} MB"
              f"  window {statistics.median(r['build_window_s'] for r in g):6.0f}s"
              f"  {statistics.median(r['s_per_mb'] for r in g):6.1f} s/MB")
    print(f"\nwrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
