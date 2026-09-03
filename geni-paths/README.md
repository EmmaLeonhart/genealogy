# `geni-paths/` — saved Geni `/path/` pages

**Emma's idea, 2026-09-02:** *"what if we mass exported the paths to the disconnected
wikidata people on geni? … the mass export of the path lists might be feasible and help
with getting wikidata generally connected even if we have a bunch of 'sinews' only linking
people in."*

A relationship path names people **whether or not any export has reached them**, so a path
to an isolated Wikidata item is a chain that joins that item to the graph without exporting
its neighbourhood. That chain is the sinew.

## What to fetch

The path is a **URL**, not a page save with a click. Both types per target, her call:

```
https://www.geni.com/path/x?from=6000000002457013227&path_type=blood&to=<geni id>
https://www.geni.com/path/x?from=6000000002457013227&path_type=inlaw&to=<geni id>
```

The slug between `/path/` and `?` is cosmetic.

**`from` is CHARLEMAGNE** — `6000000002457013227`, `Q3044`. Emma, 2026-09-03: *"I believe
Charlemagne is the most central person in the Jenny graph, so it would be going through
Charlemagne. We pin relationships to Charlemagne, and we go to each individual."* That
pinning is Geni's own pushpin — the saved pages carry
`toggleRelationshipAnchor(<id>)` with the tooltip *"Click this push pin to find relationships
from this profile to other profiles"* — and `from=` is how the anchor is expressed in the URL.

**The anchor applies to NEW paths only.** Emma, 2026-09-03: *"a bunch of the paths are from an
individual to me, and that's 100% fine and they are to be filled in I just mean new ones."* So
the 663 Emma-anchored paths in `paths/isolate-geni-*.tsv` are **live work**, not a superseded
dataset — they get filled in exactly as they always were. Charlemagne is where the anchor sits
for paths fetched from here on, and nothing about it retires an existing one.

`reports/isolate-path-pilot-urls.txt` is the fetch list; `reports/isolate-path-pilot.tsv`
is the same thing with the qid and label beside it.

## How to save

The blob capture `geni-scraping/README.md` describes — a download of the page's own
`document.documentElement.outerHTML` — named **`<geni id>-<blood|inlaw>.html`** so the two
types do not collide. No "complete webpage" saves: the `_files` asset directories are
**96% of the 2.8 GB** in `paths_for_wikidata_isolates/` and carry nothing. The HTML alone is
170 KB a page; the extracted TSV is ~4 KB.

## Rate

One a minute, no concurrency, **bail immediately on anything suspicious** — the same rule as
`geni-scraping/`. 185,327 targets is 27 days at her measured 4.7 profiles a minute, which is
why the pilot runs first.

## Then

```
python scripts/harvest-isolate-paths.py --write-paths
```

→ `reports/isolate-path-pilot-results.tsv`. Her own batches ran **34–39%** for
occupation-filtered academics and **92%** for Nordic ones; where a uniform sample lands decides
whether the full campaign is worth its request budget.

## "Not related to" does NOT mean not related

**Emma, 2026-09-03:** *"not related to is not actually a statement that the person is not
related. It superficially appears that way, but it is not that way. It sometimes gives a not
related to from a query timeout."*

So the column is `chain_found`, never `reached` and never `related`. A blank chain measures
Geni's query budget, not Geni's content — reading it otherwise is the `CLAUDE.md` § *"Is X
present?"* failure in a new costume.

**The timeout carries information the other way.** It *"usually indicates that the person is
very eccentric on the World Tree graph"*, and there are *"plenty of people that have verifiable
relationships but which it does not show up for."*

**The route for those, for high-value targets only because it is slow.** Build a seed
individual from the person's ancestry per `docs/export-seed-rules.md`, run a `Forest` export,
read the size: *"if the forest export returns five thousand people, then they generally are
connected"* — in an odd cluster rather than off the graph. Random `Forest` sampling on
high-eccentricity individuals, biased toward earlier generations, then reliably joins them.

## Blood vs in-law is non-intuitive

Geni offers one type first and the option of the other, *"which I think sometimes it hears,
sometimes doesn't"*, with a transaction timeout that behaves oddly. Both types are fetched per
target regardless — her call, 2026-09-02 — so the control flow does not have to be got right
to get the data.

## Not `geni_pages/`, not `geni-scraping/`

Three datasets, three purposes. `geni_pages/` is profile pages saved for paths by hand;
`geni-scraping/` is profile pages saved for their **immediate relatives** panel; this is the
path page itself, and it carries nothing but the chain.
