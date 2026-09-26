# What the repo holds, and how the tree relates to the owner's ancestors

2026-09-26. Read only through the derived tables and file names, never the corpus: `out/merge-report.md`
(the merge run in Actions on 2026-09-26), `git ls-tree` for paths, `reports/derived-family.csv`,
`reports/derived-places.csv` and `reports/owner-ancestors.tsv`. Every instance is in the two CSVs:

- `reports/repo-individuals-by-source.csv`: one row per merge source (32,266), with its directory,
  style and the individuals it first contributed.
- `reports/exports-vs-owner-ancestors.csv`: the same rows, plus each export's seed and what that
  seed is to the owner.

## Where the individuals are

The merged tree holds **2,250,893 individuals** and 1,124,942 families from 32,266 GEDCOM files.
By folder, people first contributed:

| folder | files | individuals |
| --- | ---: | ---: |
| exports/chain-seeds | 148 | 551,440 |
| exports/sweep-parsed | 3 | 356,998 |
| exports/bure-campaign | 40 | 140,220 |
| exports/tiny-paths | 27,165 | 128,035 |
| exports/gaps | 64 | 109,345 |
| exports/8-19 exports | 32 | 94,224 |
| exports/abul-hamza-descendants | 29 | 69,456 |
| exports/edges | 36 | 60,097 |
| exports/fleshing-out | 40 | 58,500 |
| exports/post-merge | 78 | 50,309 |

The rows sum to 1,997,411, not 2,250,893. The shortfall is a merge-report defect, not missing
people: 530 file names are shared by 1,064 exports, and the report let the second overwrite the
first. It is fixed, so the next merge's report reconciles.

## The owner's ancestors, by side: WITHDRAWN, the tree has a cycle through the owner

**The split first written here (9,708 maternal against 283 paternal, and 51% of the tree descending
from the maternal ancestors) is withdrawn.** On today's tree (`derived-family.csv` of 2026-09-26),
the owner's profile carries five fathers, three mothers and eleven children, and one of the
"children" is `Louis I, The Pious` (`6000000001266578142`, born 778). That one inverted edge closes a
cycle: the owner's father sits 34 generations above the owner's mother. Every ancestor above Louis
then counts as an ancestor of both parents, 44,067 of them, so any split by side made on this
tree measures the defect, not the family. `reports/owner-ancestors.tsv` (9,991, built the day
before) predates part of it and is itself stale.

The harvested path for Louis (`exports/tiny-paths/harvested-path-geni-6000000001266578142-blood.ged`)
and the owner's saved-page family (`exports/tiny-profiles/family-6000000087535357291.ged`) are both
correct, so the inverted families come from another file. Finding it is queued.

## The exports against those ancestors

**Read with the cycle above in mind:** "maternal" here was computed on the cyclic tree, so it
means "an ancestor of the owner" rather than a side.

By what each export's SEED is to the owner (a seed-level reading: an export seeded on a stranger
can still hold relatives):

| seed | files | individuals first contributed |
| --- | ---: | ---: |
| unrelated to the known ancestors | 602 | 1,254,677 |
| no seed in the file name (tiny paths, sweeps) | 31,453 | 522,319 |
| a maternal ancestor | 117 | 108,609 |
| not in the tree | 55 | 76,867 |
| a descendant of a maternal ancestor | 39 | 34,939 |

So the export campaigns have mostly been seeded outside the owner's own ancestry. The P2600 chain
seeds, Abul Hamza's descendants, the sparse filling and the Ben-Ovadya descendants are all
"unrelated" by seed. The seeds on the maternal line concentrate in `post-merge`, `gaps`,
`8-19 exports` and `descendants`. `bure-campaign` is mostly seeded outside the known ancestors,
with 7,271 people from seeds who descend from them.

## Leads on the mother's side: Baltic Germans, the Rurikids, the Caucasus

Tested 2026-09-26 against the derived tables. Every hit is in
`reports/maternal-leads-baltic-rus-caucasus.csv`. Because of the cycle above, "maternal" there covers
the owner's known ancestors on both sides.

- **Baltic Germans: one lead, not a line.** Per Andersson Roth (generation 10, born 1683) died in
  Livland. No birth in Livonia, Estonia, Courland or Riga, and no Baltic-German noble name among
  the known ancestors. The hypothesis is not supported by the tree as it stands.
- **The Rurikids: yes, and on both sides.** 50 ancestors carry a Rus birthplace or name, the
  nearest at generation 25: Sofia of Minsk, Queen of Denmark; Vysheslava Yaroslavna of Halych;
  Mstislav and Vladimir Monomakh. **Yuri Dolgoruky is an ancestor**
  (`6000000002187826932`, generation 24 on today's tree). Through the mother it is 29 generations:
  Frisk, then Swedish nobility (Natt och Dag, Sparre), then Svantepolk Knutsson, then Hedvig of
  Gdańsk, then Euphrosyne (Piast), then Vysheslava Yaroslavna, then Olga Yurievna, then Yuri.
  Through the father it is 26 generations: Borsheim, then Norwegian and Danish Bille and
  Skarsholm, then the same Hedvig of Gdańsk. These are the tree's links, not checked against sources.
- **The Caucasus: through Byzantium.** Seven ancestors born in Armenia, the nearest at generation 33:
  Romanos I Lekapenos (born about 870 at Lakape), Theophylaktos Abastaktos, Zoë Dalassena, Ioannes
  Kourkouas. That is the route a descent-from-antiquity claim would take, and it is a lead to test,
  not a finding.
