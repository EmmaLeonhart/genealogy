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
    kids, par, lab, fa = {}, {}, {}, {}
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
            # ⛔ **THE FATHER IS A NAMED COLUMN, NOT `par[g][0]`.** `par` concatenates four
            # columns, so position 0 is the father only when a father happens to be recorded.
            # Read positionally it returned `Wilhelmine von Romberg` as a father and scored four
            # surnames as patrilineal that are not -- CLAUDE.md § *PARSE BY FORM, never
            # positionally*, which is the ultimate cause of most name defects here.
            fs = []
            for col in ("father", "fathers"):
                v = (r.get(col) or "").strip()
                if v:
                    fs.extend(x.strip() for x in v.split(SEP) if x.strip())
            if fs:
                fa[g] = fs
    with io.open(os.path.join(ROOT, "reports", "derived-labels.csv"),
                 encoding="utf-8", errors="replace", newline="") as fh:
        for r in csv.DictReader(fh):
            g = (r.get("geni_id") or "").strip()
            if g:
                lab[g] = (r.get("label_mul") or r.get("label_en") or "").strip()
    return kids, par, lab, fa


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
    kids, par, lab, fa = load_family()

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

    # ⛔ **THE SWEPT PAGES COUNT TOO, AND THEY ARE NOT IN THE TREE.** `reports/sweep/*.tsv`
    # is the branch's raw harvest -- one file per focus person, `name_text` as Geni renders it.
    # These are exactly the people the synoptic tree does NOT hold, which is the population a
    # surname match is actually for: somebody already in the tree needs no name evidence.
    import glob
    swept = 0
    for f in glob.glob(os.path.join(ROOT, "reports", "sweep", "*.tsv")):
        with io.open(f, encoding="utf-8", errors="replace", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="	"):
                g = (r.get("geni_id") or "").strip()
                nm = re.sub(r"^\s*Name:\s*", "", (r.get("name_text") or "").strip())
                if not g or not nm:
                    continue
                swept += 1
                lab.setdefault(g, nm)
                for s in surnames(nm):
                    d_idx[s].add(g)
    print(f"  swept rows folded in: {swept:,}")

    # ⛔ **A SURNAME IS ONLY A LEAD IF IT SITS ON THE DESCENT PATH.** Ruled by measurement
    # 2026-09-20, after both of the first two leads died the same way.
    #
    # `Christina Gustaviana von Furman` IS a Yuri descendant and DOES carry a surname the owner's
    # maternal line carries. Both true, and the lead was still worthless: her Yuri blood comes
    # through her MOTHER, Margareta Charlotta von Essen, and runs von Essen -> von Wrangell ->
    # von Ritter -> von Krüdener -> von Rosen -> von Buxhoeveden -> Rurykwicz. Her father
    # `Gustaf Adolf von Furman` is **not a descendant of Yuri at all**. So even if he descends
    # from the owner's Mårten Furman, that carries no Yuri blood in either direction.
    #
    # `von Hagmann` died the same way and worse: it is a MARRIED name over a von Maydell --
    # `CLAUDE.md` § *The MARRIED name is the real name* is exactly why Geni renders it that way.
    #
    # A surname travels down the PATERNAL line, so the test is whether the father is also a
    # descendant of the target. Where no father is recorded the row is kept and flagged, because
    # a missing parent is the thing being looked for, not evidence against.
    def on_descent_path(g):
        fs = fa.get(g, [])
        if not fs:
            return "no father recorded"
        return "yes" if fs[0] in desc else "no"

    rows = []
    for side, people in (("mother (Swedish)", mat), ("father (Norwegian)", pat)):
        idx = collections.defaultdict(set)
        for g in people:
            for s in surnames(lab.get(g, "")):
                idx[s].add(g)
        for s in set(idx) & set(d_idx):
            best = sorted(d_idx[s])[0]
            rows.append((len(idx[s]) * len(d_idx[s]), s, side, len(idx[s]), len(d_idx[s]),
                         sorted(idx[s])[0], best, on_descent_path(best)))
    rows.sort()

    # ⛔ **THE MATERNAL SIDE IS NEVER TRUNCATED.** Ruled by measurement 2026-09-21: the rank is
    # rarity, `rows[:120]` cut at it, and eleven of the fourteen shared MATERNAL surnames fell
    # past the cut -- including `bure` (1x29), which is the kinship the whole pipeline is
    # pointed at. The report showed three maternal rows and was read as "three maternal leads"
    # for fourteen consecutive ticks. The paternal side keeps the cut: it has 522 of the 536.
    m_rows = [r for r in rows if r[2].startswith("mother")]
    p_rows = [r for r in rows if not r[2].startswith("mother")]
    shown = m_rows + p_rows[:120]

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Surnames shared by Yuri Dolgorukiy's descendants and the owner's ancestors\n\n")
        fh.write(f"- descendants of Yuri in the synoptic tree: **{len(desc):,}**\n")
        fh.write(f"- ancestors through the mother (Swedish): **{len(mat):,}**\n")
        fh.write(f"- ancestors through the father (Norwegian): **{len(pat):,}**\n")
        fh.write(f"- shared surnames: **{len(rows):,}**\n\n")
        fh.write("Patronymics are excluded: every Erik's daughter is an `Eriksdotter`, so they "
                 "link nothing. Titles are excluded. Ranked by rarity — a surname held by one "
                 "person on each side is a place to look, one held by dozens is a common name.\n\n")
        fh.write("| surname | side | on the descent path? | ancestors | descendants "
                 "| example ancestor | example descendant |\n")
        fh.write("|---|---|---|---|---|---|---|\n")
        for _rank, s, side, na, nd, ea, ed, onpath in shown:
            fh.write(f"| **{s}** | {side} | {onpath} | {na} | {nd} | "
                     f"{lab.get(ea,chr(39)+chr(39))[:34]} | {lab.get(ed,'')[:34]} |" + chr(10))

    print(f"{os.path.relpath(OUT, ROOT)}")
    print(f"  Yuri descendants in tree {len(desc):,} | maternal {len(mat):,} | paternal {len(pat):,}")
    print(f"  shared surnames {len(rows):,}")
    print(f"  maternal rows {len(m_rows)} (all listed) | paternal rows {len(p_rows)}")
    for _r, s, side, na, nd, ea, ed, onpath in m_rows:
        print(f"   {s:18s} {side:20s} onpath={onpath:18s} {na}x{nd}  {lab.get(ea,'')[:26]:26s} | {lab.get(ed,'')[:26]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
