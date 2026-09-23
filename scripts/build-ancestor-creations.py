"""One parent a run, up the account owner's own ancestry, created on Wikidata.

    PYTHONPATH=src python scripts/build-ancestor-creations.py

Writes `reports/wikidata-ancestor-creations-auto.qs` (two creations, for the scheduled run) and
`reports/wikidata-ancestor-creations.qs` (four, for the QuickStatements half).

## What it does, and the words it was asked in

Ruled 2026-09-17: *"I want the cicd to automatically add one randomly selected eligible ancestor
of 6000000087535357291 to wikidata every time and the quickstatements to add 2 more in the same
way. Randomly selected eligible means adding a parent to the ancestors in the universe."*

So: walk the ancestry of `6000000087535357291` — the account owner — through the synoptic tree.
Keep the ancestors that are already **in the universe**, meaning they carry a QID. An ancestor is
**eligible** when the tree knows a parent for them that Wikidata does not have. That parent is
what gets created, and the existing child is pointed at it.

It climbs by construction: every creation gives an in-universe person a parent, so the new item
is itself in the universe next run and its own parents become eligible. The ancestry grows one
generation at a time without anybody choosing who.

## ⛔ RANDOM, BUT SEEDED ON THE DATE

`CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* is not a veto on randomness; it is a veto on the
same inputs giving different bytes. The daily batch is **regenerated several times a day** —
`pipeline.yml` runs on every push — and an unseeded choice would pick different people each time.
RAISED THE SAME DAY to two and four: *"Add 2 ancestors of mine everyday with the cicd and 4 in
the quickstatements"*. The 1:2 ratio is unchanged -- it is the share the daily batch is dealt
at -- and everything below about eligibility, the date seed and the refusals is untouched.

That is not "one a run": it is one per regeneration, several a day, and the receipt in
`wikidata-edit-run.py` cannot save us because each pick is a genuinely new person.

Seeding on the ISO date makes the choice stable for the whole day and different tomorrow, which
is what was asked for. Re-running the composer is then a no-op rather than a fourth creation.

## What counts as "in the universe"

⛔ **THIS SAID "CARRYING A QID" AND THAT PRODUCED THREE ISOLATES ON WIKIDATA.** It read: *"Not
the Arne subgraph test `build-garborg-day.py` uses for its ring: these are the account owner's
own ancestors, they are the universe's origin rather than candidates for admission to it, and
gating them on the subgraph would be circular."*

The argument is coherent and the outcome is not, because **the gate downstream does not share
it**. This script appends to the batch and `refuse_non_local` then drops every line whose
subject QID is outside `out/wikidata/edit-universe.json`. A creation here carries exactly ONE
relationship — `child_qid P22|P25 LAST` — so when the child is outside that artifact the link is
stripped and the `CREATE` is not, and the run mints a bare `instance of human` with nothing
pointing at it. `Q141529844`, `Q141529845` and `Q141529847` are live and are exactly that;
Emma found them with `Special:WhatLinksHere` on 2026-09-21.

So the test is now `qid in edit-universe.json`, the same artifact the gate reads. **102
candidates remain**, so the mechanism still climbs a generation at a time; it climbs through
people whose links will survive, which is the only kind of climb that was ever happening on
Wikidata's side.

It is not circular. The universe already contains the owner's QID-bearing ancestry — that is
what put 6,239 items in it — and every creation this makes joins it, so next run the new item
is inside and its own parents become eligible. The circularity the old note feared is the
mechanism working.

## ⛔ GENI ↔ WIKIDATA DUPLICATES ARE NOT INTENDED. FAMILYSEARCH IS THE EXCEPTION.

⛔ **Ruled again from the front of `queue.md` (Fix zipper merge stuff):** intentional duplicates
are for **FamilySearch only** — `scripts/build-familysearch-day.py`, a separate QuickStatements
file, where a human merges the pair afterwards. They are **not** for Geni versus Wikidata.

The 2026-09-17 note below this used to say the opposite for this emitter — that recreating
somebody Wikidata already has (Willa of Tuscany, Sunifred I de Barcelona, …) was *"the bait"*
for other editors to merge. That reading stretched the FamilySearch ruling onto Geni↔Wikidata
and is what put World Tree duplicates into the day batch. **It is reversed here.**

**What still stands from 2026-09-17:** climb the owner's contiguous Wikidata ancestry one parent
at a time. **What does not:** mint a second item next to an existing World Tree person.

`build-garborg-day.py` already refuses a creation when the Geni id is spoken for — `P2600` on
Wikidata, or an identification in `reports/synoptic-correspondence.tsv` (zipper + structural).
This script now reads the same two sources. Holding a creation costs a day; creating a
duplicate costs a manual merge on Wikidata. Prefer hold.

⛔ **Recreating OUR OWN item** (same Geni id already in `garborg-qids.tsv`) stays forbidden too —
that was never the bait case; see `ledger_geni_ids` below.

## ⛔ EVERY CREATION CARRIES A DESCRIPTION, AND THIS SECTION USED TO SAY THE OPPOSITE

It said *"`CLAUDE.md` § NO descriptions and NO edit summaries, categorically — the exception is
name items and these are people. `Den` is not emitted, however much a bare label looks
unfinished."* **That rule was reversed on 2026-09-19** — `CLAUDE.md` § *DESCRIPTIONS ARE WRITTEN
NOW, AND THE REASON IS THE DEDUPLICATION* — and this emitter went on obeying the dead one, so
every person it made went out with no description at all: **10 of them across the two files**,
`Margareta`, `Rotrude`, `Brigida Aslaksdatter`, exactly the commonplace labels that collide.

Ruled 2026-09-21: *"all individuals should have descriptions"*, and *"no description info means
geni id referencing description not no description"*. These people have a label and a Geni id
and nothing else — no dates are loaded here — so the description is the identifier,
`Geni <id>`, which is unique by construction. `scripts/descriptions.py` is the one authority.
"""
from __future__ import annotations

