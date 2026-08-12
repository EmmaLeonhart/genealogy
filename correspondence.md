# Geni ↔ Wikidata — how the fields correspond

**What this is.** A hand-built model of how a Geni GEDCOM record maps onto a
Wikidata item, derived **one record at a time** from records Emma has actually
looked at. Emma, 2026-08-11: *"I want to go through all of the data modelling
stuff that can possibly be here to figure out what the fuck is going on with
these records. They all need to be done one by one… I want you to put together a
document of how it is that each of these corresponds, and don't make tooling for
them. Tooling is something that is going to be done all at once, once all of our
modelling is finished."*

**No code is written from this document until the modelling is finished.**

**And this is ingestion, not conversion.** Emma, same day: *"We are trying to do
an ingestion here that does not immediately get turned into wiki-dada-dada."*
Building the Wikidata-emitting end is a later part of the pipeline. Several
questions below are deliberately answered *only as far as ingestion needs*, and
say so.

**Rules of this file.**

- A row is **ESTABLISHED** only if Emma said it, and her words are quoted.
- A row is **OPEN** if we have looked and not decided.
- A row is **TO ANALYSE** if Emma assigned it to me as research rather than a
  decision — the answer comes from the data, not from her.
- Claims about what the data looks like cite the record they came from, raw.

---

## The two rules that govern everything else

### 1. Matching is genealogical only

**ESTABLISHED 2026-08-11.** Emma: *"we are first and foremost doing all this
stuff based upon genealogical links of people. I don't even want us to be doing
any kind of fuzzy search, any kind of long-distance search, based off of label
similarities or something like that. I only want us to be doing it based off of
genealogical relationships and connections and stuff. That's all I want. That is
the entirety of what I'm wanting to do."*

**The rule she gave, in her words:** *"we merge them based off of whether
something is the mother on both sides of an individual. We merge them together
unless the mothers really conflict. The same thing: if they really conflict,
we'll have to resolve it and might have it so they have a third mother or a
second mother or something."*

So a Geni person and a Wikidata item are the same person when the **mother
matches on both sides**. A genuine conflict between the two mothers is
**resolved**, not decided by picking a winner — and the resolution may leave the
person with two or three mothers rather than one.

Consequences, stated because they are load-bearing:

- **No name similarity, ever.** Not as a tiebreak, not as corroboration, not as
  a "candidate" list for a human. The fuzzy matcher in `reconcile.py` does
  exactly what this forbids and Emma ordered it removed the same day.
- **The exact `P2600` join stays** — that is Wikidata stating the Geni ID
  outright, not an inference.
- Two suspect `P2600` links are **TO ANALYSE**, below.

### 2. Conflicts are added, never corrected

**ESTABLISHED 2026-08-11.** Emma, on Geni's day-precision date meeting
Wikidata's month-precision one: *"you add the date as a conflicting fact on
Wikidata cited to Geni, citations to Geni use the reference thing (not a
qualifier) and the property Geni ID and the id. This isn't a precision rule it's
a way we deal with conflicting information."*

    <property> = <Geni's value>
        reference:  P2600 (Geni.com profile ID) = <the Geni profile ID>

A **reference**, not a qualifier. The existing Wikidata statement is untouched.
This is the general mechanism for every disagreement, not a date rule.

---

## Records looked at so far

| | who | Geni | Wikidata | note |
| --- | --- | --- | --- | --- |
| A | Arne Olson Anda, b. 1894 Norway | `6000000038740385839` | `Q16164886` | the good example |
| B | Danureja I, Java | `6000000038363753264` | `Q97255794` | **bad example** — Emma: *"the Geni ID was made by somebody who has no fucking clue what they're doing, because the person is just too non-Western for the Western data stuff to actually apply"* |
| C | Aénor of Châtellerault, b. 1103 | `6000000000701127473` | `Q507801` | **bad example** — pre-modern, no real surname |

Emma on choosing records: *"Realistically, probably people in the 1800s are the
best bet for this."*

---

## INDI — the individual's own record

### `NAME` — the line itself

**ESTABLISHED, from the specification rather than from us.** Emma: *"You realise
there's literally a rendering pipeline for GEDCOM names that you can just look
up, right? You don't need to bullshit every single one."*

