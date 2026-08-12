# Surnames that are places — the spread, before any rule

**Emma asked for exactly this, 2026-08-11.** Shown Aénor of Châtellerault —
`SURN of Châtellerault`, birthplace Châtellerault, and no `P734` on her Wikidata
item at all — and offered three options, she chose **"Show me more cases first."**
So this is the spread, and it proposes nothing.

**No place-name list was used.** That would be the fuzzy matching this repo
refuses everywhere else. The evidence comes from the records:

- **self-evidencing** — the surname, minus any leading particle, appears in one
  of *that person's own* `PLAC` / `CITY` / `STAE` / `CTRY` strings. The record
  itself says the word is a place. This is the Aénor signature.
- **particle** — the surname begins `de`, `von`, `van`, `of`, `di`, `av`… A list
  of *particles*, not of places. It labels a row; it does not classify a surname.

`reports/toponym-surn.csv` holds every row. **37,096** of them.

| signal | rows |
| --- | ---: |
| particle only | 25,624 |
| self-evidencing | 8,649 |
| self-evidencing + particle | 2,823 |

Particles, commonest first: `de` 19,439 · `von` 4,719 · `van` 1,475 · `of` 949 ·
`da` 395 · `di` 385 · `del` 188 · `zu` 187 · `du` 166 · `des` 152.

## The thing that shows up immediately: two different populations

The commonest self-evidencing surnames are **not** the noble ones:

    113x Øksnevad   97x Lyse    90x Hauge    82x Württemberg   79x Lea
     73x Braut      70x Espedal 70x Berge    68x Nassau        68x Bore
     66x Kleppe     65x Grude   63x Sveinsvoll  61x Tjørhom    53x Nese

**Those are Norwegian farm names** — Rogaland farms, the same pattern
`CLAUDE.md` already records under `_MARNM` as *"Norwegian farm names that move
with residence"*. They dominate the self-evidencing group, and they are a
different thing from `of Württemberg`: in Norwegian usage a farm name **is** the
surname, even though it is also, literally, a place.

The territorial-dynasty cases are the minority of the group, not the shape of it.

## Cases, raw

### self-evidencing — the surname is in the person's own places

    SURN 'Württemberg'   Q213618   P734 yes
      Louis Fredrick Alexander /Württemberg/ Duke
      places  Treptow, Am Riga; Pommern; Deutschland(HRR); Trzebiatów; Pomerania

    SURN 'Württemberg'   Q63472    P734 no
      Friedrich Karl /Württemberg/ Herzog zu Württemberg-Winnental
      places  Stuttgart; Württemberg; Deutschland(HRR); Winnenthal

    SURN 'Sørum'         Q5890072  P734 no
      Jon Hafthorsson /Hafthorssen Sorum/
      places  Skedjuhof, Sudreim (Sørum), Akershus; Viken; Norway

    SURN 'Bjarkøy'       Q101247946 P734 no
      Ingeborg Erlingsdotter /Bjarkøy/
      places  Bjarkøy; Troms; Norway

    SURN 'Namur'         Q2104024  P734 no
      Clémence /Namur/ Countess of Burgundy
      places  Namur; Région Wallonne; Belgique

    SURN 'Willis'        Q104006558 P734 no
      Lewis /Willis/
      places  Fredericksburg; Virginia; Colonial America; Willis Hill Cemetery

Note the last one. `Willis` is self-evidencing only because he is buried in
**Willis Hill Cemetery** — a place named *after* the family, not a family named
after a place. The signal runs backwards there, and nothing in the data
distinguishes the two directions.

### self-evidencing + particle

    SURN 'de Mauléon'    Q56285202 P734 no    Arengarde /de Mauléon/    places Mauléon; Poitou-Charentes
    SURN 'de Castilla'   Q236990   P734 no    Urraca /de Castilla/ reina consorte de Portugal
    SURN 'di Salerno'    Q2595342  P734 no    Guaimar III /of Salerno/  places Campania; Salerno; Italy
    SURN 'de Créquy'     Q555033   P734 no    Jean /de Créquy/          places Créquy; Nord-Pas-de-Calais
    SURN 'von Württemberg' Q61169  P734 no    Eberhard Ludwig /von Württemberg/ Herzog
    SURN 'av Danmark'    Q359588   P734 yes   Eric V Christofferson /Klipping (Glipping)/ King of Denmark

### particle only

    SURN 'de Saboya'              Q32432  P734 yes   Amedeo I /di Savoia/
    SURN 'de Habsbourg-Lorraine'  Q47365  P734 yes   Maria Antonia Josefa Johanna /Habsburg-Lothringen/
    SURN 'von Habsburg-Lothringen' Q51056 P734 yes   Franz Joseph I
    SURN 'von Östereich'          Q151321 P734 yes   Leopold II /Habsburg/
    SURN 'de Provenza'            Q228885 P734 no    Éléonore /de Provence/ Reine Consort d'Angleterre
    SURN 'de Vienne'              Q110602552 P734 no Jeanne /de Vienne/         places (none recorded)
    SURN 'el Emplazado'           Q316859 P734 no    Fernando IV 'el Emplazado' /de Castilla y León/

`el Emplazado` is **the Summoned** — an epithet, caught because `el` is in the
particle list. A plain false positive, left in rather than quietly filtered, so
the list's failure mode is visible.

## What Wikidata itself does, against a base rate

A percentage here is worthless without the rate it is being compared to.

**Base rate: 6,287 of 14,102 linked people carry no `P734` — 44.6%.**

| signal | has P734 | none | no-P734 rate | against base |
| --- | ---: | ---: | ---: | ---: |
| self-evidencing | 76 | 125 | 62% | **+18 points** |
| particle only | 375 | 1,263 | 77% | **+33 points** |
| self-evidencing + particle | 86 | 366 | 81% | **+36 points** |

Both signals push the same way and they compound. **Wikidata's own editors assign
a family-name item to these people markedly less often than to everyone else.**

And the cases show what the exceptions are: the `P734`s that *do* exist sit on
**dynastic** names — Habsburg-Lothringen, Savoia, Østerreich — while the ones
that do not sit on **territorial bynames** of individuals: de Provence, de
Castilla, of Württemberg, de Créquy. That distinction is visible in the data. It
is not proposed as a rule.

## What this does not settle

- **Norwegian farm names are the largest self-evidencing group and are not
  toponymic bynames in the same sense.** Any rule that screens on "the surname is
  a place" hits 8,649 rows of which the plurality are ordinary Norwegian
  surnames.
- **The signal has a direction problem** — `Willis` / Willis Hill Cemetery.
- **No rule is proposed.** Emma asked to see cases before one exists, and this is
  the cases.
