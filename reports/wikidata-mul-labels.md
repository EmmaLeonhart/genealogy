# Step 2 — `mul` for every individual, derived from `en`

Built by `scripts/build-mul-label-batch.py`. **Emits nothing to Wikidata.**

`mul` is made for every individual, almost always derived from `en`.

- step 1 `en` edits: **147312**
- `mul` mirrored from them: **8047**
- deliberately not mirrored: **139265**

## Why 139265 are left alone

*"Almost always"* is doing the work in that rule. A relationship label — `husband of Lakech Gashawbeza` — is **not a name**; copying it into `mul` would assert across every language that this is what the person is called. This shape was ruled on 2026-08-17 — `NN` for `mul` there — and those people already get `mul: NN` from `build-placeholder-label-batch.py`. Overwriting a correct marker with a description would be a regression.

| mirrored from | people |
| --- | ---: |
| en, which came from romanised from zh | 7621 |
| en, which came from wikidata's own English label | 230 |
| en, which came from romanised from ja | 196 |
