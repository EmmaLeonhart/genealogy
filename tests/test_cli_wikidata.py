"""Happy-path tests for the CLI commands that talk to Wikidata.

Branch coverage put `cli.py` at 57%, and the unexecuted ranges were exactly
these commands' bodies — the code that writes the CSV and QuickStatements files
a human then reviews. They were untestable by construction: each built its own
`WikidataClient` inline, so the injectable `fetch` the client was given for this
very purpose could not be reached. `cli.make_client` is now the seam.

Every test here substitutes a canned responder. No network.
"""

import csv
import json
import urllib.request

import pytest

from conftest import run_cli

from genimerge import cli, wikidata

# Ada and Bo are on Wikidata (Q1, Q2); Cy and Di are not.
LAKE = """0 HEAD
1 SOUR Geni.com
0 @I1@ INDI
1 NAME Ada /Alpha/
2 GIVN Ada
2 SURN Alpha
1 SEX F
1 BIRT
2 DATE 1150
1 DEAT
2 DATE 1200
1 FAMS @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME Bo /Beta/
2 GIVN Bo
2 SURN Beta
1 SEX M
1 BIRT
2 DATE 1145
1 FAMS @F1@
1 RFN geni:2
0 @I3@ INDI
1 NAME Cy /Alpha/
2 GIVN Cy
2 SURN Alpha
1 FAMC @F1@
1 RFN geni:3
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I1@
1 CHIL @I3@
0 TRLR
"""


def _bindings(rows):
    return json.dumps({"results": {"bindings": rows}}).encode("utf-8")


def _entity(qid):
    return f"http://www.wikidata.org/entity/{qid}"


class FakeWikidata:
    """Answers each query shape with something plausible and fixed.

    Dispatches on what the query asks for rather than on call order, so a test
    does not silently depend on how many requests a command happens to make.
    """

    def __init__(self):
        self.queries: list[str] = []

    def __call__(self, url, data=None, headers=None):
        if data is None:  # the entity API, used for labels
            return json.dumps(
                {
                    "entities": {
                        "Q1": {
                            "labels": {"en": {"value": "Ada of Alpha"}},
                            "descriptions": {"en": {"value": "medieval noblewoman"}},
                        },
                        "Q2": {"labels": {"en": {"value": "Bo of Beta"}}},
                    }
                }
            ).encode("utf-8")

        import urllib.parse

        query = urllib.parse.parse_qs(data.decode("utf-8"))["query"][0]
        self.queries.append(query)

        if "wdt:P2600 ?geni" in query and "VALUES ?geni" in query:
            # reconcile: which of our IDs does Wikidata know?
            return _bindings(
                [
                    {"item": {"value": _entity("Q1")}, "geni": {"value": "1"}},
                    {"item": {"value": _entity("Q2")}, "geni": {"value": "2"}},
                ]
            )
        if "?item ?rel ?other" in query:
            # expand: Ada's relatives. Cy is her child and is not yet linked.
            return _bindings(
                [
                    {
                        "item": {"value": _entity("Q1")},
                        "rel": {"value": "http://www.wikidata.org/prop/direct/P40"},
                        "other": {"value": _entity("Q3")},
                        "otherLabel": {"value": "Cy Alpha"},
                    }
                ]
            )
        if "wdt:P31 ?type" in query:
            # names / name-links: which name strings have name items?
            return _bindings(
                [
                    {
                        "item": {"value": _entity("Q900")},
                        "type": {"value": _entity("Q101352")},
                        "label": {"value": "Alpha"},
                    },
                    {
                        "item": {"value": _entity("Q901")},
                        "type": {"value": _entity("Q11879590")},
                        "label": {"value": "Ada"},
                    },
                ]
            )
        if "VALUES ?prop" in query and "P735" in query:
            return _bindings([])  # no item states a name yet
        if "VALUES ?prop" in query:
            # crosscheck: Wikidata knows Ada's birth year and nothing else.
            return _bindings(
                [
                    {
                        "item": {"value": _entity("Q1")},
                        "prop": {"value": "http://www.wikidata.org/prop/direct/P569"},
                        "value": {"value": "+1150-01-01T00:00:00Z"},
                    }
                ]
            )
        if "wdt:P2600 ?geni" in query:
            return _bindings([])  # quickstatements: no item has a Geni ID yet
        return _bindings([])


