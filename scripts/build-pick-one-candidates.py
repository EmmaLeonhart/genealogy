"""The AMBIGUOUS family slots, as a card you can actually answer.

    PYTHONPATH=src python scripts/build-pick-one-candidates.py

    -> reports/pick-one-candidates.tsv   every open slot, one row per option -- the census
    -> out/pick-one-gui-data.json        the deck
    -> out/pick-one-review.html          the deck rendered, which is what you open

Published, UNLINKED, at <https://emmaleonhart.github.io/genealogy/pick-one-review.html>.

## What this is for

`scripts/build-family-candidates.py` only offers a slot where BOTH sides hold exactly one person
of that sex, because a Same/Different card can say nothing else. **12,125 slots hold more** --
8,207 child and 3,918 sibling -- and its own docstring names them as the next thing to build a
card for: *"a 3x1 slot asks which of our three is this item?, which the Same/Different card
cannot express; offering it as three yes/no cards invites three Sames."*

This is that card. The slot is the same unit -- one parent, one sex -- and the only difference is
the shape of the question:

    N x 1   Wikidata names one person nothing accounts for, and we hold N of that sex.
            -> "which of our N is this item?"        the anchor is the ITEM.
    1 x N   we hold one unclaimed person, and Wikidata names N.
            -> "which of these items is our person?" the anchor is OUR PERSON.

**A slot where both sides hold several is NOT offered.** That is a matching problem across two
sets, not a single pick, and forcing it into this card would invite the same over-assertion the
yes/no card invites on 3x1. Those stay in the census, counted in the run's output.

## WHAT A PICK MEANS, and why the losers get a verdict

Picking is not a softer `SAME`. The slot has ONE answer by construction -- one item, one of our
people -- so saying *this one* also says *not those*. So:

    pick X          -> X gets SAME, and every other option in that slot gets DIFFERENT
    None of these   -> every option gets DIFFERENT
    Skip            -> nothing is written, and the slot comes back

**Without the losers' `DIFFERENT` rows the deck could never shrink.** `deck.answered_pairs()`
retires a `(geni_id, qid)` pair, so a card that recorded only the winner would re-offer the same
N-1 people against the same item on every rebuild, forever. This is the reading taken rather
than asked -- `CLAUDE.md` section *Working the queue: GUESS. Do not ask* -- and what would
falsify it is you saying a pick means only *this one is right* and not *those are wrong*, in
which case the losers' rows come out and the card needs a separate retire mechanism.

`Skip` is the escape and it is why `None of these` can be strict: *I cannot tell* has its own
button and writes nothing, per `deck.answered_pairs()`'s rule that an `UNSURE` comes back.

## The export format does not change

Five columns, exactly what the *Copy decisions* button already produces on both other decks --
`geni_id, our_name, qid, their_name, verdict` -- so the paste-back into
`reports/emma-judgments.tsv` is unchanged. One pick card simply emits N rows instead of one.
"""

import collections
import csv
import io
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge import deck                                              # noqa: E402

ROOT = deck.ROOT
OUT_TSV = ROOT / "reports" / "pick-one-candidates.tsv"
OUT_JSON = ROOT / "out" / "pick-one-gui-data.json"
OUT_HTML = ROOT / "out" / "pick-one-review.html"

#: Our own structural placeholders -- `CLAUDE.md` section *A sibling step gets a PLACEHOLDER
#: PARENT in our tree and NEVER on Wikidata*. They stand for a person nobody has evidence for.
PLACEHOLDER = ("9995", "9990")

#: A slot with more options than this is not a card anybody can read, and a pick among thirty
#: siblings is not a judgement you can make from a phone. They stay in the census.
MAX_OPTIONS = 8

#: **How many cards reach the PAGE.** The census is whole and this is not a filter on it -- it
#: is the size of the deck you open.
#:
#: Measured 2026-09-09: the full 6,762 cards render to a **16.9 MB** page, against the family
#: deck's 819 KB for 898 cards. A pick card is ~2.5 KB because it carries an anchor plus up to
#: eight option blocks with four relative lists each, so the page grows twice as fast per card
#: as the other decks do. 16.9 MB is not a page anybody opens on mobile data.
#:
#: So it is a rolling window, the same shape as `LABEL_EDIT_CAP` and `NAME_ADD_CAP`: what does
#: not fit today goes out tomorrow, because the deck retires what you have answered on every
#: rebuild -- `CLAUDE.md` section *The batches are a SEQUENCE*. The ordering below is
#: most-evidence-first, so the window holds the cards that can actually be settled.
#:
#: **This number is a GUESS taken rather than asked** -- `CLAUDE.md` section *Working the queue:
#: GUESS. Do not ask* -- and what would falsify it is you wanting the whole deck in one page.
#: It is one constant, it costs a rebuild to move, and the run prints what it held back.
DECK_CAP = 1000


