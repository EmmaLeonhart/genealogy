"""Per-person kana / Korean / Mandarin readings, as ALIASES rather than labels.

    py scripts/build-cjk-reading-labels.py

**Emma, 2026-09-02**, on why these are aliases and not labels: *"there would be `Amul` labels for
the rest — for the other two, or even `Amul` for all of them — and the `mul` one is set later."*

That is the whole design and it is what takes the culture classifier off the critical path. Every
reading a person's characters can have is emitted as an `Amul` alias. **Which one is promoted to
the `mul` label is a separate, later, one-line decision** — takeable per person, by hand or
agentically, and movable afterwards without rebuilding anything. A culture verdict that is wrong
now costs a reordering, not a wrong name and not a missing one.

## Why the Sino-Korean reading is a correct alias for EVERYONE, not only Koreans

The hanja reading is what the characters *say* in Korean, whoever bore them. So 陳恕 reads 진서
and 青山幸豊 reads 청산행풍 — both true, both findable, and an alias exists to be findable:
`CLAUDE.md` § *A nickname alias carries the SURNAME* quotes `Help:Aliases`, *"the purpose of
aliases is only to find entities in searches"*.

**It is the right `mul` only for Korean people.** Korean convention writes a modern Japanese name
by its Japanese reading in Hangul — 아오야마 유키토요, not 청산행풍 — so promoting the hanja
reading for a Japanese person would be wrong. That is exactly the decision this file leaves open
instead of taking.

## What is emitted and what is withheld

* **`ko`** — emitted for everyone. Mechanical, from `reports/han-readings.tsv`.
* **`ja`** — withheld unless SOURCED. `pykakasi` gets surnames right and given names wrong, so a
  row carries a kana reading only where one came from `reports/kana-readings.tsv`.
  `CLAUDE.md`: a kana reading is not derivable by rule.
* **`zh`** — no offline source; nothing is emitted and nothing is guessed.

**A person is skipped whole if any character is unreadable.** Half a name in Hangul and half in
Han is not an alias anybody can search, and § *partial is worse than absent* is the standing rule.

Writes `reports/cjk-reading-aliases.tsv`.
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
LABELS = ROOT / "reports" / "derived-labels.csv"
READINGS = ROOT / "reports" / "han-readings.tsv"
KANA = ROOT / "reports" / "kana-readings.tsv"
OUT = ROOT / "reports" / "cjk-reading-aliases.tsv"

#: **Never write these boundaries as literal characters.** U+F900 CJK COMPATIBILITY
#: IDEOGRAPH and U+8C48 render identically, and NFC normalisation maps the first to the
#: second -- so a literal range silently becomes U+8C48-U+FAFF, which swallows the whole
#: Hangul Syllables block. Measured 2026-09-02: 358 Hangul characters counted as Han and
#: 5,350 Korean people dropped as unreadable when their names needed no conversion at all.
#: The escapes cannot be normalised; the literal form did not survive one edit round-trip.
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")
HANGUL = re.compile(r"^[가-힣]+$")

#: A token that is not a name, taken from `scripts/build-cjk-romanisation.py`'s measured
#: vocabulary rather than invented here. `某` is *a certain one*, the exact sense of `NN`;
#: `氏` alone is the clan marker, so `氏 鄭` is an unnamed woman **of the Zheng clan**.
CJK_MARKERS = {"氏", "某", "未知", "佼名", "無名", "未詳"}

#: A dynasty or a collective ancestor standing where a name goes. `大唐帝國` is *the Great Tang
#: Empire* and `隋朝列祖列宗` is *the assembled ancestors of the Sui* — placeholders somebody
#: entered on Geni to hang a lineage from, not people with names. The clan-seat rule does not
#: reach them because it looks at the TRAILING token and these lead.
DYNASTY_TOKENS = {"大唐帝國", "隋朝列祖列宗"}

#: A token ending in one of these is a **relationship, not a name** — `室`/`妻` *wife of*,
#: `母` *mother of*, `女` *daughter of*. `信秀側室 織田` is not a woman called
#: Nobuhide-sokushitsu; it is Nobuhide's concubine, recorded by whose concubine she was.
RELATIONAL_SUFFIX = ("室", "妻", "母", "女")

#: …except where the ending IS part of her own name. `刀自古郎女 蘇我` is Soga no Tojiko no
#: Iratsume and `手白香皇女` is Princess Tashiraka — `郎女` and `皇女` sit after a woman's own
#: name where `室` and `妻` sit after her husband's.
NAME_BEARING_SUFFIX = ("皇女", "郎女", "郞女", "采女")


def clan_seats(tails):
    """The 郡望 — a commandery and county a clan claims, which belongs to nobody in particular.

    **Derived, not listed**, exactly as `build-cjk-romanisation.py` derives it: a trailing token
    of four Han characters occurring 20 or more times across the corpus. 隴西狄道 appears 1,253
    times and 陳郡陽夏 thousands more; reading them gives every member of a lineage the same
    place glued to their name — `진군양하` on 3,000 people who were not called that.
    """
    return {t for t, n in tails.items() if len(t) == 4 and n >= 20}


def main() -> int:
    for p in (LABELS, READINGS):
        if not p.exists():
            print("no %s" % p.relative_to(ROOT), file=sys.stderr)
            return 1

    ko_of = {}
    with io.open(READINGS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            if r["ko"]:
                ko_of[r["han"]] = r["ko"]
    print("%s characters carry a Korean reading" % format(len(ko_of), ","))

    # Sourced kana, per person. Never pykakasi: see the docstring.
    kana_of = {}
    if KANA.exists():
        with io.open(KANA, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=TAB):
                if r.get("reading") and r.get("state") in ("reading", "variants"):
                    kana_of[r["geni_id"]] = r["reading"]
        print("%s people carry a SOURCED kana reading" % format(len(kana_of), ","))

    # One pass to measure the clan seats, a second to read. The seat set is a property of the
    # corpus, so it cannot be known until the corpus has been walked once.
    tails = collections.Counter()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            toks = (row.get("cjk_names") or "").split()
            if toks:
                tails[toks[-1]] += 1
    seats = clan_seats(tails)
    print("%s clan seats identified" % format(len(seats), ","))

    def is_name_token(t):
        """Whether `t` is part of what the person was CALLED."""
        if not t or t in CJK_MARKERS or t in seats or t in DYNASTY_TOKENS:
            return False
        if t.endswith(NAME_BEARING_SUFFIX):
            return True
        return not (len(t) > 1 and t.endswith(RELATIONAL_SUFFIX))

    rows, tally = [], collections.Counter()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            raw = (row.get("cjk_names") or "").strip()
            if not HAN.search(raw):
                continue
            geni = row["geni_id"]
            tokens = [t for t in raw.split() if is_name_token(t)]
            # A token that is not wholly Han is not this file's business -- kana, Hangul and
            # Latin already carry their own reading.
            han_tokens = [t for t in tokens if t and all(HAN.match(c) for c in t)]
            if not han_tokens:
                tally["no Han token left after markers and seats"] += 1
                continue
            missing = [c for t in han_tokens for c in t if c not in ko_of]
            if missing:
                tally["a character has no Korean reading, skipped whole"] += 1
                continue
            ko = " ".join("".join(ko_of[c] for c in t) for t in han_tokens)
            if not HANGUL.match(ko.replace(" ", "")):
                tally["Korean form is not all Hangul, refused"] += 1
                continue
            tally["ko emitted"] += 1
            ja = kana_of.get(geni, "")
            if ja:
                tally["ja emitted (sourced)"] += 1
            rows.append([geni, row.get("qid", ""), raw, " ".join(han_tokens), ko, ja, ""])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "cjk_names", "han_tokens", "ko", "ja_sourced", "zh"])
        w.writerows(rows)

    print("\nwrote %s - %s people" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-46s %6s" % (k, format(v, ",")))
    print("   %-46s %6s" % ("zh emitted", 0))
    with_qid = sum(1 for r in rows if r[1])
    print("\n%s of them already have a Wikidata item, so the alias is addable today"
          % format(with_qid, ","))
    print("\na sample:")
    for r in rows[:10]:
        print("   %-22s %-16s -> %s" % (r[0], r[3][:16], r[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
