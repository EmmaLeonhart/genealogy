"""Emit what the model-vs-reality diff says the item does not already state.

    python scripts/build-from-diff.py

**Emma, 2026-08-24:** *"we are supposed to generate complete models of what the wikidata items
should be and compare with the reality for the quickstatements modelling stuff."* The half of that
instruction this script carries is her phrase *the batch becomes a projection of the diff* — a
statement is emitted because `reports/model-vs-reality.tsv` says it is absent, and for no other
reason.

**Why that ordering matters.** The method it replaces built a batch from the rules directly and
found out what was wrong when she ran it: four corrective rounds in one afternoon. A projection
cannot emit a statement the item already holds, because such a statement is not in the `missing`
column by construction.

## What is emitted and what is refused

* **`extra` is never touched.** The item holds something the model does not — almost always her
  hand-work. `CLAUDE.md`: *"the entire purpose of this is to add"*, and she edits continuously.
* **`CONFLICT` is emitted as an ADDITIONAL statement, cited `S2600` to the Geni profile.** Both
  sides hold the property with different values; the existing statement is left exactly as it is
  and ours goes in beside it, so the item records both readings. That is `CLAUDE.md` § *The
  purpose is to ADD to Wikidata, not to correct it* -- *"prefer adding a second statement cited
  to Geni over editing the existing one"* -- applied generically rather than per property.

  **It used to route these to Emma and that does not scale.** Her words, 2026-08-26, on the four
  Garborg date conflicts and the three Izumo `P22` ones being put to her as decisions: *"those
  seemed like simple data issues that by design were supposed to get pushed onto wikidata"*, and
  *"we are doing over a million people here."* Twelve conflicts is a rounding error against the
  corpus; a pipeline that stops on each one never finishes.
* **Labels and aliases are not projected at all.** `Len`/`Lmul` *replace*. `Q467497` is labelled
  *Arne Garborg* on Wikidata against our derived *Aadne (Arne) Eivindson Garborg*, and emitting
  ours would overwrite a better label with a Geni display string.
* **`P2600` is skipped where another batch already carries it.** All eight missing `P2600` rows
  are the spine people in `reports/wikidata-spine-add-p2600.qs` — the diff rediscovered that set
  independently, which is a real cross-check and also a way to emit each of them twice.
* **`P3373` *sibling* obeys the ten-a-day cap** from `CLAUDE.md`, counted here even though the
  current diff has none, so the cap cannot be lost by a later diff that does.

## Freshness

The diff is only as current as `out/model-vs-reality-items.json`. Its age is printed and refused
beyond a day, because `CLAUDE.md` § *Emma edits the tree and the items BY HAND, continuously*
means a stale diff proposes re-adding what she has already done.

Writes `reports/wikidata-from-diff.qs`. Queued, never run — editing starts 2026-09-01.
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"
ITEMS = ROOT / "out" / "model-vs-reality-items.json"

#: `CLAUDE.md` § *`P3373` sibling is capped at 10 a day*.
SIBLING_CAP = 10
#: Refuse a diff older than this. She edits by hand between runs.
MAX_AGE_HOURS = 24
#: Never projected: these replace rather than add.
NEVER = {"label", "alias", "description"}


#: Properties whose value is monolingual TEXT, which QuickStatements writes as `en:"..."`.
#: `CLAUDE.md` lists these; `P1449` *nickname* is the one this diff produces.
MONOLINGUAL = {"P1449", "P1477", "P1559", "P6375"}


def render(prop, value):
    """The diff's comparison form -> what QuickStatements actually accepts.

    Two defects this fixes, both of which would have failed on paste rather than quietly:

    * **A time needs the full timestamp.** The diff stores `+1157-00-00/9` because that is what
      compares cleanly against Wikidata's precision field; QuickStatements wants
      `+1157-00-00T00:00:00Z/9`. Dropping `T00:00:00Z` is not a rounding issue, it is invalid.
    * **Monolingual text needs a language tag and quotes.** `P1449` *nickname* emitted as a bare
      `Cecilia` is rejected; it has to read `en:"Cecilia"`.

    The comparison form and the emission form are genuinely different, and conflating them is
    how a diff-projected batch stops being runnable.
    """
    if prop in MONOLINGUAL:
        return 'en:"' + value.replace('"', "") + '"'
    if prop == "P2600":
        return f'"{value}"'
    if "/" in value and value[0] in "+-":
        stamp, _, precision = value.rpartition("/")
        return f"{stamp}T00:00:00Z/{precision}"
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", default=str(R / "model-vs-reality.tsv"), metavar="TSV")
    ap.add_argument("--items", default=str(ITEMS), metavar="JSON",
                    help="the snapshot the diff rests on, whose age is checked here.")
    ap.add_argument("--out", default=str(R / "wikidata-from-diff.qs"), metavar="QS")
    ap.add_argument("--conflicts-only", action="store_true",
                    help="emit the CONFLICT rows and not the `missing` ones. The Izumo diff's "
                         "missing column is 351 statements -- a mass batch nobody asked for.")
    args = ap.parse_args()

    diff, items_path = Path(args.diff), Path(args.items)
    if not diff.exists():
        sys.exit(f"{diff} not found -- run scripts/model-vs-reality.py first")
    if items_path.exists():
        age = (time.time() - items_path.stat().st_mtime) / 3600
        print(f"the diff rests on a snapshot {age:.1f} hours old")
        if age > MAX_AGE_HOURS:
            sys.exit(f"refusing to project from a diff older than {MAX_AGE_HOURS}h -- "
                     f"re-run scripts/model-vs-reality.py --refetch. Emma edits by hand "
                     f"continuously and a stale diff proposes re-adding her own work.")

    already = set()
    spine = R / "wikidata-spine-add-p2600.qs"
    if spine.exists():
        already = set(re.findall(r"(Q\d+)\tP2600", spine.read_text(encoding="utf-8")))
        print(f"{len(already)} items already have their P2600 in {spine.name}; skipped here")

    wanted = {"CONFLICT"} if args.conflicts_only else {"missing", "CONFLICT"}
    rows = [r for r in csv.DictReader(open(diff, encoding="utf-8"), delimiter="\t")
            if r["verdict"] in wanted]
    n_conf = sum(1 for r in rows if r["verdict"] == "CONFLICT")
    print(f"{len(rows)} statements to project: {len(rows) - n_conf} missing, "
          f"{n_conf} conflicting (emitted BESIDE what is there, never replacing it)")

    emitted, skipped, siblings = [], collections.Counter(), 0
    for r in rows:
        prop = r["property"]
        if not prop.startswith("P"):
            skipped[f"{prop or '(none)'} is not a statement"] += 1
            continue
        if prop == "P2600" and r["qid"] in already:
            skipped["P2600 already in the spine batch"] += 1
            continue
        if prop == "P3373":
            if siblings >= SIBLING_CAP:
                skipped[f"P3373 over the {SIBLING_CAP}-a-day cap"] += 1
                continue
            siblings += 1
        for value in [v for v in r["model"].split(";") if v]:
            emitted.append((r["qid"], prop, render(prop, value), r["geni_id"], r["name"],
                            r["verdict"]))

    out = Path(args.out)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# A PROJECTION OF {diff.name}, and nothing else.\n"
                "#\n"
                f"# Every line below exists because {diff.name} says the item\n"
                "# does not hold it. No statement is here because a rule produced it.\n"
                "#\n"
                "# NOT emitted: `extra` (the item holds it and the model does not -- her hand\n"
                "# work), labels and aliases (they REPLACE, and hers are better).\n"
                "#\n"
                "# A CONFLICT IS emitted, as a SECOND statement BESIDE the existing one and never\n"
                "# in place of it. The item ends up recording both readings, ours cited to Geni.\n"
                "#\n"
                "# QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.\n")
        by_person = collections.OrderedDict()
        for qid, prop, value, geni, name, verdict in emitted:
            by_person.setdefault((qid, geni, name), []).append((prop, value, verdict))
        for (qid, geni, name), sts in by_person.items():
            f.write(f"\n# {name or qid}  {qid}  <- geni:{geni}\n")
            for prop, value, verdict in sts:
                if verdict == "CONFLICT":
                    f.write(f"# {prop} disagrees with what the item already states, which STAYS. "
                            f"This goes in beside it.\n")
                f.write(f'{qid}\t{prop}\t{value}\tS2600\t"{geni}"\n')

    print(f"\n{len(emitted)} statements over {len({e[0] for e in emitted})} items "
          f"-> {out.resolve().relative_to(ROOT)}")
    for why, n in skipped.most_common():
        print(f"   {n:>3} skipped: {why}")
    by_prop = collections.Counter(e[1] for e in emitted)
    print("\nby property:")
    for p, n in by_prop.most_common():
        print(f"   {n:>3}  {p}")


if __name__ == "__main__":
    main()
