"""A clickable worklist for the Geni merge audit — Izumo first, then the strongest CJK.

    python scripts/build-merge-worklist.py

**Emma's method, 2026-08-24:** *"Find profiles that look similar like shared parents, plus look
over basically all Japanese items with higher scrutiny, and then use the browser extension to
see if they merge. Izumo ones are good to explore to see how redirects potentially work."*

Steps 1 and 2 are `scripts/find-geni-duplicates.py`. This is the handoff for step 3, which is
hers: **the merges are hers and are never performed here.** What is built here is only the
order to look in, and the links to look at.

**Why a worklist and not just the TSV.** `reports/geni-duplicate-candidates.tsv` is 12,318 rows.
Nobody opens a browser against 12,318 rows, so the report was in practice unusable for the step
it exists to serve. This is the top of it, as pages that can be clicked.

**Izumo first, and they had to be found by ID rather than by name.** She named them as the place
to start, and searching the candidate file for `izumo` returns nothing — the profiles are called
`Senge`, `Kitajima`, `Takatoshi` and so on. The ids are joined from every `reports/izumo*.tsv`
— see `izumo_ids()` for why one file is not enough. `CLAUDE.md` § *"Is X present?"* is explicit
that the id is the key on both sides and that a name search is at best a way to pick candidates
for a join — the same session that grepped for `Shalma|Tabia|Abta` missed 35 priests and matched
an Assyrian king.

**Then the CJK groups**, because that is the higher scrutiny she asked for, ranked by group size.
`CLAUDE.md` records what sits at the top of that section and it is repeated in the output: the
`Tanba` groups are the real signal, and a residue of bare one-token surnames (`杨`, `黄`, `邱`)
survives because those people have a given name recorded somewhere while their `cjk_names`
carries only the surname.

Writes `reports/geni-merge-worklist.md`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

CANDIDATES = ROOT / "reports" / "geni-duplicate-candidates.tsv"
OUT = ROOT / "reports" / "geni-merge-worklist.md"

#: A Geni profile id, as it appears anywhere in a report. Every one in the corpus is 19 digits
#: beginning `6`; `CLAUDE.md` § *four xref prefixes* is why a looser pattern is not used.
GENI_ID = re.compile(r"\b(6\d{18})\b")

#: How many CJK groups to list after the Izumo ones. A worklist longer than a sitting is a
#: report again, which is the thing this exists to stop being.
CJK_LIMIT = 40
PROFILE = "https://www.geni.com/people/x/{}"


def izumo_ids():
    """Every Geni id named anywhere in the Izumo reports.

    **Read across all of them, not out of one.** The obvious file, `izumo-coverage.tsv`, has a
    `geni_ids` column and **202 of its 214 rows read `NO GENI ID`** — so a join against it
    finds 2 ids and 0 candidate groups, which looks exactly like "there are no Izumo
    duplicates" and is not. The ids live in the files that were built by walking Geni:
    `izumo-geni-anchors.tsv` (102), `izumo-sister-p2600-pairs.tsv` (121),
    `izumo-p2600-pairs.tsv` (111), `izumo-kokuso-geni.tsv` (100) and others, overlapping into
    **210** distinct ids.

    `CLAUDE.md` § *Do not grab the first artifact that vaguely matches* is the rule this
    follows: the first file whose name and column headings fit the question was the wrong one,
    and taking its answer would have closed the question with a false negative.
    """
    ids = set()
    for path in sorted((ROOT / "reports").glob("izumo*.tsv")):
        ids |= set(GENI_ID.findall(path.read_text(encoding="utf-8")))

    # **The BIO links are the stated correspondence and are consulted first.** Emma,
    # 2026-08-31: *"Yeah you use the bio qids lol."* She writes `wikidata.org/wiki/Q…` into a
    # Geni profile's About Me, so `reports/bio-qids.tsv` is her own identity claim, captured by
    # whichever export ran after she made it -- fresher than any download.
    #
    # **For Izumo they are thin, and saying so is the point.** The 204 roster QIDs resolve to
    # **8** Geni ids through the bio links, all 8 already inside the 210 above. That is not a
    # failure of the source; it is the measurement that the bio-link campaign has barely reached
    # this family.
    #
    # `out/wikidata/p2600-all.tsv` gives **2**, and that is not staleness -- the file was
    # refreshed from live Wikidata on 2026-08-30 and the answer did not move. Only 2 of those
    # 204 items carry a `P2600` at all. The staleness reading was assumed here before the
    # refresh that refuted it, which is the failure `CLAUDE.md` § *CHECK before you alarm her*
    # names.
    bio = collections.defaultdict(set)
    bio_path = ROOT / "reports" / "bio-qids.tsv"
    if bio_path.exists():
        with bio_path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                bio[row["qid"]].add(row["geni_id"])
    roster_qids = set()
    for name in ("izumo-roster.tsv", "izumo-coverage.tsv"):
        path = ROOT / "reports" / name
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if (row.get("qid") or "").strip():
                    roster_qids.add(row["qid"].strip())
    from_bio = {g for q in roster_qids for g in bio.get(q, ())}
    print(f"   bio links contribute {len(from_bio)} of the {len(ids | from_bio)} Izumo ids")
    return ids | from_bio


def render(fh, rows, heading, note=""):
    fh.write(f"## {heading}\n\n")
    if note:
        fh.write(note + "\n\n")
    if not rows:
        fh.write("None.\n\n")
        return
    for r in rows:
        name = r["cjk_name"] or r["name"] or "(no name recorded)"
        fh.write(f"- **{name}** — {r['count']} profiles, {r['signal']}")
        if r.get("father_name"):
            fh.write(f", child of {r['father_name']}")
        fh.write("\n")
        for gid in r["geni_ids"].split(";"):
            fh.write(f"    - {PROFILE.format(gid)}\n")
    fh.write("\n")


def main():
    rows = list(csv.DictReader(CANDIDATES.open(encoding="utf-8"), delimiter="\t"))
    print(f"{len(rows):,} candidate groups")

    roster = izumo_ids()
    print(f"{len(roster):,} Izumo roster ids")

    izumo = [r for r in rows if roster & set(r["geni_ids"].split(";"))]
    rest = [r for r in rows if r not in izumo]
    cjk = [r for r in rest if r["script"] in ("Han", "Kana", "mixed")]
    cjk.sort(key=lambda r: (-int(r["count"]), r["name"]))

    with OUT.open("w", encoding="utf-8") as fh:
        fh.write("# Geni merge worklist\n\n")
        fh.write("**The merges are Emma's and are never performed here.** This is only the "
                 "order to look in, and the pages to look at. `scripts/find-geni-duplicates.py` "
                 "produces the candidates; this is the top of them.\n\n")
        fh.write(f"`reports/geni-duplicate-candidates.tsv` holds **{len(rows):,}** groups, "
                 "which is not something anyone opens a browser against. That is why this "
                 "exists.\n\n")
        fh.write("**A candidate is a candidate, not a duplicate.** `CLAUDE.md` § *The question "
                 "is whether OUR TREE MATCHES GENI* governs: the only question a pair raises is "
                 "whether our snapshot still matches Geni today. Whether the two people should "
                 "be one is not ours to adjudicate.\n\n")

        render(fh, izumo, f"Izumo — {len(izumo)} groups",
               "Emma, 2026-08-24: *\"Izumo ones are good to explore to see how redirects "
               "potentially work.\"* Found by joining the candidate ids against the 210 ids "
               "named across every `reports/izumo*.tsv`; searching the candidate file for "
               "`izumo` finds none of them, because the profiles are called Senge, "
               "Kitajima and so on.")

        render(fh, cjk[:CJK_LIMIT],
               f"Japanese and Chinese — top {min(CJK_LIMIT, len(cjk))} of {len(cjk)}",
               "Her *\"higher scrutiny\"* pass, biggest groups first. The `Tanba` groups are "
               "the real signal. A residue of bare one-token surnames (`杨`, `黄`, `邱`) "
               "survives because those people have a given name recorded somewhere while "
               "their `cjk_names` carries only the surname — those are an artefact of the "
               "name column, not evidence of duplication.")

    print(f"Izumo groups: {len(izumo)}   CJK groups: {len(cjk)}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
