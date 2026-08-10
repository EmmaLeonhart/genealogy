import json
import urllib.parse

from genimerge import gedcom, reconcile
from genimerge.model import Name, build_tree
from genimerge.reconcile import Relative, name_score, normalise_name, score_pair
from genimerge.wikidata import WikidataClient

# Sverker (matched) with a father, a wife and two children.
TREE = """0 HEAD
0 @I1@ INDI
1 NAME Sverker /the Elder/
1 SEX M
1 BIRT
2 DATE 1100
1 DEAT
2 DATE 1156
1 FAMC @F9@
1 FAMS @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME Cornube /Kolsson/
1 SEX M
1 BIRT
2 DATE ABT 1070
1 FAMS @F9@
1 RFN geni:2
0 @I3@ INDI
1 NAME Ulvhild /Hakansdotter/
1 SEX F
1 BIRT
2 DATE 1095
1 FAMS @F1@
1 RFN geni:3
0 @I4@ INDI
1 NAME Karl /Sverkersson/
1 SEX M
1 BIRT
2 DATE 1130
1 FAMC @F1@
1 RFN geni:4
0 @I5@ INDI
1 NAME Helena /of Sweden/
1 SEX F
1 FAMC @F1@
1 RFN geni:5
0 @F9@ FAM
1 HUSB @I2@
1 CHIL @I1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 CHIL @I4@
1 CHIL @I5@
0 TRLR
"""


def tree():
    return build_tree(gedcom.parse(TREE).records)


def _rows(triples):
    """(item, property, other, label, birth, death, geni) -> SPARQL JSON."""
    bindings = []
    for item, prop, other, label, birth, death, geni in triples:
        row = {
            "item": {"value": f"http://www.wikidata.org/entity/{item}"},
            "rel": {"value": f"http://www.wikidata.org/prop/direct/{prop}"},
            "other": {"value": f"http://www.wikidata.org/entity/{other}"},
        }
        if label:
            row["otherLabel"] = {"value": label}
        if birth:
            row["birth"] = {"value": birth}
        if death:
            row["death"] = {"value": death}
        if geni:
            row["geni"] = {"value": geni}
        bindings.append(row)
    return json.dumps({"results": {"bindings": bindings}}).encode("utf-8")


def _client(tmp_path, responses):
    responses = list(responses)
    calls: list[str] = []
    bodies: list[str] = []

    def fetch(url, data=None, headers=None):
        calls.append(url)
        bodies.append(data.decode("utf-8") if data else "")
        return responses.pop(0) if responses else _rows([])

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=fetch, delay=0, max_backoff=0)
    client.urls_requested = calls
    client.bodies_sent = bodies
    return client


# -- name comparison ---------------------------------------------------


def test_normalisation_folds_scandinavian_letters():
    assert normalise_name("Haraldsøn Håkon Æse") == ["haraldson", "hakon", "aese"]


def test_normalisation_drops_only_connective_words():
    assert normalise_name("Sigurd II of Norway") == ["sigurd", "ii", "norway"]
    assert normalise_name("Karl av Sverige") == ["karl", "sverige"]


def test_name_score_is_containment_so_a_longer_geni_name_is_not_punished():
    # The Geni side piles on patronymics and titles the Wikidata label omits.
    score = name_score("Sigurd II Munn Haraldsøn Konge av Norge", "Sigurd II of Norway")

    assert score >= 0.6


def test_name_score_is_zero_for_unrelated_names():
    assert name_score("Ola Nilsson", "Judith of Flanders") == 0.0


def test_name_score_handles_an_empty_side():
    assert name_score("", "Anything") == 0.0


# -- pair scoring ------------------------------------------------------


def test_agreeing_dates_plus_a_partial_name_is_high_confidence():
    person = tree().people["4"]
    relative = Relative(qid="Q1", role="child", label="Karl Sverkersson",
                        birth_year=1130, death_year=1167)
    confidence, score, evidence = score_pair(person, relative)

    assert confidence == "high"
    assert "birth 1130~1130" in evidence


def test_contradicting_dates_veto_the_match_however_good_the_name():
    person = tree().people["4"]
    twin = Relative(qid="Q1", role="child", label="Karl Sverkersson", birth_year=1400)
    confidence, _score, evidence = score_pair(person, twin)

    assert confidence is None
    assert "differ by" in evidence


def test_an_approximate_date_is_given_more_room():
    # Our Cornube's birth is "ABT 1070", so 1078 should still corroborate.
    person = tree().people["2"]
    relative = Relative(qid="Q1", role="father", label="Cornube Kolsson", birth_year=1078)

    assert score_pair(person, relative)[0] == "high"


