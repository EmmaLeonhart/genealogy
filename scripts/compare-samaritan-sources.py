"""The hand-transcribed Samaritan GEDCOMs against what Geni now holds.

Queue item 9b. **Emma, 2026-08-16, explicitly without an answer:** *"I don't
really know what you're supposed to do with the old Samaritan stuff. Now that we
have this new Samaritan stuff, has that one changed relationship? This
relationship would kind of either have to be changed in them or they need to be
superseded… I think it's an easy thing to do but I don't know."*

**This compares and reports. It supersedes nothing.** `gedcom/samaritan-sources.ged`
and `gedcom/samaritan-itamar-spine.ged` are transcribed by hand from published
sources — A.B. *The Samaritan News*, Tsedaka's *The High Priesthood and the
Israelite Samaritan Priests* — and carry **no Geni profile IDs**. A published
source is not overridden because a website now has the same names.

**Matching is by name, and that is defensible here for the same reason it was for
`samaritans/priests.txt`:** both sides are small and hand-made. 185 and 120
people against the Samaritan exports, not against 396,181. `correspondence.md`
bans *searching* for a name across everything; this is a bounded join between two
curated sets.

**Unnamed people are skipped, not guessed at.** The transcription marks explicit
placeholders as `1 NAME //` with the reasoning in a `NOTE` — generations the
source records as existing without naming. They cannot be matched and must not be
invented into a match.

**What the comparison is for** is the parent relation. For each person present in
both, does the transcription and Geni agree about who the father is? Three
outcomes:

* `AGREE` — same father name on both sides.
* `DISAGREE` — **the thing Emma is asking about.** Reported with both, never
  resolved here.
* `GENI ONLY` / `SOURCE ONLY` — one side records a father and the other does not.

Writes `reports/samaritan-source-comparison.csv`.

    py scripts/compare-samaritan-sources.py
"""

from __future__ import annotations

import csv
import glob
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SOURCES = [REPO / "gedcom" / "samaritan-sources.ged",
           REPO / "gedcom" / "samaritan-itamar-spine.ged"]
EXPORTS = REPO / "exports" / "samaritans"
OUT = REPO / "reports" / "samaritan-source-comparison.csv"

INDI = re.compile(r"^0 @(I[\w\d]+)@ INDI")
FAM = re.compile(r"^0 @(F[\w\d]+)@ FAM")
NAME = re.compile(r"^1 NAME (.*)$")
HUSB = re.compile(r"^1 HUSB @(I[\w\d]+)@")
CHIL = re.compile(r"^1 CHIL @(I[\w\d]+)@")
FAMC = re.compile(r"^1 FAMC @(F[\w\d]+)@")


def read(path):
    """names[id], father[id] -> id, for one GEDCOM."""
    names, famc, husb, chil = {}, {}, {}, {}
    cur_i = cur_f = None
    for line in open(path, encoding="utf-8-sig", errors="replace"):
        m = INDI.match(line)
        if m:
            cur_i, cur_f = m.group(1), None
            continue
        m = FAM.match(line)
        if m:
            cur_f, cur_i = m.group(1), None
            continue
        if cur_i:
            m = NAME.match(line)
            if m and cur_i not in names:
                names[cur_i] = m.group(1).strip()
            m = FAMC.match(line)
            if m:
                famc[cur_i] = m.group(1)
        elif cur_f:
            m = HUSB.match(line)
            if m:
                husb[cur_f] = m.group(1)
            m = CHIL.match(line)
            if m:
                chil.setdefault(cur_f, []).append(m.group(1))
    father = {c: husb[f] for c, f in famc.items() if f in husb}
    return names, father


#: Regnal numerals. The transcription writes `Tsedaka ben Tabia`; Geni writes
#: `Tsedaka II ben Tabia ha'Åbtå'i`. Dropping them is what stops the same person
#: being counted as absent — the first pass of this script reported 69 people as
#: "not on Geni" and several of them were there under a number.
NUMERALS = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
            "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx"}
NOISE = {"ben", "bin", "the"} | NUMERALS


def tokens(text: str) -> list[str]:
    text = text.replace("/", " ")
    text = re.sub(r"\bha'?[a-zåäöÀ-ɏ]+\b", " ", text.lower())
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return [t for t in text.split() if t not in NOISE]


def norm(text: str) -> str:
    return " ".join(tokens(text))


