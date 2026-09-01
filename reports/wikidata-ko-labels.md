# Step 5 — the `ko` label

Built by `scripts/build-ko-label-batch.py`. **Emits nothing to Wikidata.**

Emma, 2026-09-01: *"korean is extremely important on par with Chinese and you really should prioritize getting korean labels all the time and this seems to not get that cjk includes korean"*.

- **33,725 `ko` labels**, from sources that need no invention.

| source | people |
| --- | ---: |
| hanja reading | 28,397 |
| the name is already written in Hangul | 5,328 |

## Out of reach, and why

| reason | people |
| --- | ---: |
| Latin name -- transcription, excluded as ja excludes it | 1,278,536 |
| no name to work from | 126,976 |
| a Han name with a character the table cannot read | 12,324 |
| CJK name in mixed script | 392 |
| written in kana -- a Japanese reading, not a Korean one | 11 |

**Latin names are excluded on purpose**, exactly as `build-ja-label-batch.py` excludes them. `translit_ko_latin` renders 97% of them, but that is transcription rather than reading, and emitting it here while `ja` withholds the same thing would be the two batches disagreeing about what counts as honest.
