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
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from genimerge import wikidownload

#: **Marked `slow`.** This module works over the whole corpus and takes minutes,
#: not seconds; measured over 100s on its own, 2026-08-16. It is NOT skipped by
#: default — a bare `pytest` runs it, and a run that has not is not a full
#: verification. `-m "not slow"` is a deliberate opt-out for a fast signal.
pytestmark = pytest.mark.slow

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


#: Enough offenders to diagnose from, without accumulating a million of them.
EXAMPLE_LIMIT = 5


@dataclass
class _Scan:
    """Everything the tests below assert, accumulated in a single pass.

    The store is read **streaming**, and this holds aggregates rather than the
    items themselves. The fixture used to be ``list(stored_items())``, which
    was fine against the pilot store and does not survive the real one: at
    1,408 shards and ~1.4M items that list is tens of gigabytes of dicts, and
    on 2026-08-09 it took the whole suite down twice — killed at 99% with no
    summary line, which reads as a hang rather than as the memory exhaustion
    it is.

    Every stored item is still examined one at a time, so what is asserted is
    unchanged; only the retention is. Keep it that way — sampling the store
    would silently retire the guarantee Emma asked for in the module docstring.
    """

    total: int = 0
    missing_count: int = 0
    missing_keys: dict = field(default_factory=dict)
    claims_without_mainsnak: list = field(default_factory=list)
    seen_qualifiers: int = 0
    seen_references: int = 0
    properties: set = field(default_factory=set)
    with_geni: int = 0
    with_family: int = 0
    #: Seed QIDs that are in the store but carry no P2600 — the real invariant
    #: behind `test_the_seed_items_carry_the_geni_id_they_were_selected_for`.
    #: Offenders only, never the seed set itself; see the retention note above.
    seeds_without_geni: list = field(default_factory=list)
    seeds_checked: int = 0


#: The seed list: every QID Wikidata states a P2600 for. Written by
#: `genimerge overlap`, or rebuilt offline by `scripts/build-p2600-all.py`.
#: `qid<TAB>geni_id`, no header — *not* `p2600-map.tsv`, which is the other way
#: round and carries one.
SEED_FILE = Path(__file__).resolve().parents[1] / "out" / "wikidata" / "p2600-all.tsv"


def _seed_qids() -> set[str] | None:
    """Every QID in the seed file, or None when `out/` is empty.

    `out/` is gitignored, so a fresh checkout has no seed file and the precise
    invariant cannot be checked there. That is why the floor below is asserted
    unconditionally rather than only when this returns a set.
    """
    if not SEED_FILE.exists():
        return None
    qids: set[str] = set()
    with SEED_FILE.open(encoding="utf-8") as handle:
        for line in handle:
            qid, _, _ = line.partition("\t")
            if qid.startswith("Q"):
                qids.add(qid)
    return qids or None


@pytest.fixture(scope="module")
def scan():
    stats = _Scan()
    seeds = _seed_qids()
    for item in stored_items():
        stats.total += 1
        if seeds is not None and item.get("id") in seeds:
            stats.seeds_checked += 1
            if "P2600" not in (item.get("claims") or {}):
                if len(stats.seeds_without_geni) < EXAMPLE_LIMIT:
                    stats.seeds_without_geni.append(item.get("id", "?"))
        absent = FULL_ITEM_KEYS - set(item)
        if absent:
            stats.missing_count += 1
            if len(stats.missing_keys) < EXAMPLE_LIMIT:
                stats.missing_keys[item.get("id", "?")] = sorted(absent)
        # `.get`, not `[...]`: a missing `claims` is precisely what the
        # full-shape test detects, and indexing here would turn that finding
        # into a fixture error that fails all five tests with one message.
        claims = item.get("claims") or {}
        stats.properties.update(claims)
        for statements in claims.values():
            for statement in statements:
                if "mainsnak" not in statement and len(stats.claims_without_mainsnak) < EXAMPLE_LIMIT:
                    stats.claims_without_mainsnak.append(item.get("id", "?"))
                stats.seen_qualifiers += bool(statement.get("qualifiers"))
                stats.seen_references += bool(statement.get("references"))
        stats.with_geni += "P2600" in claims
        stats.with_family += bool(wikidownload.relatives(item))
    return stats


def test_every_stored_item_carries_the_full_entity_shape(scan):
    assert not scan.missing_keys, (
        f"{scan.missing_count} of {scan.total} items stored without every "
        f"top-level key: {list(scan.missing_keys.items())}"
    )


def test_claims_are_stored_in_full_not_summarised(scan):
    # A statement carries its mainsnak, and the ones that matter carry
    # qualifiers and references too. Storing only the value would halve the
    # item and lose every date qualifier the QuickStatements work needs.
    assert not scan.claims_without_mainsnak, f"claims with no mainsnak on: {scan.claims_without_mainsnak}"
    assert scan.seen_qualifiers, "no qualifier survived anywhere in the store"
    assert scan.seen_references, "no reference survived anywhere in the store"


def test_the_store_is_not_a_thin_slice_of_wikidata(scan):
    # 770 distinct properties over the first 1,000 items. A store holding only
    # the handful this repo currently reads would pass every other test here.
    assert len(scan.properties) > 100, f"only {len(scan.properties)} distinct properties in the whole store"


def test_the_seed_items_carry_the_geni_id_they_were_selected_for(scan):
    # An item fetched as a seed but stored without P2600 means the wrong thing
    # was fetched, or the seed map has drifted from Wikidata.
    #
    # This used to read `scan.with_geni > scan.total * 0.5`. That was a proxy,
    # and it expired: it holds only while the store is seed-dominated, and the
    # expansion walk has since overtaken the seed phase — 514,903 of 1,408,401,
    # 36.6%, on 2026-08-09. The download was right and the assertion was wrong.
    # Lowering the ratio to something that passes today would retire the guard
    # instead of replacing it, so it is replaced by the two checks below.

    # 1. An absolute floor, asserted everywhere including a fresh checkout.
    #    Deliberately far under the ~515k actually stored: this catches a seed
    #    phase that collapsed, not one that grew.
    assert scan.with_geni >= 500_000, f"only {scan.with_geni} of {scan.total} carry P2600"

    # 2. The real invariant, whenever the seed list is on disk. `out/` is
    #    gitignored, so this half is absent on a fresh checkout — which is
    #    exactly why it does not stand alone.
    if scan.seeds_checked:
        assert not scan.seeds_without_geni, (
            f"{len(scan.seeds_without_geni)}+ seed items stored without P2600, "
            f"starting with {scan.seeds_without_geni}"
        )


def test_relatives_finds_family_links_in_the_real_items(scan):
    # The walk's expansion depends on this reading real Wikidata JSON, not the
    # shape a fixture happens to have.
    assert scan.with_family > scan.total * 0.5, f"only {scan.with_family} of {scan.total} name any relative"
