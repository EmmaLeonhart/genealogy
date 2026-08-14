# Missing ancestors — the ancestor-page cross-reference

**A bounded task with a definition of done: get the named people into the corpus.**
**DONE — 0 left of the 63 this started at, as of 2026-08-13, 186 exports.**
Emma is running the exports. This file is what the task *is*, so it survives a
session boundary.

## Why the task exists

A Geni export stops at roughly 4,200 people (`genimerge.seeds.GENI_EXPORT_CAP`,
4,208 as of 2026-08-13). Clara Amilia Hoknes and Randolph Paulus Borsheim each
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

## Where it stands — 2026-08-13, 186 exports — COMPLETE

| | count |
| --- | ---: |
| enumerated ancestors on the pages | 337 |
| present in the corpus | 337 |
| absent rows | 0 |
| **distinct people absent** | **0** |

**63 at 178 exports → 61 at 182 → 23 at 184 → 1 at 185 → 0 at 186.** Three exports did
effectively all of it, and all three were seeded on people who were on the list:

| seed | who | closed |
| --- | --- | ---: |
| `6000000227227035828` | mother of Heimgest Godgestsson | — |
| `6000000227227016909` | father of Nauma, Queen of Haalogaland | 38 together |
| `6000000227227039845` | mother of Fiachu MacCathaír Bélach Ciannachta | 22 |
| `6000000227227104853` | father of Marianos Argyros | 1 |

The first two closed the whole Norse block — Hålogaland, the Hervarar-saga
giants, Gylfi's line, Starkad, Varmland, Reidgotaland. The third closed every
Irish line at once: Leinster / Uí Dúnlainge, Dál Fiatach / Ulster, Ciannachta /
Munster, and all four unnamed wives.

Against that, the four exports placed just before them — seeded on
cluster-joining targets rather than on the list — closed **2** between them.
**Seed on the list or the number does not move**, and that is the single lesson
of this task.

**Every enumerated ancestor on both pages is now in the corpus.** The last was
Marianos Argyros `6000000026979610847`, closed by an export seeded on his father.

**Re-run the check when new ancestor pages are saved.** This is done for the 18
pages in `missing ancestors/`, which are Clara's and Randolph's deep pages. It
says nothing about any root whose pages have not been saved.

**The gap is a band in the middle, not a cut-off tail.** Generations 50–54 are
fully present, 18 of 18 — Fjolnir King of Uppsala, Svegdi Fjolnarson, Vana,
Woden, Vanlandi, Visbur, Bældæg, Weothulgeot and the rest. The exports reached
them. What is missing sits at **generations 39–49**, and the hollow is deepest
at 44–47.

| great-grandparent generation | present | absent |
| --- | ---: | ---: |
| Clara 38–41 | 53 | 7 |
| Clara 42–44 | 38 | 5 |
| Clara 45–47 | 29 | 7 |
| Clara 48–49 | 13 | 4 |
| Clara 50–54 | 18 | **0** |
| Randolph 38–41 | 49 | 9 |
| Randolph 42–44 | 39 | 4 |
| Randolph 45–47 | 23 | 8 |
| Randolph 48–49 | 13 | 2 |
| Randolph 50–54 | 16 | **0** |

Three pages are clear: `Clara …Ancestors214`, `Randolph …Ancestors213` and
`Randolph …Ancestors214`.

## Seeding the exports

The productive seed is the **midpoint of a page's absent run** — an export ball
reaches both up and down from its seed, so the middle of a run closes more of it
than either end. Taken in page order, one per page:

| page | absent | midpoint seed |
| --- | ---: | --- |
| Clara 2017 | 3 | `6000000001452856689` Ailill mac Dunlainge |
| Clara 206 | 2 | `6000000014055774662` NN |
| Clara 208 | 2 | `6000000008630666201` Niae Dunlaing mac Éndae Niae |
| Clara 209 | 2 | `6000000008630666206` Éndae Niae mac Bressail Bélach |
| Clara 210 | 2 | `6000000002188140044` NN NN |
| Clara 211 | 2 | `6000000003828254160` Condla mac Taidhg Ciannachta |
| Clara 212 | 6 | `6000000003828110552` Cian mac Mug Nuadat, King of Munster |
| Clara 213 | 4 | `6000000003828250921` Oengus (Aenghus) Finn, King of Ulster |
| Clara 214 | 0 | — clear |
| Randolph 206 | 2 | `6000000014055774662` NN |
| Randolph 207 | 4 | `6000000014056180070` N.N. |
| Randolph 208 | 3 | `6000000002188140029` NN NN |
| Randolph 209 | 2 | `6000000002188140044` NN NN |
| Randolph 210 | 2 | `6000000003828254160` Condla mac Taidhg Ciannachta |
| Randolph 211 | 4 | `6000000003827138372` Findchaem ingen Cerb |
| Randolph 212 | 6 | `6000000011830284701` NN Dál Fiatach |
| Randolph 213 | 0 | — clear |
| Randolph 214 | 0 | — clear |

12 distinct midpoints; NN, NN NN and Condla mac Taidhg Ciannachta are each the
midpoint of two pages. Recompute these after every batch — they move as the
absent runs shrink.

**Do not group these by patronymic and export from the "line".** That was tried
on 2026-08-13 — `X Ysson` names a father who does sit one generation up, so the
chains look exact — but it is inference layered on top of an ordering the pages
already give, and it produced a different and worse set of seeds than page order
did. The page order is Geni's own enumeration. Use it.

## Definition of done

`py scripts/check-missing-ancestors.py` reports **absent: 0**. Re-run it after
every batch of exports lands; it takes about a minute over 186 GEDCOMs and needs
no merge.

## What this task is not

It is not the ancestry frontier — "which people in the tree have no parent
recorded" — which is a different question over different data and was built and
deleted on 2026-08-13 because it was not what was asked for. The saved pages are
the source here, and the only source.
