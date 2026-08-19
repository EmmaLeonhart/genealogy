# The romanisations, checked against Wikidata's own English labels

Built by `scripts/validate-cjk-romanisation.py`. **An external check** — every other measurement of this pipeline compares it against sources it already uses, or against a list of characters I wrote myself.

- romanised people: **12,068**
- of those, linked to a Wikidata item: **3,188**
- whose item already carries an English label somebody else wrote: **3,139**

## My syllables appear in their label for **2,888 of 3,144** — 91.9%

The two strings are not meant to match. Wikidata writes the whole name, surname first and the given name run together — `Sun Changqing`. This pipeline romanises the **given name only**, syllables separated — `Chang Qing`. The test is whether my syllables occur in their label.

| culture | agree | differ |
| --- | ---: | ---: |
| ja | 0 | 3 |
| zh | 2,888 | 253 |

## The 256 that differ, and why most are not errors

Wikidata catalogues rulers under **regnal and temple names**. `世民` is `Shi Min` here and `Emperor Taizong of Tang` there — the same man under the name history uses. `履` is `Tang of Shang`; `昌` is `King Wen of Zhou`. Those are naming conventions rather than readings, so this column is for reading, not for counting.

| qid | name | this pipeline | Wikidata | culture |
| --- | --- | --- | --- | --- |
| `Q4309910` | 麗質 隴西狄道 | Li Zhi | Li Lize | zh |
| `Q1149178` | 珪 拓拔 | Gui | Emperor Daowu of Northern Wei | zh |
| `Q878473` | 瞿 子姓 | Qu | Wu Yi of Shang | zh |
| `Q878455` | 新 子姓 | Xin | Zu Ding | zh |
| `Q878449` | 旦 子姓 | Dan | Zu Xin | zh |
| `Q878487` | ‏‏‎ 勝 子姓 | Sheng | Zu Yi | zh |
| `Q878465` | 至 子姓 | Zhi | Tai Jia | zh |
| `Q471820` | 履 子姓 | Lu | Tang | zh |
| `Q698909` | 昌 姬姓 | Chang | King Wen of Zhou | zh |
| `Q878479` | 密 子姓 | Mi | Tai Wu | zh |
| `Q878444` | 載 子姓 | Zai | Zu Jia | zh |
| `Q888231` | ‏‏‎ ‎丁 子姓 | Zi Xing | Da Ding of Shang | zh |
| `Q369159` | 昭 子姓 | Zhao | Wu Ding | zh |
| `Q197807` | 莊 子姓 | Zhuang | Zhong Ding | zh |
| `Q9701` | 世民 隴西狄道 | Shi Min | Emperor Taizong of Tang | zh |
| `Q1066885` | 南蘭陵 | Nan Lan Ling | Empress Xiao | zh |
| `Q77895` | 傑 愛新覺羅 | Masaru | Pujie | ja |
| `Q185152` | 儀 愛新覺羅 一 | Tadashi | Puyi | ja |
| `Q9753` | 豫 隴西狄道 | Yu | Emperor Daizong of Tang | zh |
| `Q9760` | 誦 隴西狄道 | Song | Emperor Shunzong of Tang | zh |
| `Q4604` | 丘 仲尼 子姓 | Qiu | Confucius | zh |
| `Q7239950` | 伯夏 子姓 | Bo Xia | Ba Xia | zh |
| `Q7316` | 協 伯和 劉 | Xie | Emperor Xian of Han | zh |
| `Q7488` | 桓 趙 | Huan | Emperor Qinzong of Song | zh |
| `Q7486` | 佶 趙 | Ji | Emperor Huizong of Song | zh |
| `Q11091436` | 貞幹 國葆 季洪 湖南湘鄉 | Zhen Gan | Zeng Guobao | zh |
| `Q5948949` | 共 子姓 | Gong | Duke Min I of Song | zh |
| `Q5949181` | 申 子姓 | Shen | Duke Ding of Song | zh |
| `Q736726` | 衍 叔達 南蘭陵 | Yan | Wu | zh |
| `Q837918` | 琮 溫文 南蘭陵 | Cong | Emperor Jing of Western Liang | zh |
| `Q259628` | 長懋 雲喬 南蘭陵 | Chang Mao | Xiao Zhangmao | zh |
| `Q10511648` | 整 公齊 東海蘭陵 | Tadashi | Xiao Zheng | ja |
| `Q1194981` | 道成 紹伯 南蘭陵 | Dao Cheng | Emperor Gao of Southern Qi | zh |
| `Q940037` | 賾 宣遠 南蘭陵 | Ze | Emperor Wu of Southern Qi | zh |
| `Q117312658` | 清河東武城 | Qing He Tou Wu Cheng | Lady Cui | zh |
| `Q7393` | 紹 道畿 河內溫縣 | Shao | Emperor Ming of Jin | zh |
| `Q7392` | 睿 景文 河內溫縣 | Rui | Emperor Yuan of Jin | zh |
| `Q7400` | 昱 道萬 河內溫縣 | Yu | Emperor Jianwen of Jin | zh |
| `Q22814790` | 曠 世宏 琅邪臨沂 | Kuang | Wang Guang | zh |
| `Q11572909` | 偃 子游 琅邪臨沂 | Yan | Wáng Yǎn | zh |
| `Q26158726` | 興 少贛 河南開封 | Xing | Zheng Heng | zh |
| `Q1140994` | 綱 世贊 南蘭陵 | Gang | Emperor Jianwen of Liang | zh |
| `Q45358164` | 希純 子進 壽州 | Hiu Chun | Lv Xichun | zh |
| `Q45358166` | 希績 紀常 壽州 | Hiu Ji | Lv Xiji | zh |
| `Q9628247` | 希哲 原明 壽州 | Hiu Zhe | Lü Xizhe | zh |
| `Q45365172` | 蒙亨 壽州 | Meng Heng | Lv Menghen | zh |
| `Q45376487` | 蒙巽 壽州 | Meng Xun | Lv Mengsun | zh |
| `Q45362094` | 希俊 開封 | Hiu Jun | Lv Xijun | zh |
| `Q45365867` | 希傑 壽州 | Hiu Jie | Lv Xijie | zh |
| `Q45362961` | 祐 景叔 大名莘縣 | You | Wang Hu | zh |
| `Q45363805` | 大名宗城 | Da Ming Zong Cheng | Fan Shi | zh |
| `Q45400269` | 希言 宋州宋城 | Hiu Yan | Cai Xiyan | zh |
| `Q45365963` | 泌 開封 | Mi | Su Bi | zh |
| `Q45358169` | 希道 景純 壽州 | Hiu Dao | Lv Xidao | zh |
| `Q45391533` | 東美 眉州青神 | Tou Mei | Wang Dongmei | zh |
| `Q45383376` | 游立 曾 | You Li | Zeng Ketu | zh |
| `Q45402076` | 君玉 建昌南城 | Gun Yu | Wang Junyu | zh |
| `Q45363950` | 復 信州上饒 | Fu | Han Shi | zh |
| `Q45420298` | 子斌 伯達 河東解縣 | Zi Bin | Liu Bin | zh |
| `Q133521479` | 尚之 季儒 范陽涿縣 | Shang Zhi | 盧尚之 (季儒) | zh |
| `Q10897941` | 榮男 彭城 | Ei Nan | Liu Rongnan | zh |
| `Q45588820` | 君榮 趙國柏仁 | Gun Ei | Li Junrong | zh |
| `Q45369824` | 碩 季膺 泉州永春 | Shuo | Liu Shi | zh |
| `Q45369820` | 𥵣 端父 泉州永春 | Duan Fu | Liu Duan | zh |
| `Q45420524` | 定高 河東聞喜 | Ding Gao | Pei Ding | zh |
| `Q45420497` | 安祖 河東聞喜 | An Zu | Pei Zuan | zh |
| `Q45420521` | 嵩壽 河東聞喜 | Song Shou | Pei Song | zh |
| `Q45420563` | 昚 歸厚 河東聞喜 | Shen | Pei Juan | zh |
| `Q45362384` | 朴 文季 陝州夏縣 | Piao | Sima Pu | zh |
| `Q45364124` | 開封 | Kai Feng | Chao Shi | zh |
| `Q45363022` | 覃 開封東明 | Qin | Wang Tan | zh |
| `Q45432282` | 開封 | Kai Feng | Han Shi | zh |
| `Q45363807` | 開封 | Kai Feng | Lv Shi | zh |
| `Q45387703` | 希彥 開封 | Hiu Yan | Lv Xiyan | zh |
| `Q45376494` | 開封 | Kai Feng | Lv Zhaowen | zh |
| `Q45387646` | 希朴 開封 | Hiu Piao | Lv Xipu | zh |
| `Q45428054` | 朴 蘇州長洲 | Piao | Wang Pu | zh |
| `Q45373898` | 簡 揚州江都 | Jian | Zhang Sheng | zh |
| `Q45379766` | 希古 鄭州管城 | Hiu Gu | Chen Xigu | zh |
| `Q45354797` | 榮古 鄭州管城 | Ei Gu | Chen Ronggu | zh |
| `Q45377531` | 傳師 越州山陰 | Chuan Shi | Fu Zhuanshi | zh |
| `Q45361204` | 諶 鄂州武昌 | Chen | Feng Shen | zh |
| `Q45363796` | 江陵 | Jiang Ling | Zhu Shi | zh |
| `Q45382958` | 祕 鄧州南陽 | Mi | Zhu Bi | zh |
| `Q45356303` | 傳正 越州山陰 | Chuan Zheng | Fu Zhuanzheng | zh |
| `Q45363800` | 開封 | Kai Feng | Li Shi | zh |
| `Q45364109` | 開封 | Kai Feng | Li Shi | zh |
| `Q45377462` | 希聲 越州會稽 | Hiu Sheng | Guan Xisheng | zh |
| `Q45358647` | 倬 陝州夏縣 | Zhuo | Sima Jue | zh |
| `Q45373495` | 希顏 宋州宋城 | Hiu Yan | Cai Xiyan | zh |
| `Q45364935` | 建昌南豐 | Jian Chang Nan Feng | Zeng Shi | zh |
| `Q45424477` | 彥琮 滑州匡城 | Yan Cong | Li Yanzong | zh |
| `Q45649600` | 君逸 趙州平棘 | Gun Yi | Li Junyi | zh |
| `Q45600960` | 曾 吳郡吳縣 | Zeng | Lu Ceng | zh |
| `Q65803830` | 清河東武城 | Qing He Tou Wu Cheng | Cui Shi | zh |
| `Q45537026` | 孝弁 京兆杜陵 | Xiao Bian | Du Xiaoyan | zh |
| `Q45364030` | 開封 | Kai Feng | Liu Shi | zh |
| `Q45364492` | 江寧 | Jiang Ning | Huang Shi | zh |
| `Q45364898` | 開封 | Kai Feng | Shen Shi | zh |
| `Q45371654` | 君章 時發 福州侯官 | Gun Zhang | Chen Junzhang | zh |
| `Q65803985` | 蘭陵 | Lan Ling | Xiao Shi | zh |
| `Q45450203` | 騫 蘭陵 | Qian | Xiao Jian | zh |
| `Q26209008` | 仲真 弘農華陰 | Zhong Zhen | Yang Zhen | zh |
| `Q45419602` | 不疑 潁川城父 | Bu Yi | Zhang Buni | zh |
| `Q1149132` | 鸞 景棲 南蘭陵 | Luan | Emperor Ming of Southern Qi | zh |
| `Q1190420` | 寶融 智昭 南蘭陵 | Bao Rong | Emperor He of Southern Qi | zh |
| `Q45600318` | 濬 蘭陵 | Jun | Xiao Xun | zh |
| `Q45449574` | 顒 蘭陵 | Yong | Xiao Yu | zh |
| `Q45449193` | 希諒 蘭陵 | Hiu Liang | Xiao Xiliang | zh |
| `Q45603466` | 希望 希望 湖州長城 | Hiu Wang | Chen Xiwang | zh |
| `Q45422210` | 榮 弘農華陰 | Ei | Yang Rong | zh |
| `Q718222` | 伯宗 吳興長城 | Bo Zong | Emperor Fei of Chen | zh |
| `Q17025857` | 承況 隴西狄道 | Cheng Hong | Li Chengkuang | zh |
| `Q45691838` | 士都 隴西狄道 | Shi Du | Li Shidou | zh |
| `Q45692457` | 君房 隴西狄道 | Gun Fang | Li Junfang | zh |
| `Q45692145` | 濬 隴西狄道 | Jun | Li Xun | zh |
| `Q45696069` | 榮 知言 隴西狄道 | Ei | Li Rong | zh |
| `Q11097545` | 緯 京兆長安 | Wei | Li Yi | zh |
| `Q11095612` | 千里 隴西狄道 | Qian Ri | Li Qianli | zh |
| `Q45698921` | 瓌 孝偉 隴西狄道 | Gui | Li Xiang | zh |

*136 further row(s) not listed.*

## What this says about writing labels

**Wikidata's label is better than ours wherever it exists.** It carries the surname, and for a ruler it carries the name history uses. So a label batch over this population must not overwrite: for the **3,139** people whose item already has an English label there is nothing to add, and the romanisation's value is for the ones that do not.
