# Missing ancestors — the ancestor-page cross-reference

**A bounded task with a definition of done: get 63 named people into the corpus.**
Emma is running the exports. This file is what the task *is*, so it survives a
session boundary.

## Why the task exists

A Geni export stops at roughly 4,100 people (`genimerge.seeds.GENI_EXPORT_CAP`,
4,128 as of 2026-08-13). Clara Amilia Hoknes and Randolph Paulus Borsheim each
have **more ancestors than that**, so exporting from either returns a ball that
is cut off before it finishes, and nothing in the export says who was left out.

Geni's **ancestor-list page** does say. It enumerates every ancestor Geni knows
about for a root person, twenty per page, with each one's profile id stamped on
the row. Emma saved those pages, and that enumeration is the definitive list of
who her genealogy needs — the only evidence in this repo of people no export has
reached.

**18 saved pages in `missing ancestors/`** — `Clara Amilia Hoknes's
Ancestors206…214` and `2017`, `Randolph Paulus Borsheim's Ancestors206…214`.
They are the deep pages, not the whole enumeration: the near generations are
covered by the exports and were never in question.

## What the check does

`scripts/check-missing-ancestors.py` reads every row of every saved page, pulls
the ancestor's Geni profile id, and asks one question: does that id appear as an
`INDI` xref in any GEDCOM under `exports/`?

- **Exact join on the profile id**, the repo's primary key. Never a substring —
  a short legacy id like `45855` substring-matches 59 files and none of them are
  that person. Never a name.
- **Reads `exports/` directly, not `out/merged.ged`.** The merged tree lags: on
  2026-08-13 it predated two gap exports taken that evening. A freshly extracted
  download counts immediately.
- **Scoped to the `<tr>`, never to the anchors.** Each row carries
  `data-profile-id` on the row element itself; matching `people/<slug>/<id>`
  anchors anywhere on the page silently pulls in the **profile managers**, whose
  links sit in a `managed_by-area` cell of the same row and carry the same
  `?through=` seed. That is not a near-miss — it put three living account holders
  into a list of Clara's Norwegian ancestors and inflated the absent count. Same
  trap `CLAUDE.md` documents for relationship paths.

Writes `reports/missing-ancestors-check.csv` — one row per (person, root), every
instance, with `present` and `n_exports` — and
`reports/missing-ancestors-still-absent.csv`, one row per distinct absent person.

## Where it stands — 2026-08-13, 178 exports

| | count |
| --- | ---: |
| enumerated ancestors on the pages | 337 |
| present in the corpus | 213 |
| absent rows | 124 |
| **distinct people absent** | **63** |

124 absent rows collapse to 63 people because the two roots enumerate nearly the
same set: Clara's pages carry all 63, Randolph's carry 61 — lacking only Brasila
and Evancio Chirino.

**The gap is a band in the middle, not a cut-off tail.** Generations 50–54 are
fully present, 18 of 18 — Fjolnir King of Uppsala, Svegdi Fjolnarson, Vana,
Woden, Vanlandi, Visbur, Bældæg, Weothulgeot and the rest. The exports reached
them. What is missing sits at **generations 39–49**, and the hollow is deepest
at 44–47.

| great-grandparent generation | present | absent |
| --- | ---: | ---: |
| Clara 39–41 | 44 | 16 |
| Clara 42–44 | 24 | 19 |
| Clara 45–47 | 14 | **22** |
| Clara 48–49 | 11 | 6 |
| Clara 50–54 | 18 | **0** |
| Randolph 38–41 | 40 | 18 |
| Randolph 42–44 | 22 | 21 |
| Randolph 45–47 | 13 | **18** |
| Randolph 48 | 6 | 4 |
| Randolph 49–53 | 21 | **0** |

Two pages are already clear: `Clara …Ancestors214` (14 rows) and `Randolph
…Ancestors214` (3 rows) report zero absent.

## Seeding the exports

The productive seed is the **midpoint of a page's absent run** — an export ball
reaches both up and down from its seed, so the middle of a run closes more of it
than either end. Taken in page order, one per page:

| page | absent | midpoint seed |
| --- | ---: | --- |
| Clara 2017 | 8 | `6000000006906358676` NN vife of Heimgest Godgestsson |
| Clara 206 | 2 | `6000000014055774662` NN |
| Clara 208 | 6 | `6000000008630666201` Niae Dunlaing mac Éndae Niae |
| Clara 209 | 6 | `6000000049537463401` Gudmund |
| Clara 210 | 12 | `6000000006906358126` Himileig Hodbrodsson |
| Clara 211 | 11 | `6000000008248183477` Ama Ymirsdatter |
| Clara 212 | 12 | `6000000008248206405` Kong Trym Jotun av Vârmland |
| Clara 213 | 6 | `6000000011830284701` NN Dál Fiatach |
| Clara 214 | 0 | — clear |
| Randolph 206 | 5 | `6000000045210662979` Grím Jotne |
| Randolph 207 | 5 | `6000000014056180070` N.N. |
| Randolph 208 | 8 | `6000000049537463401` Gudmund |
| Randolph 209 | 7 | `6000000002188140044` NN NN |
| Randolph 210 | 13 | `6000000000314930151` Gylfi (Gylve) King of Sweden |
| Randolph 211 | 11 | `6000000006906358038` Hodbrod Sverdhjaltsson |
| Randolph 212 | 10 | `6000000011830284701` NN Dál Fiatach |
| Randolph 213 | 2 | `6000000006271194025` Saemingr, King in Hålogaland |
| Randolph 214 | 0 | — clear |

14 distinct midpoints; Gudmund and NN Dál Fiatach are each the midpoint of two
pages.

**Do not group these by patronymic and export from the "line".** That was tried
on 2026-08-13 — `X Ysson` names a father who does sit one generation up, so the
chains look exact — but it is inference layered on top of an ordering the pages
already give, and it produced a different and worse set of seeds than page order
did. The page order is Geni's own enumeration. Use it.

## Definition of done

`py scripts/check-missing-ancestors.py` reports **absent: 0**. Re-run it after
every batch of exports lands; it takes about a minute over 178 GEDCOMs and needs
no merge.

## What this task is not

It is not the ancestry frontier — "which people in the tree have no parent
recorded" — which is a different question over different data and was built and
deleted on 2026-08-13 because it was not what was asked for. The saved pages are
the source here, and the only source.
