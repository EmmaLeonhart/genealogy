# Spec: modelling person names for Wikidata

**The purpose is to add, not to correct.** Emma, 2026-08-10: *"the entire
purpose of this is to add it… Correcting stuff on Wikidata is actually such a
pain that it's almost effectively out of the question. We will be more prone to
adding in contradictory information cited to Geni than we are to correcting
information."*

So this spec never proposes an edit to an existing label. It proposes labels for
**language slots that are empty**.

Scope right now is the **string forms** of names — labels. Linking to name
*items* (`P735`/`P734` pointing at a Wikidata item for "Henry") is a later stage
and is out of scope here.

Population is the **14,157 people carrying both a Geni ID and a Wikidata item**,
per Emma's rule that labels are only touched where both exist.

## What is missing, measured

| label | present | missing | note |
| --- | ---: | ---: | --- |
| English | 13,656 (96.5%) | **501** | effectively done |
| Japanese | 3,996 (28.2%) | **10,161** | the work |
| `mul` | 2,206 (15.6%) | **11,951** | Emma: "occasionally" |

Wikidata already carries **15.1 labels per item on average** across all
languages, so these items are not sparse in general — they are sparse in
Japanese specifically.

## The tractable slice: 4,500 people

**5,383 of the linked people have a Geni `NAME` record containing CJK script.
4,500 of them have no Japanese label on Wikidata at all.**

That is the population where a Japanese label can be proposed **without
inferring anything**: the string is already in the record, in the script, and
the slot is empty. No language detection beyond "does this contain a CJK
codepoint", which is a property of the bytes rather than a judgement about them.

The remaining ~5,660 missing Japanese labels have no CJK string in Geni and are
**not** addressable from Geni data. They would need transliteration, which is
generation rather than transcription, and is out of scope.

## Why language has to be inferred at all

**There is no language marking anywhere in the corpus. Zero `LANG` subtags.**
The only subtags under `NAME` are:

| subtag | count | of 444,874 names |
| --- | ---: | ---: |
| `GIVN` | 352,545 | 79% |
| `_MARNM` | 244,392 | 55% |
| `SURN` | 219,117 | 49% |
| `NICK` | 66,926 | 15% |
| `NSFX` | 36,072 | 8% |
| `CONC` | 6 | — |

Geni holds the language internally and drops it on export. So a person with four
`NAME` records — Henry III has `Henry III King of England`, `Henry III, King of
England`, `Enrique`, `Enrique III, rey de Inglaterra` — gives no indication which
two are Spanish. Isabelle of Angoulême has six, spanning French, English and
Lithuanian (`Izabelė iš Angulemo`).

**Script is the only signal that is read rather than guessed.** CJK-vs-Latin is
mechanical. Distinguishing English from Spanish inside Latin script is not, and
Emma has parked it: *"For linguistic stuff, we probably should be trying to
detect what languages stuff is written in, but for now we can focus on other
stuff."*

## Proposed rule for the 4,500

For each linked person with no `ja` label:

1. Take the `NAME` records containing CJK.
2. If exactly one, propose it as the `ja` label.
3. If more than one, **do not choose** — show Emma the candidates.
4. Cite the Geni profile as the source.

Step 3 is the point. This spec does not rank name variants, because nothing in
the data ranks them and the case walk has already shown Geni carrying prose,
alternates joined by "or", and empty subtags inside fields meant to hold one
value.

## `_MARNM` is the married name — answered by Emma, 2026-08-11

**And the corpus uses the slot for a good deal more than marriage.** Both halves
matter, so both are recorded here.

The answer is right about the tag. `_MARNM` is the PAF/Ancestral File convention
for a married name, and it is confirmed on the female records that can be checked
against known history: Judith `/de France/` carries `_MARNM Flandre` and married
into Flanders; Hildegarde `/of Flanders/` carries `Van Holland`; Adelheid
`/of Saxony/` carries `Przemyślid`. `SURN` is the maiden name, `_MARNM` the
married one, exactly as stated.

What the measurement adds is that most records carrying the tag are not doing
that. Over all 444,874 `NAME` records:

| `_MARNM` against `SURN` | records | of the 244,392 | sex |
| --- | ---: | ---: | --- |
| identical to `SURN` | 75,952 | 31% | M 62% / F 38% |
| `SURN` empty — `_MARNM` is the only surname present | 106,218 | 43% | M 72% / F 28% |
| **differs from `SURN`** | 62,222 | 25% | **M 53% / F 47%** |

**Three consequences for building labels and P734 links:**

1. **`_MARNM` cannot be dropped.** On 106,218 records `SURN` is empty and
   `_MARNM` holds the only surname there is. Reading `SURN` alone loses it.
2. **`_MARNM` cannot be read as "married name" per record either.** The
   differing group is 53% male. The male differences are spelling and case
   variants (`Osborn`/`Osborne`, `Wolfe`/`Wolf`, `D'ESTIENNE`/`d'Estienne`),
   Norwegian farm names that move with residence (`Byre`/`Aga`,
   `Opsal`/`Barkeland`, `Pedersen`/`Myhre`), and the CJK case below. Sex is
   barely a signal — 47% female against 38% in the redundant group.
3. **In the CJK records the two fields are the wrong way round.**

       NAME '琰 瑗度 /陳郡陽夏/'   SURN '陳郡陽夏'   _MARNM '謝'

   `陳郡陽夏` is Chen commandery, Yangxia — an ancestral *place* — and `謝` (Xie)
   is the clan surname. So `_MARNM` holds the family name and `SURN` holds no
   name at all. This is the same failure `CLAUDE.md` records for `秦州成紀` and
   `秦州清水` in the Hata investigation: a Chinese place sitting in the surname
   field. A P734 mapping that trusts `SURN` proposes a place as a family name.

**Not established, and not to be guessed:** which Geni input field feeds which
tag. The reading that fits — Geni's *Maiden name* → `SURN`, Geni's *Last name* →
`_MARNM` — explains the female cases, the empty-`SURN` majority and the farm
names at once, but it is inference from the export. Confirming it means looking
at one profile's edit form on Geni against its exported record, which is
**BLOCKED-ON-USER-ACTION**.

**A minor pattern, recorded because it looks bigger than it is.** 1,191 people
hold a constant `SURN` with a *varying* `_MARNM` across their several `NAME`
records — Otto I is `SURN Liudolfinger` with `of Saxony`, `von Sachsen` and
`saksilainen` on three records. That is the language of the record showing
through a field with no language tag. It is 1.3% of the 90,901 people with more
than one `NAME`, so it is a curiosity rather than a route to the language
marking this spec lacks.

## Open, and needing Emma

- **Which `NAME` record is the label** when several share a script. Geni's file
  order is not meaningful.
- **Whether `NSFX` belongs in a label.** `Henry III King of England` carries
  `NSFX King of England`; Wikidata's own label is `Henry III of England`. So
  Geni's full string is not what Wikidata uses even when both are English.
- **`mul` labels** — Emma said "occasionally", which is not yet a rule.
- **The 501 missing English labels.** Small enough to look at individually.

## What this spec deliberately does not do

- It does not correct a label that exists.
- It does not transliterate.
- It does not pick between name variants.
- It does not touch `P735`/`P734` name items.
