import json
import urllib.parse

import pytest

from genimerge import gedcom, names
from genimerge.model import build_tree
from genimerge.names import build_vocabulary, is_patronymic

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Ragnhild Rasmusdatter /Eikeland/
2 GIVN Ragnhild Rasmusdatter
2 SURN Eikeland
1 NAME Ragnhild Rasmusdatter /Eikeland/
2 GIVN Ragnhild Rasmusdatter
2 SURN Eikeland
1 RFN geni:1
0 @I2@ INDI
1 NAME Torstein /Olavsson/
2 GIVN Torstein
2 SURN Olavsson
1 RFN geni:2
0 @I3@ INDI
1 NAME Eric /Borsheim/
2 GIVN Eric
2 SURN Borsheim
1 NAME Eric Wade /Borsheim/
2 GIVN Eric Wade
2 SURN Borsheim
1 RFN geni:3
0 @I4@ INDI
1 RFN geni:4
0 TRLR
"""


def vocab():
    return build_vocabulary(build_tree(gedcom.parse(TREE).records))


def test_surnames_are_collected_with_counts():
    v = vocab()

    assert set(v.surnames) == {"Eikeland", "Olavsson", "Borsheim"}
    assert v.surnames["Borsheim"].count == 1
    assert v.surnames["Eikeland"].examples == ["1"]


def test_a_person_is_counted_once_however_many_name_records_repeat_it():
    # The question is how many people would gain a link, not how many NAME
    # lines exist. Eric has two NAME records, both "Borsheim".
    assert vocab().surnames["Borsheim"].count == 1


def test_whole_given_strings_are_kept_because_geni_stores_them_that_way():
    v = vocab()

    assert "Ragnhild Rasmusdatter" in v.given_full
    assert "Eric Wade" in v.given_full


def test_given_strings_are_also_split_into_the_tokens_p735_takes():
    v = vocab()

    assert set(v.given_tokens) >= {"Ragnhild", "Rasmusdatter", "Eric", "Wade", "Torstein"}
    assert v.given_tokens["Eric"].count == 1  # one person, two NAME records


def test_people_with_no_name_at_all_are_counted_not_dropped():
    assert vocab().unnamed == 1


@pytest.mark.parametrize(
    "name",
    ["Olavsson", "Rasmusdatter", "Torsteinsson", "Gunnbjørnsdotter", "Halldorsson",
     "Jensen", "Haraldssøn", "Sigurdsdóttir"],
)
def test_patronymics_are_recognised(name):
    assert is_patronymic(name)


@pytest.mark.parametrize("name", ["Borsheim", "Eikeland", "Galte", "Smør", "Aga", "Frisk"])
def test_inherited_surnames_are_not_called_patronymic(name):
    assert not is_patronymic(name)


def test_a_very_short_name_is_not_forced_into_the_patronymic_bucket():
    assert not is_patronymic("Son")
    assert not is_patronymic("")


def test_top_can_filter_to_patronymics_or_away_from_them():
    v = vocab()

    assert [u.text for u in v.top("surnames", only="patronymic")] == ["Olavsson"]
    assert set(u.text for u in v.top("surnames", only="inherited")) == {
        "Borsheim",
        "Eikeland",
    }


def test_top_ranks_by_frequency_then_alphabetically():
    extra = TREE.replace(
        "0 @I4@ INDI\n1 RFN geni:4\n",
        "0 @I4@ INDI\n1 NAME Ola /Borsheim/\n2 SURN Borsheim\n1 RFN geni:4\n",
    )
    v = build_vocabulary(build_tree(gedcom.parse(extra).records))

    assert [u.text for u in v.top("surnames")][0] == "Borsheim"


def test_examples_are_capped_so_the_report_stays_readable():
    many = "0 HEAD\n" + "".join(
        f"0 @I{n}@ INDI\n1 NAME X /Common/\n2 SURN Common\n1 RFN geni:{n}\n"
        for n in range(1, 12)
    ) + "0 TRLR\n"
    v = build_vocabulary(build_tree(gedcom.parse(many).records))

    assert v.surnames["Common"].count == 11
    assert len(v.surnames["Common"].examples) == 5


def test_all_strings_is_one_deduplicated_list_for_lookup():
    v = vocab()
    strings = v.all_strings()

    assert strings == sorted(set(strings))
    assert "Eikeland" in strings and "Ragnhild" in strings


def test_summary_counts_are_consistent():
    summary = names.summarise(vocab())

    assert summary["surnames"]["distinct"] == 3
    assert summary["surnames"]["patronymic"] == 1
    assert summary["surnames"]["uses"] == 3


def test_an_empty_tree_yields_an_empty_vocabulary():
    from genimerge.model import Tree

    v = build_vocabulary(Tree())

    assert v.all_strings() == [] and v.unnamed == 0


# -- Wikidata lookup ---------------------------------------------------


def _client(tmp_path, responses):
    from genimerge.wikidata import WikidataClient

    responses = list(responses)
    bodies: list[str] = []

    def fetch(url, data=None, headers=None):
        bodies.append(data.decode("utf-8") if data else "")
        return responses.pop(0) if responses else json.dumps({"results": {"bindings": []}}).encode()

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=fetch, delay=0, max_backoff=0)
    client.bodies_sent = bodies
    return client


def _name_response(triples):
    return json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": f"http://www.wikidata.org/entity/{qid}"},
                        "type": {"value": f"http://www.wikidata.org/entity/{type_qid}"},
                        "label": {"value": label},
                    }
                    for label, qid, type_qid in triples
                ]
            }
        }
    ).encode("utf-8")


def test_existing_name_items_are_found_and_keyed_by_the_name(tmp_path):
    client = _client(tmp_path, [_name_response([("Borsheim", "Q1", "Q101352")])])

    found = names.find_name_items(client, ["Borsheim", "Eikeland"])

    assert found == {"Borsheim": [("Q1", "Q101352")]}


def test_the_lookup_is_restricted_to_name_items(tmp_path):
    # Without the type filter "Eikeland" matches a village and "Ragnhild" a
    # queen, and neither is something P734 or P735 could point at.
    client = _client(tmp_path, [])
    names.find_name_items(client, ["Eikeland"])
    query = urllib.parse.parse_qs(client.bodies_sent[0])["query"][0]

    assert "wd:Q101352" in query and "wd:Q202444" in query
    assert "wdt:P31 ?type" in query


def test_one_name_with_several_items_keeps_them_all(tmp_path):
    client = _client(
        tmp_path,
        [_name_response([("Anders", "Q1", "Q202444"), ("Anders", "Q2", "Q12308941")])],
    )

    assert len(names.find_name_items(client, ["Anders"])["Anders"]) == 2


def test_duplicate_rows_for_one_item_are_collapsed(tmp_path):
    client = _client(
        tmp_path,
        [_name_response([("Anders", "Q1", "Q202444"), ("Anders", "Q1", "Q202444")])],
    )

    assert names.find_name_items(client, ["Anders"]) == {"Anders": [("Q1", "Q202444")]}


def test_names_are_looked_up_in_batches_not_one_at_a_time(tmp_path):
    client = _client(tmp_path, [])

    names.find_name_items(
        client, [f"Name{n}" for n in range(20)], languages=["en"], literals_per_query=10
    )

    assert client.requests_made == 2


def test_a_quote_in_a_name_is_escaped(tmp_path):
    client = _client(tmp_path, [])

    names.find_name_items(client, ['O"Hara'], languages=["en"])
    query = urllib.parse.parse_qs(client.bodies_sent[0])["query"][0]

    assert r'O\"Hara' in query


# -- report ------------------------------------------------------------


def test_the_report_separates_names_with_and_without_items():
    v = vocab()
    text = names.render_markdown(v, {"Borsheim": [("Q1", "Q101352")]})

    assert "# Name vocabulary" in text
    assert "already have items" in text
    assert "proposes creating anything" in text


def test_the_report_ranks_missing_names_by_how_many_people_would_gain_a_link():
    v = vocab()
    text = names.render_markdown(v, {})
    surnames_section = text.split("Surnames — most common with no Wikidata item")[1]

    assert "Eikeland" in surnames_section
    assert "| 3 | 0 | 0.0% |" in text  # none of the 3 surnames have items


def test_the_report_states_the_patronymic_heuristic_is_only_grouping():
    assert "used to group" in names.render_markdown(vocab(), {})
