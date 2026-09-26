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

## The owner's ancestors, by side

`reports/owner-ancestors.tsv` holds 9,991 known ancestors. **9,708 are on the mother's side** (the
Bure line) and 283 on the father's. Of the tree's 2,250,893 people, **1,143,707 (51%) descend from a
maternal ancestor**. None descend from a paternal one, which means the 283 paternal ancestors have
no child links in the Geni-derived tree; that is worth a look in its own right.

The maternal ancestors' recorded birth countries, as written (so `Norway`, `Norge` and `Rogaland`
are counted apart): Norway 882, France 312, Rogaland 183, Germany 178, Iceland 174, Sweden 170, Norge
106, Sverige 48, Denmark 39, Deutschland 35, Scotland 23, Holy Roman Empire 23, Byzantine Empire 20,
then a long tail through Kievan Rus', Bulgaria, Bavaria, Hungary, Constantinople, the Netherlands,
Switzerland, Poitou-Charentes, Prussia, Lorraine, Provence, Brittany and Armenia.

## The exports against those ancestors

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
