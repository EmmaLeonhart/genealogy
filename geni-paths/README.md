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
https://www.geni.com/path/x?from=6000000087535357291&path_type=blood&to=<geni id>
https://www.geni.com/path/x?from=6000000087535357291&path_type=inlaw&to=<geni id>
```

The slug between `/path/` and `?` is cosmetic. `from` is **Emma Himiko Leonhart**
(`Q140568870`) — measured as step 1 "You" on 679 saved paths, not taken from a constant.
`scripts/build-path-to-wikidata-report.py` carries a different id, and it is Empress Jingū.

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

→ `reports/isolate-path-pilot-results.tsv` and the hit rate. Her own batches ran **34–39%**
for occupation-filtered academics and **92%** for Nordic ones; where a uniform sample lands
decides whether the full campaign is worth its request budget.

## Not `geni_pages/`, not `geni-scraping/`

Three datasets, three purposes. `geni_pages/` is profile pages saved for paths by hand;
`geni-scraping/` is profile pages saved for their **immediate relatives** panel; this is the
path page itself, and it carries nothing but the chain.
