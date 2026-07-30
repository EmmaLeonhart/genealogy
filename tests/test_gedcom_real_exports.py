"""Integration check against the actual Geni exports in `data_lake/`.

The unit tests in `test_gedcom.py` use hand-written fixtures. This file exists
because the fixtures are what we *think* Geni emits, and these files are what it
*actually* emitted — the U+2028 handling in `parse` was found here, not there.

Skips when the exports are absent so a checkout without `data_lake/` still runs.
"""

from pathlib import Path

import pytest

from genimerge import gedcom

DATA_LAKE = Path(__file__).resolve().parents[1] / "data_lake"
EXPORTS = sorted(DATA_LAKE.glob("*.ged"))

pytestmark = pytest.mark.skipif(not EXPORTS, reason="no GEDCOM exports in data_lake/")


@pytest.fixture(scope="module", params=[p.name for p in EXPORTS])
def export(request):
    return gedcom.parse_file(DATA_LAKE / request.param)


def test_export_parses_without_warnings(export):
    assert export.warnings == []


def test_export_has_a_geni_header(export):
    assert export.header is not None
    assert export.header.value_of("SOUR") == "Geni.com"


def test_every_individual_xref_encodes_its_geni_profile_id(export):
    # This is the assumption the entire merge rests on: the xref IS the ID, and
    # RFN says the same thing. If Geni ever changes that, fail here and loudly.
    individuals = export.by_tag("INDI")
    assert individuals

    for indi in individuals:
        assert indi.xref and indi.xref.startswith("@I") and indi.xref.endswith("@")
        geni_id = indi.xref[2:-1]
        assert geni_id.isdigit()
        assert indi.value_of("RFN") == f"geni:{geni_id}"


def test_record_xrefs_are_unique(export):
    xrefs = [r.xref for r in export.records if r.xref]
    assert len(xrefs) == len(set(xrefs))


def test_round_trip_of_the_real_file_is_a_fixpoint(export):
    reparsed = gedcom.parse(gedcom.serialize(export))

    assert reparsed.header == export.header
    assert reparsed.records == export.records
