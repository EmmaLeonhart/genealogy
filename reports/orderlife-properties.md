# order.life's 94 properties: which are Wikidata's, which are its own

**Asked for by Emma, 2026-08-14** — check the order.life properties for novel ones
before anything is passed through. Source:
`order.life/wikibase/properties/*.json`.

**The split is numeric and it is sharp.** Everything **P155 and above** is
mirrored from Wikidata — same number, same meaning. Everything **below P155** is
order.life's own numbering, allocated locally, and **several of those numbers
mean something completely different on Wikidata**.

---

## The collisions — never pass a low-numbered property through

Confirmed against the property table in `CLAUDE.md`:

| number | order.life means | **Wikidata means** |
| --- | --- | --- |
| **P20** | **Child** | **place of death** |
| **P40** | Reference number (deprecated?) | **child** |
| P31 | instance of | instance of — the label agrees, but **see below** |
| **P39** | **instance of** | — *a second, identical property, and the one person items actually use* |

**order.life defines `instance of` TWICE — `P31` and `P39`, same label, same
`wikibase-item` datatype — and person items use `P39`.** Measured 2026-08-15 over
a 4,000-item sample: `P39` carried the class on 3,970 of them and `P31` on
**zero**. Kenan (`Q10`) has `P39` and no `P31` at all. This paragraph said `P31`
was "the one low number that agrees" with Wikidata, which is true of the property
*definition* and misleading about the *data* — anything reading order.life's
class must check `P39` first, or it silently finds nothing.

`P20` is the dangerous one: order.life's *Child* is Wikidata's *place of death*,
both `wikibase-item`, so a pass-through would type-check and write a person into
a place-of-death statement. That is the same class of error as `SURN 秦州成紀` —
a value that lands in the wrong field and looks plausible.

The relationship properties do not collide numerically but are still renumbered:

| order.life | meaning | Wikidata |
| --- | --- | --- |
| P47 | Father | **P22** |
| P48 | Mother | **P25** |
| P42 | Spouse | **P26** |
| P20 | Child | **P40** |
| P55 | Sex | **P21** |
| P56 / P57 | Date of Birth / Death | **P569 / P570** |
| P66 / P67 | Place of Birth / Death | **P19 / P20** |
| P12 | Occupation (monolingual text) | **P106**, but see below |

`scripts/build-orderlife-batch.py` reads the `analysis/*.tsv` tables rather than
raw claims for exactly this reason, so none of these numbers is ever touched.

## The Q-space is order.life's own, and this is the worse trap

**Emma, 2026-08-14:** *"The order.life QIDs, some of them correspond, some of them
don't. The QIDs are relatively different on order.life versus other things."*

The property numbers being local is the obvious hazard. The **item** numbers being
local is the dangerous one, because a `wikibase-item` value carries no marker
saying which wiki it belongs to.

- `Q1` in order.life is **Aster**, dated −13,000,000,000. `Q1` on Wikidata is not.
- `Q153718` / `Q153719` are order.life's **Male** / **Female**. Wikidata's are
  `Q6581097` / `Q6581072`.
- `Q153801` / `Q153802` are order.life's **Person** / **Gaiad character**.

**So no order.life QID may ever appear as a value in an emitted statement.** Every
item value has to be resolved through the target person's own `P61` (their
Wikidata QID) before it means anything, and a target with no `P61` simply cannot
be pointed at. `scripts/build-orderlife-batch.py` does this: a relationship is
emitted only when *both* ends resolve to a Wikidata item, and the value written is
the other end's `wikidata_qid`, never its order.life QID.

**Anything pointing at Q1 falls out automatically** — Aster has no Wikidata item,
so every edge into her fails the both-ends test. That is the right outcome and it
happens for the right reason rather than by a special case.

## The crosswalk properties

| | |
| --- | --- |
| **P61** | Wikidata QID (identifier) |
| **P62** | Geni.com profile ID |
| P63 / P60 | UUID / uuid refn |

`P61` and `P62` are where `persons.tsv`'s `wikidata_qid` and `geni_id` columns
come from, so they are the whole basis of the join. `P62` is Wikidata's `P2600`
under a local number.

## Genuinely novel — no Wikidata equivalent to map to

