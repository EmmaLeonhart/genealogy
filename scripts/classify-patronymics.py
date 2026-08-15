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

#: Patronymic and matronymic endings. Order matters only in that the longest
#: match is taken first, so `sdatter` is tried before `datter`.
SUFFIXES = (
    "sdottir", "sdatter", "sdotter", "dottir", "datter", "dotter",
    "ssen", "sson", "sen", "son", "zen", "zoon", "sz", "szoon",
    "ovich", "evich", "ovitch", "evitch", "owicz", "ewicz",
    "ovna", "evna", "ovic", "evic",
)

#: `ben Yitzhaq`, `bint Aabed-El`, `ibn Rushd`. The particle is followed by the
#: father's own name rather than a derived form.
PARTICLES = {"ben", "bin", "ibn", "bint", "bat", "ap", "mac", "mc", "o"}

ABSENT = {".", "..", "?", "-", "_", "nn", "n.n.", "private", "<private>"}


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


def suffixed(token: str, father_stems: set[str]) -> str | None:
    low = fold(token)
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if not low.endswith(suffix):
            continue
        head = low[: -len(suffix)]
        if head in father_stems:
            return suffix
        # `Olsen` from `Ole`: the linking -s- belongs to the suffix in some
        # spellings and to the stem in others, so allow one trailing `s`.
        if head.endswith("s") and head[:-1] in father_stems:
            return suffix
    return None


def main() -> int:
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
                if not fid:
                    verdict, evidence = "no father recorded", ""
                elif not fname:
                    verdict, evidence = "father has no given name", ""
                else:
                    parts = token.split()
                    hit = suffixed(token, fstems)
                    if hit:
                        verdict, evidence = "patronymic", f"{fname} + -{hit}"
                    elif (len(parts) >= 2 and parts[0].casefold() in PARTICLES
                          and fold(parts[1]) in {fold(fname)} | fstems):
                        verdict, evidence = "patronymic", f"{parts[0]} {fname}"
                    else:
                        verdict, evidence = "not patronymic", ""
                tally[verdict] += 1
                by_token[token][verdict] += 1
                rows.append([gid, token, where, ordinal, fid, fname,
                             verdict, evidence])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "token", "field", "ordinal", "father_id",
                         "father_given", "verdict", "evidence"])
        writer.writerows(rows)
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")

    total = sum(tally.values())
    decided = tally["patronymic"] + tally["not patronymic"]

    # The tokens that go BOTH ways are the whole point: same string, different
    # usage, different Wikidata item.
    both = {t: c for t, c in by_token.items()
            if c["patronymic"] and c["not patronymic"]}

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
    for key in ("patronymic", "not patronymic", "no father recorded",
                "father has no given name"):
        add(f"| {key} | {tally[key]:,} | {100.0*tally[key]/max(total,1):.1f}% |")
    add(f"| **total** | **{total:,}** | |")
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
    add(f"**{len(both):,} distinct tokens are a patronymic for some bearers and not for")
    add("others.** Same string, different usage, and therefore **different Wikidata")
    add("items** — `CLAUDE.md` § *\"Jackson Jackson Jackson\"*. A suffix list alone would")
    add("have called every bearer of these a patronymic.")
    add("")
    add("| token | patronymic | not | ")
    add("| --- | ---: | ---: |")
    for token, counts in sorted(both.items(),
                                key=lambda kv: -(kv[1]["patronymic"]))[:25]:
        add(f"| {token} | {counts['patronymic']:,} | {counts['not patronymic']:,} |")
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
    for key in ("patronymic", "not patronymic", "no father recorded",
                "father has no given name"):
        print(f"  {key:<26} {tally[key]:>9,}")
    print(f"\n  {len(both):,} tokens go both ways")
    for token, counts in sorted(both.items(),
                                key=lambda kv: -(kv[1]["patronymic"]))[:10]:
        print(f"    {token:<22} patronymic {counts['patronymic']:>6,}   "
              f"not {counts['not patronymic']:>6,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