import collections
import csv
import datetime
import json
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import descriptions  # noqa: E402 -- the one description rule, shared with the other emitters

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
#: Two files, one per half, because the split runs BEFORE this appends -- the same shape as
#: the subject-named-as and relationship-sources passes in `pipeline.yml`. Splitting one file
#: afterwards would have to re-do the split's arithmetic in a second place.
OUT_AUTO = ROOT / "reports" / "wikidata-ancestor-creations-auto.qs"
OUT_MANUAL = ROOT / "reports" / "wikidata-ancestor-creations.qs"

#: The account owner. `CLAUDE.md` § *Always write the English label next to an ID*: this is the
#: viewer's own Geni profile, and § *the anchor protocol* warns that it is NOT Charlemagne.
OWNER = "6000000087535357291"

HUMAN = "Q5"               # instance of -> human
MALE = "Q6581097"          # sex or gender -> male
FEMALE = "Q6581072"        # sex or gender -> female

#: ⛔ TWO a day from the scheduled run, FOUR in the QuickStatements half. Raised from 1 and 2 on
#: 2026-09-17: *"Add 2 ancestors of mine everyday with the cicd and 4 in the quickstatements"*.
#: The ratio stays 1:2, the same share the daily batch is dealt at.
#: ⛔ **TEN A DAY. Ruled 2026-09-19** as one of the MANDATORY categories inside the 500-a-day
#: budget: *"10 of my ancestors plus the ancestral rings of the other people"*. Was 2 and 4.
#:
#: **The 1:2 split is preserved and the total is the ruled number**, so the scheduled run takes
#: a third and the QuickStatements half takes the rest -- 3 and 7. The ratio is the share the
#: daily batch is dealt at and was not what changed; only the size was. Ten does not divide by
#: three, so the remainder goes to the QuickStatements side, which is the half a person runs and
#: the half that is not subject to the bot account's creation cap.
AUTO_CREATIONS = 3
MANUAL_CREATIONS = 7

#: ⛔ A PLACEHOLDER PARENT IS OURS AND NEVER WIKIDATA'S. `CLAUDE.md` § *A sibling step gets a
#: placeholder parent in OUR TREE and never on Wikidata*. `build-family-candidates.py` writes
#: them with these prefixes; creating one as a human would mint a person who does not exist.
PLACEHOLDER_PREFIXES = ("9995", "9990")


