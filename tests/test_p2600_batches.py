"""The QuickStatements batches are the only files here that will edit Wikidata.

From 2026-09-01 the `.qs` files in `reports/` get pasted into QuickStatements, so a
malformed line is not a failed parse — it is a wrong statement on a real item, or a
silent no-op that looks like success. **Every** batch is guarded here, not just the
one that happened to be newest: on 2026-08-23 only `wikidata-geni-qid-p2600.qs` was
covered, and the unguarded `wikidata-garborg.qs` was found by reading to contain
`CREATE` lines that would have minted duplicate items for two people who already
existed.

What is checked, and why each one:

* **Line shape.** `CREATE`, or `<QID|LAST><TAB><property><TAB><value>` with optional
  reference pairs. Anything else is a line QuickStatements will reject or, worse,
  misread.
* **Balanced quotes.** QuickStatements V1 has no escape for a double quote inside a
  string, which already bit this project: nine Bureätten labels carried
  `Stine "Stena"` and would have ended the string early, shifting every field after it.
* **The reference form is `S2600`.** `docs/wikidata-item-template.md`, read off Emma's
  own items: the reference is the Geni ID itself, not `S854` *reference URL* plus
  `S813` *retrieved*. The old Garborg batch used the latter.
* **Geni ids are Geni ids** — digits, and parseable back out of a GEDCOM xref by
  `GENI_ID_RE`, the single place that knows the form.
* **No repeated statement, and no `CREATE` block without exactly one `P2600`.** A
  creation with no Geni ID is unciteable; one with two is a merge nobody asked for.
* **No two batches create the same person.** Cross-file, because each generator only
  sees its own output.

**What this cannot catch, stated so nobody trusts it further than it goes.** Whether
a `CREATE` would duplicate an item that already exists on Wikidata is only decidable
against a current `P2600` map. Ours (`out/wikidata/p2600-all.tsv`) is a snapshot, it
is gitignored, and it predates the Garborg items Emma created by hand — so the check
below **would not have caught the bug that prompted this file to be widened**. It
catches the ordinary case and skips when the snapshot is absent. The reliable guard
against that failure remains reading what exists before generating a creation.
"""
import csv
import re
from pathlib import Path

import pytest

from genimerge.identity import GENI_ID_RE

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"
P2600_SNAPSHOT = REPO / "out" / "wikidata" / "p2600-all.tsv"

#: Archived records of batches Emma has already run. They are history, not proposals, and
#: are never rewritten to satisfy a rule made after they went out.
#: `CLAUDE.md` § *`P3373` sibling is capped at 10 a day*. Mirrored rather than imported so
#: the guard does not pass merely because the builder lowered its own constant.
SIBLING_CAP = 10

SPENT_BATCHES = {
    "wikidata-garborg-day-1.qs": "the first day batch, 9 creations + 362 statements",
    "wikidata-garborg-day-2026-08-25-run.qs": "archived 2026-08-25 when the live file was rebuilt",
}

BATCHES = sorted(REPORTS.glob("*.qs"))
NAMES = [p.name for p in BATCHES]

#: `Q123` or `LAST`, a property, a value, then any number of reference pairs.
#: A leading `-` REMOVES the statement — QuickStatements V1 syntax, and the only way to
#: take a qualifier off a statement this project did not create. Matched explicitly
#: rather than by loosening the pattern, exactly as `en:"…"` monolingual values are.
STATEMENT = re.compile(
    r'^-?(?:Q[1-9][0-9]*|LAST)\t[A-Z][a-z]*[0-9]*\t[^\t]+(?:\t[SPQ][0-9a-z]*\t[^\t]+)*$'
)
P2600_LINE = re.compile(r'^(?:Q[1-9][0-9]*|LAST)\tP2600\t"([^"]*)"')
#: Narrower on purpose: only a `LAST` line belongs to the `CREATE` above it.
LAST_P2600 = re.compile(r'^LAST\tP2600\t"([^"]*)"')


def statements(path):
    """(line number, text) for every line that is not blank or a comment."""
    out = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        line = raw.rstrip("\r")
        if line.strip() and not line.lstrip().startswith("#"):
            out.append((i, line))
    return out


