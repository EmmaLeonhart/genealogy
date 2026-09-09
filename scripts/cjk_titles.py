"""Native CJK forms for a title or territorial tail. `イタリアのベレンガーリオ1世`.

**Chosen from four readings of what to do with a title inside a label, 2026-09-07:**
**イタリアのベレンガーリオ1世** — the native form. Kings, dukes and the rest have Japanese
names of their own; they are not transliterated English words.

**What it replaces.** `label_in` transliterated the whole label token by token, so
`Berengar I, emperor of the Romans` came out `ベレンガル・I・エムペロル・オフ・テ・ロマンス` —
`オフ` is the English word *of* in katakana, `テ` is *the*. The transliteration table holds
`of` オフ, `the` テ, `and` アンド, `king` キング, `duke` ドケ, `count` コウント,
`emperor` エムペロル, `bishop` ビスホプ, none of which is a name. **29,119 labels carry a
title tail** that `namemodel.drop_title_tail` already finds.

**The shape is native, not translated word for word.** Japanese and Chinese put the territory
and the title BEFORE the name — `フランドル伯ボードゥアン4世`, `埃及法老拉美西斯二世` — where
Korean uses a space. With no title word it takes the worked example's form, `PLACE` + `の` +
name.

**⛔ AN UNKNOWN PLACE OR TITLE IS REFUSED, never transliterated.** The whole reason the old
output was wrong is that it rendered words it did not know as if they were names, and a
rule-transliterated `Italy` is `イタリ`, not `イタリア`. Where the vocabulary has no entry the
tail is DROPPED and the name alone is rendered — the trim behaviour — so a label can lose its
epithet but can never gain an invented one. `CLAUDE.md` § *Do not guess these*.

The Latin `mul` label is untouched by any of this; only `ja`/`zh`/`ko` change.
"""
from __future__ import annotations

import re

#: English title word -> (ja, zh, ko). Read off the tails that actually occur in
#: `reports/derived-labels.csv`, commonest first: `Pharaoh of Egypt` 137, `King of Axum` 125,
#: `Queen of Egypt` 56, `King of Bactria` 34, `King of Assyria` 27.
TITLES: dict[str, tuple[str, str, str]] = {
    "pharaoh": ("ファラオ", "法老", "파라오"),
    "king": ("王", "国王", "왕"),
    "queen": ("女王", "女王", "여왕"),
    "emperor": ("皇帝", "皇帝", "황제"),
    "empress": ("皇后", "皇后", "황후"),
    "duke": ("公", "公爵", "공작"),
    "duchess": ("女公", "女公爵", "여공작"),
    "count": ("伯", "伯爵", "백작"),
    "countess": ("女伯", "女伯爵", "여백작"),
    "earl": ("伯", "伯爵", "백작"),
    "prince": ("公", "亲王", "공"),
    "princess": ("王女", "公主", "공주"),
    "baron": ("男爵", "男爵", "남작"),
    "baroness": ("男爵夫人", "男爵夫人", "남작부인"),
    "margrave": ("辺境伯", "边疆伯爵", "변경백"),
    "landgrave": ("方伯", "方伯", "방백"),
    "bishop": ("司教", "主教", "주교"),
    "archbishop": ("大司教", "大主教", "대주교"),
    "lord": ("卿", "领主", "경"),
    "lady": ("夫人", "夫人", "부인"),
    "knight": ("騎士", "骑士", "기사"),
    "sultan": ("スルタン", "苏丹", "술탄"),
    "khan": ("ハン", "汗", "칸"),
    "tsar": ("ツァーリ", "沙皇", "차르"),
    "czar": ("ツァーリ", "沙皇", "차르"),
    "caliph": ("カリフ", "哈里发", "칼리프"),
    "high priest": ("大祭司", "大祭司", "대제사장"),
    "chief": ("首長", "首领", "족장"),
    "lagmann": ("法speaker", "法官", "법관"),
}
# `lagmann` is the Norse lawspeaker; the ja value above is a placeholder and is corrected below
TITLES["lagmann"] = ("法務官", "法官", "법관")

