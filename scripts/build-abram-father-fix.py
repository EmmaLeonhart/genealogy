"""Abram's father: Wikidata skips a generation and we can prove it.

**Emma, 2026-08-16:** *"we are right, and Wikidata is wrong for the father. Deal
with it."*

**The error, and it is the same one this project already fixed on the Geni side.**
`Q135489730` *Abram ben Yitzhaq* states:

    P22  father  -> Q135489731  Tsedaka II ben Tabia ha'Åbtå'i
    P155 follows -> Q137394557  Yitzhaq I ben Tsedaka

So one item says Yitzhaq I preceded him in the priesthood while Tsedaka II
fathered him — skipping a generation. Pummer's succession has Tsedaka II 113,
Yitzhaq I 114, Abram 115, father to son to son.

**Geni had the identical skip until Emma created Yitzhaq I** (`6000000227245553985`)
and re-exported. Four Samaritan exports still carried `Tsedaka II -> Abram`
directly and are now in `exports/excluded/`; the merged tree says Abram's father is
**Yitzhaq I**. That is the whole reason `exports/excluded/` exists.

**This ADDS a statement, it does not remove one.** `CLAUDE.md` § *The purpose is
to ADD to Wikidata, not to correct it*: *"We will be more prone to adding in
contradictory information cited to Geni than we are to correcting information."*
The existing `P22` → Tsedaka II stays; a second `P22` → Yitzhaq I is emitted,
cited to Abram's Geni profile, which is the evidence we actually hold.

**It depends on Yitzhaq I getting his Geni ID first.** `Q137394557` currently has
**no claims at all** — Emma called it *"the worst modelled one (empty)"*. Her
ordering rule is that the Geni ID lands before anything derived from Geni, so this
edit declares that dependency rather than assuming the target is ready.

Writes `reports/wikidata-abram-father.json`. Nothing is executed; no Wikidata edits
before 1 September, which is her own instruction of 2026-08-14.

    py scripts/build-abram-father-fix.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = REPO / "reports" / "wikidata-abram-father.json"

ABRAM_QID, ABRAM_GENI = "Q135489730", "6000000178795709821"
YITZHAQ_QID, YITZHAQ_GENI = "Q137394557", "6000000227245553985"
TSEDAKA_QID = "Q135489731"
FATHER, CHILD = "P22", "P40"


def reference(geni_id: str) -> list[dict]:
    return [{"property": "P854",
             "value": f"https://www.geni.com/people/x/{geni_id}"},
            {"property": "P813", "value": "+2026-08-16T00:00:00Z/11"}]


def main() -> int:
    edits = [
        {
            "id": f"abram_father:{ABRAM_QID}",
            "type": "add_statement",
            "source": "corrected Geni tree; Pummer succession 113-114-115",
            "subject": {"qid": ABRAM_QID, "geni_id": ABRAM_GENI},
            # Yitzhaq I must carry his Geni ID before a Geni-derived statement
            # points at him. The edit that adds it is
            # `samaritan_priest_link:<qid>`; `entity_resolution:<qid>` was the wrong
            # prefix and named an id nothing emits for him.
            "requires": [f"samaritan_priest_link:{YITZHAQ_QID}"],
            "statements": [{
                "property": FATHER,
                "value": YITZHAQ_QID,
                "references": reference(ABRAM_GENI),
            }],
            "note": (
                "ADDS a second father. The existing P22 -> Q135489731 Tsedaka II "
                "is left in place; this project adds contradictory information "
                "cited to Geni rather than correcting. The same item already "
                "states P155 follows -> Q137394557 Yitzhaq I, so it contradicts "
                "itself: Yitzhaq I preceded Abram in office while Tsedaka II is "
                "given as his father, skipping a generation."
            ),
            "contradicts": {"property": FATHER, "value": TSEDAKA_QID},
        },
        {
            "id": f"abram_father_child:{YITZHAQ_QID}",
            "type": "add_statement",
            "source": "corrected Geni tree; Pummer succession 113-114-115",
            "subject": {"qid": YITZHAQ_QID, "geni_id": YITZHAQ_GENI},
            # Same correction as above: the Geni ID for Yitzhaq I is added by
            # `samaritan_priest_link:<qid>`, not by an entity-resolution edit.
            "requires": [f"samaritan_priest_link:{YITZHAQ_QID}"],
            "statements": [{
                "property": CHILD,
                "value": ABRAM_QID,
                "references": reference(YITZHAQ_GENI),
            }],
            "note": (
                "The reciprocal. Q137394557 has no claims at all - Emma's 'worst "
                "modelled one (empty)' - so this is an addition to an empty item "
                "and contradicts nothing."
            ),
        },
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({len(edits)} edits)")
    for e in edits:
        s = e["statements"][0]
        print(f"  {e['subject']['qid']:<12} {s['property']} -> {s['value']}"
              f"   requires {e['requires']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