def main() -> int:
    geni_names, geni_father = {}, {}
    for path in sorted(glob.glob(str(EXPORTS / "*.ged"))):
        n, f = read(path)
        for k, v in n.items():
            geni_names.setdefault(k, v)
        geni_father.update(f)
    print(f"{len(geni_names):,} people across the Samaritan exports")

    # **Match on the person AND their father — two points, not one.**
    #
    # Three passes were needed to get here and the first two were wrong in
    # opposite directions. Exact normalised names were too strict: the two sides
    # decorate differently and in *both* directions — Geni writes `Aaron I
    # /Samaritan High Priest/` where the source writes `Aaron /ben Amram/`, and
    # plain `Ab-Hisda` where the source writes `Ab-Hisda /ben Jacob/`. Dropping
    # the numerals was too loose: `Levi` then matched any Levi, and it paired
    # `Levi ben Abraham` with a man whose father is Simeon.
    #
    # What works is what the rest of this repo already relies on: **the structure
    # confirms, the name only locates.** Two people are the same when their own
    # leading name agrees *and* their fathers' leading names agree. Decoration
    # falls out; a wrong Levi does not survive the father check.
    def lead(text: str) -> str:
        tk = [x for x in tokens(text) if x not in NUMERALS]
        return tk[0] if tk else ""

    geni_lead: dict[str, list[str]] = {}
    for gid, nm in geni_names.items():
        key = lead(nm)
        if key:
            geni_lead.setdefault(key, []).append(gid)

    def find(name: str, father_name: str):
        key = lead(name)
        if not key:
            return [], ""
        pool = geni_lead.get(key, [])
        if not pool:
            return [], ""
        want_f = lead(father_name)
        if want_f:
            confirmed = [g for g in pool
                         if lead(geni_names.get(geni_father.get(g, ""), "")) == want_f]
            if confirmed:
                return confirmed, "name and father agree"
        # No father on our side, or none of the candidates' fathers agree. Only
        # accept a bare-name match when it is unambiguous; otherwise say so
        # rather than picking one.
        if not want_f and len(pool) == 1:
            return pool, "name only, unique"
        if len(pool) == 1:
            return pool, "name only, unique - father differs or is absent"
        return [], "ambiguous on name alone"

    rows, counts = [], Counter()
    for path in SOURCES:
        names, father = read(path)
        named = {i: n for i, n in names.items() if norm(n)}
        print(f"\n{path.name}: {len(names)} people, {len(named)} named, "
              f"{len(names) - len(named)} explicit placeholders")
        for pid, nm in sorted(named.items()):
            key = norm(nm)
            sf_name = names.get(father.get(pid, ""), "")
            matches, how = find(nm, sf_name)
            if not matches:
                counts["in the source only - not on Geni"] += 1
                rows.append({"source_file": path.name, "source_name": nm,
                             "geni_id": "", "geni_name": "",
                             "source_father": names.get(father.get(pid, ""), ""),
                             "geni_father": "", "matched_by": "", "verdict": "not on Geni"})
                continue
            if len(matches) > 1:
                counts["ambiguous - several Geni people share the name"] += 1
            gid = matches[0]
            sf = sf_name
            gf = geni_names.get(geni_father.get(gid, ""), "")
            if sf and gf:
                # **Compare the father's own name, not the whole string.** Geni
                # decorates it — `Aaron I /Samaritan High Priest/` against the
                # transcription's `Aaron /ben Amram/`, `Tabia III` against
                # `Tabia`, `Phinehas` against `Phinhas`. Comparing normalised
                # full names called 13 of these a disagreement when the two
                # sides name the same man. The claim being tested is *who the
                # father is*, and that is the leading token.
                a = [x for x in tokens(sf) if x not in NUMERALS]
                b = [x for x in tokens(gf) if x not in NUMERALS]
                same = bool(a and b and (a[0] == b[0] or set(a) & set(b)))
                verdict = "AGREE" if same else "DISAGREE"
            elif sf:
                verdict = "source only: Geni records no father"
            elif gf:
                verdict = "geni only: the source records no father"
            else:
                verdict = "neither records a father"
            counts[verdict] += 1
            rows.append({"source_file": path.name, "source_name": nm,
                         "geni_id": gid, "geni_name": geni_names[gid],
                         "source_father": sf, "geni_father": gf,
                         "matched_by": how, "verdict": verdict})

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {OUT} ({len(rows)} rows)\n")
    for k, v in counts.most_common():
        print(f"  {v:>4}  {k}")
    dis = [r for r in rows if r["verdict"] == "DISAGREE"]
    if dis:
        print(f"\nthe {len(dis)} disagreements, which are the question:")
        for r in dis[:25]:
            print(f"  {r['source_name'][:30]:<32}"
                  f"source says {r['source_father'][:22]:<24}"
                  f"geni says {r['geni_father'][:22]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
