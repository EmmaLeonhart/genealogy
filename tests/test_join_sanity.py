"""Every join this repo depends on must match something. An empty one is a silent lie.

Five findings this week were about the instrument rather than the data, and each printed a
plausible number:

===========================================  ===============================  ====================
what                                         what it printed                  what was true
===========================================  ===============================  ====================
``split()`` unaware of ``" | "``             615 ambiguous slots, no ``2x2``  379,251 childless
``|`` split without ``.strip()``             pair count moved by *zero*       tokens missed index
``father[child] = husb``                     census read **0**                1,663 people
sex rate over ``zipper-pairs.tsv``           **0.0%** for all four shapes     measured the filter
``chart_name`` column that does not exist    all 10 pairs "no item held"      196 names have QIDs
===========================================  ===============================  ====================

**The shape is always the same.** An empty or narrowed join cannot be told apart from an absence
of data, and absence is precisely what these reports exist to detect. ``CLAUDE.md`` records the
same lesson for dates — *"a wrong date parser does not raise, it just quietly narrows the data"* —
and it has now recurred five times outside dates.

These tests assert that each join matches a **non-trivial share** of its input. Deliberately not
an exact figure: the corpus grows, and a test that needs updating every week gets updated without
being read. A floor catches the failure that matters — a separator change, a renamed column, a
schema drift — while leaving normal growth alone.

Marked ``slow`` where the file is one of the large derived CSVs.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"
OUT = ROOT / "out"

csv.field_size_limit(1 << 30)


def split_multi(cell):
    """The repo's multi-value convention: ` | `, and the strip is load-bearing."""
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def _rows(path, delim=","):
    with open(path, encoding="utf-8") as f:
        yield from csv.DictReader(f, delimiter=delim)


@pytest.mark.slow
def test_derived_family_multi_values_land_in_the_index():
    """`children` and `spouses` hold ` | `-separated ids that must BE people.

    This is the bug that made the zipper blind to every multi-child family: the separator is
    ` | ` with spaces, so splitting on `|` alone yields `"1050090 "` and splitting on `,;`
    alone yields one uncut token. Either way `x in ours` rejects it and the person presents
    as childless.
    """
    rows = list(_rows(R / "derived-family.csv"))
    people = {row["geni_id"] for row in rows}

    # **Only cells that actually hold several values.** Measured over ALL cells this guard does
    # not guard: the first version asserted a >50% resolve rate across every token and both
    # historical bugs passed it -- 58.5% for the unstripped split and 86.3% for the pipe-blind
    # one -- because single-valued cells have no separator and resolve either way, and they are
    # the large majority. Restricted to multi-valued cells the separation is total: 100.0%
    # correct against 0.0% for both bugs.
    checked = resolved = 0
    for row in rows:
        for col in ("children", "spouses", "fathers", "mothers"):
            cell = row.get(col) or ""
            if "|" not in cell:
                continue
            for other in split_multi(cell):
                checked += 1
                if other in people:
                    resolved += 1
    assert checked > 100_000, f"only {checked} tokens in multi-valued cells; they look empty"
    share = resolved / checked
    assert share > 0.9, (
        f"only {share:.1%} of {checked:,} ids inside MULTI-VALUED cells resolve to a person. "
        f"The separator is ' | ' WITH SPACES: splitting on '|' without stripping, or on ',;' "
        f"alone, yields tokens that match nobody, and every affected person then reads as "
        f"having no relatives at all. Both of those score 0.0% here.")


@pytest.mark.slow
def test_derived_family_records_people_with_more_than_one_parent():
    """`fathers`/`mothers` exist so a second parent is not overwritten.

    `derive-family.py` held parents in a plain dict and a second father replaced the first,
    so the multi-parent census read 0 when the merged GEDCOM holds 1,663 such people.
    """
    rows = list(_rows(R / "derived-family.csv"))
    assert "fathers" in rows[0], (
        "derived-family.csv has no `fathers` column -- re-run scripts/derive-family.py. "
        "Without it a person's second parent is silently dropped.")
    multi = sum(1 for r in rows
                if len(split_multi(r["fathers"])) > 1 or len(split_multi(r["mothers"])) > 1)
    assert multi > 100, (
        f"only {multi} people have more than one recorded parent. The merge unions FAMC/CHIL "
        f"and never drops one, so this cannot be near zero -- it was 1,663 when measured off "
        f"out/merged.ged directly.")


