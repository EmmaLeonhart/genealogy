import json

from genimerge import crosscheck, gedcom
from genimerge.crosscheck import AGREES, CONFLICT, GAP, NOT_COMPARABLE
from genimerge.model import build_tree
from genimerge.wikidata import WikidataClient

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Child /Person/
1 BIRT
2 DATE 12 MAR 1150
1 DEAT
2 DATE 1200
1 FAMC @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME Father /Person/
1 FAMS @F1@
1 RFN geni:2
0 @I3@ INDI
1 NAME Mother /Person/
1 FAMS @F1@
1 RFN geni:3
0 @I4@ INDI
1 NAME Vague /Person/
1 BIRT
2 DATE ABT 1275
1 RFN geni:4
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I3@
1 CHIL @I1@
0 TRLR
"""

LINKED = {"1": "Q1", "2": "Q2", "3": "Q3"}


def tree():
    return build_tree(gedcom.parse(TREE).records)


def check(claims, linked=None):
    return crosscheck.cross_check(tree(), linked or LINKED, claims)


def find(result, geni_id, prop):
    return next(f for f in result.findings if f.geni_id == geni_id and f.prop == prop)


# -- relationships -----------------------------------------------------


def test_a_matching_father_agrees():
    result = check({"Q1": {"P22": ["Q2"]}})

    assert find(result, "1", "P22").verdict == AGREES


def test_a_father_we_know_and_wikidata_does_not_is_a_gap():
    result = check({})

    gap = find(result, "1", "P22")
    assert gap.verdict == GAP
    assert gap.target_qid == "Q2"


def test_a_different_father_is_a_conflict():
    result = check({"Q1": {"P22": ["Q999"]}})
    conflict = find(result, "1", "P22")

    assert conflict.verdict == CONFLICT
    assert (conflict.ours, conflict.theirs) == ("Q2", "Q999")


def test_a_relationship_is_not_comparable_when_the_other_person_is_unlinked():
    # We know the child's father, but he has no Wikidata item, so there is
    # nothing for P22 to point at and its absence says nothing.
    result = check({}, linked={"1": "Q1"})
    finding = find(result, "1", "P22")

    assert finding.verdict == NOT_COMPARABLE
    assert "not linked" in finding.detail


def test_a_relationship_we_simply_do_not_have_is_not_comparable():
    result = check({}, linked={"2": "Q2"})

    assert find(result, "2", "P22").verdict == NOT_COMPARABLE


def test_one_matching_spouse_among_several_counts_as_agreement():
    result = check({"Q2": {"P26": ["Q3", "Q77"]}})

    assert find(result, "2", "P26").verdict == AGREES


def test_a_gap_with_two_possible_targets_proposes_neither():
    # Two spouses on our side and none on Wikidata's: which one a single
    # statement should name is not something to guess.
    tree_two = TREE.replace(
        "0 @F1@ FAM",
        "0 @F2@ FAM\n1 HUSB @I2@\n1 WIFE @I4@\n0 @F1@ FAM",
    ).replace("1 NAME Vague /Person/", "1 NAME Vague /Person/\n1 FAMS @F2@")
    linked = {**LINKED, "4": "Q4"}
    result = crosscheck.cross_check(
        build_tree(gedcom.parse(tree_two).records), linked, {}
    )
    finding = next(f for f in result.findings if f.geni_id == "2" and f.prop == "P26")

    assert finding.verdict == GAP
    assert finding.target_qid is None


# -- dates -------------------------------------------------------------


def test_a_matching_birth_year_agrees():
    result = check({"Q1": {"P569": ["+1150-03-12T00:00:00Z"]}})

    assert find(result, "1", "P569").verdict == AGREES


def test_a_close_enough_year_still_agrees():
    result = check({"Q1": {"P569": ["+1152-01-01T00:00:00Z"]}})

    assert find(result, "1", "P569").verdict == AGREES


def test_a_distant_year_is_a_conflict():
    result = check({"Q1": {"P569": ["+1400-01-01T00:00:00Z"]}})
    conflict = find(result, "1", "P569")

    assert conflict.verdict == CONFLICT
    assert conflict.ours == "12 MAR 1150" and conflict.theirs == "1400"


def test_an_approximate_date_of_ours_is_never_a_conflict():
    # "about 1275" and "1310" do not disagree in the way two exact dates do.
    result = check({"Q4": {"P569": ["+1310-01-01T00:00:00Z"]}}, linked={"4": "Q4"})
    finding = find(result, "4", "P569")

    assert finding.verdict == NOT_COMPARABLE
    assert finding.detail == "our date is approximate"


def test_an_approximate_date_can_still_agree():
    result = check({"Q4": {"P569": ["+1278-01-01T00:00:00Z"]}}, linked={"4": "Q4"})

    assert find(result, "4", "P569").verdict == AGREES


def test_a_date_we_hold_and_wikidata_does_not_is_a_gap_carrying_the_value():
    result = check({})
    gap = find(result, "1", "P569")

    assert gap.verdict == GAP
    assert gap.target_time == "+1150-03-12T00:00:00Z"


def test_an_approximate_date_offers_no_value_to_propose():
    result = check({}, linked={"4": "Q4"})

    assert find(result, "4", "P569").target_time is None


def test_a_date_neither_side_has_is_not_comparable():
    result = check({}, linked={"2": "Q2"})

    assert find(result, "2", "P569").verdict == NOT_COMPARABLE


# -- fetching ----------------------------------------------------------


def test_claims_are_grouped_by_item_and_property(tmp_path):
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q1"},
                        "prop": {"value": "http://www.wikidata.org/prop/direct/P22"},
                        "value": {"value": "http://www.wikidata.org/entity/Q2"},
                    },
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q1"},
                        "prop": {"value": "http://www.wikidata.org/prop/direct/P569"},
                        "value": {"value": "+1150-03-12T00:00:00Z"},
                    },
                ]
            }
        }
    ).encode("utf-8")
    client = WikidataClient(
        cache_dir=tmp_path / "c", fetch=lambda *a, **k: response, delay=0, max_backoff=0
    )

    claims = crosscheck.fetch_claims(client, ["Q1"])

    assert claims == {"Q1": {"P22": ["Q2"], "P569": ["+1150-03-12T00:00:00Z"]}}


# -- report ------------------------------------------------------------


def test_the_report_leads_with_conflicts():
    text = crosscheck.render_markdown(check({"Q1": {"P22": ["Q999"]}}))

    assert "## Conflicts (1)" in text
    assert "Q999" in text
    assert text.index("## Conflicts") < text.index("## Gaps")


def test_structural_conflicts_are_listed_before_date_conflicts():
    # A different father is a disagreement about who someone is; five years on
    # a medieval birth is two sources rounding differently.
    result = check(
        {
            "Q1": {"P22": ["Q999"], "P569": ["+1160-01-01T00:00:00Z"]},
        }
    )
    text = crosscheck.render_markdown(result)
    body = text.split("## Conflicts")[1]

    assert body.index("father") < body.index("date of birth")
    assert "structural" in body


def test_a_wider_date_conflict_is_listed_before_a_narrower_one():
    result = check(
        {
            "Q1": {
                "P569": ["+1160-01-01T00:00:00Z"],  # 10 years out
                "P570": ["+1300-01-01T00:00:00Z"],  # 100 years out
            }
        }
    )
    body = crosscheck.render_markdown(result).split("## Conflicts")[1]

    assert body.index("100 yr") < body.index("10 yr")


def test_the_report_states_the_tolerance_rather_than_widening_it():
    text = crosscheck.render_markdown(check({"Q1": {"P569": ["+1160-01-01T00:00:00Z"]}}))

    assert "not widened" in text
    assert str(crosscheck.YEAR_TOLERANCE) in text


def test_the_report_says_so_when_nothing_conflicts():
    text = crosscheck.render_markdown(check({"Q1": {"P22": ["Q2"]}}))

    assert "None. Everything both sides state, they agree on." in text


# -- the claims batch --------------------------------------------------


def _batch(claims, exact, linked=None):
    result = check(claims, linked)
    return crosscheck.build_claim_batch(
        result, tree(), set(exact), retrieved="2026-07-30"
    )


def test_a_relationship_gap_between_two_exactly_linked_people_is_proposed():
    batch = _batch({}, exact={"1", "2", "3"})
    father = [s for s in batch.statements if s.prop == "P22"]

    assert [(s.qid, s.value) for s in father] == [("Q1", "Q2")]
    # Plain P854/P813: the S prefix was QuickStatements-only and went with it.
    assert all({"P854", "P813"} <= set(dict(s.references))
               for s in batch.statements)


def test_a_relationship_is_withheld_when_the_subject_is_linked_by_inference():
    batch = _batch({}, exact={"2", "3"})

    assert [s for s in batch.statements if s.prop == "P22"] == []
    assert any("this person is linked by inference" in r for _f, r in batch.withheld)


def test_a_relationship_is_withheld_when_the_other_end_is_linked_by_inference():
    # Putting an inferred parent on a real Wikidata item is the error that
    # would be hardest for anyone to notice afterwards.
    batch = _batch({}, exact={"1"})

    assert [s for s in batch.statements if s.prop == "P22"] == []
    assert any("the other person is linked by inference" in r for _f, r in batch.withheld)


def test_an_exact_date_gap_is_proposed_with_its_full_precision():
    batch = _batch({}, exact={"1", "2", "3"})
    birth = [s for s in batch.statements if s.prop == "P569" and s.qid == "Q1"]

    assert [s.value for s in birth] == ["+1150-03-12T00:00:00Z"]


def test_an_approximate_date_is_never_proposed():
    batch = _batch({}, exact={"4"}, linked={"4": "Q4"})

    assert batch.statements == []
    assert any("our date is approximate" in r for _f, r in batch.withheld)


def test_conflicts_are_never_proposed():
    batch = _batch({"Q1": {"P22": ["Q999"]}}, exact={"1", "2", "3"})

    assert all(s.prop != "P22" or s.qid != "Q1" for s in batch.statements)


def test_the_batch_report_states_the_eligibility_rules():
    text = crosscheck.render_claim_markdown(_batch({}, exact={"1", "2", "3"}))

    assert "Nothing here has been sent to Wikidata" in text
    assert "never by inference" in text
    assert "Conflicts are never proposed" in text


def test_the_summary_counts_every_property():
    counts = check({"Q1": {"P22": ["Q2"]}}).counts()

    assert counts["P22"][AGREES] == 1
    assert set(counts) == set(crosscheck.PROPERTIES)


# --- suspect links ---------------------------------------------------------
#
# The conflicts table lists one property per row, which reads as independent
# errors. Where they concentrate on one person they are not independent: the
# thing under suspicion is the link, not the four facts.


def _finding(geni_id, qid, prop, verdict, person="Someone"):
    return crosscheck.Finding(
        geni_id=geni_id, qid=qid, prop=prop, verdict=verdict, person=person
    )


def _check(*findings):
    return crosscheck.CrossCheck(findings=list(findings), people_checked=1)


def test_balance_counts_only_agreements_and_conflicts():
    """Gaps and not-comparable are evidence about coverage, not about the link."""
    check = _check(
        _finding("1", "Q1", "P22", AGREES),
        _finding("1", "Q1", "P25", CONFLICT),
        _finding("1", "Q1", "P26", GAP),
        _finding("1", "Q1", "P569", NOT_COMPARABLE),
    )

    balance = crosscheck.link_balances(check)[0]

    assert (balance.agrees, balance.conflicts) == (1, 1)
    assert balance.comparable == 2
    assert balance.margin == 0


def test_a_person_conflicting_on_everything_is_flagged():
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT, person="Canute"),
        _finding("1", "Q1", "P25", CONFLICT, person="Canute"),
        _finding("1", "Q1", "P569", CONFLICT, person="Canute"),
        _finding("1", "Q1", "P570", CONFLICT, person="Canute"),
    )

    suspect = crosscheck.suspect_links(check)

    assert [b.person for b in suspect] == ["Canute"]
    assert suspect[0].margin == 4


def test_one_conflict_alone_is_not_suspicious():
    """Two medieval sources differing on a single date is ordinary."""
    check = _check(_finding("1", "Q1", "P569", CONFLICT))

    assert crosscheck.suspect_links(check) == []


def test_a_link_that_agrees_more_than_it_conflicts_is_not_flagged():
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT),
        _finding("1", "Q1", "P25", CONFLICT),
        _finding("1", "Q1", "P26", AGREES),
        _finding("1", "Q1", "P569", AGREES),
        _finding("1", "Q1", "P570", AGREES),
    )

    assert crosscheck.suspect_links(check) == []


def test_two_people_are_tallied_separately_not_pooled():
    """One person with four conflicts is the signal; four people with one each is not."""
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT, person="A"),
        _finding("1", "Q1", "P25", CONFLICT, person="A"),
        _finding("2", "Q2", "P569", CONFLICT, person="B"),
    )

    suspect = crosscheck.suspect_links(check)

    assert [b.person for b in suspect] == ["A"]


def test_the_most_suspect_link_is_listed_first():
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT, person="Two"),
        _finding("1", "Q1", "P25", CONFLICT, person="Two"),
        _finding("2", "Q2", "P22", CONFLICT, person="Four"),
        _finding("2", "Q2", "P25", CONFLICT, person="Four"),
        _finding("2", "Q2", "P569", CONFLICT, person="Four"),
        _finding("2", "Q2", "P570", CONFLICT, person="Four"),
    )

    assert [b.person for b in crosscheck.suspect_links(check)] == ["Four", "Two"]


def test_the_report_names_the_link_kind_because_it_shifts_the_odds():
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT, person="Exact One"),
        _finding("1", "Q1", "P25", CONFLICT, person="Exact One"),
        _finding("9", "Q9", "P22", CONFLICT, person="Inferred One"),
        _finding("9", "Q9", "P25", CONFLICT, person="Inferred One"),
    )

    markdown = crosscheck.render_markdown(check, exact_links={"1"})

    assert "## Links worth re-checking (2)" in markdown
    assert "| Exact One | [Q1](https://www.wikidata.org/wiki/Q1) | 0 | 2 | exact P2600 |" in markdown
    assert "| Inferred One | [Q9](https://www.wikidata.org/wiki/Q9) | 0 | 2 | inferred |" in markdown


def test_the_report_carries_the_not_wrong_caveat():
    """Asserted by identity, so rewording the caveat does not break this."""
    check = _check(
        _finding("1", "Q1", "P22", CONFLICT),
        _finding("1", "Q1", "P25", CONFLICT),
    )

    markdown = crosscheck.render_markdown(check, exact_links={"1"})

    assert crosscheck.SUSPECT_IS_NOT_WRONG in markdown


def test_the_not_wrong_caveat_still_offers_the_second_reading():
    """Identity alone would pass on an emptied constant, so pin its substance.

    Conflicting on everything is equally what a correct link to bad data looks
    like. Drop that sentence and the section becomes a verdict it cannot support.
    """
    assert "one side's data is badly wrong" in crosscheck.SUSPECT_IS_NOT_WRONG
    assert "does not say the links are wrong" in crosscheck.SUSPECT_IS_NOT_WRONG


def test_no_suspect_links_says_so_rather_than_omitting_the_section():
    check = _check(_finding("1", "Q1", "P22", AGREES))

    markdown = crosscheck.render_markdown(check)

    assert "## Links worth re-checking (0)" in markdown
    assert crosscheck.NO_SUSPECT_LINKS in markdown


# -- claims_from_store: the 2.B port ------------------------------------


class _FakeReader:
    """Stands in for wikistore.StoreReader.entities, which is all this uses."""

    def __init__(self, items):
        self._items = items

    def entities(self, qids):
        wanted = {str(q) for q in qids}
        return {q: e for q, e in self._items.items() if q in wanted}


def _statement(value, rank="normal", snaktype="value"):
    snak = {"snaktype": snaktype}
    if snaktype == "value":
        snak["datavalue"] = {"value": value}
    return {"mainsnak": snak, "rank": rank}


def test_the_store_port_returns_what_sparql_returned():
    reader = _FakeReader({
        "Q1": {
            "id": "Q1",
            "claims": {
                "P22": [_statement({"id": "Q2"})],
                "P569": [_statement({"time": "+1150-03-12T00:00:00Z"})],
            },
        }
    })

    assert crosscheck.claims_from_store(reader, ["Q1"]) == {
        "Q1": {"P22": ["Q2"], "P569": ["+1150-03-12T00:00:00Z"]}
    }


def test_a_deprecated_statement_is_not_a_value():
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P22": [_statement({"id": "Q2"}, rank="deprecated")]}}
    })

    assert crosscheck.claims_from_store(reader, ["Q1"]) == {}


def test_a_preferred_statement_hides_the_normal_ones():
    # This is what wdt: meant. Reading every statement instead would turn a
    # superseded value into a fresh conflict for a human to adjudicate.
    reader = _FakeReader({
        "Q1": {
            "id": "Q1",
            "claims": {
                "P22": [
                    _statement({"id": "Q_old"}),
                    _statement({"id": "Q_best"}, rank="preferred"),
                ]
            },
        }
    })

    assert crosscheck.claims_from_store(reader, ["Q1"]) == {"Q1": {"P22": ["Q_best"]}}


def test_novalue_snaks_and_absent_qids_are_simply_missing():
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P22": [_statement(None, snaktype="novalue")]}}
    })

    assert crosscheck.claims_from_store(reader, ["Q1", "Q_absent"]) == {}


def test_only_the_compared_properties_come_back():
    reader = _FakeReader({
        "Q1": {
            "id": "Q1",
            "claims": {
                "P22": [_statement({"id": "Q2"})],
                "P31": [_statement({"id": "Q5"})],
            },
        }
    })

    assert crosscheck.claims_from_store(reader, ["Q1"]) == {"Q1": {"P22": ["Q2"]}}
