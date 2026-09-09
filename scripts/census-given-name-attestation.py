"""Is a token EVER somebody's FIRST given name? -> `reports/given-name-attestation.tsv`.

**`Q141352791` was created by our own batch as an item labelled `Garborg`, `P31` *given
name*, for two people.** `Garborg` is not a given name.

Geni files both bearers with `GIVN` = `Arne Garborg` / `Siri Garborg` and an **empty** `SURN`, so
the name model reads the second token positionally as a middle name -- § *PARSE PATRONYMICS BY
FORM. Do not parse a name positionally*, in a new place. Neither bearer has a Garborg parent
(Tunheim and Talle), so they are children named after the writer, and `Garborg` is his surname:
our own plan already holds it as `family`, 39 bearers, `Q30250555`.

**⛔ THIS IS NOT THE DOMINANCE RATIO SHE DELETED, and the difference is the whole point.** Her
ruling of 2026-08-15 is that a token used in two roles gets two items: *"If something is a
surname and a given name, then it gets a surname and a given name object."* That forbids
ADJUDICATING between two real usages. This asks a different question -- **is there a given-name
usage at all?** -- and answers it categorically: zero occurrences as a first given name, against
at least one as a family name. No threshold, nothing weighed.

Two rules that WERE tried and are refuted, recorded so they are not tried again:

* **"the token is a family name elsewhere"** -- 242,831 people, headed by `Maria`, `Marie`,
  `Elisabeth`, `Johan`, `Gustaf`. Being a surname somewhere says nothing.
* **"SURN empty and `_MARNM` present, so the last `GIVN` token is the birth surname"** --
  168,309 people, and the last token is `Johan` 2,773, `Fredrik` 2,427, `Maria` 2,419,
  `Waldemar`, `Verónica`, `Hazel`. It would have rewritten every one of them.

Measured over the corpus: `Garborg` is a first given name **0** times and a family name **285**;
`Maria` 31,129 / 50, `Johan` 25,273 / 14, `Waldemar` 101 / 0, `Elisabeth` 6,564 / 6. The test
separates them without looking at a ratio.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from namemodel import classify_fields  # noqa: E402

SOURCE = ROOT / "reports" / "display-names.csv"
OUT = ROOT / "reports" / "given-name-attestation.tsv"


def main() -> int:
    if not SOURCE.exists():
        print(f"{SOURCE} is missing -- run scripts/pack-derived.py --unpack", file=sys.stderr)
        return 1
    csv.field_size_limit(10 ** 8)
    first, later, family = (collections.Counter() for _ in range(3))
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for field in ("surn", "marnm"):
                for token in (row[field] or "").split():
                    family[token] += 1
            given = [t for t, usage, _o in classify_fields(row["givn"] or "", "")
                     if usage == "given"]
            if given:
                first[given[0]] += 1
                for token in given[1:]:
                    later[token] += 1

    tokens = set(first) | set(later) | set(family)
    rows = [(t, first.get(t, 0), later.get(t, 0), family.get(t, 0)) for t in tokens]
    # **A TOTAL sort key.** `casefold` alone is not one -- § *SORTING MUST BE DETERMINISTIC*.
    rows.sort(key=lambda r: (r[0].casefold(), r[0]))
    tmp = OUT.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["token", "first_given", "later_given", "family"])
        writer.writerows(rows)
    tmp.replace(OUT)

    never = sum(1 for t, f, l, fam in rows if f == 0 and l and fam)
    print(f"{len(rows):,} tokens -> {OUT}")
    print(f"{never:,} appear in a non-first given slot, are NEVER a first given name, "
          f"and are attested as a family name")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
