"""`P7338` *regnal ordinal* on the given name, for the people whose ordinal we know.

    py scripts/build-regnal-ordinals.py

**Emma, 2026-08-15:** *"they should all have the regnal orders put on their names as
qualifiers"*, and **not only the Samaritans** — anyone whose name carries an ordering. Her
`name modelling.txt` puts it on the GIVEN NAME rather than on the person:

    Abisha III ben Phinhas ben Yittzhaq ben Shalma (Q107534535)
      P735 Abisha    P1545 1   P7452 usual forename   P7338 regnal ordinal 3

So the statement is `<person> P735 <given-name item>` carrying `P7338`, and it is the same
`P735` the name model wants anyway — the ordinal rides along rather than needing its own edit.

## Why this is small, and what the residue is

`reports/succession-and-ordinals.csv` holds 221 people; **110 carry a QID and 18 of those carry
a regnal number**. Of the 15 distinct given names behind those 18:

* **5 resolve to exactly one name item** — Abisha, Amram, Phinehas, Tabia, Yoseph. Those are
  emitted.
* **5 have no name item at all** — Aabed-El, Shalma, Tsedaka, Yaacob, Yitzhaq. They are
  Samaritan names Wikidata has never needed, so they wait on the name-item batch. `CLAUDE.md`
  § *The batches are a SEQUENCE* is the reason this is not a blocker: what cannot run today is
  tomorrow's batch, because tomorrow those items exist.
* **5 are ambiguous** — Aharon, Baba, Elazar, Jonathan, Levi, with two or three items each.
  § *One name item per USAGE* makes that hers, and they go on the same deck as the other
  ambiguous given names rather than being guessed at here.

**The ordinal is written as the ROMAN numeral the source uses**, not converted to an integer.
`P7338` is a string, and `III` is how the person is actually styled — `Abisha III`, not
`Abisha 3`. Her own worked example writes the numeral in the label and the ordinal beside it.

Writes `reports/wikidata-regnal-ordinals.qs`.
"""

from __future__ import annotations

import collections
import csv
import gzip
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SOURCE = REPO / "reports" / "succession-and-ordinals.csv"
NAME_ITEMS = REPO / "out" / "wikidata" / "name-items-in-store.tsv.gz"
OUT = REPO / "reports" / "wikidata-regnal-ordinals.qs"

TAB = chr(9)
NL = chr(10)

GIVEN_NAME = "P735"
REGNAL_ORDINAL = "P7338"
SERIES_ORDINAL = "P1545"
REASON_PREFERRED = "P7452"
USUAL_FORENAME = "Q3409033"


def given_items():
    """`{folded label: [qid]}` for every given-name item in the offline store."""
    out = collections.defaultdict(list)
    with gzip.open(NAME_ITEMS, "rt", encoding="utf-8") as fh:
        head = fh.readline().rstrip(NL).split(TAB)
        for line in fh:
            d = dict(zip(head, line.rstrip(NL).split(TAB)))
            if "given" not in (d.get("kind") or "").split("|"):
                continue
            for lab in (d.get("labels") or "").split("|"):
                if lab:
                    out[lab.casefold()].append(d["qid"])
    return out


def main() -> int:
    people = [r for r in csv.DictReader(io.open(SOURCE, encoding="utf-8"))
              if r["qid"] and r["regnal_number"].strip()]
    print(f"{len(people)} people carry both a QID and a regnal number")

    items = given_items()
    lines, held = [], []
    by_reason = collections.Counter()
    for r in sorted(people, key=lambda x: x["qid"]):
        given = r["name"].split()[0]
        qids = items.get(given.casefold(), [])
        if len(qids) != 1:
            held.append((r["qid"], r["name"], given,
                         "no name item" if not qids else f"{len(qids)} candidate items"))
            by_reason["no name item" if not qids else "ambiguous name item"] += 1
            continue
        # `P735` with the ordinal as a qualifier, plus the two qualifiers the name model puts
        # on a first given name. One statement, three qualifiers -- QuickStatements merges it
        # into the existing `P735` when the item already has one.
        lines.append(f'{r["qid"]}{TAB}{GIVEN_NAME}{TAB}{qids[0]}'
                     f'{TAB}{SERIES_ORDINAL}{TAB}"1"'
                     f'{TAB}{REASON_PREFERRED}{TAB}{USUAL_FORENAME}'
                     f'{TAB}{REGNAL_ORDINAL}{TAB}"{r["regnal_number"].strip()}"')
        by_reason["emitted"] += 1

    header = [
        "# P7338 regnal ordinal, as a qualifier on the given name.",
        "#",
        '# Emma, 2026-08-15: "they should all have the regnal orders put on their names as',
        '# qualifiers", and name modelling.txt puts P7338 on the P735 given name rather than',
        "# on the person. The ordinal is the Roman numeral the source uses, because P7338 is a",
        "# string and the person is styled Abisha III, not Abisha 3.",
        "#",
        "# Both ends already exist: the person's item and the given-name item. Nothing here is",
        "# created, so there is no single-run ordering problem.",
        "",
    ]
    OUT.write_text(NL.join(header + lines) + NL, encoding="utf-8", newline=NL)
    print(f"wrote {OUT.relative_to(REPO)} - {len(lines)} statements")
    for k, n in by_reason.most_common():
        print(f"   {n:>3}  {k}")
    if held:
        print(f"\n{len(held)} held, and each is somebody else's job:")
        for qid, name, given, why in held:
            print(f"   {qid:<13} {given:<10} {why:<22} {name[:44]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
