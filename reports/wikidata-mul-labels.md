# Step 2 — `mul` for every individual, derived from `en`

Built by `scripts/build-mul-label-batch.py`. **Emits nothing to Wikidata.**

Emma, 2026-08-17: *"then mul gets made for every individual (almost always derived from en)"*.

- step 1 `en` edits: **22373**
- `mul` mirrored from them: **14972**
- deliberately not mirrored: **7401**

## Why 7401 are left alone

*"Almost always"* is doing the work in her sentence. A relationship label — `husband of Lakech Gashawbeza` — is **not a name**; copying it into `mul` would assert across every language that this is what the person is called. She ruled on this shape on 2026-08-17: *"And NN for mul there"*, and those people already get `mul: NN` from `build-placeholder-label-batch.py`. Overwriting a correct marker with a description would be a regression.

| mirrored from | people |
| --- | ---: |
| en, which came from romanised from zh | 9539 |
| en, which came from wikidata's own English label | 5208 |
| en, which came from romanised from ja | 225 |
