# Step 1 — an `en` label for every individual who lacks one

Built by `scripts/build-en-label-batch.py`. **Emits nothing to Wikidata.**

All the `en` labels are done at once, as one step, so Japanese gets transcribed -- then `mul`, then `ja`, then `zh`. This is that step and only that step.

- individuals with no English label: **194804**
- of those, an `en` is now available: **140445**
- still without one: **54359**

| where the label comes from | people |
| --- | ---: |
| relationship label | 133470 |
| romanised from zh | 6551 |
| wikidata's own English label | 230 |
| romanised from ja | 194 |

**A marker is not an `en` label.** `NN` belongs in `mul`, which `build-marker-label-fixes.py` already emits, so a person whose name is only a marker is counted in the shortfall above rather than given a false name here.
