# Reuss and Abul Hamza against Emma's ancestors: first pass, 2026-10-09

**Question (Emma):** she found the Reuss family among the descendants of Abul Hamza
(Gregory-Abuhamza Artsruni, b. 869, the root of `rootsmagic/test_2026-10-09.ged`) and wants to
know how her own ancestors connect to them. Her words: the link "doesn't exist in either one of
them, and that's why we're fixing it."

## Material

- **Abul Hamza's descendants:** `rootsmagic/test_2026-10-09.ged` (converted from her live
  `test.rmtree`). 73,711 descendants. 185 Reuss-named people, from Heinrich I "der Reuße" von
  Plauen (b. 1253); their lines in this file stop around 1700.
- **Her ancestors:** her own line is on Wikidata (Q140568870; her parents Richard Wade Borsheim
  and Helen Frisk; Norwegian and Swedish lines: Borsheim, Hoknes, Fuglestad, Birkland, Frisk,
  Wedberg, Andersson). Exported read-only with `wikidata_to_gedcom` (5,297 ancestors, no dates).
  2,223 of them were found in the synoptic tree (`out/merged.ged`, 2,273,878 people, rebuilt
  locally with `genimerge merge --slim`), and walking up from those gives **33,541 ancestors in
  the synoptic tree**. Her Geni account profile is Jingū and carries no real parents, so it is not
  the starting point.

Matching is by name and dates, not IDs (both trees hold duplicates): same name parts (at least
two), birth year against birth year within one year, death year only when there is no birth year.
Duplicates inside a tree are followed only on the same full name, same birth year and no
conflicting death year.

## Result

**No connection found with honest links.** None of her 33,541 synoptic-tree ancestors is a Reuss
or a Vogt von Plauen, and none of them matches any of Abul Hamza's 73,711 descendants. The only
two matches are false (same given names, different families):

| her ancestor | gen. up | test.ged person | gen. below Abul Hamza |
|---|---|---|---|
| Anna Maria Thierry (1610) | 12 | Anna Maria von Lüneburg (1610) | 21 |
| Anna Katharina von Köller (1475) | 16 | Anna Katharina von Münsterberg (1474) | 19 |

So the link is genuinely missing in both trees, which is what she said.

## Earlier runs were wrong, and why

The first runs of this analysis reported Reuss ancestors (Heinrich III "der Lange" Reuß zu
Plauen, Anna von Plauen and others) and 87 Abul Hamza overlaps through the Bagrationi, Komnenoi,
Palaiologoi and Valois. **All of those came from bad bridges built by the matching, not from the
trees:** two unnamed "NN" profiles treated as one person; a birth year matched to a different
man's death year (Anders Andersson); and "Samson Леванович Шервашидзе", whose Cyrillic was
dropped by normalization, matched to the Norwegian "Samson" above Jon Samsonsen Gimre. The rules
above exclude each of these. Do not cite those earlier results.

## Next

- Find where her lines come closest: the ancestors in German-speaking lands nearest in time and
  place to the Reuss lines (Vogtland, Thuringia, Saxony), as candidates for the missing link.
- The 3,074 Wikidata ancestors not found in the synoptic tree could carry the link; getting
  their dates from Wikidata (read-only) would let them be matched too.

Scripts: `scripts/offline/compare_ah.py`, `scripts/offline/reuss_paths.py`,
`scripts/offline/ged_lib.py` (stdlib only).
