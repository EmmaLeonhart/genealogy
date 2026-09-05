# Eccentric CLUSTERS in the synoptic tree

**Emma, 2026-09-05:** *"You found a bunch of Chinese ancient people were most eccentric… I want to see other eccentric clusters"*.

`reports/eccentricity.md` ranks people, and the top of that ranking is one descent — six people on a single chain. A ranked list cannot show a second group, because everything near the top is the same lineage.

**This cuts the tail at a distance from Charlemagne and finds the connected components of what is left.** Each component is a family that is far from the centre *together*. The threshold is swept rather than chosen — one cut is a choice about the answer.

`reports/eccentric-clusters.tsv` carries every cluster at every cut; this names the largest 12 per cut. `reports/eccentric-cluster-members.tsv` carries every member of every cluster, so a description can be checked rather than believed.

## ⛔ `P2600 linked` DOES NOT MEAN WIKIDATA HAS THEM

**Emma, 2026-09-05, on the first version of this report:** *"your measurement of there being qids is a bit flawed. Both Chinese lines likely have wiki data items even if no connection… Pre dynastic Egypt definitely does… Axum certainly have qids lol… Third intermediate period def has qids lol"*.

**She is right, and the column was mislabelled rather than miscounted.** It counts a `P2600` *Geni.com profile ID* — somebody having **linked** a Geni profile to a Wikidata item. Scorpion I, Makeda Queen of Sheba and Scheschonq all have items; not one has a `P2600`, so the cluster reads `0` and the first version of this report said *"every other cluster is 0"* as though that were a fact about Wikidata's content.

**So a `0` here means UNLINKED, and nothing more.** `CLAUDE.md` § *"Is X present?"* is the standing rule: our Wikidata store is a Geni-shaped slice, so absent-from-it never means absent-from-Wikidata, and every absence has to carry the store it is about. The column is now named for what it measures.

**What it is genuinely good for is the opposite reading.** An eccentric cluster with a high link count is one we have already reconciled; one at `0` is unreconciled, and whether that is because the items do not exist or because nobody joined them is the question a live check answers and this file cannot. `reports/eccentric-cluster-candidates.tsv` is that check, one row per candidate with the evidence to judge it -- and a search hit is a CANDIDATE, never an identification.

## Rope or ball — `per hop` and `deg≤2` say which, and they are different findings

**Emma, 2026-09-05:** *"there's a bit of fuckery that geni enforced with its bible ban that we can undo, although the exact way isn't 100% clear"*. Tracing one cluster shows the shape of it, and the shape is measurable for all of them.

**The 153 hops from Charlemagne to `Solomon King of Israel` (`6000000210521125824`) are a ROPE.** The route runs Charlemagne → Louis the Pious → the Italian and Byzantine houses → the Ethiopian royal line, and then **about 120 consecutive Kings of Axum at degree 2** — each recorded only as the son of the last, no siblings, no spouses, no branches. Every generation adds a hop because there is nothing else to add.

**So that cluster is not kinship-remote; it is a succession LIST entered as a chain.** It spans 54 hops with 61 people — **1.1 people per hop, 80% of them degree ≤2**. Compare cluster 1 at the same cut: 1,524 people over 84 hops, **18.1 per hop**, which is a genuinely wide family that happens to sit a long way out.

**And the bible ban is visible in where the rope does NOT attach.** `Solomon King of Israel` exists **once** in the corpus, at 153. The medieval Jewish lines — `Shlomo ben David Ibn Yahya`, `Shlomo Ha-Zaken ben Yosef`, dozens of them — sit at **26–28** hops, and nothing in the corpus lies between 75 and 152. `CLAUDE.md` § *A second Geni ID on one Wikidata item is NOT a conflict* records the mechanism: Geni forbids connecting biblical people to living people, so users **create fresh biblical profiles** and attach to those. The gap is what that rule does to the graph.

**Two clusters with the same distance are therefore not the same finding**, and an export or a reconciliation buys different things in each. A ball is a population; a rope is one list, and closing it end to end changes one number.

## At least 60 hops from Charlemagne

