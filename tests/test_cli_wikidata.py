"""Happy-path tests for the CLI commands that talk to Wikidata.

Branch coverage put `cli.py` at 57%, and the unexecuted ranges were exactly
these commands' bodies — the code that writes the CSV and QuickStatements files
a human then reviews. They were untestable by construction: each built its own
`WikidataClient` inline, so the injectable `fetch` the client was given for this
very purpose could not be reached. `cli.make_client` is now the seam.

Every test here substitutes a canned responder. No network.
"""

import csv
import hashlib
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

        if "COUNT(" in query and "wdt:P2600" in query:
            # overlap: the endpoint's own totals, asked for separately.
            counts = {"?item)": 4, "?g)": 5, "*)": 6}
            n = 4 if "wd:Q5" in query else next(
                (v for k, v in counts.items() if f"COUNT(DISTINCT {k}" in query
                 or f"COUNT({k}" in query),
                4,
            )
            return _bindings([{"n": {"value": str(n)}}])
        if "MD5(STR(?item))" in query:
            # overlap: all of P2600, sixteen partitions. Ada and Bo are in our
            # tree; Q9 carries a Geni ID no export here has reached.
            prefix = query.split('MD5(STR(?item)), "')[1][0]
            rows = []
            for qid, geni_id in (("Q1", "1"), ("Q2", "2"), ("Q9", "77")):
                uri = _entity(qid)
                if hashlib.md5(uri.encode()).hexdigest().startswith(prefix):
                    rows.append({"item": {"value": uri}, "g": {"value": geni_id}})
            return _bindings(rows)
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


# -- overlap -----------------------------------------------------------


def test_overlap_counts_both_directions(ws, capsys):
    assert run(ws, "overlap") == 0

    printed = capsys.readouterr().out
    # Ada and Bo are on both sides; Cy is ours alone; Q9's "77" is theirs alone.
    assert "2 in both; 1 ours only; 1 Wikidata only" in printed


def test_overlap_writes_the_report_and_the_fetched_pairs(ws):
    run(ws, "overlap")

    report = (ws["reports"] / "wikidata-overlap.md").read_text(encoding="utf-8")
    assert "of Wikidata's Geni IDs" in report

    pairs = (ws["out"] / "wikidata" / "p2600-all.tsv").read_text(encoding="utf-8")
    assert sorted(pairs.split()) == sorted(["Q1", "1", "Q2", "2", "Q9", "77"])


def test_overlap_fetches_every_partition(ws):
    run(ws, "overlap")

    partitions = [q for q in ws["fake"].queries if "MD5(STR(?item))" in q]
    assert len(partitions) == len(cli.overlap_mod.PARTITIONS)


def test_overlap_says_so_when_the_fetched_rows_miss_the_reported_total(ws, capsys):
    """The fake reports 6 statements and returns 3, which is the alarm.

    Wikidata is live, so some drift between the count query and the fetch is
    ordinary; a partition failing silently is not, and the two look identical
    without this.
    """
    run(ws, "overlap")

    assert "warning: fetched 3 statements" in capsys.readouterr().err


# -- what `reconcile` and `expand` used to leave behind ------------------
#
# Both commands were deleted on 2026-08-15: they queried Wikidata live, and
# `reconcile` searched for people by name, which Emma had ordered removed on
# 2026-08-12. The four commands below still READ the CSVs they wrote, so the
# fixture writes those files directly. The rows are exactly what the deleted
# pair produced against this fake: Ada and Bo matched by P2600, Cy reached by
# walking from Ada as her child.


def seeded(ws):
    """Write the link files by hand, as `reconcile` and `expand` once did."""
    out = ws["out"] / "wikidata"
    out.mkdir(parents=True, exist_ok=True)

    with open(out / "matched_p2600.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "qid", "wikidata_label", "wikidata_description",
                    "geni_name", "birth_year", "death_year"])
        w.writerow(["1", "Q1", "Ada of Alpha", "medieval noblewoman",
                    "Ada Alpha", "1150", ""])
        w.writerow(["2", "Q2", "Bo of Beta", "", "Bo Beta", "", ""])

    with open(out / "matched_all.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "qid", "source", "geni_name"])
        w.writerow(["1", "Q1", "P2600", "Ada Alpha"])
        w.writerow(["2", "Q2", "P2600", "Bo Beta"])
        w.writerow(["3", "Q3", "expansion", "Cy Alpha"])

    with open(out / "candidates.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "qid", "role", "via_geni_id", "confidence",
                    "used_to_expand"])
        w.writerow(["3", "Q3", "child", "1", "high", "yes"])


# -- crosscheck --------------------------------------------------------