def creations(path):
    """The P2600 values of each CREATE block, in order."""
    blocks, current, inside = [], [], False
    for _i, line in statements(path):
        if line == "CREATE":
            if inside:
                blocks.append(current)
            current, inside = [], True
        elif inside:
            # Only a LAST line belongs to the CREATE above it. Matching a
            # `Q123<TAB>P2600` line here attributed the next explicit statement to
            # the previous block — found by
            # `test_the_creation_reader_finds_the_geni_id_of_each_block`.
            if not line.startswith("LAST\t"):
                blocks.append(current)
                current, inside = [], False
                continue
            m = LAST_P2600.match(line)
            if m:
                current.append(m.group(1))
    if inside:
        blocks.append(current)
    return blocks


pytestmark = pytest.mark.skipif(not BATCHES, reason="no .qs batches in reports/")


@pytest.mark.parametrize("name", NAMES)
def test_every_line_is_a_well_formed_quickstatements_line(name):
    path = REPORTS / name
    bad = [(i, ln) for i, ln in statements(path)
           if ln != "CREATE" and not STATEMENT.match(ln)]
    assert not bad, f"{name}: malformed lines — " + "; ".join(
        f"line {i}: {ln!r}" for i, ln in bad[:5])


def badly_quoted(line):
    """A quoted field must open and close and contain no quote of its own.

    Counting parity is not enough and misses the case this exists for:
    `LAST	Len	"Stine "Stena" Garborg"` has four quotes, an even number, and
    QuickStatements still ends the string at the second one. Check each field.
    """
    for field in line.split("	"):
        # A monolingual-text value is `en:"..."` -- the form `P1449` *nickname* and
        # every other monolingual property needs. It does not start with a quote and
        # is still correct, so it is matched explicitly rather than by loosening the
        # rule: the value inside must contain no quote at all, exactly as above.
        if re.fullmatch(r'[a-z]{2,3}(-[a-z]+)?:"[^"]*"', field):
            continue
        if field.startswith('"') and not re.fullmatch(r'"[^"]*"', field):
            return True
        if not field.startswith('"') and '"' in field:
            return True
    return False


@pytest.mark.parametrize("name", NAMES)
def test_no_line_carries_an_unescapable_quote(name):
    path = REPORTS / name
    bad = [(i, ln) for i, ln in statements(path) if badly_quoted(ln)]
    assert not bad, f"{name}: unusable quoting — " + "; ".join(
        f"line {i}: {ln!r}" for i, ln in bad[:5])


@pytest.mark.parametrize("name", NAMES)
def test_references_are_the_geni_id_not_a_url(name):
    """Her model: the reference is `P2600`. `S854` + `S813` is the old generator."""
    path = REPORTS / name
    bad = [(i, ln) for i, ln in statements(path) if "\tS854\t" in ln or "\tS813\t" in ln]
    assert not bad, (
        f"{name}: {len(bad)} statements cite a reference URL rather than the Geni id; "
        f"see docs/wikidata-item-template.md")


@pytest.mark.parametrize("name", NAMES)
def test_every_geni_id_is_one_this_repo_could_parse(name):
    path = REPORTS / name
    bad = []
    for i, ln in statements(path):
        for value in P2600_LINE.findall(ln):
            if not GENI_ID_RE.match(f"@I{value}@"):
                bad.append((i, value))
        for chunk in re.findall(r'\tS2600\t"([^"]*)"', ln):
            if not GENI_ID_RE.match(f"@I{chunk}@"):
                bad.append((i, chunk))
    assert not bad, f"{name}: not parseable as a Geni xref — " + "; ".join(
        f"line {i}: {g}" for i, g in bad[:5])


