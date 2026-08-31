"""Every turn Emma actually typed, across every transcript, newest first.

    python scripts/extract-user-turns.py [--since 2026-08-15]

**`queue.md` § STANDING PROCEDURE is what this serves**, and it is a procedure rather than a
step: run it before executing the rest of the queue, because otherwise the rest is not
trustworthy. This is step 1 of it — *extract every user turn with its timestamp, and do not
summarise while extracting, because that is where instructions get lost.*

**Read BOTH record types, or the scan misses half of her.** A turn she typed while the model was
idle is `{"type": "user", "message": {"role": "user"}}`. A turn she typed while a tool call was
running is `{"type": "queue-operation", "operation": "enqueue", "content": "..."}` and is **not**
a user record. Measured 2026-08-16: 28 user records against 21 queue-operations, so a
`role == "user"` scan finds 57% of what she said.

**What is dropped, and why each one is not her:**

* tool results — a `user` record whose content is a `tool_result` block is the harness replying
  to the model, not a person typing;
* `<system-reminder>`, `<task-notification>` and `<local-command-...>` payloads;
* cron prompts, which arrive as enqueues and are the harness talking;
* compaction turns — `CLAUDE.md`-style narration reinserted at a context boundary. Their quoted
  messages are evidence, their narration is not, so the whole record is dropped rather than
  half-trusted.

Everything else is kept **verbatim**. The classification step is deliberately not done here:
summarising during extraction is the failure the procedure names.

Writes `reports/user-turns.tsv` — `when`, `session`, `kind`, `text`.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

TRANSCRIPTS = Path.home() / ".claude" / "projects" / "C--Users-Emma-Documents-GitHub-geni"
OUT = ROOT / "reports" / "user-turns.tsv"

#: Payloads that are the harness rather than Emma. Matched against the start of the text after
#: stripping whitespace, except `system-reminder` which can be preceded by her own words.
HARNESS_PREFIXES = (
    "<task-notification", "<local-command", "<command-name", "<command-message",
    "[Request interrupted", "Caveat: The messages below",
)

#: A cron prompt reaches the queue as an enqueue and is not her. These are the opening words of
#: the three work-loop crons and the daily rebuild; matching on the opening line is enough.
CRON_OPENERS = (
    "Work-loop tick", "Auto-flush tick", "Status-report tick",
    "Rebuild BOTH QuickStatements files",
)

SYSTEM_REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)


def text_of(content):
    """A message's text, whether it is a plain string or a list of blocks.

    Returns `None` when the record carries no text a person could have typed -- notably a
    `tool_result`, which is the harness answering the model inside a `user`-typed record.
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return None
    parts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_result":
            return None
        if block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts) if parts else None


def is_harness(text):
    stripped = SYSTEM_REMINDER.sub("", text).strip()
    if not stripped:
        return True
    if stripped.startswith(HARNESS_PREFIXES):
        return True
    if any(stripped.startswith(opener) for opener in CRON_OPENERS):
        return True
    # A compaction turn: narration reinserted at a context boundary, not something she wrote.
    if stripped.startswith("This session is being continued from a previous conversation"):
        return True
    return False


def turns(path):
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            kind = None
            if rec.get("type") == "user" and isinstance(rec.get("message"), dict):
                if rec["message"].get("role") == "user":
                    kind = "typed"
                    text = text_of(rec["message"].get("content"))
                else:
                    continue
            elif rec.get("type") == "queue-operation" and rec.get("operation") == "enqueue":
                kind = "enqueued"
                text = rec.get("content")
            else:
                continue

            if not isinstance(text, str) or is_harness(text):
                continue
            yield {
                "when": rec.get("timestamp", ""),
                "session": path.stem[:8],
                "kind": kind,
                "text": SYSTEM_REMINDER.sub("", text).strip(),
            }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="", metavar="YYYY-MM-DD",
                    help="only turns on or after this date")
    args = ap.parse_args()

    files = sorted(TRANSCRIPTS.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"{len(files)} transcripts", flush=True)

    rows = []
    for n, path in enumerate(files, 1):
        got = list(turns(path))
        rows.extend(got)
        print(f"  {n:>2}/{len(files)}  {path.stem[:8]}  {len(got):>4} turns", flush=True)

    if args.since:
        rows = [r for r in rows if r["when"][:10] >= args.since]
    rows.sort(key=lambda r: r["when"], reverse=True)

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["when", "session", "kind", "text"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            r = dict(r, text=r["text"].replace("\t", " ").replace("\r", " ").replace("\n", " ⏎ "))
            w.writerow(r)

    typed = sum(1 for r in rows if r["kind"] == "typed")
    print(f"\n{len(rows):,} turns  ({typed:,} typed, {len(rows) - typed:,} enqueued while busy)")
    if rows:
        print(f"range {rows[-1]['when'][:10]} .. {rows[0]['when'][:10]}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
