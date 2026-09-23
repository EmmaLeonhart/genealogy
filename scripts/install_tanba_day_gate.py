"""Idempotently wire the Tanba final gate + Given-NN usable() fix into build-garborg-day.py.

    python scripts/install_tanba_day_gate.py

Ruled 2026-09-22: day QuickStatements must not edit Tanba people.
Also: reject Given-NN relatives (Margreta NN) so CI describe_all stays clean.

Prefers `from tanba_batch_block import tanba_blocked_qids` (not an inline copy).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "scripts" / "build-garborg-day.py"

IMPORT_LINE = (
    "from tanba_batch_block import tanba_blocked_qids  "
    "# noqa: E402 — day batch must never edit Tanba\n"
)

OLD_EXCLUDED = "    excluded = set(KLUGE_UNIVERSE_BLOCK) | set(KLUGE_ENTITY_RESOLUTION_ASIA)\n"
NEW_EXCLUDED = (
    "    excluded = (set(KLUGE_UNIVERSE_BLOCK) | set(KLUGE_ENTITY_RESOLUTION_ASIA)\n"
    "                | tanba_blocked_qids())\n"
)

OLD_NAMES = """    def names_excluded(line):
        return any(tok in line for tok in excluded)


    kept, dropped = [], 0
    for ln in lines:
        if not ln.lstrip().startswith("#") and names_excluded(ln):
            while kept and kept[-1].lstrip().startswith("#"):
                kept.pop()
            dropped += 1
            continue
        kept.append(ln)
    if dropped:
        print(f"excluded ids: {dropped} statement line(s) dropped "
              f"({', '.join(sorted(excluded))}) — never emitted, in any position")
"""

NEW_NAMES = """    def names_excluded(line):
        # QIDs, and the clan surname itself in annotations (\"Yorikiyo Tanba\").
        if "tanba" in line.lower():
            return True
        return any(tok in line for tok in excluded)

    kept, dropped = [], 0
    for ln in lines:
        # Comments naming an excluded person are dropped too: annotate() writes
        # multi-line description blocks, and popping only the immediate preceding
        # comment left a 500-line Tanba wall after the statements were gone.
        if names_excluded(ln):
            if not ln.lstrip().startswith("#"):
                while kept and kept[-1].lstrip().startswith("#"):
                    kept.pop()
            dropped += 1
            continue
        kept.append(ln)
    if dropped:
        print(f"excluded ids: {dropped} line(s) dropped incl. Tanba "
              f"({len(tanba_blocked_qids())} Tanba QIDs on disk) — never emitted")
"""

OLD_USABLE = """            markers = {w.lower() for w in WORDS_MEANING_UNKNOWN} | {"nn", "unknown", "ukjent"}
            if any(low == w or low.startswith(w + " ") for w in markers):
                return ""
"""

NEW_USABLE = """            markers = {w.lower() for w in WORDS_MEANING_UNKNOWN} | {"nn", "unknown", "ukjent"}
            # PREFIX catches `NN Surname` and multi-word markers (`name not known`).
            # TOKEN catches the mirror shape `Given NN` / `Margreta NN`, which the prefix
            # test misses and which put `father of Margreta NN` into the day batch.
            if any(low == w or low.startswith(w + " ") for w in markers):
                return ""
            single_word = {w for w in markers if " " not in w}
            tokens = low.replace("/", " ").split()
            if any(t in single_word for t in tokens):
                return ""
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    changed = False

    if "from tanba_batch_block import tanba_blocked_qids" not in text:
        if "def tanba_blocked_qids(" in text:
            print("inline tanba_blocked_qids present; leaving as-is (prefer import on fresh installs)")
        else:
            anchor = "import qs_v1  # noqa: E402 -- the one module that knows what a CREATE block is\n"
            if anchor not in text:
                sys.exit("anchor qs_v1 import not found")
            text = text.replace(anchor, anchor + IMPORT_LINE, 1)
            changed = True
            print("inserted from tanba_batch_block import tanba_blocked_qids")
    else:
        print("import already present")

    if OLD_EXCLUDED in text:
        text = text.replace(OLD_EXCLUDED, NEW_EXCLUDED, 1)
        changed = True
        print("wired tanba into excluded set")
    elif "tanba_blocked_qids()" in text and "excluded = (set(KLUGE_UNIVERSE_BLOCK)" in text:
        print("excluded set already wired")

    if OLD_NAMES in text:
        text = text.replace(OLD_NAMES, NEW_NAMES, 1)
        changed = True
        print("wired names_excluded comment+Tanba drop")
    elif 'if "tanba" in line.lower():' in text:
        print("names_excluded already wired")
    else:
        print("WARNING: could not find names_excluded block to patch")

    if OLD_USABLE in text:
        text = text.replace(OLD_USABLE, NEW_USABLE, 1)
        changed = True
        print("wired Given-NN token check in usable()")
    elif "single_word = {w for w in markers if" in text:
        print("usable() NN token check already wired")
    else:
        print("WARNING: could not find usable() markers block to patch")

    if changed:
        TARGET.write_text(text, encoding="utf-8")
        print(f"wrote {TARGET}")
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
