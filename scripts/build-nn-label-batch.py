"""Wikidata items labelled `NN`, relabelled from a named relative.

**Emma's item, 2026-08-15:** *"I am not sure if we did something with NN on
Wikidata, but we also want to be updating the English language name and stuff. We
also want to be doing the label application stuff for basically all the NN stuff
on Wikidata."* She listed forty-odd examples; one of them,
`Q111238834`, already reads *"daughter of Fujiwara no Tadaki"*, which is the shape
the rest should take.

**This is the same rule the Geni side already uses**, applied to Wikidata items
instead of placeholder profiles: name somebody by the nearest relative who has a
name. Her precedence, from the placeholder work: **parent, then spouse, then
child.**

**`NN` is not a redaction and this is not the `Private` case.** `CLAUDE.md`:
*"`NN` is nomen nescio, a genealogist saying the name is unknown — a real
statement about a person, not Geni withholding data."* So the label is replaced
with something informative rather than emptied, and Emma's own instruction here is
to update it rather than blank it.

**A relative whose own label is `NN` is skipped, not used.** *"mother of NN"* names
nobody, and the fall-through continues to the next candidate. 22 of the 1,588 have
no usable relative at all and get no proposal.

**Offline.** Everything is read from `wikidata/items/` through the store index;
nothing is asked of Wikidata. **Nothing is executed** — this writes a reviewable
batch, and no Wikidata edits run before 1 September.

Writes `reports/wikidata-nn-labels.json` and `reports/wikidata-nn-labels.csv`.

    py scripts/build-nn-label-batch.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
SOURCE = REPO / "reports" / "wikidata-nn-items.csv"
OUT_JSON = REPO / "reports" / "wikidata-nn-labels.json"
OUT_CSV = REPO / "reports" / "wikidata-nn-labels.csv"

csv.field_size_limit(10_000_000)

FATHER, MOTHER, SPOUSE, CHILD, SEX = "P22", "P25", "P26", "P40", "P21"
SEX_LETTER = {"Q6581097": "M", "Q6581072": "F"}

#: The words, by the sex of the person being named. Unknown sex takes the neutral
#: form rather than a guess — inventing a gender to make a label read better is
#: the normalisation Emma has objected to before.
AS_CHILD = {"M": "son", "F": "daughter", "": "child"}
AS_SPOUSE = {"M": "husband", "F": "wife", "": "spouse"}
AS_PARENT = {"M": "father", "F": "mother", "": "parent"}

#: A label that names nobody. Used to reject a *relative* as a source, which is
#: the whole point: "mother of NN" is no better than "NN".
UNUSABLE = re.compile(r"^\s*(NN|N\.?\s?N\.?|\?+|unknown|anonymous|"
                      r"unnamed|no name)\s*$", re.I)


def main() -> int:
    rows = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    qids = [r["qid"] for r in rows]
    print(f"{len(qids):,} items labelled NN", flush=True)

    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(qids)

        def targets(entity: dict, prop: str) -> list[str]:
            out = []
            for claim in (entity.get("claims") or {}).get(prop, []):
                snak = claim.get("mainsnak") or {}
                if snak.get("snaktype") != "value":
                    continue
                value = (snak.get("datavalue") or {}).get("value")
                if isinstance(value, dict) and value.get("id"):
                    out.append(value["id"])
            return out

        wanted: set[str] = set()
        for q in qids:
            for prop in (FATHER, MOTHER, SPOUSE, CHILD):
                wanted |= set(targets(items.get(q, {}), prop))
        wanted -= set(qids)
        relatives = reader.entities(sorted(wanted))
        print(f"{len(relatives):,} relatives read", flush=True)

    def label_of(qid: str) -> str:
        entity = relatives.get(qid) or items.get(qid) or {}
        labels = entity.get("labels") or {}
        for lang in ("en", "mul"):
            if lang in labels:
                return (labels[lang] or {}).get("value", "") or ""
        return ""

    def sex_of(entity: dict) -> str:
        for claim in (entity.get("claims") or {}).get(SEX, []):
            value = (claim.get("mainsnak", {}).get("datavalue") or {}).get("value", {})
            if isinstance(value, dict):
                return SEX_LETTER.get(value.get("id"), "")
        return ""

    def targets(entity: dict, prop: str) -> list[str]:
        out = []
        for claim in (entity.get("claims") or {}).get(prop, []):
            snak = claim.get("mainsnak") or {}
            if snak.get("snaktype") != "value":
                continue
            value = (snak.get("datavalue") or {}).get("value")
            if isinstance(value, dict) and value.get("id"):
                out.append(value["id"])
        return out

    edits, out_rows, skipped = [], [], 0
    for row in rows:
        qid = row["qid"]
        entity = items.get(qid, {})
        sex = sex_of(entity)
        proposed, via, relation = "", "", ""
        # Parent, then spouse, then child - her precedence from the Geni side.
        for prop, words, name in ((FATHER, AS_CHILD, "father"),
                                  (MOTHER, AS_CHILD, "mother"),
                                  (SPOUSE, AS_SPOUSE, "spouse"),
                                  (CHILD, AS_PARENT, "child")):
            for target in targets(entity, prop):
                text = label_of(target)
                if not text or UNUSABLE.match(text):
                    continue          # names nobody; keep looking
                proposed = f"{words.get(sex, words[''])} of {text}"
                via, relation = target, name
                break
            if proposed:
                break

        out_rows.append([qid, row["en_label"], row.get("geni_id", ""), sex,
                         relation, via, proposed])
        if not proposed:
            skipped += 1
            continue
        edits.append({
            "id": f"nn_label:{qid}",
            "type": "set_label",
            "source": "relationship label from a named relative",
            "subject": {"qid": qid, "geni_id": row.get("geni_id") or None},
            "requires": [],
            "label": {"language": "en", "value": proposed},
            "replaces": row["en_label"],
            "kind": "change",
            "via": {"qid": via, "relation": relation},
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qid", "current_en", "geni_id", "sex",
                         "via_relation", "via_qid", "proposed_en"])
        writer.writerows(out_rows)

    print(f"\nwrote {OUT_JSON} ({len(edits):,} label edits) and {OUT_CSV}")
    print(f"  {skipped:,} have no relative with a usable name and get no proposal")
    for e in edits[:8]:
        print(f"   {e['subject']['qid']:<12} {e['label']['value'][:56]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
