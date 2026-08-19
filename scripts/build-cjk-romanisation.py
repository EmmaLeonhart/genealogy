"""Romanise Han-only names, from Wikidata's own name items.

Emma, 2026-08-18: *"I am convinced we can actually do the romanization of the CJK pretty
decently… if there's any listed place of birth, then you know which one it is. Chinese and
Korean readings are all very straightforward. Japanese readings are not straightforward,
but Chinese and Korean readings are very straightforward."*

**Both halves of that are built here, and the second half is why this works without a
transliteration library.** No `pypinyin`, no `hanja`, no `pykakasi` is installed, and her
standing instruction is against programmatic transliteration anyway — *"from CJK to English
do not remotely try to do any kind of programmatic transliteration because they all suck."*

So nothing is transliterated. **The romanisations are read out of Wikidata's own name
items**, which carry the Han form and the Latin form as labels on one item:

    Q4464775   zh 屠   en Tu       Chinese family name
    Q11983535  ja 李   ko 이  en Lee   Korean family name
    Q16884158  ja 橘   en Tachibana     Japanese family name

That is a *published* reading of that character as a name, not a guess, and it is
per-culture because the item is per-culture — 李 as a Korean family name is `Lee`, and the
Chinese item for the same character says `Li`.

## Culture first, in her order of evidence

1. **Birth place.** Her words: *"if there's any listed place of birth, then you know which
   one it is."* Strongest and checked first.
2. **Export provenance.** `reports/export-provenance.csv` plus the script mix of the
   exports a person appears in — a Han-only person inside a hangul-writing export is
   Korean. Built 2026-08-18 because the merge deliberately does not track it.
3. **Neighbours.** The scripts used by parents, children and spouses.

**Japanese is emitted separately and marked**, because she is right that its readings are
not straightforward: the same character takes different readings in different names, and a
name item only gives the reading for *that* name. A Chinese or Korean character reading is
effectively one-to-one; a Japanese one is not.

    py scripts/build-cjk-romanisation.py [--limit N]

Writes `reports/cjk-romanisation.csv` and `reports/cjk-romanisation.md`. Reads only.
"""

from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from genimerge import wikistore  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
FACTS = REPO / "reports" / "derived-facts.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
PROV = REPO / "reports" / "export-provenance.csv"
QIDS = REPO / "reports" / "name-item-qids.tsv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT_CSV = REPO / "reports" / "cjk-romanisation.csv"
OUT_MD = REPO / "reports" / "cjk-romanisation.md"

csv.field_size_limit(10_000_000)

HAN = re.compile(r"[㐀-鿿]")
#: A whole token of Han characters. `HAN` is a single-character class, so `HAN.fullmatch`
#: on a four-character token never matches -- which silently disabled clan-seat stripping
#: and made the "nothing but a clan seat" counter measure something else entirely.
HAN_TOKEN = re.compile(r"[㐀-鿿]+")
KANA = re.compile(r"[぀-ヿ]")
HANGUL = re.compile(r"[가-힯]")
LATIN_NAME = re.compile(r"^[A-Z][A-Za-z\-']*$")

#: `P31` values that say what kind of name an item is, and for which culture.
CHINESE = {"Q1093580"}          # Chinese family name
JAPANESE = {"Q16919315", "Q17111581"}   # Japanese family name / given name
KOREAN = {"Q11420694", "Q17300640"}     # Korean family name / given name

