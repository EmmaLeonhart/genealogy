# `gedcom/` — GEDCOMs that are **not** Geni exports

**Nothing in this directory is a Geni export, and nothing in it is corpus.**
`genimerge.sources.find_exports()` reads `exports/` only, so the merge, the
density and presence counts, and `tests/test_gedcom_real_exports.py` never see
these files. That last one matters: it asserts that exactly four xref prefixes
occur across the corpus and that each binds to one record type, and a
hand-built file would fail it for reasons that say nothing about Geni's format.

These files carry **no `RFN geni:` lines and no profile IDs**, because the people
in them have no Geni profiles — that is the point of them.

## `samaritan-sources.ged`

The Israelite Samaritan genealogy as the published sources give it: **176
individuals, 69 named and 107 explicit placeholders**, built by
`scripts/build-samaritan-gedcom.py` from `reports/samaritan-priesthood.md` and
`reports/samaritan-families.md`.

**Open it in a tree editor and enter the named people into Geni.** That is what
it is for. The corpus holds a component of 33 Samaritan priests cut off from the
main tree, and every person in this file is either above that component or beside
it in a household Geni does not record at all.

**The placeholders are marked and must stay marked.** 107 of the 176 have no
`NAME` and a `NOTE` that says so. They fill the stretch of the 'Abtah line
between Itamar ben Aaron and Shalma, which no source names — the length is
borrowed from the *parallel* Phinhas line's 112 generations, so it is an estimate
from a sibling lineage rather than a count anybody made of this one. **No name is
invented anywhere in this file.** If a placeholder ever acquires a name it should
come from a source, not from the shape of the tree.

One placeholder is doing something different and is worth knowing about: the one
between `'Abed Ela ben Shalma` and `Yusef` carries a distance the source does not
state, and **it may be zero** — 'Abed Ela may simply be Yusef's father.

**The high-priestly office is not descent.** From 1624 the office passes to "the
eldest priest of his brothers", not father to son, so the twenty high priests are
linked by the patronymics the source states and never by their order in office.

## `reports/sources/`

The three source documents, archived because two of the three hosts are dead:

| file | what |
| --- | --- |
| `samaritan-update-2012-marchapril.html` | the March–April 2012 issue carrying "The High Priesthood and the Israelite Samaritan Priests" |
| `ratson-2012.pdf` | "Ratson b. Benyamim Tsedaka — 90 Years to His Birthday" |
| `tsedakafamily-2008.pdf` | "The Tsedaka Family", 2008 |

`shomron0.tripod.com` and `thesamaritanupdate.com` both refuse connections now.
Emma's browser reached them; the archive is why that does not have to happen
twice.
