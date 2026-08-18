# Living relatives on Google Scholar and ORCID — first pass

**Emma's item, 2026-08-18.** Candidates she supplied: two Google Scholar profiles and
twelve ORCID records on the father's side (`Borsheim` / `Børsheim`, the more unique
surname), ten Scholar profiles on the mother's side, and three arXiv papers.

**This pass answers one question and no more: are any of the twelve ORCID people already
in the corpus?** Offline, from `reports/display-names.csv` and `reports/derived-facts.csv`.
Nothing was fetched, nothing was written to Wikidata, no export was run.

## The answer is no, and the near-miss is worth stating

The corpus holds **215 records** carrying `Borsheim`/`Børsheim` in a name field, 190 of
them distinct people, **143 with a birth year, running 1566 to 1998**. So this is not a
family that stops before living memory — **38 of them were born in 1940 or later**, and
the youngest in 1998. If these academics were in the tree, this is where they would be.

**None of the twelve ORCID names is among those 38.** Not Brianna, Christoffer, Sjur,
Elisabet, Anna, Preston, Kirsten, Ragnar Loken, Ingebjørg Træland, Carlin, or either
Knut Yngve.

### The false positive this replaced, because it is the trap

A first pass matched ORCID *given names* against the 215 and reported **5 of 12 as hits** —
Sjur, Anna, Kirsten, and Knut Yngve twice. Every one of those matched a person born in the
seventeenth to nineteenth century: `Sjur Ivarson`, `Sjur Hansson`, `Anna Ivarsdtr.`,
`Kirsten Taletta Olsdatter`, `Knut Sjurson`.

Norwegian farm families recycle given names down the generations by rule — a son is named
for a grandfather — so a given-name match inside one such family is close to **no evidence
at all**. Restricting to people who could plausibly *be* the living person takes it from
five hits to zero. **A name match is not a person match.**

## What the corpus family actually is, which narrows the question

| | |
| --- | --- |
| birth places | `Borsheim` (18), `Borsok` (12), `Klepp` (3), `Årsvoll`, `Raustad`, `Nærbø` |
| region | **Rogaland / Jæren** — Klepp and Nærbø are Jæren municipalities, south of Stavanger |
| emigrant branch | Canada — `Birch Hills, Saskatchewan`, `Vancouver`, two more just `Canada` |

Against the candidates' affiliations:

| candidate | affiliation | region |
| --- | --- | --- |
| Sjur Børsheim | Haukeland University Hospital | **Bergen — Hordaland** |
| Christoffer Børsheim | University of Bergen; Bournemouth | **Bergen — Hordaland** |
| Ragnar Loken Borsheim | University of Bergen | **Bergen — Hordaland** |
| Elisabet Børsheim | Arkansas Children's; UAMS | **USA** |
| Brianna Borsheim | Wake Forest; Lurie Children's | **USA** |
| Carlin Borsheim-Black | — | **USA** (Michigan, by publication record) |

**Two mismatches, not one.** The Norwegian candidates are Hordaland and the corpus family
is Rogaland; the American candidates are the United States and the corpus emigrant branch
went to **Canada**. Neither is fatal — people move, and Bergen is where western Norwegians
go to work — but neither supports the connection either.

**`Børsheim` is a farm name.** It is a toponym, and there is more than one farm: Børsheim
in Hordaland and Børsheim in Rogaland are different places, and families took the name of
the farm they lived on. Two unrelated families can carry it honestly. That is why the
surname on its own is the weakest evidence available here, and why the regional split
above matters more than the spelling.

## One thing that is decidable and is not genealogy

**`0000-0003-2180-1811` and `0009-0009-7736-1326` are both `Knut Yngve Børsheim`.** One
person with a duplicate ORCID record, or two people sharing a name. ORCID's own record
shows the affiliations, and the newer `0009-` prefix is a later registration — the usual
shape of somebody registering twice. Worth resolving before either is treated as a
candidate, because a duplicate counted twice inflates whatever comes next.

## What would actually decide this, in order of cost

1. **The Scholar profiles' own co-author and affiliation history** — a Bergen academic
   with a Jæren birthplace is a real signal; a Bergen academic with a Bergen family is
   not. Not yet fetched.
2. **The three arXiv papers**, which may name institutions and given names not in the
   ORCID rows.
3. **The mother's side, deliberately not started.** Emma's own framing is that the surname
   is generic, which means the method above — surname census, then birth cohort — will
   return noise rather than a shortlist. It needs the given names and the affiliations to
   do the work, not the surname. Ten Scholar profiles are recorded in `queue.md`.

## What this does not settle, and is not mine to settle

**Whether any of these people is a relative at all**, and **whether living people belong
in the tree**, are Emma's rulings. This report establishes only that none of the twelve is
in the corpus today, and that the regional evidence points away from rather than toward
the connection. A negative result on a first pass is not a refutation — the corpus is one
family's exports, not a census of the surname.
