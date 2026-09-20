"""Order the descendants of a scraped relatives list into the queue the scrape runs in.

Ruled 2026-09-19: *"go from the end up to the beginning"*, and before that
*"Find everyone who appears scandinavian through text searches on patronymics like
'ssen' 'sson' 'dotter' 'datter' 'dottir' etc and those people going from the last to the
first go first and then the rest of the people going from the last to the first."*

So there are exactly two blocks and both run BACKWARDS through the file:

    1  the patronymic hits, last row to first
    2  everyone else, last row to first

Backwards is the point, not a detail. The list is ordered by relationship distance, so the
END is the far tail -- page 750 of 6000000227822546944 is Beauclerk and Sheffield, page 2 is
Tabaristan and Turgesh. The European descent, and with it any Scandinavian link, sits at the
bottom of the file.

The matching is DELIBERATELY GENEROUS. A false positive only moves somebody earlier in a
queue that reaches everybody anyway, so it costs nothing; a miss leaves a Scandinavian
person waiting behind 14,000 others. `CLAUDE.md` § *STOP GUESSING CONSERVATIVELY* applies
directly -- this is the do-it-or-leave-it case.
"""

from __future__ import annotations

import io
import re
import sys

#  -sson/-ssen doubled forms are distinctly Nordic; bare -sen/-son are shared with Dutch and
#  English and are taken anyway, per the generosity rule above. The -dotter/-datter/-dottir
#  family is the matronymic/patronymic feminine and is unambiguous.
#  Tested as a SUFFIX OF A NAME TOKEN, never as a substring of the line. Matching the raw
#  string caught the English word "son" in `Stillborn son 2 van Oranje` and `Charles, apparent
#  son of Louise`, and a toponym list caught `Berg-Op-Zoom` -- 6 of the first 6 hits were junk.
#  A token must be at least 5 characters and must not BE the bare word, so `Ericsson` matches
#  and `son` does not.
#  EXACTLY the endings Emma named, and no additions. Widening it to bare -sen/-son was mine
#  and it pulled in English `Robertson`, `Farquharson` and French `Nogaret-Calvisson`.
#  CLAUDE.md § *THE STUPIDER AND MORE SPECIFIC THE INSTRUCTION* -- implement the list given.
SUFFIXES = ("sson", "ssen", "sdatter", "sdottir", "dotter", "datter", "dottir")
BARE = {"son", "sen", "dotter", "datter", "dottir"}
TOKEN = re.compile(r"[A-Za-zÀ-ɏ]+")


def is_patronymic(name: str) -> bool:
    for tok in TOKEN.findall(name):
        low = tok.lower()
        if low in BARE or len(tok) < 5:
            continue
        if low.endswith(SUFFIXES):
            return True
    return False


def rows(path: str) -> list[list[str]]:
    out = []
    with io.open(path, encoding="utf-8") as fh:
        fh.readline()
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) >= 7:
                out.append(f)
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else "reports/list-worklist.tsv"
    rs = rows(src)
    hits, rest = [], []
    for r in rs:
        (hits if is_patronymic(r[2]) else rest).append(r)
    # Both blocks reversed: last row of the file first.
    order = list(reversed(hits)) + list(reversed(rest))
    with io.open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write("rank\tgeni_id\tblock\tname\n")
        for i, r in enumerate(order, 1):
            block = "patronymic" if is_patronymic(r[2]) else "rest"
            fh.write("%d\t%s\t%s\t%s\n" % (i, r[0], block, r[2]))
    print("%s: %d rows -> %d patronymic first, then %d rest" % (dst, len(order), len(hits), len(rest)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
