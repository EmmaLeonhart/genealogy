"""Build the Sinosphere label overrides (Emma's queue item of 2026-10-04) as `label-applications.tsv` rows.

Inputs, all committed: `reports/sinosphere-label-overrides-size-2026-10-06.csv` (who, and which live slots are ours),
`reports/sinosphere-label-live-2026-10-06.json` (live labels), `reports/sinosphere-label-history-2026-10-06.json`
(label edits on items changed since creation), and the pending `L en` readings in `label-applications.tsv`
(2026-10-04, JMnedict / Wikidata / hand). Rules, decided by the session (devlog 2026-10-06):

Chinese people (established items, pinyin `en`): `ja` and `ko` = the item's own traditional-Han label (`zh-hant`, else
`zh`), replacing our katakana / Hangul read off the pinyin; `fr`/`es` = the pinyin and `ru` = Palladius, only where
the slot is empty. `mul`/`en` stay.
Japanese people (our Han creations): `ja`/`zh` = family name + given name with no space (`中山篤親`) where the Geni
form is a clean `given family`; `mul` = the sourced reading (`Nakayama Atsuchika`, or `NN Surname` by the NN rule);
for a real name also `fr`/`es` = the reading, `ru` = Polivanov, `ko` = the Korean spelling of the reading.
Never: a slot not ours, an item corrected by hand or by a fix batch since creation, a protected item.
Writes `reports/sinosphere-label-overrides-2026-10-06.tsv` (every row with its reason) and prints the counts;
`--apply` appends the rows to `reports/label-applications.tsv`.
"""
import csv, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from palladius import to_palladius
from japanese_reading import to_ru, to_ko

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "Emma queue 2026-10-04 (Sinosphere overrides)"
DATE = "2026-10-06"
PROTECTED = {"Q140568870"}
SEPARATE_ITEM = {"Q141633806", "Q141637029", "Q141636958", "Q141633826"}  # the Aido family: its own queue item
NOT_SINOSPHERE = {"Q141512464", "Q141534009", "Q141635927", "Q141635298"}  # `no name` x2, 未知, NN
NOT_A_NAME = {"Q141636535"}  # "Kiyochika's doughter Kasai": an English description with a typo, no kanji known
ENGLISH_WORD = re.compile(r"\b(Prince|Princess|Emperor|Empress|Lady|Lord|wife|daughter|son|of)\b")
MARKERS = re.compile(r"室|妻|娘|女|后|の|養女|？|\?|\(|（|天皇|内大臣")
MANCHU = {"鈕祜祿", "葉赫納喇", "葉赫那拉", "喜塔臘", "瓜爾佳", "富察", "烏雅", "富察氏"}
# Read one by one: a tsūshō, an art name or an office between the names is not part of the name; a title joins.
BY_HAND = {"Q141640647": ("内藤清成", "tsūshō 弥三郎 dropped"), "Q141638437": ("粟屋悦岑", "gō 笑鴎軒 dropped"),
           "Q141636834": ("三条西公国", "office 内大臣 dropped"), "Q141638641": ("光仁天皇", "Emperor Kōnin")}
# Romanised Japanese creations whose kanji are attested on the established item they duplicate.
ATTESTED = {"Q141635487": ("大伴長徳", "大伴長德", "= Q11432357 Ōtomo no Nagatoko, died 651"),
            "Q141637004": ("大伴咋", "大伴咋", "= Q30932358 Ōtomo no Kui")}
LATIN = re.compile(r"^[A-Za-zĀāĒēĪīŌōŪūÂâÊêÎîÔôÛû' .-]+$")


