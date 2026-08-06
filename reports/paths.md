# Do we have the small-world core?

Generated from the saved Geni pages in `geni_pages/` — re-run with
`python -m genimerge path-from-html <page> -o paths/<name>.tsv` then
`python -m genimerge path paths/<name>.tsv --source out/merged.ged`.

**Why this is the right instrument.** Raw size cannot answer the question: the
Geni world tree is around 210 million people and this merge holds 202,433, which
is 0.1% of it. But a relationship path is a chain Geni computes *itself*, naming
people whether or not any export has reached them. It is the one piece of
evidence here that comes from outside our own data. If arbitrary chains to
far-flung people are held end to end, we hold the connective tissue — which is
what "small-world core" means operationally.

Measured 2026-08-06 over the **202,433-person merge (98 exports)**. A 99th
export landed after this run and is not in it.

## Result

**1,692 of 1,826 steps held — 92.7%**, across **18 distinct chains** reaching
Assyria, Sheba, Egypt, Numidia, Mongolia, the Jin clan, Malwa, Samaria, Toledo,
Japan and Mesopotamia.

`paths/` holds nineteen files, not eighteen: `jimmu.tsv` and
`emperor-jimmu-no-mikoto-711-585-kashihar.tsv` are byte-identical, the same
chain saved twice under two names. It is counted once here. Both are left on
disk — deleting one would only invite it to be saved a third time.

| path | held | | unbroken run ends | gaps |
| --- | ---: | ---: | ---: | ---: |
| Makeda → Enlil-nirari | 225/225 | 100% | 225 | 0 |
| Makeda → Matthew | 219/219 | 100% | 219 | 0 |
| Makeda, Queen of Sheba | 170/170 | 100% | 170 | 0 |
| Emperor Jimmu no Mikoto | 83/83 | 100% | 83 | 0 |
| Lady Palsu of the Jin clan | 60/60 | 100% | 60 | 0 |
| Princess NN | 60/60 | 100% | 60 | 0 |
| Gervasio of Toledo | 42/42 | 100% | 42 | 0 |
| Temüjin Borjigin, Khagan of the Mongol Empire | 36/36 | 100% | 36 | 0 |
| Makeda → Marguerite | 148/155 | 95% | 145 | 2 |
| Eleazar II, Samaritan High Priest | 87/97 | 90% | 34 | 1 |
| daughter of the king of Assyria | 81/91 | 89% | 34 | 1 |
| NN of Malwa | 81/91 | 89% | 34 | 1 |
| NN daughter of Berenice | 80/90 | 89% | 34 | 1 |
| NN | 80/90 | 89% | 34 | 1 |
| Psamtik II, Pharaoh of Egypt | 97/117 | 83% | 42 | 2 |
| NN Basse | 47/57 | 82% | 35 | 2 |
| Madgacen | 67/88 | 76% | 32 | 2 |
| 意美 Hata | 29/55 | 53% | 9 | 2 |

**Eight of the eighteen are complete end to end**, including a **225-step chain
to Enlil-nirari** and the full chain to Temüjin. A 225-step path holding every
single step is not something a peripheral sample produces.

So the answer is **largely yes** — with one specific, nameable hole.

## The headline moved for the wrong reason, so here is the like-for-like

The previous version of this report read *1,095 of 1,227 (89.2%) over 15
chains*, measured over the 186,551-person merge (90 exports). Comparing that to
92.7% would credit eight exports with an improvement they did not make: the
three Makeda chains are new to this table and two of them are complete, so
adding them raises the percentage on their own.

**On the same fifteen chains, the eight new exports moved the figure from
1,095/1,227 (89.2%) to 1,100/1,227 (89.7%).** Five steps. Every one of them is
`意美 Hata`, which went 24/55 → 29/55. Nothing else changed at all.

That is the number to keep. A chain already held end to end cannot improve, and
the eight exports since 2026-08-05 landed somewhere none of these chains run.

## The gaps are not scattered. One block of ten people blocks five paths.

134 steps are missing, spread over 94 distinct people. But **50 of those 134 —
37% — are the same ten people**, each needed by five different paths:

| Geni ID | who |
| --- | --- |
| `6000000001266578142` | **Louis I, The Pious** |
| `6000000001669654269` | Berengar I, emperor of the Romans |
| `6000000000424624719` | Giséle of Cysoing |
| `6000000003715297906` | Hildegard |
| `6000000009025970491` | Emma of Alemannia, duchess of Swabia |
| `6000000005588774140` | Hnabi — Nebi, Duke of Alamannia |
| `6000000005588538629` | Huoching of the Alemannians |
| `6000000006128411604` | Gotfrid, duke of the Alemannians |
| `6000000010011384542` | Leutharis III, duke of the Alemannians |
| `6000000003828107379` | Uncilien, duke of the Alemannians |

Verified absent by profile ID against `out/merged.ged`, not inferred from names.
**Unchanged since 2026-08-05** — the same ten, blocking the same five paths.

This is a contiguous run: the Alemannian ducal line ascending into the
Carolingians. Five paths all run unbroken to **step 34** and stop at the same
person — Louis the Pious's line — then resume once past it.

**That we hold Makeda and Temüjin but not Louis the Pious is the surprising
part.** It says our coverage is not "core versus periphery" in the way one would
guess. The exports have reached deep into several ancient lines while leaving a
hole in the single most-connected region of European genealogy — which is
precisely the region Wikidata already models best, and therefore the region
where reconciliation would pay most per person.

Emma's own explanation for why this hole persists is in `todo.md` § 8 and is not
something any measurement here could have produced: she gains access to a Geni
cluster through *nearby contributions*, and a region already densely covered by
other contributors is one she cannot add a profile to — so she cannot create the
foothold an export needs. The Carolingian hole is a constraint of Geni's editing
model, not of our sampling.

## What to export next, and why it beats the density picks

**Seed an export on Louis I, The Pious `6000000001266578142`, style `Forest`.**

- The payoff is **observed, not inferred**. Every seed in `reports/seeds.md` and
  every region in `reports/density.md` is a bet about material behind a door.
  Here Geni has already told us exactly who is behind it, by name and profile ID.
- **One export plausibly closes all five paths.** The block is ten people in a
  contiguous run, and the measured reach of a targeted export in this repo is
  6–9 steps of chain per take (the Jimmu bridge). Ten is at the edge of that, so
  it may take two.
- **`Forest`, not `Ancestors`.** Giséle of Cysoing and Emma of Alemannia enter
  through marriages; a blood-only style walks past them. This is the same trap
  that nearly cost the Jimmu bridge.

The remaining 84 missing people are singletons on one path each — the Merrell
and Daniels American lines, the Hitotsuyanagi chain and the eight-person 惟宗
stretch that together make 意美 Hata the worst-covered path at 29/55
(`reports/hata.md` has that one in full), and the six behind Mahaut de Poissy on
Makeda → Marguerite. Those are ordinary frontier, not core.

## What this does not say

A path is evidence about **connectivity**, not completeness. Holding every step
of the chain to Enlil-nirari says we have the people who link us to him; it says
nothing about how much of his surrounding family Geni knows and we do not. The
Hata clan is the worked example of exactly that gap: `reports/path-hata.md` says
29 of 55 steps of the *chain* are held, while `reports/hata.md` says the clan
those steps run through is 27 people with no wives and one branch point. A path
held end to end and a family recorded thinly are entirely compatible.

And `genimerge.paths` falls back to name matching only for rows carrying no
profile ID — every figure above is an exact join on the Geni ID, which is why
the Carolingian block can be stated as fact rather than as a likely match.
