# What a person item looks like, taken from what Emma actually builds

Read off `Q467497` and everything it links to. First captured 2026-08-22, re-read
2026-08-23, **re-read again 2026-08-24 against the live items** — she is working through this by hand and the shape is the template for the
whole expansion programme, so this file tracks what she is actually doing rather than what
a generator assumed.

## Where she has got to

| item | who | state |
| --- | --- | --- |
| `Q141152512` | Eivind Aadnesson Garborg — father | full: dates, names, spouse, 3 children |
| `Q141152523` | Ane Oline Jonsdatter Raugstad — mother | no dates, no name properties yet |
| `Q141152600` | Stena Eivindsdatter Garborg — sister | parents + sibling link, no dates |
| `Q141152614` | Jon Eivindson Garborg — brother | parents, no dates |
| `Q141152710` | **Aadnesson** — a patronymic name item | `P31` → `Q110874` and nothing else |

**Four of the ten created.** Six siblings still absent: Samuel, Even, Inger Marie, Abel,
Ole, Ane Oline "Lena".

**Changed since 2026-08-22:** `Q467497` gained `P22`, `P25` and `P3373`; `Q141152614` was
created and given `P22`/`P25`; `Q141152523` gained its third `P40`. The links the generated
batch left as a commented second pass are the ones she has been doing by hand.

## The shape

**Reference is `P2600` used as a reference snak** — not `P854` + `P813`. A statement reads
*Geni.com profile ID = 6000000003492005111*.

**Only some statements carry it, and the split is consistent.** Referenced: `P569`, `P570`,
`P22`, `P25`, `P26`, `P40`. Unreferenced: `P31`, `P21`, `P2600`, `P734`, `P735`, `P5056`.
Genealogical and biographical claims are cited; identity and name scaffolding is not.

**Relationships are reciprocal.** Eivind carries `P40` three times — Arne, Stena, Jon —
while each child carries `P22` and `P25`. `P26` runs both ways between the parents. And
`P3373` runs both ways between Arne and Stena.

**`P3373` *sibling* IS used**, against the tidiness argument that shared parents make it
redundant.

**Labels are `en` and `mul`, the same string. No descriptions at all** — every one of the
five is description-empty.

**The label is the name as used.** Geni holds `Stine "Stena" Eivindsdatter Garborg`; her
label is `Stena Eivindsdatter Garborg`. **This is not a shortening rule** — `Jon Eivindson
Garborg` keeps his full name. What happened is that Geni wrapped the nickname in quotes and
she took the nickname; where there is no nickname the name stands.

**Names are modelled, and this is the part a generator misses.** Eivind carries:

    P735  given name           Q3358418   Eivind      (existing item)
    P734  family name          Q30250555  Garborg     (existing item)
    P5056 patronym or matronym Q141152710 Aadnesson   (SHE CREATED THIS)

The patronymic item is **minimal**: labels `en` and `mul`, `P31` → `Q110874` *patronymic*,
nothing else. No `P1705`, no `P282`, no `P407` — the measurement in `CLAUDE.md` found those
on most existing patronymic items, and she does not add them.

**Name modelling is applied incrementally, not uniformly.** Eivind has all three name
properties; Ane Oline has none yet. Dates likewise — only Eivind has `P569`/`P570`. So the
absence of a property on a given item means *not yet*, not *deliberately omitted*.

## Where the generated batch was wrong

`reports/wikidata-garborg.qs`, built 2026-08-22, differed on six counts:

- **Reference form** — it used `S854` + `S813`; she uses `P2600`.
- **No name properties at all** — no `P735`, `P734`, `P5056`, and no creation of the
  patronymic item. The largest gap, and it is the whole of `name modelling.txt`.
- **Argued against `P3373`** as redundant. She uses it, both ways.
- **One-directional relationships** — `P22`/`P25` on children only, no `P40` on parents.
- **Suggested `en` descriptions.** She writes none.
- **Kept the full Geni string as the label**, rather than the name as used.


## The regenerated batch, 2026-08-23

`reports/wikidata-garborg.qs` is rebuilt to this model. What changed, and why the old one
could not simply be left in place:

- **It opened with `CREATE` for Eivind and Ane Oline.** Both exist now — `Q141152512` and
  `Q141152523` — so running it would have minted duplicate items for real people. That is
  the reason this file was regenerated rather than annotated.
- **Reference is `S2600 "<geni id>"`**, not `S854` + `S813`.
- **No descriptions**, and `P3373` *sibling* emitted both ways.
- **The links come earlier now.** The old batch deferred every relationship to a commented
  second pass because QuickStatements V1 cannot point at a QID a `CREATE` in the same run
  has just minted. The parents have QIDs today, so each new sibling gets `P22`, `P25` and
  `P3373` in the first pass. Only what points *at* the six new items is still deferred.
- **Dates only where they are missing** — Ane Oline, Stena, Jon. Eivind and Arne already
  carry `P569`/`P570`, and a second birth date with a different reference is noise.

**Name properties are still not emitted, on purpose.** Eivind has `P735`, `P734` and the
`P5056` patronym item Emma created (`Q141152710` *Aadnesson*). Doing the same for the others
needs the QID of each given-name item and a new patronymic item per patronym —
*Jonsdatter*, *Eivindsdatter*, *Eivindsen*, *Eivindson*. Guessing a name-item QID is the
error this repo keeps paying for, so they are listed in the file's trailer for Emma rather
than generated.


