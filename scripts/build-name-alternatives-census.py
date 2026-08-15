"""For every profile carrying a placeholder name: does it ALSO have a real one?

**This is the question that decides whether normalising is safe.** Emma,
2026-08-14: *"I want to know if any of these have additional names that are not
in the unknown thing or whatever, because a lot of these individuals, we are
normalizing them but they're expected to be like this."*

A Geni profile carries several `NAME` records and they disagree. If a profile's
only names are placeholders, collapsing them to `NN` loses nothing. If a profile
has `Private` on one record and a real name on another, collapsing it **destroys
a real name**, and the count of those is the thing to know before touching
anything.

**Placeholder forms are discovered, not listed.** An earlier census used a fixed
set of forms written from memory and would have missed anything not thought of —
`(No name)` among them. Here every distinct given-name string in the corpus is
counted, and the ones that look like placeholders are reported by frequency so
the list comes from the data.

Writes:
  `reports/name-alternatives.csv` one row per profile that has any placeholder
      name: how many names it has, how many are real, and what they are
  `reports/given-name-forms.csv`  every distinct given-name string with a count,
      so the placeholder vocabulary can be read off rather than guessed

    py scripts/build-name-alternatives-census.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

INDI = re.compile(r"^0 @I(\d+)@ INDI")

#: Only used to *report* which discovered forms look like placeholders. Nothing
#: is filtered by it — every distinct given name is counted either way.
LOOKS_PLACEHOLDER = re.compile(
    r"^\s*[\(\[<]?\s*(private|no\s*name|noname|unknown|unk|nn|n\.?\s*n\.?|"
    r"anonymous|anon|\?+|\.+|-+|_+|na|n/a)\s*[\)\]>]?\s*$",
    re.IGNORECASE,
)


def given_and_surname(raw: str) -> tuple[str, str]:
    parts = raw.split("/")
    return (" ".join(parts[0].split()),
            " ".join(parts[1].split()) if len(parts) > 2 else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/name-alternatives.csv")
    ap.add_argument("--forms-out", default="reports/given-name-forms.csv")
    args = ap.parse_args()

    names: dict[str, set[str]] = defaultdict(set)
    paths = sources.find_exports()
    for n, path in enumerate(paths, 1):
        cur = None
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            for raw in fh:
                m = INDI.match(raw)
                if m:
                    cur = m.group(1)
                    continue
                if raw.startswith("0 "):
                    cur = None
                elif cur and raw.startswith("1 NAME "):
                    names[cur].add(raw[7:].strip())
        if n % 25 == 0:
            print(f"  read {n}/{len(paths)} exports, {len(names):,} profiles")

    givens = Counter()
    for nameset in names.values():
        for nm in nameset:
            givens[given_and_surname(nm)[0]] += 1

    forms = REPO / args.forms_out
    with forms.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["given_name", "records", "looks_placeholder"])
        for g, c in givens.most_common():
            w.writerow([g, c, "yes" if LOOKS_PLACEHOLDER.match(g or "") or not g
                        else "no"])
    print(f"\nwrote {forms} ({len(givens):,} distinct given names)")

    def is_ph(nm: str) -> bool:
        g = given_and_surname(nm)[0]
        return (not g) or bool(LOOKS_PLACEHOLDER.match(g))

    rows = []
    both = only_ph = 0
    for gid, nameset in names.items():
        ph = {nm for nm in nameset if is_ph(nm)}
        if not ph:
            continue
        real = nameset - ph
        if real:
            both += 1
        else:
            only_ph += 1
        rows.append({
            "geni_id": gid,
            "n_names": len(nameset),
            "n_placeholder": len(ph),
            "n_real": len(real),
            "has_real_name": "yes" if real else "no",
            "placeholder_names": " | ".join(sorted(ph)),
            "real_names": " | ".join(sorted(real)),
        })

    out = REPO / args.out
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows):,} profiles carry a placeholder name)\n")

    print(f"  {only_ph:>7,}  ONLY placeholder names - safe to normalise to NN")
    print(f"  {both:>7,}  ALSO have a real name - normalising would destroy it")

    print("\ntop placeholder-looking forms found in the data:")
    for g, c in givens.most_common():
        if (not g) or LOOKS_PLACEHOLDER.match(g):
            print(f"   {c:>7,}  {g!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
