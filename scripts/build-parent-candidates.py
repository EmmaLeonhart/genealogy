"""The parent identifications the duplicate guard is sitting on, as a file she can answer.

    python scripts/build-parent-candidates.py

**Emma, 2026-08-31:** the generator should *"actively create merge candidates like our ones that
are files for potential geni identifications related to parents"*.

**The problem this closes is delivery, not detection.** The guard already finds these: our person
is the parent of somebody whose Wikidata item names a parent nothing accounts for, so creating
them might duplicate that item. The guard refuses, prints a line, and the person falls into the
carry-forward. Nothing ever put the question in front of her -- which is why thousands of them
accumulated unexamined until a one-off script was written after the fact. That script is the
failure, not the fix: an output nobody generates is an output nobody answers.

So this runs with the batch and writes three things:

  * `reports/parent-candidates.tsv` -- every open candidate, one row
  * `out/gui-data.json` -- the deck, with the evidence needed to judge
  * `out/parent-review.html` -- the deck rendered, ready to open

**What makes a case answerable is the EVIDENCE, not the names.** Emma, shown a question carrying
neither: *"Fuck you no relationships means I can't make a judgment."* So each case carries the
spouses and children of **both** sides plus the child whose item triggered the block. The shared
words between the two sides are computed here and highlighted there; they are an aid to reading
and never a decision -- `CLAUDE.md` no-name-similarity still governs, and this proposes nothing.

**A DECIDED pair never comes back. An UNSURE one does.** `reports/emma-judgments.tsv` is the
record and `ledger()` already folds its `SAME` rows. A `SAME` or a `DIFFERENT` is an answer and
retires the case. **An `UNSURE` is not an answer** -- it is *I cannot tell from this*, and
retiring it was something I invented and she did not ask for. Those come back, so a later run
that has more evidence (a new export, a relative who has since gained an item) can put a better
version of the same question in front of her.
"""

import csv
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELATIONS = ROOT / "out" / "wikidata" / "relations.tsv"
LABELS_WD = ROOT / "out" / "wikidata" / "labels.tsv"
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
JUDGMENTS = ROOT / "reports" / "emma-judgments.tsv"
TEMPLATE = ROOT / "out" / "parent-review.template.html"
OUT_TSV = ROOT / "reports" / "parent-candidates.tsv"
OUT_JSON = ROOT / "out" / "gui-data.json"
OUT_HTML = ROOT / "out" / "parent-review.html"

csv.field_size_limit(1 << 30)
SEP = "|"

#: How many cases the deck carries. She works through these by hand, so a deck of nine thousand
#: is not a deck. Ordered by how much evidence a case has, so the answerable ones come first.
DECK = 60


def cell(row, column):
    return [x.strip() for x in (row.get(column) or "").split(SEP) if x.strip()]


def fold(w):
    w = w.lower()
    for a, b in (("æ", "a"), ("ä", "a"), ("å", "a"), ("ö", "o"),
                 ("ø", "o"), ("é", "e"), ("ü", "u")):
        w = w.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", w)


def words(names):
    """Folded tokens of length > 2 across a list of names."""
    out = set()
    for n in names:
        for tok in str(n).split():
            f = fold(tok)
            if len(f) > 2:
                out.add(f)
    return out