def test_the_izumo_chart_roster_joins_to_the_chart_edges():
    """`izumo-chart-edges.tsv` writes `Izumo no Otoyama#26`; the roster writes `english`.

    Joining on a `chart_name` column that does not exist matched nothing, and every pair then
    reported "no item held" -- indistinguishable from the clan simply not being on Wikidata.
    """
    roster = {(r.get("english") or "").strip(): (r.get("qid") or "").strip()
              for r in _rows(R / "izumo-chart-roster.tsv", "\t")}
    roster = {k: v for k, v in roster.items() if k and v.startswith("Q")}
    assert len(roster) > 50, f"only {len(roster)} roster names carry a QID"

    seat = re.compile(r"#(\d+)\s*$")
    names = set()
    for r in _rows(R / "izumo-chart-edges.tsv", "\t"):
        names.add(seat.sub("", r["parent"]).strip())
        names.add(seat.sub("", r["child"]).strip())
    hit = sum(1 for n in names if n in roster)
    assert hit > 0.3 * len(names), (
        f"only {hit} of {len(names)} chart names join to the roster. The join is on the BASE "
        f"name -- the roster column is `english` and the seat lives in `succession`, while the "
        f"edges carry `#NN` inline.")


def test_the_garborg_ledger_joins_to_the_derived_tree():
    """Every ledger Geni id from HER CONTRIBUTIONS should be a person we hold.

    **The Bureätten rows are excluded, and that is a finding rather than an exemption.** Since
    2026-08-27 the ledger has a second source — `reports/bureatten.csv`, the sv.wikipedia
    Category:Bureätten listing, on Emma's definition: *"every item whose swedish wikipedia item
    is in category:bureatten and which has a geni id."* Those people have Geni profiles but are
    **not all in our exports**: about 101 are absent from `derived-labels.csv`, which took the
    ledger to 349 of 450 and broke this floor.

    That is worth knowing — the batch resolves names through `derived-labels.csv`, so a Bureätten
    person we do not hold gets no label. It is not a broken join, which is what this test exists
    to catch, so the assertion now covers the contributions rows, where a miss really would mean
    the tree and the ledger had come apart.
    """
    ledger = [r["geni_id"] for r in _rows(R / "garborg-qids.tsv", "\t")
              if r.get("qid", "").startswith("Q")
              and "Bureätten" not in (r.get("note") or "")]
    assert len(ledger) > 20, f"only {len(ledger)} ledger rows from her contributions"
    people = {r["geni_id"] for r in _rows(R / "derived-labels.csv")}
    hit = sum(1 for g in ledger if g in people)
    assert hit > 0.8 * len(ledger), (
        f"only {hit} of {len(ledger)} ledger people are in derived-labels.csv. The batch "
        f"builder resolves names through that file; a broken join makes everyone unnamed.")


def test_the_spine_paths_resolve_to_people_we_hold():
    """The three lines are the programme's spine; every step must be a real profile."""
    ids = []
    for name in ("charlemagne-to-arne-garborg.tsv", "bergitte-to-emma.tsv"):
        path = ROOT / "paths" / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            m = re.search(r"geni:(\d{10,})", line)
            if m:
                ids.append(m.group(1))
    assert len(ids) > 30, f"only {len(ids)} spine steps carry a Geni id"
    people = {r["geni_id"] for r in _rows(R / "derived-labels.csv")}
    missing = [g for g in ids if g not in people]
    assert not missing, (
        f"{len(missing)} spine steps are not in our tree: {missing[:5]}. Every step was held "
        f"when the paths were captured, so this means the corpus moved under them.")


@pytest.mark.slow
def test_a_measurement_over_a_filtered_file_is_not_mistaken_for_the_population():
    """`zipper-pairs.tsv` holds SURVIVORS; the refused ones are a separate file.

    Measuring sex disagreement over the kept file alone returned 0.0% for every shape, which
    describes the filter rather than the join. Both files must exist and the refused one must
    be non-empty, or that mistake is available again.
    """
    kept = R / "zipper-pairs.tsv"
    refused = R / "zipper-sex-refuted.tsv"
    assert kept.exists(), "reports/zipper-pairs.tsv missing"
    assert refused.exists(), (
        "reports/zipper-sex-refuted.tsv missing -- without it, any rate computed over "
        "zipper-pairs.tsv alone measures the filter and reads as a property of the join.")
    n_ref = sum(1 for _ in _rows(refused, "\t"))
    assert n_ref > 0, (
        "no sex-refused pairs recorded. Either the filter is off, or the file was written "
        "empty -- and a rate computed against it would come out 0.0% either way.")


