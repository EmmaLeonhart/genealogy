# What the 769 still-ambiguous name strings actually are

**Queue item, 2026-08-18.** Offline, from the local Wikidata store — the 1,380 competing
items were all found there, so nothing was fetched.

**This corrects the queue's own account of the cause.** It said, of the open cases:

> *"A real cause visible in the 467: several are the same spelling in different
> languages… `Juan` is Chinese and Spanish; `Marie` is Japanese and French. Resolving
> those needs a view on which language a Geni name is, which is the CJK-culture problem
> and is not solved."*

**Measured: the different-language case is 12 strings of 769 — 1.6%.** It is real (`Kang`
Chinese 康 vs Korean 강; `José` Portuguese vs Spanish) and it is not the cause of anything.

## What the 769 are

| cause | strings | bearers |
| --- | ---: | ---: |
| **one item is the native-script version of the other** | **271** | 20,372 |
| other | 231 | 25,938 |
| **different characters, same romanisation** | **210** | 5,725 |
| **identical descriptions — a Wikidata duplicate** | **57** | 700 |

### 271 · one item is the native-script version of the other

`Landau` is `Q1127822` *family name* and `Q21286163` *family name (לנדאו)*. `Cohen` is
`Q1158586` and `Q66723764` *(כהן)*. `Lee` is `Q12794688` *family name* and `Q11983535`
*Korean family name (이)*.

**These are one name held as two items**, one Latin and one in its own script. **Not our
defect and not our decision** — picking one is a Wikidata modelling question, and merging
them is a Wikidata edit.

### 210 · different characters, same romanisation

`Tu` is Chinese 涂 **and** Chinese 屠. `Tachibana` is 橘 **and** 立花. `Lang` is 郎 and 狼.

**These are genuinely different names that collide when romanised**, and the two items are
correctly separate. **This bucket is unresolvable from a Latin string** — the information
needed was destroyed before the data reached us. It is the CJK problem the queue named,
but it is not the language problem: both items are the *same* language.

### 57 · identical descriptions

`Schloss` is `Q105540652` *family name* and `Q37300956` *family name*. Also `Strauss`,
`de Sousa`, `Rodríguez`. Two items, one name, **nothing distinguishing them**.

**These look like Wikidata duplicates.** Worth reporting upstream rather than choosing
between.

### 231 · other

Mixed. Some are the sex split already ruled on (`María` male vs female). Some have an item
with **no English description at all** (`John` → `Q104552334`), which is a gap in Wikidata
rather than an ambiguity.

## What this changes

**Three of the four buckets are not ours to fix.** 271 script pairs and 57 duplicates are
Wikidata modelling; 210 romanisation collisions cannot be resolved from the string. That
is **538 of 769 — 70%** — where the right action is to record the ambiguity, not resolve
it.

**The language view the queue said was needed would buy 12 strings.** Building it for this
purpose is not worth it, and the item should stop describing it as the blocker.
