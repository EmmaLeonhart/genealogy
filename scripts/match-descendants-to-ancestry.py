"""Leads between a descendants roster and the account owner's own ancestry.

    PYTHONPATH=src python scripts/match-descendants-to-ancestry.py

⛔ **THIS IS ONE OF THE FEW PLACES FUZZY MATCHING IS RIGHT.** Ruled 2026-09-20: *"this is one of
the few situations in which fuzzy string matching might actually be good. Because you'd be able
to potentially find things like common names, common last names, even common managing
individuals."* Everywhere else in this repo matching is on the Geni id and never on a name --
§ *Merging is an exact join, never fuzzy name matching*. That rule governs MERGING. This is not
merging: it produces leads for a person to look at, and nothing it emits is written to Wikidata.

**The exact join is run first and is expected to return nothing.** Measured 2026-09-20: 0 of
8,254 ancestors appear in the 14,897-person roster by id. If it ever returns something, the
connection is already known and there is no research to do.

⛔ **THE MANAGING INDIVIDUAL IS A LEAD AND IT WAS THROWN AWAY ONCE.** The first 6N descendants
batch omitted it because *"Claude decided to use its own discretion to omit the managing
individual, which is not a thing you're supposed to do."* Two people managed by one account is a
human connection, not a name coincidence -- far stronger evidence than a shared surname. The
roster carries it at 99.4%, and the manager axis is the one this file exists for.

**The ancestors side has two forms and they are not interchangeable.** The tree-derived list
(`owner-ancestors.tsv`) gives exact ids and NO manager; the scraped list gives Geni's own name
rendering AND the manager. Both are read when present, and which one a lead came from is
reported, because a surname match between two different renderings is weaker evidence than one
between two identical ones.
"""
from __future__ import annotations

import collections
import csv
import glob
import io
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "descendant-ancestry-leads.md")
#: Every shared token, not the top of it -- the markdown shows the rarest 60.
OUT_CSV = os.path.join(ROOT, "reports", "descendant-ancestry-leads.csv")
csv.field_size_limit(10 ** 9)

#: Tokens that carry no identifying force. A surname match on one of these is noise, and they
#: dominate this corpus: `NN` alone is thousands of people on both sides.
STOP = {
    "nn", "unknown", "private", "de", "van", "von", "der", "den", "di", "da", "of", "the",
    "ibn", "bin", "bint", "al", "el", "and", "or", "jr", "sr", "i", "ii", "iii", "iv", "v",
    "king", "queen", "prince", "princess", "duke", "count", "lord", "lady", "saint", "st",
}