## Re-read 2026-08-24 — all ten exist, and two claims above are now wrong

Six items were read live: `Q467497`, `Q141152512`, `Q141152523`, `Q141152600`,
`Q141162040`, `Q141162043`, plus the name item `Q141152710`. Emma authorised reading
these specific pages; it was one batched read, not the ad-hoc lookup `CLAUDE.md` forbids.

**All ten people now have items.** The "four of the ten" table above is superseded —
Samuel `Q141162040`, Even `Q141162041`, Inger Marie `Q141162043`, Abel `Q141162044`,
Ole `Q141162045` and Ane Oline "Lena" `Q141162046` were all created since the 08-23 read.

**Dates are no longer outstanding.** Ane Oline, Stena and Jon all carry `P569` and `P570`
now. The 08-23 note that only Eivind had dates is out of date.

### The citation split is NOT consistent — that claim above was wrong

It was stated as a rule and the live items refute it. Measured per item:

| item | referenced | not referenced |
| --- | --- | --- |
| `Q141152512` Eivind | `P40` (first three only), `P569`, `P570`, `P26` (two refs) | `P31`, `P21`, `P2600`, `P734`, `P735`, `P5056` |
| `Q141152600` Stena | `P31`, `P21`, `P22`, `P25`, `P3373`, `P569`, `P570` | `P2600` |
| `Q141162040` Samuel | `P31`, `P22`, `P25`, `P3373`, `P569`, `P570` | **`P21`**, `P2600` |
| `Q141162043` Inger Marie | `P31`, `P22`, `P25`, `P3373`, `P569`, `P570` | **`P21`**, `P2600` |
| `Q141162046` Ane Oline "Lena" | `P22`, `P25`, `P3373`, `P569`, `P570` | **`P31`**, **`P21`**, `P2600` |

So `P31` *instance of* is cited on three of the five and `P21` *sex or gender* on one of
them, in no order that tracks creation date — Lena was made in the same sitting as Samuel
and Inger Marie and carries neither. What holds across all of them is
narrower: **`P2600` itself never carries a reference** — it *is* the reference — and every
date and every relationship does. Treat identity as *usually* uncited rather than as a
rule, and do not "correct" an item to match the pattern.

### The name qualifiers in `name modelling.txt` are not in the items

`Q141152512` is still the **only** one of the ten carrying name statements, and all three
are bare:

    P735  Q3358418   Eivind      -- no P1545, no P7452
    P5056 Q141152710 Aadnesson   -- no P144
    P734  Q30250555  Garborg

`name modelling.txt` prescribes `P1545` *series ordinal* and `P7452` → `Q3409033`
*usual forename* on the given name, and `P144` *based on* → the father on the patronym.
None is present. **This is weak evidence about the multi-name case** — Eivind has one
given name, so an ordinal of 1 is the least useful place for it, and no item with two given
names carries name statements yet. It is strong evidence about `P144`: the patronym
*Aadnesson* names his father Aadne, and the link is simply not there.

`docs/` records what she builds; `name modelling.txt` records what she wants. Where they
disagree the spec is not overruled by the backlog — but a generator should not claim the
items already look like the spec.

### The nickname rule does not generalise — two cases, handled differently

| Geni | her label |
| --- | --- |
| `Stine "Stena" Eivindsdatter Garborg` | **`Stena Eivindsdatter Garborg`** — `Stine` dropped |
| `Inger Marie "Mary" Eivindsdatter Garborg` | **`Inger Marie Mary Eivindsdatter Garborg`** — all kept |
| `Ane Oline "Lena" Eivindsdatter Garborg` | **`Ane Oline Lena Eivindsdatter Garborg`** — all kept |

Three cases, and **Stena is the only one that loses a token**. *Stena* is a short form of
*Stine*, so keeping both would repeat one name; *Mary* and *Lena* sit beside given names
they are not variants of. So the default is **strip the quote marks and keep every
token** — exactly what `qs()` does — and Stena is a one-person exception rather than a
rule the generator is missing. Do not build the exception into the generator; it needs a
judgement about whether two tokens are the same name.

### Everything else held

- **Labels are `en` and `mul`, the same string.** No item carries `ja` or `zh` yet, so her
  2026-08-24 instruction to add them is outstanding work, not something already done.
- **No descriptions, no aliases, no sitelinks** on any of the ten.
- **The name item is minimal.** `Q141152710` *Aadnesson*: `en` and `mul` labels, `P31` →
  `Q110874` *patronymic*, and nothing else — no description, no `P144`, no `P407`.
- **`P3373` runs both ways**, and the later items each carry three sibling links.
- **Never used on any item:** `P19` *place of birth*, `P20` *place of death*, `P119` *place
  of burial*, despite Geni holding those values.

### What this changes for the generator

- **`P5056` is emittable now.** `reports/wikidata-garborg-day.qs` emits zero on the
  grounds that no patronymic item exists. *Aadnesson* does. Only that one — the other
  patronyms still need items.
- **Do not emit `P1545`/`P7452`/`P144`** as though matching her items; they match the spec
  instead, which is a defensible choice but should be a stated one.
- **`Q467497` is a community item**, ~120 properties, most of them external identifiers.
  It is not a template for anything and should not be read as one.