def test_the_model_vs_reality_snapshot_is_a_dict_of_items():
    """`full_entities` already unwraps `entities`; unwrapping twice yields `{}`.

    The first run printed `0 items held` and reported all 71 people as ITEM NOT FETCHED,
    which reads like a network failure rather than a bug two lines up.
    """
    snap = OUT / "model-vs-reality-items.json"
    if not snap.exists():
        pytest.skip("no snapshot fetched in this checkout")
    items = json.loads(snap.read_text(encoding="utf-8"))
    assert isinstance(items, dict) and items, "the snapshot is empty"
    assert all(k.startswith("Q") for k in list(items)[:20]), (
        "the snapshot's keys are not QIDs -- it is probably the raw API envelope rather than "
        "its `entities` value.")


def test_the_duplicate_report_actually_contains_japanese_profiles():
    """Emma asked for higher scrutiny on the Japanese profiles. The column said `Latin`.

    `scripts/find-geni-duplicates.py` carried a `script` column and a sort key putting
    `Han`/`Kana`/`mixed` first — and for the whole life of the report it classified
    **every one of 1,329,328 people as Latin, and none as Han**. It matched on
    `label_en` falling back to `label_mul`, which are the romanised forms; the kanji live
    in `cjk_names`, a column it never read. The higher-scrutiny pass had nothing in it.

    Nothing crashed and no file was empty. The report had the right shape, the right
    column and a plausible 9,546 rows — the population it was built to surface simply was
    not in it. That is the same failure as the ` | ` separator and the `chart_name` join.

    Verified by reverting `find-geni-duplicates.py` to match on the label: this drops to 0.
    """
    path = R / "geni-duplicate-candidates.tsv"
    if not path.exists():
        pytest.skip("duplicate candidates not built")
    rows = list(_rows(path, "\t"))
    assert rows, "the report is empty"
    cjk = [r for r in rows if r["script"] in ("Han", "Kana", "mixed")]
    assert len(cjk) > 50, (
        f"only {len(cjk)} CJK-scripted candidate groups of {len(rows)} — the script "
        f"classification is reading the romanised label again")
    named = [r for r in cjk if r["cjk_name"].strip()]
    assert len(named) == len(cjk), "a CJK-scripted row with no kanji recorded"


def test_no_candidate_group_is_a_shared_surname_with_no_given_name():
    """A sibship where nobody has a given name is not a set of duplicates.

    Their "name" is then whatever string the family shares, so the signal fires on every
    child at once: 22 children of Emperor Xuanzong of Tang, each with `SURN 隴西狄道`
    — Longxi Didao, a **place** — `_MARNM 李` and `GIVN` empty, reported as 22 duplicates
    of each other. `Tachibana ×8` was the same thing in Latin, at rank 7 of the report.

    The guard is that every member of a group must have a given name recorded. It is
    checked here through the group's size against its name: a group of eight people
    sharing a bare one-token surname is the signature.
    """
    path = R / "geni-duplicate-candidates.tsv"
    if not path.exists():
        pytest.skip("duplicate candidates not built")
    strong = [r for r in _rows(path, "\t") if r["signal"] == "same parent, same name"]
    suspicious = [r for r in strong
                  if int(r["count"]) >= 6 and len((r["name"] or r["cjk_name"]).split()) == 1
                  and (r["father_name"] or "").endswith(r["name"] or "\x00")]
    assert not suspicious, (
        "groups that are one shared surname across a whole sibship: "
        + "; ".join(f"{r['name']}x{r['count']}" for r in suspicious[:5]))


