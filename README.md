# geni

Merge Geni.com genealogy exports into one canonical tree, then connect that tree
to Wikidata.

> Scaffolded with [cleanvibe](https://github.com/Immanuelle/cleanvibe).

## What this is

Geni.com exports a family tree as GEDCOM, and **each export is bounded at a few
thousand people** — the five in `data_lake/` hold 3836, 3836, 3836, 3840 and
3844 individuals. They overlap far less than that suggests:

| | individuals | families |
| --- | ---: | ---: |
| largest single export | 3844 | 2474 |
| all five merged | **16266** | **8268** |
| present in every export | 0 | 0 |

So the exports are overlapping slices of one tree rather than copies of it, and
getting the whole tree means merging many slices. That is the first half of this
project. The second half is reconciling the merged tree against Wikidata, and
eventually generating the edits that would put the missing people *into*
Wikidata.

The three numbers above are close together but they are **not** a cap Geni
enforces — see `genimerge.seeds.GENI_EXPORT_CAP`, which records what is actually
known (very little) rather than the pattern they suggest.

Merging is exact, not fuzzy. Geni writes the profile ID as the GEDCOM xref
itself:

```
0 @I6000000087535357291@ INDI
1 RFN geni:6000000087535357291
```

so every record carries a stable primary key across exports, and the same ID is
the join key to Wikidata via **P2600 (Geni.com profile ID)**.

The merge of all five currently produces 16266 individuals and 8268 families
with **zero conflicts and no lost lines** — see `reports/merge.md`.

It is **two trees, not one.** The 2026-08-02 export shares not a single person
or family with the other four: it is the Japanese mythological line, 3844 people
rooted at Kunino-tokotachi-no-mikoto, and nothing relates it to the Norwegian
material. Merging is still correct — disjoint components do not conflict, they
just never meet — but until an export bridges them, "the tree" is a shorthand
for two. `reports/frontier.md` tracks the components.

## Layout

```
data_lake/     the exports as received (zips gitignored, .ged files tracked)
data_lake/paths/ Geni relationship paths, generated from saved pages
geni_pages/    Geni profile pages saved from the browser (the source of the above)
src/genimerge/ the package
reports/       generated reports that are worth reviewing and keeping
out/           generated data (gitignored)
tests/         pytest
```

- `queue.md` — concrete steps currently in scope
- `todo.md` — the long-horizon backlog
- `devlog.md` — what has been finished, dated

## Usage

Nothing to install; the package is stdlib-only and `pytest` is wired to find it
via `pythonpath`.

Tests run **locally**, not on push. This is a private repo, where GitHub Actions
minutes are billable rather than free, so `.github/workflows/ci.yml` is
manual-only (`workflow_dispatch`) and disabled at the GitHub end. Run the suite
before pushing:

```bash
python -m pytest                     # run the tests

export PYTHONPATH=src                # on PowerShell: $env:PYTHONPATH="src"
python -m genimerge inventory        # measure the exports  -> reports/inventory.md
python -m genimerge merge            # merge them           -> out/merged.ged
python -m genimerge export           # canonical dataset    -> out/people.jsonl
python -m genimerge reconcile        # match by P2600       -> out/wikidata/
python -m genimerge expand --search  # propose more links   -> out/wikidata/candidates.csv
python -m genimerge coverage         # what is linked       -> reports/wikidata-coverage.md
python -m genimerge consistency      # dates that contradict -> reports/consistency.md
python -m genimerge frontier         # where the tree stops -> reports/frontier.md
python -m genimerge seeds            # what to export next  -> reports/seeds.md
# a saved Geni profile page -> a path file carrying every profile ID
python -m genimerge path-from-html "geni_pages/<saved page>.html" -o data_lake/paths/jimmu.tsv
# how much of that path the tree holds -> reports/path-jimmu.md and .json
python -m genimerge path data_lake/paths/jimmu.tsv
python -m genimerge names            # name-item coverage   -> reports/names.md
python -m genimerge quickstatements  # edits to review      -> out/wikidata/add-p2600.qs
python -m genimerge name-links       # name links to review -> out/wikidata/add-names.qs
python -m genimerge crosscheck       # us vs Wikidata       -> reports/wikidata-crosscheck.md
```

Every command is re-runnable and reads the previous stage's output. Wikidata
responses are cached under `out/wikidata/cache/`, so re-running a report costs
nothing; delete that directory to force a refresh.

Every command also takes `--data-lake`, `--out` and `--reports`, so a second
dataset can be processed without touching the first:

```bash
python -m genimerge merge --data-lake ~/other-tree --out /tmp/o --reports /tmp/r
```

## Reports

Generated, and worth reading in this order:

- `reports/inventory.md` — what is in each export, and how little they overlap
- `reports/merge.md` — what merged, what conflicted, what did not resolve
- `reports/wikidata-coverage.md` — how much of the tree reaches Wikidata
- `reports/consistency.md` — dates in the tree that contradict each other, split into impossible and implausible
- `reports/frontier.md` — where the tree stops: parentless people, components, generational depth
- `reports/seeds.md` — the next exports to take, as a sequence whose breadth-first balls barely overlap
- `reports/path-jimmu.md` — how much of a Geni relationship path the tree holds, and where it breaks; `reports/path-jimmu.json` is the same thing per step, with each person's Geni link, whether we hold them, and which component they are in. Joined on the profile ID, because the IDs are extracted from a saved page rather than a pasted one — see `path-from-html`. A path file missing IDs falls back to name matching, and then the report says so at the top
- `reports/names.md` — which surnames and given names already have Wikidata items
- `reports/wikidata-crosscheck.md` — where we and Wikidata disagree about parents, spouses and dates

## Editing Wikidata

This project **never writes to Wikidata**. Three commands each produce a
QuickStatements batch and a readable `.md` beside it listing every edit with
links to both sides. Review the `.md`, then run the `.qs` yourself at
[QuickStatements](https://quickstatements.toolforge.org/) if you agree with it.
Nothing is sent from here, ever.

| command | batch | changes | risk if wrong |
| --- | --- | --- | --- |
| `quickstatements` | `add-p2600.qs` | the Geni profile ID on items that should carry one | an external ID pointing at the wrong profile |
| `name-links` | `add-names.qs` | P735/P734 links to name items that already exist | a person linked to the wrong name item |
| `crosscheck` | `add-claims.qs` | **parents, spouses and dates** | a false statement about a person's family |

They are listed in ascending order of consequence, and that ordering is worth
respecting when deciding what to run first. Adding a Geni ID is a fact about a
record. Asserting someone's mother is a claim about a person, on a public site,
that other projects will copy.

Each batch enforces its own rule for staying out of trouble, and each refuses
rather than guesses:

- **`add-p2600`** — only links confirmed by family *structure* get in.
  Name-search proposals stay in `out/wikidata/candidates.csv` however good their
  score looked, because a matching string is not evidence that two records
  describe the same person. An item already carrying a *different* Geni ID is
  reported as a contradiction and left alone, never overwritten.
- **`add-names`** — an ambiguous name is set aside rather than picked between.
  On the current tree that is 413 names, listed with reasons in `add-names.md`.
  This batch only *links to* name items that already exist; it never creates
  one.
- **`add-claims`** — only gaps are proposed, never conflicts. A relationship
  needs **both** people linked by their Geni ID, not by inference. A date must
  be exact in our export — anything marked `ABT`, `BEF` or `AFT` is not eligible.
  A claim with more than one possible value is withheld. On the current tree
  that withholds 100 gaps to propose 65 statements.

`reports/wikidata-crosscheck.md` also lists **links worth re-checking**: people
who conflict with their Wikidata item on more properties than they agree on.
That is a signal about the *link*, not about any one fact, and it is for a human
to resolve — nothing there reaches a batch.
