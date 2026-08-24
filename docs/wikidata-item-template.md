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


## Re-read 2026-08-24 from the FULL items — and a retraction

**Emma:** *"you're supposed to download the full wikidata items for the people I've
edited to get the modelling not look at my edit history to see what's in them."*

An earlier pass today read each item through a fetch-and-summarise channel and wrote its
output into this file, the artifact and a commit message. **Three of its findings were
false.** `out/garborg-full-items.json` — all 14 items, fetched once via
`genimerge.wikidata.full_entities` — is the real thing, and
`scripts/garborg-modelling.py` derives everything below from it offline.

### What the summarised read got wrong

- **It reported `Q467497` Arne Garborg as having no `P22`, no `P25` and no `P3373`**,
  answering ABSENT to a question posed narrowly to be reliable. He has all three:
  `P22` → `Q141152512`, `P25` → `Q141152523`, `P3373` → Stena and Jon.
  It was reported as "the single highest-value outstanding edit in the programme". It was
  not an edit at all.
- **It invented the claim that the citation split is inconsistent.** It reported `P31`
  referenced on some items and `P21` on one. Counted over all 14 full items, **`P2600` is
  never a reference on `P31` or `P21`, anywhere.** The original modelling note — dates
  and relationships cited, identity and names not — was correct and was "corrected"
  wrongly.
- **It could not see six of the fourteen items at all**, and it mislabelled properties
  freely: `P2600` as "Peruvian NLB", `P1411` as "Nobel Prize recipient".

**The lesson is the instruction:** a summary of an item is not the item. Anything that
decides what to emit gets read from the downloaded JSON.

### The modelling, counted from the full items

**Every one of the eleven items she created carries exactly:** `P31`, `P21`, `P2600`,
`P569`, `P570`, and then `P22`/`P25`/`P3373` for a child or `P26`/`P40` for a parent. The
shape is uniform — there is no partial item among them.

| | items |
| --- | --- |
| `P735` *given name* | `Q141152512` Eivind only |
| `P734` *family name* | `Q141152512` Eivind only |
| `P5056` *patronym or matronym* | `Q141152512` Eivind only → `Q141152710` *Aadnesson* |
| `P19`, `P20`, `P119`, `P1477` | **none of them** |

**References are `P2600` and nothing else, on exactly these properties:** `P3373` (×24),
`P569` (×10), `P570` (×10), `P22` (×8), `P25` (×8), `P40` (×5), `P26` (×4). Never on
`P31`, `P21`, `P2600`, `P735`, `P734` or `P5056`. The `P248`/`P813`/`P143` references that
appear in the data are all on `Q467497`, `Q3143008` and `Q11959067` — community items —
and are not hers.

**No qualifier she added appears anywhere.** No `P1545` *series ordinal*, no `P7452`
*reason for preferred rank*, no `P3831`, no `P144` *based on*. The only qualifiers in the
14 items are on `Q467497` and `Q3143008`: `P580`/`P582`/`P12506` on `P26`, `P17` on
`P19`/`P20`, and one `P7452` on each of `P569`/`P570` — all community-added.

**Labels: `en` and `mul`, the same string, on all eleven.** No description, no alias, no
sitelink on any of them. `Q467497` has 45 label languages including `ja` and `zh` and
**no `mul` label**; `Q3143008` and `Q11959067` do have `mul`.

**The name item is minimal.** `Q141152710` *Aadnesson*: `en` and `mul` labels, `P31` →
`Q110874` *patronymic*, nothing else.

### The nickname label

| Geni | her label |
| --- | --- |
| `Stine "Stena" Eivindsdatter Garborg` | **`Stena Eivindsdatter Garborg`** — `Stine` dropped |
| `Inger Marie "Mary" Eivindsdatter Garborg` | **`Inger Marie Mary Eivindsdatter Garborg`** — all kept |
| `Ane Oline "Lena" Eivindsdatter Garborg` | **`Ane Oline Lena Eivindsdatter Garborg`** — all kept |

Stena is the only one that loses a token, and *Stena* is a short form of *Stine* where
*Mary* and *Lena* are not variants of the names beside them. So the default is **strip the
quote marks and keep every token** — what `qs()` already does — with Stena a one-person
judgement rather than a rule to automate.

### What is actually outstanding

- **Names on ten of the eleven.** Only Eivind has any. This is the whole gap.
- **`Q467497` needs `P3373` to six more siblings** (he has Stena and Jon) and has no
  `P5056`.
- **No item carries `ja` or `zh`** except the three community ones, so her instruction to
  add them is untouched work.