def test_compose_returns_stripped_geni_ids():
    """`compose`'s `kin()` tested the stripped id and returned the raw one.

    `reports/derived-family.csv` separates multi-values with ` | `, spaces included. The
    filter read `if x.strip() and x.strip() in fam` and the value read `x` — so every id
    it yielded carried whitespace while passing its own guard. Everything downstream
    looked the id up unstripped and missed: **59 people per run** were picked as
    candidates and dropped with the reason *"no derived facts"*, which reads as a hole in
    the data rather than a bug in the caller. Fixing it took one run from **5 creations to
    50**.

    `CLAUDE.md` § *Our side could never have two children* records the same bug in
    `zipper-join.py`, including that the pipe-aware fix without the strip *"moved the pair
    count by exactly zero"*. This is that bug in the one disguise that survives a careful
    reading — the strip is present, on the test rather than on the value.

    Verified by reverting the `.strip()`: every id comes back with a space and the
    assertion fires.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "bgd", ROOT / "scripts" / "build-garborg-day.py")
    bgd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bgd)

    import random
    fam = {
        "100": {"father": "200 | 300", "mother": "", "spouses": "", "children": "400"},
        "200": {"father": "", "mother": "", "spouses": "", "children": "100"},
        "300": {"father": "", "mother": "", "spouses": "", "children": "100"},
        "400": {"father": "100", "mother": "", "spouses": "", "children": ""},
    }
    picked, _why = bgd.compose({"100"}, fam, random.Random(0))
    assert picked, "compose returned nobody from a tree that has two uncreated parents"
    bad = [g for g in picked if g != g.strip()]
    assert not bad, (
        f"compose returned ids carrying whitespace: {bad!r} — the ` | ` split is not "
        f"stripping its values, so every downstream lookup will miss")
    # **One parent, not both.** Her revised algorithm takes a single parent per person per
    # run — `PARENTS_PER_RUN` is a count of parents, not of pairs — so the assertion is that
    # a parent behind the ` | ` is reachable at all, which is what the strip governs.
    assert {"200", "300"} & set(picked), (
        f"neither parent behind a ` | ` was reachable; got {sorted(picked)}")


def test_the_freshness_census_can_see_output_older_than_input():
    """`repo-freshness.csv` must carry the drift column, and it must find things.

    **Drift between stages is this repo's actual failure mode**, not defects inside one.
    Three consecutive findings on 2026-08-27 were all drift: the structural walk two days
    older than `reports/derived-family.csv`; `garborg-live-state.tsv` frozen at 2026-08-24
    while the ledger rebuilt daily, making three-quarters of a batch duplicates; the
    correspondence batch four days behind the walk. Each was found by hand, one at a time.

    **Git-commit age cannot see any of them** — every one of those files was committed
    recently, just built from something older. That is what the rest of that census measures,
    which is why it never caught them.

    An all-empty column would mean the input detection had stopped matching, which reads
    exactly like a clean repo. Since it is a heuristic over path literals in the generator,
    that is the likely way it breaks.
    """
    path = R / "repo-freshness.csv"
    if not path.exists():
        pytest.skip("repo-freshness.csv not built")
    rows = list(_rows(path))
    assert rows, "the census is empty"
    assert "stale_against_input" in rows[0], (
        "the drift column is gone — git-commit age alone cannot see a file built from "
        "something newer than itself")
    with_generator = [r for r in rows if r.get("generator")]
    assert len(with_generator) > 100, (
        f"only {len(with_generator)} files resolved to a generator; the source scan that "
        f"finds them has stopped matching, so the drift column cannot fire")


def _freshness():
    """`scripts/build-repo-freshness.py`, loaded by path — the name is hyphenated."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_freshness", ROOT / "scripts" / "build-repo-freshness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_a_read_is_not_a_write():
    """`open(P / "x.tsv", encoding=...)` must not register as writing `x.tsv`.

    **This was the bug, and it hid 82 drift rows.** The census works out a generator's
    *inputs* by subtracting what it writes from what it names, and `written` matched any
    `open(` followed by a filename literal. So every file a script opened for READING was
    classified as its output and deleted from its inputs — which both hid real drift and
    defeated the reader-is-not-a-generator skip, reporting Emma's hand-written
    `reports/emma-judgments.tsv` as 35h behind an input it does not have.

    The distinction is the mode. A synthetic source is used rather than a real script so the
    test keeps meaning something when the scripts change.
    """
    writes_in = _freshness().writes_in
    # **The literal must sit INSIDE the `open(` call.** The old detector only ever matched
    # that shape, so a synthetic source that binds the path to a constant first would pass
    # against the broken version too and pin nothing — the `xfail`-that-never-ran mistake in
    # a new costume. Checked: the old pattern calls both of these writes.
    source = (
        'with open(ROOT / "reports" / "read-only.tsv", encoding="utf-8") as f:\n'
        '    rows = list(f)\n'
        'with open(ROOT / "reports" / "written.csv", "w", encoding="utf-8") as f:\n'
        '    f.write("x")\n'
    )
    found = writes_in(source)
    assert "written.csv" in found, (
        f"a constant opened with mode 'w' is a write and was missed: {sorted(found)}")
    assert "read-only.tsv" not in found, (
        f"a read-mode open registered as a write: {sorted(found)} — this is the defect that "
        f"took the drift count from 95 down to 13")


