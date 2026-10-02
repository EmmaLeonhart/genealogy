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
import qs_v1  # noqa: E402 -- the one module that knows what a CREATE block is

ROOT = pathlib.Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "out" / "wikidata" / "edit-universe.json"
LIVE_LABELS = ROOT / "reports" / "garborg-live-labels.tsv"
#: ⛔ **THE FAMILYSEARCH BATCH IS A BATCH.** `CLAUDE.md` § *AN EDIT GOES ON AN ITEM IN THE
#: UNIVERSE, OR ONE STEP BEYOND IT. ALL EDITS, NO EXCEPTIONS* — a separate output file is not
#: an exemption from the locality rule, it is another file that has to obey it.
#: `build-familysearch-day.py` gates its own reciprocals against the same artifact, and this
#: is the second reading of it for the reason the docstring below gives: a gate that lives
#: only in the composer is one stale artifact away from being no gate.
BATCHES = ("reports/wikidata-garborg-day.txt",
           "reports/wikidata-garborg-day-auto.txt",
           "reports/wikidata-garborg-day-manual.txt",
           "reports/wikidata-familysearch-day.txt")

SUBJECT = re.compile(r"^(Q\d+)\t")
LABEL_EDIT = re.compile(r"^(Q\d+)\t[LAD](?:mul|en|ja|zh|ko)\t")
#: `#   Q<item> <name>: ...` -- the header a backfill pass writes above an item's statements.
ANNOTATION = re.compile(r"^#   (Q\d+) ")
#: The Han ranges as ASCII escapes. `CLAUDE.md` § *Write a Han range as ASCII escapes* — the
#: literal form ate the Hangul block and cost 5,338 Korean people.
HAN = re.compile("[一-鿿㐀-䶿豈-﫿]")
#: A digit followed by the generation kanji is an ordinal, not a Sinosphere name.
ORDINAL = re.compile("[0-9]+世")


#: A court rank (P14005) line. From `wikidata_lockout.COURT_RANK_ANYONE_FROM` (2027-06-01) it may
#: go on anyone, inside the universe or not (Emma, 2026-09-26).
COURT_RANK = re.compile(r"^Q\d+\tP14005\t")


def court_rank_anywhere(line, today=None) -> bool:
    """True for a court-rank line once the date has come; such a line is never non-local."""
    return bool(COURT_RANK.match(line)) and wikidata_lockout.court_rank_anyone(today)


def universe():
    """`{qid}` for the universe and its one-step ring, or `None` when it cannot be read."""
    if not UNIVERSE.exists():
        return None
    d = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    allowed = set(d.get("universe") or ()) | set(d.get("one_step") or ())
    # The name items universe people bear, recorded by `build-garborg-name-items.py`.
    allowed |= set(d.get("name_items") or ())
    return allowed or None


#: An `NN` token in an item's `mul`/`en` label marks one of the NN items we made.
NN_TOKEN = re.compile(r"(^|\s)NN(\s|$)")


def is_our_nn(labels):
    """True when the item's `mul` or `en` label is one of our NN labels (`NN Lende`, `Ulvåse NN`)."""
    return any(NN_TOKEN.search(labels.get(lang) or "") for lang in ("mul", "en"))


def kanji_items():
    """`{qid}` whose LIVE `ja` label is kanji once a regnal ordinal is stripped.

    ⛔ Then the NN items we made are taken back out (Emma, 2026-09-30: "we can identify the labels on
    the NN items that we made and our check to see if something is one of those comes after our
    check to see if a kanji is in the name"). Their `ja` label is ours, a katakana name with a
    kinship word in kanji, and says nothing about the person being Sinosphere.
    """
    if not LIVE_LABELS.exists():
        return set()
    labels = {}
    for row in LIVE_LABELS.read_text(encoding="utf-8").split("\n"):
        p = row.split("\t")
        if len(p) >= 3:
            labels.setdefault(p[0], {})[p[1]] = p[2]
    out = {q for q, ls in labels.items() if HAN.search(ORDINAL.sub("", ls.get("ja") or ""))}
    return {q for q in out if not is_our_nn(labels[q])}


