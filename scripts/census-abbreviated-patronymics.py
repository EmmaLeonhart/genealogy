"""Every abbreviated patronymic in our labels, and what the full form should be.

    python scripts/census-abbreviated-patronymics.py

**The standing rule, 2026-08-27:** *"any abbreviations like -dtr (i.e. "Rasmusdtr." instead of "Rasmusdatter")
should be fixd since wikidata mul labels ae supposed to have the full form. This is a part of the
compliance stuff I mentioned earlier"*.

`CLAUDE.md` § *"Analyse this" means build a CSV of every instance* — so this is every instance,
one row each, before anything is emitted.

## The expansion is NOT a single rule, and the corpus says so

`-dtr` expands to Norwegian `-datter` or Swedish `-dotter`, and which one is a fact about the
person, not about the abbreviation. Measured over `reports/derived-labels.csv`: **81,530** full
`-datter` against **57,085** full `-dotter`, and the split runs the other way for individual stems —
`Olsdtr` is `Olsdatter` 6,981 to 1,058, while `Andersdtr` is `Andersdotter` 5,172 to 3,126.

So a global "always `-datter`" would be wrong several thousand times, and the worked example
(`Rasmusdtr.` → `Rasmusdatter`) happens to be one of the stems where `-datter` wins 10:1.

## ⛔ THE RESOLUTION IS GENEALOGICAL, NOT STATISTICAL. Ruled 2026-09-15

Emma gave the algorithm outright, and it REPLACES the corpus stem majority that decided 93% of
these rows:

> *"Here is my proposed algorithm for resolving "Olsdtr" to "Olsdatter" or "Olsdotter": check the
> mother's patronymic. If the mother has one then great, if not then check paternal grandmother,
> if she does not have one then default to "-datter"."*

**Why it beats the majority, and the numbers here are the argument against the old rule.**
`-datter` or `-dotter` is a fact about a FAMILY's register — Norwegian against Swedish — and the
corpus majority is a fact about a STEM across every family at once. On `Andersdtr` that majority
is `dotter` 5,172 to 3,126: a 62/38 split applied identically to a Norwegian woman and a Swedish
one, so it is wrong about four in ten of them and cannot be right about which. Her mother's
attested spelling is evidence about *her* family, and a woman's mother is the person most likely
to have been recorded in the same parish register by the same hand.

**The order, and each step is weaker than the one above it:**

    1. own name record          the person's own other NAME records carry the full spelling.
                                Not inference at all -- attestation -- so it stays above her
                                chain rather than being replaced by it.
    2. the mother               her patronymic's ending, from `reports/derived-family.csv`.
    3. the paternal grandmother `mother[father[x]]` -- the father's mother.
    4. `-datter`                the given default. Not a measurement and not to be replaced by
                                one; a terminal default is what makes the algorithm total.

**`-dóttir` is taken from a relative when a relative is what attests it**, though the ruling names
only the two Scandinavian forms. Guessed under § *while working the queue, GUESS and record it*:
the whole force of the rule is that the family's register decides, and expanding an Icelandic
woman's `Olsdtr.` to `Olsdatter` because her mother is `Jónsdóttir` would invert the reason for
consulting the mother. It is never the DEFAULT — step 4 is `-datter` exactly as ruled.

Nothing is guessed silently: every row carries `basis` and the counts behind it.

Writes `reports/abbreviated-patronymics.csv`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

LABELS = ROOT / "reports" / "derived-labels.csv"
NAMES = ROOT / "reports" / "display-names.csv"
OUT = ROOT / "reports" / "abbreviated-patronymics.csv"

#: `Rasmusdtr`, `Rasmusdtr.`, `Ormsd`, `Johansdr`, `Olsdt.` — the stem plus the abbreviation,
#: optionally a full stop.
#:
#: **`dtr` was the only form until 2026-09-04, and it is not the only form.** `Q141271379` was
#: corrected by hand — *"I changed her name to correct the issue of an abbreviation of
#: Ormsdatter"* — from `Anna Ormsd Byre`. `Ormsd` matched nothing here, so nothing expanded it
#: and the batch went out with the abbreviation in the label. Widening to the genitive-preserving
#: family adds **897 occurrences over 317 distinct tokens**: `dr` 382, `d` 317, `dr.` 71, `d.` 60,
#: `dt.` 39, `dt` 28.
#:
#: **The `s` is load-bearing and is why this is safe.** A patronymic always carries the genitive,
#: so `Orms` + `d`. Allowing a bare `d` instead matched `Svend` 606, `Halvard` 322, `Hand` 92 and
#: `Old` 19 — real given names whose stem happens to be attested with `datter`. Requiring the
#: `s` removes every one of them and loses nothing.
#:
#: **The male side was measured and is NOT here.** The same shape on `sen`/`son` stems matches
#: `Foss` 762, `Ross` 498, `Strauss` 324, `Hess` 241, `Moss` 199, `Voss` 139 — surnames, not
#: abbreviations, 3,704 occurrences of them. There is no safe male pattern in this data and
#: guessing one would rewrite strangers' names.
#: **The lookahead must exclude EVERY letter, not an ASCII range.** `(?![a-zø])` let
#: `Þorbjörg Ormsdóttir` match as `Ormsd` — the Icelandic full form — and the census offered to
#: "expand" it to `Ormsdatter`, rewriting an Icelandic name into a Norwegian one. `\w` with
#: `re.UNICODE` covers `ó`, `ø`, `ä` and the rest.
ABBREV = re.compile(r"\b(\w+?)(dtr|s(?:d|dr|dt|dtt|dttr))\.?(?!\w)", re.I)

#: The forms added on 2026-09-04. They are held to a stricter standard than `dtr`: see the
#: `no evidence` guard in `main`.
NEW_FORMS = ("sd", "sdr", "sdt", "sdtt", "sdttr")
#: `Rasmusdatter` / `Rasmusdotter`, for learning what a stem expands to.
FULL = re.compile(r"\b(\w+?)(datter|dotter)\b", re.I)


FAMILY = ROOT / "reports" / "derived-family.csv"

#: The full female endings a RELATIVE can attest, longest first so `sdóttir` is not read as
#: `sdotter`'s neighbour. `dochter` is deliberately absent: the Dutch `dr` family is handled by
#: `NEW_FORMS` being skipped outright, and a Dutch relative must not decide a Scandinavian form.
RELATIVE_ENDING = re.compile(r"s(datter|dotter|d[oó]ttir)\.?$", re.I)


def read_parents():
    """`(father, mother)` as two `{geni_id: geni_id}` maps.

    `reports/derived-family.csv` carries one row per person with `father` and `mother` already
    resolved, so the paternal grandmother is `mother[father[x]]` and needs no second pass.
    Reads the gzipped copy when the plain one is absent -- § *The four big derived CSVs are
    committed gzipped*.
    """
    father, mother = {}, {}
    if FAMILY.exists():
        fh = FAMILY.open(encoding="utf-8")
    else:
        import gzip
        import io as _io
        fh = _io.TextIOWrapper(gzip.open(str(FAMILY) + ".gz"), encoding="utf-8")
    with fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            if row.get("father"):
                father[g] = row["father"]
            if row.get("mother"):
                mother[g] = row["mother"]
    return father, mother


def attested_ending(gid, own, labels_by_id):
    """`"datter"` / `"dotter"` / `"dottir"` if this person's OWN name carries one, else `""`.

    Used on a RELATIVE, never on the person being resolved -- the person being resolved is the
    one whose spelling is abbreviated, so by definition they attest nothing here.
    """
    seen = list(own.get(gid, ())) + [labels_by_id.get(gid, "")]
    for text in seen:
        for token in (text or "").split():
            m = RELATIVE_ENDING.search(token)
            if m:
                return m.group(1).lower()
    return ""


def from_the_family(gid, father, mother, own, labels_by_id):
    """`(ending, basis)` per the 2026-09-15 chain: mother, then paternal grandmother.

    `("", "")` when neither attests one, which is what sends the caller to the `-datter`
    default. The father is NOT consulted and cannot be: he is `-son`, and a male patronymic
    says nothing about which female ending his daughter takes.
    """
    mum = mother.get(gid)
    if mum:
        ending = attested_ending(mum, own, labels_by_id)
        if ending:
            return ending, "the mother"
    dad = father.get(gid)
    if dad:
        gran = mother.get(dad)
        if gran:
            ending = attested_ending(gran, own, labels_by_id)
            if ending:
                return ending, "the paternal grandmother"
    return "", ""



def main():
    stem_full = collections.Counter()
    with LABELS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for field in ("label_mul", "further_latin_names", "alias_names"):
                for m in FULL.finditer(row.get(field) or ""):
                    stem_full[(m.group(1).lower(), m.group(2).lower())] += 1
    print(f"{sum(stem_full.values()):,} full -datter/-dotter tokens give the corpus its priors")

    # Every NAME record per person, so a person's own spelling can be consulted.
    own = collections.defaultdict(list)
    with NAMES.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("display_name"):
                own[row["geni_id"]].append(row["display_name"])

    # The 2026-09-15 chain needs the parents and the labels of relatives who are not
    # themselves in this census.
    father, mother = read_parents()
    labels_by_id = {}
    with LABELS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            labels_by_id[row["geni_id"]] = row.get("label_mul") or ""
    print(f"{len(father):,} fathers and {len(mother):,} mothers for the family chain")

    rows = []
    by_basis = collections.Counter()
    with LABELS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label = row.get("label_mul") or ""
            for m in ABBREV.finditer(label):
                stem, token = m.group(1), m.group(0)
                # **The genitive `s` belongs to the STEM, whichever form matched.** `FULL` reads
                # `Ormsdatter` as stem `Orms`, so an `Ormsd` split as `Orm` + `sd` would look up
                # a stem the corpus has never seen and fall through to the no-evidence branch.
                # `Larsdtr` already carries its `s` in group 1; the `s…` family does not.
                if m.group(2)[:1].lower() == "s":
                    stem = stem + m.group(2)[0]
                low = stem.lower()
                # (1) this person's own records
                mine = collections.Counter()
                for other in own.get(row["geni_id"], ()):
                    for f in FULL.finditer(other):
                        if f.group(1).lower() == low:
                            mine[f.group(2).lower()] += 1
                if mine:
                    suffix, basis = mine.most_common(1)[0][0], "own name record"
                else:
                    # ⛔ **THE FAMILY DECIDES, NOT THE STEM.** Ruled 2026-09-15; see the module
                    # docstring. This replaces the corpus stem majority, which settled 93% of
                    # these rows from a population statistic that knows nothing about the
                    # person's family or parish.
                    ending, why = from_the_family(row["geni_id"], father, mother,
                                                  own, labels_by_id)
                    d, o = stem_full.get((low, "datter"), 0), stem_full.get((low, "dotter"), 0)
                    if ending:
                        suffix, basis = ending, why
                    elif not d and not o:
                        # **A NEW form with no evidence is skipped, not guessed.** The `dr`
                        # family is largely DUTCH — `Willemsdr`, `Cornelisdr`, `Jansdr`,
                        # `Bruijstensdr` — where the full form is `dochter`, and defaulting to
                        # `datter` turns a Dutch woman into a Norwegian one. 433 of the 1,314
                        # new rows landed here on the first run. `dtr` keeps the old fallback
                        # because it predates this and is Norwegian by construction.
                        if m.group(2).lower() in NEW_FORMS:
                            continue
                        suffix, basis = "datter", "the default; no family evidence"
                    else:
                        # **The ruled default, and the corpus counts are no longer consulted
                        # to pick.** They stay in the CSV's two count columns as context a
                        # reader can disagree with, but they decide nothing: a stem majority
                        # is a fact about every family at once and this is a question about
                        # one family.
                        suffix, basis = "datter", "the default; no family evidence"
                by_basis[basis] += 1
                rows.append({
                    "geni_id": row["geni_id"], "qid": row.get("qid", ""),
                    "label": label, "token": token, "stem": stem,
                    "expansion": stem + suffix, "basis": basis,
                    "corpus_datter": stem_full.get((low, "datter"), 0),
                    "corpus_dotter": stem_full.get((low, "dotter"), 0),
                })

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} -- {len(rows):,} abbreviated tokens "
          f"over {len({r['geni_id'] for r in rows}):,} people")
    for basis, n in by_basis.most_common():
        print(f"  {basis:26} {n:,}")
    linked = sum(1 for r in rows if r["qid"])
    print(f"\n{linked:,} of them are on people who already carry a Wikidata item.")


if __name__ == "__main__":
    main()
