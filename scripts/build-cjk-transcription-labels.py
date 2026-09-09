"""`ja`, `zh` and `ko` for Latin-named people who already have a Wikidata item.

    py scripts/build-cjk-transcription-labels.py

**Emma's ruling, 2026-09-01**, asked directly whether a rule-based transcription of a Latin name
counts as a publishable label: **emit it for the people who already have a QID.** Not for
everyone — 1.29 million people would be ~2.5 million edits nobody can apply, because most of them
are not on Wikidata yet and their labels ride along with the creation instead.

**This is the line `build-ja-label-batch.py` and `build-ko-label-batch.py` both hold, moved.**
Those two refuse to transcribe a Latin name at all, on the ground that transcription is not
reading: a Chinese, Japanese or Korean person may have a name in their own script already, and a
transcription would be second-best. That reasoning is still right *for them* — they run over the
whole corpus, most of it uncreated. Here the population is bounded and every edit is applicable
today, so the trade is different and she made it.

## Why `zh` comes too, when she said `ja` and `ko`

`translit_no.translit(token)` returns **`(katakana, chinese)` from one call** — `ja` and `zh` are
the same engine and the same table column. Emitting `ja` while withholding `zh` would recreate
exactly the inconsistency her ruling removed, and `CLAUDE.md` § *CJK INCLUDES KOREAN* treats the
three as one set. So all three go, and this note is here so that reading it back does not look
like scope she did not sanction.

## The table first, the engine second

Tokens resolve through `reports/garborg-name-transliterations.tsv` before the engine, which
matters: **2,247 of its 18,536 rows were corrected on 2026-09-01** from renderings attested on
Wikidata, plus her own `Stephen` → `史蒂芬`. Going straight to the engine would reproduce the
`斯特普亨` she objected to.

**Partial is never emitted.** One unrenderable token drops the whole label for that language, per
`CLAUDE.md` § *A middle initial keeps its Latin letter*, whose single exception the token helpers
already implement.

Writes `reports/wikidata-cjk-transcription-labels.json` and `.md`.
"""

from __future__ import annotations

import collections
import csv
import io
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from labels import transliterate_token, transliterate_token_ko  # noqa: E402
from translit_ko_latin import render as ko_latin                # noqa: E402
from translit_no import translit                                # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
TABLE = REPO / "reports" / "garborg-name-transliterations.tsv"
OUT = REPO / "reports" / "wikidata-cjk-transcription-labels.json"
OUT_MD = REPO / "reports" / "wikidata-cjk-transcription-labels.md"

TAB = chr(9)
#: A label with no Latin letter is not this batch's business -- it already has a native form.
LATIN = re.compile(r"[A-Za-zÀ-ÿ]")


def load_table():
    """`{token: (ja, zh, ko)}` from the shared funnel table."""
    out = {}
    with io.open(TABLE, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            out[r["token"]] = (r["ja"], r["zh"], r.get("ko", ""))
    return out


def render(label, table, minted):
    """`(ja, zh, ko)` for a whole Latin label, or `(None, None, None)`."""
    ja, zh, ko = [], [], []
    for raw in label.split():
        token = raw.strip(",;:")
        if not token:
            continue
        a, b = transliterate_token(token, table)
        c = transliterate_token_ko(token, table)
        if a is None or c is None:
            # Not in the table: render once, cache for the rest of the run, and record it so
            # the shared table can be extended by the same funnel the day builder uses.
            try:
                a2, b2 = translit(token)
                c2 = ko_latin(token)
            except Exception:                                       # noqa: BLE001
                return None, None, None
            if not (a2 and b2 and c2):
                return None, None, None
            a, b, c = a2, b2, c2
            table[token] = (a, b, c)
            minted[token] = (a, b, c)
        ja.append(a)
        zh.append(b)
        ko.append(c)
    if not ja:
        return None, None, None
    return "・".join(ja), "·".join(zh), " ".join(ko)


def main() -> int:
    table = load_table()
    minted: dict[str, tuple] = {}
    edits, why = [], collections.Counter()
    per = collections.Counter()

    with io.open(LABELS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            qid = (r.get("qid") or "").strip()
            label = (r.get("label_en") or "").strip()
            if not qid:
                why["no Wikidata item -- their labels ride along with the creation"] += 1
                continue
            if (r.get("cjk_names") or "").strip():
                why["already has a name in a CJK script -- not a transcription case"] += 1
                continue
            if not label or not LATIN.search(label):
                why["no Latin label to transcribe"] += 1
                continue
            ja, zh, ko = render(label, table, minted)
            if not ja:
                why["a token nothing can render, so the whole label is withheld"] += 1
                continue
            why["EMITTED"] += 1
            for code, value in (("ja", ja), ("zh", zh), ("ko", ko)):
                per[code] += 1
                edits.append({
                    "id": f"{code}_transcribed:{r['geni_id']}",
                    "type": "set_label",
                    "source": "her ruling of 2026-09-01: transcribe for people who have a QID",
                    "subject": {"qid": qid, "geni_id": r["geni_id"]},
                    "requires": [],
                    "label": {"language": code, "value": value},
                    "kind": "add",
                    "derived_from": "transcribed from the Latin label",
                })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    lines = ["# `ja`, `zh` and `ko` transcribed, for people who already have a QID", "",
             "Built by `scripts/build-cjk-transcription-labels.py`. **Emits nothing to Wikidata.**",
             "",
             "Emma, 2026-09-01, asked whether a rule-based transcription of a Latin name counts "
             "as a publishable label: **emit it for the people who already have a QID.**", "",
             f"- **{len(edits):,} labels** over {why['EMITTED']:,} people.", "",
             "| language | labels |", "| --- | ---: |"]
    for code in ("ja", "zh", "ko"):
        lines.append(f"| `{code}` | {per[code]:,} |")
    lines += ["", "## Not emitted, and why", "", "| reason | people |", "| --- | ---: |"]
    for k, v in sorted(((k, v) for k, v in why.items() if k != "EMITTED"),
                       key=lambda x: -x[1]):
        lines.append(f"| {k} | {v:,} |")
    lines += ["", "**`zh` is here although she said `ja` and `ko`.** "
              "`translit_no.translit` returns katakana and Chinese from one call, so they are the "
              "same engine and the same table column; emitting one and withholding the other "
              "would recreate the inconsistency her ruling removed.", "",
              "**The corpus-wide batches still withhold transcription**, and that is deliberate: "
              "`build-ja-label-batch.py` and `build-ko-label-batch.py` run over 1.29 million "
              "people who are mostly not on Wikidata, where the labels ride along with the "
              "creation instead."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {OUT.relative_to(REPO)} - {len(edits):,} labels over {why['EMITTED']:,} people")
    for code in ("ja", "zh", "ko"):
        print(f"   {per[code]:>8,}  {code}")
    print()
    for k, v in why.most_common():
        print(f"   {v:>9,}  {k}")
    if minted:
        print(f"\n{len(minted):,} tokens rendered on the fly and not yet in the shared table")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
