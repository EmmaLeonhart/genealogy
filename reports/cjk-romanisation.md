# Romanising the Han-only names

Built by `scripts/build-cjk-romanisation.py`. **Nothing is transliterated** — every reading is read off a Wikidata name item that carries both the Han form and the Latin form, so it is a published reading of that character *as a name*.

- people with a CJK name and no Latin label: **38,609**
- culture settled: **37,298**
- romanised: **13,589** — zh **13,359**, ko **0**, ja **230**

## How culture was settled, in the specified order of evidence

| evidence | people |
| --- | ---: |
| neighbours' script | 25,384 |
| a Chinese clan seat (郡望) | 8,936 |
| unclassified | 1,445 |
| a Japanese given-name ending | 1,043 |
| a simplified-only Chinese character | 304 |
| a character that exists only in Japanese | 186 |
| **total** | **37,298** |

## Japanese is separated on purpose

Chinese and Korean readings are very straightforward; Japanese readings are not. That is structural: a Chinese or Korean character has effectively one reading as a name, while a Japanese one takes different readings in different names and the item only gives the reading for *that* name. **The `ja` rows are the ones to distrust.**
