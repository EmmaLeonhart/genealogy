# The first `job.create` run: the parent walk from Søren Hansen Hiuler

**2026-09-09.** The first time the collector's live-site write path has been exercised. You:
*"Turn the switch on and watch it."* This is what it did.

## Why he qualified

`373218413260013352` Søren Hansen Hiuler, 1754–d., Herslev, Denmark. Both relationship searches
answered and **both missed** — no blood path and no in-law path to Charlemagne — while his
statistics are large:

    family_tree      1365
    blood_relatives  15000
    ancestors         104
    descendants       144

`individual.js` cleared him on its own: `state: miss_export_warranted`, `export_decision:
"export -- cleared by family_tree, blood_relatives"`. That is the rule in its own comment —
*"15,000 blood relatives or really any of these numbers being high on this scale indicates that
they are in the world tree but it was a database failure"* — so the miss is a Geni query failure
rather than a real disconnection, and an export is the way through it.

## The walk, and it did not terminate

`runSeed` does ONE person and hands back a queue; walking it needs a page load per step, because
agentic navigation is the CAPTCHA mitigation. Every level came back `both_present`, which is
rule 4 of `docs/parent-walk-algorithm.md` — *"both present -> add neither; enqueue the mother,
THEN the father, and carry on up"* — so **nobody was created and nothing was written to Geni.**

Following `enqueue[0]` at each step:

| # | person | born | id | state |
| ---: | --- | --- | --- | --- |
| 0 | Søren Hansen Hiuler | 1754 | `373218413260013352` | both_present |
| 1 | Malene Sørensdatter Koed | c.1735 | `373182827690012954` | both_present |
| 2 | Søren Iversen Koed | 1698 | `311400826980001473` | both_present |
| 3 | Magdalene "Malleene" Mortensdatter Heyring | 1666 | `369853793810012928` | both_present |
| 4 | Giertrud Ravn | 1655 | `4119311448320030565` | both_present |
| 5 | Dorothea Hansdatter From | c.1620 | `6000000000180326569` | both_present |
| 6 | Johanne Bertelsdatter Struck | c.1595 | `4436105144730128270` | both_present |
| 7 | Dorethe Sørensdatter Stage | 1561 | `6000000007980472551` | both_present |

**Still queued at the point of stopping:** `6000000000175785551` Søren Jacobsen Stage and
`6000000007266557325` Anna Sørensdatter Stage, the parents of step 7.

## What the run establishes

* **The mechanism works exactly as written.** The gate fired without any prose judgement from
  the agent, `runSeed` refused to invent a parent where two were recorded, and the queue came
  back for the agent to walk. No discretion was applied and none was needed.
* **⛔ THE WALK IS THE COST, and it is unbounded from the top.** Eight levels, ~17 tool calls,
  no open slot, and no way to know from the start how deep the line runs. This is a Danish
  clerical and gentry line recorded continuously to 1561; the `6000000…` ids from step 5 onward
  say those people are in the main World Tree.
* **The two facts sit oddly together and that is the interesting part.** His ancestry is recorded
  eight generations deep into the World Tree, and Geni still cannot find a path from Charlemagne
  to him. That is the database failure the floor rule predicts, seen directly.

## What has NOT happened

No profile created, no export submitted, nothing written to Geni. The walk stopped by choice to
put the cost to you rather than spend the session on it.
