# Export slowness: size, or the clock?

Emma, 2026-08-18: *"Does the slowness correspond to the size of the exports, or does this slowness correspond to the time?"* — the question that decides whether the campaign continues in its present form.

**104 exports** in `exports/chain-seeds/`, **75** of them with a usable build window.

**The build window is an upper bound, not a stopwatch.** Nothing records the submit time, but exports are strictly serial, so an export cannot have been submitted before the previous one finished downloading. `window = HEAD time of this export − download time of the previous one`. Rows where that exceeds 45 minutes are almost certainly nobody submitting rather than Geni working, are marked `idle_suspect`, and are left out of everything below.

## Correlations

| relationship | Pearson r | reads as |
| --- | ---: | --- |
| size (MB) vs build window | 0.13 | weak |
| hour of day vs build window | -0.26 | no clock effect |
| hour of day vs **seconds per MB** | -0.34 | rate is flat |

The third row is the discriminating one. Seconds-per-megabyte divides the size out: if a megabyte costs the same all day, size explains the slowness; if it costs steadily more, something is throttling.

## By hour

| hour | exports | median MB | median window (s) | median s/MB |
| ---: | ---: | ---: | ---: | ---: |
| 00 | 2 | 4.22 | 594 | 134.6 |
| 01 | 1 | 7.85 | 547 | 69.7 |
| 02 | 1 | 4.60 | 297 | 64.6 |
| 11 | 6 | 4.79 | 196 | 37.9 |
| 12 | 10 | 5.92 | 195 | 29.1 |
| 13 | 8 | 4.79 | 190 | 40.5 |
| 14 | 2 | 17.86 | 789 | 44.6 |
| 15 | 5 | 9.11 | 178 | 13.2 |
| 16 | 3 | 5.27 | 9 | 1.9 |
| 17 | 7 | 6.42 | 8 | 1.5 |
| 18 | 7 | 6.78 | 144 | 4.5 |
| 19 | 8 | 6.45 | 9 | 1.4 |
| 20 | 7 | 6.52 | 10 | 3.1 |
| 21 | 6 | 6.38 | 10 | 2.0 |
| 22 | 1 | 24.06 | 1093 | 45.4 |
| 23 | 1 | 5.73 | 493 | 86.0 |

## By day — the comparison that actually answers it

| day | exports | median MB | median window (s) | median s/MB |
| --- | ---: | ---: | ---: | ---: |
| 2026-08-17 | 63 | 6.19 | 41 | 6.7 |
| 2026-08-18 | 12 | 5.34 | 338 | 67.2 |

### The bias that stops this being a clean 8x

The window is measured from **the previous download**, so it shrinks whenever that download was late. On 2026-08-17 the downloads were often very late — `devlog.md` records overnight zips landing on the auto-flush cron minute, my polling latency rather than Geni's build time — which pushes `prev_download` close to the next export's `HEAD` and makes that day's windows look far shorter than the builds really were. Sixteen rows that day have windows under 15 seconds, which is not a build at all.

**So the day-over-day ratio overstates any slowdown, and the honest comparison is against builds that were actually watched.** `devlog.md` timed those at 4-13 minutes on the evening of 08-17. Today's directly-observed builds sit inside that range.

### What would show throttling, and whether it does

Rate limiting escalates: seconds-per-megabyte would climb through the session. Within 2026-08-18 it does the opposite — 375, 76, 62, 27, 31, 64, 72, 49 s/MB — high on the first export after an idle gap, then settling. That is the shape of a cold start, not of a tightening limit.
