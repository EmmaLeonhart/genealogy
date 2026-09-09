"""Every profile in the corpus whose given name is a placeholder, one row each.

**Census first, normalisation after.** Emma, 2026-08-14: *"I want you to actually
be doing a serious analysis of the degree of things that have the NN thing with
them before you do anything, before you do any of this."* So this measures and
decides nothing. `scripts/labels.py` is untouched until the CSV has been read.

The proposal it exists to test — Emma's, same message — is that all of these
collapse to a single standard form:

    <private> -> NN
    Private   -> NN
    N N       -> NN
    blank     -> NN
    unknown   -> NN   (only when the ENTIRE name is "unknown")
    ?         -> undecided

**and the surname is kept in every case**, so `<private> /Larsson/` becomes
`NN Larsson` rather than losing the family name. The one exception she confirmed:
a surname of `.` becomes nothing, because a full stop is not a family name.

**One row per NAME record, not per person.** A Geni profile carries several
`NAME` lines and they disagree — that disagreement is the phenomenon. Rows are
deduplicated on (profile, raw name) across exports, with `n_exports` recording
how many exports carried it, because the same export arriving twice would
otherwise double every count.

    py scripts/build-unnamed-census.py
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
from genimerge.dates import date_fields  # noqa: E402

INDI = re.compile(r"^0 @I(\d+)@ INDI")

#: The given-name forms this census is about. Compared case-insensitively on the
#: text before the `/surname/` slot, whitespace collapsed.
FORMS = {
    "<private>": "<private>",
    "private": "Private",
    "nn": "NN",
    "n n": "N N",
    "n.n.": "N.N.",
    "unknown": "unknown",
    "?": "?",
    "??": "??",
    "": "(blank)",
    ".": ".",
    "-": "-",
    "_": "_",
}


def given_and_surname(raw: str) -> tuple[str, str]:
    """Split `<private> /Larsson/` into `('<private>', 'Larsson')`."""
    parts = raw.split("/")
    given = " ".join(parts[0].split())
    surname = " ".join(parts[1].split()) if len(parts) > 2 else ""
    return given, surname


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="reports/unnamed-profiles.csv")
    args = ap.parse_args()

    # (geni_id, raw_name) -> record
    seen: dict[tuple[str, str], dict] = {}
    exports_with: dict[tuple[str, str], set[str]] = defaultdict(set)

    paths = sources.find_exports()
    for n, path in enumerate(paths, 1):
        rel = str(path.relative_to(REPO))
        cur = None
        pending: dict[str, str] = {}
        sub = None
        # keys added for the profile currently being read, so SEX/BIRT/DEAT can
        # be attached without scanning every row seen so far - that was O(n) per
        # line and would not have finished.
        cur_keys: list[tuple[str, str]] = []
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            for raw in fh:
                raw = raw.rstrip("\n")
                m = INDI.match(raw)
                if m:
                    cur = m.group(1)
                    pending = {}
                    sub = None
                    cur_keys = []
                    continue
                if raw.startswith("0 "):
                    cur = None
                    continue
                if cur is None:
                    continue
                if raw.startswith("1 NAME "):
                    name = raw[7:].strip()
                    given, surname = given_and_surname(name)
                    if given.lower() not in FORMS:
                        sub = "NAME"
                        pending["last_name_row"] = ""
                        continue
                    key = (cur, name)
                    exports_with[key].add(rel)
                    seen.setdefault(key, {
                        "geni_id": cur,
                        "raw_name": name,
                        "given_form": FORMS[given.lower()],
                        "given_raw": given,
                        "surname": surname,
                        "surname_present": "yes" if surname and surname != "." else "no",
                        "GIVN": "", "SURN": "", "_MARNM": "",
                        "sex": "", "birt": "", "deat": "",
                        "first_export": rel,
                    })
                    pending["last_name_row"] = name
                    cur_keys.append(key)
                    sub = "NAME"
                    continue
                if raw.startswith("2 ") and pending.get("last_name_row"):
                    tag, _, val = raw[2:].partition(" ")
                    if tag in ("GIVN", "SURN", "_MARNM"):
                        rec = seen.get((cur, pending["last_name_row"]))
                        if rec is not None and not rec[tag]:
                            rec[tag] = val.strip()
                    continue
                if raw.startswith("1 "):
                    tag, _, val = raw[2:].partition(" ")
                    sub = tag
                    if tag == "SEX":
                        for k in cur_keys:
                            if not seen[k]["sex"]:
                                seen[k]["sex"] = val.strip()
                    pending["last_name_row"] = ""
                elif raw.startswith("2 DATE") and sub in ("BIRT", "DEAT"):
                    for k in cur_keys:
                        if not seen[k][sub.lower()]:
                            seen[k][sub.lower()] = raw[7:].strip()
        if n % 25 == 0:
            print(f"  read {n}/{len(paths)} exports, {len(seen):,} placeholder names")

    rows = []
    for key, rec in seen.items():
        rec = dict(rec)
        rec["n_exports"] = len(exports_with[key])
        rec.update({f"birt_{k}": v for k, v in date_fields(rec.pop("birt")).items()})
        rec.update({f"deat_{k}": v for k, v in date_fields(rec.pop("deat")).items()})
        rows.append(rec)

    out = REPO / args.out
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {out} ({len(rows):,} rows)\n")

    people = {r["geni_id"] for r in rows}
    print(f"{len(people):,} distinct profiles carry at least one placeholder name\n")
    forms = Counter(r["given_form"] for r in rows)
    with_sur = Counter(r["given_form"] for r in rows if r["surname_present"] == "yes")
    print(f"{'form':<12} {'rows':>8} {'with a real surname':>21}")
    for f, c in forms.most_common():
        print(f"{f:<12} {c:>8,} {with_sur.get(f, 0):>21,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
