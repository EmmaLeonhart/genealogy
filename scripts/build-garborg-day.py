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


def sibling_budget_left():
    return SIBLING_CAP - len(_siblings_emitted)
HUMAN = "Q5"


def qs(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def ledger():
    out = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["geni_id"]] = row["qid"]
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


def describe_all(geni_id, facts, father, mother, labels, table):
    """`{lang: "daughter of Arne Olaus Fjørtoft Garborg"}` for a redacted person.

    Built from the nearest named parent. `ja` and `zh` are included **here** where
    `build-nn-label-batch.py` excludes them, and the reason it excludes them is the
    reason this can: it warns the phrase would come out `Gerard Spencerの娘`, mixing
    scripts, *because the relative's name has not been transliterated*. In this family
    it has — `reports/garborg-name-transliterations.tsv` covers every token — so the
    Japanese and Chinese forms are whole rather than half Latin.
    """
    sex = (facts.get(geni_id, {}).get("sex") or "")
    for parent in (father.get(geni_id), mother.get(geni_id)):
        if not parent:
            continue
        name = (labels.get(parent) or "").strip()
        if not name or name.lower() in ("nn", "private", "unknown", "?"):
            continue
        out = {}
        for lang, words in WORDS.items():
            group = words["child_of"]
            word = group.get(sex) or group[""]
            joiner = words["of"]
            if isinstance(joiner, dict):
                joiner = joiner.get("child_of", joiner[""])
            out[lang] = f"{word} {joiner} {qs(name)}"
        ja, zh = label_in(name, table)
        if ja:
            out["ja"] = f"{ja}の{'息子' if sex == 'M' else '娘' if sex == 'F' else '子'}"
            out["zh"] = f"{zh}之{'子' if sex == 'M' else '女' if sex == 'F' else '子女'}"
        return out
    return {}


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
    Japanese label, it is a broken one.
    """
    ja, zh = [], []
    for token, _usage, _o in classify(label):
        pair = table.get(token)
        if not pair:
            return None, None
        ja.append(pair[0])
        zh.append(pair[1])
    return "・".join(ja), "·".join(zh)


def name_lines(label, plan, geni_id, father_qid, fields=None, sex=""):
    """`P735`/`P734`/`P5056` lines for one person, and what could not be emitted.

    **Only tokens whose item already exists.** A name item this run is creating
    cannot be pointed at, same single-run rule as everybody else, so the rest waits
    for `reports/wikidata-garborg-name-items.qs` to have been run.

    QuickStatements takes qualifiers exactly like references, property then value on
    the same line: `LAST<TAB>P735<TAB>Q629347<TAB>P1545<TAB>"1"<TAB>P7452<TAB>Q3409033`.
    """
    out, notes = [], []
    lines, why = statements_for(label, plan, geni_id, father_qid=father_qid,
                                fields=fields, sex=sex)
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

SPINE_PATH = "paths/charlemagne-to-arne-garborg.tsv"
RANDOM_PARENT_SETS = 4
RANDOM_FAMILIES = 4
RANDOM_COUPLES = 1


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


def compose(have, fam, rng):
    """`{geni_id: why}` -- the people this run creates, per `docs/batch-rules.md`.

    `have` is the ball: every Geni id we can already point at a Wikidata item.
    `fam` is `reports/derived-family.csv` keyed by Geni id.
    """
    def kin(g, col):
        return [x for x in re.split(r"[,;|]", (fam.get(g) or {}).get(col) or "")
                if x.strip() and x.strip() in fam]

    picked, why = {}, []

    # --- 1. the spine couple ------------------------------------------------------
    # Emma chose "the chain person plus their spouse" over "both parents of the chain
    # person", so one run advances the line by exactly one step and brings the
    # off-chain partner with it.
    for step, gid, name in spine_chain():
        if gid in have:
            continue
        picked[gid] = f"spine step {step}"
        for sp in kin(gid, "spouses"):
            if sp not in have:
                picked.setdefault(sp, f"spouse of spine step {step}")
        why.append(f"1. spine step {step}: {name} + {len(kin(gid, 'spouses'))} spouse(s)")
        break
    else:
        why.append("1. spine: every step already has an item")

    # --- 2. four random sets of parents, drawn from the ball ----------------------
    # "We always make both parents, if both parents exist, as a part of the generation."
    # A candidate is somebody in the ball at least one of whose parents we could create.
    cands = sorted(g for g in have
                   if any(p not in have for p in kin(g, "father") + kin(g, "mother")))
    rng.shuffle(cands)
    n = 0
    for g in cands:
        if n >= RANDOM_PARENT_SETS:
            break
        new = [p for p in kin(g, "father") + kin(g, "mother") if p not in have]
        if not new:
            continue
        for p in new:
            picked.setdefault(p, f"parent of {g}")
        n += 1
    why.append(f"2. {n}/{RANDOM_PARENT_SETS} random parent sets")

    # --- 3. four random families off a SOLITARY individual ------------------------
    # An item with no spouse and no child on it. Our own creations qualify, which is
    # her instruction and also the only reason this component is not starved: almost
    # nothing in the ball has family statements yet.
    solo = sorted(g for g in have
                  if not any(x in have for x in kin(g, "spouses") + kin(g, "children"))
                  and (kin(g, "spouses") or kin(g, "children")))
    rng.shuffle(solo)
    n = 0
    for g in solo:
        if n >= RANDOM_FAMILIES:
            break
        new = [x for x in kin(g, "spouses") + kin(g, "children") if x not in have]
        if not new:
            continue
        for x in new:
            picked.setdefault(x, f"family of solitary {g}")
        n += 1
    why.append(f"3. {n}/{RANDOM_FAMILIES} random families off a solitary individual")

    # --- 4. one random existing couple, all their children ------------------------
    couples = sorted({(g, sp) for g in have for sp in kin(g, "spouses")
                      if sp in have and g < sp})
    rng.shuffle(couples)
    n = 0
    for a, b in couples:
        if n >= RANDOM_COUPLES:
            break
        kids = [k for k in set(kin(a, "children")) | set(kin(b, "children"))
                if k not in have]
        if not kids:
            continue
        for k in kids:
            picked.setdefault(k, f"child of existing couple {a}+{b}")
        n += 1
        why.append(f"4. couple {a}+{b}: {len(kids)} children")
    if not n:
        why.append("4. no existing couple in the ball has an uncreated child")

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
    ap.add_argument("--seed", type=int, default=0, metavar="N",
                    help="seed for --compose, so a run is reproducible.")
    ap.add_argument("--limit", type=int, default=0, metavar="N",
                    help="create only the N people closest to Arne (0 = no limit)")
    args = ap.parse_args()

    have = ledger()
    for path in args.known:
        with open(path, encoding="utf-8") as f:
            head = f.readline()
            f.seek(0)
            rd = csv.DictReader(f, delimiter="\t" if "\t" in head else ",")
            n = 0
            for row in rd:
                g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
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
        picked, why = compose(have, fam_rows, rng)
        # Everyone an earlier batch TODAY already creates. The ledger only catches up once
        # Emma has run the file, so within a single day this is the only thing that keeps
        # two batches disjoint.
        already = set()
        for path in args.exclude:
            text = Path(path).read_text(encoding="utf-8")
            already |= set(re.findall(r'P2600	"(\d+)"', text))
        if already:
            drop = [g for g in picked if g in already]
            for g in drop:
                picked.pop(g)
            print(f"--exclude: {len(already)} already created by an earlier batch today, "
                  f"{len(drop)} of them dropped from this one")
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

    ids = set(frontier) | set(have)
    facts, labels = {}, {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                facts[row["geni_id"]] = row
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = row["label_en"] or row["label_mul"]

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

    lines, carried = [], []
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
    lines += [
        "# 1. Everything missing from people who already have items -- the links that",
        "#    yesterday's creations made possible, and the properties never emitted.",
        "#    Every subject and every value already has a QID.",
        "",
    ]
    seen = set()

    def add(q, prop, value, g):
        if (q, prop, value) in seen:
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
            for line in name_lines(labels.get(g, ""), plan, g,
                                   have.get(dad) if dad else None)[0]:
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
    lines += ["# 2. The next ring. Each is linked only to items that already exist;",
              "#    links between two of these wait for tomorrow, when they have QIDs.",
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
            described = describe_all(g, facts, father, mother, labels, table)
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

            lines.append(f'LAST\tLen\t"{qs(primary)}"')
            lines.append(f'LAST\tLmul\t"{qs(primary)}"')
            if birth and qs(birth) != qs(primary):
                lines.append(f'LAST\tAen\t"{qs(birth)}"')
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
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in have:
                lines.append(f"LAST\t{prop}\t{have[target]}{ref(g)}")
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                lines.append(f"LAST\tP26\t{have[sp]}{ref(g)}")
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                lines.append(f"LAST\tP3373\t{have[sib]}{ref(g)}")
        for kid in sorted(children.get(g, ())):
            if kid in have:
                lines.append(f"LAST\tP40\t{have[kid]}{ref(g)}")

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
                fields=fields.get(g), sex=f["sex"])
            lines.extend(name_statements)
            # Aliases: the nickname, and the full name under a married surname. Emma
            # asked for these alongside the second `P734` *family name*.
            # An alias identical to the label is noise. Now that the married name is
            # the primary label, `aliases_for`'s married-full-name alias often
            # duplicates it exactly -- `Aen "Inger Kristoffersdatter"` sitting beside
            # `Len "Inger Kristoffersdatter"`. The birth-name alias is already emitted
            # with the labels above, so this carries only what those do not.
            # **Every alias gets BOTH `Aen` and `Amul`.** Emma, 2026-08-24: *"the married
            # name is the primary label and the birth name is amul"*, and on 2026-08-25,
            # looking at a built file: *"you seem to be getting Aen and Amul confused
            # again"*. She was right — this block wrote `Aen` alone, so the birth-name
            # alias reached `en` and never `mul`. The file she was looking at had **4
            # `Aen` and 1 `Amul`**. `mul` is the language-neutral label and an alias that
            # exists only in `en` is invisible to every other language.
            emitted = {qs(primary), qs(birth)}
            for alias in aliases_for(fields.get(g, {})):
                if qs(alias) and qs(alias) not in emitted:
                    lines.append(f'LAST	Aen	"{qs(alias)}"')
                    lines.append(f'LAST	Amul	"{qs(alias)}"')
                    emitted.add(qs(alias))
            for note in unresolved:
                carried.append((g, label, f"name item missing: {note}"))

        lines.append("")
        created += 1

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
