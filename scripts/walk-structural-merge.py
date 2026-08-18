"""Walk up the parental lines, matching Geni's parents against Wikidata's.

Emma, 2026-08-15: *"For the synoptic tree, we're supposed to be specifically
going up the parental lines and stuff like that and merging the parents on Jenny
and Wikidata if there are ones on both. Same with all the other relationships.
That is a critical part of building up this synoptic tree."*

**This shows cases. It does not build a pipeline.** `CLAUDE.md` § *How this
project works now*: show records one by one, derive the rule from them, never the
other way round. It writes no edits and merges nothing.

**The structure picks the pair; the label only confirms it.** Start from somebody
holding **both** a Geni ID and a QID. Our father of that Geni ID and Wikidata's
`P22` of that QID are the *same position in the same family*, so they are the
same person unless something says otherwise — Emma's 2026-08-12 rule: *"we merge
them based off of whether something is the mother on both sides of an individual.
We merge them together unless the mothers really conflict."*

**What this must never become:** searching Wikidata for a name. That is the
matcher Emma killed on 2026-08-12 and whose module was deleted on 2026-08-15.
`correspondence.md`: *"No name similarity, ever. Not as a tiebreak, not as
corroboration, not as a candidate list for a human."* Every comparison here is
between two people the structure already placed opposite each other.

**Four outcomes at each position**, and they are reported separately because they
need different decisions:

* `AGREE`    — both sides name a parent and they are already the same item.
* `MERGE`    — both sides name a parent, ours has no QID: **this is the
  correspondence to record.**
* `GENI ONLY`— we have a parent, Wikidata does not. A creation, later.
* `WD ONLY`  — Wikidata has a parent, we do not. Nothing to do here.

Offline: `reports/derived-family.csv` for our side, the downloaded store for
Wikidata's. Nothing is asked of the network.

    py scripts/walk-structural-merge.py --start <geni id> --lines 5
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from collections import Counter  # noqa: E402
from genimerge import wikistore  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
import labels as _labels  # noqa: E402

FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
PREVIEW = REPO / "reports" / "relationship-label-preview.csv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
STORE = REPO / "wikidata" / "items"

csv.field_size_limit(10 ** 7)

FATHER, MOTHER = "P22", "P25"

#: Emma's gate on everything created: `en` · `ja` · `zh` · `hi` · `ar` · `ru` ·
#: `el`, plus `mul`. *"WE ARE NOT DOING THIS SHIT UNTIL WE HAVE JA and ZH LABELS
#: ON EVERYTHING THIS IS RIGHT BEFORE WIKIDATA EDITING."* Every edit records which
#: of these it still lacks, so the batch that fills them can find its own work.
REQUIRED_LANGUAGES = ("en", "ja", "zh", "hi", "ar", "ru", "el")


#: A label that names nobody, so it must never reach a local language. From
#: `reports/given-name-forms.csv` by way of
#: `scripts/build-relationship-label-preview.py`, which screens the same vocabulary.
PLACEHOLDER_LABELS = _labels.PLACEHOLDER_FORMS


def is_placeholder_label(label: str) -> bool:
    """Whether this string is a marker rather than a name.

    **Emma, 2026-08-16:** *"NN is always preserved in the multi-language label. It
    just has more descriptive labels added in some languages for the
    relationships."* And: *"no local language should have it."* So `NN` in `en` is
    the specific thing forbidden — the first version of this walk's label set put
    it there for 10 people whose derived label is literally `NN`, plus the
    `NN <surname>` forms, by copying `label_en` across without looking at it.
    """
    low = (label or "").strip().lower()
    if not low or low in PLACEHOLDER_LABELS:
        return True
    if "private" in low:
        return True
    head = low.split()[0]
    return head in PLACEHOLDER_LABELS


def label_set_for(row: dict) -> dict:
    """The label set for one `derived-labels.csv` row, per `emission-spec.md`.

    **A placeholder was being created with `en` and nothing else.** Emma's spec is
    that *"the multi-language label comes from the Latin alphabet name, and the
    English language label will come from it too"* — so `mul` is the label that
    matters and it was the one missing on all 12,260. `mul` is not a nicety here:
    it is the only label a person keeps when a local-language bot clears the rest.

    `ja` and `zh` come from the Han/kanji name **as written**, which is the same
    string for both: *"If the name is solely in kanji, then the Chinese and
    Japanese labels are both the same for it."* Only a name carrying kana would
    need translating, and none is invented here — a person with no CJK name
    recorded simply has no `ja`, and the seven-language item is what fills it.
    """
    out = {}
    mul = (row.get("label_mul") or "").strip()
    en = (row.get("label_en") or "").strip()
    # **A marker is not this function's business, in either slot.** `Private` must
    # never be written as a label at all — `CLAUDE.md`: *"'Private' is a redaction
    # marker, not a name, and an item labelled that asserts something false while
    # being impossible to find"* — and the marker these people *do* get is `NN`,
    # her words: *"if there's a private individual whose name is not exported, it
    # comes out as an NN."* So both slots drop it here and the `NN` overlay below
    # supplies `mul`; a person that overlay cannot reach ends up with no label,
    # which is the honest outcome rather than a false one.
    if mul and not is_placeholder_label(mul):
        out["mul"] = mul
    if en and not is_placeholder_label(en):
        out["en"] = en
    cjk = (row.get("cjk_names") or "").strip()
    if cjk:
        first = cjk.split(" | ")[0].strip()
        # **The same guard `mul` and `en` get, and it was missing here.** A marker
        # is not a label in any local language, and this branch wrote one straight
        # through: 22 edits carried `未知` — Chinese for *unknown* — as their `ja`
        # and `zh` label. Emma, 2026-08-18: *"Ukjent and 未知 get the mul NN
        # treatment"*, which is `NN` in `mul` and a descriptive label elsewhere,
        # never the marker itself in a local slot.
        #
        # It went unnoticed because `未知` was not in `labels.WORDS_MEANING_UNKNOWN`
        # until the same day, so `is_placeholder_label` said no and the asymmetry
        # in this function had nothing to catch. Two faults, one visible symptom:
        # the vocabulary was short a word *and* this branch was not consulting it.
        if first and not is_placeholder_label(first):
            out["ja"] = out["zh"] = first
    return out


def wd_parent(entity, prop):
    """The QIDs Wikidata states for this parent property, truthy ranks only."""
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


def label_of(entity, lang="en"):
    if not entity:
        return None
    lab = (entity.get("labels") or {}).get(lang)
    return lab.get("value") if isinstance(lab, dict) else lab



def walk_all(anchors, fam, ourqid, names, label_sets, depth):
    """Every anchor, writing what the walk finds.

    Emma, 2026-08-16, on the three "questions" this had been sitting on:
    *"if they are only on wikidata there is no problem is there lol. But about
    only geni well same? Tehy are created lol. WAHT TE FUCK IS THIS THIS IS A
    SUPER EASY THING ANS YOU ARE TRATING IT AS A BLOCKER."* She is right on both.
    `WD ONLY` needs nothing — Wikidata knowing a parent we do not costs us
    nothing. `GENI ONLY` is a **creation**, which is the entire point of the
    project. Neither was ever a decision.

    So this writes the two things she asked the midnight job to produce: the
    QID ↔ Geni ID correspondence built from the merges, and the placeholder list
    for people on Geni and not on Wikidata.
    """
    import csv as _csv
    import json as _json

    # Everything the walk needs to look up, gathered before touching the store.
    need = set()
    for g in anchors:
        cur = g
        for _ in range(depth):
            if cur in ourqid:
                need.add(ourqid[cur])
            row = fam.get(cur)
            if not row:
                break
            cur = (row.get("father") or row.get("mother") or "").strip()
            if not cur:
                break
    print(f"reading {len(need):,} items out of the store")
    with wikistore.StoreReader(STORE, INDEX) as reader:
        ents = reader.entities(sorted(need))
    print(f"{len(ents):,} of them are held")

    corr, placeholders, tally = {}, {}, Counter()
    for start in anchors:
        cur = start
        for _ in range(depth):
            row = fam.get(cur)
            if not row:
                break
            ent = ents.get(ourqid.get(cur, ""))
            for prop, key in ((FATHER, "father"), (MOTHER, "mother")):
                ours_id = (row.get(key) or "").strip()
                theirs = wd_parent(ent, prop) if ent else []
                if not ours_id and not theirs:
                    continue
                if ours_id and theirs:
                    mine = ourqid.get(ours_id, "")
                    if mine and mine in theirs:
                        tally["AGREE"] += 1
                    elif len(theirs) == 1:
                        # One candidate in the same family position: the
                        # correspondence. More than one and the position does not
                        # single anybody out, so it is left alone.
                        tally["MERGE"] += 1
                        # **Record the anchor too.** Without it a row says "this
                        # Geni person is that QID" and gives no way to check the
                        # claim: the whole basis is that both sit at the same
                        # parent position of the SAME child, and the child was
                        # missing from the output. Emma reviews cases one by one,
                        # so a row she cannot verify is not a case.
                        corr[ours_id] = (theirs[0], key,
                                         names.get(ours_id, ""),
                                         label_of(ents.get(theirs[0])) or "",
                                         cur, ourqid.get(cur, ""),
                                         names.get(cur, ""))
                    else:
                        tally["AMBIGUOUS"] += 1
                elif ours_id:
                    tally["GENI ONLY"] += 1
                    if not ourqid.get(ours_id):
                        placeholders[ours_id] = (names.get(ours_id, ""), key, cur)
                else:
                    tally["WD ONLY"] += 1
            nxt = (row.get("father") or row.get("mother") or "").strip()
            if not nxt:
                break
            cur = nxt

    # **Second store read, for the parents' own labels.**
    #
    # `need` above holds only the QIDs of people *we* already link — the anchors
    # and their linked ancestors. The QID on the other side of a correspondence
    # comes out of the anchor's `P22`/`P25` and is therefore discovered *during*
    # the walk, after the store has been read. It was never fetched, so
    # `label_of` had nothing to read and **3,526 of 3,668 rows came out with an
    # empty `wikidata_label`**.
    #
    # That is not cosmetic. Emma's method is *"the structure picks the pair; the
    # label only confirms it"* — a correspondence with no label cannot be
    # reviewed at all, which is the entire purpose of this file.
    missing = sorted({v[0] for v in corr.values()} - set(ents))
    if missing:
        print(f"reading {len(missing):,} more items for the parents' own labels")
        with wikistore.StoreReader(STORE, INDEX) as reader:
            extra = reader.entities(missing)
        print(f"{len(extra):,} of them are held")
        for g, v in list(corr.items()):
            if not v[3]:
                corr[g] = (v[0], v[1], v[2], label_of(extra.get(v[0])) or "",
                           v[4], v[5], v[6])

    labelled = sum(1 for v in corr.values() if v[3])
    print(f"{labelled:,} of {len(corr):,} correspondences carry a Wikidata label")

    c = REPO / "reports" / "structural-correspondence.csv"
    with c.open("w", encoding="utf-8", newline="") as fh:
        w = _csv.writer(fh)
        w.writerow(["geni_id", "qid", "position", "geni_name", "wikidata_label",
                    "anchor_geni_id", "anchor_qid", "anchor_name"])
        for g, v in sorted(corr.items()):
            q, pos, gn, wl, ag, aq, an = v
            w.writerow([g, q, pos, gn, wl, ag, aq, an])

    # **The label set, not just `en`.** `emission-spec.md`: `mul` is the
    # Latin-alphabet name and `en` is the same string; `ja`/`zh` are the kanji
    # name as written. Every one of these 12,260 was going out with `en` alone,
    # which is the one label a bot that clears redundant locals would remove.
    edits = [{
        "id": f"structural_placeholder:{g}",
        "type": "create_individual",
        "source": "structural merge walk",
        "subject": {"qid": None, "geni_id": g},
        "requires": [],
        # `label_sets` is authoritative and there is **no raw-name fallback**.
        # There was one — `or {"en": nm}` — and it put back exactly the strings
        # `is_placeholder_label` had just removed: `NN wife of Aun`, `Unknown
        # Wife`, `N.N. Andersdatter Skeel`, 113 of them in `en`. A filter with a
        # fallback past it filters nothing.
        "labels": label_sets.get(g, {}),
        "missing_languages": [lang for lang in REQUIRED_LANGUAGES
                              if lang not in label_sets.get(g, {})],
        "statements": [{"property": "P31", "value": "Q5", "references": []},
                       {"property": "P2600", "value": g, "references": []}],
        "found_as": pos,
        "child_geni_id": child,
    } for g, (nm, pos, child) in sorted(placeholders.items())]
    j = REPO / "reports" / "wikidata-structural-placeholders.json"
    j.write_text(_json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")

    for k, v in tally.most_common():
        print(f"  {v:>8,}  {k}")
    print(f"\nwrote {c} ({len(corr):,} correspondences)")
    print(f"wrote {j} ({len(edits):,} placeholder creations)")
    with_mul = sum(1 for e in edits if "mul" in e["labels"])
    with_cjk = sum(1 for e in edits if "ja" in e["labels"])
    bare = sum(1 for e in edits if not e["labels"])
    print(f"  {with_mul:,} carry a `mul` label, {with_cjk:,} a ja/zh one, "
          f"{bare:,} carry none at all")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", help="one Geni ID to walk from")
    ap.add_argument("--lines", type=int, default=5, help="how many lines to show")
    ap.add_argument("--depth", type=int, default=8, help="generations up")
    ap.add_argument("--all", action="store_true",
                    help="walk every anchor and write the correspondence + placeholders")
    args = ap.parse_args()

    fam, ourqid = {}, {}
    with FAMILY.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            fam[r["geni_id"]] = r
            if (r.get("qid") or "").strip():
                ourqid[r["geni_id"]] = r["qid"].strip()
    print(f"{len(fam):,} people in reports/derived-family.csv, "
          f"{len(ourqid):,} carry a QID")

    names, label_sets = {}, {}
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            names[r["geni_id"]] = (r.get("label_en") or "").strip()
            label_set = label_set_for(r)
            if label_set:
                label_sets[r["geni_id"]] = label_set

    # The NN treatment, for a person whose own name is a placeholder: `mul` is
    # `NN` or `NN <surname>` and `en` **describes** them by their nearest named
    # relative. Same file `build-placeholder-label-batch.py` emits from, joined on
    # the Geni ID, so the two batches cannot disagree about one person.
    #
    # This **overlays** rather than filling gaps. A placeholder-named person does
    # have a `label_mul` — it is `NN` — so keying on "not already present" left
    # `NN Hildesheim` sitting in `en`, which is the one placement her rule names.
    if PREVIEW.exists():
        with PREVIEW.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                gid = r["geni_id"]
                described = dict(label_sets.get(gid) or {})
                mul = (r.get("mul_label") or "").strip()
                generated = (r.get("generated_en") or "").strip()
                if mul:
                    described["mul"] = mul
                if generated:
                    described["en"] = generated
                elif is_placeholder_label(described.get("en", "")):
                    described.pop("en", None)
                if described:
                    label_sets[gid] = described

    # Anchors: people with BOTH identifiers AND a parent on our side.
    anchors = [g for g, q in ourqid.items()
               if fam[g].get("father") or fam[g].get("mother")]
    anchors.sort(key=lambda g: -(len(fam[g].get("father", ""))
                                 + len(fam[g].get("mother", ""))))
    if args.start:
        anchors = [args.start] + [a for a in anchors if a != args.start]
    print(f"{len(anchors):,} anchors hold both identifiers and a recorded parent\n")

    wanted = set()
    for g in anchors[:args.lines]:
        cur = g
        for _ in range(args.depth):
            if cur in ourqid:
                wanted.add(ourqid[cur])
            row = fam.get(cur)
            if not row:
                break
            cur = row.get("father") or row.get("mother") or ""
            if not cur:
                break

    with wikistore.StoreReader(STORE, INDEX) as reader:
        # Two passes: the anchors' own items, then the parents those name.
        ents = reader.entities(sorted(wanted))
        more = set()
        for e in ents.values():
            more.update(wd_parent(e, FATHER) + wd_parent(e, MOTHER))
        ents.update(reader.entities(sorted(more - set(ents))))

    if args.all:
        return walk_all(anchors, fam, ourqid, names, label_sets,
                        args.depth)

    tally = {"AGREE": 0, "MERGE": 0, "GENI ONLY": 0, "WD ONLY": 0}
    for n, start in enumerate(anchors[:args.lines], 1):
        print("=" * 78)
        print(f"LINE {n}: {names.get(start, '(no label)')}   geni {start}   "
              f"{ourqid.get(start, '(no qid)')}")
        print("=" * 78)
        cur = start
        for gen in range(args.depth):
            row = fam.get(cur)
            if not row:
                break
            qid = ourqid.get(cur)
            ent = ents.get(qid) if qid else None
            for prop, key, word in ((FATHER, "father", "father"),
                                    (MOTHER, "mother", "mother")):
                ours_id = (row.get(key) or "").strip()
                theirs = wd_parent(ent, prop) if ent else []
                if not ours_id and not theirs:
                    continue
                ours_qid = ourqid.get(ours_id, "")
                if ours_id and theirs:
                    if ours_qid and ours_qid in theirs:
                        verdict = "AGREE"
                    else:
                        verdict = "MERGE"
                elif ours_id:
                    verdict = "GENI ONLY"
                else:
                    verdict = "WD ONLY"
                tally[verdict] += 1
                geni_side = (f"{names.get(ours_id, '(no label)')} [{ours_id}"
                             f"{'/' + ours_qid if ours_qid else ''}]"
                             if ours_id else "-")
                wd_side = " ; ".join(
                    f"{label_of(ents.get(t)) or '(not in store)'} [{t}]"
                    for t in theirs) or "-"
                print(f"  gen {gen}  {word:<6} {verdict:<10}")
                print(f"           geni:     {geni_side}")
                print(f"           wikidata: {wd_side}")
            nxt = (row.get("father") or row.get("mother") or "").strip()
            if not nxt:
                print(f"  gen {gen}  line ends - no parent recorded on our side")
                break
            cur = nxt
        print()

    print("across these lines:", ", ".join(f"{k} {v}" for k, v in tally.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
