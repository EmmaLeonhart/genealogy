"""Wikidata items labelled `NN`, relabelled from a named relative.

**Emma's item, 2026-08-15:** *"I am not sure if we did something with NN on
Wikidata, but we also want to be updating the English language name and stuff. We
also want to be doing the label application stuff for basically all the NN stuff
on Wikidata."* She listed forty-odd examples; one of them,
`Q111238834`, already reads *"daughter of Fujiwara no Tadaki"*, which is the shape
the rest should take.

**The descriptive label uses the same rule the Geni side already uses**, applied to Wikidata items
instead of placeholder profiles: name somebody by the nearest relative who has a
name. Her precedence, from the placeholder work: **parent, then spouse, then
child.**

**`NN` IS PRESERVED. It is never replaced.** Emma, 2026-08-16: *"NN is not
relabeled. Why are you thinking that I'm saying that it's relabeled? NN is always
preserved in the multi-language label. It just has more descriptive labels added in
some languages for the relationships."*

This script previously emitted `set_label` on `en` with `"replaces": "NN"` — and
**NN lives in `en` on 1,549 of these 1,570 items and in `mul` on only 278**, so
that batch would have destroyed the only copy of it on 1,271 items. Measured, not
supposed:

    en 1549 · nl 671 · mul 278 · cy 25 · be 6 · pl 4 · ru 3 · da 3 · ca 3

**So each item gets two edits, and the NN survives both:**

* `mul` ← `NN`, where `mul` does not already carry it. This is the copy that is
  *"always preserved"*, and it is what makes overwriting `en` safe.
* `en` ← *"daughter of Fujiwara no Tadaki"*, the descriptive relationship label,
  **only where `en` is absent or is itself `NN`.** An item whose `en` already says
  something real is left alone.

`nl` keeps its 671 `NN`s untouched. A Dutch descriptive label is *"some languages"*
work that has not been asked for and is not guessed at here.

**And this is the same treatment `Private` should get** — Emma, same message:
*"NN and private are the same thing here, because if there's a private individual
whose name is not exported, it comes out as an NN."* `scripts/labels.py` currently
empties `Private` and keeps `NN`, which is the inconsistency she named. That is a
Geni-side change tracked in `queue.md`, not here.

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

#: Just the `NN` forms, for deciding whether a language slot is free. Narrower
#: than `UNUSABLE`: `unknown` in `en` is somebody else's editorial choice and is
#: not ours to overwrite.
NN_LABEL = re.compile(r"^\s*N\.?\s?N\.?\s*$", re.I)


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

    edits, out_rows, skipped, preserved, occupied = [], [], 0, 0, 0
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

        labels = (entity.get("labels") or {})

        def value(lang: str) -> str:
            return ((labels.get(lang) or {}).get("value") or "").strip()

        # **The preserving half, and it comes first.** NN goes into `mul` unless
        # it is already there, so the marker survives the `en` change below. This
        # is emitted whether or not a descriptive label could be found - the
        # preservation does not depend on naming a relative.
        if not NN_LABEL.match(value("mul")):
            preserved += 1
            edits.append({
                "id": f"nn_preserve:{qid}",
                "type": "set_label",
                "source": "preserve the NN marker in the multilingual label",
                "subject": {"qid": qid, "geni_id": row.get("geni_id") or None},
                "requires": [],
                "label": {"language": "mul", "value": "NN"},
                "kind": "add" if not value("mul") else "change",
                "replaces": value("mul"),
                "note": ("NN is nomen nescio and is preserved, never replaced. It "
                         "sits in `en` on this item and `en` is about to carry a "
                         "descriptive relationship label instead, so `mul` is "
                         "where the marker is kept."),
            })

        # **The descriptive half.** Only where `en` is free - absent, or NN
        # itself. An item already carrying a real English label is not touched.
        en_now = value("en")
        en_free = (not en_now) or bool(NN_LABEL.match(en_now))
        out_rows.append([qid, en_now, row.get("geni_id", ""), sex,
                         relation, via, proposed if en_free else "",
                         "yes" if en_free else "no (en already named)"])
        if not proposed:
            skipped += 1
            continue
        if not en_free:
            occupied += 1
            continue
        edits.append({
            "id": f"nn_label:{qid}",
            "type": "set_label",
            "source": "relationship label from a named relative",
            "subject": {"qid": qid, "geni_id": row.get("geni_id") or None},
            "requires": [f"nn_preserve:{qid}"] if not NN_LABEL.match(value("mul")) else [],
            "label": {"language": "en", "value": proposed},
            "replaces": en_now,
            "kind": "change" if en_now else "add",
            "via": {"qid": via, "relation": relation},
            "note": ("NN is not lost: it is preserved in `mul` by the required "
                     "nn_preserve edit, or was already there."),
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qid", "current_en", "geni_id", "sex",
                         "via_relation", "via_qid", "proposed_en", "en_free"])
        writer.writerows(out_rows)

    print(f"\nwrote {OUT_JSON} ({len(edits):,} label edits) and {OUT_CSV}")
    print(f"  {preserved:,} get NN written into `mul` so the marker survives")
    print(f"  {skipped:,} have no relative with a usable name and get no proposal")
    print(f"  {occupied:,} already carry a real `en` label and are not touched")
    for e in edits[:8]:
        print(f"   {e['subject']['qid']:<12} {e['label']['value'][:56]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
