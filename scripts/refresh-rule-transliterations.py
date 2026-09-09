"""Re-derive the transliteration rows a RULE change invalidates. Hand rows are never touched.

    python scripts/refresh-rule-transliterations.py [--dry-run]

**A system to fix romanisation errors**, asked for 2026-08-29. The first case:
`Q141216408` came out **ウン・モルクク** and was hand-corrected to **ウン・モルク**.

## What was wrong, and why it was never one name

`Mørck` reads letter by letter: `m`+`ø` → モ, `r` coda → ル, `c` coda → ク, `k` coda → ク.
`ck` is one sound spelled with two letters, and `translit_no.py` had a geminate rule for
`nn`/`ll` — *identical* letters — but nothing for a digraph of *different* letters spelling one
phoneme. So every `ck` in the corpus doubled: `Falck` ファルクク, `Munck` ムンクク, `Rudbeck`
ルドベクク, `Sack` サクク, and in onset position `Sacken` サクケン. **47 tokens.**

The fix is one line in `translit_no.translit` — `ck` normalises to `k` before the walk, the same
way `aa` already normalises to `å` — and it gives the hand correction exactly: `Mørck` →
`モルク` / `莫尔克`.

## Why this script exists at all

`extend-transliterations.py` only ever ADDS: *"The hand table always wins. Every existing row is
preserved untouched."* That is right for hand rows and wrong for rule rows, which are a cached
function of an engine that can change. Without this, a rule fix corrects nothing already
written — the table keeps serving `モルクク` forever, and an error corrected on one item stays
live on every other.

**So the split is by the `note` column, and it is the whole safety story:**

* **ANY note beginning `by rule`** — recomputed. These are cache. That means `by rule`,
  `by rule, minted for the transcription batch` (15,836 rows) and `by rule, minted during the
  run` (237) alike. **The test was `note == "by rule"` until 2026-09-07 and that froze 16,071
  rows — 42% of the table — against every rule fix.** It is how the reported example survived:
  `Carl August Tigerstedt` read `ティゲルステドト`, the `-dt` rule was fixed and the refresh run,
  and that row did not move, because it is noted *minted during the run*.
* `composed by rule: …` — recomputed, same reason.
* everything else (`composed: …` off a hand stem, blank, or any hand annotation) — **untouched**.
  Those readings were checked by a person, and `CLAUDE.md` § *the entire purpose of this is to
  add* applies: a rule does not get to overwrite a human.

A row whose rule output is unchanged is left byte-identical, so the diff is exactly the rows the
rule change moved.
"""
from __future__ import annotations

import os
import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

TABLE = ROOT / "reports" / "garborg-name-transliterations.tsv"


