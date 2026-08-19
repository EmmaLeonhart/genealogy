# `geni-scraping/` — saved Geni pages for the small gaps

**Emma, 2026-08-18.** A relationship path missing only one, two or three people is not
worth an export: *"a gap with one person or two people is actually basically useless as a
deliverable… It is not worth six minutes to fill in something on the flat tail."*

Those people are captured by **saving their Geni page** instead, and the profiles are
built from the saved pages later. Her words: *"We later on build up the profiles from this
separate thing, which won't really be a fallback thing. It'll be another thing."*

## What to save

- The person's own profile page.
- **The relatives section expanded first** — the linked relatives are not in the page
  until it is opened, and the immediate relatives are the point: *"you would be needing to
  save the page for the immediate relatives of the person on Wikidata we're trying to
  connect to."* Siblings, parents, spouses, with their names and Geni IDs.
- Anything else on the page that needs a click to reveal.

## Not `geni_pages/`

`geni_pages/` holds pages saved for **relationship paths**, which
`genimerge.genipage` parses for `span.segment > span.name` anchors. This is a different
dataset with a different purpose, and she was explicit: *"Do not save it in geni pages as
a specific thing. Save it into geni-scraping."*

## Rate

One a minute, no concurrency — *"so it doesn't look bad"* — and **bail immediately on any
suspicious behaviour**.

## The threshold, settled from her own words

> *"if a gap is **one person or two people**, you use the thing that I came up with…
> I would say even **three people** is a safe enough thing that you should just go through
> it. **For a larger export, say four or more people in the chain**, my view would be
> this: you start with an export centered on the destination person."*

**≤ 3 missing on a path → save the page. ≥ 4 → export.** Measured against the tail on
2026-08-18: **102 paths of 543 (19%) fall under the threshold, and they are only 221
people.** The other 441 paths hold 4,621 people and are where exports go.

**Every missing person on the path gets their OWN page saved.** Emma, 2026-08-18,
correcting exactly this: *"You run through and save everybody in the path. You go through
and run and save every single person in the path."* And the reason: *"A mention on the
saved page is not legitimate enough for a path member. It's just enough for making a
non-path individual."*

So there are two grades of person coming out of this, and they must not be confused:

| | source | good enough for |
| --- | --- | --- |
| **path member** | **their own saved page** | a person on the chain — the thing being connected |
| **non-path individual** | a mention in someone else's relatives panel | a peripheral relative, thin but still worth creating |

The tempting shortcut — save one page and harvest the two or three missing neighbours out
of its relatives list — is **wrong**, and it was written into this file before she caught
it. A mention gives a name, an ID and a relationship word; that is enough to create
somebody's cousin, and not enough to stand as a link in the chain.

## What a saved page yields, and what it becomes

Emma, 2026-08-18: *"That other method essentially generates relatives. The information you
have is the display name, the relationship, and the geni ID. You can make an individual
with a gender, a geni ID, and the relationship and the display name so it's not the most
difficult."*

So each relative in the expanded panel gives:

| from the page | becomes |
| --- | --- |
| Geni profile ID | `P2600` *Geni.com profile ID* — the primary key, and what makes the item findable |
| display name | the label, subject to `scripts/labels.py` — `Private` and `NN` are markers, never labels |
| relationship word | the link, and the **sex**: son/brother/father → `Q6581097` *male*, daughter/sister/mother → `Q6581072` *female* |
| relationship word | `P22` *father*, `P25` *mother*, `P3373` *sibling*, `P26` *spouse*, `P40` *child* |

**These people are deliberately thin, and that is the point.** Her words: *"These
individuals are a bit sparse and not that big but they are individuals that still
contribute some value to wiki data… We want to represent the person's family and we want
to represent the families of the people decently."* A sparse item carrying a Geni ID, a
sex and a parent link is worth having; spending six minutes of export time to get a
richer version of the same two people is not.

**The sex comes from the relationship word, never from the name.** That is the one
inference this method makes, and it is safe because the word states it — `his daughter`
is not a guess. No sex is recorded where the relationship word is neutral.

## How the page actually gets saved, and the Chrome block that shapes it

**The page saves itself.** A tiny script in the page builds a `Blob` of its own
`document.documentElement.outerHTML` and clicks an `<a download="<geni id>.html">`,
so Chrome writes the file and **the markup never passes through the agent's
context**. `scripts/sweep-scraped-pages.sh` then moves it here, refusing to
overwrite a page already saved.

**Chrome allows exactly one automatic download per tab.** The second script-driven
download from the same tab is blocked silently — no error in the page, nothing in
`Downloads`, just a blocked-downloads bubble in the omnibox. So the loop is **one
fresh tab per person**: create tab, navigate, save, close it, create the next.

That is why this is not done with `Ctrl+S` (a native dialog the extension cannot
answer) and not by reading the page into the agent (a 145 KB page per person, and
1,824 people).

**Reading the page instead of saving it is not a substitute, and the reason is
measurable.** The visible *Immediate Family* block truncates — Alfred Ingerman
Hoknes reads `Father of Caroline Signe Borsheim; Floyd Olaf Hoknes; ... and 4
others`. The DOM carries all **27** relatives with their profile IDs. The text
loses seven people; the saved page keeps them.

    PYTHONPATH=src python scripts/build-scrape-targets.py   # who to save
    PYTHONPATH=src python scripts/next-scrape-batch.py 20   # next N, skipping saved
    bash scripts/sweep-scraped-pages.sh                     # file what landed
