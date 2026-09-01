# Step 1 — an `en` label for every individual who lacks one

Built by `scripts/build-en-label-batch.py`. **Emits nothing to Wikidata.**

Emma, 2026-08-17: *"makes en labels for every individual (so Japanese gets transcribed)... all of the en labels are done at the same time as one step, and then mul, then ja, then zh."* This is that step and only that step.

- individuals with no English label: **62522**
- of those, an `en` is now available: **25930**
- still without one: **36592**

| where the label comes from | people |
| --- | ---: |
| relationship label | 20053 |
| romanised from zh | 5459 |
| wikidata's own English label | 231 |
| romanised from ja | 187 |

**A marker is not an `en` label.** `NN` belongs in `mul`, which `build-marker-label-fixes.py` already emits, so a person whose name is only a marker is counted in the shortfall above rather than given a false name here.
