"""Emit only what the model-vs-reality diff says is MISSING. Nothing else.

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

## What is refused, and why each refusal is load-bearing

* **`extra` is never touched.** The item holds something the model does not — almost always her
  hand-work. `CLAUDE.md`: *"the entire purpose of this is to add"*, and she edits continuously.
* **`CONFLICT` is never emitted.** Both sides hold the property with different values. Those are
  hers to adjudicate, and `CLAUDE.md` is explicit that contradiction resolution *"is worth doing
  but genuinely not that important"* next to adding.
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
    diff = R / "model-vs-reality.tsv"
    if not diff.exists():
        sys.exit("run scripts/model-vs-reality.py first")
    if ITEMS.exists():
        age = (time.time() - ITEMS.stat().st_mtime) / 3600
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

    rows = [r for r in csv.DictReader(open(diff, encoding="utf-8"), delimiter="\t")
            if r["verdict"] == "missing"]
    print(f"{len(rows)} missing statements in the diff")

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
            emitted.append((r["qid"], prop, render(prop, value), r["geni_id"], r["name"]))

    out = R / "wikidata-from-diff.qs"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("# A PROJECTION OF THE DIFF, and nothing else.\n"
                "#\n"
                "# Every line below exists because reports/model-vs-reality.tsv says the item\n"
                "# does not hold it. No statement is here because a rule produced it.\n"
                "#\n"
                "# NOT emitted: `extra` (the item holds it and the model does not -- her hand\n"
                "# work), `CONFLICT` (both hold it with different values -- hers to settle),\n"
                "# labels and aliases (they REPLACE, and hers are better).\n"
                "#\n"
                "# QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.\n")
        by_person = collections.OrderedDict()
        for qid, prop, value, geni, name in emitted:
            by_person.setdefault((qid, geni, name), []).append((prop, value))
        for (qid, geni, name), sts in by_person.items():
            f.write(f"\n# {name or qid}  {qid}  <- geni:{geni}\n")
            for prop, value in sts:
                f.write(f'{qid}\t{prop}\t{value}\tS2600\t"{geni}"\n')

    print(f"\n{len(emitted)} statements over {len({e[0] for e in emitted})} items "
          f"-> {out.relative_to(ROOT)}")
    for why, n in skipped.most_common():
        print(f"   {n:>3} skipped: {why}")
    by_prop = collections.Counter(e[1] for e in emitted)
    print("\nby property:")
    for p, n in by_prop.most_common():
        print(f"   {n:>3}  {p}")


if __name__ == "__main__":
    main()
