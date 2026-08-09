# The Geni-linked Wikidata items with no family at all

Sampled 2026-08-09, offline. **24 of 1,408 shards, evenly spaced** — 24,000
items, ~1.7% of the store. Spaced rather than taken from the front because the
store is written in walk order: the front is all seed phase, the tail all
expansion, and the first 24 shards would have answered a different question.

A full count is queued rather than run — nothing CPU-intensive before 18:30.
Everything below is a sample proportion, and is written as one.

## The split that matters

`reports/wikidata-components.md` found 183,296 isolated single items and could
not say *why* they were isolated. Two readings were open, and `queue.md` 2.E
insisted on keeping them apart:

- a **true isolate** carries no relation statement at all;
- an item **only looks isolated** when its P22/P25/P26/P40/P3373 point at QIDs
  the download never fetched.

Of 9,000 sampled items carrying a Geni ID:

| | count | of Geni-linked |
| --- | ---: | ---: |
| connected — a relation pointing at an item we hold | 5,857 | 65.1% |
| **true isolate — no relation statement whatsoever** | **3,143** | **34.9%** |
| looks isolated, relations all point at un-fetched items | **0** | **0.0%** |

**The second reading is dead.** Not rare — *absent* from a 9,000-item sample.
The isolation is not an artifact of stopping the download early, and finishing
the import will not close it. Which also means the 183,296 is close to a real
figure rather than the upper bound `wikidata-components.md` had to call it: the
one mechanism that would have inflated it does not occur here.

Scaled to the 514,903 stored items carrying a Geni ID, 34.9% is **~180,000**,
against 183,296 isolates found globally. The two nearly coincide, and the reason
is structural: an expansion item was fetched *because* it was somebody's
relative, so it is connected by construction. **Essentially every isolate in the
store is a Geni-linked person with no family on Wikidata.**

## They are not stubs — this is the surprise

| | share of isolates |
| --- | ---: |
| instance of human (`P31`=`Q5`) | 100.0% |
| sex or gender (`P21`) | 100.0% |
| family name (`P734`) | 87.8% |
| date of birth (`P569`) | 85.1% |
| given name (`P735`) | 82.5% |
| date of death (`P570`) | 81.4% |
| country of citizenship (`P27`) | 62.5% |
| occupation (`P106`) | 57.6% |
| place of birth (`P19`) | 53.9% |

The median isolate carries about **15 distinct claim properties**. Examples,
with their claim-property and sitelink counts:

| item | label | properties | sitelinks |
| --- | --- | ---: | ---: |
| [Q1000203](https://www.wikidata.org/wiki/Q1000203) | Robert Mallet-Stevens | 122 | 19 |
| [Q1000005](https://www.wikidata.org/wiki/Q1000005) | Karel Matěj Čapek-Chod | 89 | 15 |
| [Q1000498](https://www.wikidata.org/wiki/Q1000498) | Bud Greenspan | 50 | 13 |
| [Q1000051](https://www.wikidata.org/wiki/Q1000051) | Joseph C. O'Mahoney | 44 | 11 |

These are well-described people with Wikipedia articles in a dozen-plus
languages. What they are missing is **exclusively the genealogy**: no father, no
mother, no spouse, no child, no sibling.

## Why this is the clearest authoring target in the project

`todo.md` § 4 is about creating absent people on Wikidata. This population is
the easier half of that and had not been identified: the *items already exist*
and are good. Each one names a Geni profile, and Geni is a genealogy site whose
whole content is the relationships Wikidata is missing here.

So the edit is P22/P25 (and P26/P40) onto an existing, well-sourced item — not
item creation, not entity resolution, and not a name match: the Geni ID on the
item is the join, which is this repo's primary key.

## The full count, 2026-08-09

The sample above is now superseded by a complete pass. **183,681 Geni-linked
items carry no relation statement**, of which **246** are people our tree holds.
The sample predicted ~179,800 and ~286 — close enough on both that nothing in
the reasoning changes.

Full list: `reports/wikidata-isolates.tsv`. Browsable, sorted by number of
Wikipedia articles so the best-documented come first:
`out/wikidata-isolates.html` (gitignored; rebuild with
`python scripts/build-isolates-page.py`).

**One definitional catch worth stating.** 183,681 here is slightly *larger* than
the 183,296 single-item components in `reports/wikidata-components.md`, and the
two are not the same measurement. This count is "the item states no relation";
that one is "nothing links the item in either direction". An item can state no
parent and still be named as somebody else's parent — no outgoing edge, an
incoming one. For adding family **to** an item, the outgoing-absent count is the
right one, which is why it is used here. For "is this person isolated in the
graph", it is not.

The isolates also stop appearing after roughly shard 800 of 1,408: they are
concentrated in the seed phase, and the expansion tail is made of items fetched
*because* they were someone's relative, which by construction have relations.

## Except it is not, and the same sample says so

The obvious next step was to assume Geni supplies the family. Measuring the
overlap costs nothing once the sample is open, so it was measured rather than
assumed — and it kills the easy version of the story:

| | in our tree |
| --- | ---: |
| Geni-linked items **with** family on Wikidata | 201 of 5,857 — **3.43%** |
| Geni-linked items **without** family (the isolates) | 5 of 3,143 — **0.16%** |

**An isolate is twenty-one times less likely to be somebody we hold.** Scaled
up: of ~180,000 isolates, roughly **286** are people already in our tree. The
immediately actionable slice is not 180,000. It is a few hundred.

The asymmetry is itself the finding, and it is not a sampling accident at these
counts. Our tree is built by walking Geni's family graph, so it fills with
exactly the densely-related population — the royal and noble lines Wikidata also
records parents for. The isolates are the other kind of notable person: writers,
architects, senators, who have a Geni profile and sit outside the big
interconnected genealogy on *both* sites.

**What this does not say.** It does not say Geni lacks their family. It says no
export here has reached them, which is a fact about our sampling and not about
Geni — the distinction `CLAUDE.md` insists on for `density`, and it applies
unchanged. Whether Geni holds parents for a Wikidata isolate is exactly the
unknown one export would settle, and the cheapest test is a handful of exports
seeded on isolates we can already see.

So the population is **an export target list, not an authoring list** — the
reverse of the reading the previous section sets up, and the reason that section
is left standing above rather than quietly rewritten.

**Still not established:** whether an isolate exported from Geni comes back with
family. Until one does, "add P22/P25 to 180,000 good items" is a hypothesis with
a measured obstacle in front of it.
