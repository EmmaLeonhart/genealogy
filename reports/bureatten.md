# Bureätten: who is covered, who is not

Emma's queue item: *"run exports to get a good account of the Bure Kinship... Check to
make sure all members of the category are covered, since I think they are all on geni and
can be highly linked up, all of them should have geni exports on them if they are unlinked
and we check for those whose wikidata items do not connected geni ids similar to Samaritan
high priests"*.

Source: <https://sv.wikipedia.org/wiki/Kategori:Bure%C3%A4tten>, read 2026-08-22 —
**576 pages, 575 carrying a Wikidata item.** One MediaWiki category call plus pageprops;
the Wikidata side is entirely offline against `out/wikidata/store-index.sqlite3` and
`out/merged.ged`.

## The four groups

| | pages |
| --- | ---: |
| **person, has a Geni ID, in our corpus** | **147** |
| **person, has a Geni ID, NOT in our corpus** | **104** |
| person or probable person, Wikidata item but **no Geni ID at all** | **199** |
| family / clan / noble-house articles, not people | 126 |
| no Wikidata item (`Munck af Sommernäs`) | 1 |

The 126 are `(släkt)`, `(adelsätt)`, `(friherrlig ätt)` and bare-surname articles — Bure
(adelsätt), Rosenblad, Sprengtporten and so on. They are houses, not humans, and are not
work.

## CONNECTIVITY IS NOT THE PROBLEM — measured 2026-08-22

**All 147 Bureätten people already in the tree sit in ONE connected component**, the same
1,274,287-person component as everything else. `scripts/measure-bure-connectivity.py`.

Emma's framing was *"we're just trying to connect them to each other... We're not trying
to run a gigantic export on all of them"*, and the answer is that they already are. The
work is **coverage**, not joining.

That kills the plan this report originally implied — one export per target, ~26 sweeps —
which was being set up when the measurement was taken. Two exports had run; the second was
abandoned unsubmitted.

**The cheap route for the unlinked is Google, not exports.** `site:geni.com "<name>"`
returns the profile directly, with dates and relatives, and no upsell — confirmed working
on `Anders Grubb`. `docs/export-seed-rules.md` already names this as the sanctioned
substitute and only warns it fails for *freshly created* profiles; these are long-standing
historical ones. Geni's own search stays banned.

## The 104 remain the targets, but for coverage not connection

They have a Wikidata item **and** a Geni profile ID, and the profile is simply not in any
of our 547 exports. Nothing has to be guessed: the person exists on both sides, the join
already resolves, and an export puts them in the tree.

`reports/bureatten-export-targets.tsv` lists them with a `family-tree/index` URL each.
The head of it is not obscure — Adolf Erik Nordenskiöld (`Q156749`), Christopher Jacob
Boström (`Q821990`), Baltzar von Platen, Charlotta Aurora De Geer, Carl Reinhold Sahlberg.

**This is a different proposition from the sparse-region and presence-contrast work, both
of which were refuted the same day.** Those picked seeds by a heuristic about where
material *might* be. This is a named list of people known to exist on Geni and known to be
absent here. The failure mode of the refuted methods — exporting into an exhausted
neighbourhood — cannot apply, because the target is a specific person rather than a
region.

## The 199 are the Samaritan pattern

They have a Wikidata item and **no `P2600`**, so no query in this repo can connect them to
Geni even if the profile exists. This is the shape Emma pointed at: *"those whose wikidata
items do not connected geni ids similar to Samaritan high priests"* — present on both
sides, joined on neither.

**85 of the 199 are not in the local Wikidata store at all**, which is itself the
evidence: the store was seeded from `P2600` holders and their neighbours, so an item with
no Geni link and no linked neighbour never entered it. Their `P31` is therefore unverified
here and the report calls them *unknown* rather than asserting they are people; every one
of the 85 carries a personal name.

Finding their Geni profiles is not something this repo can do offline, and Geni's own
search is banned. The route is the tree: export from the 104 first, then re-run this join
— many of the 199 will be pulled in as relatives of people we now hold, and their Geni IDs
will arrive with them.

## Files

- `reports/bureatten.csv` — all 576 pages: title, QID, kind, Geni IDs.
- `reports/bureatten-export-targets.tsv` — the 104, ready to open.


## The 198 unlinked: Google works but cannot be automated naively

