"""Which of Emma's instructions are not written down anywhere in the repo?

    python scripts/audit-turns-recorded.py

**Step 3 of `queue.md` § STANDING PROCEDURE**, after `extract-user-turns.py` does step 1. For
each turn: *is it done? is it here? is it in `CLAUDE.md` / `devlog.md`?* Done and recorded →
nothing. Done and unrecorded → `devlog.md`. Not done → a concrete step in the queue.

**The screen is mechanical on purpose.** Judging 3,679 turns by reading them is what the
procedure warns against — *do not summarise, that is where instructions get lost*. So this makes
two objective cuts and hands the residue to a human:

1. **Directive shape.** A turn carrying an imperative or a ruling — *add to the queue*, *never*,
   *always*, *stop*, *don't*, *I want*, *you need to*. Conversation and questions drop out.
   Frustration is kept: `CLAUDE.md` and the procedure both say *"just fucking run the census"* is
   a queue item, so profanity is a signal rather than noise.
2. **Recordedness.** A turn's most distinctive phrase is searched in `CLAUDE.md`, `queue.md`,
   `devlog.md` and `docs/`. A hit means somebody wrote it down; a miss means nobody did.

**Why a distinctive PHRASE and not the whole turn.** The whole turn never matches -- the repo
quotes her in fragments, and matching on any single common word matches everything. The phrase
taken is the longest run of words that is rare in the repo, which is what makes a hit meaningful
in both directions.

**A miss is a CANDIDATE, not a finding.** She repeats herself, rephrases, and much of what she
says is answered in the moment and needs no record. The output is a shortlist to read, and the
reading is the part this cannot do.

Writes `reports/unrecorded-instructions.tsv`.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

TURNS = ROOT / "reports" / "user-turns.tsv"
OUT = ROOT / "reports" / "unrecorded-instructions.tsv"

#: Where the project writes down what she has said.
RECORDS = [ROOT / "CLAUDE.md", ROOT / "queue.md", ROOT / "devlog.md",
           ROOT / "name modelling.txt"]

DIRECTIVE = re.compile(
    r"\b(add (it )?to the (end of the )?queue|queue item|never|always|stop |don'?t |do not "
    r"|i want|i need|you need to|you should|make sure|instead of|from now on|remember to"
    r"|we (are|should|will|need)|has to|must )", re.I)

#: A turn shorter than this is an acknowledgement rather than an instruction -- "yeah", "ok",
#: "do it". They are real but carry nothing to record.
MIN_WORDS = 8

#: **And a turn longer than this is the HARNESS talking, not Emma.** Cron prompts, skill bodies
#: and pasted system text come through the same channel as her typing -- `CLAUDE.md` already says
#: to skip cron prompts and `<task-notification>` for this reason, and skills are the same class.
#:
#: Measured 2026-08-31 over the 376 flagged turns: the six that are harness text have a **median
#: of 1,775 words** against **42** for everything else, so length separates them cleanly and
#: needs no keyword list to maintain. Only six -- the audit was far cleaner than I guessed, which
#: is worth recording because I went looking expecting it to be mostly noise.
MAX_WORDS = 400

WORD = re.compile(r"[a-z0-9']+")


def phrases(text, n=6):
    """Every n-word run of the turn, lowercased. The candidate distinctive phrases."""
    words = WORD.findall(text.lower())
    return [" ".join(words[i:i + n]) for i in range(0, max(0, len(words) - n + 1))]


def main():
    corpus = []
    for path in RECORDS:
        if path.exists():
            corpus.append(" ".join(WORD.findall(path.read_text(encoding="utf-8").lower())))
    for path in sorted((ROOT / "docs").rglob("*.md")):
        corpus.append(" ".join(WORD.findall(path.read_text(encoding="utf-8").lower())))
    blob = "\n".join(corpus)
    print(f"{len(RECORDS)} record files plus docs/, {len(blob):,} chars")

    rows = list(csv.DictReader(TURNS.open(encoding="utf-8"), delimiter="\t"))
    print(f"{len(rows):,} extracted turns")

    seen, candidates = set(), []
    for r in rows:
        text = r["text"].replace(" ⏎ ", " ").strip()
        key = " ".join(WORD.findall(text.lower()))
        if not key or key in seen:
            continue
        seen.add(key)
        n_words = len(key.split())
        if n_words < MIN_WORDS or n_words > MAX_WORDS or not DIRECTIVE.search(text):
            continue
        # Recorded if ANY six-word run of the turn appears in the records.
        hit = next((p for p in phrases(text) if p in blob), "")
        if hit:
            continue
        candidates.append({
            "when": r["when"][:16].replace("T", " "),
            "session": r["session"],
            "kind": r["kind"],
            "words": len(key.split()),
            "text": text[:600],
        })

    candidates.sort(key=lambda c: c["when"], reverse=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["when", "session", "kind", "words", "text"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        for c in candidates:
            w.writerow(dict(c, text=c["text"].replace("\t", " ")))

    print(f"\n{len(seen):,} distinct turns after de-duplication")
    print(f"{len(candidates):,} directive and not found in any record file")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