#: Territory -> (ja, zh, ko). The places that actually occur after a connective in a title tail,
#: commonest first. A place NOT here refuses the tail rather than being transliterated.
PLACES: dict[str, tuple[str, str, str]] = {
    "egypt": ("エジプト", "埃及", "이집트"),
    "axum": ("アクスム", "阿克苏姆", "악숨"),
    "armenia": ("アルメニア", "亚美尼亚", "아르메니아"),
    "burgundy": ("ブルグント", "勃艮第", "부르고뉴"),
    "leinster": ("レンスター", "伦斯特", "렌스터"),
    "bactria": ("バクトリア", "巴克特里亚", "박트리아"),
    "denmark": ("デンマーク", "丹麦", "덴마크"),
    "assyria": ("アッシリア", "亚述", "아시리아"),
    "ireland": ("アイルランド", "爱尔兰", "아일랜드"),
    "bohemia": ("ボヘミア", "波希米亚", "보헤미아"),
    "france": ("フランス", "法国", "프랑스"),
    "sweden": ("スウェーデン", "瑞典", "스웨덴"),
    "hungary": ("ハンガリー", "匈牙利", "헝가리"),
    "georgia": ("グルジア", "格鲁吉亚", "조지아"),
    "lithuania": ("リトアニア", "立陶宛", "리투아니아"),
    "kiev": ("キエフ", "基辅", "키예프"),
    "poland": ("ポーランド", "波兰", "폴란드"),
    "rome": ("ローマ", "罗马", "로마"),
    "the romans": ("ローマ人", "罗马人", "로마인"),
    "romans": ("ローマ人", "罗马人", "로마인"),
    "italy": ("イタリア", "意大利", "이탈리아"),
    "norway": ("ノルウェー", "挪威", "노르웨이"),
    "england": ("イングランド", "英格兰", "잉글랜드"),
    "scotland": ("スコットランド", "苏格兰", "스코틀랜드"),
    "flanders": ("フランドル", "佛兰德", "플랑드르"),
    "estland": ("エストニア", "爱沙尼亚", "에스토니아"),
    "estonia": ("エストニア", "爱沙尼亚", "에스토니아"),
    "ulster": ("アルスター", "阿尔斯特", "얼스터"),
    "munster": ("マンスター", "芒斯特", "먼스터"),
    "connacht": ("コナハト", "康诺特", "코노트"),
    "wales": ("ウェールズ", "威尔士", "웨일스"),
    "israel": ("イスラエル", "以色列", "이스라엘"),
    "judah": ("ユダ", "犹大", "유다"),
    "babylon": ("バビロン", "巴比伦", "바빌론"),
    "persia": ("ペルシア", "波斯", "페르시아"),
    "russia": ("ロシア", "俄罗斯", "러시아"),
    "spain": ("スペイン", "西班牙", "스페인"),
    "portugal": ("ポルトガル", "葡萄牙", "포르투갈"),
    "germany": ("ドイツ", "德国", "독일"),
    "austria": ("オーストリア", "奥地利", "오스트리아"),
    "bavaria": ("バイエルン", "巴伐利亚", "바이에른"),
    "saxony": ("ザクセン", "萨克森", "작센"),
    "brittany": ("ブルターニュ", "布列塔尼", "브르타뉴"),
    "normandy": ("ノルマンディー", "诺曼底", "노르망디"),
    "aquitaine": ("アキテーヌ", "阿基坦", "아키텐"),
    "anjou": ("アンジュー", "安茹", "앙주"),
    "castile": ("カスティーリャ", "卡斯蒂利亚", "카스티야"),
    "aragon": ("アラゴン", "阿拉贡", "아라곤"),
    "navarre": ("ナバラ", "纳瓦拉", "나바라"),
    "jerusalem": ("エルサレム", "耶路撒冷", "예루살렘"),
    "byzantium": ("ビザンティン", "拜占庭", "비잔티움"),
    "constantinople": ("コンスタンティノープル", "君士坦丁堡", "콘스탄티노폴리스"),
    "finland": ("フィンランド", "芬兰", "핀란드"),
    "iceland": ("アイスランド", "冰岛", "아이슬란드"),
    "orkney": ("オークニー", "奥克尼", "오크니"),
    "moravia": ("モラヴィア", "摩拉维亚", "모라비아"),
    "serbia": ("セルビア", "塞尔维亚", "세르비아"),
    "bulgaria": ("ブルガリア", "保加利亚", "불가리아"),
    "croatia": ("クロアチア", "克罗地亚", "크로아티아"),
    "wessex": ("ウェセックス", "威塞克斯", "웨식스"),
    "mercia": ("マーシア", "麦西亚", "머시아"),
    "northumbria": ("ノーサンブリア", "诺森布里亚", "노섬브리아"),
}