def test_the_other_write_spellings_are_all_recognised():
    """`write_text`, `.open("w")` and an inline literal are all writes.

    A false NEGATIVE here is the opposite failure and just as bad: a genuine output that is
    not recognised stays in its own generator's input list, so the script is skipped as a
    reader of its own file and its drift never fires.
    """
    writes_in = _freshness().writes_in
    assert "a.md" in writes_in('A = ROOT / "a.md"\nA.write_text("x")\n')
    assert "b.csv" in writes_in('B = ROOT / "b.csv"\nwith B.open("w") as f:\n    pass\n')
    assert "c.json" in writes_in('open("out/c.json", "w").write("{}")\n')
    assert "d.tsv" in writes_in('D = ROOT / "d.tsv"\nD.write_bytes(b"x")\n')


def test_emma_s_hand_written_files_are_not_claimed_as_generated():
    """The real case: `reports/emma-judgments.tsv` has no generator and must not gain one.

    It is her hand-verdict file — `CLAUDE.md` § *The chain of provenance* — and nothing in
    `scripts/` writes it. Two scripts READ it, and while a read looked like a write they were
    named its writers.
    """
    freshness = _freshness()
    for script in ("zipper-provenance.py", "measure-zipper-reliability.py"):
        path = ROOT / "scripts" / script
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        assert "emma-judgments.tsv" not in freshness.writes_in(text), (
            f"scripts/{script} is claimed to WRITE emma-judgments.tsv; it reads it, and "
            f"Emma maintains it by hand")
        assert "reports/emma-judgments.tsv" in freshness.inputs_of(f"scripts/{script}"), (
            f"scripts/{script} no longer reports emma-judgments.tsv as an input — the "
            f"filename scan has stopped matching")


