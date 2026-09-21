"""Surname links between Yuri Dolgorukiy's descendants and the owner's ancestors.

    PYTHONPATH=src python scripts/yuri-descent-candidates.py

⛔ **THE QUESTION IS DESCENT, AND ONLY DESCENT.** Ruled 2026-09-20: *"I want to analyze if any of
these are possible genealogical links that would make me his descendant that aren't present ...
Common surnames, whatever might link it on either my mothers or fathers side."*

So: a surname carried BOTH by somebody descended from Yuri AND by somebody in the owner's
ancestry is a candidate for a marriage the tree does not record. Nothing here asserts a link; it
ranks places to look.

⛔ **A BLOOD CONNECTION THAT IS NOT DESCENT IS NOT AN ANSWER.** The owner's existing path to Yuri
runs up through Mstislav to Vladimir Monomakh and back down to Yuri, so Yuri is an ancestor's
BROTHER and his descendants are cousins. That relationship already exists and is not what is
being asked for. Intersecting Yuri's descendants with the owner's ancestors is worse than
useless -- a descendant of Yuri cannot be an ancestor of somebody who is not his descendant, so
the intersection is empty by construction and says nothing.

**Each side is split, because the sides are not equivalent.** The owner's mother's line is
Swedish and the Baltic German families married into Swedish nobility heavily; the father's line
is Norwegian and did so far less. A hit on the maternal side is a better candidate than the same
hit on the paternal side, so which side is reported rather than averaged away.
"""
from __future__ import annotations

import collections
import csv
import io
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "yuri-descent-candidates.md")
csv.field_size_limit(10 ** 9)

OWNER = "6000000087535357291"
YURI = "6000000002187826932"
SEP = " | "

#: Not surnames. Patronymic endings are handled separately; these are words that would match
#: everywhere and mean nothing.
STOP = {
    "nn", "unknown", "private", "de", "van", "von", "der", "den", "af", "av", "di", "da", "of",
    "the", "til", "til.", "and", "eller", "jr", "sr", "mp", "king", "queen", "prince", "princess",
    "duke", "duchess", "count", "countess", "lord", "lady", "sir", "saint", "st", "ridder",
    "knight", "herzog", "grevinde", "greve", "kong", "konge", "prinsessa", "prinsesse",
}

#: A patronymic is not a family name: `Eriksdotter` links nothing, because every Erik's daughter
#: carries it. Dropped, or the output is all patronymics.
PATRONYMIC = re.compile(
    r"(s?(son|sen|sson|ssen|datter|dotter|dttr|dattir|sdatter|sdotter)|"
    r"(ovich|evich|ovna|evna|owicz|ewicz))$", re.I)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def surnames(label: str) -> set[str]:
    """The FAMILY NAME only -- the trailing token, not every word in the label.

    ⛔ **TAKING EVERY TOKEN MAKES THE OUTPUT GIVEN NAMES.** The first version did, and the top
    of the report was `adeliza`, `agnar`, `agota`, `alienor` -- forenames matching forenames,
    1x1 each, ranked as the rarest and best evidence when they are the weakest. A shared
    forename between a 12th-century Rus princess and a 19th-century Swede is nothing.

    So: the last token, which is where a family name sits in both Scandinavian and German
    renderings, plus any `von`/`van`/`af`/`de` phrase, because those ARE the Baltic German
    family names and dropping the particle loses `von Rosen` entirely.
    """
    n = re.sub(r"\([^)]*\)", " ", label or "")
    n = re.sub(r'"[^"]*"', " ", n)
    n = re.sub(r"[0-9]", " ", n)
    n = re.sub(r",.*$", " ", n)                 # drop the title tail: ", Duke of Estland"
    toks = [t for t in re.split(r"[^\w'À-ɏ-]+", fold(n)) if t]
    out = set()

    # the particle phrase: `von rosen`, `van hoogwoud`, `de thouars`
    for i, t in enumerate(toks[:-1]):
        if t in {"von", "van", "de", "af", "av", "til", "zu"}:
            tail = toks[i + 1]
            if len(tail) >= 3 and tail not in STOP:
                out.add(f"{t} {tail}")

    # ⛔ **THE LABEL MUST HAVE A SURNAME POSITION AT ALL.** A label that IS a single given
    # name -- `Agatha`, `Alan`, `Basil`, `Alvor` -- has that name as its last token, and taking
    # it produced forename-to-forename matches ranked as the rarest evidence in the file. A
    # surname is the trailing token of a name that has something in front of it.
    # ⛔ **A NAME ENDING IN A PATRONYMIC HAS NO FAMILY NAME, AND POPPING IT INVENTS ONE.**
    # `Anna Brita Nilsdotter` -> popping `nilsdotter` leaves `brita`, a FORENAME, which then
    # matched other Britas and ranked as rare evidence. But `Helga Toresdatter Fosse` really
    # does carry a farm name after the patronymic, and that one must survive. So: a trailing
    # patronymic means there is no surname at all; a patronymic in the middle is ignored.
    while toks and (toks[-1] in STOP or len(toks[-1]) < 4):
        toks.pop()
    if len(toks) >= 2 and not PATRONYMIC.search(toks[-1]):
        out.add(toks[-1])
    return out


