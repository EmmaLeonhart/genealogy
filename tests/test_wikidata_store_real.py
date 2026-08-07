"""Assert the download stores **whole** Wikidata items, against the real store.

Emma's requirement, 2026-08-07, and the failure it guards against is expensive
rather than subtle: *"I don't want to end up running this entire thing and then
finding that suddenly all they stored was the name."* A four-hour run that
quietly kept labels and dropped claims would look like a success and be worth
nothing, and no unit test on a hand-written fixture would notice — the fixture
would be whatever shape the code produced.

So this checks the bytes on disk. `wbgetentities` is called with ``props``
omitted, which is what makes the response the full entity export; if that ever
changes to a props list, or a caller starts trimming items before storing them,
these fail.

Skipped when the store is absent, the same way the real-export tests skip
without `exports/` — the suite must run on a fresh checkout.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from genimerge import wikidownload

STORE = Path(__file__).resolve().parents[1] / "wikidata" / "items"

#: What `wbgetentities` returns for an item when nothing is selected away. The
#: three that matter most are `claims`, `sitelinks` and `aliases`: they are the
#: bulk of an item and the first things a `props` parameter would drop.
FULL_ITEM_KEYS = {
    "pageid",
    "ns",
    "title",
    "lastrevid",
    "modified",
    "type",
    "id",
    "labels",
    "descriptions",
    "aliases",
    "claims",
    "sitelinks",
}


def stored_items():
    shards = sorted(STORE.glob("items-*.jsonl.gz"))
    if not shards:
        pytest.skip(f"no downloaded items under {STORE}")
    for shard in shards:
        with gzip.open(shard, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


@pytest.fixture(scope="module")
def items():
    return list(stored_items())


def test_every_stored_item_carries_the_full_entity_shape(items):
    missing = {}
    for item in items:
        absent = FULL_ITEM_KEYS - set(item)
        if absent:
            missing[item.get("id", "?")] = sorted(absent)
    assert not missing, f"items stored without every top-level key: {list(missing.items())[:5]}"


def test_claims_are_stored_in_full_not_summarised(items):
    # A statement carries its mainsnak, and the ones that matter carry
    # qualifiers and references too. Storing only the value would halve the
    # item and lose every date qualifier the QuickStatements work needs.
    seen_qualifiers = seen_references = 0
    for item in items:
        for statements in item["claims"].values():
            for statement in statements:
                assert "mainsnak" in statement, f"{item['id']} has a claim with no mainsnak"
                seen_qualifiers += bool(statement.get("qualifiers"))
                seen_references += bool(statement.get("references"))
    assert seen_qualifiers, "no qualifier survived anywhere in the store"
    assert seen_references, "no reference survived anywhere in the store"


def test_the_store_is_not_a_thin_slice_of_wikidata(items):
    # 770 distinct properties over the first 1,000 items. A store holding only
    # the handful this repo currently reads would pass every other test here.
    properties = {prop for item in items for prop in item["claims"]}
    assert len(properties) > 100, f"only {len(properties)} distinct properties in the whole store"


def test_the_seed_items_carry_the_geni_id_they_were_selected_for(items):
    # The seed list is every QID with P2600. An item stored without it means
    # the wrong thing was fetched, or the P2600 map has drifted from Wikidata.
    # Expansion items legitimately have none, so this is a floor, not a rule.
    with_geni = sum(1 for item in items if "P2600" in item["claims"])
    assert with_geni > len(items) * 0.5, f"only {with_geni} of {len(items)} carry P2600"


def test_relatives_finds_family_links_in_the_real_items(items):
    # The walk's expansion depends on this reading real Wikidata JSON, not the
    # shape a fixture happens to have.
    with_family = sum(1 for item in items if wikidownload.relatives(item))
    assert with_family > len(items) * 0.5, f"only {with_family} of {len(items)} name any relative"
