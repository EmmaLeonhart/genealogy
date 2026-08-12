# Family links, and the parents that would be invented

Plan item 5. Emma, 2026-08-12: *"And family links. Noting that sibling
relationships without parents need to get two parents that are 'father of x and
y' and 'mother of x and y' and geni linked if possible. Mother father spouse and
child is easier."*

Two halves, different in kind. The links are **conversion**; the invented parents
are the first step in this plan that **creates data**, so the shapes were counted
before anything was generated and the placeholders live in their own file.

Matching is genealogical only, so nothing here uses a name to decide anything.
Names are used solely to *label* an invented parent.

## The links — `reports/derived-family.csv`, one row per person

| | people |
| --- | ---: |
| father recorded | 231,472 |
| mother recorded | 178,656 |
| spouse recorded | 125,890 |
| at least one child | 138,511 |

Over 298,591 people and 149,613 families. Each row carries the related person's
Geni ID and, where there is one, their QID — so a link is emittable only when
both ends exist on Wikidata, which the file makes checkable rather than assumed.

## Family shapes — the census before inventing anything

| shape | families |
| --- | ---: |
| children, both parents | 53,964 |
| **children, father only** | **36,097** |
| one spouse alone | 33,889 |
| couple, no children | 16,868 |
| **children, mother only** | **4,787** |
| one child, no parent recorded | 3,758 |
| **children (plural), no parent recorded** | **250** |

## The case Emma named is 250 families

`reports/invented-parents.csv` — **500 placeholders over 250 families**, two per
family, labelled from the children exactly as she specified:

    father of Mary Payne and Lucy Payne
    father of Frances Moncure and John Moncure Jr. and Ann Moncure
    father of Agatha Johansdotter Læstadia, Anders Johannesson Læstadius,
             Johannes Læstadius and Sara Johansdotter Læstadia

Group sizes: 194 families of two children, 33 of three, 14 of four, two of five,
six of six, one of nine.

**"Geni linked if possible" barely applies.** Only **17 of the 250** groups have
even one child carrying a QID. The other 233 would attach invented parents to
children who do not exist on Wikidata either, so the placeholder cannot be
anchored to anything already there.

## Two adjacent populations her rule does not cover

**These are not proposed. They are named because the rule as given stops short of
them and the sizes are lopsided.**

- **40,884 families have exactly one recorded parent** — 36,097 father-only,
  4,787 mother-only. Her rule covers families with *no* parent. Whether a
  single-parent family gets its missing parent invented is not stated, and the
  population is **163 times** the one she described.
- **3,758 families have one child and no parent.** With a single child there is
  no sibling relationship, so by her wording — *"sibling relationships without
  parents"* — they are out of scope. Correct as written, and worth seeing.

**NEEDS-DECISION — Emma**, on both.

## What is not done

- **Nothing is emitted.** The placeholders are proposals in a CSV; no item is
  created anywhere.
- **No `P3373`.** Her approach routes siblings through invented parents rather
  than stating sibling links directly, which is the Wikidata-preferred shape —
  recorded because it is a consequence of her rule rather than a separate
  decision.
- **No spouse link is qualified.** Marriage dates and places are plan item 6;
  `reports/marriages.md` already holds the cases and the gaps.