def test_crosscheck_reports_agreements_and_gaps(ws, capsys):
    seeded(ws)
    assert run(ws, "crosscheck", "--retrieved", "2026-07-30") == 0

    out = capsys.readouterr().out
    assert "3 people:" in out
    text = (ws["reports"] / "wikidata-crosscheck.md").read_text(encoding="utf-8")
    assert "# Cross-check" in text
    assert (ws["out"] / "wikidata" / "add-claims.md").exists()


def test_crosscheck_proposes_a_date_wikidata_lacks(ws):
    seeded(ws)
    run(ws, "crosscheck", "--retrieved", "2026-07-30")

    # `add-claims.qs` was the QuickStatements rendering of this batch and went
    # with the rest of QuickStatements on 2026-08-15. The markdown carries the
    # same proposals, which is what a reviewer reads anyway.
    statements = (ws["out"] / "wikidata" / "add-claims.md").read_text(encoding="utf-8")
    # Ada's death year is ours alone, and both she and it are exact.
    assert "+1200-00-00T00:00:00Z" in statements
    # Her birth year agrees, so it is not proposed again. Checked per row:
    # the markdown lists every person, and Bo's P569 is a different gap.
    assert not [l for l in statements.splitlines()
                if "/Q1)" in l and "P569" in l]


# -- names and name-links ----------------------------------------------


def test_name_links_proposes_links_to_existing_name_items(ws):
    seeded(ws)
    assert run(ws, "name-links", "--retrieved", "2026-07-30") == 0

    report = (ws["out"] / "wikidata" / "add-names.md").read_text(encoding="utf-8")
    assert "Q900" in report  # Alpha, the family name
    assert "Q901" in report  # Ada, the given name


def test_name_links_leaves_a_name_with_no_item_alone(ws):
    seeded(ws)
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
    seeded(ws)
    for command in ("overlap", "crosscheck"):
        assert run(ws, command) == 0, command

    # Reaching here at all means nothing touched urlopen, and the fake saw the
    # traffic instead.
    assert ws["fake"].queries


# -- crosscheck --offline: the 2.B port ---------------------------------


def _store_item(qid, geni=None, claims=None):
    built = {}
    for value in geni or []:
        built.setdefault("P2600", []).append(
            {"mainsnak": {"snaktype": "value", "datavalue": {"value": value}}}
        )
    for prop, value in (claims or {}).items():
        built.setdefault(prop, []).append(
            {"mainsnak": {"snaktype": "value", "datavalue": {"value": value}}}
        )
    return {"id": qid, "claims": built}


def _offline_inputs(ws, items, pairs):
    """A store, its index and a P2600 map, wired where --offline looks."""
    import gzip

    from genimerge import wikistore

    store = ws["out"] / "store"
    store.mkdir(parents=True, exist_ok=True)
    with gzip.open(store / "items-00000.jsonl.gz", "wt", encoding="utf-8") as handle:
        for entity in items:
            handle.write(json.dumps(entity) + "\n")

    index = ws["out"] / "index.sqlite3"
    wikistore.build_index(store, index)

    pairs_file = ws["out"] / "wikidata" / "p2600-all.tsv"
    pairs_file.parent.mkdir(parents=True, exist_ok=True)
    pairs_file.write_text(
        "".join(f"{qid}\t{geni}\n" for qid, geni in pairs), encoding="utf-8", newline="\n"
    )
    return store, index


def test_crosscheck_offline_reads_the_store_and_never_the_network(ws):
    # The `ws` fixture makes urlopen explode, so passing here is itself the
    # proof that nothing reached Wikidata — the point of queue.md 2.B.
    store, index = _offline_inputs(
        ws,
        items=[
            # Ada's spouse on both sides is Bo -> AGREES.
            # Her Wikidata birth is 1400, ours is 1150 -> CONFLICT.
            _store_item("Q1", geni=["1"], claims={"P26": {"id": "Q2"}, "P569": {"time": "+1400-00-00T00:00:00Z"}}),
            _store_item("Q2", geni=["2"]),
        ],
        pairs=[("Q1", "1"), ("Q2", "2")],
    )

    code = run(ws, "crosscheck", "--offline", "--store", str(store), "--index", str(index))

    assert code == 0
    report = (ws["reports"] / "wikidata-crosscheck.md").read_text(encoding="utf-8")
    assert "Cross-check" in report
    assert "P26 spouse" in report
    # The conflict is real and reported, not smoothed away.
    assert "1400" in report


def test_crosscheck_offline_says_which_file_to_build_when_one_is_missing(ws, capsys):
    # No pairs file and no index at all.
    code = run(ws, "crosscheck", "--offline")

    assert code == 1
    err = capsys.readouterr().err
    assert "p2600-all.tsv" in err
    assert "build-p2600-all.py" in err
