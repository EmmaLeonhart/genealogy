# The suspect P2600 links, censused

**The question.** `reports/wikidata-crosscheck.md` § *Links worth re-checking*
named two links as suspect — Canute I Erikska `Q442876` and Bengt Folkesson
`Q1621801` — and they sat in `queue.md` as UNSAFE-TO-GUESS for weeks. Emma,
2026-08-11: **"Analyse them like the dates."**

The dates analysis worked because it censused every instance rather than reading
the two worst. So: `reports/link-findings.csv` is all **70,785** property
comparisons over the **14,157** linked people, and `reports/link-balance.csv` is
one row per person. Built by `scripts/build-link-census.py`, reusing
`crosscheck.cross_check` and `crosscheck.link_balances` rather than restating
their rules. Offline; nothing queried.

## What the comparison actually yields

| verdict | comparisons |
| --- | ---: |
| not comparable | 34,852 |
| agrees | 30,303 |
| gap (Wikidata silent) | 4,700 |
| **conflict** | **930** |

| property | agrees | gap | conflict | not comparable |
| --- | ---: | ---: | ---: | ---: |
| P22 father | 8,777 | 239 | 134 | 5,007 |
| P25 mother | 3,025 | 382 | 90 | 10,660 |
| P26 spouse | 2,791 | 801 | 68 | 10,497 |
| P569 birth | 6,387 | 1,842 | 321 | 5,607 |
| P570 death | 9,323 | 1,436 | 317 | 3,081 |

## Finding 1 — there are 66 suspect links, not 2

Applying the report's **own** criterion — at least two conflicts, and more
conflicts than agreements — to every linked person yields **66**. The section
that named two was not wrong about those two; it was not a census.

**The single worst link in the corpus was never named.**
`Q23502804` Catalina Fernández de Córdoba y Enríquez de Ribera: **0 agreements,
4 conflicts**, every comparable property disagreeing.

    P22  father         ours Q11905099    theirs Q110586519
    P25  mother         ours Q110586544   theirs Q110586521
    P569 date of birth  ours 8 DEC 1607   theirs 1589
    P570 date of death  ours 28 DEC 1607  theirs 1646

Geni has her born and dead within twenty days of December 1607. Wikidata has a
woman who lived 1589–1646. Both parents differ too. That is a coherent story —
an infant who died, linked to the item of an adult relative of the same name —
but it is a story, and this report does not assert it.

## Finding 2 — where the two flagged links actually sit

| | agrees | conflicts | margin | rank of 14,157 |
| --- | ---: | ---: | ---: | ---: |
| `Q442876` Canute I Erikska | 0 | 3 | +3 | **2** |
| `Q1621801` Bengt Folkesson | 1 | 2 | +1 | **52** |

Canute is genuinely near the top. **Bengt Folkesson is not remarkable** — 51
links are worse, and 143 people share his +1 margin. Singling him out was an
artefact of looking at a short list rather than a distribution.

Canute's own numbers have moved since the earlier report, which recorded *0
agreements, 4 conflicts*; the census finds 3 conflicts. The corpus has grown by
several exports since. Recorded because a changed number is worth noticing, not
because either figure is suspect.

## Finding 3 — suspect links disagree about *relationships*, not dates

| | father + mother | all conflicts | share |
| --- | ---: | ---: | ---: |
| among the 66 suspects | 67 | 137 | **49%** |
| across all 930 conflicts | 224 | 930 | **24%** |

Twice the rate. That is the shape you would expect if the *link* were wrong
rather than a date being sloppy: two sources can differ by four years on a
medieval birth and both be describing one person, but they cannot name different
parents and be doing so. It is a discriminator worth having, and it is measured
rather than reasoned.

## Finding 4 — the suspects are not scattered. 39% are one batch of items

Grouping the 66 by QID range:

**26 of the 66 sit in `Q1349864xx`–`Q1349865xx`** — a contiguous block, which on
Wikidata means items created together in one import. Names in it include Pedro
Matías Fernández de Córdoba y Enríquez, Catalina María Fernández de Córdoba,
Tzihuacpopoca, Axayac, Catarina Cortés Osorio — a Spanish-colonial and Nahua
cluster.

That band holds **241 of the 14,157 linked people (1.7%)** and supplies
**39% of the suspects** — a **23-fold** enrichment.

So the right unit of investigation is not a person. It is a batch: one import of
Wikidata items whose P2600 values disagree with our tree at twenty-three times
the base rate. Whoever created those items linked them to Geni profiles
systematically, and the systematic part is what to check.

## What this does not say

`crosscheck.SUSPECT_IS_NOT_WRONG` stands unchanged and is worth restating,
because a census makes it tempting to start deleting links:

> **This does not say the links are wrong.** Two readings fit every row and
> nothing here separates them: the link is mistaken, or it is correct and one
> side's data is badly wrong.

Nothing here has been edited, excluded or proposed for exclusion. **66 links out
of 14,157 is 0.47%** — the P2600 join remains overwhelmingly sound, which is why
it stays the one non-genealogical matching method in the project.

## What is now worth doing, and what needs Emma

- **NEEDS-DECISION — Emma:** whether the `Q1349864xx` batch is worth
  investigating as a batch. It is 26 suspect links and 241 linked people, and it
  is the only structure in this data rather than a list of individuals.
- The per-person section of `reports/wikidata-crosscheck.md` should stop
  presenting a hand-picked pair as *the* suspect links. It has a census now.