**20,672 people in 828 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 4,865 | 60–183 | 39.2 | 67% | 62 | 譚 10% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 1,987 | 60–79 | 99.3 | 65% | 0 | 邱 21% 曾 15% khoo 10% | (private) | (private) | (private) | (no label) | (private) |
| 3 | 1,413 | 60–129 | 20.2 | 57% | 11 | egypt 26% pharaoh 10% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 4 | 827 | 60–63 | 206.8 | 59% | 0 | zerbib 14% guedj 11% | (no label) | (no label) | (private) | (private) | (private) |
| 5 | 530 | 60–78 | 27.9 | 77% | 0 |  | Degnai Akeletzion | Guzay TeKletzion | TSinAi Akeletzion | Akeletzion MaluK | Hanis Hadgay |
| 6 | 455 | 60–94 | 13.0 | 53% | 0 | 曾 50% zēng 27% surname 12% | (private) | (private) | (private) | (private) | (private) |
| 7 | 427 | 60–78 | 22.5 | 74% | 1 | 黄 24% wong 22% <private> 12% huang 10% | (private) | (no label) | (private) | (private) | (private) |
| 8 | 381 | 60–88 | 13.1 | 62% | 0 | bhattacharya 19% | (private) | Ojus Sharma | Rajeev Sharma | Rashmi Atray | Sandeep Sharma |
| 9 | 365 | 60–69 | 36.5 | 75% | 0 | chin 13% | (private) | (private) | (private) | (private) | (private) |
| 10 | 324 | 60–168 | 3.0 | 85% | 18 | samaritan 69% itamar 36% line 36% generation 35% priest 34% high 33% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 11 | 256 | 60–63 | 64.0 | 58% | 0 | ghrenassia 10% | (private) | (private) | (no label) | (no label) | (no label) |
| 12 | 242 | 60–70 | 22.0 | 68% | 0 | chén 57% 陳 39% | Bóchāng Chén | Chén Bǐngdé 陳炳德 | Chén Chéngjiù 陳成就 | Chén Chéngyuán 陳成元 | Chén Déchéng 陳德成 |
| … | | | | | | | 816 more clusters in the TSV |

## At least 70 hops from Charlemagne

**10,603 people in 365 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 4,283 | 70–183 | 37.6 | 66% | 51 | 譚 12% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 1,138 | 70–129 | 19.0 | 55% | 5 | egypt 30% pharaoh 11% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 3 | 499 | 70–79 | 49.9 | 70% | 0 | neo 21% see 13% lee 11% tan 10% | (private) | (private) | (private) | Agnes Kim Lwi TAN | Alfred Siew Sin TAN SSM SPMS JP |
| 4 | 378 | 70–78 | 42.0 | 75% | 1 | wong 25% 黄 15% | (private) | (no label) | (private) | (private) | (private) |
| 5 | 317 | 70–79 | 31.7 | 67% | 0 | khoo 26% 邱 13% | (no label) | (private) | (private) | (private) | (private) |
| 6 | 293 | 70–168 | 3.0 | 84% | 18 | samaritan 69% itamar 40% line 39% generation 39% priest 31% high 30% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 7 | 281 | 70–94 | 11.2 | 51% | 0 | 曾 25% zēng 24% hong 10% | (private) | (private) | (private) | (private) | (private) |
| 8 | 228 | 70–79 | 22.8 | 58% | 0 | 邱 23% | (no label) | (no label) | (no label) | (no label) | (no label) |
| 9 | 158 | 70–79 | 15.8 | 71% | 0 | <private> 34% wong 30% 黃 18% | (private) | (private) | (private) | (private) | (private) |
| 10 | 151 | 70–89 | 7.5 | 69% | 1 | ben 14% exilarch 11% ibn 11% | Addai | Andronikos | Assia | James 9th Apostle | Judas |
| 11 | 146 | 70–79 | 14.6 | 65% | 0 | 曾 21% zēng 15% | (private) | (private) | (private) | (private) | (private) |
| 12 | 137 | 70–79 | 13.7 | 57% | 0 | 邱 41% khoo 20% qiū 19% 曾 16% | (private) | Gaik Choo KHOO | Gaik Kim KHOO 邱 | Hong Cheng KHOO 邱 | Hong Chow KHOO |
| … | | | | | | | 353 more clusters in the TSV |

