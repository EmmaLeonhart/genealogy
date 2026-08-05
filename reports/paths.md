# Do we have the small-world core?

Generated from the saved Geni pages in `geni_pages/` — re-run with
`python -m genimerge path-from-html <page> -o paths/<name>.tsv` then
`python -m genimerge path paths/<name>.tsv --source out/merged.ged`.

**Why this is the right instrument.** Raw size cannot answer the question: the
Geni world tree is around 210 million people and this merge holds 186,551, which
is 0.09% of it. But a relationship path is a chain Geni computes *itself*,
naming people whether or not any export has reached them. It is the one piece of
evidence here that comes from outside our own data. If arbitrary chains to
far-flung people are held end to end, we hold the connective tissue — which is
what "small-world core" means operationally.

Measured 2026-08-05 over the 186,551-person merge (90 exports).

## Result

**1,095 of 1,227 steps held — 89.2%**, across 15 independent chains reaching
Assyria, Sheba, Egypt, Numidia, Mongolia, the Jin clan, Malwa, Samaria, Toledo
and Japan.

| path | held | | unbroken run ends | gaps |
| --- | ---: | ---: | ---: | ---: |
| Makeda, Queen of Sheba | 170/170 | 100% | 170 | 0 |
| Emperor Jimmu no Mikoto | 83/83 | 100% | 83 | 0 |
| Lady Palsu of the Jin clan | 60/60 | 100% | 60 | 0 |
| Princess NN | 60/60 | 100% | 60 | 0 |
| Gervasio of Toledo | 42/42 | 100% | 42 | 0 |
| Temüjin Borjigin, Khagan of the Mongol Empire | 36/36 | 100% | 36 | 0 |
| Eleazar II, Samaritan High Priest | 87/97 | 90% | 34 | 1 |
| daughter of the king of Assyria | 81/91 | 89% | 34 | 1 |
| NN of Malwa | 81/91 | 89% | 34 | 1 |
| NN daughter of Berenice | 80/90 | 89% | 34 | 1 |
| NN | 80/90 | 89% | 34 | 1 |
| Psamtik II, Pharaoh of Egypt | 97/117 | 83% | 42 | 2 |
| NN Basse | 47/57 | 82% | 35 | 2 |
| Madgacen | 67/88 | 76% | 32 | 2 |
| 意美 Hata | 24/55 | 44% | 9 | 1 |

**Six of the fifteen are complete end to end**, including a **170-step chain to
Makeda** and the full chain to Temüjin. A 170-step path holding every single
step is not something a peripheral sample produces.

So the answer is **largely yes** — with one specific, nameable hole.

## The gaps are not scattered. One block of ten people blocks five paths.

132 steps are missing, spread over 92 distinct people. But **50 of those 132 —
38% — are the same ten people**, each needed by five different paths:

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

This is a contiguous run: the Alemannian ducal line ascending into the
Carolingians. Five paths all run unbroken to **step 34** and stop at the same
person — Louis the Pious's line — then resume once past it.

**That we hold Makeda and Temüjin but not Louis the Pious is the surprising
part.** It says our coverage is not "core versus periphery" in the way one would
guess. The exports have reached deep into several ancient lines while leaving a
hole in the single most-connected region of European genealogy — which is
precisely the region Wikidata already models best, and therefore the region
where reconciliation would pay most per person.

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

The remaining 82 missing people are singletons on one path each — the Merrell
and Daniels American lines, and the Hitotsuyanagi chain that makes 意美 Hata the
worst-covered path at 24/55. Those are ordinary frontier, not core.

## What this does not say

A path is evidence about **connectivity**, not completeness. Holding every step
of the chain to Makeda says we have the people who link us to her; it says
nothing about how much of her surrounding family Geni knows and we do not. And
`genimerge.paths` falls back to name matching only for rows carrying no profile
ID — every figure above is an exact join on the Geni ID, which is why the
Carolingian block can be stated as fact rather than as a likely match.
