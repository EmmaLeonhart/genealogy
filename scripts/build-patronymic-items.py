"""The patronymic name items her algorithm needs, and the `P144` derivations that gate it.

    python scripts/build-patronymic-items.py

**Emma's design, 2026-08-31**, dictated after the string-comparison version was built and found
wanting: a patronymic resolves by **item identity**, not by comparing strings per person.

    the patronymic resolves to a patronymic NAME ITEM
    that item records the given names it derives from   (its own P144 based on, MULTI-VALUED)
    the parent carries a given name OBJECT              (P735 -> an item)
    parent's P735 item among the P144 values?           -> emit P5056, P144 -> that parent

*"structurally this is a thing to be done but it requires well developed patronymic objects we
currently lack."* This builds the plan for those objects. It writes no QuickStatements: the
deliverable is the data, per `CLAUDE.md` § *"Analyse this" means build a CSV*, and an edit batch
nobody asked for is its own rule.

## The one string comparison, and where it lives

Her constraint: *"it only uses a string comparison once."* Here it is -- establishing which given
name a patronymic derives from -- and the comparison is made **against the fathers our tree
already names**, never by searching the store. Searching returns 553 candidates for `Olsdatter`
including `oala` and `oilbhe`; the father is one fixed person, which is the same boundary the
zipper's name step runs on. After this file exists, no bearer is ever string-compared again.

## What each item carries

Measured live over all 631 patronymic items that exist, so the shape is copied not invented:
`P31` 100%, `P282` *writing system* 92%, `P1705` *native label* 81%, `P407` 59%, `P144` 19%,
`P5278` *surname for other gender* 15%.

  * `P31` *instance of* -> `Q110874` *patronymic*
  * `P1705` *native label* -- the token as written
  * `P144` *based on* -- every given-name item the fathers actually carry. **Multi-valued, her
    ruling:** 1,892 of 7,352 tokens are attested by more than one given name, and keeping only
    the commonest would make the 1,364 `Olsdatter`s whose father was `Ola` fail the identity test
    and receive no `P5056` at all.
  * `P5278` *surname for other gender* -- `Olsson` <-> `Olsdotter`, same stem, gendered suffix.

**`P407` *language of work or name* is deliberately absent** though 59% of existing items carry
it. Nothing in a token says which language it is: `Andersson` reads Swedish and `Andersen`
Danish-Norwegian by convention rather than rule, and taking it from the export or the region is
the geography inference `CLAUDE.md` forbids everywhere else.

Writes `reports/patronymic-items-to-create.tsv`.
"""

import collections
import csv
import io
import gzip
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import namemodel as nm                                              # noqa: E402

LABELS = ROOT / "reports" / "derived-labels.csv"
FAMILY = ROOT / "reports" / "derived-family.csv"
NAME_ITEMS = ROOT / "out" / "wikidata" / "name-items-in-store.tsv.gz"
OUT = ROOT / "reports" / "patronymic-items-to-create.tsv"

csv.field_size_limit(1 << 30)

#: The gendered suffix pairs, for `P5278` *surname for other gender*. Norwegian/Danish first,
#: then Swedish. `-sen` and `-son` are both male; the female forms differ by country, so a stem
#: can pair with more than one and every pairing found is emitted.
GENDER_PAIRS = (("sen", "datter"), ("sen", "sdatter"), ("son", "datter"),
                ("son", "dotter"), ("sson", "sdotter"), ("son", "sdotter"))