@pytest.fixture
def ws(tmp_path, monkeypatch):
    lake = tmp_path / "lake"
    lake.mkdir()
    (lake / "one.ged").write_text(LAKE, encoding="utf-8", newline="\n")

    # Make the real network explode. Any command that bypasses the seam and
    # builds its own client fails loudly here instead of quietly reaching
    # Wikidata and leaving these tests only looking offline.
    #
    # Patched at `urllib.request.urlopen`, not at `wikidata._http_fetch`:
    # `WikidataClient.fetch` defaults to the *function object* captured when the
    # dataclass was defined, so rebinding the module name would not affect a
    # client built with the default and the guard would never fire.
    def forbidden(*args, **kwargs):
        raise AssertionError("something bypassed cli.make_client and hit the network")

    monkeypatch.setattr(urllib.request, "urlopen", forbidden)

    fake = FakeWikidata()
    monkeypatch.setattr(
        cli,
        "make_client",
        lambda workspace, args: wikidata.WikidataClient(
            cache_dir=workspace.cache, fetch=fake, delay=0, max_backoff=0
        ),
    )
    return {
        "lake": lake,
        "out": tmp_path / "out",
        "reports": tmp_path / "reports",
        "fake": fake,
    }


#: Shared with test_cli.py -- see tests/conftest.py for why.
run = run_cli


