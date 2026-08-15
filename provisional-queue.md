# Provisional queue

**Emma, 2026-08-15:** *"we're basically in a situation where we kind of need to
build a provisional queue thing that we operate off of, that we put new stuff in,
and that we're queuing because the old queue is kind of messed up… once we're
clear of all of this, the provisional queue is just going to basically get back
into the regular queue."*

So: **new work goes here, not in `queue.md`.** `queue.md` is being audited and is
not trustworthy enough to operate from yet — its item 0 is the audit procedure
and `reports/audit-transcripts-2026-08-15.md` is the first run of it. When the
audit is settled, this file folds back into `queue.md` and stops existing.

**"Queued" here never means "written in a file and hoped for".** Anything with a
time attached is a real `CronCreate` job, listed with its id below. The file
records *what* and *why*; the cron is *what actually fires*.

## Scheduled — live cron jobs, this session

Session-only: they die when the Claude session ends and are recreated at the
start of the next one.

| id | fires | what |
| --- | --- | --- |
| `d425c1f5` | :03 hourly | work-loop |
| `be98e574` | :15 hourly | auto-flush — commit and push anything pending |
| `f8b152ab` | :42 hourly | status-report — reporting only |
| `f3d681e4` | **19:07** | **re-merge** the 203-export corpus, refresh the derived reports |
| `43140a93` | **21:02** | **bloat review** — candidates only, nothing deleted without asking |
| `d62449e3` | **22:01** | ask about `reports/seeds.md`'s future |
| `9f41a7a4` | **23:03** | entity-resolution: is it still a real task, and what format now |
| `05926d1d` | **00:01** | **the structural Geni↔Wikidata merge** |

The ordering is deliberate. The midnight merge needs *"the proper synoptic tree
and the proper samaritans"*, so the re-merge runs at 19:07, five hours ahead of
it, rather than after midnight.

## 1 · The name analysis — DONE 2026-08-15, decision below

`reports/name-classes.md` and `reports/name-classes.csv`, 140,764 distinct
tokens. What it settled, so it does not get re-litigated:

- **Classify by dominance ratio WITH a bearer floor**, not by presence in both
  slots. Only 12% of the 7,838 both-slot tokens put 95% of bearers in one slot;
  above 50 bearers it is 45%. Below the floor a 1-vs-1 split is arithmetic, not
  evidence.
- **Particles and regnal numerals never become name items** — 41 particles
  (`de`, `von`, `van`, `y`, `la`, `of`) across 86,772 bearers, plus `I`/`II`/`III`
  in the given slot.
- **The patronymic is inside the `GIVN` string**, which is why it needs its own
  role rather than being read as a middle name. `P3831` → `Q110874`, now in
  `CLAUDE.md`'s table alongside `Q245025` for middle names. All three resolved
  **offline** against `reports/wikidata-labels.tsv`.

**Still open:** the bearer floor is set at 50 in the report's analysis because
that is where the ratio flips, not because it was chosen. Worth Emma's eye before
anything is generated from it.

## 2 · Relationship labels — SETTLED 2026-08-15, ready to generate

`reports/relationship-label-preview.md` showed both populations and Emma decided
on the rows. **26,281 people carry a placeholder given name.**

**Who gets a generated label: everyone with a placeholder given name.** No
filter on whether they have a surname, and **no filter on whether the surname is
repeated inside the generated label** — the 331 cases where `NN Kalf` becomes
`son of Anders Kalf` are generated, because the label still carries a given name
the `mul` label does not. Her two earlier answers pointed opposite ways on this;
shown the actual rows, she chose to generate.

**The surname is preserved, and the 36% is the reason.** A relative has a real
name for **69%** of bare-`NN` people but only **36%** of `NN <surname>` people.
Emma read that correctly and I had it backwards: *"the surname ones being badly
connected is kind of evidence in favour of the fact that we need to keep the
surname."* For that population the relationship label usually **cannot** be
built, so the surname is the only informative thing they have. `mul` stays `NN`
or `NN <surname>`.

**Precedence, one hop:** parent (father, then mother), spouse, child →
`daughter of Joe`, `wife of Carl`, `mother of Joseph`.

**Two rules from the preview, both hers:**

- **A redacted or placeholder relative is skipped** and the precedence falls
  through to the next one, trying every spouse and child rather than only the
  first. This removed all 2,730 labels reading *"husband of `<private>` Gaya
  Pereira"*. Only 1,052 of the 7,654 affected people (13%) recover a label from a
  later relative — for the rest the skip costs the label outright.
- **A surname that is itself placeholder vocabulary collapses to bare `NN`** —
  `NN ???`, `NN NN`, `NN N.N.`, `NN Unknown`. 351 people.

**Unknown sex takes the neutral form** (`child of`, `spouse of`), 127 cases. No
gender is inferred to make a label read better.

**Yield:** 14,351 of the 26,281 get a one-hop label — 13,140 bare `NN` and 1,211
with a surname.

## 3 · Label languages: English, Japanese, Chinese, and `mul`

Emma, 2026-08-15, resolving the 08-12 / 08-14 conflict in favour of the longer
list: **English + Japanese + Chinese + `mul`**, with Korean in the covered set
too. Her reasoning, which is the part worth keeping:

- *"Japanese is the lostiest language"* — it is not in Wikidata's top 18 by
  coverage, so `ja` nearly always has to be constructed rather than copied.
- *"Chinese needs to be generated to differentiate stuff with Japanese and
  Korean."* A Han-only string does not say which language it is; having zh
  explicitly is what separates the three.
- English is standard.

*"We might extend this to other languages, but this is something I consider to be
up for debate right now."* So the set is not final — do not build it as if it
were closed.

## 4 · The old Geni export on Google Drive

`1nwHvAJTv_rrq_rBWhFrJXjy62ok-Ly-E` — **`export-geni.zip`, 895,065 bytes, created
2026-08-13 06:56**, owned by Emma. The Drive MCP server **can** see it; the
metadata above came from it.

What stopped it: moving 895 KB of binary through the model's context as base64
costs roughly 300k tokens in and 300k back out to write it to disk, for a file
Emma can download in one click. So it sits here rather than being forced.

**Unblock:** download it to `~/Downloads` and it gets filed and merged like any
other export. Per `CLAUDE.md`, where it goes under `exports/` is **her call** —
and if the destination path already exists, stop rather than overwrite.

## 5 · Multi-hop relationship labels — parked at the tail

Emma, 2026-08-15: *"Put this at the end of the provisional queue… we'll work on
this later."* Her sketch of the ordering, extending the one-hop precedence rather
than replacing it:

**child-of → spouse-of → parent-of → grandchild-of → sibling / nephew / uncle.**

**Measured, so the size is known before it is built:** of the **11,930** people
with no one-hop label, **3,604 (30%) have a named relative two hops out** — 2,020
via a grandfather, 1,449 a grandmother, 135 a grandchild. So it is present in the
data and worth about a third of what one hop leaves behind.

Sibling, uncle and nephew need the family graph rather than the derived CSVs, so
that part waits on the re-merge.
