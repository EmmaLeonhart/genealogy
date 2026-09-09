"""Guards on the three-office Izumo succession, `reports/wikidata-izumo-succession.json`.

Emma's model, 2026-08-24: three offices distinguished by the organisation, not one chain,
with the last unified holder carrying two successors.

Every assertion here is against the built file rather than the builder, so a change that
stops emitting something fails even if the code still looks right. `CLAUDE.md`'s recurring
lesson is that an empty or narrowed join reads exactly like an absence of data -- so the
first test is that the file has content at all, and the rest would pass vacuously without it.
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
BATCH = REPO / "reports" / "wikidata-izumo-succession.json"
ROSTER = REPO / "reports" / "izumo-chart-roster.tsv"

OFFICE = "Q11395856"          # Izumo no Kuni no Miyatsuko
IZUMO_TAISHA = "Q696362"      # the unified line
IZUMOKYO = "Q11395891"        # the Kitajima line
IZUMO_TAISHAKYO = "Q6102386"  # the Senge line
LAST_UNIFIED = "Q135579414"   # Izumo no Kiyotaka, seat 54
FIRST_SENGE = "Q135579415"    # Senge no Takamune, seat 55
FIRST_KITAJIMA = "Q135579416"  # Kitajima no Sadataka, seat 55

pytestmark = pytest.mark.skipif(not BATCH.exists(), reason="succession batch not built")


def edits():
    return json.loads(BATCH.read_text(encoding="utf-8"))


def quals(edit):
    out = collections.defaultdict(list)
    for q in edit["add"][0]["qualifiers"]:
        out[q["property"]].append(q["value"])
    return out


def test_the_batch_is_not_empty_and_covers_all_three_lines():
    """The join is on the roster's `succession` column; an empty one reads as no work.

    Three organisations must each appear, or a line has silently dropped out -- which is
    what screening the surname on the Latin name alone did to the two `Kitashima` rows.
    """
    orgs = collections.Counter(
        v for e in edits() for v in quals(e)["P2389"])
    assert len(edits()) > 90, f"only {len(edits())} statements; the roster join has narrowed"
    for org, name in ((IZUMO_TAISHA, "Izumo Taisha"),
                      (IZUMOKYO, "Izumo-kyō"),
                      (IZUMO_TAISHAKYO, "Izumo-taishakyo")):
        assert orgs[org] > 15, f"{name} ({org}) holds only {orgs[org]} seats"


def test_every_statement_is_the_office_with_an_organisation_and_an_ordinal():
    bad = [e["subject"]["qid"] for e in edits()
           if e["add"][0]["value"] != OFFICE
           or len(quals(e)["P2389"]) != 1 or len(quals(e)["P1545"]) != 1]
    assert not bad, f"not office+organisation+ordinal: {bad[:5]}"


def test_the_last_unified_holder_has_exactly_two_successors():
    """The fork is the whole reason this is three offices and not one chain."""
    by = {e["subject"]["qid"]: e for e in edits()}
    assert LAST_UNIFIED in by, "the last unified holder is not in the batch"
    assert sorted(quals(by[LAST_UNIFIED])["P1366"]) == sorted(
        [FIRST_SENGE, FIRST_KITAJIMA])
    assert quals(by[LAST_UNIFIED])["P2389"] == [IZUMO_TAISHA]
    for first, org in ((FIRST_SENGE, IZUMO_TAISHAKYO), (FIRST_KITAJIMA, IZUMOKYO)):
        assert quals(by[first])["P1365"] == [LAST_UNIFIED], f"{first} does not replace him"
        assert quals(by[first])["P2389"] == [org]


def test_nobody_but_the_fork_has_two_successors():
    many = [e["subject"]["qid"] for e in edits()
            if len(quals(e)["P1366"]) > 1 and e["subject"]["qid"] != LAST_UNIFIED]
    assert not many, f"a second fork appeared: {many}"


def test_no_ordering_link_crosses_the_ambiguous_seat():
    """Seat 36 has two holders and seat 37 has none, so 35 -> 36 -> 38 cannot be ordered.

    Emitting a link here would assert an adjacency the chart does not support. Both
    holders still get `P39` -- that they held the office is not what is in doubt.
    """
    seat_of = {e["subject"]["qid"]: int(quals(e)["P1545"][0]) for e in edits()}
    for e in edits():
        seat, q = seat_of[e["subject"]["qid"]], e["subject"]["qid"]
        if seat in (35, 36, 38):
            linked = quals(e)["P1365"] if seat in (36, 38) else quals(e)["P1366"]
            assert not any(seat_of.get(x) in (35, 36, 38) for x in linked), (
                f"{q} at seat {seat} links across the unresolved 36/37 boundary")


def test_a_link_always_points_at_the_adjacent_seat_of_a_real_line():
    """`P1365`/`P1366` may only join seats one apart. A skipped seat is dropped, never bridged.

    The one crossing between lines is the fork, where Senge 55 and Kitajima 55 both
    replace Izumo 54.
    """
    seat_of = {e["subject"]["qid"]: int(quals(e)["P1545"][0]) for e in edits()}
    bad = []
    for e in edits():
        here = seat_of[e["subject"]["qid"]]
        for other in quals(e)["P1365"]:
            if seat_of.get(other) != here - 1:
                bad.append((e["subject"]["qid"], here, other, seat_of.get(other)))
        for other in quals(e)["P1366"]:
            if seat_of.get(other) != here + 1:
                bad.append((e["subject"]["qid"], here, other, seat_of.get(other)))
    assert not bad, f"links to a non-adjacent seat: {bad[:5]}"


def test_the_source_is_the_chart_and_never_a_geni_reference():
    """The seat numbering comes from the Shinto Wiki chart, not from Geni.

    `S2600` would be a miscitation: the Geni profile says nothing about which seat a man
    held. Every other batch in this repo cites `P2600` because every other batch is
    emitting a Geni-derived fact.
    """
    for e in edits():
        refs = e["add"][0]["references"]
        assert [r["property"] for r in refs] == ["P854"], (
            f"{e['subject']['qid']} cites {refs}, not the chart URL")


#: The seats each line holds, and the gaps that are real rather than a classification error.
#: Seat 37 is empty because seat 36 carries two holders; seats 1 and 2 are Ame no Hohi and
#: Takehi-Nateru, who have no Wikidata item and so cannot be the subject of a statement.
LINE_SEATS = {IZUMO_TAISHA: (1, 54), IZUMOKYO: (55, 79), IZUMO_TAISHAKYO: (55, 84)}
KNOWN_GAPS = {IZUMO_TAISHA: {1, 2, 37}, IZUMOKYO: set(), IZUMO_TAISHAKYO: set()}


def test_each_line_occupies_its_own_seat_range_with_no_hole():
    """The unified office ENDS at 54 and the two sects BEGIN at 55. A hole means a
    misclassified holder.

    **This is the test that catches the Latin-name screen, and the first version of this
    file did not have it.** Screening the surname on `english` alone leaves
    `Kitashima no Naotaka` (北島脩孝, 75) and 北島斉孝 (76) in the *unified* line, which then
    reads seats 1-54 plus 75-76 — a 20-seat hole. Every other assertion here passed: the
    counts were still plausible, all three organisations were still populated, and 75->76
    are adjacent to each other so even the adjacency check was satisfied.

    Verified by reintroducing the bug and watching this fail, which is the only reason to
    believe it guards. `CLAUDE.md`: *a guard that has not been seen to fail is not known
    to guard.*
    """
    seats = collections.defaultdict(set)
    for e in edits():
        seats[quals(e)["P2389"][0]].add(int(quals(e)["P1545"][0]))
    for org, (lo, hi) in LINE_SEATS.items():
        got = seats[org]
        # `min` is `>=` because seats 1 and 2 (Ame no Hohi, Takehi-Nateru) have no
        # Wikidata item and so cannot be emitted. `max` is exact: it is the end of the
        # line, and the misclassification moves it.
        assert min(got) >= lo and max(got) == hi, (
            f"{org} runs {min(got)}-{max(got)}, expected {lo}-{hi} — "
            f"a holder is in the wrong line")
        holes = {s for s in range(lo, hi + 1) if s not in got} - KNOWN_GAPS[org]
        # A seat whose holder has no Wikidata item is legitimately absent, so a hole is
        # only reported when it is wider than one seat — a misclassification moves a run.
        runs, prev = [], None
        for s in sorted(holes):
            if prev is None or s != prev + 1:
                runs.append([s])
            else:
                runs[-1].append(s)
            prev = s
        wide = [r for r in runs if len(r) > 1]
        assert not wide, f"{org} has a run of missing seats {wide}, not single unheld ones"
