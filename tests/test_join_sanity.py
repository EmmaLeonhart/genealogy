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
