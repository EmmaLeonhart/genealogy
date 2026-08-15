# Questions for Emma — asked at 09:00, not before

**Emma, 2026-08-16, going to sleep:** *"please try to abstain from actually asking
me questions… having a questions queue thing that's separate from the regular
queue that is all asked at like 9 a.m. And for all questions and all stuff that
needs to be done, you are going to barrel through it overnight without needing to
ask the questions."*

**So: do not stop overnight.** A question is not a reason to halt. Write it here,
pick the option that loses the least if it is wrong, keep going, and say in the
entry what was done in the meantime so she can reverse it cheaply.

**The bar for asking at all.** If a wrong guess is cheap to undo — a report, a
generated file, a queue ordering — decide it and record it. Only put something
here when getting it wrong would be expensive: an irreversible edit, a deletion,
a Wikidata write, or work that would have to be thrown away wholesale.

**Nothing runs against Wikidata before 1 September regardless**, so no entry here
can be urgent in that direction.

Asked by cron `9:04`. When one is answered, apply it, delete the entry, and
record the decision in `CLAUDE.md` if it governs how the project works.

---

## 1 · The 1,171 ambiguous name items

`reports/name-item-plan.csv`. A name whose label matches **several** Wikidata
items — `Maria` matches nine, `Anna` five, `John` and `Anne` two each. 928 given
names and 243 family names.

**Done in the meantime: nothing.** They are held, marked
`AMBIGUOUS - review, do not create`, and are **not** in
`reports/wikidata-name-items.json`. Reversing costs nothing; the alternative was
creating a tenth `Maria`, which does not reverse cheaply.

**The options:**

- **Link the most-referenced item.** `reports/name-items.csv` has a `references`
  count per item, so "the one most of Wikidata already uses" is available and is
  probably right for common given names.
- **Hold all 1,171** until the rest of the name items are done.
- **Show you the top 20 by bearer count** and decide those by hand; they cover
  most of the affected people.
