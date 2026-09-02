"""How many people the culture walk filed as Chinese are actually Japanese.

    py scripts/measure-japanese-in-zh.py

**This is the measurement `queue.md` § LABELS names as the blocker on the `en` step:** *"Do not
wire `romanised` into `label_en` until the Japanese-in-`zh` rate is measured — a wrong reading of
a real name is the one thing her rules forbid outright."*

The symptom that prompted it: `幸豊 青山` romanised `Qing Shan Heng Li` and `忠貫 酒井`
`Jiu Jing Zhong Guan`. Aoyama and Sakai are Japanese samurai houses being read in Mandarin
because the graph walk put them in `zh`.

## The discriminator, and why it is not a guess about the name

`pykakasi` carries a **surname dictionary**. Given a token it knows, it returns the irregular
kun'yomi reading a Japanese person actually uses — 青山 あおやま, 酒井 さかい, 藤原 ふじわら.
Given a token it does not know, it falls back to reading each character by its on'yomi.

So the two cases are separable **without looking at the name itself**: take Unihan's
`kJapaneseOn` for each character, concatenate, and compare with what `pykakasi` returned.

* they **match** → `pykakasi` had nothing and fell back. No evidence either way.
* they **differ** → `pykakasi` resolved the token out of its dictionary. That is positive
  evidence the token is a Japanese surname, from a source that knows nothing about our tree.

**Compare ROMAJI, not kana.** `kJapaneseOn` is written `KOU`, `CHIN`, `RYUU` — romaji, not
katakana — and `pykakasi`'s `hepburn` field is the same transcription. The first version of this
converted katakana to hiragana and compared against `hira`, so **nothing ever matched** and every
row scored as a dictionary hit: it reported 陳, 曾, 劉 and 王 as Japanese surnames and put the
rate at 45.9%. The sample is what caught it; the number alone looked plausible.

**A one-character token is refused.** Read alone, `pykakasi` gives a lone character its *word*
reading, so 李 comes back `sumomo` (the plum), 孔 `ana` (a hole) and 黄 `ki` (yellow) — kun'yomi
that differ from the on'yomi and would score as dictionary hits while saying nothing about
surnames. The restriction is also the right shape: Chinese surnames are overwhelmingly one
character and Japanese ones two, so a resolved **two**-character token is the informative case.

`CLAUDE.md` § *"Is X present?"* forbids classifying people by what their name looks like. This
does not do that: it asks a Japanese-language dictionary whether it holds the token, which is
the same kind of evidence as a Wikidata name item, not a similarity heuristic.

**It is one-directional and that is stated rather than hidden.** A dictionary hit is evidence
*for* Japanese; a miss is evidence for nothing at all, because the dictionary is not a census of
Chinese surnames. So this measures a **floor** on the misclassification, never a ceiling.

Writes `reports/japanese-in-zh.tsv` — every `zh` person whose surname `pykakasi` resolves.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
CULTURE = ROOT / "reports" / "cjk-culture.csv"
UNIHAN = ROOT / "reports" / "unihan-corpus-readings.tsv"
OUT = ROOT / "reports" / "japanese-in-zh.tsv"

# See scripts/build-han-readings.py: never write these boundaries as literal characters.
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")


def norm_on(s):
    """Unihan `kJapaneseOn` is romaji -- `KOU`, `CHIN`, `RYUU`. Uppercase it and drop the
    apostrophe some readings carry, so it compares against `pykakasi`'s `hepburn`."""
    return s.upper().replace("'", "").replace("-", "")


