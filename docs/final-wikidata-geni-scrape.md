# `final-wikidata-geni-scrape`

**The task, named by Emma 2026-09-06.** Walk the Geni profiles this project cares about, take from
each one the things the collector can take, and turn every one of them into a **tiny GEDCOM** that
merges into the synoptic tree on the Geni id.

**It cannot start until the extension and these deliverables are good** — her words: *"The scrape
is to be done with the extension we built yesterday and it can only be done after we have a
coherent idea of the deliverables."* § *NOT SETTLED* below is that gate, and it is not
decoration: nothing the extension writes can reach disk today.

## What it covers

| population | count | source |
| --- | ---: | --- |
| every member of every sibling pair | **2,527** unscraped of 2,528 | `reports/sibling-pair-worklist.tsv` |
| the isolate path pilot | 82 of 100 remaining | `reports/isolate-path-pilot.tsv` |
| legacy saved pages already on disk | **1,555** | `geni-scraping/` |
| the full isolate campaign the pilot decides | 185,327 | `reports/isolate-path-pilot-urls.txt` is the sample |

## Why it is called final

Because after it there is nothing further to take off a Geni page: the immediate family, the
relationship path, and the statistics block are the whole of what a profile exposes. What follows
is merging and then Wikidata authoring, not more collection.

---

**Emma, 2026-09-06:** *"The scrape is to be done with the extension we built yesterday and it can
only be done after we have a coherent idea of the deliverables."*

Written because the deliverable moved three times in one day — a TSV, then a tiny GEDCOM with `NN`
placeholder parents, then a tiny GEDCOM with absent slots — while collection carried on through
all three. Nothing more is scraped until this is right.

## SETTLED — her words, this session

**Two distinct operations.** *"There's two distinct operations. Paths and profiles. Both ought to
make tiny gedcoms for each path or individual. Both have similar information. Many saved pages
have the info to make both tiny gedcoms from them."*

| operation | unit | one file per |
| --- | --- | --- |
| **profiles** | a person's immediate family | person |
| **paths** | a relationship path | path |

**The output is thousands of tiny GEDCOMs, and that shape is the point.** *"you didn't understand
that thousands of tiny gedcom files was the signal."* Not two aggregate files. The granularity is
what distinguishes this from the earlier incomplete attempt.

**GEDCOM is the native format.** *"for all intents and purposes the native format of this project
is the gedcom now."* A `.ged` under `exports/` is read recursively by `genimerge.sources`, so it
reaches the synoptic tree with no wiring.

**Geni ids are the entity resolution.** *"with the geni ids set up so that they end up getting
merged in ... the entity resolution in them means they significantly link things together."* Every
`INDI` xref is a Geni id, so the merge is an exact join and these files fuse into the tree.

**An unknown parent is an ABSENT SLOT, not a person.** Her ruling, chosen between the two
readings. A sibling pair with no known parents is a `FAM` with two `CHIL` and no `HUSB`/`WIFE`.
This supersedes her 2026-08-29 *"Both parents are 'NN' placeholders"*.

**Every member of every sibling pair gets the profile scrape, and the redundancy is deliberate.**
*"every single sibling pair gets the small scrape done on it ... I know this is slightly
redundant, but I'm telling you to do it."* Because: *"it'll create a gedcom for each one of the
members of the sibling pair, and then this links them as siblings with their parents in this new
gedcom file, but they're also linked as siblings in the path gedcom files."* The path GEDCOM says
*siblings, parents unknown*; each member's profile GEDCOM carries the real parents; the merge
fuses all three on the Geni id.

**The extension does the scraping.** *"The scrape is to be done with the extension we built
yesterday."* Not agentically, and not by hand-carrying data through tool results — which
double-encoded 4 of 14 scrapes before it was caught.

## BUILT

`scripts/build-tiny-gedcoms.py` — both operations, absent slots, zero invented people. Currently
13 profile GEDCOMs from `geni-families/*.tsv` and 694 path GEDCOMs from `paths/*.tsv`, 28,648
`INDI` lines.

`scripts/sibling-pair-worklist.py` — 2,130 pairs, 2,528 distinct people, 2,527 with no scrape.

## NOT SETTLED — these gate the scrape

1. **How the extension writes the files.** It holds the TSV in the tab. `chrome.downloads` from
   the background is not subject to the content setting that blocks an `<a download>` click, so
   the collector can write to disk — but the background service worker has never updated and that
   needs a reload at `chrome://extensions`. Until then nothing the extension writes can land, and
   hand-transport is barred.

2. **The 1,555 legacy saved pages in `geni-scraping/`.** She said the emitter should run on
   *"legacy scrapings and with the new scrapings by the extension"*. Nothing in
   `build-tiny-gedcoms.py` reads them. Only `build-scraped-gedcom.py` does, and its output uses
   the superseded `NN` placeholders.

3. **What happens to `scraped-pages.ged` and `scraped-paths.ged`.** Two aggregate files in the
   merge carrying 4,928 `NN` people, which the absent-slot ruling says should not exist. Removing
   them changes every merge.

4. **Whether path GEDCOMs should also come from saved pages.** *"Many saved pages have the info to
   make both tiny gedcoms from them."* Today paths come only from `paths/*.tsv`.
