# Synoptic

**A family tree for Wikidata, and later for the Gaiad at
[genealogy.order.life](https://genealogy.order.life).**

One genealogy is assembled from many sources, reconciled against Wikidata, and used to add the
people and relationships Wikidata is missing. Later the same tree becomes the family tree of the
Gaiad, published at genealogy.order.life.

> Scaffolded with [cleanvibe](https://github.com/Immanuelle/cleanvibe).

## What this is

The tree is the thing. Several sources feed it, and none of them is what it is *for*:

| source | what it brings |
| --- | --- |
| **FamilySearch** | downloads under `gedcom/familysearch/`, keyed on the FamilySearch tree id (`_FSFTID`) and walked against the tree by `zipper-join.py --familysearch`. This is the direction the project is moving in. |
| **Wikidata** | the people who already have items, and the relationships between them, joined on their identifiers. |
| **Geni** | GEDCOM exports under `exports/`, the bulk of the tree as it stands. Geni writes its profile id as the GEDCOM xref, so merging exports is an exact join, never a name match. |
| **RootsMagic** | a hand-kept tree, exported as GEDCOM. |

Everything is merged into one tree, `out/merged.ged`, and joined to Wikidata. What Wikidata lacks
goes out as edits: today as a daily QuickStatements batch, generated in CI, sent partly by an
automatic run and published for pasting on the [Pages site](https://emmaleonhart.github.io/genealogy/).
QuickStatements are the main part of that site for now and will become less prominent as the
project moves away from them; the site also has a page for every person the tree has paired with a
Wikidata item.

How the Geni side is merged is exact rather than fuzzy. Geni writes the profile ID as the GEDCOM
xref itself:

```
0 @I6000000001846508982@ INDI
1 RFN geni:6000000001846508982
```

so every record carries a stable primary key across exports, and the same ID is the join key to
Wikidata via **P2600 (Geni.com profile ID)**. **Later sources win** a value conflict, because the
newer export holds the correction.

A Geni relationship path can be checked against the tree step by step on the profile ID:
`reports/path-jimmu.md` walked an 83-step path, Empress Jingū to Emperor Jimmu, from 62 of 83 steps
held to 83 of 83. That is the method, not a one-off: extract the path to someone you want to reach,
and it tells you precisely which people stand between you and them.

## Layout

```
exports/       every Geni export, one directory per batch — the corpus
paths/         Geni relationship paths, generated from saved pages
geni_pages/    Geni profile pages saved from the browser (the source of the above)
src/genimerge/ the package
reports/       generated reports that are worth reviewing and keeping
out/           generated data (gitignored)
tests/         pytest
```

**`exports/` is the corpus, read recursively.** Geni's downloads arrive as
`export-geni (N).zip`, get extracted beside themselves, and are grouped under a
directory named for whoever they were exported from — `exports/Li Hong/`,
`exports/n n/` — or under `exports/archive/` and `exports/fleshing-out/` for
bulk takes. The subdirectories are filing and carry no meaning for the merge;
every `.ged` beneath `exports/` is corpus, and a newly extracted file is picked
up with no further step.

`genimerge.sources` is the single place that resolves this, and it **drops
byte-identical repeats**: the same export arrives twice often enough that
counting one file as two would corrupt `inventory`'s overlap figures and
`density`'s presence counts, both of which divide by how many exports contain a
person.

There used to be a `data_lake/` here that the merge read instead, and ingesting
meant copying a file into it under a second name. That was scaffolding from the
first session that quietly became load-bearing; it is gone, and its five
unique files are in `exports/originals/`.

The zips are gitignored **one line at a time on purpose**, not by a `*.zip`
pattern: an un-ignored zip shows up in `git status`, which is how a finished
download announces itself.

- `queue.md` — concrete steps currently in scope
- `todo.md` — the long-horizon backlog
- `devlog.md` — what has been finished, dated

**On `geni_pages/`.** Pages are saved with the browser's "complete" option,
which writes the HTML plus a `_files/` tree of JavaScript, CSS and images. Only
the HTML is ever read — `genimerge.genipage` parses the relationship panel out
of it and nothing touches the assets. They are kept anyway, and tracked, because
they are what lets the saved page still open and render offline; a page saved
HTML-only is a page you cannot look at later to check what the parser saw.

The cost is real and worth knowing before saving the next one: the Jimmu page is
**4.4 MB, of which 4.2 MB is assets across 55 files**. A handful of these is
fine; a habit of them is not. If the directory grows past being useful, the
decision to make is *which pages* to keep whole — not to strip the assets from
all of them, which would leave HTML that no longer renders.

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
python -m genimerge overlap          # us vs all of P2600   -> reports/wikidata-overlap.md
python -m genimerge consistency      # dates that contradict -> reports/consistency.md
python -m genimerge frontier         # where the tree stops -> reports/frontier.md
python -m genimerge seeds            # what to export next  -> reports/seeds.md
python -m genimerge density          # where the tree is thin -> reports/density.md
python -m genimerge descendants      # lines that stop early -> reports/descendants.md
# a saved Geni profile page -> a path file carrying every profile ID
python -m genimerge path-from-html "geni_pages/<saved page>.html" -o paths/jimmu.tsv
# how much of that path the tree holds -> reports/path-jimmu.md and .json
python -m genimerge path paths/jimmu.tsv
python -m genimerge entity-resolution # hand-made links -> out/wikidata/entity-resolution.qs
python -m genimerge profile-names    # what the profiles hold -> reports/profile-names.md
python -m genimerge quickstatements  # edits to review      -> out/wikidata/add-p2600.qs
python -m genimerge name-links       # name links to review -> out/wikidata/add-names.qs
python -m genimerge crosscheck       # us vs Wikidata       -> reports/wikidata-crosscheck.md
```

Every command is re-runnable and reads the previous stage's output. Wikidata
responses are cached under `out/wikidata/cache/`, so re-running a report costs
nothing; delete that directory to force a refresh.

### Downloading Wikidata items

`wikidata-download` is deliberately **not** in the block above. It is a
long-running background job rather than a report, it writes source material into
a tracked directory instead of `out/`, and it is the one command that runs for
hours. `todo.md` § 8a-revised is the design; `queue.md` item 4 is the pilot that
has to come first.

```bash
python -m genimerge wikidata-download --dry-run       # how many items remain
python -m genimerge wikidata-download --limit 1000    # the pilot: measure, then decide
python -m genimerge wikidata-download                 # the long run
```

It reads its seed list from `out/wikidata/p2600-all.tsv` — already on disk from
`overlap`, so the seed phase needs no SPARQL — and writes whole items, 50 per
request, into gzipped JSONL shards under `wikidata/items/`. Those shards are
committed; the resume index beside them in `out/` is derived and disposable
(`--rebuild-index` regenerates it). Nothing is ever requested twice, a killed
run resumes, and `--limit` caps how many *new* items a run attempts.

Every command also takes `--exports-dir`, `--out` and `--reports`, so a second
dataset can be processed without touching the first:

```bash
python -m genimerge merge --exports-dir ~/other-tree --out /tmp/o --reports /tmp/r
```

## Reports

Generated, and worth reading in this order:

- `reports/inventory.md` — what is in each export, and how little they overlap
- `reports/merge.md` — what merged, what conflicted, what did not resolve
- `reports/wikidata-overlap.md` — the same join counted from *both* sides: how much of our tree Wikidata knows, and how much of Wikidata's Geni-linked population we hold. `coverage` asks about the IDs we already have and so can only answer the first; `overlap` fetches every P2600 statement, which is the only way to see an item whose Geni profile no export has reached
- `reports/consistency.md` — dates in the tree that contradict each other, split into impossible and implausible
- `reports/frontier.md` — where the tree stops: parentless people, components, generational depth
- `reports/descendants.md` — the downward counterpart to `frontier.md`: people with few but **not zero** lines of descent running down from them, so the line demonstrably continues and we have barely followed it, ranked inside birth-year bands by how few generations down we have walked. It counts **descent paths, not distinct people** — `paths(p) = Σ over children (1 + paths(child))` — so somebody reached down two lines counts twice, because two lines is what an export would follow. The axis `density.md` does not have — it is about *when*, which is what the `Descendants` export campaign is for
- `reports/seeds.md` — the next exports to take, as a sequence whose breadth-first balls barely overlap
- `reports/path-jimmu.md` — how much of a Geni relationship path the tree holds, and where it breaks; `reports/path-jimmu.json` is the same thing per step, with each person's Geni link, whether we hold them, and which component they are in. Joined on the profile ID, because the IDs are extracted from a saved page rather than a pasted one — see `path-from-html`. A path file missing IDs falls back to name matching, and then the report says so at the top
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
