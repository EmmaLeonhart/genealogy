"""Every edit in a batch is on an item in the universe, or one step beyond it. Stdlib only.

    python scripts/check-batch-locality.py        # exits 1 if any batch is bad

⛔ **THIS EXISTS BECAUSE THE RULE WAS BROKEN AND NOTHING NOTICED.** On 2026-09-18 nine `ja` labels
were written onto `Q135525010`, `Q135579354` and seven more — Jan-1 entry points, outside the
universe, inactive until 2027-01-01 — and were reverted by hand one at a time. Behind them sat
936, 962 and 985 more non-local lines in the three day batches, on 300, 321 and 348 items.

`CLAUDE.md` § *AN EDIT GOES ON AN ITEM IN THE UNIVERSE, OR ONE STEP BEYOND IT. ALL EDITS, NO
EXCEPTIONS.*

## ⛔ STDLIB ONLY, BECAUSE `pipeline.yml` INSTALLS NOTHING

The first version of this guard was a pytest step in `pipeline.yml`. It failed on run
`35329948498` with `No module named pytest` — that workflow is stdlib-only and has no
`pip install` anywhere. The guard failed CLOSED, which is right, but it had not checked anything:
a gate that cannot run is not a gate, and one that reports failure without looking is worse than
one that is absent, because the next person reads the red tick as evidence.

## ⛔ ONE IMPLEMENTATION, TWO CALLERS

`pipeline.yml` runs this script; `tests/test_batch_locality.py` calls the same functions. Writing
the check twice is how `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* happens, and this
night is made of exactly that mistake: the locality gate was written for the sender, then for
`derived_labels`, then for `lines`, and leaked each time because each was a path rather than the
output.

## What is checked

1. **No batch line may name a subject outside the universe and its ring.** `CREATE` and its
   `LAST` lines carry no QID and are picked from inside the universe by `compose` already.
2. **No label edit on an item whose LIVE `ja` label is kanji.** `CLAUDE.md` § *THE KANJI SIGNAL
   DECIDES WHICH LABEL UNIVERSE A PERSON IS IN*: kanji means a Sinosphere name and a different
   universe of labels, so no label edit in any language; katakana or blank means ours. A regnal
   numeral is stripped first — the generation kanji after a digit is how an ordinal is written,
   so `アダルベルト2世` is Adalbert II in katakana and not a Sinosphere name at all.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import wikidata_lockout  # noqa: E402 -- NEVER_EDIT lives there, one definition, three readers

ROOT = pathlib.Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "out" / "wikidata" / "edit-universe.json"
LIVE_LABELS = ROOT / "reports" / "garborg-live-labels.tsv"
BATCHES = ("reports/wikidata-garborg-day.txt",
           "reports/wikidata-garborg-day-auto.txt",
           "reports/wikidata-garborg-day-manual.txt")

SUBJECT = re.compile(r"^(Q\d+)\t")
LABEL_EDIT = re.compile(r"^(Q\d+)\t[LAD](?:mul|en|ja|zh|ko)\t")
#: The Han ranges as ASCII escapes. `CLAUDE.md` § *Write a Han range as ASCII escapes* — the
#: literal form ate the Hangul block and cost 5,338 Korean people.
HAN = re.compile("[一-鿿㐀-䶿豈-﫿]")
#: A digit followed by the generation kanji is an ordinal, not a Sinosphere name.
ORDINAL = re.compile("[0-9]+世")


def universe():
    """`{qid}` for the universe and its one-step ring, or `None` when it cannot be read."""
    if not UNIVERSE.exists():
        return None
    d = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    allowed = set(d.get("universe") or ()) | set(d.get("one_step") or ())
    return allowed or None


def kanji_items():
    """`{qid}` whose LIVE `ja` label is kanji once a regnal ordinal is stripped."""
    if not LIVE_LABELS.exists():
        return set()
    out = set()
    for row in LIVE_LABELS.read_text(encoding="utf-8").split("\n"):
        p = row.split("\t")
        if len(p) >= 3 and p[1] == "ja" and HAN.search(ORDINAL.sub("", p[2] or "")):
            out.add(p[0])
    return out


def offenders(path, allowed, kanji):
    """`(non_local, on_kanji, never)` -- all three `{qid: first line number}`."""
    non_local, on_kanji, never = {}, {}, {}
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        m = SUBJECT.match(line)
        if m and m.group(1) not in allowed:
            non_local.setdefault(m.group(1), n)
        k = LABEL_EDIT.match(line)
        if k and k.group(1) in kanji:
            on_kanji.setdefault(k.group(1), n)
        if m and m.group(1) in wikidata_lockout.NEVER_EDIT:
            never.setdefault(m.group(1), n)
    return non_local, on_kanji, never


def strip(path, allowed, kanji) -> int:
    """Delete the offending lines from `path` in place. Returns how many went.

    ⛔ **THE COMPOSER'S GATE CANNOT SEE THE GROWTH PASSES, AND THAT IS WHY THIS EXISTS.**
    `build-garborg-day.refuse_non_local` runs over the assembled file and is correct at the
    moment it runs -- but `pipeline.yml` then `cat`s three universe-growth passes onto all three
    day files afterwards, ungated. On run 35398258982 that put 7 items past the gate and the
    locality CHECK then failed the whole run, so the batch was composed, refused and thrown
    away, every single day.

    Checking after the last append is not enough: a check can only fail the run, and failing the
    run is what has kept the composed batch from ever landing. So the same rule is applied as a
    FILTER at the same point, and the check that follows it then passes on merit.

    `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* -- one rule, in one file, with the
    check and the filter reading it together.
    """
    lines = path.read_text(encoding="utf-8").split(chr(10))
    keep, dropped = [], []
    for line in lines:
        m = SUBJECT.match(line)
        k = LABEL_EDIT.match(line)
        if m and (m.group(1) not in allowed
                  or m.group(1) in wikidata_lockout.NEVER_EDIT):
            dropped.append(m.group(1)); continue
        if k and k.group(1) in kanji:
            dropped.append(k.group(1)); continue
        keep.append(line)
    if dropped:
        path.write_text(chr(10).join(keep), encoding="utf-8")
        names = sorted(set(dropped))
        print("%s: STRIPPED %d line(s) on %d item(s): %s%s"
              % (path.name, len(dropped), len(names), ", ".join(names[:8]),
                 " ..." if len(names) > 8 else ""))
    return len(dropped)


def main() -> int:
    fix = "--fix" in sys.argv
    allowed = universe()
    if allowed is None:
        print("REFUSING TO PASS: out/wikidata/edit-universe.json is missing or empty, so "
              "locality cannot be checked. That is the absence of the gate, not permission.")
        return 1
    kanji = kanji_items()
    bad = 0
    for rel in BATCHES:
        path = ROOT / rel
        if not path.exists():
            print("%-44s not built, skipped" % rel)
            continue
        if fix:
            strip(path, allowed, kanji)
        non_local, on_kanji, never = offenders(path, allowed, kanji)
        if non_local:
            bad = 1
            print("%s: %d item(s) neither in the universe nor one step beyond it, first at line "
                  "%d: %s" % (rel, len(non_local), min(non_local.values()),
                              ", ".join(sorted(non_local)[:8])))
        if on_kanji:
            bad = 1
            print("%s: label edits on %d item(s) whose ja label is KANJI, which marks a "
                  "Sinosphere name and takes no label edit in any language: %s"
                  % (rel, len(on_kanji), ", ".join(sorted(on_kanji)[:8])))
        if never:
            bad = 1
            print("%s: %d edit(s) on an item this pipeline may NEVER touch again, first at "
                  "line %d: %s -- scripts/wikidata_lockout.NEVER_EDIT"
                  % (rel, len(never), min(never.values()), ", ".join(sorted(never))))
        if not non_local and not on_kanji and not never:
            print("%-44s clean (universe %d, kanji items %d)" % (rel, len(allowed), len(kanji)))
    if bad:
        print("\nCLAUDE.md: AN EDIT GOES ON AN ITEM IN THE UNIVERSE, OR ONE STEP BEYOND IT. "
              "ALL EDITS, NO EXCEPTIONS.")
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