def test_a_strong_name_alone_is_high_even_with_no_dates():
    person = tree().people["5"]
    relative = Relative(qid="Q1", role="child", label="Helena of Sweden")

    assert score_pair(person, relative)[0] == "high"


def test_a_weak_name_with_no_dates_is_not_promoted():
    person = tree().people["5"]
    relative = Relative(qid="Q1", role="child", label="Ingrid Ylva")

    assert score_pair(person, relative)[0] is None


def test_years_are_read_out_of_wikidata_time_literals():
    assert reconcile._year_of("+1130-01-01T00:00:00Z") == 1130
    assert reconcile._year_of("-0044-03-15T00:00:00Z") == -44


def test_a_blank_node_where_a_date_should_be_is_ignored():
    # Wikidata returns these for "some value"; parsing one as a year would
    # invent a date that nobody asserted.
    assert reconcile._year_of("http://www.wikidata.org/.well-known/genid/abc") is None
    assert reconcile._year_of(None) is None


# -- fetching ----------------------------------------------------------


def test_relatives_are_grouped_by_item_and_role(tmp_path):
    client = _client(
        tmp_path,
        [
            _rows(
                [
                    ("Q1", "P22", "Q2", "Cornube Kolsson", "+1070-01-01T00:00:00Z", None, None),
                    ("Q1", "P26", "Q3", "Ulvhild", "+1095-01-01T00:00:00Z", None, "3"),
                    ("Q1", "P40", "Q4", "Karl Sverkersson", "+1130-01-01T00:00:00Z", None, None),
                ]
            )
        ],
    )

    relatives = reconcile.fetch_relatives(client, ["Q1"])

    assert {r.role for r in relatives["Q1"]} == {"father", "spouse", "child"}
    assert next(r for r in relatives["Q1"] if r.role == "father").birth_year == 1070
    assert next(r for r in relatives["Q1"] if r.role == "spouse").geni_id == "3"


def test_repeated_rows_for_one_relative_are_merged_not_duplicated(tmp_path):
    # An item with two birth dates produces two rows for the same relationship.
    client = _client(
        tmp_path,
        [
            _rows(
                [
                    ("Q1", "P40", "Q4", "Karl", "+1130-01-01T00:00:00Z", None, None),
                    ("Q1", "P40", "Q4", "Karl", "+1131-01-01T00:00:00Z", None, None),
                ]
            )
        ],
    )

    assert len(reconcile.fetch_relatives(client, ["Q1"])["Q1"]) == 1


def test_a_later_blank_value_does_not_erase_an_earlier_real_one(tmp_path):
    client = _client(
        tmp_path,
        [
            _rows(
                [
                    ("Q1", "P40", "Q4", "Karl", "+1130-01-01T00:00:00Z", None, None),
                    ("Q1", "P40", "Q4", "Karl", None, None, None),
                ]
            )
        ],
    )

    assert reconcile.fetch_relatives(client, ["Q1"])["Q1"][0].birth_year == 1130


# -- expansion ---------------------------------------------------------


def test_expansion_reaches_relatives_of_a_seed(tmp_path):
    client = _client(
        tmp_path,
        [
            _rows(
                [
                    ("Q1", "P22", "Q2", "Cornube Kolsson", "+1070-01-01T00:00:00Z", None, None),
                    ("Q1", "P26", "Q3", "Ulvhild Hakansdotter", "+1095-01-01T00:00:00Z", None, None),
                    ("Q1", "P40", "Q4", "Karl Sverkersson", "+1130-01-01T00:00:00Z", None, None),
                ]
            )
        ],
    )

    result = reconcile.expand_from_matches(client, tree(), {"1": "Q1"})

    assert result.confirmed == {"1": "Q1", "2": "Q2", "3": "Q3", "4": "Q4"}
    assert result.per_ring[0] == 3


def test_expansion_keeps_walking_ring_by_ring(tmp_path):
    client = _client(
        tmp_path,
        [
            _rows([("Q1", "P40", "Q4", "Karl Sverkersson", "+1130-01-01T00:00:00Z", None, None)]),
            _rows([("Q4", "P22", "Q1", "Sverker", "+1100-01-01T00:00:00Z", None, None)]),
        ],
    )

    result = reconcile.expand_from_matches(client, tree(), {"1": "Q1"})

    # Ring 2 walks back to a person already matched, so it adds nothing and the
    # walk stops rather than looping.
    assert result.confirmed == {"1": "Q1", "4": "Q4"}
    assert result.per_ring == [1, 0]