#: **A PEOPLE is a territory for this purpose** — `King of the Franks`, `of the Picts`. Measured
#: over the labels, these outnumber true epithets several times over.
PLACES.update({
    "the franks": ("フランク人", "法兰克人", "프랑크인"),
    "franks": ("フランク人", "法兰克人", "프랑크인"),
    "the picts": ("ピクト人", "皮克特人", "픽트인"),
    "the isles": ("諸島", "群岛", "제도"),
    "the burgundians": ("ブルグント人", "勃艮第人", "부르군트인"),
    "the hittites": ("ヒッタイト人", "赫梯人", "히타이트인"),
    "the obotrites": ("オボトリート人", "鄂博德里特人", "오보트리트인"),
    "the huns": ("フン人", "匈人", "훈족"),
    "the ostrogoths": ("東ゴート人", "东哥特人", "동고트족"),
    "the visigoths": ("西ゴート人", "西哥特人", "서고트족"),
    "the vandals": ("ヴァンダル人", "汪达尔人", "반달족"),
    "the angles": ("アングル人", "盎格鲁人", "앵글인"),
    "the goths": ("ゴート人", "哥特人", "고트족"),
    "the danes": ("デーン人", "丹麦人", "데인인"),
    "the swedes": ("スウェーデン人", "瑞典人", "스웨덴인"),
    "the saxons": ("ザクセン人", "撒克逊人", "작센인"),
    "the lombards": ("ランゴバルド人", "伦巴第人", "랑고바르드족"),
    "the turks": ("テュルク人", "突厥人", "튀르크인"),
    "the alemannians": ("アレマンニ人", "阿勒曼尼人", "알레만니인"),
    "the heruli": ("ヘルール人", "赫鲁利人", "헤룰리인"),
    "ivrea": ("イヴレア", "伊夫雷亚", "이브레아"),
    "friuli": ("フリウリ", "弗留利", "프리울리"),
    "cysoing": ("シソワン", "西苏瓦恩", "시수앙"),
    "blekinge": ("ブレーキンゲ", "布莱金厄", "블레킹에"),
    "lolland": ("ロラン", "洛兰", "롤란"),
})

#: **An EPITHET is a byname, and Japanese gives it its own established form** — `敬虔王`,
#: `禿頭王`, `大王`. It carries no connective, so `drop_title_tail` never sees it and
#: `Louis I, The Pious` came out `ルイ・I・ザ・ピオウス`. Small population: `the great` 34,
#: `the black` 9. Anything not listed is dropped, not transliterated.
EPITHETS: dict[str, tuple[str, str, str]] = {
    "great": ("大王", "大帝", "대왕"),
    "pious": ("敬虔王", "虔诚者", "경건왕"),
    "bald": ("禿頭王", "秃头王", "대머리왕"),
    "fat": ("肥満王", "胖子", "비만왕"),
    "simple": ("単純王", "糊涂王", "단순왕"),
    "stammerer": ("吃音王", "口吃者", "말더듬이왕"),
    "bold": ("豪胆公", "勇敢者", "대담공"),
    "good": ("善良王", "善良者", "선량왕"),
    "black": ("黒王", "黑王", "흑왕"),
    "bearded": ("髭王", "大胡子", "수염왕"),
    "holy": ("聖", "圣", "성"),
    "elder": ("大", "老", "대"),
    "younger": ("小", "少", "소"),
    "young": ("小", "少", "소"),
    "wise": ("賢王", "贤王", "현왕"),
    "conqueror": ("征服王", "征服者", "정복왕"),
    "lion": ("獅子王", "狮王", "사자왕"),
    "red": ("赤王", "红王", "적왕"),
    "tall": ("長身王", "高个", "장신왕"),
    "quarrelsome": ("喧嘩王", "好斗者", "싸움왕"),
}

_EPITHET_RE = re.compile(r"[, ]+the\s+([A-Za-z]+)[\s,]*$", re.IGNORECASE)


