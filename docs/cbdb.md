# The CBDB people: not a dead end, and the missing piece is kinship that was never imported

Ruled 2026-09-15 from `queue.md` section *CBDB people*:

> *"My current working hypothesis is that these people all have the geni tree 100% present on
> wikidata due to the mass export coming from some external gedcom. So for the people for which we
> are not able to add ancestors, do not be too concerned with it. I think this might be a better
> thing to investigate using other things like familysearch and geni is just kinda a dead end there
> and wikidata has all of the geni information already for it. But searching the web for these
> things may be helpful so do it."*

## The hypothesis was right about Geni and about the data, and wrong about nothing

**Geni is a dead end and that is settled.** The profiles are managed by `CBDB (China Biographical
Database)`, carry no `Add Family` link and are not editable, which is why 54,164 were parked at
`2026-10-31`. Nothing here changes that; not being concerned about them was correct.

**And they are not data-poor on Wikidata.** Measured 2026-09-10 over `reports/cbdb-route.tsv`:
**49,339 of 71,474 (69%) already carry `P22`/`P25`/`P40`/`P3373`**, in exactly the shape a
patrilineal Chinese source produces — `P22` 20,157, `P22,P40` 18,706, `P40` 6,620.

## The standing hypothesis about WHY they stay disconnected is REFUTED

`devlog.md` 2026-09-10 left one, explicitly as a hypothesis and explicitly queued rather than
assumed:

> *"a Tang-dynasty father-son lattice is connected to itself and disjoint from the European royal
> graph that the campaign measures against ... If it holds, the CBDB question is ... answered ...
> and they are done rather than parked."*

**It does not hold.** Over `out/wikidata/relations.tsv` — 1,800,688 people, 3,349,534 edge
endpoints — Charlemagne's component holds **1,549,441 people, and 23,137 of the 71,469 CBDB items
(32%) are inside it.**

**The bridge is the Golden Horde, and the path is real.** The shortest runs 20 steps:

    Q3044      Charlemagne
    Q299645    Pepin of Italy
    Q333319    Bernard of Italy
    Q559062    Pepin I, Count of Vermandois
    Q961145    Herbert I, Count of Vermandois
    Q76300774  Cunegonda of Vermandois
    Q100906    Herbert of Wetterau
    Q3198477   Gerberga
    Q63607     Otto III
    Q80934446  Gisela of Schweinfurt
    Q96566     Berthold II, Count of Andechs
    Q68632     Berthold I of Istria
    Q61454     Berthold IV, Duke of Merania
    Q61491     Gertrude of Merania
    Q152370    Béla IV of Hungary
    Q737328    Constance of Hungary, Queen of Galicia
    Q12086698  Agrippina
    Q297295    Yury of Moscow
    Q4231919   Konchaka
    Q335097    Öz Beg Khan
    Q45678941  Tuogulieer

`Konchaka` is the hinge — a Mongol princess who married `Yury of Moscow` — and the route
Europe → Rus' → Golden Horde → Yuan is ordinary, well-documented history rather than a bad edge.

**So `confirmed impossible` does NOT apply and they must not be closed as such.**

## The worklist is correct, checked rather than trusted

**0 of the 23,137 connected CBDB people appear in `reports/unconnected-p2600.tsv`.** The worklist
and this measurement agree completely: it already excludes every one of them.

## What the remaining 48,332 actually are, and it is not one lattice

    CBDB items                               71,469
    reach Charlemagne                        23,137   32%
    do not                                   48,332   68%
      ... and they fall into            25,169 separate components
      ... of which SINGLETONS                20,133   no family edge at all
      largest disconnected components   518, 504, 287, 163, 152, 145, 136, 133

`reports/cbdb-connectivity.csv` is one row per item.

**20,133 people with no family edge whatever is not a connectivity problem, it is an absence.**
There is nothing to traverse. No amount of work on the Wikidata side connects a person who has no
recorded relative, and Geni cannot supply one because Geni is shut.

## The web search Emma asked for found the cause, and it is clean

The Wikidata CBDB import — `Wikidata:WikiProject East Asia/China Biographical Database import` —
took **basic biographical data only: gender, dynasty, English name.** Over 300,000 records were
matched through Mix'n'Match. **Kinship was never part of it**, and the project page does not
mention family relationships at all.

Meanwhile **CBDB itself holds 482,953 kinship records** across roughly 657,909 people (May 2026),
with a notation precise enough to distinguish a father's brother's son from a mother's brother's
son. The database is freely downloadable.

**So the 20,133 empty items are empty because nobody imported the half of CBDB that has the
families in it** — not because the families are unknown.

**The join key already exists and costs nothing**: `CBDB ID` is `P497` on Wikidata, and
**69,516 of our 71,469 items (97%) carry the CBDB person number in their English description**
(`Yao Shu` — *Yuan dynasty person CBDB = 27889*), so `reports/cbdb-items.tsv` is already joinable
against a CBDB download with a regex.

## ⛔ AND THE IMPORT IS NOT OURS TO DO

Recording the route is not proposing it. A CBDB kinship import is a **mass, non-local edit** over
tens of thousands of items with no relation to the Bure kinship — the exact shape
`CLAUDE.md` § *ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT* exists to
forbid, and the exact shape of *"I don't want to draw more attention than I've been getting from
being non-local."* It is also somebody else's project: the WikiProject that did the biographical
import is where kinship belongs.

**What this closes:** the CBDB people are neither a dead end nor confirmed impossible. A third of
them are already connected, the worklist is right about all of them, and the remainder is waiting
on a data import that is not this repo's to make.