def family():
    """`{geni_id: (qid, father, father_qid, mother, mother_qid)}` off the derived layer.

    Streamed and kept as plain tuples: the file is ~190 MB over 1.45 M people and this needs
    random access to walk upward.
    """
    path = FAMILY
    if not path.exists():
        gz = path.with_name(path.name + ".gz")
        if not gz.exists():
            raise SystemExit("%s is absent -- run pack-derived.py --unpack or rebuild the tree"
                             % path.relative_to(ROOT))
        import gzip
        fh = gzip.open(gz, "rt", encoding="utf-8", newline="")
    else:
        fh = path.open(encoding="utf-8", newline="")
    out = {}
    with fh:
        for row in csv.DictReader(fh):
            gid = (row.get("geni_id") or "").strip()
            if gid:
                out[gid] = ((row.get("qid") or "").strip(),
                            (row.get("father") or "").strip(),
                            (row.get("father_qid") or "").strip(),
                            (row.get("mother") or "").strip(),
                            (row.get("mother_qid") or "").strip())
    return out


def ledger_geni_ids():
    """Every Geni id this project already holds a QID for, from `reports/garborg-qids.tsv`.

    ⛔ **THE DERIVED LAYER'S `qid` COLUMN IS NOT THE LEDGER, AND TRUSTING IT MADE DUPLICATES.**
    `eligible()` calls a parent creatable when `parent_qid` is empty — but that column comes
    from `derived-family.csv`, which is rewritten only when the tree is rebuilt, while
    `garborg-qids.tsv` is refreshed every run. So a person we created last week still reads as
    having no QID here, and the picker creates them a second time.

    Found 2026-09-21 in CI: `6000000003378670599`, `6000000177945982827` and
    `6000000225709965832` are all in the ledger AND being created again in
    `wikidata-garborg-day.txt`. `6000000177945982827` is Jacob Knutson Skiftun, one of today's
    four ancestor creations.

    **Recreating our own item is never intended.** The Geni↔Wikidata bait doctrine above was
    reversed: FamilySearch is the only pipeline that may mint a deliberate parallel item.
    Recreating a Geni id we already hold a QID for is worse still — nobody is being merged into
    anything useful, and § *DESCRIPTIONS ARE WRITTEN NOW, AND THE REASON IS THE DEDUPLICATION*
    exists precisely to stop it.

    `bridge-familysearch-qids.geni_by_qid` folds the same two sources for the same reason.
    """
    path = ROOT / "reports" / "garborg-qids.tsv"
    if not path.exists():
        return set()
    out = set()
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="	"):
            gid = (row.get("geni_id") or "").strip()
            if gid:
                out.add(gid)
    return out


def spoken_for():
    """Geni ids that already have a Wikidata item — do NOT create them again.

    Same floor `build-garborg-day.py` uses before minting a person:

    * `out/wikidata/p2600-all.tsv` — Wikidata already carries `P2600` for them
    * `reports/synoptic-correspondence.tsv` — zipper / structural identification

    Missing files fail open only for that source (empty contribution), matching garborg: a
    missing correspondence simply cannot hold anyone. The ledger check stays separate and
    stricter.
    """
    out = {}
    p2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if p2600.exists():
        with p2600.open(encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh, delimiter="\t"):
                if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                    out.setdefault(row[1].strip(), row[0])
    corr = ROOT / "reports" / "synoptic-correspondence.tsv"
    if corr.exists():
        with corr.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
                if g and q.startswith("Q"):
                    out.setdefault(g, q)
    return out


def labels():
    """`{geni_id: mul label}`, which is the label a creation carries."""
    out = {}
    with (LABELS).open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) >= 3 and row[0].strip():
                out[row[0].strip()] = row[2].strip()
    return out


#: ⛔ **A LABEL THAT IS NOT A NAME MUST NOT BECOME AN ITEM.** The first run of this script
#: picked `6000000067045743836`, whose label is **`n`** — Geni's placeholder for a name nobody
#: recorded, the same `n n` that names the Seljuq matriarch in `CLAUDE.md`. Creating a human on
#: Wikidata labelled `n` is precisely the complaint `queue.md` already carries about non-name
#: items being generated as names.
#:
#: **And a bare `n` escapes both detectors this repo already has**, which is why the test is
#: restated here rather than imported: `build-name-alternatives-census.LOOKS_PLACEHOLDER` matches
#: `nn`, `n.n.` and `n n` but not a single `n`, and `build-name-classes.PLACEHOLDERS` holds
#: `"nn"` and `"n n"` and again not `"n"`.
#:
#: A creation with NO label is worse than none at all, so an unusable label is a REFUSAL rather
#: than a create-without-label: the person stays eligible for a later run, when a scrape or an
#: export may have given them a real name.
PLACEHOLDER_LABEL = re.compile(
    r"^\s*[\(\[<]?\s*(private|no\s*name|noname|unknown|unk|n|nn|n\.?\s*n\.?|"
    r"anonymous|anon|\?+|\.+|-+|_+|\*+|na|n/a)\s*[\)\]>]?\s*$",
    re.IGNORECASE,
)


