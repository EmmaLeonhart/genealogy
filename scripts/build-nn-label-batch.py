"""`NN` belongs in `mul` and nowhere else; the local languages describe the person.

**Emma, 2026-08-16, stating the model in full:**

    "If it's on Wikidata and it's not somebody's name on Wikidata, or if it's on
    Wikidata and it is already the multi-language label, it should be preserved
    there. If it's in somebody's name on Wikidata but it is not in their
    multi-language label, it should be moved to it. Even while we change the names
    in local languages to be more specific things, no local language should have
    it. It's just the multi-language. The individual languages have more specific
    names."

Three states, and one of them needs work:

| state | action |
| --- | --- |
| `NN` already in `mul` | preserve — leave it |
| `NN` somewhere that is not a person's label | preserve — not ours |
| `NN` in a person's local-language label | **move it to `mul`, describe the local** |

**`mul` is where the marker lives.** Measured over the store rather than assumed:
`NN` sits in `en` on **1,549** of these 1,588 items and in `mul` on only **278**.
An earlier version of this script emitted `set_label` on `en` with
`"replaces": "NN"` and no `mul` edit at all, which would have erased the only copy
of the marker on 1,271 items.

**Every local language is cleared — fifteen of them, 2,273 labels.**

    en 1549 · nl 671 · cy 25 · be 6 · pl 4 · ru 3 · da 3 · ca 3
    uk 2 · de 2 · nb 1 · sv 1 · pt 1 · it 1 · es 1

A previous version kept `nl`'s 671 on the grounds that a Dutch label had not been
asked for. That was wrong twice over: it left `NN` in a local language, and it
treated "describe it in Dutch" as optional when the instruction is that **no local
language should have it**.

**Long-range relationships count.** Emma, 2026-08-16: *"It can work off of those
long-range things… grandparents or grandchildren or siblings."* So the search runs
parent → spouse → child → **sibling → grandparent → grandchild**.

**And the reach was measured on the synoptic tree, not on one store.** Emma named
that failure directly: *"you're using one source, like either the Wikidata or the
Jenny stuff, and not the Synoptic Tree… I'm pretty sure that long-range
relationships have much larger things to contribute than you consider them to do
so."* The method was wrong and the check was owed. **The result, for this
population, is that the join adds almost nothing** — and the reason is worth
recording because it bounds the claim rather than settling it:

| | count |
| --- | ---: |
| NN items | 1,588 |
| …carrying a `P2600` Geni.com profile ID at all | **27** |
| …whose Geni profile is in our corpus | **4** |
| Wikidata relatives unnamed on Wikidata but named in Geni | **4** |

These are Wikidata-only people. That is a fact about *this* set, not a reason to
skip the synoptic check next time.

**Nothing emits `remove_label`, because a bot already does it.** Emma, 2026-08-16:
*"We add the NN to the multi-language label first, and then afterwards we overwrite
the NN in other languages with whatever the goal is, because there is a bot that
exists that does the NN overwriting for other stuff. There is a bot that exists that
removes labels that match the multi-language label, so we don't need to stretch it
that much."*

So the order is **`mul` first, then overwrite the locals**, and any local still
reading `NN` afterwards now *matches* `mul` and the bot clears it. `cy`, `be`, `pl`,
`ru` and `uk` therefore get no edit at all: Slavic and Welsh inflect the name after
the relationship word, so `сын X` with an undeclined X is ungrammatical, a mangled
label is worse than none, and the bot removes the marker without our help. Those
languages are the seven-language item's job, which builds hand-made tables.

`ja` and `zh` are deliberately not written either, for a different reason: the
phrase would come out `Gerard Spencerの娘`, mixing scripts, because the relative's
name has not been transliterated. `CLAUDE.md` § *Labels in seven languages* owns
that and does it agentically, name by name.

**Offline.** Everything is read from `wikidata/items/` through the store index.
**Nothing is executed** — this writes a reviewable batch.

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

FATHER, MOTHER, SPOUSE, CHILD, SIBLING, SEX = "P22", "P25", "P26", "P40", "P3373", "P21"
SEX_LETTER = {"Q6581097": "M", "Q6581072": "F"}

#: The marker itself. Narrow on purpose: `unknown` and `?` are somebody else's
#: editorial choice and are not ours to move or delete.
NN_LABEL = re.compile(r"^\s*N\.?\s?N\.?\s*$", re.I)

#: Rejects a *relative* as the thing to name somebody by. Wider than `NN_LABEL`,
#: because "mother of unknown" names nobody either.
UNUSABLE = re.compile(r"^\s*(NN|N\.?\s?N\.?|\?+|unknown|anonymous|"
                      r"unnamed|no name|private)\s*$", re.I)

#: **Relationship words by language, keyed by what the SUBJECT is to the relative,
#: then by the subject's sex.** Unknown sex takes the neutral form rather than a
#: guess — inventing a gender to make a label read better is normalisation Emma has
#: objected to before.
#:
#: Only Germanic and Romance languages are here, and only ones already holding an
#: `NN`. Both build the phrase with a preposition and leave the following name
#: untouched, so the relative's label drops in verbatim and nothing is declined.
#: Languages that inflect the name are handled by removal instead.
WORDS: dict[str, dict[str, object]] = {
    "en": {"of": "of",
           "child_of": {"M": "son", "F": "daughter", "": "child"},
           "spouse_of": {"M": "husband", "F": "wife", "": "spouse"},
           "parent_of": {"M": "father", "F": "mother", "": "parent"},
           "sibling_of": {"M": "brother", "F": "sister", "": "sibling"},
           "grandchild_of": {"M": "grandson", "F": "granddaughter",
                             "": "grandchild"},
           "grandparent_of": {"M": "grandfather", "F": "grandmother",
                              "": "grandparent"}},
    "nl": {"of": "van",
           "child_of": {"M": "zoon", "F": "dochter", "": "kind"},
           "spouse_of": {"M": "echtgenoot", "F": "echtgenote", "": "partner"},
           "parent_of": {"M": "vader", "F": "moeder", "": "ouder"},
           "sibling_of": {"M": "broer", "F": "zus", "": "broer of zus"},
           "grandchild_of": {"M": "kleinzoon", "F": "kleindochter",
                             "": "kleinkind"},
           "grandparent_of": {"M": "grootvader", "F": "grootmoeder",
                              "": "grootouder"}},
    "de": {"of": "von",
           "child_of": {"M": "Sohn", "F": "Tochter", "": "Kind"},
           "spouse_of": {"M": "Ehemann", "F": "Ehefrau", "": "Ehepartner"},
           "parent_of": {"M": "Vater", "F": "Mutter", "": "Elternteil"},
           "sibling_of": {"M": "Bruder", "F": "Schwester", "": "Geschwister"},
           "grandchild_of": {"M": "Enkel", "F": "Enkelin", "": "Enkelkind"},
           "grandparent_of": {"M": "Großvater", "F": "Großmutter",
                              "": "Großelternteil"}},
    "da": {"of": "af",
           "child_of": {"M": "søn", "F": "datter", "": "barn"},
           "spouse_of": {"M": "ægtemand", "F": "hustru", "": "ægtefælle"},
           "parent_of": {"M": "far", "F": "mor", "": "forælder"},
           "sibling_of": {"M": "bror", "F": "søster", "": "søskende"},
           "grandchild_of": {"M": "barnebarn", "F": "barnebarn", "": "barnebarn"},
           "grandparent_of": {"M": "bedstefar", "F": "bedstemor",
                              "": "bedsteforælder"}},
    "sv": {"of": "till",
           "child_of": {"M": "son", "F": "dotter", "": "barn"},
           "spouse_of": {"M": "make", "F": "maka", "": "make eller maka"},
           "parent_of": {"M": "far", "F": "mor", "": "förälder"},
           "sibling_of": {"M": "bror", "F": "syster", "": "syskon"},
           "grandchild_of": {"M": "barnbarn", "F": "barnbarn", "": "barnbarn"},
           "grandparent_of": {"M": "morfar eller farfar",
                              "F": "mormor eller farmor",
                              "": "mor- eller farförälder"}},
    "nb": {"of": "til",
           "child_of": {"M": "sønn", "F": "datter", "": "barn"},
           "spouse_of": {"M": "ektemann", "F": "hustru", "": "ektefelle"},
           "parent_of": {"M": "far", "F": "mor", "": "forelder"},
           "sibling_of": {"M": "bror", "F": "søster", "": "søsken"},
           "grandchild_of": {"M": "barnebarn", "F": "barnebarn", "": "barnebarn"},
           "grandparent_of": {"M": "bestefar", "F": "bestemor",
                              "": "besteforelder"}},
    "es": {"of": "de",
           "child_of": {"M": "hijo", "F": "hija", "": "hijo o hija"},
           "spouse_of": {"M": "esposo", "F": "esposa", "": "cónyuge"},
           "parent_of": {"M": "padre", "F": "madre", "": "progenitor"},
           "sibling_of": {"M": "hermano", "F": "hermana",
                          "": "hermano o hermana"},
           "grandchild_of": {"M": "nieto", "F": "nieta", "": "nieto o nieta"},
           "grandparent_of": {"M": "abuelo", "F": "abuela",
                              "": "abuelo o abuela"}},
    "pt": {"of": "de",
           "child_of": {"M": "filho", "F": "filha", "": "filho ou filha"},
           "spouse_of": {"M": "marido", "F": "esposa", "": "cônjuge"},
           "parent_of": {"M": "pai", "F": "mãe", "": "progenitor"},
           "sibling_of": {"M": "irmão", "F": "irmã", "": "irmão ou irmã"},
           "grandchild_of": {"M": "neto", "F": "neta", "": "neto ou neta"},
           "grandparent_of": {"M": "avô", "F": "avó", "": "avô ou avó"}},
    "it": {"of": "di",
           "child_of": {"M": "figlio", "F": "figlia", "": "figlio o figlia"},
           "spouse_of": {"M": "marito", "F": "moglie", "": "coniuge"},
           "parent_of": {"M": "padre", "F": "madre", "": "genitore"},
           "sibling_of": {"M": "fratello", "F": "sorella",
                          "": "fratello o sorella"},
           "grandchild_of": {"M": "nipote", "F": "nipote", "": "nipote"},
           "grandparent_of": {"M": "nonno", "F": "nonna", "": "nonno o nonna"}},
    "ca": {"of": "de",
           "child_of": {"M": "fill", "F": "filla", "": "fill o filla"},
           "spouse_of": {"M": "marit", "F": "esposa", "": "cònjuge"},
           "parent_of": {"M": "pare", "F": "mare", "": "progenitor"},
           "sibling_of": {"M": "germà", "F": "germana", "": "germà o germana"},
           "grandchild_of": {"M": "nét", "F": "néta", "": "nét o néta"},
           "grandparent_of": {"M": "avi", "F": "àvia", "": "avi o àvia"}},
}

#: `en` is written on every item, not only where it already held `NN`: it is the
#: language a reader is most likely to have, and an item whose only label is `NN`
#: in `mul` cannot be found. Other languages are touched only where they carry the
#: marker already.
ALWAYS = ("en",)


def main() -> int:
    rows = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    qids = [r["qid"] for r in rows]
    print(f"{len(qids):,} items labelled NN", flush=True)

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

    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(qids)

        # First hop: everyone directly related. Second hop: their parents and
        # children, which is where grandparents and grandchildren come from.
        first: set[str] = set()
        for q in qids:
            for prop in (FATHER, MOTHER, SPOUSE, CHILD, SIBLING):
                first |= set(targets(items.get(q, {}), prop))
        first -= set(qids)
        near = reader.entities(sorted(first))
        print(f"{len(near):,} direct relatives read", flush=True)

        second: set[str] = set()
        for q in sorted(first):
            for prop in (FATHER, MOTHER, CHILD):
                second |= set(targets(near.get(q, {}), prop))
        second -= set(qids) | first
        far = reader.entities(sorted(second))
        print(f"{len(far):,} second-hop relatives read", flush=True)

    def label_of(qid: str) -> str:
        entity = near.get(qid) or far.get(qid) or items.get(qid) or {}
        labels = entity.get("labels") or {}
        for lang in ("en", "mul"):
            if lang in labels:
                return (labels[lang] or {}).get("value", "") or ""
        return ""

    def named(qid: str) -> str:
        """The relative's name, or `''` if they have none worth naming anyone by."""
        text = label_of(qid)
        return "" if not text or UNUSABLE.match(text) else text

    def sex_of(ent: dict) -> str:
        for claim in (ent.get("claims") or {}).get(SEX, []):
            value = (claim.get("mainsnak", {}).get("datavalue") or {}).get("value", {})
            if isinstance(value, dict):
                return SEX_LETTER.get(value.get("id"), "")
        return ""

    def nearest(qid: str) -> tuple[str, str, str]:
        """`(relation, relative_qid, relative_name)` for the nearest named one.

        Nearest-first: parent, spouse, child, sibling, then the long-range pair.
        """
        ent = items.get(qid, {})
        for key, candidates in (
            ("child_of", targets(ent, FATHER) + targets(ent, MOTHER)),
            ("spouse_of", targets(ent, SPOUSE)),
            ("parent_of", targets(ent, CHILD)),
            ("sibling_of", targets(ent, SIBLING)),
        ):
            for target in candidates:
                text = named(target)
                if text:
                    return key, target, text
        # **The long-range pass — Emma's widening.** Two hops up is a grandparent,
        # two hops down a grandchild. Computed, because Wikidata has no
        # grandparent property.
        for key, up, down in (("grandchild_of", (FATHER, MOTHER), (FATHER, MOTHER)),
                              ("grandparent_of", (CHILD,), (CHILD,))):
            for step in (t for p in up for t in targets(ent, p)):
                for target in (t for p in down
                               for t in targets(near.get(step, {}), p)):
                    text = named(target)
                    if text:
                        return key, target, text
        return "", "", ""

    edits, out_rows = [], []
    preserved = described = unnameable = 0

    for row in rows:
        qid = row["qid"]
        ent = items.get(qid, {})
        sex = sex_of(ent)
        labels = ent.get("labels") or {}

        def value(lang: str) -> str:
            return ((labels.get(lang) or {}).get("value") or "").strip()

        relation, via, other = nearest(qid)
        if not relation:
            unnameable += 1

        # --- preserve: NN into `mul`, and it lands first -----------------------
        needs_mul = not NN_LABEL.match(value("mul"))
        if needs_mul:
            preserved += 1
            edits.append({
                "id": f"nn_preserve:{qid}",
                "type": "set_label",
                "source": "move the NN marker into the multilingual label",
                "subject": {"qid": qid, "geni_id": row.get("geni_id") or None},
                "requires": [],
                "label": {"language": "mul", "value": "NN"},
                "kind": "add" if not value("mul") else "change",
                "replaces": value("mul"),
                "note": ("NN is nomen nescio and belongs in `mul` alone. Every "
                         "local-language copy is cleared below, so this has to "
                         "land first."),
            })
        depends = [f"nn_preserve:{qid}"] if needs_mul else []

        # --- clear every local language that holds NN --------------------------
        holders = sorted(
            lang for lang, val in labels.items()
            if lang != "mul" and NN_LABEL.match((val or {}).get("value") or "")
        )
        touched: set[str] = set()
        for lang in sorted(set(holders) | set(ALWAYS)):
            if lang == "mul":
                continue
            current = value(lang)
            holds_nn = bool(NN_LABEL.match(current))
            if current and not holds_nn:
                continue          # a real label here; not ours to touch
            words = WORDS.get(lang)
            if words and relation:
                described += 1
                touched.add(lang)
                table = words[relation]
                word = table.get(sex) or table[""]
                edits.append({
                    "id": f"nn_label:{qid}:{lang}",
                    "type": "set_label",
                    "source": "relationship label from the nearest named relative",
                    "subject": {"qid": qid, "geni_id": row.get("geni_id") or None},
                    "requires": depends,
                    "label": {"language": lang,
                              "value": f"{word} {words['of']} {other}"},
                    "replaces": current,
                    "kind": "change" if current else "add",
                    "via": {"qid": via, "relation": relation},
                })

        out_rows.append([qid, row.get("geni_id", ""), sex, relation, via, other,
                         "|".join(holders), "|".join(sorted(touched)),
                         "yes" if needs_mul else "already"])

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qid", "geni_id", "sex", "relation", "via_qid",
                         "via_name", "languages_holding_nn", "languages_changed",
                         "mul_needed"])
        writer.writerows(out_rows)

    print(f"\nwrote {OUT_JSON} ({len(edits):,} edits) and {OUT_CSV}")
    print(f"  {preserved:,} move NN into `mul`; the rest already had it there")
    print(f"  {described:,} descriptive labels across {len(WORDS)} languages")
    print("  no remove_label emitted: a bot clears locals that match `mul`")
    print(f"  {unnameable:,} have no named relative at any distance — `mul` only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
