# What the saved Geni pages hold, and how much of it is extracted

Measured 2026-09-24 over all **695 saved pages** in `paths_for_wikidata_isolates/` (666) and
`geni_pages/` (29). `saved-page-extraction.csv` has a row per page. Every page carries two
things: a **relationship path** and an **immediate family**.

## The path: 693 of 695 extracted

`genimerge.genipage.parse_relationship_path` finds a full path on every page (12 to 267 steps;
none is the collapsed three-segment *You → X*). Compared step by step, by Geni id, with
`paths/*.tsv`:

    identical to a paths/ TSV that names the page as its source   691
    identical to a TSV under another name (duplicate saves)         2   Matthew -> makeda-to-matthew, Gōng Liú -> gong-liu
    NOT EXTRACTED                                                    2   Inger Axelsdatter Güntersberg (27 steps)
                                                                         James VI/I Stewart (51 steps)

Every `paths/*.tsv` has its tiny GEDCOM in `exports/tiny-paths/`, apart from five paths
`path-between.py` computed over our own tree, which carry no new people.

## The immediate family: in the HTML, and in two places

The Immediate Family block renders **two views, and a saved page carries both**, whichever was on
screen:

    <span class="photo_view_only">Showing 12 of 46 people</span>
    <span class="text_view_only">Showing 46 people</span>
    <ul class="photo_view_only ...">       12 cards, one person and one relation word each
    <div class="text_view_only"><table class="data_table">
      <tr><th>Son of</th><td><a data-profile-id="...">...</a> and <a ...>...</a></td></tr>

**The photo view stops at 12. The text view is the whole family.** Over the 695 pages:

    relatives the pages count (text-view "Showing N")      5,667
    in the text-view table                                 5,357
    on photo cards                                         5,024
      of which on a card and NOT in the table                195
    table + cards                                          5,552   98%
    counted but in neither                                   132   on 44 pages, not yet found

The table's relation words: `Son of` 614, `Brother of` 478, `Husband of` 473, `Father of` 388,
`Half brother of` 70, `Ex-husband of` 39, `Daughter of` 36, `Sister of` 23, `Wife of` 18,
`Mother of` 16, `Partner of` and `Ex-partner of` 9 each, and a few rarer ones.

## ⛔ The 2026-09-14 "6,477 never rendered" was wrong

The devlog entry *THE SAVED PAGES WERE TRUNCATED AND THE NUMBER IS 6,477* read `Showing 12 of N`
on the photo view, extracted the photo cards, and concluded that the rest *"were never in the
files"*. They were in the files, in the text-view table next to the cards. The 1,555
`geni-scraping/` pages were deleted on that basis. They are still in git history, and
their tiny profiles were built from at most 12 cards each.

The text-view table has the shape the 2026-09-10 ruling moved away from: a relation heading over
a run of names. It is a table cell, not prose, and every name in a row takes that row's relation
(`Father of | Alexander IV Aegus; Heracles and Alexander of Megalopolis`). Read it by the
`th`/`td` structure and the `data-profile-id` of each anchor, never by splitting text.

## The 1,555 deleted `geni-scraping/` pages (restored from `30786275d^`)

These are profile pages, not path pages, but each has the same relationship panel. Measured on
every page:

    a real path on the page                                   457
      4+ steps                                                452
      2-3 steps (parents and grandparents)                      5
      every step already in exports/tiny-paths/saved-<id>.ged  457 of 457
    saved before Geni computed a path                        1,088
      "<!-- no paths loaded -->" and the unclicked "How are you related?" button;
      the page holds only You -> ? -> subject, so there is no path to extract
    no path on the page                                         10
      the account's own profile, and 9 with an empty relationship panel

**The family is where the loss was.** The 2026-09-14 extraction read the photo cards, 15,995
people. The text-view tables on the same pages hold 20,079. Table and cards together give 20,637
of the 22,464 the pages count. 1,532 pages carry a table.

## Extracted, 2026-09-25: every page's path and family are in GEDCOMs

**Paths.** The two missing paths are extracted:
`paths/isolate-geni-inger-axelsdatter-g-ntersberg-1571-1613-voss.tsv` (27 steps) and
`paths/isolate-geni-james-vi-i-stewart-king-of-scots-king-of-england-irelan.tsv` (51 steps), each
with its `exports/tiny-paths/<same stem>.ged`. They were built by `genimerge path-from-html` and
`build-tiny-gedcoms.path_gedcom`, and committed in `83e32b58c`. So all 695, plus the 457 real paths
among the 1,555, are in GEDCOMs.

**Family.** All 2,250 pages (695 here, 1,555 restored) were read by the text-view table
(`th`/`td` plus each anchor's `data-profile-id`) and the photo cards. They were unioned per
subject (2,155 subjects, since some are saved more than once) and rendered with
`build-tiny-gedcoms.render`. The result is **2,131 `exports/tiny-profiles/family-<id>.ged`**. The other
24 subjects are private profiles with no family block. They are new files beside the old
`saved-<id>.ged`, not overwrites. The merge joins on the Geni id, so the two fuse.

    parent slot       from the relative's own stated sex (card word, or the same person's
                      word on any of the 2,250 pages: 12,925 people, 0 contradictions),
                      never from position
    siblings          full siblings go in the birth family; half-siblings are not paired
    children          the subject is the one parent; the other parent is NOT asserted, because
                      the page doesn't say which spouse a child is by
    adoptive/foster   own family, with the attested PEDI/ADOP shape
    step-parent       married to the birth parent of the other sex; the subject is not a CHIL

**What the old card-only files said that this doesn't: 853 edges, every one false.** Old
edges not in the new files: 848 stepchildren and stepmothers written as birth children and
parents, 6 fiancé(e)s written as spouses, and one biological mother married to the adoptive
mother. The old files also named the subject `NN`; the new ones use the page's `h1`.

**The 132 (and 1,827 on the restored pages) are not in the HTML.** Every link in every text-view
cell on all 2,250 pages is either a person with a `data-profile-id` (hidden "and N others"
spans included) or one of 2,524 `N others`/`« less` toggles. No cell carries a bare name. The
`Showing N people` count is larger than what Geni rendered, and the HTML can't close the gap.

**Residuals: `saved-page-family-residuals.tsv`, 2,334 rows.** These are relatives on a page that
went into no family. 2,253 have a relation with no family shape (half-siblings, stepchildren,
fiancé(e)s, `ex-partner's son` and similar). 77 are parents whose sex no page states. 4 are
contradictions. They stay because the HTML is going.
