# Izumo / Senge clan: the roster, and where it actually stands

Emma's queue item, from 2026-08-19: build the family tree that is visually on
<https://shinto.miraheze.org/wiki/Izumo_clan> onto Geni, carry the Wikidata links, and
flag duplicate-profile merges rather than performing them.

`scripts/build-izumo-roster.py` parses the page's **wikitext**, not the rendered page. The
rendered `{{familytree}}` collapses into unusable prose — names run together with the
emperors they sit beside — while the wikitext keeps each person in their own
`{{ill|Name|…|qid=Q…}}` cell. That is why the previous attempt at this thrashed in the
browser.

## The roster

**214 people. 204 carry a Wikidata item. 89 carry a regnal number.**

The regnal numbers are the *Izumo no Kuni no Miyatsuko* succession, 1 to 84 — Emma flagged
that these are **not middle names**, and the roster keeps them in their own column rather
than inside the name.

| lineage | people |
| --- | ---: |
| other (the pre-split trunk, and in-laws) | 137 |
| Izumo | 39 |
| Senge | 22 |
| Kitajima | 16 |

The Senge/Kitajima split is the 1340 dispute the article describes: the eldest son was too
sickly to perform the fire-drill succession ritual, so the older line became Senge and the
younger Kitajima, and they alternated the office until the late 19th century.

## The gap is almost total

| status | people |
| --- | ---: |
| **Wikidata item but NO Geni ID** | **202** |
| in our corpus | 2 |
| no Wikidata item at all | 10 |

**Two of 214.** This is the Samaritan-high-priest shape again and far more extreme than
Bureätten, where 251 of 576 carried a Geni ID. Here the Wikidata side is nearly complete —
204 items, most of them created for exactly this genealogy — and the Geni side is joined to
almost none of it.

That reframes the item. It is not "build the tree onto Geni" as a first step, because
Emma's own account is that the clan is **already on Geni three times over** — added in
2008 in Japanese, in 2011 in English, and by her in 2026 off this page. The profiles exist.
What does not exist is any `P2600` connecting them to the 204 Wikidata items.

## So the work is resolution first, not creation

Creating people on Geni before finding the ones already there would manufacture a fourth
duplicate set on top of the three she already has to merge — and she has said the merges
are hers, not ours.

The order that follows:

1. **Find the existing Geni profiles.** Google `site:geni.com "<name>"` per the standing
   rule; Geni's own search is banned. 214 names, many highly distinctive
   (`Kushichitoriuminomikoto`, `Izumo no Ihohiku`), which is the good case for that route —
   unlike `Adolf Ludvig Piper`, these have no near-namesakes to confuse the first hit.
2. **Where a profile is found, record the pairing** for a `P2600` after the lockout lifts.
3. **Only then** consider creating anyone genuinely absent, and flag rather than perform
   any duplicate merge.

## Files

- `reports/izumo-roster.tsv` — 214 people: regnal number, name, qid, lineage, role.
- `reports/izumo-coverage.tsv` — the same with Geni IDs and status.


## The lineage is not in our corpus, and the browser warning has expired

`scripts/walk-izumo-geni.py` walks outward from Emma's own seed
(`6000000012789160423`, Tsusa-no-mikoto 4), which **is** already in the merged tree — so
the Geni side did not have to be searched name by name.

**At 25 hops the ball holds 1,312 people and matches only 10 of the 214.** Worse, most of
those ten are the *emperors* in the genealogy's parallel column — Jimmu, Chūai, Yamato
Takeru — not Izumo priests. Of the priestly line only Kushidanomikoto (8) and
Chirinomikoto (9) are present.

So "the clan is already on Geni three times over" and "the clan is in our corpus" are
different statements, and only the first is true. The profiles exist on Geni; our 548
exports have never reached them.

**Her 2026-08-19 browser warning no longer holds.** The Izumo tree renders cleanly now —
Ameno-hohi 1, Takehinatori 2, Kushini 3, Tsusa 4, regnal numbers visible in the node
labels exactly as she described. Whatever was failing that day was the *"high volume of
automated traffic"* banner, not something structural.

**Her seed is not exportable directly** — `/gedcom/export/6000000012789160423` redirects to
`/error`, so she does not manage it despite having built around it. A placeholder was
created at Kushini-no-mikoto 3's open mother slot: `NN no Mikoto`
(`6000000227389059850`), keeping Geni's suggested `no Mikoto` surname because that matches
the `NN no Mikoto` already in her tree rather than the generic tier-3 rule.

**That export is the right instrument here** and it is not the refuted sparse-region work:
this is a named lineage known to exist on Geni and known to be absent from the corpus,
which is the Bureätten shape that returned 66% new.
