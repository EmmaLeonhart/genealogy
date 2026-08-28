"""Where an unknown-name marker sits in only ONE field of a name, and what shape it takes.

    python scripts/census-partial-nn.py

**Emma, 2026-08-27**, on `Q141198538`: *"clearly has 'nn' as its first name however it was not
produced as an NN person"*. The worked case is `Sara /NN/` — `GIVN Sara`, surname field the
literal marker `NN` — where the fields concatenate to `Sara NN` and that went to Wikidata as her
label. `nn Gunnarsdatter /Frafjord/` is the mirror image: the marker sits in `GIVN`, in front of
a real patronymic.

**These are PARTIAL markers and they are a different population from the fully-unnamed.** A
person recorded as `NN` alone has no name at all and takes the treatment in `CLAUDE.md`
§ *`NN` is PRESERVED in `mul`* — marker in `mul`, formulaic descriptive labels elsewhere. A
person recorded as `Sara /NN/` **has half a name**, and nothing had ever decided what that
should look like.

Counted over `reports/display-names.csv`, one row per `NAME` record. The shapes are reported
separately because they are not obviously the same question:

* **marker in GIVN only** — surname known, given name not. `nn Gunnarsdatter /Frafjord/`.
* **marker in SURN/_MARNM only** — given name known, surname not. `Sara /NN/`.
* **nothing survives** — both fields marked, or one marked and the other empty. These are the
  fully-unnamed and the existing NN treatment already covers them; they are counted only to keep
  the partial figures honest.

The vocabulary is `scripts/labels`' — `NARROW_MARKERS` and `WORDS_MEANING_UNKNOWN` — so a marker
added there is counted here with no second list to keep in step.

Writes `reports/partial-nn.csv`, one row per affected name record.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
NAMES = ROOT / "reports" / "display-names.csv"
OUT = ROOT / "reports" / "partial-nn.csv"


def main() -> None:
    from labels import NARROW_MARKERS, WORDS_MEANING_UNKNOWN

    markers = NARROW_MARKERS | WORDS_MEANING_UNKNOWN

    def marked(field: str) -> bool:
        """True when ANY token of the field is a marker — `nn Gunnarsdatter` counts."""
        return any(tok.casefold().strip(".,") in markers for tok in (field or "").split())

    rows, shapes, total = [], collections.Counter(), 0
    with open(NAMES, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            total += 1
            givn, surn, marnm = r.get("givn") or "", r.get("surn") or "", r.get("marnm") or ""
            family = surn or marnm
            g, f = marked(givn), marked(family)
            if not (g or f):
                continue
            # **An EMPTY field is not a known name.** The first run called `NN` with no surname
            # at all "marker in GIVN, family name known", because `marked("")` is False — the
            # absent-versus-empty trap this repo keeps paying for. A field must be non-empty
            # AND unmarked to count as known.
            givn_known = bool(givn.strip()) and not g
            family_known = bool(family.strip()) and not f
            shape = ("nothing survives — no usable name in either field"
                     if not givn_known and not family_known else
                     "marker in GIVN, family name known" if family_known else
                     "marker in the family name, given name known")
            shapes[shape] += 1
            rows.append({
                "geni_id": r["geni_id"], "shape": shape,
                "name_raw": r.get("name_raw", ""), "display_name": r.get("display_name", ""),
                "givn": givn, "surn": surn, "marnm": marnm,
                "qid": r.get("qid", ""), "wikidata_mul": r.get("wikidata_mul", ""),
            })

    if not rows:
        sys.exit("no name record carries a marker at all — that is a broken read of "
                 f"{NAMES.name}, not a corpus without NN people")

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"{total:,} name records; {len(rows):,} carry a marker\n")
    for shape, n in shapes.most_common():
        print(f"  {n:>7,}  {shape}")

    partial = [r for r in rows if not r["shape"].startswith("nothing survives")]
    print(f"\n{len(partial):,} are PARTIAL — half a name is recorded")
    on_wd = [r for r in partial if (r.get("qid") or "").startswith("Q")]
    print(f"{len(on_wd):,} of those already have a Wikidata item")

    for shape in ("marker in the family name, given name known",
                  "marker in GIVN, family name known"):
        sample = [r for r in rows if r["shape"] == shape][:6]
        print(f"\n{shape}:")
        for r in sample:
            print(f"    {r['geni_id']:<21} {r['name_raw'][:44]:<45} -> {r['display_name'][:28]}")

    print(f"\nwrote {OUT.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
