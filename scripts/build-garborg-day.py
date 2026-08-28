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
import csv
import random
import re
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
    item carrying no `P2600` yet -- which is exactly Emma's own `Q140568870`. Without it
    the spine walk reached step 1 of `paths/bergitte-to-emma.tsv`, which is HER, found her
    in neither `garborg-qids.tsv` nor `p2600-all.tsv`, and emitted a `CREATE` that would
    have minted her a SECOND item. `CLAUDE.md` says it plainly: she *"has `Q140568870` and
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
        n = (labels.get(gid) or "").strip()
        return "" if not n or n.lower() in ("nn", "private", "unknown", "?") else n

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
SPINE_PATHS = ("paths/charlemagne-to-arne-garborg.tsv", "paths/bergitte-to-emma.tsv")
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

#: **How far from Arne a person may sit and still SEED the daily ring.**
#:
#: Emma, 2026-08-28: *"Why is there a ring that is any more than 1 hop lol?"* There is not —
#: `compose` takes exactly one hop. The defect was where it hopped *from*: `pool = sorted(have)`
#: was the entire ledger, so the run took one hop from each of 156 different places. Measured
#: the same day, those 156 sit at hop distances from Arne of 1 to **46**, and one hop out from
#: the 46 is how a 7th-century Baekje royal (덕장 부여) landed in a batch beside Rogaland
#: farmers, along with Carolingian Friuli and 20th-century Iowa.
#:
#: **The spine is what puts them there.** Her rule that the Arne→Bergitte→Charlemagne couples
#: are always made, outside the caps, is right — but each one then entered the ledger and the
#: *next* run treated it as an ordinary seed and grew a ring around it. The ball sprouted a new
#: lobe at the far end every day. Nobody chose that; it is the spine rule and the seeding rule
#: composing.
#:
#: So the ledger stays whole for *"does this person already have an item"*, and only the seed
#: pool is bounded. `--max-hops` moves it; it is not a cap on how far the programme ever
#: reaches, it is what makes "one hop a day" mean one hop *from Arne*.
#:
#: **One, because she said one.** Emma, 2026-08-28: *"literally nothing in the algorithm as I
#: specified it has any business knowing about anything more than 1 hop away."* This was first
#: written as 6, which was me picking a number that looked reasonable against the measured
#: spread — exactly the kind of invented threshold this repo keeps having to delete. Her
#: specification is hyperlocal and says one.
RING_MAX_HOPS = 1