## At least 80 hops from Charlemagne

**5,443 people in 119 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 2,742 | 80–183 | 26.4 | 66% | 14 | 譚 19% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 421 | 80–129 | 8.4 | 56% | 0 | egypt 33% pharaoh 13% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 3 | 284 | 80–107 | 10.1 | 52% | 0 | egypt 23% | Pasuti | Mehitenusechet | Scheschonq | Scheschonq X | Namlit |
| 4 | 270 | 80–168 | 3.0 | 85% | 18 | samaritan 67% itamar 44% line 43% generation 42% priest 26% high 25% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 5 | 241 | 80–94 | 16.1 | 50% | 0 | zēng 19% 曾 19% hong 12% | (private) | (private) | (private) | (private) | (private) |
| 6 | 201 | 80–102 | 8.7 | 73% | 20 | 陸 66% 陳 20% chén 10% | Xun Boyan, 字:伯言 Lu 陸 | [火荀] 陸 | 令 陸 | 典 陸 | 勛 陸 |
| 7 | 105 | 80–126 | 2.2 | 73% | 0 | 林 17% | 禄 (入闽始祖晋安郡王) 林 第1世闽南林氏衍派 | 颖 (黄门待郎) 林 第46世长林衍派 | 林礼(徒居下邳) 第45世长林衍派 | 裸 林 第45世长林衍派 | 林述 第44世长林衍派 |
| 8 | 90 | 80–118 | 2.3 | 58% | 0 | gōng 43% lài 43% 赖 43% 娶 34% | 娶: 潘氏 | 爱公 Ài Gōng LÀI 赖 | 娶: 陶氏 | 覃公 Tán Gōng LÀI 赖 | 娶: 姜氏 |
| 9 | 83 | 80–153 | 1.1 | 80% | 0 | king 98% axum 97% | Makeda Queen of Sheba | Solomon King of Israel | Menelik I Dawit I King of Axum | Handeyon I King of Axum | Sera I Tomai King of Axum |
| 10 | 82 | 80–93 | 5.9 | 59% | 0 | egypt 46% pharaoh 23% queen 15% | Ay Pharaoh of Egypt | Dedetanuq | Iuhetibu Fendy | Neni | Senebhenas |
| 11 | 79 | 80–93 | 5.6 | 64% | 1 | jatavallabha 56% award 16% by 16% maharaja 16% | Appan Jatavallabha | Aprameya Iyengar Jatavallabha | Krishnaswamy Iyengar Jatavallabha | Narasimhachar Jatavallabha | Rangachar Jatavallabha |
| 12 | 67 | 80–114 | 1.9 | 70% | 0 | 趙 100% | 厲 趙 | 冬曦 趙 | 和壁 趙 | 夏日 趙 | 安貞 趙 |
| … | | | | | | | 107 more clusters in the TSV |

## At least 90 hops from Charlemagne

**3,783 people in 67 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 2,050 | 90–183 | 21.8 | 67% | 3 | 譚 24% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 375 | 90–129 | 9.4 | 57% | 0 | egypt 28% pharaoh 14% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 3 | 250 | 90–168 | 3.2 | 84% | 18 | samaritan 65% itamar 47% line 46% generation 46% priest 20% high 19% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 4 | 187 | 90–133 | 4.2 | 60% | 0 | 李 53% lee 32% | (private) | (private) | (private) | (private) | (private) |
| 5 | 121 | 90–94 | 24.2 | 47% | 0 | hong 22% | (private) | (private) | (private) | (private) | (private) |
| 6 | 96 | 90–107 | 5.3 | 55% | 0 | egypt 26% | Pasuti | Mehitenusechet | Scheschonq | Scheschonq X | Namlit |
| 7 | 92 | 90–102 | 7.1 | 77% | 20 | 陸 100% | Xun Boyan, 字:伯言 Lu 陸 | [火荀] 陸 | 令 陸 | 典 陸 | 勛 陸 |
| 8 | 74 | 90–126 | 2.0 | 74% | 0 |  | 禄 (入闽始祖晋安郡王) 林 第1世闽南林氏衍派 | 颖 (黄门待郎) 林 第46世长林衍派 | 林礼(徒居下邳) 第45世长林衍派 | 裸 林 第45世长林衍派 | 林述 第44世长林衍派 |
| 9 | 72 | 90–153 | 1.1 | 80% | 0 | king 98% axum 97% | Makeda Queen of Sheba | Solomon King of Israel | Menelik I Dawit I King of Axum | Handeyon I King of Axum | Sera I Tomai King of Axum |
| 10 | 70 | 90–118 | 2.4 | 61% | 0 | gōng 41% lài 41% 赖 41% 娶 30% 娶1 10% 娶2 10% | 娶: 潘氏 | 爱公 Ài Gōng LÀI 赖 | 娶: 陶氏 | 覃公 Tán Gōng LÀI 赖 | 娶: 姜氏 |
| 11 | 52 | 90–114 | 2.1 | 71% | 0 | 趙 100% | 厲 趙 | 冬曦 趙 | 和壁 趙 | 夏日 趙 | 安貞 趙 |
| 12 | 39 | 90–94 | 7.8 | 53% | 0 | zeng 10% | (private) | (private) | (private) | (private) | (private) |
| … | | | | | | | 55 more clusters in the TSV |