def load_family():
    kids, par, lab = {}, {}, {}
    with io.open(os.path.join(ROOT, "reports", "derived-family.csv"),
                 encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            g = (r.get("geni_id") or "").strip()
            if not g:
                continue
            c = (r.get("children") or "").strip()
            if c:
                kids[g] = [x.strip() for x in c.split(SEP) if x.strip()]
            ps = []
            for col in ("father", "mother", "fathers", "mothers"):
                v = (r.get(col) or "").strip()
                if v:
                    ps.extend(x.strip() for x in v.split(SEP) if x.strip())
            if ps:
                par[g] = ps
    with io.open(os.path.join(ROOT, "reports", "derived-labels.csv"),
                 encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            g = (r.get("geni_id") or "").strip()
            if g:
                lab[g] = (r.get("label_mul") or r.get("label_en") or "").strip()
    return kids, par, lab


def walk(start, edges):
    seen, q = {start}, collections.deque([start])
    while q:
        g = q.popleft()
        for n in edges.get(g, ()):
            if n not in seen:
                seen.add(n)
                q.append(n)
    seen.discard(start)
    return seen


def main() -> int:
    kids, par, lab = load_family()

    desc = walk(YURI, kids)

    # the owner's ancestry, split by which parent it came through
    first = par.get(OWNER, [])
    father = first[0] if len(first) > 0 else None
    mother = first[1] if len(first) > 1 else None
    pat = walk(father, par) | ({father} if father else set())
    mat = walk(mother, par) | ({mother} if mother else set())

    d_idx = collections.defaultdict(set)
    for g in desc:
        for s in surnames(lab.get(g, "")):
            d_idx[s].add(g)

    rows = []
    for side, people in (("mother (Swedish)", mat), ("father (Norwegian)", pat)):
        idx = collections.defaultdict(set)
        for g in people:
            for s in surnames(lab.get(g, "")):
                idx[s].add(g)
        for s in set(idx) & set(d_idx):
            rows.append((len(idx[s]) * len(d_idx[s]), s, side, len(idx[s]), len(d_idx[s]),
                         sorted(idx[s])[0], sorted(d_idx[s])[0]))
    rows.sort()

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Surnames shared by Yuri Dolgorukiy's descendants and the owner's ancestors\n\n")
        fh.write(f"- descendants of Yuri in the synoptic tree: **{len(desc):,}**\n")
        fh.write(f"- ancestors through the mother (Swedish): **{len(mat):,}**\n")
        fh.write(f"- ancestors through the father (Norwegian): **{len(pat):,}**\n")
        fh.write(f"- shared surnames: **{len(rows):,}**\n\n")
        fh.write("Patronymics are excluded: every Erik's daughter is an `Eriksdotter`, so they "
                 "link nothing. Titles are excluded. Ranked by rarity — a surname held by one "
                 "person on each side is a place to look, one held by dozens is a common name.\n\n")
        fh.write("| surname | side | ancestors | descendants | example ancestor | example descendant |\n")
        fh.write("|---|---|---|---|---|---|\n")
        for _rank, s, side, na, nd, ea, ed in rows[:120]:
            fh.write(f"| **{s}** | {side} | {na} | {nd} | {lab.get(ea,'')[:38]} | {lab.get(ed,'')[:38]} |\n")

    print(f"{os.path.relpath(OUT, ROOT)}")
    print(f"  Yuri descendants in tree {len(desc):,} | maternal {len(mat):,} | paternal {len(pat):,}")
    print(f"  shared surnames {len(rows):,}")
    for _r, s, side, na, nd, ea, ed in rows[:25]:
        print(f"   {s:20s} {side:20s} {na}x{nd}  {lab.get(ea,'')[:30]:30s} | {lab.get(ed,'')[:30]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
