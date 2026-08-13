# How far the fetched labels resolve the Geni name vocabulary

Plan item 2 is *"derive name items but never create name items"*. Deriving
means looking up which existing item a name string corresponds to, which was
impossible offline until `reports/wikidata-labels.tsv` landed. **Being possible
and reaching anything are different questions**; this is the second.

Every distinct name string is a row in `reports/name-resolution.csv`.

## The answer

### Given-name tokens

| | distinct | share | occurrences | share |
| --- | ---: | ---: | ---: | ---: |
| resolved | 9,344 | 9.0% | 163,386 | 30.7% |
| ambiguous — several items share the label | 2,107 | 2.0% | 91,450 | 17.2% |
| no item | 92,224 | 89.0% | 276,630 | 52.1% |
| **total** | **103,675** | | **531,466** | |

### Surnames

| | distinct | share | occurrences | share |
| --- | ---: | ---: | ---: | ---: |
| resolved | 6,487 | 14.6% | 57,462 | 27.3% |
| ambiguous — several items share the label | 560 | 1.3% | 5,198 | 2.5% |
| no item | 37,432 | 84.2% | 147,993 | 70.3% |
| **total** | **44,479** | | **210,653** | |

**Distinct and occurrences differ a lot, and the second is the one that
matters for coverage.** A common name resolving is worth thousands of records;
a rare one is worth one. Both are given so neither can be quoted alone.

## The unresolved head is mostly not names

Before reading 30.7% as a name-coverage figure, look at what fails. The
commonest unresolved strings, by occurrence:

- **given-name tokens** — `I` (2,663), `II` (2,540), `of` (2,418), `NN` (2,351), `/` (1,380), `N.N.` (1,223), `III` (1,213), `Rd.` (1,114)
- **surnames** — `隴西狄道` (2,526), `曾` (2,319), `陳` (1,871), `河南洛陽` (1,528), `Chén 陳` (1,340), `京兆長安` (1,205), `藤原` (1,135), `이` (902)

The given-name head is **regnal ordinals, particles, placeholders and
punctuation** — `I`, `II`, `of`, `NN`, `/`, `N.N.`, `Rd.` None is a name, so
none can have a name item, and their presence in the denominator drags the rate
down without any name having failed to resolve. This is `todo.md` § 4's trap
appearing from the other side: a naive split puts non-names into the token
stream, and here they show up as unresolvable.

The surname head is **CJK** — and two of the commonest, `隴西狄道` and
`河南洛陽`, are *places* in the surname field, the inversion `CLAUDE.md` records
for `陳郡陽夏`. The rest — `曾`, `陳`, `藤原`, `이` — are real surnames that
almost certainly have items; they fail because **nobody in our store points at
those items**, which is the floor this measure was built to expose.

So the true resolution rate for strings that are actually names is higher than
the table says, and **it is not measured here** — separating names from
non-names is the step `todo.md` says is needed and nobody has built.

## What this cannot see

The lookup is built from **name items our own people already point at** —
`reports/name-items.csv`. A Geni name that Wikidata has an item for, which
nobody in our store carries, is invisible here and stays invisible until a
download goes wider than the family walk. So this is a **floor**, not a
measure of what Wikidata holds.

Matching is exact on the label, case- and diacritic-folded, and nothing else.
A label shared by several items is reported ambiguous rather than resolved by
picking one — that would be the guess the genealogical-matching rule forbids.
