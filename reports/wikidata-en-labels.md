# Step 1 — an `en` label for every individual who lacks one

Built by `scripts/build-en-label-batch.py`. **Emits nothing to Wikidata.**

All the `en` labels are done at once, as one step, so Japanese gets transcribed -- then `mul`, then `ja`, then `zh`. This is that step and only that step.

- individuals with no English label: **184299**
- of those, an `en` is now available: **132011**
- still without one: **52288**

| where the label comes from | people |
| --- | ---: |
| relationship label | 126168 |
| romanised from zh | 5419 |
| wikidata's own English label | 230 |
| romanised from ja | 194 |

**A marker is not an `en` label.** `NN` belongs in `mul`, which `build-marker-label-fixes.py` already emits, so a person whose name is only a marker is counted in the shortfall above rather than given a false name here.
