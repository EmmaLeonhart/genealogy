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

A path's missing people are usually adjacent, so one saved page frequently captures
several of them at once — they appear in each other's relatives list.

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
