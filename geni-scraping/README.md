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
