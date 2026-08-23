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


## The first export failed, and the reason is about which END of a lineage you seed

`export-Forest-6000000227389059850.ged`, seeded on the placeholder at Kushini-no-mikoto 3's
mother slot: **5000 people, 131 new (2.6%), 7 of the 214 rostered, and ZERO carrying a
regnal number.**

The Izumo priestly line is exactly what it did not bring.

**Why.** Kushini 3 sits at the *top* of the lineage, one generation below Ame no Hohi, and
that end of it is welded to the ancient imperial material — Amaterasu, Ninigi, Jimmu — which
548 exports already cover thoroughly. A breadth-first ball of 5000 from there spends
itself on the dense, well-covered side and never travels down the thin 84-generation
priestly chain.

**The correction: seed at the far end, not the founder.** The lineage runs 1 → 84 and the
material we lack is the middle and modern end — the Izumo no Kuni no Miyatsuko proper, then
the Senge and Kitajima branches after the 1340 split. Emma's own account points the same
way: she built these *"as ancestors of the spouse of Noriko Senge"*, so the modern Senge
end is where her additions attach and where the chain is reachable without crossing the
imperial mass first.

This is a different failure from the refuted sparse-region work. That one seeded into
exhausted neighbourhoods and got nothing anywhere. This one got 2.6% because the ball went
the *wrong direction* out of a correctly chosen lineage — a fixable aim, not a dead
premise.


## Two errors in the measurement above, both mine, both corrected

The "10 of 214" figure was wrong twice over.

**Word order.** The roster writes `Senge no Takamune` — Japanese order with the `no`
particle. Geni writes `Takamune Senge`. A normalised string comparison misses every one of
them, and the tree contained `Takamune Senge`, `Sadataka Kitajima`, `Naokuni Senge` and
`Kunimaro Senge` the whole time. `variants()` now generates both orders. Nothing about it
is fuzzy: the tokens must still agree exactly, only their order and the particle move.

**Searching only the ball.** The first run indexed just the 1,312 people within 25 hops of
Emma's seed. But the Senge and Kitajima profiles are reached through the **modern imperial
line** — Kunimaro Senge married Princess Noriko in 2014 — not through the founder end, so
no radius around Tsusa 4 was ever going to contain them. The search now runs over the whole
tree and the ball is used only to report distance.

**Corrected: 21 of 214 matched, 11 ambiguous, 182 absent.**

And the ones that appeared are the right kind — not more emperors but the office-holders
themselves:

| regnal | person | Geni |
| ---: | --- | --- |
| 39 | Izumo no Yoshitada | `6000000222521205883` |
| 53 | Izumo no Takatoki | `6000000222507315857` |
| 55 | Senge no Takamune | `6000000019459773306` |
| 55 | Kitajima no Sadataka | `6000000019459854230` |
| 56 | Senge no Naokuni | `6000000019459924115` |

Plus the En'ya and Sasaki figures the genealogy runs beside, and `Hiraoka no Sadataka`.

**Both 55s are there** — Takamune and Sadataka are the two men the 1340 split created, and
holding both means the fork itself is in our tree even though most of the line between and
after is not.

**This also revises the earlier export post-mortem.** That export was aimed at the wrong
end, which stands. But part of what it "failed to find" was material we already held under
a name the matcher could not see.


## Seeding the far end worked: 60 of the 77 lineage people, with their Geni IDs

`exports/izumo/export-Forest-6000000227390753876.ged`, seeded on a placeholder created at
**Naokuni Senge's open mother slot** — Naokuni is regnal 56, one generation past the 1340
split, and the deepest Senge our tree already held.

| | founder end (Kushini 3) | far end (Naokuni Senge 56) |
| --- | ---: | ---: |
| people | 5000 | 5000 |
| new to the corpus | 131 (2.6%) | 313 (6.3%) |
| rostered lineage people found | 0 | **60 of 77** |
| carrying a regnal number | 0 | 57 |

**Judge an export by what it was aimed at, not by its newness percentage.** 6.3% is a poor
number and this export is a success: of the 70 office-holder profiles it identifies, **48
were not in any of the other 543 exports**. The other 5000-person ball was spent on
imperial material we already hold.

The whole Senge line 57–76 and the whole Kitajima line 56–68 came through, plus the two men
of the 1340 split we already had. Only **17** rostered people are still absent, and they are
one contiguous stretch — Izumo 11 and 18–33, the ancient middle of the succession.

**Eight numbered office-holders arrived that the Shinto-wiki chart does not list**:
Kitajima 69, 70, 71, 72, 73, 74 and Senge 77, 78. The chart stops at Senge 76 / Kitajima 68;
Geni carries the succession further. That is material flowing the other way for once.

`reports/izumo-p2600-pairs.tsv` is the result: **60 rows, every one carrying a Wikidata
item**, ready as `P2600` *Geni.com profile ID* statements from 2026-09-01.

**One ambiguity, flagged not resolved.** Regnal 36 has two roster entries — Izumo no
Tsunesuke and Izumo no Ujihiro — and two Geni profiles, `6000000227331939856` and
`6000000227331989821`. Which is which is not decidable from the number. Both ids are in the
row for both people so the ambiguity is visible rather than guessed away.

## The Google route does not work for this clan — two controls, both failed

The queue's step 2 was `site:geni.com "<name>"`, on the reasoning that these names are
distinctive. The reasoning was fine and the route is still dead here:

- `site:geni.com "Naokuni Senge"` → no results. He is `6000000019459924115`.
- `site:geni.com "Sadataka Kitajima"` → no results. He is `6000000019459854230`.

