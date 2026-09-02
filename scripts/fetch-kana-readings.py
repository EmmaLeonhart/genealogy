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

#: Only ever the FIRST parenthetical, and balanced so a nested one does not truncate it. See
#: the module docstring: searching further is how a posthumous title gets emitted as a name.
def _first_paren(text):
    """The contents of the first balanced `（…）`, or `""`."""
    start = -1
    depth = 0
    for i, ch in enumerate(text):
        if ch in "（(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch in "）)":
            depth -= 1
            if depth == 0 and start >= 0:
                return text[start:i]
            if depth < 0:
                return ""
    return ""


def _strip_inner(s):
    """`("あがた（の）いぬかい", ["の"])` — the text outside nested parens, and what was inside."""
    out, inner, buf, depth = [], [], [], 0
    for ch in s:
        if ch in "（(":
            depth += 1
            if depth == 1:
                buf = []
                continue
        if ch in "）)":
            depth -= 1
            if depth == 0:
                inner.append("".join(buf))
                continue
        (buf if depth else out).append(ch)
    return "".join(out), inner


def reading_of(extract, title=""):
    """`(reading, state)` for one lead sentence.

    `state` is `reading` for a single unambiguous yomi, `variants` where the lead offers more
    than one, and `needs a human` when nothing in the first parenthetical is a reading.

    **Three shapes the six 2026-09-02 refusals turned out to be**, each handled explicitly rather
    than by widening the pattern until something matches:

    * **the title is already kana** — `おふう`. Then the title IS the reading and there is nothing
      to parse. The lead for these opens with a kanji form the article does not use as its name.
    * **a nested parenthesis** — REFUSED, because the form is ambiguous and does not say which
      it is. `あがた（の）いぬかい` is an optional infix, あがたのいぬかい; `きし（ひろこ）じょおう`
      is two whole readings, きしじょおう and ひろこじょおう. Flattening produced
      `あがたいぬかい の おおとも／の` and `きしじょおう／ひろこ`, names nobody has, and marking
      them `variants` made them look answerable when they were mangled.
    * **a kanji restatement first** — `眞龍院、しんりゅういん、…`. The reading is the second
      comma-element. It is only accepted when every element before it is made of characters the
      TITLE already contains: that is what makes it a restatement rather than a different person's
      name, and it is the guard that stops the 平滋子 fall-through coming back.
    """
    if title and all("぀" <= c <= "ヿ" or c in "・ー" for c in title):
        return title, "reading from the title, which is already kana"
    text = (extract or "").replace(chr(10), " ")
    inner_p = _first_paren(text)
    if not inner_p:
        return "", "needs a human: no parenthetical in the lead"
    title_chars = set(title)
    for n, element in enumerate(re.split(r"[、,]", inner_p)):
        element = element.strip()
        if not element:
            continue
        outside, inside = _strip_inner(element)
        outside = outside.strip()
        if not re.fullmatch(KANA + "+", outside or "x"):
            # Only a restatement of the title may be skipped over. Anything else and we stop:
            # a later parenthetical belonging to somebody else is how a wrong name gets emitted.
            if n == 0 and outside and set(outside) <= title_chars:
                continue
            return "", "needs a human: first parenthetical is %r" % inner_p[:40]
        # **A nested parenthesis is REFUSED, not flattened.** `（…）` inside the reading means two
        # different things and the form does not say which: `あがた（の）いぬかい` is an OPTIONAL
        # INFIX — あがたのいぬかい — while `きし（ひろこ）じょおう` is two whole alternative readings,
        # きしじょおう and ひろこじょおう. Flattening gave `あがたいぬかい の おおとも／の` and
        # `きしじょおう／ひろこ`, both of which are names nobody has. Three rows refused beats two
        # rows mangled, and a mangled reading marked `variants` looks answerable when it is not.
        if any(x.strip() for x in inside):
            return "", ("needs a human: nested parenthesis, %r — optional infix or two whole "
                        "readings?" % element[:40])
        if "／" in outside or "/" in outside:
            return outside, "variants"
        return outside, "reading"
    return "", "needs a human: nothing in the first parenthetical parsed as kana"


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
        reading, state = reading_of(got.get(title, ""), title)
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