def name_items():
    """`({given label -> qids}, {patronymic label -> qid})` from the store index."""
    given, pat = collections.defaultdict(set), {}
    with gzip.open(NAME_ITEMS, "rt", encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            r = dict(zip(head, line.rstrip("\n").split("\t")))
            kinds = (r.get("kind") or "").split("|")
            for lab in (r.get("labels") or "").split("|"):
                if not lab:
                    continue
                if "given" in kinds:
                    given[lab.casefold()].add(r["qid"])
                if "patronymic" in kinds:
                    pat.setdefault(lab.casefold(), r["qid"])
    return given, pat


def main():
    label, father = {}, {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            f = (r.get("father") or "").strip()
            if f:
                father[r["geni_id"]] = f

    # ---- the ONE string comparison: which given names attest each patronymic ------------
    #
    # Against the father this tree already names, never against the store. The father is one
    # fixed person, so this confirms a position the structure chose rather than searching.
    sources = collections.defaultdict(collections.Counter)
    bearers = collections.Counter()
    for g, lab in label.items():
        dad = label.get(father.get(g, ""), "")
        if not dad:
            continue
        for tok in lab.split():
            if not nm.PATRONYMIC.match(tok):
                continue
            if nm.patronymic_or_surname(tok, dad) != "patronymic":
                continue
            m = nm.PATRONYMIC_PARTS.match(tok)
            if not m:
                continue
            stem = m.group(1).casefold().rstrip("s")
            bearers[tok.casefold()] += 1
            for w in dad.split():
                if nm.PATRONYMIC.match(w):
                    continue
                if nm._same_name(stem, w.casefold().rstrip("s")):
                    sources[tok.casefold()][w] += 1
                    break

    given, pat_items = name_items()
    sys.stderr.write(f"{len(sources):,} attested patronymic tokens; "
                     f"{len(given):,} given-name labels with an item\n")

    rows = []
    for tok, srcs in sorted(sources.items()):
        # `P144` targets. An exact label lookup -- case folds and NOTHING else, per the
        # diacritic rule: `Maria`/`María`/`Mária` are three names with three items.
        targets, ambiguous, unknown = [], [], []
        for name in sorted(srcs, key=lambda n: -srcs[n]):
            qids = given.get(name.casefold())
            if not qids:
                unknown.append(name)
            elif len(qids) == 1:
                targets.append((name, next(iter(qids))))
            else:
                ambiguous.append(f"{name}({len(qids)})")

        # `P5278` surname for other gender: same stem, the opposite gendered suffix.
        # **Pair off the STEM, not by swapping suffixes on the whole token.** Swapping produced
        # `olsdatter` -> `olssen` and `olsen` -> `oldatter`, neither of which is a word: the
        # genitive `s` belongs to the stem and the naive strip either doubled it or ate it.
        # `PATRONYMIC_PARTS` already splits the two, so build both gendered forms from the stem
        # and keep whichever the corpus actually attests.
        m = nm.PATRONYMIC_PARTS.match(tok)
        stem_raw = m.group(1) if m else ""
        pair = ""
        if stem_raw:
            # `PATRONYMIC_PARTS` splits the genitive `s` onto the stem for `olsdatter` and off
            # it for `olsen`, so the stem is not the same string in the two directions. Build
            # both spellings and let the corpus decide -- `olsen` -> `oldatter` is nobody's word,
            # `olsdatter` is.
            bases = {stem_raw, stem_raw + "s", stem_raw.rstrip("s")}
            male = {b + suf for b in bases for suf in ("en", "on", "son", "sen")}
            female = {b + suf for b in bases for suf in ("datter", "dotter", "dtr")}
            here = female if any(tok.endswith(x) for x in ("datter", "dotter")) else male
            other = (male if here is female else female)
            # **Most-borne wins, not alphabetical.** Sorting by string picked `oldatter` over
            # `olsdatter` for `olsen`, because a handful of people really are recorded that way
            # and `o-l-d` sorts before `o-l-s`. The pair should be the form the corpus actually
            # uses.
            cands = [c for c in other if c != tok and (c in pat_items or c in sources)]
            if cands:
                pair = max(cands, key=lambda c: (bearers.get(c, 0), c in pat_items))

        rows.append({
            "token": tok,
            "bearers": bearers[tok],
            "existing_item": pat_items.get(tok, ""),
            "action": "link" if tok in pat_items else "create",
            "native_label": tok,
            "p144_targets": " ".join(q for _, q in targets),
            "p144_names": " ".join(n for n, _ in targets),
            "p144_ambiguous": " ".join(ambiguous),
            "p144_unknown": " ".join(unknown),
            "p5278_pair": pair,
            "stem": stem_raw,
        })

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    have144 = sum(1 for r in rows if r["p144_targets"])
    amb = sum(1 for r in rows if not r["p144_targets"] and r["p144_ambiguous"])
    unk = sum(1 for r in rows if not r["p144_targets"] and not r["p144_ambiguous"])
    pairs = sum(1 for r in rows if r["p5278_pair"])
    create = sum(1 for r in rows if r["action"] == "create")
    print(f"{len(rows):,} patronymic tokens attested by a father in our tree")
    print(f"  {create:,} need an item created; {len(rows)-create:,} already have one")
    print(f"  {have144:,} have at least one unambiguous P144 target")
    print(f"  {amb:,} blocked ONLY by an ambiguous given name (several items share the label)")
    print(f"  {unk:,} have no given-name item for any attesting father")
    print(f"  {pairs:,} have a P5278 surname-for-other-gender partner")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
