# Which languages a relationship label can be generated in

**Emma asked, 2026-08-14:** *"The language things are obviously very strongly
based upon the presence of the label in the language already. I would like you to
check."*

Right — `daughter of Joe` can only be written in language L if **Joe has a label
in L**. So the ceiling on stage 2 is the relatives' label coverage, not ours.

## Measured: 40,044 items sampled from 40 of the 1,409 store shards

| language | coverage |
| --- | ---: |
| **en** | **96.10%** |
| **nl** | **81.07%** |
| de | 32.99% |
| es | 32.48% |
| fr | 31.24% |
| ast | 25.68% |
| **mul** | **25.27%** |
| sl | 21.84% |
| ca | 21.81% |
| sq | 21.31% |
| sv | 21.02% |
| it | 21.02% |
| pt | 18.07% |
| pt-br | 17.80% |
| da | 17.28% |
| ru | 16.45% |
| nb | 16.23% |
| ga | 15.63% |

**Median labels per item: 3.** Only **4.1%** of items have just one label.

## What that means for the plan

**Stage 2 is an English operation with a Dutch second, and a cliff after that.**
English at 96% means a relationship label is nearly always generable; Dutch at
81% is a genuine second; German, Spanish and French sit at a third; everything
else is a fifth or less. Generating into a language the relative lacks would mean
inventing a rendering of their name, which is not something this project does.

**`mul` is only on 25% of items**, so Emma's `mul: "NN"` is mostly *adding* a
multilingual label where none exists rather than overwriting one. That is the
right slot and it is largely empty.

**The asymmetry that decides the design:** where the relative is an item **we are
creating**, we set their labels, so we control which languages are available and
the constraint disappears. Where the relative is an **existing Wikidata item**,
the table above is a hard ceiling. So the generator has to ask, per relative,
which case it is — and the answer differs for almost every person.

## Still open

Emma's own uncertainty, unresolved: whether to run stage 2 at all for people who
already have a surname, or only for the bare `NN` ones. Not decided, and not
decided here.
