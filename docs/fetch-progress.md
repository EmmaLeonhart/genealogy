# Where the RootsMagic fetch has got to (2026-10-10)

Method, per Emma (pc-manager chat, 15:33): RootsMagic person IDs run roughly in fetch order, a
breadth-first search out from Abul Hamza (I1, then his wife, father, mother, daughter, grandparents
…), with an odd tail of some very recent people. So the newest IDs are the frontier, and diffing two
snapshots shows who was just fetched. Script: `scripts/offline/fetch_progress.py`. "Hops" = steps
from Abul Hamza over parent, child and spouse links.

## 14:43:58 → 15:37:47 snapshot

- 163,942 → 165,402 people: **1,460 added**, IDs 163943–165402.
- **Birth years of the added:** 1,394 dated; 1850–1899: 663, 1900–1949: 688, 1800–1849: 19,
  1600–1649: 18, 1550–1599: 5, 1500–1549: 1. Median 1899, range 1523–1947.
- **Hops from Abul Hamza:** 1,435 at 21, 25 at 22.
- **Birthplaces:** Brazil 1,084 (mostly Paraná: Guarapuava, Laranjeiras do Sul, Ponta Grossa),
  Russia 19, a handful elsewhere.
- **Frontier (last IDs):** the Natel de Camargo, Pereira and Hilgenberg families of Paraná, born
  1880s–1930s.

## The ring people and the home regions

- **Ring people:** none of Pfinzing, Güntersberg / Guntersberg (Inger Axelsdatter), "Axelsdatter"
  or Rømer occurs anywhere in the 165,402-person file. The fetch has not reached them.
- **Born in Östergötland, Rogaland or Västerbotten:** 17 people, all nobility or royalty reached
  through princely lines (Johan III Vasa at Stegeborg, hop 18; Pfalz-Zweibrücken children at
  Stegeborg, Lewenhaupt at Charlottenborg, Natt och Dag, Snakenborg, Wrangel, hop 21–22), plus one
  Stavanger man, Lauritz Lauritzsen Rasch (1607, hop 22). None of them is a low-generation farm
  family of the kind Emma's own lines come through.

## Reading

The search is now at hops 21–22, and at this moment it is spending itself on the 19th- and
20th-century descendants of a few Brazilian families. Her continental links (the ring people in
Germany and France) are not in the file at all, so the fetch is still well short of them. On
Emma's test ("really good evidence of ... ties to Östergötland or to Rogaland", or proof that the
continental links are well past the frontier): neither holds yet. The links are not reached, and
the home-region people present are princely, not the recent low-generation people that would
show a tie.
