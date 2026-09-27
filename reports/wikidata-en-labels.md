# Step 1 — an `en` label for every individual who lacks one

Built by `scripts/build-en-label-batch.py`. **Emits nothing to Wikidata.**

All the `en` labels are done at once, as one step, so Japanese gets transcribed -- then `mul`, then `ja`, then `zh`. This is that step and only that step.

- individuals with no English label: **239605**
- of those, an `en` is now available: **176844**
- still without one: **62761**

| where the label comes from | people |
| --- | ---: |
| relationship label | 168368 |
| romanised from zh | 8053 |
| wikidata's own English label | 225 |
| romanised from ja | 198 |

**A marker is not an `en` label.** `NN` belongs in `mul`, which `build-marker-label-fixes.py` already emits, so a person whose name is only a marker is counted in the shortfall above rather than given a false name here.
