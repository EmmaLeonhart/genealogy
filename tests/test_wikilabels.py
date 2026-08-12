"""`genimerge.wikilabels` — the English-label resolver behind the readable pair view.

**Nothing here touches the network.** `_fetch` is replaced in every test that
would reach it, and one test asserts that a fully-cached `resolve` does not call
it at all — which is the module's central claim: one request for everything
missing, never a loop, and never a request when nothing is missing.
"""

from __future__ import annotations

import pytest

from genimerge import wikilabels


def _snak(prop: str, value=None, *, snaktype: str = "value") -> dict:
    snak: dict = {"property": prop, "snaktype": snaktype}
    if value is not None:
        snak["datavalue"] = {"value": value}
    return snak


def test_collect_ids_takes_the_property_and_the_item_it_points_at():
    entity = {"claims": {"P31": [{"mainsnak": _snak("P31", {"id": "Q5"})}]}}
    assert wikilabels.collect_ids(entity) == {"P31", "Q5"}


def test_collect_ids_walks_qualifiers_and_references_too():
    """The genealogy lives beside the value as often as in it.

    Henry III's marriage date, place and end cause are all qualifiers; a
    collector that read mainsnaks only would leave them unlabelled.
    """
    entity = {
        "claims": {
            "P26": [
                {
                    "mainsnak": _snak("P26", {"id": "Q228885"}),
                    "qualifiers": {"P2842": [_snak("P2842", {"id": "Q29265"})]},
                    "references": [{"snaks": {"P248": [_snak("P248", {"id": "Q5933"})]}}],
                }
            ]
        }
    }
    assert wikilabels.collect_ids(entity) == {"P26", "Q228885", "P2842", "Q29265", "P248", "Q5933"}


def test_collect_ids_ignores_literals_and_unknown_value_snaks():
    """A time or a string has no label, and a `somevalue` snak has no value."""
    entity = {
        "claims": {
            "P569": [{"mainsnak": _snak("P569", {"time": "+1894-04-25T00:00:00Z"})}],
            "P570": [{"mainsnak": _snak("P570", snaktype="somevalue")}],
            "P2600": [{"mainsnak": _snak("P2600", "6000000038740385839")}],
        }
    }
    assert wikilabels.collect_ids(entity) == {"P569", "P570", "P2600"}


def test_collect_ids_on_an_entity_with_no_claims():
    assert wikilabels.collect_ids({}) == set()


def test_describe_keeps_the_id_because_the_id_is_what_gets_written(tmp_path):
    cache = wikilabels.LabelCache(tmp_path / "labels.tsv")
    cache.labels["Q5"] = "human"
    assert cache.describe("Q5") == "Q5 (human)"


def test_describe_falls_back_to_the_bare_id_when_there_is_no_label(tmp_path):
    cache = wikilabels.LabelCache(tmp_path / "labels.tsv")
    assert cache.describe("Q140458948") == "Q140458948"
    assert cache["Q140458948"] == ""


def test_resolve_fetches_only_what_is_missing(tmp_path, monkeypatch):
    cache = wikilabels.LabelCache(tmp_path / "labels.tsv")
    cache.labels["Q5"] = "human"

    asked: list[list[str]] = []

    def fake_fetch(ids, attempt=1):
        asked.append(list(ids))
        return {i: f"label for {i}" for i in ids}

    monkeypatch.setattr(wikilabels, "_fetch", fake_fetch)
    added = cache.resolve(["Q5", "P31", "Q6581097"], verbose=False)

    assert asked == [["P31", "Q6581097"]], "Q5 was cached and must not be requested again"
    assert added == 2
    assert cache["Q5"] == "human"
    assert cache["P31"] == "label for P31"


def test_resolve_makes_no_request_when_everything_is_cached(tmp_path, monkeypatch):
    """The module's whole point: a second case costs nothing."""
    cache = wikilabels.LabelCache(tmp_path / "labels.tsv")
    cache.labels.update({"Q5": "human", "P31": "instance of"})

    def explode(ids, attempt=1):  # pragma: no cover - must never run
        raise AssertionError(f"resolve reached the network for {ids}")

    monkeypatch.setattr(wikilabels, "_fetch", explode)
    assert cache.resolve(["Q5", "P31"], verbose=False) == 0


def test_a_miss_is_recorded_so_it_is_not_requested_again(tmp_path, monkeypatch):
    """`Q140458948` really has no English label. Asking forever would be a loop."""
    path = tmp_path / "labels.tsv"
    cache = wikilabels.LabelCache(path)

    calls = []
    monkeypatch.setattr(wikilabels, "_fetch", lambda ids, attempt=1: calls.append(list(ids)) or {})
    assert cache.resolve(["Q140458948"], verbose=False) == 0

    reloaded = wikilabels.LabelCache(path)
    monkeypatch.setattr(
        wikilabels,
        "_fetch",
        lambda ids, attempt=1: (_ for _ in ()).throw(AssertionError("re-requested a known miss")),
    )
    assert reloaded.resolve(["Q140458948"], verbose=False) == 0
    assert calls == [["Q140458948"]]


def test_the_cache_round_trips_through_disk(tmp_path, monkeypatch):
    path = tmp_path / "labels.tsv"
    cache = wikilabels.LabelCache(path)
    monkeypatch.setattr(wikilabels, "_fetch", lambda ids, attempt=1: {"Q5": "human"})
    cache.resolve(["Q5"], verbose=False)

    assert wikilabels.LabelCache(path)["Q5"] == "human"


def test_resolve_skips_empty_ids(tmp_path, monkeypatch):
    cache = wikilabels.LabelCache(tmp_path / "labels.tsv")
    monkeypatch.setattr(
        wikilabels,
        "_fetch",
        lambda ids, attempt=1: (_ for _ in ()).throw(AssertionError("asked for nothing")),
    )
    assert cache.resolve(["", None], verbose=False) == 0


@pytest.mark.parametrize(
    "code,name",
    [(11, "day"), (10, "month"), (9, "year"), (8, "decade"), (7, "century")],
)
def test_precision_codes_are_named(code, name):
    """A year-precision date is `+1103-01-01`; without this it reads as 1 January.

    `CLAUDE.md` records a case where reading mainsnaks without their context
    reported that Wikidata held nothing when it held the answer. Precision is the
    same trap one level down.
    """
    assert wikilabels.PRECISION[code] == name
