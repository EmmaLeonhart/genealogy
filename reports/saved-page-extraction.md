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
