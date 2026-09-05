"""Parse Emma's Wikidata interaction log into a CSV of every edit.

The source is `reports/wikidata-interaction-log-2026-09-03.txt` --- the pastebin she
handed over on 2026-09-03: *"These are all of the users I ever interacted with, please
look into them"*. It is a MediaWiki contributions/watchlist rendering pasted as text, so
every line is one revision by somebody else touching an item this project created or
edited.

One row per revision, per `CLAUDE.md` § *"Analyse this" means build a CSV*. No judgment
here --- the columns are read off the line and nothing is inferred. The reading lives in
`reports/wikidata-editor-interactions.md`.

Line shape, and the three characters that are not ASCII:

    diffhist Anna Hedenberg (Q124477457) 08:55 +101 Anvilaquarius talk contribs (<LRM>Added ...) Tag: Wikidata user interface thank

  * the minus in a negative byte delta is U+2212 MINUS SIGN, not a hyphen;
  * the edit summary opens with U+200E LEFT-TO-RIGHT MARK;
  * a section-header line is a bare date, `3 September 2026`.

`b` and `N` flags (bot, new page) sit between `diffhist` and the label. A `Talk:Qnnn`
target has no parenthesised qid and no label.
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "wikidata-interaction-log-2026-09-03.txt"
OUT = ROOT / "reports" / "wikidata-interactions.csv"

MINUS = "−"
LRM = "‎"

MONTHS = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
    "December": 12,
}

DATE_RE = re.compile(r"^(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})$")

# diffhist [flags] [label ](Qnnn)|Talk:Qnnn HH:MM delta user talk contribs (summary) [Tag(s): ...]
LINE_RE = re.compile(
    r"^diffhist\s+"
    r"(?P<flags>(?:[bN]\s+)*)"
    r"(?P<target>.*?)\s+"
    r"(?P<time>\d{2}:\d{2})\s+"
    r"(?P<delta>[+" + MINUS + r"\-]?[\d,]+)\s+"
    r"(?P<user>.+?)\s+talk\s+contribs\s+"
    r"\((?P<summary>.*)\)"
    r"(?P<trailer>.*)$"
)

QID_RE = re.compile(r"\((Q\d+)\)$")
TALK_RE = re.compile(r"^Talk:(Q\d+)$")
TAG_RE = re.compile(r"Tags?:\s*(.*?)\s*(?:thank)?\s*$")

# What the edit did, read off the summary text alone. `other` is a real outcome and is
# never widened to make the table look tidy.
ACTIONS = [
    ("redirect", re.compile(r"^Redirected to (Q\d+)")),
    ("merge", re.compile(r"^Merged Item from (Q\d+)")),
    ("claim_removed", re.compile(r"^Removed claim")),
    ("claim_changed", re.compile(r"^Changed claim")),
    ("claim_created", re.compile(r"^Created claim")),
    ("item_updated", re.compile(r"^Updated Item")),
    ("description_added", re.compile(r"^Added \[[^\]]+\] description")),
    ("alias_added", re.compile(r"^Added multiple languages alias")),
    ("label_added", re.compile(r"^Added \[[^\]]+\] label")),
    ("sitelink_moved", re.compile(r"^Page moved")),
    ("talk_section", re.compile(r"^→|new section")),
]

PROPERTY_RE = re.compile(r"\b(P\d+)\b")
TARGET_QID_RE = re.compile(r"\((Q\d+)\)")


def classify(summary: str) -> str:
    for name, pattern in ACTIONS:
        if pattern.search(summary):
            return name
    return "other"


def parse(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: date | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = DATE_RE.match(line)
        if m:
            current = date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
            continue
        if not line.startswith("diffhist"):
            continue
        m = LINE_RE.match(line)
        if m is None:
            raise SystemExit(f"unparsed revision line, refusing to write a short file:\n  {line}")

        target = m.group("target").strip()
        qid, label = "", ""
        talk = TALK_RE.match(target)
        if talk:
            qid = talk.group(1)
            label = ""
            namespace = "Talk"
        else:
            namespace = "Item"
            q = QID_RE.search(target)
            if q:
                qid = q.group(1)
                label = target[: q.start()].strip()
            else:
                label = target

        delta_text = m.group("delta").replace(MINUS, "-").replace(",", "")
        summary = m.group("summary").replace(LRM, "").strip()
        trailer = m.group("trailer")
        tag_m = TAG_RE.search(trailer)
        tags = tag_m.group(1) if tag_m else ""

        action = classify(summary)
        # The other item named by the summary: a redirect target, a merge source, or the
        # value of a claim. It is what tells us which of our items was folded away.
        others = [q for q in TARGET_QID_RE.findall(summary)]
        rows.append(
            {
                "date": current.isoformat() if current else "",
                "time": m.group("time"),
                "namespace": namespace,
                "qid": qid,
                "label": label,
                "delta": delta_text,
                "user": m.group("user").strip(),
                "action": action,
                "property": ";".join(dict.fromkeys(PROPERTY_RE.findall(summary))),
                "other_qids": ";".join(dict.fromkeys(others)),
                "flags": m.group("flags").split() and " ".join(m.group("flags").split()) or "",
                "tags": tags,
                "summary": summary,
            }
        )
    return rows


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"missing source: {SOURCE}")
    rows = parse(SOURCE.read_text(encoding="utf-8"))
    if not rows:
        raise SystemExit("parsed zero revisions --- the format has changed, not the data")

    # Deterministic and total: date, time, qid, user, summary. `CLAUDE.md` § SORTING MUST
    # BE DETERMINISTIC --- the last field is what makes the key total.
    rows.sort(key=lambda r: (r["date"], r["time"], r["qid"], r["user"], r["summary"]))

    tmp = OUT.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(OUT)
    print(f"{len(rows)} revisions -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
