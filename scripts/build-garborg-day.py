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

Writes `reports/wikidata-garborg-day.txt` and `reports/garborg-carry-forward.tsv`.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import csv
import os
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from datequals import date_quals  # noqa: E402
from namemodel import (  # noqa: E402
    aliases_for, classify, classify_fields, load_plan,
    normalise_generation_suffix, statements_for)


def _load_gaps():
    """`garborg-existing-gaps.py` has a hyphen, so `import` cannot reach it."""
    import importlib.util
    path = Path(__file__).resolve().parent / "garborg-existing-gaps.py"
    spec = importlib.util.spec_from_file_location("garborg_existing_gaps", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.existing_state


existing_state = _load_gaps()

NEWLINE = chr(10)
ROOT = Path(__file__).resolve().parent.parent

#: **Emma, 2026-08-25:** *"sibling relationships are too numerous to send at once.
#: We limit sibling relationship adding to 10 quickstatements a day."* This builder was
#: emitting **162** `P3373` in one file. Siblings grow as the SQUARE of a family -- nine
#: children is 72 statements by itself -- while parents grow linearly, so a batch that looks
#: balanced by people is mostly sibling links by statement. The cap is per DAY across every
#: batch, so it is shared with `build-missing-reciprocals.py`, and the overflow is carried
#: rather than dropped: the statements are correct, there are just too many at once.
SIBLING_CAP = 10
_siblings_emitted = []

SEX = {"M": "Q6581097", "F": "Q6581072"}

#: **The only two people whose CJK labels were not written by us.** Emma, 2026-08-30:
#: *"Arne Garborg and Johannes Bureus are the only people with cjk labels not added by us. So
#: only those ones are to be taken as gospel."*
#:
#: Checked live the same day, and both readings are visibly not ours -- our own transliterator
#: would never produce either:
#:
#:     Q467497  Arne Garborg     ja アルネ・ガルボルグ   zh 阿尔内·嘉宝
#:     Q633094  Johannes Bureus  ja ヨーハン・ブーレ     zh 约翰内斯·托马松
#:
#: `嘉宝` is the established Chinese rendering of *Garbo*, against our `加尔博格`; `ヨーハン・
#: ブーレ` is the Swedish reading, against our letter-by-letter one. Every other `ja`/`zh` on a
#: ledger item came from this pipeline, which is what makes redoing them safe.
CJK_LABELS_NOT_OURS = {"Q467497", "Q633094"}

#: **The Chinese overwrite is ON because the reason not to do it was fixed.** Emma,
#: 2026-08-30: *"is 塞恩 right for sen? Sounds like you made coda -n its own character instead
#: of merging them which sounds sussy for Chinese."* It was not right, and she named the cause:
#: `translit_no` gave every coda consonant its own character, so a syllable-final nasal came
#: out as a separate 恩 -- `sen` as 塞 + 恩 rather than 森. **1,701 rows carried the shape and
#: 1,201 a standalone 恩.**
#:
#: Her instruction on being shown a proposal to gate the Chinese half instead:
#: *"don't gate it, fucking fix it and then do the overwrite."* `translit_no.NASAL_FINAL` is
#: the fix; agreement with the rows the engine did not write went **11.7% -> 46.5%**, and
#: 1,078 cached rows were re-derived by `refresh-rule-transliterations.py`.
#:
#: Japanese was never affected: `ン` is a real mora, so `アブサロン` was always right.
ZH_OVERWRITE = True

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
    # **`entity_resolution.md` was deleted in `12f3134a` and its readers were not.**
    # Emma, 2026-08-31: *"no files should read it lol."* The block that stood here
    # folded that file's hand-asserted pairs into this lookup; the file has been gone
    # since 2026-08-29, so the block contributed nothing and only reported its own
    # absence. `CLAUDE.md` § *LEGACY CODE IS DELETED* is the rule and § *Systematic
    # review for legacy code* is the other half of it -- deleting the file is half the
    # job, and a reader that degrades quietly is the worse half.

    # **Emma's own identity confirmations, and they have to be READ, not appended once.**
    #
    # On 2026-08-31 she judged 13 blocked creations to be the same person as an existing
    # Wikidata item, one `AskUserQuestion` each, and asked: *"these quickstatements are gonna be
    # permanent right? Like the geni things aren't a random thing you added that will disappear
    # next run right"*. They were exactly that — appended to `reports/wikidata-garborg-day.txt`,
    # which this script rewrites from scratch every run. The next regeneration would have
    # silently dropped all 13 and gone back to proposing the creations she had just ruled out.
    #
    # `reports/emma-judgments.tsv` is the durable record — `CLAUDE.md` § *The chain of
    # provenance* already calls it the place her hand verdicts live, and says they are nodes in
    # the provenance graph rather than a side note. Folding it in here makes a confirmation
    # permanent in the only way that counts: the person is never created again, the item becomes
    # something statements can point AT, and it anchors its neighbours.
    try:
        # **`reports/manual-identifications.csv` is the file now, and it is a superset.**
        # Emma, 2026-09-01: *"we need to have the two identifications I did, and all other things
        # as being from a manual identification csv"*, and *"the right verdicts need to be
        # actually implemented"*.
        #
        # This used to read `emma-judgments.tsv` and accept only `SAME`, which left **17 `RIGHT`
        # verdicts inert** -- all from the 2026-08-25 `zipper-sample` batch, all carrying both
        # ids, every one an affirmation she made that nothing acted on. `RIGHT` is the older word
        # from before the deck settled on `SAME`; the fold never learned it.
        #
        # `build-manual-identifications.py` unions both verdicts with the pairs she gives
        # directly in conversation, so there is one file to read and one place to append.
        manual = ROOT / "reports" / "manual-identifications.csv"
        if manual.exists():
            with open(manual, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
                    if g.isdigit() and q.startswith("Q"):
                        out.setdefault(g, q)
        judgments = ROOT / "reports" / "emma-judgments.tsv"
        if judgments.exists() and not manual.exists():
            with open(judgments, encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="	"):
                    if row.get("verdict") not in ("SAME", "RIGHT"):
                        continue
                    g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
                    if g.isdigit() and q.startswith("Q"):
                        out.setdefault(g, q)
    except Exception as exc:                                        # noqa: BLE001
        print(f"WARNING: emma-judgments.tsv not folded into the ledger ({exc}) -- "
              f"a person she has confirmed could be created a second time")
    return out


def translit():
    out = {}
    with open(ROOT / "reports" / "garborg-name-transliterations.tsv",
              encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            # Three languages, not two. `ko` joined the table on 2026-09-01 and 96% of the
            # 18,536 tokens carry one; a row written before that has an empty `ko` and is
            # re-rendered by the funnel like any other gap.
            out[row["token"]] = (row["ja"], row["zh"], row.get("ko", ""))
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


def _relationship_prefixes():
    """`{"son of ", "sønn av ", "filla de ", ...}` -- every opening a DESCRIPTION can have.

    **A descriptive label is not a name, and the whole bug is that nothing said so.** The
    `en` label of a redacted person is `son of Astri Torchelsdatter Øvre Time` by design --
    `CLAUDE.md` § *The NN/Private label algorithm applies to EVERY unnamed person*. Two
    places then treated that sentence as the person's name.

    Built from `WORDS`, never restated: the table already holds the relationship word per sex
    and the preposition per direction (`datter af` but `mor til`), so a language added there
    is covered here with no second edit. Danish and Norwegian carry `of` as a dict keyed on
    the group, which is exactly that direction rule, so both forms are generated.
    """
    out = set()
    for words in WORDS.values():
        joiner = words["of"]
        for group, forms in words.items():
            if group == "of" or not isinstance(forms, dict):
                continue
            j = joiner.get(group, joiner[""]) if isinstance(joiner, dict) else joiner
            for word in forms.values():
                if word:
                    out.add(f"{word} {j} ".casefold())
    return frozenset(out)


RELATIONSHIP_PREFIXES = _relationship_prefixes()


def is_relationship_description(text):
    """True when `text` is one of our own descriptive labels rather than a name.

    **What it cost, measured on the 2026-09-03 batch.** `Q141249589` went out as
    `Amul "NN"` + `Lmul "son of Astri Torchelsdatter Øvre Time"` -- demoting the marker
    `CLAUDE.md` § *`NN` is PRESERVED in `mul`* says is *"always preserved"* -- and then as
    `Lja "ソン・オフ・アストリ・トルケルスダッテル・オヴレ・ティメ"`, which is the English words
    *son* and *of* spelled out in katakana. `zh` and `ko` the same: `松·奥夫·`, `손 오프`.
    Eight such labels in one batch, on a rolling window with 2,552 more behind it.

    The correct CJK form is built by `describe_all`, which puts the native relationship word
    after the name -- `…の息子`, `…之子`, `…의 아들`. Nothing here reconstructs it; this only
    stops a description being fed to the name transliterator, and the description keeps
    living in `en` and the other languages where it belongs.

    A PREFIX test, and deliberately not a search: `Anne of Denmark` is a name, and only a
    label that OPENS with a relationship word is one of ours.
    """
    low = (text or "").strip().casefold()
    return any(low.startswith(p) for p in RELATIONSHIP_PREFIXES)


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
        if any(low == w or low.startswith(w + " ") for w in markers):
            return ""
        # **A relative whose own label is one of these descriptions names nobody either**, and
        # it composes into nonsense rather than stopping: `daughter of father of`, and
        # `wife of Son of Menon III Pharsalos`. 21 of those are sitting in
        # `reports/wikidata-placeholder-labels.json`. Same fix as a marker -- fall through to
        # the next relative, never reconstruct.
        return "" if is_relationship_description(n) else n

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
            ja, zh, ko = label_in(name, table)
            if ja:
                JA = {"child_of": {"M": "息子", "F": "娘", "": "子"},
                      "parent_of": {"M": "父", "F": "母", "": "親"},
                      "spouse_of": {"M": "夫", "F": "妻", "": "配偶者"},
                      "sibling_of": {"M": "兄弟", "F": "姉妹", "": "きょうだい"}}
                ZH = {"child_of": {"M": "子", "F": "女", "": "子女"},
                      "parent_of": {"M": "父", "F": "母", "": "父母"},
                      "spouse_of": {"M": "夫", "F": "妻", "": "配偶"},
                      "sibling_of": {"M": "兄弟", "F": "姐妹", "": "同胞"}}
                # **Korean too.** Emma, 2026-09-01: *"cjk includes korean"*. Without this the
                # NN/relationship people were the one population still leaving Wikidata with two
                # CJK labels out of three, which is what `queue.md` § *ABSOLUTE PREREQUISITE*
                # exists to stop. Korean takes the genitive 의 and the relationship word after
                # it, the same shape as the Japanese の and the Chinese 之.
                KO = {"child_of": {"M": "아들", "F": "딸", "": "자녀"},
                      "parent_of": {"M": "아버지", "F": "어머니", "": "부모"},
                      "spouse_of": {"M": "남편", "F": "아내", "": "배우자"},
                      "sibling_of": {"M": "형제", "F": "자매", "": "형제자매"}}
                out["ja"] = f"{ja}の{JA[group_name].get(sex) or JA[group_name]['']}"
                out["zh"] = f"{zh}之{ZH[group_name].get(sex) or ZH[group_name]['']}"
                if ko:
                    out["ko"] = f"{ko}의 {KO[group_name].get(sex) or KO[group_name]['']}"
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


def read_suppressed():
    """`{(qid, property, value)}` -- statements ANOTHER editor removed. Never re-emit them.

    **The edit war, 2026-08-30.** `OBender12` merged our duplicate name items and stripped the
    `P734` links pointing at the losers. The next build put them straight back, because the
    generator emits a name statement when the item does not have one — and his deletion is
    exactly what "does not have one" looks like. Emma had to undo her own undos and then make
    cosmetic edits to cover the trail.

    **It is not statefulness, it is the absence of it.** Nothing recorded that a human had
    decided about that statement, so every rebuild saw a fresh gap and filled it. Any *emit
    what is missing* pipeline fights any editor who deletes, indefinitely, and gets more
    confident each round.

    **This is the opposite safe direction from `read_live_values`, and deliberately so.** There
    a missing file costs a redundant statement, which QuickStatements merges away. Here a
    missing file costs an edit war with a stranger, so it warns loudly rather than shrugging.

    Built by `scripts/refresh-suppressed-statements.py`, which reads the contributions of
    editors *other than* the account and keeps their `wbremoveclaims` edits on ledger items.
    **A removal by Emma herself is not in it** — she runs the batches, and her removing
    something the batch re-adds is a conversation with her own pipeline, not an edit war.

    **This sits ALONGSIDE `OBENDER_HOLD_EXPIRES`; neither supersedes the other.** The queue
    asked which, and they answer different questions:

    * the hold is **temporary, per ITEM, and one editor** — it buys time by controlling how
      many further times that particular person sees the account, because *"recognition
      decays but at a slower rate"* than the errors do. It expires on its own, 2026-09-30.
    * this is **permanent, per STATEMENT, and every editor** — it fixes the mechanism that
      caused the war rather than the exposure to one witness.

    If the hold superseded this, the war would simply restart on 2026-10-01 when it lapses.
    If this superseded the hold, the mechanism would be fixed while that editor kept seeing
    the account in their batch through the month she wanted quiet. Both, therefore.
    """
    out = set()
    path = ROOT / "reports" / "suppressed-statements.tsv"
    if not path.exists():
        print("WARNING: reports/suppressed-statements.tsv missing - the batch may re-add "
              "statements another editor deleted. Run "
              "scripts/refresh-suppressed-statements.py")
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="	"):
            out.add((row["qid"], row["property"], row["value"]))
    return out


def read_live_labels():
    """`{(qid, lang): label}` -- what each ledger item's label actually SAYS, live.

    Emma, 2026-08-30: *"Every single label gets redone and if they disagree then they go onto
    the quickstatements that are generated."* A disagreement needs the value, and
    `live_state()` gives only which languages exist, from a store that predates her items.

    Written by `refresh-live-values.py` off the same fetch as the statements. A missing file
    yields an empty map, which makes every label look absent -- so callers must treat "no live
    value" as "do not know", never as "the item has nothing".
    """
    out = {}
    path = ROOT / "reports" / "garborg-live-labels.tsv"
    if not path.exists():
        print("WARNING: reports/garborg-live-labels.tsv missing - label disagreements cannot "
              "be seen. Run scripts/refresh-live-values.py")
        return out
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="	"):
            out[(row["qid"], row["lang"])] = row["label"]
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


#: The four family maps, extracted once during a tree rebuild so this script can run without
#: the 409 MB `out/merged.ged`.
#:
#: **Why it exists: the scheduled pipeline could not run without it.** `--compose` was believed
#: to read only the derived CSVs -- that is what `rebuild-everything.py`'s docstring says and what
#: the CI checkout was scoped for -- and on 2026-09-01 the first pipeline run died in two seconds
#: with `FileNotFoundError: out/merged.ged`. The GEDCOM is gitignored because GitHub refuses a
#: 409 MB file, so no runner can ever have it.
#:
#: **It is the same data, not a reinterpretation.** `reports/derived-family.csv` holds parents and
#: children per PERSON and would need siblings re-derived by indexing the whole file; the two
#: call sites below ask *who shares a family with this person*, which is a question about
#: FAMILIES. So the family grouping is written out verbatim rather than reconstructed, and
#: `read_tree` returns byte-identical maps from either source.
#:
#: 630,050 families, 54 MB, 14 MB gzipped -- `pack-derived.py` carries it.
FAMILY_STRUCTURE = ROOT / "out" / "family-structure.tsv"


#: How many manual `P2600` statements go out per run. Her number, 2026-09-01: *"the pipeline
#: generates 10 quickstatements adding the geni id to the individuals at the beginning of each
#: generation. The 10 quickstatements are 10 of the ones from the csv that are found not to be
#: present in the thing."*
MANUAL_P2600_PER_RUN = 10


def manual_p2600_lines(priority_qids=()):
    """PRIORITY: items this run is about to touch come first and are NOT capped.

    **The ordering defect, found 2026-09-03.** This picked the first ten missing pairs in file
    order and had no idea which items the run was about to label. So `Q138582215` and
    `Q29246906` -- both identified by Emma herself -- received `P735`, `P5056` and `ja`/`zh`/`ko`
    labels from the daily batch while their Geni id waited behind 7,000 others, and
    `Q138582215` had no `P2600` line generated anywhere at all.

    That inverts `CLAUDE.md` § *An item with no relationships is not a missing item*: *"The
    Geni ID needs to be present before any properties derived from Geni can be taken from it."*
    We were publishing Geni-derived names onto items while withholding the statement saying
    where they came from.
    """
    """Up to ten `Q… P2600 "geni"` lines for identifications Wikidata does not yet hold.

    **The candidates come from `reports/manual-identifications.csv`** -- her hand verdicts,
    `SAME` and `RIGHT` both, plus the pairs she gives in conversation.

    **"found not to be present" is checked LIVE**, in one batched request, not against
    `out/wikidata/p2600-all.tsv`. That file was last refreshed 2026-08-30 and she adds `P2600`
    statements by hand continuously; a stale check would keep re-proposing pairs she has already
    made. `CLAUDE.md` § *Emma edits the tree and the items BY HAND* is explicit that a snapshot
    goes stale in minutes.

    **No reference.** Emma, 2026-08-31: *"geni ids do not get sources you retard"* -- an `S2600`
    citing the very id being added is circular.

    Returns `(lines, checked, already_held)`.
    """
    path = ROOT / "reports" / "manual-identifications.csv"
    if not path.exists():
        return [], 0, 0
    want = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            q, g = (row.get("qid") or "").strip(), (row.get("geni_id") or "").strip()
            if q.startswith("Q") and g.isdigit() and q not in NEVER_TOUCH_QID                     and g not in NEVER_TOUCH_GENI:
                want.append((q, g, (row.get("name") or "").strip()))
    if not want:
        return [], 0, 0
    held = set()
    import json as _json
    import urllib.parse as _up
    import urllib.request as _ur
    ids = [q for q, _, _ in want]
    for i in range(0, len(ids), 50):
        try:
            qs = _up.urlencode({"action": "wbgetentities", "ids": "|".join(ids[i:i + 50]),
                                "format": "json", "props": "claims"})
            rq = _ur.Request("https://www.wikidata.org/w/api.php?" + qs,
                             headers={"User-Agent": "genimerge manual P2600 "
                                                    "(emma@topazcomputing.com)"})
            data = _json.loads(_ur.urlopen(rq, timeout=90).read().decode("utf-8"))
        except Exception as exc:                                    # noqa: BLE001
            # **Fail CLOSED here, unlike the pipeline gate.** Unknown means "might already be
            # there", and re-adding a statement Wikidata holds is noise on her watchlist.
            print(f"WARNING: manual P2600 check could not reach Wikidata ({exc}); "
                  f"emitting none this run")
            return [], 0, 0
        for qid, ent in (data.get("entities") or {}).items():
            for st in (ent.get("claims") or {}).get("P2600", []):
                v = st.get("mainsnak", {}).get("datavalue", {}).get("value")
                if isinstance(v, str):
                    held.add((qid, v))
    missing = [(q, g, n) for q, g, n in want if (q, g) not in held]
    # Anything this run touches leads, and is exempt from the cap: the cap is a pacing rule for
    # speculative identifications, never a reason to label an item whose id we are withholding.
    pri = set(priority_qids or ())
    lead = [t for t in missing if t[0] in pri]
    rest = [t for t in missing if t[0] not in pri]
    lines = []
    for q, g, n in lead + rest[:MANUAL_P2600_PER_RUN]:
        if n:
            lines.append(f"#   {q} {n}: P2600 from her own identification")
        lines.append(f'{q}\tP2600\t"{g}"')
    return lines, len(want), len(want) - len(missing)


def read_tree():
    fam_p = collections.defaultdict(list)
    fam_c = collections.defaultdict(list)
    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    merged = ROOT / "out" / "merged.ged"
    if not merged.exists() and FAMILY_STRUCTURE.exists():
        # **All four maps are stored, not two of them inverted.** Deriving `fams`/`famc` by
        # inverting `fam_p`/`fam_c` looked equivalent and is not: those come from the PERSON's
        # `FAMS`/`FAMC` pointers while the others come from the FAMILY's `HUSB`/`WIFE`/`CHIL`,
        # and the two disagree wherever one side of the pair is missing -- 842,548 against
        # 833,632, and 1,182,519 against 1,177,873. Measured before shipping, not after.
        into = {"fam_p": fam_p, "fam_c": fam_c, "fams": fams, "famc": famc}
        with open(FAMILY_STRUCTURE, encoding="utf-8") as f:
            next(f, None)
            for line in f:
                name, _, rest = line.rstrip(chr(10)).partition(chr(9))
                key, _, values = rest.partition(chr(9))
                target = into.get(name)
                if target is not None and key:
                    target[key].extend(values.split())
        return fam_p, fam_c, fams, famc
    cur = kind = None
    with open(merged, encoding="utf-8", errors="replace") as f:
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
        # **The label we want is the EXPANDED one.** Emma, 2026-08-27: *"any abbreviations like
        # -dtr … should be fixd since wikidata mul labels are supposed to have the full form.
        # This is a part of the compliance stuff"*. `expand_abbreviations` ran only on the
        # creation path, so an item created before the census covered its form keeps the
        # abbreviation forever and nothing here ever noticed.
        want = qs(expand_abbreviations(labels.get(geni_id, ""), geni_id))
        have = live.get(qid, "")
        if not want or not have or have == want:
            continue
        # **An abbreviation expansion is its own ground for a correction**, alongside the
        # birth-name case below. It cannot rewrite anything else: the test is that the live
        # label expands to exactly what we want, so the only difference between the two IS the
        # abbreviation. Emma fixed `Q141271379` by hand on 2026-09-04 — *"I changed her name to
        # correct the issue of an abbreviation of Ormsdatter"* — and an item she has already
        # fixed simply matches `want` and is skipped by the line above.
        if expand_abbreviations(have, geni_id) == want:
            out.append(f"#   {qid}: holds the abbreviated {have!r}; the full form is {want!r}")
            out.append(f"#   {qid}: keep the outgoing label as an alias before it is replaced")
            out.append(f'{qid}\tAmul\t"{have}"')
            out.append(f"#   {qid}: set the mul label to {want!r}")
            out.append(f'{qid}\tLmul\t"{want}"')
            out.append(f"#   {qid}: set the en label to {want!r}")
            out.append(f'{qid}\tLen\t"{want}"')
            ja, zh, ko = label_in(want, table)
            if ja:
                for code, value in (("ja", ja), ("zh", zh), ("ko", ko)):
                    out.append(f"#   {qid}: set the {code} label")
                    out.append(f'{qid}\tL{code}\t"{value}"')
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
        ja, zh, ko = label_in(want, table)
        if ja:
            out.append(f"#   {qid}: set the ja label")
            out.append(f'{qid}	Lja	"{ja}"')
            out.append(f"#   {qid}: set the zh label")
            out.append(f'{qid}	Lzh	"{zh}"')
            out.append(f"#   {qid}: set the ko label")
            out.append(f'{qid}	Lko	"{ko}"')
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


#: **The order label edits go out in, by LANGUAGE. Emma, 2026-09-04:**
#:
#:     En / Mul / Ja / Zh / Ko
#:     Then any ordering of our actively supported languages
#:     Then any other language labels that might be changed for some reason
#:
#: She gave it when told that the 15-a-batch cap was being spent before `mul` was reached, so it
#: is both an ordering and a priority: the tiers are taken in turn until the budget runs out, so
#: an `en` edit displaces a `hi` one rather than merely printing above it.
#:
#: **The five are the creation gate.** § *The label gate* makes `ja` + `zh` + `ko` the condition
#: for creating anybody, and § *The MARRIED name is the real name* shows the shape of an item as
#: `en`, `mul`, `Amul`, `ja` — so these are the labels the programme is actually about, and the
#: four scripts below are the ones it adds afterwards.
#:
#: **The actively supported set is `hi`, `ar`, `ru`, `el`** — `build-four-script-labels.CODES`,
#: 151,320 labels, § *HER RULINGS, 2026-09-01* — read from that module rather than restated, so
#: adding a language there moves it up this list for free.
LABEL_LANGUAGE_ORDER = ("en", "mul", "ja", "zh", "ko")


def _supported_languages():
    """`hi`/`ar`/`ru`/`el`, read from the script that emits them rather than copied."""
    try:
        import importlib.util
        path = ROOT / "scripts" / "build-four-script-labels.py"
        spec = importlib.util.spec_from_file_location("four_script_labels", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return tuple(module.CODES)
    except Exception:                                               # noqa: BLE001
        # Never let the ordering break the batch: an unreadable list means those languages
        # rank with "any other", which is one tier lower and nothing worse.
        return ()


def _label_tiers():
    """The slot-name sets to take in turn, in her order.

    A slot is `Lmul`, `Amul`, `Lja`… so the language is everything after the first character.
    Both the label and the alias for one language sit in the same tier and keep the order they
    were emitted in — which is what protects the `Amul` that preserves an outgoing `mul` label
    from being separated from the `Lmul` that replaces it.
    """
    named = list(LABEL_LANGUAGE_ORDER)
    supported = [c for c in _supported_languages() if c not in named]
    return [{"L" + lang, "A" + lang, "D" + lang} for lang in named] + [
        {"L" + lang for lang in supported} | {"A" + lang for lang in supported}
        | {"D" + lang for lang in supported}]


def _cap_label_edits(lines, clan_block, corrections):
    """Move label edits on existing items to the FRONT, capped at `LABEL_EDIT_CAP` QIDS.

    **⛔ The cap counts PEOPLE, not lines, and everything for one person goes at once.** Emma,
    2026-09-04: *"we do all at once per qid (15 qids) in descending order of qids"*. It counted
    lines until then, which split a person across runs — an item could get its `mul` today and
    its `ja` in a fortnight, and be wrong in the meantime in a way that reads as carelessness
    rather than as a queue.

    **Descending QID: the newest items first, and she pre-empted the objection.** *"I am 100%
    aware that descending qids can cause an issue of a backlog theoretically never going away
    … I do not consider this to actually be a major concern"*, for two reasons she gave: *"making
    an item very recently that has an error in it looks worse than an item that I made a long
    time ago having an error in it"*, and the real answer is upstream — *"my expectation is that
    we're going to ideally be never, ever, ever creating items with errors in them like this"*.
    So the starvation is **intentional**, *"an intentional effect based off of live prioritization
    of different things"*. Do not add a fairness pass, an age bonus or an oldest-first sweep: that
    is the *"safety thing you made up"* she named in the same breath.

    **Within a person, her language order**, `LABEL_LANGUAGE_ORDER` then the supported set then
    the rest — *"En / Mul / Ja / Zh / Ko / Then any ordering of our actively supported languages /
    Then any other language labels that might be changed for some reason"*. With all of a QID's
    edits going out together this is a LAYOUT within the person, not a priority between people;
    it was read as a priority when the cap still counted lines, and this supersedes that.

    **The cap itself is hers and unchanged.** 2026-08-28: *"We are way too gung ho about adding
    cjk labels to existing items… any label changes should occur at the beginning of the batch
    and be limited to a count of 15 labels added per batch."* A label at CREATION time is neither
    counted nor capped — *"a label added during item creation is good"* — so this only ever sees
    `Q… L…`/`Q… A…`, never `LAST L…`.

    **Corrections before the clan block, within a person.** *"Fixing something wrong outranks
    adding something missing."*

    **What has already gone out, so the cap DRAINS instead of repeating**, keyed on
    `(qid, slot, value)` — see the note at `done` below.
    """
    # See the module note: keyed on the VALUE too, so a rule fixed after an item was labelled
    # can still reach it. It was `(qid, slot)` until 2026-09-04 and that froze 220 of the 1,860
    # emitted CJK labels against every later correction.
    done_path = ROOT / "reports" / "label-edits-emitted.tsv"
    done = set()
    if done_path.exists():
        for row in csv.DictReader(done_path.open(encoding="utf-8"), delimiter="	"):
            done.add((row["qid"], row["slot"], row.get("value", "")))

    def is_label_edit(ln):
        return bool(re.match(r"^Q[1-9][0-9]*	[LAD][a-z-]+	", ln))

    def split(source, rank):
        """`(kept, edits)` — the non-label lines in order, and each edit with its comments.

        A `#` comment or blank line belongs to the edit below it, which is how the batch is
        written; carrying them together is what keeps a regrouped file readable. `rank` orders
        the sources within one person.
        """
        kept, edits, pending = [], [], []
        for ln in source:
            if not ln.strip() or ln.lstrip().startswith("#"):
                pending.append(ln)
                continue
            if is_label_edit(ln):
                qid, slot = ln.split("	")[0], ln.split("	")[1]
                value = ln.split("	")[2].strip('"')
                edits.append({"qid": qid, "slot": slot, "value": value,
                              "lines": pending + [ln], "rank": rank,
                              "order": len(edits)})
                pending = []
                continue
            kept.extend(pending)
            kept.append(ln)
            pending = []
        kept.extend(pending)
        return kept, edits

    clan_lines = clan_block.splitlines()
    _, correction_edits = split(corrections, 0)
    _, clan_edits = split(clan_lines, 1)
    lines, line_edits = split(lines, 2)
    every = [e for e in correction_edits + clan_edits + line_edits
             if (e["qid"], e["slot"], e["value"]) not in done]

    #: Language rank inside a person. Anything she did not name sorts last, stably.
    tiers = _label_tiers()
    def language_rank(slot):
        for i, tier in enumerate(tiers):
            if slot in tier:
                return i
        return len(tiers)

    by_qid = collections.defaultdict(list)
    for edit in every:
        by_qid[edit["qid"]].append(edit)

    # Descending QID — numerically, because `Q9` is newer than `Q10000` as a string and older
    # as an item.
    chosen = sorted(by_qid, key=lambda q: -int(q[1:]))[:LABEL_EDIT_CAP]
    held = sum(len(v) for q, v in by_qid.items() if q not in chosen)

    head, newly = [], []
    for qid in chosen:
        for edit in sorted(by_qid[qid],
                           key=lambda e: (language_rank(e["slot"]), e["rank"], e["order"])):
            head.extend(edit["lines"])
            newly.append((edit["qid"], edit["slot"], edit["value"]))

    if head:
        head = ["# " + "-" * 72,
                "# LABEL EDITS ON EXISTING ITEMS -- at the head of the batch and capped at "
                f"{LABEL_EDIT_CAP} PEOPLE,",
                "#   both her instruction: \"any label changes should occur at the beginning of",
                "#   the batch and be limited to a count of 15 labels added per batch\", and",
                "#   \"we do all at once per qid (15 qids) in descending order of qids\". A label",
                "#   set at CREATION time is neither counted nor capped -- \"a label added during",
                "#   item creation is good\".",
                "#   Newest items first, deliberately: a recent item with an error in it looks",
                "#   worse than an old one. Within a person: en, mul, ja, zh, ko, the supported",
                "#   languages, then the rest.",
                f"#   {len(chosen)} people, {len(newly)} edits; {held} edits held for a later run",
                "#   across " + str(len(by_qid) - len(chosen)) + " more people. A repeat is a "
                "no-op, so nothing is lost.",
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
    print(f"label edits on existing items: {len(newly)} edits over {len(chosen)} people "
          f"(cap {LABEL_EDIT_CAP} people); {held} edits held across "
          f"{len(by_qid) - len(chosen)} more people; "
          f"{len(done):,} already done in earlier batches")
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


#: **`without_nickname` now lives in `scripts/namemodel.py`**, the module that models a name,
#: because applying it only at emission left `reports/derived-labels.csv` holding the bracketed
#: form for all 48 readers of `label_en`/`label_mul`. `derive-labels.py` applies it at source.
#: Re-exported here so this file's own callers are unchanged.
from namemodel import without_nickname  # noqa: E402,F401


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


#: Words that introduce a place a person was *of*, rather than a further name token.
#:
#: **`van`, `von`, `af` and `av` are deliberately NOT here, and the first draft had them.** They
#: form surnames rather than designations -- `Reinoud I van Brederode` truncated to `Reinoud`,
#: losing the family name, and `CLAUDE.md` § *A parenthesised token* records Emma's ruling that
#: particles are *"integral parts of what the people are called"* and belong in the label.
#: `Hård af Segerstad` is a family in this corpus, not a man of Segerstad.
#:
#: What is left is the Scandinavian locative, which is never a surname: `till Krageholm`,
#: `til Gundestrup`, `i Gjesdal`, `på Berg`. That is 10,898 of the 11,873 affected people;
#: giving up the `av`/`af` 727 is the price of not destroying a surname.
TERRITORIAL = {"till", "til", "i", "på", "paa"}


def _drop_territorial(label):
    """Everything from the first territorial word onward, removed. See `label_in`.

    Only when something FOLLOWS it: a trailing `i` with nothing after it is a name token that
    happens to look like the preposition, and truncating there would delete a real name. And
    never when it is the first token, which would empty the label entirely.
    """
    tokens = (label or "").split()
    for n, token in enumerate(tokens):
        if not n or n + 1 >= len(tokens):
            continue
        bare = token.strip(",")
        # **`i` is the preposition ONLY in lower case.** A capital `I` is a regnal ordinal or
        # an initial -- `Reinoud I van Brederode` truncated to `Reinoud` while this folded
        # case, losing the whole name. `CLAUDE.md` § *A middle initial keeps its Latin letter*
        # records the mirror image of the same trap: `Ragnhild … i Gjesdal` read the Norwegian
        # `i` as an initial because `.upper()` was applied. Case separates them and is never
        # changed in either direction.
        if bare == "i" or (bare != "I" and bare.casefold() in TERRITORIAL):
            return " ".join(tokens[:n])
    return label


#: A label written in Latin script -- letters, marks, spaces and the punctuation names carry.
_LATIN_LABEL = re.compile(r"^[A-Za-zÀ-ÿĀ-ſĲ-ŉŊ-ž'’.,()\-\s]+$")


#: Words that open a Wikidata label and are a TITLE rather than a name. Used for one narrow
#: question only -- see `_only_adds_a_title`.
_LEADING_TITLE = re.compile(
    r"^(?:Baron|Baroness|Count|Countess|Duke|Duchess|Lord|Lady|Sir|Dame|King|Queen|Prince|"
    r"Princess|Earl|Friherre|Friherrinna|Greve|Grevinna|Graf|Gr\u00e4fin|Freiherr|Freifrau|"
    r"Hertig|Kung|Drottning)\s+", re.I)


def _only_adds_a_title(current, proposed):
    """True when `proposed` is `current` with nothing but title words stuck on the front.

    **A label that already reads correctly is not improved by a title.** Found 2026-09-04, when
    `mul` was given first claim on the label cap and the pending values were read: `Q136376245`
    holds `Fredrik Elof Gyllenkrok` and the consensus proposed `Baron Fredrik Elof Gyllenkrok`.
    That is a live label being made worse, at 15 a batch.

    **It does NOT stop a titled label being ADDED**, which is the other 7 of the 8 titled values
    pending: those items have no `mul` at all, and a label with a title on it is a label. Emma's
    § *A TITLE IS NOT A NAME* is about what becomes a `P735`/`P734` and says in terms that it
    *"does not touch the LABEL"* — so this stays as narrow as it can be and only refuses the
    replacement.

    Title-word matching is used rather than a general prefix test on purpose: `Anne` becoming
    `Carl Anne` is somebody's given name being added and is not this.
    """
    if not current or not proposed or current == proposed:
        return False
    rest = proposed
    while True:
        stripped = _LEADING_TITLE.sub("", rest, count=1)
        if stripped == rest:
            break
        rest = stripped
    return rest != proposed and rest.strip() == current.strip()


def consensus_latin_label(labels):
    """The Latin name an item is called by, by a VOTE across its own languages. `''` when none.

    **⛔ Emma's specification, 2026-09-04, correcting what was here:** *"in the event that just
    the English exists as a Latin alphabet thing, the English name turns into the multi language
    label. And if two or more Latin alphabet labels exist, then the Latin alphabet labels vote on
    whichever one is going to be the multi language label. I guess in this sense you can say that
    it even is the case if there's only English, because it's just, like, English ties or English
    is a tiebreaker. So in that case there would just be a single Latin language one, and English
    is just a single vote for that."*

    So it is one rule and not two, and English has **no special standing except as a tiebreaker**:

    * every Latin-script label is a vote for its own string;
    * the string with the most votes wins;
    * a tie is broken by the English label, if English is one of the tied;
    * **one vote is enough** — a lone Latin label is a majority of one.

    **Two things here were wrong and both changed the answer.** The old version returned the
    `en` label immediately whenever it was Latin, so English did not vote, it decided — twelve
    languages agreeing on `Fredrik Elof Gyllenkrok` would have lost to one `en` reading
    `Baron Fredrik Elof Gyllenkrok`. And it required `n >= 2`, so an item whose only Latin label
    was English got **no `mul` at all**, which is a large part of what she reported as *"many
    people are just never given mul labels"*.

    **`mul` itself does not vote**, and that is deliberate rather than an oversight in her
    wording: `mul` is the output. Letting it vote for itself makes the rule self-reinforcing —
    a wrong `mul` would defend its own position against a single correcting label — and no
    correction could ever reach an item, which is the same shape as the emitted-labels set that
    froze 220 CJK labels until 2026-09-04.

    **A tie with English not among the tied is broken by sorting**, so the answer is a function
    of the labels and not of dict order — `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*.

    `Q6161733` remains the worked case for why this reads the item's own labels rather than our
    Geni string: `en` and `sv` both say `Carl Fredrik Piper`, so that is the `mul` and what
    `ja`/`zh` are built from, while our `Carl Fredrik Piper till Krageholm` goes to `P1810`
    *subject named as* and to an `Amul` alias.
    """
    votes = collections.Counter(
        value.strip() for lang, value in labels.items()
        if lang != "mul" and value and _LATIN_LABEL.match(value.strip()))
    if not votes:
        return ""
    best = max(votes.values())
    tied = sorted(v for v, n in votes.items() if n == best)
    if len(tied) == 1:
        return tied[0]
    english = (labels.get("en") or "").strip()
    return english if english in tied else tied[0]


def _label_collisions():
    """Geni ids whose creation would duplicate an existing label+empty-description pair.

    From `reports/label-collisions.tsv`, written by `scripts/check-label-collisions.py`. A
    missing file yields an empty set and today's behaviour, which is the safe direction: the
    batch is no worse than it was, and the check is a pre-flight rather than a dependency.
    """
    path = ROOT / "reports" / "label-collisions.tsv"
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        return {row["geni_id"] for row in csv.DictReader(f, delimiter="	") if row["geni_id"]}


def _has_given_name(fields):
    """Does this person have a GIVEN name, once a stillborn description is removed?

    **Emma, 2026-08-30, on `Q141224141`:** *"please stop trying to assign names to this person
    who does not in fact have any names at all."* Geni records him `En dodfodd son Bielke` --
    Swedish for *a stillborn son* -- and the batch emitted `P735` given name `En`, the
    indefinite article, carrying `P7452` *usual forename*.

    **Testing the whole label is not enough and that was the first fix.** Stripped, he reads
    `NN Bielke`, so "does this person have a name" answers yes -- on the strength of a surname.
    The defect is on the given-name side, so that is what has to be asked. `Bielke` still
    reaches `P734` through the ordinary path.

    505 people in the corpus carry a stillborn word.
    """
    from labels import _STILLBORN_PHRASE, NARROW_MARKERS, WORDS_MEANING_UNKNOWN
    givn = _STILLBORN_PHRASE.sub(" ", (fields or {}).get("givn", "") or "")
    markers = NARROW_MARKERS | WORDS_MEANING_UNKNOWN
    return any(t for t in givn.split() if t.casefold().strip(".,") not in markers)


#: Tokens this run rendered on the fly, flushed to the shared table at the end. See the funnel
#: note in `label_in`.
MINTED_TOKENS = {}


def _render_token(token):
    """`(ja, zh, ko)` for a token nothing has read yet, or `(None, None, None)`.

    Her standard is what makes an on-the-fly rendering acceptable: *"Incorrect romanization or
    incorrect representations in katakana are totally acceptable. An incorrect name is not,
    because half these words, nobody knows how they're pronounced anyway."* A rendering that a
    native reader would spell differently is fine; dropping the label entirely is what the funnel
    exists to stop.

    `translit_no` is the engine, the same one `extend-transliterations.py` uses, so a token
    rendered here and a token rendered by the batch step come out identical.
    """
    if not token or not any(c.isalpha() for c in token):
        return None, None, None
    try:
        from translit_no import translit
        from translit_ko import render as ko_han
        from translit_ko_latin import render as ko_latin
        ja, zh = translit(token)
        # Han first: a token already written in Han characters has a Sino-Korean reading, and
        # routing it through the Latin renderer would be nonsense. `translit_ko.render` returns
        # `''` for anything that is not Han, so the fallback is exact rather than a guess.
        ko = ko_han(token) or ko_latin(token)
    except Exception:                                               # noqa: BLE001
        return None, None, None
    return (ja, zh, ko) if ja and zh and ko else (None, None, None)


def label_in(label, table):
    """(ja, zh, ko) for a whole name, or (None, None, None) if any token is unknown.

    **Korean is the third CJK language and was missing until 2026-09-01.** Emma: *"cjk includes
    korean"*. All three are required together: a person with two of them is not a person whose
    CJK labels are done.

    Partial is worse than absent: half a name in katakana and half in Latin is not a
    Japanese label, it is a broken one. **A middle initial is the one exception** —
    `labels.transliterate_token` keeps `F` as `F` in every script, per Emma 2026-08-27.
    """
    from labels import (ORDINAL_RE, FINAL_ORDINALS, transliterate_token,
                        transliterate_token_ko)

    # **A DESCRIPTION is not a name and never goes through here.** This is the choke point
    # rather than the callers, because every CJK label in the batch comes out of this one
    # function -- guarding it once covers the additions pass, the label corrections and the
    # creations alike, and a caller added next month is covered without knowing about this.
    # `describe_all` builds the right CJK form for these people (`…の息子`), so refusing here
    # loses nothing and stops `son of X` becoming `ソン・オフ・X`.
    if is_relationship_description(label):
        return None, None, None

    # **A territorial designation is not part of the name, and transliterating it is how
    # `Q6161733` got `カール・フレドリク・パイパー・ティル・クラゲホルム`.** Emma spotted it and
    # corrected the item to `カール・フレドリク・パイパー`: *"why was the japanese label we added
    # so weird?"*
    #
    # `till Krageholm` is Swedish for *of Krageholm*, an estate he held. Read token by token it
    # becomes two more name syllables, so the label reads as a five-part personal name. The
    # same shape is `til Gundestrup`, `i Gjesdal`, `av Norge`, `på Berg` -- and `CLAUDE.md`
    # already records the Norwegian `i` biting once before, on
    # `Ragnhild Toresdatter Håland i Gjesdal`.
    #
    # **11,873 people in `derived-labels.csv` carry one**: `i` 5,428, `til` 3,592, `till`
    # 1,878, `av` 695, `på` 248, `paa` 32. Every one of them would get the estate rendered as
    # part of their name.
    #
    # The Latin label keeps it -- that is how Geni renders the person and it is real
    # information -- and only the CJK label truncates, which is exactly the edit Emma made.
    label = _drop_territorial(label)

    # **Punctuation stuck to a token is not part of the name.** `Christina, Sofia Carlsdotter`
    # tokenised to `Christina,` with the comma attached, which is in no table and therefore
    # killed the whole label -- one stray comma costing a person both their `ja` and `zh`.
    # Stripped for the LOOKUP only; the label itself is untouched, so a name that genuinely
    # carries punctuation still reads as it does.
    ja, zh, ko = [], [], []
    # **An ordinal ATTACHES; every other token takes the separator.** Emma's hand-fix of
    # `Q141223436` on 2026-09-04 reads `トーレ・ウンデルベルゲ3世` and `托雷·温德尔贝尔盖三世` -- the
    # `・` and the `·` stop before the ordinal. `ko` is unaffected because it separates every
    # word with a space anyway, and hers reads `토레 운데르베르게 3세`.
    attached = []
    tokens = list(classify(label))
    for position, (token, _usage, _o) in enumerate(tokens):
        clean = token.strip(",;:")
        # A single `I`/`V` is an ordinal only in the FINAL position; anywhere else it is a
        # middle initial and keeps its letter. `labels.FINAL_ORDINALS` carries the census.
        final = position == len(tokens) - 1 and len(tokens) > 1
        attached.append(bool(ORDINAL_RE.match(clean))
                        or (final and clean in FINAL_ORDINALS))
        a, b = transliterate_token(clean, table, final=final)
        c = transliterate_token_ko(clean, table, final=final)
        if a is None or c is None:
            # **THE FUNNEL, at the call rather than only in the pipeline.** Emma, 2026-08-29:
            # *"If anything even remotely wants to generate without having katakana or Chinese
            # characters, it goes through this thing and then adds the token to the library, and
            # then continues on."*
            #
            # It was wired as STEP 0d of `build-daily-batch.py`, which fills the table before
            # anything composes -- and that covers the pipeline and **not the builder**. Running
            # `build-garborg-day.py --compose` directly, which happens constantly, skipped it
            # entirely, so the guarantee held only when somebody used the wrapper. That is the
            # same *"the pieces existed and nothing called them"* shape the funnel was written
            # against, one layer up.
            #
            # A rendered token is cached in `table` for the rest of the run and collected in
            # `MINTED_TOKENS`, which `main` appends to the shared file at the end. Writing
            # per-token would interleave writes into a file other scripts read.
            a, b, c = _render_token(clean)
            if a is None or c is None:
                return None, None, None
            table[clean] = (a, b, c)
            MINTED_TOKENS[clean] = (a, b, c)
        ja.append(a)
        zh.append(b)
        ko.append(c)
    # **Korean separates the words of a personal name with a SPACE**, where `ja` takes the
    # middle dot and `zh` its own. Joining on nothing gave 안나츠리스티나프리가레 for
    # `Anna Christina Flygare` -- one unreadable run of fourteen syllables.
    def joined(parts, sep):
        out = ""
        for i, part in enumerate(parts):
            out += part if (i == 0 or attached[i]) else sep + part
        return out

    return joined(ja, "・"), joined(zh, "·"), " ".join(ko)


def name_lines(label, plan, geni_id, father_qid, fields=None, sex="",
               father_name=""):
    """`P735`/`P734`/`P5056` lines for one person, and what could not be emitted.

    **Only tokens whose item already exists.** A name item this run is creating
    cannot be pointed at, same single-run rule as everybody else, so the rest waits
    for `reports/wikidata-garborg-name-items.txt` to have been run.

    QuickStatements takes qualifiers exactly like references, property then value on
    the same line: `LAST<TAB>P735<TAB>Q629347<TAB>P1545<TAB>"1"<TAB>P7452<TAB>Q3409033`.
    """
    out, notes = [], []
    lines, why = statements_for(label, plan, geni_id, father_qid=father_qid,
                                fields=fields, sex=sex, father_name=father_name)
    for prop, value, quals in lines:
        # `P1449` *nickname* never arrives: `namemodel.statements_for` stops modelling it,
        # per Emma's 2026-08-29 ruling. The drop used to be here, and having it in the emitter
        # while the model still produced it is what gave `model-vs-reality.py` 66 phantom
        # "missing nickname" rows.
        parts = [f"LAST	{prop}	{value}"]
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
#: **The Kitajima/Kitashima hold — MONTH-LONG, not permanent.** Emma, 2026-09-01:
#: *"we're doing a month long exclusion on the other ones too"*. Same shape as
#: `OBENDER_HOLD_EXPIRES` and for the same reason recorded there: a hold that has to be
#: remembered to be lifted is a hold that stays forever.
#:
#: **Emma herself is NOT in these sets any more**, her instruction of the same day: *"Yeah remove
#: it"*. She was excluded on 2026-08-27, removed by `9968793c`, and I put her back in `ad14619a`
#: on 2026-08-31 because `build-missing-reciprocals.py` emitted two live edits to `Q232803`
#: and a test went red — I reached for the nearest existing mechanism instead of asking which of
#: her two instructions won, and then described it in the queue as *"they were not removed"*,
#: which hid that I had re-added her. Her anonymisation instruction is the one that governs:
#: **remove code that treats her item as special.**
KITAJIMA_HOLD_EXPIRES = datetime.date(2026, 10, 1)

KITAJIMA_GENI = {
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

KITAJIMA_QID = {
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

#: Ids no batch may name, in any position. Empty once the Kitajima hold expires — which is the
#: point: nothing here is permanent any more.
NEVER_TOUCH_GENI = set(KITAJIMA_GENI) if datetime.date.today() < KITAJIMA_HOLD_EXPIRES else set()
NEVER_TOUCH_QID = set(KITAJIMA_QID) if datetime.date.today() < KITAJIMA_HOLD_EXPIRES else set()


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


from qscomment import annotate  # noqa: E402


#: The two roots of the Wikidata subgraph the ring grows from. These are NOT spine
#: machinery -- they survived the 2026-09-02 spine removal because `subgraph_roots()`
#: needs them: `CLAUDE.md` § *The seed set is the WIKIDATA SUBGRAPH from Arne*.
ARNE_QID = "Q11959067"      # Arne Olaus Fjortoft Garborg
#: **Johannes Bureus -- the second root.** Emma, 2026-08-28: *"it is supposed to do this
#: from Johannes Bureus and Arne Garborg, subgraphs coming from both of them."*
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

    **ARNE IS THE ONE EXCEPTION, and that is the design.** Checked 2026-09-03: of the 252 roots
    before the drip-in, **251 are Bure** -- Johannes Bureus is himself in `bureatten.csv` -- and
    Arne is the only one who is not. Emma: *"Almost all of them are Bure people… Arne Garborg is
    the one exception."*

    **Why the two sides differ, in her words:** *"the family of Arne were precreated by me and are
    generally pretty well connected to each other. Whereas this other family is in the interesting
    situation where… a massive amount of them had Wikidata items because of having Swedish
    Wikipedia articles, but nobody actually did genealogical work on Wikidata. So them as entry
    points means they have a high level of activity in connecting to each other, whereas the
    [Arne] people have been in large part added exclusively by me, and there's about the same
    amount of them, probably a bit less surface area. And the [Arne] people primarily connect to
    other groups."*

    So the imbalance is not lopsidedness to correct: an item that exists and states no
    relationships is the highest-yield entry point there is, which is exactly what a sv.wikipedia
    article with no genealogical work leaves behind. The roster stays at **about 250** -- her
    instruction, same day -- so `reports/entry-points.tsv` is a trickle, not a second campaign.
    """
    roots = [ARNE_QID, BUREUS_QID]
    roster = ROOT / "reports" / "bureatten.csv"
    if roster.exists():
        with open(roster, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if (row.get("geni_ids") or "").strip() and row.get("qid"):
                    roots.append(row["qid"])
    roots.extend(q for q, _ in active_entry_points())
    roots.extend(active_group_qids())
    return tuple(dict.fromkeys(roots))


#: Where the dripped-in entry points live. One row per person, with the date they switch on.
ENTRY_POINTS = ROOT / "reports" / "entry-points.tsv"


def entry_points():
    """Every row of `reports/entry-points.tsv`, as `(qid, geni_id, label, active_from, note)`.

    **Emma, 2026-09-03, asking for this on a clock:** *"for entry points into the graph: I
    actually want this as a timer: on October 1 George RR Martin is added as an entry point, and
    Robert Ettinger is added as an entry point right now! I think there probably are other people
    worthy of dripping in as entry points. But I'm not sure who."*

    **The timer is a DATE COLUMN, not a scheduler**, and that is deliberate. A cron here is
    session-local and dies with the session --- `CLAUDE.md` § *A cron only fires while the session
    is idle* is the record of one starving for four hours, and every cron died in the 2026-08-28
    crash. An `active_from` date cannot be lost, needs nothing running on the day, and makes the
    switch-on a property of the repo rather than of whoever happened to be at a terminal. Adding
    the next person she thinks of is one line in a TSV.

    **The two she named, resolved from our own tree rather than guessed** --- `CLAUDE.md` § *Do
    not guess these* --- by joining `reports/derived-labels.csv` on the label and reading the qid
    column, since neither Wikidata nor Geni is reachable from a remote session:

    * `Q714044` **Robert Chester Wilson Ettinger**, Geni `6000000003022010249`, live now.
    * `Q181677` **George R.R. Martin**, Geni `6000000081001962237`, live 2026-10-01.

    **Both are textbook service areas by her own specification.** Neither states a single `P22`,
    `P25`, `P40` or `P26` on Wikidata, so each reaches exactly itself there --- and § *THE EDIT
    ALGORITHM* wants precisely that: *"something that has a GeniID but is otherwise isolated."*
    In our Geni tree both are richly attached (Ettinger: parents, 2 spouses, 2 children; Martin:
    parents, 2 spouses) and both sit in the main 1,446,089-person component, so the ring has
    somewhere to go from the first day each switches on.
    """
    if not ENTRY_POINTS.exists():
        return []
    rows = []
    with open(ENTRY_POINTS, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r.get("geni_id")]

    # **A row may name a person we hold no QID for, and that is not a reason to refuse it.**
    # The Chinese legendary lineage rows are exactly that: they are the far edge of our tree and
    # our data records no Wikidata correspondence for them. Whether Wikidata *has* items for
    # 少昊 or 顓頊 is a different question our store cannot answer --- `CLAUDE.md` § *"Is X
    # present?"* --- so a blank qid means "we do not hold the link", never "no item exists".
    #
    # Resolve blanks from `derived-labels.csv` at load, so an entry point switches on by itself
    # the moment the correspondence lands, with no edit here. The file is 1.45M rows, so it is
    # read only when a blank actually needs it: this function runs at import.
    if any(not (r.get("qid") or "").strip() for r in rows):
        want = {r["geni_id"] for r in rows if not (r.get("qid") or "").strip()}
        for gid, qid in _qids_for(want).items():
            for r in rows:
                if r["geni_id"] == gid and not (r.get("qid") or "").strip():
                    r["qid"] = qid

    # Sorted on the geni id, which is unique and present on every row ---
    # `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* wants a total key, and a blank qid is not one.
    return sorted(rows, key=lambda r: r["geni_id"])


def _qids_for(geni_ids):
    """Geni id -> QID out of `derived-labels.csv`, for the handful that need it."""
    import gzip

    plain = ROOT / "reports" / "derived-labels.csv"
    packed = ROOT / "reports" / "derived-labels.csv.gz"
    if plain.exists():
        handle = open(plain, encoding="utf-8")
    elif packed.exists():
        handle = gzip.open(packed, "rt", encoding="utf-8")
    else:
        return {}
    found = {}
    with handle as fh:
        for row in csv.DictReader(fh):
            if row["geni_id"] in geni_ids and row.get("qid"):
                found[row["geni_id"]] = row["qid"]
                if len(found) == len(geni_ids):
                    break
    return found


#: Whole populations that become entry points on a date, named by the roster file that lists
#: them rather than pasted in person by person.
ENTRY_POINT_GROUPS = ROOT / "reports" / "entry-point-groups.tsv"


def entry_point_groups():
    """Every row of `reports/entry-point-groups.tsv`, sorted by group name.

    **Emma, 2026-09-03, naming whole blocs at once:** *"Ancient Chinese bloc / All Samaritan high
    priests / All Ethiopian Emperors / All Japanese Emperors / All Tanba people / All
    Izumo/Senge/Kitajima people / All people with special geni gedcom recognition become entry
    people."*

    **A group is a REFERENCE TO A ROSTER, not hundreds of pasted ids.** `subgraph_roots()` already
    reads `reports/bureatten.csv` for exactly this reason --- *"Reading the file rather than
    pasting the ids keeps one list of these people in the repo"* --- and the same holds here:
    these rosters are maintained by their own scripts, so a copy would go stale silently.

    **Why this is not as reckless as it sounds, in her words:** *"the invariant graph structure
    will probably mean they are cumulatively at most a quarter of edits. 1->251 got the 250 giving
    ~50%."* That is the measured precedent: going from 2 roots to 252 took the subgraph 316 -> 565,
    so 250 extra roots bought ~249 people. Roots have sharply diminishing returns because a root
    only seeds what the Wikidata subgraph already connects. Her quarter is a **prediction**, and
    the honest test is running it --- not arguing about it here.

    **A row with no `source` is a placeholder for a group we cannot yet build**, and it stays
    visible rather than being dropped: two of the seven have no roster in this repo at all, and
    one is awaiting her definition. `CLAUDE.md` § *Code that is WRITTEN but never CALLED* is the
    same failure with a data file.
    """
    if not ENTRY_POINT_GROUPS.exists():
        return []
    with open(ENTRY_POINT_GROUPS, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r.get("group")]
    return sorted(rows, key=lambda r: r["group"])


def group_qids(row):
    """The QIDs a group row resolves to, or `[]` if it has no usable roster."""
    # Distinct, because `group_pairs` dedupes on the PAIR: one QID can appear both with and
    # without a Geni id when a group names two rosters of different shapes.
    return sorted(dict.fromkeys(q for q, _ in group_pairs(row)))


def group_pairs(row):
    """`(qid, geni_id)` per roster row --- the Geni id blank when the roster does not carry one.

    **The roster's own `geni_ids` column is the right source and beats a lookup.** The ledger is
    keyed on the Geni id, so an entry point with no Geni id cannot become a ledger row at all.
    Resolving the 321 QIDs through `derived-labels.csv` found only **14**, because that file's
    `qid` column is populated from a different source than these curated pair files ---
    `izumo-p2600-pairs.tsv` and `tanba-p2600-pairs.tsv` each carry the correspondence directly.
    Reading it here rather than re-deriving it is the same rule as reading `bureatten.csv`.
    """
    src = (row.get("source") or "").strip()
    if not src:
        return []
    # **A group may name SEVERAL rosters, comma-separated.** The Samaritan priests are the reason:
    # `samaritan-succession-list.tsv` is the authoritative list of who they are and carries a qid
    # on only 14 of its 132 rows, while `samaritan-priest-links.csv` carries qid/geni pairs for a
    # different, overlapping handful. Neither is the group; the union is closer.
    column = (row.get("qid_column") or "qid").strip()
    out = []
    for part in src.split(","):
        path = ROOT / part.strip()
        if not part.strip() or not path.exists():
            continue
        if path.suffix == ".ged":
            # **The "special geni gedcom recognition" group is a GEDCOM, not a table.** Emma,
            # 2026-09-03: *"There's a specific gedcom that just links geni profiles to wikidata.
            # It carries no relationship data just ids and bios with wikidata links in it."* That
            # is `exports/post-merge/wikidata-qid-links.ged`: `INDI` records holding nothing but a
            # `NOTE` with a Wikidata URL.
            import re

            text = path.read_text(encoding="utf-8")
            current = ""
            for line in text.splitlines():
                ref = re.match(r"0 @I(\d+)@ INDI", line)
                if ref:
                    current = ref.group(1)
                hit = re.search(r"wikidata\.org/wiki/(Q\d+)", line)
                if hit:
                    out.append((hit.group(1), current))
            continue
        delimiter = "\t" if path.suffix == ".tsv" else ","
        geni_col = (row.get("geni_column") or "geni_ids").strip()
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=delimiter):
                q = (r.get(column) or "").strip()
                if not q.startswith("Q"):
                    continue
                raw = (r.get(geni_col) or "").replace(";", " ").replace(",", " ").replace("|", " ")
                ids = [g for g in raw.split() if g.isdigit()]
                out.append((q, ids[0] if ids else ""))
    # Deterministic and deduped on the pair, so a QID appearing with and without a Geni id keeps
    # both rather than depending on which file was read first.
    return sorted(dict.fromkeys(out))


def active_group_qids(today=None):
    """Every QID from every group whose date has arrived."""
    import datetime

    today = today or datetime.date.today().isoformat()
    out = []
    for row in entry_point_groups():
        if (row.get("active_from") or "").strip() <= today:
            out.extend(group_qids(row))
    return sorted(dict.fromkeys(out))


def group_status(today=None):
    """`(group, active_from, qids, state)` per group --- what each one currently contributes."""
    import datetime

    today = today or datetime.date.today().isoformat()
    out = []
    for row in entry_point_groups():
        when = (row.get("active_from") or "").strip()
        n = len(group_qids(row))
        if not (row.get("source") or "").strip():
            state = "NO ROSTER"
        elif n == 0:
            state = "ROSTER EMPTY OR MISSING"
        elif when <= today:
            state = "LIVE"
        else:
            state = "PENDING"
        out.append((row["group"], when, n, state))
    return out


def unresolved_entry_points():
    """Rows that name a person we hold no QID for --- they cannot be roots until one lands.

    Reported rather than dropped silently: a roster row that does nothing and says nothing is
    the § *Code that is WRITTEN but never CALLED* failure with a data file instead of a function.
    """
    return [
        (r["geni_id"], r.get("label", ""), r.get("active_from", ""))
        for r in entry_points()
        if not (r.get("qid") or "").strip()
    ]


def active_entry_points(today=None):
    """The entry points switched on as of `today`, as `(qid, label)`.

    A run is a function of its inputs **and the date**, which is what a timer means. `today` is
    injectable so a run can be reproduced for a past date rather than only for now.
    """
    import datetime

    today = today or datetime.date.today().isoformat()
    return [
        (r["qid"], r.get("label", ""))
        for r in entry_points()
        if (r.get("qid") or "").strip() and (r.get("active_from") or "").strip() <= today
    ]


def pending_entry_points(today=None):
    """The ones still waiting for their date --- reported so a timer is never silent."""
    import datetime

    today = today or datetime.date.today().isoformat()
    return [
        (r.get("qid") or r["geni_id"], r.get("label", ""), r.get("active_from", ""))
        for r in entry_points()
        if (r.get("active_from") or "").strip() > today
    ]


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

#: The clan labels do not go out before this date. See the gate at its use site.
CLAN_BLOCK_GATE = datetime.date(2026, 10, 1)

#: The month-long hold on every item `OBender12` has touched.
#:
#: **Emma's control, 2026-08-30**, and the reasoning is in
#: Emma's decision of 2026-08-30, and the live constraint after that day is
#: not the errors themselves -- those clear -- but **one editor holding a recent memory of the
#: account**. Her words: *"the issue was specifically with this one editor and the fact they
#: saw the same error many times."* Recognition decays more slowly than duplicates do, so the
#: single variable worth controlling is how many further times that person sees us.
#:
#: The hold is on the FULL contributions list, not on its overlap with the ledger. Holding the
#: overlap would re-derive the collision set on every run, which is the coupling the hold
#: exists to break -- a batch tomorrow is not a batch today, and the ledger grows.
#:
#: It expires on its own. A hold that has to be remembered to be lifted is a hold that stays
#: forever, and the whole premise here is that recognition decays.
OBENDER_HOLD_EXPIRES = datetime.date(2026, 9, 30)

#: Written by `scripts/fetch-obender12-touched.py`.
OBENDER_TOUCHED = ROOT / "reports" / "obender12-touched.tsv"


def held_items(today=None):
    """Items our QuickStatements may not edit, because that editor has touched them.

    **Subject only, never value.** Her control is *"our QuickStatements may not edit it"*, and
    a QuickStatements line edits its SUBJECT. `Q1 P22 Q2` is an edit to `Q1`; `Q2` is only
    referenced, and appears on nobody's batch for it. Holding values as well would drop
    every statement pointing at a held person -- which is most of the ring, since the items
    that editor merged are exactly the well-connected ones -- and would buy no reduction in
    what they see.

    **This is also what closes the re-emission loop for the people they edited.** A generator
    that emits what is missing cannot tell a deletion from an absence, so it re-adds anything
    anyone removes; see `queue.md` § *The unintentional edit war*. Holding the subject stops
    that for exactly the items where it actually happened, which is a narrower fix than
    suppression tracking and lands first.

    Returns an empty set once the hold expires, so nothing has to remember to lift it.
    """
    today = today or datetime.date.today()
    if today >= OBENDER_HOLD_EXPIRES:
        return set()
    if not OBENDER_TOUCHED.exists():
        return set()
    held = set()
    with OBENDER_TOUCHED.open(encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            qid = line.split("\t")[0].strip()
            if qid.startswith("Q"):
                held.add(qid)
    return held


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
                    # relations.tsv is semicolon-separated -- see build-parent-candidates.
                    # Splitting on "|" here meant an item with two parents or two children
                    # contributed one glued token that linked to nothing real, so the
                    # subgraph this gates every creation on was missing those edges.
                    for v in (row.get(col) or "").split(";"):
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


#: **The CJK clan labels, hard-coded and appended to every batch, exactly like
#: the spine `P2600` block (since removed).** Emma, 2026-08-28: *"Fucking wire it in"*, after the formula was
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
# **15 of these people are NOT unnamed, and they are removed from this block.**
# Emma, 2026-08-29: *"the entire idea of them having unknown names should not be part of the
# pipeline at all if these names are remotely real, even if there are potentially errors."*
#
# Measured by joining each item's P2600 to its Geni record. Three shapes, not one:
#   162  BOTH say unknown -- Wikidata's `Li Mou` is the marker transliterated, since 李某 is
#        literally "Li so-and-so". Calling these people unnamed is correct.
#    11  BOTH have a real name. Geni carries the given name in front of the marker and the
#        pipeline was reading the whole GIVN as a marker: `道古 某` -> Li Daogu, `鎮 某` ->
#        Liu Zhen, `渠牟 某` -> Wei Qumou, `杲之 某` -> Cui Gaozhi.
#     4  WIKIDATA has a name and Geni does not -- Wanshou, Guangde, Liu Yushi, Li Ru. Exactly
#        the case she predicted: *"there might be instances where the Geni has an unknown name
#        and the wikidata has a known name"*.
#
# Writing `Lmul "NN"` on the 15 would assert something one or both databases contradict, on an
# item that already reads with a real name in English. Removed here rather than filtered at the
# use site, so the block itself never carries a false claim.
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
    # Both write `reports/wikidata-garborg-day.txt`, so a bare run silently replaces a batch Emma
    # may already have run, and `--compose` itself ADVANCES the sequence: it consumes and
    # rewrites `reports/garborg-carry-forward.tsv`, so re-running it on the same day produced a
    # batch differing by 19 people out and 17 in -- the next hop, not today's.
    #
    # `--roster` runs are a real second mode and stay allowed. What is refused is the
    # argument-free invocation, which has no purpose except the mistake.
    if not args.compose and not args.roster:
        sys.exit(
            "refusing an argument-free run: it skips the daily caps (272 creations against 34) "
            "and overwrites reports/wikidata-garborg-day.txt, which may be a day already run.\n"
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

    def father_item(dad):
        """The QID for a patronymic's `P144` *based on*, or `None`.

        **Emma, 2026-09-02:** *"Patronymics are not getting the names they come from in the
        logic lol that's actually essential to the real specified algorithm."* She is right and
        the cause was scope, not a missing feature: `namemodel.statements_for` has taken a
        `father_qid` since it was written, and both call sites passed one -- but they looked the
        father up in `our_items`, **the 1,179-row ledger**, when 518,855 Geni ids carry a
        `P2600` on Wikidata. So `P144` fired only when she happened to have made the father
        herself. Measured before the change: 6 `P5056` statements, 2 with `P144`.

        **The ledger first, then any `P2600` -- and the correspondence union NOT at all.** Those
        first two are direct statements of identity: one she made, one Wikidata already holds.
        `known_pair` is 568,535 wide and includes zipper-inferred pairs, which
        `reports/zipper-reliability.md` measures at 2.8-4.8% error. A wrong `P144` does not
        merely mis-rank something -- it asserts this patronymic derives from THAT man, which is
        a false claim about a named person. `CLAUDE.md`: labels confirm a position, they never
        choose one, and the same caution applies to a father.
        """
        if not dad:
            return None
        return our_items.get(dad) or any_wikidata_item.get(dad)

    # **A P2600 is not the only way we know somebody already has an item -- and on 2026-09-01 it
    # let a duplicate through.** Emma, on `Q550343` *Welf I, Duke of Bavaria*, an item with 27
    # sitelinks that a batch re-created as `Q141249742`: *"this one was made as a new individual
    # ... idk why but it was an error."*
    #
    # Welf carried **no `P2600` at all**, so the map above could not see him. The zipper could,
    # and did: `4927821250240067090 -> Q550343` was in `reports/zipper-pairs.tsv` on 2026-08-26,
    # a week before the batch, and `reports/synoptic-correspondence.tsv` recorded it as
    # `structural;zipper` -- two independent sources.
    #
    # **The rule was already known and applied in the wrong script.**
    # `scripts/build-parent-candidates.py` treats the correspondence as authoritative for "this
    # person is spoken for", with a comment quoting her on exactly this failure:
    # *"Most have identification already on wikidata lmao."* The script that CREATES items never
    # learned it. That is `CLAUDE.md` § *Code that is WRITTEN but never CALLED*, one level up --
    # the lesson landed, in one place only.
    #
    # **Held, not linked, matching how the `P2600` guard already behaves.** A zipper pair carries
    # a measured 2.8-4.8% error, so some of these will be wrong -- and the two outcomes are not
    # symmetric. Holding a creation costs a day, because tomorrow's batch runs again; creating a
    # duplicate costs her a manual merge on Wikidata, which is what this is written against.
    correspondence = ROOT / "reports" / "synoptic-correspondence.tsv"
    known_pair = {}
    if correspondence.exists():
        with open(correspondence, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="	"):
                g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
                if g and q:
                    known_pair.setdefault(g, (q, row.get("sources") or "?"))
        print(f"{len(known_pair):,} Geni ids identified with an item in the correspondence union")
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
        # **A timer that fires silently is a timer nobody can check.** Both lists print every
        # run, so the day one switches on is visible in the output rather than inferred.
        for qid, label in active_entry_points():
            print(f"  entry point LIVE  {qid} {label}")
        for qid, label, when in pending_entry_points():
            print(f"  entry point PENDING {qid} {label} — switches on {when}")
        for gid, label, when in unresolved_entry_points():
            print(f"  entry point UNRESOLVED geni:{gid} {label} — dated {when}, but we hold no "
                  f"QID for them, so they cannot be a root until the correspondence lands")
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

    # The same rule, from the correspondence rather than the P2600 snapshot. See the note above.
    corr_dup = [g for g in to_create if g in known_pair and g not in our_items]
    for g in corr_dup:
        q, src = known_pair[g]
        to_create.pop(g, None)
        carried.append((g, "", f"already identified as {q} via {src} "
                               f"(reports/synoptic-correspondence.tsv) - creating it would "
                               f"duplicate; link it instead"))
    if corr_dup:
        print(f"{len(corr_dup)} dropped: already identified with an item by the correspondence")

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
                # **`nsfx` is read so the name model can REFUSE it.** Geni puts a title in the
                # name-suffix field -- `Queen of Sweden`, `Graf`, `Knight` -- and
                # `build-display-names.py` concatenates every piece into `display_name`, so
                # without this column nothing downstream can tell a title from a surname.
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm", "nsfx",
                                           "display_name")}

    # Relationships, from the tree, in both directions.
    father, mother = {}, {}
    children = collections.defaultdict(set)
    spouses = collections.defaultdict(set)
    siblings = collections.defaultdict(set)
    # **A person can sit in several parent families, and this used to keep whichever came
    # last.** `(father if sex == "M" else mother)[k] = p` is a plain dict write, so for anyone
    # with more than one recorded parent-family the last one processed silently won — and the
    # synthetic placeholders minted by `build-scraped-gedcom.py` (`9995…`, which carry no QID
    # and never will) compete on equal terms with the real parent.
    #
    # Found 2026-08-31 on `Kristofer Sahlin`, step 6 of the Arne↔Bureus spine. His mothers are
    # `4520166 | 9995000000000000647 | 9995000000000102355`; the real one is Maria Nordenfelt,
    # a hardcoded anchor holding `Q116760688`. With a placeholder winning, he had no relative
    # with a QID, so his creation was dropped as *"no relationship could be emitted"* and the
    # spine stalled a step short at that end.
    #
    # **Collect every candidate, then choose.** A parent we can actually point at beats one we
    # cannot; a real Geni id beats a minted placeholder; otherwise keep the first, which is at
    # least stable between runs rather than dependent on dict ordering. This is the same shape
    # as the `fathers`/`mothers` plural-column bug: multi-valued data flattened to one
    # arbitrary value, producing a clean number that is about the flattening.
    father_all = collections.defaultdict(list)
    mother_all = collections.defaultdict(list)
    for fam, parents in fam_p.items():
        kids = fam_c.get(fam, [])
        for p in parents:
            for k in kids:
                children[p].add(k)
                sex = (facts.get(p, {}).get("sex") or "")
                (father_all if sex == "M" else mother_all)[k].append(p)
        for a in parents:
            for b in parents:
                if a != b:
                    spouses[a].add(b)
        for a in kids:
            for b in kids:
                if a != b:
                    siblings[a].add(b)

    def _best_parent(candidates):
        """The parent worth pointing at: one with a QID, else a real profile, else the first."""
        for c in candidates:
            if c in our_items:
                return c
        for c in candidates:
            if not c.startswith(("9995", "9990")):
                return c
        return candidates[0]

    for _k, _v in father_all.items():
        father[_k] = _best_parent(_v)
    for _k, _v in mother_all.items():
        mother[_k] = _best_parent(_v)

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

    # **A QID that already carries a `P2600` is SPOKEN FOR, whoever holds it.** `claimed` was
    # built from the ledger alone, so a child item Wikidata has already tied to some other Geni
    # profile counted as "unmatched" and blocked a creation that could not possibly duplicate it.
    #
    # Found 2026-08-31 on `Kristofer Sahlin`, step 6 of the Arne↔Bureus spine. His mother
    # `Q116760688` has two children on Wikidata, `Q6088529` and `Q6088489` — and both already
    # state `P2600` for *other* people (Mauritz Sahlin `6000000004565255638` and Enar Sahlin
    # `6000000023073624991`). Kristofer is `6000000003002231602`, neither of them. The guard
    # nevertheless held him, because neither QID was in the ledger.
    #
    # This is the same blind spot the spine anchors had (since removed): knowledge that lives in
    # `out/wikidata/p2600-all.tsv` and never reached the logic that needed it. Widening
    # `claimed` does not weaken the guard — it still refuses when a parent has a child item
    # nothing accounts for. It stops it refusing when Wikidata plainly accounts for it.
    claimed = set(our_items.values()) | set(any_wikidata_item.values())
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
    # What the labels actually SAY, live, so a disagreement can be seen. See
    # `read_live_labels` and Emma's rule of 2026-08-30.
    live_labels = read_live_labels()
    # A live read beats both the store and the guess. `reports/garborg-live-state.tsv`
    # records what each item held on 2026-08-24; the store predates most of them and
    # the fallback below assumes our own batch made them, which is wrong wherever Emma
    # edited by hand. Eivind is the case: he carries P735/P734/P5056 she added herself.
    state.update(live_state())
    live_values = read_live_values()
    suppressed = read_suppressed()
    suppressed_hits = set()
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

        **NEITHER form of private gets a qualifier.** Emma, 2026-08-30, shown that
        `Q141223549` carried `P1810 "Private"` while Geni's site displays `<private> Paulson`:

        > *"there are two different kinds of private on Jenny… this is some weird-ass backend
        > difference that affects the Gedcom export, but they display identically. If this is
        > the case, there's no way to get a consistent subject name as a thing from the Gedcom
        > thing for these individuals, so neither form of private should be present as the
        > qualifier."*

        **This reverses her 2026-08-29 ruling that the marker went in verbatim**, and why that
        one failed is the part worth keeping: it assumed the export and the web display agree.
        They do not. Both forms are in the corpus — `<private> /Surname/` **19,945** times and
        bare `Private` **99,645** — and Geni shows the same thing for both, so which one a
        profile exports as is a backend artefact rather than a fact about the person. A
        qualifier built from it records our export, not what the source displays, which is the
        entire justification for the property.

        `P1810` on a NAMED person is unchanged and still carries what Geni renders.
        """
        raw = (fields.get(g) or {}).get("display_name", "")
        if not raw or _carries_marker(raw) or "<private>" in raw.casefold():
            return ""
        return f'\tP1810\t"{qs(raw)}"'

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
        # **Never re-add what another editor removed.** `read_suppressed` carries the why.
        # This sits after the live-values check on purpose: a statement the item still holds
        # is a no-op, but one a stranger deleted is the start of an edit war, so it is the
        # last word before a line is written.
        if (q, prop, value.strip('"')) in suppressed:
            suppressed_hits.add((q, prop, value.strip('"')))
            return
        seen.add((q, prop, value))
        # **An identifier is not sourced to itself.** Emma, 2026-08-31: *"geni ids do not get
        # sources"*. `Q6014618 P2600 "4198641" S2600 "4198641"` cites the Geni id statement to
        # the Geni id -- circular, and it says nothing a reader did not already have in the
        # value. `S2600` is right on every *derived* statement, because there the Geni profile
        # is external evidence for a claim; on `P2600` it IS the claim.
        #
        # The CREATE path already had this right -- it emits `LAST P2600 "..." P1810 "..."`
        # with no reference -- so this is the two paths disagreeing, not a new rule.
        reference = "" if prop == "P2600" else ref(g)
        lines.append(f"{q}\t{prop}\t{value}{qual}{reference}")

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
        # **A person with no name gets no name statements.** Emma, 2026-08-30, on
        # `Q141224141`: *"please stop trying to assign names to this person who does not in
        # fact have any names at all."* Geni records him `En dodfodd son Bielke` -- Swedish for
        # *a stillborn son* -- and this emitted `P735` given name `En`, the indefinite article,
        # carrying `P7452` *usual forename*. 505 people in the corpus carry a stillborn word.
        #
        # The label fix in `labels.strip_markers` is not enough on its own, because the name
        # model reads the raw `GIVN`/`SURN` fields rather than the label, which is exactly the
        # separation `namemodel` was built for. So the gate goes here as well.
        if absent(q, "P735") and absent(q, "P734") and _has_given_name(fields.get(g)):
            dad = father.get(g)
            # The father's NAME, not just his QID: Emma's test reads his given name and
            # his own patronymic to decide whether this token is inherited or derived.
            # **`fields` was NOT passed here, and that is how `Queen` became a given name.**
            # Without it `statements_for` falls back to parsing the rendered label
            # positionally, and the rendered label is `givn + surn + NSFX` run together --
            # so `Bengta Ebbesdotter Ebbesdatter Hvide Queen of Sweden` gave `P735` *given
            # name* Queen and `P734` *family name* Sweden on `Q2183430`. The creation path
            # 400 lines below always passed them; this one never did.
            for line in name_lines(labels.get(g, ""), plan, g,
                                   father_item(dad),
                                   fields=fields.get(g),
                                   father_name=labels.get(dad, "") if dad else "")[0]:
                lines.append(line.replace("LAST\t", f"{q}\t", 1))

        # **Every CJK label is redone, and a DISAGREEMENT is emitted.** Emma, 2026-08-30:
        # *"Every single label gets redone and if they disagree then they go onto the
        # quickstatements that are generated."*
        #
        # This used to emit only into a language the item did not have, on the reasoning that
        # `Lja`/`Lzh` REPLACE and overwriting is dangerous. That reasoning was right about
        # `en`/`mul`, which can hold a curated Norwegian label, and wrong about `ja`/`zh`:
        # **we wrote essentially all of them**, so declining to overwrite meant a rule fix
        # never reached the items the old rule had already labelled. The `ck` doubling
        # (`モルクク`) would have sat on every affected item forever.
        #
        # The absence check also could not work: `langs` comes from the offline store, which
        # predates every item Emma has made, so an item she created yesterday looks label-less
        # whatever it holds. `reports/garborg-live-labels.tsv` is the live value, from the same
        # fetch as the live statements.
        langs = state.get(q, (set(), set()))[0]
        # **Transliterate the item's OWN Latin label, not our Geni display string.**
        #
        # Emma, 2026-08-30, on `Q6161733`: *"why was the japanese label we added so weird?"*
        # then, cutting to it: *"The wikidata label doesn't have that in it… I think it's the
        # geni display name."* She is right. The item reads `Carl Fredrik Piper` in both `en`
        # and `sv`; our derived label reads `Carl Fredrik Piper till Krageholm`, and reading
        # that token by token produced `カール・フレドリク・パイパー・ティル・クラゲホルム`.
        #
        # `CLAUDE.md` already states this for the Latin label -- *"emitting ours would
        # overwrite a better label with a Geni display string"*, on `Q467497` -- and the CJK
        # label is derived from a label, so the same reasoning applies one step earlier and was
        # simply never applied there.
        #
        # It is not only estates. Of 701 ledger items with a live label, **41 differ from
        # ours**, and the differences are Geni disambiguators: `(1745–1800)`, `(jurist)`,
        # `Erik Benzelius den yngre` against `the Younger`. Every one of those would have been
        # transliterated as part of the name.
        #
        # A creation has no item yet, so there ours is all there is; that path keeps
        # `_drop_territorial`.
        #
        # **The `mul` label is chosen by CONSENSUS across the item's own languages**, and
        # everything else follows from it. Emma's specification, 2026-08-30:
        #
        # > *"it would have observed that the person either has an English-language label that
        # > is in Latin characters, or they have a consistent Latin label across two or more
        # > languages. It would have assigned that one, whichever one is the most common, as
        # > the multi-language label… and it would have also been assigned to the English
        # > language if English language lacked it. The Chinese and Japanese would have been
        # > derived from the multi-language label. The real multi-language label will be
        # > assigned, and then the Geni one would have been added as the Geni display name, the
        # > Geni display name qualifier subject named as, and it would have been added as a mul
        # > alias."*
        #
        # And the one she closed explicitly: *"The transliteration of the Geni display name
        # does not go into Japanese or Chinese aliases."* No `Aja`, no `Azh`.
        mine = {lang: value for (qq, lang), value in live_labels.items() if qq == q}
        # **No live labels means we do not know what the item says, and a `Lmul` REPLACES.**
        # `Q19842232` got `Lmul "Algot Brynolfsson"` written over whatever it held, because an
        # item outside the ledger is never fetched, so `mine` was empty, so the consensus read
        # as "it has no `mul`" rather than "we have not looked". Absence of evidence was being
        # treated as evidence of absence -- the same shape as every other bug today.
        mul = consensus_latin_label(mine) if mine else ""
        # **`consensus_latin_label` reads `en` first, and for a redacted person `en` is our own
        # descriptive sentence** -- `CLAUDE.md` § *The NN/Private label algorithm* puts it
        # there on purpose. Promoting it to `mul` displaced the marker that
        # § *`NN` is PRESERVED in `mul`* calls *"always preserved"*: `Q141249589` went out as
        # `Amul "NN"` followed by `Lmul "son of Astri Torchelsdatter Øvre Time"`, which is the
        # exact erasure that section was written against, in the one slot every language falls
        # back to. Dropping it here leaves `mul` alone; the description keeps living in `en`.
        if is_relationship_description(mul):
            mul = ""
        # **The consensus label carries whatever language Wikidata wrote it in**, and for a
        # generation suffix that is the wrong language for `mul`. `Q106206114` reads
        # `Elias Lagerheim den yngre` in `sv` and in `en`, so the consensus is the Swedish
        # phrase; Emma wants `Elias Lagerheim II` in `mul` and `Elias Lagerheim Jr.` in `en`.
        # See `namemodel.GENERATION_SUFFIX`.
        mul = normalise_generation_suffix(mul, "mul")
        source = mul or labels.get(g, "")

        # A live label that already reads correctly is not replaced by the same thing with a
        # title on the front. See `_only_adds_a_title`.
        if _only_adds_a_title(mine.get("mul"), mul):
            mul = ""
            source = labels.get(g, "")

        if mul:
            # A label REPLACES, so whatever `mul` currently reads goes out as an alias FIRST --
            # `CLAUDE.md` § *The MARRIED name is the real name*, where some of those values are
            # Emma's own hand-edits and nothing else records them.
            current = mine.get("mul")
            if current and current != mul:
                lines.append(f'{q}\tAmul\t"{qs(current)}"')
            if current != mul:
                lines.append(f'{q}\tLmul\t"{qs(mul)}"')
            if not mine.get("en"):
                lines.append(f'{q}\tLen\t"{qs(normalise_generation_suffix(mul, "en"))}"')
            # The Geni rendering is an ALIAS on `mul`, never a label and never a CJK alias.
            # A redaction marker is not a name and does not become one here either.
            geni_name = (fields.get(g) or {}).get("display_name", "")
            if (geni_name and geni_name != mul and not _carries_marker(geni_name)
                    and "<private>" not in geni_name.casefold()
                    and geni_name not in {v for (qq, _l), v in live_labels.items() if qq == q}):
                lines.append(f'{q}\tAmul\t"{qs(geni_name)}"')

        ja, zh, ko = label_in(source, table)
        if ja and q not in CJK_LABELS_NOT_OURS:
            for code, value in (("ja", ja), ("zh", zh), ("ko", ko)):
                live = live_labels.get((q, code))
                if live is None and code in langs:
                    # The store says the language exists but we do not know its value, and a
                    # blind overwrite is what this branch used to refuse to do. Leave it: the
                    # next live refresh gives the value and the disagreement is emitted then.
                    continue
                if live != value:
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

        # **A creation whose label+empty-description pair is already taken is REFUSED by
        # Wikidata**, and a refusal lands mid-batch. `CLAUDE.md` § *NO descriptions and NO edit
        # summaries*: the resolution is to hold the person, never to add a description.
        # `scripts/check-label-collisions.py` writes the list; it is data, so the hold cannot
        # drift into a hand-maintained exclusion.
        if g in _label_collisions():
            carried.append((g, label, "label+empty-description pair already taken on Wikidata"))
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
            from labels import drop_marker_surname as _dms, UNNAMED_MARKER
            # **An empty label is never emitted, and `NN` is what an unnamed person gets.**
            # `6000000184732963823` is recorded on Geni as a bare `1 NAME` with nothing after
            # it, so the whole chain produced `""` and the batch carried `LAST Lmul ""` --
            # creating an item with no label at all, which is not a person anyone can find and
            # is not what `CLAUDE.md` § *`NN` is PRESERVED in `mul`* asks for. The marker is
            # the floor: *"NN is always preserved in the multi-language label."*
            mul_value = _dms(nn_form(qs(labels.get(g, "")))) or UNNAMED_MARKER

            # **A married NN woman has TWO recorded surnames and was keeping one.**
            # This branch set `birth = ""` and never reached the alias block below, so
            # `NN /Thaulow/` who married a Hahn went out as one label and her birth
            # surname was dropped. **1,636 NN or redacted people carry a `SURN` and a
            # DIFFERENT `_MARNM`** -- measured over `display-names.csv`, not supposed.
            #
            # `CLAUDE.md` § *The MARRIED name is the real name* decides which way round:
            # the married form is the label and the birth form is the `Amul`. That is
            # exactly what the named branch does, and there is no reason a redacted
            # person should be treated differently -- the surname is the part redaction
            # does not take.
            _f = fields.get(g, {})
            _surn = " ".join((_f.get("surn") or "").split())
            _marnm = " ".join((_f.get("marnm") or "").split())
            _nn_birth = ""
            if _surn and _marnm and _surn.casefold() != _marnm.casefold():
                mul_value = f"{UNNAMED_MARKER} {qs(_marnm)}"
                _nn_birth = f"{UNNAMED_MARKER} {qs(_surn)}"
            lines.append(f'LAST\tLmul\t"{mul_value}"')
            if _nn_birth and _nn_birth != mul_value:
                lines.append(f'LAST\tAmul\t"{_nn_birth}"')
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

            ja, zh, ko = label_in(primary, table)
            if ja:
                lines.append(f'LAST\tLja\t"{ja}"')
                lines.append(f'LAST\tLzh\t"{zh}"')
                # **Korean is CJK and a creation carries it too.** Emma, 2026-09-01:
                # *"cjk includes korean"*. Without this the gate could require `ko`
                # while the CREATE block never wrote one.
                lines.append(f'LAST\tLko\t"{ko}"')
                # **A TRANSLITERATED birth name is not a `ja`/`zh` alias.** Emma, 2026-08-30:
                # *"The transliteration of the Geni display name does not go into Japanese or
                # Chinese aliases"*, and asked directly: *"No ja/zh alias at all."*
                #
                # The rule above was already narrower than what this did. `CLAUDE.md`
                # § *The MARRIED name is the real name* allows `Aja`/`Azh` for **a non-Latin
                # birth form**, *"which cannot live in `mul`"* -- a name already written in
                # CJK. This emitted `ペルネル・ヴェライネ・スヘルン`, our own transliteration of
                # a Latin name, which is a reading we invented rather than a form she has.
                #
                # So the alias survives only where the birth name is genuinely non-Latin, and
                # then it is the name itself, not a transliteration of it.
                if birth and not re.search(r"[A-Za-zÀ-ÿ]", birth):
                    lines.append(f'LAST\tAja\t"{qs(birth)}"')
                    lines.append(f'LAST\tAzh\t"{qs(birth)}"')
            else:
                # **THE GATE: no `ja`/`zh`, no creation.** Emma, 2026-08-31, asked whether the
                # seven-language rule is still real given the daily batch creates people every
                # day: *"Still a gate, and the daily batch is violating it."*
                #
                # It was. This carried the person forward AND emitted the `CREATE` anyway, so
                # the carry-forward recorded a debt that was never owed while the person was
                # made without their CJK labels regardless. Abandoning the block is what the
                # carry always claimed to be doing.
                #
                # `queue.md` § *ABSOLUTE PREREQUISITE* is her earlier statement of the same rule
                # -- *"an absolute prerequisite for the creation of any individual: that we have
                # their CJK labels"* -- filed for later. Her ruling today moves it to now.
                carried.append((g, label, "GATE: no ja/zh/ko label, so not created"))
                del lines[block_start:]
                continue
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
        # **A date carries its GEDCOM modifier as a qualifier, or it asserts something Geni
        # does not.** Emma, 2026-08-29: *"we very much need to have those qualifiers, and I
        # don't know why it is that you don't. That was almost a prerequisite for putting any
        # Geni information on Wikidata."*
        #
        # Every `ABT`, `BEF`, `AFT` and `BET x AND y` was being flattened to a bare value --
        # **70,665 `about`, 5,923 `after`, 5,907 `before`, 3,004 `between`** in
        # `derived-facts.csv` -- which states a date the source explicitly hedges. The parse
        # was never the missing part: that file has carried `birth_date_modifier` and
        # `birth_date_year_end` all along, and `genimerge.dates` is the authority on the
        # grammar. Only the emission was absent.
        for prop, iso, prec, mod, end in (
                ("P569", f["birth_date_iso"], f["birth_date_precision"],
                 f.get("birth_date_modifier", ""), f.get("birth_date_year_end", "")),
                ("P570", f["death_date_iso"], f["death_date_precision"],
                 f.get("death_date_modifier", ""), f.get("death_date_year_end", ""))):
            if iso and prec:
                lines.append(f"LAST\t{prop}\t{iso}/{prec}"
                             f"{date_quals(mod, iso, prec, end)}{ref(g)}")
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
        # sibling links too numerous on one batch. `_siblings_emitted` is shared module state
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
        # the ones still to be made are in reports/wikidata-garborg-name-items.txt and
        # join the batch the day after that runs, same single-run rule as everyone.
        # A redacted profile gets no name statements for the same reason it gets no
        # label: `<private>` is Geni withholding the name, not a name. Asking the plan
        # for a `<private>` given-name item produced three "name item missing" rows
        # that read as work to do, when the right answer is that there is nothing
        # underneath. The *surname* survives redaction and is real data -- but these
        # three are `<private> Garborg`, and `Garborg` is their father's family name,
        # which `P22` already says.
        # **The same no-name gate as the existing-items path.** A stillborn description is not
        # a name: `En dodfodd son Bielke` produced `P735` given name `En`, the Swedish
        # indefinite article, on `Q141224141`. Emma, 2026-08-30: *"please stop trying to assign
        # names to this person who does not in fact have any names at all."* Gating only the
        # existing-item path would fix the item she saw and keep making new ones.
        if not redacted and _has_given_name(fields.get(g)):
            dad = father.get(g)
            name_statements, unresolved = name_lines(
                labels[g], plan, g, father_item(dad),
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
    # `reports/wikidata-garborg-name-items.txt`, run between the two.
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

    # **Say what the suppressor stopped, every run.** A guard nobody can see is a guard
    # nobody trusts, and this one exists precisely because a silent re-emission started an
    # edit war. If this number is ever large, that is worth reading rather than ignoring.
    if suppressed_hits:
        print(f"suppressed: {len(suppressed_hits)} statement(s) another editor removed and "
              f"this batch would have re-added")
        for q, prop, value in sorted(suppressed_hits)[:10]:
            print(f"   {q} {prop} -> {value}")

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

    # ---- NEVER emit the same statement twice in one CREATE block ------------------------
    #
    # **What produced it, seen 2026-08-30 in `wikidata-garborg-name-items.txt`:** the name-item
    # emitter writes one line per *bearer*, and a bearer is a Geni profile. Two Geni profiles
    # resolving to the same Wikidata item therefore write the same statement twice --
    # `Q141216607 P5056 LAST` under the `Erikson` block, whose third "bearer" had no name to
    # put in the comment because it was the second profile of the second one.
    #
    # `CLAUDE.md` § *Duplication is a DOUBLE-EDGED SWORD* is not in tension with this. Her
    # duplication is deliberate and lives on ITEMS, where it attracts a bot. This is one file
    # saying the same thing twice, which is the unintentional repetition the same section names
    # as the actual failure -- and it is what a reader sees, not what a bot fixes.
    #
    # Scoped to the block, exactly as `tests/test_p2600_batches.py` scopes it: a `LAST` line is
    # only meaningful under the `CREATE` above it, so identical text in two different blocks is
    # two different subjects and must survive.
    seen_in_block, deduped, repeats = set(), [], 0
    for ln in kept:
        stripped = ln.strip()
        if stripped == "CREATE":
            seen_in_block = set()
            deduped.append(ln)
            continue
        if not stripped or stripped.startswith("#"):
            deduped.append(ln)
            continue
        if stripped in seen_in_block:
            while deduped and deduped[-1].lstrip().startswith("#"):
                deduped.pop()
            repeats += 1
            continue
        seen_in_block.add(stripped)
        deduped.append(ln)
    if repeats:
        print(f"repeated statements: {repeats} line(s) dropped")
    kept = deduped

    # ---- THE HOLD: nothing we emit may edit an item that editor has touched -------------
    #
    # `held_items()` carries the reasoning. It is applied here, at the last thing that touches
    # the file, for the same reason the exclusion above is: whatever the rest of the algorithm
    # decided, this holds it. It is SUBJECT-only -- a line edits the item in its first field.
    #
    # A `CREATE` mints a new item and so can never be held; the `LAST` lines that follow it
    # address that new item, so they are not held either.
    held = held_items()
    if held:
        kept2, held_dropped = [], 0
        for ln in kept:
            stripped = ln.strip()
            if stripped == "CREATE":
                kept2.append(ln)
                continue
            subject = stripped.split("\t")[0].lstrip("-")
            if subject == "LAST":
                kept2.append(ln)
                continue
            if subject in held:
                while kept2 and kept2[-1].lstrip().startswith("#"):
                    kept2.pop()
                held_dropped += 1
                continue
            kept2.append(ln)
        if held_dropped:
            print(f"OBender12 hold: {held_dropped} statement line(s) dropped across "
                  f"{len(held):,} held items — expires {OBENDER_HOLD_EXPIRES}")
        kept = kept2

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
    # **The drops are RECORDED, not just logged.** A `P22`/`P25` suppressed here leaves its
    # `P40` partner one-way, which is deliberate -- `P40` is multi-valued and states the same
    # fact from the side that permits it -- but it looks identical to the one-way links Emma
    # spent weeks repairing by hand. `test_every_link_to_an_existing_item_is_emitted_in_BOTH
    # _directions` exempts exactly the pairs in this file and nothing else, so the exemption
    # cannot quietly widen into "one-way links are fine".
    drops = ROOT / "reports" / "single-value-drops.tsv"
    with open(drops, "w", encoding="utf-8", newline="") as f:
        f.write("subject\tproperty\tdropped_value\talready_holds\n")
        for subject, prop, value, held in second_parent:
            f.write(f"{subject}\t{prop}\t{value}\t{';'.join(held)}\n")
    if second_parent:
        print(f"single-value guard: {len(second_parent)} P22/P25 line(s) dropped -- the item "
              f"already has one, and a second trips the constraint")
        for subject, prop, value, held in second_parent[:6]:
            print(f"   {subject} {prop} -> {value}; already has {';'.join(held)}")
        print(f"   recorded in {drops.relative_to(ROOT)}")
    lines = kept

    # The CJK clan labels, same mechanism. See `CJK_CLAN_BLOCK`. **Removed on 2026-08-29 and
    # put straight back** -- I read *"remove that particular section"* as this block when she
    # meant the spine P2600 one. Emma: *"What the fuck the clan block is gone? Bring it the
    # fuck back"*.
    # **The clan block is GATED until October.** Emma, 2026-08-29: *"we block the clan name
    # application stuff for one month. In October, once the October gate passes, then the quick
    # statements generate with these clan names in them, but otherwise they do not, because I'm
    # just too sceptical of the clan names."*
    #
    # Her reason is doubt about the labels themselves, not their volume: *"I don't know if this
    # clan stuff is right. If this clan stuff is wrong, it looks really bad."* So this suppresses
    # the whole block rather than trimming it, and the date is the same 2026-10-01 the universe
    # kluge expires on.
    #
    # It appeared in every batch because it is hard-coded and appended unconditionally, NOT
    # because everyone else's `ja`/`zh` was finished -- on the day she asked, 19 people in the
    # carry-forward still had no transliteration at all.
    clan_block = CJK_CLAN_BLOCK if datetime.date.today() >= CLAN_BLOCK_GATE else ""
    if not clan_block:
        print(f"CJK clan labels suppressed until {CLAN_BLOCK_GATE} (her ruling, 2026-08-29)")
    lines = _cap_label_edits(
        lines, clan_block,
        _label_corrections(our_items, labels, table, state) + _cjk_follows_mul(table))

    out = ROOT / "reports" / "wikidata-garborg-day.txt"
    # **ONE file, names first.** Emma, 2026-08-30: *"One file, not two. Names first, then
    # everything else. Today it is `wikidata-garborg-day.txt` plus
    # `wikidata-garborg-name-items.txt` and a run order to remember."*
    #
    # The two files are the same shape they always were; what changes is that the name items are
    # regenerated in this run and land at the TOP of the day file, so there is no order left to
    # remember and no way to run half of it. `CLAUDE.md` § *Code that is WRITTEN but never
    # CALLED* is the reason this matters more than tidiness: her own diagnosis of why no name
    # item was ever created is *"name creations were always segregated into a different Quick
    # Statements generation pipeline that was never run."*
    #
    # The name items go first because a person's `P735` may point at one. That only works for
    # items that ALREADY exist -- `LAST` names the most recent creation and nothing else, so a
    # person created here cannot reference a name item created here. The ordering is therefore
    # correct rather than load-bearing, and the day after, the link lands.
    name_file = ROOT / "reports" / "wikidata-garborg-name-items.txt"
    # **Her identifications go FIRST, before the name items.** Emma, 2026-09-01: *"the
    # pipeline generates 10 quickstatements adding the geni id to the individuals at the
    # beginning of each generation."* A `P2600` on an existing item needs nothing created, so
    # it can lead; and putting it first means the ledger is truest at the moment the rest runs.
    # **Two blocks lead the file and they are kept SEPARATE**, because they were not and one
    # silently ate the other -- see the note at the name-items block below.
    ident_block = []
    # Every QID this run emits anything for -- so its Geni id leads the file.
    _touched = {ln.split("	", 1)[0] for ln in lines
                if ln[:1] == "Q" and "	" in ln}
    man_lines, man_total, man_held = manual_p2600_lines(_touched)
    if man_lines:
        ident_block = ["# " + "=" * 72,
                       "# HER OWN IDENTIFICATIONS -- P2600 on items that do not carry it yet.",
                       "# These lead the file: the Geni id is the FIRST edit on any individual,",
                       "# and a name item is not an exception to that.",
                       f"# {man_total} in reports/manual-identifications.csv, {man_held} already "
                       f"on Wikidata, {MANUAL_P2600_PER_RUN} a run beyond the ones this run "
                       f"touches.",
                       "# " + "=" * 72] + man_lines + [""]
    print(f"manual identifications: {man_total} in the file, {man_held} already held, "
          f"{len([l for l in man_lines if not l.startswith('#')])} emitted")
    try:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build-garborg-name-items.py")],
                       check=True, cwd=str(ROOT), capture_output=True)
    except Exception as exc:                                        # noqa: BLE001
        print(f"WARNING: could not regenerate the name items ({exc}); using the file on disk")
    # **This block used to ASSIGN `head`, and that discarded every `P2600` above it.** Emma,
    # 2026-09-04: *"It seems it is still messing with people's names without doing geni
    # identifications. Like the name objects are being linked on people without geni ids, this
    # should be categorically not allowed as the geni id must be applied as the first edit on
    # any individual… Idk why it thinks name objects are an exception when the name data even
    # comes from geni"*.
    #
    # She is right and the cause was one character. `manual_p2600_lines` ran, found the ids,
    # `head += …` collected them, `print` reported them as emitted -- and then `head = [ … ]`
    # here replaced the list. **Measured on the batch of 2026-09-04: 161 existing items received
    # `P735`/`P734`/`P5056`, and a live `wbgetentities` says 161 of 161 carry no `P2600`.** Every
    # one is in `reports/manual-identifications.csv`, so the line that would have fixed it was
    # generated on every run and thrown away on every run.
    #
    # That is `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done* in its worst
    # form: the code ran, and only its output was dropped, so the log said the opposite of what
    # the file held.
    name_block = []
    if name_file.exists():
        body = name_file.read_text(encoding="utf-8").strip()
        if body:
            name_block = ["# " + "=" * 72,
                          "# NAME ITEMS. One file, her instruction of 2026-08-30 -- there is no",
                          "# longer a second batch to remember to run. They follow the Geni ids",
                          "# above, per her 2026-09-04 correction.",
                          "# " + "=" * 72,
                          body, "",
                          "# " + "=" * 72,
                          "# THE DAY'S PEOPLE",
                          "# " + "=" * 72, ""]
            print(f"prepended {sum(1 for l in body.splitlines() if l.strip() and not l.startswith('#'))}"
                  f" name-item lines")
    head = ident_block + name_block
    out.write_text(NEWLINE.join(head + lines) + NEWLINE, encoding="utf-8", newline=NEWLINE)
    print(f"wrote {out.relative_to(ROOT)}: {created} creations, {len(seen)} links")

    cf = ROOT / "reports" / "garborg-carry-forward.tsv"
    with open(cf, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "label", "why"])
        w.writerows(carried)
    print(f"wrote {cf.relative_to(ROOT)}: {len(carried)} carried to a later day")

    # **Flush what the funnel rendered on the fly.** A token minted inside `label_in` must
    # reach the shared table, or the next run re-derives it and a hand correction to it is
    # silently overwritten by the rule. Appended once, at the end, because writing per-token
    # would interleave into a file other scripts read while they read it.
    if MINTED_TOKENS:
        tpath = ROOT / "reports" / "garborg-name-transliterations.tsv"
        known = set()
        if tpath.exists():
            with open(tpath, encoding="utf-8") as fh:
                known = {r["token"] for r in csv.DictReader(fh, delimiter="\t")}
        fresh = {t: v for t, v in MINTED_TOKENS.items() if t not in known}
        if fresh:
            # **Read, merge, sort, replace -- never append.** Appending broke the file's
            # ordering, which `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* is about, and it did
            # worse than that on 2026-09-04: the loader keeps the LAST row for a token, so five
            # rule-minted rows sitting past the end silently overrode the readings Emma had just
            # chosen. `d.y.` went back to `ドイ` and `Jr.` to `イル` after both had been fixed,
            # and the fix looked applied because the table's early rows said so.
            #
            # The `t not in known` guard was already there and is not enough on its own: a token
            # deleted from the table and re-minted in the same session is legitimately "not
            # known", and that is exactly how these five arrived. Rewriting the whole file with
            # one row per token makes a duplicate impossible rather than unlikely.
            rows = []
            if tpath.exists():
                with open(tpath, encoding="utf-8", newline="") as fh:
                    reader = csv.DictReader(fh, delimiter="\t")
                    fieldnames = reader.fieldnames
                    rows = list(reader)
            else:
                fieldnames = ["token", "ja", "zh", "ko", "note"]
            by_token = {r["token"]: r for r in rows}
            for t, (ja, zh, ko) in fresh.items():
                by_token[t] = {"token": t, "ja": ja, "zh": zh, "ko": ko,
                               "note": "by rule, minted during the run"}
            from translit_no import table_sort_key
            ordered = sorted(by_token.values(), key=table_sort_key)
            tmp = tpath.with_suffix(".tsv.tmp")
            with open(tmp, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t",
                                   lineterminator="\n")
                w.writeheader()
                w.writerows(ordered)
            os.replace(tmp, tpath)
        print(f"funnel: {len(MINTED_TOKENS)} tokens rendered on the fly, "
              f"{len(fresh)} new to the table")
    for g, label, why in carried[:10]:
        print(f"  {g}  {label[:40]:<40} {why}")


if __name__ == "__main__":
    main()
