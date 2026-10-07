# What this project is for

_Maintained by Claude: a running read of what the user is trying to do. It is
analysis, not a transcript, and it changes as understanding improves._

Work mode started: 2026-10-05 02:29 PST (from `date`), after the user had been
quiet for an hour.

## Current understanding

A tool that exports GEDCOM family-tree files from Wikidata. In the user's words
(2026-10-03): "I want to be making a thing that exports gedcoms from wikidata.
First thing is first it exports full ancestor things of individuals using
wikidata father mother things and opens them."

The first target is Q140568870, exported in English, Chinese, Japanese and
Korean. `wikidata_to_gedcom.py` does this. It walks P22 (father) and P25
(mother) breadth-first, writes one `.ged` per language and opens each file
with the default program. The user has been editing Wikidata labels between
runs and re-exporting to see the results (`-2`, `-3`, ...), at 10, 15, 30 and
50 generations.

## What supports it

- The chat (sessions/2026-10-03_e624f7de.md, sessions/2026-10-05_42236218.md).
- The folder name, chosen by the user: `wikidata_to_gedcom`.
- `data_lake/` holds only a GEDCOM viewer log, so there is no spec material.

## Constraints the user gave in chat

- Names: "the display label is first name and no last name (I know does not
  scale well)". Label in the requested language, else "mul label is the label
  there if there is no label in the requested language".
- "the notes thing contains a link to the qid".
- "as soon as you get it you export" and "just force open every one of them
  with defalt program". Exports are opened automatically.
- Re-runs get a numbered suffix ("with -2 appended on all of them"). Earlier
  exports are never overwritten.
- Generation depth is whatever the user asks for: 10, then 15 (now the
  default), then 30 (ja, ko), then 50 (ko).
- She said "hurry". Speed of turnaround matters more than polish.

## Open questions

- What is the "second thing"? She said "I have two simple things I want to do"
  and only described the first.
- Should the exporter grow beyond ancestors (descendants, spouses, dates,
  places)? Not asked for yet. Assumption: keep the current behavior exactly as
  it is and make only additive improvements that change no default output.

## Project tooling

- Update check 2026-10-05: the vendored skills match cleanvibe v2.0.3, so no
  skill text changed. v2.0.4 adds a hook, `.claude/hooks/intent_staleness.py`,
  plus a `UserPromptSubmit` entry in settings, to be copied "from a fresh
  project". BLOCKED-ON-USER-ACTION: no fresh v2.0.4 project exists in this
  folder, and copying the hook in means reading outside the project. Unblock:
  the user creates a fresh cleanvibe project or says to copy it from the
  installed cleanvibe package.

## Confidence

High on the goal (an ancestor exporter from Wikidata to GEDCOM). The next
feature is unknown.