#: Place words that settle the culture outright — her first rule.
PLACE = [
    ("zh", ("China", "Chinese", "Taiwan", "Hong Kong", "Beijing", "Shanghai", "Guangdong",
            "Fujian", "Zhejiang", "Jiangsu", "Shandong", "Sichuan", "Henan", "Hubei",
            "Hunan", "Anhui", "Shanxi", "Shaanxi", "Yunnan", "Guangxi", "Jiangxi")),
    ("ko", ("Korea", "Korean", "Seoul", "Busan", "Joseon", "Goryeo", "Silla", "Baekje",
            "Gyeongsang", "Jeolla", "Chungcheong", "Gyeonggi", "Hanyang", "Pyongyang")),
    ("ja", ("Japan", "Japanese", "Tokyo", "Kyoto", "Osaka", "Edo", "Yamato", "Musashi",
            "Owari", "Echizen", "Satsuma", "Hizen", "Kii", "Mutsu", "Shinano", "Nagano",
            "Hokkaido", "Kyushu", "Honshu", "Shikoku")),
]


#: Mandarin pinyin is a **closed syllable set**, and that is what separates a Chinese
#: reading from a Japanese one hiding on the same character. `哲` came out `Akira`, `信`
#: `Makoto`, `旦` `Akira` -- 174 rows -- because Japanese name items carry a `zh` label of
#: the same kanji and do not always carry a kana one, so excluding kana-labelled items was
#: not enough. A single Han character has a single-syllable Mandarin reading; `Akira` and
#: `Makoto` are not syllables of Mandarin at all, and no amount of item metadata is needed
#: to see it.
_INITIALS = ["", "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x",
             "zh", "ch", "sh", "r", "z", "c", "s", "y", "w"]
_FINALS = ["a", "o", "e", "i", "u", "v", "ai", "ei", "ao", "ou", "an", "en", "ang",
           "eng", "ong", "er", "ia", "ie", "iao", "iu", "ian", "in", "iang", "ing",
           "iong", "ua", "uo", "uai", "ui", "uan", "un", "uang", "ueng", "ue", "van",
           "vn", "ve", "uang", "o", "n", "ng"]
PINYIN_SYLLABLES = {i + f for i in _INITIALS for f in _FINALS}


def is_pinyin_syllable(word: str) -> bool:
    """One Mandarin syllable, so a plausible reading of one Han character."""
    return word.lower() in PINYIN_SYLLABLES


#: Sino-Korean readings are a closed syllable set too, and the mirror of the pinyin
#: check. It is what stops the `ko` table returning `He Zi` and `Gui Zi` -- pinyin, from
#: items whose Korean label happens to sit beside a Han one. Revised Romanization
#: shapes: an optional initial, a vowel, an optional final consonant.
_K_INIT = ["", "g", "k", "n", "d", "t", "r", "l", "m", "b", "p", "s", "j", "ch", "h",
           "ss", "jj", "kk", "tt", "pp"]
_K_VOWEL = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe",
            "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i"]
_K_FINAL = ["", "k", "n", "t", "l", "m", "p", "ng"]
#: Conventional spellings Wikidata actually uses, which Revised Romanization does not
#: generate: RR gives 이 as `I`, 박 as `Bak`, 최 as `Choe`, yet the items say `Lee`,
#: `Park`, `Choi`. Generated shapes alone would reject the three commonest Korean
#: surnames there are.
_K_CONVENTIONAL = {"lee", "park", "choi", "kim", "shin", "yoon", "cho", "chung",
                   "hyun", "woo", "hwang", "kwon", "kang", "yoo", "sung", "seo",
                   "rhee", "paik", "pak", "moon", "ahn", "oh", "koo", "noh"}
SINO_KOREAN = ({i + v + f for i in _K_INIT for v in _K_VOWEL for f in _K_FINAL}
               | _K_CONVENTIONAL)


def is_sino_korean_syllable(word: str) -> bool:
    """One Sino-Korean syllable, so a plausible hanja reading."""
    return word.lower() in SINO_KOREAN


