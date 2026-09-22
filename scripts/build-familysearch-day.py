"""QuickStatements for the FamilySearch corpus. A SEPARATE file, and duplicates are the design.

⛔ **Ruled 2026-09-21:** *"I want to have a pipeline that creates duplicates of familysearch vs
geni but we can manually merge it. Makes separate quickstatements."*

A FamilySearch person gets their own Wikidata item **even when a Geni person for the same human
already has one**. A human merges the pair afterwards on Wikidata, which is one click there and
leaves a redirect behind. That is not a defect this script should be preventing.

**Why, and it is measured rather than assumed.** The `P2889` bridge resolves **11 of 3,103**
people — 0.35% — so automated resolution cannot join these two trees
(`reports/familysearch-qid-bridge.tsv`, `scripts/bridge-familysearch-qids.py`). Withholding an
item until the join is proven means **3,092 people never enter Wikidata at all**. Creating both
and merging by hand is the stopgap `CLAUDE.md` § *THE PRACTICAL BARRIER: THE ZIPPER MERGE*
already describes, applied to a second source.

⛔ **THIS OVERRIDES THE ANTI-DUPLICATE REASONING FOR THIS PIPELINE ONLY.** `CLAUDE.md`
§ *DESCRIPTIONS ARE WRITTEN NOW, AND THE REASON IS THE DEDUPLICATION* exists to stop us
recreating **our own** items. It is not a reason to refuse a FamilySearch item beside a Geni
one. Descriptions are still written, and here they are what lets the person doing the merge see
the two items are the same human — the description works *for* the duplicate, not against it.

⛔ **AND `P2889` GOES ON EVERY ITEM THIS CREATES.** The FamilySearch id is the only identifier
these people have. An item created without it cannot be joined by anyone later, including the
person doing the merge — and it is what turns this pipeline into the bridge rather than a
consumer of one: the next `bridge-familysearch-qids.py` run resolves against the ids we
ourselves published, so the 11 grows on its own.

**The 11 that already join take statements, not a creation.** They hold `P2889` by construction
— that is how the bridge found them — so what they take here is the other direction of a
relationship to somebody this run creates: `Q… P40 LAST`. That is what attaches the new
component to Wikidata instead of leaving 2,975 items floating.

**The gates this obeys, none of them invented here:**

* ⛔ **CJK labels are an absolute prerequisite for creating an individual**, confirmed
  2026-08-31. `label_in` is the one choke point and it answers all-three-or-none; a person it
  cannot read is carried forward, not created without them. Measured over the first export:
  **2,984 of 3,103** names resolve against the existing table, and the 119 that do not are
  Polish tokens and unknown-name markers.
* ⛔ **An edit on an EXISTING item goes on an item in the universe or one step beyond it**,
  ruled 2026-09-17. `out/wikidata/edit-universe.json` is the gate and it is read here rather
  than trusted from the composer. All 11 bridge items are in the universe today; one that is
  not is refused and reported.
* ⛔ **A woman goes under her MAIDEN name; a man under his MARRIED name**, ruled 2026-09-21.
  FamilySearch writes the maiden form as the untyped `1 NAME` and the married one as
  `2 TYPE married` — 215 women and 33 men carry one — so the two sexes read opposite ends of
  the same pair of fields.
* ⛔ **A title is not a name.** `namemodel.drop_label_title`, the same call the other two
  emitters make. FamilySearch puts 601 of them in `NPFX` and more inside the name string.
* ⛔ **GEDCOM dates have a specification** — `genimerge.dates`, never a regex. What is added
  here is a *source-format normaliser*, not a second parser: FamilySearch writes free text in
  half a dozen languages (`about 1520`, `21 February 1572`, `omkring 1350`, `from 1500 to
  1520`), so the text is rewritten into GEDCOM tokens and `parse_date` remains the only thing
  that reads a date. Anything the normaliser does not recognise passes through unchanged and
  parses to nothing, which is the safe direction: a date we cannot read never becomes a date we
  guessed.

**Nothing here is folded into the daily batch.** Its own output, so the duplicates it creates
are reviewable and mergeable as a set rather than mixed into edits that are meant to be unique.
`wikidata-edits.yml` sends `reports/wikidata-garborg-day-auto.txt` and this file is not it.

Writes:

    reports/wikidata-familysearch-day.txt    the QuickStatements
    reports/familysearch-carry-forward.tsv   everyone NOT created, with the reason

Usage:
    python scripts/build-familysearch-day.py [--limit N] [<rendered.ged> ...]
"""
from __future__ import annotations