def main() -> int:
    for p in (CULTURE, UNIHAN):
        if not p.exists():
            print("no %s" % p.relative_to(ROOT), file=sys.stderr)
            return 1
    try:
        import pykakasi
    except Exception as exc:                                          # noqa: BLE001
        print("pykakasi is required for this measurement: %s" % exc, file=sys.stderr)
        return 1
    kks = pykakasi.kakasi()

    onyomi = {}
    with io.open(UNIHAN, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            if r.get("kJapaneseOn"):
                # A character may list several on'yomi; any of them matching means fallback.
                onyomi[r["han"]] = [norm_on(x) for x in r["kJapaneseOn"].split()]
    print("%s characters carry an on'yomi" % format(len(onyomi), ","))

    # **The clan seats have to go first or they dominate the answer.** A 郡望 is a Chinese
    # commandery sitting in the surname slot -- 南蘭陵, 太原, 清河, 渤海 -- and `pykakasi` resolves
    # many of them as ordinary Japanese words or place-names (南蘭陵 MINAMIRANRYOU, 太原 TAWARA),
    # so they score as dictionary hits while being the opposite of evidence for Japanese. Before
    # this filter they were the top nine results.
    tails = collections.Counter()
    with io.open(CULTURE, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            toks = (r.get("cjk") or "").split()
            if toks:
                tails[toks[-1]] += 1
    seats = {t for t, n in tails.items() if len(t) >= 2 and n >= 20}
    print("%s repeated trailing tokens treated as clan seats" % format(len(seats), ","))

    rows, tally = [], collections.Counter()
    with io.open(CULTURE, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            culture = (r.get("culture") or "").strip()
            tally["culture=%s" % (culture or "(none)")] += 1
            if culture != "zh":
                continue
            tokens = [t for t in (r.get("cjk") or "").split()
                      if t and all(HAN.match(c) for c in t)]
            if len(tokens) < 1:
                continue
            # Geni writes given names first, so the surname is the LAST token.
            surname = tokens[-1]
            if surname in seats:
                tally["zh: the token is a clan SEAT, not a surname"] += 1
                continue
            if len(surname) > 3:
                tally["zh: surname token too long to be one"] += 1
                continue
            if len(surname) < 2:
                # See the docstring: a lone character gets its WORD reading, not a surname one.
                tally["zh: one-character surname, refused (Chinese-shaped anyway)"] += 1
                continue
            reading = "".join(x["hepburn"] for x in kks.convert(surname)).upper()
            if not reading or reading == surname:
                tally["zh: pykakasi returned nothing"] += 1
                continue
            # Every way the characters could read by on'yomi alone.
            fallbacks = {""}
            ok = True
            for ch in surname:
                cands = onyomi.get(ch)
                if not cands:
                    ok = False
                    break
                fallbacks = {a + b for a in fallbacks for b in cands}
            if not ok:
                tally["zh: a character has no on'yomi, cannot compare"] += 1
                continue
            if reading in fallbacks:
                tally["zh: on'yomi fallback -- no evidence"] += 1
                continue
            tally["zh: DICTIONARY HIT -- evidence of Japanese"] += 1
            rows.append([r.get("geni_id", ""), r.get("cjk", ""), surname, reading,
                         " ".join(sorted(fallbacks))[:40], r.get("evidence", "")[:60]])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "cjk", "surname", "pykakasi_reading",
                    "onyomi_fallback", "walk_evidence"])
        w.writerows(sorted(rows, key=lambda x: (x[2], x[0])))

    zh_total = tally["culture=zh"]
    hits = tally["zh: DICTIONARY HIT -- evidence of Japanese"]
    print("\nwrote %s - %s rows" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in sorted(tally.items()):
        print("   %-48s %7s" % (k, format(v, ",")))
    if zh_total:
        print("\nFLOOR on the Japanese-in-zh rate: %s of %s = %.1f%%"
              % (format(hits, ","), format(zh_total, ","), 100.0 * hits / zh_total))
        print("A dictionary miss is evidence for nothing, so the true rate is HIGHER.")
    by = collections.Counter(r[2] for r in rows)
    print("\nthe surnames driving it:")
    for name, n in by.most_common(15):
        ex = next(r for r in rows if r[2] == name)
        print("   %-6s %5s people   pykakasi=%-12s on'yomi=%s"
              % (name, format(n, ","), ex[3], ex[4][:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