def main():
    rel, geni_of = deck.load_relations(("p22", "p25", "p40", "p26", "p3373"))
    kids_of, sp_of, sib_of = rel["p40"], rel["p26"], rel["p3373"]
    father_of, mother_of = rel["p22"], rel["p25"]
    qid_of = {g: q for q, g in geni_of.items()}
    claimed = set(geni_of)
    print("%s items carry a P2600; %s carry a P3373 sibling"
          % (format(len(geni_of), ","), format(len(sib_of), ",")), file=sys.stderr)

    known_qid, known_geni, syn_qid = deck.load_correspondence()
    claimed |= known_qid

    def q_of(g):
        return qid_of.get(g) or syn_qid.get(g)

    def spoken_for(g):
        return g in qid_of or g in known_geni or g.startswith(PLACEHOLDER)

    our_fathers, our_mothers, our_children, our_spouses = deck.load_our_family()
    labels = deck.load_our_labels()
    answered, unsure = deck.answered_pairs()
    print("%s pairs decided; %d UNSURE, which stay in the deck"
          % (format(len(answered), ","), unsure), file=sys.stderr)

    wd_sex = deck.load_wikidata_sex()
    our_sex, our_life = deck.load_our_facts()

    # ---- the same walk build-family-candidates.py does, keeping the OTHER shapes -----
    slots, shapes = [], collections.Counter()
    for parent, kids in our_children.items():
        ours = [k for k in kids if not spoken_for(k)]
        if not ours:
            continue

        arms = []
        pq = q_of(parent)
        if pq:
            loose = [k for k in kids_of.get(pq, ()) if k not in claimed]
            if loose:
                arms.append(("child", loose, {}))
        sib_loose, sib_via = [], {}
        for k in kids:
            kq = q_of(k)
            if not kq:
                continue
            for q in sib_of.get(kq, ()):
                if q not in claimed and q not in sib_via:
                    sib_via[q] = k
                    sib_loose.append(q)
        if sib_loose:
            arms.append(("sibling", sib_loose, sib_via))

        for arm, loose, via_of in arms:
            for sex in ("M", "F"):
                mine = [g for g in ours if our_sex.get(g) == sex]
                theirs = [q for q in loose if wd_sex.get(q) == sex]
                if not mine or not theirs:
                    continue
                shapes[(arm, min(len(mine), 9), min(len(theirs), 9))] += 1
                if len(mine) == 1 and len(theirs) == 1:
                    continue                      # build-family-candidates.py's population
                if len(mine) > 1 and len(theirs) > 1:
                    continue                      # a matching problem, not a pick
                slots.append((arm, parent, sex, mine, theirs, via_of))

    one = sum(v for k, v in shapes.items() if k[1] == 1 and k[2] == 1)
    n_by_1 = sum(v for k, v in shapes.items() if k[1] > 1 and k[2] == 1)
    one_by_n = sum(v for k, v in shapes.items() if k[1] == 1 and k[2] > 1)
    many = sum(v for k, v in shapes.items() if k[1] > 1 and k[2] > 1)
    print("slots: %s answerable 1x1 (the other deck), %s Nx1, %s 1xN, %s many-to-many (held)"
          % tuple(format(x, ",") for x in (one, n_by_1, one_by_n, many)), file=sys.stderr)

    # ---- one card per slot, dropping options you have already ruled on ----------------
    cards, oversize, exhausted = [], 0, 0
    for arm, parent, sex, mine, theirs, via_of in slots:
        if len(mine) == 1:
            opts = [(mine[0], q) for q in theirs]
            side = "theirs"
        else:
            opts = [(g, theirs[0]) for g in mine]
            side = "ours"
        opts = [p for p in opts if p not in answered]
        if not opts:
            exhausted += 1
            continue
        if len(opts) > MAX_OPTIONS:
            oversize += 1
            continue
        via = via_of.get(opts[0][1]) if arm == "sibling" else parent
        cards.append({"arm": arm, "parent": parent, "sex": sex, "side": side,
                      "opts": opts, "via": via})

    print("%s cards; %s slots already fully ruled on, %s wider than %d options and held"
          % (format(len(cards), ","), format(exhausted, ","), format(oversize, ","),
             MAX_OPTIONS), file=sys.stderr)

    # ---- names -----------------------------------------------------------------------
    label_ids, chip_ids = set(), set()
    for card in cards:
        for _, q in card["opts"]:
            chip_ids.add(q)
            label_ids.add(q)
            for src in (kids_of, sp_of, sib_of, father_of, mother_of):
                label_ids |= set(src.get(q, ()))
    wd_label, cand_sex, cand_life, gone = deck.wikidata_facts(label_ids, chip_ids)

    def ours_named(ids):
        return [labels.get(x) or x for x in ids]

    def theirs_named(ids):
        return [wd_label.get(x, x) for x in ids]

    def our_name(g):
        # `g` can be a MULTI-VALUED cell -- a merged person carries every id they were merged
        # from -- so fall back to the first id that actually resolves.
        return labels.get(g) or next(
            (labels[t] for t in (x.strip() for x in str(g).split(deck.FAMILY_SEP))
             if labels.get(t)), "")

    def our_block(g, parent):
        return {"name": our_name(g), "id": g, "kind": "geni",
                "sex": our_sex.get(g, ""), "life": our_life.get(g, ("", "")),
                "fields": [["Parents", ours_named(our_fathers.get(g, [])
                                                  + our_mothers.get(g, []))],
                           ["Siblings", ours_named([k for k in our_children.get(parent, ())
                                                    if k != g])],
                           ["Spouse", ours_named(our_spouses.get(g, ()))],
                           ["Children", ours_named(our_children.get(g, ()))]]}

    def their_block(q):
        return {"name": wd_label.get(q, q), "id": q, "kind": "qid",
                "sex": cand_sex.get(q, ""), "life": cand_life.get(q, ("", "")),
                "gone": q in gone,
                "fields": [["Parents", theirs_named(father_of.get(q, [])
                                                    + mother_of.get(q, []))],
                           ["Siblings", theirs_named(sib_of.get(q, []))],
                           ["Spouse", theirs_named(sp_of.get(q, []))],
                           ["Children", theirs_named(kids_of.get(q, []))]]}

    cases = []
    for card in cards:
        opts, parent = card["opts"], card["parent"]
        if card["side"] == "ours":
            anchor = their_block(opts[0][1])
            options = [dict(our_block(g, parent), geni=g, qid=q,
                            our=our_name(g), cand=anchor["name"]) for g, q in opts]
            ask = "Which of these is the item?"
        else:
            anchor = our_block(opts[0][0], parent)
            options = [dict(their_block(q), geni=g, qid=q,
                            our=anchor["name"], cand=wd_label.get(q, q)) for g, q in opts]
            ask = "Which of these items is our person?"

        if card["arm"] == "child":
            trigger = ("held because their parent ", our_name(parent) or parent,
                       " holds an item whose child list names more people than we can place")
        else:
            trigger = ("held because their sibling ", our_name(card["via"]) or card["via"],
                       " holds an item naming siblings we cannot place one-to-one")

        # Shared words are an aid to READING and never a decision -- `CLAUDE.md` no-name
        # similarity. Computed against the anchor so every option is highlighted the same way.
        anchor_words = set()
        for _, vals in anchor["fields"]:
            anchor_words |= deck.words(vals)
        shared = set()
        for opt in options:
            for _, vals in opt["fields"]:
                shared |= anchor_words & deck.words(vals)

        cases.append({
            "kind": "pick",
            "id": "%s|%s|%s|%s" % (card["arm"], parent, card["sex"], card["side"]),
            "side": card["side"],
            "slot": card["arm"],
            "ask": ask,
            "anchor": anchor,
            "options": options,
            "trigger_pre": trigger[0], "trigger_bold": trigger[1], "trigger_post": trigger[2],
            "highlight": sorted(shared),
            # Top-level `our`/`cand` exist so `deck.render`'s CJK holdout sees something; they
            # name the anchor, which is what the card is about.
            "our": anchor["name"] if card["side"] == "theirs" else options[0]["our"],
            "cand": anchor["name"] if card["side"] == "ours" else options[0]["cand"],
        })

    # ---- the census ------------------------------------------------------------------
    with io.open(OUT_TSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["card_id", "slot", "side", "sex", "options", "geni_id", "our_name",
                    "qid", "candidate_name"])
        for c in cases:
            for opt in c["options"]:
                w.writerow([c["id"], c["slot"], c["side"], opt.get("sex", ""),
                            len(c["options"]), opt["geni"], opt["our"], opt["qid"],
                            opt["cand"]])

    # **An option with no name on OUR side is data, not a bug** -- Geni redacts. A bare QID on
    # the Wikidata side is the label lookup having failed, and that still fails the run.
    def unnamed(opt):
        our, cand = (opt["our"] or "").strip(), (opt["cand"] or "").strip()
        return not our or not cand or bool(re.fullmatch(r"Q\d+", cand))

    ready, dropped_opts, dropped_cards = [], 0, 0
    for c in cases:
        keep = [o for o in c["options"] if not unnamed(o)]
        dropped_opts += len(c["options"]) - len(keep)
        if not keep or not (c["anchor"]["name"] or "").strip() \
                or re.fullmatch(r"Q\d+", c["anchor"]["name"].strip()):
            dropped_cards += 1
            continue
        c["options"] = keep
        ready.append(c)
    if dropped_opts or dropped_cards:
        print("%s options and %s whole cards dropped: no name to judge on one side"
              % (format(dropped_opts, ","), format(dropped_cards, ",")), file=sys.stderr)

    # **Most evidence first.** A card whose sides share names is one you can settle in a glance;
    # one with nothing on either side is one nobody can. This orders the deck; it judges nothing.
    ready.sort(key=lambda c: (len(c["highlight"]),
                              sum(len(f[1]) for f in c["anchor"]["fields"]),
                              -len(c["options"])), reverse=True)

    # **Hold the CJK cards out BEFORE the window, not after.** `deck.render` does it either way,
    # but doing it after spends window slots on cards that are then dropped -- the first run
    # published 995 of a 1000-card window for that reason. Your ruling of 2026-09-07 is that a
    # CJK case is undoable from where you are, so it is never what a slot should hold.
    ready = [c for c in ready
             if not any(deck.has_cjk(n) for n in deck.card_names(c))]

    windowed = len(ready) - DECK_CAP
    if windowed > 0:
        print("%s cards held for a later rebuild; %d reach the page. See DECK_CAP."
              % (format(windowed, ","), DECK_CAP), file=sys.stderr)
        ready = ready[:DECK_CAP]

    out = deck.render(ready, OUT_HTML, OUT_JSON,
                      title="Pick One",
                      sub="One side of this family slot names somebody we cannot place. "
                          "Which of the others is it?",
                      key="pick-one-v1")

    rows = sum(len(c["options"]) for c in cases)
    print("%s cards over %s options -> %s" % (format(len(cases), ","), format(rows, ","),
                                              OUT_TSV.relative_to(ROOT)))
    print("%s in the deck -> %s, %s" % (format(len(out), ","), OUT_JSON.relative_to(ROOT),
                                        OUT_HTML.relative_to(ROOT)))
    by = collections.Counter((c["slot"], c["side"]) for c in out)
    for k in sorted(by):
        print("   %-8s anchored on %-6s %s" % (k[0], k[1], format(by[k], ",")))

    # An empty deck beside a non-empty census is a join that matched nothing, which is
    # indistinguishable from an absence of data -- `CLAUDE.md` section *A CARD THAT NAMES
    # NOBODY IS THE TELL*.
    if cases and not out:
        print("BROKEN DECK: %s cards and nothing reached the deck" % format(len(cases), ","),
              file=sys.stderr)
        return 1
    if cases and dropped_cards > len(cases) // 2:
        print("BROKEN DECK: %s of %s cards had no name -- that is the lookup failing, not the "
              "data. See CLAUDE.md section THE PARENT DECK."
              % (format(dropped_cards, ","), format(len(cases), ",")), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
