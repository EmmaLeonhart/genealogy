"""The CHILD and SIBLING half of the manual zipper, as a deck to answer by hand.

**More manual zipper merging, now on siblings and children**, the parents being mostly worked
through.

    python scripts/pack-derived.py --unpack     # clean clone only; the derived CSVs are gitignored
    PYTHONPATH=src python scripts/build-family-candidates.py

    -> reports/family-candidates.tsv    every open case, one row -- the census
    -> out/family-gui-data.json         the deck
    -> out/family-review.html           the deck rendered, which is what gets opened

Published, UNLINKED, at <https://emmaleonhart.github.io/genealogy/family-review.html>.

## The two arms, and why the second one is not the first one in disguise

`scripts/build-parent-candidates.py` asks *is our person the PARENT their child already names?*
These ask the mirror question one slot down:

* **child** --- a parent of our person holds a QID, and that item's `P40` names a child nothing
  accounts for. **This is the duplicate guard's own first arm**, the one that caught
  `Q2183430` *Benedicta Ebbesdotter of Hvide* being created a second time: `CLAUDE.md`
  § *THE DUPLICATE GUARD*, *"the duplicate was sitting in a list the batch already had a QID
  for"*. It has held people back ever since and nothing ever put the question up to be
  answered.
* **sibling** --- a sibling of our person holds a QID, and that item's `P3373` names a sibling
  nothing accounts for.

**The sibling arm reaches families the child arm cannot, and that is the whole reason it
exists.** It does not need the *parent* to have an item; it needs a *sibling* to have one. Geni
records no sibling edge at all --- `CLAUDE.md` § *A sibling step is the worked example* --- so
two of our siblings are joined only through a shared parent, and a Wikidata item that states
`P3373` directly is saying something our tree structurally cannot.

`P3373` had no column in `out/wikidata/relations.tsv` until 2026-09-09, which is why nothing
could use it. 155,456 items carry it, 418,004 statements.

## ⛔ A CARD IS ONLY OFFERED WHERE THE SLOT HAS ONE ANSWER

The unit is the **slot**, exactly as in `scripts/zipper-join.py`: one parent, one sex, our
unclaimed children of that sex against Wikidata's unaccounted ones. A card is emitted only where
both sides hold **exactly one**.

**Sex splits the slot and it is not decoration.** `scripts/census-solo-children.py` measured
`P21` refuting **10.0%** of solo-child pairs, against 0.0% for solo father and mother slots ---
so a 2x2 slot that is one son and one daughter on each side is two answerable questions, while
a 2x2 of two sons is not one. It takes the deck from 1,466 slots to 3,507 pairs.

**Everything else stays in the census and out of the deck.** A `3x1` slot asks *which of our
three is this item?*, which the Same/Different card cannot express; offering it as three yes/no
cards invites three Sames. Those shapes are counted in the run's output and are the next thing
to build a card for, not something to smuggle through this one.

## What the card carries

Parents, siblings, spouses and children on **both** sides: a card carrying no relationships
cannot be judged at all. For these two arms the
siblings are the discriminating list --- the slot is a sibship, and whether the two sides line up
is what settles it.

Shared words between the sides are highlighted. They are an aid to reading and never a decision;
`CLAUDE.md` no-name-similarity governs and nothing here proposes anything. In 1600-1900 they will
often disagree on a real pair --- § *1600-1900 is the band where NAMES LIE and YEARS decide*,
71% of the hand-confirmed pairs spell the name differently --- which is why sex and years are on
the card and the names are not the evidence.

Verdicts come back through *Copy decisions* and go into `reports/emma-judgments.tsv` with
`batch` = `family-adjudication-gui`. `SAME` and `DIFFERENT` retire a pair; `UNSURE` comes back.
"""

import collections
import csv
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge import deck                                              # noqa: E402

ROOT = deck.ROOT
OUT_TSV = ROOT / "reports" / "family-candidates.tsv"
OUT_JSON = ROOT / "out" / "family-gui-data.json"
OUT_HTML = ROOT / "out" / "family-review.html"

#: Our own structural placeholders -- `CLAUDE.md` § *A sibling step gets a PLACEHOLDER PARENT in
#: our tree and NEVER on Wikidata*. They stand for a person nobody has evidence for, so they are
#: never offered as an identification.
PLACEHOLDER = ("9995", "9990")


