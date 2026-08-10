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

## Open, and needing Emma

- **Which `NAME` record is the label** when several share a script. Geni's file
  order is not meaningful.
- **Whether `NSFX` belongs in a label.** `Henry III King of England` carries
  `NSFX King of England`; Wikidata's own label is `Henry III of England`. So
  Geni's full string is not what Wikidata uses even when both are English.
- **What `_MARNM` is.** 55% of name records carry it, it is a non-standard tag,
  and nothing in the export says what Geni means by it. It is the second most
  common subtag and completely undefined here.
- **`mul` labels** — Emma said "occasionally", which is not yet a rule.
- **The 501 missing English labels.** Small enough to look at individually.

## What this spec deliberately does not do

- It does not correct a label that exists.
- It does not transliterate.
- It does not pick between name variants.
- It does not touch `P735`/`P734` name items.
