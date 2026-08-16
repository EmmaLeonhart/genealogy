import json

from genimerge import gedcom, namelinks
from genimerge.model import build_tree

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Eric Wade /Borsheim/
2 GIVN Eric Wade
2 SURN Borsheim
1 NAME Eric /Other/
2 GIVN Eric
2 SURN Other
1 RFN geni:1
0 @I2@ INDI
1 NAME Ragnhild Rasmusdatter /Eikeland/
2 GIVN Ragnhild Rasmusdatter
2 SURN Eikeland
1 RFN geni:2
0 @I3@ INDI
1 NAME Anders /Nyland/
2 GIVN Anders
2 SURN Nyland
1 RFN geni:3
0 TRLR
"""

ITEMS = {
    "Borsheim": [("Q100", "Q101352", "label")],
    "Eric": [("Q200", "Q12308941", "label")],
    "Wade": [("Q201", "Q202444", "label")],
    "Eikeland": [("Q102", "Q101352", "label")],
    "Ragnhild": [("Q202", "Q11879590", "label")],
    "Nyland": [("Q103", "Q101352", "label")],
    # Deliberately ambiguous.
    "Anders": [("Q300", "Q12308941", "label"), ("Q301", "Q202444", "label")],
}


def tree():
    return build_tree(gedcom.parse(TREE).records)


def build(tmp_path, linked, existing_claims=(), items=None):
    """`existing_claims` is an iterable of (qid, property).

    `build_name_links` took a `WikidataClient` and asked SPARQL which items
    already state a name. It stopped touching the network on 2026-08-15 and now
    takes that mapping directly, so the fake client this used to build is gone.
    """
    existing: dict[str, set[str]] = {}
    for qid, prop in existing_claims:
        existing.setdefault(qid, set()).add(prop)
    return namelinks.build_name_links(
        existing,
        tree(),
        linked,
        ITEMS if items is None else items,
        retrieved="2026-07-30",
    )


def test_a_surname_with_one_item_becomes_a_family_name_link(tmp_path):
    batch = build(tmp_path, {"1": "Q1"})
    family = [l for l in batch.links if l.prop == "P734"]

    assert [(l.qid, l.name_item, l.text) for l in family] == [("Q1", "Q100", "Borsheim")]


def test_given_names_become_ordered_given_name_links(tmp_path):
    batch = build(tmp_path, {"1": "Q1"})
    given = [l for l in batch.links if l.prop == "P735"]

    assert [(l.name_item, l.ordinal) for l in given] == [("Q200", 1), ("Q201", 2)]


def test_a_match_on_an_alias_only_is_not_acted_on(tmp_path):
    # An alias is a weaker assertion than a label, and this batch proposes
    # edits, so alias-only matches are reported for review instead.
    aliased = {**ITEMS, "Nyland": [("Q999", "Q101352", "alias")]}
    batch = build(tmp_path, {"3": "Q3"}, items=aliased)

    assert [l.text for l in batch.links] == []
    assert any("only as an alias" in s.reason for s in batch.skipped)


def test_a_label_match_wins_over_an_alias_match_on_the_same_text(tmp_path):
    both = {**ITEMS, "Nyland": [("Q999", "Q101352", "alias"), ("Q103", "Q101352", "label")]}
    batch = build(tmp_path, {"3": "Q3"}, items=both)

    assert [(l.text, l.name_item) for l in batch.links] == [("Nyland", "Q103")]


def test_a_single_given_name_gets_no_series_ordinal(tmp_path):
    # An ordinal on a lone value says "first of several" when there is only one.
    batch = build(
        tmp_path, {"3": "Q3"}, items={**ITEMS, "Anders": [("Q300", "Q202444", "label")]}
    )
    given = [l for l in batch.links if l.prop == "P735"]

    assert [(l.name_item, l.ordinal) for l in given] == [("Q300", None)]


def test_only_the_primary_name_record_is_used(tmp_path):
    # Eric's second NAME record says surname "Other"; order across records is
    # not meaningful, so it is not proposed.
    batch = build(tmp_path, {"1": "Q1"})

    assert "Other" not in [l.text for l in batch.links]


def test_an_ambiguous_name_is_set_aside_not_picked_between(tmp_path):
    batch = build(tmp_path, {"3": "Q3"})

    assert [l.text for l in batch.links] == ["Nyland"]
    assert any("2 name items share this text" in s.reason for s in batch.skipped)


def test_a_patronymic_is_emitted_as_P5056_not_dropped(tmp_path):
    """**This test replaces one that asserted the opposite, and the change is the
    point.** Until 2026-08-15 a patronymic in the `GIVN` field was skipped with
    "patronymic in the given-name field", because the only property available was
    `P735` given name and putting it there would have been a false claim.

    Emma's `name modelling.txt` gives a patronymic **its own property**, `P5056`
    patronym or matronym, parallel to `P735` and `P734`. There is now somewhere
    correct to put it, so discarding it is no longer right - the old test encoded
    a workaround for a missing property, not a rule about names.
    """
    items = dict(ITEMS)
    items["Rasmusdatter"] = [("Q400", "Q110874", "label")]
    batch = build(tmp_path, {"2": "Q2"}, items=items)

    patronyms = [l for l in batch.links if l.prop == namelinks.PATRONYM]
    assert [(l.text, l.name_item) for l in patronyms] == [("Rasmusdatter", "Q400")]
    assert not any(
        s.reason == "patronymic in the given-name field" for s in batch.skipped
    )


def test_the_first_given_name_carries_usual_forename(tmp_path):
    """`P7452` reason for preferred rank -> `Q3409033` usual forename, on the
    first given name only; a later one carries
    `P3831` object of statement has role -> `Q245025` middle name."""
    batch = build(tmp_path, {"1": "Q1"})
    quals = {
        st.value: dict(st.qualifiers)
        for st in namelinks.to_statements(batch)
        if st.prop == namelinks.GIVEN_NAME
    }
    assert quals["Q200"].get(namelinks.PREFERRED_RANK_REASON) == namelinks.USUAL_FORENAME
    assert quals["Q201"].get(namelinks.HAS_ROLE) == namelinks.MIDDLE_NAME
    assert namelinks.PREFERRED_RANK_REASON not in quals["Q201"]


def test_a_partly_resolvable_given_string_is_held_back_entirely(tmp_path):
    # Ragnhild resolves; Rasmusdatter does not. Proposing only Ragnhild would
    # put a wrong series ordinal on the item.
    batch = build(tmp_path, {"2": "Q2"})

    assert [l.prop for l in batch.links] == ["P734"]  # surname only
    assert any("held back" in s.reason for s in batch.skipped)


def test_an_item_that_already_states_a_family_name_is_left_alone(tmp_path):
    batch = build(tmp_path, {"1": "Q1"}, existing_claims=[("Q1", "P734")])

    assert [l.prop for l in batch.links] == ["P735", "P735"]
    assert any("already states a family name" in s.reason for s in batch.skipped)


def test_an_item_that_already_states_a_given_name_is_left_alone(tmp_path):
    batch = build(tmp_path, {"1": "Q1"}, existing_claims=[("Q1", "P735")])

    assert [l.prop for l in batch.links] == ["P734"]
    assert any("already states a given name" in s.reason for s in batch.skipped)


def test_a_name_with_no_item_at_all_is_reported_not_invented(tmp_path):
    batch = build(tmp_path, {"1": "Q1"}, items={})

    assert batch.links == []
    assert any("no Wikidata name item exists" in s.reason for s in batch.skipped)


def test_the_statements_are_well_formed(tmp_path):
    """`render_quickstatements` went with QuickStatements on 2026-08-15.

    What it rendered is still built: `to_statements` turns the batch into the
    claim model in `genimerge.claims`, which is what the JSON edit objects will
    serialise. The reference properties are plain `P854`/`P813` now — the `S`
    prefix was QuickStatements' way of marking a reference inside a flat line.
    """
    statements = namelinks.to_statements(build(tmp_path, {"1": "Q1"}))
    family = [s for s in statements if s.prop == "P734"][0]
    given = [s for s in statements if s.prop == "P735"][0]

    assert (family.qid, family.value) == ("Q1", "Q100")
    assert dict(given.qualifiers)["P1545"] == '"1"'
    # Every statement carries its source.
    for s in statements:
        refs = dict(s.references)
        assert "P854" in refs and "P813" in refs
        assert refs["P813"] == "+2026-07-30T00:00:00Z/11"


def test_an_empty_batch_yields_no_statements():
    assert namelinks.to_statements(namelinks.NameBatch()) == []


def test_the_report_states_the_rules_and_counts(tmp_path):
    text = namelinks.render_markdown(build(tmp_path, {"1": "Q1", "2": "Q2", "3": "Q3"}))

    assert "Nothing here has been sent to Wikidata" in text
    assert "Ambiguous names" in text
    assert "already exists" in text


def test_people_touched_counts_people_not_statements(tmp_path):
    batch = build(tmp_path, {"1": "Q1"})

    assert len(batch.links) == 3  # one surname, two given names
    assert batch.people_touched == 1


# -- existing_name_claims_from_store: the 2.B port ---------------------


class _FakeReader:
    def __init__(self, items):
        self._items = items

    def entities(self, qids):
        wanted = {str(q) for q in qids}
        return {q: e for q, e in self._items.items() if q in wanted}


def _claim(value, rank="normal", snaktype="value"):
    snak = {"snaktype": snaktype}
    if snaktype == "value":
        snak["datavalue"] = {"value": {"id": value}}
    return {"mainsnak": snak, "rank": rank}


def test_the_store_port_reports_which_name_properties_an_item_states():
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P735": [_claim("Q100")], "P734": [_claim("Q200")]}},
        "Q2": {"id": "Q2", "claims": {"P735": [_claim("Q100")]}},
        "Q3": {"id": "Q3", "claims": {}},
    })

    got = namelinks.existing_name_claims_from_store(reader, ["Q1", "Q2", "Q3"])

    assert got == {"Q1": {"P735", "P734"}, "Q2": {"P735"}}


def test_a_deprecated_name_claim_is_not_something_the_item_states():
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P735": [_claim("Q100", rank="deprecated")]}}
    })

    assert namelinks.existing_name_claims_from_store(reader, ["Q1"]) == {}


def test_the_values_are_never_read_so_absent_name_items_do_not_matter():
    # The name items themselves are not in the store - 0.4% of referenced
    # P735/P734 targets were present when measured. This function must still
    # answer correctly, because it only ever asks which properties exist.
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P735": [_claim("Q_not_in_store")]}}
    })

    assert namelinks.existing_name_claims_from_store(reader, ["Q1"]) == {"Q1": {"P735"}}


def test_novalue_snaks_and_absent_qids_are_missing():
    reader = _FakeReader({
        "Q1": {"id": "Q1", "claims": {"P734": [_claim(None, snaktype="novalue")]}}
    })

    assert namelinks.existing_name_claims_from_store(reader, ["Q1", "Q_absent"]) == {}
