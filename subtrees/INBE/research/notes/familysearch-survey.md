# FamilySearch survey

Accessed 2026-10-02 through the user's signed-in account (Claude in Chrome,
FamilySearch tree API called from the page). Data:
`data_lake/downloads/familysearch/inbe_father_line.csv`.

## Short answer

FamilySearch has **a 14-generation Inbe father-line**, which Wikidata lacks. It
runs from Inbe no Hamanari (8th century) down to Inbe no Chikazane (d. 1260),
the claimed Oda founder. **It stops at Hamanari.** Hamanari has no parents in
the tree, so it does not reach Futodama or any god. Every link above Chikazane
has **zero sources** attached.

## The chain (top to bottom)

1. 斎部浜成 Hamanari (L286-81J), no parents in the tree
2. 斎部広成 Hironari (L286-827), the author of the Kogo Shūi (807); born 726 on FamilySearch
3. 斎部明成 Akinari
4. 斎部伴主 Tomonushi (reading not given on FamilySearch)
5. 斎部文山 Fumiyama (822–867); a historical court Inbe, also in Wikidata
6. 斎部季長 Norinaga (as romanised on FamilySearch)
7. 斎部茂藤 Shigefuji
8. 斎部春光 Harumitsu
9. 斎部頼友 Yoritomo
10. 斎部頼成 Yorinari
11. 斎部頼親 Yorichika
12. 斎部親光 Chikamitsu (FamilySearch also gives "OTA", i.e. Oda/Ōta)
13. 忌部/斎部親澄 Chikazumi
14. 忌部/斎部親真 Chikazane (1184–1260). Parents on FamilySearch: Chikazumi,
    *and* Taira no Sukemori, *and* "Tsuda Gōchō", *and* a niece of the ajari
    Shinkai. Its one source is a legacy "Family genealogies" entry titled
    忌部 又は 平親眞 ("Inbe or Taira Chikazane").

A duplicate profile, INBE CHIKAZUMI (GN46-T6S, b. ~1200), lists TAIRA
CHIKAZANE (GN46-R55) as a child, so two separate copies of this line exist in
the tree.

## How far to trust it

- *Inference:* the chain has the shape of a family-tradition pedigree. It
  looks like the kind of Inbe line the Oda or the Tsurugi Shrine priests would
  have kept to explain their descent, copied into FamilySearch without
  citation. The source behind it needs to be found (NEEDS-INVESTIGATION,
  queue).
- Chronology warning: FamilySearch makes Hamanari Hironari's father, but
  Wikidata gives both a birth year around 750, and FamilySearch dates Hironari to 726.
  Whether Hamanari was Hironari's father, brother or unrelated needs a primary
  source (Shoku Nihongi, Nihon Kōki).
- Four generations (Hironari → Fumiyama) cover roughly 726 to 822, about
  24 years per generation. That's plausible. Eight generations from Fumiyama
  (b. 822) to Chikazumi (fl. ~1180) is about 45 years each, which is too long.
  Generations are probably missing or invented in the middle of the chain.

## What this means for the question

The best "Inbe to the gods" account found so far, in either database:

- FamilySearch: real Inbe → back to Hamanari (8th c.), then nothing.
- Wikidata: the god layer down to Ame no Tomi, then nothing.

The gap between Hamanari and Futodama is where a documented chain would have
to be. No source for it has turned up yet.

## Source of the line (found 2026-10-02)

Japanese Wikipedia's 斎部文山 article gives "father: 斎部伴主, son: 斎部季長" and
cites **中田憲信「織田右大臣信長公ノ系統及履歴」, 『好古類纂』 vol. 7**. That is
a Meiji-period account of Oda Nobunaga's ancestry by the genealogist **Nakata
Norinobu**. The 平親真 article gives the end of the same chain: Chikazane is
the son of **忌部親澄 Chikazumi, 神祇権大祐** (assistant official of the Jingikan).
The mainstream Oda pedigree (「織田系図」, 『続群書類従』 vol. 142) instead
makes him Taira no Sukemori's son, later adopted by Chikazumi.

So the FamilySearch line is **Nakata Norinobu's reconstruction of Nobunaga's
Inbe ancestry**: Hamanari → Hironari → … → Fumiyama → … → Chikazumi →
Chikazane → Oda.

- **Confirmed:** Nakata Norinobu (1835–1910) was a Hirata-school kokugaku
  scholar and the "fellow student and ally" (同学の士で盟友) of **Suzuki
  Masatoshi** (1831–1894), the man Kosugi named as forger of the Ono
  honkeichō. Hōga Toshio, whose 1986 『古代氏族系譜集成』 Japanese Wikipedia also
  cites, revived and drew on both men's collections (ja Wikipedia 鈴木眞年 and
  宝賀寿男; NDL Reference 1000090125). So **every multi-generation Inbe chain
  found so far traces back to the same Meiji circle.**
- **A conflict with a primary source:** the 『日本三代実録』 entry for Fumiyama's
  death (Jōgan 9.4.4, 867) says he was **of humble birth** (身分の低い出自,
  as Japanese Wikipedia summarises it) and known for his craft skill. He repaired the head of the Tōdaiji
  Great Buddha. The Nakata pedigree makes him the son of a **Jingi Taifu** (vice-head of the
  Jingikan). Those don't fit together.
- **Correction (2026-10-03): the Hōraku-ji stone is not independent evidence
  for Chikazane.** The 2011 announcement (Nikkei, 2011-11-04) treated a
  five-ring stupa at Hōraku-ji, Echizen town, as Chikazane's tomb. The town's
  own survey report (『広報えちぜん』 Sept. 2012, pp. 2–3, saved as
  `data_lake/downloads/echizen/koho_echizen_2012-09_horakuji.pdf`) concluded
  that the inscription reads **喪親尊阿聖霊／正應三年庚刀二／月十九日未尅**.
  That makes it the grave of a man called **親尊 (Chikataka)** who died on the 19th day
  of the 2nd month of Shōō 3 (1290), around 2 pm. It is **not 親真**. The report
  suggests the stone, which is easily misread as 親真, may have been a model
  when the Oda pedigrees were drawn up.
- What the same report says about the Oda pedigrees:
  - Oze Hoan's 『信長記』 (c. 1611) has the Taira story (Sukemori's pregnant
    concubine fleeing to Tsuda in Ōmi; the child adopted by the Tsurugi Shrine
    priests) but **does not name Chikazane**.
  - **Chikazane first appears in Hayashi Razan's 『織田信長譜』** (commissioned
    1641, published 1658), on Taira lines.
  - The 『続群書類従』 「織田系図」 (c. 1692) has Chikazane as Sukemori's son.
  - **The Oda's own "Inbe pedigree"** (織田氏、忌部氏説の系譜) says Chikazane's
    father was **忌部(斎部)親澄**, his mother a daughter of 平基度 (Ise Heishi),
    that he became priest of Oda Myōjin in Jōei 2 (1233), took the Buddhist
    name 覚盛, and died on Shōgen 2.2.18 (1260). It says explicitly
    "平氏にあらず、忌部神主の正系なり" ("not Taira, but the direct line of the
    Inbe priests"). FamilySearch's dates for Chikazane (d. 1260) and his father
    Chikazumi match this pedigree.
  - Nobunaga himself signed as "Fujiwara Nobunaga" at 16 and claimed Taira
    descent in the 1570s.
- So Chikazane's Inbe identity rests on **a family pedigree of uncertain date**,
  not on the stone. Chikazane is not attested earlier than 1641 at all.