def cjk_of(row: dict) -> str:
    """The first CJK name string on a record, or empty."""
    return (row.get("cjk_names") or "").split(" | ")[0].strip()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    # ---- who needs romanising ------------------------------------------------
    need = {}
    scripts = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            cjk = cjk_of(r)
            if not cjk:
                continue
            scripts[r["geni_id"]] = cjk
            if not (r.get("label_en") or "").strip() and HAN.search(cjk):
                need[r["geni_id"]] = cjk
    print(f"people with a CJK name and no Latin label: {len(need):,}")

    # The clan seats are needed as CULTURE evidence below, so they are computed here
    # rather than just before stripping. A trailing 4-character token repeated 20+ times
    # across a lineage is a 郡望 -- see reports/cjk-name-structure.md.
    _tails = collections.Counter()
    for _g, _c in need.items():
        _t = [p for p in _c.split() if HAN_TOKEN.fullmatch(p)]
        if _t:
            _tails[_t[-1]] += 1
    SEATS_EARLY = {t for t, n in _tails.items() if len(t) == 4 and n >= 20}
    print(f"clan seats identified: {len(SEATS_EARLY)}")

    # ---- culture evidence 1: birth place ------------------------------------
    culture = {}
    why = {}
    place_culture = {}
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            place = f"{r.get('birth_place') or ''} {r.get('death_place') or ''}"
            if not place.strip():
                continue
            for code, words in PLACE:
                if any(w in place for w in words):
                    # kept for EVERYONE, not just the need-set: a Han-only person's
                    # culture is often settled by a relative's place rather than by
                    # their own, which is the whole point of the traversal below.
                    place_culture[g] = code
                    if g in need:
                        culture[g] = code
                        why[g] = f"place: {place.strip()[:40]}"
                    break
    print(f"  settled by a listed place: {len(culture):,}")

    # ---- culture evidence 2: NOT export provenance ---------------------------
    # **Removed on Emma's instruction, 2026-08-18: "don't fucking do export provenance,
    # do graph traversal."** It was in here and it was wrong, in a way the output showed
    # plainly: 大唐帝國, the Tang Empire, came out tagged Korean because the export it sits
    # in is Korean-rooted. A Korean-rooted tree is full of Chinese ancestors, so the
    # signal characterises the EXPORT and not the person, and applying it per person
    # mislabels every foreign ancestor inside a national tree.
    #
    # `reports/export-provenance.csv` still stands and is still useful for asking what an
    # export is; it is simply not evidence about an individual.

    # ---- culture evidence 3: graph traversal ---------------------------------
    # Emma, 2026-08-18: *"graph traversal for people with unknown country there will
    # probably work for inferring nationality"*. Immediate kin is not enough -- a
    # Han-only person's parents are often Han-only too -- so this walks outward and
    # takes the NEAREST evidence, which is what makes it an inference rather than a
    # vote over the whole component.
    adj = collections.defaultdict(set)
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            me = r["geni_id"]
            for p in (r.get("father"), r.get("mother")):
                if p:
                    adj[me].add(p)
                    adj[p].add(me)
            for k in (r.get("children") or "").replace("|", " ").split():
                adj[me].add(k)
                adj[k].add(me)
            for sp in (r.get("spouses") or "").replace("|", " ").split():
                adj[me].add(sp)
                adj[sp].add(me)

    def evidence_at(g):
        """What this one person says about culture, if anything."""
        s = scripts.get(g)
        if s:
            if KANA.search(s):
                return "ja"
            if HANGUL.search(s):
                return "ko"
        return place_culture.get(g)

    settled_by_neighbour = 0
    MAX_HOPS = 6
    for g in list(need):
        if g in culture:
            continue
        seen = {g}
        frontier = [g]
        for hop in range(1, MAX_HOPS + 1):
            nxt = []
            votes = collections.Counter()
            for x in frontier:
                for y in adj[x]:
                    if y in seen:
                        continue
                    seen.add(y)
                    nxt.append(y)
                    e = evidence_at(y)
                    if e:
                        votes[e] += 1
            if votes:
                top, n = votes.most_common(1)[0]
                if n / sum(votes.values()) >= 0.7:
                    culture[g] = top
                    why[g] = f"graph traversal, {hop} hop(s)"
                    settled_by_neighbour += 1
                break
            frontier = nxt
            if not frontier:
                break
    # ---- culture evidence 2: the NAME's own form ----------------------------
    # Evidence carried by the name itself, which outranks the graph: a neighbour tells
    # you where a family was reached from, a name tells you what it is.
    #
    # **A 郡望 is Chinese, full stop.** The clan seat is a commandery-and-county of the
    # Chinese empire, and 8,315 Han-only records carry one. It was already being computed
    # to strip it and was not being used as evidence, which is the whole reason so many
    # records had no culture.
    #
    # **The Japanese given-name endings.** `-子` is the big one at 816 -- 和子, 貴子 and
    # 頼子 are Kazuko, Takako and Yoriko, filed Korean by the traversal because a Japanese
    # family reached from the Korean side has Korean neighbours. `-郎`, `-助`, `-丸`,
    # `-衛門`, `-兵衛` and `-之丞` are the same signal and add 186 more.
    JP_ENDINGS = ("子", "郎", "助", "丸", "衛門", "兵衛", "之丞")

    #: Characters COINED IN JAPAN -- 国字. They exist in no Chinese script and in no
    #: Korean hanja, so one of them in a name settles the culture outright rather than
    #: probably. Deliberately conservative: every character a Chinese reader would also
    #: recognise is left out, which is why 栗 is absent -- it looks like a kokuji, it is
    #: not one, it is the ordinary Chinese surname Lì, and including it would have moved
    #: 12 Chinese people to Japanese.
    KOKUJI = set("辻込峠榊畑畠匂枠塀鰯鱈鴫笹麿凪凧栃橳杢躾柾椙椛栂樫俣匁籾裃辷雫毟働")
    #: The mirror: forms that exist ONLY in simplified Chinese -- not in traditional, not
    #: in Japanese shinjitai. Every form the two share is excluded, which is why 国, 学,
    #: 会, 体 and 声 are absent; they are shinjitai as well and prove nothing.
    SIMPLIFIED_ONLY = set(
        "张陈刘杨赵郑冯韩邓萧谢邹苏潘让讲认识语说请记论试谁议访许"
        "钱铁银锦锋钟钢针钦锡镇镜链锁铺铭"
        "红纳结给织经纪级纯纲纸绍绝统继绣绪维绵"
        "马鸟车门页贝见风飞长东业丽丰严义乐习书买卖农孙师华龙无爱")
    # The two sets are disjoint over this data -- checked 2026-08-19: 175 records carry a
    # kokuji, 318 carry a simplified-only form, and **no record carries both**, which is
    # the check that would have caught a character wrongly filed in either set.
    by_kokuji = by_simp = 0
    by_seat = by_ending = 0
    for g, cjk in need.items():
        toks = [p for p in cjk.split() if HAN_TOKEN.fullmatch(p)]
        if not toks:
            continue
        first, last = toks[0], toks[-1]
        # The script facts go first: they are properties of the characters themselves,
        # not inferences about the family, so nothing outranks them.
        if any(ch in KOKUJI for ch in cjk):
            if culture.get(g) != "ja":
                by_kokuji += 1
            culture[g] = "ja"
            why[g] = "carries a character that exists only in Japanese"
        elif any(ch in SIMPLIFIED_ONLY for ch in cjk):
            if culture.get(g) != "zh":
                by_simp += 1
            culture[g] = "zh"
            why[g] = "carries a form that exists only in simplified Chinese"
        elif len(first) >= 2 and first.endswith(JP_ENDINGS):
            if culture.get(g) != "ja":
                by_ending += 1
            culture[g] = "ja"
            why[g] = f"name ends in {first[-1]}, a Japanese given-name ending"
        elif last in SEATS_EARLY:
            if culture.get(g) != "zh":
                by_seat += 1
            culture[g] = "zh"
            why[g] = f"carries the clan seat {last}, which is Chinese"
    print(f"  settled by a Japan-only character: {by_kokuji:,}")
    print(f"  settled by a simplified-only form: {by_simp:,}")
    print(f"  settled by a Chinese clan seat: {by_seat:,}")
    print(f"  settled by a Japanese name ending: {by_ending:,}")
    print(f"  settled by graph traversal: {settled_by_neighbour:,}")
    print(f"  culture settled for {len(culture):,} of {len(need):,}")

    # ---- the reading table, out of Wikidata's own name items ----------------
    qids = []
    with io.open(QIDS, encoding="utf-8", newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd, None)
        for row in rd:
            if row:
                qids.append(row[0])
    print(f"\nname items to read: {len(qids):,}")
    # **The table is built from the labels, not from P31.** A first version required the
    # item to carry a name-kind P31 and got 494 Chinese characters, 6 Korean and *zero*
    # Japanese -- the P31 vocabulary for name items is not consistent enough to filter on,
    # and filtering on it threw away most of the readings that are actually present.
    #
    # What is consistent is the label set: an item whose `zh` label is a single Han
    # character and whose `en` label is a Latin word is a published romanisation of that
    # character. The culture comes from WHICH language label carries the Han form and
    # whether a hangul or kana label sits beside it, which is the item's own statement
    # about itself rather than an inference from a property.
    table = {"zh": {}, "ja": {}, "ko": {}}
    seen_items = 0
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(qids), 5000):
            for q, e in rd.entities(qids[i:i + 5000]).items():
                L = {k: v["value"] for k, v in (e.get("labels") or {}).items()}
                en = L.get("en") or L.get("mul")
                if not en or not LATIN_NAME.match(en):
                    continue
                seen_items += 1
                zh = L.get("zh") or L.get("zh-hant") or L.get("zh-hans")
                ja = L.get("ja")
                ko = L.get("ko")
                # Korean: a hangul label beside a Han one means the Han is hanja and the
                # Latin is its Korean reading.
                if ko and HANGUL.search(ko) and is_sino_korean_syllable(en):
                    for han in (ja, zh):
                        if han and HAN.fullmatch(han):
                            table["ko"].setdefault(han, en)
                            break
                # Japanese: a kana label beside a Han one, same logic.
                if ja and KANA.search(ja):
                    for han in (L.get("ja_kanji"), zh):
                        if han and HAN.fullmatch(han):
                            table["ja"].setdefault(han, en)
                            break
                elif ja and HAN.fullmatch(ja) and not zh:
                    table["ja"].setdefault(ja, en)
                # **A Japanese name item usually also carries a `zh` label of the same
                # character**, so taking every Han `zh` label put Japanese readings in the
                # Chinese table: 端 came out `Tadashi`, 宏 `Hiroshi`, 清 `Kiyoshi`, 治
                # `Osamu` -- 77 rows. A kana `ja` label is the item saying it is Japanese,
                # so it is excluded from Chinese rather than trusted for it.
                # **Single character only, and `len(zh) > 1` is NOT the fix.** The
                # condition here used to read `len(zh) > 1 or is_pinyin_syllable(en)`,
                # which was unreachable -- `HAN` is a one-character class, so
                # `HAN.fullmatch` never matches a longer token -- and enabling it would
                # have been much worse than leaving it dead. Measured 2026-08-19: of the
                # name items whose `zh` label is Han and whose `en` label is a Latin
                # name, **1,356 are one character and 38,710 are longer**, and the long
                # ones are overwhelmingly Chinese *transcriptions of foreign names* --
                # 布瓦索纳德 = Boissonade, 穆特卢 = Mutlu, 赖克曼 = Reichmann. Aligning
                # those character-by-character would teach the table that 德 reads
                # "-ade". They are phonetic spellings of names that are not Chinese, so
                # they are not readings of anything and the branch stays shut.
                if (zh and HAN.fullmatch(zh) and not (ja and KANA.search(ja))
                        and is_pinyin_syllable(en)):
                    table["zh"].setdefault(zh, en)
            if i and i % 200000 == 0:
                print(f"  ...{i:,} read", flush=True)
    print(f"  {seen_items:,} item(s) had a Latin en label")
    for code in table:
        print(f"  {code}: {len(table[code]):,} character(s) with a published reading")

    # ---- strip the clan seat -------------------------------------------------
    # A trailing 4-character token repeated across a lineage is a 郡望, the commandery
    # and county a clan claims -- 隴西狄道 appears 1,253 times. It is a PLACE and belongs
    # to nobody in particular, and romanising it produced "Chen Koori Yang Xia" glued to
    # a person's name. See reports/cjk-name-structure.md.
    SEATS = SEATS_EARLY

    # ---- romanise -----------------------------------------------------------
    rows = []
    done = collections.Counter()
    for g, cjk in need.items():
        code = culture.get(g)
        if not code:
            done["culture unknown"] += 1
            continue
        tokens = [p for p in cjk.split() if HAN_TOKEN.fullmatch(p)]
        seat = tokens[-1] if tokens and tokens[-1] in SEATS else None
        if seat:
            tokens = tokens[:-1]
        if not tokens:
            done["no Han token, or seat only" if seat else "no usable Han token"] += 1
            continue
        # **Only the first token.** After the seat, what is left is the given name and
        # then the courtesy name (字) -- 鯤 幼輿 is Kun, courtesy Youyu. A courtesy name
        # is not what a person is catalogued under, so it does not go in the label.
        name = tokens[0]
        if len(tokens) > 1:
            done[f"{code} given+courtesy, took given"] += 1
        # **Chinese and Korean compose per character; Japanese does not.** Emma said so
        # -- *"Chinese and Korean readings are all very straightforward. Japanese readings
        # are not straightforward"* -- and composing anyway proved it: 文仁 came out
        # `Aya Masashi` when it is *Fumihito*, 信直 `Shin Tadashi` when it is *Nobunao*,
        # 信行 `Shin Kou` when it is *Nobuyuki*. A Japanese given name is read as a whole,
        # and the reading of each kanji in isolation is not a part of it.
        #
        # So Japanese is only emitted when a name item exists for the WHOLE token. That
        # costs coverage and is the only honest option: a composed Japanese reading is
        # not a worse guess, it is a different name.
        if code == "ja":
            whole = table["ja"].get(name)
            if whole:
                rows.append((g, cjk, code, whole, why.get(g, ""), name, seat or ""))
                done["ja romanised (whole-name item)"] += 1
            else:
                done["ja skipped - no whole-name item, and kanji do not compose"] += 1
            continue
        if code == "ko":
            # **Still suppressed, and the syllable check is why it cannot be lifted.**
            # `is_sino_korean_syllable` is the mirror of `is_pinyin_syllable` and it does
            # not separate the two: Mandarin and Sino-Korean syllable inventories OVERLAP.
            # `Ji`, `Jing`, `Wen`, `Cheng` and `Wang` are well-formed in both, so gating
            # the table on Korean shapes still let pinyin through -- 基敬 came out
            # `Ji Jing` and 承旺 `Cheng Wang`, which are Mandarin readings wearing a legal
            # Korean shape.
            #
            # That is the difference from the Japanese case, where `Akira` and `Makoto`
            # are outside Mandarin entirely and the check bites cleanly. Korean needs the
            # ITEM to say which language its reading is in; the string cannot.
            #
            # The 子 rule stayed and was worth having on its own -- 179 people moved off
            # the Korean pile to Japanese, which is where Kazuko and Takako belong.
            # so the method is sound -- the inputs are not. All 51 rows were wrong in two
            # ways at once: 和子, 貴子, 頼子 are Japanese female names (Kazuko, Takako,
            # Yoriko) that the traversal put in `ko`, and the `ko` table returned pinyin
            # for them -- `He Zi`, `Gui Zi`, `Lai Zi`. The `-子` ending is a Japanese
            # signal the culture step does not know about, and the table is polluted the
            # way the Chinese one was before the pinyin check.
            #
            # Fixing it needs a Sino-Korean syllable check, the mirror of
            # `is_pinyin_syllable`, plus a `-子` rule in the culture step. Until then 51
            # wrong labels are worth less than none.
            done["ko suppressed - table polluted and culture misfires on -子"] += 1
            continue
        chars = [c for c in name if HAN.match(c)]
        parts = [table[code].get(c) for c in chars]
        if parts and all(parts):
            rows.append((g, cjk, code, " ".join(parts), why.get(g, ""),
                         name, seat or ""))
            done[f"{code} romanised"] += 1
        else:
            done[f"{code} incomplete"] += 1
    print()
    for k, v in done.most_common():
        print(f"  {k:24} {v:,}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "cjk", "culture", "romanised", "culture_evidence",
                    "name_token", "clan_seat"])
        for row in rows[:limit] if limit else rows:
            w.writerow(row)

    zh = sum(1 for r in rows if r[2] == "zh")
    ko = sum(1 for r in rows if r[2] == "ko")
    ja = sum(1 for r in rows if r[2] == "ja")
    md = ["# Romanising the Han-only names", "",
          "Built by `scripts/build-cjk-romanisation.py`. **Nothing is transliterated** — "
          "every reading is read off a Wikidata name item that carries both the Han form "
          "and the Latin form, so it is a published reading of that character *as a name*.",
          "",
          f"- people with a CJK name and no Latin label: **{len(need):,}**",
          f"- culture settled: **{len(culture):,}**",
          f"- romanised: **{len(rows):,}** — zh **{zh:,}**, ko **{ko:,}**, ja **{ja:,}**",
          "", "## How culture was settled, in Emma's order of evidence", "",
          "| evidence | people |", "| --- | ---: |"]
    # **Derived from `why`, never hand-listed.** The hand-written version went stale the
    # moment the clan seat and the name endings were added: it still carried an `export
    # provenance` row that had been removed on instruction, had no row at all for the two
    # new kinds, and summed to 17,255 against a stated 22,296 -- a report that visibly
    # does not add up is worse than no table.
    kinds = collections.Counter()
    for g in culture:
        w = why.get(g, "")
        if w.startswith("place"):
            kinds["a listed birth or death place"] += 1
        elif w.startswith("graph"):
            kinds["neighbours' script"] += 1
        elif "clan seat" in w:
            kinds["a Chinese clan seat (郡望)"] += 1
        elif "Japanese given-name ending" in w:
            kinds["a Japanese given-name ending"] += 1
        elif "only in Japanese" in w:
            kinds["a character that exists only in Japanese"] += 1
        elif "only in simplified" in w:
            kinds["a simplified-only Chinese character"] += 1
        else:
            kinds["unclassified"] += 1
    md += [f"| {k} | {v:,} |" for k, v in kinds.most_common()]
    md += [f"| **total** | **{sum(kinds.values()):,}** |",
          "", "## Japanese is separated on purpose", "",
          "Emma: *\"Chinese and Korean readings are all very straightforward. Japanese "
          "readings are not straightforward.\"* She is right, and it is structural: a "
          "Chinese or Korean character has effectively one reading as a name, while a "
          "Japanese one takes different readings in different names and the item only "
          "gives the reading for *that* name. **The `ja` rows are the ones to distrust.**"]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT_CSV} and {OUT_MD}")
    for g, cjk, code, rom, ev, name, seat in rows[:15]:
        print("   %-20s %-14s %-3s %-18s %-6s %s" % (g, cjk[:14], code, rom[:18], name, ev[:24]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
