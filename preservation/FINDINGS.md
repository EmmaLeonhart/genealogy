# What is in the preservation archive

Queue item 3, 2026-09-17: *"investigate if the pfinzing and reuss connections are there in that"*.

## Yes. Both, as real people, in a file that is not in the Geni corpus

The lead was *"I could have sworn that there was a connection to two Bavarian noble families here
that I can't actually find."* They are in `preservation/genealogy/dropbox/Hethel Pedigree.ged` —
**33,878 people** — which is why they could not be found: the corpus under `exports/` is Geni, and
this tree never came from Geni.

**`Pfinzing von Henfenfeld`, a lineage rather than a stray name** — Siboto, Berthold II,
Berthold III, Markward Merklin, Markward Sigfried, Endres/Andreas, Nicolaus, Elisabeth, Otildis.
34 name lines.

**`Reuss`** — Heinrich XXIV Count of Reuss-Ebersdorf, Augusta Reuss-Ebersdorf, Princess Augusta
Reuss-Köstritz, Charlotte Princess Heinrich XVIII Reuss of Köstritz. 9 name lines.

## And the same file carries the campaign's targets

| name | count | why it matters |
| --- | --- | --- |
| `Pfinzing von Henfenfeld` | 34 | the Bavarian family that could not be found |
| `Reuss` | 9 | the other one |
| `Lusignan` | 32 | the kings of Cyprus |
| `Ibelin` | 8 | the Cyprus hinge already in `exports/tiny-paths/` |
| `Bagration` | 2 | **Princess Leonida Bagration of Mukhrani**, and `Bagrationi` |
| `Flemming` | 1 | the Pomeranian cluster |

`Bagration` is the stated goal — *"that would get us to the Georgian royal family, who is the
goal"* — and it is sitting in the same 33,878-person pedigree as Cyprus and the two Bavarian
families.

## The other files

* `a.ged` — 33,877 people, a different md5 from `Hethel Pedigree.ged` and one person fewer. Two
  versions of one tree, not a duplicate.
* `Theogrammaticus.ged` / `Mannus.ged.doc` — 8,244 people each, different md5s. Carry Pfinzing
  (15) and Reuss (11) and Bagration (2), but **no Lusignan and no Ibelin**.
* `Gaiad.ged` — 62,294 people, the largest single tree in the archive.
* The three MyHeritage *Descent from Antiquity archive* snapshots — 1,550 / 4,033 / 4,093 people,
  late-antique Roman names, and **no Pfinzing and no Reuss at all**.

⛔ **PRESENCE IS NOT CONNECTION, AND NOTHING HERE CLAIMS IT IS.** These are counts of name lines in
a GEDCOM. Whether Pfinzing reaches Bagration *through* this pedigree is a separate question, and
`CLAUDE.md`'s rule for the campaign applies to it: the point is to **add** blood, not to find it in
a graph. What this file establishes is that the material exists and where it lives.

⛔ **THE XREFS HERE ARE NOT GENI IDS.** Nothing in `preservation/` is corpus. It must not be merged
into the synoptic tree on the assumption that its ids join.