def usable_label(label):
    """True when `label` is fit to be a Wikidata label for a human.

    Needs a letter in it, more than one character, and must not read as a placeholder.
    """
    v = (label or "").strip()
    if len(v) < 2:
        return False
    if PLACEHOLDER_LABEL.match(v):
        return False
    return any(ch.isalpha() for ch in v)


def _universe():
    """The QIDs an edit may land on: `out/wikidata/edit-universe.json`, universe plus ring.

    Read here as well as in the composer because this script appends to the batch AFTER the
    composer has run, and `CLAUDE.md` is explicit that a gate living in one place is one stale
    artifact away from being no gate. Missing file -> empty set -> nothing is eligible, which
    is the safe direction: no creation is better than an isolate.
    """
    path = ROOT / "out" / "wikidata" / "edit-universe.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("universe") or ()) | set(data.get("one_step") or ())


def eligible(fam):
    """`[(child_geni, child_qid, parent_geni, 'father'|'mother'), ...]`, in tree order.

    A QID-bearing ancestor, reachable from the owner THROUGH QID-bearing people only, whose
    parent the tree knows and Wikidata does not.

    ⛔ **THE WALK ONLY TRAVELS THROUGH PEOPLE WHO CARRY A QID, AND NOT DOING SO WAS A REAL
    DEFECT.** Ruled 2026-09-20: *"the create my ancestors stuff just creates random ancestors
    instead of creating connected ancestors ... disconnected ancestors are not even really able
    to come into anything."*

    The old walk enqueued EVERY parent regardless of QID, so it crossed long stretches of people
    Wikidata has never heard of and then fired wherever some distant QID-bearing person had a
    parent we lacked. The creation was linked -- `child_qid P22 LAST` is emitted either way --
    but linked to an item with **no Wikidata path back to the owner**, because the generations in
    between were never created. Connected on Geni, a free-floating pair on Wikidata.

    Restricting the queue to QID-bearing parents makes every pick an extension of the owner's
    CONTIGUOUS Wikidata ancestry: the child is reachable from the owner through items that all
    exist, so the new parent joins the same component rather than starting an island.

    This is the contiguity rule `build-garborg-day.priority_ancestor_ring` already uses -- *"the
    walk goes up THROUGH people who already hold a QID"* -- and nothing more. **It is not a
    ring**: the ring returns the whole boundary, this still returns candidates for a random pick
    of `AUTO_CREATIONS` + `MANUAL_CREATIONS`. *"I did not request a ring."*

    ⛔ **AND THE CHILD MUST BE IN THE EDIT UNIVERSE, WHICH THIS SAID AND DID NOT DO.** The line
    below reads *"The CHILD must be in the universe"* and tested `qid` — that the child is on
    Wikidata at all, which is a different and much larger set. The creation carries **exactly
    one** relationship, the reciprocal `child_qid P22|P25 LAST`, and `refuse_non_local` drops
    that line when the child is outside the universe. The `CREATE` above it is not dropped with
    it. So a pick outside the universe does not produce a linked item, it produces an **isolate**
    — a bare `instance of human` with a `P2600` and nothing pointing at it, which is what gets
    nominated for deletion.

    Three of them are live and Emma found them by hand on 2026-09-21: `Q141529844` Solveig
    Halfdansdatter off `Q2521523`, `Q141529845` Ogmund Torbergsson Giske off `Q12001101`,
    `Q141529847` Poppo von Berg-Schelklingen zu Roggenstein off `Q30301558`. None of those three
    children is in `edit-universe.json`; the fourth pick of the same run, off `Q141216494`,
    which is, kept its link and is fine. *"They become immediate entry points and fix the error
    that made them."*
    """
    allowed, held, taken = _universe(), ledger_geni_ids(), spoken_for()
    seen, queue, found = {OWNER}, collections.deque([OWNER]), []
    while queue:
        gid = queue.popleft()
        rec = fam.get(gid)
        if not rec:
            continue
        qid, father, father_qid, mother, mother_qid = rec
        for parent, parent_qid, role in ((father, father_qid, "father"),
                                         (mother, mother_qid, "mother")):
            if not parent:
                continue
            # ⛔ Only step THROUGH a parent who is already on Wikidata. A parent with no QID is
            # the frontier, not a road: walking past them is what produced islands.
            if parent_qid and parent not in seen:
                seen.add(parent)
                queue.append(parent)
            # The CHILD must be in the universe and the PARENT must not already be spoken for.
            # `qid in allowed`, not merely `qid`: see the docstring. An empty universe means
            # the artifact is missing, and then nothing is eligible -- failing closed, the same
            # choice every other reader of this file makes.
            #
            # ⛔ `parent not in taken`: Geni↔Wikidata duplicate safeguard. Same sources as
            # `build-garborg-day` — a P2600 or a zipper/structural correspondence means the
            # person already has an item. FamilySearch intentional duplicates live in a
            # different emitter; this one does not mint World Tree doubles.
            if (qid in allowed and not parent_qid and parent not in held
                    and parent not in taken
                    and not parent.startswith(PLACEHOLDER_PREFIXES)):
                found.append((gid, qid, parent, role))
    return found