## At least 100 hops from Charlemagne

**2,931 people in 62 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 1,524 | 100–183 | 18.1 | 65% | 0 | 譚 32% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 315 | 100–176 | 4.1 | 72% | 0 | zēng 13% 鄫 13% sì 11% 姒 11% | Wu, 73G | Jing, 72G | Cáng Huáng 黄 | Xin, 70G | Xu, 69G |
| 3 | 295 | 100–129 | 9.8 | 58% | 0 | egypt 22% pharaoh 15% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 4 | 222 | 100–168 | 3.2 | 84% | 18 | samaritan 65% itamar 49% line 49% generation 48% priest 18% high 17% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 5 | 174 | 100–133 | 5.1 | 59% | 0 | 李 50% lee 34% | (private) | (private) | (private) | (private) | (private) |
| 6 | 61 | 100–153 | 1.1 | 80% | 0 | king 98% axum 96% amen 11% | Makeda Queen of Sheba | Solomon King of Israel | Menelik I Dawit I King of Axum | Handeyon I King of Axum | Sera I Tomai King of Axum |
| 7 | 50 | 100–118 | 2.6 | 66% | 0 | gōng 38% lài 38% 赖 38% 娶 22% 娶1 14% 娶2 14% | 娶: 潘氏 | 爱公 Ài Gōng LÀI 赖 | 娶: 陶氏 | 覃公 Tán Gōng LÀI 赖 | 娶: 姜氏 |
| 8 | 42 | 100–126 | 1.6 | 73% | 0 |  | 禄 (入闽始祖晋安郡王) 林 第1世闽南林氏衍派 | 颖 (黄门待郎) 林 第46世长林衍派 | 林礼(徒居下邳) 第45世长林衍派 | 裸 林 第45世长林衍派 | 林述 第44世长林衍派 |
| 9 | 34 | 100–114 | 2.3 | 70% | 0 | 趙 100% | 厲 趙 | 冬曦 趙 | 和壁 趙 | 夏日 趙 | 安貞 趙 |
| 10 | 28 | 100–113 | 2.0 | 96% | 0 | huang 89% zǔ 10% | Cuì HUANG 黄萃 18A | Lěi HUANG 黄耒 17A | Fēn HUANG 黄芬 19A | Zi Xuān HUANG 黄自軒 16A | Běn Zōng HUANG 黄本宗15A |
| 11 | 20 | 100–113 | 1.4 | 65% | 0 | 李 70% | (no label) | 棟 李 | 侃翁 李 | 子然 李 | (no label) |
| 12 | 17 | 100–107 | 2.1 | 47% | 0 | scheschonq 23% osorkon 11% takelot 11% x 11% | Pasuti | Mehitenusechet | Scheschonq | Scheschonq X | Namlit |
| … | | | | | | | 50 more clusters in the TSV |

## At least 120 hops from Charlemagne

