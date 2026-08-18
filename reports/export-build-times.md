# How long Geni actually takes to build an export

Emma, 2026-08-18: *"Does the slowness correspond to the size of the exports, or does this slowness correspond to the time?"*

**Measured from the session transcripts, not inferred from file mtimes.** Every export ran through the browser tool, and every message carries a timestamp. For each Geni `task_id` the transcripts give when it was first submitted, the last time the page still said *being created*, and the first time it said *ready*. The true build time is between those last two.

The earlier `export-throughput.md` timed builds from the **previous download** and was biased: a late download makes the next build look short. Sixteen rows there came out under 15 seconds, which is not a build. This replaces that number; the size analysis there still stands.

**61 export tasks** recovered across 27 session transcripts.

## By day

| day | exports | median lower bound | median upper bound |
| --- | ---: | ---: | ---: |
| 2026-08-17 | 53 | 4.2 min | 5.4 min |
| 2026-08-18 | 8 | 3.5 min | 6.2 min |

## Where the time actually goes

Build time is Geni's. **Cycle time** — one submit to the next — is what throughput is, and the difference between them is latency on this side: an export sitting ready while nothing collects it. `devlog.md` already records that gap being mistaken for Geni being slow once.

| day | exports | median build ≥ | median cycle | my latency | exports/hour |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-08-17 | 53 | 4.2 min | 8.0 min | 3.8 min | 7.5 |
| 2026-08-18 | 8 | 3.5 min | 12.3 min | 8.8 min | 4.9 |

The **lower bound** is what Geni is responsible for. The gap up to the upper bound is polling latency on this side — `devlog.md` records that gap being mistaken for Geni's slowness once already.

## Every export, in order