GEDCOM 5.5.1: the `NAME` value is the name **as normally spoken**, with the
surname enclosed in slashes. The parts follow the order the person would have
used. So the rendered display name is the line with the slashes removed:

    1 NAME Arne Olson /Anda/            ->  Arne Olson Anda
    1 NAME Aénor /of Châtellerault/ Duchess of Aquitaine
                                        ->  Aénor of Châtellerault Duchess of Aquitaine

The display name is therefore not a separate field to hunt for. It is this line.

### Splitting several `NAME` records — **by script, not by language**

**ESTABLISHED 2026-08-11.** Emma: *"we are sorting by scripts. We are not sorting
by languages. We will sort by languages later. We are sorting by scripts right
now. Please do not overcomplicate this. This is not the completion of the
pipeline by any means."*

So: group a person's `NAME` records by writing system. Nothing assigns a
language to any of them, and nothing needs to at this stage. This supersedes the
"parked, needs linguistic judgement" state the question had been in since
2026-08-10 — the judgement was only needed for the *language* split, which is
later.

Emma's sketch of where it goes afterwards, recorded as her intent and **not**
as a rule to build: unless there is a custom display name, a single Latin display
name becomes the multilingual label; where there are several, one becomes the
label and the others aliases, or they split by language — *"but that is a part
for later on in the pipeline"*.

### `GIVN`

**OPEN.** The protocol Emma named is to iterate the given names with the
numbering — `P735` per token, each carrying `P1545` series ordinal — then the
surname.

Record A:

    1 NAME Arne Olson /Anda/
    2 GIVN Arne Olson

Wikidata has `P735 = Q645757 (Arne)` and nothing for `Olson`.

**The unresolved part:** `Olson` is a patronymic sitting in `GIVN`. Emitting
`P735 Olson` at ordinal 2 follows the protocol mechanically and may be wrong
about what `Olson` is. Not decided, and it is downstream of ingestion anyway.

**Censused 2026-08-12 — `reports/givn.md`, and it is not one record's problem.**
Of 342,340 `NAME` records carrying a `GIVN`, **130,712 (38.2%) hold more than
one token**. Within the Latin-script ones, the last token is:

| | records | share |
| --- | ---: | ---: |
| wordlike | 76,069 | 68.2% |
| **patronymic** | **27,003** | **24.2%** |
| honorific / particle / ordinal | 7,219 | 6.5% |

So roughly **one Latin multi-token `GIVN` in four ends in a patronymic** —
`Olsen`, `Olsdatter`, `Pedersdatter`, `Pedersen` are all top-twenty tokens. Arne
is not an edge case; he is the ordinary case.

**This corrects `todo.md` § 4**, which says the multi-token strings are *"most …
romanised CJK/steppe names where the extra tokens are honorifics, particles and
titles"* and that the genuine P1545 case is *"the Latin-script subset"*. The
count it gives is right; the population is not. **85% of multi-token records are
Latin-script**, and Han is the *least* multi-token script at 10.3%. Patronymics
outnumber honorifics about four to one. The conclusion survives — a naive space
split emits wrong `P735`s — but not for the stated reason.

### `SURN`

**OPEN.** Record A is the easy shape and it agrees: `SURN Anda` against
`P734 = Q16479635 (Anda)`.

The hard shapes, recorded and unresolved:

- **A toponym in the surname slot.** Record C: `SURN of Châtellerault`, which is
  the town her own birth field names; Wikidata gives her no `P734` at all. Emma
  asked to see more cases before any rule.
- **The CJK inversion**: `SURN 陳郡陽夏` (a Chinese place) against `_MARNM 謝`
  (the actual clan surname) — the wrong way round from what a `P734` mapping
  assumes.

### `_MARNM`

**ESTABLISHED — it is the married name.** Emma, 2026-08-11: *"_MARNM is married
name."*

**ESTABLISHED — identical to `SURN` means ignore it.** Emma: *"if the married
name and the surname are identical to each other, this is a simple thing where
our algorithm will just ignore the married name."* Record A fires this:
`SURN Anda` / `_MARNM Anda`.

**OPEN — what to do when it differs.** Of 244,392 records carrying the tag, 31%
duplicate `SURN`, 43% are the only surname on the record because `SURN` is empty,
and the 25% that differ are 53% male. So "differs" does not mean "married name"
either.

### A single `.` in a name field

**ESTABLISHED 2026-08-11.** Emma: *"if the surname is just a single dot, or the
married name is just a single dot or anything like that, we just pretend it
doesn't exist because that is the convention on Geni. This person would just have
their first name be the entirety of their label."*

