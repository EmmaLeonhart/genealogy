"""Tests for the Wikidata client — no network involved.

`WikidataClient` takes its `fetch` as a parameter precisely so these can run
offline and in CI. What is worth testing here is the batching, the caching, the
retry policy and the parsing; whether Wikidata is up is not our business.
"""

import json
import urllib.error

import pytest

from genimerge import wikidata
from genimerge.wikidata import Match, WikidataClient


def _sparql_response(pairs):
    return json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": f"http://www.wikidata.org/entity/{qid}"},
                        "geni": {"value": geni},
                    }
                    for geni, qid in pairs
                ]
            }
        }
    ).encode("utf-8")


class Recorder:
    """A stand-in for the network that remembers what it was asked."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, url, data=None, headers=None):
        self.calls.append((url, data.decode("utf-8") if data else None, headers))
        return self.responses.pop(0)


def _client(tmp_path, responses, **kwargs):
    # max_backoff=0 so a retry test does not actually sleep.
    kwargs.setdefault("max_backoff", 0)
    return WikidataClient(
        cache_dir=tmp_path / "cache", fetch=Recorder(responses), delay=0, **kwargs
    )


def test_a_query_returns_flattened_bindings(tmp_path):
    client = _client(tmp_path, [_sparql_response([("100", "Q1")])])

    assert client.sparql("SELECT ...") == [
        {"item": "http://www.wikidata.org/entity/Q1", "geni": "100"}
    ]


def test_a_repeated_query_is_served_from_disk_not_the_network(tmp_path):
    client = _client(tmp_path, [_sparql_response([("100", "Q1")])])
    first = client.sparql("SELECT ...")
    second = client.sparql("SELECT ...")

    assert first == second
    assert client.requests_made == 1
    assert client.cache_hits == 1


def test_the_cache_survives_a_new_client(tmp_path):
    _client(tmp_path, [_sparql_response([("100", "Q1")])]).sparql("SELECT ...")
    # No responses left: if this reached the network it would raise IndexError.
    fresh = _client(tmp_path, [])

    assert fresh.sparql("SELECT ...") == [
        {"item": "http://www.wikidata.org/entity/Q1", "geni": "100"}
    ]
    assert fresh.requests_made == 0


def test_different_queries_do_not_share_a_cache_entry(tmp_path):
    client = _client(
        tmp_path, [_sparql_response([("100", "Q1")]), _sparql_response([("200", "Q2")])]
    )

    assert client.sparql("query A")[0]["geni"] == "100"
    assert client.sparql("query B")[0]["geni"] == "200"


def test_a_query_is_posted_so_a_long_values_clause_still_fits(tmp_path):
    client = _client(tmp_path, [_sparql_response([])])
    client.sparql("SELECT ...")
    url, body, _ = client.fetch.calls[0]

    assert url == wikidata.SPARQL_ENDPOINT
    assert body is not None and "query=SELECT" in body


def test_requests_identify_the_tool(tmp_path):
    # Wikimedia asks for a descriptive User-Agent; anonymous scripts get blocked.
    assert "genimerge" in wikidata.USER_AGENT


def test_ids_are_queried_in_batches(tmp_path):
    ids = [str(n) for n in range(1, 11)]
    client = _client(tmp_path, [_sparql_response([]) for _ in range(4)])

    wikidata.match_by_geni_id(client, ids, batch_size=3)

    assert client.requests_made == 4  # 3 + 3 + 3 + 1


def test_matches_are_collected_across_batches(tmp_path):
    client = _client(
        tmp_path,
        [_sparql_response([("1", "Q1")]), _sparql_response([("3", "Q3")])],
    )

    matches = wikidata.match_by_geni_id(client, ["1", "2", "3", "4"], batch_size=2)

    assert sorted((m.geni_id, m.qid) for m in matches) == [("1", "Q1"), ("3", "Q3")]


def test_duplicate_input_ids_are_asked_about_once(tmp_path):
    client = _client(tmp_path, [_sparql_response([("1", "Q1")])])

    matches = wikidata.match_by_geni_id(client, ["1", "1", "1"], batch_size=10)

    assert client.requests_made == 1
    assert len(matches) == 1


def test_one_geni_id_matching_two_items_is_reported_as_two_matches(tmp_path):
    # Collapsing this to a dict would hide the case a human most needs to see:
    # two Wikidata items claiming the same Geni profile.
    client = _client(tmp_path, [_sparql_response([("1", "Q1"), ("1", "Q2")])])

    matches = wikidata.match_by_geni_id(client, ["1"])

    assert sorted(m.qid for m in matches) == ["Q1", "Q2"]


def test_no_matches_means_no_matches_not_an_error(tmp_path):
    client = _client(tmp_path, [_sparql_response([])])

    assert wikidata.match_by_geni_id(client, ["9999"]) == []


def test_progress_is_reported_per_batch(tmp_path):
    seen = []
    client = _client(tmp_path, [_sparql_response([]) for _ in range(3)])

    wikidata.match_by_geni_id(
        client, ["1", "2", "3"], batch_size=1, progress=lambda i, n: seen.append((i, n))
    )

    assert seen == [(1, 3), (2, 3), (3, 3)]


def test_a_throttled_request_is_retried(tmp_path):
    class Flaky:
        def __init__(self):
            self.attempts = 0

        def __call__(self, url, data=None, headers=None):
            self.attempts += 1
            if self.attempts == 1:
                raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)
            return _sparql_response([("1", "Q1")])

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=Flaky(), delay=0, max_backoff=0)

    assert client.sparql("SELECT ...")[0]["geni"] == "1"
    assert client.fetch.attempts == 2


def test_a_client_error_is_raised_immediately_rather_than_retried(tmp_path):
    def bad_request(url, data=None, headers=None):
        raise urllib.error.HTTPError(url, 400, "Bad Request", {}, None)

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=bad_request, delay=0)

    with pytest.raises(urllib.error.HTTPError):
        client.sparql("SELECT ...")
    assert client.requests_made == 1


def test_a_retry_after_header_is_obeyed(tmp_path):
    # Wikimedia says how long to wait; ignoring it just gets the retry rejected.
    error = urllib.error.HTTPError(
        "u", 429, "Too Many Requests", {"Retry-After": "7"}, None
    )
    client = WikidataClient(cache_dir=tmp_path / "c", fetch=lambda *a: b"", delay=0.5)

    assert client._backoff(0, error) == 7.0


def test_backoff_without_a_header_grows_from_a_floor_not_from_the_delay(tmp_path):
    # A fast run must not back off faster than a slow one.
    quick = WikidataClient(cache_dir=tmp_path / "a", fetch=lambda *a: b"", delay=0.1)
    slow = WikidataClient(cache_dir=tmp_path / "b", fetch=lambda *a: b"", delay=5.0)

    assert quick._backoff(0) == 2.0
    assert quick._backoff(2) == 8.0
    assert slow._backoff(0) == 5.0


def test_backoff_is_capped(tmp_path):
    client = WikidataClient(cache_dir=tmp_path / "c", fetch=lambda *a: b"", delay=1, max_backoff=10)

    assert client._backoff(20) == 10


def test_throttling_is_counted_so_a_slow_run_is_explainable(tmp_path):
    class Once:
        def __init__(self):
            self.n = 0

        def __call__(self, url, data=None, headers=None):
            self.n += 1
            if self.n == 1:
                raise urllib.error.HTTPError(url, 429, "slow down", {}, None)
            return _sparql_response([])

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=Once(), delay=0, max_backoff=0)
    client.sparql("SELECT ...")

    assert client.throttled == 1


def test_persistent_failure_gives_up_with_a_clear_error(tmp_path):
    def always_down(url, data=None, headers=None):
        raise urllib.error.HTTPError(url, 503, "Service Unavailable", {}, None)

    client = WikidataClient(cache_dir=tmp_path / "c", fetch=always_down, delay=0, retries=2, max_backoff=0)

    with pytest.raises(RuntimeError, match="giving up"):
        client.sparql("SELECT ...")


def test_labels_are_attached_to_matches(tmp_path):
    response = json.dumps(
        {
            "entities": {
                "Q1": {
                    "labels": {"en": {"value": "Harald Fairhair"}},
                    "descriptions": {"en": {"value": "king of Norway"}},
                }
            }
        }
    ).encode("utf-8")
    client = _client(tmp_path, [response])

    labelled = wikidata.add_labels(client, [Match(geni_id="1", qid="Q1")])

    assert labelled[0].label == "Harald Fairhair"
    assert labelled[0].description == "king of Norway"


def test_a_match_with_no_label_gets_an_empty_one_not_a_crash(tmp_path):
    client = _client(tmp_path, [json.dumps({"entities": {"Q1": {}}}).encode("utf-8")])

    labelled = wikidata.add_labels(client, [Match(geni_id="1", qid="Q1")])

    assert labelled[0].label == ""
