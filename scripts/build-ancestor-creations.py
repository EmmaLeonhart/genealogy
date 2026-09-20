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

Carrying a QID. Not the Arne subgraph test `build-garborg-day.py` uses for its ring: these are
the account owner's own ancestors, they are the universe's origin rather than candidates for
admission to it, and gating them on the subgraph would be circular.

## ⛔ CREATING SOMEBODY WIKIDATA ALREADY HAS IS THE POINT, NOT A DEFECT

Ruled 2026-09-17, and this is the whole design rather than a tolerated cost: *"the idea is that
duplicates are intended behaviour lol ... The reasoning here is specifically that adding all of
them may over time lead to other editors merging in the duplicates and that specifically is
likely gonna help with my brandenburg ancestry"*.

**The duplicate is the bait.** A new item carrying a `P2600` and a parent link sits next to an
existing unlinked item for the same person; other Wikidata editors notice the pair and merge
them, and **the merge is what does the entity resolution** — it brings their item's statements
and sitelinks together with our Geni id and our parent edge, on one item, without us having
identified anything. That is the zipper's job being done by other people, at their pace, for
free. `CLAUDE.md` § *the zipper merge* records that our own resolution *"is not doing that well"*;
this routes round it.

So the count of duplicates is not a number to drive down. Do not add a label-search gate, do not
route these to a review file, do not "improve" the eligibility test to avoid people who probably
already exist — avoiding them removes the mechanism. Measured on the first real run: of three
picks two existed unlinked (`Willa of Tuscany` as `Q2054995`, `Q60040644`, `Q4019888`;
`Sunifred I de Barcelona` as `Q1342360`), which is a good day rather than a bad one.

I asked whether to gate this before it was wired. That was the wrong question and the answer is
written here so nobody asks it again.

## ⛔ NO DESCRIPTIONS

`CLAUDE.md` § *NO descriptions and NO edit summaries, categorically* — the exception is name
items and these are people. `Den` is not emitted, however much a bare label looks unfinished.
"""
from __future__ import annotations

import collections
import csv
import datetime
import pathlib
import random
import re
import sys

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
    """
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
            # The CHILD must be in the universe and the PARENT must not be on Wikidata.
            if qid and not parent_qid and not parent.startswith(PLACEHOLDER_PREFIXES):
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
    lines.append('LAST\tP31\t%s\tS2600\t"%s"' % (HUMAN, parent_geni))
    lines.append('LAST\tP2600\t"%s"' % parent_geni)
    lines.append('LAST\tP21\t%s\tS2600\t"%s"' % (sex, parent_geni))
    # ⛔ `LAST` AS A VALUE, which `CLAUDE.md` says is valid: only two items created in ONE batch
    # cannot point at each other. The child already exists, so this is safe.
    lines.append("#   %s: %s = the item just created" % (child_qid, prop))
    lines.append('%s\t%s\tLAST\tS2600\t"%s"' % (child_qid, prop, child_geni))
    return lines


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
