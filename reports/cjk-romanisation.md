# Romanising the Han-only names

Built by `scripts/build-cjk-romanisation.py`. **Nothing is transliterated** — every reading is read off a Wikidata name item that carries both the Han form and the Latin form, so it is a published reading of that character *as a name*.

- people with a CJK name and no Latin label: **45,580**
- culture settled: **43,976**
- romanised: **18,151** — zh **17,919**, ko **0**, ja **232**

## How culture was settled, in the specified order of evidence

| evidence | people |
| --- | ---: |
| neighbours' script | 30,021 |
| a Chinese clan seat (郡望) | 10,667 |
| unclassified | 1,719 |
| a Japanese given-name ending | 1,051 |
| a simplified-only Chinese character | 332 |
| a character that exists only in Japanese | 186 |
| **total** | **43,976** |

## Japanese is separated on purpose

Chinese and Korean readings are very straightforward; Japanese readings are not. That is structural: a Chinese or Korean character has effectively one reading as a name, while a Japanese one takes different readings in different names and the item only gives the reading for *that* name. **The `ja` rows are the ones to distrust.**
