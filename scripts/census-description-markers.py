#!/usr/bin/env python3
"""Every person whose LABEL carries a `_DESCRIPTION` marker out of their own `NSFX`.

**`Q141313961` read *Helena Maria Linnerhielm ogift*.** `ogift` is a suffix that should never
have been treated as part of the name, and it needs correcting on everyone whose label carries
it.

`ogift` is Swedish for *unmarried*. It is already in `namemodel._DESCRIPTION` -- the group
whose own comment reads *"a description of the person, never a name"* -- so it has never
become a `P735` *given name* or a `P734` *family name*. What nothing removed it from is the
**label**: `build-display-names.py` concatenates `givn + surn + NSFX` into `display_name`, and
`derive-labels.py` takes that string whole. § *A TITLE IS NOT A NAME* said in as many words
that the tail rule *"does not touch the LABEL"*, and left what the label should read as an
open question. This is that question answered for one class of token.

**The census matches the person's OWN `NSFX`, never a bare word list against a trailing
token** -- the rule `drop_title_suffix` already carries, and the reason `Anna King` keeps her
surname. So a `Twin` or an `Infant` that Geni recorded as a *name* is untouched here; only a
token the profile itself files as a suffix is counted.

Writes `reports/description-markers-in-labels.tsv`, sorted on the Geni id.
"""
from __future__ import annotations

import csv
import gzip
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from namemodel import _DESCRIPTION, drop_description_suffix  # noqa: E402 - after sys.path

DESCRIPTION = frozenset(t.casefold() for t in _DESCRIPTION)
OUT = REPO_ROOT / "reports" / "description-markers-in-labels.tsv"


def opened(stem: str):
    """The plain CSV where a clone has unpacked it, else the tracked `.gz`."""
    plain = REPO_ROOT / "reports" / f"{stem}.csv"
    if plain.exists():
        return open(plain, encoding="utf-8", newline="")
    return gzip.open(REPO_ROOT / "reports" / f"{stem}.csv.gz", "rt", encoding="utf-8", newline="")


def marker_tokens(nsfx: str) -> list[str]:
    """The `_DESCRIPTION` tokens of one `NSFX` field, in the order Geni wrote them."""
    return [t for t in (nsfx or "").split()
            if t.strip("()[]{}.,").casefold() in DESCRIPTION]


def main() -> int:
    # The ledger is what says a person is LIVE on Wikidata, and it is refreshed from the
    # account's contributions -- an item created since the last download is in here and in no
    # store.
    ledger: dict[str, str] = {}
    ledger_path = REPO_ROOT / "reports" / "garborg-qids.tsv"
    if ledger_path.exists():
        with open(ledger_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                gid, qid = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
                if gid and qid:
                    ledger[gid] = qid

    # **Read `display-names.csv`, NOT `derived-labels.csv`.** The first run of this census read
    # the derived labels, so once `derive-labels.py` had applied the fix it re-ran and reported
    # **4 people** where the population is 631 -- a census that measures whether it has already
    # been run is not a census. `display_name` is the raw `givn + surn + NSFX` concatenation and
    # does not move when the label rule changes, so this answers the same question before and
    # after.
    rows = []
    counts: Counter[str] = Counter()
    with opened("display-names") as handle:
        for row in csv.DictReader(handle):
            nsfx = (row["nsfx"] or "").strip()
            toks = marker_tokens(nsfx)
            if not toks:
                continue
            shown = (row["display_name"] or "").strip()
            corrected = drop_description_suffix(shown, nsfx)
            if corrected == shown:
                continue  # the marker is in the suffix field but never reached the name
            gid = row["geni_id"]
            for tok in toks:
                counts[tok.strip("()[]{}.,").casefold()] += 1
            rows.append({
                "geni_id": gid,
                "qid": ledger.get(gid, ""),
                "live": "yes" if gid in ledger else "no",
                "nsfx": nsfx,
                "markers": " ".join(toks),
                "geni_display_name": shown,
                "corrected": corrected,
            })

    # A TOTAL key. `geni_id` alone is not unique -- a person with several NAME records has a row
    # each -- so the name index rides along behind it, exactly as the id orders the rest of the
    # generated tables. § *SORTING MUST BE DETERMINISTIC*.
    rows.sort(key=lambda r: (r["geni_id"], r["geni_display_name"], r["nsfx"]))
    fields = ["geni_id", "qid", "live", "nsfx", "markers", "geni_display_name", "corrected"]
    with open(OUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", lineterminator="\n", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    people = len({r["geni_id"] for r in rows})
    live = len({r["geni_id"] for r in rows if r["live"] == "yes"})
    print(f"{len(rows):,} name records over {people:,} people carry a description marker in "
          f"the rendered name; {live:,} are live on Wikidata")
    for tok, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {n:5d}  {tok}")
    print(f"-> {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
