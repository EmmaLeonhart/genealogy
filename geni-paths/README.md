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

⛔ **SUPERSEDED ON THE SAVE, 2026-09-06.** Emma: *"we are not supposed to be saving pages lol
... Only the exports need downloading because you write stuff into files in the repo you dummy."*
Everything below about navigating, waiting and clicking *"Show short path"* is still exactly
right and is still what the collector's `path` job does. What changed is the last step: the page
is **not** Blob-downloaded. The chain is parsed in the tab, where the markup is, and the job
RETURNS the finished path TSV on its result attribute for the agent to write into `paths/`.

The six `*.html` files in this directory are what the page-saving method left behind. They stay
as the record of those six captures; nothing new lands here.

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

## ⛔ THE STATISTICS BLOCK IS THE REAL INSTRUMENT. "No relationship found" is not a negative result

**Emma, 2026-09-03**, on George Drouillard, whose path search resolved to *"No blood relationship
was found. No in-law relationship was found."*:

> *"Family Tree 10,575 / Blood Relatives 15,000 / Ancestors 61 / Followers 13 — this means that
> it literally is pretty much impossible that he is not linked to charlemagne. 15,000 blood
> relatives or really any of these numbers being high on this scale indicates that they are in
> the world tree but it was a database failure."*

**MEASURED, and she was right.** She ran a `Forest` export from a seed near him. It came back
5,000 people, and:

- Drouillard sits in a 1,174-person component of that export;
- **7 of the 5,000 are already in our tree** — Pierre Billiau dit Morand Wyandot, and six
  Lespérance/Morand people;
- **all 7 are in the main component**, 1,450,615 people reachable from Charlemagne;
- Drouillard reaches Charles Lespérance `6000000002076959885` in **4 hops** inside the export.

So Geni reported no relationship for a man four steps from a family continuous with Charlemagne.

**15,000 IS A CEILING, NOT A COUNT — her rule, same day:** *"keep in mind that 15,000 on any
number there is a flag that the query number exceeded the maximum it can do. I do not believe
there is any section of 15,000 connected people on geni that is not connected to the world tree
either, or 5,000 for that matter. So anything at those numbers pretty much always will indicate
connection to the world tree."*

So a saturated figure means *at least* that many, and it is the **strongest** evidence of
connection there is. A `no path found` sitting beside one is a database failure.

**AND A MISSING ROW MEANS ZERO.** Dorothy Jeakins `6000000018119318134` reads
`Family Tree 1,405 / Blood Relatives 1 / Followers 1` with **no Ancestors row at all** — Emma:
*"ancestors are not mentioned at all because she has no ancestors and geni is weird and gives
zero as not an option there"*. Record `0`, never blank: blank later reads as *we failed to
scrape it*, which is the absent-versus-zero confusion that costs this repo real numbers
elsewhere.

### `reports/isolates.csv` — what to store, and when

Her instruction: *"just list these numbers for all of the people for whom no path is found in a
csv file... no judgment you just store the returned numbers for everyone... you store these
numbers even before a path is found or not, but you always stay on the page and request the
path"*, with `path_found` added afterwards once it resolves.

    geni_id, label, family_tree, blood_relatives, ancestors, descendants, followers,
    requested_at, path_found      <- filled in LATER: yes / no / (blank while running)

**No `qid` column.** Emma, 2026-09-03: *"there should be no qid line since the qid line is just
completely prone to fabrication lol"* --- and she was right about the specific risk, because a
QID was typed from memory twice in one sitting while a roster file with the real value sat
unread. Every column here is read off the page.

**`descendants` is in the block and was missed on the first pass.** The extractor looked for four
labels and Geni prints five. **The zeros in the first six rows are her shortcut, not
measurements** --- *"just list everyone except for anna rood as being 0 descendants, since that
is easier than you looking at each page lol"* --- and at least Ole Klemet Sara and Moshe Bar
Nissim visibly have children. Do not read those zeros as data; re-read the block for anyone
whose descendants matter.

**No judgment at collection time.** The numbers go in as returned; reading them is a separate
step.

## ⛔ HOW THE PAGE IS ACTUALLY DRIVEN — three visible states, and a hidden template that lies

**The state must be read off the RENDERED page, never off the DOM text.** The markup contains a
**hidden** `Path search in progress` element — zero width, zero height, no `offsetParent` — that
is present *before any request is made*. Reading `document.body.innerText` for it reports every
untouched profile as "in progress". About 22 profiles were recorded that way on 2026-09-03 and
**not one search had been requested**; the whole loop did nothing but load pages.

| what is VISIBLE in the box | state | what to do |
| --- | --- | --- |
| a **"How are they related?"** button | not requested | click it |
| a green **"Path search in progress. If we find a path, we will notify you."** bar | running | **leave the tab open** |
| *"No blood relationship was found. No in-law relationship was found."* | resolved, no path | record `path_found=no` |
| a chain of names | resolved, path | save the page |

