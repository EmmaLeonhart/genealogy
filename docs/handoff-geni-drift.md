# Handoff: items whose Geni profile turned into another person

Written 2026-10-05 by session genealogy-fa, for whichever session takes the queue item
"Items that turned into another person with their Geni profile". Nothing here has been changed on
Wikidata or in the pipeline yet.

## The problem

We create a Wikidata item from a Geni profile and put the Geni id (`P2600`) on it. Later the Geni
profile is edited (merged, reused or corrected on Geni) until it describes a different person. The
pipeline keys everything on the Geni id, so it keeps appending the NEW person's names, parents and ids
to the OLD item, and the item slowly becomes two people.

Worked example: `Q141532596`, created 2026-09-22 from Geni `6000000005607694001` as Berit Rasmusdatter
Høyland. The profile now says Elen Svensdatter Fosse (devlog, 2026-10-04).

## The population

`reports/geni-identity-drift.csv` (`qid, geni_id, label_at_creation, geni_name_now, kind, cluster`),
155 rows, built 2026-10-04:

| kind | rows | is it a problem |
| --- | --- | --- |
| spelling only | 51 | no, same person |
| name expanded, shortened or reordered | 16 | no, same person |
| label was a description or marker | 25 | no, same person |
| our creation merged into an established item (2026-10-03) | 5 | no |
| different given name, shared surname or patronymic | 19 | probably yes |
| different person | 39 | yes |

The real problem is those 58 rows. Many of the 39 sit in a few families (Bjørgås, Bjørgo, Mestad,
Güntersberg, Pfinzing), which looks like those families being reworked on Geni.

## What is waiting

Emma has to decide what an item should do once its Geni profile changes person. On 2026-10-05 she was
asked, and moved the item to the end of the queue without choosing. The options she was offered:

1. **Keep the original person.** The item stays who it was created as. The pipeline stops reading that
   Geni id for it, the names, parents and ids appended from the new person come off, and the new person
   gets their own item. The Geni id stays on the old item.
2. **The same, but move the Geni id** to the new person's item, since Geni now says the id is them.
3. **Only stop the appending** for the 58, leave what is there, and decide the rest after Geni reopens.

Present it to her as a specific question with a few of the 58 cases shown first (Geni name then and
now, and what was appended). Never as a general rule, and always with the "explain more first"
option.

## Constraints that apply

- No contact with geni.com until at least 2026-10-21, so the current Geni profiles cannot be re-read.
  The CSV's `geni_name_now` comes from our exports.
- Be cautious about removing ids (CLAUDE.md, 2026-10-04). An id comes off only when the record is
  clearly another person.
- A specific issue is not a general rule (CLAUDE.md, 2026-10-02): handle the families
  (Bjørgås, Bjørgo, Mestad, Güntersberg, Pfinzing) as the cases they are.
- Before writing any fix, check live what has actually been appended to each item. Never infer it
  from the local files.
- Duplicates get the common id and the common label, not a merge attempt.
