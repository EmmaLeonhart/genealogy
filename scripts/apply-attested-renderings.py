"""Let what Wikidata's own editors wrote beat what our rule engine guessed.

    py scripts/apply-attested-renderings.py

**Emma, 2026-09-01, on `Stephen`:** *"斯特普亨·弗里斯克 — this is a terrible rendering of Stephen
Frisk lol"*, and then *"This is what I've found for stephen 史蒂芬"*.

She is right and the cause is not the engine. `reports/attested-name-renderings.tsv` already holds
**Stephen → スティーヴン (85 uses) / 斯蒂芬 (26 uses)**, harvested from real Wikidata labels — and
`reports/garborg-name-transliterations.tsv` carried the by-rule `ステプヘン` / `斯特普亨` anyway.
**The attested file was built and never applied.** That is the *"logic that never gets in"* shape
`CLAUDE.md` records, in the data layer rather than the code.

## What it does

For every token whose `note` says **`by rule`**, if the attested file has a non-empty rendering,
that rendering replaces ours and the count is recorded. **2,035 tokens have a `ja` attestation
that differs from ours**, and reading them the attested one is plainly better nearly every time:

    Aaron      オーロン  ->  アーロン        61 uses
    Abdullah   アブドラ  ->  アブドゥッラー    12 uses      阿布杜拉 -> 阿卜杜拉
    Aarne      オールネ  ->  アールネ         5 uses      奥尔内   -> 阿尔内

**A middle initial is among them and it is the sharpest case.** `A` renders by rule as `ア`; the
attested value is `A`, 146 uses — which is exactly what `CLAUDE.md` § *A middle initial keeps its
Latin letter in every language* already requires, arrived at independently by Wikidata's editors.

## What it does NOT do

**It never touches a row that is not `by rule`.** A hand entry, a patronymic construction, or a
value Emma has corrected stays exactly as it is — attestation is evidence, not authority over her.

**It does not overwrite with an empty value.** Many tokens are attested in `ja` and not in `zh`;
those keep the by-rule `zh` rather than losing it.

**No threshold.** A rendering used even twice was written by a person looking at that name, where
ours was assembled letter by letter with no idea what the name is. Her standing rule is that an
imperfect katakana reading is acceptable and an incorrect *name* is not — and `斯特普亨` for
Stephen is closer to a wrong name than to an imperfect reading. The use count is written into the
`note` so any row can be argued with.

Rewrites `reports/garborg-name-transliterations.tsv` in place.
"""

from __future__ import annotations

import os
import collections
import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TAB = chr(9)
sys.path.insert(0, str(REPO / "scripts"))
from translit_no import table_sort_key  # noqa: E402

TABLE = REPO / "reports" / "garborg-name-transliterations.tsv"
ATTESTED = REPO / "reports" / "attested-name-renderings.tsv"

#: Any note beginning "by rule" is the engine talking and is replaceable. Matching exact
#: strings meant the 18,295 tokens minted for the transcription batch -- note
#: "by rule, minted for the transcription batch" -- were skipped wholesale on the first
#: run, which is the same brittleness as listing relations beside a table instead of
#: deriving them from it.
BY_RULE_PREFIX = "by rule"

#: Her own corrections, which outrank both the engine and the attestation. She looked `Stephen`
#: up and gave `史蒂芬`; Wikidata attests `斯蒂芬` 26 times. Both are standard and hers wins,
#: because `CLAUDE.md` § *Emma edits the tree and the items BY HAND* makes a value she has
#: supplied a decision rather than drift.
HERS = {
    "Stephen": {"zh": "史蒂芬"},
}


def main() -> int:
    # Both readers are closed before the atomic replace below: Windows refuses to rename over
    # a file it still has open, which is how os.replace first died with WinError 5.
    with io.open(ATTESTED, encoding="utf-8") as fh:
        att = {r["token"]: r for r in csv.DictReader(fh, delimiter=TAB)}
    with io.open(TABLE, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter=TAB))
    fields = ["token", "ja", "zh", "ko", "note"]

    n = collections.Counter()
    changed = []
    for r in rows:
        if not (r.get("note") or "").startswith(BY_RULE_PREFIX):
            n["left alone -- not a by-rule row"] += 1
            continue
        a = att.get(r["token"])
        mine = HERS.get(r["token"], {})
        if not a and not mine:
            n["left alone -- no attestation"] += 1
            continue
        before = (r["ja"], r["zh"])
        used = []
        for lang in ("ja", "zh"):
            new = mine.get(lang) or (a or {}).get(lang, "")
            if new and new != r[lang]:
                r[lang] = new
                used.append(lang)
        if not used:
            n["attested but identical to ours"] += 1
            continue
        src = ("Emma" if mine else
               f"attested on Wikidata (ja {(a or {}).get('ja_count', '?')}x, "
               f"zh {(a or {}).get('zh_count', '?')}x)")
        r["note"] = src
        n[f"replaced: {'+'.join(used)}"] += 1
        if len(changed) < 15:
            changed.append((r["token"], before, (r["ja"], r["zh"]), src))

    # **Deterministic order, and an atomic replace.** Emma, 2026-09-01: *"sorting needs to be
    # deterministic"*. This wrote in input order while `extend-transliterations.py` sorted, so
    # every hand-off between the two reshuffled the 738 tokens that tie under `casefold` — and a
    # rewrite that changed nothing at all came out as 36,901 changed lines in `git diff`. A diff
    # that noisy hides the change you actually need to see.
    rows.sort(key=table_sort_key)
    tmp = TABLE.with_name(TABLE.name + ".tmp")
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter=TAB, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    os.replace(tmp, TABLE)

    for k, v in n.most_common():
        print(f"  {v:>7,}  {k}")
    print("\na sample of what changed:")
    for tok, b, a_, src in changed:
        print(f"   {tok:<14} {b[0]:<14} -> {a_[0]:<14}   {b[1]:<12} -> {a_[1]:<12}  {src[:34]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