@pytest.mark.parametrize("name", NAMES)
def test_no_statement_is_repeated(name):
    """`LAST` lines are scoped to their own CREATE block, and that is the whole rule.

    A first cut compared every line against every other and failed on
    `wikidata-garborg.qs` for nine `LAST	P31	Q5` and `LAST	P21	Q6581097`
    lines. Those are not duplicates: `LAST` names whichever item the preceding
    `CREATE` minted, so identical text is a different subject each time. Repetition
    is a defect only where the subject is the same — an explicit QID across the file,
    or a line repeated inside one CREATE block.
    """
    path = REPORTS / name
    explicit, dupes = set(), []
    block, inside = set(), False
    for _i, ln in statements(path):
        if ln == "CREATE":
            block, inside = set(), True
            continue
        # `LAST` in EITHER position is scoped to the CREATE above it: as the subject
        # it names the new item, as a value it points at it.
        if (ln.startswith("LAST	") or "	LAST	" in ln
                or ln.endswith("	LAST")):
            if inside and ln in block:
                dupes.append(ln)
            block.add(ln)
            continue
        inside = False
        if ln in explicit:
            dupes.append(ln)
        explicit.add(ln)
    assert not dupes, f"{name}: {len(dupes)} repeated statements, e.g. {dupes[:2]}"


#: `P31` values that mean the created item is a NAME, not a person: family name,
#: given name, patronymic. `CLAUDE.md` § Wikidata properties and items.
NAME_CLASSES = {"Q101352", "Q202444", "Q110874", "Q12308941", "Q11879590", "Q3409032"}


def is_name_item(block_lines):
    return any(ln.split("	")[-1] in NAME_CLASSES for ln in block_lines
               if ln.startswith("LAST	P31	"))


def create_blocks(path):
    """Each CREATE block's lines, so a block can be judged on what it creates."""
    blocks, current, inside = [], [], False
    for _i, line in statements(path):
        if line == "CREATE":
            if inside:
                blocks.append(current)
            current, inside = [], True
        elif inside:
            if line.startswith("LAST	"):
                current.append(line)
            else:
                blocks.append(current)
                current, inside = [], False
    if inside:
        blocks.append(current)
    return blocks


@pytest.mark.parametrize("name", NAMES)
def test_every_created_person_carries_exactly_one_geni_id(name):
    """A created person with no `P2600` cannot be cited; with two it is a merge.

    **A created NAME is exempt, and the first version of this test was wrong about
    that.** It failed `wikidata-garborg-name-items.qs`, where every block is a family
    name, given name or patronymic — things that have no Geni profile because they are
    not people. `CLAUDE.md` § *One name item per USAGE* is the reason those items exist
    at all. The same distinction is `CREATIONS` in `tests/test_edit_graph.py`.
    """
    path = REPORTS / name
    bad = []
    for n, block in enumerate(create_blocks(path), 1):
        ids = [m.group(1) for ln in block
               for m in [LAST_P2600.match(ln)] if m]
        if is_name_item(block):
            if ids:
                bad.append((n, f"name item carrying P2600 {ids}"))
        elif len(ids) != 1:
            bad.append((n, f"{len(ids)} P2600 on a created person"))
    assert not bad, f"{name}: {bad[:5]}"


@pytest.mark.parametrize("name", NAMES)
def test_every_created_name_item_says_what_kind_of_name_it_is(name):
    """A name item with no `P31` is untyped, and nothing can tell given from family."""
    path = REPORTS / name
    bad = []
    for n, block in enumerate(create_blocks(path), 1):
        p31 = [ln for ln in block if ln.startswith("LAST	P31	")]
        if len(p31) != 1:
            bad.append((n, f"{len(p31)} P31 statements"))
    assert not bad, f"{name}: every CREATE needs exactly one P31 — {bad[:5]}"


def test_no_two_batches_create_the_same_person():
    """Each generator sees only its own output, so this is only visible across files.

    **Spent records are excluded, by name, for the reason they exist.** `SPENT_BATCHES`
    holds archived records of runs already made; nobody runs them again, so a person they
    name is not a person about to be created twice. Comparing them against a live batch
    asks the wrong question and answers it wrongly: on 2026-08-26 the live batch and
    `wikidata-garborg-day-1.qs` shared `6000000019384841547` *Martin Tollefson Tunheim*,
    and the ledger — refreshed from `Special:Contributions/日巫女` that minute, 0 rows
    added, so current — says he has **no item at all**. Day-1 was only partly run, which
    Emma said at the time: *"I only ran some of the quick statements because many of them
    required links that couldn't exist."*

    **What actually protects against a duplicate creation is the ledger**, plus
    `out/wikidata/p2600-all.tsv`, both consulted live inside `build-garborg-day.py`. This
    test protects against something narrower: two files a person could run today, both
    minting the same person.
    """
    owner = {}
    clashes = []
    for path in BATCHES:
        if path.name in SPENT_BATCHES:
            continue
        for ids in creations(path):
            for g in ids:
                if g in owner and owner[g] != path.name:
                    clashes.append((g, owner[g], path.name))
                owner[g] = path.name
    assert not clashes, f"the same person is created in two batches: {clashes[:5]}"


