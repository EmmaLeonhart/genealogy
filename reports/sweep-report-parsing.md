# Can the descendant reports be parsed into a family tree?

**Yes. Measured, not assumed.** Queue item ruled 2026-09-21: *"we can make the descendant reports
into family trees through parsing. The report's relationship needs to be parsed but might work."*

`reports/sweep/*.tsv` is **8,959 files, 1,352,812 rows with a Geni id**. Each row is one person as
a Geni descendant-report page renders them, and two of its columns carry structure.

## What the columns actually hold

| column | coverage | what it is |
|---|---|---|
| `relationship_text` | **100.0%** | `Relationship: Yuri's 8th great grandson` — the relation to the focus person |
| `immediate_family_text` | **94.3%** | `Immediate Family: Son of X and Y Husband of Z Father of A; B and C Brother of …` |
| `immediate_family_hrefs` | — | ⛔ **always `#`** — the links are dead, so the family list carries **names, never ids** |

The family string has a closed role vocabulary and **99.8% of the rows that have one parse against
it**:

    Son of 676,963      Brother of 619,532   Daughter of 595,154   Sister of 550,752
    Husband of 394,378  Wife of 362,177      Father of 340,707     Mother of 298,321
    Half brother of 124,068   Half sister of 111,974
    Ex-husband of 38,978      Ex-wife of 28,831    Partner of 6,469

## The two things it yields

**1. A generation number for 88.7% of all rows**, straight out of `relationship_text` with no name
matching at all. The forms are `son`, `grandson`, `8th great grandson` and `fifth great grandson`
— digits and words both, so the reader needs an ordinal table. Depth runs past 10 generations in
quantity.

**2. 1,090,278 parent-child edges**, by resolving the names in `Son of` / `Daughter of` against the
`name_text` of other rows in the same file:

| | |
|---|---|
| parent names parsed out | **2,557,648** |
| resolved to exactly one Geni id in the same file | **1,090,278 — 42.6%** |
| of those where both ends have a depth, generation-consistent | **941,381 consistent / 73,930 not — 92.7%** |

⛔ **THE 92.7% IS THE POINT, BECAUSE IT IS AN INDEPENDENT CHECK.** The generation number comes from
`relationship_text` and the edge comes from name matching, so *parent depth == child depth − 1* is
a test the edge did not get to influence. It both validates the method and gives a filter: the
7.3% that fail it can be dropped without a human looking at them.

**The 57.4% that do not resolve are mostly correct behaviour, not loss.** A descendant ball
contains the descendant parent but usually not the spouse who married in, so one of the two names
in `Son of X and Y` routinely has no row to match. Ambiguous matches — one folded name, several
ids — are counted as unresolved here rather than guessed.

## The limits, stated

- ⛔ **49.0% of family lists are truncated** — `and 3 others`, `« less`. Sibling and children lists
  are therefore incomplete about half the time. **The parents are not affected**: `Son of …` opens
  the string and 1,272,117 rows name both.
- ⛔ **This is name matching, which the repo forbids for MERGING and for good reason.** It is
  admissible here only because it is scoped inside one file, cross-checked by generation, and
  produces a *candidate* edge for people who are not in the synoptic tree at all. **It must not be
  used to join a swept person to a corpus person** — `CLAUDE.md` § *the Geni profile ID is the
  primary key* is untouched by this.
- The rows carry no dates and no places, so nothing here thickens the place-based instruments
  directly.

## What it is worth

The sweep currently contributes a name and nothing else. Parsed, the same files give **a
generation ladder over 1.2M people and roughly a million candidate parent-child edges**, for a
population the GEDCOM exports never reached — and `yuri-junction-hunt.md` § *Where this leaves it*
names the frontier as the bottleneck on the whole descent hunt.

Not built. This establishes that building it is worth doing and what it would yield.
