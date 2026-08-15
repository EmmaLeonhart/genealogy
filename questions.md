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

## 1 · The 1,312 ambiguous name items

`reports/name-item-plan.csv`. A name whose label matches **several** Wikidata
items — `Maria` matches nine, `Anna` five, `John` and `Anne` two each. 1,034 given
names and 278 family names.

**Done in the meantime: nothing.** They are held, marked
`AMBIGUOUS - review, do not create`, and are **not** in
`reports/wikidata-name-items.json`. Reversing costs nothing; the alternative was
creating a tenth `Maria`, which does not reverse cheaply.

**The options:**

- **Link the most-referenced item.** `reports/name-items.csv` has a `references`
  count per item, so "the one most of Wikidata already uses" is available and is
  probably right for common given names.
- **Hold all 1,312** until the rest of the name items are done.
- **Show you the top 20 by bearer count** and decide those by hand; they cover
  most of the affected people.


## 2 · The Itamar spine says 112 in its header and 121 in its content

`gedcom/samaritan-itamar-spine.ged`. The `HEAD` note says *"Itamar is 2 and Tabia
is 112"*; Tabia's own note says **Generation 121**; the file holds **120 people
numbered 2 through 121**. Nine more than its header, and nine more than the
**112** generations the source gives father-to-son for the parallel Phinhas line.

**Done in the meantime: nothing.** The file is hand-made and hand-sourced, and
`@I3@` already carries the right caveat — *"Nobody counted this line. Do not read
the number as measured."* Changing it on inference is the thing item 9b just
established should not happen.

**The options:**

- **Renumber to end at 112**, dropping nine invented placeholders, so the file
  agrees with its own header and with the source's figure.
- **Collapse the whole unnamed stretch** to one *"distance not recorded"* link
  between Itamar and Tabia — your original suggestion, and the only version that
  asserts nothing the source does not.
- **Leave the chain, fix the header** to say 121 — keeps the Geni-entry ordering
  intact and admits the number is borrowed rather than counted.

The third is cheapest and the second is most honest; they differ in whether you
want 118 placeholder people to enter Geni.
