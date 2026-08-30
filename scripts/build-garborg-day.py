"""One day's Garborg batch: everything that can run in a SINGLE QuickStatements run.

    python scripts/build-garborg-day.py

**Emma, 2026-08-24, after running yesterday's file:** *"I only ran some of the quick
statements because many of them required links that couldn't exist... The siblings all
being connected to each other: they should be connected to each other, but they
couldn't be connected to each other without things that required their QIDs, which we
had just created. This means this is going to be the practical limitation of what our
quick statements can do. With every day, we are kind of going through a full run of
what we can do on the frontier like this."*

So the rule is: **a statement goes in only if both ends already have a QID.** Nothing
deferred, nothing commented out, nothing that fails. What could not run today becomes
tomorrow's batch, because tomorrow those items exist.

`reports/garborg-qids.tsv` is the ledger of who has one. It is filled from **Emma's
Wikidata contributions**, not from a bulk download — her instruction: *"You should be
looking at my contributions to see the new ones I've created."* Her account is 日巫女.

Each day therefore does three things, all runnable:

1. **Close the links that yesterday's creations made possible** — the reciprocal `P40`
   from the parents, and `P3373` among siblings who all have QIDs now.
2. **Create the next ring**, everyone one edge away from someone who has a QID.
3. **Link the new people to anything that already exists** — parents, spouses,
   siblings — but never to each other, because they are being minted right now.

Labels come with `ja` and `zh` from `reports/garborg-name-transliterations.tsv`, per
Emma 2026-08-24: *"we should also be adding their names in languages that are not
English, or at least in Japanese... and Chinese."*

Writes `reports/wikidata-garborg-day.qs` and `reports/garborg-carry-forward.tsv`.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import csv
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import (  # noqa: E402
    NICKNAME, aliases_for, classify, classify_fields, load_plan,
    statements_for)


def _load_gaps():
    """`garborg-existing-gaps.py` has a hyphen, so `import` cannot reach it."""
    import importlib.util
    path = Path(__file__).resolve().parent / "garborg-existing-gaps.py"
    spec = importlib.util.spec_from_file_location("garborg_existing_gaps", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.existing_state


existing_state = _load_gaps()

ROOT = Path(__file__).resolve().parent.parent

#: **Emma, 2026-08-25:** *"siblin relationships are too numerous and imo come off as spammy.
#: We limit sibling relationship adding to 10 quickstatements a day."* This builder was
#: emitting **162** `P3373` in one file. Siblings grow as the SQUARE of a family -- nine
#: children is 72 statements by itself -- while parents grow linearly, so a batch that looks
#: balanced by people is mostly sibling links by statement. The cap is per DAY across every
#: batch, so it is shared with `build-missing-reciprocals.py`, and the overflow is carried
#: rather than dropped: the statements are correct, there are just too many at once.
SIBLING_CAP = 10
_siblings_emitted = []

SEX = {"M": "Q6581097", "F": "Q6581072"}

#: Geni ids released from the duplicate guard by hand, with the unmatched item that held them.
#: The guard refuses to create anybody whose parent has a `P40` child item we have not matched,
#: because the person may BE that item. It is conservative on purpose and these two are false
#: positives: the unmatched item is a NAMED OTHER PERSON, which the guard cannot see because it
#: compares QIDs and not labels.
#:
#: Emma released both on 2026-08-26 when they were put to her.
RELEASED_FROM_DUPLICATE_GUARD = {
    # Ramborg Knutsdotter Lejon. Her parent `Q5915800` has unmatched children `Q4955715`
    # *Ingegerd Knutsdotter* and `Q16595443` *Katarina Knutsdotter* -- her sisters, both named,
    # neither of them Ramborg.
    "6000000004870648136": "the two unmatched children are her named sisters",
    # Algot Bryniolfsson. `Q101247444` has unmatched child `Q101247439` *NN Brynolvsdotter* --
    # a daughter, where Algot is a son. The patronymic settles it.
    "6000000005795638082": "the unmatched child is a -dotter and Algot is a -son",
}


def sibling_budget_left():
    return SIBLING_CAP - len(_siblings_emitted)
HUMAN = "Q5"


def qs(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def ledger():
    """Geni id -> QID for everybody we can already point at an item.

    **`entity_resolution.md` is folded in, and it has to be.** That file is where a
    correspondence recognised BY HAND lives, and it is the only place that knows about an
    item carrying no `P2600` yet -- which is exactly the shape of Emma's own. Without it
    the spine walk reached step 1 of `paths/bergitte-to-emma.tsv`, which is HER, found her
    in neither `garborg-qids.tsv` nor `p2600-all.tsv`, and emitted a `CREATE` that would
    have minted her a SECOND item. `CLAUDE.md` says it plainly: she *"has her own item and
    needs an id rather than a creation"*.
    """
    out = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["geni_id"]] = row["qid"]
    try:
        sys.path.insert(0, str(ROOT / "src"))
        from genimerge import entities
        for r in entities.read_file(ROOT / "entity_resolution.md").resolutions:
            if r.geni_id and r.qid:
                out.setdefault(r.geni_id, r.qid)
    except Exception as exc:                                        # noqa: BLE001
        print(f"WARNING: entity_resolution.md not folded into the ledger ({exc}) -- "
              f"a hand-asserted item could be created a second time")
    return out


def translit():
    out = {}
    with open(ROOT / "reports" / "garborg-name-transliterations.tsv",
              encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["token"]] = (row["ja"], row["zh"])
    return out


def _words():
    """The per-language relationship table from `build-nn-label-batch.py`.

    Imported rather than restated: it carries decisions that were paid for, notably
    that Danish and Norwegian take a different preposition depending on which way the
    relation runs (`datter af` but `mor til`), and that Slavic and Welsh are left out
    because they inflect the name after the relationship word.
    """
    import importlib.util
    path = Path(__file__).resolve().parent / "build-nn-label-batch.py"
    spec = importlib.util.spec_from_file_location("build_nn_label_batch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WORDS


WORDS = _words()


def describe_all(geni_id, facts, father, mother, labels, table,
                 children=None, spouses=None, siblings=None):
    """`{lang: "daughter of Arne Olaus Fjørtoft Garborg"}` for a redacted person.

    Built from the nearest named parent. `ja` and `zh` are included **here** where
    `build-nn-label-batch.py` excludes them, and the reason it excludes them is the
    reason this can: it warns the phrase would come out `Gerard Spencerの娘`, mixing
    scripts, *because the relative's name has not been transliterated*. In this family
    it has — `reports/garborg-name-transliterations.tsv` covers every token — so the
    Japanese and Chinese forms are whole rather than half Latin.
    """
    children = children or {}
    spouses = spouses or {}
    siblings = siblings or {}
    sex = (facts.get(geni_id, {}).get("sex") or "")

    def named(gid):
        """The relative's name, or `""` when it names nobody and the walk must fall through.

        **A marker plus a surname names nobody either**, and only the bare forms were being
        caught. `<private> Skårland` passed, so a redacted *parent* put the marker into ten
        descriptive labels at once -- `filla de <private> Skårland`, `datter af <private>
        Skårland`, down the whole language table -- on a person whose own `mul` correctly read
        `NN Undheim`. The rule was enforced on a person's own label and not on their child's.

        **Falling through is the fix, not reconstructing.** Rewriting the relative to
        `NN Skårland` was tried first and is wrong for the reason
        `test_a_redacted_person_gets_the_marker_in_mul_and_a_description_elsewhere` already
        states: a description built on an unnamed relative describes nobody, so the walk should
        move to the next relative -- the other parent, then a child, spouse or sibling -- which
        `BY` exists to do.

        `WORDS_MEANING_UNKNOWN` is imported rather than restated; `CLAUDE.md` names
        `scripts/labels` as the one place that owns which words mean the name is unknown.
        """
        from labels import WORDS_MEANING_UNKNOWN
        n = (labels.get(gid) or "").strip()
        low = n.lower()
        if not n or low in ("nn", "private", "unknown", "?") or "<private>" in low:
            return ""
        # A PREFIX test, not a head-token one: the set holds multi-word phrases
        # (`name not known`, `no name`) as well as single words, so splitting on space
        # would miss exactly the longest and most obvious markers.
        markers = {w.lower() for w in WORDS_MEANING_UNKNOWN} | {"nn", "unknown", "ukjent"}
        return "" if any(low == w or low.startswith(w + " ") for w in markers) else n

    #: Which relative to describe by, nearest first, and the `WORDS` group naming the
    #: relationship FROM this person TO them.
    #:
    #: **Only `child_of` was ever used, and that left people undescribed.** A redacted person
    #: with no recorded parent got `Lmul "NN Skårland"` and nothing else -- while carrying a
    #: named CHILD, which `CLAUDE.md` covers: the description is built *"from the nearest named
    #: relative"*, and a child is one. The `WORDS` table already carried `parent_of`,
    #: `spouse_of` and `sibling_of` with the right word per sex and the right preposition per
    #: direction (`datter af` but `mor til`); nothing consulted them.
    BY = (("child_of", (father.get(geni_id), mother.get(geni_id))),
          ("parent_of", tuple(children.get(geni_id, ()))),
          ("spouse_of", tuple(spouses.get(geni_id, ()))),
          ("sibling_of", tuple(siblings.get(geni_id, ()))))

    for group_name, relatives in BY:
        for rel in relatives:
            name = named(rel) if rel else ""
            if not name:
                continue
            out = {}
            for lang, words in WORDS.items():
                group = words[group_name]
                word = group.get(sex) or group[""]
                joiner = words["of"]
                if isinstance(joiner, dict):
                    joiner = joiner.get(group_name, joiner[""])
                out[lang] = f"{word} {joiner} {qs(name)}"
            ja, zh = label_in(name, table)
            if ja:
                JA = {"child_of": {"M": "息子", "F": "娘", "": "子"},
                      "parent_of": {"M": "父", "F": "母", "": "親"},
                      "spouse_of": {"M": "夫", "F": "妻", "": "配偶者"},
                      "sibling_of": {"M": "兄弟", "F": "姉妹", "": "きょうだい"}}
                ZH = {"child_of": {"M": "子", "F": "女", "": "子女"},
                      "parent_of": {"M": "父", "F": "母", "": "父母"},
                      "spouse_of": {"M": "夫", "F": "妻", "": "配偶"},
                      "sibling_of": {"M": "兄弟", "F": "姐妹", "": "同胞"}}
                out["ja"] = f"{ja}の{JA[group_name].get(sex) or JA[group_name]['']}"
                out["zh"] = f"{zh}之{ZH[group_name].get(sex) or ZH[group_name]['']}"
            return out
    return {}


def read_live_values():
    """`{(qid, property, value)}` -- every statement the ledger items already hold.

    Built by `scripts/refresh-live-values.py` from whole items. Missing file means an empty
    set and today's behaviour, which is the safe direction: a redundant statement is a no-op
    in QuickStatements, a suppressed one would be a loss.
    """
    out = set()
    path = ROOT / "reports" / "garborg-live-values.tsv"
    if not path.exists():
        print("WARNING: reports/garborg-live-values.tsv missing - the batch will re-emit "
              "statements the items already hold. Run scripts/refresh-live-values.py")
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="	"):
            out.add((row["qid"], row["property"], row["value"]))
    return out


def live_state():
    """`{qid: (label languages, properties)}` from the 2026-08-24 live read.

    Ground truth, and it outranks the store: the store was downloaded before Emma made
    most of these items, and the fallback in `absent` assumes an item outside the store
    was made by our own batch and so carries no name statements. She edits by hand, so
    that assumption is wrong exactly where it matters most.

    A row marked `no` was **not** re-read and is deliberately omitted from the result,
    so it falls through to the store and then to the assumption rather than being
    reported as an item with no properties at all.
    """
    out = {}
    path = ROOT / "reports" / "garborg-live-state.tsv"
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("qid\t"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4 or parts[1] == "no":
                continue
            langs = {p.strip() for p in parts[2].replace(",", " ").split()
                     if p.strip().isalpha()}
            out[parts[0]] = (langs, set(parts[3].split()))
    return out


def read_tree():
    fam_p = collections.defaultdict(list)
    fam_c = collections.defaultdict(list)
    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    cur = kind = None
    with open(ROOT / "out" / "merged.ged", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                p = line.split()
                cur, kind = p[1][2:-1], (p[2].strip() if len(p) > 2 else "")
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                if kind == "FAM":
                    if tag in ("HUSB", "WIFE"):
                        fam_p[cur].append(val[2:-1])
                    elif tag == "CHIL":
                        fam_c[cur].append(val[2:-1])
                elif kind == "INDI":
                    if tag == "FAMS":
                        fams[cur].append(val[2:-1])
                    elif tag == "FAMC":
                        famc[cur].append(val[2:-1])
    return fam_p, fam_c, fams, famc



def _label_corrections(our_items, labels, table, state):
    """`Lmul`/`Len`/`Lja`/`Lzh` for existing items whose label is still the BIRTH name.

    **Emma, 2026-08-29:** *"You should be adding into the generated quick statements a block
    that's just all of these corrections. Need all of these corrections on the existing
    items."*

    `derive-labels.py` flipped 251,707 labels to the married form on 2026-08-29. Every item
    created before that carries the birth name in `mul` and `en` -- and, because `ja`/`zh`
    are transliterated from `label_mul`, in Japanese and Chinese too. Her words: *"the CJK
    names are being put in the birth name form"*.

    **The live label comes from `reports/garborg-qids.tsv`**, whose `label` column is written
    by the contributions refresh at the top of every run, so it is what Wikidata says today.
    `state` was the obvious-looking source and is the wrong one: it records which *languages*
    an item has, not what they say.

    **Only where it actually differs**, so the block empties itself as it is run rather than
    repeating unconditionally the way the clan block did. A label REPLACES, so the outgoing
    value goes out as an `Amul` on the line above -- § *The MARRIED name is the real name*,
    *"first amul added if applicable"* -- which is what stops a hand correction of hers being
    silently overwritten.
    """
    # The birth forms, so a correction can be recognised as one rather than guessed at.
    aliases_of = {}
    dl = ROOT / "reports" / "derived-labels.csv"
    if dl.exists():
        csv.field_size_limit(10 ** 8)
        want_ids = set(our_items)
        for row in csv.DictReader(dl.open(encoding="utf-8")):
            if row["geni_id"] in want_ids:
                aliases_of[row["geni_id"]] = {
                    a.strip() for a in (row.get("alias_names") or "").split(" | ") if a.strip()}

    live = {}
    ledger = ROOT / "reports" / "garborg-qids.tsv"
    if ledger.exists():
        for row in csv.DictReader(ledger.open(encoding="utf-8"), delimiter="	"):
            lab = (row.get("label") or "").strip()
            if row.get("qid") and lab:
                live[row["qid"]] = lab

    out = []
    for geni_id, qid in sorted(our_items.items(), key=lambda kv: kv[1]):
        want = qs(labels.get(geni_id, ""))
        have = live.get(qid, "")
        if not want or not have or have == want:
            continue
        # **Only where the item literally holds the BIRTH name.** The first version corrected
        # every difference, and its own output showed why that is wrong: it offered to rewrite
        # `Carl August Ehrensvärd (1745-1800)` to `Carl August Ehrensvärd` and to strip
        # `of Viby, heiress, lady of Händelöö` off Ingegerd Svantepolksdotter -- Wikidata's
        # labels being BETTER than ours, and § *The purpose is to ADD to Wikidata, not to
        # correct it* forbids exactly that. Matching against the birth-name alias makes this
        # a correction of our own 2026-08-29 flip and nothing else.
        if have not in aliases_of.get(geni_id, ()):
            continue
        # **A comment above EVERY line, not just the first.** `tests/test_p2600_batches.py`
        # asserts it and was right to: these are five separate edits to a live item, and a
        # reader scanning the batch to approve or delete one of them needs each to say what it
        # does. One comment over a five-line group leaves four unexplained.
        out.append(f"#   {qid}: holds {have!r}; ours is {want!r}")
        out.append(f"#   {qid}: keep the outgoing label as an alias before it is replaced")
        out.append(f'{qid}	Amul	"{have}"')
        out.append(f"#   {qid}: set the mul label to {want!r}")
        out.append(f'{qid}	Lmul	"{want}"')
        out.append(f"#   {qid}: set the en label to {want!r}")
        out.append(f'{qid}	Len	"{want}"')
        ja, zh = label_in(want, table)
        if ja:
            out.append(f"#   {qid}: set the ja label")
            out.append(f'{qid}	Lja	"{ja}"')
            out.append(f"#   {qid}: set the zh label")
            out.append(f'{qid}	Lzh	"{zh}"')
    if out:
        out = ["", "# " + "-" * 72,
               "# LABEL CORRECTIONS -- existing items whose label is not what our tree now",
               "#   says. derive-labels.py made the married form primary on 2026-08-29 and",
               "#   these items predate it. The outgoing label is preserved as an Amul on",
               "#   the line above the Lmul that replaces it, so nothing hand-written is",
               "#   lost. This block SHRINKS as it is run -- it is not the clan block.",
               "# " + "-" * 72] + out
    return out


#: **Labels written onto items that ALREADY EXIST, per batch.** Emma, 2026-08-28: *"We are way
#: too gung ho about adding cjk labels to existing items. You may have noticed that I am
#: constantly removing them from the quickstatements. I consider them to be disruptive and
#: suspicion raising. imo any label changes should occur at the beginning of the batch and be
#: limited to a count of 15 labels added per batch."*
#:
#: **A label at CREATION time is not capped and is not counted.** Her distinction, same message:
#: *"a label added after item creation is a risk and a label added during item creation is good."*
#: So this counts only `Q… L…`/`Q… A…` lines, never `LAST L…`.
LABEL_EDIT_CAP = 15


def _cap_label_edits(lines, clan_block, corrections):
    """Move label edits on existing items to the FRONT and cut them to `LABEL_EDIT_CAP`.

    Both halves are hers. *"any label changes should occur at the beginning of the batch"* — so
    they lead the file rather than trailing 5,000 lines below, where she was scrolling to find
    them. *"limited to a count of 15 labels added per batch"* — so the rest wait for another day.

    **What this bites on, and the number is why it matters.** The batch was writing **2,192**
    label and alias lines onto **508** existing items; 1,947 of them are `CJK_CLAN_BLOCK`, which
    she hand-deleted from the last run in its entirety. At 15 a batch the clan block drains over
    many runs instead of arriving as a wall — which is what she asked for, not a compromise on it.

    **The block stays in the source, in full.** She restored it herself on 2026-08-29 — *"What the
    fuck the clan block is gone? Bring it the fuck back"* — after I deleted it by mistake. What is
    capped is how much of it goes out per run, not whether it exists. A repeat is a no-op, so the
    ones held back are simply emitted on a later day; nothing is lost and no state is needed.

    **Corrections go first within the cap.** `_label_corrections` fixes items whose label is still
    the birth name, which is a defect in what we already published; the clan block adds a label to
    an item that has none. Fixing something wrong outranks adding something missing.
    """
    # **What has already gone out, so the cap DRAINS instead of repeating.** Emma, 2026-08-29:
    # *"So I guess the clans thing will be saved and check which ones it was implemented on so
    # that it can limit it to 15 like this and same with other label edits."* Without this the
    # same first 15 lines are emitted every run and the remaining 2,177 never are.
    #
    # Keyed on `(qid, slot)` -- `Q10864996` + `Lnb` -- not on the value, so a re-worded label for
    # an item already done does not sneak past. `reports/label-edits-emitted.tsv` is tracked, one
    # row per edit, with the date it first went out.
    #
    # **It records what was EMITTED, not what Wikidata accepted.** If she does not run a batch,
    # those 15 do not come back on their own. That is the honest cost of a stateless cap becoming
    # a stateful one, and the recovery is to delete their rows from the file.
    done_path = ROOT / "reports" / "label-edits-emitted.tsv"
    done = set()
    if done_path.exists():
        for row in csv.DictReader(done_path.open(encoding="utf-8"), delimiter="	"):
            done.add((row["qid"], row["slot"]))
    newly = []

    def is_label_edit(ln):
        return bool(re.match(r"^Q[1-9][0-9]*	[LAD][a-z-]+	", ln))

    def take(source, budget, head, held):
        """Move this source's label edits into `head` while budget lasts; return what is left.

        Non-label lines pass through to `rest` untouched -- the additions pass emits `P22`,
        `P40` and the like beside its labels, and those are relationships, not labels, and are
        not capped by anything.
        """
        rest, pending = [], []
        for ln in source:
            if not ln.strip() or ln.lstrip().startswith("#"):
                pending.append(ln)
                continue
            if is_label_edit(ln):
                qid, slot = ln.split("	")[0], ln.split("	")[1]
                if (qid, slot) in done:
                    pending = []
                    continue
                if budget[0] <= 0:
                    held[0] += 1
                    pending = []
                    continue
                budget[0] -= 1
                done.add((qid, slot))
                newly.append((qid, slot, ln.split("	")[2].strip('"')))
                head.extend(pending)
                head.append(ln)
            else:
                rest.extend(pending)
                rest.append(ln)
            pending = []
        rest.extend(pending)
        return rest

    budget, held, head = [LABEL_EDIT_CAP], [0], []
    # Corrections first, then the clan block, then anything the rest of the batch emits onto an
    # existing item -- the additions pass writes `ja`/`zh` labels too, and capping only the two
    # hard-coded blocks left 664 label edits in the file when the cap is 15.
    take(corrections, budget, head, held)
    take(clan_block.splitlines(), budget, head, held)
    lines = take(lines, budget, head, held)

    if head:
        head = ["# " + "-" * 72,
                "# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at "
                f"{LABEL_EDIT_CAP}, both",
                "#   her instruction: \"any label changes should occur at the beginning of the",
                "#   batch and be limited to a count of 15 labels added per batch\". A label set",
                "#   at CREATION time is neither counted nor capped -- \"a label added during item",
                "#   creation is good\".",
                f"#   {held[0]} more are held for a later run; a repeat is a no-op, so nothing is lost.",
                "# " + "-" * 72] + head + [""]
    if newly:
        today = datetime.date.today().isoformat()
        fresh = not done_path.exists()
        with done_path.open("a", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            if fresh:
                w.writerow(["qid", "slot", "value", "first_emitted"])
            for qid, slot, value in newly:
                w.writerow([qid, slot, value, today])
    print(f"label edits on existing items: {LABEL_EDIT_CAP - budget[0]} emitted, {held[0]} held "
          f"for a later batch (cap {LABEL_EDIT_CAP}); "
          f"{len(done) - len(newly):,} already done in earlier batches")
    return head + lines


_ABBREV_EXPANSIONS = None


def expand_abbreviations(label, geni_id):
    """`Guri Pedersdtr. Foss` -> `Guri Pedersdatter Foss`.

    **Emma, 2026-08-27:** *"any abbreviations like -dtr (i.e. "Rasmusdtr." instead of
    "Rasmusdatter") should be fixd since wikidata mul labels ae supposed to have the full form.
    This is a part of the compliance stuff I mentioned earlier"*.

    **The expansion is per person, not per abbreviation**, and the corpus is what says so:
    `-dtr` is Norwegian `-datter` or Swedish `-dotter`, 81,530 against 57,085 overall, and the
    split reverses by stem — `Olsdtr` is `Olsdatter` 6,981 to 1,058 while `Andersdtr` is
    `Andersdotter` 5,172 to 3,126. A single global rule would be wrong several thousand times.

    `scripts/census-abbreviated-patronymics.py` decides each one and records **why** in a `basis`
    column: this person's own other `NAME` records first (588 of 10,923), the stem's corpus
    majority second (10,100), and her own example where the corpus knows nothing (235). This
    function only looks the answer up — the reasoning is in the CSV, where it can be read and
    disagreed with.

    Only **11** of the 10,923 are on people who already hold a Wikidata item, so this changes
    almost nothing today and everything about what future creations look like.
    """
    global _ABBREV_EXPANSIONS
    if _ABBREV_EXPANSIONS is None:
        _ABBREV_EXPANSIONS = {}
        path = ROOT / "reports" / "abbreviated-patronymics.csv"
        if path.exists():
            for row in csv.DictReader(path.open(encoding="utf-8")):
                _ABBREV_EXPANSIONS.setdefault(row["geni_id"], []).append(
                    (row["token"], row["expansion"]))
    out = label
    for token, expansion in _ABBREV_EXPANSIONS.get(geni_id, ()):
        # The census records the token without a trailing stop; the label may carry one, and
        # `Pedersdtr.Foss` -- no space -- occurs too, so replace the longest form first.
        for form in (token + ".", token):
            if form in out:
                out = out.replace(form, expansion)
                break
    return " ".join(out.split())


def without_nickname(label, fields):
    """`Ingvold (Pinkie) Remmie` → `Ingvold Remmie`. The nickname is a statement, not a label.

    **Emma, 2026-08-27, on `Q141199868`:** *"analyze https://www.wikidata.org/wiki/Q141199868 and
    why it came out as brackets instead of what it is supposed to be too"*. Geni records her as
    `Ingvold (Pinkie) /Remmie/` and the brackets went straight into `mul` and `en`.

    `CLAUDE.md` § *A nickname alias carries the SURNAME* is the rule and it is hers: a quoted token
    inside `GIVN` is `P1449` *nickname*, **not** a given name and not part of the label, and
    *"quotes never go in a label"*. `namemodel.QUOTED` already recognised both the quoted and the
    parenthesised form — but it is applied to the `GIVN` **field**, and the label is rendered
    separately, so the name statements were right while the label was wrong.

    **Read off the FIELD, never off the rendered label**, which is the trap `namemodel` records
    Emma catching once already: *"I thought we were resolving name objects but now we're determining
    which name field to use as a source of the label?"* Regexing the label directly matches the
    apostrophe in `Jean d'O Seigneur d'O` and would mangle French names — 27,211 labels match that
    way against **22,707** genuine nickname tokens in `GIVN` (16,742 parenthesised, 5,965 quoted).

    **Only spans that are in the label verbatim are removed.** The label may carry a married
    surname the `GIVN` field knows nothing about, so this deletes what it can find and leaves
    everything else alone rather than rebuilding the name.

    **The apostrophe guard here is gone, because `QUOTED` itself was fixed.** It used to accept
    any `'` as a delimiter, so `Jean d'O Seigneur d'O & de Maillebois` matched `'O Seigneur d'`
    and this returned `Jean d O & de Maillebois` — a French name destroyed to strip a nickname
    that was never there. The workaround was to ignore apostrophe matches in the label path only.
    That was wrong in the other direction: measured over `display-names.csv`, **963** apostrophe
    spans exist and most are real bynames — `Illugi svarte i Gilsbakki 'svarti'`,
    `Ivan II Ivanovich 'the Fair'` — so ignoring them stripped nothing that should have been
    stripped. `QUOTED` now distinguishes a delimiter from an elision, per Emma: *"d' can be an
    escaped substring lol"*, and every branch of it is trustworthy here.
    """
    if not label or not fields:
        return label
    from namemodel import QUOTED
    out = label
    for m in QUOTED.finditer(fields.get("givn") or ""):
        if m.group(0) in out:
            out = out.replace(m.group(0), " ")
    return " ".join(out.split())


def nn_form(raw):
    """`<private> Skårland` → `NN Skårland`; anything else is returned untouched.

    The reconstruction `CLAUDE.md` § *The NN/Private label algorithm applies to EVERY unnamed
    person* specifies: the marker goes, **the surname stays** because it survives redaction and
    is real data, and `NN` marks that the given name is withheld.

    **Extracted so the two callers cannot drift, which they had.** The `mul` line built this
    inline and was right — `NN Garborg`. `referred_to_as`, which is what `describe_all` names a
    relative by, did not, so a redacted *parent* leaked the marker into ten descriptive labels
    at once: `filla de <private> Skårland`, `datter af <private> Skårland`, and so on down the
    language table. The rule that a marker must not reach a label was being enforced on the
    person's own label and not on their child's.
    """
    low = (raw or "").lower()
    if "<private>" not in low and low.strip() not in ("private", "nn"):
        return raw
    surname = " ".join(t for t in (raw or "").split()
                       if not t.lower().startswith("<private")
                       and t.lower() not in ("private", "nn"))
    return ("NN " + surname).strip()


def _cjk_follows_mul(table):
    """`Lja`/`Lzh` for items whose CJK label was transliterated from a SUPERSEDED `mul`.

    **Emma, 2026-08-27, on `Q141180412`:** *"it appears that it has Japanese and presumably Chinese
    label that are no derived from the mul label like we wanted. Remember that the mul lable takes
    priority."*

    She is exactly right and the item shows it: `mul` and `en` read `Marta Rasmusdatter Li` while
    `ja` reads `マルタ・ラスムスダッテル・ヘーレ` and `zh` `玛尔塔·拉斯穆斯达特·赫勒` — **Helle**,
    a different surname. The CJK was derived when `mul` held the other form, `mul` later changed,
    and nothing brought the CJK with it.

    **`_label_corrections` cannot see this**, and that is the gap rather than a second opinion about
    it: that block fires only when the live `mul` differs from ours. Here `mul` *agrees*. So an item
    can be right in the two languages anyone reads and wrong in the two nobody checks.

    **The population is small and unambiguous: 24 items, 46 label rows**, measured over
    `reports/name-audit.csv` on 2026-08-29. Unambiguous because `mul` is agreed by *both* sides, so
    the CJK is not a judgement call — it follows from a string neither of us disputes. `CLAUDE.md`
    already records one of them, `Q141168785`, and rules on it: *"the stale half was ours, not
    hers."*

    **Reads the audit rather than re-fetching.** `scripts/audit-ledger-names.py` fetched all 508
    items live; doing it again inside every daily build would be eleven more requests a run for a
    number that moves slowly. The cost is that this is a **snapshot** — re-run the audit before
    trusting it after she has been editing.

    Everything here is a label edit on an existing item, so `LABEL_EDIT_CAP` governs how many
    actually go out; at 15 a batch these 46 drain in four runs.
    """
    audit = ROOT / "reports" / "name-audit.csv"
    if not audit.exists():
        return []
    out = []
    rows = {}
    for row in csv.DictReader(audit.open(encoding="utf-8")):
        rows.setdefault(row["qid"], {})[row["lang"]] = row
    for qid, by_lang in sorted(rows.items()):
        if (by_lang.get("mul") or {}).get("state") != "match":
            continue
        for lang in ("ja", "zh"):
            r = by_lang.get(lang)
            if not r or r["state"] != "differs" or not r["ours"]:
                continue
            out.append(f"#   {qid}: {lang} was transliterated from a superseded mul "
                       f"({r['wikidata']!r}); mul now says {by_lang['mul']['ours']!r}")
            out.append(f'{qid}	L{lang}	"{r["ours"]}"')
    if out:
        out = ["", "# " + "-" * 72,
               "# CJK FOLLOWS mul -- items whose ja/zh came from a mul that has since changed.",
               "#   Emma: \"the mul lable takes priority\". These are ours: mul is agreed by both",
               "#   sides, so the CJK is not a judgement call, it follows from it.",
               "#   Snapshot from reports/name-audit.csv -- re-run the audit after she edits.",
               "# " + "-" * 72] + out
    return out


def label_in(label, table):
    """(ja, zh) for a whole name, or (None, None) if any token is unknown.

    Partial is worse than absent: half a name in katakana and half in Latin is not a
    Japanese label, it is a broken one. **A middle initial is the one exception** —
    `labels.transliterate_token` keeps `F` as `F` in every script, per Emma 2026-08-27.
    """
    from labels import transliterate_token

    ja, zh = [], []
    for token, _usage, _o in classify(label):
        a, b = transliterate_token(token, table)
        if a is None:
            return None, None
        ja.append(a)
        zh.append(b)
    return "・".join(ja), "·".join(zh)


def name_lines(label, plan, geni_id, father_qid, fields=None, sex="",
               father_name=""):
    """`P735`/`P734`/`P5056` lines for one person, and what could not be emitted.

    **Only tokens whose item already exists.** A name item this run is creating
    cannot be pointed at, same single-run rule as everybody else, so the rest waits
    for `reports/wikidata-garborg-name-items.qs` to have been run.

    QuickStatements takes qualifiers exactly like references, property then value on
    the same line: `LAST<TAB>P735<TAB>Q629347<TAB>P1545<TAB>"1"<TAB>P7452<TAB>Q3409033`.
    """
    out, notes = [], []
    lines, why = statements_for(label, plan, geni_id, father_qid=father_qid,
                                fields=fields, sex=sex, father_name=father_name)
    for prop, value, quals in lines:
        # `P1449` *nickname* is monolingual TEXT, so QuickStatements wants a language
        # tag and quotes rather than a bare item id.
        rendered = f'en:"{value}"' if prop == NICKNAME else value
        parts = [f"LAST	{prop}	{rendered}"]
        for qprop, qvalue in quals:
            # A series ordinal is a string; everything else here is an item.
            qv = f'"{qvalue}"' if qprop == "P1545" else qvalue
            parts.append(f"{qprop}	{qv}")
        out.append("	".join(parts))
    notes.extend(why)
    return out, notes



# ---------------------------------------------------------------------------------
# THE BATCH COMPOSITION -- `docs/batch-rules.md`, dictated by Emma 2026-08-25 and
# clarified by her the same day.
#
# **The subgraph is Arne's component ON WIKIDATA, as it currently stands.** Not a radius
# over our Geni tree. Emma: *"Everyone within n hops of Arne as his family exists on
# wikidata."* Asked what `n` should be over our tree she said *"you misunderstand it
# completely if you're even asking the question"* -- and she is right: the ball is what
# the programme is building, so it is 42 items today and larger after every run. Each
# run draws its random work from what exists and enlarges the pool the next run draws
# from. That is what makes the thing self-bootstrapping and why it takes ~18 runs.
#
# This is also why Bure needs its own algorithm rather than a bigger `n`. Emma:
# *"bure is a bunch of unlinked people with entity resolutions to geni, so it isn't
# dense it's a different kind of area though which needs its own algorithm."* There the
# items already exist and carry `P2600`; the work is linking, not creating.
#
# One run is:
#
#   1. the spine couple  -- the next chain person and their spouse
#   2. 4 random sets of parents, drawn from the ball
#   3. 4 random families -- a solitary individual gets their spouse and children
#   4. 1 random existing couple -- all their children, properly linked
#   5. <=10 mutual sibling links, which the additions pass emits under SIBLING_CAP
#
# Every component reduces to *which people go in `frontier`*, because the emitter below
# already does labels, names, dates, sex, `S2600` references and the duplicate guard.
# Components 2-4 differ only in how the people are chosen.
#
# **Emma's own reading of component 4, replacing what the spec called "Arne's side":**
# *"this is just part of the add 4 sets of parents randomly in the neighborhood not its
# own thing. But one thing that is worth doing imo is randomly choose an existing couple
# and add all the children."*
#
# **Solitary means an item with no `P26` spouse and no `P40` child** -- her wording,
# *"Has an item and no SPOUSE or CHILD specifically"* -- and it explicitly counts the
# people our own earlier runs created, since a fresh `CREATE` starts with neither.

#: The two saved relationship paths that make up the spine, walked in order. Emma,
#: 2026-08-26: *"The ancestral couples between Bergitte, going from Arne to Bergitte to
#: Charlemagne, are always getting made."* Line 2 -- Bergitte down to her -- exists as a
#: saved path and holds **16 steps, none of which had a QID** when this was written, which
#: is the *"critical path going to me"* she doubted the last run produced. It did not.
#: **Three lines, and each is stored ANCESTOR-FIRST.** Emma, 2026-08-28: *"You understand that
#: we are supposed to be building a path from Bergitte to me, not from me to Bergitte? That is
#: a pretty significant difference."* The spine takes the first uncreated step of each path per
#: run, so the stored order decides which end it grows from. `bergitte-to-emma.tsv` is stored
#: Emma-first and is therefore REVERSED here; it had been walking outward from her, which is
#: why it took `Richard Wade Borsheim` every single run.

SPINE_PATHS = ("paths/charlemagne-to-arne-garborg.tsv", "paths/bergitte-to-emma.tsv",
               "paths/bureus-to-emma.tsv",
               #: **Arne → Signe, and Emma added it herself.** 2026-08-29: *"your path gets added
               #: starting at Arne and moving to Signe. Record this as another spine and wire it
               #: in."* 15 steps, built by `scripts/path-between.py --avoid Borsheim` because she
               #: asked for a route to Signe with **no Borsheim on it** — her married name is
               #: Borsheim, so the family it names is not the family the path may travel.
               #:
               #: Stored **Arne-first**, which is the direction she named, so it is NOT in
               #: `SPINE_REVERSED`: the walk takes the first uncreated step and grows outward from
               #: Arne toward Signe. Steps 1–4 already hold items, so it starts at step 5.
               #:
               #: **It is two steps longer than the route on her saved page and that is deliberate.**
               #: `paths/caroline-signe-borsheim-hoknes.tsv` reaches Signe in 13 by hopping
               #: `his sister` and `her sister` directly; `path-between.py` walks parent, child and
               #: spouse only, so it routes through the shared parent instead and names
               #: `Jon Olsen Heigre` and `Søren Sørenson Gjesdal`. Those two are real people who
               #: have to exist for the line to be continuous either way.
               "paths/arne-to-signe-no-borsheim.tsv")

#: Paths whose file runs Emma-first and must be walked from the far end.
SPINE_REVERSED = ("paths/bergitte-to-emma.tsv",)
SPINE_PATH = SPINE_PATHS[0]

#: **Her revised caps, 2026-08-26**, after stopping a run of 50 creations partway:
#: *"creating individuals with all of their children is just crazy talk... we essentially do
#: 10 parents, 10 spouses, and 10 children."* Then, revising in the same message, she folded
#: spouses into the children step -- *"spouses are only added through the 10 parents and 10
#: children... you go to a person, and then it adds a child... If the person has a childless
#: marriage, then it can generate their spouse instead. Otherwise, it generates their child,
#: and then the next run it generates the child's parent."*
#:
#: So there is **no independent spouse bucket**. The later revision wins over the earlier
#: "10 spouses", and the shape is two caps plus a substitution.
#: Arne Olaus Fjørtoft Garborg — the centre the whole programme is measured from.
ARNE_GENI = "6000000005607426327"

#: **Never emitted, in any position, ever.** Emma, 2026-08-27: *"I should not be in the
#: traversable graph and neither should any kitajima people."*
#:
#: The batch of 2026-08-27 created her parents and wrote a `P22` and a `P25` onto her own
#: item, which attached it to the 1,339,227-person component that
#: contains Charlemagne. Her Geni id reaches the builder through `paths/bergitte-to-emma.tsv`,
#: whose step 1 is her, so excluding her at one call site is not enough — this set is enforced
#: at source *and* asserted over the finished file before it is written.
NEVER_TOUCH_GENI = {
    # The Kitajima/Kitashima family -- 22 people. Emma, 2026-08-27: *"neither should any
    # kitajima people"*.  was created anyway on 2026-08-28, because the
    # exclusion covered her and nobody else.
    "6000000019459854230",
    "6000000227335008051",
    "6000000227335094894",
    "6000000227335131944",
    "6000000227335155963",
    "6000000227335224861",
    "6000000227335233864",
    "6000000227335299879",
    "6000000227335301867",
    "6000000227335324856",
    "6000000227335337887",
    "6000000227335339873",
    "6000000227335344839",
    "6000000227335360837",
    "6000000227335365856",
    "6000000227335365861",
    "6000000227335366839",
    "6000000227335376843",
    "6000000227335378827",
    "6000000227335393824",
    "6000000227335397826",
    "6000000227335402830",
    "6000000227335430822",
    "6000000227335430827",
}
NEVER_TOUCH_QID = {
    "Q135579416",
    "Q135579421",
    "Q135579425",
    "Q135579447",
    "Q135579457",
    "Q135579466",
    "Q135579475",
    "Q135579485",
    "Q135579488",
    "Q135579492",
    "Q135579497",
    "Q135579502",
    "Q135579503",
    "Q135579506",
    "Q135579509",
    "Q135579512",
    "Q135579513",
    "Q135579514",
    "Q135579516",
    "Q135579517",
}

CHILDREN_PER_RUN = 10
PARENTS_PER_RUN = 10

#: **Free parents, and they do not count against `PARENTS_PER_RUN`.** Her rolling rule:
#: *"if a child is present and it appears like they have a single mother or single father,
#: then the next time they get their parents for free. Parents that are added for this reason
#: do not count towards the total parents that we're adding."*
#:
#: A half-attached child is the structural wart the old algorithm left behind -- one parent
#: linked, the other never created -- so this closes them as it goes rather than accumulating
#: them. Capped anyway at a number far above what the corpus produces per run, because
#: "uncapped" is what she stopped the last run for; the cap is reported when it bites.
#: **Her formula, 2026-08-26: "10 free parents plus half of the remaining."** So of the
#: half-attached people eligible for one, the first ten are free and half of whatever is
#: left beyond ten comes too. It bounds the step without stalling the backlog: 17 eligible
#: gives 10 + 3 = 13, and the rest wait for the next run.
#:
#: Two earlier readings, both wrong and both hers to correct. A flat ceiling of 40 was mine.
#: Scoping it to this run's children alone gave 5, which under-serves a backlog she wants
#: worked down.
FREE_PARENTS_FREE = 10


def free_parent_budget(eligible):
    """`10 + (n - 10) // 2` -- ten free, then half the remainder."""
    return eligible if eligible <= FREE_PARENTS_FREE else (
        FREE_PARENTS_FREE + (eligible - FREE_PARENTS_FREE) // 2)


def spine_chain():
    """`[(step, geni_id, name)]` up the saved Geni relationship path, Arne first.

    `paths/charlemagne-to-arne-garborg.tsv` is the authority -- `CLAUDE.md` is explicit
    that `reports/charlemagne-route.csv` is a *different* descent that does not contain
    Bergitte, and that treating the two as one produced a wrong junction.
    """
    rows = [l.rstrip("\n").split("\t") for l in
            open(ROOT / SPINE_PATH, encoding="utf-8")
            if not l.startswith("#") and l.strip()]
    header, out = rows[0], []
    for r in rows[1:]:
        d = dict(zip(header, r))
        gid = re.sub(r"\D", "", d.get("note", ""))
        if gid:
            out.append((int(d["step"]), gid, d["name"]))
    return out


from qscomment import annotate  # noqa: E402


#: Arne Olaus Fjørtoft Garborg. The subgraph is measured from here.
ARNE_QID = "Q11959067"

#: **Johannes Bureus — the second root.** Emma, 2026-08-28: *"it is supposed to do this from
#: Johannes Bureus and Arne Garborg, subgraphs coming from both of them."* Her line to Bureus
#: runs through her mother's side and is captured in `paths/bureus-to-emma.tsv`; her line to
#: Arne runs through her father's. Two roots, one subgraph — the union of what each reaches.
BUREUS_QID = "Q633094"

def subgraph_roots():
    """**Arne, Bureus, and EVERY Bureätten person. 252 entry points, not 2.**

    **Emma, 2026-08-29:** *"My idea was that there would be 252 entry points into the graph,
    which would be all of the Bure people plus Arnie"*, and then, when told it was still two:
    *"YES THE BURE PEOPLE ARE ALL ENTRY POINS."*

    They were in the `universe` -- walkable *through* -- but not roots, so they only joined the
    subgraph if a walk from Arne or Bureus happened to land on them. **113 of the 251 are islands
    of exactly one person**, so they were unreachable by construction, and 2 of 251 were inside.

    **Her prediction was right and it is measured, not argued.** Two roots gave 284 Arne-side
    against 36 Bureus-side. All 252 gives 284 against 281 -- **50/50**, which is what she said
    it would be, for the reason she gave: the Bure people have far more entry points but each
    reaches almost nothing, so the extra 250 roots buy only ~245 people. Subgraph 316 -> 565,
    and 565 of 614 ledger people seed instead of 316.

    Read from `reports/bureatten.csv`, the sv.wikipedia Category:Bureätten listing, taking only
    rows that carry a Geni id -- the same 251 the coverage campaign used. Reading the file rather
    than pasting the ids keeps one list of these people in the repo.
    """
    roots = [ARNE_QID, BUREUS_QID]
    roster = ROOT / "reports" / "bureatten.csv"
    if roster.exists():
        with open(roster, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if (row.get("geni_ids") or "").strip() and row.get("qid"):
                    roots.append(row["qid"])
    return tuple(dict.fromkeys(roots))


SUBGRAPH_ROOTS = subgraph_roots()

#: **A KLUGE, and it is labelled one on purpose. Expires 2026-10-01.**
#:
#: **Emma, 2026-08-29:** *"A kluge is a specific programming thing which is designed to be an
#: unscalable fix to a problem that's meant to be operating temporarily. Simply, it blocks all
#: three of those people from being considered part of the universe until, let's say, October."*
#:
#: These three are her own Korean work -- Buyeo Deokjang and Buyeo Taebi are items she added a
#: `P2600` to, and the wife was minted by the ring on 2026-08-27 at 17:41, **41 minutes before
#: the subgraph gate landed** (`ebf88d64` 18:22, `5ddf8560` 18:52). The gate already stops that
#: recurring and none of the three is in the subgraph today. This is belt and braces over a
#: mechanism that is already fixed, which is exactly why it is a kluge and not a rule: it does
#: not scale, it names three people, and it is dated.
#:
#: It removes them from the **universe**, not merely from the roots -- so no walk may pass
#: *through* them either. That is the whole point: the worry is Korean princes being reached,
#: not their seeding.
KLUGE_UNIVERSE_BLOCK = ("Q19657284", "Q12598947", "Q141198548")

#: **The Asian people from the deleted `entity_resolution.md`, plus Ame no Hohi.**
#:
#: **Emma, 2026-08-29:** *"It's best to overinclude all the Asian people from the
#: entity_resolution.md file that were discussed earlier... The main thing would be Ame no
#: Houhi and some other stuff."* Her reason, in her words: *"the idea is nothing is supposed
#: to even know that I exist, but I'm a bit concerned that the existence is going to be
#: figured out by other things."*
#:
#: `entity_resolution.md` was deleted on 2026-08-29; this list was read back out of git
#: (`12f3134a^`) rather than reconstructed from memory. It held nine Wikidata items. Four are
#: already blocked -- Buyeo Deokjang and Buyeo Taebi above, Kitajima no Tokitaka `Q135579474`
#: and Kitajima no Yasutaka `Q135579480` through `NEVER_TOUCH_QID`. One is **her own item and
#: is deliberately left out**, on her instruction *"except for me"*. These are the remaining
#: four, plus Ame no Hohi.
#:
#: The first three are also the whole content of `exports/post-merge/wikidata-qid-links.ged`,
#: the bio-link GEDCOM, which is the other place these pairings live.
KLUGE_ENTITY_RESOLUTION_ASIA = (
    "Q11596350",    # 稚武彦命, geni 6000000001835522164
    "Q11078587",    # 播磨稲日大郎姫, geni 6000000001844033355
    "Q24890131",    # 物部伊莒弗 Mononobe, geni 6000000002039751362
    "Q11443857",    # 太媛 Futohime, geni 6000000001902786893
    # Ame no Hohi 天穂日命 -- the one she named aloud, and he is not in that file by QID.
    # Resolved offline against out/wikidata/labels.tsv, which carries him with the aliases
    # 天菩比神 / 天之菩卑能命 / 天穂日神 / アメノホヒ. He is the ancestor the Izumo line
    # descends from, so he is the doorway the Kitajima people would be reached through.
    "Q10940685",
)


def kluge_blocked_from_universe():
    """The kluge's full set: the three Buyeo people **and the 178 CJK clan individuals**.

    **Emma, 2026-08-29**, extending it: *"every single one of those clan individuals will
    mechanically not go into the universe until October"*, and, drawing the line herself,
    *"we probably are going to be changing their labelling in September, but being in the
    universe is not going to happen until October."*

    So this blocks **universe membership only**. It does not touch labelling: `CJK_CLAN_BLOCK`
    is emitted through `_cap_label_edits` and never consults the subgraph, so the 15-a-day
    label drip is unaffected and September's labelling can proceed exactly as planned.

    The clan QIDs are read out of `CJK_CLAN_BLOCK` rather than restated, so the two cannot
    drift apart -- there is one list of these people in this file, not two.
    """
    clan = set(re.findall(r"^(Q\d+)", CJK_CLAN_BLOCK, re.M))

    # **Emma, 2026-08-29:** *"just add every single kitajima person into the klug too. It's
    # better to include more people in it."*  So the Kitajima/Kitashima family joins, taken
    # from `NEVER_TOUCH_QID` rather than restated.
    #
    # **Her own item is deliberately NOT here, and is no longer named anywhere in this repo.**
    # Emma, 2026-08-29: *"my QID should be nonexistent in the repository... It shouldn't be in
    # the repo at all, simple as that."* `NEVER_TOUCH_QID` used to hold it alongside
    # them, and she is not a Kitajima -- blocking her from the universe is a separate decision
    # about her own duplicates, which is hers to make and not implied by this instruction.
    #
    # The 25 ids in `NEVER_TOUCH_GENI` add nothing: **0 of them resolve to a QID** in
    # `out/wikidata/p2600-all.tsv`, because these items carry no `P2600` at all -- which is
    # the same blind spot that let them be created in the first place.
    kitajima = set(NEVER_TOUCH_QID)

    return (set(KLUGE_UNIVERSE_BLOCK) | set(KLUGE_ENTITY_RESOLUTION_ASIA)
            | clan | kitajima)

#: The date the block above stops applying. After this, `wikidata_subgraph` ignores it.
KLUGE_UNIVERSE_BLOCK_EXPIRES = datetime.date(2026, 10, 1)

#: The relationship properties that make two Wikidata items neighbours in the subgraph.
#: P22 father, P25 mother, P26 spouse, P40 child, P3373 sibling.
SUBGRAPH_PROPS = ("P22", "P25", "P26", "P40", "P3373")


def wikidata_subgraph(roots=SUBGRAPH_ROOTS, universe=None):
    """The connected group reachable from Arne and Bureus **through items Emma has edited**.

    **Emma, 2026-08-28:** *"my algorithm is entirely based on anyone on the continuous subgraph
    currently on wikidata from Arne"*, then *"it is supposed to do this from Johannes Bureus and
    Arne Garborg, subgraphs coming from both of them"*, and — the sentence that decides the
    shape — *"The subgraph is stored and added to with my contributions."*

    **The walk is restricted to her own items.** Unrestricted it is not a neighbourhood: Bureus
    `Q633094` sits in Wikidata's 1,339,227-item genealogical component, so following every
    `P22`/`P25`/`P26`/`P40`/`P3373` from him reaches **1.34 million** people and the ring becomes
    the whole world tree. She listed the humans she has edited that are *outside* the contiguous
    group — Buyeo Taebi `Q12598947`, Cecilie Ebbesdatter `Q116150300`, Buyeo Deokjang
    `Q19657284`, Jon Jonsen `Q116150298`, Cecilie Jonsdatter `Q141189062`, Tøre Jonsen
    `Q141189110`, Lave `Q141189080` — and the unrestricted walk puts four of those seven *inside*
    it, which is how the mistake was caught.

    So `universe` is the ledger: her items, plus the two roots. An edge counts only when both
    ends are hers. That is what makes the group grow *with her contributions* rather than
    swallow Wikidata the moment one of her items touches the world tree.

    Two edge sources, because neither is current alone: the bulk `out/wikidata/relations.tsv`,
    which predates most of her edits, and `reports/garborg-live-values.tsv`, refreshed each run.
    """
    universe = set(universe or ()) | set(roots)
    if datetime.date.today() < KLUGE_UNIVERSE_BLOCK_EXPIRES:
        universe -= kluge_blocked_from_universe()
    adj = collections.defaultdict(set)

    def link(a, b):
        if a in universe and b in universe:
            adj[a].add(b)
            adj[b].add(a)

    rel = ROOT / "out" / "wikidata" / "relations.tsv"
    if rel.exists():
        with open(rel, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="	"):
                q = row["qid"]
                if q not in universe:
                    continue
                for col in ("p22", "p25", "p40", "p26"):
                    for v in (row.get(col) or "").split("|"):
                        v = v.strip()
                        if v.startswith("Q"):
                            link(q, v)
    live = ROOT / "reports" / "garborg-live-values.tsv"
    if live.exists():
        with open(live, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="	"):
                if row["property"] in SUBGRAPH_PROPS and row["value"].startswith("Q"):
                    link(row["qid"], row["value"])

    seen = set(roots)
    stack = list(seen)
    while stack:
        for other in adj[stack.pop()]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return seen


def _carries_marker(label):
    """True when any token of the label is an unknown-name marker.

    Shares `scripts/labels`' vocabulary, so a marker added there is detected here with no
    second list to keep in step. Case-folded, because Geni writes `nn`, `Nn` and `NN`.
    """
    from labels import NARROW_MARKERS, WORDS_MEANING_UNKNOWN
    markers = NARROW_MARKERS | WORDS_MEANING_UNKNOWN
    return any(tok.casefold().strip(".,") in markers for tok in (label or "").split())


def _strip_markers(label):
    """`labels.strip_markers`, imported lazily — `scripts/` is on the path only at runtime."""
    from labels import strip_markers
    return strip_markers(label)


#: **Appended verbatim to the end of every batch. Hard-coded on purpose. Do not generalise it.**
#:
#: Emma, 2026-08-27, asking for exactly this and warning against what would otherwise happen to
#: it: *"I have the biggest kludge of a solution: every quickstatement batch just adds these qids
#: at the end... literally, there is a block of text with the quick statements hard-coded into
#: the end of it. They stay in forever, adding the QIDs every single time."*
#:
#: **These are manual zipper merges.** Each line says *this Wikidata item is that Geni person*.
#: The daily algorithm needs those eight pairings to exist on Wikidata for the Charlemagne chain
#: to link up, and the work depending on it is due within about a week. Until the statement is on
#: the item, the pairing lives only in `reports/garborg-qids.tsv`, where nothing outside this
#: repo can see it and a ledger rebuild would lose it.
#:
#: **It is self-healing by being stupid.** The first run that reaches an item adds the statement;
#: every run after that adds a duplicate, which QuickStatements merges away. Eight no-op lines a
#: day, no state, no check, no dated logic. When the eight are done, delete the block.
#:
#: **Her explicit fear, recorded because it is the likely failure:** *"My fear with asking you to
#: do this thing is that you are going to decide to over-engineer this into something that takes
#: a gazillion years to make and has a high likelihood of later on being repurposed into
#: something that's actively harmful... If you get any clever ideas about making it more
#: scalable, then it's going to get shot down."* So: no lookup, no filtering, no *only emit if
#: absent*, no reading it from a file. A literal string.
#:
#: **European only.** She ruled the Asian identifications out: *"for the Asian people I'm going
#: to say no... the Asian people are long-term and there are potential concerns."*
SPINE_P2600_BLOCK = """
# ---------------------------------------------------------------------------
# MANUAL ZIPPER MERGES -- hard-coded, appended to every batch, on purpose.
#
# Each line asserts that an existing Wikidata item IS a particular Geni person.
#
# Eight are on the Arne -> Charlemagne chain. Their items exist and are
# well documented, but carry no P2600 Geni.com profile ID, so nothing outside
# this repo records the correspondence and the chain cannot be followed on
# Wikidata. The daily algorithm depends on these pairings.
#
# They repeat every run by design. The first run that reaches an item adds the
# statement; every later run adds a duplicate, which QuickStatements merges away.
# That is the whole mechanism -- no state, no checking, no cleverness. When all
# eight are on Wikidata, delete this block.
#
# Evidence for each is in reports/wikidata-spine-add-p2600.qs: every one is
# anchored on a DIFFERENT relative that already carries a recorded P2600, never
# on a name match. Two were accepted by Emma on 2026-08-26.
# ---------------------------------------------------------------------------
#   Q5915800 Knut Algotsson: P2600 Geni.com profile ID
Q5915800\tP2600\t"6000000002572699392"
#   Q101247444 Ingegerd Svantepolksdotter: P2600 Geni.com profile ID
Q101247444\tP2600\t"6000000011239201122"
#   Q6197518 Svantepolk Knutsson Viby: P2600 Geni.com profile ID
Q6197518\tP2600\t"6000000003418900347"
#   Q3743799 Knut Valdemarsson, Duke of Estland: P2600 Geni.com profile ID
Q3743799\tP2600\t"6000000003076221220"
#   Q4953376 Helena Guttormsdatter: P2600 Geni.com profile ID
Q4953376\tP2600\t"6000000034013672054"
#   Q466257 Rozala of Italy: P2600 Geni.com profile ID
Q466257\tP2600\t"4258970970100070152"
#   Q274606 Berengar I, emperor of the Romans: P2600 Geni.com profile ID
Q274606\tP2600\t"6000000001669654269"
#   Q284400 Gisele of Cysoing: P2600 Geni.com profile ID
Q284400\tP2600\t"6000000000424624719"
#
#   Q10411463 Andreas Olai: P2600 Geni.com profile ID.  Emma, 2026-08-28:
#   "we add this qid geni id add thing to the quickstatements block that
#   always gets added in".  Identified during the mass export campaign by
#   STRUCTURE, never by name: the Geni profile reads "Son of Olof, Brother of
#   Kerstin Olofsdotter and Benedictus Olai", and the item carries P3373
#   sibling -> Q4355463 Benedictus Olai.  Its About text gives 1521-1560,
#   matching the item's P569 date of birth and P570 date of death exactly.
#   The structured Birth field is the trap -- it says "estimated between 1450
#   and 1570", which is why the pairing looked unmakeable.  Emma put P1889
#   different from on the item to separate him from the better-known
#   Andreas Olai, so the name alone could never have settled this.
Q10411463\tP2600\t"6000000040951562251"
"""


#: **The CJK clan labels, hard-coded and appended to every batch, exactly like
#: `SPINE_P2600_BLOCK`.** Emma, 2026-08-28: *"Fucking wire it in"*, after the formula was
#: worked out on `Q10864996` and measured across the population.
#:
#: 177 people, 1,947 statement lines. Larger than the `P2600` block by two orders of
#: magnitude, and the same mechanism for the same reason: the first run that reaches an
#: item sets the labels, every run after that sets them to what they already say, and
#: QuickStatements makes that a no-op. No state, no check, no conditional. Delete the
#: block when the 177 are done.
#:
#: Built by `scripts/build-cjk-clan-labels.py` from `reports/cjk-clan-labels.tsv` and
#: pasted here as a literal. It is not read from the file at run time on purpose — the
#: same reason the `P2600` block is a literal.
CJK_CLAN_BLOCK = """
# -------------------------------------------------------------------------
# CJK CLAN LABELS -- hard-coded, appended to every batch, on purpose.
#
# Geni records these people as a marker, a place and a clan:
#   GIVN 某 (unknown-name marker) / SURN 隴西狄道 (a PLACE) / _MARNM 李 (the clan).
# 348 of 354 records have that shape and every _MARNM is one character, so the
# married-name field holds the real surname and the surname field holds a place.
#
# Emma, 2026-08-28: "this formulation should be 'woman of the Li clan, from Longxi
# Didao' as the English label and all languages have a similar thing but NN is the
# right mul". Sex comes from the data -- 169 of these 177 are men.
#
# ONLY EMPTY LABEL SLOTS ARE WRITTEN. A label REPLACES, and her other ruling is that
# Wikidata wins where it already knows a name: `en` is occupied on all 177 (Q10864996
# reads "Wanshou") and `nl` on all 177, so neither is touched here. mul is empty on
# all 177; es on 84 of them.
#
# ja and zh are absent on purpose -- the idiomatic Chinese form is a question about
# Chinese rather than about this data.
#
# Repeats every run: setting a label to what it already says is a no-op. Delete when
# the 177 are done.
# -------------------------------------------------------------------------
#   Q10864996 (李 of 隴西狄道): mul label = NN
Q10864996	Lmul	"NN"
#   Q10864996: set the nb label
Q10864996	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q10864996: set the da label
Q10864996	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q10864996: set the sv label
Q10864996	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q10864996: set the de label
Q10864996	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q10864996: set the it label
Q10864996	Lit	"donna del clan Li, da Longxi Didao"
#   Q10864996: set the pt label
Q10864996	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q10864996: set the ca label
Q10864996	Lca	"dona del clan Li, de Longxi Didao"
#   Q10881168 (李 of 隴西狄道): mul label = NN
Q10881168	Lmul	"NN"
#   Q10881168: set the nb label
Q10881168	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q10881168: set the da label
Q10881168	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q10881168: set the sv label
Q10881168	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q10881168: set the de label
Q10881168	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q10881168: set the it label
Q10881168	Lit	"donna del clan Li, da Longxi Didao"
#   Q10881168: set the pt label
Q10881168	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q10881168: set the ca label
Q10881168	Lca	"dona del clan Li, de Longxi Didao"
#   Q11064679 (李 of 隴西狄道): mul label = NN
Q11064679	Lmul	"NN"
#   Q11064679: set the nb label
Q11064679	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q11064679: set the da label
Q11064679	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q11064679: set the sv label
Q11064679	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q11064679: set the de label
Q11064679	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q11064679: set the it label
Q11064679	Lit	"donna del clan Li, da Longxi Didao"
#   Q11064679: set the pt label
Q11064679	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q11064679: set the ca label
Q11064679	Lca	"dona del clan Li, de Longxi Didao"
#   Q11098137 (李 of 河南府): mul label = NN
Q11098137	Lmul	"NN"
#   Q11098137: set the nb label
Q11098137	Lnb	"mann av Li-slekten, fra Henan Prefecture"
#   Q11098137: set the da label
Q11098137	Lda	"mand af Li-slægten, fra Henan Prefecture"
#   Q11098137: set the sv label
Q11098137	Lsv	"man av Li-ätten, från Henan Prefecture"
#   Q11098137: set the de label
Q11098137	Lde	"Mann des Klans Li, aus Henan Prefecture"
#   Q11098137: set the es label
Q11098137	Les	"hombre del clan Li, de Henan Prefecture"
#   Q11098137: set the it label
Q11098137	Lit	"uomo del clan Li, da Henan Prefecture"
#   Q11098137: set the pt label
Q11098137	Lpt	"homem do clã Li, de Henan Prefecture"
#   Q11098137: set the ca label
Q11098137	Lca	"home del clan Li, de Henan Prefecture"
#   Q11110062 (柳 of 河東解縣): mul label = NN
Q11110062	Lmul	"NN"
#   Q11110062: set the nb label
Q11110062	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q11110062: set the da label
Q11110062	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q11110062: set the sv label
Q11110062	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q11110062: set the de label
Q11110062	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q11110062: set the it label
Q11110062	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q11110062: set the pt label
Q11110062	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q11110062: set the ca label
Q11110062	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q11180129 (李 of 隴西狄道): mul label = NN
Q11180129	Lmul	"NN"
#   Q11180129: set the nb label
Q11180129	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q11180129: set the da label
Q11180129	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q11180129: set the sv label
Q11180129	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q11180129: set the de label
Q11180129	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q11180129: set the es label
Q11180129	Les	"mujer del clan Li, de Longxi Didao"
#   Q11180129: set the it label
Q11180129	Lit	"donna del clan Li, da Longxi Didao"
#   Q11180129: set the pt label
Q11180129	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q11180129: set the ca label
Q11180129	Lca	"dona del clan Li, de Longxi Didao"
#   Q15954845 (李 of ): mul label = NN
Q15954845	Lmul	"NN"
#   Q15954845: set the nb label
Q15954845	Lnb	"kvinne av Li-slekten"
#   Q15954845: set the da label
Q15954845	Lda	"kvinde af Li-slægten"
#   Q15954845: set the sv label
Q15954845	Lsv	"kvinna av Li-ätten"
#   Q15954845: set the de label
Q15954845	Lde	"Frau des Klans Li"
#   Q15954845: set the es label
Q15954845	Les	"mujer del clan Li"
#   Q15954845: set the it label
Q15954845	Lit	"donna del clan Li"
#   Q15954845: set the pt label
Q15954845	Lpt	"mulher do clã Li"
#   Q15954845: set the ca label
Q15954845	Lca	"dona del clan Li"
#   Q16603665 (李 of 隴西狄道): mul label = NN
Q16603665	Lmul	"NN"
#   Q16603665: set the nb label
Q16603665	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q16603665: set the da label
Q16603665	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q16603665: set the sv label
Q16603665	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q16603665: set the de label
Q16603665	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q16603665: set the es label
Q16603665	Les	"mujer del clan Li, de Longxi Didao"
#   Q16603665: set the it label
Q16603665	Lit	"donna del clan Li, da Longxi Didao"
#   Q16603665: set the pt label
Q16603665	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q16603665: set the ca label
Q16603665	Lca	"dona del clan Li, de Longxi Didao"
#   Q18908886 (韋 of 京兆杜陵): mul label = NN
Q18908886	Lmul	"NN"
#   Q18908886: set the nb label
Q18908886	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q18908886: set the da label
Q18908886	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q18908886: set the sv label
Q18908886	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q18908886: set the de label
Q18908886	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q18908886: set the it label
Q18908886	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q18908886: set the pt label
Q18908886	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q18908886: set the ca label
Q18908886	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45420125 (權 of 秦州清水): mul label = NN
Q45420125	Lmul	"NN"
#   Q45420125: set the nb label
Q45420125	Lnb	"mann av Quan-slekten, fra Qinzhou Qingshui"
#   Q45420125: set the da label
Q45420125	Lda	"mand af Quan-slægten, fra Qinzhou Qingshui"
#   Q45420125: set the sv label
Q45420125	Lsv	"man av Quan-ätten, från Qinzhou Qingshui"
#   Q45420125: set the de label
Q45420125	Lde	"Mann des Klans Quan, aus Qinzhou Qingshui"
#   Q45420125: set the it label
Q45420125	Lit	"uomo del clan Quan, da Qinzhou Qingshui"
#   Q45420125: set the pt label
Q45420125	Lpt	"homem do clã Quan, de Qinzhou Qingshui"
#   Q45420125: set the ca label
Q45420125	Lca	"home del clan Quan, de Qinzhou Qingshui"
#   Q45421489 (崔 of 深州安平): mul label = NN
Q45421489	Lmul	"NN"
#   Q45421489: set the nb label
Q45421489	Lnb	"mann av Cui-slekten, fra Shenzhou Anping"
#   Q45421489: set the da label
Q45421489	Lda	"mand af Cui-slægten, fra Shenzhou Anping"
#   Q45421489: set the sv label
Q45421489	Lsv	"man av Cui-ätten, från Shenzhou Anping"
#   Q45421489: set the de label
Q45421489	Lde	"Mann des Klans Cui, aus Shenzhou Anping"
#   Q45421489: set the it label
Q45421489	Lit	"uomo del clan Cui, da Shenzhou Anping"
#   Q45421489: set the pt label
Q45421489	Lpt	"homem do clã Cui, de Shenzhou Anping"
#   Q45421489: set the ca label
Q45421489	Lca	"home del clan Cui, de Shenzhou Anping"
#   Q45422231 (柳 of 河東解縣): mul label = NN
Q45422231	Lmul	"NN"
#   Q45422231: set the nb label
Q45422231	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45422231: set the da label
Q45422231	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45422231: set the sv label
Q45422231	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45422231: set the de label
Q45422231	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45422231: set the it label
Q45422231	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45422231: set the pt label
Q45422231	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45422231: set the ca label
Q45422231	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45429773 (韋 of 襄州穀城): mul label = NN
Q45429773	Lmul	"NN"
#   Q45429773: set the nb label
Q45429773	Lnb	"mann av Wei-slekten, fra Xiangzhou Gucheng"
#   Q45429773: set the da label
Q45429773	Lda	"mand af Wei-slægten, fra Xiangzhou Gucheng"
#   Q45429773: set the sv label
Q45429773	Lsv	"man av Wei-ätten, från Xiangzhou Gucheng"
#   Q45429773: set the de label
Q45429773	Lde	"Mann des Klans Wei, aus Xiangzhou Gucheng"
#   Q45429773: set the it label
Q45429773	Lit	"uomo del clan Wei, da Xiangzhou Gucheng"
#   Q45429773: set the pt label
Q45429773	Lpt	"homem do clã Wei, de Xiangzhou Gucheng"
#   Q45429773: set the ca label
Q45429773	Lca	"home del clan Wei, de Xiangzhou Gucheng"
#   Q45448943 (蕭 of 蘭陵): mul label = NN
Q45448943	Lmul	"NN"
#   Q45448943: set the nb label
Q45448943	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45448943: set the da label
Q45448943	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45448943: set the sv label
Q45448943	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45448943: set the de label
Q45448943	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45448943: set the it label
Q45448943	Lit	"uomo del clan Xiao, da Lanling"
#   Q45448943: set the pt label
Q45448943	Lpt	"homem do clã Xiao, de Lanling"
#   Q45448943: set the ca label
Q45448943	Lca	"home del clan Xiao, de Lanling"
#   Q45449130 (蕭 of 蘭陵): mul label = NN
Q45449130	Lmul	"NN"
#   Q45449130: set the nb label
Q45449130	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45449130: set the da label
Q45449130	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45449130: set the sv label
Q45449130	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45449130: set the de label
Q45449130	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45449130: set the it label
Q45449130	Lit	"uomo del clan Xiao, da Lanling"
#   Q45449130: set the pt label
Q45449130	Lpt	"homem do clã Xiao, de Lanling"
#   Q45449130: set the ca label
Q45449130	Lca	"home del clan Xiao, de Lanling"
#   Q45450462 (韋 of 京兆萬年): mul label = NN
Q45450462	Lmul	"NN"
#   Q45450462: set the nb label
Q45450462	Lnb	"mann av Wei-slekten, fra Jingzhao Wannian"
#   Q45450462: set the da label
Q45450462	Lda	"mand af Wei-slægten, fra Jingzhao Wannian"
#   Q45450462: set the sv label
Q45450462	Lsv	"man av Wei-ätten, från Jingzhao Wannian"
#   Q45450462: set the de label
Q45450462	Lde	"Mann des Klans Wei, aus Jingzhao Wannian"
#   Q45450462: set the it label
Q45450462	Lit	"uomo del clan Wei, da Jingzhao Wannian"
#   Q45450462: set the pt label
Q45450462	Lpt	"homem do clã Wei, de Jingzhao Wannian"
#   Q45450462: set the ca label
Q45450462	Lca	"home del clan Wei, de Jingzhao Wannian"
#   Q45450834 (蕭 of 蘭陵): mul label = NN
Q45450834	Lmul	"NN"
#   Q45450834: set the nb label
Q45450834	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45450834: set the da label
Q45450834	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45450834: set the sv label
Q45450834	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45450834: set the de label
Q45450834	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45450834: set the it label
Q45450834	Lit	"uomo del clan Xiao, da Lanling"
#   Q45450834: set the pt label
Q45450834	Lpt	"homem do clã Xiao, de Lanling"
#   Q45450834: set the ca label
Q45450834	Lca	"home del clan Xiao, de Lanling"
#   Q45453968 (韋 of 京兆杜陵): mul label = NN
Q45453968	Lmul	"NN"
#   Q45453968: set the nb label
Q45453968	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45453968: set the da label
Q45453968	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45453968: set the sv label
Q45453968	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45453968: set the de label
Q45453968	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45453968: set the it label
Q45453968	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45453968: set the pt label
Q45453968	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45453968: set the ca label
Q45453968	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45461450 (崔 of 清河東武城): mul label = NN
Q45461450	Lmul	"NN"
#   Q45461450: set the nb label
Q45461450	Lnb	"mann av Cui-slekten, fra Qinghe Dongwucheng"
#   Q45461450: set the da label
Q45461450	Lda	"mand af Cui-slægten, fra Qinghe Dongwucheng"
#   Q45461450: set the sv label
Q45461450	Lsv	"man av Cui-ätten, från Qinghe Dongwucheng"
#   Q45461450: set the de label
Q45461450	Lde	"Mann des Klans Cui, aus Qinghe Dongwucheng"
#   Q45461450: set the it label
Q45461450	Lit	"uomo del clan Cui, da Qinghe Dongwucheng"
#   Q45461450: set the pt label
Q45461450	Lpt	"homem do clã Cui, de Qinghe Dongwucheng"
#   Q45461450: set the ca label
Q45461450	Lca	"home del clan Cui, de Qinghe Dongwucheng"
#   Q45469083 (李 of 隴西狄道): mul label = NN
Q45469083	Lmul	"NN"
#   Q45469083: set the nb label
Q45469083	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45469083: set the da label
Q45469083	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45469083: set the sv label
Q45469083	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45469083: set the de label
Q45469083	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45469083: set the it label
Q45469083	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45469083: set the pt label
Q45469083	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45469083: set the ca label
Q45469083	Lca	"home del clan Li, de Longxi Didao"
#   Q45471981 (李 of 隴西狄道): mul label = NN
Q45471981	Lmul	"NN"
#   Q45471981: set the nb label
Q45471981	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45471981: set the da label
Q45471981	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45471981: set the sv label
Q45471981	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45471981: set the de label
Q45471981	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45471981: set the es label
Q45471981	Les	"hombre del clan Li, de Longxi Didao"
#   Q45471981: set the it label
Q45471981	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45471981: set the pt label
Q45471981	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45471981: set the ca label
Q45471981	Lca	"home del clan Li, de Longxi Didao"
#   Q45472107 (李 of 隴西狄道): mul label = NN
Q45472107	Lmul	"NN"
#   Q45472107: set the nb label
Q45472107	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45472107: set the da label
Q45472107	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45472107: set the sv label
Q45472107	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45472107: set the de label
Q45472107	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45472107: set the es label
Q45472107	Les	"hombre del clan Li, de Longxi Didao"
#   Q45472107: set the it label
Q45472107	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45472107: set the pt label
Q45472107	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45472107: set the ca label
Q45472107	Lca	"home del clan Li, de Longxi Didao"
#   Q45473385 (李 of 隴西狄道): mul label = NN
Q45473385	Lmul	"NN"
#   Q45473385: set the nb label
Q45473385	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45473385: set the da label
Q45473385	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45473385: set the sv label
Q45473385	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45473385: set the de label
Q45473385	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45473385: set the es label
Q45473385	Les	"hombre del clan Li, de Longxi Didao"
#   Q45473385: set the it label
Q45473385	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45473385: set the pt label
Q45473385	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45473385: set the ca label
Q45473385	Lca	"home del clan Li, de Longxi Didao"
#   Q45474359 (李 of 隴西狄道): mul label = NN
Q45474359	Lmul	"NN"
#   Q45474359: set the nb label
Q45474359	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45474359: set the da label
Q45474359	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45474359: set the sv label
Q45474359	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45474359: set the de label
Q45474359	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45474359: set the es label
Q45474359	Les	"hombre del clan Li, de Longxi Didao"
#   Q45474359: set the it label
Q45474359	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45474359: set the pt label
Q45474359	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45474359: set the ca label
Q45474359	Lca	"home del clan Li, de Longxi Didao"
#   Q45481279 (李 of 隴西狄道): mul label = NN
Q45481279	Lmul	"NN"
#   Q45481279: set the nb label
Q45481279	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45481279: set the da label
Q45481279	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45481279: set the sv label
Q45481279	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45481279: set the de label
Q45481279	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45481279: set the es label
Q45481279	Les	"hombre del clan Li, de Longxi Didao"
#   Q45481279: set the it label
Q45481279	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45481279: set the pt label
Q45481279	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45481279: set the ca label
Q45481279	Lca	"home del clan Li, de Longxi Didao"
#   Q45484623 (崔 of 河南): mul label = NN
Q45484623	Lmul	"NN"
#   Q45484623: set the nb label
Q45484623	Lnb	"mann av Cui-slekten, fra Henan"
#   Q45484623: set the da label
Q45484623	Lda	"mand af Cui-slægten, fra Henan"
#   Q45484623: set the sv label
Q45484623	Lsv	"man av Cui-ätten, från Henan"
#   Q45484623: set the de label
Q45484623	Lde	"Mann des Klans Cui, aus Henan"
#   Q45484623: set the it label
Q45484623	Lit	"uomo del clan Cui, da Henan"
#   Q45484623: set the pt label
Q45484623	Lpt	"homem do clã Cui, de Henan"
#   Q45484623: set the ca label
Q45484623	Lca	"home del clan Cui, de Henan"
#   Q45484673 (陳 of 吳興長城): mul label = NN
Q45484673	Lmul	"NN"
#   Q45484673: set the nb label
Q45484673	Lnb	"mann av Chen-slekten, fra Wuxing Changcheng"
#   Q45484673: set the da label
Q45484673	Lda	"mand af Chen-slægten, fra Wuxing Changcheng"
#   Q45484673: set the sv label
Q45484673	Lsv	"man av Chen-ätten, från Wuxing Changcheng"
#   Q45484673: set the de label
Q45484673	Lde	"Mann des Klans Chen, aus Wuxing Changcheng"
#   Q45484673: set the it label
Q45484673	Lit	"uomo del clan Chen, da Wuxing Changcheng"
#   Q45484673: set the pt label
Q45484673	Lpt	"homem do clã Chen, de Wuxing Changcheng"
#   Q45484673: set the ca label
Q45484673	Lca	"home del clan Chen, de Wuxing Changcheng"
#   Q45484869 (陳 of 昇州江寧): mul label = NN
Q45484869	Lmul	"NN"
#   Q45484869: set the nb label
Q45484869	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484869: set the da label
Q45484869	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484869: set the sv label
Q45484869	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484869: set the de label
Q45484869	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484869: set the it label
Q45484869	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484869: set the pt label
Q45484869	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484869: set the ca label
Q45484869	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484932 (陳 of 昇州江寧): mul label = NN
Q45484932	Lmul	"NN"
#   Q45484932: set the nb label
Q45484932	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484932: set the da label
Q45484932	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484932: set the sv label
Q45484932	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484932: set the de label
Q45484932	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484932: set the it label
Q45484932	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484932: set the pt label
Q45484932	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484932: set the ca label
Q45484932	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45484995 (陳 of 昇州江寧): mul label = NN
Q45484995	Lmul	"NN"
#   Q45484995: set the nb label
Q45484995	Lnb	"mann av Chen-slekten, fra Shengzhou Jiangning"
#   Q45484995: set the da label
Q45484995	Lda	"mand af Chen-slægten, fra Shengzhou Jiangning"
#   Q45484995: set the sv label
Q45484995	Lsv	"man av Chen-ätten, från Shengzhou Jiangning"
#   Q45484995: set the de label
Q45484995	Lde	"Mann des Klans Chen, aus Shengzhou Jiangning"
#   Q45484995: set the it label
Q45484995	Lit	"uomo del clan Chen, da Shengzhou Jiangning"
#   Q45484995: set the pt label
Q45484995	Lpt	"homem do clã Chen, de Shengzhou Jiangning"
#   Q45484995: set the ca label
Q45484995	Lca	"home del clan Chen, de Shengzhou Jiangning"
#   Q45485126 (陳 of 京兆長安): mul label = NN
Q45485126	Lmul	"NN"
#   Q45485126: set the nb label
Q45485126	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485126: set the da label
Q45485126	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485126: set the sv label
Q45485126	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485126: set the de label
Q45485126	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485126: set the it label
Q45485126	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485126: set the pt label
Q45485126	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485126: set the ca label
Q45485126	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485317 (陳 of 京兆長安): mul label = NN
Q45485317	Lmul	"NN"
#   Q45485317: set the nb label
Q45485317	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485317: set the da label
Q45485317	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485317: set the sv label
Q45485317	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485317: set the de label
Q45485317	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485317: set the it label
Q45485317	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485317: set the pt label
Q45485317	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485317: set the ca label
Q45485317	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485382 (陳 of 京兆長安): mul label = NN
Q45485382	Lmul	"NN"
#   Q45485382: set the nb label
Q45485382	Lnb	"mann av Chen-slekten, fra Jingzhao Chang'an"
#   Q45485382: set the da label
Q45485382	Lda	"mand af Chen-slægten, fra Jingzhao Chang'an"
#   Q45485382: set the sv label
Q45485382	Lsv	"man av Chen-ätten, från Jingzhao Chang'an"
#   Q45485382: set the de label
Q45485382	Lde	"Mann des Klans Chen, aus Jingzhao Chang'an"
#   Q45485382: set the it label
Q45485382	Lit	"uomo del clan Chen, da Jingzhao Chang'an"
#   Q45485382: set the pt label
Q45485382	Lpt	"homem do clã Chen, de Jingzhao Chang'an"
#   Q45485382: set the ca label
Q45485382	Lca	"home del clan Chen, de Jingzhao Chang'an"
#   Q45485462 (李 of 隴西狄道): mul label = NN
Q45485462	Lmul	"NN"
#   Q45485462: set the nb label
Q45485462	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45485462: set the da label
Q45485462	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45485462: set the sv label
Q45485462	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45485462: set the de label
Q45485462	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45485462: set the es label
Q45485462	Les	"hombre del clan Li, de Longxi Didao"
#   Q45485462: set the it label
Q45485462	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45485462: set the pt label
Q45485462	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45485462: set the ca label
Q45485462	Lca	"home del clan Li, de Longxi Didao"
#   Q45485716 (裴 of 河東聞喜): mul label = NN
Q45485716	Lmul	"NN"
#   Q45485716: set the nb label
Q45485716	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45485716: set the da label
Q45485716	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45485716: set the sv label
Q45485716	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45485716: set the de label
Q45485716	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45485716: set the it label
Q45485716	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45485716: set the pt label
Q45485716	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45485716: set the ca label
Q45485716	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45486474 (蕭 of ): mul label = NN
Q45486474	Lmul	"NN"
#   Q45486474: set the nb label
Q45486474	Lnb	"mann av Xiao-slekten"
#   Q45486474: set the da label
Q45486474	Lda	"mand af Xiao-slægten"
#   Q45486474: set the sv label
Q45486474	Lsv	"man av Xiao-ätten"
#   Q45486474: set the de label
Q45486474	Lde	"Mann des Klans Xiao"
#   Q45486474: set the it label
Q45486474	Lit	"uomo del clan Xiao"
#   Q45486474: set the pt label
Q45486474	Lpt	"homem do clã Xiao"
#   Q45486474: set the ca label
Q45486474	Lca	"home del clan Xiao"
#   Q45486525 (陳 of 湖州長城): mul label = NN
Q45486525	Lmul	"NN"
#   Q45486525: set the nb label
Q45486525	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486525: set the da label
Q45486525	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486525: set the sv label
Q45486525	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486525: set the de label
Q45486525	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486525: set the it label
Q45486525	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486525: set the pt label
Q45486525	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486525: set the ca label
Q45486525	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45486588 (陳 of 湖州長城): mul label = NN
Q45486588	Lmul	"NN"
#   Q45486588: set the nb label
Q45486588	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486588: set the da label
Q45486588	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486588: set the sv label
Q45486588	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486588: set the de label
Q45486588	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486588: set the it label
Q45486588	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486588: set the pt label
Q45486588	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486588: set the ca label
Q45486588	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45486909 (陳 of 湖州長城): mul label = NN
Q45486909	Lmul	"NN"
#   Q45486909: set the nb label
Q45486909	Lnb	"mann av Chen-slekten, fra Huzhou Changcheng"
#   Q45486909: set the da label
Q45486909	Lda	"mand af Chen-slægten, fra Huzhou Changcheng"
#   Q45486909: set the sv label
Q45486909	Lsv	"man av Chen-ätten, från Huzhou Changcheng"
#   Q45486909: set the de label
Q45486909	Lde	"Mann des Klans Chen, aus Huzhou Changcheng"
#   Q45486909: set the it label
Q45486909	Lit	"uomo del clan Chen, da Huzhou Changcheng"
#   Q45486909: set the pt label
Q45486909	Lpt	"homem do clã Chen, de Huzhou Changcheng"
#   Q45486909: set the ca label
Q45486909	Lca	"home del clan Chen, de Huzhou Changcheng"
#   Q45497731 (盧 of 潤州丹陽): mul label = NN
Q45497731	Lmul	"NN"
#   Q45497731: set the nb label
Q45497731	Lnb	"mann av Lu-slekten, fra Runzhou Danyang"
#   Q45497731: set the da label
Q45497731	Lda	"mand af Lu-slægten, fra Runzhou Danyang"
#   Q45497731: set the sv label
Q45497731	Lsv	"man av Lu-ätten, från Runzhou Danyang"
#   Q45497731: set the de label
Q45497731	Lde	"Mann des Klans Lu, aus Runzhou Danyang"
#   Q45497731: set the es label
Q45497731	Les	"hombre del clan Lu, de Runzhou Danyang"
#   Q45497731: set the it label
Q45497731	Lit	"uomo del clan Lu, da Runzhou Danyang"
#   Q45497731: set the pt label
Q45497731	Lpt	"homem do clã Lu, de Runzhou Danyang"
#   Q45497731: set the ca label
Q45497731	Lca	"home del clan Lu, de Runzhou Danyang"
#   Q45501359 (楊 of 弘農華陰): mul label = NN
Q45501359	Lmul	"NN"
#   Q45501359: set the nb label
Q45501359	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45501359: set the da label
Q45501359	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45501359: set the sv label
Q45501359	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45501359: set the de label
Q45501359	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45501359: set the it label
Q45501359	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45501359: set the pt label
Q45501359	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45501359: set the ca label
Q45501359	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45501424 (楊 of 弘農華陰): mul label = NN
Q45501424	Lmul	"NN"
#   Q45501424: set the nb label
Q45501424	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45501424: set the da label
Q45501424	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45501424: set the sv label
Q45501424	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45501424: set the de label
Q45501424	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45501424: set the it label
Q45501424	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45501424: set the pt label
Q45501424	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45501424: set the ca label
Q45501424	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45502571 (李 of 隴西狄道): mul label = NN
Q45502571	Lmul	"NN"
#   Q45502571: set the nb label
Q45502571	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45502571: set the da label
Q45502571	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45502571: set the sv label
Q45502571	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45502571: set the de label
Q45502571	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45502571: set the es label
Q45502571	Les	"hombre del clan Li, de Longxi Didao"
#   Q45502571: set the it label
Q45502571	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45502571: set the pt label
Q45502571	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45502571: set the ca label
Q45502571	Lca	"home del clan Li, de Longxi Didao"
#   Q45502705 (楊 of 弘農華陰): mul label = NN
Q45502705	Lmul	"NN"
#   Q45502705: set the nb label
Q45502705	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45502705: set the da label
Q45502705	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45502705: set the sv label
Q45502705	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45502705: set the de label
Q45502705	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45502705: set the it label
Q45502705	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45502705: set the pt label
Q45502705	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45502705: set the ca label
Q45502705	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45503478 (楊 of 弘農華陰): mul label = NN
Q45503478	Lmul	"NN"
#   Q45503478: set the nb label
Q45503478	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45503478: set the da label
Q45503478	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45503478: set the sv label
Q45503478	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45503478: set the de label
Q45503478	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45503478: set the it label
Q45503478	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45503478: set the pt label
Q45503478	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45503478: set the ca label
Q45503478	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45503541 (楊 of 弘農華陰): mul label = NN
Q45503541	Lmul	"NN"
#   Q45503541: set the nb label
Q45503541	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45503541: set the da label
Q45503541	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45503541: set the sv label
Q45503541	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45503541: set the de label
Q45503541	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45503541: set the it label
Q45503541	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45503541: set the pt label
Q45503541	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45503541: set the ca label
Q45503541	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45507781 (柳 of 河東解縣): mul label = NN
Q45507781	Lmul	"NN"
#   Q45507781: set the nb label
Q45507781	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45507781: set the da label
Q45507781	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45507781: set the sv label
Q45507781	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45507781: set the de label
Q45507781	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45507781: set the it label
Q45507781	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45507781: set the pt label
Q45507781	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45507781: set the ca label
Q45507781	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45508685 (楊 of 弘農華陰): mul label = NN
Q45508685	Lmul	"NN"
#   Q45508685: set the nb label
Q45508685	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45508685: set the da label
Q45508685	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45508685: set the sv label
Q45508685	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45508685: set the de label
Q45508685	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45508685: set the it label
Q45508685	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45508685: set the pt label
Q45508685	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45508685: set the ca label
Q45508685	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45508942 (楊 of 弘農華陰): mul label = NN
Q45508942	Lmul	"NN"
#   Q45508942: set the nb label
Q45508942	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45508942: set the da label
Q45508942	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45508942: set the sv label
Q45508942	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45508942: set the de label
Q45508942	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45508942: set the it label
Q45508942	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45508942: set the pt label
Q45508942	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45508942: set the ca label
Q45508942	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45509891 (楊 of 弘農華陰): mul label = NN
Q45509891	Lmul	"NN"
#   Q45509891: set the nb label
Q45509891	Lnb	"mann av Yang-slekten, fra Hongnong Huayin"
#   Q45509891: set the da label
Q45509891	Lda	"mand af Yang-slægten, fra Hongnong Huayin"
#   Q45509891: set the sv label
Q45509891	Lsv	"man av Yang-ätten, från Hongnong Huayin"
#   Q45509891: set the de label
Q45509891	Lde	"Mann des Klans Yang, aus Hongnong Huayin"
#   Q45509891: set the it label
Q45509891	Lit	"uomo del clan Yang, da Hongnong Huayin"
#   Q45509891: set the pt label
Q45509891	Lpt	"homem do clã Yang, de Hongnong Huayin"
#   Q45509891: set the ca label
Q45509891	Lca	"home del clan Yang, de Hongnong Huayin"
#   Q45510761 (柳 of 河東解縣): mul label = NN
Q45510761	Lmul	"NN"
#   Q45510761: set the nb label
Q45510761	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510761: set the da label
Q45510761	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510761: set the sv label
Q45510761	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510761: set the de label
Q45510761	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510761: set the it label
Q45510761	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510761: set the pt label
Q45510761	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510761: set the ca label
Q45510761	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45510826 (柳 of 河東解縣): mul label = NN
Q45510826	Lmul	"NN"
#   Q45510826: set the nb label
Q45510826	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510826: set the da label
Q45510826	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510826: set the sv label
Q45510826	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510826: set the de label
Q45510826	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510826: set the it label
Q45510826	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510826: set the pt label
Q45510826	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510826: set the ca label
Q45510826	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45510888 (柳 of 河東解縣): mul label = NN
Q45510888	Lmul	"NN"
#   Q45510888: set the nb label
Q45510888	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45510888: set the da label
Q45510888	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45510888: set the sv label
Q45510888	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45510888: set the de label
Q45510888	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45510888: set the it label
Q45510888	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45510888: set the pt label
Q45510888	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45510888: set the ca label
Q45510888	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511272 (柳 of 河東解縣): mul label = NN
Q45511272	Lmul	"NN"
#   Q45511272: set the nb label
Q45511272	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511272: set the da label
Q45511272	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511272: set the sv label
Q45511272	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511272: set the de label
Q45511272	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511272: set the it label
Q45511272	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511272: set the pt label
Q45511272	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511272: set the ca label
Q45511272	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511461 (柳 of 河東解縣): mul label = NN
Q45511461	Lmul	"NN"
#   Q45511461: set the nb label
Q45511461	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511461: set the da label
Q45511461	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511461: set the sv label
Q45511461	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511461: set the de label
Q45511461	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511461: set the it label
Q45511461	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511461: set the pt label
Q45511461	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511461: set the ca label
Q45511461	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45511905 (柳 of 河東解縣): mul label = NN
Q45511905	Lmul	"NN"
#   Q45511905: set the nb label
Q45511905	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45511905: set the da label
Q45511905	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45511905: set the sv label
Q45511905	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45511905: set the de label
Q45511905	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45511905: set the it label
Q45511905	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45511905: set the pt label
Q45511905	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45511905: set the ca label
Q45511905	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45512915 (柳 of 河東解縣): mul label = NN
Q45512915	Lmul	"NN"
#   Q45512915: set the nb label
Q45512915	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45512915: set the da label
Q45512915	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45512915: set the sv label
Q45512915	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45512915: set the de label
Q45512915	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45512915: set the it label
Q45512915	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45512915: set the pt label
Q45512915	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45512915: set the ca label
Q45512915	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45513489 (柳 of 河東解縣): mul label = NN
Q45513489	Lmul	"NN"
#   Q45513489: set the nb label
Q45513489	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45513489: set the da label
Q45513489	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45513489: set the sv label
Q45513489	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45513489: set the de label
Q45513489	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45513489: set the it label
Q45513489	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45513489: set the pt label
Q45513489	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45513489: set the ca label
Q45513489	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45513552 (柳 of 河東解縣): mul label = NN
Q45513552	Lmul	"NN"
#   Q45513552: set the nb label
Q45513552	Lnb	"mann av Liu-slekten, fra Hedong Jiexian"
#   Q45513552: set the da label
Q45513552	Lda	"mand af Liu-slægten, fra Hedong Jiexian"
#   Q45513552: set the sv label
Q45513552	Lsv	"man av Liu-ätten, från Hedong Jiexian"
#   Q45513552: set the de label
Q45513552	Lde	"Mann des Klans Liu, aus Hedong Jiexian"
#   Q45513552: set the it label
Q45513552	Lit	"uomo del clan Liu, da Hedong Jiexian"
#   Q45513552: set the pt label
Q45513552	Lpt	"homem do clã Liu, de Hedong Jiexian"
#   Q45513552: set the ca label
Q45513552	Lca	"home del clan Liu, de Hedong Jiexian"
#   Q45517450 (房 of 齊州臨淄): mul label = NN
Q45517450	Lmul	"NN"
#   Q45517450: set the nb label
Q45517450	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517450: set the da label
Q45517450	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517450: set the sv label
Q45517450	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517450: set the de label
Q45517450	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517450: set the it label
Q45517450	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517450: set the pt label
Q45517450	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517450: set the ca label
Q45517450	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517515 (房 of 齊州臨淄): mul label = NN
Q45517515	Lmul	"NN"
#   Q45517515: set the nb label
Q45517515	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517515: set the da label
Q45517515	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517515: set the sv label
Q45517515	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517515: set the de label
Q45517515	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517515: set the it label
Q45517515	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517515: set the pt label
Q45517515	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517515: set the ca label
Q45517515	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517579 (房 of 齊州臨淄): mul label = NN
Q45517579	Lmul	"NN"
#   Q45517579: set the nb label
Q45517579	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517579: set the da label
Q45517579	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517579: set the sv label
Q45517579	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517579: set the de label
Q45517579	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517579: set the it label
Q45517579	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517579: set the pt label
Q45517579	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517579: set the ca label
Q45517579	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517644 (房 of 齊州臨淄): mul label = NN
Q45517644	Lmul	"NN"
#   Q45517644: set the nb label
Q45517644	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45517644: set the da label
Q45517644	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45517644: set the sv label
Q45517644	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45517644: set the de label
Q45517644	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45517644: set the it label
Q45517644	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45517644: set the pt label
Q45517644	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45517644: set the ca label
Q45517644	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45517670 (李 of 隴西狄道): mul label = NN
Q45517670	Lmul	"NN"
#   Q45517670: set the nb label
Q45517670	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q45517670: set the da label
Q45517670	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q45517670: set the sv label
Q45517670	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q45517670: set the de label
Q45517670	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q45517670: set the es label
Q45517670	Les	"mujer del clan Li, de Longxi Didao"
#   Q45517670: set the it label
Q45517670	Lit	"donna del clan Li, da Longxi Didao"
#   Q45517670: set the pt label
Q45517670	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q45517670: set the ca label
Q45517670	Lca	"dona del clan Li, de Longxi Didao"
#   Q45518351 (房 of 齊州臨淄): mul label = NN
Q45518351	Lmul	"NN"
#   Q45518351: set the nb label
Q45518351	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45518351: set the da label
Q45518351	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45518351: set the sv label
Q45518351	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45518351: set the de label
Q45518351	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45518351: set the it label
Q45518351	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45518351: set the pt label
Q45518351	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45518351: set the ca label
Q45518351	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45518415 (房 of 齊州臨淄): mul label = NN
Q45518415	Lmul	"NN"
#   Q45518415: set the nb label
Q45518415	Lnb	"mann av Fang-slekten, fra Qizhou Linzi"
#   Q45518415: set the da label
Q45518415	Lda	"mand af Fang-slægten, fra Qizhou Linzi"
#   Q45518415: set the sv label
Q45518415	Lsv	"man av Fang-ätten, från Qizhou Linzi"
#   Q45518415: set the de label
Q45518415	Lde	"Mann des Klans Fang, aus Qizhou Linzi"
#   Q45518415: set the it label
Q45518415	Lit	"uomo del clan Fang, da Qizhou Linzi"
#   Q45518415: set the pt label
Q45518415	Lpt	"homem do clã Fang, de Qizhou Linzi"
#   Q45518415: set the ca label
Q45518415	Lca	"home del clan Fang, de Qizhou Linzi"
#   Q45521650 (李 of 隴西狄道): mul label = NN
Q45521650	Lmul	"NN"
#   Q45521650: set the nb label
Q45521650	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45521650: set the da label
Q45521650	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45521650: set the sv label
Q45521650	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45521650: set the de label
Q45521650	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45521650: set the es label
Q45521650	Les	"hombre del clan Li, de Longxi Didao"
#   Q45521650: set the it label
Q45521650	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45521650: set the pt label
Q45521650	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45521650: set the ca label
Q45521650	Lca	"home del clan Li, de Longxi Didao"
#   Q45534434 (李 of 隴西狄道): mul label = NN
Q45534434	Lmul	"NN"
#   Q45534434: set the nb label
Q45534434	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45534434: set the da label
Q45534434	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45534434: set the sv label
Q45534434	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45534434: set the de label
Q45534434	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45534434: set the es label
Q45534434	Les	"hombre del clan Li, de Longxi Didao"
#   Q45534434: set the it label
Q45534434	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45534434: set the pt label
Q45534434	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45534434: set the ca label
Q45534434	Lca	"home del clan Li, de Longxi Didao"
#   Q45534750 (鄭 of 鄭州榮澤): mul label = NN
Q45534750	Lmul	"NN"
#   Q45534750: set the nb label
Q45534750	Lnb	"mann av Zheng-slekten, fra Zhengzhou Rongze"
#   Q45534750: set the da label
Q45534750	Lda	"mand af Zheng-slægten, fra Zhengzhou Rongze"
#   Q45534750: set the sv label
Q45534750	Lsv	"man av Zheng-ätten, från Zhengzhou Rongze"
#   Q45534750: set the de label
Q45534750	Lde	"Mann des Klans Zheng, aus Zhengzhou Rongze"
#   Q45534750: set the it label
Q45534750	Lit	"uomo del clan Zheng, da Zhengzhou Rongze"
#   Q45534750: set the pt label
Q45534750	Lpt	"homem do clã Zheng, de Zhengzhou Rongze"
#   Q45534750: set the ca label
Q45534750	Lca	"home del clan Zheng, de Zhengzhou Rongze"
#   Q45536767 (杜 of 京兆杜陵): mul label = NN
Q45536767	Lmul	"NN"
#   Q45536767: set the nb label
Q45536767	Lnb	"mann av Du-slekten, fra Jingzhao Duling"
#   Q45536767: set the da label
Q45536767	Lda	"mand af Du-slægten, fra Jingzhao Duling"
#   Q45536767: set the sv label
Q45536767	Lsv	"man av Du-ätten, från Jingzhao Duling"
#   Q45536767: set the de label
Q45536767	Lde	"Mann des Klans Du, aus Jingzhao Duling"
#   Q45536767: set the es label
Q45536767	Les	"hombre del clan Du, de Jingzhao Duling"
#   Q45536767: set the it label
Q45536767	Lit	"uomo del clan Du, da Jingzhao Duling"
#   Q45536767: set the pt label
Q45536767	Lpt	"homem do clã Du, de Jingzhao Duling"
#   Q45536767: set the ca label
Q45536767	Lca	"home del clan Du, de Jingzhao Duling"
#   Q45536832 (杜 of 京兆杜陵): mul label = NN
Q45536832	Lmul	"NN"
#   Q45536832: set the nb label
Q45536832	Lnb	"mann av Du-slekten, fra Jingzhao Duling"
#   Q45536832: set the da label
Q45536832	Lda	"mand af Du-slægten, fra Jingzhao Duling"
#   Q45536832: set the sv label
Q45536832	Lsv	"man av Du-ätten, från Jingzhao Duling"
#   Q45536832: set the de label
Q45536832	Lde	"Mann des Klans Du, aus Jingzhao Duling"
#   Q45536832: set the es label
Q45536832	Les	"hombre del clan Du, de Jingzhao Duling"
#   Q45536832: set the it label
Q45536832	Lit	"uomo del clan Du, da Jingzhao Duling"
#   Q45536832: set the pt label
Q45536832	Lpt	"homem do clã Du, de Jingzhao Duling"
#   Q45536832: set the ca label
Q45536832	Lca	"home del clan Du, de Jingzhao Duling"
#   Q45541151 (李 of 隴西狄道): mul label = NN
Q45541151	Lmul	"NN"
#   Q45541151: set the nb label
Q45541151	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45541151: set the da label
Q45541151	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45541151: set the sv label
Q45541151	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45541151: set the de label
Q45541151	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45541151: set the es label
Q45541151	Les	"hombre del clan Li, de Longxi Didao"
#   Q45541151: set the it label
Q45541151	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45541151: set the pt label
Q45541151	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45541151: set the ca label
Q45541151	Lca	"home del clan Li, de Longxi Didao"
#   Q45542682 (李 of 隴西狄道): mul label = NN
Q45542682	Lmul	"NN"
#   Q45542682: set the nb label
Q45542682	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45542682: set the da label
Q45542682	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45542682: set the sv label
Q45542682	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45542682: set the de label
Q45542682	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45542682: set the es label
Q45542682	Les	"hombre del clan Li, de Longxi Didao"
#   Q45542682: set the it label
Q45542682	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45542682: set the pt label
Q45542682	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45542682: set the ca label
Q45542682	Lca	"home del clan Li, de Longxi Didao"
#   Q45544329 (李 of 隴西狄道): mul label = NN
Q45544329	Lmul	"NN"
#   Q45544329: set the nb label
Q45544329	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45544329: set the da label
Q45544329	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45544329: set the sv label
Q45544329	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45544329: set the de label
Q45544329	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45544329: set the es label
Q45544329	Les	"hombre del clan Li, de Longxi Didao"
#   Q45544329: set the it label
Q45544329	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45544329: set the pt label
Q45544329	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45544329: set the ca label
Q45544329	Lca	"home del clan Li, de Longxi Didao"
#   Q45553927 (李 of 京兆長安): mul label = NN
Q45553927	Lmul	"NN"
#   Q45553927: set the nb label
Q45553927	Lnb	"mann av Li-slekten, fra Jingzhao Chang'an"
#   Q45553927: set the da label
Q45553927	Lda	"mand af Li-slægten, fra Jingzhao Chang'an"
#   Q45553927: set the sv label
Q45553927	Lsv	"man av Li-ätten, från Jingzhao Chang'an"
#   Q45553927: set the de label
Q45553927	Lde	"Mann des Klans Li, aus Jingzhao Chang'an"
#   Q45553927: set the es label
Q45553927	Les	"hombre del clan Li, de Jingzhao Chang'an"
#   Q45553927: set the it label
Q45553927	Lit	"uomo del clan Li, da Jingzhao Chang'an"
#   Q45553927: set the pt label
Q45553927	Lpt	"homem do clã Li, de Jingzhao Chang'an"
#   Q45553927: set the ca label
Q45553927	Lca	"home del clan Li, de Jingzhao Chang'an"
#   Q45556055 (李 of 河南洛陽): mul label = NN
Q45556055	Lmul	"NN"
#   Q45556055: set the nb label
Q45556055	Lnb	"mann av Li-slekten, fra Henan Luoyang"
#   Q45556055: set the da label
Q45556055	Lda	"mand af Li-slægten, fra Henan Luoyang"
#   Q45556055: set the sv label
Q45556055	Lsv	"man av Li-ätten, från Henan Luoyang"
#   Q45556055: set the de label
Q45556055	Lde	"Mann des Klans Li, aus Henan Luoyang"
#   Q45556055: set the es label
Q45556055	Les	"hombre del clan Li, de Henan Luoyang"
#   Q45556055: set the it label
Q45556055	Lit	"uomo del clan Li, da Henan Luoyang"
#   Q45556055: set the pt label
Q45556055	Lpt	"homem do clã Li, de Henan Luoyang"
#   Q45556055: set the ca label
Q45556055	Lca	"home del clan Li, de Henan Luoyang"
#   Q45557842 (崔 of 貝州清河): mul label = NN
Q45557842	Lmul	"NN"
#   Q45557842: set the nb label
Q45557842	Lnb	"mann av Cui-slekten, fra Beizhou Qinghe"
#   Q45557842: set the da label
Q45557842	Lda	"mand af Cui-slægten, fra Beizhou Qinghe"
#   Q45557842: set the sv label
Q45557842	Lsv	"man av Cui-ätten, från Beizhou Qinghe"
#   Q45557842: set the de label
Q45557842	Lde	"Mann des Klans Cui, aus Beizhou Qinghe"
#   Q45557842: set the it label
Q45557842	Lit	"uomo del clan Cui, da Beizhou Qinghe"
#   Q45557842: set the pt label
Q45557842	Lpt	"homem do clã Cui, de Beizhou Qinghe"
#   Q45557842: set the ca label
Q45557842	Lca	"home del clan Cui, de Beizhou Qinghe"
#   Q45562647 (裴 of 京兆萬年): mul label = NN
Q45562647	Lmul	"NN"
#   Q45562647: set the nb label
Q45562647	Lnb	"mann av Pei-slekten, fra Jingzhao Wannian"
#   Q45562647: set the da label
Q45562647	Lda	"mand af Pei-slægten, fra Jingzhao Wannian"
#   Q45562647: set the sv label
Q45562647	Lsv	"man av Pei-ätten, från Jingzhao Wannian"
#   Q45562647: set the de label
Q45562647	Lde	"Mann des Klans Pei, aus Jingzhao Wannian"
#   Q45562647: set the it label
Q45562647	Lit	"uomo del clan Pei, da Jingzhao Wannian"
#   Q45562647: set the pt label
Q45562647	Lpt	"homem do clã Pei, de Jingzhao Wannian"
#   Q45562647: set the ca label
Q45562647	Lca	"home del clan Pei, de Jingzhao Wannian"
#   Q45562711 (裴 of 河東聞喜): mul label = NN
Q45562711	Lmul	"NN"
#   Q45562711: set the nb label
Q45562711	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45562711: set the da label
Q45562711	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45562711: set the sv label
Q45562711	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45562711: set the de label
Q45562711	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45562711: set the it label
Q45562711	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45562711: set the pt label
Q45562711	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45562711: set the ca label
Q45562711	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45562775 (裴 of 河東聞喜): mul label = NN
Q45562775	Lmul	"NN"
#   Q45562775: set the nb label
Q45562775	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45562775: set the da label
Q45562775	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45562775: set the sv label
Q45562775	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45562775: set the de label
Q45562775	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45562775: set the it label
Q45562775	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45562775: set the pt label
Q45562775	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45562775: set the ca label
Q45562775	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45570419 (李 of 京兆萬年): mul label = NN
Q45570419	Lmul	"NN"
#   Q45570419: set the nb label
Q45570419	Lnb	"mann av Li-slekten, fra Jingzhao Wannian"
#   Q45570419: set the da label
Q45570419	Lda	"mand af Li-slægten, fra Jingzhao Wannian"
#   Q45570419: set the sv label
Q45570419	Lsv	"man av Li-ätten, från Jingzhao Wannian"
#   Q45570419: set the de label
Q45570419	Lde	"Mann des Klans Li, aus Jingzhao Wannian"
#   Q45570419: set the es label
Q45570419	Les	"hombre del clan Li, de Jingzhao Wannian"
#   Q45570419: set the it label
Q45570419	Lit	"uomo del clan Li, da Jingzhao Wannian"
#   Q45570419: set the pt label
Q45570419	Lpt	"homem do clã Li, de Jingzhao Wannian"
#   Q45570419: set the ca label
Q45570419	Lca	"home del clan Li, de Jingzhao Wannian"
#   Q45570482 (李 of 京兆萬年): mul label = NN
Q45570482	Lmul	"NN"
#   Q45570482: set the nb label
Q45570482	Lnb	"mann av Li-slekten, fra Jingzhao Wannian"
#   Q45570482: set the da label
Q45570482	Lda	"mand af Li-slægten, fra Jingzhao Wannian"
#   Q45570482: set the sv label
Q45570482	Lsv	"man av Li-ätten, från Jingzhao Wannian"
#   Q45570482: set the de label
Q45570482	Lde	"Mann des Klans Li, aus Jingzhao Wannian"
#   Q45570482: set the es label
Q45570482	Les	"hombre del clan Li, de Jingzhao Wannian"
#   Q45570482: set the it label
Q45570482	Lit	"uomo del clan Li, da Jingzhao Wannian"
#   Q45570482: set the pt label
Q45570482	Lpt	"homem do clã Li, de Jingzhao Wannian"
#   Q45570482: set the ca label
Q45570482	Lca	"home del clan Li, de Jingzhao Wannian"
#   Q45574741 (李 of 趙州贊皇): mul label = NN
Q45574741	Lmul	"NN"
#   Q45574741: set the nb label
Q45574741	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45574741: set the da label
Q45574741	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45574741: set the sv label
Q45574741	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45574741: set the de label
Q45574741	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45574741: set the es label
Q45574741	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45574741: set the it label
Q45574741	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45574741: set the pt label
Q45574741	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45574741: set the ca label
Q45574741	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45574802 (李 of 趙州贊皇): mul label = NN
Q45574802	Lmul	"NN"
#   Q45574802: set the nb label
Q45574802	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45574802: set the da label
Q45574802	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45574802: set the sv label
Q45574802	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45574802: set the de label
Q45574802	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45574802: set the es label
Q45574802	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45574802: set the it label
Q45574802	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45574802: set the pt label
Q45574802	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45574802: set the ca label
Q45574802	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45583513 (鄭 of 滎陽開封): mul label = NN
Q45583513	Lmul	"NN"
#   Q45583513: set the nb label
Q45583513	Lnb	"mann av Zheng-slekten, fra Xingyang Kaifeng"
#   Q45583513: set the da label
Q45583513	Lda	"mand af Zheng-slægten, fra Xingyang Kaifeng"
#   Q45583513: set the sv label
Q45583513	Lsv	"man av Zheng-ätten, från Xingyang Kaifeng"
#   Q45583513: set the de label
Q45583513	Lde	"Mann des Klans Zheng, aus Xingyang Kaifeng"
#   Q45583513: set the it label
Q45583513	Lit	"uomo del clan Zheng, da Xingyang Kaifeng"
#   Q45583513: set the pt label
Q45583513	Lpt	"homem do clã Zheng, de Xingyang Kaifeng"
#   Q45583513: set the ca label
Q45583513	Lca	"home del clan Zheng, de Xingyang Kaifeng"
#   Q45600896 (陸 of 吳郡吳縣): mul label = NN
Q45600896	Lmul	"NN"
#   Q45600896: set the nb label
Q45600896	Lnb	"mann av Lu-slekten, fra Wujun Wuxian"
#   Q45600896: set the da label
Q45600896	Lda	"mand af Lu-slægten, fra Wujun Wuxian"
#   Q45600896: set the sv label
Q45600896	Lsv	"man av Lu-ätten, från Wujun Wuxian"
#   Q45600896: set the de label
Q45600896	Lde	"Mann des Klans Lu, aus Wujun Wuxian"
#   Q45600896: set the es label
Q45600896	Les	"hombre del clan Lu, de Wujun Wuxian"
#   Q45600896: set the it label
Q45600896	Lit	"uomo del clan Lu, da Wujun Wuxian"
#   Q45600896: set the pt label
Q45600896	Lpt	"homem do clã Lu, de Wujun Wuxian"
#   Q45600896: set the ca label
Q45600896	Lca	"home del clan Lu, de Wujun Wuxian"
#   Q45602475 (李 of 京兆長安): mul label = NN
Q45602475	Lmul	"NN"
#   Q45602475: set the nb label
Q45602475	Lnb	"mann av Li-slekten, fra Jingzhao Chang'an"
#   Q45602475: set the da label
Q45602475	Lda	"mand af Li-slægten, fra Jingzhao Chang'an"
#   Q45602475: set the sv label
Q45602475	Lsv	"man av Li-ätten, från Jingzhao Chang'an"
#   Q45602475: set the de label
Q45602475	Lde	"Mann des Klans Li, aus Jingzhao Chang'an"
#   Q45602475: set the es label
Q45602475	Les	"hombre del clan Li, de Jingzhao Chang'an"
#   Q45602475: set the it label
Q45602475	Lit	"uomo del clan Li, da Jingzhao Chang'an"
#   Q45602475: set the pt label
Q45602475	Lpt	"homem do clã Li, de Jingzhao Chang'an"
#   Q45602475: set the ca label
Q45602475	Lca	"home del clan Li, de Jingzhao Chang'an"
#   Q45611337 (鄭 of 鄭州榮澤): mul label = NN
Q45611337	Lmul	"NN"
#   Q45611337: set the nb label
Q45611337	Lnb	"mann av Zheng-slekten, fra Zhengzhou Rongze"
#   Q45611337: set the da label
Q45611337	Lda	"mand af Zheng-slægten, fra Zhengzhou Rongze"
#   Q45611337: set the sv label
Q45611337	Lsv	"man av Zheng-ätten, från Zhengzhou Rongze"
#   Q45611337: set the de label
Q45611337	Lde	"Mann des Klans Zheng, aus Zhengzhou Rongze"
#   Q45611337: set the it label
Q45611337	Lit	"uomo del clan Zheng, da Zhengzhou Rongze"
#   Q45611337: set the pt label
Q45611337	Lpt	"homem do clã Zheng, de Zhengzhou Rongze"
#   Q45611337: set the ca label
Q45611337	Lca	"home del clan Zheng, de Zhengzhou Rongze"
#   Q45620545 (楊 of ): mul label = NN
Q45620545	Lmul	"NN"
#   Q45620545: set the nb label
Q45620545	Lnb	"mann av Yang-slekten"
#   Q45620545: set the da label
Q45620545	Lda	"mand af Yang-slægten"
#   Q45620545: set the sv label
Q45620545	Lsv	"man av Yang-ätten"
#   Q45620545: set the de label
Q45620545	Lde	"Mann des Klans Yang"
#   Q45620545: set the it label
Q45620545	Lit	"uomo del clan Yang"
#   Q45620545: set the pt label
Q45620545	Lpt	"homem do clã Yang"
#   Q45620545: set the ca label
Q45620545	Lca	"home del clan Yang"
#   Q45621550 (李 of 趙州贊皇): mul label = NN
Q45621550	Lmul	"NN"
#   Q45621550: set the nb label
Q45621550	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45621550: set the da label
Q45621550	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45621550: set the sv label
Q45621550	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45621550: set the de label
Q45621550	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45621550: set the es label
Q45621550	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45621550: set the it label
Q45621550	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45621550: set the pt label
Q45621550	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45621550: set the ca label
Q45621550	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45621738 (李 of 趙州贊皇): mul label = NN
Q45621738	Lmul	"NN"
#   Q45621738: set the nb label
Q45621738	Lnb	"mann av Li-slekten, fra Zhaozhou Zanhuang"
#   Q45621738: set the da label
Q45621738	Lda	"mand af Li-slægten, fra Zhaozhou Zanhuang"
#   Q45621738: set the sv label
Q45621738	Lsv	"man av Li-ätten, från Zhaozhou Zanhuang"
#   Q45621738: set the de label
Q45621738	Lde	"Mann des Klans Li, aus Zhaozhou Zanhuang"
#   Q45621738: set the es label
Q45621738	Les	"hombre del clan Li, de Zhaozhou Zanhuang"
#   Q45621738: set the it label
Q45621738	Lit	"uomo del clan Li, da Zhaozhou Zanhuang"
#   Q45621738: set the pt label
Q45621738	Lpt	"homem do clã Li, de Zhaozhou Zanhuang"
#   Q45621738: set the ca label
Q45621738	Lca	"home del clan Li, de Zhaozhou Zanhuang"
#   Q45622685 (唐 of 晉昌冥安): mul label = NN
Q45622685	Lmul	"NN"
#   Q45622685: set the nb label
Q45622685	Lnb	"mann av Tang-slekten, fra Jinchang Ming'an"
#   Q45622685: set the da label
Q45622685	Lda	"mand af Tang-slægten, fra Jinchang Ming'an"
#   Q45622685: set the sv label
Q45622685	Lsv	"man av Tang-ätten, från Jinchang Ming'an"
#   Q45622685: set the de label
Q45622685	Lde	"Mann des Klans Tang, aus Jinchang Ming'an"
#   Q45622685: set the it label
Q45622685	Lit	"uomo del clan Tang, da Jinchang Ming'an"
#   Q45622685: set the pt label
Q45622685	Lpt	"homem do clã Tang, de Jinchang Ming'an"
#   Q45622685: set the ca label
Q45622685	Lca	"home del clan Tang, de Jinchang Ming'an"
#   Q45628948 (薛 of 蒲州寶鼎): mul label = NN
Q45628948	Lmul	"NN"
#   Q45628948: set the nb label
Q45628948	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45628948: set the da label
Q45628948	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45628948: set the sv label
Q45628948	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45628948: set the de label
Q45628948	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45628948: set the it label
Q45628948	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45628948: set the pt label
Q45628948	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45628948: set the ca label
Q45628948	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45632756 (裴 of 河東聞喜): mul label = NN
Q45632756	Lmul	"NN"
#   Q45632756: set the nb label
Q45632756	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45632756: set the da label
Q45632756	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45632756: set the sv label
Q45632756	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45632756: set the de label
Q45632756	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45632756: set the it label
Q45632756	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45632756: set the pt label
Q45632756	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45632756: set the ca label
Q45632756	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45635644 (蕭 of 蘭陵): mul label = NN
Q45635644	Lmul	"NN"
#   Q45635644: set the nb label
Q45635644	Lnb	"mann av Xiao-slekten, fra Lanling"
#   Q45635644: set the da label
Q45635644	Lda	"mand af Xiao-slægten, fra Lanling"
#   Q45635644: set the sv label
Q45635644	Lsv	"man av Xiao-ätten, från Lanling"
#   Q45635644: set the de label
Q45635644	Lde	"Mann des Klans Xiao, aus Lanling"
#   Q45635644: set the it label
Q45635644	Lit	"uomo del clan Xiao, da Lanling"
#   Q45635644: set the pt label
Q45635644	Lpt	"homem do clã Xiao, de Lanling"
#   Q45635644: set the ca label
Q45635644	Lca	"home del clan Xiao, de Lanling"
#   Q45639455 (薛 of 蒲州寶鼎): mul label = NN
Q45639455	Lmul	"NN"
#   Q45639455: set the nb label
Q45639455	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45639455: set the da label
Q45639455	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45639455: set the sv label
Q45639455	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45639455: set the de label
Q45639455	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45639455: set the it label
Q45639455	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45639455: set the pt label
Q45639455	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45639455: set the ca label
Q45639455	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45642399 (裴 of 河東聞喜): mul label = NN
Q45642399	Lmul	"NN"
#   Q45642399: set the nb label
Q45642399	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642399: set the da label
Q45642399	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642399: set the sv label
Q45642399	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642399: set the de label
Q45642399	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642399: set the it label
Q45642399	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642399: set the pt label
Q45642399	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642399: set the ca label
Q45642399	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642460 (裴 of 河東聞喜): mul label = NN
Q45642460	Lmul	"NN"
#   Q45642460: set the nb label
Q45642460	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642460: set the da label
Q45642460	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642460: set the sv label
Q45642460	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642460: set the de label
Q45642460	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642460: set the it label
Q45642460	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642460: set the pt label
Q45642460	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642460: set the ca label
Q45642460	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642520 (裴 of 河東聞喜): mul label = NN
Q45642520	Lmul	"NN"
#   Q45642520: set the nb label
Q45642520	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642520: set the da label
Q45642520	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642520: set the sv label
Q45642520	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642520: set the de label
Q45642520	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642520: set the it label
Q45642520	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642520: set the pt label
Q45642520	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642520: set the ca label
Q45642520	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642643 (裴 of 河東聞喜): mul label = NN
Q45642643	Lmul	"NN"
#   Q45642643: set the nb label
Q45642643	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642643: set the da label
Q45642643	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642643: set the sv label
Q45642643	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642643: set the de label
Q45642643	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642643: set the it label
Q45642643	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642643: set the pt label
Q45642643	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642643: set the ca label
Q45642643	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45642829 (裴 of 河東聞喜): mul label = NN
Q45642829	Lmul	"NN"
#   Q45642829: set the nb label
Q45642829	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45642829: set the da label
Q45642829	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45642829: set the sv label
Q45642829	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45642829: set the de label
Q45642829	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45642829: set the it label
Q45642829	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45642829: set the pt label
Q45642829	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45642829: set the ca label
Q45642829	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45644430 (李 of 趙州平棘): mul label = NN
Q45644430	Lmul	"NN"
#   Q45644430: set the nb label
Q45644430	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644430: set the da label
Q45644430	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644430: set the sv label
Q45644430	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644430: set the de label
Q45644430	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644430: set the es label
Q45644430	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644430: set the it label
Q45644430	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644430: set the pt label
Q45644430	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644430: set the ca label
Q45644430	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45644491 (李 of 趙州平棘): mul label = NN
Q45644491	Lmul	"NN"
#   Q45644491: set the nb label
Q45644491	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644491: set the da label
Q45644491	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644491: set the sv label
Q45644491	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644491: set the de label
Q45644491	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644491: set the es label
Q45644491	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644491: set the it label
Q45644491	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644491: set the pt label
Q45644491	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644491: set the ca label
Q45644491	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45644550 (李 of 趙州平棘): mul label = NN
Q45644550	Lmul	"NN"
#   Q45644550: set the nb label
Q45644550	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45644550: set the da label
Q45644550	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45644550: set the sv label
Q45644550	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45644550: set the de label
Q45644550	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45644550: set the es label
Q45644550	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45644550: set the it label
Q45644550	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45644550: set the pt label
Q45644550	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45644550: set the ca label
Q45644550	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45645832 (李 of 河南): mul label = NN
Q45645832	Lmul	"NN"
#   Q45645832: set the nb label
Q45645832	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645832: set the da label
Q45645832	Lda	"mand af Li-slægten, fra Henan"
#   Q45645832: set the sv label
Q45645832	Lsv	"man av Li-ätten, från Henan"
#   Q45645832: set the de label
Q45645832	Lde	"Mann des Klans Li, aus Henan"
#   Q45645832: set the es label
Q45645832	Les	"hombre del clan Li, de Henan"
#   Q45645832: set the it label
Q45645832	Lit	"uomo del clan Li, da Henan"
#   Q45645832: set the pt label
Q45645832	Lpt	"homem do clã Li, de Henan"
#   Q45645832: set the ca label
Q45645832	Lca	"home del clan Li, de Henan"
#   Q45645892 (李 of 河南): mul label = NN
Q45645892	Lmul	"NN"
#   Q45645892: set the nb label
Q45645892	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645892: set the da label
Q45645892	Lda	"mand af Li-slægten, fra Henan"
#   Q45645892: set the sv label
Q45645892	Lsv	"man av Li-ätten, från Henan"
#   Q45645892: set the de label
Q45645892	Lde	"Mann des Klans Li, aus Henan"
#   Q45645892: set the es label
Q45645892	Les	"hombre del clan Li, de Henan"
#   Q45645892: set the it label
Q45645892	Lit	"uomo del clan Li, da Henan"
#   Q45645892: set the pt label
Q45645892	Lpt	"homem do clã Li, de Henan"
#   Q45645892: set the ca label
Q45645892	Lca	"home del clan Li, de Henan"
#   Q45645904 (裴 of 河東聞喜): mul label = NN
Q45645904	Lmul	"NN"
#   Q45645904: set the nb label
Q45645904	Lnb	"mann av Pei-slekten, fra Hedong Wenxi"
#   Q45645904: set the da label
Q45645904	Lda	"mand af Pei-slægten, fra Hedong Wenxi"
#   Q45645904: set the sv label
Q45645904	Lsv	"man av Pei-ätten, från Hedong Wenxi"
#   Q45645904: set the de label
Q45645904	Lde	"Mann des Klans Pei, aus Hedong Wenxi"
#   Q45645904: set the it label
Q45645904	Lit	"uomo del clan Pei, da Hedong Wenxi"
#   Q45645904: set the pt label
Q45645904	Lpt	"homem do clã Pei, de Hedong Wenxi"
#   Q45645904: set the ca label
Q45645904	Lca	"home del clan Pei, de Hedong Wenxi"
#   Q45645953 (李 of 河南): mul label = NN
Q45645953	Lmul	"NN"
#   Q45645953: set the nb label
Q45645953	Lnb	"mann av Li-slekten, fra Henan"
#   Q45645953: set the da label
Q45645953	Lda	"mand af Li-slægten, fra Henan"
#   Q45645953: set the sv label
Q45645953	Lsv	"man av Li-ätten, från Henan"
#   Q45645953: set the de label
Q45645953	Lde	"Mann des Klans Li, aus Henan"
#   Q45645953: set the es label
Q45645953	Les	"hombre del clan Li, de Henan"
#   Q45645953: set the it label
Q45645953	Lit	"uomo del clan Li, da Henan"
#   Q45645953: set the pt label
Q45645953	Lpt	"homem do clã Li, de Henan"
#   Q45645953: set the ca label
Q45645953	Lca	"home del clan Li, de Henan"
#   Q45646012 (李 of 河南): mul label = NN
Q45646012	Lmul	"NN"
#   Q45646012: set the nb label
Q45646012	Lnb	"mann av Li-slekten, fra Henan"
#   Q45646012: set the da label
Q45646012	Lda	"mand af Li-slægten, fra Henan"
#   Q45646012: set the sv label
Q45646012	Lsv	"man av Li-ätten, från Henan"
#   Q45646012: set the de label
Q45646012	Lde	"Mann des Klans Li, aus Henan"
#   Q45646012: set the es label
Q45646012	Les	"hombre del clan Li, de Henan"
#   Q45646012: set the it label
Q45646012	Lit	"uomo del clan Li, da Henan"
#   Q45646012: set the pt label
Q45646012	Lpt	"homem do clã Li, de Henan"
#   Q45646012: set the ca label
Q45646012	Lca	"home del clan Li, de Henan"
#   Q45646435 (李 of 趙州平棘): mul label = NN
Q45646435	Lmul	"NN"
#   Q45646435: set the nb label
Q45646435	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646435: set the da label
Q45646435	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646435: set the sv label
Q45646435	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646435: set the de label
Q45646435	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646435: set the es label
Q45646435	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646435: set the it label
Q45646435	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646435: set the pt label
Q45646435	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646435: set the ca label
Q45646435	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646493 (李 of 趙州平棘): mul label = NN
Q45646493	Lmul	"NN"
#   Q45646493: set the nb label
Q45646493	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646493: set the da label
Q45646493	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646493: set the sv label
Q45646493	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646493: set the de label
Q45646493	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646493: set the es label
Q45646493	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646493: set the it label
Q45646493	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646493: set the pt label
Q45646493	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646493: set the ca label
Q45646493	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646554 (李 of 趙州平棘): mul label = NN
Q45646554	Lmul	"NN"
#   Q45646554: set the nb label
Q45646554	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45646554: set the da label
Q45646554	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45646554: set the sv label
Q45646554	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45646554: set the de label
Q45646554	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45646554: set the es label
Q45646554	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45646554: set the it label
Q45646554	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45646554: set the pt label
Q45646554	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45646554: set the ca label
Q45646554	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45646854 (李 of 滑州匡城): mul label = NN
Q45646854	Lmul	"NN"
#   Q45646854: set the nb label
Q45646854	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646854: set the da label
Q45646854	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646854: set the sv label
Q45646854	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646854: set the de label
Q45646854	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646854: set the es label
Q45646854	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646854: set the it label
Q45646854	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646854: set the pt label
Q45646854	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646854: set the ca label
Q45646854	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45646912 (李 of 滑州匡城): mul label = NN
Q45646912	Lmul	"NN"
#   Q45646912: set the nb label
Q45646912	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646912: set the da label
Q45646912	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646912: set the sv label
Q45646912	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646912: set the de label
Q45646912	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646912: set the es label
Q45646912	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646912: set the it label
Q45646912	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646912: set the pt label
Q45646912	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646912: set the ca label
Q45646912	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45646972 (李 of 滑州匡城): mul label = NN
Q45646972	Lmul	"NN"
#   Q45646972: set the nb label
Q45646972	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45646972: set the da label
Q45646972	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45646972: set the sv label
Q45646972	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45646972: set the de label
Q45646972	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45646972: set the es label
Q45646972	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45646972: set the it label
Q45646972	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45646972: set the pt label
Q45646972	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45646972: set the ca label
Q45646972	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647031 (李 of 滑州匡城): mul label = NN
Q45647031	Lmul	"NN"
#   Q45647031: set the nb label
Q45647031	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647031: set the da label
Q45647031	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647031: set the sv label
Q45647031	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647031: set the de label
Q45647031	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647031: set the es label
Q45647031	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647031: set the it label
Q45647031	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647031: set the pt label
Q45647031	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647031: set the ca label
Q45647031	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647089 (李 of 滑州匡城): mul label = NN
Q45647089	Lmul	"NN"
#   Q45647089: set the nb label
Q45647089	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647089: set the da label
Q45647089	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647089: set the sv label
Q45647089	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647089: set the de label
Q45647089	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647089: set the es label
Q45647089	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647089: set the it label
Q45647089	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647089: set the pt label
Q45647089	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647089: set the ca label
Q45647089	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647334 (李 of 滑州匡城): mul label = NN
Q45647334	Lmul	"NN"
#   Q45647334: set the nb label
Q45647334	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647334: set the da label
Q45647334	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647334: set the sv label
Q45647334	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647334: set the de label
Q45647334	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647334: set the es label
Q45647334	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647334: set the it label
Q45647334	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647334: set the pt label
Q45647334	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647334: set the ca label
Q45647334	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647512 (李 of 滑州匡城): mul label = NN
Q45647512	Lmul	"NN"
#   Q45647512: set the nb label
Q45647512	Lnb	"mann av Li-slekten, fra Huazhou Kuangcheng"
#   Q45647512: set the da label
Q45647512	Lda	"mand af Li-slægten, fra Huazhou Kuangcheng"
#   Q45647512: set the sv label
Q45647512	Lsv	"man av Li-ätten, från Huazhou Kuangcheng"
#   Q45647512: set the de label
Q45647512	Lde	"Mann des Klans Li, aus Huazhou Kuangcheng"
#   Q45647512: set the es label
Q45647512	Les	"hombre del clan Li, de Huazhou Kuangcheng"
#   Q45647512: set the it label
Q45647512	Lit	"uomo del clan Li, da Huazhou Kuangcheng"
#   Q45647512: set the pt label
Q45647512	Lpt	"homem do clã Li, de Huazhou Kuangcheng"
#   Q45647512: set the ca label
Q45647512	Lca	"home del clan Li, de Huazhou Kuangcheng"
#   Q45647926 (李 of 河南): mul label = NN
Q45647926	Lmul	"NN"
#   Q45647926: set the nb label
Q45647926	Lnb	"mann av Li-slekten, fra Henan"
#   Q45647926: set the da label
Q45647926	Lda	"mand af Li-slægten, fra Henan"
#   Q45647926: set the sv label
Q45647926	Lsv	"man av Li-ätten, från Henan"
#   Q45647926: set the de label
Q45647926	Lde	"Mann des Klans Li, aus Henan"
#   Q45647926: set the es label
Q45647926	Les	"hombre del clan Li, de Henan"
#   Q45647926: set the it label
Q45647926	Lit	"uomo del clan Li, da Henan"
#   Q45647926: set the pt label
Q45647926	Lpt	"homem do clã Li, de Henan"
#   Q45647926: set the ca label
Q45647926	Lca	"home del clan Li, de Henan"
#   Q45648222 (李 of 河南洛陽): mul label = NN
Q45648222	Lmul	"NN"
#   Q45648222: set the nb label
Q45648222	Lnb	"mann av Li-slekten, fra Henan Luoyang"
#   Q45648222: set the da label
Q45648222	Lda	"mand af Li-slægten, fra Henan Luoyang"
#   Q45648222: set the sv label
Q45648222	Lsv	"man av Li-ätten, från Henan Luoyang"
#   Q45648222: set the de label
Q45648222	Lde	"Mann des Klans Li, aus Henan Luoyang"
#   Q45648222: set the es label
Q45648222	Les	"hombre del clan Li, de Henan Luoyang"
#   Q45648222: set the it label
Q45648222	Lit	"uomo del clan Li, da Henan Luoyang"
#   Q45648222: set the pt label
Q45648222	Lpt	"homem do clã Li, de Henan Luoyang"
#   Q45648222: set the ca label
Q45648222	Lca	"home del clan Li, de Henan Luoyang"
#   Q45648878 (薛 of 蒲州寶鼎): mul label = NN
Q45648878	Lmul	"NN"
#   Q45648878: set the nb label
Q45648878	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45648878: set the da label
Q45648878	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45648878: set the sv label
Q45648878	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45648878: set the de label
Q45648878	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45648878: set the it label
Q45648878	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45648878: set the pt label
Q45648878	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45648878: set the ca label
Q45648878	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45648938 (薛 of 蒲州寶鼎): mul label = NN
Q45648938	Lmul	"NN"
#   Q45648938: set the nb label
Q45648938	Lnb	"mann av Xue-slekten, fra Puzhou Baoding"
#   Q45648938: set the da label
Q45648938	Lda	"mand af Xue-slægten, fra Puzhou Baoding"
#   Q45648938: set the sv label
Q45648938	Lsv	"man av Xue-ätten, från Puzhou Baoding"
#   Q45648938: set the de label
Q45648938	Lde	"Mann des Klans Xue, aus Puzhou Baoding"
#   Q45648938: set the it label
Q45648938	Lit	"uomo del clan Xue, da Puzhou Baoding"
#   Q45648938: set the pt label
Q45648938	Lpt	"homem do clã Xue, de Puzhou Baoding"
#   Q45648938: set the ca label
Q45648938	Lca	"home del clan Xue, de Puzhou Baoding"
#   Q45649066 (李 of 河南): mul label = NN
Q45649066	Lmul	"NN"
#   Q45649066: set the nb label
Q45649066	Lnb	"mann av Li-slekten, fra Henan"
#   Q45649066: set the da label
Q45649066	Lda	"mand af Li-slægten, fra Henan"
#   Q45649066: set the sv label
Q45649066	Lsv	"man av Li-ätten, från Henan"
#   Q45649066: set the de label
Q45649066	Lde	"Mann des Klans Li, aus Henan"
#   Q45649066: set the es label
Q45649066	Les	"hombre del clan Li, de Henan"
#   Q45649066: set the it label
Q45649066	Lit	"uomo del clan Li, da Henan"
#   Q45649066: set the pt label
Q45649066	Lpt	"homem do clã Li, de Henan"
#   Q45649066: set the ca label
Q45649066	Lca	"home del clan Li, de Henan"
#   Q45649184 (李 of 趙州平棘): mul label = NN
Q45649184	Lmul	"NN"
#   Q45649184: set the nb label
Q45649184	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45649184: set the da label
Q45649184	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45649184: set the sv label
Q45649184	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45649184: set the de label
Q45649184	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45649184: set the es label
Q45649184	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45649184: set the it label
Q45649184	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45649184: set the pt label
Q45649184	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45649184: set the ca label
Q45649184	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45650019 (李 of 趙州平棘): mul label = NN
Q45650019	Lmul	"NN"
#   Q45650019: set the nb label
Q45650019	Lnb	"mann av Li-slekten, fra Zhaozhou Pingji"
#   Q45650019: set the da label
Q45650019	Lda	"mand af Li-slægten, fra Zhaozhou Pingji"
#   Q45650019: set the sv label
Q45650019	Lsv	"man av Li-ätten, från Zhaozhou Pingji"
#   Q45650019: set the de label
Q45650019	Lde	"Mann des Klans Li, aus Zhaozhou Pingji"
#   Q45650019: set the es label
Q45650019	Les	"hombre del clan Li, de Zhaozhou Pingji"
#   Q45650019: set the it label
Q45650019	Lit	"uomo del clan Li, da Zhaozhou Pingji"
#   Q45650019: set the pt label
Q45650019	Lpt	"homem do clã Li, de Zhaozhou Pingji"
#   Q45650019: set the ca label
Q45650019	Lca	"home del clan Li, de Zhaozhou Pingji"
#   Q45651316 (薛 of 河南洛陽): mul label = NN
Q45651316	Lmul	"NN"
#   Q45651316: set the nb label
Q45651316	Lnb	"mann av Xue-slekten, fra Henan Luoyang"
#   Q45651316: set the da label
Q45651316	Lda	"mand af Xue-slægten, fra Henan Luoyang"
#   Q45651316: set the sv label
Q45651316	Lsv	"man av Xue-ätten, från Henan Luoyang"
#   Q45651316: set the de label
Q45651316	Lde	"Mann des Klans Xue, aus Henan Luoyang"
#   Q45651316: set the it label
Q45651316	Lit	"uomo del clan Xue, da Henan Luoyang"
#   Q45651316: set the pt label
Q45651316	Lpt	"homem do clã Xue, de Henan Luoyang"
#   Q45651316: set the ca label
Q45651316	Lca	"home del clan Xue, de Henan Luoyang"
#   Q45651377 (薛 of 河南洛陽): mul label = NN
Q45651377	Lmul	"NN"
#   Q45651377: set the nb label
Q45651377	Lnb	"mann av Xue-slekten, fra Henan Luoyang"
#   Q45651377: set the da label
Q45651377	Lda	"mand af Xue-slægten, fra Henan Luoyang"
#   Q45651377: set the sv label
Q45651377	Lsv	"man av Xue-ätten, från Henan Luoyang"
#   Q45651377: set the de label
Q45651377	Lde	"Mann des Klans Xue, aus Henan Luoyang"
#   Q45651377: set the it label
Q45651377	Lit	"uomo del clan Xue, da Henan Luoyang"
#   Q45651377: set the pt label
Q45651377	Lpt	"homem do clã Xue, de Henan Luoyang"
#   Q45651377: set the ca label
Q45651377	Lca	"home del clan Xue, de Henan Luoyang"
#   Q45655203 (鄭 of 河南府): mul label = NN
Q45655203	Lmul	"NN"
#   Q45655203: set the nb label
Q45655203	Lnb	"mann av Zheng-slekten, fra Henan Prefecture"
#   Q45655203: set the da label
Q45655203	Lda	"mand af Zheng-slægten, fra Henan Prefecture"
#   Q45655203: set the sv label
Q45655203	Lsv	"man av Zheng-ätten, från Henan Prefecture"
#   Q45655203: set the de label
Q45655203	Lde	"Mann des Klans Zheng, aus Henan Prefecture"
#   Q45655203: set the it label
Q45655203	Lit	"uomo del clan Zheng, da Henan Prefecture"
#   Q45655203: set the pt label
Q45655203	Lpt	"homem do clã Zheng, de Henan Prefecture"
#   Q45655203: set the ca label
Q45655203	Lca	"home del clan Zheng, de Henan Prefecture"
#   Q45655848 (李 of 京兆府): mul label = NN
Q45655848	Lmul	"NN"
#   Q45655848: set the nb label
Q45655848	Lnb	"mann av Li-slekten, fra Jingzhao Prefecture"
#   Q45655848: set the da label
Q45655848	Lda	"mand af Li-slægten, fra Jingzhao Prefecture"
#   Q45655848: set the sv label
Q45655848	Lsv	"man av Li-ätten, från Jingzhao Prefecture"
#   Q45655848: set the de label
Q45655848	Lde	"Mann des Klans Li, aus Jingzhao Prefecture"
#   Q45655848: set the es label
Q45655848	Les	"hombre del clan Li, de Jingzhao Prefecture"
#   Q45655848: set the it label
Q45655848	Lit	"uomo del clan Li, da Jingzhao Prefecture"
#   Q45655848: set the pt label
Q45655848	Lpt	"homem do clã Li, de Jingzhao Prefecture"
#   Q45655848: set the ca label
Q45655848	Lca	"home del clan Li, de Jingzhao Prefecture"
#   Q45657616 (韋 of 京兆杜陵): mul label = NN
Q45657616	Lmul	"NN"
#   Q45657616: set the nb label
Q45657616	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45657616: set the da label
Q45657616	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45657616: set the sv label
Q45657616	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45657616: set the de label
Q45657616	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45657616: set the it label
Q45657616	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45657616: set the pt label
Q45657616	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45657616: set the ca label
Q45657616	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45657676 (韋 of 京兆杜陵): mul label = NN
Q45657676	Lmul	"NN"
#   Q45657676: set the nb label
Q45657676	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45657676: set the da label
Q45657676	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45657676: set the sv label
Q45657676	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45657676: set the de label
Q45657676	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45657676: set the it label
Q45657676	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45657676: set the pt label
Q45657676	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45657676: set the ca label
Q45657676	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659526 (韋 of 京兆杜陵): mul label = NN
Q45659526	Lmul	"NN"
#   Q45659526: set the nb label
Q45659526	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659526: set the da label
Q45659526	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659526: set the sv label
Q45659526	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659526: set the de label
Q45659526	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659526: set the it label
Q45659526	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659526: set the pt label
Q45659526	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659526: set the ca label
Q45659526	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659585 (韋 of 京兆杜陵): mul label = NN
Q45659585	Lmul	"NN"
#   Q45659585: set the nb label
Q45659585	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659585: set the da label
Q45659585	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659585: set the sv label
Q45659585	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659585: set the de label
Q45659585	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659585: set the it label
Q45659585	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659585: set the pt label
Q45659585	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659585: set the ca label
Q45659585	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45659766 (韋 of 京兆杜陵): mul label = NN
Q45659766	Lmul	"NN"
#   Q45659766: set the nb label
Q45659766	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45659766: set the da label
Q45659766	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45659766: set the sv label
Q45659766	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45659766: set the de label
Q45659766	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45659766: set the it label
Q45659766	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45659766: set the pt label
Q45659766	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45659766: set the ca label
Q45659766	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660005 (韋 of 京兆杜陵): mul label = NN
Q45660005	Lmul	"NN"
#   Q45660005: set the nb label
Q45660005	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660005: set the da label
Q45660005	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660005: set the sv label
Q45660005	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660005: set the de label
Q45660005	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660005: set the it label
Q45660005	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660005: set the pt label
Q45660005	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660005: set the ca label
Q45660005	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660063 (韋 of 京兆杜陵): mul label = NN
Q45660063	Lmul	"NN"
#   Q45660063: set the nb label
Q45660063	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660063: set the da label
Q45660063	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660063: set the sv label
Q45660063	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660063: set the de label
Q45660063	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660063: set the it label
Q45660063	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660063: set the pt label
Q45660063	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660063: set the ca label
Q45660063	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660721 (韋 of 京兆杜陵): mul label = NN
Q45660721	Lmul	"NN"
#   Q45660721: set the nb label
Q45660721	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660721: set the da label
Q45660721	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660721: set the sv label
Q45660721	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660721: set the de label
Q45660721	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660721: set the it label
Q45660721	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660721: set the pt label
Q45660721	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660721: set the ca label
Q45660721	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660780 (韋 of 京兆杜陵): mul label = NN
Q45660780	Lmul	"NN"
#   Q45660780: set the nb label
Q45660780	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660780: set the da label
Q45660780	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660780: set the sv label
Q45660780	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660780: set the de label
Q45660780	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660780: set the it label
Q45660780	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660780: set the pt label
Q45660780	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660780: set the ca label
Q45660780	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45660841 (韋 of 京兆杜陵): mul label = NN
Q45660841	Lmul	"NN"
#   Q45660841: set the nb label
Q45660841	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45660841: set the da label
Q45660841	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45660841: set the sv label
Q45660841	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45660841: set the de label
Q45660841	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45660841: set the it label
Q45660841	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45660841: set the pt label
Q45660841	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45660841: set the ca label
Q45660841	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45664697 (韋 of 京兆杜陵): mul label = NN
Q45664697	Lmul	"NN"
#   Q45664697: set the nb label
Q45664697	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45664697: set the da label
Q45664697	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45664697: set the sv label
Q45664697	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45664697: set the de label
Q45664697	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45664697: set the it label
Q45664697	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45664697: set the pt label
Q45664697	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45664697: set the ca label
Q45664697	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45664752 (韋 of 京兆杜陵): mul label = NN
Q45664752	Lmul	"NN"
#   Q45664752: set the nb label
Q45664752	Lnb	"mann av Wei-slekten, fra Jingzhao Duling"
#   Q45664752: set the da label
Q45664752	Lda	"mand af Wei-slægten, fra Jingzhao Duling"
#   Q45664752: set the sv label
Q45664752	Lsv	"man av Wei-ätten, från Jingzhao Duling"
#   Q45664752: set the de label
Q45664752	Lde	"Mann des Klans Wei, aus Jingzhao Duling"
#   Q45664752: set the it label
Q45664752	Lit	"uomo del clan Wei, da Jingzhao Duling"
#   Q45664752: set the pt label
Q45664752	Lpt	"homem do clã Wei, de Jingzhao Duling"
#   Q45664752: set the ca label
Q45664752	Lca	"home del clan Wei, de Jingzhao Duling"
#   Q45678944 (郭 of 太原): mul label = NN
Q45678944	Lmul	"NN"
#   Q45678944: set the nb label
Q45678944	Lnb	"mann av Guo-slekten, fra Taiyuan"
#   Q45678944: set the da label
Q45678944	Lda	"mand af Guo-slægten, fra Taiyuan"
#   Q45678944: set the sv label
Q45678944	Lsv	"man av Guo-ätten, från Taiyuan"
#   Q45678944: set the de label
Q45678944	Lde	"Mann des Klans Guo, aus Taiyuan"
#   Q45678944: set the it label
Q45678944	Lit	"uomo del clan Guo, da Taiyuan"
#   Q45678944: set the pt label
Q45678944	Lpt	"homem do clã Guo, de Taiyuan"
#   Q45678944: set the ca label
Q45678944	Lca	"home del clan Guo, de Taiyuan"
#   Q45682618 (武 of 太原文水): mul label = NN
Q45682618	Lmul	"NN"
#   Q45682618: set the nb label
Q45682618	Lnb	"mann av Wu-slekten, fra Taiyuan Wenshui"
#   Q45682618: set the da label
Q45682618	Lda	"mand af Wu-slægten, fra Taiyuan Wenshui"
#   Q45682618: set the sv label
Q45682618	Lsv	"man av Wu-ätten, från Taiyuan Wenshui"
#   Q45682618: set the de label
Q45682618	Lde	"Mann des Klans Wu, aus Taiyuan Wenshui"
#   Q45682618: set the it label
Q45682618	Lit	"uomo del clan Wu, da Taiyuan Wenshui"
#   Q45682618: set the pt label
Q45682618	Lpt	"homem do clã Wu, de Taiyuan Wenshui"
#   Q45682618: set the ca label
Q45682618	Lca	"home del clan Wu, de Taiyuan Wenshui"
#   Q45684235 (蘇 of 京兆萬年): mul label = NN
Q45684235	Lmul	"NN"
#   Q45684235: set the nb label
Q45684235	Lnb	"mann av Su-slekten, fra Jingzhao Wannian"
#   Q45684235: set the da label
Q45684235	Lda	"mand af Su-slægten, fra Jingzhao Wannian"
#   Q45684235: set the sv label
Q45684235	Lsv	"man av Su-ätten, från Jingzhao Wannian"
#   Q45684235: set the de label
Q45684235	Lde	"Mann des Klans Su, aus Jingzhao Wannian"
#   Q45684235: set the es label
Q45684235	Les	"hombre del clan Su, de Jingzhao Wannian"
#   Q45684235: set the it label
Q45684235	Lit	"uomo del clan Su, da Jingzhao Wannian"
#   Q45684235: set the pt label
Q45684235	Lpt	"homem do clã Su, de Jingzhao Wannian"
#   Q45684235: set the ca label
Q45684235	Lca	"home del clan Su, de Jingzhao Wannian"
#   Q45685725 (張 of 襄州襄陽): mul label = NN
Q45685725	Lmul	"NN"
#   Q45685725: set the nb label
Q45685725	Lnb	"mann av Zhang-slekten, fra Xiangzhou Xiangyang"
#   Q45685725: set the da label
Q45685725	Lda	"mand af Zhang-slægten, fra Xiangzhou Xiangyang"
#   Q45685725: set the sv label
Q45685725	Lsv	"man av Zhang-ätten, från Xiangzhou Xiangyang"
#   Q45685725: set the de label
Q45685725	Lde	"Mann des Klans Zhang, aus Xiangzhou Xiangyang"
#   Q45685725: set the it label
Q45685725	Lit	"uomo del clan Zhang, da Xiangzhou Xiangyang"
#   Q45685725: set the pt label
Q45685725	Lpt	"homem do clã Zhang, de Xiangzhou Xiangyang"
#   Q45685725: set the ca label
Q45685725	Lca	"home del clan Zhang, de Xiangzhou Xiangyang"
#   Q45685758 (張 of 襄州襄陽): mul label = NN
Q45685758	Lmul	"NN"
#   Q45685758: set the nb label
Q45685758	Lnb	"mann av Zhang-slekten, fra Xiangzhou Xiangyang"
#   Q45685758: set the da label
Q45685758	Lda	"mand af Zhang-slægten, fra Xiangzhou Xiangyang"
#   Q45685758: set the sv label
Q45685758	Lsv	"man av Zhang-ätten, från Xiangzhou Xiangyang"
#   Q45685758: set the de label
Q45685758	Lde	"Mann des Klans Zhang, aus Xiangzhou Xiangyang"
#   Q45685758: set the it label
Q45685758	Lit	"uomo del clan Zhang, da Xiangzhou Xiangyang"
#   Q45685758: set the pt label
Q45685758	Lpt	"homem do clã Zhang, de Xiangzhou Xiangyang"
#   Q45685758: set the ca label
Q45685758	Lca	"home del clan Zhang, de Xiangzhou Xiangyang"
#   Q45686328 (李 of 隴西狄道): mul label = NN
Q45686328	Lmul	"NN"
#   Q45686328: set the nb label
Q45686328	Lnb	"kvinne av Li-slekten, fra Longxi Didao"
#   Q45686328: set the da label
Q45686328	Lda	"kvinde af Li-slægten, fra Longxi Didao"
#   Q45686328: set the sv label
Q45686328	Lsv	"kvinna av Li-ätten, från Longxi Didao"
#   Q45686328: set the de label
Q45686328	Lde	"Frau des Klans Li, aus Longxi Didao"
#   Q45686328: set the es label
Q45686328	Les	"mujer del clan Li, de Longxi Didao"
#   Q45686328: set the it label
Q45686328	Lit	"donna del clan Li, da Longxi Didao"
#   Q45686328: set the pt label
Q45686328	Lpt	"mulher do clã Li, de Longxi Didao"
#   Q45686328: set the ca label
Q45686328	Lca	"dona del clan Li, de Longxi Didao"
#   Q45691897 (李 of 隴西狄道): mul label = NN
Q45691897	Lmul	"NN"
#   Q45691897: set the nb label
Q45691897	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45691897: set the da label
Q45691897	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45691897: set the sv label
Q45691897	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45691897: set the de label
Q45691897	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45691897: set the es label
Q45691897	Les	"hombre del clan Li, de Longxi Didao"
#   Q45691897: set the it label
Q45691897	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45691897: set the pt label
Q45691897	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45691897: set the ca label
Q45691897	Lca	"home del clan Li, de Longxi Didao"
#   Q45692090 (李 of 隴西狄道): mul label = NN
Q45692090	Lmul	"NN"
#   Q45692090: set the nb label
Q45692090	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692090: set the da label
Q45692090	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692090: set the sv label
Q45692090	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692090: set the de label
Q45692090	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692090: set the es label
Q45692090	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692090: set the it label
Q45692090	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692090: set the pt label
Q45692090	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692090: set the ca label
Q45692090	Lca	"home del clan Li, de Longxi Didao"
#   Q45692318 (李 of 隴西狄道): mul label = NN
Q45692318	Lmul	"NN"
#   Q45692318: set the nb label
Q45692318	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692318: set the da label
Q45692318	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692318: set the sv label
Q45692318	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692318: set the de label
Q45692318	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692318: set the es label
Q45692318	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692318: set the it label
Q45692318	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692318: set the pt label
Q45692318	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692318: set the ca label
Q45692318	Lca	"home del clan Li, de Longxi Didao"
#   Q45692515 (李 of 隴西狄道): mul label = NN
Q45692515	Lmul	"NN"
#   Q45692515: set the nb label
Q45692515	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692515: set the da label
Q45692515	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692515: set the sv label
Q45692515	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692515: set the de label
Q45692515	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692515: set the es label
Q45692515	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692515: set the it label
Q45692515	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692515: set the pt label
Q45692515	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692515: set the ca label
Q45692515	Lca	"home del clan Li, de Longxi Didao"
#   Q45692573 (李 of 隴西狄道): mul label = NN
Q45692573	Lmul	"NN"
#   Q45692573: set the nb label
Q45692573	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692573: set the da label
Q45692573	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692573: set the sv label
Q45692573	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692573: set the de label
Q45692573	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692573: set the es label
Q45692573	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692573: set the it label
Q45692573	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692573: set the pt label
Q45692573	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692573: set the ca label
Q45692573	Lca	"home del clan Li, de Longxi Didao"
#   Q45692881 (李 of 隴西狄道): mul label = NN
Q45692881	Lmul	"NN"
#   Q45692881: set the nb label
Q45692881	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692881: set the da label
Q45692881	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692881: set the sv label
Q45692881	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692881: set the de label
Q45692881	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692881: set the es label
Q45692881	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692881: set the it label
Q45692881	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692881: set the pt label
Q45692881	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692881: set the ca label
Q45692881	Lca	"home del clan Li, de Longxi Didao"
#   Q45692909 (李 of 隴西狄道): mul label = NN
Q45692909	Lmul	"NN"
#   Q45692909: set the nb label
Q45692909	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692909: set the da label
Q45692909	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692909: set the sv label
Q45692909	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692909: set the de label
Q45692909	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692909: set the es label
Q45692909	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692909: set the it label
Q45692909	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692909: set the pt label
Q45692909	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692909: set the ca label
Q45692909	Lca	"home del clan Li, de Longxi Didao"
#   Q45692937 (李 of 秦州成紀): mul label = NN
Q45692937	Lmul	"NN"
#   Q45692937: set the nb label
Q45692937	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45692937: set the da label
Q45692937	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45692937: set the sv label
Q45692937	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45692937: set the de label
Q45692937	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45692937: set the es label
Q45692937	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45692937: set the it label
Q45692937	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45692937: set the pt label
Q45692937	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45692937: set the ca label
Q45692937	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45692964 (李 of 揚州): mul label = NN
Q45692964	Lmul	"NN"
#   Q45692964: set the nb label
Q45692964	Lnb	"mann av Li-slekten, fra Yangzhou"
#   Q45692964: set the da label
Q45692964	Lda	"mand af Li-slægten, fra Yangzhou"
#   Q45692964: set the sv label
Q45692964	Lsv	"man av Li-ätten, från Yangzhou"
#   Q45692964: set the de label
Q45692964	Lde	"Mann des Klans Li, aus Yangzhou"
#   Q45692964: set the es label
Q45692964	Les	"hombre del clan Li, de Yangzhou"
#   Q45692964: set the it label
Q45692964	Lit	"uomo del clan Li, da Yangzhou"
#   Q45692964: set the pt label
Q45692964	Lpt	"homem do clã Li, de Yangzhou"
#   Q45692964: set the ca label
Q45692964	Lca	"home del clan Li, de Yangzhou"
#   Q45692991 (李 of 隴西狄道): mul label = NN
Q45692991	Lmul	"NN"
#   Q45692991: set the nb label
Q45692991	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45692991: set the da label
Q45692991	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45692991: set the sv label
Q45692991	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45692991: set the de label
Q45692991	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45692991: set the es label
Q45692991	Les	"hombre del clan Li, de Longxi Didao"
#   Q45692991: set the it label
Q45692991	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45692991: set the pt label
Q45692991	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45692991: set the ca label
Q45692991	Lca	"home del clan Li, de Longxi Didao"
#   Q45693019 (李 of 隴西狄道): mul label = NN
Q45693019	Lmul	"NN"
#   Q45693019: set the nb label
Q45693019	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45693019: set the da label
Q45693019	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45693019: set the sv label
Q45693019	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45693019: set the de label
Q45693019	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45693019: set the es label
Q45693019	Les	"hombre del clan Li, de Longxi Didao"
#   Q45693019: set the it label
Q45693019	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45693019: set the pt label
Q45693019	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45693019: set the ca label
Q45693019	Lca	"home del clan Li, de Longxi Didao"
#   Q45693047 (李 of 隴西狄道): mul label = NN
Q45693047	Lmul	"NN"
#   Q45693047: set the nb label
Q45693047	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45693047: set the da label
Q45693047	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45693047: set the sv label
Q45693047	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45693047: set the de label
Q45693047	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45693047: set the es label
Q45693047	Les	"hombre del clan Li, de Longxi Didao"
#   Q45693047: set the it label
Q45693047	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45693047: set the pt label
Q45693047	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45693047: set the ca label
Q45693047	Lca	"home del clan Li, de Longxi Didao"
#   Q45697303 (李 of 隴西狄道): mul label = NN
Q45697303	Lmul	"NN"
#   Q45697303: set the nb label
Q45697303	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45697303: set the da label
Q45697303	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45697303: set the sv label
Q45697303	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45697303: set the de label
Q45697303	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45697303: set the es label
Q45697303	Les	"hombre del clan Li, de Longxi Didao"
#   Q45697303: set the it label
Q45697303	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45697303: set the pt label
Q45697303	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45697303: set the ca label
Q45697303	Lca	"home del clan Li, de Longxi Didao"
#   Q45698977 (李 of 隴西狄道): mul label = NN
Q45698977	Lmul	"NN"
#   Q45698977: set the nb label
Q45698977	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45698977: set the da label
Q45698977	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45698977: set the sv label
Q45698977	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45698977: set the de label
Q45698977	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45698977: set the es label
Q45698977	Les	"hombre del clan Li, de Longxi Didao"
#   Q45698977: set the it label
Q45698977	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45698977: set the pt label
Q45698977	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45698977: set the ca label
Q45698977	Lca	"home del clan Li, de Longxi Didao"
#   Q45699052 (李 of 隴西狄道): mul label = NN
Q45699052	Lmul	"NN"
#   Q45699052: set the nb label
Q45699052	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699052: set the da label
Q45699052	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699052: set the sv label
Q45699052	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699052: set the de label
Q45699052	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699052: set the es label
Q45699052	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699052: set the it label
Q45699052	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699052: set the pt label
Q45699052	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699052: set the ca label
Q45699052	Lca	"home del clan Li, de Longxi Didao"
#   Q45699104 (李 of 隴西狄道): mul label = NN
Q45699104	Lmul	"NN"
#   Q45699104: set the nb label
Q45699104	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699104: set the da label
Q45699104	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699104: set the sv label
Q45699104	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699104: set the de label
Q45699104	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699104: set the es label
Q45699104	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699104: set the it label
Q45699104	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699104: set the pt label
Q45699104	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699104: set the ca label
Q45699104	Lca	"home del clan Li, de Longxi Didao"
#   Q45699589 (李 of 潤州): mul label = NN
Q45699589	Lmul	"NN"
#   Q45699589: set the nb label
Q45699589	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699589: set the da label
Q45699589	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699589: set the sv label
Q45699589	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699589: set the de label
Q45699589	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699589: set the es label
Q45699589	Les	"hombre del clan Li, de Runzhou"
#   Q45699589: set the it label
Q45699589	Lit	"uomo del clan Li, da Runzhou"
#   Q45699589: set the pt label
Q45699589	Lpt	"homem do clã Li, de Runzhou"
#   Q45699589: set the ca label
Q45699589	Lca	"home del clan Li, de Runzhou"
#   Q45699613 (李 of 潤州): mul label = NN
Q45699613	Lmul	"NN"
#   Q45699613: set the nb label
Q45699613	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699613: set the da label
Q45699613	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699613: set the sv label
Q45699613	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699613: set the de label
Q45699613	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699613: set the es label
Q45699613	Les	"hombre del clan Li, de Runzhou"
#   Q45699613: set the it label
Q45699613	Lit	"uomo del clan Li, da Runzhou"
#   Q45699613: set the pt label
Q45699613	Lpt	"homem do clã Li, de Runzhou"
#   Q45699613: set the ca label
Q45699613	Lca	"home del clan Li, de Runzhou"
#   Q45699639 (李 of 潤州): mul label = NN
Q45699639	Lmul	"NN"
#   Q45699639: set the nb label
Q45699639	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699639: set the da label
Q45699639	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699639: set the sv label
Q45699639	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699639: set the de label
Q45699639	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699639: set the es label
Q45699639	Les	"hombre del clan Li, de Runzhou"
#   Q45699639: set the it label
Q45699639	Lit	"uomo del clan Li, da Runzhou"
#   Q45699639: set the pt label
Q45699639	Lpt	"homem do clã Li, de Runzhou"
#   Q45699639: set the ca label
Q45699639	Lca	"home del clan Li, de Runzhou"
#   Q45699665 (李 of 潤州): mul label = NN
Q45699665	Lmul	"NN"
#   Q45699665: set the nb label
Q45699665	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699665: set the da label
Q45699665	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699665: set the sv label
Q45699665	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699665: set the de label
Q45699665	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699665: set the es label
Q45699665	Les	"hombre del clan Li, de Runzhou"
#   Q45699665: set the it label
Q45699665	Lit	"uomo del clan Li, da Runzhou"
#   Q45699665: set the pt label
Q45699665	Lpt	"homem do clã Li, de Runzhou"
#   Q45699665: set the ca label
Q45699665	Lca	"home del clan Li, de Runzhou"
#   Q45699690 (李 of 潤州): mul label = NN
Q45699690	Lmul	"NN"
#   Q45699690: set the nb label
Q45699690	Lnb	"mann av Li-slekten, fra Runzhou"
#   Q45699690: set the da label
Q45699690	Lda	"mand af Li-slægten, fra Runzhou"
#   Q45699690: set the sv label
Q45699690	Lsv	"man av Li-ätten, från Runzhou"
#   Q45699690: set the de label
Q45699690	Lde	"Mann des Klans Li, aus Runzhou"
#   Q45699690: set the es label
Q45699690	Les	"hombre del clan Li, de Runzhou"
#   Q45699690: set the it label
Q45699690	Lit	"uomo del clan Li, da Runzhou"
#   Q45699690: set the pt label
Q45699690	Lpt	"homem do clã Li, de Runzhou"
#   Q45699690: set the ca label
Q45699690	Lca	"home del clan Li, de Runzhou"
#   Q45699766 (李 of 隴西狄道): mul label = NN
Q45699766	Lmul	"NN"
#   Q45699766: set the nb label
Q45699766	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699766: set the da label
Q45699766	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699766: set the sv label
Q45699766	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699766: set the de label
Q45699766	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699766: set the es label
Q45699766	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699766: set the it label
Q45699766	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699766: set the pt label
Q45699766	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699766: set the ca label
Q45699766	Lca	"home del clan Li, de Longxi Didao"
#   Q45699789 (李 of 隴西狄道): mul label = NN
Q45699789	Lmul	"NN"
#   Q45699789: set the nb label
Q45699789	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699789: set the da label
Q45699789	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699789: set the sv label
Q45699789	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699789: set the de label
Q45699789	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699789: set the es label
Q45699789	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699789: set the it label
Q45699789	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699789: set the pt label
Q45699789	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699789: set the ca label
Q45699789	Lca	"home del clan Li, de Longxi Didao"
#   Q45699816 (李 of 隴西狄道): mul label = NN
Q45699816	Lmul	"NN"
#   Q45699816: set the nb label
Q45699816	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699816: set the da label
Q45699816	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699816: set the sv label
Q45699816	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699816: set the de label
Q45699816	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699816: set the es label
Q45699816	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699816: set the it label
Q45699816	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699816: set the pt label
Q45699816	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699816: set the ca label
Q45699816	Lca	"home del clan Li, de Longxi Didao"
#   Q45699868 (李 of 隴西狄道): mul label = NN
Q45699868	Lmul	"NN"
#   Q45699868: set the nb label
Q45699868	Lnb	"mann av Li-slekten, fra Longxi Didao"
#   Q45699868: set the da label
Q45699868	Lda	"mand af Li-slægten, fra Longxi Didao"
#   Q45699868: set the sv label
Q45699868	Lsv	"man av Li-ätten, från Longxi Didao"
#   Q45699868: set the de label
Q45699868	Lde	"Mann des Klans Li, aus Longxi Didao"
#   Q45699868: set the es label
Q45699868	Les	"hombre del clan Li, de Longxi Didao"
#   Q45699868: set the it label
Q45699868	Lit	"uomo del clan Li, da Longxi Didao"
#   Q45699868: set the pt label
Q45699868	Lpt	"homem do clã Li, de Longxi Didao"
#   Q45699868: set the ca label
Q45699868	Lca	"home del clan Li, de Longxi Didao"
#   Q45700460 (李 of 秦州成紀): mul label = NN
Q45700460	Lmul	"NN"
#   Q45700460: set the nb label
Q45700460	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700460: set the da label
Q45700460	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700460: set the sv label
Q45700460	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700460: set the de label
Q45700460	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700460: set the es label
Q45700460	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700460: set the it label
Q45700460	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700460: set the pt label
Q45700460	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700460: set the ca label
Q45700460	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700483 (李 of 秦州成紀): mul label = NN
Q45700483	Lmul	"NN"
#   Q45700483: set the nb label
Q45700483	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700483: set the da label
Q45700483	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700483: set the sv label
Q45700483	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700483: set the de label
Q45700483	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700483: set the es label
Q45700483	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700483: set the it label
Q45700483	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700483: set the pt label
Q45700483	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700483: set the ca label
Q45700483	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700509 (李 of 秦州成紀): mul label = NN
Q45700509	Lmul	"NN"
#   Q45700509: set the nb label
Q45700509	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700509: set the da label
Q45700509	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700509: set the sv label
Q45700509	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700509: set the de label
Q45700509	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700509: set the es label
Q45700509	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700509: set the it label
Q45700509	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700509: set the pt label
Q45700509	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700509: set the ca label
Q45700509	Lca	"home del clan Li, de Qinzhou Chengji"
#   Q45700685 (李 of 秦州成紀): mul label = NN
Q45700685	Lmul	"NN"
#   Q45700685: set the nb label
Q45700685	Lnb	"mann av Li-slekten, fra Qinzhou Chengji"
#   Q45700685: set the da label
Q45700685	Lda	"mand af Li-slægten, fra Qinzhou Chengji"
#   Q45700685: set the sv label
Q45700685	Lsv	"man av Li-ätten, från Qinzhou Chengji"
#   Q45700685: set the de label
Q45700685	Lde	"Mann des Klans Li, aus Qinzhou Chengji"
#   Q45700685: set the es label
Q45700685	Les	"hombre del clan Li, de Qinzhou Chengji"
#   Q45700685: set the it label
Q45700685	Lit	"uomo del clan Li, da Qinzhou Chengji"
#   Q45700685: set the pt label
Q45700685	Lpt	"homem do clã Li, de Qinzhou Chengji"
#   Q45700685: set the ca label
Q45700685	Lca	"home del clan Li, de Qinzhou Chengji"
#
# -------------------------------------------------------------------------
# THE CLAN PREFIX, on a NAMED person. Not one of the 177 above.
#
# Emma, 2026-08-29: "Put Futohime in the queued up clan block and just make sure
# we are implementing the idea in question". The idea is the clan prefix, and it
# is already carried by every other CJK person in entity_resolution.md -- checked
# live that day: Q24890131 reads "Mononobe no Ikofutsu", Q135579474 "Kitajima no
# Tokitaka", Q135579480 "Kitajima no Yasutaka". Futohime is the one straggler.
#
# Her instruction in entity_resolution.md is older and unambiguous: "change her
# name to 'Mononobe no Futohime'". Live 2026-08-29 the item read en "Futohime",
# with mul, ja and zh all empty and no aliases.
#
# The outgoing "Futohime" is kept as an Amul rather than lost: mul was empty, so
# nothing of hers is overwritten and the bare given name stays searchable.
#
# ja and zh are left alone for the same reason the block above leaves them alone.
# Her Geni name is 太媛, so 物部太媛 is the obvious Japanese form -- and "obvious"
# is not the standard here, and she has not been asked.
# -------------------------------------------------------------------------
#   Q11443857: keep the outgoing label as an alias before replacing it
Q11443857	Amul	"Futohime"
#   Q11443857 Futohime: mul label = Mononobe no Futohime
Q11443857	Lmul	"Mononobe no Futohime"
#   Q11443857: set the en label
Q11443857	Len	"Mononobe no Futohime"
"""


def spine_created():
    """Every Geni id that sits on a spine path — these never seed a ring of their own.

    **The defect this closes.** Emma's spine rule is right and stays: the ancestral couples
    from Arne through Bergitte to Charlemagne are made every run, outside the caps. But each
    one then entered the ledger, and the next run drew on it like any other seed and grew a
    ring around it. After several days the ball had lobes at the far end of a 34-step medieval
    path, and a batch of 36 held a 7th-century Baekje royal, Carolingian Friuli and
    20th-century Iowa alongside Rogaland farmers. Emma: *"there are tons of completely random
    people that were created."*

    They stay in `have`, so nothing re-creates them. They are simply not somewhere the ring
    grows from. The spine advances along the path, one step per path per run, which is what she
    asked for and all she asked for.
    """
    ids = set()
    for steps in spine_steps().values():
        ids.update(gid for _label, gid, _name in steps)
    return ids


def spine_steps():
    """`{path: [(label, geni_id, name)]}` -- BOTH spine paths, kept apart.

    **Kept apart deliberately.** Concatenating them and taking the first uncreated step
    advances only whichever path is listed first, so `bergitte-to-emma` never moved and the
    *"critical path going to me"* stayed at zero of sixteen. One step per path per run.
    """
    out = {}
    for rel in SPINE_PATHS:
        path = ROOT / rel
        if not path.exists():
            continue
        rows = [l.rstrip(chr(10)).split(chr(9)) for l in
                open(path, encoding="utf-8") if not l.startswith("#") and l.strip()]
        header = rows[0]
        steps = []
        for r in rows[1:]:
            d = dict(zip(header, r))
            gid = re.sub(r"\D", "", d.get("note", "") or "")
            if gid:
                steps.append((f"{Path(rel).stem} step {d.get('step')}", gid,
                              d.get("name", "")))
        out[rel] = list(reversed(steps)) if rel in SPINE_REVERSED else steps
    return out


def compose(our_items, fam, rng, ring_seeds=None):
    """`{geni_id: why}` -- the people this run creates, per `docs/daily-algorithm.md`.

    **Emma's revised algorithm, 2026-08-26**, written after she stopped a run of 50
    creations partway through: *"creating individuals with all of their children is just
    crazy talk."* The old shape drew 28 of its 50 from one component -- five couples with
    their *entire* children, one of which had eleven.

    The new shape is two caps, one substitution and one free rule:

    1. **The spine, always, outside the caps.** *"The ancestral couples between Bergitte,
       going from Arne to Bergitte to Charlemagne, are always getting made."* Both saved
       paths are walked, so the line down to her advances every run as well as the line up
       to Charlemagne -- she doubted the last run produced the *"critical path going to
       me"*, and it did not: all 16 steps of `paths/bergitte-to-emma.tsv` were uncreated.
    2. **Ten children.** A random person who has an uncreated child gets **one** child.
       *"you go to a person, and then it adds a child."*
    3. **The substitution.** *"If the person has a childless marriage, then it can generate
       their spouse instead."* So a person picked in step 2 who has a spouse we lack and no
       child to add contributes the spouse. There is **no independent spouse bucket** --
       her earlier *"10 spouses"* was revised away in the same message.
    4. **Ten parents.** A random person missing a parent gets one. *"then the next run it
       generates the child's parent."*
    5. **Free parents, not counted against the ten.** *"if a child is present and it appears
       like they have a single mother or single father, then the next time they get their
       parents for free."*

    `have` is the ball: every Geni id we can already point at a Wikidata item.
    `fam` is `reports/derived-family.csv` keyed by Geni id.
    """
    ring_seeds = our_items if ring_seeds is None else ring_seeds

    def kin(g, col):
        # The strip is load-bearing: `derived-family.csv` separates with ` | `, and
        # returning the raw token made 59 people a run resolve to nothing.
        return [x.strip() for x in re.split(r"[,;|]", (fam.get(g) or {}).get(col) or "")
                if x.strip() and x.strip() in fam]

    picked, why = {}, []

    def take(gid, reason):
        if gid and gid not in our_items and gid not in picked:
            picked[gid] = reason
            return True
        return False

    # --- 1. the spine, both directions, outside every cap ------------------------
    # One step per PATH, so the line down to her advances every run as well as the line up
    # to Charlemagne. Her words: *"The ancestral couples ... are always getting made."*
    spine_added = 0
    for rel, steps in spine_steps().items():
        for label, gid, name in steps:
            if take(gid, f"spine: {label}"):
                spine_added += 1
                why.append(f"1. spine {label}: {name}")
                for sp in kin(gid, "spouses"):
                    if take(sp, f"spouse of spine {label}"):
                        spine_added += 1
                break
        else:
            why.append(f"1. spine {Path(rel).stem}: every step already has an item")

    # --- 2 & 3. ten children, or a spouse where the marriage is childless --------
    # The seed pool, not the whole ledger: spine steps are excluded upstream.
    pool = sorted(ring_seeds)
    rng.shuffle(pool)
    kids = spouses_instead = 0
    for g in pool:
        if kids + spouses_instead >= CHILDREN_PER_RUN:
            break
        new_kids = [k for k in kin(g, "children") if k not in our_items and k not in picked]
        if new_kids:
            # ONE child, not all of them. This is the change.
            if take(rng.choice(new_kids), f"child of {g}"):
                kids += 1
            continue
        new_spouses = [x for x in kin(g, "spouses")
                       if x not in our_items and x not in picked]
        if new_spouses and take(rng.choice(new_spouses), f"spouse of childless couple {g}"):
            spouses_instead += 1
    why.append(f"2. {kids}/{CHILDREN_PER_RUN} children, one per person")
    why.append(f"3. {spouses_instead} spouses instead, where the marriage had no child "
               f"left to add")

    # --- 4. ten parents ----------------------------------------------------------
    rng.shuffle(pool)
    parents = 0
    for g in pool:
        if parents >= PARENTS_PER_RUN:
            break
        missing = [p for p in kin(g, "father") + kin(g, "mother")
                   if p not in our_items and p not in picked]
        if missing and take(rng.choice(missing), f"parent of {g}"):
            parents += 1
    why.append(f"4. {parents}/{PARENTS_PER_RUN} parents, one per person")

    # --- 5. free parents for anyone half-attached --------------------------------
    # Her rolling rule. A person with one parent linked and the other never created is
    # the structural wart the old algorithm left behind; this closes them as it goes.
    # **Every half-attached person is eligible; the budget is `10 + half the rest`.**
    # Her formula. The eligible set is counted first and the budget derived from it, so the
    # number is a function of the backlog rather than of iteration order.
    eligible = []
    # Bounded the same way: a half-attached person 40 hops out is still a real wart,
    # but repairing it is not what 'one hop a day from Arne' means.
    for g in sorted(set(ring_seeds) | set(picked)):
        father, mother = kin(g, "father"), kin(g, "mother")
        if not father or not mother:
            continue
        known = [x for x in father + mother if x in our_items or x in picked]
        absent = [x for x in father + mother if x not in our_items and x not in picked]
        if known and absent:
            eligible.append((g, absent[0]))
    budget = free_parent_budget(len(eligible))
    rng.shuffle(eligible)
    free = 0
    for g, missing in eligible:
        if free >= budget:
            break
        if take(missing, f"free parent: {g} had only one"):
            free += 1
    why.append(f"5. {free} free parents of {len(eligible)} eligible "
               f"(10 free + half the remaining = {budget}), outside the cap")

    return picked, why


def main():
    # `--skip-nn` is a per-run choice, not a rule. Emma, 2026-08-24: *"for this
    # quickstatements run the NN people are not worth creating"* -- for THIS run. The
    # standing rule in `CLAUDE.md` is that redacted people go in, with the marker in
    # `mul` and a formulaic description elsewhere, so this must not become the default.
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-nn", action="store_true",
                    help="omit redacted/NN people from this batch (a per-run choice)")
    # **Emma, 2026-08-25:** *"Since it is clear that there are way too many people to do
    # everything, we focus on ancestry and in-laws that get to my item."* Without this the
    # frontier is every edge out of every item that has a QID -- 138 creations in all
    # directions on the day this was added -- and most of them lead away from her rather
    # than toward Charlemagne or toward Arne.
    #
    # The roster is a file of Geni ids, one per line or in a `geni_id` column;
    # `reports/charlemagne-route.csv` is the 399-step Emma-to-Charlemagne spine and
    # `paths/isolate-geni-aadne-eivindson-garborg-1851-1924.tsv` is the Emma-to-Arne pair
    # of paths. Spouses of roster members are kept too -- those are the in-laws she named.
    ap.add_argument("--roster", action="append", default=[], metavar="FILE",
                    help="restrict the ring to these Geni ids (repeatable)")
    # **The ledger is only who EMMA created.** `reports/charlemagne-route.csv` carries 383
    # people who already had a Wikidata item long before this programme, with their QIDs in
    # a `qid` column — and the "both ends must exist" rule needs those to count as existing,
    # or the ring around them is empty and the route can never be worked. Without this the
    # roster filter cut the ring to zero: the 41 items she has made are Arne's family, and
    # the route is her own ancestry, which touches them only at the far end.
    ap.add_argument("--known", action="append", default=[], metavar="FILE",
                    help="CSV/TSV with geni_id and qid columns of items that already exist")
    # **In-laws are opt-in, because they are the bulk.** With the Charlemagne route as the
    # roster, the spine itself needs 16 creations and adding spouses took that to 510 --
    # far past the "up to 4 people a day" the queue asks for. The spine first, the in-laws
    # when the spine is done.
    ap.add_argument("--in-laws", action="store_true",
                    help="also include spouses of roster members")
    ap.add_argument("--compose", action="store_true",
                    help="build the batch to docs/batch-rules.md instead of taking the "
                         "whole one-edge ring: spine couple, 4 random parent sets, 4 "
                         "random families off a solitary individual, 1 existing couple's "
                         "children, and the sibling links the additions pass emits.")
    ap.add_argument("--exclude", action="append", default=[], metavar="QS",
                    help="a .qs already produced today; everyone it CREATES is held out of "
                         "this batch. Two runs on the same day both see a ledger that has "
                         "not caught up yet, so without this the second run re-creates "
                         "people the first one already makes -- 4 of 9 on the first attempt.")
    ap.add_argument("--roster-is-frontier", action="store_true",
                    help="take the roster AS the people to create, instead of using it to "
                         "filter the one-edge ring. Needed for the spine, whose middle sits "
                         "many edges from anyone holding a QID. Every guard still applies.")
    ap.add_argument("--seed", type=int, default=0, metavar="N",
                    help="seed for --compose, so a run is reproducible.")
    ap.add_argument("--no-refresh", action="store_true",
                    help="do NOT read her Wikidata contributions first. Only for offline "
                         "work: the batch is then built against whatever the ledger last "
                         "recorded, which is how items she has already made get re-created.")
    ap.add_argument("--limit", type=int, default=0, metavar="N",
                    help="create only the N people closest to Arne (0 = no limit)")
    args = ap.parse_args()

    # **A bare run is a DIFFERENT PROGRAM, and it overwrites a committed day.**
    #
    # Measured 2026-08-27 by doing it: bare, this emits **272 creations**; with `--compose` --
    # the flag `build-daily-batch.py` passes, and where `CHILDREN_PER_RUN`, `PARENTS_PER_RUN`,
    # `FREE_PARENTS_FREE` and `SIBLING_CAP` all live -- it emits **34**. The bare path is not a
    # smaller daily algorithm; it skips the algorithm.
    #
    # Both write `reports/wikidata-garborg-day.qs`, so a bare run silently replaces a batch Emma
    # may already have run, and `--compose` itself ADVANCES the sequence: it consumes and
    # rewrites `reports/garborg-carry-forward.tsv`, so re-running it on the same day produced a
    # batch differing by 19 people out and 17 in -- the next hop, not today's.
    #
    # `--roster` runs are a real second mode and stay allowed. What is refused is the
    # argument-free invocation, which has no purpose except the mistake.
    if not args.compose and not args.roster:
        sys.exit(
            "refusing an argument-free run: it skips the daily caps (272 creations against 34) "
            "and overwrites reports/wikidata-garborg-day.qs, which may be a day already run.\n"
            "  the daily batch:  python scripts/build-daily-batch.py\n"
            "  this script only: --compose (the daily algorithm) or --roster FILE")

    # **Her contributions are read EVERY run, before anything else.**
    #
    # Emma, 2026-08-28: *"this is worrying since it seems to indicate that you might be
    # building the ledger as a separate part from the script, when in reality the script is
    # supposed to go through my contributions and update the ledger every time."* It was
    # separate, and it cost exactly what she predicted: a batch built at 17:33 used a ledger
    # refreshed hours earlier, so `Q141198835` Bergitte Gunnbjørnsdatter Aukland — the hinge of
    # all three lines, which she had just created — read as missing, and the spine reported the
    # Charlemagne path as unable to reach her.
    #
    # It **fails the run** rather than falling back to the file on disk. A stale ledger does not
    # look like an error, it looks like work to do, and the work it invents is re-creating items
    # she already made.
    if args.compose and not args.no_refresh:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "refresh-garborg-ledger.py")],
                           cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            sys.exit("the ledger refresh failed, so the batch would be built against a stale "
                     "picture of what Emma has already created:\n"
                     + (r.stderr or r.stdout)[-800:])
        print((r.stdout or "").strip().splitlines()[-1] if r.stdout.strip() else
              "ledger refreshed")

        # **And the live values, for the same reason.** `add()` drops a statement the item
        # already holds by checking `reports/garborg-live-values.tsv`; if that file is stale the
        # check silently passes and the batch re-emits things she has already done. Measured
        # 2026-08-27: the file was 21 hours old and covered 131 of 209 ledger items, so 78
        # people had no dedupe at all. This is the same defect as the ledger being refreshed
        # separately, which she ruled on the same day — *"the script is supposed to go through
        # my contributions and update the ledger every time."*
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "refresh-live-values.py")],
                           cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            sys.exit("the live-values refresh failed, so every duplicate check would silently "
                     "pass and the batch would re-emit statements already on Wikidata:\n"
                     + (r.stderr or r.stdout)[-800:])
        print((r.stdout or "").strip().splitlines()[-1] if r.stdout.strip() else
              "live values refreshed")

    our_items = ledger()

    # **`linked` is every Geni id Wikidata already carries a `P2600` for. `have` is not.**
    #
    # These are two different questions and conflating them cost a run: `have` seeds the
    # FRONTIER ("everyone one edge from somebody with a QID"), so folding 517,750 ids into it
    # made the frontier most of the tree and the build never finished. `linked` answers only
    # "would creating this person duplicate an item", which is a set lookup.
    #
    # The gap this closes was caught by `tests/test_p2600_batches.py` on `5101295410550070399`,
    # whose item exists and was about to be duplicated. The parent-`P40` duplicate guard does
    # not cover it: that fires when a PARENT has an unmatched child item, and here the person
    # themselves is already present.
    #
    # This is the offline half of the check Emma rejected in its live form -- *"we are noy gonna
    # do a fuckin glive P2600 check"* -- and it costs nothing, because the file is on disk. It
    # is a floor, not the whole answer: the map predates every item she has made, which is why
    # `scripts/refresh-garborg-ledger.py` reads her contributions separately.
    any_wikidata_item = {}
    p2600_all = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if p2600_all.exists():
        with open(p2600_all, encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                    any_wikidata_item.setdefault(row[1].strip(), row[0])
        print(f"{len(any_wikidata_item):,} Geni ids already carry a P2600 somewhere on Wikidata")
    else:
        print("WARNING: out/wikidata/p2600-all.tsv missing - a person whose item nobody here "
              "made is invisible and could be created twice")
    for path in args.known:
        with open(path, encoding="utf-8") as f:
            head = f.readline()
            f.seek(0)
            rd = csv.DictReader(f, delimiter="\t" if "\t" in head else ",")
            n = 0
            for row in rd:
                # `candidate_qid` is what `reports/spine-already-on-wikidata.tsv` calls the
                # column, and that file is the canonical list of spine people who already have
                # an item. Without this it reads as having no QIDs at all and the batch offers
                # to CREATE seven people who exist -- the Q2183430 failure, on the exact
                # population most carefully checked against it.
                g = (row.get("geni_id") or "").strip()
                q = (row.get("qid") or row.get("candidate_qid") or "").strip()
                if g.isdigit() and q.startswith("Q") and g not in our_items:
                    our_items[g] = q
                    n += 1
        print(f"{n} already-existing items read from {path}")
    table = translit()
    plan = load_plan()
    fam_p, fam_c, fams, famc = read_tree()
    print(f"{len(our_items)} people already carry a QID; {len(table)} tokens transliterated")

    # Everyone one edge away from somebody who has a QID.
    to_create = {}
    if args.roster_is_frontier:
        # **The roster IS the frontier.** `--roster` alone cannot build the spine: it FILTERS
        # the one-edge ring, and steps 4-22 sit many edges away from anybody holding a QID --
        # that distance is the whole reason the spine needs building. Filtering a ring they are
        # not in returns nothing, which reads as "no work to do".
        #
        # This is the mode `queue.md`'s pinned last item asks for: *"queue says to build the
        # thing that makes a lot of them"*. Every other guard still applies -- the modern
        # cutoff, the duplicate guard, `linked`, `--exclude` -- so it is a different way of
        # CHOOSING people, not a way of skipping checks.
        for path in args.roster:
            text = Path(path).read_text(encoding="utf-8")
            for gid in re.findall(r"(?:geni:)?(\d{10,})", text):
                if gid not in our_items:
                    to_create.setdefault(gid, "")
        print(f"--roster-is-frontier: {len(to_create)} people taken straight from "
              f"{len(args.roster)} roster file(s), not from the one-edge ring")
    else:
        for person in our_items:
            for fam in fams.get(person, []) + famc.get(person, []):
                for other in set(fam_p.get(fam, [])) | set(fam_c.get(fam, [])):
                    if other not in our_items:
                        to_create.setdefault(other, fam)
        print(f"{len(to_create)} people one edge away and not yet on Wikidata")

    # **There is no birth-year filter, deliberately.** `MODERN_CUTOFF = 1880` lived here
    # from 2026-08-25 to 2026-08-27. It came from one objection to one person -- *"no we
    # are no fuckin gmaking my father as a wikidata item right now lol"* -- generalised
    # into a demographic exclusion nobody asked for, and it was dead code under
    # `--compose` the whole time, filtering a ring that `compose()` then replaced while
    # printing a reassuring "112 dropped". Emma, 2026-08-27: **"totally undesired"**, and
    # *"Yes I explicitly want my father created"*. Do not reintroduce it in any form.

    if args.roster:
        # **Find the ids by pattern, not by parsing the file's shape.** Two attempts
        # failed before this one, both silently: the first accepted only bare digits and
        # missed `geni:6000000003492005116`; the second sniffed the delimiter from line
        # one, which in a path file is a `#` comment with no tab, so a TSV was read as
        # CSV and every row came back as one uncut string. Both reported "0 ids" and cut
        # the ring to nothing, which looks exactly like "there is no work to do".
        wanted = set()
        for path in args.roster:
            text = Path(path).read_text(encoding="utf-8")
            found = set(re.findall(r"(?:geni:)?(\d{10,})", text))
            print(f"  {len(found)} Geni ids in {path}")
            wanted |= found

        # **In-laws means SPOUSES, not everyone in the family.** The first cut unioned
        # every parent and child of every family a roster member appears in, which took the
        # ring from 138 to 2569 -- it pulled in whole sibling sets and their descendants,
        # which is the sprawl the roster exists to stop. A spouse is the *other parent* of
        # a family the roster member parents, and that is all this adds.
        near = set(wanted)
        if args.in_laws:
            for person in wanted:
                for fam in fams.get(person, []):
                    near |= set(fam_p.get(fam, []))
        before = len(to_create)
        to_create = {g: f for g, f in to_create.items() if g in near}
        print(f"roster: {len(wanted)} ids from {len(args.roster)} file(s); "
              f"ring cut {before} -> {len(to_create)} (roster members and their in-laws)")

    # ---- THE COMPOSITION replaces the ring entirely, when asked for -------------
    if args.compose:
        fam_rows = {}
        with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                fam_rows[row["geni_id"]] = row
        # Seeded so a run is reproducible and reviewable. `Math.random`-style
        # irreproducibility would make a batch impossible to explain after the fact.
        rng = random.Random(args.seed)
        # **The seed pool is the Wikidata subgraph reachable from Arne — her algorithm.**
        #
        # Not the ledger, which is "every item Emma has made" and therefore includes her Izumo
        # and Kitajima work; not a hop radius, which was my invention and cut a batch to 7.
        # A person seeds a ring when Wikidata already connects them to Arne by any chain of
        # relationship statements, however long.
        our_wikidata_subgraph = wikidata_subgraph(universe=set(our_items.values()))
        ring_seeds = {g for g, q in our_items.items() if q in our_wikidata_subgraph}
        print(f"contiguous group from Arne {ARNE_QID} and Bureus {BUREUS_QID}, through her own "
              f"items: {len(our_wikidata_subgraph)} items; {len(ring_seeds)} of {len(our_items)} ledger people seed")
        if not ring_seeds:
            sys.exit(f"no ledger person is in the group reachable from {ARNE_QID}/{BUREUS_QID} "
                     f"— that is a broken join over relations.tsv/garborg-live-values.tsv, not "
                     f"an unconnected Arne")
        picked, why = compose(our_items, fam_rows, rng, ring_seeds=ring_seeds)
        print("\ncomposition, per docs/batch-rules.md:")
        for line in why:
            print("   " + line)
        before = len(to_create)
        to_create = {g: to_create.get(g, "") for g in picked}
        compose_why = picked
        print(f"composed batch: {len(to_create)} people to create "
              f"(the unrestricted ring would have been {before})")
    else:
        compose_why = {}

    # **`--exclude` applies to EVERY batch shape, not only `--compose`.** It lived inside the
    # compose branch, so a `--roster` run ignored it completely -- which is how a roster batch
    # came out re-creating two people an earlier batch the same day had already given Emma.
    # A guard that silently does not run is worse than none, because it gets reported as
    # protection. Her verdict on exactly that: *"you even said you deduplicated and then you
    # just didn't."*
    #
    # The ledger only catches up once she has actually run a file, so within a single day this
    # is the only thing keeping two batches disjoint.
    # `carried` collects everyone held back, with the reason. Defined here rather than beside
    # `lines` because the exclusion and duplicate checks below both append to it.
    carried = []

    # Anyone Wikidata already links is never created, whatever the batch shape asked for.
    dup = [g for g in to_create if g in any_wikidata_item and g not in our_items]
    for g in dup:
        to_create.pop(g, None)
        carried.append((g, "", f"Wikidata already links this profile as {any_wikidata_item[g]} "
                               f"(out/wikidata/p2600-all.tsv) - creating it would duplicate"))
    if dup:
        print(f"{len(dup)} dropped: Wikidata already carries a P2600 for them")

    already = set()
    for path in args.exclude:
        already |= set(re.findall('P2600\\t"(\\d+)"',
                                  Path(path).read_text(encoding="utf-8")))
    if already:
        drop = [g for g in to_create if g in already]
        for g in drop:
            to_create.pop(g, None)
        print(f"--exclude: {len(already)} created by an earlier batch today, "
              f"{len(drop)} of them dropped from this one")


    ids = set(to_create) | set(our_items)
    facts, labels = {}, {}
    #: How a person is named when SOMEBODY ELSE's label refers to them -- the married
    #: form where there is one. Separate from `labels` on purpose; see the comment at
    #: the assignment below.
    referred_to_as = {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                facts[row["geni_id"]] = row
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                # **Fall back to the NON-LATIN name before calling somebody unnamed.**
                # 55,547 people in `derived-labels.csv` have `label_en` and `label_mul`
                # both empty while carrying a name in `cjk_names` (44,028) or
                # `other_script_names` (11,519); only 22,174 are genuinely nameless.
                # Without this they reach the redacted branch and are created as a bare
                # `NN`, losing a name Geni actually recorded --
                # `6000000186285688241`, whose name is `부여융 무명`, is the case Emma's
                # batch surfaced.
                #
                # `CLAUDE.md` § *Do not confuse redacted with unnamed* is exactly this
                # distinction: the test is never "is the label bad", it is "is there
                # anything real underneath it".
                raw_label = (
                    row["label_en"] or row["label_mul"]
                    or (row.get("cjk_names") or "").split(" | ")[0].strip()
                    or (row.get("other_script_names") or "").split(" | ")[0].strip())
                # **An unknown-name marker never becomes part of a name.** Geni records
                # `Sara /NN/` — given name Sara, surname field the marker `NN`, meaning the
                # surname is unknown — and `display_name` concatenates the fields, so the label
                # reached this batch as `Sara NN` and would have been written to Wikidata as
                # what she is called. `NN` is a statement that a name is missing.
                #
                # Only stripped when a real name survives. A label that is nothing but markers
                # is left exactly as it is, so the NN treatment below still fires and
                # § *`NN` is PRESERVED in `mul`* holds.
                # **Stored RAW.** Normalising the marker here destroys the signal the
                # redacted branch keys on: `<private> Garborg` became `NN Garborg`, the
                # `"<private>" in low` test then failed, and three redacted people took the
                # ordinary-name path — so they got `Len "NN Garborg"` and none of the ten
                # formulaic descriptions. `strip_markers` belongs where a label is emitted
                # for a person who is NOT redacted, which is the `Sara NN` case.
                labels[row["geni_id"]] = raw_label
                # **How a person is named when somebody ELSE's label refers to them.**
                #
                # Emma, 2026-08-29, on `Q141205933`: *"it appears that it uses the birth name
                # of the wife. This is concerning and it may mean that a lot of places
                # primarily use the birth names of women and this causes inconsistency"*.
                #
                # It was an inconsistency between two layers of this one file.
                # `derived-labels.csv` puts the BIRTH name in `label_mul` and the married one
                # in `aliases_from_married_name` -- 185,426 women. The CREATION path never
                # reads those columns; it recomputes primary-vs-birth from raw `SURN`/`_MARNM`
                # and correctly makes the married name primary, per § *The MARRIED name is the
                # real name*. `describe_all` read `labels`, so one run created a woman as
                # `Thelma Geraldine Bagby` while calling a man "husband of Mona Beth Tunheim",
                # her BIRTH name -- two readings of one rule in a single file.
                #
                # A SEPARATE dict rather than changing `labels`, because `labels` also feeds
                # `name_lines`, where the birth surname and the married surname are DIFFERENT
                # `P734` statements carrying different `P3831` roles (`Q2507958` birth name,
                # `Q28418670` married name). Overwriting it there would put the married form
                # into both slots and lose the distinction the name model is built on.
                # `derive-labels.py` now emits the MARRIED form as `label_en`/`label_mul`,
                # so `raw_label` already is the name a relative should be called by. The
                # dict stays as the seam: it is what `describe_all` reads, and keeping it
                # separate from `labels` is still right, because `labels` feeds
                # `name_lines` where birth and married surnames are two DIFFERENT `P734`
                # statements (`Q2507958` birth name, `Q28418670` married name).
                referred_to_as[row["geni_id"]] = raw_label

    # **The GEDCOM name FIELDS, which is where name objects come from.** Emma,
    # 2026-08-24: *"I thought we were resolving name objects but now we're determining
    # which name field to use as a source of the label?"* -- catching that the name
    # model was re-parsing the rendered label. The first NAME record wins; later ones
    # are alternate forms and `derive-labels.py` already owns those.
    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids and row["geni_id"] not in fields:
                # `display_name` is the name GENI renders, untouched by our married-name
                # flip -- it is what `P1810` *subject named as* must carry. Emma, 2026-08-28:
                # *"I want us to have the property P1810 with the specific name geni gives
                # them."* Taking it from the same first row is the point: `derived-labels.csv`
                # holds our derived label, which is a different claim.
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm", "display_name")}

    # Relationships, from the tree, in both directions.
    father, mother = {}, {}
    children = collections.defaultdict(set)
    spouses = collections.defaultdict(set)
    siblings = collections.defaultdict(set)
    for fam, parents in fam_p.items():
        kids = fam_c.get(fam, [])
        for p in parents:
            for k in kids:
                children[p].add(k)
                sex = (facts.get(p, {}).get("sex") or "")
                (father if sex == "M" else mother)[k] = p
        for a in parents:
            for b in parents:
                if a != b:
                    spouses[a].add(b)
        for a in kids:
            for b in kids:
                if a != b:
                    siblings[a].add(b)

    lines = []
    # ---- THE DUPLICATE GUARD -------------------------------------------------------
    # **Emma, 2026-08-25, after running a batch:** *"you also kinda immediately just fucked
    # up with making a person who has an item see here
    # https://www.wikidata.org/wiki/Q2183430"*.
    #
    # `Q2183430` is *Benedicta Ebbesdotter of Hvide*, b.1165 d.1199, father `Q16063657`. The
    # batch created a second item for her -- same father, same death year, and it even wrote
    # `Benedicta` as her nickname, which is that item's own label. She was in our local store
    # the whole time with 30 properties on her.
    #
    # **Why nothing caught it.** The builder knew about existing items two ways only:
    # `garborg-qids.tsv`, the 41 people Emma had made, and `p2600-all.tsv`, items carrying a
    # `P2600`. `Q2183430` has no `P2600`, so it was invisible to both.
    #
    # **The check that does catch it is the parent's own child list.** `Q16063657`'s `P40` is
    # `Q2183430; Q12320052; Q116150300` -- the duplicate was sitting in a list the batch
    # already had a QID for. So: before creating anyone, look at every parent of theirs that
    # has a QID, and if that parent has a `P40` child item **not already matched to one of
    # our people**, refuse. The person being created may BE that item.
    #
    # This is conservative on purpose and will hold back people who really are new, whenever
    # a sibling of theirs has an unmatched item. Holding a real person back costs a day;
    # creating a duplicate costs Emma a manual merge on a public database.
    #
    # `out/wikidata/relations.tsv` (scripts/extract-wikidata-relations.py) carries `P40` for
    # every item in the store, so this is a dict lookup rather than a shard read.
    #
    # **THE MIRROR, and it is the half Emma actually complained about.** 2026-08-29:
    # *"you appear to be actively creating rival parent profiles in a way that is harmful. For
    # eample this one had to be mered."*
    #
    # The `P40` check above is the CHILD direction: it holds a person whose parent already has
    # unclaimed children. It says nothing about the PARENT direction -- creating a father for a
    # child who, on Wikidata, already declares one. Only `p40` was ever loaded here, so
    # `P22`/`P25` were never consulted and a rival parent could not be seen.
    #
    # So: before creating anyone, look at every CHILD of theirs that has a QID, and if that
    # child already declares a `P22`/`P25` parent item **not matched to one of our people**,
    # refuse. The person being created may BE that item.
    #
    # Same conservatism and same trade as the child direction: holding a real person back costs
    # a day, creating a rival costs Emma a manual merge on a public database.
    kids_of = {}
    parents_of = {}
    #: `P22`/`P25` kept apart, for the single-value guard at the end of the run.
    wd_fathers, wd_mothers = {}, {}
    rel = ROOT / "out" / "wikidata" / "relations.tsv"
    if rel.exists():
        with open(rel, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="	"):
                if row.get("p40"):
                    kids_of[row["qid"]] = [x for x in row["p40"].split(";") if x]
                ps = [x for c in ("p22", "p25") for x in (row.get(c) or "").split(";") if x]
                if ps:
                    parents_of[row["qid"]] = ps
                for c, into in (("p22", wd_fathers), ("p25", wd_mothers)):
                    for x in (row.get(c) or "").split(";"):
                        if x:
                            into.setdefault(row["qid"], set()).add(x)
        print(f"{len(kids_of):,} items with a P40 child list, for the duplicate guard")
        print(f"{len(parents_of):,} items with a P22/P25 parent, for the rival-parent "
              f"guard ({len(wd_fathers):,} with a father, {len(wd_mothers):,} with a "
              f"mother, for the single-value guard)")

    # The store predates most of the ledger, so a person Emma created this week has no row in
    # it. `reports/garborg-live-values.tsv` is refreshed every run and carries the current
    # statements for exactly those people, which is where a fresh rival would show up.
    live = ROOT / "reports" / "garborg-live-values.tsv"
    if live.exists():
        with open(live, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="	"):
                if row.get("property") in ("P22", "P25") and row.get("value", "").startswith("Q"):
                    parents_of.setdefault(row["qid"], [])
                    if row["value"] not in parents_of[row["qid"]]:
                        parents_of[row["qid"]].append(row["value"])
                    into = wd_fathers if row["property"] == "P22" else wd_mothers
                    into.setdefault(row["qid"], set()).add(row["value"])
    else:
        print("WARNING: out/wikidata/relations.tsv missing - duplicate guard is OFF")

    claimed = set(our_items.values())
    blocked = {}
    for g in list(to_create):
        if g in RELEASED_FROM_DUPLICATE_GUARD:
            print(f"   released from the duplicate guard: {labels.get(g, g)} -- "
                  f"{RELEASED_FROM_DUPLICATE_GUARD[g]}")
            continue
        hit = None
        for parent in (father.get(g), mother.get(g)):
            pq = our_items.get(parent) if parent else None
            if not pq:
                continue
            loose = [k for k in kids_of.get(pq, []) if k not in claimed]
            if loose:
                hit = (pq, loose, "child")
                break

        # The mirror: a child of theirs already names a parent item we do not hold.
        if hit is None:
            for c in children.get(g, ()):
                cq = our_items.get(c)
                if not cq:
                    continue
                loose = [x for x in parents_of.get(cq, []) if x not in claimed]
                if loose:
                    hit = (cq, loose, "parent")
                    break

        if hit is not None:
            blocked[g] = hit
    if blocked:
        kinds = collections.Counter()
        for g, (other, loose, kind) in blocked.items():
            kinds[kind] += 1
            what = ("parent {0} has unmatched child item(s) {1} - this person may already be one"
                    if kind == "child" else
                    "child {0} already names parent item(s) {1} - this person may already be one")
            carried.append((g, labels.get(g, ""),
                            "HELD by the duplicate guard: "
                            + what.format(other, ";".join(loose[:4]))))
            to_create.pop(g, None)
        print(f"duplicate guard held {len(blocked)} people "
              f"({kinds['child']} whose parent has an unmatched child item, "
              f"{kinds['parent']} whose child already names a parent item)")

    # `--skip-nn` must bite BEFORE `--limit`, or the limit spends slots on people the run
    # is about to drop: asking for 10 named people returned 7, because 3 of the 10 closest
    # were redacted and were removed afterwards.
    if args.skip_nn:
        dropped = [g for g in to_create
                   if (labels.get(g, "").strip().lower().startswith(("nn", "private", "<private"))
                       or not labels.get(g, "").strip())]
        for g in dropped:
            to_create.pop(g, None)
            carried.append((g, labels.get(g, ""), "redacted: skipped by --skip-nn for this run"))
        if dropped:
            print(f"--skip-nn: {len(dropped)} redacted people held for a later run")

    # ---- order the ring by CLOSENESS TO ARNE ---------------------------------------
    # Emma: *"I want to build more connected Arne Garborg individuals"* and
    # *"we maybe make 10 people connected to Arne Garborg"*. The ring was emitted in label
    # order, which is alphabetical and meaningless. Distance is measured over the same
    # parent/child/spouse edges the tree records.
    ARNE = "6000000003492005116"
    dist, seen_d = {ARNE: 0}, [ARNE]
    while seen_d:
        nxt = []
        for x in seen_d:
            for y in (list(children.get(x, ())) + list(spouses.get(x, ()))
                      + [father.get(x), mother.get(x)]):
                if y and y not in dist:
                    dist[y] = dist[x] + 1
                    nxt.append(y)
        seen_d = nxt
    ring_order = sorted(to_create, key=lambda g: (dist.get(g, 10**6), labels.get(g, "")))
    if args.limit:
        keep = set(ring_order[:args.limit])
        for g in list(to_create):
            if g not in keep:
                carried.append((g, labels.get(g, ""),
                                f"beyond --limit {args.limit}; "
                                f"{dist.get(g, '?')} steps from Arne"))
                to_create.pop(g, None)
        ring_order = [g for g in ring_order if g in keep]
        print(f"--limit {args.limit}: keeping the {len(ring_order)} closest to Arne "
              f"({dist.get(ring_order[0], '?')}-{dist.get(ring_order[-1], '?')} steps)")


    def ref(g):
        return f'\tS2600\t"{g}"'

    # ---- 1. everything missing from people who ALREADY have QIDs ------------
    # Emma, 2026-08-24, asked whether to add properties to items that already exist:
    # yes. This section used to close *links* only, so an item that existed was never
    # asked whether it was missing a date, a name statement or a label -- which is a
    # large part of what "not remotely comprehensive" meant. `Q467497` Arne Garborg
    # had no `P22` father and no `P25` mother while both his parents had QIDs.
    state = existing_state(set(our_items.values()))
    # A live read beats both the store and the guess. `reports/garborg-live-state.tsv`
    # records what each item held on 2026-08-24; the store predates most of them and
    # the fallback below assumes our own batch made them, which is wrong wherever Emma
    # edited by hand. Eivind is the case: he carries P735/P734/P5056 she added herself.
    state.update(live_state())
    live_values = read_live_values()
    # **The order of the two sections is her spec and it is structurally rigid.** Emma,
    # 2026-08-26: *"Creation of individuals comes first, then creation of names, then the
    # relationships between the individuals... The order itself is structurally rigid because
    # it depends on certain things being capable of being referenced in certain situations."*
    # This file emitted relationships first until 2026-08-26. Both sections are built in the
    # order the code finds convenient and CONCATENATED in her order at the end -- see
    # `preamble`, `rel_from` and `create_from` below.
    preamble = len(lines)
    lines += [
        "# RELATIONSHIPS between items that already exist -- the links yesterday's",
        "#    creations made possible, and the properties never emitted. Every subject",
        "#    and every value already has a QID, so this section depends on nothing above",
        "#    it. It is emitted LAST, per her order: individuals, names, relationships.",
        "",
    ]
    rel_from = preamble
    seen = set()

    def named_as(g):
        """The `\\tP1810\\t"..."` qualifier for this person, or `""` where there is nothing to say.

        **Emma, 2026-08-28:** *"I want us to have the property P1810 with the specific name geni
        gives them."* So the value is `display_name` from `display-names.csv` — the name GENI
        renders — and never our own label, which since 2026-08-29 is the married form we chose.
        `P1810` is a plain `string` qualifier and it belongs on an external identifier: confirmed
        offline against `wikidata/items/`, where every `P1810` sits on one (`P396`, `P1280`,
        `P8034`, `P12458`). Hanging it on `P2600` is that shape, not an invention.

        **A redaction marker goes in VERBATIM here, and only here.** Emma ruled on this
        2026-08-29, choosing the literal string over both the reconstructed `NN Garborg` and
        omitting the qualifier: `P1810` documents what the source database literally shows, so
        `<private> Garborg` is the true and useful value. That is a **narrow exception** to
        § *Redacted people go in. `Private` never becomes a label*, and the reason the two do
        not conflict is that they are different claims — a *label* asserts what the person is
        called, and this asserts what Geni displays. Her `mul` label stays `NN Garborg`.

        So the marker is barred from every label and permitted in exactly one qualifier;
        `tests/test_garborg_day_batch.py` enforces the line rather than leaving it to memory.
        """
        raw = (fields.get(g) or {}).get("display_name", "")
        return f'\tP1810\t"{qs(raw)}"' if raw else ""

    def add(q, prop, value, g, qual=""):
        # `qual` is a ready-made qualifier fragment, tab-prefixed, and is deliberately NOT
        # part of the dedupe key: a statement is the same statement whether or not we also
        # say what the source database called the person.
        if (q, prop, value) in seen:
            return
        # **Never re-emit a statement the item already states.** Emma, 2026-08-27, on the
        # relationship section never shrinking: *"the relationship one is questionable that
        # it's always gonna be so huge and growing."* Measured that day: **229 of 306**
        # statements on existing items were already on Wikidata, 75% of the section.
        #
        # `absent()` could not have caught them. It is property-level -- it knows an item has
        # SOME `P40`, not which children -- and it reads a file frozen at 2026-08-24. And
        # `P40`, `P26` and `P3373` never consulted it at all, so every child, spouse and
        # sibling link went out on every run. QuickStatements merges a duplicate rather than
        # failing, which is why nothing ever broke.
        if (q, prop, value.strip('"')) in live_values:
            return
        seen.add((q, prop, value))
        lines.append(f"{q}\t{prop}\t{value}{qual}{ref(g)}")

    def absent(q, prop):
        """True when the item demonstrably lacks `prop`, or our own batch made it.

        The store answers exactly for an item it holds. For one it does not hold --
        Emma's creations from the last two days -- what the item carries is what our
        `CREATE` block carried, and name statements were only added on 2026-08-24, so
        those are genuinely absent. Either way QuickStatements merges an identical
        statement rather than duplicating it, so a redundant line is a no-op.
        """
        known = state.get(q)
        return prop not in known[1] if known else True

    for g, q in sorted(our_items.items()):
        before_this_person = len(seen)
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in our_items and absent(q, prop):
                add(q, prop, our_items[target], g)
        for kid in sorted(children.get(g, ())):
            if kid in our_items:
                add(q, "P40", our_items[kid], g)
        for sib in sorted(siblings.get(g, ())):
            if sib in our_items:
                if sibling_budget_left() <= 0:
                    carried.append((g, labels.get(g, ""),
                                    f"P3373 sibling {our_items[sib]} held: over the "
                                    f"{SIBLING_CAP}-a-day cap"))
                    continue
                _siblings_emitted.append((q, our_items[sib]))
                add(q, "P3373", our_items[sib], g)
        for sp in sorted(spouses.get(g, ())):
            if sp in our_items:
                add(q, "P26", our_items[sp], g)

        # **If we linked this person to anybody, write their Geni id too.**
        #
        # Emma, 2026-08-27: *"we should have a thing that allows the algorithm to, when it's
        # attaching people together, add in a Geni ID... Link a person to their parent who's an
        # actual person in the tree, and add onto the parent the parent's geni ID."* Asked which
        # people should get it, she chose **only when actually linked in that batch** rather
        # than every ledger member — so it is self-limiting: an item gets its `P2600` at the
        # moment the algorithm asserts a relationship about it, and never otherwise.
        #
        # Why it matters beyond tidiness: a pairing that exists only in
        # `reports/garborg-qids.tsv` is invisible to Wikidata, so a ledger rebuilt from her
        # contributions cannot recover it. Writing the statement makes the pairing resolvable
        # by anyone, including the next rebuild. `add()` drops it if the item already has it.
        if len(seen) > before_this_person:
            # Same `P1810` *subject named as* qualifier as the creation path, so an item
            # that gets its Geni id late is not modelled differently from one created with it.
            add(q, "P2600", f'"{g}"', g, named_as(g))

        # Name statements, but never onto an item that already states one: `Q467497`
        # carries `P735` Arne, and our label reads the parenthesised `(Arne)` as a
        # middle name -- emitting it would contradict a curated statement rather than
        # add to it. `CLAUDE.md`: the purpose is to ADD, not to correct.
        if absent(q, "P735") and absent(q, "P734"):
            dad = father.get(g)
            # The father's NAME, not just his QID: Emma's test reads his given name and
            # his own patronymic to decide whether this token is inherited or derived.
            for line in name_lines(labels.get(g, ""), plan, g,
                                   our_items.get(dad) if dad else None,
                                   father_name=labels.get(dad, "") if dad else "")[0]:
                lines.append(line.replace("LAST\t", f"{q}\t", 1))

        # A label ONLY in a language the item does not have. `Len`/`Lmul` REPLACE,
        # and `Q467497` is labelled `Arne Garborg` on Wikidata against our derived
        # `Aadne (Arne) Eivindson Garborg` -- emitting ours would overwrite a better
        # label with a Geni display string.
        langs = state.get(q, (set(), set()))[0]
        ja, zh = label_in(labels.get(g, ""), table)
        if ja:
            for code, value in (("ja", ja), ("zh", zh)):
                if code not in langs:
                    lines.append(f'{q}\tL{code}\t"{value}"')
    print(f"{len(seen)} statements added to existing items")
    lines.append("")

    # ---- 2. the next ring ---------------------------------------------------
    create_from = len(lines)
    lines += ["# INDIVIDUALS. Each is linked only to items that already exist; links",
              "#    between two people created here wait for tomorrow, when they have",
              "#    QIDs -- two items minted in one batch cannot point at each other.",
              ""]
    created = 0
    for g in sorted(to_create, key=lambda x: labels.get(x, "")):
        f, label = facts.get(g), qs(expand_abbreviations(
            without_nickname(labels.get(g, ""), fields.get(g)), g))
        if not f:
            carried.append((g, label, "no derived facts"))
            continue

        # A redacted profile is created and gets NO label. `CLAUDE.md`: *"Private is
        # a redaction marker, not a name, and an item labelled that asserts something
        # false while being impossible to find. The P2600 is what makes it
        # retrievable."* The person is real and none of the structure is redacted —
        # the Geni id, the sex, the parents, the dates all come through.
        low = label.lower()
        # **An unknown-name marker of ANY kind takes the NN treatment, not just `<private>`.**
        # This tested for Geni's redaction markers only, so `NN Jonsdotter` — whose Geni name
        # is literally that — took the ordinary-name path and `NN` went out in her `en` label
        # with no description. `reports/partial-nn.csv` counts **9,539** people with a marker
        # in one name field and a real name in the other; every one of them belongs here.
        redacted = ("<private>" in low or low.startswith("private")
                    or _carries_marker(label))
        if redacted and args.skip_nn:
            carried.append((g, label, "redacted: skipped by --skip-nn for this run"))
            continue

        block_start = len(lines)
        lines.append("CREATE")
        # **Both branches must leave these bound.** The alias block below reads them after
        # the branch, and the redacted branch never set them -- so creating a redacted
        # person crashed with `UnboundLocalError`. It went unseen because the unfiltered
        # ring happened to contain no redacted people; restricting the ring to Emma's own
        # ancestry surfaced it immediately. A redacted person has no married-name alias to
        # emit, so empty strings are the right values, not a guard around the block.
        primary, birth = _strip_markers(label) or label, ""
        if redacted or not label:
            # **NOT unlabelled.** `CLAUDE.md` § *`NN` is PRESERVED in `mul`.
            # Descriptive labels are ADDED in other languages* -- the marker stays in
            # `mul` and every local language gets a formulaic description built from
            # the nearest named relative. Emma, 2026-08-16: *"NN and private are the
            # same thing here"*. The surname survives redaction and is real data, so
            # `mul` reads `NN Garborg`, not a bare `NN`.
            # The surname survives redaction and is real data -- CLAUDE.md measured
            # 3,605 such profiles. `<private> Garborg` -> `Garborg`.
            from labels import drop_marker_surname as _dms
            lines.append(f'LAST	Lmul	"{_dms(nn_form(qs(labels.get(g, ""))))}"')
            described = describe_all(g, facts, father, mother, referred_to_as, table,
                                     children, spouses, siblings)
            for code, value in sorted(described.items()):
                lines.append(f'LAST\tL{code}\t"{value}"')
            if not described:
                carried.append((g, label, "redacted: no named relative to describe by"))
        else:
            # **The MARRIED name is the primary label; the BIRTH name is an alias.**
            # Emma, 2026-08-24, after running the first batch: *"the married name is
            # the primary label and the birth name is amul"*, then *"we move the lmul
            # to amul and the lja to aja and so on"*. The first version had it exactly
            # backwards -- birth name in `en` and `mul`, married name pushed out as an
            # `Aen` alias -- and cost her a corrective run over five items.
            f_ = fields.get(g, {})
            surn = " ".join((f_.get("surn") or "").split())
            marnm = " ".join((f_.get("marnm") or "").split())
            # `SURN` must be populated for `_MARNM` to mean *married*: `CLAUDE.md`
            # measured 43% of `_MARNM` values as the ONLY surname on the record, where
            # it is the family name rather than a married one.
            is_married = bool(marnm and surn and marnm.casefold() != surn.casefold())

            given = [t for t, u, _o in classify_fields(f_.get("givn", ""), "")
                     if u in ("given", "patronymic")]
            # **The expansion has to happen HERE, not on `label`.** For a married person
            # `primary` is rebuilt out of the raw `GIVN` and `_MARNM` fields, so an expansion
            # applied to `label` upstream is thrown away -- which is exactly how
            # `Anne Govertsdtr. Bratland` kept its abbreviation through two rebuilds while
            # `expand_abbreviations` tested correct in isolation. Married people are the
            # majority of the batch, so the upstream call alone fixed almost nobody.
            primary = expand_abbreviations(
                " ".join(given + marnm.split()), g) if is_married else label
            birth = expand_abbreviations(
                " ".join(given + surn.split()), g) if is_married else ""

            # **A marker in the SURNAME slot never reaches a label.** Emma, 2026-08-29, on
            # `Q141217396` coming out *Maria No name*: *"I would say I just use it by its
            # first name."* `is_marker_label` tests the whole label or a LEADING marker, so
            # `unknown Bloomfield` was caught and `Maria No name` was not -- and Geni puts
            # the marker in `SURN`, which is always the trailing position.
            from labels import drop_marker_surname
            primary = drop_marker_surname(primary, marnm, surn)
            birth = drop_marker_surname(birth, surn) if birth else birth

            # **`en` only for a name written in Latin script.** The non-Latin fallback
            # above rescues 55,547 people from being created as a bare `NN`, but their
            # name is Korean or Chinese and an ENGLISH label holding it is wrong twice
            # over -- it is not English, and `Help:Default values for labels and aliases`
            # says a name not in Latin script should not be a default label. `mul` is the
            # language-neutral slot and takes it.
            if re.search(r"[A-Za-z]", primary):
                lines.append(f'LAST\tLen\t"{qs(primary)}"')
            lines.append(f'LAST\tLmul\t"{qs(primary)}"')
            # **No `Aen`. Ever.** Emma, 2026-08-26: *"No aen are ever supposed to be
            # added lol only ones in non-latin scripts get aliases for their birth names
            # that are not in amul"*. The birth name is an `Amul` and nothing else; the
            # `Aja`/`Azh` below are the one exception, and only because a non-Latin form
            # cannot live in `mul`.
            if birth and qs(birth) != qs(primary):
                lines.append(f'LAST\tAmul\t"{qs(birth)}"')

            ja, zh = label_in(primary, table)
            if ja:
                lines.append(f'LAST\tLja\t"{ja}"')
                lines.append(f'LAST\tLzh\t"{zh}"')
                bja, bzh = label_in(birth, table) if birth else (None, None)
                if bja and bja != ja:
                    lines.append(f'LAST\tAja\t"{bja}"')
                    lines.append(f'LAST\tAzh\t"{bzh}"')
            else:
                carried.append((g, label, "no transliteration for every token"))
        lines.append(f"LAST\tP31\t{HUMAN}")
        if f["sex"] in SEX:
            lines.append(f"LAST\tP21\t{SEX[f['sex']]}")
        # **`P1810` *subject named as*, qualifying the Geni id with the name Geni renders.**
        # Emma, 2026-08-28: *"I want us to have the property P1810 with the specific name geni
        # gives them."* Datatype confirmed OFFLINE against the downloaded item store rather
        # than guessed: every `P1810` in `wikidata/items/` is a plain `string` qualifier and
        # every one of them sits on an external identifier -- `P396`, `P1280`, `P8034`,
        # `P12458` -- so hanging it on `P2600` is the established shape, not an invention.
        #
        # The value is `display_name` from `display-names.csv`, NOT our label: the point of
        # the property is what the source database calls the person, and our label is the
        # married form we chose on 2026-08-29. They differ for exactly the people it matters
        # for.
        lines.append(f'LAST\tP2600\t"{g}"{named_as(g)}')
        for prop, iso, prec in (("P569", f["birth_date_iso"], f["birth_date_precision"]),
                                ("P570", f["death_date_iso"], f["death_date_precision"])):
            if iso and prec:
                lines.append(f"LAST\t{prop}\t{iso}/{prec}{ref(g)}")
        # **`LAST` IS valid as a VALUE, and this batch never used it.**
        #
        # Emma, 2026-08-25: *"you never actually did the 2-way relationship addin qith the
        # creation of items that is completely possible but you just decide to fuck off and
        # no do it because it goes QID PID LAST instead of LAST PID QID"*.
        #
        # She is right and the error was mine. `LAST` cannot be the value in a statement
        # whose subject is *also* newly created -- two items minted in one run cannot point
        # at each other, because `LAST` names only the most recent. That is a real limit and
        # it is the one she described in the batch-rules dictation. **It says nothing about a
        # statement whose subject already exists**: `Q467497 P40 LAST` is ordinary
        # QuickStatements and resolves to the item this block just made.
        #
        # Generalising the narrow limit into "no reciprocals at all" is what produced the
        # one-way links she has been having to fix by hand, and `build-missing-reciprocals.py`
        # exists only because of it. Every relationship to somebody who ALREADY has a QID is
        # now emitted in both directions in the same run.
        reciprocal = []
        for prop, target, back in (("P22", father.get(g), "P40"),
                                   ("P25", mother.get(g), "P40")):
            if target and target in our_items:
                lines.append(f"LAST\t{prop}\t{our_items[target]}{ref(g)}")
                reciprocal.append((our_items[target], back, g))
        for sp in sorted(spouses.get(g, ())):
            if sp in our_items:
                lines.append(f"LAST\tP26\t{our_items[sp]}{ref(g)}")
                reciprocal.append((our_items[sp], "P26", g))
        # **The cap is 10 a day ACROSS EVERY BATCH, and this site was escaping it.**
        # `CLAUDE.md` § *`P3373` sibling is capped at 10 a day*: *"A builder emitting
        # siblings must count them and stop."* The additions pass counted; this one, on the
        # people being CREATED, did not -- so a run came out with 10 capped statements and
        # **28 uncapped**, 38 in a file whose whole reason for the cap is that Emma finds
        # sibling links spammy on a watchlist. `_siblings_emitted` is shared module state
        # precisely so both sites draw on one budget.
        for sib in sorted(siblings.get(g, ())):
            if sib in our_items:
                if sibling_budget_left() <= 0:
                    carried.append((g, label, f"P3373 sibling {our_items[sib]} held: over the "
                                    f"{SIBLING_CAP}-a-day cap"))
                    continue
                _siblings_emitted.append(("LAST", our_items[sib]))
                lines.append(f"LAST\tP3373\t{our_items[sib]}{ref(g)}")
                reciprocal.append((our_items[sib], "P3373", g))
        for kid in sorted(children.get(g, ())):
            if kid in our_items:
                lines.append(f"LAST\tP40\t{our_items[kid]}{ref(g)}")
                sex_of = (facts.get(g, {}) or {}).get("sex", "")
                reciprocal.append((our_items[kid], "P22" if sex_of == "M" else "P25", g))

        # **The other direction, in the SAME run.** `Q… P… LAST` -- the subject already
        # exists, so QuickStatements resolves `LAST` to the item created just above.
        # This is what makes the batch two-way instead of leaving one-way links behind.
        for subject, prop, source in reciprocal:
            lines.append(f"{subject}\t{prop}\tLAST{ref(source)}")

        # The name model. Emma, 2026-08-24: *"we should be modelling the names
        # properly, which he didn't do."* Only tokens whose item ALREADY exists --
        # the ones still to be made are in reports/wikidata-garborg-name-items.qs and
        # join the batch the day after that runs, same single-run rule as everyone.
        # A redacted profile gets no name statements for the same reason it gets no
        # label: `<private>` is Geni withholding the name, not a name. Asking the plan
        # for a `<private>` given-name item produced three "name item missing" rows
        # that read as work to do, when the right answer is that there is nothing
        # underneath. The *surname* survives redaction and is real data -- but these
        # three are `<private> Garborg`, and `Garborg` is their father's family name,
        # which `P22` already says.
        if not redacted:
            dad = father.get(g)
            name_statements, unresolved = name_lines(
                labels[g], plan, g, our_items.get(dad) if dad else None,
                fields=fields.get(g), sex=f["sex"],
                father_name=labels.get(dad, "") if dad else "")
            lines.extend(name_statements)
            # Aliases: the nickname, and the full name under a married surname. Emma
            # asked for these alongside the second `P734` *family name*.
            # An alias identical to the label is noise. Now that the married name is
            # the primary label, `aliases_for`'s married-full-name alias often
            # duplicates it exactly -- `Aen "Inger Kristoffersdatter"` sitting beside
            # `Len "Inger Kristoffersdatter"`. The birth-name alias is already emitted
            # with the labels above, so this carries only what those do not.
            # **An alias is an `Amul` and nothing else.** Emma, 2026-08-26: *"No aen are
            # ever supposed to be added"*. This block wrote both, and before 2026-08-25 it
            # wrote `Aen` alone — an alias that exists only in `en` is invisible to every
            # other language, which is why `mul` is the one that matters and `en` is the
            # one that never applies.
            emitted = {qs(primary), qs(birth)}
            for alias in aliases_for(fields.get(g, {})):
                if qs(alias) and qs(alias) not in emitted:
                    lines.append(f'LAST	Amul	"{qs(alias)}"')
                    emitted.add(qs(alias))
            for note in unresolved:
                carried.append((g, label, f"name item missing: {note}"))

        # **A creation with NO relationship is not shipped. It is carried.**
        #
        # Emma, 2026-08-29, on `Anders Persson`: *"where the fuck is this in the tree? why
        # no relationships... relationships on creation is the thin that keeps items from
        # being deleted"*. She is right, and a bare `instance of human` with a `P2600` and
        # nothing else is exactly what gets nominated for deletion.
        #
        # The cause was a composition bug, not an emission one. Rule 3 picks a person **for**
        # a spouse — and when that spouse is also being created today, the same-run limit
        # (`LAST` names only the most recent item) strips the one link they were chosen for.
        # Anders Persson and Peder Tormodson Foss both arrived this way: every other relative
        # of theirs has no QID, and the single relative that mattered was in the same file.
        #
        # Holding them costs nothing. Tomorrow the spouse has a QID and the link is ordinary.
        if not any(re.match(r"^(LAST|Q[0-9]+)	(P22|P25|P26|P40|P3373)	", ln)
                   for ln in lines[block_start:]):
            del lines[block_start:]
            carried.append((g, label,
                            "no relationship could be emitted: every relative either has no "
                            "QID or is being created in this same batch"))
            continue

        lines.append("")
        created += 1

    # Her order, applied at the last moment so neither section's construction has to
    # care: preamble, then the INDIVIDUALS this run creates, then the RELATIONSHIPS
    # between items that already existed. Names are the middle step and live in
    # `reports/wikidata-garborg-name-items.qs`, run between the two.
    lines = lines[:preamble] + lines[create_from:] + lines[rel_from:create_from]

    # **Drop every statement the item already holds, as a POST-PASS.** The check inside
    # `add()` caught only what `add()` emitted; the name-statement block appends to `lines`
    # directly, so 81 of 98 concrete-valued statements survived it. This file emits from a
    # dozen places and a rule applied at each call site is a rule missed at the thirteenth --
    # the same reason the per-line comments are a post-pass.
    #
    # `LAST` is never dropped: it names an item being created in this run, so the statement
    # cannot already exist. Labels and aliases are never dropped either -- they REPLACE, and
    # whether to send one is a different question from whether a claim is present.
    if live_values:
        kept, dropped = [], 0
        for line in lines:
            parts = line.split(chr(9))
            if (len(parts) >= 3 and parts[0].startswith("Q") and parts[1].startswith("P")
                    and parts[2] != "LAST"
                    and (parts[0], parts[1], parts[2].strip('"')) in live_values):
                dropped += 1
                continue
            kept.append(line)
        lines = kept
        print(f"{dropped} statements dropped: the item already holds them")

    # **A comment above every line.** Her format, 2026-08-26. `name_of` resolves either a
    # QID or a Geni id to a person, so the comments read as sentences rather than as pairs
    # of numbers; `qid_to_geni` inverts the ledger for that.
    qid_to_geni = {q: g for g, q in our_items.items()}

    def name_of(token):
        # **A redaction marker never reaches the file, not even as prose.** `qscomment` names
        # people from the raw display label, so `<private> Skårland` was appearing in comment
        # lines — asserting nothing on Wikidata, but writing out the marker `CLAUDE.md`
        # § *Redacted people go in. `Private` never becomes a label* exists to keep out. The
        # person is still named by whatever survives redaction, which for `<private> /Surname/`
        # is the surname — the part that is real data.
        geni = qid_to_geni.get(token, token)
        raw = labels.get(geni, "")
        low = raw.lower()
        if "<private>" in low or low.strip() == "private":
            raw = re.sub(r"(?i)<private>\s*", "", raw).strip() or "NN"
            raw = f"NN {raw}" if not raw.startswith("NN") else raw
        return qs(raw)

    lines = annotate(lines, name_of)

    # **The last gate: nothing Emma has excluded may reach the file, in any position.**
    #
    # Enforced here rather than only where statements are built, for the reason `qscomment`
    # gives about comments: this file emits from a dozen sites and a rule applied at each one
    # is a rule that will be missed at the thirteenth. It was — the batch of 2026-08-27 wrote
    # a `P22` and a `P25` onto her own item, attaching it to the
    # 1,339,227-person component containing Charlemagne, because her Geni id arrives through
    # `paths/bergitte-to-emma.tsv` whose step 1 is her.
    #
    # **A statement line is DROPPED; a `CREATE` for an excluded person REFUSES the run.**
    # Dropping a statement cannot change which item a later `LAST` resolves to — only a
    # dropped `CREATE` could do that — so the two cases are not the same risk and are not
    # treated the same way. The preceding comment goes with the line it describes.
    # **The kluge is enforced HERE too, not only in the subgraph walk.**
    #
    # **Emma, 2026-08-29:** *"im not assuming anything wrongly about the algorithm im assuming
    # you fucked the algorithm up at some point and it might try to do something with these
    # people."* That is the right premise, and removing them from the `universe` does not meet
    # it: `universe` only governs the subgraph walk, so it gates CREATIONS. The additions pass
    # iterates the whole ledger, and the three Buyeo people ARE in the ledger -- so a bug
    # anywhere upstream could still emit a statement about them.
    #
    # This filter is the last thing that touches the file, so it holds whatever the rest of the
    # algorithm did.
    #
    # **The 178 clan individuals are deliberately NOT here.** Her line, same day: *"we probably
    # are going to be changing their labelling in September, but being in the universe is not
    # going to happen until October."* They are blocked from the universe and their labels still
    # go out; excluding them here would silently drop the 15-a-day label drip.
    excluded = (NEVER_TOUCH_GENI | NEVER_TOUCH_QID
                | set(KLUGE_UNIVERSE_BLOCK) | set(KLUGE_ENTITY_RESOLUTION_ASIA))

    def names_excluded(line):
        return any(tok in line for tok in excluded)

    for i, ln in enumerate(lines):
        if ln.strip() == "CREATE":
            block = "\n".join(lines[i:i + 40])
            if any(f'P2600\t"{g}"' in block for g in NEVER_TOUCH_GENI):
                sys.exit(f"REFUSING to write: a CREATE at line {i + 1} would mint a new item "
                         f"for an excluded person. Emma, 2026-08-27: \"I should not be in the "
                         f"traversable graph.\"")

    kept, dropped = [], 0
    for ln in lines:
        if not ln.lstrip().startswith("#") and names_excluded(ln):
            while kept and kept[-1].lstrip().startswith("#"):
                kept.pop()
            dropped += 1
            continue
        kept.append(ln)
    if dropped:
        print(f"excluded ids: {dropped} statement line(s) dropped "
              f"({', '.join(sorted(excluded))}) — never emitted, in any position")

    # ---- NEVER give an item a SECOND father or mother -------------------------------
    #
    # **Emma, 2026-08-29, and her rule is narrower than "no duplicates":** *"my rule is not
    # explicitly a rule saying that we can't create duplicates. It's a more specific one...
    # We should not be adding the father property on something that already has a father
    # linked, or the mother property, because the father property being duplicated or the
    # mother property being duplicated gets flagged... this is the situation where it is
    # intended to be flagged, and then the flagging can cause potential issues."*
    #
    # So the thing to stop is the STATEMENT, not the person. `P22` and `P25` carry a
    # single-value constraint on Wikidata; a second one is what trips it, and a tripped
    # constraint is what gets our work noticed.
    #
    # **No exception is built for two fathers.** She raised it and dismissed it herself --
    # *"I think there's probably some exception for, I don't know, gay parents or something.
    # This isn't it."* Adding an exception nobody asked for is the over-engineering this repo
    # keeps having to undo.
    #
    # This sits beside the creation guard rather than replacing it. The guard holds the
    # PERSON before they are minted; this holds the LINE whatever produced it, including the
    # ledger-wide additions pass, which the guard never sees.
    # NB: iterate the PREVIOUS result under its own name. Rebinding `kept` before the loop
    # empties the very list being iterated, which silently drops the whole file.
    survivors, second_parent = [], []
    for ln in kept:
        m = re.match(r"^(Q\d+)	(P22|P25)	(\S+)", ln)
        if m:
            subject, prop, value = m.groups()
            held = (wd_fathers if prop == "P22" else wd_mothers).get(subject, set())
            if held and value not in held:
                while survivors and survivors[-1].lstrip().startswith("#"):
                    survivors.pop()
                second_parent.append((subject, prop, value, sorted(held)))
                continue
        survivors.append(ln)
    kept = survivors
    if second_parent:
        print(f"single-value guard: {len(second_parent)} P22/P25 line(s) dropped -- the item "
              f"already has one, and a second trips the constraint")
        for subject, prop, value, held in second_parent[:6]:
            print(f"   {subject} {prop} -> {value}; already has {';'.join(held)}")
    lines = kept

    # **The SPINE P2600 block is NOT emitted.** Emma, 2026-08-29: *"I wanted the spine entity
    # resolution geni id adding statements gone"*. `SPINE_P2600_BLOCK` stays defined -- it is
    # the record of nine pairings anchored on structure rather than on names, and
    # `reports/wikidata-spine-add-p2600.qs` carries the evidence -- but it no longer rides
    # along with every daily batch.

    # The CJK clan labels, same mechanism. See `CJK_CLAN_BLOCK`. **Removed on 2026-08-29 and
    # put straight back** -- I read *"remove that particular section"* as this block when she
    # meant the spine P2600 one. Emma: *"What the fuck the clan block is gone? Bring it the
    # fuck back"*.
    lines = _cap_label_edits(
        lines, CJK_CLAN_BLOCK,
        _label_corrections(our_items, labels, table, state) + _cjk_follows_mul(table))

    out = ROOT / "reports" / "wikidata-garborg-day.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT)}: {created} creations, {len(seen)} links")

    cf = ROOT / "reports" / "garborg-carry-forward.tsv"
    with open(cf, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "label", "why"])
        w.writerows(carried)
    print(f"wrote {cf.relative_to(ROOT)}: {len(carried)} carried to a later day")
    for g, label, why in carried[:10]:
        print(f"  {g}  {label[:40]:<40} {why}")


if __name__ == "__main__":
    main()
