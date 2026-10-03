# Shinsen Shōjiroku (815): what the official clan register says

Text used: the clan-by-lineage reorganisation at
<https://www.eonet.ne.jp/~temb/7/shoziroku.htm> (accessed 2026-10-02; grep
hits saved in `scratch/`). Entries quoted as that page gives them. *To check
against a critical edition (Saeki Arikiyo's 『新撰姓氏録の研究』).*

## The Inbe entry: no generations at all

- **齊部宿祢**, 右京神別上: "高皇産霊命子、天太玉命之後". In English, "descendants of
  Ame no Futodama, child of Takamimusubi."

That's the whole official statement of Inbe descent in 815. It names the
ancestor god and gives no generations and no intermediate names. Many other
clans in the same register give counts like "fifth-generation descendant of…"
or "eighth-generation descendant of…".

## Ame no Hiwashi: the register disagrees with itself

| Clan | Section | Statement |
|---|---|---|
| 弓削宿祢 | 左京神別下 | 高魂命孫、天日鷲翔矢命之後: Hiwashi is **Takamimusubi's grandson** |
| 弓削宿祢 | 河内国神別 | 高御魂乃命孫、天毘和志可気流夜命之後: same |
| 多米宿祢 / 多米連 | 右京・左京・摂津 | 神魂命五世孫、天日鷲命 (天比和志命): **Kamimusubi's 5th-generation descendant** |
| 田辺宿祢 | 大和国神別 | 同神五世孫、天日鷲命: same |
| 天語連 | 右京神別上 | 県犬養宿祢同祖、神魂命七世孫、天日鷲命: **Kamimusubi's 7th-generation descendant** |

So in 815 Hiwashi's ancestry was already given three different ways.

## Ame no Kushimimi is not Futodama's son here

- **日置部**, 未定雑姓 和泉国: "天櫛玉命男天櫛耳命之後". In English, "descendants of Ame no
  Kushimimi, son of **Ame no Kushitama**."

Wikidata cites the Shinsen Shōjiroku for "Futodama → child Ame no Kushimimi".
That only works if 天櫛玉命 Kushitama is taken to be Futodama. The Ono
honkeichō makes exactly that equation: it gives 玉櫛比古命 as an alias of
Futodama. *Inference:* the Wikidata statement depends on the Ono pedigree's
identification, not on the 815 text as written.

## How the Ono honkeichō was built from this register

The honkeichō (`genealogy/ono_inbe_honkeicho.csv`) attaches branch notes to
its generations. They match Shinsen Shōjiroku entries one for one:

| Honkeichō entry | Shinsen Shōjiroku entry |
|---|---|
| 古佐麻豆知命, "ancestor of the 泉之穴師 shrine priests" | 穴師神主 (和泉国神別): 天富貴命五世孫、古佐真豆智命之後 |
| 葉耳命, "ancestor of the 日置部" | 日置部 (未定雑姓和泉): 天櫛玉命男天櫛耳命之後 |
| 意保熊命, "ancestor of the 白堤首" | 白堤首 (大和国神別): 天櫛玉命八世孫、大熊命之後 |
| 古止祢, "ancestor of the 小山連" | 小山連 (摂津国神別): 高魂命子、櫛玉命之後 |
| The Hiwashi line: 神魂命 → 角凝魂命 → 天底立命 → 五十狭布魂命 → 伊加志保魂命 → 天背男命 → 許登能麻遅命 → 天日鷲命, which makes Hiwashi **seventh** from Kamimusubi | 天語連: 神魂命**七世孫**、天日鷲命 |

*Inference, strong:* the compiler took the "Nth-generation descendant of god X"
counts scattered through the 815 register and filled in names to make the
counts come out. The Hiwashi line is the clearest case, with exactly seven
steps to match 天語連's "seventh-generation descendant". Ame no Tomi to 古佐麻豆知 comes out
at about the "fifth-generation descendant" of the 穴師神主 entry. That is how
a genealogist who knew the sources well, as Suzuki Masatoshi did, would
assemble a complete-looking pedigree out of separate clan claims. It fits
Kosugi's 1876 account of Suzuki "rearranging" lines.

## What this means for the user's question

The oldest official source, from 815, gives the Inbe a divine ancestor and
**no chain**. The chains appear only in the 1870 pedigrees, and the most
complete one can be seen being assembled from the register's own fragments.