def test_one_wikidata_item_is_not_given_to_two_of_our_people(tmp_path):
    client = _client(
        tmp_path,
        [
            _rows(
                [
                    ("Q1", "P40", "Q4", "Karl Sverkersson", "+1130-01-01T00:00:00Z", None, None),
                ]
            )
        ],
    )
    result = reconcile.expand_from_matches(client, tree(), {"1": "Q1"})

    assert list(result.confirmed.values()).count("Q4") == 1


def test_a_weak_proposal_is_recorded_but_not_used_to_expand(tmp_path):
    client = _client(
        tmp_path,
        [_rows([("Q1", "P40", "Q9", "Someone Else Entirely", None, None, None)])],
    )
    result = reconcile.expand_from_matches(client, tree(), {"1": "Q1"})

    assert result.confirmed == {"1": "Q1"}
    weak = [c for c in result.candidates if c.qid == "Q9"]
    assert all(not c.accepted for c in weak)


def test_a_contradicted_proposal_is_not_recorded_at_all(tmp_path):
    client = _client(
        tmp_path,
        [_rows([("Q1", "P40", "Q9", "Karl Sverkersson", "+1500-01-01T00:00:00Z", None, None)])],
    )
    result = reconcile.expand_from_matches(client, tree(), {"1": "Q1"})

    assert result.candidates == []


def test_every_candidate_carries_the_link_it_came_through(tmp_path):
    client = _client(
        tmp_path,
        [_rows([("Q1", "P22", "Q2", "Cornube Kolsson", "+1070-01-01T00:00:00Z", None, None)])],
    )
    candidate = reconcile.expand_from_matches(client, tree(), {"1": "Q1"}).candidates[0]

    assert (candidate.role, candidate.via_geni_id, candidate.via_qid) == ("father", "1", "Q1")
    assert candidate.to_row()[0] == "2"
    assert len(candidate.to_row()) == len(reconcile.CANDIDATE_COLUMNS)


def test_expansion_with_no_seeds_does_nothing(tmp_path):
    result = reconcile.expand_from_matches(_client(tmp_path, []), tree(), {})

    assert result.confirmed == {} and result.candidates == []


# -- name search -------------------------------------------------------


def test_distance_counts_family_steps_from_the_nearest_match():
    distance = reconcile.distance_from_matched(tree(), ["1"])

    assert distance["1"] == 0          # the seed
    assert distance["2"] == 1          # father
    assert distance["3"] == 1          # wife
    assert distance["4"] == 1          # child
    assert "9" not in distance         # nobody unrelated crept in


def test_search_targets_pick_the_close_the_titled_and_the_old():
    t = tree()
    t.people["4"].events.clear()       # remove the 1130 birth: only closeness left
    targets = {p.geni_id for p in reconcile.search_targets(t, {"1": "Q1"}, max_distance=1)}

    assert "4" in targets              # one step away
    assert "2" in targets              # one step away
    assert "1" not in targets          # already matched


def test_a_distant_modern_person_is_not_worth_a_search_request():
    t = tree()
    # Nobody matched at all, so nothing is close; and this person is recent and
    # untitled, so searching their name would only return noise.
    assert reconcile.search_targets(t, {}, born_before=1000) == []


def test_search_proposals_are_never_marked_accepted(tmp_path):
    search_response = json.dumps(
        {"query": {"search": [{"title": "Q77"}]}}
    ).encode("utf-8")
    details = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q77"},
                        "itemLabel": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    }
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [search_response, details])
    t = tree()

    candidates = reconcile.search_candidates(client, t, [t.people["4"]], {})

    assert len(candidates) == 1
    assert candidates[0].confidence == "high"
    assert candidates[0].accepted is False
    assert candidates[0].role == "name-search"


def test_a_search_hit_already_claimed_by_another_match_is_skipped(tmp_path):
    client = _client(
        tmp_path, [json.dumps({"query": {"search": [{"title": "Q1"}]}}).encode("utf-8")]
    )
    t = tree()

    assert reconcile.search_candidates(client, t, [t.people["4"]], {"1": "Q1"}) == []


def test_weak_search_hits_are_dropped_rather_than_listed(tmp_path):
    search_response = json.dumps({"query": {"search": [{"title": "Q88"}]}}).encode("utf-8")
    details = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q88"},
                        "itemLabel": {"value": "Somebody Unrelated"},
                    }
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [search_response, details])
    t = tree()

    assert reconcile.search_candidates(client, t, [t.people["4"]], {}) == []


