# What a person item looks like, taken from what Emma actually built

**Read off Q467497 and the five items around it on 2026-08-22**, after she created
Arne Garborg's father, mother and two siblings by hand. She asked for this explicitly:
the shape those items are in *now* is the template for the expansion programme, not
whatever a generator would have emitted.

The QuickStatements batch I built that morning (`reports/wikidata-garborg.qs`) got
several things wrong. They are listed at the bottom, because the corrections are the
useful part.

## The items she made

| item | who |
| --- | --- |
| `Q141152512` | Eivind Aadnesson Garborg — father |
| `Q141152523` | Ane Oline Jonsdatter Raugstad — mother |
| `Q141152600` | Stena Eivindsdatter Garborg — sister |
| `Q141152614` | Jon Eivindson Garborg — brother |
| `Q141152710` | **Aadnesson** — a *patronymic* name item she created |

## The shape

**Labels: `en` and `mul`, the same string, nothing else.** No other languages, and
**no descriptions at all** — every one of the five is description-empty.

**The label is the name as used, not the full Geni string.** Geni holds
`Stine "Stena" Eivindsdatter Garborg`; her label is `Stena Eivindsdatter Garborg`. The
nickname won and the formal first name was dropped.

**The reference is `P2600` itself, used as a reference snak** — not `P854` *reference
URL* plus `P813` *retrieved*. A statement's reference reads *Geni.com profile ID =
6000000003492005111*. This is tighter than a URL and matches the repo's own rule that the
Geni ID is the primary key.

**Only some statements carry that reference.** Referenced: `P569`, `P570`, `P22`, `P25`,
`P26`, `P40`. Unreferenced: `P31`, `P21`, `P2600`, `P734`, `P735`, `P5056`. So the
genealogical and biographical claims are cited and the identity/name scaffolding is not.

**Relationships go on both sides.** Eivind carries `P40` *child* three times — Arne,
Stena and Jon — while each child carries `P22` and `P25`. The spouse link is reciprocal
too: Eivind `P26` → Ane Oline and Ane Oline `P26` → Eivind.

**`P3373` *sibling* IS used.** Stena carries `P3373` → Q467497.

**Names are modelled, and this is the part a generator would miss entirely.** Eivind has:

    P735  given name           Q3358418   Eivind      (an existing item)
    P734  family name          Q30250555  Garborg     (an existing item)
    P5056 patronym or matronym Q141152710 Aadnesson   (SHE CREATED THIS)

`Q141152710` is `Aadnesson`, labelled `en` and `mul`, whose only claim is `P31` →
`Q110874` *patronymic*. That is `name modelling.txt` being applied: the patronymic gets
its own property and its own item, parallel to given name and family name.

## Where the generated batch was wrong

- **Reference form.** It emitted `S854` + `S813`; she uses `P2600` as the reference.
- **No name properties at all.** No `P735`, no `P734`, no `P5056`, and no creation of the
  patronymic item. This is the largest gap — it is the whole name model.
- **Siblings.** The batch argued *against* `P3373` on the grounds that shared `P22`/`P25`
  makes it redundant. She uses it. The argument was about tidiness; hers is about the
  statement being present.
- **One-directional relationships.** It put `P22`/`P25` on children only. She also puts
  `P40` on the parents.
- **Descriptions.** It suggested `en` descriptions. She writes none.
- **Labels.** It kept the full Geni string minus quote marks. She uses the short form.

## What is still open

She has created four of the ten and is still working. Five siblings have no item yet, and
the ones that exist carry no dates. The 07:28 cron re-reads these items daily so this file
tracks what she is actually doing rather than what it assumed on the first pass.
