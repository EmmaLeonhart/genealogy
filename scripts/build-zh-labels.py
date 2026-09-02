"""The `zh` step: a Chinese label for every individual, or `unknown`.

    py scripts/build-zh-labels.py

**Her order, `queue.md` § LABELS:** `en`, then `mul`, then `ja`, then **`zh`**, then the rest —
each one step over the whole population. This is the last of the four she named individually.

## The three populations, and they need different things

* **A Han name is already Chinese.** Emma: *"If the name is solely in kanji, then the Chinese and
  Japanese labels are both the same for it."* Written as it stands, exactly as the `ja` step does.
* **A Latin name is TRANSCRIBED into Han characters** — 约翰·史密斯 for John Smith. Chinese has
  no katakana, so a foreign name is written with characters chosen for their sound. That choice is
  conventional, not derivable, so it is **read from Wikidata's own name items** and never
  generated — the same rule and the same source as the `ja` step's katakana.
* **A kana name needs a real Chinese form** and does not have one here. Those are reported, not
  invented: kana carries no Han reading, so there is nothing to carry across.

## Why the separator differs from `ja`

Japanese joins the parts of a foreign name with `・` U+30FB KATAKANA MIDDLE DOT; Chinese uses
`·` U+00B7 MIDDLE DOT. `CLAUDE.md` § *A middle initial keeps its Latin letter* shows both forms
of the same name — ジョン・F・スミス against 约翰·F·史密斯 — and they are different characters.

**A partly-transcribed name is not emitted**, per § *partial is worse than absent*. The one
exception is a middle initial, which keeps its Latin letter in every language.

Writes `reports/label-zh.tsv`.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

import labels as L  # noqa: E402

TAB = chr(9)
DERIVED = ROOT / "reports" / "derived-labels.csv"
NAME_ITEMS = ROOT / "out" / "wikidata" / "name-items-in-store.tsv"
OUT = ROOT / "reports" / "label-zh.tsv"

# Escapes, never literal boundary characters -- see scripts/build-han-readings.py.
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")
HAN_ONLY = re.compile(r"^[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u00B7\u30FB]+$")
KANA = re.compile(r"[\u3040-\u309F\u30A0-\u30FF]")
LATIN_TOKEN = re.compile(r"^[A-Za-zÀ-ɏ'.-]+$")

#: Chinese joins the parts of a foreign name with U+00B7, NOT the katakana middle dot.
MIDDLE_DOT = "·"


def han_table():
    """`{latin token casefolded: han transcription}` from Wikidata's name items."""
    table = {}
    if not NAME_ITEMS.exists():
        return table
    with io.open(NAME_ITEMS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            labs = [x for x in (r.get("labels") or "").split("|") if x]
            han = [x for x in labs if HAN_ONLY.match(x) and not KANA.search(x)]
            if not han:
                continue
            # **The FIRST Latin label only.** Keying every one was measured on the `ja` step and
            # is garbage: `sayaka`, `solovjev` and `muhàmmad` all resolved to the same value.
            for lat in labs:
                if LATIN_TOKEN.match(lat):
                    table.setdefault(lat.casefold(), han[0])
                    break
    return table


def main() -> int:
    if not DERIVED.exists():
        print("no %s" % DERIVED.relative_to(ROOT), file=sys.stderr)
        return 1
    table = han_table()
    print("%s Latin tokens carry a sourced Han transcription" % format(len(table), ","))
    if not table:
        print("no name-item table; nothing can be transcribed", file=sys.stderr)
        return 1
    pairs = {k: (v, v) for k, v in table.items()}

    rows, tally = [], collections.Counter()
    with io.open(DERIVED, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            cjk = (r.get("cjk_names") or "").strip()
            en = (r.get("label_en") or "").strip()

            if cjk and HAN.search(cjk) and not KANA.search(cjk):
                tally["from the Han name, written as it stands"] += 1
                rows.append([g, r.get("qid", ""), cjk, en, "from the Han name, as written"])
                continue
            if cjk and KANA.search(cjk):
                # Kana carries no Han reading, so there is nothing to carry across and
                # nothing here will invent one.
                tally["unknown: the name is kana, which needs a real Chinese form"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: kana name"])
                continue
            if not en:
                tally["unknown: no English label to transcribe"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: no English label"])
                continue

            toks = en.split()
            if not all(LATIN_TOKEN.match(t) for t in toks):
                tally["unknown: the label is not plain Latin"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: not plain Latin"])
                continue

            out = []
            for t in toks:
                _ja, zh = L.transliterate_token(t.casefold(), pairs)
                if zh is None:
                    _ja, zh = L.transliterate_token(t, pairs)
                out.append(zh)
            if all(out):
                tally["transcribed into Han characters"] += 1
                rows.append([g, r.get("qid", ""), MIDDLE_DOT.join(out), en,
                             "transcribed into Han characters"])
            elif any(out):
                tally["unknown: only SOME tokens transcribe, so none is emitted"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: only some tokens transcribe"])
            else:
                tally["unknown: no token has a Han transcription"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: no token transcribes"])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "label_zh", "label_en", "state"])
        w.writerows(rows)

    print("\nwrote %s - %s people" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-56s %9s" % (k, format(v, ",")))
    got = sum(1 for r in rows if r[2])
    print("\n%s carry a zh label; %s are unknown and rostered"
          % (format(got, ","), format(len(rows) - got, ",")))
    print("%s of the labelled ones already have a Wikidata item"
          % format(sum(1 for r in rows if r[1] and r[2]), ","))
    print("\na sample of the transcriptions:")
    n = 0
    for r in rows:
        if r[4] == "transcribed into Han characters":
            print("   %-34s -> %s" % (r[3][:34], r[2]))
            n += 1
            if n >= 10:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
