# Step 3 — the `ja` label

Built by `scripts/build-ja-label-batch.py`. **Emits nothing to Wikidata**, and emits only labels that require no invention.

- individuals: **448665**
- `ja` available honestly: **41952**
- not reached: **406713**

| where it comes from | people |
| --- | ---: |
| the name as written, which Japanese uses unchanged | 37405 |
| wikidata's own ja label | 4547 |

## What is deliberately not emitted

**Hangul-only names: 5293.** A `ja` label must not be the hangul — Japanese does not write Korean names that way. They need a katakana reading, which is the same unsolved problem as the Latin names.

**English → katakana: the rest.** Emma's method for this direction is a hand-built table (*"hand-built tables, except CJK → English"*). A table that turns `Brodsky` into `ブロツキー` correctly has real failure modes — syllabification, long vowels, and the fact that established Japanese spellings of European names are conventional rather than derivable. Guessing at that many names would be the largest act of invention in this repo, so it is sized here and left for a deliberate build.
