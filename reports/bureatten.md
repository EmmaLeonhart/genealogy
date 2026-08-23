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

## The 104 are the best export targets in the repo right now

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