#: **Never emitted, in any position, ever.** Emma, 2026-08-27: *"I should not be in the
#: traversable graph and neither should any kitajima people."*
#:
#: The batch of 2026-08-27 created her parents and wrote `Q140568870 P22 LAST` and
#: `Q140568870 P25 LAST`, which attached her item to the 1,339,227-person component that
#: contains Charlemagne. Her Geni id reaches the builder through `paths/bergitte-to-emma.tsv`,
#: whose step 1 is her, so excluding her at one call site is not enough — this set is enforced
#: at source *and* asserted over the finished file before it is written.
NEVER_TOUCH_GENI = {
    "6000000087535357291",          # Emma Leonhart herself
}
NEVER_TOUCH_QID = {
    "Q140568870",                   # Emma Leonhart
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
        out[rel] = steps
    return out


def hops_from(start, fam, limit):
    """Geni ids within `limit` hops of `start` over parent/child/spouse edges.

    Breadth-first over `reports/derived-family.csv`. The separator is ` | ` with spaces and
    the strip is load-bearing — `CLAUDE.md` records 379,251 people reading as childless when
    it was missed, so this splits the same way `kin` does rather than inventing a second rule.
    """
    seen = {start: 0}
    frontier = [start]
    for depth in range(1, limit + 1):
        nxt = []
        for g in frontier:
            row = fam.get(g) or {}
            for col in ("fathers", "mothers", "children", "spouses", "father", "mother"):
                for raw in re.split(r"[,;|]", row.get(col) or ""):
                    other = raw.strip()
                    if other and other not in seen:
                        seen[other] = depth
                        nxt.append(other)
        frontier = nxt
        if not frontier:
            break
    return seen


def compose(have, fam, rng, seeds=None):
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
    seeds = have if seeds is None else seeds

    def kin(g, col):
        # The strip is load-bearing: `derived-family.csv` separates with ` | `, and
        # returning the raw token made 59 people a run resolve to nothing.
        return [x.strip() for x in re.split(r"[,;|]", (fam.get(g) or {}).get(col) or "")
                if x.strip() and x.strip() in fam]

    picked, why = {}, []

    def take(gid, reason):
        if gid and gid not in have and gid not in picked:
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
    # **The seed pool, not the ledger.** One hop from Arne's ball, never one hop from
    # everything that happens to hold a QID -- see `RING_MAX_HOPS`.
    pool = sorted(seeds)
    rng.shuffle(pool)
    kids = spouses_instead = 0
    for g in pool:
        if kids + spouses_instead >= CHILDREN_PER_RUN:
            break
        new_kids = [k for k in kin(g, "children") if k not in have and k not in picked]
        if new_kids:
            # ONE child, not all of them. This is the change.
            if take(rng.choice(new_kids), f"child of {g}"):
                kids += 1
            continue
        new_spouses = [x for x in kin(g, "spouses")
                       if x not in have and x not in picked]
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
                   if p not in have and p not in picked]
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
    for g in sorted(set(seeds) | set(picked)):
        father, mother = kin(g, "father"), kin(g, "mother")
        if not father or not mother:
            continue
        known = [x for x in father + mother if x in have or x in picked]
        absent = [x for x in father + mother if x not in have and x not in picked]
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
    ap.add_argument("--max-hops", type=int, default=RING_MAX_HOPS, metavar="N",
                    help=f"how far from Arne a ledger person may sit and still seed the "
                         f"daily ring (default {RING_MAX_HOPS}). The ledger itself is never "
                         f"shrunk by this — only the seed pool.")
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

    have = ledger()

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
    linked = {}
    p2600_all = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if p2600_all.exists():
        with open(p2600_all, encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                    linked.setdefault(row[1].strip(), row[0])
        print(f"{len(linked):,} Geni ids already carry a P2600 somewhere on Wikidata")
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
                if g.isdigit() and q.startswith("Q") and g not in have:
                    have[g] = q
                    n += 1
        print(f"{n} already-existing items read from {path}")
    table = translit()
    plan = load_plan()
    fam_p, fam_c, fams, famc = read_tree()
    print(f"{len(have)} people already carry a QID; {len(table)} tokens transliterated")

    # Everyone one edge away from somebody who has a QID.
    frontier = {}
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
                if gid not in have:
                    frontier.setdefault(gid, "")
        print(f"--roster-is-frontier: {len(frontier)} people taken straight from "
              f"{len(args.roster)} roster file(s), not from the one-edge ring")
    else:
        for person in have:
            for fam in fams.get(person, []) + famc.get(person, []):
                for other in set(fam_p.get(fam, [])) | set(fam_c.get(fam, [])):
                    if other not in have:
                        frontier.setdefault(other, fam)
        print(f"{len(frontier)} people one edge away and not yet on Wikidata")

    # **Emma's own recent family is never created.** Emma, 2026-08-25, looking at a batch:
    # *"no we are no fuckin gmaking my father as a wikidata item right now lol"*. Her father
    # Richard Wade Borsheim (b.1963) sits at step 2 of the Arne path, so any roster built
    # from that path reaches him, and living people are not this programme's business.
    #
    # Five people on that path are 1880 or later: Emma herself (1996), her father (1963),
    # her grandfather Randolph (1926), Reinhert Borsheim (1891) and Selma Pedersdtr.
    # Borsheim (1890). The cut is at **1880** rather than at a name list, so a path that
    # reaches a different modern relative is caught too. "Right now" is hers to lift.
    MODERN_CUTOFF = 1880
    modern = set()
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = (row.get("birth_date_year") or "").strip()
            if b.lstrip("-").isdigit() and int(b) >= MODERN_CUTOFF:
                modern.add(row["geni_id"])
    before = len(frontier)
    frontier = {g: fam for g, fam in frontier.items() if g not in modern}
    if before != len(frontier):
        print(f"born {MODERN_CUTOFF} or later: {before - len(frontier)} dropped, "
              f"never created")

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
        before = len(frontier)
        frontier = {g: f for g, f in frontier.items() if g in near}
        print(f"roster: {len(wanted)} ids from {len(args.roster)} file(s); "
              f"ring cut {before} -> {len(frontier)} (roster members and their in-laws)")

    # ---- THE COMPOSITION replaces the ring entirely, when asked for -------------
    if args.compose:
        fam_rows = {}
        with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                fam_rows[row["geni_id"]] = row
        # Seeded so a run is reproducible and reviewable. `Math.random`-style
        # irreproducibility would make a batch impossible to explain after the fact.
        rng = random.Random(args.seed)
        # **The ball, measured from Arne.** `have` stays whole — it answers "does this person
        # already have an item" and must not shrink — while `seeds` answers "who may the ring
        # grow from", which is the question that was never asked.
        within = hops_from(ARNE_GENI, fam_rows, args.max_hops)
        seeds = {g for g in have if g in within}
        far = len(have) - len(seeds)
        print(f"seed pool: {len(seeds)} of {len(have)} ledger people are within "
              f"{args.max_hops} hops of Arne; {far} further out do NOT seed a ring")
        if not seeds:
            sys.exit(f"no ledger person is within {args.max_hops} hops of Arne "
                     f"({ARNE_GENI}) — that is a broken join over derived-family.csv, not an "
                     f"empty neighbourhood")
        picked, why = compose(have, fam_rows, rng, seeds=seeds)
        print("\ncomposition, per docs/batch-rules.md:")
        for line in why:
            print("   " + line)
        before = len(frontier)
        frontier = {g: frontier.get(g, "") for g in picked}
        compose_why = picked
        print(f"composed batch: {len(frontier)} people to create "
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
    dup = [g for g in frontier if g in linked and g not in have]
    for g in dup:
        frontier.pop(g, None)
        carried.append((g, "", f"Wikidata already links this profile as {linked[g]} "
                               f"(out/wikidata/p2600-all.tsv) - creating it would duplicate"))
    if dup:
        print(f"{len(dup)} dropped: Wikidata already carries a P2600 for them")

    already = set()
    for path in args.exclude:
        already |= set(re.findall('P2600\\t"(\\d+)"',
                                  Path(path).read_text(encoding="utf-8")))
    if already:
        drop = [g for g in frontier if g in already]
        for g in drop:
            frontier.pop(g, None)
        print(f"--exclude: {len(already)} created by an earlier batch today, "
              f"{len(drop)} of them dropped from this one")


    ids = set(frontier) | set(have)
    facts, labels = {}, {}
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
                labels[row["geni_id"]] = (
                    row["label_en"] or row["label_mul"]
                    or (row.get("cjk_names") or "").split(" | ")[0].strip()
                    or (row.get("other_script_names") or "").split(" | ")[0].strip())

    # **The GEDCOM name FIELDS, which is where name objects come from.** Emma,
    # 2026-08-24: *"I thought we were resolving name objects but now we're determining
    # which name field to use as a source of the label?"* -- catching that the name
    # model was re-parsing the rendered label. The first NAME record wins; later ones
    # are alternate forms and `derive-labels.py` already owns those.
    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm")}

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
    kids_of = {}
    rel = ROOT / "out" / "wikidata" / "relations.tsv"
    if rel.exists():
        with open(rel, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="	"):
                if row.get("p40"):
                    kids_of[row["qid"]] = [x for x in row["p40"].split(";") if x]
        print(f"{len(kids_of):,} items with a P40 child list, for the duplicate guard")
    else:
        print("WARNING: out/wikidata/relations.tsv missing - duplicate guard is OFF")

    claimed = set(have.values())
    blocked = {}
    for g in list(frontier):
        if g in RELEASED_FROM_DUPLICATE_GUARD:
            print(f"   released from the duplicate guard: {labels.get(g, g)} -- "
                  f"{RELEASED_FROM_DUPLICATE_GUARD[g]}")
            continue
        for parent in (father.get(g), mother.get(g)):
            pq = have.get(parent) if parent else None
            if not pq:
                continue
            loose = [k for k in kids_of.get(pq, []) if k not in claimed]
            if loose:
                blocked[g] = (pq, loose)
                break
    if blocked:
        for g, (pq, loose) in blocked.items():
            carried.append((g, labels.get(g, ""),
                            f"HELD by the duplicate guard: parent {pq} has unmatched child "
                            f"item(s) {';'.join(loose[:4])} - this person may already be one"))
            frontier.pop(g, None)
        print(f"duplicate guard held {len(blocked)} people whose parent has an "
              f"unmatched child item on Wikidata")

    # `--skip-nn` must bite BEFORE `--limit`, or the limit spends slots on people the run
    # is about to drop: asking for 10 named people returned 7, because 3 of the 10 closest
    # were redacted and were removed afterwards.
    if args.skip_nn:
        dropped = [g for g in frontier
                   if (labels.get(g, "").strip().lower().startswith(("nn", "private", "<private"))
                       or not labels.get(g, "").strip())]
        for g in dropped:
            frontier.pop(g, None)
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
    ring_order = sorted(frontier, key=lambda g: (dist.get(g, 10**6), labels.get(g, "")))
    if args.limit:
        keep = set(ring_order[:args.limit])
        for g in list(frontier):
            if g not in keep:
                carried.append((g, labels.get(g, ""),
                                f"beyond --limit {args.limit}; "
                                f"{dist.get(g, '?')} steps from Arne"))
                frontier.pop(g, None)
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
    state = existing_state(set(have.values()))
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

    def add(q, prop, value, g):
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
        lines.append(f"{q}\t{prop}\t{value}{ref(g)}")

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

    for g, q in sorted(have.items()):
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in have and absent(q, prop):
                add(q, prop, have[target], g)
        for kid in sorted(children.get(g, ())):
            if kid in have:
                add(q, "P40", have[kid], g)
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                if sibling_budget_left() <= 0:
                    carried.append((g, labels.get(g, ""),
                                    f"P3373 sibling {have[sib]} held: over the "
                                    f"{SIBLING_CAP}-a-day cap"))
                    continue
                _siblings_emitted.append((q, have[sib]))
                add(q, "P3373", have[sib], g)
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                add(q, "P26", have[sp], g)

        # Name statements, but never onto an item that already states one: `Q467497`
        # carries `P735` Arne, and our label reads the parenthesised `(Arne)` as a
        # middle name -- emitting it would contradict a curated statement rather than
        # add to it. `CLAUDE.md`: the purpose is to ADD, not to correct.
        if absent(q, "P735") and absent(q, "P734"):
            dad = father.get(g)
            # The father's NAME, not just his QID: Emma's test reads his given name and
            # his own patronymic to decide whether this token is inherited or derived.
            for line in name_lines(labels.get(g, ""), plan, g,
                                   have.get(dad) if dad else None,
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
    for g in sorted(frontier, key=lambda x: labels.get(x, "")):
        f, label = facts.get(g), qs(labels.get(g, ""))
        if not f:
            carried.append((g, label, "no derived facts"))
            continue

        # A redacted profile is created and gets NO label. `CLAUDE.md`: *"Private is
        # a redaction marker, not a name, and an item labelled that asserts something
        # false while being impossible to find. The P2600 is what makes it
        # retrievable."* The person is real and none of the structure is redacted —
        # the Geni id, the sex, the parents, the dates all come through.
        low = label.lower()
        redacted = "<private>" in low or low.startswith("private")
        if redacted and args.skip_nn:
            carried.append((g, label, "redacted: skipped by --skip-nn for this run"))
            continue

        lines.append("CREATE")
        # **Both branches must leave these bound.** The alias block below reads them after
        # the branch, and the redacted branch never set them -- so creating a redacted
        # person crashed with `UnboundLocalError`. It went unseen because the unfiltered
        # ring happened to contain no redacted people; restricting the ring to Emma's own
        # ancestry surfaced it immediately. A redacted person has no married-name alias to
        # emit, so empty strings are the right values, not a guard around the block.
        primary, birth = label, ""
        if redacted or not label:
            # **NOT unlabelled.** `CLAUDE.md` § *`NN` is PRESERVED in `mul`.
            # Descriptive labels are ADDED in other languages* -- the marker stays in
            # `mul` and every local language gets a formulaic description built from
            # the nearest named relative. Emma, 2026-08-16: *"NN and private are the
            # same thing here"*. The surname survives redaction and is real data, so
            # `mul` reads `NN Garborg`, not a bare `NN`.
            # The surname survives redaction and is real data -- CLAUDE.md measured
            # 3,605 such profiles. `<private> Garborg` -> `Garborg`.
            surname = " ".join(t for t in qs(labels.get(g, "")).split()
                               if not t.lower().startswith("<private")
                               and t.lower() not in ("private", "nn"))
            lines.append(f'LAST\tLmul\t"{("NN " + surname).strip()}"')
            described = describe_all(g, facts, father, mother, labels, table,
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
            primary = " ".join(given + marnm.split()) if is_married else label
            birth = " ".join(given + surn.split()) if is_married else ""

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
        lines.append(f'LAST\tP2600\t"{g}"')
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
            if target and target in have:
                lines.append(f"LAST\t{prop}\t{have[target]}{ref(g)}")
                reciprocal.append((have[target], back, g))
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                lines.append(f"LAST\tP26\t{have[sp]}{ref(g)}")
                reciprocal.append((have[sp], "P26", g))
        # **The cap is 10 a day ACROSS EVERY BATCH, and this site was escaping it.**
        # `CLAUDE.md` § *`P3373` sibling is capped at 10 a day*: *"A builder emitting
        # siblings must count them and stop."* The additions pass counted; this one, on the
        # people being CREATED, did not -- so a run came out with 10 capped statements and
        # **28 uncapped**, 38 in a file whose whole reason for the cap is that Emma finds
        # sibling links spammy on a watchlist. `_siblings_emitted` is shared module state
        # precisely so both sites draw on one budget.
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                if sibling_budget_left() <= 0:
                    carried.append((g, label, f"P3373 sibling {have[sib]} held: over the "
                                    f"{SIBLING_CAP}-a-day cap"))
                    continue
                _siblings_emitted.append(("LAST", have[sib]))
                lines.append(f"LAST\tP3373\t{have[sib]}{ref(g)}")
                reciprocal.append((have[sib], "P3373", g))
        for kid in sorted(children.get(g, ())):
            if kid in have:
                lines.append(f"LAST\tP40\t{have[kid]}{ref(g)}")
                sex_of = (facts.get(g, {}) or {}).get("sex", "")
                reciprocal.append((have[kid], "P22" if sex_of == "M" else "P25", g))

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
                labels[g], plan, g, have.get(dad) if dad else None,
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
    qid_to_geni = {q: g for g, q in have.items()}

    def name_of(token):
        geni = qid_to_geni.get(token, token)
        return qs(labels.get(geni, ""))

    lines = annotate(lines, name_of)

    # **The last gate: nothing Emma has excluded may reach the file, in any position.**
    #
    # Enforced here rather than only where statements are built, for the reason `qscomment`
    # gives about comments: this file emits from a dozen sites and a rule applied at each one
    # is a rule that will be missed at the thirteenth. It was — the batch of 2026-08-27 wrote
    # `Q140568870 P22 LAST` and `Q140568870 P25 LAST`, attaching her item to the
    # 1,339,227-person component containing Charlemagne, because her Geni id arrives through
    # `paths/bergitte-to-emma.tsv` whose step 1 is her.
    #
    # **A statement line is DROPPED; a `CREATE` for an excluded person REFUSES the run.**
    # Dropping a statement cannot change which item a later `LAST` resolves to — only a
    # dropped `CREATE` could do that — so the two cases are not the same risk and are not
    # treated the same way. The preceding comment goes with the line it describes.
    excluded = NEVER_TOUCH_GENI | NEVER_TOUCH_QID

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
    lines = kept

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
