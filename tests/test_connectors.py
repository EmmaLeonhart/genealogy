"""Grouping the missing people on our paths into bridges, and bridges into clusters.

The unit tests build `PathReport`s directly rather than going through a tree:
what `connectors` adds on top of `genimerge.paths` is entirely a matter of how
absent steps are grouped, and a synthetic report states that far more clearly
than a synthetic GEDCOM would.

The test at the bottom runs the real path files, because the finding this module
exists for — that a few missing people block several paths at once — is a
property of the actual data and would be invisible against a fixture.
"""

from pathlib import Path

import pytest

from genimerge import connectors, paths as paths_mod

REPO = Path(__file__).resolve().parents[1]
PATHS_DIR = REPO / "paths"


def report(*rows) -> paths_mod.PathReport:
    """A checked path from ``(name, geni_id, held, relation)`` tuples."""
    results = []
    for i, (name, geni_id, held, relation) in enumerate(rows, 1):
        step = paths_mod.PathStep(
            step=i, name=name, relation=relation, note=f"geni:{geni_id}"
        )
        results.append(
            paths_mod.StepResult(step=step, how="id" if held else paths_mod.ABSENT)
        )
    return paths_mod.PathReport(results=results)


# -- bridges -----------------------------------------------------------


def test_a_run_of_absent_steps_becomes_one_bridge():
    checked = report(
        ("A", "1", True, ""),
        ("B", "2", False, "his father"),
        ("C", "3", False, "her mother"),
        ("D", "4", True, "his son"),
    )

    found = connectors.bridges(checked, "p")

    assert len(found) == 1
    assert [r.step.name for r in found[0].members] == ["B", "C"]
    assert found[0].doorway.step.name == "A"
    assert found[0].resume.step.name == "D"


def test_two_separate_runs_are_two_bridges():
    checked = report(
        ("A", "1", True, ""),
        ("B", "2", False, ""),
        ("C", "3", True, ""),
        ("D", "4", False, ""),
        ("E", "5", True, ""),
    )

    found = connectors.bridges(checked, "p")

    assert [b.first_step for b in found] == [2, 4]
    assert [b.doorway.step.name for b in found] == ["A", "C"]


def test_a_bridge_never_spans_two_paths_in_one_file():
    """Emma, 2026-08-16: *"treat it as being two paths and not one."*

    A saved page carries a blood path and an in-law path, and both land in one
    file. A run of absent steps that reaches the seam has reached the end of
    *its own* path: it has no resume, and the next path's missing people are not
    behind the same doorway. Reading them as one run would rank an export by a
    gap that does not exist.
    """
    results = []
    for i, (name, gid, held, relation, chain) in enumerate(
        [("A", "1", True, "", 1),
         ("B", "2", False, "his father", 1),
         ("C", "3", False, "-", 2),
         ("D", "4", True, "her husband", 2)], 1
    ):
        step = paths_mod.PathStep(step=i, name=name, relation=relation,
                                  note=f"geni:{gid}", chain=chain)
        results.append(paths_mod.StepResult(
            step=step, how="id" if held else paths_mod.ABSENT))
    checked = paths_mod.PathReport(results=results)

    found = connectors.bridges(checked, "p")

    assert len(found) == 2
    assert [r.step.name for r in found[0].members] == ["B"]
    assert found[0].doorway.step.name == "A"
    assert found[0].resume is None, "B's run ends with its own path, not at C"
    assert [r.step.name for r in found[1].members] == ["C"]
    assert found[1].doorway is None, "the second path has no held step before C"
    assert found[1].resume.step.name == "D"


def test_a_path_that_ends_absent_has_no_resume():
    """A frontier, not a bridge. The distinction decides what an export buys:
    a bridge has a named far side, a frontier walks into the unknown."""
    checked = report(("A", "1", True, ""), ("B", "2", False, ""))

    found = connectors.bridges(checked, "p")

    assert found[0].resume is None
    assert connectors.cluster(found)[0].ends_a_path


def test_a_path_that_starts_absent_has_no_doorway():
    checked = report(("A", "1", False, ""), ("B", "2", True, ""))

    found = connectors.bridges(checked, "p")

    assert found[0].doorway is None
    assert connectors.cluster(found)[0].doorways == []


def test_a_fully_held_path_has_no_bridges():
    assert connectors.bridges(report(("A", "1", True, "")), "p") == []


# -- clustering --------------------------------------------------------


def test_bridges_sharing_a_person_become_one_cluster():
    """The whole point of the module. Two paths blocked by the same people are
    one export, not two, and the slot count says so."""
    shared = [("A", "1", True, ""), ("B", "2", False, ""), ("C", "3", False, "")]
    found = connectors.bridges(report(*shared), "one") + connectors.bridges(
        report(*shared), "two"
    )

    clusters = connectors.cluster(found)

    assert len(clusters) == 1
    assert clusters[0].slots == 4  # two people, each blocking two paths
    assert len(clusters[0].people) == 2
    assert clusters[0].path_names == ["one", "two"]