Check visibility with `offsetParent` and a non-zero `getBoundingClientRect()`, or read a
screenshot. The button disappearing is the confirmation that the click took.

### The rate is about ATTENTION, not about requests

Emma, 2026-09-03: *"this takes about 10 seconds max of attention per profile, but each profile
must be open for quite a while... it is still not done and might take 10 minutes."*

So the shape is **many tabs open at once**, not one at a time:

1. open a tab, read the Statistics block, click *"How are they related?"* — about 10 seconds;
2. **leave it open** and move to the next;
3. come back after minutes and read the resolved box.

**Closing the tab breaks it.** Her words: *"If you do not leave the tabs open then it actually
messes a bit with the data that is given"*, and *"if you request many profiles at once after
closing the tabs then I think it actually drops its promise to notify you, or it only notifies
you on the most recent one you requested."* It is **RAM intensive** on our side, so the batch
size is bounded by the machine rather than by politeness.

**The notifications are not the collector.** *"There are notifications but the notifications
actively give a worse version of the data."* Read the page.

**The pushpin is set ONCE, BY HER, and is not ours to touch.** Emma, 2026-09-03: *"You do not
pin Charlemagne, it needs to be done exactly once and I did it."* Toggling it mid-run is how a
batch of profiles came to be queued against *"You"* instead of Charlemagne. The box naming
**Charlemagne** on both ends is the check that the anchor is right.

## How to save

The blob capture `geni-scraping/README.md` describes — a download of the page's own
`document.documentElement.outerHTML` — named **`<geni id>-<blood|inlaw>.html`** so the two
types do not collide. No "complete webpage" saves: the `_files` asset directories are
**96% of the 2.8 GB** in `paths_for_wikidata_isolates/` and carry nothing. The HTML alone is
170 KB a page; the extracted TSV is ~4 KB.

### ⛔ THE CALL THAT WORKS — copy it, do not re-derive it

**Recorded 2026-09-05 because it was re-derived once already.** Everything above states the
*steps*; none of it stated the *call*, so a later session read the prose, found that a plain
`fetch()` returns zero `span.segment` anchors, and started building a local HTTP sink to POST
captures to. Emma: *"did you either not document the original successful way you did it or
decide to be creative here? Just do the successful way."* The steps are not the method — this
is:

    browser_batch [
      navigate        https://www.geni.com/people/x/<ID>
      javascript_tool <the block below>
      tabs_close_mcp
    ]

```js
const ID='<ID>';
const t0=Date.now();
while(!document.querySelector('#relation_description') && Date.now()-t0<20000){
  await new Promise(r=>setTimeout(r,500));
}
const link=[...document.querySelectorAll('a')].find(x=>/show short path/i.test(x.textContent));
if(link) link.click();
const t1=Date.now();
while(document.querySelectorAll('span.segment > span.name a[data-profile-id]').length===0
      && Date.now()-t1<20000){
  await new Promise(r=>setTimeout(r,500));
}
const ids=[...document.querySelectorAll('span.segment > span.name a[data-profile-id]')]
  .map(x=>x.getAttribute('data-profile-id'));
const b=new Blob([document.documentElement.outerHTML],{type:'text/html'});
const dl=document.createElement('a');
dl.href=URL.createObjectURL(b); dl.download=ID+'-blood.html';
document.body.appendChild(dl); dl.click();
({id:ID, rdPresent:!!document.querySelector('#relation_description'), clicked:!!link,
  steps:ids.length, hasTarget:ids.includes(ID), bytes:document.documentElement.outerHTML.length})
```

Then the file lands in `~/Downloads` and is moved:

    mv /c/Users/Emma/Downloads/<ID>-blood.html geni-paths/<ID>-blood.html

**Three things about it that are not obvious and are why guessing fails.**

- **A `fetch()` of the profile is not enough.** It returns 200 and the summary sentence in
  `#relation_description`, and **zero** segments — the chain is written in by the page's own
  JS. Measured 2026-09-05 on Arne Garborg: 92,891 bytes, `segs 0`. The capture has to come
  from a rendered page, which is what the `navigate` is for.
- **The last expression is the return value.** It is written `({...})` in parentheses, with
  top-level `await` above it. Wrapping the whole thing in an `async` IIFE returns `{}` —
  measured twice on 2026-09-05 before the shape was read off the transcript.
- **The verdict comes back small.** `steps` and `hasTarget` are the two that matter and they
  are exactly what `harvest-isolate-paths.chain_found` re-derives from the saved file, so a
  batch that reports `hasTarget:false` is a miss you already know about before harvesting.

**The transcript is `7a11670b-624d-43f7-ae9b-48665823b8e7.jsonl`** — see `CLAUDE.md`
§ *The working Geni capture call lives in ONE transcript*.

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
