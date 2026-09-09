"""The parent identifications the duplicate guard is sitting on, as a file she can answer.

THE RUNBOOK --- this is the deck Emma means by *"the artifact we used for identifying parents"*,
and it is regenerated on demand rather than served from the last commit:

    python scripts/pack-derived.py --unpack     # clean clone only; the derived CSVs are gitignored
    PYTHONPATH=src python scripts/build-parent-candidates.py

    -> reports/parent-candidates.tsv   one row per open case
    -> out/gui-data.json               the deck
    -> out/parent-review.html          the deck rendered, which is what she opens

It is published, UNLINKED, at
<https://emmaleonhart.github.io/genealogy/parent-review.html> --- `scripts/build-pages-site.py`
copies the HTML into the site.

**A session with no corpus on disk does not run this by hand.** `gh workflow run parent-deck.yml`
builds it on a runner and commits it to `main`, and that push republishes Pages.
`.github/workflows/pipeline.yml` also rebuilds the deck on every push, but it does so downstream
of a ledger refresh and a batch commit, either of which can fail and take the site job with it.

Her verdicts come back in `reports/emma-judgments.tsv`. `SAME` and `DIFFERENT` retire a case; an
`UNSURE` is *I cannot tell from this* and comes back on a later run with more evidence.

**ALWAYS REGENERATE BEFORE HANDING IT OVER.** `CLAUDE.md` § *Emma edits the tree and the items BY
HAND, continuously* --- the committed HTML is a photograph, and a card she has already answered
costs her a turn.

**The check that catches a broken build is not the count, it is the page.** Three separate bugs
published a deck of cards that named nobody while this script printed a healthy
`17 structural candidates` every time; `CLAUDE.md` § *THE PARENT DECK* has all three. If any card
shows a bare QID or an empty name box, the deck is broken, whatever the count says.

**This is the PARENT slot only.** `scripts/build-family-candidates.py` is the child and sibling
one, and every helper both of them use lives in `genimerge.deck` --- one copy, because the three
bugs above were each a helper that was right in one place and wrong in another.

**Emma, 2026-08-31:** the generator should *"actively create merge candidates like our ones that
are files for potential geni identifications related to parents"*.

**The problem this closes is delivery, not detection.** The guard already finds these: our person
is the parent of somebody whose Wikidata item names a parent nothing accounts for, so creating
them might duplicate that item. The guard refuses, prints a line, and the person falls into the
carry-forward. Nothing ever put the question in front of her.

**What makes a case answerable is the EVIDENCE, not the names.** Emma, shown a question carrying
neither: *"Fuck you no relationships means I can't make a judgment."* So each case carries the
spouses and children of **both** sides plus the child whose item triggered the block. The shared
words between the two sides are computed here and highlighted there; they are an aid to reading
and never a decision -- `CLAUDE.md` no-name-similarity still governs, and this proposes nothing.

**A DECIDED pair never comes back. An UNSURE one does.**
"""

import csv
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge import deck                                              # noqa: E402

ROOT = deck.ROOT
OUT_TSV = ROOT / "reports" / "parent-candidates.tsv"
OUT_JSON = ROOT / "out" / "gui-data.json"
OUT_HTML = ROOT / "out" / "parent-review.html"


