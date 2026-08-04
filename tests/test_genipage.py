"""Pulling the relationship path out of a saved Geni profile page."""

from pathlib import Path

import pytest

from genimerge import genipage

REPO = Path(__file__).resolve().parents[1]
SAVED = next((REPO / "geni_pages").glob("*.html"), None) if (REPO / "geni_pages").exists() else None


# Two path steps, plus the two kinds of link that are on every Geni profile page
# and are *not* on the path: an immediate-family link and a profile-manager
# link. Both carry `data-profile-id`, which is why matching anchors directly
# does not work.
PAGE = """<html><body>
<div class="rel-path">
<span class="segment"><span class="name"><a
  href="https://www.geni.com/people/Eric-Borsheim/6000000087535357291"
  data-profile-id="6000000087535357291">You</a></span><span class="subtext"><span
  class="clipboard-hide">&nbsp;</span></span></span>
<span class="arrow">&rarr;</span>
<span class="segment"><span class="name"><a
  href="https://www.geni.com/people/Richard/6000000177921459056?through=6000000001829589817"
  data-profile-id="6000000177921459056">Richard Wade Borsheim</a></span> <span
  class="subtext"><span class="clipboard-only">(</span>your father<span
  class="clipboard-only">)</span></span></span>
</div>
<div class="immediate-family">
  <a href="/people/x/6000000999999999" data-profile-id="6000000999999999">Someone Else</a>
</div>
<div class="managers"><span class="name"><a
  href="/people/x/6000000888888888" data-profile-id="6000000888888888">A Manager</a></span></div>
</body></html>
"""


def test_only_anchors_inside_a_segment_name_are_path_steps():
    links = genipage.parse_relationship_path(PAGE)

    assert [l.geni_id for l in links] == [
        "6000000087535357291",
        "6000000177921459056",
    ]


def test_a_manager_link_in_a_name_span_is_not_on_the_path():
    """`span.name` alone is not enough — `span.segment` has to be outside it."""
    links = genipage.parse_relationship_path(PAGE)

    assert "6000000888888888" not in {l.geni_id for l in links}


def test_the_relation_loses_the_parentheses_that_are_markup():
    links = genipage.parse_relationship_path(PAGE)

    assert links[1].relation == "your father"


def test_the_first_step_has_no_relation():
    links = genipage.parse_relationship_path(PAGE)

    assert links[0].name == "You"
    assert links[0].relation == ""


def test_no_path_on_a_page_without_one():
    assert genipage.parse_relationship_path("<html><body>nothing</body></html>") == []


def test_tsv_carries_every_id_and_marks_the_missing_relation():
    text = genipage.to_tsv(genipage.parse_relationship_path(PAGE), header="# hi")
    rows = [line.split("\t") for line in text.splitlines() if not line.startswith("#")]

    assert rows[0] == ["step", "name", "relation_to_previous", "note"]
    assert rows[1] == ["1", "You", "-", "geni:6000000087535357291"]
    assert rows[2][3] == "geni:6000000177921459056"


@pytest.mark.skipif(SAVED is None, reason="no saved Geni page in geni_pages/")
def test_the_real_saved_page_yields_the_whole_jimmu_path():
    links = genipage.read_relationship_path(SAVED)

    assert len(links) == 83, "83 steps, not the several hundred profile links on the page"
    assert links[0].name == "You"
    assert links[0].geni_id == "6000000087535357291"
    assert links[-1].name == "Emperor Jimmu"
    assert links[-1].geni_id == "6000000001829589817"
    assert all(l.geni_id.isdigit() for l in links)
    assert all(l.relation for l in links[1:]), "every step but the first states a relation"


@pytest.mark.skipif(SAVED is None, reason="no saved Geni page in geni_pages/")
def test_the_committed_path_file_still_matches_the_saved_page():
    """`data_lake/paths/jimmu.tsv` is generated; this is what says so.

    It is committed rather than gitignored because the whole point is that the
    path survives a session, but that makes it a copy that can drift from its
    source. Re-running `path-from-html` must reproduce it exactly.
    """
    from genimerge import paths

    generated = genipage.read_relationship_path(SAVED)
    committed = paths.load_path(REPO / "data_lake" / "paths" / "jimmu.tsv")

    assert [(l.geni_id, l.name) for l in generated] == [
        (s.geni_id, s.name) for s in committed
    ]
