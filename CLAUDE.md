# geni

## Skills

Workflow behaviors live as skills in `.claude/skills/` (auto-discovered by Claude Code):
`emergency-stop`, `cron-is-local`, `autonomous-loop`, `queue-driven-workflow`,
`writing-style`, `cleanvibe-update-check`. They are vendored into this repo and kept
current by the `cleanvibe-update-check` skill.

- **Last cleanvibe update check:** `never`
- **Updates source:** <https://cleanvibe.emmaleonhart.com/updates.md>

## Project Description

Merge Geni.com GEDCOM exports into one canonical genealogy, then reconcile that
genealogy against Wikidata — and eventually generate the edits that would create
the missing people on Wikidata.

The user's stated direction, in their own framing:

1. Merge the exports into a single tree.
2. Work out the Wikidata connections as far as the data allows, using the Geni
   ID that every record preserves.
3. Later, expand the tree with more exports (from Geni, and from Jenny) — which
   means finding good **branch points** in the genealogy to export from next.
4. Much later, queue up creation of the absent people *on* Wikidata, connected
   to their parents, carrying whatever the genealogy supports: multilingual
   label, English label, Geni ID, sex, and the relationship links. Harder
   pieces they named explicitly: the name/surname *properties*, creating
   Wikidata items for surnames that have none so people can be linked to them,
   and queued edits adding name links to people who already have items.

## Architecture and Conventions

**The Geni profile ID is the primary key for everything.** Geni's export writes
it as the GEDCOM xref (`0 @I6000000087535357291@ INDI`) and repeats it as
`1 RFN geni:6000000087535357291`. Merging is therefore an exact join, never
fuzzy name matching. `genimerge.identity` is the single place that knows this;
`tests/test_gedcom_real_exports.py` asserts it against the real files so a
change in Geni's format fails loudly.

Exactly **four xref prefixes** occur, each bound to one record type: `I` on
`INDI`, `F` on `FAM`, `N` on `NOTE`, `S` on `SUBM` — measured over all 19,274
xrefs. `GENI_ID_RE` accepts only those on purpose: when it accepted any letters,
the foreign xref `@NI04461@` parsed as Geni ID `04461` and would have produced a
URL to a stranger's profile.

**The xref is the merge key; `RFN` is corroboration checked elsewhere.**
`Merger.add_source` deliberately does not call `geni_id_of`, so a contradictory
`RFN` does not stop a merge. The cross-check runs in `inventory`, in `model`,
and over the merged output in `tests/test_merge_real_exports.py`.

**Exports are capped at 3836 individuals.** All three exports hit that number
exactly while sharing only 354 people, so they are overlapping slices, not
copies. Expect to merge many exports over time, and expect the merge to be
re-run rather than hand-edited. See `reports/inventory.md`.

**Stdlib only.** `urllib` covers the Wikidata SPARQL endpoint. Add a dependency
only when the stdlib genuinely cannot do the job.

**Layout.** `data_lake/` raw inputs (`*.zip` gitignored, `*.ged` tracked) ·
`src/genimerge/` the package · `reports/` generated reports worth keeping in git
· `out/` generated data, gitignored · `tests/` pytest.

### Wikidata properties and items

All confirmed against live Wikidata via `wbgetentities` on 2026-07-30. **Do not
guess these** — several plausible-looking IDs are something else entirely
(P1288, for instance, is a German literature encyclopedia, not a genealogy
identifier).

**Identity and structure**

| ID | label | datatype |
| --- | --- | --- |
| P2600 | Geni.com profile ID | external-id |
| P31 | instance of | item — value `Q5` human |
| P21 | sex or gender | item — `Q6581097` male, `Q6581072` female |
| P22 / P25 | father / mother | item |
| P26 | spouse | item |
| P40 | child | item |
| P3373 | sibling | item |

**Life events**

| ID | label | datatype |
| --- | --- | --- |
| P569 / P570 | date of birth / date of death | time |
| P19 / P20 | place of birth / place of death | item |
| P119 | place of burial | item |
| P2842 | place of marriage | item (qualifier on P26) |
| P106 | occupation | item |
| P97 | noble title | item |
| P535 | Find a Grave memorial ID | external-id |

**Names** — the part of `todo.md` that needs new items created

| ID | label | datatype |
| --- | --- | --- |
| P735 | given name | item — name items are `Q202444` given name, or `Q12308941` male / `Q11879590` female / `Q3409032` unisex given name |
| P734 | family name | item — name items are `Q101352` family name |
| P1950 | second family name in Spanish name | item (not applicable here) |
| P1477 | birth name | monolingual text |
| P1559 | name in native language | monolingual text |

**Date qualifiers** — the GEDCOM modifiers map onto these

| GEDCOM | Wikidata |
| --- | --- |
| `ABT` / `EST` / `CAL` | P1480 sourcing circumstances = `Q5727902` circa |
| `BEF` | P1326 latest date |
| `AFT` | P1319 earliest date |
| `BET x AND y` | P1319 earliest date + P1326 latest date |

**References** — P248 stated in, P854 reference URL, P813 retrieved,
P143 imported from Wikimedia project.

### Cost: this repo is private, so CI is manual-only

**Never add a `push:` or `pull_request:` trigger to `.github/workflows/`.**
Actions minutes are free on public repos but billable on private ones once the
monthly allowance is used, and a surprise bill is not worth a green tick.
`ci.yml` is `workflow_dispatch:` only, and the workflow is disabled at the
GitHub end as well.

Verification therefore happens **locally, before pushing**: `python -m pytest`.
The suite is fast, needs only pytest, and covers the real 24 MB exports. The one
thing local runs cannot do is the Python version matrix — `tests/test_python_floor.py`
is a partial stand-in for that, and says so.

### Working on Windows here

- Commit with `git commit -F <msgfile>`, not `-m` with a here-string: PowerShell
  5.1 mangles `<` and `>` in native-command arguments even inside quotes.
- Never edit UTF-8 text files with `Get-Content -Raw` + `Set-Content` — it
  double-encodes non-ASCII. Use the editing tools, or Python with an explicit
  `encoding="utf-8"`.

## Long command series run in strict order
When the user gives a long series of commands, treat it as a long series of commands to be
executed in relatively STRICT ORDER, one after another, EVEN IF the order seems not to make
sense or seems inefficient. The sequencing is intentional — the user organizes the steps so
states change in the order they want. Do not reorder, merge, or skip steps.

## Not-done taxonomy (never "deliberately deferred")
When work is NOT done, tag it with exactly ONE of: **NEEDS-DECISION** (name the decision +
who decides), **BLOCKED-ON-USER-ACTION** (a real-world action only the user can take — name
it), **BLOCKED-ON-EXTERNAL** (CI / a remote / a third party / another session's unpushed
commit — name it + the unblock signal), **NEEDS-INVESTIGATION** (not understood yet — a
to-do for the next tick, never a resting place), **UNSAFE-TO-GUESS** (could cause damage —
name the risk + what makes it safe), or **OUT-OF-SCOPE** (another repo's job — name it).
LOAD-BEARING DEFAULT: if it fits none of these with a specifically-named blocker, it is NOT
deferred — DO IT NOW. Bare "deliberately not done" / "blocked on <person>" is banned.

# currentDate
Today's date is 2026-07-30.