def test_name_variants_offer_several_shots_at_one_person():
    t = tree()
    variants = reconcile.name_variants(t.people["1"])

    assert "Sverker the Elder" in variants
    assert all(len(v.split()) >= 2 for v in variants)


def test_a_mononym_yields_no_variants():
    # "Olof" alone would match hundreds of unrelated people and nothing
    # downstream could tell them apart, so it is not looked up at all.
    t = tree()
    t.people["1"].names = [Name(full="Olof", given="Olof")]

    assert reconcile.name_variants(t.people["1"]) == []


def test_a_name_alone_never_reaches_high_confidence():
    # This tree is full of patronymics. Without a relationship behind it, a
    # matching string is not enough on its own.
    person = tree().people["5"]
    relative = Relative(qid="Q1", role="name-match", label="Helena of Sweden")

    assert score_pair(person, relative, structural=True)[0] == "high"
    assert score_pair(person, relative, structural=False)[0] == "medium"


def test_a_name_plus_an_agreeing_date_is_high_even_without_a_relationship():
    person = tree().people["4"]
    relative = Relative(qid="Q1", role="name-match", label="Karl Sverkersson",
                        birth_year=1130)

    assert score_pair(person, relative, structural=False)[0] == "high"


def test_scoring_can_use_the_variant_that_actually_matched():
    person = tree().people["1"]  # display name "Sverker the Elder"
    relative = Relative(qid="Q1", role="name-match", label="Sverker I of Sweden")

    plain = score_pair(person, relative, structural=False)[1]
    via_variant = score_pair(
        person, relative, person_name="Sverker I of Sweden", structural=False
    )[1]

    assert via_variant > plain


def test_several_people_sharing_one_name_are_all_downgraded(tmp_path):
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": f"http://www.wikidata.org/entity/Q{n}"},
                        "label": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    }
                    for n in (77, 78, 79)
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])
    t = tree()

    candidates = reconcile.label_candidates(client, t, [t.people["4"]], {})

    assert len(candidates) == 3
    assert {c.confidence for c in candidates} == {"medium"}
    assert all("3 Wikidata people share this name" in c.year_evidence for c in candidates)


def test_a_single_unambiguous_hit_keeps_its_confidence(tmp_path):
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q77"},
                        "label": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    }
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])
    t = tree()

    candidates = reconcile.label_candidates(client, t, [t.people["4"]], {})

    assert [c.confidence for c in candidates] == ["high"]
    assert "share this name" not in candidates[0].year_evidence


def test_label_lookup_proposes_matches_without_accepting_them(tmp_path):
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q77"},
                        "label": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    }
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])
    t = tree()

    candidates = reconcile.label_candidates(client, t, [t.people["4"]], {})

    assert [(c.qid, c.confidence, c.accepted, c.role) for c in candidates] == [
        ("Q77", "high", False, "name-match")
    ]


def test_label_lookup_batches_many_names_into_few_queries(tmp_path):
    t = tree()
    people = list(t.people.values())
    client = _client(tmp_path, [_rows([]) for _ in range(5)])

    reconcile.label_candidates(
        client, t, people, {}, languages=["en", "sv"], literals_per_query=4
    )

    # Far fewer requests than people: that is the whole point of this pass.
    assert client.requests_made <= 3


def test_a_label_hit_already_claimed_is_skipped(tmp_path):
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q1"},
                        "label": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    }
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])
    t = tree()

    assert reconcile.label_candidates(client, t, [t.people["4"]], {"1": "Q1"}) == []


def test_the_same_item_is_not_proposed_twice_for_one_person(tmp_path):
    # Two name variants can both match the same item.
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q77"},
                        "label": {"value": "Karl Sverkersson"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    },
                    {
                        "item": {"value": "http://www.wikidata.org/entity/Q77"},
                        "label": {"value": "Karl /Sverkersson/"},
                        "birth": {"value": "+1130-01-01T00:00:00Z"},
                    },
                ]
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])
    t = tree()

    assert len(reconcile.label_candidates(client, t, [t.people["4"]], {})) == 1


def test_a_quote_in_a_name_is_escaped_rather_than_ending_the_literal(tmp_path):
    # 'Knud IV "the Holy" Estridson' is a real name in this tree. Unescaped, it
    # closes the SPARQL string early and the whole batch fails to parse.
    t = tree()
    t.people["4"].names = [
        Name(full='Knud IV "the Holy" Estridson', given="Knud", surname="Estridson")
    ]
    client = _client(tmp_path, [_rows([])])

    reconcile.label_candidates(client, t, [t.people["4"]], {}, languages=["en"])
    query = urllib.parse.parse_qs(client.bodies_sent[0])["query"][0]

    assert r'\"the Holy\"' in query
    # Every literal opens and closes, so discounting the escaped quotes must
    # leave exactly two per literal.
    assert query.count('"') - query.count(r'\"') == 2 * query.count("@en")