def main():
    size = [r for r in csv.DictReader(open(ROOT / "reports/sinosphere-label-overrides-size-2026-10-06.csv",
                                           encoding="utf-8")) if r["ours"]]
    live = json.load(open(ROOT / "reports/sinosphere-label-live-2026-10-06.json", encoding="utf-8"))
    hist = json.load(open(ROOT / "reports/sinosphere-label-history-2026-10-06.json", encoding="utf-8"))
    pending = {r["qid"]: r["value"] for r in csv.DictReader(open(ROOT / "reports/label-applications.tsv",
                                                                 encoding="utf-8"), delimiter="\t")
               if r["kind"] == "L" and r["lang"] == "en"}
    corrected = {q for q, revs in hist.items()
                 if any(tag == "wikidata-ui" or ts >= "2026-10-05" for _, ts, tag, _c in revs)}
    out, skipped = [], []

    def put(q, lang, value, why):
        if value and live[q]["labels"].get(lang) != value:
            out.append({"qid": q, "kind": "L", "lang": lang, "value": value, "source": SOURCE, "date": DATE,
                        "note": f"Sinosphere override: {why}"})

    for r in size:
        q = r["qid"]
        L = live[q]["labels"]
        ours = set(r["ours"].split())
        if q in PROTECTED or q in SEPARATE_ITEM or q in NOT_SINOSPHERE or q in NOT_A_NAME:
            skipped.append((q, "protected / its own queue item / not a Sinosphere name")); continue
        if q in corrected:
            skipped.append((q, "corrected by hand or a fix batch since creation")); continue
        if r["created_range"] == "no":
            en = L.get("en", "")
            han = L.get("zh-hant") or L.get("zh-tw") or L.get("zh") or ""
            if not han or not LATIN.match(en or "-"):
                skipped.append((q, "no Han label or no pinyin")); continue
            if q in ("Q229333", "Q2666864"):
                skipped.append((q, "modern Japanese, only our mul, which is right")); continue
            for lang in ("ja", "ko"):
                if lang in ours or not L.get(lang):
                    put(q, lang, han, f"the item's own Han name ({'zh-hant' if L.get('zh-hant') else 'zh'}), "
                                      f"replacing a reading of the pinyin")
            for lang in ("fr", "es"):
                if not L.get(lang):
                    put(q, lang, en, "the pinyin, as en")
            if not L.get("ru"):
                put(q, "ru", to_palladius(en), "Palladius from the pinyin")
            continue
        # Japanese (and a few Chinese) names we created.
        mul = L.get("mul", "")
        toks = mul.split()
        if q in ATTESTED:
            ja, zh, why = ATTESTED[q]
            put(q, "ja", ja, f"attested kanji, {why}"); put(q, "zh", zh, f"attested kanji, {why}")
            continue
        if q in BY_HAND:
            han, why = BY_HAND[q]
        elif (len(toks) == 2 and toks[1] not in MANCHU and not MARKERS.search(mul)
              and all(re.search("[一-鿿]", t) for t in toks)):
            han, why = toks[1] + toks[0], "family name first, no space"
        else:
            han, why = "", ""
        if han:
            for lang in ("ja", "zh"):
                if lang in ours:
                    put(q, lang, han, why)
        reading = pending.get(q) or (L.get("en") if "en" in ours and len((L.get("en") or "").split()) > 1 else "")
        if not reading or not LATIN.match(reading):
            if not han:
                skipped.append((q, f"left as is: {mul} (descriptive, Manchu or one word, and no reading)"))
            continue
        if "mul" in ours:
            put(q, "mul", reading, "mul = the English reading (Emma's item)")
        if reading.split()[0] == "NN" or ENGLISH_WORD.search(reading):
            continue  # NN: mul only (the NN rule); an English word does not belong in fr/es/ru/ko
        manchu = any(t in MANCHU for t in toks)
        for lang in ("fr", "es"):
            if not L.get(lang):
                put(q, lang, reading, "the reading, as en")
        if manchu:
            continue  # Polivanov and the Korean spelling are for Japanese readings, not Manchu
        if not L.get("ru"):
            put(q, "ru", to_ru(reading), "Polivanov from the reading")
        if not L.get("ko") or "ko" in ours:
            put(q, "ko", to_ko(reading), "Korean spelling of the reading")

    path = ROOT / "reports/sinosphere-label-overrides-2026-10-06.tsv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "kind", "lang", "value", "source", "date", "note"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out)
        for q, why in skipped:
            f.write(f"# {q}\tnot overridden: {why}\n")
    import collections
    print(len(out), "rows on", len({o['qid'] for o in out}), "items;", len(skipped), "skipped")
    print(collections.Counter(o["lang"] for o in out))
    print(collections.Counter(why.split(":")[0] for _, why in skipped))
    if "--apply" in sys.argv:
        with open(ROOT / "reports/label-applications.tsv", "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["qid", "kind", "lang", "value", "source", "date", "note"],
                               delimiter="\t", lineterminator="\n")
            w.writerows(out)
        print("appended to reports/label-applications.tsv")


if __name__ == "__main__":
    main()
