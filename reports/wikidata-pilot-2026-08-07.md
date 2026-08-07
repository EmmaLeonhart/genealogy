# Wikidata download — the 1000-item pilot

**2026-08-07.** `python -m genimerge wikidata-download --limit 1000`, the first
request this repo has ever made to `wbgetentities`. Written by hand from the
command's own output rather than generated, because it is one run and the point
is the decision it feeds, not a report to re-render.

## What happened

| | |
| --- | --- |
| items stored | 1,000 |
| requests | 20 (50 QIDs each, as documented) |
| wall clock | 33s, at the default 1s between requests |
| rate | 30.4 items/s |
| **429s / retries** | **0** |
| missing QIDs | 0 |
| errors | 0 |
| JSON per item | 13,713 bytes uncompressed |
| on disk | 2.0 MB gzipped for the 1,000 — **~7:1** |

Seeding the fetch queue with all 514,822 P2600 QIDs takes 1.6s.

## What it projects to

Straight multiplication, and to be read as a **floor**: 33 seconds has not met
the throttling four hours will.

- **10,305 requests** for the seed set — the figure that made the ~100 GB JSON
  dump unnecessary.
- **~4.7 hours** at this rate, before any backoff.
- **7.1 GB** of JSON uncompressed, **~1.05 GB** as shards on disk — roughly 515
  files of 2 MB.

For the repo that means about **+1 GB**, against 1.1 GB of exports and a 230 MB
`.git` today. Comfortable against GitHub's limits, and incremental: each shard
is a separate small file, so pushes stay ordinary. No LFS.

## The one number that is not going to plan

**428 QIDs discovered from the first 1,000 items scanned** — 0.43 per item.

These are relatives named by P22/P25/P26/P40/P3373 that are **not in the P2600
seed set at all**, so they are the expansion frontier: people Wikidata records
and no Geni-linked item does. That is the thing the whole walk exists to reach.

It is also **larger than `todo.md` § 8a-revised predicts**. Emma's expectation
was a small, patchy frontier — most family edges landing on other seed-set items —
and § 8a-revised says in terms that a much-larger-than-expected frontier should be
treated as a symptom rather than a success. At 0.43 per item sustained, the
frontier would be **~220,000 items**, which is not patchy.

Three reasons not to act on that yet, in order of how much they'd explain:

1. **The walk has covered 0.19% of the seed set.** Every relative looks new when
   almost nothing is held. The rate should fall as coverage rises, and how fast
   it falls is the actual measurement.
2. **The seed file is QID-ascending, so the first 1,000 are the lowest QIDs** —
   the oldest, most-edited items on Wikidata, which skews heavily to royalty and
   nobility. Those have more recorded relatives, and more relatives who are
   notable without being on Geni, than a random 1,000 would.
3. **P3373 (sibling) is in the walk and is not in § 8a's list of four.** It was
   added on the argument that a sibling edge can be the only link on an item
   with unrecorded parents. If the frontier stays high, this is the first thing
   to measure the contribution of and the cheapest to drop.

**What to watch during the long run:** discovered-per-scanned over successive
progress lines. Falling steadily means the prediction holds and the frontier is
the tail. Flat near 0.4 means it does not, and the run is heading for a set half
again as large as the seed — worth stopping to understand rather than letting it
finish.

## Not measured

- **Sustained-rate behaviour.** Zero 429s in 20 requests says nothing about
  10,305. The backoff is in place and honours `Retry-After`; whether 1s between
  requests is sustainable is answered by the long run and nothing else.
- **Whether the seed list is clean.** Zero missing in 1,000 is a good sign for
  the 514,822 and not a claim about them.
