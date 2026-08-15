"""Standardise how the Samaritan high priests are modelled on Wikidata.

**Emma, 2026-08-16, adding this as the final queue item:** *"I want you to look
over the data modeling of all of them and try to put together something based
upon the most recent data modeling to be done across all of them in a standard
way, with the succession… they're rather poorly modeled… Particularly the ones
from around 1600 to 1980 are really badly modeled."*

**Measured, and it is worse than "inconsistent": there are two opposite styles
and no item uses both.**

| | items | style |
| --- | ---: | --- |
| `P39` = `Q678510` *Samaritan High Priest*, no succession | 5 | the modern ones |
| item-level `P155`/`P156` succession, **no `P39` at all** | 11 | the older ones |
| neither | 5 | |

So **16 of 21 do not say they held the office**, and the 5 that do say nothing
about who preceded them. Her earlier description of the fix, 2026-08-14: *"an
example of a single one of these custom atomic edits would be one that, in a
single sweep, removes the old style of 'preceded by' and 'followed by' and puts
in the occupation 'Samaritan high priest' preceded by 'followed by' as used by
the modern ones."*

**The target model**, which is Wikidata's normal shape for an office:

    P39  Q678510            position held: Samaritan High Priest
      P1365 <predecessor>     replaces
      P1366 <successor>       replaced by

Succession becomes **qualifiers on the office statement**, not free-floating
item-level `P155`/`P156`. `P155`/`P156` are generic "follows/followed by" and say
nothing about *what* is being succeeded to; on a person they are the wrong
property for holding an office.

**The order is sourced, not inferred.** The existing `P155`/`P156` edges gave one
chain of 14 running Yitzhaq I → Yaacob II and left the five modern priests
floating entirely. Emma offered the way out — *"You can use the Wikipedia article
on Samaritan high priest to find the order of succession if you need it"* — and
that article (Pummer's list) supplies both missing ends and the term dates. All
**21 of 21** are now placed. Where the article and the existing links disagree the
article wins: it is a source, and the `P155`/`P156` here are an artefact of
piecemeal editing.

**Term dates come with it**, as `P580`/`P582` qualifiers on the office statement.
A slashed year like `1859/60` is left out rather than halved — the article is
hedging between two, and choosing one would assert a precision the source does
not have.

**Nothing here runs before 1 September.** Writes
`reports/wikidata-samaritan-succession.json`.

    py scripts/build-samaritan-succession.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

LINKS = REPO / "reports" / "samaritan-priest-links.csv"
OUT = REPO / "reports" / "wikidata-samaritan-succession.json"

OFFICE = "Q678510"          # Samaritan High Priest
POSITION_HELD = "P39"
REPLACES, REPLACED_BY = "P1365", "P1366"
FOLLOWS, FOLLOWED_BY = "P155", "P156"


#: The succession, from the Wikipedia article Emma pointed at: *"You can use the
#: Wikipedia article on Samaritan high priest to find the order of succession if
#: you need it."* Pummer's list. `(qid, name, start, end)`; `None` for a QID we
#: do not hold, `""` for a year that is not stated unambiguously.
#:
#: **This closes what the existing links could not.** `P155`/`P156` on the items
#: gave one chain of 14 running Yitzhaq I → Yaacob II, and left the five modern
#: priests floating. The article supplies both ends: Tsedaka II before Yitzhaq I,
#: and Yaacob II → Yoseph II → Levi VI → Shalom II → Elazar XX → Aharon IV →
#: Aabed-El V.
#:
#: **`Saloum Cohen` `Q2067443` is Shalom II**, and that is checked rather than
#: assumed: its `nl` and `fr` labels both read *Shalom ben Amram*, and its `P570`
#: is 2004-02-09 against the article's 2001–2004 term.
#:
#: **A slashed year is left empty rather than halved.** `1859/60` is the article
#: hedging between two, and picking one would state a precision the source does
#: not have.
SUCCESSION = [
    (None,         "Shalma I ben Phinehas",                       "", ""),
    ("Q135489731", "Tsedaka II ben Tabia ha'Åbtå'i",              "", "1650"),
    ("Q137394557", "Yitzhaq I ben Tsedaka",                   "1650", "1694"),
    ("Q135489730", "Abram ben Yitzhaq",                       "1694", "1732"),
    ("Q135489805", "Levi V ben Abram",                        "1733", "1752"),
    ("Q135489728", "Tabia III ben Yitzhaq ben Abram",         "1752", "1787"),
    ("Q135489727", "Shalma II ben Tabia",                     "1798", "1828"),
    ("Q135489819", "Amram VIII ben Shalma",                   "1828",     ""),
    ("Q109888305", "Yaacob I ben Aaharon ben Shalma",             "", "1916"),
    ("Q107534637", "Yitzhaq II ben Amram ben Shalma ben Tabia",    "", "1932"),
    ("Q108907045", "Matzliach ben Phinehas ben Yitzhaq ben Shalma", "1933", "1943"),
    ("Q107534535", "Abisha III ben Phinehas ben Yitzhaq ben Shalma", "1943", "1960"),
    ("Q107534557", "Amram IX ben Yitzhaq ben Amram ben Shalma", "1960", "1980"),
    ("Q108764515", "Asher ben Matzliach ben Phinehas",         "1980", "1982"),
    ("Q108907046", "Phinehas X ben Matzliach ben Phinehas",    "1982", "1984"),
    ("Q118782320", "Yaacob II ben Uzzi ben Yaacob ben Aaharon", "1984", "1987"),
    ("Q8055954",   "Yoseph II ben Ab-Hisda ben Yaacov ben Aaharon", "1987", "1998"),
    ("Q2666440",   "Levi VI ben Abisha ben Phinehas ben Yitzhaq", "1998", "2001"),
    ("Q2067443",   "Shalom II ben Amram ben Yitzhaq",          "2001", "2004"),
    ("Q2164896",   "Elazar XX ben Tsedaka ben Yitzhaq",        "2004", "2010"),
    ("Q2031200",   "Aharon IV ben Ab-Chisda ben Yaacob",       "2010", "2013"),
    ("Q13485740",  "Aabed-El V ben Asher ben Matzliach",       "2013",     ""),
]

START_TIME, END_TIME = "P580", "P582"


def values(entity, prop):
    out = []
    for st in (entity.get("claims") or {}).get(prop, []):
        if st.get("rank") == "deprecated":
            continue
        snak = st.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        v = snak.get("datavalue", {}).get("value")
        if isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def main() -> int:
    rows = list(csv.DictReader(LINKS.open(encoding="utf-8", newline="")))
    qids = [r["qid"] for r in rows]
    name = {r["qid"]: r["wikidata_name"] for r in rows}
    geni = {r["qid"]: r["geni_id"] for r in rows}

    with wikistore.StoreReader(REPO / "wikidata" / "items",
                               REPO / "out" / "wikidata" / "store-index.sqlite3") as rd:
        ents = rd.entities(qids)
    print(f"{len(ents)} of {len(qids)} priest items held")

    # The order comes from SUCCESSION, not from the existing links. The links
    # gave 14 of 21 and left the modern five floating; the article closes both
    # ends. Where the two disagree, the article wins - it is a source, and
    # P155/P156 here are an artefact of piecemeal editing.
    order = [q for q, _n, _s, _e in SUCCESSION if q]
    terms = {q: (s, e) for q, _n, s, e in SUCCESSION if q}
    predecessor, successor = {}, {}
    for i, q in enumerate(order):
        if i:
            predecessor[q] = order[i - 1]
        if i + 1 < len(order):
            successor[q] = order[i + 1]
    print(f"{len(order)} of {len(qids)} priests placed in the sourced succession")
    unplaced = [q for q in qids if q not in terms]
    if unplaced:
        print("  not in the article's list: "
              + ", ".join(name.get(q, q) for q in unplaced))
    print("  " + " -> ".join(name[q].split(" ben ")[0] for q in order if q in name))
    print()

    edits = []
    for q in qids:
        e = ents.get(q, {})
        has_office = OFFICE in values(e, POSITION_HELD)
        old = values(e, FOLLOWS) + values(e, FOLLOWED_BY)
        quals = {}
        if q in predecessor:
            quals[REPLACES] = predecessor[q]
        if q in successor:
            quals[REPLACED_BY] = successor[q]
        if has_office and not old and not quals:
            continue                      # already correct and nothing to add
        edits.append({
            "id": f"samaritan_succession:{q}",
            "type": "normalise_office",
            "source": "samaritans/priests.txt + existing P155/P156",
            "subject": {"qid": q, "geni_id": geni.get(q) or None},
            "requires": [],
            "add": [{
                "property": POSITION_HELD,
                "value": OFFICE,
                "qualifiers": ([{"property": p, "value": v}
                                for p, v in sorted(quals.items())]
                               + [{"property": pr, "value": f"+{yr}-00-00T00:00:00Z/9"}
                                  for pr, yr in ((START_TIME, terms.get(q, ("", ""))[0]),
                                                 (END_TIME, terms.get(q, ("", ""))[1]))
                                  if yr]),
                "references": ([{"property": "P2600", "value": geni[q]}]
                               if geni.get(q) else []),
            }] if not has_office or quals else [],
            # The old style goes only where the new statement carries the same
            # fact, so no succession is lost in the swap.
            "remove": [{"property": p, "value": v}
                       for p in (FOLLOWS, FOLLOWED_BY) for v in values(e, p)
                       if quals],
            "name": name[q],
            "already_had_office": has_office,
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    add = sum(1 for e in edits if e["add"])
    rem = sum(1 for e in edits if e["remove"])
    print(f"\nwrote {OUT} ({len(edits)} entries)")
    print(f"  {add} add a P39 office statement, {rem} remove old P155/P156")
    print(f"  {sum(1 for q in qids if OFFICE in values(ents.get(q, {}), POSITION_HELD))}"
          f" of {len(qids)} already stated the office before this")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