Searching `site:geni.com "Adolf Ludvig Piper"` returns real Geni profiles with no upsell,
so the route Emma named does work. **But the top hit is the wrong man.** He is
*Adolf Ludvig Piper, till Ängsö* on Geni, so his own page does not match the plain name,
while he appears constantly inside other people's pages as *"son of"* and *"brother of"*.
The first result is **Axel Adolf Piper**, his son. Taking the first hit would be exactly
the name matching this repo refuses everywhere else.

So Google is for confirming a candidate a human or a structural walk has already picked,
not for generating one.

## The structural route reaches 83 of the 198, offline

`scripts/measure-bure-structural-anchors.py`. A person's Wikidata item names their
parents, spouse, children and siblings. Where one of those relatives already carries a
`P2600` we hold, the unlinked person sits in a **known position beside a known Geni
profile** — and the Geni side of that position is the candidate. Structure picks the pair;
the label only checks it is not absurd. That is `CLAUDE.md` § *Merging the two trees is a
walk up the relationships*.

| | count |
| --- | ---: |
| unlinked non-family articles | 198 |
| in the local Wikidata store (so their relations are readable offline) | 114 |
| **have ≥1 relative already carrying a Geni ID** | **83** |
| of those, anchored by 3+ relatives | 24 |

Adolf Ludvig Piper is the worked example of why this beats the search: his item gives
`P22` → Carl Fredrik Piper (Geni `6000000001883008064`), `P26` → Sophie Piper
(`1551393`), `P40` → a son (`6000000002787896786`). Three independent anchors, all
already in our tree. The Geni person who is *son of that father and husband of that wife*
is him, and no name was consulted to say so.

**Not yet done:** walking those anchors into our merged tree to name the candidate on the
Geni side, and deciding what counts as confirmation when two anchors disagree. That is
the next step, not this measurement.

**The other 115** have no anchor — 84 are absent from the local store entirely, which is
itself the signal, since the store was seeded from `P2600` holders and their neighbours.
Those are the genuinely disconnected ones and Google plus a human eye is the only route.


## The anchor walk, run 2026-08-23 — and what confirmation actually needs

`scripts/resolve-bure-anchors.py`. Each anchor inverts to a position on the Geni side —
their `P22` means *child of*, their `P40` means *parent of*, `P26` *spouse of*, `P3373`
*sibling of* — and the tree is asked who stands there. **Confirmation is intersection**:
one person present in every anchor's candidate set.

**Intersection alone produced four wrong matches out of seven.** It "confirmed" Olof
Kolmodin den yngre as *Johanna Helena Dahl* and Hans Fredrik Harald Strömfelt as *Brita
Lovisa Strömfelt*. A position holds several people — siblings above all — and the
intersection collapsing to one only means the others were already claimed by some other
Wikidata item, not that the survivor is the right person.

So a **sanity gate** follows: sex must agree and the first given token must match. This is
what `CLAUDE.md` means by reading the label to check the pair is not absurd — the
structure still chooses, the gate only rejects.

| verdict | count |
| --- | ---: |
| CONFIRMED — two or more anchors agree, gate passed | 3 |
| single-anchor — one anchor, gate passed, unverified | 3 |
| **rejected by the gate** | **6** |
| ambiguous — intersection holds several people | 33 |
| anchor not reachable in our tree | 38 |

**The three confirmed:** Adolf Ludvig Piper → `6000000006127557407`, Hedvig Catharina von
Fersen → `6000000001515228463`, Johan Magnus af Nordin → `6000000012734285538`.

### The gate is too strict in one direction, and that is left as it is

`Jacob Nils Tersmeden` was rejected against `Jakob Nils Tersmeden` — *jacob* vs *jakob*.
That is almost certainly the same man and the gate is wrong about him. It is **not** being
loosened: relaxing the comparison to absorb c/k is fuzzy name matching arriving by the back
door, and this repo deleted a whole module for that. Six rejections is a small enough pile
for Emma to eyeball, and the row keeps its reason so she can see exactly what the machine
objected to.

`Hedvig Catharina von Fersen` → `Hedvig Catharina Charlotta De la Gardie` passed the gate
on given name and sex but the surname differs. For a woman that is an ordinary married
name, and it is recorded as confirmed on the structure — but it is the one of the three
worth a human glance.

### Where the remaining 71 stand

**33 ambiguous** — the intersection holds more than one person. More anchors would cut
these; most have only one or two.

**38 with no anchor reachable in our tree** — the related Geni profile carries an ID we do
not hold, so there is nothing on our side to stand beside. These need coverage first, which
is what the 100 uncovered targets are for.
