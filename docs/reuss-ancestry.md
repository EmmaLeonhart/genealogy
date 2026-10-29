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

## Wikidata side, with dates (same evening)

Birth and death years were read from Wikidata (read only, `scripts/offline/wd_dates.py`) for all
5,298 people in her Wikidata ancestry; 4,082 have a date, and 2,048 were born 900–1600, the span
of Abul Hamza's descendants. Matched with the same strict rules (`scripts/offline/wd_vs_ah.py`):
**no Reuss or Plauen among them, and no match with Abul Hamza's descendants.**

**Weak point:** Wikidata labels are English ("Christian of Thuringia") while `test.ged` names are
often German, Portuguese or Latin ("von Thüringen"), and the matching compares words literally.
So this zero is weaker than the synoptic-tree one. Language-aware matching is queued.

## Language-aware rerun

`compare_ah.py` now maps names across languages (Henry/Heinrich/Henrique/Enrique, John/Johann/
Jean/João/Juan, Thuringia/Thüringen, Saxony/Sachsen, Braganza/Bragança and about 200 more).
Rerun of both comparisons:

- **Wikidata ancestors (dated):** still no match and no Reuss. The 2,841 near misses (same birth
  year, one shared name word) were checked: all are different people (e.g. Anna Maria Thierry vs
  Anna Maria von Lüneburg).
- **Synoptic-tree ancestors:** 5 matches, all false: Anna Maria Thierry / Anna Maria von Lüneburg
  (1610), Anna Katharina von Köller / von Münsterberg (1475), Jean II Baillet / Juan II of Aragón
  (1400), Johann II von Saffenberg / Jan II van Bouchout (1320), Guillaume I de Mont Saint Jean
  (Burgundy) / William de Saint John (England) (1175).

**Conclusion: neither tree contains a link between Emma's ancestors and Abul Hamza's
descendants.** The missing link has to be found or made; the next step is to find where the two
sets come closest (shared houses in overlapping centuries).