def block(parent_geni, label, role, child_geni, child_qid):
    """One creation and the link from the child that made it eligible."""
    prop = "P22" if role == "father" else "P25"
    sex = MALE if role == "father" else FEMALE
    lines = [
        "#   %s: %s of %s (%s), created because the tree knows them and Wikidata does not"
        % (parent_geni, role, child_qid, child_geni),
        "CREATE",
    ]
    if label:
        # An empty label is left UNSET rather than written as "" -- `Len ""` sets a blank one.
        lines.append('LAST\tLen\t"%s"' % label)
        lines.append('LAST\tLmul\t"%s"' % label)
        # ⛔ **IMMEDIATELY AFTER THE LABEL, because QuickStatements applies a `CREATE` line by
        # line**: a `Den` written at the end of the block means the item is born label-only and
        # is fully furnished before the pair can be refused, which is how
        # `Anders Jørgensen Heier` came to exist twice.
        lines.append('LAST\tDen\t"%s"' % descriptions.id_description("P2600", parent_geni))
    lines.append('LAST\tP31\t%s\tS2600\t"%s"' % (HUMAN, parent_geni))
    lines.append('LAST\tP2600\t"%s"' % parent_geni)
    lines.append('LAST\tP21\t%s\tS2600\t"%s"' % (sex, parent_geni))
    # ⛔ `LAST` AS A VALUE, which `CLAUDE.md` says is valid: only two items created in ONE batch
    # cannot point at each other. The child already exists, so this is safe.
    lines.append("#   %s: %s = the item just created" % (child_qid, prop))
    lines.append('%s\t%s\tLAST\tS2600\t"%s"' % (child_qid, prop, child_geni))
    return lines


CARRY_FORWARD = ROOT / "reports" / "garborg-carry-forward.tsv"


