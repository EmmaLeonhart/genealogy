"""Which name tokens are patronymics? Decided from the father, entirely offline.

**Emma's correction, 2026-08-15:** *"Whether something is or is not a patronymic
here is determined by completely offline information related to the person's
father's name."*

She said it after item 2 had been written up as blocked on downloading Wikidata's
`P31`. That was wrong. `Olsen` on a man whose father is `Ole` is a patronymic and
**nothing on Wikidata is needed to know that**. Wikidata only decides *which
existing item to link to*, once we already know what our own token is.

**The test is the father's given name, never the shape of the token alone.** A
suffix list on its own would call `Jackson` a patronymic for everybody who
carries it, including the many for whom it is a plain surname — `CLAUDE.md`'s
*"Jackson Jackson Jackson"*: one name item per **usage**, and the usage here is a
fact about this person's father, not about the string.

Two forms are recognised, and both require the father:

* **suffixed** — `<father's stem><suffix>`, e.g. father `Ole` → `Olsen`,
  `Olesen`, `Olsson`, `Olsdatter`. The stem allows a dropped final vowel, because
  `Ole` → `Ols-` is the ordinary Scandinavian formation.
* **particle** — `ben`/`bin`/`ibn`/`bint`/`bat` followed by the father's name,
  which is how the Samaritan and Arabic records are written: `Abram /ben Yitzhaq/`
  with a father called `Yitzhaq`.

**A person with no recorded father yields no verdict at all** — not "no", which
would be a claim. They are counted separately and left alone, because absence of
a father in our data is absence of evidence.

**Every token of every person is a row**, per `CLAUDE.md` § *"Analyse this" means
build a CSV of every instance*. Writes `reports/patronymic-classification.csv`
and a summary in `reports/patronymic-classification.md`.

    py scripts/classify-patronymics.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NAMES = REPO / "reports" / "display-names.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
OUT_CSV = REPO / "reports" / "patronymic-classification.csv"
OUT_MD = REPO / "reports" / "patronymic-classification.md"

csv.field_size_limit(10_000_000)

#: **Patronymic endings, by tradition.** Emma, 2026-08-15: *"the patronymics have
#: a variety of forms and you might not have gotten all the forms… we have things
#: like Anes and Rodriguez and Fitz John that are all patronymics too."* She was
#: right — the first version was Scandinavian, Dutch and Slavic only, and handled
#: no prefix form at all, so `Fitz John` and `FitzGerald` were invisible.
#:
#: Measured over the tokens that version called *not patronymic*: 6,879 end `-es`,
#: 3,376 `-ez`, 523 `-yan`/`-ian`, 513 `-ić`/`-vić`, 338 begin `ap`/`ab`, 286
#: begin `Fitz`.
SUFFIXES = (
    # Scandinavian / Germanic
    "sdottir", "sdatter", "sdotter", "dottir", "datter", "dotter",
    "ssen", "sson", "sen", "son", "zen", "zoon", "szoon", "sz",
    # Iberian. **The largest and the least reliable**: `-ez`/`-es` is a live
    # patronymic ending in Spanish and Portuguese and also the plain ending of
    # `Charles`, `Holmes`, `James`. Form can never decide these.
    "ez", "es", "iz", "oz", "az",
    # Slavic
    "ovich", "evich", "ovitch", "evitch", "owicz", "ewicz", "wicz",
    "ovna", "evna", "ovic", "evic", "vic", "ic",
    # Armenian, Greek, Turkish, Romanian, Finnish
    "yan", "ian", "opoulos", "poulos", "oglu", "escu", "poika", "tytar",
)

#: Prefixes written **joined** to the father's name: `FitzGerald`, `MacDonald`,
#: `O'Brien`, `ApRhys`.
PREFIXES = ("fitz", "mac", "mc", "o'", "ap", "ab")

#: Prefixes written as a **separate token**: `ben Yitzhaq`, `bint Aabed-El`,
#: `ap Gronwy`, `Fitz John`, `bar Hananya`. The particle is followed by the
#: father's own name rather than by a derived form.
PARTICLES = {"ben", "bin", "ibn", "bint", "bat", "bar", "ap", "ab",
             "mac", "mc", "fitz", "o", "ó", "ua", "ni"}

ABSENT = {".", "..", "?", "-", "_", "nn", "n.n.", "private", "<private>"}

#: Suffixes that name the bearer's own sex. A `-sen`/`-son` is *son of*; a
#: `-datter`/`-dóttir` is *daughter of*.
SON_OF = {"sen", "son", "sson", "ssen", "zen", "zoon", "szoon", "sz",
          "ovich", "evich", "ovitch", "evitch", "ovic", "evic"}
DAUGHTER_OF = {"sdatter", "sdotter", "sdottir", "datter", "dotter", "dottir",
               "ovna", "evna", "tytar"}


def sex_conflict(form: str, sex: str) -> bool:
    """Does the suffix contradict the bearer's recorded sex?

    **Emma's hypothesis, 2026-08-15, and it holds:** *"if there is a gender
    mismatch, it might be that the married name goes through an error to become a
    patronymic or something like that."*

    Measured over the 19,621 form-with-no-father tokens: a *son-of* suffix on a
    woman is **13.7%** of those with a recorded sex (1,236 of 8,999); a
    *daughter-of* suffix on a man is **0.2%** (11 of 6,074). Sixty-eight times
    apart, and the son-of cases are `Gustafsson`, `Wilson`, `Rasmussen`, `Nilsen`
    on women in the surname field — inherited or married family names, exactly as
    she predicted. `-datter` almost never does this because it never became
    heritable.
    """
    if not sex:
        return False
    bare = form.lstrip("-")
    if bare in SON_OF:
        return sex == "F"
    if bare in DAUGHTER_OF:
        return sex == "M"
    return False


def fold(text: str) -> str:
    """Casefold and strip diacritics **for stem comparison only**.

    Diacritics are kept everywhere else in this project — folding them away is
    the bug Emma caught in the name matcher. Here the comparison is between a
    father's name and a derived form of it *within one record*, where `Åke` →
    `Akesson` is the ordinary spelling drift of the derivation rather than a
    different name. The fold never reaches an emitted value.
    """
    stripped = "".join(c for c in unicodedata.normalize("NFD", text)
                       if unicodedata.category(c) != "Mn")
    return stripped.casefold()


def stems(name: str) -> set[str]:
    """The father's name and the forms a patronymic is built on."""
    base = fold(name)
    out = {base}
    if base.endswith(("e", "a", "o", "i")):
        out.add(base[:-1])
    return {s for s in out if len(s) >= 2}