def offenders(path, allowed, kanji):
    """`(non_local, on_kanji, never)` -- all three `{qid: first line number}`."""
    non_local, on_kanji, never = {}, {}, {}
    text = path.read_text(encoding="utf-8").split("\n")
    # A relative of a person this batch creates is one hop from an edited item: in the universe.
    allowed = set(allowed) | qs_v1.creation_relatives(text)
    for n, line in enumerate(text, 1):
        m = SUBJECT.match(line)
        if m and m.group(1) not in allowed and not court_rank_anywhere(line):
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
    allowed = set(allowed) | qs_v1.creation_relatives(lines)
    keep, dropped = [], []
    for line in lines:
        m = SUBJECT.match(line)
        k = LABEL_EDIT.match(line)
        if wikidata_lockout.touches_protected(line):
            dropped.append(m.group(1) if m else "protected"); continue
        if m and ((m.group(1) not in allowed and not court_rank_anywhere(line))
                  or m.group(1) in wikidata_lockout.NEVER_EDIT):
            dropped.append(m.group(1)); continue
        if k and k.group(1) in kanji:
            dropped.append(k.group(1)); continue
        keep.append(line)
    # ⛔ **AND A STRIPPED ITEM TAKES ITS ANNOTATION WITH IT.** Reported 2026-09-24, on the Izumo
    # blocks: the backfill passes write `#   Q<item> <name>: P22 father = ...` above each item's
    # statements, with `#   P40 child = ...` continuation lines under it, and this filter took
    # the statements and left the comments -- 113 Izumo lines in every day file and on the site,
    # describing edits that were never going out. An item none of whose statements survived
    # loses its header and continuations; one that keeps a statement keeps its comments.
    live = {m.group(1) for m in map(SUBJECT.match, keep) if m}
    gone = set(dropped) - live
    if gone:
        kept, drop_block = [], False
        for line in keep:
            head = ANNOTATION.match(line)
            if head:
                drop_block = head.group(1) in gone
            elif not line.startswith("#   P"):
                drop_block = False
            if drop_block:
                continue
            kept.append(line)
        keep = kept
    # ⛔ **AND A STRIPPED LINE TAKES ITS ORPHANED CREATION WITH IT.** Ruled 2026-09-21 on three
    # live isolates: *"three isolated individuals were created."* `build-ancestor-creations.py`
    # emits a creation and exactly ONE relationship, the reciprocal `Q<child> P… LAST`. This
    # filter drops that line when the child is outside the universe and leaves the `CREATE`
    # standing, so the run mints a bare `instance of human` with nothing pointing at it —
    # `Q141529844`, `Q141529845`, `Q141529847`, all three reporting *"No pages link to"*.
    #
    # The picker no longer chooses a child outside the universe, which is the root cause; this
    # is the guard for everything else that ever appends to a batch. A filter that can orphan a
    # creation has to be able to withdraw it.
    keep, orphaned = qs_v1.drop_orphaned_creations(keep)
    if dropped or orphaned:
        path.write_text(chr(10).join(keep), encoding="utf-8")
    if dropped:
        names = sorted(set(dropped))
        print("%s: STRIPPED %d line(s) on %d item(s): %s%s"
              % (path.name, len(dropped), len(names), ", ".join(names[:8]),
                 " ..." if len(names) > 8 else ""))
    if orphaned:
        print("%s: WITHDREW %d creation(s) the strip left with no relationship at all: %s"
              % (path.name, len(orphaned), ", ".join(orphaned[:6])))
    return len(dropped) + len(orphaned)


def strip_protected() -> int:
    """Remove every line naming the owner's item or a protected Geni profile, from EVERY batch.

    Not only the day files: `wikidata-from-diff.qs` carried `Q141498271 P40 Q140568870` on
    2026-09-27, so this reads every `reports/*.qs` and `*.txt` batch. It refuses nothing else, so
    it is safe on files the locality rule does not govern. `wikidata_lockout.PROTECTED_*`.
    """
    bad = 0
    paths = sorted(set((ROOT / "reports").glob("*.qs")) | {ROOT / r for r in BATCHES})
    for path in paths:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").split(chr(10))
        keep = [l for l in lines if not wikidata_lockout.touches_protected(l)]
        if len(keep) != len(lines):
            keep, _orphaned = qs_v1.drop_orphaned_creations(keep)
            path.write_text(chr(10).join(keep), encoding="utf-8")
            bad += len(lines) - len(keep)
            print("%s: STRIPPED %d line(s) naming a protected item or Geni profile"
                  % (path.name, len(lines) - len(keep)))
    return bad


def main() -> int:
    fix = "--fix" in sys.argv
    if fix:
        strip_protected()
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
