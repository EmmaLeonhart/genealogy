# `ja`, `zh` and `ko` transcribed, for people who already have a QID

Built by `scripts/build-cjk-transcription-labels.py`. **Emits nothing to Wikidata.**

Emma, 2026-09-01, asked whether a rule-based transcription of a Latin name counts as a publishable label: **emit it for the people who already have a QID.**

- **101,760 labels** over 33,920 people.

| language | labels |
| --- | ---: |
| `ja` | 33,920 |
| `zh` | 33,920 |
| `ko` | 33,920 |

## Not emitted, and why

| reason | people |
| --- | ---: |
| no Wikidata item -- their labels ride along with the creation | 1,408,284 |
| already has a name in a CJK script -- not a transcription case | 5,908 |
| a token nothing can render, so the whole label is withheld | 3,545 |
| no Latin label to transcribe | 307 |

**`zh` is here although she said `ja` and `ko`.** `translit_no.translit` returns katakana and Chinese from one call, so they are the same engine and the same table column; emitting one and withholding the other would recreate the inconsistency her ruling removed.

**The corpus-wide batches still withhold transcription**, and that is deliberate: `build-ja-label-batch.py` and `build-ko-label-batch.py` run over 1.29 million people who are mostly not on Wikidata, where the labels ride along with the creation instead.