@pytest.mark.skipif(not P2600_SNAPSHOT.exists(),
                    reason="no local P2600 snapshot; this check is best-effort")
def test_no_creation_is_of_a_person_wikidata_already_links():
    """Best-effort only — read the module docstring before trusting it.

    The snapshot is not current, so this catches the ordinary case and would NOT
    have caught the Garborg duplicate, whose items were created after the dump.
    """
    known = set()
    with open(P2600_SNAPSHOT, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q"):
                known.add(row[1].strip())

    offenders = []
    for path in BATCHES:
        for ids in creations(path):
            for g in ids:
                if g in known:
                    offenders.append((path.name, g))
    assert not offenders, (
        "CREATE for a Geni id Wikidata already links — this would duplicate an "
        f"existing item: {offenders[:5]}")


# The checks above only prove today's batches are clean. These prove the checks
# would notice if they were not — the shape `test_repo_invariants.py` uses for its
# trigger reader, and the reason those exist.

@pytest.mark.parametrize("line", [
    'Q123\tP2600\t"6000000000000000001"',
    'LAST\tP31\tQ5',
    'Q467497\tP569\t+1851-01-25T00:00:00Z/11\tS2600\t"6000000003492005116"',
    'LAST\tLen\t"Samuel Eivindsen Garborg"',
])
def test_the_line_reader_accepts_a_real_statement(line):
    assert STATEMENT.match(line)


@pytest.mark.parametrize("line,why", [
    ('Q123 P2600 "6000000000000000001"', "spaces instead of tabs"),
    ('Q0123\tP2600\t"600000"', "QID with a leading zero"),
    ('123\tP2600\t"600000"', "no Q prefix and not LAST"),
    ('PREVIOUS\tP31\tQ5', "not a subject QuickStatements understands"),
    ('Q123\tP2600\t', "empty value"),
])
def test_the_line_reader_rejects_what_would_go_wrong(line, why):
    assert not STATEMENT.match(line), why


def test_the_quote_check_catches_the_bureatten_case(tmp_path):
    """`Stine "Stena"` ends the string early and shifts every field after it."""
    bad = tmp_path / "x.qs"
    bad.write_text('CREATE\nLAST\tLen\t"Stine "Stena" Garborg"\n', encoding="utf-8")
    offenders = [ln for _i, ln in statements(bad) if badly_quoted(ln)]
    assert offenders, "an embedded quote leaves an EVEN count; parity misses it"


def test_the_creation_reader_finds_the_geni_id_of_each_block(tmp_path):
    f = tmp_path / "x.qs"
    f.write_text(
        'CREATE\nLAST\tP31\tQ5\nLAST\tP2600\t"111"\n\n'
        'CREATE\nLAST\tP2600\t"222"\n\n'
        'Q9\tP2600\t"333"\n', encoding="utf-8")
    assert creations(f) == [["111"], ["222"]], "a non-CREATE P2600 must not be counted"


def test_the_creation_reader_notices_a_block_with_no_geni_id(tmp_path):
    f = tmp_path / "x.qs"
    f.write_text('CREATE\nLAST\tP31\tQ5\n', encoding="utf-8")
    assert creations(f) == [[]]


@pytest.mark.parametrize("name", NAMES)
def test_no_batch_ever_adds_an_english_alias(name):
    """`Aen` is never emitted. Emma, 2026-08-26.

    Her rule: *"married name is always the 'real' name and applied as the primary mul
    label (first amul added if applicable) and then the birth name is next as an amul.
    No aen are ever supposed to be added lol only ones in non-latin scripts get aliases
    for their birth names that are not in amul."*

    `mul` is the language-neutral label; an alias that exists only in `en` is invisible
    to every other language, which is the whole reason it never applies. The one
    exception is a **non-Latin** script -- `Aja`/`Azh` for a birth name that cannot live
    in `mul` -- and that is a different language code, so this test does not touch it.

    **The emitters got this wrong twice**, in opposite directions: `Aen` alone (so the
    birth-name alias reached `en` and never `mul`), then `Aen` *and* `Amul` together.
    Both passed every other guard in this file.

    A REMOVAL (`-Q123 Aen "..."`) is allowed and is how the wrong ones already on
    Wikidata come off: `reports/wikidata-garborg-label-fixes.qs` carries 13.

    **Two SPENT files are exempt and are named one at a time, never matched by a
    pattern.** They are archived records of batches Emma has already run -- 12 `Aen` in
    one, 3 in the other -- and rewriting a record of what was run would falsify it. The
    corrective batch removes those aliases from Wikidata instead. A pattern like
    `*-run.qs` would also exempt whatever a future run is named, which is the opposite
    of what this guard is for.
    """
    if name in SPENT_BATCHES:
        pytest.skip(f"{name} is a record of a batch already run; {SPENT_BATCHES[name]}")
    path = REPORTS / name
    bad = [(i, ln) for i, ln in statements(path)
           if not ln.startswith("-") and re.search(r"(?:^|\t)Aen\t", ln)]
    assert not bad, (
        f"{name}: adds an English alias, which no batch ever does — " + "; ".join(
            f"line {i}: {ln!r}" for i, ln in bad[:5]))


def test_the_sibling_cap_holds_across_every_live_batch():
    """`P3373` *sibling* is capped at 10 a day ACROSS BATCHES, not per file or per pass.

    `CLAUDE.md` § *`P3373` sibling is capped at 10 a day*: *"The cap is 10 `P3373` statements
    per day, across every batch, not per file. A builder emitting siblings must count them and
    stop."* Emma's reason is presentation, not correctness — *"siblin relationships are too
    numerous and imo come off as spammy"* — and sibling links grow as the SQUARE of a family,
    so one family of nine children is 72 statements on its own.

    **`build-garborg-day.py` had two emission sites and only one counted.** The additions pass
    drew on `sibling_budget_left()`; the block that emits relationships onto people being
    CREATED did not, so a run came out with 10 capped statements and **28 uncapped** — 38 in
    the file, in a batch whose entire reason for a cap is that 38 is too many. Nothing caught
    it because every other guard here is about line shape, not about volume.

    **Scope: the files one day's run produces.** The cap is *per day*, and `reports/` also
    holds batches built on other days plus one explicit overflow file
    (`wikidata-reciprocals-siblings-held.qs`, 155 statements deliberately parked). Asserting
    over every `.qs` on disk would either fail forever or force rewriting committed history,
    and neither is the rule. Scoped here to what `scripts/build-daily-batch.py` writes, which
    is exactly where the two-emission-sites bug lived.

    The others, so the exclusion is visible rather than silent: `wikidata-garborg-links.qs`
    106, `wikidata-reciprocals-siblings-held.qs` 155, `wikidata-join-izumo.qs` 30,
    `wikidata-reciprocals.qs` 10.
    """
    daily = {"wikidata-garborg-day.qs", "wikidata-garborg-name-items.qs"}
    total, per_file = 0, {}
    for path in BATCHES:
        if path.name not in daily:
            continue
        n = sum(1 for _i, ln in statements(path) if re.search(r"(?:^|\t)P3373\t", ln))
        if n:
            per_file[path.name] = n
        total += n
    assert total <= SIBLING_CAP, (
        f"{total} P3373 sibling statements in one day's run, cap is {SIBLING_CAP}: "
        f"{per_file}")


@pytest.mark.parametrize("name", NAMES)
def test_every_statement_has_a_comment_above_it(name):
    """Emma's format, 2026-08-26: *"Every line has a comment the line above it saying what
    change is happening."*

    Applied as a post-pass in `scripts/qscomment.py` rather than at each `lines.append`,
    because these builders emit from a dozen sites and a rule applied at every call site
    is one that will be missed at the thirteenth. This asserts the structural property the
    post-pass guarantees, so a new emission site cannot quietly arrive uncommented.

    Only the files the daily run writes are checked: batches built before the format
    existed are history and are not rewritten to satisfy a rule made after them.
    """
    if name not in {"wikidata-garborg-day.qs", "wikidata-garborg-name-items.qs"}:
        pytest.skip(f"{name} predates the commented format")
    path = REPORTS / name
    raw = path.read_text(encoding="utf-8").split("\n")
    bare = []
    for i, line in enumerate(raw):
        if not line.strip() or line.startswith("#"):
            continue
        prev = raw[i - 1].strip() if i else ""
        if not prev.startswith("#"):
            bare.append((i + 1, line[:60]))
    assert not bare, (
        f"{name}: {len(bare)} statement lines with no comment above them — "
        + "; ".join(f"line {i}: {ln!r}" for i, ln in bare[:4]))


@pytest.mark.parametrize("name", NAMES)
def test_no_english_label_is_written_in_a_non_latin_script(name):
    """An `Len` value must contain a Latin letter. It is the ENGLISH label.

    The non-Latin fallback added 2026-08-26 rescues **55,547 people** whose `label_en` and
    `label_mul` are both empty while they carry a name in `cjk_names` (44,028) or
    `other_script_names` (11,519) — without it they hit the redacted branch and were created
    as a bare `NN`, losing a name Geni actually recorded. `6000000186285688241` is the case
    Emma's own batch surfaced: their name is `부여융 무명`.

    But that name then landed in `Len` as well as `Lmul`, and an English label holding a
    Korean string is wrong twice over: it is not English, and Wikidata's `Help:Default values
    for labels and aliases` says outright that a name not in Latin script should not be a
    default label. `mul` is the language-neutral slot and takes it alone.

    Verified by removing the guard and watching this fail.
    """
    if name in SPENT_BATCHES:
        pytest.skip(f"{name} is a record of a batch already run")
    bad = []
    for i, ln in statements(REPORTS / name):
        parts = ln.split("	")
        if len(parts) > 2 and parts[1] == "Len":
            value = parts[2].strip('"')
            if value and not re.search(r"[A-Za-z]", value):
                bad.append((i, value))
    assert not bad, (
        f"{name}: English labels with no Latin letter — "
        + "; ".join(f"line {i}: {v!r}" for i, v in bad[:4]))


def test_the_daily_batch_never_restates_what_the_item_already_holds():
    """A statement already on the item must not be emitted again.

    **Emma, 2026-08-27**, on the relationship section never shrinking: *"the relationship one
    is questionable that it's always gonna be so huge and growing."* Measured that day: **229
    of 306** statements on existing items were already on Wikidata — 75% of the section.

    Two causes, and the stale file was only one. `P40` *child*, `P26` *spouse* and `P3373`
    *sibling* consulted **no** check at all, so every such link went out on every run; and
    `absent()` is property-level against a snapshot frozen at 2026-08-24, which cannot tell a
    second father from an existing one nor that yesterday's batch was run.

    QuickStatements merges a duplicate rather than failing, which is exactly why it went
    unnoticed for days: nothing broke, the batches were simply three-quarters things she had
    already done.

    `LAST` is exempt — it names an item created in this run, so the statement cannot already
    exist. Labels and aliases are exempt because they REPLACE rather than add.
    """
    values = REPORTS / "garborg-live-values.tsv"
    batch = REPORTS / "wikidata-garborg-day.qs"
    if not values.exists() or not batch.exists():
        pytest.skip("live values or the daily batch not built")
    live = {(r["qid"], r["property"], r["value"]) for r in
            csv.DictReader(open(values, encoding="utf-8"), delimiter="\t")}
    assert len(live) > 500, f"only {len(live)} live statements — that is a broken read"

    repeats = []
    for i, ln in statements(batch):
        p = ln.split("\t")
        if (len(p) >= 3 and p[0].startswith("Q") and p[1].startswith("P")
                and p[2] != "LAST"
                and (p[0], p[1], p[2].strip('"')) in live):
            repeats.append((i, ln[:60]))
    assert not repeats, (
        f"{len(repeats)} statements the item already holds — "
        + "; ".join(f"line {i}: {ln!r}" for i, ln in repeats[:4]))