def main():
    # ---- Wikidata: who holds a P2600, and what each item says about its family ----------
    geni_of, kids_of, sp_of, parents_of = {}, {}, {}, {}
    father_of, mother_of = {}, {}
    with io.open(RELATIONS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = row["qid"]
            if row.get("p2600"):
                geni_of[qid] = row["p2600"].split(SEP)[0].strip()
            fa = [x for x in (row.get("p22") or "").split(SEP) if x]
            mo = [x for x in (row.get("p25") or "").split(SEP) if x]
            if fa or mo:
                parents_of[qid] = fa + mo
                father_of[qid], mother_of[qid] = fa, mo
            ks = [x for x in (row.get("p40") or "").split(SEP) if x]
            if ks:
                kids_of[qid] = ks
            ss = [x for x in (row.get("p26") or "").split(SEP) if x]
            if ss:
                sp_of[qid] = ss
    qid_of = {g: q for q, g in geni_of.items()}
    claimed = set(geni_of)

    # **`P2600` is not the only thing that identifies somebody, and using it alone made the deck
    # stale.** Emma, 2026-08-31, on the nine cases that survived the slot fix: *"I think literally
    # all these people were identified earlier and some are very stale. Most have identification
    # already on wikidata lmao."* She answered `SAME` to all nine, and **7 of the 9 were already
    # in `reports/synoptic-correspondence.tsv`** -- known through the structural walk, the zipper,
    # her own bio links or her earlier verdicts, none of which put a `P2600` on Wikidata.
    #
    # So an item is spoken for if ANY source in the synoptic correspondence claims it, and a Geni
    # profile we have already identified is not a candidate for identification. That file is the
    # union of all eight sources; `docs/synoptic-correspondence.md` is what each is worth.
    known_geni, known_qid = set(), set()
    synoptic = ROOT / "reports" / "synoptic-correspondence.tsv"
    if synoptic.exists():
        with io.open(synoptic, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="	"):
                if r.get("qid") and r.get("geni_id"):
                    known_qid.add(r["qid"])
                    known_geni.add(r["geni_id"])
        claimed |= known_qid
        print("%s items and %s profiles already identified somewhere"
              % (format(len(known_qid), ","), format(len(known_geni), ",")), file=sys.stderr)
    sys.stderr.write("%s items carry a P2600\n" % format(len(geni_of), ","))

    # ---- our side ------------------------------------------------------------------
    our_parents, our_children, our_spouses = {}, {}, {}
    our_father, our_mother = {}, {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            fa, mo = cell(row, "fathers"), cell(row, "mothers")
            if fa or mo:
                our_parents[g] = fa + mo
                our_father[g], our_mother[g] = set(fa), set(mo)
            ks = cell(row, "children")
            if ks:
                our_children[g] = ks
            ss = cell(row, "spouses")
            if ss:
                our_spouses[g] = ss

    labels = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            labels[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""

    # ---- already answered, in either direction --------------------------------------
    answered, unsure = set(), 0
    if JUDGMENTS.exists():
        with io.open(JUDGMENTS, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if not (row.get("geni_id") and row.get("qid")):
                    continue
                if (row.get("verdict") or "").strip().upper() == "UNSURE":
                    unsure += 1
                    continue
                answered.add((row["geni_id"].strip(), row["qid"].strip()))
    sys.stderr.write("%s pairs decided; %d UNSURE, which stay in the deck\n"
                     % (format(len(answered), ","), unsure))

    # ---- the guard's second arm, over every candidate --------------------------------
    rows = []
    for child, parents in our_parents.items():
        cq = qid_of.get(child)
        if not cq:
            continue
        if not parents_of.get(cq):
            continue
        for g in parents:
            if g in qid_of or g in known_geni or g.startswith(("9995", "9990")):
                continue
            # **MATCH THE SLOT.** Emma, 2026-08-31, shown a case pairing
            # `Helena Mikontytär Schulin` with `Lars Henrik Keckman`: *"pretty sure this is the
            # wife of the person lol."* She was right and it was systematic, not one bad row.
            #
            # A child has two parents. The guard offered whichever parent item was unaccounted
            # for, without checking which slot **our** person occupies -- so our mother was
            # routinely paired with the child's father, who is her husband and is sitting in her
            # own spouse list two lines above. `Q17381568` was literally the second name under
            # *Spouse* on that card.
            #
            # Our tree records the slot (`fathers` / `mothers`) and so does Wikidata (`P22` /
            # `P25`), so this is structural and touches no names.
            if g in our_father.get(child, ()):
                candidates_q = father_of.get(cq, [])
            elif g in our_mother.get(child, ()):
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
    # **The deck is the LEDGER ones; 9,061 was never the question.** Emma, 2026-08-31:
    # *"there are not 9,061 open candidates lol"*, then *"there could at the very maximum in
    # principle be 400 people in the network right now... just do all 47 in a run."* The 9,061
    # is corpus-wide -- every person in a 1.45M-person tree who parents somebody holding a QID
    # whose item names an unaccounted parent. A structural pattern, not a backlog. The full
    # file keeps them all, because the network grows into it; the deck is what is blocked now.
    ledger = set()
    lpath = ROOT / "reports" / "garborg-qids.tsv"
    if lpath.exists():
        with io.open(lpath, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="	"):
                if r.get("geni_id"):
                    ledger.add(r["geni_id"].strip())
    in_ledger = [t for t in unique if t[0] in ledger]
    print("%s structural candidates corpus-wide; %s in the ledger -- the deck"
          % (format(len(unique), ","), format(len(in_ledger), ",")), file=sys.stderr)

    # ---- labels for the Wikidata side ------------------------------------------------
    wanted = set()
    for _, q, _ in unique:
        wanted.add(q)
        wanted |= set(kids_of.get(q, ())) | set(sp_of.get(q, ()))
    wd_label = {}
    if LABELS_WD.exists():
        with io.open(LABELS_WD, encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if parts[0] in wanted and len(parts) > 1:
                    wd_label.setdefault(parts[0], parts[1])
    else:
        sys.stderr.write("WARNING: out/wikidata/labels.tsv missing -- the Wikidata side will "
                         "show QIDs instead of names, which makes a case much harder to judge. "
                         "Rebuild with scripts/extract-wikidata-labels.py\n")

    cases = []
    for g, q, child in unique:
        our_sp = [labels.get(x, x) for x in our_spouses.get(g, ())]
        our_kids = [labels.get(x, x) for x in our_children.get(g, ())]
        cand_sp = [wd_label.get(x, x) for x in sp_of.get(q, ())]
        cand_kids = [wd_label.get(x, x) for x in kids_of.get(q, ())]
        cases.append({
            "our": labels.get(g, ""),
            "geni": g,
            "qid": q,
            "cand": wd_label.get(q, q),
            "our_sp": our_sp,
            "our_kids": our_kids,
            "cand_sp": cand_sp,
            "cand_kids": cand_kids,
            "via": labels.get(child, child),
            "shared_kid_words": sorted(words(our_kids) & words(cand_kids)),
            "shared_spouse_words": sorted(words(our_sp) & words(cand_sp)),
        })

    with io.open(OUT_TSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["geni_id", "our_name", "qid", "candidate_name", "via_child",
                    "shared_kid_words", "shared_spouse_words"])
        for c in cases:
            w.writerow([c["geni"], c["our"], c["qid"], c["cand"], c["via"],
                        " ".join(c["shared_kid_words"]), " ".join(c["shared_spouse_words"])])

    # **Most evidence first.** A case with children on both sides is one she can settle; a case
    # with nothing on either side is one nobody can, and leading with those is how a deck stops
    # being worked. This orders the deck; it judges nothing.
    cases.sort(key=lambda c: (len(c["shared_kid_words"]) + len(c["shared_spouse_words"]),
                              len(c["cand_kids"]) + len(c["our_kids"])), reverse=True)
    # **All of the ledger ones, not a slice.** Her instruction: *"just do all 47 in a run so I
    # can do it."* A cap is right for 9,061 and wrong for 47.
    ledger_ids = {t[0] for t in in_ledger}
    deck = [c for c in cases if c["geni"] in ledger_ids]
    json.dump(deck, io.open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if TEMPLATE.exists():
        html = TEMPLATE.read_text(encoding="utf-8")
        if "__DATA__" not in html:
            sys.exit("template has no __DATA__ placeholder")
        io.open(OUT_HTML, "w", encoding="utf-8").write(
            html.replace("__DATA__", json.dumps(deck, ensure_ascii=False)))

    print("%s structural candidates -> %s"
          % (format(len(cases), ","), OUT_TSV.relative_to(ROOT)))
    print("%d in the deck -> %s, %s" % (len(deck), OUT_JSON.relative_to(ROOT),
                                        OUT_HTML.relative_to(ROOT)))


if __name__ == "__main__":
    main()
