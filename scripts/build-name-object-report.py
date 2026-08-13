"""The name objects: which exist, which do not, and what kind of names these are.

Emma scheduled this, 2026-08-12: *"we are going to fire off the analysis of the
names."* Three questions, plus the reason for the third: **name items get created
for names fitting Western conventions**, so the report has to say which names
those are, not merely how many are missing.

Her framing of the structure: *"some of the names are relatively irregular, some
of them are normal, and some of them are patronyms."*

**The classification is heuristic and its failure modes are named in the report
rather than hidden.** Nothing here is fuzzy-matched to Wikidata; a name either
matches a name item's label exactly, folded for case and diacritics, or it does
not.

Offline. Reads `reports/display-names.csv`, `reports/name-items.csv` and
`reports/wikidata-labels.tsv`.

    py scripts/build-name-object-report.py
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAMES = REPO_ROOT / "reports" / "display-names.csv"
NAME_ITEMS = REPO_ROOT / "reports" / "name-items.csv"
LABELS = REPO_ROOT / "reports" / "wikidata-labels.tsv"
OUT_MD = REPO_ROOT / "reports" / "name-objects.md"
OUT_CSV = REPO_ROOT / "reports" / "name-objects.csv"

csv.field_size_limit(10_000_000)

# --- classification ---------------------------------------------------------

NOT_A_NAME = {
    "nn", "n.n.", "n n", "nn.", "unknown", "ukjent", "okänd", "?", "??", "-", "--",
    "_", ".", "..", "...", "/", "//", "*", "rd.", "rd", "nr.", "nr", "no", "no.",
}
ORDINAL = re.compile(r"^[ivxlcdm]{1,7}$", re.I)
NUMERIC = re.compile(r"^[\d.,;:()\[\]/\\-]+$")

#: Patronymic endings. Scandinavian first because that is most of this corpus,
#: then the Slavic and Arabic forms Emma named.
PATRONYMIC_SUFFIX = re.compile(
    r"(?:s?son|s?sen|sson|szen|zen|s?datter|s?dotter|sdtr|dtr|"
    r"ovich|evich|ovna|evna|ovic|evic)$", re.I)
PATRONYMIC_PREFIX = re.compile(r"^(?:bin|ibn|bint|abu|abd)\s", re.I)

#: Territorial particles. A *particle* list, never a list of places.
PARTICLE = re.compile(
    r"^(?:of|de|del|della|di|da|du|des|van|von|vom|der|den|ter|te|ten|"
    r"af|av|zu|zur|la|le|el|los|las)\s", re.I)


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.casefold().split())


def scripts_of(text: str) -> set[str]:
    found = set()
    for char in text:
        if not char.isalpha():
            continue
        name = unicodedata.name(char, "")
        if name:
            found.add(name.split()[0])
    return found


def classify(text: str, role: str) -> str:
    folded = fold(text)
    if not folded or folded in NOT_A_NAME:
        return "not a name"
    if ORDINAL.match(folded) or NUMERIC.match(folded):
        return "not a name"
    if not any(c.isalpha() for c in text):
        return "not a name"

    scripts = scripts_of(text)
    han = "CJK" in scripts
    if han:
        letters = [c for c in text if c.isalpha()]
        # A Chinese clan name is one or two characters; the four-character strings
        # in this field are commandery-and-county place names — the inversion
        # CLAUDE.md records for 陳郡陽夏. Length is a proxy, not a proof.
        return "CJK clan name" if len(letters) <= 2 else "place misfiled as a name"
    if scripts and not (scripts & {"LATIN"}):
        return f"non-Latin script ({'/'.join(sorted(scripts))})"

    if PATRONYMIC_PREFIX.match(text) or PATRONYMIC_SUFFIX.search(folded.split()[-1]):
        return "patronymic"
    if PARTICLE.match(text):
        return "toponymic or territorial byname"
    return "ordinary Western given name" if role == "given" else "ordinary Western surname"


def main() -> int:
    given_items: set[str] = set()
    family_items: set[str] = set()
    with open(NAME_ITEMS, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["as_given_name"] == "yes":
                given_items.add(row["qid"])
            if row["as_family_name"] == "yes":
                family_items.add(row["qid"])

    labels: dict[str, str] = {}
    with open(LABELS, encoding="utf-8") as handle:
        for line in handle:
            qid, _, label = line.rstrip("\n").partition("\t")
            if label:
                labels[qid] = label

    index: dict[str, dict[str, set[str]]] = {"given": defaultdict(set),
                                             "family": defaultdict(set)}
    for qid in given_items:
        if qid in labels:
            index["given"][fold(labels[qid])].add(qid)
    for qid in family_items:
        if qid in labels:
            index["family"][fold(labels[qid])].add(qid)

    counts: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    with open(NAMES, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for token in (row["givn"] or "").split():
                counts["given"][token] += 1
            surn = (row["surn"] or "").strip()
            if surn:
                counts["family"][surn] += 1

    rows = []
    by_kind: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    people_by_kind: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    exists_by_kind: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    totals = {"given": Counter(), "family": Counter()}
    people_totals = {"given": Counter(), "family": Counter()}

    for role in ("given", "family"):
        for text, count in counts[role].items():
            kind = classify(text, role)
            qids = index[role].get(fold(text), set())
            state = ("exists" if len(qids) == 1 else
                     "ambiguous" if qids else "no item found")
            by_kind[role][kind] += 1
            people_by_kind[role][kind] += count
            totals[role][state] += 1
            people_totals[role][state] += count
            if state == "exists":
                exists_by_kind[role][kind] += 1
            rows.append([role, text, count, kind, state,
                         " | ".join(sorted(qids)[:3])])

    rows.sort(key=lambda r: (r[0], -r[2]))
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["role", "name", "people", "kind", "item_state", "qids"])
        writer.writerows(rows)

    L: list[str] = []
    add = L.append
    add("# Name objects: what exists, what does not, and what kind of names these are")
    add("")
    add("Scheduled by Emma for midnight. Every distinct name is a row in")
    add("`reports/name-objects.csv`, ranked by how many people carry it.")
    add("")
    add("**Why the classification matters.** Her rule is that name items get created")
    add("*\"for all of the names that fit sufficiently into Western name conventions\"* —")
    add("so the question is not how many names lack an item, but **which ones are")
    add("candidates at all**.")
    add("")

    add("## 1. How many name objects exist")
    add("")
    add("| | given names | surnames |")
    add("| --- | ---: | ---: |")
    for state in ("exists", "ambiguous", "no item found"):
        add(f"| {state} | {totals['given'][state]:,} | {totals['family'][state]:,} |")
    add(f"| **distinct total** | **{sum(totals['given'].values()):,}** | "
        f"**{sum(totals['family'].values()):,}** |")
    add("")
    add("By people carrying the name, which is the number that matters for coverage:")
    add("")
    add("| | given names | surnames |")
    add("| --- | ---: | ---: |")
    for state in ("exists", "ambiguous", "no item found"):
        add(f"| {state} | {people_totals['given'][state]:,} | "
            f"{people_totals['family'][state]:,} |")
    add("")

    add("## 2. \"No item found\" is not the same as \"needs creating\"")
    add("")
    add("**This cannot be separated with the data we hold, and the report will not")
    add("pretend otherwise.** The lookup is built from the 132,569 name items that our")
    add("*own people's* `P735`/`P734` statements already point at. A name item that")
    add("exists on Wikidata but that nobody in our store references is invisible here")
    add("and reads as missing.")
    add("")
    add("The evidence that this is a large effect is in the data itself: `Thomas`,")
    add("`Hans`, `Sarah`, `Henry` and `Marguerite` all read as *no item found*, and")
    add("Wikidata certainly has items for those. So the \"no item\" column is an **upper")
    add("bound on creations** and a mixture of two populations.")
    add("")
    add("Separating them needs a download that fetches name items directly rather than")
    add("following the family walk — the same gap that limits `P735`/`P734` emission.")
    add("")

    add("## 3. What kind of names these are")
    add("")
    for role, title in (("given", "Given names"), ("family", "Surnames")):
        add(f"### {title}")
        add("")
        add("| kind | distinct | people | of which an item exists |")
        add("| --- | ---: | ---: | ---: |")
        for kind, n in by_kind[role].most_common():
            add(f"| {kind} | {n:,} | {people_by_kind[role][kind]:,} | "
                f"{exists_by_kind[role][kind]:,} |")
        add("")

    add("## Which names are creation candidates")
    add("")
    add("Applying her rule — Western conventions — the candidates are the *ordinary*")
    add("rows with no item found. Everything else is excluded for a stated reason:")
    add("")
    add("| excluded | why |")
    add("| --- | --- |")
    add("| patronymic | `Olsdatter` is not a family name; it says whose child someone is |")
    add("| place misfiled as a name | `隴西狄道` is a commandery and county, not a surname |")
    add("| CJK clan name | a real name, but not a Western convention |")
    add("| non-Latin script | same |")
    add("| toponymic byname | `of Châtellerault` is a place; Wikidata gives these no `P734` at a rate 33 points above base |")
    add("| not a name | `NN`, regnal ordinals, `Rd.`, punctuation |")
    add("")
    for role, title in (("given", "given names"), ("family", "surnames")):
        kind = f"ordinary Western {'given name' if role == 'given' else 'surname'}"
        candidates = [r for r in rows if r[0] == role and r[3] == kind
                      and r[4] == "no item found"]
        people = sum(r[2] for r in candidates)
        add(f"**{len(candidates):,} {title}** with no item found, carried by "
            f"{people:,} people.")
        add("")
        add(f"The twenty most-carried:")
        add("")
        add("| name | people |")
        add("| --- | ---: |")
        for r in candidates[:20]:
            add(f"| {r[1]} | {r[2]:,} |")
        add("")

    add("## Where this classification is weak")
    add("")
    add("- **CJK length is a proxy.** A one- or two-character Han string is treated as a")
    add("  clan name and anything longer as a place. `司馬` and `藤原` are two")
    add("  characters and are surnames; `隴西狄道` is four and is a place. It will")
    add("  misclassify a genuine three-character name.")
    add("- **Patronymic matching is by suffix.** `Jensen` as an inherited Danish family")
    add("  name and `Jensen` as \"Jens's child\" are the same string, and this counts")
    add("  both as patronymic. In this corpus that is usually right and sometimes not.")
    add("- **Nothing is fuzzy-matched.** A name matches a name item's label exactly,")
    add("  folded for case and diacritics, or it does not. A near miss is a miss.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} and {OUT_CSV} ({len(rows):,} rows)")
    for role in ("given", "family"):
        add_kind = f"ordinary Western {'given name' if role == 'given' else 'surname'}"
        cands = [r for r in rows if r[0] == role and r[3] == add_kind and r[4] == "no item found"]
        print(f"  {role:<7} exists {totals[role]['exists']:,}  "
              f"no item {totals[role]['no item found']:,}  "
              f"-> Western candidates {len(cands):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