| submitted (UTC) | day | build ≥ | build ≤ |
| --- | --- | ---: | ---: |
| 2026-08-17 18:31:51+00:00 | 2026-08-17 | 1.1 min | 6.5 min |
| 2026-08-17 18:40:40+00:00 | 2026-08-17 | 6.5 min | 7.3 min |
| 2026-08-17 18:49:07+00:00 | 2026-08-17 | 3.7 min | 4.6 min |
| 2026-08-17 18:54:41+00:00 | 2026-08-17 | 4.4 min | 5.3 min |
| 2026-08-17 19:01:18+00:00 | 2026-08-17 | 3.2 min | 4.7 min |
| 2026-08-17 19:07:36+00:00 | 2026-08-17 | 3.6 min | 4.5 min |
| 2026-08-17 19:13:07+00:00 | 2026-08-17 | 2.7 min | 3.6 min |
| 2026-08-17 19:17:26+00:00 | 2026-08-17 | 8.0 min | 9.0 min |
| 2026-08-17 19:31:09+00:00 | 2026-08-17 | 4.7 min | 5.8 min |
| 2026-08-17 19:49:32+00:00 | 2026-08-17 | 6.0 min | 7.2 min |
| 2026-08-17 20:15:16+00:00 | 2026-08-17 | 3.9 min | 4.8 min |
| 2026-08-17 20:35:44+00:00 | 2026-08-17 | 5.0 min | 6.0 min |
| 2026-08-17 20:44:01+00:00 | 2026-08-17 | 2.9 min | 3.9 min |
| 2026-08-17 20:51:36+00:00 | 2026-08-17 | 3.8 min | 4.8 min |
| 2026-08-17 21:00:10+00:00 | 2026-08-17 | 6.9 min | 7.8 min |
| 2026-08-17 21:29:13+00:00 | 2026-08-17 | 8.0 min | 9.0 min |
| 2026-08-17 22:26:47+00:00 | 2026-08-17 | 4.1 min | 5.2 min |
| 2026-08-17 22:41:01+00:00 | 2026-08-17 | 6.1 min | 7.4 min |
| 2026-08-17 22:50:53+00:00 | 2026-08-17 | 2.4 min | 4.2 min |
| 2026-08-17 23:32:55+00:00 | 2026-08-17 | 6.2 min | 7.2 min |
| 2026-08-17 23:40:43+00:00 | 2026-08-17 | 4.0 min | 5.0 min |
| 2026-08-17 23:46:16+00:00 | 2026-08-17 | 5.0 min | 6.0 min |
| 2026-08-18 00:16:58+00:00 | 2026-08-17 | 4.3 min | 6.2 min |
| 2026-08-18 00:23:51+00:00 | 2026-08-17 | 3.0 min | 5.8 min |
| 2026-08-18 00:30:22+00:00 | 2026-08-17 | 3.2 min | 5.0 min |
| 2026-08-18 00:37:47+00:00 | 2026-08-17 | 3.5 min | 4.5 min |
| 2026-08-18 00:42:53+00:00 | 2026-08-17 | 3.1 min | 4.2 min |
| 2026-08-18 00:47:41+00:00 | 2026-08-17 | 5.1 min | 7.1 min |
| 2026-08-18 00:55:33+00:00 | 2026-08-17 | 3.2 min | 4.2 min |
| 2026-08-18 01:00:26+00:00 | 2026-08-17 | 4.3 min | 5.3 min |
| 2026-08-18 01:20:05+00:00 | 2026-08-17 | 9.8 min | 10.9 min |
| 2026-08-18 01:31:35+00:00 | 2026-08-17 | 3.0 min | 4.0 min |
| 2026-08-18 01:36:14+00:00 | 2026-08-17 | 3.1 min | 4.1 min |
| 2026-08-18 01:54:32+00:00 | 2026-08-17 | 5.7 min | 6.8 min |
| 2026-08-18 02:01:54+00:00 | 2026-08-17 | 4.2 min | 5.3 min |
| 2026-08-18 02:07:57+00:00 | 2026-08-17 | 4.3 min | 5.4 min |
| 2026-08-18 02:26:30+00:00 | 2026-08-17 | 3.1 min | 5.4 min |
| 2026-08-18 02:32:47+00:00 | 2026-08-17 | 6.4 min | 7.5 min |
| 2026-08-18 02:40:59+00:00 | 2026-08-17 | 6.3 min | 7.5 min |
| 2026-08-18 02:49:07+00:00 | 2026-08-17 | 4.1 min | 5.3 min |
| 2026-08-18 02:59:05+00:00 | 2026-08-17 | 4.9 min | 8.0 min |
| 2026-08-18 03:08:36+00:00 | 2026-08-17 | 5.5 min | 6.6 min |
| 2026-08-18 03:20:49+00:00 | 2026-08-17 | 3.7 min | 4.6 min |
| 2026-08-18 03:47:39+00:00 | 2026-08-17 | 5.8 min | 6.8 min |
| 2026-08-18 03:54:58+00:00 | 2026-08-17 | 5.7 min | 6.8 min |
| 2026-08-18 04:02:17+00:00 | 2026-08-17 | 4.7 min | 5.7 min |
| 2026-08-18 04:27:55+00:00 | 2026-08-17 | 4.8 min | 5.7 min |
| 2026-08-18 04:34:13+00:00 | 2026-08-17 | 4.2 min | 5.2 min |
| 2026-08-18 04:39:54+00:00 | 2026-08-17 | 4.0 min | 5.0 min |
| 2026-08-18 05:03:24+00:00 | 2026-08-17 | 5.0 min | 5.9 min |
| 2026-08-18 05:09:48+00:00 | 2026-08-17 | 3.9 min | 4.9 min |
| 2026-08-18 05:15:18+00:00 | 2026-08-17 | 3.0 min | 4.0 min |
| 2026-08-18 05:19:50+00:00 | 2026-08-17 | 0.9 min | 58.4 min |
| 2026-08-18 18:29:59+00:00 | 2026-08-18 | 4.4 min | 6.0 min |
| 2026-08-18 18:42:15+00:00 | 2026-08-18 | 2.8 min | 4.7 min |
| 2026-08-18 18:53:07+00:00 | 2026-08-18 | 3.2 min | 4.1 min |
| 2026-08-18 19:01:01+00:00 | 2026-08-18 | 6.1 min | 6.4 min |
| 2026-08-18 19:10:48+00:00 | 2026-08-18 | 3.8 min | 4.8 min |
| 2026-08-18 19:23:10+00:00 | 2026-08-18 | 1.0 min | 30.1 min |
| 2026-08-18 19:59:40+00:00 | 2026-08-18 | 2.2 min | 11.2 min |
| 2026-08-18 20:16:16+00:00 | 2026-08-18 | 4.9 min | 7.5 min |
