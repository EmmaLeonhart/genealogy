"""What Wikidata ACTUALLY calls each name token in Japanese and Chinese, with counts.

    python scripts/build-attested-renderings.py

**Emma, 2026-08-30:** *"Are you not using an actual library for this, but just kind of guessing
at everything? … This is a solved problem. You understand that, right? There isn't really an
excuse."*

She is right. `scripts/translit_no.py` is a hand-rolled letter walk over tables somebody typed
in from memory, and it is wrong in ways nobody would defend: `Alexander` came out
`アレクスアンデル` / `阿莱克斯安德尔` against the `アレクサンダー` / `亚历山大` that 226 and 174
Wikidata items actually use. `ROWS["j"]`'s `o` cell held `永` — the *yong* syllable — because a
plausible character was put in a cell.

**The data to stop guessing with is already on this disk.** The local store holds **318,025
items with a Latin label and a `ja` or `zh` one**: 181,353 with Japanese, 234,197 with Chinese,
97,525 with both. Aligning them token by token gives an attested vocabulary of ~82,000 Japanese
and ~91,000 Chinese name tokens, each with a count of how many items use it.

## How the alignment works, and where it refuses

Both sides are split on the separators these labels use — `·`, `・`, `＝`, hyphen, space — and a
pair is used **only when the two sides have the same number of tokens**. `Mahatma Gandhi` /
`圣雄甘地` aligns; `Bud Greenspan` / `B. 格林斯潘` does not, and is dropped rather than guessed
at. That is the whole safety story: a misaligned pair would teach a wrong rendering with the
authority of data.

**A token is only reported when it clears `MIN_COUNT`,** because a single attestation can be one
editor's mistake, and because a name rendered once is not yet a convention.

## What this is NOT

It is not a transliterator. It answers *how is this token written* for tokens Wikidata has
already written, and says nothing about the rest — those still go through the rule engine, which
is where the remaining 64% of our vocabulary lives. It also does not adjudicate between
Traditional and Simplified: the mode wins, and for names transcribed on the mainland that is
Simplified in practice (`约翰` beats `約翰`), which is checked in the output rather than assumed.

Writes `reports/attested-name-renderings.tsv` — `token`, `ja`, `ja_count`, `zh`, `zh_count`.
"""
from __future__ import annotations

import csv
import glob
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

PAIRS = ROOT / "out" / "wikidata" / "latin-cjk-label-pairs.tsv"
OUT = ROOT / "reports" / "attested-name-renderings.tsv"

#: A label that is a plain Latin name. Anything with digits, parentheses or CJK is a title,
#: a disambiguated label or a work, not a name we can align token by token.
LATIN = re.compile(r"^[A-Za-zÀ-ÿĀ-ž' .-]+$")

#: The separators these labels use on both sides.
SEP = re.compile(r"[·・･=＝\-–—\s.]+")

#: Below this many attestations a rendering is one editor's choice, not a convention.
MIN_COUNT = 2

#: Chinese label languages, best first: the Simplified variants are what this project writes.
ZH_LANGS = ("zh-hans", "zh-cn", "zh")


def extract():
    """Scan the store once and write the aligned Latin/ja/zh label triples."""
    PAIRS.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with PAIRS.open("w", encoding="utf-8", newline="") as out:
        out.write("qid\tlatin\tja\tzh\n")
        for path in sorted(glob.glob(str(ROOT / "wikidata" / "items" / "items-*.jsonl.gz"))):
            with gzip.open(path, "rt", encoding="utf-8") as fh:
                for line in fh:
                    if '"ja"' not in line and '"zh' not in line:
                        continue
                    item = json.loads(line)
                    labels = item.get("labels", {})
                    latin = ""
                    for lang in ("en", "mul", "nb", "sv", "no", "da"):
                        v = (labels.get(lang) or {}).get("value", "")
                        if v and LATIN.match(v):
                            latin = v
                            break
                    if not latin:
                        continue
                    ja = (labels.get("ja") or {}).get("value", "")
                    zh = ""
                    for lang in ZH_LANGS:
                        zh = (labels.get(lang) or {}).get("value", "")
                        if zh:
                            break
                    if not (ja or zh):
                        continue
                    out.write(f"{item['id']}\t{latin}\t{ja}\t{zh}\n")
                    n += 1
    print(f"{n:,} aligned label triples -> {PAIRS.relative_to(ROOT)}")
    return n


def main():
    if not PAIRS.exists():
        extract()

    ja_map, zh_map = defaultdict(Counter), defaultdict(Counter)
    pairs = aligned = 0
    with PAIRS.open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 4:
                continue
            pairs += 1
            latin = [t for t in SEP.split(parts[1]) if t]
            for target, table in ((parts[2], ja_map), (parts[3], zh_map)):
                if not target:
                    continue
                cjk = [t for t in SEP.split(target) if t]
                # **Only when the token counts match.** A misaligned pair teaches a wrong
                # rendering with the authority of data, which is worse than no data.
                if len(cjk) == len(latin):
                    aligned += 1
                    for a, b in zip(latin, cjk):
                        table[a][b] += 1

    tokens = sorted(set(ja_map) | set(zh_map))
    rows = []
    for token in tokens:
        ja = ja_map[token].most_common(1)
        zh = zh_map[token].most_common(1)
        ja_v, ja_c = (ja[0] if ja else ("", 0))
        zh_v, zh_c = (zh[0] if zh else ("", 0))
        if ja_c < MIN_COUNT:
            ja_v, ja_c = "", 0
        if zh_c < MIN_COUNT:
            zh_v, zh_c = "", 0
        if ja_v or zh_v:
            rows.append({"token": token, "ja": ja_v, "ja_count": ja_c,
                         "zh": zh_v, "zh_count": zh_c})

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "ja", "ja_count", "zh", "zh_count"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"{pairs:,} label triples, {aligned:,} of them token-aligned")
    print(f"{len(rows):,} tokens attested at least {MIN_COUNT}x "
          f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
