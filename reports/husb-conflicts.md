# The three `FAM.HUSB` conflicts — decided on evidence

Queue item 0.00Z. Two exports named different husbands for one family, and
later-wins picked the survivor by **path order, not export date**, so filename
sorting decided which man is in the tree. That is inside the stated merge rule
and is still the wrong instrument for the question, so the question is answered
here from the records instead.

Read against the 151-export merge, offline. Three conflict rows over **two**
families: `@F6000000179131721834@` appears twice in `out/merge-report.md` with
the winners reversed, because two exports each beat the other in a different
pass.

**Both are two records of one man.** Neither is a genealogical disagreement.

## 1. `@F6000000179131721834@` — Emperor Ōjin, twice

| | `@I6000000179131744821@` | `@I6000000001829492981@` |
| --- | --- | --- |
| name | `Ōjin /Tenno/` | `誉田別命 /応神天皇/`, also `Ojin-tenno (Homutawake)` |
| birth | 201 | 5 JAN 201 |
| death | — | 11 MAR 310 |
| occupation | — | 15th Emperor of Japan, 第15代天皇 |
| parents (`FAMC`) | **`@F6000000001829393843@`** | **`@F6000000001829393843@`** |
| spouse families | 1 | 6 |

応神天皇 *is* Ōjin-tennō, and 誉田別命 (Homutawake) is his personal name — the
second record spells out what the first abbreviates. They share a birth year,
and **they share the same `FAMC`**: both profiles are children of the same
family record. Two men who happen to share a name do not share a parent record.

Emma already predicted this one. `queue.md` 0.2, in her words: *"there were some
profile merges and edits related to Japanese emperors, particularly Emperor
Ojin … there were duplicates of Emperor Ojin and some other people."* This is
that duplicate, surfacing structurally.

**The merge currently keeps the wrong one.** `@F6000000179131744821@` won on
filename order, and it is the thin record — a birth year and nothing else. The
record it displaced carries the death date, the occupation, five further spouse
families and the images. Nothing was lost from the file, but the family points
at the sparser of the two.

## 2. `@F6000000195596077832@` — Wikramawardhana, twice

| | `@I6000000198604813825@` | `@I6000000195595965846@` |
| --- | --- | --- |
| name | `Hyang Wisesa Aji Wikramawardhana Bhre Mataram Raja Majapahit ke-7` | `Wikramawardhana / Raden Gagaksali (Bhre Hyang Wisesa Aji Wikrama)` |
| parents (`FAMC`) | **`@F6000000195596206839@`** | **`@F6000000195596206839@`** |
| spouse families | 4 | 1 |

Both are Wikramawardhana, seventh ruler of Majapahit; both carry *Bhre Hyang
Wisesa Aji Wikrama* inside the name string. Again **the same `FAMC`**. Here the
richer record won, but by the same accident of path order rather than by any
rule — the two conflicts resolved opposite ways for no reason connected to the
evidence.

## Why this matters beyond three rows

**`FAM.HUSB` conflict is a duplicate detector that Wikidata cannot provide.**
`reports/wikidata-doubles.md` finds Geni duplicates by looking for one Wikidata
item claiming two Geni IDs. **None of these four profiles appears in it** —
Wikidata does not link them, so that method is blind to them. Our own merge
found them structurally, from two exports disagreeing about one family.

That makes the conflict list worth mining rather than merely resolving: it is
the only signal here that finds duplicates Wikidata has never noticed.

Both pairs are also the first real test case for entity resolution — the
"person has two fathers" shape `queue.md` names — and in both, the discriminator
that settles it is the **shared `FAMC`**, not the names. Names are where the two
records differ most; parentage is where they agree exactly.

## What is not decided here

**Whether `merge_files` should sort sources by `HEAD` date** before merging.
`CLAUDE.md` says that follows without a code change. It would make the winner
deterministic and defensible, but it would *not* have produced a better answer
here: the right resolution is not "the newer export wins", it is "these are one
person, merge them on Geni". Date-sorting would still have picked one of two
duplicates. **NEEDS-DECISION — Emma.**

**The Geni-side merges themselves.** Merging two profiles is an edit on Geni and
only Emma can make it. **BLOCKED-ON-USER-ACTION**, and it belongs with the
postponed Geni-side merge queue rather than being done piecemeal.

One artefact noticed in passing and not chased: `@F6000000179131721834@` carries
the same `CHIL` pointer twice.
