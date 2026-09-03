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

## ⛔ THE `/path/` URL DOES NOT WORK AS WRITTEN ABOVE — measured 2026-09-03

**The `to=` parameter is ignored.** Fetched from her own logged-in Chrome, all four probe
requests behaved the same way:

    https://www.geni.com/path/x?from=6000000002457013227&path_type=blood&to=6000000004051490175
      -> redirects to https://www.geni.com/people/Charlemagne/6000000002457013227
      -> body carries "The relationship could not be found."
      -> and `#relation_description` reads "Charlemagne is your 35th great grandfather."

So the page that comes back is **Charlemagne's profile showing his relationship to the
logged-in viewer**, which is Emma. The requested target appears nowhere on it.

**⚠ The dangerous part is that this page looks like a HIT.** It renders **38** anchors inside
`span.segment > span.name` — the viewer's own 38-step chain to Charlemagne. `harvest-isolate-paths.py`
discriminates on the parsed step count (`MIN_STEPS`), so it would score every miss as a hit and
report a **100% reach rate** made of 100 identical copies of the Charlemagne→Emma path. Its
docstring anticipates the opposite failure — *"a run reporting 0 steps on every page means the
markup differs"* — and this is the one that produces a plausible number instead of a zero.
`CLAUDE.md` § *check the separator before believing a distribution* is the family.

**Two guards are therefore mandatory before any harvest of these pages**, and neither is in
the script yet:

- the body must not contain *"The relationship could not be found"*; and
- the **target's own Geni id must appear among the parsed step ids**. On the probes the chain
  ran `6000000087535357291 … 6000000002457013227` and `targetPresent` was `false`.

**What produced the 663 existing paths was a PROFILE page, not a `/path/` URL.** `geni_pages/`
holds `Geni - <Name>.html` — profile saves — which is what `CLAUDE.md` § *Relationship paths:
save the page, never the pasted text* describes. The relationship panel lives on the profile.

**THE ANCHOR ROUTE WORKS, and it is the method — established and validated 2026-09-03.**
The pushpin is real: `toggleRelationshipAnchor('6000000002457013227')` on Charlemagne's profile
pins him as the anchor for the account, and every profile visited afterwards reports its
relationship **to him** rather than to the viewer. The tell is the sentence itself —
*"Arne Garborg is Charlemagne's 31st great grandson"*, where before it read *"Charlemagne is
your 35th great grandfather"*.

**The chain is COLLAPSED until "Show short path" is clicked.** With the anchor set,
`#relation_description` carries the summary sentence and **zero** `span.segment` anchors; the
segments only exist after the click. A capture taken before it saves a page with no path on it
— the same shape as § *Wait for `#family_profile_module` before saving* in
`geni-scraping/README.md`, and it would look like a miss rather than an error.

So the fetch is, per target:

    navigate  https://www.geni.com/people/x/<geni id>
    wait      for #relation_description
    click     the "Show short path" link
    wait      for span.segment > span.name a[data-profile-id]
    save      the blob of document.documentElement.outerHTML

**Validated against a path we already hold.** Target `6000000003492005116` Arne Garborg came
back **34 steps, first `6000000002457013227` Charlemagne, last the target** — reproducing
`paths/charlemagne-to-arne-garborg.tsv`, which is 34 steps, exactly. That is the check that the
markup matches the parser, and it passes.

**A missing panel is the `no_chain` outcome, not a broken fetch.** `6000000174444394081`
(bishop Camillo Ballin) carries no `#relation_description` at all and no occurrence of the word
*relationship* — which is what an isolate looks like, and these targets are isolates by
selection. Read it as `chain_found=0` and never as *unrelated*, per the harvester's own docstring.

**Blood against in-law is a control on the page, not a URL parameter.** The profile carries a
**"Blood Relatives"** link beside "Show short path". The `path_type=` parameter above is part of
the URL form that does not work; whichever chain the page opens with is what the capture holds,
and the type must be recorded from the page rather than assumed from a URL.

## ⛔ THE SEARCH IS ASYNCHRONOUS. This is a TWO-PASS campaign — found 2026-09-03

**Geni does not compute the path while you wait.** On the first visit to a target the page
renders two segments and this sentence between them:

    You  →  Path search in progress. If we find a path, we will notify you.
            Joseph-Massé Gravel dit Brindelière (your relative?)

`(your relative?)` is not a relationship. It is the placeholder on a search that has been
**queued server-side**, and the answer arrives later.

**Nine targets were probed before this was spotted and every one returned "0 steps".** A clean,
plausible, meaningless zero — the same shape as every other instrument in `CLAUDE.md`
§ *check the separator before believing a distribution*. Clicking *"How are you related?"* and
polling for 45 seconds did not resolve it either; the page still said *in progress*.

**So a first-visit capture measures our own impatience, not connectivity**, and PENDING is a
third state that must never be folded into the miss column:

| page says | state | what to do |
| --- | --- | --- |
| a chain naming the target | **hit** | parse it |
| *"the relationship could not be found"* | **miss** | record `chain_found=0` |
| *"path search in progress"* | **pending** | **fetch it again later** |

`harvest-isolate-paths.py` now carries `PENDING_TEXT` and a `pending()` test, reports a
`PENDING re-fetch` count, and — the part that matters — **divides the reach rate by RESOLVED
pages only**. Its first run said `0/5 = 0%` when four of the five were still searching.

**What this does to the 185,327-target campaign**: it is two passes with a delay between them,
not one. Pass one *requests* every search; pass two collects. The delay is unmeasured — the one
target watched for 45 seconds had not finished — and the sentence promises a notification, so
the notification feed may be the cheaper collector than re-visiting 185,327 profiles. **Neither
is established and this needs her.**

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