def test_search_restricts_results_to_humans(tmp_path):
    client = _client(tmp_path, [json.dumps({"query": {"search": []}}).encode("utf-8")])

    client.search_people("Karl Sverkersson")

    # Without haswbstatement:P31=Q5 the search returns books and articles about
    # the person rather than the person, so this filter is load-bearing.
    assert "haswbstatement" in client.urls_requested[0]
    assert "P31%3DQ5" in client.urls_requested[0]
    assert "Karl+Sverkersson" in client.urls_requested[0]


# -- relatives_from_store: the 2.B port --------------------------------


class _FakeReader:
    def __init__(self, items):
        self._items = items

    def entities(self, qids):
        wanted = {str(q) for q in qids}
        return {q: e for q, e in self._items.items() if q in wanted}


def _item_claim(value, rank="normal", snaktype="value"):
    snak = {"snaktype": snaktype}
    if snaktype == "value":
        snak["datavalue"] = {"value": value}
    return {"mainsnak": snak, "rank": rank}


def _person(qid, labels=None, claims=None):
    return {
        "id": qid,
        "labels": {lang: {"value": text} for lang, text in (labels or {}).items()},
        "claims": claims or {},
    }


def test_relatives_from_store_returns_role_label_and_dates():
    reader = _FakeReader({
        "Q1": _person("Q1", claims={"P22": [_item_claim({"id": "Q2"})]}),
        "Q2": _person(
            "Q2",
            labels={"en": "Father"},
            claims={
                "P569": [_item_claim({"time": "+1150-01-01T00:00:00Z"})],
                "P570": [_item_claim({"time": "+1200-01-01T00:00:00Z"})],
                "P2600": [_item_claim("900")],
            },
        ),
    })

    got = reconcile.relatives_from_store(reader, ["Q1"])

    assert list(got) == ["Q1"]
    (rel,) = got["Q1"]
    assert (rel.qid, rel.role, rel.label) == ("Q2", "father", "Father")
    assert (rel.birth_year, rel.death_year, rel.geni_id) == (1150, 1200, "900")


def test_the_label_language_order_matches_what_sparql_asked_for():
    # en,no,nb,nn,sv,da,de,fr - so a Norwegian label wins over a German one,
    # and the candidate is scored on the same string either way.
    reader = _FakeReader({
        "Q1": _person("Q1", claims={"P26": [_item_claim({"id": "Q2"})]}),
        "Q2": _person("Q2", labels={"de": "Deutsch", "no": "Norsk"}),
    })

    (rel,) = reconcile.relatives_from_store(reader, ["Q1"])["Q1"]
    assert rel.label == "Norsk"


def test_a_preferred_relation_hides_the_normal_ones():
    reader = _FakeReader({
        "Q1": _person("Q1", claims={"P22": [
            _item_claim({"id": "Q_old"}),
            _item_claim({"id": "Q_best"}, rank="preferred"),
        ]}),
        "Q_old": _person("Q_old"),
        "Q_best": _person("Q_best"),
    })

    rels = reconcile.relatives_from_store(reader, ["Q1"])["Q1"]
    assert [r.qid for r in rels] == ["Q_best"]


def test_a_deprecated_relation_is_not_returned():
    reader = _FakeReader({
        "Q1": _person("Q1", claims={"P22": [_item_claim({"id": "Q2"}, rank="deprecated")]}),
        "Q2": _person("Q2"),
    })

    assert reconcile.relatives_from_store(reader, ["Q1"]) == {}


def test_a_relative_the_download_never_reached_is_still_an_edge():
    # Returned with QID and role and nothing else, the way the endpoint would
    # answer for an item with no label in those languages. Dropping it would
    # hide a real edge from the reconciler.
    reader = _FakeReader({
        "Q1": _person("Q1", claims={"P40": [_item_claim({"id": "Q_absent"})]}),
    })

    (rel,) = reconcile.relatives_from_store(reader, ["Q1"])["Q1"]
    assert (rel.qid, rel.role, rel.label) == ("Q_absent", "child", "")
    assert (rel.birth_year, rel.death_year, rel.geni_id) == (None, None, None)