import argparse
import collections
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from genimerge.dates import parse_date                                  # noqa: E402
from datequals import date_quals                                        # noqa: E402
import descriptions                                                     # noqa: E402
import labels as labelmod                                               # noqa: E402
import namemodel                                                        # noqa: E402

CORPUS = ROOT / "exports" / "familysearch"
BRIDGE = ROOT / "reports" / "familysearch-qid-bridge.tsv"
UNIVERSE = ROOT / "out" / "wikidata" / "edit-universe.json"
OUT = ROOT / "reports" / "wikidata-familysearch-day.txt"
CARRY = ROOT / "reports" / "familysearch-carry-forward.tsv"

#: `P2889` FamilySearch person ID -- the identifier that makes a created item joinable.
FS_PROP = "P2889"


def garborg():
    """The daily builder, imported for its choke points rather than copied.

    `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* — there are two emitters and the
    rules live in one place. This is a third emitter, so it calls the same `label_in`,
    `life_description` and `qs` the others do instead of growing its own copies, which is how
    the generation-suffix rule went out wrong from one block for a day.

    The hyphen in the filename is why this is `importlib` rather than an `import` statement.
    """
    path = ROOT / "scripts" / "build-garborg-day.py"
    spec = importlib.util.spec_from_file_location("garborg_day", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- the GEDCOM

def records(text):
    """`[(xref, type, [lines])]` in file order. A record ends where the next `0` begins."""
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^0 @([^@]+)@ (\w+)", line)
        if m:
            cur = (m.group(1), m.group(2), [])
            out.append(cur)
        elif line.startswith("0 "):
            cur = None
        elif cur is not None:
            cur[2].append(line)
    return out


def _event(lines, tag):
    """`(date, place)` for the first `1 <tag>` block, either half possibly empty.

    A `1 DEAT` with nothing under it is 3,103 of 3,103 in the first export — `getmyancestors`
    writes it as a deceased flag — so an empty block yields two empty strings rather than
    being mistaken for a date.
    """
    date = place = ""
    inside = False
    for line in lines:
        if re.match(rf"^1 {tag}\b", line):
            inside = True
            continue
        if re.match(r"^1 ", line):
            if inside:
                break
            continue
        if not inside:
            continue
        m = re.match(r"^2 DATE (.+)$", line)
        if m and not date:
            date = m.group(1).strip()
        m = re.match(r"^2 PLAC (.+)$", line)
        if m and not place:
            place = m.group(1).strip()
    return date, place


def individual(xref, lines):
    """One `INDI`, reduced to the fields this batch emits.

    `names` keeps the GEDCOM type beside each string because the type is the whole of the
    maiden/married rule: FamilySearch writes the maiden form untyped and the married one as
    `TYPE married`, and reading them positionally would get 215 women backwards.
    """
    rec = {"xref": xref, "fs_id": "", "sex": "", "names": [], "famc": "", "fams": [],
           "birth_date": "", "birth_place": "", "death_date": "", "death_place": ""}
    pending = None
    for line in lines:
        m = re.match(r"^1 NAME ?(.*)$", line)
        if m:
            pending = [m.group(1), ""]
            rec["names"].append(pending)
            continue
        m = re.match(r"^2 TYPE (\S+)", line)
        if m and pending is not None:
            pending[1] = m.group(1).strip().lower()
            continue
        if re.match(r"^1 ", line):
            pending = None
        m = re.match(r"^1 SEX (\S+)", line)
        if m:
            rec["sex"] = m.group(1).strip()
        m = re.match(r"^1 _FSFTID (\S+)", line)
        if m:
            rec["fs_id"] = m.group(1).strip()
        m = re.match(r"^1 FAMC @([^@]+)@", line)
        if m:
            rec["famc"] = m.group(1)
        m = re.match(r"^1 FAMS @([^@]+)@", line)
        if m:
            rec["fams"].append(m.group(1))
    rec["birth_date"], rec["birth_place"] = _event(lines, "BIRT")
    rec["death_date"], rec["death_place"] = _event(lines, "DEAT")
    return rec


def family(lines):
    """`(husband, wife, [children])` for one `FAM`, as raw xrefs."""
    husb = wife = ""
    chil = []
    for line in lines:
        m = re.match(r"^1 HUSB @([^@]+)@", line)
        if m:
            husb = m.group(1)
        m = re.match(r"^1 WIFE @([^@]+)@", line)
        if m:
            wife = m.group(1)
        m = re.match(r"^1 CHIL @([^@]+)@", line)
        if m:
            chil.append(m.group(1))
    return husb, wife, chil


def read_corpus(paths):
    """`(people, father, mother, spouses, children)`, all keyed on a namespaced xref.

    **Each file gets its own xref namespace.** `getmyancestors` numbers from 1 in every export,
    so two files both hold `@IFS1@` and merging them on the xref would fuse two unrelated
    people — the same hazard `render-familysearch-gedcom.py` exists for, one level up. The
    join between files is `fs_id`, which is exact, and it happens in `build`.
    """
    people, fams = {}, {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        stem = path.stem
        for xref, kind, lines in records(text):
            key = f"{stem}:{xref}"
            if kind == "INDI":
                people[key] = individual(key, lines)
            elif kind == "FAM":
                husb, wife, chil = family(lines)
                fams[key] = (f"{stem}:{husb}" if husb else "",
                             f"{stem}:{wife}" if wife else "",
                             [f"{stem}:{c}" for c in chil])

    father, mother = {}, {}
    spouses = collections.defaultdict(set)
    children = collections.defaultdict(set)
    for husb, wife, chil in fams.values():
        if husb and wife:
            spouses[husb].add(wife)
            spouses[wife].add(husb)
        for kid in chil:
            if husb:
                father[kid] = husb
                children[husb].add(kid)
            if wife:
                mother[kid] = wife
                children[wife].add(kid)
    return people, father, mother, spouses, children


# --------------------------------------------------------------------------- dates

#: FamilySearch date text -> the GEDCOM token `genimerge.dates` specifies.
#:
#: **Built from a census of the file, not from imagination.** 5,666 `DATE` lines in
#: `MBW7-P7H-ancestors12-descendants2.ged` fall into 253 shapes; 42.7% are a bare year and the
#: next 50% are a modifier word in front of one, in Norwegian, Swedish, Polish, German, Spanish
#: or English. The foreign words are here because the source wrote them, not because a rule was
#: generalised: `omkring`, `rundt`, `um`, `około` and `aproximadamente` all mean *about*.
_MODIFIER_WORDS = {
    "abt": "ABT", "abt.": "ABT", "about": "ABT", "circa": "ABT", "cir": "ABT",
    "cir.": "ABT", "ca": "ABT", "ca.": "ABT", "c.": "ABT", "around": "ABT",
    "omkring": "ABT", "rundt": "ABT", "um": "ABT", "około": "ABT", "okolo": "ABT",
    "aproximadamente": "ABT", "cirka": "ABT", "estimated": "EST", "est": "EST",
    "after": "AFT", "efter": "AFT", "etter": "AFT", "nach": "AFT",
    "before": "BEF", "före": "BEF", "vor": "BEF", "antes": "BEF",
}

#: Month names as FamilySearch writes them, long and short, mapped to the GEDCOM abbreviation.
_MONTH_WORDS = {}
for _i, _long in enumerate(("January February March April May June July August September "
                            "October November December").split(), start=1):
    _abbr = _long[:3].upper()
    _MONTH_WORDS[_long.lower()] = _abbr
    _MONTH_WORDS[_long[:3].lower()] = _abbr
    _MONTH_WORDS[_long[:3].lower() + "."] = _abbr


def to_gedcom(raw):
    """FamilySearch free text -> a GEDCOM `DATE` string, or the text unchanged.

    ⛔ **This is a NORMALISER, not a parser.** `CLAUDE.md` § *GEDCOM dates have a
    specification — `genimerge.dates`, never a regex*: nothing here decides what a date
    *means*. It rewrites the source's spelling into the grammar and hands the result to
    `parse_date`, which stays the only thing that reads one. A word it does not know is left
    alone, `parse_date` then reports no structured value, and the date survives as raw text in
    the description — exactly what an unreadable Geni date does.

        about 1520          -> ABT 1520
        21 February 1572    -> 21 FEB 1572
        from 1500 to 1520   -> BET 1500 AND 1520
        omkring 1350        -> ABT 1350

    **`for` is deliberately NOT in the modifier table** although Swedish `för` means *before*:
    unaccented `for` is a word in half the languages in this file and the accented form is the
    one that means it.
    """
    text = " ".join((raw or "").split())
    if not text:
        return ""
    # `from X to Y` is a RANGE, and GEDCOM spells a range `BET x AND y`. Left as `FROM`,
    # `parse_date` reads the head as a modifier and then fails on `1500 TO 1520`, so the whole
    # date is lost -- 36 of them in the first export, plus 13 Swedish `från … till`.
    m = re.match(r"^(?:from|från|fra)\s+(.+?)\s+(?:to|till|til)\s+(.+)$", text, re.I)
    if m:
        return f"BET {to_gedcom(m.group(1))} AND {to_gedcom(m.group(2))}"
    out = []
    for token in text.split():
        low = token.casefold()
        if low in _MODIFIER_WORDS and not out:
            out.append(_MODIFIER_WORDS[low])
        elif low in _MONTH_WORDS:
            out.append(_MONTH_WORDS[low])
        else:
            out.append(token)
    return " ".join(out)


def date_row(raw):
    """`(gedcom_text, iso, precision, modifier, year_end)` for one FamilySearch date."""
    ged = to_gedcom(raw)
    d = parse_date(ged)
    if d.year is None:
        return ged, "", "", "", ""
    return (ged, d.iso() or "", str(d.precision or ""), d.modifier or "",
            str(d.year_end) if d.year_end is not None else "")


# --------------------------------------------------------------------------- labels

def name_plan(rec):
    """`(primary, aliases)` — the label this person goes under and the forms beside it.

    ⛔ **`CLAUDE.md`, ruled 2026-09-21: a woman goes under her MAIDEN name, a man under his
    MARRIED name.** FamilySearch writes the maiden form as the untyped `1 NAME` and the married
    one as `2 TYPE married`, so the two sexes read opposite ends of the same pair of fields:

        F   mul = the untyped NAME          the married form becomes an Amul
        M   mul = the TYPE married NAME     the birth form becomes an Amul
        U   mul = the untyped NAME          there is nothing to choose between

    `TYPE aka` — 733 of them — are aliases whichever way round the pair goes. Titles come out
    of every one of them through `namemodel.drop_label_title`, which is the same call the other
    two emitters make rather than a fourth copy of the rule.

    ⛔ **A MARKER IN THE SURNAME SLOT NEVER REACHES A LABEL**, and it did. `Maria /No name/` is
    the ruling of 2026-08-29 and `labels.drop_marker_surname` is the call; without it
    `Olav /N. N/` and `Ikke kjent` went out as somebody's name. The marker vocabulary is
    `labels`' and the two gaps this corpus found — `n. n` and `ikke kjent` — were filled there
    rather than worked around here, because a guard in one emitter is not a guard.

    ⛔ **A ONE-TOKEN ALIAS IS DROPPED.** It is a bare given name, a bare family name or a
    title, and none of the three names a person — `CLAUDE.md` § *A bare given name is not a
    label*. The FamilySearch `aka` slot is full of them: `Sysselmann` (an office), `Anna`,
    `Bolt`. The primary label is not subject to this; a genuine mononym keeps its label.
    """
    untyped = [n for n, t in rec["names"] if not t]
    married = [n for n, t in rec["names"] if t == "married"]
    aka = [n for n, t in rec["names"] if t == "aka"]

    def label(raw):
        # `labels_for` is the ROUTING call and `label_for` is the raw one. Using the raw one
        # here is what put `N. N. Harniktsdatter` and `Ikke kjent` in a label: a leading marker
        # is normalised to `NN <surname>` by `labels_for` and by nothing else, and the marker
        # vocabulary is only consulted on that path.
        mul = labelmod.labels_for(raw).get("mul", "")
        if not mul:
            return ""
        surn = labelmod.surname_of(raw)
        out = namemodel.drop_label_title(labelmod.drop_marker_surname(mul, surn))
        # ⛔ **A BARE GIVEN NAME IS NOT A LABEL**, ruled 2026-09-07: the farm name is the
        # surname, and where there is none the form is `Given NN`. `Olav /N. N/` loses its
        # marker surname just above and would otherwise go out as `Olav`. The marker goes back
        # where the unknown half is, normalised, and the builder then routes it to the
        # descriptive path like any other unnamed person.
        givn = " ".join((raw or "").split("/")[0].split())
        return labelmod.name_with_unknown_surname(out, givn, surn)

    birth = label(untyped[0]) if untyped else ""
    wed = label(married[0]) if married else ""
    if rec["sex"] == "M" and wed:
        primary, displaced = wed, birth
    else:
        primary, displaced = birth or wed, (wed if birth else "")

    seen = {primary.casefold()} if primary else set()
    aliases = []
    for cand in [displaced] + [label(a) for a in aka] + [label(u) for u in untyped[1:]]:
        # **An `NN <surname>` ALIAS is noise on a person who has a name.** That form is what
        # `mul` becomes for someone unnamed; hung on a named person as an alias it says *also
        # known as NN Toresdatter*, which names nobody. 24 of them come out of the `aka` slot.
        if labelmod.leads_with_a_marker(cand) or cand == labelmod.UNNAMED_MARKER:
            continue
        if cand and len(cand.split()) > 1 and cand.casefold() not in seen:
            seen.add(cand.casefold())
            aliases.append(cand)
    return primary, aliases


# --------------------------------------------------------------------------- the batch

def read_bridge():
    """`fs_id -> qid` for everyone `P2889` already resolves, from the committed bridge."""
    out = {}
    if not BRIDGE.exists():
        return out
    with open(BRIDGE, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            fs, qid = (row.get("fs_id") or "").strip(), (row.get("qid") or "").strip()
            if fs and qid.startswith("Q"):
                out[fs] = qid
    return out


def read_universe():
    """The QIDs an edit may land on: the universe and the ring one step beyond it.

    ⛔ Ruled 2026-09-17, and read HERE rather than taken on trust from whoever composed the
    batch — `CLAUDE.md`: *a gate that lives only in the composer is one stale artifact away
    from being no gate*. A missing file means no existing item is edited at all, which is the
    safe direction: the creations still go out and nothing lands on a stranger.
    """
    if not UNIVERSE.exists():
        return set()
    data = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    return set(data.get("universe") or ()) | set(data.get("one_step") or ())


def build(args):
    G = garborg()
    table = G.translit()
    qs = G.qs

    paths = ([Path(p) for p in args.gedcom] if args.gedcom
             else sorted(CORPUS.rglob("*.ged")))
    if not paths:
        sys.exit(f"no .ged under {CORPUS.relative_to(ROOT)}")

    people, father, mother, spouses, children = read_corpus(paths)
    bridge, universe = read_bridge(), read_universe()

    # `fs_id` is the primary key on this side, the way the Geni profile id is on the other.
    # Two exports of overlapping trees hold the same person twice and the first record wins,
    # for the same reason the Geni merge joins on an id: a second copy is the same human, not
    # a second one.
    by_fs, order = {}, []
    for rec in people.values():
        fs = rec["fs_id"]
        if fs and fs not in by_fs:
            by_fs[fs] = rec
            order.append(fs)
    qid_of_key = {key: bridge[rec["fs_id"]]
                  for key, rec in people.items() if bridge.get(rec["fs_id"])}

    lines, carried, created = [], [], 0
    lines += [
        "# ========================================================================",
        "# FAMILYSEARCH. A SEPARATE FILE, AND THE DUPLICATES ARE THE DESIGN.",
        "# Ruled 2026-09-21. A FamilySearch person gets their own item even where a",
        "# Geni person for the same human already has one; a human merges the pair on",
        "# Wikidata afterwards, which is one click there and leaves a redirect.",
        "#",
        f"# {FS_PROP} goes on every item created here -- it is the only identifier these",
        "# people have, and it is what lets the next bridge run resolve them. Without it",
        "# nobody, including the person doing the merge, can join the item to anything.",
        "# ========================================================================",
        "",
    ]

    for fs in order:
        rec = by_fs[fs]
        key = rec["xref"]
        if fs in bridge:
            carried.append((fs, "", f"already on Wikidata as {bridge[fs]}: takes "
                                    f"statements, not a creation"))
            continue
        primary, aliases = name_plan(rec)
        if not primary:
            # `labels.label_for` returns empty deliberately, and a caller that falls back to
            # the raw string reintroduces the `Private` labels it exists to stop.
            carried.append((fs, "", "no label: the name is a redaction or unknown marker"))
            continue
        if (primary == labelmod.UNNAMED_MARKER or labelmod.leads_with_a_marker(primary)
                or primary.split()[-1] == labelmod.UNNAMED_MARKER):
            # **Not a defect and not a drop.** `CLAUDE.md` § *Redacted people go in* — the
            # garborg emitter creates these with `NN <surname>` in `mul` and a relationship
            # phrase in every other language, built by `describe_all` out of the merged tree.
            # That machine is keyed on Geni ids and this corpus has none, so these people wait
            # for it rather than going out under a label that names nobody. Counted, named and
            # carried, never silently skipped.
            carried.append((fs, primary, "unnamed: needs the NN/describe treatment, which is "
                                         "keyed on the Geni tree"))
            continue
        primary = qs(primary)
        ja, zh, ko = G.label_in(primary, table)
        if not ja:
            # ⛔ THE GATE, confirmed 2026-08-31: no ja/zh/ko, no creation. 119 of 3,103 land
            # here on the first export -- Polish tokens the table has never seen, and
            # unknown-name markers `label_in` refuses on purpose.
            carried.append((fs, primary, "GATE: no ja/zh/ko label, so not created"))
            continue

        # ⛔ **EVERY ITEM GETS A DESCRIPTION, AND NO TWO OF OURS MAY MATCH.** Ruled 2026-09-21:
        # *"no description info means geni id referencing description not no description"* and
        # *"base it on the other id referencing descriptions"* — the other id being `P2889`.
        # 182 of these blocks used to carry no `Den` at all, which is the absence of the only
        # guard Wikibase offers against us duplicating our own items. `descriptions` holds the
        # rule; `deduplicate` below then settles the collisions between two descriptions that
        # are both present and identical.
        desc = G.life_description(
            {"birth_date_raw": to_gedcom(rec["birth_date"]),
             "death_date_raw": to_gedcom(rec["death_date"])},
            {"birth_place": rec["birth_place"], "death_place": rec["death_place"]})
        desc = desc or descriptions.id_description(FS_PROP, fs)

        block = ["CREATE",
                 f'LAST\tLmul\t"{primary}"',
                 f'LAST\tLen\t"{primary}"',
                 f'LAST\tDen\t"{qs(desc)}"']
        block += [f'LAST\tLja\t"{ja}"', f'LAST\tLzh\t"{zh}"', f'LAST\tLko\t"{ko}"']
        for alias in aliases:
            block.append(f'LAST\tAmul\t"{qs(alias)}"')
        block.append(f"LAST\tP31\t{G.HUMAN}")
        if rec["sex"] in G.SEX:
            block.append(f"LAST\tP21\t{G.SEX[rec['sex']]}")
        # ⛔ NOT OPTIONAL, AND IT IS THE POINT. An item created without this cannot be joined
        # by anyone later, including the person doing the merge it exists for.
        block.append(f'LAST\t{FS_PROP}\t"{fs}"')

        ref = f'\tS{FS_PROP[1:]}\t"{fs}"'
        for prop, raw in (("P569", rec["birth_date"]), ("P570", rec["death_date"])):
            _ged, iso, prec, mod, end = date_row(raw)
            if iso and prec:
                block.append(f"LAST\t{prop}\t{iso}/{prec}"
                             f"{date_quals(mod, iso, prec, end)}{ref}")

        # **Both directions, in the same run.** `LAST` is valid as a VALUE when the subject
        # already exists, so a relationship to one of the bridge items is emitted from the new
        # item AND back from the old one. That is what attaches this component to Wikidata
        # instead of leaving it floating; treating the reciprocal as impossible was an
        # invented limit on the Geni side and cost a whole corrective script.
        back = []
        for prop, target, other in (("P22", father.get(key), "P40"),
                                    ("P25", mother.get(key), "P40")):
            q = qid_of_key.get(target or "")
            if q and q in universe:
                block.append(f"LAST\t{prop}\t{q}{ref}")
                back.append((q, other))
        for sp in sorted(spouses.get(key, ())):
            q = qid_of_key.get(sp)
            if q and q in universe:
                block.append(f"LAST\tP26\t{q}{ref}")
                back.append((q, "P26"))
        for kid in sorted(children.get(key, ())):
            q = qid_of_key.get(kid)
            if q and q in universe:
                block.append(f"LAST\tP40\t{q}{ref}")
                back.append((q, "P22" if rec["sex"] == "M" else "P25"))
        for subject, prop in back:
            block.append(f"{subject}\t{prop}\tLAST{ref}")

        lines += block
        lines.append("")
        created += 1
        if args.limit and created >= args.limit:
            break

    # ⛔ THE LAST GUARD, over the ASSEMBLED file. Two people with the same name and the same
    # dates produce the same description, which is the commonest shape in a Scandinavian
    # corpus and is no guard at all -- Wikibase refuses a creation only on label AND
    # description TOGETHER, so an identical pair is a duplicate we make ourselves and then
    # have to merge by hand.
    collided = descriptions.deduplicate(lines, FS_PROP)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    # `newline="\n"` explicitly: on Windows the default translates to CRLF, and the garborg
    # batch beside it is written LF. One batch in each convention is how a line-based guard
    # starts matching in one file and not the other.
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    with open(CARRY, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["fs_id", "label", "reason"])
        w.writerows(carried)

    reasons = collections.Counter(r.split(":")[0] for _f, _l, r in carried)
    print(f"  {len(by_fs):,} distinct FamilySearch people over {len(paths)} file(s)")
    print(f"  {created:,} CREATE blocks")
    print(f"  {collided:,} descriptions collided and took their FamilySearch id")
    print(f"  {len(carried):,} carried forward, not created:")
    for reason, n in reasons.most_common():
        print(f"      {n:6,}  {reason}")
    for path in (OUT, CARRY):
        print(f"  -> {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("gedcom", nargs="*",
                    help="rendered FamilySearch GEDCOMs; "
                         "default: every .ged under exports/familysearch/")
    ap.add_argument("--limit", type=int, default=0, help="stop after N creations")
    return build(ap.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
