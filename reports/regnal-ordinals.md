# Names in the corpus that carry an ordinal

**19,450 people** of 883,478, one row each in `regnal-ordinals.csv`. The ordinal is searched for in the given-name portion only — everything before the first GEDCOM slash — and never in the first token, because a name that opens with a numeral is a record that begins oddly rather than somebody's regnal number.

**Emma, 2026-08-18, on what this population actually is:** *"regular ordinals simply are not a thing. There won't be regular ordinals here because somebody would need to be like a monarch or something."* So the roman class is the real one and the other two want reading with care.

| kind | people | |
| --- | ---: | --- |
| roman | 8,341 | `II`, `III`, `IV` — unambiguous at two characters or more |
| single-letter | 6,031 | a lone `I V X L C D M`: a numeral **and** the commonest Anglophone middle initial, so never folded in with the roman count |
| arabic | 5,078 | `12`, `14th` |

171 of them also carry a patronymic chain.

**Two false-positive classes were found by reading the rows**, and both are excluded in code rather than filtered here: `DI` (3,076) is the Italian preposition, not 501, so a token must equal its own upper-casing; and `LI` (99) is the surname, pulled in because `given_part` strips slashes, so the search runs on the pre-slash portion only.

## Most common roman tokens

| token | people |
| --- | ---: |
| II | 3,971 |
| III | 2,007 |
| IV | 1,181 |
| VI | 346 |
| VII | 269 |
| VIII | 165 |
| IX | 116 |
| XI | 63 |
| XII | 48 |
| XV | 28 |
| XIII | 28 |
| XIV | 23 |
| XVII | 13 |
| XVI | 10 |
| DI | 8 |
| XX | 8 |
| XIX | 7 |
| XVIII | 7 |
| XXV | 5 |
| XXI | 5 |
