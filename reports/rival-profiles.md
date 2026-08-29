# Rival profiles: what the offline sweep can and cannot see

`scripts/find-rival-profiles.py`, run 2026-08-29. Fully offline against `out/wikidata/`.

## What it looks for

A person **this programme minted** and some **other item already on Wikidata** that share a
neighbour (a parent, or a child) and carry the same label. That is the shape Emma has been
merging by hand.

Comparison is set-against-set across the six label columns of `out/wikidata/labels.tsv`
(`en`, `mul`, `no`, `nb`, `sv`, `da`). Case and whitespace fold; **diacritics do not** — CLAUDE.md
is explicit that a diacritic makes a different name.

## Result

| | count |
| --- | ---: |
| ledger items | 580 |
| minted by us (not merely a `P2600` added to an existing item) | 550 |
| ...of those, absent from the store snapshot, i.e. genuinely new | 303 |
| ...with a parent or child recorded | 287 |
| **rival pairs found** | **0** |

## The ceiling, which is the actual finding

**Only 15 of those 287 people have a neighbour that exists in the store snapshot.**

The sweep can only see a rival through a shared neighbour, and the neighbour has to be in
`out/wikidata/relations.tsv` — a download of 2026-08-25. Almost everyone our new items are
attached to was minted by the same batches, days after that snapshot, so there is nothing to
anchor a comparison to. **A zero here is close to vacuous and must not be read as "no rivals
exist".**

So the `P2600` blind spot has a second, compounding half. The guard cannot see a person who has
an item without a Geni id; and the offline store cannot see the neighbourhood our own recent
creations live in. Both point the same way: **the screen has to run against live Wikidata at
compose time**, on the specific parents a batch is about to create, not against a snapshot.

## What was checked and rejected

- **Same-label siblings among our own items** — 109 parents carry two or more of our items as
  children; **0** of those sibling sets share a label. We are not duplicating within a batch.
- **Namesake pairs already on Wikidata** — an earlier pass that did not distinguish minted items
  from ones Emma merely linked returned 5 pairs, all pre-existing ancestor/descendant namesakes
  (Carl Gustaf Mannerheim, Henning Mankell, Axel von Rosen, Carl Fredrik Piper, Nils Burensköld).
  None is ours and none is a defect.

## Ground truth for any future screen

The ledger records the three merges Emma has already had to perform, and a screen that cannot
retrodict these is not working:

| Geni id | ours, merged away | into |
| --- | --- | --- |
| `6000000004334566448` | `Q141199808` | `Q141199704` |
| `6000000005264351012` | `Q141178149` | `Q110302791` |
| `6000000011239545575` | `Q141216475` | `Q10511224` |

They cannot be caught retrospectively by this sweep: a merged QID redirects, so it no longer
appears with kin of its own.
