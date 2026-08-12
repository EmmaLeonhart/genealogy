# Marriage cases, both sides

**Emma, 2026-08-10: "Marriage mapping: not decided. Show me marriage cases
first."** Walk more `FAM` records before choosing any `P26`-qualifier shape.
These are the cases. **Nothing here proposes a mapping.**

`reports/marriages.csv` holds every one: **20,059 Geni families** with both
spouses named and a marriage event. **1,251** of them have both spouses carrying
a Wikidata item, which is the comparable set.

**Qualifiers are read, not just the value** — the Henry III lesson from
`CLAUDE.md`, where a pass that read mainsnaks only reported Wikidata held nothing
when it held the answer.

## What Wikidata has, over the 1,251 comparable marriages

| | count | share |
| --- | ---: | ---: |
| `P26` present, with qualifiers | 618 | 49% |
| `P26` present, bare | 363 | 29% |
| **`P26` absent entirely** | **240** | **19%** |
| `P26` present but to a different spouse | 30 | 2% |

Qualifier use across the 981 where `P26` exists:

| qualifier | statements | share |
| --- | ---: | ---: |
| P580 start time | 556 | 57% |
| P582 end time | 257 | 26% |
| P1545 series ordinal | 256 | 26% |
| P2842 place of marriage | 87 | **9%** |
| P1534 end cause | 87 | 9% |

## The addable gap, measured

Over the 981 marriages where `P26` already exists:

| | Geni has | Wikidata has | **Geni only** |
| --- | ---: | ---: | ---: |
| marriage **date** | 981 | 556 | **425** |
| marriage **place** | 649 | 87 | **575** |

Plus the **240** marriages Wikidata does not record at all.

**Place is the striking one.** Wikidata carries `P2842` on 9% of the marriages it
records; Geni has a place string for 66% of them. That is the largest
proportional gap this project has measured on any field.

## Cases

### `P26` present, with qualifiers

    Antal Apponyi de Nagy-Appony  Q75367364  x  Maria Sophia von Montenuovo  Q75367362
      GENI      MARR 23 MAY 1878    PLAC Vienna, Vienna, Austria      children 2
      WIKIDATA  P580=+1878-05-23/p11   P2842=Q1741   refs=1

    Christian IV Oldenburg        Q153586    x  Anne Catherine Hohenzollern  Q170394
      GENI      MARR 27 NOV 1597    PLAC Haderslev, Schleswig, Danmark  children 6
      WIKIDATA  P580=+1597-11-27/p11  P582=+1612-04-08/p11  P1545=1   refs=1

**Wikidata sometimes states two start times for one marriage:**

    Ramón Berenguer 'Alfonso el Casto'  Q299156  x  Sancha de Castilla  Q296003
      GENI      MARR 18 JAN 1174    PLAC Zaragoza, Aragon, Spain      children 9
      WIKIDATA  P580 = +1174-01-18/p11  AND  +1175-01-18/p11
                P582 = +1196-04-25/p11   refs=2

    Valdemar "The Victorious"     Q157799    x  Berenguela de Portugal  Q253571
      GENI      MARR MAY 1214       PLAC Denmark                      children 4
      WIKIDATA  P580 = +1214-05-00/p10  AND  +1213-00-00/p9
                P582 = +1221-03-27/p11  P1534=Q4   refs=1

Two competing values, at different precisions, on one statement. Geni matches one
of the two in both cases. **This is the shape `reports/consistency-analysis.md`
argued for** — Wikidata's own idiom for a disputed date is more than one value —
and it is here in real data rather than as a proposal.

### `P26` present, bare — no qualifiers at all

    Jørgen Jakobsen Vind    Q2688918  x  Ingeborg Holgersdatter Ulfstand  Q110304273
      GENI      MARR 27 AUG 1620    PLAC Malmö, Malmöhus, Sverige     children 11
      WIKIDATA  (no qualifiers)   refs=0

    Adefonso III 'el Magno' Q311138   x  Xemena Garsea de Pamplona  Q1627093
      GENI      MARR 869            PLAC Asturias, Spain              children 7
      WIKIDATA  (no qualifiers)   refs=1

363 marriages where Wikidata says only *that* the marriage happened.

### `P26` absent entirely — 240 of them

    Malte Clausen Sehested  Q94899102  x  Margrethe Frederiksdatter Reedtz  Q110304140
      GENI      MARR 25 SEP 1640    PLAC Region Midtjylland, Denmark  children 9

    Ebenezer Avery          Q123900623 x  Lucy Davis  Q123900655
      GENI      MARR 3 MAY 1744     PLAC Groton, Connecticut Colony   children 9

    Tore Bolt               Q15851234  x  Ingebjørg Erlingsdatter  Q101247950
      GENI      MARR 29 SEP 1276    PLAC Norderhov Norway             children 1

Both people have items. Both items exist. Neither states the other as a spouse.

### `P26` to a different spouse — 30, and these may not be gaps

    Christian IV Oldenburg  Q153586  x  Vibeke Kruse  Q460566
      GENI      MARR 1629           PLAC (none)                       children 2

    Attila                  Q36724   x  Justa Grata Honoria  Q232271
      GENI      MARR ABT 450        PLAC **Not Married**              children 0

Christian IV appears in both this bucket and the first: Wikidata records
Anne Catherine as his spouse with `P1545 = 1`, and does not record Vibeke Kruse,
who was his mistress. **Geni is recording a union; Wikidata is recording a
marriage.** Treating this bucket as missing data would push non-marriages onto
Wikidata as marriages.

And the Attila row carries `PLAC Not Married` — prose in a structured place
field, the same fault class as Aénor's three birthplaces joined by "or".

## What this does not settle

- **No `P26` shape is proposed.** That was the point of showing cases first.
- **The 30 "different spouse" rows are not a gap** and probably should never be
  emitted; the Christian IV pair shows why.
- **`P1545` appears 256 times.** Emma already ruled that marriage ordinals derive
  from dates and that `P1545` is a cross-check, not a source — that stands, and
  these 256 are the cross-check material.
- **A Geni place string is genuinely mis-encoded, and I nearly published the
  opposite.** The row rendered as `Malm÷…` in my terminal, which I wrote off as
  console encoding. Checking the bytes rather than trusting that: the file
  contains **`Malm°`** — `U+00B0 DEGREE SIGN` where `ö` belongs. Other rows in
  the same corpus carry `Malmø` correctly and `Malmohus` unaccented, so all three
  forms of one place name coexist. How widespread the mis-encoding is has **not**
  been measured; only that it is real.