Record B:

    1 NAME Kanjeng Raden Adipati Danureja I / Patih Cakrajaya /./
    2 GIVN Kanjeng Raden Adipati Danureja I / Patih Cakrajaya
    2 _MARNM .

### `NSFX` — and why the strip rule is refused

**ESTABLISHED 2026-08-11 — do not strip it from a Latin-alphabet name.** Emma:
*"a noble suffix or a noble particle is a legitimately common thing in English,
to the point that it makes it useless to do that rule on Latin names."*

So the earlier framing of this question — "does `NSFX` belong in a label" — was
wrong. `Duchess of Aquitaine` and `King of England` are not foreign matter to be
removed before a name is usable in English; they are how the name is written in
English. The Latin-alphabet name is taken **as it renders**, suffix included.

**Censused 2026-08-12 — `reports/nsfx.md`.** 36,072 records carry the tag, and
they hold **19,875 distinct values**, so it is an open field and not a controlled
vocabulary of titles. It appears inside the rendered display name **99.8%** of
the time, which is the GEDCOM `NPFX GIVN /SPFX SURN/ NSFX` rendering holding.

At least four different kinds of thing live in it:

| kind | examples |
| --- | --- |
| regnal ordinals, Latin | `II` 825, `I` 755, `III` 437, `IV` 196, `V` 96 |
| **regnal/generation numerals, CJK** | `一` 762, `二` 653, `三` 416, `四` 264, `五` 179 |
| generational suffixes | `Jr.` 460, `Sr.` 415, `Jr` 121, `Sr` 95 — unnormalised |
| noble titles, many languages | `Graf` 278, `Herzog` 118, `Prinz` 118, `Gräfin` 114, `książę` 94 |
| roles and epithets | `Pharaoh of Egypt` 107, `Saint` 104, `Capitán` 99 |

The CJK numerals are the finding worth carrying: **the same slot holds `II` and
`二`**, so a suffix rule written for Latin ordinals silently covers a CJK
population it was not designed for.

**Against Wikidata's own English labels**, over the 5,700 `NSFX` records whose
person has one: 536 keep every suffix token, 1,017 keep part, 4,147 keep none.
But "keeps none" splits, and the split reverses the obvious reading —

| | records | share of "keeps none" |
| --- | ---: | ---: |
| different name entirely | 1,959 | 47.2% |
| name partly shared | 1,544 | 37.2% |
| **same name, suffix dropped** | **615** | **14.8%** |

So Wikidata genuinely writes the same name minus the suffix in only **615 of
5,700 cases (10.8%)**. The rest of the divergence is the regnal-name substitution
`reports/display-names.md` already found — `Louis II` against `Louis the
Stammerer` — which is not a suffix question at all. **Emma's rule is not in
tension with Wikidata's practice nearly as often as a first reading suggested.**

---

## Labels — where they come from

**ESTABLISHED 2026-08-11.** Emma: *"my vision here is that the English language
label comes from the Latin display name… The big thing is that the multi-language
label comes from the Latin alphabet name, and the English language label will
come from it too."*

So both the `mul` label and the `en` label are the **Latin-alphabet display
name** — the rendered `NAME` line, suffix and particle included, per the rule
above. One source, two labels.

**When there is no Latin-script name at all**, a **translation** is required.
Emma: *"If there's only a name present in some sort of other script, we have to
do a translation. If you do a translation, you understand what it is that I'm
actually telling you to do."*

Recorded as it stands: a translated or transliterated label is a **value we
generated**, not a value the source held. Nothing else in this project invents
data, so this is the one place where a produced string enters the labels — and it
must be visible as such rather than blended in with names read off the record.
How that is marked is not yet decided.

**Latin names in several languages: not a problem we have measured.** Emma:
*"I don't know the degree to which we are having real issues with the names being
the Latin names in different languages. My thought is we are probably going to be
able to, at some point, determine which one we're going to be using and
categorise them based off of languages."* At some point — not now.

**And none of this is being emitted.** Emma, same message: *"We're ingesting, and
we are a long fucking way from actually putting any of this stuff on Wikidata."*

### `NICK`

**OPEN.** 66,926 records. Record C has two. Wikidata's alias slot is the obvious
counterpart; nothing decided.

### `SEX`

**ESTABLISHED and trivial.** `M` → `P21 = Q6581097 (male)`, `F` → `Q6581072
(female)`. Record A agrees.

### `BIRT` / `DEAT` — dates