def _refresher():
    """`scripts/refresh-drift.py`, loaded by path."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_refresh_drift", ROOT / "scripts" / "refresh-drift.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_refresher_never_runs_a_script_that_talks_to_wikidata():
    """A topological sort must not be trusted to respect the one rail that matters.

    `CLAUDE.md` § *Never query Wikidata to check something* — one bulk downloader, nothing else.
    The refresher picks its scripts from a generated CSV, so nobody reads the list before it
    runs; the offline screen is the only thing standing between that and a 429.
    """
    offline = _refresher().offline
    real = "scripts/genimerge-noop-that-does-not-exist.py"
    assert offline(real) is False, "a missing script must not count as safe to run"
    for script in ("scripts/refresh-live-values.py",):
        if (ROOT / script).exists():
            assert not offline(script), (
                f"{script} builds a WikidataClient and must never be auto-run")
    for script in ("scripts/build-repo-freshness.py",):
        assert offline(script), f"{script} makes no request and should be runnable"


def test_the_refresher_decodes_subprocess_output_as_utf8():
    """`text=True` alone decodes as cp1252 here and dies on the first Japanese name.

    The real run raised `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81` out of a
    subprocess reader thread — this process failing to read a child that was perfectly fine.
    The reports are full of kana and Han, so it is the common case.
    """
    import subprocess
    import sys as _sys
    run = _refresher().RUN
    assert run.get("encoding") == "utf-8", "explicit utf-8 is what stops the cp1252 default"
    r = subprocess.run(
        [_sys.executable, "-c",
         'import sys;sys.stdout.reconfigure(encoding="utf-8");print("\u30ab\u30ca \u9ec4")'],
        **run)
    assert r.returncode == 0 and "カナ" in r.stdout, (
        f"non-ASCII child output did not survive capture: {r.stdout!r}")


def test_a_middle_initial_stays_latin_in_a_japanese_label():
    """`John F. Smith` -> ジョン・F・スミス, not "no label at all".

    **Emma, 2026-08-27**, choosing between four readings: keep the initial Latin inside the
    label. Dropping it loses what the Latin label carries; rendering it エフ invents a reading
    nobody uses. 12,805 tokens sit in the middle-initial position across the corpus and every
    name containing one was getting no `ja`/`zh` label at all, because the transliteration rule
    is all-or-nothing.

    The all-or-nothing rule itself is untouched — an unknown NAME still blocks the whole label.
    """
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from labels import transliterate_token

    table = {"John": ("ジョン", "约翰"), "Smith": ("スミス", "史密斯")}
    assert transliterate_token("F.", table) == ("F", "F")
    assert transliterate_token("F", table) == ("F", "F")
    assert transliterate_token("John", table) == ("ジョン", "约翰")
    assert transliterate_token("Zzz", table) == (None, None), (
        "an unknown NAME must still block the label — the initial rule is the one exception, "
        "not a licence to render half a name")


def test_the_two_phrases_emma_ruled_on_are_in_the_marker_vocabulary():
    """`Name Not Known` (45 people) and `Unknown Wife` (37) — "Both are markers".

    Held out of the vocabulary until she ruled, because widening it is her call. Pinned here
    because a queue item claimed for nine days that they were still waiting while they were
    already in `labels.py`.
    """
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from labels import WORDS_MEANING_UNKNOWN

    for phrase in ("name not known", "unknown wife", "ukjent", "未知", "某"):
        assert phrase in WORDS_MEANING_UNKNOWN, f"{phrase!r} fell out of the marker vocabulary"


def test_a_lowercase_norwegian_particle_is_not_an_initial():
    r"""`Ragnhild Toresdatter Håland i Gjesdal` — that `i` is Norwegian for *in*.

    The first version of the initial rule was `^[A-Za-z]\.?$` with an `.upper()`, so the
    preposition became an initial `I` and was planted in a Japanese label:
    `ラグンヒル・トーレスダッテル・ホーランド・I・イェスダール`. Found by reading the emitted
    batch rather than by reasoning about the rule.

    An initial is capitalised, or carries a full stop. A bare lowercase letter is a word.
    """
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from labels import transliterate_token

    table = {}
    assert transliterate_token("i", table) == (None, None), (
        "bare lowercase `i` is Norwegian *in*, not an initial — it must block the label the "
        "way any other untransliterated word does")
    assert transliterate_token("I", table) == ("I", "I")
    assert transliterate_token("i.", table) == ("i", "i"), "case is never changed"
    assert transliterate_token("F.", table) == ("F", "F")


def test_an_argument_free_day_build_is_refused():
    """`build-garborg-day.py` with no arguments must exit non-zero and write nothing.

    **Bare it emits 272 creations; with `--compose` it emits 34** — the flag carries
    `CHILDREN_PER_RUN`, `PARENTS_PER_RUN`, `FREE_PARENTS_FREE` and `SIBLING_CAP`, so the bare
    path is not a smaller daily algorithm, it skips the algorithm. Both write the same file, so
    a bare run silently replaces a day Emma may already have run.

    `--roster` is a real second mode and stays allowed; only the argument-free call is refused,
    because it has no purpose except the mistake.
    """
    import subprocess
    import sys as _sys

    batch = R / "wikidata-garborg-day.txt"
    before = batch.read_bytes() if batch.exists() else None
    env = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")}
    r = subprocess.run([_sys.executable, str(ROOT / "scripts" / "build-garborg-day.py")],
                       cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    assert r.returncode != 0, "an argument-free day build must refuse, not run"
    assert "--compose" in (r.stdout + r.stderr), "the refusal must name the flag that is missing"
    if before is not None:
        assert batch.read_bytes() == before, (
            "the refused run still touched reports/wikidata-garborg-day.txt")


def test_the_ck_digraph_is_one_sound_not_two():
    """Emma hand-corrected `Q141216408` from **ウン・モルクク** to **ウン・モルク**, 2026-08-29.

    `translit_no` walks letter by letter with a geminate rule for *identical* adjacent letters
    (`nn` in `Anna`), and had none for a digraph of *different* letters spelling one phoneme.
    So `Mørck` came out `m`+`ø` モ, `r` ル, `c` ク, `k` ク — a `ク` too many, and the same on the
    Chinese side. 47 tokens in `reports/garborg-name-transliterations.tsv` carried the doubling.

    Pinned in both positions, because the bug showed differently in each: in the coda it doubled
    the kana, and in an onset (`Sacken`) it produced a spurious extra syllable `サクケン`.
    """
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from translit_no import translit

    assert translit("Mørck") == ("モルク", "莫尔克"), "her correction, exactly"
    assert translit("Sacken") == ("サケン", "萨肯"), (
        "ck in onset position. The Chinese was 萨凯恩 when this test was written, which "
        "encoded the coda-nasal bug Emma caught on 2026-08-30: ken is 肯, one syllable.")
    assert translit("Anna") == ("アナ", "阿纳"), "the geminate rule for identical letters stands"


def test_the_rule_refresh_never_rewrites_a_hand_checked_row():
    """`refresh-rule-transliterations.py` re-derives cache and nothing else.

    The `note` column is the whole safety story: `by rule` and `composed by rule: …` are a
    cached function of an engine that changes, and every other note means a person checked the
    reading. `CLAUDE.md` § *the purpose is to ADD* — a rule does not overwrite a human.
    """
    import csv as _csv
    table = ROOT / "reports" / "garborg-name-transliterations.tsv"
    rows = list(_csv.DictReader(table.open(encoding="utf-8"), delimiter="\t"))
    derived = [r for r in rows if (r["note"] or "").startswith(("by rule", "composed by rule:"))]
    hand = [r for r in rows if r not in derived]
    assert hand, "the hand rows are the test set; losing them would make the score meaningless"

    # No row of either kind may still carry the doubled digraph.
    doubled = [r["token"] for r in rows if "クク" in r["ja"] and "ck" in r["token"].lower()]
    assert not doubled, f"the ck doubling came back on: {doubled[:10]}"


def test_a_syllable_final_nasal_is_inside_the_chinese_syllable():
    """Emma, 2026-08-30: *"is 塞恩 right for sen? … sounds sussy for Chinese"*. It was not.

    `translit_no` gave every coda consonant its own character, so a syllable-final nasal became
    a separate 恩: `sen` as 塞 + 恩 rather than 森. **1,701 rows of the table carried the shape
    and 1,201 a standalone 恩.** Agreement with the rows the engine did not write went
    11.7% -> 46.5% when `NASAL_FINAL` landed.

    Japanese is asserted alongside on purpose: `ン` is a real mora and was always right, so a
    change that "fixes" the katakana here is a regression, not an improvement.
    """
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from translit_no import translit

    assert translit("Arnesen")[1] == "阿尔内森", "sen is 森, not 塞恩"
    assert translit("Absalon") == ("アブサロン", "阿布萨隆")
    assert translit("Hansen") == ("ハンセン", "汉森")
    assert translit("Bing")[1] == "宾", "-ng is a nasal final too"
    # A nasal with a vowel after it is not final: `Anna` is `an` + `na`.
    assert translit("Anna") == ("アナ", "阿纳")


def test_emmas_own_corrections_are_in_the_table():
    """Her hand corrections outrank the engine and must survive every re-derivation.

    `Mørck` -> `モルク` (2026-08-29, on `Q141216408`) and `Minnie` -> `ミニー` / `米妮`
    (2026-08-30, on `Q141216493`). The `Minnie` row was `ミニエ` / `米尼埃` by rule, and the
    engine still produces that — so this fails the moment a refresh treats her row as cache.
    """
    import csv as _csv
    rows = {r["token"]: r for r in _csv.DictReader(
        (ROOT / "reports" / "garborg-name-transliterations.tsv").open(encoding="utf-8"),
        delimiter="\t")}
    assert (rows["Minnie"]["ja"], rows["Minnie"]["zh"]) == ("ミニー", "米妮")
    assert rows["Mørck"]["ja"] == "モルク"


def test_the_two_items_whose_cjk_labels_are_not_ours_are_never_overwritten():
    """Emma, 2026-08-30: *"Arne Garborg and Johannes Bureus are the only people with cjk labels
    not added by us. So only those ones are to be taken as gospel."*

    Everything else in the ledger got its `ja`/`zh` from this pipeline, which is what makes
    redoing them safe — and makes these two the one place where redoing them is not.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_garborg_day", ROOT / "scripts" / "build-garborg-day.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.CJK_LABELS_NOT_OURS == {"Q467497", "Q633094"}
    assert module.ZH_OVERWRITE is True, (
        "she said fix it and do the overwrite, not gate it")


