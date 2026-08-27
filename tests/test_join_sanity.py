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
    """Every ledger Geni id should be a person we hold, or the batch builder sees nothing."""
    ledger = [r["geni_id"] for r in _rows(R / "garborg-qids.tsv", "\t")
              if r.get("qid", "").startswith("Q")]
    assert len(ledger) > 20, f"only {len(ledger)} ledger rows"
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
