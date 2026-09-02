"""Find the kana reading of a Japanese name on ja.wikipedia. Never generate one.

    py scripts/fetch-kana-readings.py [--limit N]

**Emma, 2026-08-29:** *"do a cjk label conversion thing with research to fill in the korean and
name in kana properties"*. `CLAUDE.md` is explicit that a kana reading is **not derivable by rule**
— the same characters take different readings per person, which is why `P1814` exists as a property
rather than being computed. So this **finds** readings; it never builds one.

Reads `reports/p1814-worklist.tsv`, takes the rows whose state is `jawiki article`, and writes
`reports/kana-readings.tsv`.

## Two sources were tried and only one survives

**`DEFAULTSORT` is NOT the reading, and it looks exactly like one.** jawiki's sort key strips
dakuten by convention, so 藤原薬子 sorts as `ふしわら の くすこ` when the reading is
`ふじわら の くすこ`, 榊原 as `さかきはら` for `さかきばら`, 平滋子 as `たいら の しけこ`. Emitting
sort keys as readings would put a wrong name on every voiced item — and it is a *structured* field,
which is what makes it tempting. Measured before use, rejected.

**The lead sentence carries the real reading**, parenthesised straight after the title:
`藤原 薬子（ふじわら の くすこ、…）`.

## The fall-through is the bug this file is written around

A first attempt matched *any* parenthesis holding kana and took the first that matched. On 平滋子
the real reading is `たいら の じし／しげこ` — two variants separated by `／` — which the kana class
excluded, so the match **fell through to a later parenthetical** and returned
`けんしゅんもんいん`, her posthumous title 建春門院. One wrong reading in eight.

So: **only the FIRST parenthetical is ever considered.** If it does not parse as kana, the row is
reported as needing a human rather than searched further. A reading that is wrong is worse than one
that is missing — `CLAUDE.md` § *partial is worse than absent* — and a fall-through search is a
machine for finding plausible wrong answers.

`／` and `・` are kept, and a row carrying one is marked `variants` for her to choose. Nothing here
picks between two readings a Japanese editor thought worth recording.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

WORKLIST = ROOT / "reports" / "p1814-worklist.tsv"
OUT = ROOT / "reports" / "kana-readings.tsv"
API = "https://ja.wikipedia.org/w/api.php"
AGENT = "genimerge kana readings (emma@topazcomputing.com)"
TAB = chr(9)

#: Hiragana, the long vowel mark, the separators a Japanese lead legitimately uses inside a
#: reading, and space. Katakana is deliberately absent: a lead gives the reading in hiragana,
#: and katakana in that slot is usually a foreign name rather than a yomi.
KANA = r"[ぁ-ゖー・／/\s]"

#: Only ever the FIRST parenthetical. See the module docstring: searching further is how a
#: posthumous title gets emitted as somebody's name.
FIRST_PAREN = re.compile(r"[（(]([^）)]*)[）)]")


def reading_of(extract):
    """`(reading, state)` for one lead sentence.

    `state` is `reading` for a single unambiguous yomi, `variants` where the lead offers more
    than one, and `needs a human` when the first parenthetical is not a reading at all.
    """
    text = (extract or "").replace("\n", " ")
    m = FIRST_PAREN.search(text)
    if not m:
        return "", "needs a human: no parenthetical in the lead"
    inner = m.group(1).strip()
    # The lead routinely continues `（よみ、生年 - 没年）`; the reading is the part before the
    # first comma. Everything after it is dates and prose.
    head = re.split(r"[、,]", inner)[0].strip()
    if not head or not re.fullmatch(KANA + "+", head):
        return "", "needs a human: first parenthetical is %r" % inner[:40]
    if "／" in head or "/" in head:
        return head, "variants"
    return head, "reading"


def fetch(titles):
    """`{title: extract}` for up to 20 titles, one request."""
    q = urllib.parse.urlencode({
        "action": "query", "prop": "extracts", "exintro": "1", "explaintext": "1",
        "redirects": "1", "titles": "|".join(titles), "format": "json"})
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=90) as fh:
        data = json.loads(fh.read().decode("utf-8"))
    pages = (data.get("query") or {}).get("pages") or {}
    return {p.get("title", ""): p.get("extract", "") for p in pages.values()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, help="stop after this many rows, for a trial run.")
    args = ap.parse_args()

    with io.open(WORKLIST, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter=TAB)
                if r["state"] == "jawiki article" and r["reading_or_source"]]
    if args.limit:
        rows = rows[:args.limit]
    print("%d rows with a jawiki article" % len(rows))

    by_title = {}
    for r in rows:
        by_title.setdefault(r["reading_or_source"], []).append(r)
    titles = sorted(by_title)

    got = {}
    # 20 at a time: `exintro` extracts are large, and this is somebody else's server.
    for i in range(0, len(titles), 20):
        try:
            got.update(fetch(titles[i:i + 20]))
        except Exception as exc:                                        # noqa: BLE001
            print("  request failed for a chunk (%s); those rows stay unresolved" % exc,
                  file=sys.stderr)
        time.sleep(0.5)
        if i and i % 200 == 0:
            print("  %d/%d" % (i, len(titles)), file=sys.stderr)

    out, tally = [], {}
    for title in titles:
        reading, state = reading_of(got.get(title, ""))
        if title not in got:
            reading, state = "", "needs a human: no article returned"
        tally[state.split(":")[0]] = tally.get(state.split(":")[0], 0) + len(by_title[title])
        for r in by_title[title]:
            out.append([r["geni_id"], r["qid"], r["geni_name"], title, reading,
                        state, r["evidence_strength"]])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "geni_name", "jawiki_title", "reading", "state",
                    "evidence_strength"])
        w.writerows(sorted(out, key=lambda x: (x[5], x[6])))

    print("\nwrote %s - %d rows" % (OUT.relative_to(ROOT), len(out)))
    for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("   %-34s %5d" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
