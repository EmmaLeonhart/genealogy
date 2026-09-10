"""Every item whose Wikidata label carries a generation suffix that Geni's `NSFX` does not.

`queue.md` § *`den yngre` NEEDS THE PROPER NAME-CHANGE TREATMENT* leaves one half unmeasured:
*"how many items carry `den yngre` and the rest of `GENERATION_SUFFIX`'s surface forms in a label
but no `NSFX` -- unmeasured, and it is a CSV of every instance."* This is that CSV.

**Why the gap exists.** `namemodel.generation_suffix_key` reads Geni's `NSFX` field and matches
the whole of it. `Q5797554` Detlof Heijkenskjöld den yngre is filed on Geni as
`NAME Detlof /Heijkenskjöld/` with **no `NSFX` at all**, so the suffix existed only inside
Wikidata's own label, our derived label came out bare, and the `ja`/`zh`/`ko` labels this pipeline
wrote onto the item dropped it in all three. `b22afdf1` added
`namemodel.generation_suffix_in_label`, which searches the same table inside a string, and
`derive-labels.py` falls back to it on `wikidata_en`/`wikidata_mul`. What was never counted is how
many people are in that position.

**The population is every one of the 23 surface forms**, not just `den yngre` — the queue names
`d.y.`, `the younger`, `nuorempi` and *"every senior form"* as the same question.

⛔ **`NSFX` COMES FROM THE CORPUS AND NOTHING ELSE.** There is no derived CSV carrying it, so the
GEDCOMs are read directly: a single pass over `exports/**/*.ged` tracking the current `INDI` xref
and recording every `NSFX` under it. Reading it off a label instead would be circular — the label
is the thing being tested.

⛔ **THIS MEASURES. It writes a CSV and changes nothing** — `CLAUDE.md` § *"Analyse this" means:
build a CSV of every instance*.
"""

from __future__ import annotations

import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from namemodel import GENERATION_SUFFIX  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "generation-suffix-gap.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"

INDI = re.compile(r"^0 @I(\d+)@ INDI")
NSFX = re.compile(r"^\d+ NSFX (.+)$")

#: A surface form counts only as a whole token run, so `dy` does not fire inside `Grundy` and
#: `sr` does not fire inside `Sr` inside a longer word. `\b` is wrong at both ends for the
#: dotted forms, so the boundary is spelled out.
FORMS = sorted(GENERATION_SUFFIX, key=len, reverse=True)
FORM_RE = re.compile(r"(?:(?<=\s)|^)(" + "|".join(re.escape(f) for f in FORMS) + r")(?=\s|$|,)",
                     re.IGNORECASE)


def nsfx_by_geni_id() -> dict:
    """`geni_id -> the NSFX values on that person`, straight out of the corpus."""
    found = {}
    files = sorted((ROOT / "exports").rglob("*.ged"))
    for n, path in enumerate(files):
        current = None
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = INDI.match(line)
                if m:
                    current = m.group(1)
                    continue
                if current is None:
                    continue
                m = NSFX.match(line)
                if m:
                    found.setdefault(current, set()).add(m.group(1).strip())
        if n % 500 == 0:
            print("  %d/%d files, %d people with NSFX" % (n, len(files), len(found)), flush=True)
    return found


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    print("reading NSFX out of the corpus ...", flush=True)
    nsfx = nsfx_by_geni_id()
    print("people carrying any NSFX: %d" % len(nsfx), flush=True)

    rows = []
    seen = 0
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for rec in csv.DictReader(fh):
            seen += 1
            gid = (rec.get("geni_id") or "").strip()
            hits = {}
            for field in ("wikidata_en", "wikidata_mul", "label_en", "label_mul"):
                val = (rec.get(field) or "").strip()
                m = FORM_RE.search(val)
                if m:
                    hits[field] = m.group(1)
            if not hits:
                continue
            have = nsfx.get(gid, set())
            # Does Geni's own NSFX carry a form? That is the case the existing rule handles.
            nsfx_has = any(FORM_RE.search(v) for v in have)
            rows.append({
                "geni_id": gid,
                "qid": (rec.get("qid") or "").strip(),
                "form": next(iter(hits.values())),
                "where": "|".join(sorted(hits)),
                "nsfx": "|".join(sorted(have)),
                "nsfx_carries_form": "yes" if nsfx_has else "no",
                "wikidata_en": (rec.get("wikidata_en") or "").strip(),
                "wikidata_mul": (rec.get("wikidata_mul") or "").strip(),
                "label_en": (rec.get("label_en") or "").strip(),
                "label_mul": (rec.get("label_mul") or "").strip(),
            })

    rows.sort(key=lambda r: (r["form"].lower(), r["geni_id"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                           ["geni_id", "qid", "form", "where", "nsfx", "nsfx_carries_form",
                            "wikidata_en", "wikidata_mul", "label_en", "label_mul"])
        w.writeheader()
        w.writerows(rows)

    gap = [r for r in rows if r["nsfx_carries_form"] == "no"]
    print()
    print("rows in derived-labels.csv           %7d" % seen)
    print("carrying a generation suffix anywhere%7d" % len(rows))
    print("  Geni's NSFX carries it too         %7d" % (len(rows) - len(gap)))
    print("  ⛔ NSFX does NOT carry it           %7d   <- the gap" % len(gap))
    by_form = {}
    for r in gap:
        by_form[r["form"].lower()] = by_form.get(r["form"].lower(), 0) + 1
    for form, n in sorted(by_form.items(), key=lambda kv: -kv[1]):
        print("     %-14s %5d" % (form, n))
    print("-> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
