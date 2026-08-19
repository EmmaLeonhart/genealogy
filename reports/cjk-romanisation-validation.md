# The romanisations, checked against Wikidata's own English labels

Built by `scripts/validate-cjk-romanisation.py`. **An external check** — every other measurement of this pipeline compares it against sources it already uses, or against a list of characters I wrote myself.

- romanised people: **12,242**
- of those, linked to a Wikidata item: **3,067**
- whose item already carries an English label somebody else wrote: **2,996**

## My syllables appear in their label for **2,798 of 3,001** — 93.2%

The two strings are not meant to match. Wikidata writes the whole name, surname first and the given name run together — `Sun Changqing`. This pipeline romanises the **given name only**, syllables separated — `Chang Qing`. The test is whether my syllables occur in their label.

| culture | agree | differ |
| --- | ---: | ---: |
| ja | 0 | 3 |
| zh | 2,798 | 200 |

## The 203 that differ, and why most are not errors

Wikidata catalogues rulers under **regnal and temple names**. `世民` is `Shi Min` here and `Emperor Taizong of Tang` there — the same man under the name history uses. `履` is `Tang of Shang`; `昌` is `King Wen of Zhou`. Those are naming conventions rather than readings, so this column is for reading, not for counting.

| qid | name | this pipeline | Wikidata | culture |
| --- | --- | --- | --- | --- |
| `Q4309910` | 麗質 隴西狄道 | Li Zhi | Li Lize | zh |
| `Q22812640` | 長孫 孔 | Chang Sun | Kong Zhangsun | zh |
| `Q11091436` | 貞幹 國葆 季洪 湖南湘鄉 | Zhen Gan | Zeng Guobao | zh |
| `Q45420819` | 道賜 南蘭陵 | Dao Ci | Xiao Fu | zh |
| `Q117312658` | 清河東武城 | Qing He Tou Wu Cheng | Lady Cui | zh |
| `Q22814790` | 曠 世宏 琅邪臨沂 | Kuang | Wang Guang | zh |
| `Q11572909` | 偃 子游 琅邪臨沂 | Yan | Wáng Yǎn | zh |
| `Q26158726` | 興 少贛 河南開封 | Xing | Zheng Heng | zh |
| `Q45387263` | 浩 相州安陽 | Kou | Han Hao | ja |
| `Q45358164` | 希純 子進 壽州 | Hiu Chun | Lv Xichun | zh |
| `Q45358166` | 希績 紀常 壽州 | Hiu Ji | Lv Xiji | zh |
| `Q9628247` | 希哲 原明 壽州 | Hiu Zhe | Lü Xizhe | zh |
| `Q45365172` | 蒙亨 壽州 | Meng Heng | Lv Menghen | zh |
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
| `Q45432282` | 開封 | Kai Feng | Han Shi | zh |
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
| `Q45600318` | 濬 蘭陵 | Jun | Xiao Xun | zh |
| `Q45449574` | 顒 蘭陵 | Yong | Xiao Yu | zh |
| `Q45449193` | 希諒 蘭陵 | Hiu Liang | Xiao Xiliang | zh |
| `Q45603466` | 希望 希望 湖州長城 | Hiu Wang | Chen Xiwang | zh |
| `Q45422210` | 榮 弘農華陰 | Ei | Yang Rong | zh |
| `Q17025857` | 承況 隴西狄道 | Cheng Hong | Li Chengkuang | zh |
| `Q45691838` | 士都 隴西狄道 | Shi Du | Li Shidou | zh |
| `Q45692457` | 君房 隴西狄道 | Gun Fang | Li Junfang | zh |
| `Q45692145` | 濬 隴西狄道 | Jun | Li Xun | zh |
| `Q45696069` | 榮 知言 隴西狄道 | Ei | Li Rong | zh |
| `Q11097545` | 緯 京兆長安 | Wei | Li Yi | zh |
| `Q11095612` | 千里 隴西狄道 | Qian Ri | Li Qianli | zh |
| `Q45698921` | 瓌 孝偉 隴西狄道 | Gui | Li Xiang | zh |
| `Q45620986` | 構 趙州贊皇 | Gou | Li Jie | zh |
| `Q45616214` | 東王 趙州贊皇 | Tou Wang | Li Dongwang | zh |
| `Q26159835` | 誕 紹元 趙州平棘 | Dan | Li Yan | zh |
| `Q26159039` | 希騫 趙州贊皇 | Hiu Qian | Li Jian | zh |
| `Q45573721` | 顒 趙州贊皇 | Yong | Li Yu | zh |
| `Q30942534` | 希禮 趙州贊皇 | Hiu Li | Li Xili | zh |
| `Q45624242` | 重光 趙州贊皇 | Zhong Guang | Li Chongguang | zh |
| `Q45599547` | 公曾 趙州贊皇 | Gong Zeng | Li Gongceng | zh |
| `Q45419087` | 世宗 晉昌冥安 | Shi Zong | Tang Zong | zh |
| `Q7682754` | 璿 休璟 晉昌冥安 | Xuan | Tang Xiujing | zh |
| `Q45691930` | 濬 君賾 北海中山 | Jun | Tang Xun | zh |
| `Q45419706` | 靈芝 晉昌冥安 | Ling Zhi | Tang Ling | zh |
| `Q45458949` | 世榮 晉昌冥安 | Shi Ei | Tang Shirong | zh |
| `Q45419713` | 惠兒 晉昌冥安 | Hui Ni | Tang Huier | zh |
| `Q45458380` | 玄都 晉昌冥安 | Xuan Du | Tang Xuandou | zh |
| `Q45690623` | 令則 君憲 北海中山 | Ling Ze | Tang Ze | zh |
| `Q45460406` | 希一 晉昌冥安 | Hiu Yi | Tang Xiyi | zh |
| `Q45419705` | 岳 令世 晉昌冥安 | Yue | Tang Lingshi | zh |
| `Q45419898` | 行成 河東汾陰 | Xing Cheng | Xue Xing | zh |
| `Q45424500` | 希莊 河東汾陰 | Hiu Zhuang | Xue Xizhuang | zh |
| `Q45422684` | 希曾 河東汾陰 | Hiu Zeng | Xue Xizeng | zh |
| `Q45422679` | 謨 河東汾陰 | Mo | Xue Mu | zh |
| `Q45625676` | 播 河中寶鼎 | Ban | Xue Bo | zh |
| `Q45673680` | 承台 太原 | Cheng Yi | Guo Chengtai | zh |
| `Q45680327` | 時 太原 | Shi | Guo Hui | zh |
| `Q11095388` | 偲 京兆萬年 | Si | Li Sui | zh |
| `Q11098132` | 嘉 隴西狄道 | Jia | Li Yun | zh |
| `Q11098126` | 逸 隴西狄道 | Hayaru | Li Yi | ja |
| `Q45394587` | 仕雋 河南洛陽 | Shi Juan | Liu Shijun | zh |
| `Q45537214` | 乾播 京兆杜陵 | Qian Ban | Du Qianbo | zh |
| `Q45537656` | 南榮 京兆杜陵 | Nan Ei | Du Nanrong | zh |
| `Q45421634` | 景秀 京兆杜陵 | Jing Xiu | Du xiu | zh |
| `Q45418946` | 福嗣 京兆杜陵 | Fu Si | Wei Fu | zh |
| `Q10719160` | 琰 隴西狄道 | Yan | Li Tan | zh |
| `Q45454042` | 藏器 弘農華陰 | Zang Qi | Yang Cangqi | zh |
| `Q45529806` | 承騫 隴西狄道 | Cheng Qian | Li Chengjian | zh |
| `Q19853831` | 胤伯 滎陽開封 | Yin Bo | Zheng Yin | zh |
| `Q45511068` | 履順 鄭州榮陽 | Lu Shun | Zheng Lvshun | zh |
| `Q45529715` | 顒 鄭州榮澤 | Yong | Zheng Yu | zh |

*83 further row(s) not listed.*

## What this says about writing labels

**Wikidata's label is better than ours wherever it exists.** It carries the surname, and for a ruler it carries the name history uses. So a label batch over this population must not overwrite: for the **2,996** people whose item already has an English label there is nothing to add, and the romanisation's value is for the ones that do not.
