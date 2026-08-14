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

**No relationship statements.** Both men are the husbands of the two
`wife of ...` profiles whose exports form the corpus's two cut-off
components — 4,088 and 4,084 people that share nobody with the other 173
exports. Every relative either man has sits inside that ball, so a `P26` or
`P40` would point at an item that does not exist yet. That is the whole
reason these are being created standalone:

- **Baruch Jafe** `6000000040078764766` — spouses `6000000227145774838`, children `6000000008471807525`
- **Samuell Standen** `6000000107265740881` — father `6000000107265740865`, mother `6000000107265740822`, spouses `6000000227145420853`, children `6000000024557679929`

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
