"""The name items the Garborg batches need and Wikidata does not have.

    python scripts/build-garborg-name-items.py

Emma, 2026-08-24: *"we should be modelling the names properly, which he didn't
do."* `P735` given name, `P734` family name and `P5056` patronym all point at
**items**, and a link cannot be written before the item exists.

**A patronymic is its own item even when the spelling already exists.**
`CLAUDE.md` § *One name item per USAGE*: `Eivindsen` has a Wikidata item as a given
name, and the patronymic `Eivindsen` is *"a different object"*. Her own `Q141152710`
*Aadnesson* is the pattern — labels, `P31` → `Q110874` *patronymic*, and nothing else.
That minimalism is copied deliberately: the measurement in `CLAUDE.md` found `P1705`,
`P282` and `P407` on most existing patronymic items and **she does not add them**.

**Ambiguous tokens are never created.** Where `reports/name-item-plan.csv` says a
token already resolves to several items — `Marie`, `Olga`, `Anton` — creating one more
is the `Maria` failure that would have made a tenth. They are listed for Emma instead.

**It no longer runs first and on its own, because the limit it was built around is not
real.** This file said *"QuickStatements V1 cannot point at an item a `CREATE` in the same
batch has just minted"*, and that is the same false generalisation `CLAUDE.md` records for
relationship links: `LAST` **is** how you point at what was just created. What cannot be done
is having two items created in one run cite *each other*. A name item and a person who already
exists are not two new items.

**Emma, 2026-08-26:** *"For every missing name the daily quickstatements generation should
generate the ones for existing items and in the generation run add it to the existing ones too
lol. Just like with people being linked on their relatives through QID PID LAST inverted of the
creation property setting LAST PID QID."*

So each `CREATE` is followed immediately by the statements that use it:

    CREATE
    LAST    Len     "Mjolhus"          <- the name item
    LAST    P31     Q101352
    Q141152600  P734  LAST  S2600 "…"  <- every EXISTING bearer, in the same run

The bearers are the people in `reports/garborg-qids.tsv` who already hold a QID; a person the
day batch is *creating* still cannot be linked here, because `LAST` would then name the person
rather than the name item. Those wait for the next run, which is the ordinary carry-forward and
not a gate.

Writes `reports/wikidata-garborg-name-items.txt`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import (  # noqa: E402
    PATRONYMIC_CLASS, classify_fields, load_plan, statements_for, store_name_item)
from live_name_items import (LookupUnavailable,                   # noqa: E402
                              existing_item as live_existing_item)
from qscomment import annotate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items.
INSTANCE_OF = "P31"
FAMILY_NAME_CLASS = "Q101352"     # family name
GIVEN_NAME_CLASS = "Q202444"      # given name

#: **3 name items a run while the hold is on; 10 after it lifts.**
#:
#: The original cap is Emma's, 2026-08-26: *"generating 10 name items based upon the missing
#: name items from the ideal state, with the links as a thing that specifically is made."*
#: WHICH ones is not specified, so the most-borne tokens go first -- that maximises the links
#: each created item earns in the same run. Rejected: taking them at random, which would leave
#: a nine-bearer surname waiting behind a one-bearer one for no reason. Falsified if she says
#: the choice should be random, as the parent pairs are.
#:
#: **The reduction is hers too, 2026-08-30**, asked directly and answered *"Cut it to 2-3 a
#: day"*. Her decision of 2026-08-30: name-item creation is
#: the highest-risk operation in the pipeline, because the duplicates another editor merged
#: were name items and the people side has no comparable audience. Three keeps the vocabulary
#: growing while staying well under the rate that produced them.
#:
#: **It restores itself.** The reduction is tied to the `OBender12` hold, so it lifts on the
#: same date rather than needing to be remembered -- the same reasoning as `held_items()` in
#: `build-garborg-day.py`, and for the same reason: a limit that must be remembered to be
#: lifted is a limit that never lifts.
NAME_ITEMS_PER_RUN_HELD = 3
NAME_ITEMS_PER_RUN_NORMAL = 10

#: Kept in step with `build-garborg-day.OBENDER_HOLD_EXPIRES`; `tests/test_obender_hold.py`
#: fails if the two dates drift apart.
NAME_ITEM_HOLD_EXPIRES = datetime.date(2026, 9, 30)

NAME_ITEMS_PER_RUN = (NAME_ITEMS_PER_RUN_HELD
                      if datetime.date.today() < NAME_ITEM_HOLD_EXPIRES
                      else NAME_ITEMS_PER_RUN_NORMAL)

CLASS_FOR = {
    "patronymic": PATRONYMIC_CLASS,
    "family": FAMILY_NAME_CLASS,
    "given": GIVEN_NAME_CLASS,
}

#: **The English description each kind of name item carries**, and it is the one exception to
#: `CLAUDE.md` § *NO descriptions and NO edit summaries*.
#:
#: Emma, 2026-09-01: *"All patronymics get the description 'patronymic' so that they actually are
#: properly deduplicated. We are still creating duplicate patronymics and it is at the point of
#: intolerability."* Then: *"All surnames get 'family name', all matronymics (do we even have
#: any) get 'matronymic'."*
#:
#: **The description is what makes WIKIDATA ITSELF refuse the duplicate.** A label and description
#: must be unique together per language, so two undescribed `Olsdatter` items are both legal while
#: a second `Olsdatter` + `patronymic` is refused at creation. That is the same uniqueness
#: constraint § *NO descriptions* calls *"by far the worst trap"* -- turned round and pointed at
#: the problem.
#:
#: **`matronymic` currently fires for nothing, and that answers her question.** The classifier
#: produces three usages -- `given` 11,515, `family` 9,799, `patronymic` 1,677 -- and matronymic
#: is not among them: a `-datter` token is classified `patronymic` whether or not it names a
#: mother. `P5056` is *patronym or matronym*, one property for both. The entry is here so that a
#: classifier that learns the distinction needs no second change.
#:
#: **`given` is deliberately absent.** She named patronymics, surnames and matronymics. A given
#: name is not obviously one description -- Wikidata distinguishes male, female and unisex given
#: names -- so guessing one would be inventing a description she has not asked for, which is what
#: the rule this overrides exists to prevent.
DESCRIPTION_FOR = {
    "patronymic": "patronymic",
    "family": "family name",
    "matronymic": "matronymic",
}

#: The live day batch. The earlier `wikidata-garborg.qs` and `-hop2.qs` were retired
#: on 2026-08-24: their creations are recorded in `reports/garborg-qids.tsv` and
#: re-running them would mint duplicates, which
#: `test_no_two_batches_create_the_same_person` caught.
BATCHES = ["reports/wikidata-garborg-day.txt"]


def people_in_batches():
    ids = set()
    for rel in BATCHES:
        path = ROOT / rel
        if path.exists():
            ids |= set(re.findall(r'P2600\t"(\d+)"',
                                  path.read_text(encoding="utf-8")))
    return ids


def ledger():
    """The people who ALREADY hold a QID -- the only ones a `LAST` statement can name."""
    out = {}
    path = ROOT / "reports" / "garborg-qids.tsv"
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="	"):
            if (row.get("qid") or "").startswith("Q") and (row.get("geni_id") or "").isdigit():
                out[row["geni_id"]] = row["qid"]
    return out


#: The property a name item of each usage hangs off the PERSON by.
PROP_FOR = {"given": "P735", "family": "P734", "patronymic": "P5056"}


def live_values():
    """`(qid, property) -> {values}` from `reports/garborg-live-values.tsv`.

    That file is a LIVE read of her items and is refreshed by the same run that builds the
    batch, so it is the freshest thing on disk -- fresher than the offline store download and
    fresher than `created-name-items.tsv`.
    """
    out = collections.defaultdict(set)
    path = ROOT / "reports" / "garborg-live-values.tsv"
    if not path.exists():
        return out
    with open(path, encoding="utf-8") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) >= 3 and row[0].startswith("Q"):
                out[(row[0], row[1])].add(row[2].strip())
    return out


def reuse_from_bearers(fields, have, live):
    """`(token, usage) -> qid` the token's OWN bearers already point at on Wikidata.

    **This is the source that catches what the other three miss, and the case that named it is
    `Kristiansen`.** On 2026-09-04 the batch emitted a `CREATE` for it while THREE of its four
    bearers already carried `P5056` -> `Q141267893`; QuickStatements refused the duplicate on the
    `patronymic` description, exactly as Emma designed it to. But a refused `CREATE` is not free:
    every following line in that block resolves `LAST`, so all four `P5056` statements, their
    `P144` qualifiers and their `P2600` sources died with it -- "No last item available", six
    rows lost per refusal.

    The offline store is a download that predates the item, `created-name-items.tsv` is 19 rows,
    and the live `wbsearchentities` needs a network the runner may not have. The bearers' own
    statements need nothing: the answer was already sitting in a file this run had just written.

    **Attribution has to be unambiguous or nothing is reused.** A person with two given names and
    one `P735` cannot tell you WHICH token that item is, so a bearer counts only when they carry
    exactly one token of the usage and exactly one value for its property. A chained patronymic
    (three `P5056`) is therefore skipped rather than guessed, which is `CLAUDE.md`
    § *One name item per USAGE* holding: an ambiguity is left, never resolved by a coin flip.
    """
    by_token = collections.defaultdict(list)
    for geni_id, person in fields.items():
        qid = have.get(geni_id)
        if not qid:
            continue
        toks = [(t, "family" if u == "married" else u)
                for t, u, _ in classify_fields(**person)]
        counts = collections.Counter(u for _, u in toks)
        for token, usage in toks:
            if usage in PROP_FOR and counts[usage] == 1:
                by_token[(token, usage)].append(qid)
    out = {}
    for (token, usage), qids in by_token.items():
        prop = PROP_FOR[usage]
        seen = [live[(q, prop)] for q in qids if len(live.get((q, prop)) or ()) == 1]
        if seen and len(set.union(*seen)) == 1:
            out[(token, usage)] = next(iter(seen[0]))
    return out


def main():
    ids = people_in_batches()
    have = ledger()

    # **The father for a patronymic's `P144` comes from a WIDER map than the ledger.**
    # Emma, 2026-09-02: *"Patronymics are not getting the names they come from in the logic lol
    # that's actually essential to the real specified algorithm."* The ledger is ~1,179 rows;
    # 518,855 Geni ids carry a `P2600` on Wikidata. Looking only in the ledger meant `P144`
    # fired only where she had made the father herself.
    #
    # The correspondence union is deliberately NOT consulted: it is 568,535 wide and includes
    # zipper-inferred pairs measured at 2.8-4.8% error, and a wrong `P144` asserts that this
    # patronymic derives from THAT man -- a false claim about a named person, not a mis-ranking.
    any_item = {}
    _p2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if _p2600.exists():
        with open(_p2600, encoding="utf-8") as _f:
            for _row in csv.reader(_f, delimiter="	"):
                if len(_row) >= 2 and _row[0].startswith("Q") and _row[1].strip().isdigit():
                    any_item.setdefault(_row[1].strip(), _row[0])

    def father_item(dad):
        return (have.get(dad) or any_item.get(dad)) if dad else None
    print(f"{len(ids)} people across {len(BATCHES)} Garborg batches, "
          f"{len(have)} already holding a QID")
    # The token scan covers BOTH populations: the people being created (so the item
    # exists by the time they are linked on a later day) and the people who already
    # hold a QID (so they are linked in this very run).
    ids = ids | set(have)

    # **The GEDCOM name FIELDS, not the rendered label.** Emma, 2026-08-24, caught the
    # name model re-parsing a display string; this file was still doing it after the
    # model was fixed, which mattered more here than anywhere else. It gates every
    # other batch, so a wrong list means she creates items nobody needs and lacks ones
    # that are needed: nicknames stopped needing an item at all (`P1449` takes text)
    # and married surnames started needing one.
    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm")}

    labels_of, father_of, sex_of = {}, {}, {}
    # **The family pass runs FIRST so the father's LABEL can be loaded in the same
    # sweep as everyone else's.** `namemodel.patronymic_or_surname` needs the father's
    # NAME, not his QID: without it every `-sen`/`-son`/`-datter` token falls through
    # to `"patronymic"`, which is how `Fersen` -- a Baltic-German family name -- was
    # created twice as an item whose `P31` reads `Q110874` *patronymic*
    # (`Q141223488`, and `Q141223718` merged into it). Emma, 2026-08-30: *"both just
    # completely erroneous"*. `reports/audit-q141223488.md` is the audit.
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                # ` | ` is the repo's multi-value separator and the strip is load-bearing.
                first = [x.strip() for x in (row.get("father") or "").split("|") if x.strip()]
                if first:
                    father_of[row["geni_id"]] = first[0]
    # The fathers are wanted for their labels alone and are NOT added to `ids`, which
    # decides who gets an item.
    wanted_labels = ids | set(father_of.values())
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted_labels:
                labels_of[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                sex_of[row["geni_id"]] = row.get("sex", "")

    # `classify_fields(**person)` reads `father_name`, so it has to be in the dict.
    for geni_id, person in fields.items():
        dad = father_of.get(geni_id)
        person["father_name"] = labels_of.get(dad, "") if dad else ""

    plan = load_plan()
    need = collections.Counter()
    ambiguous = collections.Counter()
    linked = collections.Counter()
    live_rescues = []
    bearer_rescues = []
    unavailable = []
    bearer_reuse = reuse_from_bearers(fields, have, live_values())
    if bearer_reuse:
        print(f"{len(bearer_reuse)} token(s) are already pointed at by their own bearers")
    for person in fields.values():
        for token, usage, _ordinal in classify_fields(**person):
            # A nickname is monolingual text on the person's own item, so it needs no
            # name item and must not be proposed as one.
            if usage == "nickname":
                continue
            # **A particle and an unknown-name marker are never items.** `CLAUDE.md`
            # § *A parenthesised token in `SURN`/`_MARNM`*: `de`, `von`, `af` belong in the
            # `mul` label, and `(anonyma)` is an NN marker. `CLASS_FOR` has no entry for
            # either, so one reaching the emit loop is a `KeyError` -- which is how this was
            # found, rather than by a wrong item being created.
            if usage in ("particle", "unknown"):
                continue
            # A married surname is a family name like any other -- same item kind, same
            # lookup -- it just reaches the person by a different field.
            usage = "family" if usage == "married" else usage
            qid, action = plan.get((token, usage), ("", "not in the plan"))
            # **Ask the store before creating anything.** A token missing from the plan used
            # to fall straight through to `need`, and `Ronneberg` is exactly that: not in
            # `name-item-plan.csv`, already `Q37504456` on Wikidata, created by Emma once and
            # merged away by another editor. Five of the ten name items she has ever created
            # went the same way -- Tunheim, Ronneberg, Bø, Heigre, Nyvold.
            if not qid:
                qid = store_name_item(token, usage)
                if qid:
                    action = "link (already on Wikidata)"
            # **Then ask Wikidata LIVE, because both offline sources are snapshots.** Emma,
            # 2026-09-01: *"I thought we reused name objects by default lol... Fuck you for
            # defaulting to the dangerous one lol."*
            #
            # `store_name_item` reads the offline download plus the 18-row
            # `created-name-items.tsv`. An item created since the download is invisible to
            # both, and `CREATE` never checks -- it mints a new one every time. Measured live
            # on 2026-09-01 against the three tokens this batch was about to create: `Voster`
            # was already `Q141244184`, `Olofsson` already `Q23645132`, and `Jonsson` already
            # existed THREE times. The batch would have made a fourth.
            #
            # Only an exact label match with the right `P31`, and SEVERAL qualifying items
            # means no answer -- that ambiguity is § *One name item per USAGE* and is hers.
            # **Then the bearers' OWN statements, before any network call.** See
            # `reuse_from_bearers`: this is the source that caught `Kristiansen`, and it costs
            # nothing because the file it reads was refreshed by this same run.
            if not qid:
                qid = bearer_reuse.get((token, usage), "")
                if qid:
                    action = "link (the bearers already point at it)"
                    bearer_rescues.append((token, usage, qid))
            if not qid:
                # **A lookup that could not RUN holds the token; it never falls through to
                # CREATE.** `live_existing_item` used to swallow every exception and return
                # `""`, which is the same value as "nothing exists" and sends the token
                # straight to creation -- so a 429, a timeout or a blocked proxy minted a
                # duplicate of something already on Wikidata, on the one path whose entire
                # job is to prevent that. Emma has had five merged away by another editor.
                try:
                    qid = live_existing_item(token, usage)
                except LookupUnavailable as exc:
                    unavailable.append((token, usage, str(exc)))
                    continue
                if qid:
                    action = "link (found live on Wikidata)"
                    live_rescues.append((token, usage, qid))
            if qid:
                linked[(token, usage)] += 1
            elif "AMBIG" in action.upper():
                ambiguous[(token, usage)] += 1
            else:
                need[(token, usage)] += 1

    # **Held, not created**, and reported loudly: a silent hold looks like a token that had
    # nothing to do, which is the failure this whole block exists against.
    if unavailable:
        print(f"⛔ {len(unavailable)} token(s) HELD -- the duplicate check could not run, so "
              f"creating them would risk a duplicate. They go out on a later day.")
        for token, usage, why in unavailable[:10]:
            print(f"   {token:<20} {usage:<12} {why[:70]}")

    print(f"{len(linked)} tokens already have an item and are linked, not created")
    print(f"{len(need)} need creating, {len(ambiguous)} are ambiguous and are not")
    if bearer_rescues:
        print(f"{len(bearer_rescues)} token(s) RESCUED by the bearers' own statements -- "
              f"these would have been created a second time:")
        for token, usage, q in sorted(set(bearer_rescues)):
            print(f"   {token:<20} {usage:<12} {q}")
    if live_rescues:
        print(f"{len(live_rescues)} token(s) RESCUED by the live check -- these would "
              f"have been created a second time:")
        for token, usage, qid in live_rescues:
            print(f"   {token:<20} {usage:<12} already {qid}")

    lines = [
        "# Name items the Garborg batches need, AND the statements that use them.",
        "#",
        "# Each CREATE is followed by `Qperson  Pprop  LAST` for every bearer who",
        "# ALREADY holds a QID -- LAST is exactly how you point at what was just",
        "# created. A person this run is also CREATING cannot be linked here, because",
        "# LAST would then name the person; they wait for the next run.",
        "#",
        "# A patronymic is its own item even where the spelling exists as a given",
        "# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is",
        "# the pattern -- labels, P31, nothing else.",
        "",
    ]
    ranked = sorted(need.items(), key=lambda kv: (-kv[1], kv[0]))
    held_back = ranked[NAME_ITEMS_PER_RUN:]
    linked_now = 0
    for (token, usage), bearers in ranked[:NAME_ITEMS_PER_RUN]:
        lines.append(f"# {token} -- {usage}, {bearers} bearer(s) in the batches")
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{token}"')
        lines.append(f'LAST\tLmul\t"{token}"')
        # **A PATRONYMIC carries a description, and it is the one exception to the hard rule.**
        # Emma, 2026-09-01: *"All patronymics get the description 'patronymic' so that they
        # actually are properly deduplicated. We are still creating duplicate patronymics and
        # it is at the point of intolerability."*
        #
        # `CLAUDE.md` § *NO descriptions and NO edit summaries* is categorical and this
        # overrides it for this one case, because the description is precisely what makes
        # WIKIDATA ITSELF refuse the duplicate. A label and description must be unique together
        # per language, so two undescribed `Olsdatter` items are both legal, while a second
        # `Olsdatter` + `patronymic` is REFUSED at creation.
        #
        # That is the same uniqueness constraint § *NO descriptions* warns can BLOCK a creation
        # -- her *"by far the worst trap"*. Here it is turned round and pointed at the problem:
        # the trap becomes the mechanism.
        if usage in DESCRIPTION_FOR:
            lines.append(f'LAST\tDen\t"{DESCRIPTION_FOR[usage]}"')
        lines.append(f"LAST\t{INSTANCE_OF}\t{CLASS_FOR[usage]}")
        # **The statements that use it, in the same run.** The name model is run with
        # this ONE token pointed at `LAST` and every other token left at its real QID,
        # so only the statement about the item just created comes back carrying `LAST`,
        # and it lands under that item's own `CREATE`.
        #
        # A person with several created names therefore gets one line in each of those
        # blocks, and those lines are TEXTUALLY IDENTICAL while meaning different things:
        # `Q141168787 P734 LAST` appears under *Tunheim*, *Bring* and *Iverson*. That is
        # correct and `tests/test_p2600_batches.py` had to learn it -- it already knew
        # `LAST` as a SUBJECT is scoped to its block and did not know the same of `LAST`
        # as a value.
        for geni_id, qid in sorted(have.items()):
            person = fields.get(geni_id)
            if not person:
                continue
            if not any(t == token and (u if u != "married" else "family") == usage
                       for t, u, _o in classify_fields(**person)):
                continue
            local = dict(plan)
            local[(token, usage)] = ("LAST", "created immediately above")
            if usage == "family":
                local[(token, "married")] = ("LAST", "created immediately above")
            dad = father_of.get(geni_id)
            try:
                sts, _notes = statements_for(
                    labels_of.get(geni_id, ""), local, geni_id,
                    father_qid=father_item(dad),
                    fields=person, sex=sex_of.get(geni_id, ""),
                    father_name=person.get("father_name", ""))
            except Exception as exc:                                   # noqa: BLE001
                lines.append(f"#   {qid}: the name model failed -- {exc}")
                continue
            for prop, value, quals in sts:
                if value != "LAST":
                    continue
                tail = "".join(f"\t{qp}\t{qv}" for qp, qv in quals)
                lines.append(f'{qid}\t{prop}\tLAST{tail}\tS2600\t"{geni_id}"')
                linked_now += 1
        lines.append("")

    if held_back:
        lines.append(f"# {len(held_back)} more name items are needed and wait for a later")
        lines.append(f"# run -- {NAME_ITEMS_PER_RUN} a day is her cap, not a limit of the data:")
        for (token, usage), n in held_back[:12]:
            lines.append(f"#   {token} ({usage}), {n} bearer(s)")
        if len(held_back) > 12:
            lines.append(f"#   ... and {len(held_back) - 12} more")
        lines.append("")

    if ambiguous:
        lines.append("# NOT created -- the plan says these already resolve to more than")
        lines.append("# one item, and creating another is the Maria failure that would")
        lines.append("# have made a tenth. Emma picks, the person's sex decides.")
        for (token, usage), bearers in sorted(ambiguous.items()):
            lines.append(f"#   {token} ({usage}), {bearers} bearer(s)")

    # A comment above every line, the same post-pass the day batch uses. Emma, 2026-08-26:
    # *"Every line has a comment the line above it saying what change is happening."*
    # `name_of` turns a QID back into the person it belongs to, so a link reads as a
    # sentence rather than as two numbers.
    # ---- descriptions on name items that ALREADY exist -----------------------------
    #
    # **Emma, 2026-09-02:** *"add an item at the end of the queue to make the generated
    # quickstatements add these descriptions to the patronymics and family names"*.
    #
    # The block above puts a description on every name item it CREATES, because label plus
    # description must be unique per language and that is what makes Wikidata refuse a second
    # `Olsdatter`. Items created before that rule went in have no description, so the guard does
    # not protect them -- and they are the ones most likely to be duplicated, being the ones
    # already in use.
    #
    # **A description is only ADDED, never replaced.** If the item already says something, that
    # is somebody's editorial choice and `CLAUDE.md` § *The purpose is to ADD to Wikidata, not
    # to correct it* governs.
    #
    # **This is name items only.** Descriptions on PEOPLE are the categorical ban, and confusing
    # the two cost a scare on 2026-09-02 when I deleted this mechanism over a description another
    # editor had put on a person.
    described = []
    want = {}
    for (token, usage), (existing, _action) in plan.items():
        q = (existing or "").strip()
        if q.startswith("Q") and usage in DESCRIPTION_FOR:
            want.setdefault(q, (token, usage))
    if want:
        ids = sorted(want)
        print("")
        print(f"checking {len(ids):,} existing name items for a missing description")
        missing = 0
        for k in range(0, len(ids), 50):
            chunk = ids[k:k + 50]
            try:
                data = get({"action": "wbgetentities", "format": "json",
                            "props": "descriptions", "languages": "en",
                            "ids": "|".join(chunk)}, ua)
            except Exception as exc:                                   # noqa: BLE001
                print(f"   chunk at {k} failed ({exc}); those items are left alone")
                continue
            for q, ent in (data.get("entities") or {}).items():
                if "missing" in ent or q not in want:
                    continue
                if (ent.get("descriptions") or {}).get("en"):
                    continue
                token, usage = want[q]
                missing += 1
                described.append(f'{q}	Den	"{DESCRIPTION_FOR[usage]}"')
        if described:
            lines.append("")
            lines.append("# " + "=" * 70)
            lines.append("# DESCRIPTIONS on name items that already exist and have none.")
            lines.append("# Label + description must be unique per language, so this is what")
            lines.append("# makes Wikidata refuse a duplicate of a name item already in use.")
            lines.append("# Name items only -- never people.")
            lines.append("# " + "=" * 70)
            lines.extend(described)
        print(f"   {missing:,} of them have no English description; "
              f"{len(ids) - missing:,} already do")

    qid_to_geni = {q: g for g, q in have.items()}
    lines = annotate(lines, lambda t: labels_of.get(qid_to_geni.get(t, t), ""))

    out = ROOT / "reports" / "wikidata-garborg-name-items.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {out.relative_to(ROOT)}: {lines.count('CREATE')} name items "
          f"(cap {NAME_ITEMS_PER_RUN}, {len(held_back)} carried to a later run), "
          f"{linked_now} statements linking an EXISTING person to one, in the same run")
    for (token, usage), n in sorted(need.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  create  {token:<20} {usage:<12} {n}")
    for (token, usage), n in sorted(ambiguous.items()):
        print(f"  AMBIG   {token:<20} {usage:<12} {n}")


if __name__ == "__main__":
    main()
