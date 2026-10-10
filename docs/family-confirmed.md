# Same person on both sides, confirmed by family: 2026-10-09

**Result: none.** No one among Emma's 33,495 synoptic-tree ancestors is the same person as any of
Abul Hamza's 73,711 descendants, even with loose dates, when identity is confirmed by family.

**Rule** (`scripts/offline/family_confirmed.py`): same first name (across languages), at least one
more shared real name word (not a numeral, title or particle), birth years within 40 years or one
missing, **and** a parent or spouse of one matches a parent or spouse of the other by the same rule.
Polish letters are transliterated and coat-of-arms markers ("h. Nałęcz") ignored.

**The check works:** with the Princess of Achaea added to Emma's side as a control, it finds her
in Abul Hamza's descendants (12 generations down), confirmed by her father (William II = Guillaume
II de Villehardouin) despite a 28-year gap in recorded birth years (1263 vs 1235). With only her
real ancestors, it finds nothing.

**Earlier runs of this check were wrong:** the first gave 265 matches (Polish names split on "ł"
so "Nałęcz" became "na" + "ecz", matching everyone of that coat of arms), the second 9 (numerals
like "III" counted as a shared family name). Both fixed before this result.

This covers every lead in `closest-approaches.md` at once: none of those shared houses has a
person who is on both sides.