def fold(s: str) -> str:
    """Casefolded, accent-stripped. `Ø` and `O` must not be two different surnames."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.casefold()


def tokens(name: str) -> set[str]:
    """Identifying word tokens of a rendered Geni name."""
    n = re.sub(r"^\s*Name:\s*", "", name or "")
    n = re.sub(r"\([^)]*\)", " ", n)          # (c.1389 - 1467)
    n = re.sub(r'"[^"]*"', " ", n)            # "Heinrich IX. d. Ä."
    n = re.sub(r"[0-9]", " ", n)
    out = set()
    for t in re.split(r"[^\w'À-ɏ]+", fold(n)):
        if len(t) >= 4 and t not in STOP:
            out.add(t)
    return out


def load_desc():
    """The roster: the list pages AND the branch's sweep, one row per Geni id.

    ⛔ **THE SWEEP IS THE ROSTER NOW.** The list pages held 14,897 people on 2026-09-20; the
    sweep of `exports/2026-09-19` has since harvested 269,698 into `reports/sweep/*.tsv`, with
    `managed_by_text` on nearly every row. Reading only the list file answered the question for
    the first slice. The 209 focus people whose capture was the WAF's 403 page are skipped.
    """
    p = os.path.join(ROOT, "reports", "list-descendants-6000000227822546944.tsv")
    with io.open(p, encoding="utf-8", errors="replace", newline="") as fh:
        rows = {r["geni_id"].strip(): r for r in csv.DictReader(fh, delimiter="\t")
                if (r.get("geni_id") or "").strip()}
    bad = set()
    partial = os.path.join(ROOT, "reports", "sweep-partial-incapsula-2026-09-21.txt")
    if os.path.exists(partial):
        bad = set(io.open(partial, encoding="utf-8").read().split())
    for f in sorted(glob.glob(os.path.join(ROOT, "reports", "sweep", "*.tsv"))):
        if re.sub(r"\D", "", os.path.basename(f)) in bad:
            continue
        with io.open(f, encoding="utf-8", errors="replace", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                g = (r.get("geni_id") or "").strip()
                if g and g not in rows:
                    rows[g] = {"geni_id": g, "name": r.get("name_text") or "",
                               "managed_by": r.get("managed_by_text") or ""}
    return list(rows.values())


def load_anc_names():
    """`{geni_id: rendered name}` for the owner's ancestors, off the derived labels."""
    ids = {r["geni_id"] for r in csv.DictReader(
        io.open(os.path.join(ROOT, "reports", "owner-ancestors.tsv"), encoding="utf-8"),
        delimiter="\t")}
    out = {}
    p = os.path.join(ROOT, "reports", "derived-labels.csv")
    with io.open(p, encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g in ids:
                out[g] = (row.get("label_mul") or row.get("label_en") or "").strip()
    return out


def main() -> int:
    desc = load_desc()
    anc = load_anc_names()

    # 1. the exact join, which should return nothing
    exact = {r["geni_id"] for r in desc} & set(anc)

    # 2. token index over the ancestry
    idx = collections.defaultdict(set)
    for g, name in anc.items():
        for t in tokens(name):
            idx[t].add(g)

    hits = collections.defaultdict(list)
    for r in desc:
        for t in tokens(r.get("name", "")):
            if t in idx:
                hits[t].append(r)

    # 3. managers, ranked by how much of the roster they hold
    mgr = collections.Counter(
        re.sub(r"^\s*Managed By:\s*", "", (r.get("managed_by") or "").strip())
        for r in desc if (r.get("managed_by") or "").strip())

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Leads: the descendants roster against the owner's ancestry\n\n")
        fh.write(f"- ancestors of the owner: **{len(anc):,}** named, from the synoptic tree\n")
        fh.write(f"- descendants in the roster: **{len(desc):,}**\n")
        fh.write(f"- **exact Geni id overlap: {len(exact)}** — expected to be 0; anything here is "
                 "a connection already known\n\n")
        fh.write("## Shared name tokens\n\n")
        fh.write("A token is >=4 characters, accent-folded, with titles and `NN` removed. "
                 "Ranked by how FEW ancestors carry it: a token held by two people on each side "
                 "is a lead, one held by hundreds is a common word.\n\n")
        fh.write("| token | ancestors | descendants | example ancestor | example descendant |\n")
        fh.write("|---|---|---|---|---|\n")
        ranked = sorted(hits.items(), key=lambda kv: (len(idx[kv[0]]) * len(kv[1])))
        for t, rs in ranked[:60]:
            a = sorted(idx[t])[0]
            fh.write(f"| `{t}` | {len(idx[t])} | {len(rs)} | {anc[a][:40]} | "
                     f"{re.sub(r'^Name: ', '', rs[0].get('name',''))[:40]} |\n")
        fh.write(f"\n## Managing individuals in the roster\n\n")
        fh.write("⛔ The strongest axis, and the one the first batch discarded. A manager who "
                 "also appears on the owner's ancestry is a human link, not a name coincidence. "
                 "**The tree-derived ancestors carry no manager**, so this half waits on the "
                 "scraped ancestors list.\n\n")
        fh.write(f"- distinct managers: **{len(mgr):,}**\n\n| people | manager |\n|---|---|\n")
        for m, n in mgr.most_common(30):
            fh.write(f"| {n} | {m} |\n")

    with io.open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["token", "ancestors", "descendants", "ancestor_ids", "example_descendant_ids"])
        for t, rs in sorted(hits.items(), key=lambda kv: (len(idx[kv[0]]) * len(kv[1]), kv[0])):
            w.writerow([t, len(idx[t]), len(rs), " ".join(sorted(idx[t])),
                        " ".join(sorted(r["geni_id"] for r in rs)[:20])])

    print(f"{os.path.relpath(OUT, ROOT)}")
    print(f"  ancestors {len(anc):,} | descendants {len(desc):,} | exact overlap {len(exact)}")
    print(f"  shared tokens {len(hits):,} | distinct managers {len(mgr):,}")
    print("  tightest shared tokens:")
    for t, rs in sorted(hits.items(), key=lambda kv: (len(idx[kv[0]]) * len(kv[1])))[:10]:
        print(f"    {t:22s} {len(idx[t])} ancestor(s) x {len(rs)} descendant(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