**ESTABLISHED as easy.** Emma: *"The birth date and place are very easy things
that we can do. They're very easy, established things."*

Record A, exact agreement at day precision both ways:

| | Geni | Wikidata |
| --- | --- | --- |
| birth | `2 DATE 25 APR 1894` | `P569 = +1894-04-25T00:00:00Z`, precision 11 |
| death | `2 DATE 15 NOV 1984` | `P570 = +1984-11-15T00:00:00Z`, precision 11 |

**A Wikidata date cannot be read without `precision`.** `+1103-01-01` at
precision 9 means "1103"; the day components are padding. Record C is exactly
that, and additionally carries `P1480 = Q5727902 (circa)`.

**GEDCOM dates go through `genimerge.dates`, never a hand-rolled parser** — the
corpus writes BC years as a minus (`-73`), and two hand-rolled parsers have
already silently dropped all 4,750 of them.

### `BIRT` / `DEAT` — places

**ESTABLISHED — `PLAC` only, `ADDR` ignored.** Emma, 2026-08-11, choosing
between the options: **ignore `ADDR`, use `PLAC` only.**

Record A:

    2 PLAC Anda
    2 ADDR
    3 STAE Rogaland
    3 CTRY Norway

against `P19 = Q500223 (Klepp Municipality)`.

**OPEN — granularity.** Anda is a farm *in* Klepp. Geni's string and Wikidata's
item are different levels of one hierarchy, not a conflict. Nothing yet decides
which level a `PLAC` string resolves to.

**OPEN — prose inside the field.** Record C:

    2 PLAC Nieul-sur-Autize, Vendée or Château de Belin, Guyenne or Palais d'Ombrière, Bordeaux

Three candidate places joined by "or", in a field that should hold one.

### `BURI`

**ESTABLISHED — two properties, no qualifiers.** Emma, 2026-08-11: *"the date of
burial and the place of burial have their own properties. It's not done with
qualifiers, and it's simple as that."*

- place of burial → **P119**
- date of burial or cremation → **P4602**

Record C has `1 BURI / 2 DATE ABT MAR 1130` and its item carries `P119` with no
date — an addable case, not a conflict.

### `OCCU`

**OPEN.** Record A: `1 OCCU Missionær i Kina` against `P106 = Q219477
(missionary)`, whose own reference already carries `P1932 (object named as) =
Misjonær`. The Geni string additionally says *i Kina*, which `P106` does not
express. Record B has `1 OCCU` with no value at all.

### `NOTE`

**ESTABLISHED — not used.** Emma, 2026-08-11: *"The note: we don't use notes
generally."*

Recorded once as a cost rather than an objection: on record A the note is the
only place a source appears on the Geni side —

    1 NOTE {geni:about_me} * Klepp Gards- og ættesoga gjenom 400 år, 1519-1900, Anda, side 36, nr. 34d, https://www.nb.no/items/URN:NBN:no-nb_digibok_2016090948122?page=41

Geni's field-level sources have separately been shown to be plainly wrong —
Henry III's first name and death date both cite a Find A Grave memorial for his
*son* — so a Geni citation is not usable as a Wikidata reference on its face.

### `FAMS`, `RFN`, `SUBM`, `CHAN`

**ESTABLISHED — ignored on the individual's own record.** Emma, 2026-08-11:
*"we are going to ignore, for the purpose of this, FAMS, RFN, SUBM, and CHAN…
you have an extremely clear way of representing all of the information in it, and
you are going to use it."* The `FAM` records carry the family information; the
pointer lines say nothing alone.

- **`RFN`** — restates the profile ID that `P2600` already carries. Emma:
  *"anything that has Geni in it is just not useful."*
- **`SUBM`** — **ANSWERED, `reports/subm.md`.** It is the Geni **user who
  manages the profile**, and that user is themselves a Geni profile: `SUBM` ids
  share the namespace with `INDI` ids, and **657 of the 12,176 submitters also
  occur as people in our tree**. 99.6% of people carry one. The records hold a
  name and sometimes a postal address, and no other subtag. It stays ignored for
  the conversion — nothing on Wikidata records who typed a fact into a
  third-party site — but it is the only provenance the corpus has.
- **`CHAN`** — the profile's last-edited stamp.

### `OBJE`

**OPEN, not looked at.** Record C withholds 9 blocks; Henry III has 367. Nothing
has been examined.

---

## FAM — the family records

