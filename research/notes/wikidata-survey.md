# Wikidata survey: how far does Wikidata connect the Inbe to the gods?

Queried 2026-10-02. Raw results are in `data_lake/downloads/wikidata/`.

## Short answer

Wikidata connects **no historical Inbe person to Futodama**. Every named Inbe
of the 7th–14th centuries in Wikidata has no father recorded. The god layer is
connected (Futodama → Takamimusubi, Futodama's children and grandson), and the
real people are present, but there is no link between the two layers.

The only Inbe-associated person whose Wikidata father chain reaches the gods
is **Inbe (Taira) no Chikazane**, the claimed founder of the Oda clan. His
chain runs through the **Taira and the imperial line**, not through Futodama.
47 generations take him to Izanagi (`father_chains.txt`).

## What is in Wikidata

**The clan item.** Inbe clan is Q8189229 (instance of *uji*). Only two items
carry family (P53) = Inbe clan: Futodama (Q11059539) and Inbe no Hironari
(Q11500712). Source: `inbe_members_P53.csv`.

**The god layer.** Source: `futodama_lineage.csv`.
- Futodama's father is Takamimusubi (Q125400), which has no father recorded.
- Futodama's children: Ame no Iwatowake, Ōmiyanome, Ame no Kushimimi, Kamo
  Taketsunumi, and Ame no Uzume. His wife is Ame no Hiritome (Q85879124).
- Ame no Tomi (Q24899653), who led the Awa Inbe east to Bōsō, is the son of
  Ame no Kushimimi and so Futodama's grandson. This matches the Kogo Shūi
  calling Ame no Tomi Futodama's grandson (to verify in the text, queue item 3).
- Through Kamo Taketsunumi, Futodama's descent passes into the **Kamo** and
  **Katsuragi kuni-no-miyatsuko** lines (Tamayorihiko → Tsurugine), not into
  any Inbe person.
- *Inference, to check:* Ame no Uzume as Futodama's daughter and Kamo
  Taketsunumi as his son look like minority traditions. The usual Kojiki and
  Nihon Shoki texts don't give them that parentage. Each needs its Wikidata
  reference checked.

**Branch-ancestor deities.** Source: `jawiki_inbe_category_items.csv` and
`father_chains.txt`.
- Ame no Hiwashi (Awa Inbe ancestor) → Ame no Tajikarao → Omoikane →
  Takamimusubi. So in Wikidata the Awa branch ancestor is Futodama's
  great-nephew (Omoikane is Futodama's brother, both sons of Takamimusubi), not
  his descendant.
- Ama no Mahitotsu (Tsukushi/Ise Inbe ancestor) → Amatsuhikone → Susanoo →
  Izanagi. This branch ancestor is on a completely different divine line from
  Futodama.

So Wikidata itself shows that the branches aren't one bloodline. Their divine
ancestors sit on separate branches of the god tree.

**Historical people.** Japanese Wikipedia's 忌部氏 category lists these. All
have Wikidata items, none has a father, and none except Hironari has
P53 = Inbe clan.

| QID | Name | Dates in Wikidata | Note |
|---|---|---|---|
| Q11490720 | 忌部子人 Inbe no Kobito | 650?–719 | Jinshin War 672; from 682 a compiler of the imperial chronicles with Nakatomi no Ōshima (ja Wikipedia) |
| Q11490725 | 忌部色夫知 Inbe no Shikobuchi | b. 650? | |
| Q11490721 | 忌部多夜須子 Inbe no Tayasuko | — | |
| Q24874467 | 忌部鳥麻呂 Inbe no Torimaro | — | |
| Q105711606 | 忌部人上 Inbe no Hitokami | — | |
| Q27920470 | 斎部浜成 Inbe no Hamanari | b. 750? | |
| Q11500712 | 斎部広成 Inbe no Hironari | b. 750? | author of the Kogo Shūi (807) |
| Q11500711 | 斎部文山 Inbe no Fumiyama | 822–867 | |
| Q17193839 | 忌部正通 Inbe no Masamichi | — | medieval; *Jindai Kuketsu* attributed to him |
| Q11677504 | 麻植持光 Oe no Mochimitsu | d. 1553 | Awa (麻植 = Oe district, "hemp-planting") |
| Q2502463 | 平親真 / 忌部親真 Chikazane | d. 1260 or 1290 | claimed founder of the Oda and Tsuda clans |
| Q11608365 | 織田常昌 Oda Jōshō | Muromachi | father 織田真昌 (no further) |

忌部百継 (Inbe no Momotsugu) has a Japanese Wikipedia page but no Wikidata
item linked to it.

## The Oda route to the gods

Japanese Wikipedia gives Chikazane as **忌部親真 / 斎部親真**: an Inbe who is
"said to be the ancestor of the Oda and Tsuda clans" (織田氏・津田氏の祖とされ).
Wikidata labels him 平親真 (Taira no Chikazane) and gives his father as Taira
no Sukemori, Kiyomori's grandson. From there the chain is the standard Taira →
Emperor Kanmu → imperial line → Jimmu → Ninigi → Ame no Oshihomimi → Susanoo
→ Izanagi.

*Inference, to verify in queue item 5:* the Taira parentage looks like the
Oda clan's later claim to Taira descent stacked on top of an Inbe shrine-priest
origin. If that is right, Wikidata's only "Inbe to the gods" path is a
genealogy that **replaces** the Inbe ancestry rather than tracing it.

## For the GEDCOM

- The god layer can be imported from Wikidata, with each link checked against
  the primary texts.
- The historical layer goes in as unconnected individuals.
- The Chikazane → Taira link goes in marked as a claimed descent (GEDCOM
  QUAY 0 or 1) with a note.
