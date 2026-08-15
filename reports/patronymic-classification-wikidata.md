# Patronymics on the Wikidata side

**Queue item 11.** Emma, 2026-08-15: *"we also should be running this
processing on both the geni stuff and the wiki data stuff."*

Same method as `reports/patronymic-classification.md` — the **father's**
given name decides, never the token's shape — reusing that script's form
tables and father test by import, so the two cannot drift apart.

**1,417,101 humans in the store, 888,685 stating a `P22`
father, 2,523,585 name tokens classified.**

| verdict | tokens | share |
| --- | ---: | ---: |
| not patronymic | 1,582,814 | 62.7% |
| no father recorded | 723,289 | 28.7% |
| AMBIGUOUS: form, father differs | 106,054 | 4.2% |
| patronymic (inferred, no father recorded) | 50,870 | 2.0% |
| father has no label | 47,062 | 1.9% |
| surname: patronymic form conflicts with recorded sex | 5,686 | 0.2% |
| patronymic | 4,816 | 0.2% |
| AMBIGUOUS: form, father unnamed | 2,994 | 0.1% |

## The limitation, stated rather than worked around

**Wikidata gives no `GIVN`/`SURN` split here, so the tokens are the
label's words.** `P735`/`P734` name *items* rather than strings, and
resolving those to strings needs the name-item download that is still
running. A label is a rendering of a name, not its parts, so a token's
position in it is weaker evidence than a GEDCOM field.

**A father with no label yields no verdict**, exactly as an unnamed father
does on the Geni side. Absence of evidence is not a `no`.