def _suffixes():
    """`SUFFIXES` from `extend-transliterations.py`, imported rather than restated.

    The module's name carries a dash, so it cannot be imported by name. Copying the table
    here would be a second answer to *what is a patronymic suffix*, which is the failure
    `CLAUDE.md` names throughout -- one fact, one place.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "extend_transliterations", ROOT / "scripts" / "extend-transliterations.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SUFFIXES


SUFFIXES = _suffixes()


def _ko(token):
    """The Korean reading the engine gives now, or `""` when it cannot read the token."""
    try:
        from translit_ko_latin import render
        return render(token) or ""
    except Exception:
        return ""


def recompute(row, by_rule, hand):
    """The `(ja, zh, ko)` this row's note says it was derived by, recomputed now.

    **`ko` was NOT recomputed until 2026-09-07 and this file never mentioned it.** So every
    Korean value in the table was frozen at whatever it was first written as, immune to every
    later fix to `translit_ko_latin`: `Carl` still read `카르르` in the table while the engine
    had given `칼` since the `rl` collapse was added. `CLAUDE.md` § *CJK INCLUDES KOREAN* is the
    rule this quietly broke -- `ko` was being maintained as a leftover, not as a third language.
    """
    note = row.get("note") or ""
    token = row["token"]
    if note.startswith("by rule"):
        ja, zh = by_rule(token)
        return ja, zh, _ko(token)
    if note.startswith("composed by rule:"):
        for suf, sja, szh in SUFFIXES:
            if token.casefold().endswith(suf) and len(token) > len(suf) + 1:
                stem = token[: len(token) - len(suf)]
                # The note records which stem was used; a stem that has since become a hand
                # row is that row's business, and `composed:` (no "by rule") covers it.
                sja_, szh_ = by_rule(stem)
                if sja_:
                    return sja_ + sja, szh_ + szh, _ko(token)
                return None, None, None
    return None, None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would change and write nothing.")
    args = ap.parse_args()

    from translit_no import translit, table_sort_key

    # Closed before the atomic replace below: Windows will not rename over an open file.
    with TABLE.open(encoding="utf-8") as _fh:
        rows = list(csv.DictReader(_fh, delimiter="\t"))
    hand = {r["token"]: r for r in rows}
    changed, unreadable, kept = [], [], 0
    ko_only = []
    for row in rows:
        note = row.get("note") or ""
        if not (note.startswith("by rule") or note.startswith("composed by rule:")):
            # **AN ATTESTED ROW IS ATTESTED IN `ja` AND `zh`, NEVER IN `ko`.** No note in this
            # table has ever cited a Korean count -- 0 of 38,376 -- so the Korean value on an
            # "attested" row was always machine output, and skipping the whole row froze it
            # forever. `Carl` reads `카르르` here while the engine has given `칼` since the `rl`
            # collapse; `Schmidt` reads `스미드트` where Korean writes `슈미트`.
            #
            # So a row a human checked keeps its `ja` and `zh` untouched -- the rule does not
            # get to overwrite a person -- and has only its `ko` recomputed.
            if "ko " not in note and (row.get("ko") or ""):
                fresh = _ko(row["token"])
                if fresh and fresh != row["ko"]:
                    ko_only.append((row["token"], row["ko"], fresh))
                    row["ko"] = fresh
                    continue
            kept += 1
            continue
        ja, zh, ko = recompute(row, translit, hand)
        if ja is None:
            # The engine no longer reads this token. Leave the cached value rather than
            # emptying a cell -- *partial is worse than absent* is about what gets EMITTED,
            # and deleting a reading we already published would be a silent regression.
            unreadable.append(row["token"])
            continue
        # `ko` falls back to the cached value when the Korean engine cannot read the token,
        # for the same reason `ja` does: deleting a published reading is a silent regression.
        ko = ko or row.get("ko", "")
        if (ja, zh, ko) != (row["ja"], row["zh"], row.get("ko", "")):
            changed.append((row["token"], row["ja"], row["zh"], ja, zh))
            row["ja"], row["zh"], row["ko"] = ja, zh, ko

    if ko_only:
        print(f"{len(ko_only):,} attested rows had ONLY their ko re-derived "
              f"(an attestation covers ja and zh; no note has ever cited a Korean count)")
        for token, old_ko, new_ko in ko_only[:10]:
            print(f"   {token:<20}{old_ko:<18}-> {new_ko}")
    print(f"{len(rows):,} rows: {kept:,} hand-checked and untouched, "
          f"{len(changed):,} re-derived, {len(unreadable):,} no longer readable and left as-is")
    for token, oja, ozh, ja, zh in changed[:40]:
        print(f"   {token:<20}{oja:<22}-> {ja:<22}{ozh:<18}-> {zh}")
    if len(changed) > 40:
        print(f"   ... and {len(changed) - 40:,} more")
    if unreadable:
        print(f"   no longer readable: {', '.join(unreadable[:15])}")

    if args.dry_run:
        print("\n--dry-run: table untouched")
        return
    # `ko_only` counts: an attested row whose Korean was re-derived is a change to the table
    # even though its `ja` and `zh` did not move. Gating on `changed` alone computed 105 of
    # them, printed them, and wrote nothing.
    if not changed and not ko_only:
        print("\nnothing to write")
        return
    # **Columns from the file, a total sort, and an atomic replace.** This carried the same
    # `["token", "ja", "zh", "note"]` literal that truncated the table to an 18-byte header on
    # 2026-09-01, destroying 36,902 hand-built rows: the table has had a `ko` column since CJK
    # was ruled to include Korean, and `open(..., "w")` truncates before `writerows`
    # raises. A second copy of a landmine is still a landmine.
    #
    # The sort is `translit_no.table_sort_key` because **sorting has to be deterministic**,
    # ruled 2026-09-01. 738 tokens tie under `casefold` alone, and three scripts write this
    # file, so an unsorted hand-off reshuffles the ties and a content-identical rewrite shows up
    # as 36,901 changed lines.
    with TABLE.open(encoding="utf-8") as fh:
        fieldnames = fh.readline().rstrip(chr(10)).rstrip(chr(13)).split(chr(9))
    for r in rows:
        for k in r:
            if k not in fieldnames:
                fieldnames.append(k)
    rows.sort(key=table_sort_key)
    tmp = TABLE.with_name(TABLE.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", restval="")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, TABLE)
    print(f"\nwrote {TABLE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