**1,308 people in 57 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 283 | 120–183 | 4.4 | 64% | 0 | 譚 20% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 166 | 120–168 | 3.4 | 84% | 18 | samaritan 56% line 53% generation 52% itamar 52% cohen 21% ben 18% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 3 | 154 | 120–176 | 2.7 | 64% | 0 | huáng 15% 黄 15% | Wu, 73G | Jing, 72G | Cáng Huáng 黄 | Xin, 70G | Xu, 69G |
| 4 | 82 | 120–177 | 1.4 | 85% | 0 | yú 100% 余 100% | Can 灿 Yú 余 | Guang 光 Yú 余 | Hong 烘 Yú 余 | Huang 煌 Yú 余 | Yu 煜 Yú 余 |
| 5 | 82 | 120–133 | 5.9 | 54% | 0 | lee 29% 李 15% | (private) | (private) | (private) | (private) | (private) |
| 6 | 81 | 120–126 | 11.6 | 58% | 0 | chung 11% | (private) | (private) | (private) | (private) | (private) |
| 7 | 58 | 120–177 | 1.0 | 100% | 0 | 黃 100% | 新 黃 | 序 黃 | 重 黃 | 伊 黃 | 乔 黃 |
| 8 | 58 | 120–127 | 7.2 | 50% | 0 | 梁 10% 謝 10% | (private) | (private) | (private) | (private) | (private) |
| 9 | 55 | 120–129 | 5.5 | 61% | 0 | egypt 29% pharaoh 29% | Scorpion I | Khentneith | Pharaoh Crocodile | (no label) | Irinetjer |
| 10 | 50 | 120–124 | 10.0 | 48% | 0 |  | (private) | (private) | (private) | (private) | (private) |
| 11 | 49 | 120–124 | 9.8 | 53% | 0 | 林 18% <private> 14% | (private) | (private) | (private) | (private) | (private) |
| 12 | 37 | 120–153 | 1.1 | 86% | 0 | king 97% axum 94% amen 16% | Makeda Queen of Sheba | Solomon King of Israel | Menelik I Dawit I King of Axum | Handeyon I King of Axum | Sera I Tomai King of Axum |
| … | | | | | | | 45 more clusters in the TSV |

## At least 140 hops from Charlemagne

**436 people in 9 clusters.**

| # | people | dist (min–max) | per hop | deg≤2 | P2600 linked | shared across the whole cluster | the farthest members |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 171 | 140–183 | 3.9 | 68% | 0 | 譚 22% | 少昊 | 顓頊 | 女修 | 大業 | 皋陶 |
| 2 | 86 | 140–176 | 2.3 | 61% | 0 | huáng 10% 黄 10% | Wu, 73G | Jing, 72G | Cáng Huáng 黄 | Xin, 70G | Xu, 69G |
| 3 | 62 | 140–177 | 1.6 | 80% | 0 | yú 100% 余 100% | Can 灿 Yú 余 | Guang 光 Yú 余 | Hong 烘 Yú 余 | Huang 煌 Yú 余 | Yu 煜 Yú 余 |
| 4 | 57 | 140–168 | 2.0 | 100% | 0 | generation 100% itamar 100% line 100% samaritan 100% | 79th generation Samaritan Itamar line | 78th generation Samaritan Itamar line | 80th generation Samaritan Itamar line | 77th generation Samaritan Itamar line | 81st generation Samaritan Itamar line |
| 5 | 38 | 140–177 | 1.0 | 100% | 0 | 黃 100% | 新 黃 | 序 黃 | 重 黃 | 伊 黃 | 乔 黃 |
| 6 | 16 | 140–153 | 1.1 | 81% | 0 | king 93% axum 87% aksumay 12% amen 12% handeyon 12% sera 12% | Makeda Queen of Sheba | Solomon King of Israel | Menelik I Dawit I King of Axum | Handeyon I King of Axum | Sera I Tomai King of Axum |
| 7 | 4 | 140–140 | 4.0 | 75% | 0 | yú 25% 魚 25% | Daughter 1 | Daughter 2 | Daughter 3 | 魚 (Yú ) |
| 8 | 1 | 140–140 | 1.0 | 100% | 0 | zhāo 100% zi 100% 子昭 100% | 子昭 (Zi Zhāo) |
| 9 | 1 | 140–140 | 1.0 | 100% | 0 |  | Daughter |