def main():
    rel, geni_of = deck.load_relations(("p22", "p25", "p40", "p26", "p3373"))
    kids_of, sp_of, sib_of = rel["p40"], rel["p26"], rel["p3373"]
    father_of, mother_of = rel["p22"], rel["p25"]
    qid_of = {g: q for q, g in geni_of.items()}
    claimed = set(geni_of)
    print("%s items carry a P2600; %s carry a P3373 sibling"
          % (format(len(geni_of), ","), format(len(sib_of), ",")), file=sys.stderr)
    if not sib_of:
        print("no p3373 column in out/wikidata/relations.tsv -- the sibling arm will find "
              "nothing. Re-run scripts/extract-wikidata-relations.py.", file=sys.stderr)

    known_qid, known_geni, syn_qid = deck.load_correspondence()
    claimed |= known_qid
    print("%s items and %s profiles already identified somewhere"
          % (format(len(known_qid), ","), format(len(known_geni), ",")), file=sys.stderr)

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
    print("%s of our people have a recorded sex; %s Wikidata items do"
          % (format(len(our_sex), ","), format(len(wd_sex), ",")), file=sys.stderr)

    # ---- walk every sibship in our tree ---------------------------------------------
    # The slot is (parent, sex) for both arms: what differs is where Wikidata's side of it comes
    # from -- the parent's own child list, or a sibling's sibling list.
    pairs, shapes = [], collections.Counter()
    for parent, kids in our_children.items():
        ours = [k for k in kids if not spoken_for(k)]
        if not ours:
            continue

        arms = []
        pq = q_of(parent)
        if pq:
            loose = [k for k in kids_of.get(pq, ()) if k not in claimed]
            if loose:
                arms.append(("child", pq, loose))
        # Every sibling of theirs that holds an item, and what that item says its siblings are.
        # An item already spoken for is not a candidate, which also removes the siblings we
        # ourselves supplied.
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
            arms.append(("sibling", None, sib_loose))

        for arm, anchor, loose in arms:
            for sex in ("M", "F"):
                mine = [g for g in ours if our_sex.get(g) == sex]
                theirs = [q for q in loose if wd_sex.get(q) == sex]
                shapes[(arm, min(len(mine), 9), min(len(theirs), 9))] += 1
                if len(mine) != 1 or len(theirs) != 1:
                    continue
                g, q = mine[0], theirs[0]
                if (g, q) in answered:
                    continue
                via = sib_via[q] if arm == "sibling" else parent
                pairs.append((g, q, arm, parent, via, sex))

    print("%s (person, item) proposals across both arms" % format(len(pairs), ","),
          file=sys.stderr)
    for arm in ("child", "sibling"):
        got = [k for k in shapes if k[0] == arm]
        one = sum(shapes[k] for k in got if k[1] == 1 and k[2] == 1)
        many = sum(shapes[k] for k in got if k[1] and k[2] and not (k[1] == 1 and k[2] == 1))
        print("  %-8s slots: %s answerable (1x1), %s ambiguous and held back in the census"
              % (arm, format(one, ","), format(many, ",")), file=sys.stderr)

    # One question per person, the child arm first -- a parent's own child list is the more
    # reliable of the two (`CLAUDE.md` § *Link reliability order*), and a person offered the same
    # item by both arms should be asked once.
    pairs.sort(key=lambda t: (t[0], t[2] != "child"))
    seen, unique = set(), []
    for g, q, arm, parent, via, sex in pairs:
        if g in seen:
            continue
        seen.add(g)
        unique.append((g, q, arm, parent, via, sex))
    print("%s after one question per person" % format(len(unique), ","), file=sys.stderr)

    # ---- names and chips -------------------------------------------------------------
    label_ids, chip_ids = set(), set()
    for _, q, _, _, _, _ in unique:
        chip_ids.add(q)
        label_ids.add(q)
        for src in (kids_of, sp_of, sib_of, father_of, mother_of):
            label_ids |= set(src.get(q, ()))
    wd_label, cand_sex, cand_life, gone = deck.wikidata_facts(label_ids, chip_ids)

    def ours_named(ids):
        return [labels.get(x, x) for x in ids]

    def theirs_named(ids):
        return [wd_label.get(x, x) for x in ids]

    cases = []
    for g, q, arm, parent, via, sex in unique:
        our_par = ours_named([x for x in our_fathers.get(g, []) + our_mothers.get(g, [])])
        our_sib = ours_named([k for k in our_children.get(parent, ()) if k != g])
        our_sp = ours_named(our_spouses.get(g, ()))
        our_kids = ours_named(our_children.get(g, ()))
        cand_par = theirs_named(father_of.get(q, []) + mother_of.get(q, []))
        cand_sib = theirs_named(sib_of.get(q, []))
        cand_sp = theirs_named(sp_of.get(q, []))
        cand_kids = theirs_named(kids_of.get(q, []))
        shared = sorted((deck.words(our_sib) & deck.words(cand_sib))
                        | (deck.words(our_par) & deck.words(cand_par))
                        | (deck.words(our_sp) & deck.words(cand_sp))
                        | (deck.words(our_kids) & deck.words(cand_kids)))
        # **`labels.get(x, x)` is not the same as `labels.get(x) or x`**, and the difference
        # shows on the card: a redacted relative HAS a row in `derived-labels.csv` with an empty
        # label, so the first form returns `""` and the trigger reads *"held because their
        # sibling  holds an item"*. Fall back to the id, which at least names the profile.
        if arm == "child":
            pre, bold = "held because their parent ", labels.get(parent) or parent
            post = " holds an item whose child list names somebody nothing accounts for"
        else:
            pre, bold = "held because their sibling ", labels.get(via) or via
            post = " holds an item that names a sibling nothing accounts for"
        cases.append({
            # `g` can itself be a MULTI-VALUED cell -- a merged person carries every id they were
            # merged from -- so take the first id that actually resolves.
            "our": labels.get(g) or next(
                (labels[t] for t in (x.strip() for x in str(g).split(deck.FAMILY_SEP))
                 if labels.get(t)), ""),
            "geni": g,
            "qid": q,
            "cand": wd_label.get(q, q),
            "slot": arm,
            "via": labels.get(via) or via,
            "trigger_pre": pre,
            "trigger_bold": bold,
            "trigger_post": post,
            "our_fields": [["Parents", our_par], ["Siblings", our_sib],
                           ["Spouse", our_sp], ["Children", our_kids]],
            "cand_fields": [["Parents", cand_par], ["Siblings", cand_sib],
                            ["Spouse", cand_sp], ["Children", cand_kids]],
            "highlight": shared,
            "shared": shared,
            "our_sex": our_sex.get(g, ""),
            "cand_sex": cand_sex.get(q, sex),
            "gone": q in gone,
            "our_life": our_life.get(g, ("", "")),
            "cand_life": cand_life.get(q, ("", "")),
        })

    with io.open(OUT_TSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["geni_id", "our_name", "qid", "candidate_name", "slot", "via",
                    "sex", "shared_words"])
        for c in cases:
            w.writerow([c["geni"], c["our"], c["qid"], c["cand"], c["slot"], c["via"],
                        c["our_sex"], " ".join(c["shared"])])

    deck.mark_also_offered(cases)

    # **A card with no name on OUR side is data, not a bug.** Geni redacts, so `Private` and the
    # unnamed come through with an empty label, and an empty box cannot be judged against a name.
    # Those are dropped from the deck and counted. A bare QID on the WIKIDATA side is the other
    # thing entirely -- that is the label lookup having failed -- and it still fails the run.
    unnamed = [c for c in cases if not (c.get("our") or "").strip()]
    if unnamed:
        print("%s cards dropped: Geni records no name on our side, so there is nothing to judge"
              % format(len(unnamed), ","), file=sys.stderr)
    ready = [c for c in cases if c not in unnamed]
    # **And a bare QID on the Wikidata side is the INSTRUMENT failing, not the data.** It is
    # unanswerable either way, so the card goes; what changes is that a systematic failure --
    # the label file absent, the store excluded and the API refused all at once -- must not
    # quietly produce a small deck. `unresolved` over half the census IS that failure, and the
    # run ends non-zero below rather than publishing it.
    unresolved = deck.nameless(ready)
    if unresolved:
        print("%s cards dropped: the Wikidata name did not resolve, so the card would face a "
              "bare QID" % format(len(unresolved), ","), file=sys.stderr)
        ready = [c for c in ready if c not in unresolved]

    # **Most evidence first.** A case with names in common across the two sibships settles in a
    # glance; a case with nothing on either side settles for nobody, and leading with
    # those is how a deck stops being worked. This orders the deck; it judges nothing.
    ready.sort(key=lambda c: (len(c["shared"]),
                              sum(len(f[1]) for f in c["cand_fields"]),
                              sum(len(f[1]) for f in c["our_fields"])), reverse=True)
    out = deck.render(ready, OUT_HTML, OUT_JSON,
                      title="Family Adjudication",
                      sub="Is our Geni person the same as the child or sibling their family "
                          "already names on Wikidata?",
                      key="family-adjudication-v1")

    print("%s candidates -> %s" % (format(len(cases), ","), OUT_TSV.relative_to(ROOT)))
    print("%s in the deck -> %s, %s" % (format(len(out), ","), OUT_JSON.relative_to(ROOT),
                                        OUT_HTML.relative_to(ROOT)))
    by_slot = collections.Counter(c["slot"] for c in out)
    print("   %s from the child arm, %s from the sibling arm"
          % (format(by_slot["child"], ","), format(by_slot["sibling"], ",")))

    # **A CARD THAT NAMES NOBODY IS THE TELL, and a count never showed it.** Three separate bugs
    # each published a parent deck whose cards were a name facing an empty box or a bare QID,
    # while the generator printed a healthy candidate count every run.
    if len(unresolved) > len(cases) // 2:
        print("BROKEN DECK: %s of %s cards had no Wikidata name -- that is the lookup failing, "
              "not the data. See CLAUDE.md section THE PARENT DECK."
              % (format(len(unresolved), ","), format(len(cases), ",")), file=sys.stderr)
        return 1
    bad = deck.nameless(out)
    if bad:
        print("BROKEN DECK: %d of %d cards name nobody on one side -- e.g. %s. See CLAUDE.md"
              " section THE PARENT DECK."
              % (len(bad), len(out), ", ".join(sorted(c["qid"] for c in bad)[:5])),
              file=sys.stderr)
        return 1
    # An empty deck beside a non-empty census is the shape of a join that matched nothing, which
    # is indistinguishable from an absence of data. Say so rather than publishing a blank page.
    if cases and not out:
        print("BROKEN DECK: %s candidates and nothing reached the deck" % format(len(cases), ","),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