def rows(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


# -- reconcile ---------------------------------------------------------


def test_reconcile_writes_the_matches_it_found(ws):
    assert run(ws, "reconcile") == 0

    matched = rows(ws["out"] / "wikidata" / "matched_p2600.csv")
    assert [(r["geni_id"], r["qid"]) for r in matched] == [("1", "Q1"), ("2", "Q2")]


def test_reconcile_carries_both_sides_of_each_match(ws):
    run(ws, "reconcile")
    ada = rows(ws["out"] / "wikidata" / "matched_p2600.csv")[0]

    assert ada["wikidata_label"] == "Ada of Alpha"
    assert ada["wikidata_description"] == "medieval noblewoman"
    assert ada["geni_name"] == "Ada Alpha"
    assert ada["birth_year"] == "1150"


def test_reconcile_reports_what_it_did(ws, capsys):
    run(ws, "reconcile")

    assert "2 of 3 people matched by P2600" in capsys.readouterr().out


# -- expand ------------------------------------------------------------


def test_expand_walks_to_an_unlinked_relative(ws):
    run(ws, "reconcile")
    assert run(ws, "expand") == 0

    linked = rows(ws["out"] / "wikidata" / "matched_all.csv")
    by_id = {r["geni_id"]: r for r in linked}
    assert by_id["3"]["qid"] == "Q3"
    assert by_id["3"]["source"] == "expansion"
    assert by_id["1"]["source"] == "P2600"


def test_expand_records_its_candidates_with_evidence(ws):
    run(ws, "reconcile")
    run(ws, "expand")

    candidates = rows(ws["out"] / "wikidata" / "candidates.csv")
    cy = next(c for c in candidates if c["geni_id"] == "3")
    assert cy["role"] == "child"
    assert cy["via_geni_id"] == "1"
    assert cy["used_to_expand"] == "yes"


# -- coverage ----------------------------------------------------------


def test_coverage_reports_both_link_sources_separately(ws):
    run(ws, "reconcile")
    run(ws, "expand")
    assert run(ws, "coverage") == 0

    text = (ws["reports"] / "wikidata-coverage.md").read_text(encoding="utf-8")
    assert "| **linked by P2600** (exact Geni ID on the Wikidata item) | 2 |" in text
    assert "| **linked, total** | 3 |" in text


# -- quickstatements ---------------------------------------------------


def test_quickstatements_proposes_the_geni_id_for_the_expansion_match(ws):
    run(ws, "reconcile")
    run(ws, "expand")
    assert run(ws, "quickstatements", "--retrieved", "2026-07-30") == 0

    line = (ws["out"] / "wikidata" / "add-p2600.qs").read_text(encoding="utf-8").strip()
    assert line.split("\t")[:3] == ["Q3", "P2600", '"3"']
    assert "Nothing here has been sent to Wikidata" in (
        ws["out"] / "wikidata" / "add-p2600.md"
    ).read_text(encoding="utf-8")


# -- crosscheck --------------------------------------------------------


def test_crosscheck_reports_agreements_and_gaps(ws, capsys):
    run(ws, "reconcile")
    run(ws, "expand")
    assert run(ws, "crosscheck", "--retrieved", "2026-07-30") == 0

    out = capsys.readouterr().out
    assert "3 people:" in out
    text = (ws["reports"] / "wikidata-crosscheck.md").read_text(encoding="utf-8")
    assert "# Cross-check" in text
    assert (ws["out"] / "wikidata" / "add-claims.qs").exists()


def test_crosscheck_proposes_a_date_wikidata_lacks(ws):
    run(ws, "reconcile")
    run(ws, "expand")
    run(ws, "crosscheck", "--retrieved", "2026-07-30")

    statements = (ws["out"] / "wikidata" / "add-claims.qs").read_text(encoding="utf-8")
    # Ada's death year is ours alone, and both she and it are exact.
    assert "Q1\tP570\t+1200-00-00T00:00:00Z" in statements
    # Her birth year agrees, so it is not proposed again.
    assert "Q1\tP569" not in statements


# -- names and name-links ----------------------------------------------


def test_names_measures_the_vocabulary_against_wikidata(ws, capsys):
    assert run(ws, "names") == 0

    text = (ws["reports"] / "names.md").read_text(encoding="utf-8")
    assert "# Name vocabulary" in text
    assert "surnames:" in capsys.readouterr().out


def test_name_links_proposes_links_to_existing_name_items(ws):
    run(ws, "reconcile")
    run(ws, "expand")
    assert run(ws, "name-links", "--retrieved", "2026-07-30") == 0

    statements = (ws["out"] / "wikidata" / "add-names.qs").read_text(encoding="utf-8")
    assert "Q1\tP734\tQ900" in statements  # Alpha, the family name
    assert "Q1\tP735\tQ901" in statements  # Ada, the given name


def test_name_links_leaves_a_name_with_no_item_alone(ws):
    run(ws, "reconcile")
    run(ws, "expand")
    run(ws, "name-links", "--retrieved", "2026-07-30")

    report = (ws["out"] / "wikidata" / "add-names.md").read_text(encoding="utf-8")
    # "Beta" and "Bo" have no name item in the fake, so they are set aside.
    assert "no Wikidata name item exists" in report


# -- the seam itself ---------------------------------------------------


def test_the_offline_guard_actually_fires(ws):
    """Prove the guard is live, so the rest of this file means something.

    A client built the ordinary way — the way a command that ignored the seam
    would build one — must hit the patched network and fail.
    """
    default_client = wikidata.WikidataClient(cache_dir=ws["out"] / "c", delay=0)

    with pytest.raises(AssertionError, match="hit the network"):
        default_client.sparql("SELECT * WHERE { ?s ?p ?o }")


def test_every_command_went_through_the_seam(ws):
    for command in ("reconcile", "expand", "coverage", "names"):
        assert run(ws, command) == 0, command

    # Reaching here at all means nothing touched urlopen, and the fake saw the
    # traffic instead.
    assert ws["fake"].queries