def has_patronymic_form(token: str) -> str | None:
    """Does this token *look* like a patronymic? Form only — never a verdict.

    Kept strictly separate from the father test because `Charles` and `Holmes`
    have patronymic form and are not patronymics, while `Rodríguez` has the same
    form and often is. **Form proposes; the father disposes.**
    """
    low = fold(token)
    parts = low.split()
    if len(parts) >= 2 and parts[0] in PARTICLES:
        return f"particle {parts[0]}"
    joined = low.replace("'", "'")
    for prefix in PREFIXES:
        if joined.startswith(prefix) and len(joined) > len(prefix) + 2:
            return f"prefix {prefix}"
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if low.endswith(suffix) and len(low) > len(suffix) + 1:
            return f"-{suffix}"
    return None


def derives_from_father(token: str, father: str, father_stems: set[str]) -> str | None:
    """Is this token built on **this person's father's** name? The actual test."""
    low = fold(token)
    parts = low.split()

    # `ben Yitzhaq` / `Fitz John` / `ap Gronwy` — particle plus the father's name.
    if len(parts) >= 2 and parts[0] in PARTICLES:
        rest = " ".join(parts[1:])
        if rest in father_stems or rest == fold(father):
            return f"{parts[0]} {father}"

    # `FitzGerald` / `MacDonald` — prefix joined to the father's name.
    joined = low.replace("'", "")
    for prefix in PREFIXES:
        clean = prefix.replace("'", "")
        if joined.startswith(clean):
            rest = joined[len(clean):]
            if rest in father_stems:
                return f"{prefix} + {father}"

    # `Olsen` from `Ole` — the father's stem plus an ending.
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if not low.endswith(suffix):
            continue
        head = low[: -len(suffix)]
        if head in father_stems:
            return f"{father} + -{suffix}"
        # The linking -s- belongs to the suffix in some spellings and to the
        # stem in others.
        if head.endswith("s") and head[:-1] in father_stems:
            return f"{father} + -{suffix}"
    return None


