# People Geni records as having no surname

Emma, 2026-08-18: **"Mononyms are `Name /./`"** — Geni writes an explicit full stop in the GEDCOM surname slot to say *this person has no surname*. That is a positive statement, and different from an empty slot, which says nothing. Both are counted here and kept apart.

| surname slot | people |
| --- | ---: |
| `/./` — Geni says there is no surname | 2,817 |
| `//` — the slot is simply empty | 92,772 |
| **total** | **95,589** |

The first version of this script measured only the second row, because it read a `.` as a surname and skipped exactly the people it was looking for.

## What they get

Emma, same day: *"if it repeats, it's a name. If it repeats over 10 times, I think that was our actual criterion. […] People with mononyms get a first name if it's a repeated name."*

| | people |
| --- | ---: |
| qualify for a `P735` given name | 1,651 |
| …of those, in the `/./` form | 194 |
| a marker rather than a name | 41,321 |
| the name appears exactly once | 46,435 |

The qualifying people share **76 distinct names**, which is why the rule is worth having: a few name items cover thousands of people. 54,739 of all these people have a single given token; the rest have several and still no surname, which is ordinary in the Indonesian and Javanese records this form is common in.

**The marker vocabulary is imported from `scripts/labels.py`, not redefined.** The first version carried its own English-only list and ranked `Ukjent` (Norwegian) and `未知` (Chinese) among Anna, Anders and Lars as if they were names. `ukjent` was already in `labels.py` — Emma: *"I thought that was in the logic"* — and `未知` was the real gap, now added there at 204 occurrences. Those people are not discarded: *"Ukjent and 未知 get the mul NN treatment"*, so they keep `NN` in `mul` and gain descriptive labels in other languages. They are excluded here only from becoming a given name.

## The most common qualifying names

| name | people |
| --- | ---: |
| Anna | 76 |
| Anders | 70 |
| Mohammed | 70 |
| Ali | 46 |
| Lars | 46 |
| Maria | 45 |
| Name Not Known | 45 |
| Olof | 44 |
| Nils | 42 |
| Erik | 40 |
| Unknown Wife | 37 |
| Ahmed | 33 |
| Johan | 32 |
| Per | 32 |
| Johannes | 30 |
| Ingeborg | 28 |
| Ola | 28 |
| Hans | 27 |
| Isteri | 27 |
| alHassan | 26 |
| alHussein | 26 |
| Abdullah | 24 |
| Johan Johansson | 24 |
| Daughter | 23 |
| Jon | 23 |
| Karin | 22 |
| Peder | 22 |
| Maria Johansdotter | 21 |
| Ole | 21 |
| Brita | 20 |
| Knut | 19 |
| Marta | 19 |
| David | 17 |
| .... | 16 |
| CHANDRA | 16 |
| Kerstin | 16 |
| Margareta | 16 |
| Son | 16 |
| Sven | 16 |
| Anne | 15 |
