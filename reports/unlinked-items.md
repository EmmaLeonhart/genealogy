# Two unlinked items, to create on 2026-09-30

Emma, 2026-08-13: *"create wikidata items for [these two] on September 30
as independent unlinked items completely independently of their links
elsewhere... these appear to have gotten into the data somehow but are
apparently completely unlinked and I still want them to get in."*

**2 creations, scheduled `2026-09-30`.** Queued the way the
Charlemagne route is queued — written down as edit objects now, executed
later. `out/wikidata/unlinked-items.json` is the machine-readable half and
shares its shape with `out/wikidata/priority-chain.json`.

| geni id | label | sex | born | died | buried | statements |
| --- | --- | --- | --- | --- | --- | ---: |
| [`6000000040078764766`](https://www.geni.com/people/Baruch-Jafe/6000000040078764766) | Baruch Jafe | M | — | 1790 | — | 4 |
| [`6000000107265740881`](https://www.geni.com/people/Samuell-Standen/6000000107265740881) | Samuell Standen | M | 1620 | SEP 1658 | 21 SEP 1658 | 6 |

## What is deliberately not on them

**No relationship statements — because there is nothing to point at.**
Every relative either man has is listed below, and **not one of them
carries a Wikidata item**. A `P22`/`P25`/`P26`/`P40` needs a target QID,
so the links wait until those relatives have items of their own.

- **Baruch Jafe** `6000000040078764766` — spouse wife of Baruch Jafe `6000000227145774838` (no item); children Edel Jafe `6000000008471807525` (no item)
- **Samuell Standen** `6000000107265740881` — father John Standen `6000000107265740865` (no item); mother Joane Simmons `6000000107265740822` (no item); spouse wife of Samuel Standen `6000000227145420853` (no item); children Samuel Standen `6000000024557679929` (no item)

**The Geni side differs between them, and that is not why.** Samuell
Standen joined the main tree on 2026-08-13, when a `Forest` of
`6000000227226600829` bridged the ball he sat in. Baruch Jafe is still
inside the remaining cut-off component of 4,088 people. Both are queued the
same way regardless: the goal is everything on Geni linked to Wikidata and
into both world trees, and an item has to exist before it can be connected.

**No places.** Geni gives Samuell Standen "Sussex, England" as free text.
Resolving that to an item means asking Wikidata which item it is, and this
repo does not query Wikidata — it waits for the local store. `P19`/`P20`
stay off until that can be answered offline.

## The properties used

| property | what | reference |
| --- | --- | --- |
| P31 | instance of `Q5` human | P2600 |
| P2600 | Geni.com profile ID | — (it is the citation) |
| P21 | sex or gender | P2600 |
| P569 / P570 | date of birth / death | P2600 |
| P4602 | date of burial or cremation | P2600 |

Dates carry the GEDCOM precision Geni stated — 9 year, 10 month, 11 day —
never widened or narrowed. The raw GEDCOM text rides along in the JSON so a
reviewer can see what was read.
