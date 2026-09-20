"""Add our standardised CJK readings to the name items our own corpus bears.

Ruled 2026-09-14: *"Given names and surnames should have our standardized cjk-izations attached
to them. imo they should even be the source of it in the logic. update the old ones to this form
and new ones are always gonna be created in this manner"*.

`build-garborg-name-items.py` does the *new ones* half — a created name item now carries
`Lja`/`Lzh`/`Lko` beside `Len`/`Lmul`. This is the *old ones* half: the items that already exist
and were made before the rule.

**The readings come from `label_in`, which is `build-garborg-day.py`'s and stays there.** One
source, one reading. § *A GUARD IN ONE EMITTER IS NOT A GUARD* cuts both ways — a second
transliterator here would be a second answer to the same question, and the point of the ruling is
that the name item and the token table stop being two copies of one thing.

## ⛔ LOCAL. It does NOT touch all 699,287 name items on Wikidata

`reports/name-item-languages.csv` knows 823,907 name items and 699,287 of them carry no CJK at
all. Backfilling that set would be precisely the failure Emma named on 2026-09-14: *"the
quickstatements that are generated are supposed to be local, but they're not local ... having
stuff that leaks out from the universe and into just random areas ... is an intrinsic risk"*.

So the scope is the name items **our corpus actually bears** — the rows of
`reports/name-item-plan.csv` that carry an `existing_qid`. 8,006 items, 7,930 of them with a
language row, 7,516 missing at least one reading:

    missing ko only      3108      missing zh,ko         867
    missing ja,zh,ko     2486      missing zh only        24
    missing ja,ko        1003      missing ja only        18

Korean being the largest single gap is not a surprise: § *The gate is `ja` + `zh` + `ko`. CJK
INCLUDES KOREAN* was added on 2026-09-01, after most of these items existed.

## ⛔ PURELY ADDITIVE

A language that already has a label is never touched. `Lja` REPLACES, and replacing is how 110
live CJK labels were overwritten on 2026-09-14 — Q236972 Fuxi among them, whose correct 伏羲 was
buried under a letter-by-letter katakanisation of a romanisation. § *Wikidata's label beats ours*.
Emitting only into an empty slot is what makes `L` safe here.

All three readings or none, per the gate: `label_in` returns `(None, None, None)` for a token it
cannot read, and half a name in katakana is not a Japanese label. A token already holding `ja`
but missing `ko` still gets only its `ko` written.

    PYTHONPATH=src python scripts/build-name-item-cjk.py

Writes `reports/wikidata-name-item-cjk.qs`. Offline; reads the committed CSVs and nothing else.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLAN = REPO / "reports" / "name-item-plan.csv"
LANGS_DIR = REPO / "reports"
OUT = REPO / "reports" / "wikidata-name-item-cjk.qs"


#: The census is sixteen shards now -- `measure-name-item-languages.py` says why, and the
#: short version is that one tracked file over 100 MB refuses EVERY push to the repo. Every
#: reader here scans the whole census, so it needs the concatenation and not the shard rule.
def _language_rows(folder):
    for path in sorted(folder.glob("name-item-languages-*.csv")):
        with path.open(encoding="utf-8", newline="") as fh:
            yield from csv.DictReader(fh)

#: The same per-run ceiling every other label edit answers to, read from the composer so the
#: two cannot drift. § *Caps:* `LABEL_EDIT_CAP`.
CAPS_FROM = REPO / "scripts" / "build-garborg-day.py"

CJK = ("ja", "zh", "ko")


def _day():
    """`build-garborg-day.py`, loaded by path — the filename is not importable as a module."""
    spec = importlib.util.spec_from_file_location("garborg_day", str(CAPS_FROM))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def our_name_items():
    """`{qid: token}` for the name items this corpus actually bears."""
    out = {}
    with PLAN.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            qid = (row.get("existing_qid") or "").strip()
            token = (row.get("token") or "").strip()
            if qid.startswith("Q") and token:
                out[qid] = token
    return out


def live_languages(wanted):
    """`{qid: {lang: label}}` for the wanted qids, from the committed census."""
    out = {}
    for row in _language_rows(LANGS_DIR):
        qid = row.get("qid")
        if qid in wanted:
            out[qid] = {k: (row.get(k) or "").strip() for k in CJK}
    return out


def main() -> int:
    csv.field_size_limit(10 ** 7)
    day = _day()
    table = day.translit()
    cap = day.LABEL_EDIT_CAP

    ours = our_name_items()
    live = live_languages(set(ours))

    lines = [
        "# CJK readings for the name items this corpus bears.",
        "# Ruled 2026-09-14: our standardised cjk-izations belong on the given names and",
        "# surnames themselves. PURELY ADDITIVE -- a language already holding a label is",
        "# never written. Readings from build-garborg-day.label_in, the one source.",
        "",
    ]
    reasons = Counter()
    written = 0
    # deterministic: most-borne first, then the qid. § *SORTING MUST BE DETERMINISTIC*
    bearers = {}
    with PLAN.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            qid = (row.get("existing_qid") or "").strip()
            if qid.startswith("Q"):
                bearers[qid] = max(bearers.get(qid, 0), int(row.get("bearers") or 0))

    for qid in sorted(ours, key=lambda q: (-bearers.get(q, 0), q)):
        if written >= cap:
            reasons["held for a later run (cap)"] += 1
            continue
        token = ours[qid]
        have = live.get(qid)
        if have is None:
            reasons["no language row in the census"] += 1
            continue
        gaps = [lang for lang in CJK if not have[lang]]
        if not gaps:
            reasons["already has all three"] += 1
            continue
        ja, zh, ko = day.label_in(token, table)
        if not ja:
            reasons["the table cannot read this token"] += 1
            continue
        reading = {"ja": ja, "zh": zh, "ko": ko}
        lines.append(f"# {qid} {token} -- adding {', '.join(gaps)}"
                     f" ({bearers.get(qid, 0)} bearer(s))")
        for lang in gaps:
            lines.append(f'{qid}\tL{lang}\t"{reading[lang]}"')
        written += 1
        reasons["written"] += 1

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(ours)} name items this corpus bears; {written} written to "
          f"{OUT.relative_to(REPO)} (LABEL_EDIT_CAP {cap})")
    for reason, n in reasons.most_common():
        print(f"  {n:>6}  {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