def main():
    rel, geni_of = deck.load_relations(("p22", "p25", "p40", "p26"))
    father_of, mother_of = rel["p22"], rel["p25"]
    kids_of, sp_of = rel["p40"], rel["p26"]
    parents_of = {q: father_of.get(q, []) + mother_of.get(q, []) for q in set(father_of) | set(mother_of)}
    qid_of = {g: q for q, g in geni_of.items()}
    claimed = set(geni_of)
    sys.stderr.write("%s items carry a P2600\n" % format(len(geni_of), ","))

    # **`P2600` is not the only thing that identifies somebody, and using it alone made the deck
    # stale.** Emma, 2026-08-31: *"I think literally all these people were identified earlier and
    # some are very stale."* Seven of nine cases she answered `SAME` were already in
    # `reports/synoptic-correspondence.tsv`, known through the structural walk, the zipper, her
    # bio links or her earlier verdicts -- none of which puts a `P2600` on Wikidata.
    known_qid, known_geni, _syn = deck.load_correspondence()
    claimed |= known_qid
    print("%s items and %s profiles already identified somewhere"
          % (format(len(known_qid), ","), format(len(known_geni), ",")), file=sys.stderr)

    our_fathers, our_mothers, our_children, our_spouses = deck.load_our_family()
    our_parents = {g: our_fathers.get(g, []) + our_mothers.get(g, [])
                   for g in set(our_fathers) | set(our_mothers)}
    labels = deck.load_our_labels()

    answered, unsure = deck.answered_pairs()
    sys.stderr.write("%s pairs decided; %d UNSURE, which stay in the deck\n"
                     % (format(len(answered), ","), unsure))

    # ---- the guard's second arm, over every candidate --------------------------------
    rows = []
    for child, parents in our_parents.items():
        cq = qid_of.get(child)
        if not cq or not parents_of.get(cq):
            continue
        for g in parents:
            if g in qid_of or g in known_geni or g.startswith(("9995", "9990")):
                continue
            # **MATCH THE SLOT.** Emma, 2026-08-31, shown a case pairing
            # `Helena Mikontytar Schulin` with `Lars Henrik Keckman`: *"pretty sure this is the
            # wife of the person lol."* She was right and it was systematic: the guard offered
            # whichever parent item was unaccounted for, without checking which slot **our**
            # person occupies -- so our mother was routinely paired with the child's father, who
            # is her husband and is sitting in her own spouse list two lines above.
            if g in our_fathers.get(child, ()):
                candidates_q = father_of.get(cq, [])
            elif g in our_mothers.get(child, ()):
                candidates_q = mother_of.get(cq, [])
            else:
                continue
            for q in candidates_q:
                if q not in claimed and (g, q) not in answered:
                    rows.append((g, q, child))

    # One question per person: the first child that raises it.
    seen, unique = set(), []
    for g, q, child in rows:
        if g in seen:
            continue
        seen.add(g)
        unique.append((g, q, child))
    print("%s structural candidates corpus-wide" % format(len(unique), ","), file=sys.stderr)

    # ---- labels and chips ------------------------------------------------------------
    wanted = set()
    for _, q, _ in unique:
        wanted.add(q)
        wanted |= set(kids_of.get(q, ())) | set(sp_of.get(q, ()))
    # **Years above all, because she measured why:** in 1600-1900 the names are bilingual across
    # the records and 71% of her own confirmed pairs spell them differently -- `CLAUDE.md`
    # § *1600-1900 is the band where NAMES LIE and YEARS decide*.
    wd_label, cand_sex, cand_life, gone = deck.wikidata_facts(wanted, {q for _, q, _ in unique})
    our_sex, our_life = deck.load_our_facts({g for g, _, _ in unique})

    cases = []
    for g, q, child in unique:
        our_sp = [labels.get(x, x) for x in our_spouses.get(g, ())]
        our_kids = [labels.get(x, x) for x in our_children.get(g, ())]
        cand_sp = [wd_label.get(x, x) for x in sp_of.get(q, ())]
        cand_kids = [wd_label.get(x, x) for x in kids_of.get(q, ())]
        cases.append({
            # `g` can itself be a MULTI-VALUED cell -- a merged person carries every id they
            # were merged from -- so take the first id that actually resolves.
            "our": labels.get(g) or next(
                (labels[t] for t in (x.strip() for x in str(g).split(deck.FAMILY_SEP))
                 if labels.get(t)), ""),
            "geni": g,
            "qid": q,
            "cand": wd_label.get(q, q),
            "slot": "parent",
            "trigger_pre": "held because their child ",
            "trigger_bold": labels.get(child, child),
            "trigger_post": " already names a parent item on Wikidata",
            "our_fields": [["Spouse", our_sp], ["Children", our_kids]],
            "cand_fields": [["Spouse", cand_sp], ["Children", cand_kids]],
            "via": labels.get(child, child),
            "shared_kid_words": sorted(deck.words(our_kids) & deck.words(cand_kids)),
            "shared_spouse_words": sorted(deck.words(our_sp) & deck.words(cand_sp)),
            "our_sex": our_sex.get(g, ""),
            "cand_sex": cand_sex.get(q, ""),
            # **11 of 501 candidate items are simply gone** -- deleted, or merged in a way that
            # left no redirect. There is no judgement to make on a card whose right-hand side
            # does not exist, so it says so.
            "gone": q in gone,
            "our_life": our_life.get(g, ("", "")),
            "cand_life": cand_life.get(q, ("", "")),
        })
        cases[-1]["highlight"] = sorted(set(cases[-1]["shared_kid_words"])
                                        | set(cases[-1]["shared_spouse_words"]))

    with io.open(OUT_TSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["geni_id", "our_name", "qid", "candidate_name", "via_child",
                    "shared_kid_words", "shared_spouse_words"])
        for c in cases:
            w.writerow([c["geni"], c["our"], c["qid"], c["cand"], c["via"],
                        " ".join(c["shared_kid_words"]), " ".join(c["shared_spouse_words"])])

    deck.mark_also_offered(cases)

    # **Most evidence first.** A case with children on both sides is one she can settle; a case
    # with nothing on either side is one nobody can, and leading with those is how a deck stops
    # being worked. This orders the deck; it judges nothing.
    cases.sort(key=lambda c: (len(c["shared_kid_words"]) + len(c["shared_spouse_words"]),
                              len(c["cand_fields"][1][1]) + len(c["our_fields"][1][1])),
               reverse=True)
    # **The deck is every open candidate**, settled by what she did rather than by argument. It
    # was scoped to the ledger on 2026-08-31 -- *"just do all 47 in a run"* -- and by 2026-09-01
    # that filter selected **0 of 709**, so the page rendered empty while the work was still
    # there. She then ruled on **207 of those 709** in one sitting. No cap either: `DECK = 60`
    # was the other half of the same mistake.
    out = deck.render(cases, OUT_HTML, OUT_JSON,
                      title="Parent Adjudication",
                      sub="Is our Geni person the same as the parent their child already "
                          "names on Wikidata?",
                      key="parent-adjudication-v1")

    print("%s structural candidates -> %s" % (format(len(cases), ","), OUT_TSV.relative_to(ROOT)))
    print("%d in the deck -> %s, %s" % (len(out), OUT_JSON.relative_to(ROOT),
                                        OUT_HTML.relative_to(ROOT)))

    bad = deck.nameless(out)
    if bad:
        print("BROKEN DECK: %d of %d cards name nobody on one side -- e.g. %s. See CLAUDE.md"
              " section THE PARENT DECK."
              % (len(bad), len(out), ", ".join(sorted(c["qid"] for c in bad)[:5])),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
