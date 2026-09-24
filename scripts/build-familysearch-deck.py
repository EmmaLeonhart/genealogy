"""The FamilySearch slots the zipper refuses to guess, as a deck you can answer.

    PYTHONPATH=src python scripts/build-familysearch-deck.py

    -> out/familysearch-review.html, out/familysearch-gui-data.json

Queued 2026-09-24 under *FAMILYSEARCH ZIPPERING*: *"A FamilySearch deck for
`reports/familysearch-zipper-ambiguous.tsv` ... The pick-one card is the shape (`N x 1` and
`1 x N`); `genimerge.deck` is QID-shaped, so the FamilySearch side needs its own relatives and
dates from the download."* Published as the fourth artifact beside the three decks.

**The shapes.** A slot where one side holds ONE person is a pick: the anchor is that person and
the options are the other side's unmatched. `1 x 1` is a pick with one option, which is a yes/no
by another name. `N x M` is a matching problem across two sets, not a pick -- it stays in the
census, exactly as it does for the Wikidata pick-one deck.

**Verdicts go into `reports/emma-judgments.tsv` with the FamilySearch id in the `qid` column**,
and `zipper-join.py --familysearch` reads the `SAME` ones back as anchors. A pair already
judged never comes back (`deck.answered_pairs`), so the deck shrinks as it is worked.

The FamilySearch side is read from the raw downloads through `zipper-join.load_familysearch`,
the same reader the zipper uses -- keyed on `_FSFTID`, never on a file's own counter.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge import deck                                              # noqa: E402

ROOT = deck.ROOT
AMBIGUOUS = ROOT / "reports" / "familysearch-zipper-ambiguous.tsv"
OUT_JSON = ROOT / "out" / "familysearch-gui-data.json"
OUT_HTML = ROOT / "out" / "familysearch-review.html"

_spec = importlib.util.spec_from_file_location(
    "zipper_join", ROOT / "scripts" / "zipper-join.py")
zipper = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(zipper)


def ids(cell):
    return [x for x in (cell or "").split(";") if x]


def main() -> int:
    theirs, fs_name, fs_year, fs_sex = zipper.load_familysearch()
    fs_name = {k: " ".join(v.split()) for k, v in fs_name.items()}
    fathers, mothers, children, spouses = deck.load_our_family()
    labels = deck.load_our_labels()
    our_sex, our_life = deck.load_our_facts()
    answered, _unsure = deck.answered_pairs()

    def our_names(gs):
        return [(labels.get(g) or g) for g in gs]

    def fs_names(fs):
        return [fs_name.get(x, x) for x in fs]

    def fs_rel(fs, prop):
        return [x for x in (theirs.get(fs, {}).get(prop) or "").split(" | ") if x]

    def our_block(g, parent):
        return {"name": (labels.get(g) or g), "id": g, "kind": "geni",
                "sex": our_sex.get(g, ""), "life": list(our_life.get(g, ("", ""))),
                "fields": [["Parents", our_names(fathers.get(g, []) + mothers.get(g, []))],
                           ["Siblings", our_names([k for k in children.get(parent, ())
                                                   if k != g])],
                           ["Spouse", our_names(spouses.get(g, ()))],
                           ["Children", our_names(children.get(g, ()))]]}

    def fs_block(fs, parent):
        return {"name": fs_name.get(fs, fs), "id": fs, "kind": "fs",
                "sex": fs_sex.get(fs, ""), "life": [str(fs_year.get(fs, "")), ""],
                "fields": [["Parents", fs_names(fs_rel(fs, "p22") + fs_rel(fs, "p25"))],
                           ["Siblings", fs_names([k for k in fs_rel(parent, "p40")
                                                  if k != fs])],
                           ["Spouse", fs_names(fs_rel(fs, "p26"))],
                           ["Children", fs_names(fs_rel(fs, "p40"))]]}

    cases, seen, shapes = [], set(), {"NxM": 0, "answered": 0, "repeat": 0}
    with io.open(AMBIGUOUS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            ours, fss = ids(r["ours_unmatched"]), ids(r["theirs_unmatched"])
            if len(ours) > 1 and len(fss) > 1:
                shapes["NxM"] += 1
                continue
            # The same slot is reached from the father AND the mother; one card, not two.
            key = (r["slot"], frozenset(ours), frozenset(fss))
            if key in seen:
                shapes["repeat"] += 1
                continue
            seen.add(key)
            if len(ours) == 1:
                g = ours[0]
                open_ = [f for f in fss if (g, f) not in answered]
                if not open_:
                    shapes["answered"] += 1
                    continue
                anchor = our_block(g, r["from_geni"])
                options = [dict(fs_block(f, r["from_fs_id"]), geni=g, qid=f,
                                our=anchor["name"], cand=fs_name.get(f, f)) for f in open_]
                side, ask = "theirs", "Which of these FamilySearch people is our person?"
            else:
                f = fss[0]
                open_ = [g for g in ours if (g, f) not in answered]
                if not open_:
                    shapes["answered"] += 1
                    continue
                anchor = fs_block(f, r["from_fs_id"])
                options = [dict(our_block(g, r["from_geni"]), geni=g, qid=f,
                                our=(labels.get(g) or g), cand=anchor["name"]) for g in open_]
                side, ask = "ours", "Which of these is the FamilySearch person?"
            # A known sex that contradicts the anchor's is not a candidate -- the zipper's own
            # refuter would drop that pair, so offering it is a question with one answer.
            want = anchor["sex"]
            options = [o for o in options if not (want and o["sex"] and o["sex"] != want)]
            if not options:
                shapes["answered"] += 1
                continue
            words = set()
            for _, vals in anchor["fields"]:
                words |= deck.words(vals)
            shared = set()
            for o in options:
                for _, vals in o["fields"]:
                    shared |= words & deck.words(vals)
            cases.append({
                "kind": "pick",
                "id": "fs|%s|%s|%s|%s" % (r["slot"], r["from_geni"], anchor["id"], side),
                "side": side, "slot": r["slot"], "ask": ask,
                "anchor": anchor, "options": options,
                "trigger_pre": "held because the zipper reached this %s slot from " % r["slot"],
                "trigger_bold": (labels.get(r["from_geni"]) or r["from_geni"]),
                "trigger_post": " and could not tell who is who",
                "highlight": sorted(shared),
                "our": options[0]["our"], "cand": options[0]["cand"],
            })

    out = deck.render(cases, OUT_HTML, OUT_JSON,
                      title="FamilySearch Zipper",
                      sub="The zipper walked into this family slot from both sides and could "
                          "not tell who is who. Which one is it?",
                      key="familysearch-v1")
    print("%d cards in the deck -> %s; %d N x M slots stay in the census, %d answered or "
          "left with no option of the right sex, %d repeats of one slot"
          % (len(out), OUT_HTML.relative_to(ROOT), shapes["NxM"], shapes["answered"],
             shapes["repeat"]))
    if cases and not out:
        print("BROKEN DECK: %d cards and nothing reached the deck" % len(cases), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