def record_carried_surnames(picked, lab):
    """Append a carry row for every married surname these creations cannot link yet.

    ⛔ **THIS SCRIPT APPENDS PEOPLE THE NAME MACHINERY NEVER SAW, AND THE DROP WAS SILENT.**
    `pipeline.yml` runs `build-garborg-day.py --compose` -- which plans the name items and
    writes `garborg-carry-forward.tsv` -- and only then appends these creations to the batch.
    So a `_MARNM` on somebody picked here is neither linked, nor proposed as a name item, nor
    recorded as carried: the second `P734` *family name* is simply lost.

    `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done* has a sibling in the
    carry-forward's own rule -- a surname that cannot be linked today must be RECORDED as
    carried, never silently dropped. `tests/test_garborg_day_batch` asserts exactly that and
    failed on `Berg-Schelklingen`, `zu`, `Roggenstein` and `Skiftun` on 2026-09-21.

    Appending rather than rewriting, because the composer owns this file and has already
    finished with it by the time this runs. A missing input is skipped rather than guessed at:
    no name plan means nothing can be said about what is linkable.
    """
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        from namemodel import classify_fields, load_plan
    except Exception:                                                   # noqa: BLE001
        return
    names = ROOT / "reports" / "display-names.csv"
    if not names.exists() or not CARRY_FORWARD.exists():
        return
    wanted = {parent for _g, _q, parent, _r in picked}
    fields = {}
    with names.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            gid = (row.get("geni_id") or "").strip()
            if gid in wanted and gid not in fields:
                fields[gid] = {k: row.get(k, "") for k in ("givn", "surn", "nick", "marnm")}
    try:
        plan = load_plan()
    except Exception:                                                   # noqa: BLE001
        return
    rows = []
    for gid, person in sorted(fields.items()):
        for token, usage, _ordinal in classify_fields(**person):
            if usage != "married" or plan.get((token, "family"), ("", ""))[0]:
                continue
            rows.append((gid, lab.get(gid, ""),
                         "name item missing: %s (married): not in the plan, and this person "
                         "was appended after the composer wrote its own carries" % token))
    # **Idempotent, because the batch is regenerated several times a day.** `pipeline.yml` runs
    # on every push and the composer rewrites this file each time -- but a second run of THIS
    # script inside one pipeline pass, or a local re-run, would otherwise append the same rows
    # again. The seed makes the picks stable for the day, so the rows are stable too.
    existing = set()
    with CARRY_FORWARD.open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh, delimiter=chr(9)):
            if row:
                existing.add(tuple(row))
    rows = [r for r in rows if tuple(r) not in existing]
    if not rows:
        return
    with CARRY_FORWARD.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=chr(9), lineterminator=chr(10))
        w.writerows(rows)
    print("%d married surname(s) recorded as carried in %s"
          % (len(rows), CARRY_FORWARD.relative_to(ROOT)))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    fam = family()
    if OWNER not in fam:
        raise SystemExit("the owner %s is not in %s" % (OWNER, FAMILY.name))
    cand = eligible(fam)
    lab = labels()
    # ⛔ Refused, not created unlabelled: see `PLACEHOLDER_LABEL`.
    before = len(cand)
    cand = [c for c in cand if usable_label(lab.get(c[2], ""))]
    refused = before - len(cand)

    today = datetime.date.today()
    # Deterministic within the day; see the module docstring.
    rng = random.Random("ancestor-creations:%s" % today.isoformat())
    want = AUTO_CREATIONS + MANUAL_CREATIONS
    picked = rng.sample(cand, min(want, len(cand))) if cand else []

    def header(which, n):
        return ["# " + "=" * 72,
                "# ONE PARENT A RUN, UP THE ACCOUNT OWNER'S OWN ANCESTRY -- %s, %d creation(s)."
                % (which, n),
                "# %d eligible: an ancestor of %s who carries a QID and whose parent the tree"
                % (len(cand), OWNER),
                "# knows and Wikidata does not. Chosen at random, seeded on %s so the pick is"
                % today.isoformat(),
                "# stable for the day -- the batch is recomposed several times a day and an",
                "# unseeded choice would create a different person on each recomposition.",
                "# " + "=" * 72]

    auto_picks = picked[:AUTO_CREATIONS]
    manual_picks = picked[AUTO_CREATIONS:]
    for path, which, group in ((OUT_AUTO, "the scheduled run", auto_picks),
                               (OUT_MANUAL, "the QuickStatements half", manual_picks)):
        body = header(which, len(group))
        for child_geni, child_qid, parent_geni, role in group:
            body.extend(block(parent_geni, lab.get(parent_geni, ""), role,
                              child_geni, child_qid))
        path.parent.mkdir(parents=True, exist_ok=True)
        # An empty run writes an empty file rather than a header alone, so `[ -s ... ]` in
        # `pipeline.yml` skips it instead of appending a comment block to the batch.
        path.write_text(("\n".join(body) + "\n") if group else "",
                        encoding="utf-8", newline="\n")

    record_carried_surnames(picked, lab)

    print("%d people in the derived layer" % len(fam))
    print("%d eligible ancestor/parent pairs (%d refused for an unusable label)"
          % (len(cand), refused))
    print("picked %d (seed %s) -> %d auto, %d manual"
          % (len(picked), today.isoformat(), len(auto_picks), len(manual_picks)))
    for child_geni, child_qid, parent_geni, role in picked:
        print("   %s %s of %s  %s" % (parent_geni, role, child_qid,
                                      lab.get(parent_geni, "(no label)")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