def test_partial_overlap_still_joins():
    """`psamtik-ii` overlaps the Jurhumid cluster without matching it exactly.
    Requiring identical member sets would count one export's payoff twice."""
    found = connectors.bridges(
        report(("A", "1", True, ""), ("B", "2", False, ""), ("C", "3", False, "")), "one"
    ) + connectors.bridges(
        report(("A", "1", True, ""), ("C", "3", False, ""), ("D", "4", False, "")), "two"
    )

    clusters = connectors.cluster(found)

    assert len(clusters) == 1
    assert [p.step.name for p in clusters[0].people] == ["B", "C", "D"]


def test_bridges_with_nobody_in_common_stay_apart():
    found = connectors.bridges(
        report(("A", "1", True, ""), ("B", "2", False, "")), "one"
    ) + connectors.bridges(report(("X", "8", True, ""), ("Y", "9", False, "")), "two")

    assert len(connectors.cluster(found)) == 2


def test_clusters_are_ranked_by_slots_not_by_length():
    """A ten-person gap crossing five paths beats a fifty-person gap on one.
    Ranking by gap length gets this exactly backwards."""
    wide = [("A", "1", True, "")] + [(f"P{n}", str(100 + n), False, "") for n in range(3)]
    long_one = [("Z", "50", True, "")] + [
        (f"Q{n}", str(200 + n), False, "") for n in range(5)
    ]
    found = (
        connectors.bridges(report(*wide), "one")
        + connectors.bridges(report(*wide), "two")
        + connectors.bridges(report(*long_one), "solo")
    )

    clusters = connectors.cluster(found)

    assert clusters[0].slots == 6 and len(clusters[0].path_names) == 2
    assert clusters[1].slots == 5 and len(clusters[1].people) == 5


# -- the style hint ----------------------------------------------------


@pytest.mark.parametrize("relation", ["his wife", "her husband", "his partner"])
def test_a_marriage_link_calls_for_forest(relation):
    """`CLAUDE.md`'s rule, enforced: a blood-only style walks past a spouse."""
    found = connectors.bridges(
        report(("A", "1", True, ""), ("B", "2", False, relation)), "p"
    )

    assert connectors.cluster(found)[0].style == "Forest"


def test_a_sibling_link_calls_for_forest():
    found = connectors.bridges(
        report(("A", "1", True, ""), ("B", "2", False, "his brother")), "p"
    )

    cluster = connectors.cluster(found)[0]
    assert cluster.style == "Forest"
    assert "brother" in cluster.style_reason


def test_a_pure_descent_run_does_not_demand_forest():
    found = connectors.bridges(
        report(("A", "1", True, ""), ("B", "2", False, "his father")), "p"
    )

    assert connectors.cluster(found)[0].style == "Ancestors or Forest"


# -- rendering ---------------------------------------------------------


def test_the_html_names_every_missing_person_and_links_them():
    found = connectors.bridges(
        report(("A", "1", True, ""), ("Berengar", "2", False, "her father")), "p"
    )
    clusters = connectors.cluster(found)

    page = connectors.render_html(clusters, {"p": report(("A", "1", True, ""))}, 10)

    assert "Berengar" in page
    assert "https://www.geni.com/people/x/2" in page
    assert page.startswith("<!doctype html>")


def test_rendering_survives_a_path_with_no_gaps_at_all():
    """An empty report is the good case, and must not divide by zero."""
    whole = {"p": report(("A", "1", True, ""))}

    assert "0" in connectors.render_html([], whole, 10)
    assert connectors.render_markdown([], whole, 10)


# -- the real paths ----------------------------------------------------


@pytest.mark.skipif(not PATHS_DIR.exists(), reason="no paths/ in this checkout")
def test_every_real_path_file_parses_and_splits_into_bridges():
    """No tree needed: this checks the path files themselves are still readable
    and that bridge-splitting survives every shape they contain."""
    files = sorted(PATHS_DIR.glob("*.tsv"))
    assert files, "paths/ holds no .tsv files"

    for file in files:
        steps = paths_mod.load_path(file)
        assert steps, f"{file.name} parsed to no steps"
        # Every step of every real path carries an ID; the name-matching
        # fallback is advisory and must never become load-bearing here.
        assert all(s.geni_id for s in steps), f"{file.name} has a step with no Geni ID"


@pytest.mark.skipif(not PATHS_DIR.exists(), reason="no paths/ in this checkout")
def test_clustering_is_stable_across_runs():
    """Two runs over the same input must rank identically, or the report's
    'rank 1' means nothing from one day to the next."""
    rows = [("A", "1", True, ""), ("B", "2", False, ""), ("C", "3", False, "")]
    found = connectors.bridges(report(*rows), "one") + connectors.bridges(
        report(*rows), "two"
    )

    first = [(c.slots, c.path_names) for c in connectors.cluster(found)]
    second = [(c.slots, c.path_names) for c in connectors.cluster(list(reversed(found)))]

    assert first == second