def test_a_territorial_designation_is_not_transliterated_as_a_name():
    """`Q6161733` came out `カール・フレドリク・パイパー・ティル・クラゲホルム`. Emma fixed it.

    *"why was the japanese label we added so weird? I fixed it but we added a weird one"* --
    `till Krageholm` is Swedish for *of Krageholm*, an estate, and reading it token by token
    turns two more syllables into part of his name. **11,873 people carry a territorial word**;
    7,179 labels are truncated once the case rule below is applied.

    Two things this must NOT do, both found by running it:

    * `van`, `von`, `af`, `av` form SURNAMES. The first draft included them and truncated
      `Reinoud I van Brederode` to `Reinoud`. `CLAUDE.md`: particles are *"integral parts of
      what the people are called"*, and `Hård af Segerstad` is a family.
    * a capital `I` is a regnal ordinal, not the Norwegian preposition. Folding case truncated
      `Reinoud I …` to `Reinoud` a second time, by a different route.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_garborg_day", ROOT / "scripts" / "build-garborg-day.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    drop = module._drop_territorial

    assert drop("Carl Fredrik Piper till Krageholm") == "Carl Fredrik Piper"
    assert drop("Mogens Pedersen Baden til Gundestrup") == "Mogens Pedersen Baden"
    assert drop("Ragnhild Toresdatter Håland i Gjesdal") == "Ragnhild Toresdatter Håland"
    # Surnames survive.
    assert drop("Hård af Segerstad") == "Hård af Segerstad"
    assert drop("Reinoud I van Brederode") == "Reinoud I van Brederode"
    # A regnal ordinal is not a preposition.
    assert drop("Abisha III ben Phinhas") == "Abisha III ben Phinhas"
    # A trailing preposition with nothing after it is a name token, not a designation.
    assert drop("Ole Olsen i") == "Ole Olsen i"


def test_the_duplicate_finder_finds_the_duplicates_geni_actually_merged():
    """Recall against the only ground truth in the repo, not a count of what it produced.

    **Measured 2026-08-30, and it is the reason this test exists.** `find-geni-duplicates.py`
    reported **10,111 candidate groups**, a plausible number nobody had reason to doubt. Checked
    against `reports/geni-stale-duplicates.tsv` -- 29 pairs Geni has actually merged -- it
    contained **one** of them, and 25 of the 29 appeared in it not at all.

    The cause was structural rather than a coding slip: the group key was `(father_id,
    mother_id)`, and a Geni duplicate is almost never one lone profile. Somebody re-creates a
    stretch of line, so the child *and* the parent are duplicated, the two children hang off two
    different parent ids, and that key can never bring them together. Every `strong` row in the
    ground truth is that shape -- its own `father_name_matches` column reads `yes` while the
    father ids differ.

    So the assertion is on **recall over known answers**, which is the only thing that would
    have caught it. `CLAUDE.md` § *Our side could never have two children* is the general
    lesson, and its closing rule -- *a guard that has not been seen to FAIL is not known to
    guard* -- is why this is pinned at the level the fix achieved rather than at something
    comfortably below it.
    """
    import csv as _csv

    known = list(_csv.DictReader(
        (ROOT / "reports" / "geni-stale-duplicates.tsv").open(encoding="utf-8"),
        delimiter="\t"))
    assert known, "the ground truth file is empty; this guard measures nothing"

    groups = [set(r["geni_ids"].split(";")) for r in _csv.DictReader(
        (ROOT / "reports" / "geni-duplicate-candidates.tsv").open(encoding="utf-8"),
        delimiter="\t")]

    def paired(row):
        return any(row["stale_twin"] in g and row["merged_survivor"] in g for g in groups)

    strong = [r for r in known if r["evidence"] == "strong"]
    missed = [r["name"] for r in strong if not paired(r)]
    assert not missed, (
        f"{len(missed)} of {len(strong)} strongly-evidenced merged pairs are not grouped "
        f"together as candidates: {missed[:3]}")

    # The weak and medium rows are weaker evidence of a merge, so they are not required --
    # but the overall figure must not slide back towards the single hit it started at.
    assert sum(paired(r) for r in known) >= 15