| property | what it is |
| --- | --- |
| **P59 Cladoplast of** (external-id) | evolutionism/Gaiad-specific; nothing on Wikidata corresponds |
| **P64 Multi language label** | a local packing of labels into one string |
| **P49 ordinal within year, P50 ordinal within month, P51 ISO week number, P52 ISO weekday number** | calendar machinery, quantity-typed — this is the `calendar-lib` side of order.life, not genealogy |
| **P41 GEDCOM REFN, P40 Reference number** | GEDCOM import plumbing, meaningless off-wiki |
| **P5 Gedcom Full Name** | the raw `Given /Surname/` string; `persons.tsv` exposes it as the `gedcom` column |
| **P7 / P8 Birth date / Death date (deprecated)** | monolingual **text**, superseded by P56/P57 which are proper `time` |
| **P12 Occupation / P13 Residence (monolingual text)** | free text, not items — usable only after normalisation, which is the same job the Samaritan "high priest" office needs |
| **P15 Notes page, P45 Described at url, P46 notes page, P54 suffix, P65 Blazon** | local editorial fields |
| **P39 instance of** | a **second** "instance of" alongside P31. `Q153801` Person and `Q153802` Gaiad character are carried here, so P39 is the Gaiad flag's home |

**Two "instance of" properties is the structural oddity to remember.** P31 exists
and is empty on the items checked; P39 is the one actually carrying the class.

## Mirrored from Wikidata — safe, and mostly identifiers

Fifty-nine properties from P155 up. Same number, same meaning, and all but a
handful are `external-id` links to other genealogy databases:

**Genealogy databases** — Rodovid (P1185, P13492), genealogics.org (P1819),
FamilySearch (P2889), WikiTree (P2949, P7607), Kindred Britain (P3051), GEDBAS
(P4108), JewAge (P4116), WeRelate (P4159), Familypedia (P4193), Merkelstiftung
(P4620), The Peerage (P4638), MyHeritage (P5452), Roglo (P7929), DAR (P7969),
SAR (P8143), GeneaStar (P8094), Sejm-Wielki (P8172), Geneanet (P9644),
Hungarian Peerage (P9129), Political Graveyard (P8462), CRGPG (P8857), Beit
Hatfutsot (P9280), Find a Grave (P535).

**A large Swedish cluster** — P3217, P4819, P4820, P4963, P5259, P5316, P5324,
P5536, P6192, P6303, P6821, P6996, P7434, P7931, P9495, plus Norwegian war
refugees (P5871), GENUKI (P7352), Historical Gazetteer (P2503), Alvin (P6821),
SIUSA (P8356), LombardiaBeniCulturali (P9195).

**Non-identifier mirrors** — P155/P156 follows/followed by, P460 said to be the
same as, P1317 floruit, P1630 formatter URL, P1813 short name, P1814 name in
kana, P4425 mtDNA haplogroup, P4426 Y-DNA haplogroup, **P4602 date of burial or
cremation** (in CLAUDE.md's table already), P58/P68/P94 image properties.

## Emma's decisions, 2026-08-14

- **P64 Multi language label → Wikidata's `mul` label.** It is the multilingual
  label and is emitted as `Lmul`, not as a claim.
- **P59 Cladoplast of → do nothing.** *"We don't do anything with it until there
  is a Cladoplast object on Wikidata, which there currently is not. I do not have
  any intention of making it right now."* Not mapped, not emitted, not created.
- **P12 Occupation and P13 Residence → do not include.** *"The only monolingual
  text that we just don't do is the P12 and P13 occupation and residence."* They
  are dropped rather than normalised. This supersedes the note above suggesting
  they wait for normalisation.
- **Of the monolingual-text properties, address is the one that is done** —
  `P6375 street address`, which is already where a GEDCOM `ADDR` block goes
  (`CLAUDE.md` § Life events).

## The Gaiad flag does not discriminate — measured, 2026-08-14

`Q153802` "Gaiad character" is carried by **105,720 of 106,908** persons, and by
**400 of 400** sampled people who also carry a Wikidata QID — people who are
definitely real and historical. The epic runs through the entire genealogy rather
than sitting beside it.

So the flag cannot be used to hold the epic back. An earlier version of
`build-orderlife-batch.py` tiered on it and put **45,437 creations, real people
included, into "add last"**. Tiering is now on identifiers, where a person with
neither a Geni ID nor a Wikidata QID is order.life-only — which is the population
that actually needs to go last. The flag is still written onto every entry as
data.

## The decision

1. **Nothing below P155 is ever emitted with its own number.** Translate through
   the table above, or read the `analysis/*.tsv` tables, which is what the batch
   script does.
2. **P155-and-above external IDs are addable statements** and a large, easy win —
   these are identifiers Wikidata has properties for and often lacks values for,
   on items that already exist. That work is not built yet.
3. **P59, P49–P52 and P64 have no target** and should not be mapped to anything.
4. **P12 Occupation and P13 Residence are free text** and need the same
   normalisation the Samaritan high-priest office needs before they can become
   `P106` and `P551`.
5. **P39 is where the Gaiad flag lives**, so it stays as the classifier and is
   never emitted as a Wikidata statement.