Both men were in our tree before this export and both have live Geni profiles. Google has
simply not indexed these pages. It worked for Bureätten because Swedish nobility profiles
are linked from Wikipedia; nothing links to these. **The export is the only instrument that
reaches this clan**, which is what the 60 rows above demonstrate.


## CORRECTION, 2026-08-23: the founder-end export did not fail, and I ran one export too many

Everything above about *which end of a lineage you seed* was measured against **one export
file at a time**, or against a stale `out/merged.ged`. Measured against the corpus, the
conclusions do not survive.

`python scripts/match-izumo-export.py --corpus` — 545 exports, joined on the regnal number:

| | rostered lineage people |
| --- | ---: |
| founder end, Kushini 3 (`…227389059850`) | **23** — Izumo **18 → 40** |
| far end, Naokuni Senge 56 (`…227390753876`) | **60** — Izumo 34 → 54, Senge/Kitajima 55 → 78 |
| **the corpus, all 545 exports** | **76 of 77** |
| still absent | **1** — Izumo no Furune (11) |

**The founder-end export was not a failure.** The post-mortem above says it returned
*"ZERO carrying a regnal number"*. It returned twenty-three, and they are the exact stretch
the far-end export could not reach — the ancient middle, 18 to 33. The two balls are
complementary and between them the lineage is complete. The "zero" came from
`walk-izumo-geni.py`, which matches romanised names against `out/merged.ged`; the merge is
stale at 248 exports and the names are spelled three different ways, so it saw nothing.

**And the third export was unnecessary.** `export-Forest-6000000227331852896.ged`, seeded on
Obitake 23 to fetch the supposedly-missing 18–33, added **51 people and not one rostered
person** — all 77 profiles were in the corpus before it ran. It is filed and committed
because a GEDCOM is never discarded, but it bought nothing.

**The error is one question standing in for another.** *What does this file hold* is not
*what do we hold*, and reporting the first as the second is what sent an export after
sixteen people we already had. `--corpus` now exists so the right question is the easy one
to ask, and the module docstring says why.

### Where it actually stands

- **76 of 77** rostered Izumo/Senge/Kitajima people are in the corpus with their Geni IDs.
- **One absent: Izumo no Furune (11)**, `Q55533077`. He sits above the 18–40 stretch and
  neither ball reached him.
- **Eleven numbered office-holders beyond the chart** — Kitajima 69–74, Senge 77–81. The
  Shinto-wiki roster stops at Senge 76 / Kitajima 68; Geni carries five more Senge and six
  more Kitajima.
- `reports/izumo-p2600-pairs.tsv` is now built from the **corpus**, not one file: 76 rows,
  every one carrying a Wikidata item.
- **Two ambiguities, flagged not guessed.** Regnal 36 — Tsunesuke and Ujihiro against
  `6000000227331989821` / `6000000227331939856`. Regnal 71 — Senge no Munetoshi against
  `6000000227331623899` / `6000000227350446840`, which is a duplicate pair on Geni and so
  correctly becomes two `P2600` statements on one item.


## The ancient seats resolve by POSITION, and nine of them are contested

"76 of 77, one absent" was again a complete answer to a narrower question. The matcher
only looked at rows whose Geni surname is `Izumo`, `Senge` or `Kitajima`. **Fifteen of the
89 numbered roster rows are the kokuso from before those surnames existed** — Geni writes
them `Mishima 15 /Ashinazu-ni-Mikoto/`, `Kushida-no-mikoto` — and they had never been
looked at at all.

Adding them raised two problems and settled both.

**Romanisation defeats name matching here, silently.** Three men reported absent were in
the corpus the whole time under other spellings:

| roster | Geni | seat |
| --- | --- | ---: |
| Kushifusakinomikoto | Kushimikasaki-no-mikoto | 5 |
| Kushitsukinomikoto | Kishitsuki-no-mikoto | 6 |
| Kushichitoriuminomikoto | Kushimikatomi-no-mikoto | 7 |

**So the join is the seat, not the spelling.** `scripts/walk-izumo-succession.py` anchors on
the kokuso the regnal-number join already resolved exactly and walks **up** the father
chain — one father per person, so each step is unambiguous and decrements the number.
Walking down would have to choose among children, which is a guess.

**All 17 rostered seats 1–18 resolve, including Izumo no Furune (11)** — `Q55533077`, on
Geni as `Ibe /no Mikoto/`, `6000000227332042822`. The queue's one remaining absent person
was never absent.

### Nine seats are CONTESTED and are Emma's, not ours

Seats **1–9** land two different people, because two of Geni's three copies of this clan
disagree by one generation:

| seat | 2011 romaji chain | 2008 kanji chain |
| ---: | --- | --- |
| 8 | Kushida-no-mikoto | 櫛知理 |
| 9 | Chiri-no-mikoto | 世毛呂須 |

The kanji chain sits one seat higher throughout, so `世毛呂須` (Yomorosu, the roster's
**10**) is where the romaji chain puts Chiri (**9**). Both chains are internally consistent;
they cannot both be right about the seats.

This is exactly the duplicate-profile situation Emma described — *the clan was added to Geni
three separate times* — and the merges are hers. The contested seats are **flagged and not
emitted as pairings**. Seats 10–18 come from a single chain and are clean.

`reports/izumo-succession-chain.tsv` carries all 17 with their status.

### Standing lesson for this clan

Four times now, "absent" has meant "the matcher could not see it": once from a stale merge,
once from word order, once from measuring one file instead of the corpus, and now from
romanisation. **An absence claim about this roster is not trustworthy until it has been
checked structurally** — by seat, by parent chain, by ID — never by how a name is spelled.