**This is where the value is, and it is the least modelled part of the file.**

Record A is the demonstration. Everything on his own record is already on
Wikidata at equal or better precision with better references. What Geni has that
Wikidata does not is the whole family:

    0 @F6000000034054654706@ FAM
    1 MARR
    2 DATE 11 NOV 1880
    1 HUSB @I6000000034054654701@     <- his father
    1 WIFE @I6000000034054746464@     <- his mother
    1 CHIL @I6000000038739592699@
    1 CHIL @I6000000038740234936@
    1 CHIL @I6000000038739979194@
    1 CHIL @I6000000038740385839@     <- him
    1 CHIL @I6000000038740360876@

`Q16164886` has **no `P22`, no `P25`, no `P3373`**. It has `P26 = Q7291689 (Randi
Anda)` while his Geni spouse-family is one line:

    0 @F6000000043188048333@ FAM
    1 HUSB @I6000000038740385839@

**OPEN — everything about the mapping.** `HUSB`/`WIFE`/`CHIL` plainly correspond
to `P22`/`P25`/`P40`/`P3373`, and no rule has been stated for any of them; nor
for `MARR`, whose date and place would hang off `P26` as qualifiers.

**But the mother edge is now load-bearing** — it is the matching key (rule 1),
so `WIFE` on a `FAMC` is not just a field to convert, it is how the two datasets
join.

Two facts recorded elsewhere that bear on it:

- **22,513 families name one spouse with no children and no marriage event** —
  corpus-wide, not a quirk. Emma reads these as relationships Geni knows about
  whose partner was outside the export's scope.
- **16,229 of 36,257 dated `FAM` records name no spouse at all** (45%). Emma:
  *"These aren't anything meaningful because they can't be represented on
  Wikidata"* — with no spouse there is no `P26` to qualify.

---

## Work assigned to me as analysis, not decision

Emma, 2026-08-11, repeatedly: the answer comes from the data and it is my job to
find it, not to label it and move on.

### The "impossible" dates

**TO ANALYSE.** `reports/consistency.md` calls 3,189 dates impossible and 1,966
implausible. Emma: *"it's your job to do analysis on these to figure out what's
actually going on with them. The chances are there is actually something going on
with them, and you're just deeming them impossible or whatever… so you have to do
the research on it."*

The report is not to be trusted as a verdict until that is done.

### The five missing minus signs

**Fix them in our data.** Emma: *"Fix them in the fucking data."* Five records —
pharaohs with positive birth years above 2026 — where the BCE minus is absent.
Corrected locally, not on Geni.

### The two suspect `P2600` links

**TO ANALYSE.** Canute I Erikska `Q442876` (0 agreements, 4 conflicts, birth 1145
against 857) and Bengt Folkesson `Q1621801`. Same treatment as the dates: work
out what is actually going on before calling either side wrong.

### `SUBM`

**TO ANALYSE**, as above.

### Duplicate profiles — merged locally, by us

**Ōjin and Wikramawardhana are ours to merge.** Emma: *"Fix them in our fucking
local data. Just merge the fucking Geni stuff within our data… I have merged them
on Geni, but it's not going to appear for you because the export's already done.
You've got to fucking merge them yourself."*

So this is **not** blocked on anything. The discriminator that identified both is
the **shared `FAMC`** — the same structural, genealogical evidence rule 1 relies
on, and not the names, which is where the two records differ most.

---

## Decided elsewhere, recorded here because it bears on the model

- **Creating new items is the point.** Emma, 2026-08-11: *"We create new people
  and new name items. This is literally the fundamental purpose of this entire
  project."* How much name-item creation is needed depends on what share of names
  already exist.
- **Name items must be downloaded.** The store holds people; 0.4% of referenced
  name items are in it, so no name resolves offline. Emma chose a bulk
  `wikidownload` pass fetching items with `P31` = family name / given name.
- **Labels are only in scope for people carrying both IDs**, Wikidata is
  definitive for a person's label, and someone who already has an English and a
  Japanese label is parked immediately (2026-08-10).

---

## What has not been looked at at all

- `OBJE` image blocks, on any record.
- `FAM`-level `MARR` place and address.
- Any record where Geni and Wikidata disagree on a **relationship** — 134 `P22`
  and 90 `P25` conflicts exist.
- Any record where Wikidata's family is *richer* than Geni's.
- Divorce, adoption, illegitimacy, or any `FAM` with a non-standard structure.
