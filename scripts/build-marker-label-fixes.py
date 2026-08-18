"""Turn the marker-label census into label edits, by Emma's rules.

**Emma, 2026-08-17:** *"finds these kinds of ones where the label has this stuff already
in it, and normalizes them into proper things based on our rules."* The census found
them; this normalises them.

Reads `reports/marker-labels.csv` and writes `reports/wikidata-marker-label-fixes.json`.
Offline, emits nothing to Wikidata.

### Four rules, and which class a row falls into is the whole design

The census records `kind` and `position` precisely so this can tell them apart. Getting
the class wrong does not produce a broken edit — it produces a *plausible* one that says
the wrong thing about a person.

* **`marker` at `whole`** — there is no name here. `mul: NN`, and a description in the
  local languages if a relative supplies one. `NN`, `Private`, `Без име`, `?`.

* **`marker` at `head`** — a marker leading a real surname, so the surname survives into
  the marker label. `unknown Bloomfield` → `mul: NN Bloomfield`. `CLAUDE.md` is explicit
  that discarding these loses 3,605 surnames.

* **`marker` at `tail` or `inside`** — **the person HAS a name** and the marker is
  wedged into it. `Catherine unknown` → `Catherine`; `Hadaburg N.N. Gräfin im Saalgau` →
  `Hadaburg Gräfin im Saalgau`. These get the corrected name in `mul` and `en` and
  **no `NN` at all** — they are not unnamed people, they are named people with a
  typo-shaped hole. Reading them as unnamed would erase a given name that is right there.

* **`description`** — the label describes somebody by their relationship instead of
  naming them. `mul: NN` plus the real surname where the remainder is one, and the
  description itself kept as the local-language label, which is where it always
  belonged. Emma: *"And NN for mul there."* Covers the English phrases, the CJK suffixes
  and the honorific forms alike.

### Where the remainder is a surname and where it is somebody else

A `head` marker leaves the person's **own** surname. A `description` remainder is
whatever the census could salvage, and that differs by form:

* `氏` — her own clan, so `盧氏 Chan` → `mul: NN 盧 Chan`.
* `娘` / `妻` / `母` / `正室` — the **relative**, so the remainder must not go into her
  `mul`. `織田敏信娘` leaves `織田敏信`, which is her father, and the marker label stays
  bare `NN`.
* `wife of` / `Mrs.` — likewise the relative.

`CLAN_SUFFIX` and `RELATIVE_FORMS` below carry that split, and a form this script does
not recognise contributes nothing to `mul` rather than being guessed at.

    PYTHONPATH=src python scripts/build-marker-label-fixes.py
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import labels as _labels  # noqa: E402  — the single marker vocabulary

CENSUS = REPO / "reports" / "marker-labels.csv"
OUT = REPO / "reports" / "wikidata-marker-label-fixes.json"

csv.field_size_limit(10 ** 7)

#: `NN` — *nomen nescio*, and the marker `mul` carries for anybody with no usable name.
UNNAMED_MARKER = "NN"

#: Description forms whose remainder is the **relative**, not the subject. The
#: remainder is still recorded on the edit, because it is what a local-language
#: description gets built from — it just must never reach `mul`.
RELATIVE_FORMS = {"娘", "妻", "母", "正室", "側室", "室", "某",
                  "mrs.", "mrs", "miss", "frau", "fru", "madame", "señora", "sra.",
                  "hustru", "wife", "daughter", "widow"}


def _census_module():
    spec = importlib.util.spec_from_file_location(
        "marker_label_census", REPO / "scripts" / "build-marker-label-census.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_a_plausible_name(text: str) -> bool:
    """Whether a repaired remainder can be somebody's label.

    **Taking a marker out of the middle of a label can leave wreckage**, and the
    output looks like a name until you read it:

        Daughter (name unknown) Biard   ->  "Daughter (name Biard"   unbalanced
        (Female) Unknown                ->  "(Female)"               not a name

    Both are objective faults rather than matters of taste — brackets either balance
    or they do not, and a string with no unbracketed word in it names nobody — so
    this rejects them and the caller falls back to `NN`. A repair that cannot be
    trusted is worse than no repair: it ships a label nobody would think to check.

    **A repair that yields another marker is not a repair.** `?? Unknown` had its
    word marker taken out and shipped `??` as both `mul` and `en` on four items —
    a Wikidata label made entirely of question marks. The brackets balanced and
    there was a bare token, so both tests above passed it. `labels.is_placeholder_form`
    is the check that catches it, and deferring to that module rather than adding a
    local test is the *one set, replacing three* rule in `scripts/labels.py`.

    Rejecting here is the right outcome rather than a loss: the caller falls back to
    the unnamed treatment, so the person still gets `NN` in `mul` and stays
    findable. What is prevented is only the false label.
    """
    if text.count("(") != text.count(")"):
        return False
    if text.count("[") != text.count("]"):
        return False
    if _labels.is_placeholder_form(text):
        return False
    bare = [t for t in text.split()
            if not (t.startswith("(") or t.endswith(")")
                    or t.startswith("[") or t.endswith("]"))]
    return bool(bare)


def drop_bracket_debris(text: str) -> str:
    """Remove bracket characters that have no partner.

    Two causes, and both leave the same wreckage. **The source label was already
    broken** — `NN Guttormsdatter Ålesdatter?)` carries a stray `)` in Geni, and
    `NN Wife of Quintus Pedius Publicola)` in Wikidata — or **taking the marker out
    broke it**: `(Unknown Given Name) Unknown` loses `(unknown` and leaves
    `Given Name)`.

    Dropping an unpartnered bracket is not a guess: `Guttormsdatter Ålesdatter` is
    the surname either way, and the character was noise before this script touched
    it. What is *inside* balanced brackets is left alone.
    """
    out, depth = [], 0
    for ch in text:
        if ch in "([":
            depth += 1
            out.append(ch)
        elif ch in ")]":
            if depth == 0:
                continue          # no opener — debris
            depth -= 1
            out.append(ch)
        else:
            out.append(ch)
    if depth:                     # unclosed openers, dropped right to left
        kept, remaining = [], depth
        for ch in reversed(out):
            if ch in "([" and remaining:
                remaining -= 1
                continue
            kept.append(ch)
        out = list(reversed(kept))
    return " ".join("".join(out).split())


def usable_remainder(text: str) -> str:
    """A remainder fit to sit in a label, or `''` when nothing survives.

    Applied to **every** rule that puts a remainder into `mul`, not only the repair
    branch. The first version guarded the repair alone, and 28 labels still shipped
    with unbalanced brackets through `marker+surname` and `description+clan` — which
    is the same defect arriving by a different door.
    """
    cleaned = drop_bracket_debris(text)
    return cleaned if is_a_plausible_name(cleaned) else ""


def classify_row(row: dict, clan_suffixes: tuple[str, ...]) -> dict | None:
    """The labels one census row implies, or `None` when it implies none."""
    kind, position = row["kind"], row["position"]
    remainder = (row["remainder"] or "").strip()
    marker = row["marker"]

    if kind == "marker" and position == "whole":
        return {"rule": "unnamed", "mul": UNNAMED_MARKER, "name": ""}

    if kind == "marker" and position == "head":
        # The remainder is the subject's own surname.
        surname = usable_remainder(remainder)
        if not surname:
            return {"rule": "unnamed", "mul": UNNAMED_MARKER, "name": ""}
        return {"rule": "marker+surname",
                "mul": f"{UNNAMED_MARKER} {surname}", "name": ""}

    if kind == "marker":
        # tail or inside: a real name with a marker wedged into it.
        if not remainder:
            return None
        # **The repair branch checks BEFORE cleaning, and the other branches after.**
        # That asymmetry is the point rather than an oversight. A remainder that is
        # the person's *surname* is worth rescuing from stray punctuation —
        # `Guttormsdatter Ålesdatter?)` is a real surname pair either way. A
        # remainder that is supposed to be a whole *name* and arrives with debris in
        # it is evidence the parse went wrong, not a name with a typo: cleaning
        # `Daughter (name unknown) Biard` yields `Daughter name Biard`, which is a
        # description wearing a name's clothes. So this one refuses instead.
        repaired = remainder if is_a_plausible_name(remainder) else ""
        if not repaired:
            # The repair produced something that is not a name. Fall back to the
            # unnamed treatment rather than emit it, and keep the rule name
            # distinct so the population stays countable instead of merging
            # silently into the 21,054 genuinely-unnamed.
            return {"rule": "repair rejected", "mul": UNNAMED_MARKER, "name": ""}
        return {"rule": "name repaired", "mul": repaired, "name": repaired}

    if kind == "description":
        if marker in RELATIVE_FORMS or not remainder:
            return {"rule": "description", "mul": UNNAMED_MARKER, "name": ""}
        if marker in clan_suffixes:
            clan = usable_remainder(remainder)
            if not clan:
                return {"rule": "description", "mul": UNNAMED_MARKER, "name": ""}
            return {"rule": "description+clan",
                    "mul": f"{UNNAMED_MARKER} {clan}", "name": ""}
        # A description form this script does not know: keep the marker label bare
        # rather than guessing whose name the remainder is.
        return {"rule": "description", "mul": UNNAMED_MARKER, "name": ""}

    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", choices=("geni", "wikidata", "both"), default="both")
    args = ap.parse_args()

    if not CENSUS.exists():
        print(f"no {CENSUS}; run scripts/build-marker-label-census.py first",
              file=sys.stderr)
        return 1

    clan_suffixes = _census_module().CLAN_SUFFIX

    # One decision per subject, not per row: `label_en` and `label_mul` hold the same
    # string for most Geni people, and a Wikidata item repeats its label across
    # languages. Keyed on the subject, and the strongest rule wins so a person whose
    # name is repairable is never also reported as unnamed.
    STRENGTH = {"name repaired": 3, "marker+surname": 2, "description+clan": 2,
                "description": 1, "repair rejected": 1, "unnamed": 1}
    best: dict[tuple[str, str], dict] = {}
    seen_labels: dict[tuple[str, str], set[str]] = {}

    with CENSUS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if args.store != "both" and row["store"] != args.store:
                continue
            decided = classify_row(row, clan_suffixes)
            if not decided:
                continue
            key = (row["store"], row["qid"] or row["geni_id"])
            seen_labels.setdefault(key, set()).add(row["label"])
            current = best.get(key)
            if current is None or STRENGTH[decided["rule"]] > STRENGTH[current["rule"]]:
                decided = dict(decided)
                decided["row"] = row
                best[key] = decided

    edits, tally = [], Counter()
    for (store, subject), decided in sorted(best.items()):
        row = decided["row"]
        labels = {"mul": decided["mul"]}
        if decided["name"]:
            labels["en"] = decided["name"]
        tally[(store, decided["rule"])] += 1
        edits.append({
            "id": f"marker_label:{store}:{subject}",
            "type": "set_labels",
            "source": "marker-label census",
            "subject": {"qid": row["qid"] or None, "geni_id": row["geni_id"] or None},
            "requires": [],
            "labels": labels,
            "rule": decided["rule"],
            "replaces": sorted(seen_labels[(store, subject)]),
            "marker": row["marker"],
            "marker_kind": row["kind"],
            "marker_vocabulary": row["vocabulary"],
            # What a local-language description would be built from. Empty for a
            # repaired name, which needs no description.
            "describes_via": "" if decided["name"] else (row["remainder"] or ""),
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} ({len(edits):,} set_labels edits)\n")
    for (store, rule), count in tally.most_common():
        print(f"  {count:>7,}  {store:<9} {rule}")
    repaired = sum(1 for e in edits if e["rule"] == "name repaired")
    print(f"\n  {repaired:,} are a real name with the marker taken out — no NN at all")
    print(f"  {sum(1 for e in edits if e['labels']['mul'] != UNNAMED_MARKER):,} "
          "keep a real surname beside the marker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