def split_epithet(label: str) -> tuple[str, tuple[str, str, str] | None]:
    """`(label without its trailing epithet, the epithet's CJK forms or None)`.

    An unknown byname is left ON the label rather than dropped, because it may be a name --
    only a word in `EPITHETS` is taken.
    """
    m = _EPITHET_RE.search(label or "")
    if not m:
        return label, None
    form = EPITHETS.get(m.group(1).casefold())
    if form is None:
        return label, None
    return label[:m.start()].strip().strip(","), form


#: The connectives that introduce a territory. `i` and `till` are Scandinavian and are already
#: handled by `build-garborg-day._drop_territorial`; `of` is the English one this adds.
_CONNECTIVE = r"(?:of|av|af|von|de|di|du|zu)"

_CONNECTIVE_RE = re.compile(r"\b(?:of|av|af|von|de|di|du|zu)\b", re.IGNORECASE)

#: A katakana title is a LOANWORD and takes `の`: `エジプトのファラオ`, not `エジプトファラオ`.
#: A kanji one attaches directly, which is the standard form -- `エジプト王`, `フランドル伯`.
_KATAKANA = re.compile(r"^[\u30a0-\u30ff]")


def render_tail(tail: str) -> tuple[str, str, str] | None:
    """`(ja, zh, ko)` for a title tail like `emperor of the Romans`, or `None` to drop it.

    `None` means the vocabulary does not cover this tail, and the caller renders the name
    alone. Never a transliteration — see the module docstring.
    """
    tail = (tail or "").strip().strip(",").strip()
    if not tail:
        return None
    m = _CONNECTIVE_RE.search(tail)
    if m:
        title = tail[:m.start()].strip().strip(",")
        place = tail[m.end():].strip().strip(",")
    else:
        title, place = tail, ""
    title = re.sub(r"^the\s+", "", title, flags=re.IGNORECASE).strip().casefold()
    place = place.casefold()
    tj = TITLES.get(title) if title else ("", "", "")
    if title and tj is None:
        return None
    pj = PLACES.get(place) if place else ("", "", "")
    # **A tail can stack two of them** -- `of Ivrea, king of Italy` -- and the first connective
    # then swallows the rest as one unfindable place. `drop_title_tail` deliberately truncates
    # at the EARLIEST title word, so this is the ordinary case rather than an edge one: retry
    # on the part after the last comma, which is the innermost title.
    if place and pj is None and "," in place:
        return render_tail(place.rsplit(",", 1)[1])
    if place and pj is None:
        return None
    if not title and not place:
        return None
    if title and place and _KATAKANA.match(tj[0]):
        return (pj[0] + "の" + tj[0], pj[1] + tj[1], pj[2] + " " + tj[2])
    return tuple(p + t for p, t in zip(pj, tj))       # place first, then the title word


def is_bare_place(tail: str) -> bool:
    """True when the tail is a territory with NO title word -- `of Italy`.

    That case takes the worked example's form, `イタリアのベレンガーリオ1世`, rather than the
    place attaching straight to the name. **It follows the same comma recursion as
    `render_tail`**: `of Ivrea, king of Italy` opens with a bare connective but resolves to
    `king of Italy`, which has a title, and reading only the front gave `イタリア王のベレンガル
    2世` with a `の` that does not belong.
    """
    tail = (tail or "").strip().strip(",")
    m = _CONNECTIVE_RE.search(tail)
    if not m:
        return False
    if tail[:m.start()].strip().strip(","):
        return False
    rest = tail[m.end():].strip().strip(",")
    if rest.casefold() not in PLACES and "," in rest:
        return is_bare_place(rest.rsplit(",", 1)[1])
    return True


def compose(name: tuple[str, str, str], tail: tuple[str, str, str] | None,
            bare_place: bool) -> tuple[str, str, str]:
    """The finished `(ja, zh, ko)`. The title goes BEFORE the name in `ja` and `zh`.

    `bare_place` is true when the tail was a territory with no title word, which takes the worked
    example's form: `イタリア` + `の` + the name.
    """
    if tail is None:
        return name
    ja, zh, ko = name
    tja, tzh, tko = tail
    if bare_place:
        return f"{tja}の{ja}", f"{tzh}的{zh}", f"{tko}의 {ko}"
    return f"{tja}{ja}", f"{tzh}{zh}", f"{tko} {ko}"