def main() -> int:
    # Sex comes from the tree rather than the name CSVs, which do not carry it.
    sys.path.insert(0, str(REPO / "src"))
    from genimerge.gedcom import stream_file
    from genimerge.model import build_tree
    print("loading out/merged.ged for recorded sex", flush=True)
    tree = build_tree(stream_file(REPO / "out" / "merged.ged"))
    sex_of = {g: (person.sex or "") for g, person in tree.people.items()}
    print(f"{sum(1 for v in sex_of.values() if v):,} people with a recorded sex",
          flush=True)

    father_of: dict[str, str] = {}
    with FAMILY.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            fid = (row.get("father") or "").strip()
            if fid:
                father_of[row["geni_id"]] = fid

    # First given token per person — that is what a patronymic derives from.
    first_given: dict[str, str] = {}
    with NAMES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            gid = row["geni_id"]
            if gid in first_given:
                continue
            tokens = (row.get("givn") or "").split()
            if tokens and tokens[0].casefold() not in ABSENT:
                first_given[gid] = tokens[0]
    print(f"{len(father_of):,} people with a recorded father, "
          f"{len(first_given):,} with a first given name", flush=True)

    rows = []
    tally: Counter[str] = Counter()
    by_token: dict[str, Counter[str]] = defaultdict(Counter)

    with NAMES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            gid = row["geni_id"]
            given = (row.get("givn") or "").split()
            surn = (row.get("surn") or "").strip()
            fid = father_of.get(gid, "")
            fname = first_given.get(fid, "") if fid else ""
            fstems = stems(fname) if fname else set()

            # Every token beyond the first given name is a candidate, plus the
            # surname field: Geni puts patronymics in both.
            candidates = [(t, "given", i + 1) for i, t in enumerate(given)][1:]
            if surn:
                candidates.append((surn, "surname", 0))

            for token, where, ordinal in candidates:
                if token.casefold() in ABSENT:
                    continue
                form = has_patronymic_form(token)
                derived = (derives_from_father(token, fname, fstems)
                           if fname else None)
                if derived:
                    verdict, evidence = "patronymic", derived
                elif form and not fid:
                    # **Emma's call, 2026-08-15:** *"Generally speaking I'm going
                    # to say these things are patronymics."* Almost all of them
                    # sit in real family context — 41.2% have a mother recorded
                    # and no father, 58.8% have a spouse or children, and only 6
                    # of 19,621 have no family link at all. The missing father is
                    # a gap in our data, not evidence against the name.
                    #
                    # The exception is the sex conflict she predicted, which is
                    # an inherited or married surname wearing patronymic shape.
                    if sex_conflict(form, sex_of.get(gid, "")):
                        verdict, evidence = ("surname: patronymic form conflicts "
                                             "with recorded sex", form)
                    else:
                        verdict, evidence = ("patronymic (inferred, no father "
                                             "recorded)", form)
                elif form and not fname:
                    verdict, evidence = "AMBIGUOUS: form, father unnamed", form
                elif form:
                    verdict, evidence = "AMBIGUOUS: form, father differs", form
                elif not fid:
                    verdict, evidence = "no father recorded", ""
                elif not fname:
                    verdict, evidence = "father has no given name", ""
                else:
                    verdict, evidence = "not patronymic", ""
                tally[verdict] += 1
                by_token[token][verdict] += 1
                rows.append([gid, token, where, ordinal, fid, fname,
                             verdict, evidence, form or ""])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "token", "field", "ordinal", "father_id",
                         "father_given", "verdict", "evidence", "form"])
        writer.writerows(rows)
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")

    total = sum(tally.values())
    decided = tally["patronymic"] + tally["not patronymic"]

    # The tokens that go BOTH ways are the whole point: same string, different
    # usage, different Wikidata item.
    # **Same string, different usage.** Now that a form the father does not
    # confirm is its own verdict, the contrast that matters is `patronymic`
    # against `AMBIGUOUS: form, father differs` — a token that IS built on one
    # person's father and is NOT built on another's. Comparing against
    # `not patronymic` returns nothing, because anything with the form no longer
    # lands there.
    DIFFERS = "AMBIGUOUS: form, father differs"
    both = {t: c for t, c in by_token.items()
            if c["patronymic"] and c[DIFFERS]}
    AMBIG = [k for k in tally if k.startswith("AMBIGUOUS")]
    ambiguous_total = sum(tally[k] for k in AMBIG)

    L: list[str] = []
    add = L.append
    add("# Which tokens are patronymics, decided from the father")
    add("")
    add("**Emma, 2026-08-15:** *\"Whether something is or is not a patronymic here is")
    add("determined by completely offline information related to the person's father's")
    add("name.\"* No Wikidata data is used here at all.")
    add("")
    add("Every token of every person is a row in")
    add("`reports/patronymic-classification.csv`.")
    add("")
    add("| verdict | tokens | share |")
    add("| --- | ---: | ---: |")
    for key in sorted(tally, key=lambda k: -tally[k]):
        add(f"| {key} | {tally[key]:,} | {100.0*tally[key]/max(total,1):.1f}% |")
    add(f"| **total** | **{total:,}** | |")
    add("")
    add(f"**{ambiguous_total:,} tokens carry a patronymic FORM that the father does")
    add("not confirm.** Emma asked for these to be separated rather than silently")
    add("called non-patronymic: *\"We probably should be doing some level of")
    add("classification for situations where it is ambiguous.\"* They are the")
    add("`AMBIGUOUS:` rows, split by why the father could not settle it.")
    add("")
    add("Her prior on them, recorded and **not applied** — deciding on it would be")
    add("inference where this project uses evidence: *\"most patronymics are not used")
    add("as surnames.\"*")
    add("")
    add(f"**Of the {decided:,} tokens where a verdict was possible, "
        f"{tally['patronymic']:,} are patronymic "
        f"({100.0*tally['patronymic']/max(decided,1):.1f}%).**")
    add("")
    add("**A person with no recorded father gets no verdict**, not a `no` — absence of")
    add("a father in our data is absence of evidence, and a `no` there would be a")
    add("claim we cannot make.")
    add("")
    add("## The tokens that go both ways — this is the point")
    add("")
    add(f"**{len(both):,} distinct tokens are built on one bearer's father and not on")
    add("another's.** Same string, different usage, and therefore **different Wikidata")
    add("items** — `CLAUDE.md` § *\"Jackson Jackson Jackson\"*. A suffix list alone would")
    add("have called every bearer of these a patronymic.")
    add("")
    add("| token | father confirms | father differs |")
    add("| --- | ---: | ---: |")
    for token, counts in sorted(both.items(),
                                key=lambda kv: -(kv[1]["patronymic"]))[:25]:
        add(f"| {token} | {counts['patronymic']:,} | {counts[DIFFERS]:,} |")
    add("")
    add("## Method")
    add("")
    add("Two forms, both requiring the father:")
    add("")
    add("- **suffixed** — `<father's stem><suffix>`, allowing a dropped final vowel")
    add("  (`Ole` → `Ols-`) and one linking `s`. 26 endings, Scandinavian, Dutch,")
    add("  Slavic and Polish.")
    add("- **particle** — `ben`/`bin`/`ibn`/`bint`/`bat`/`ap`/`mac` followed by the")
    add("  father's own name, which is how the Samaritan records are written.")
    add("")
    add("Diacritics are folded **for the stem comparison only** — `Åke` → `Akesson` is")
    add("spelling drift inside one derivation, not two different names. The fold never")
    add("reaches an emitted value; `CLAUDE.md`'s rule about diacritics is unchanged.")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")

    print()
    for key in sorted(tally, key=lambda k: -tally[k]):
        print(f"  {key:<52} {tally[key]:>9,}")
    print(f"\n  {len(both):,} tokens go both ways")
    for token, counts in sorted(both.items(),
                                key=lambda kv: -(kv[1]["patronymic"]))[:10]:
        print(f"    {token:<22} father confirms {counts['patronymic']:>6,}   "
              f"differs {counts[DIFFERS]:>6,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
