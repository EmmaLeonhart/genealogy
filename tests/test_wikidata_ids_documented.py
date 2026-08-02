"""Every Wikidata ID the code can emit must be documented in `CLAUDE.md`.

`CLAUDE.md`'s property table exists because plausible-looking IDs are often
something else entirely — P1288 reads like a genealogy identifier and is a
German literature encyclopedia. The table is the control against guessing, and
a control only works over things inside it.

`P1545` was outside it for as long as it existed. `genimerge.namelinks` emitted
it as a qualifier on every P735 statement for a person with more than one given
name, and it was found by grepping the source, not by anyone remembering the
rule. `CLAUDE.md` then gained a sentence asking people to remember — which is
what this file replaces, for the same reason `test_gedcom_real_exports.py`
replaced "re-measure the xref prefixes when an export lands".

**This checks that an ID is documented. It cannot check that it is correct.**
Confirming an ID means asking Wikidata, which is network, and this suite is
offline on purpose. A typo added to the code and the table in the same change
passes here — `wbgetentities` is still the only thing that catches that, and
the table's header records when it was last run.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "src" / "genimerge"
REFERENCE = REPO_ROOT / "CLAUDE.md"

#: A Wikidata property or item ID written as a string literal in the source.
#: Quoted deliberately: bare `P123` in prose or a docstring is a mention, while
#: a quoted one is a value the code can put in a statement.
ID_LITERAL = re.compile(r"""["'](P\d+|Q\d+)["']""")

pytestmark = pytest.mark.skipif(
    not REFERENCE.exists(), reason="CLAUDE.md absent from this checkout"
)


def _ids_in_source() -> dict[str, list[str]]:
    """Every quoted Wikidata ID in the package, mapped to where it appears."""
    found: dict[str, list[str]] = {}
    for path in sorted(SOURCE.glob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for wikidata_id in ID_LITERAL.findall(line):
                found.setdefault(wikidata_id, []).append(f"{path.name}:{number}")
    return found


def _undocumented(found: dict[str, list[str]], reference: str) -> dict[str, list[str]]:
    """The IDs in `found` that `reference` never mentions."""
    return {i: places for i, places in found.items() if i not in reference}


def test_the_source_actually_contains_ids_to_check():
    """Guards the guard: a broken regex would make every other test here vacuous."""
    found = _ids_in_source()

    assert "P2600" in found, "expected the Geni profile ID property in the source"
    assert "Q101352" in found, "expected the family-name item in the source"
    assert len(found) > 10


def test_every_wikidata_id_in_the_code_is_documented():
    reference = REFERENCE.read_text(encoding="utf-8")
    found = _ids_in_source()

    undocumented = _undocumented(found, reference)

    assert not undocumented, (
        "Wikidata IDs used in the code but missing from CLAUDE.md's table: "
        f"{undocumented}. The table is what stops a plausible-looking ID being "
        "the wrong one — P1288 looks like a genealogy identifier and is a German "
        "literature encyclopedia. Confirm the ID against live Wikidata with "
        "wbgetentities, then add it to the table with its datatype in the same "
        "change."
    )


def test_the_check_reads_quoted_ids_and_not_prose_mentions():
    """`P1288` appears in CLAUDE.md as a warning, never as a value in the code.

    If this matched unquoted text, every ID named in a docstring would be
    treated as one the code emits, and the failure message would send people
    documenting things that are already documented as counter-examples.
    """
    assert ID_LITERAL.findall('PROPERTY = "P2600"') == ["P2600"]
    assert ID_LITERAL.findall("SERIES = 'P1545'") == ["P1545"]
    assert ID_LITERAL.findall("# P1288 is a literature encyclopedia") == []
    assert ID_LITERAL.findall("see P735 for given names") == []


def test_an_undocumented_id_is_reported_with_where_it_came_from():
    """Proof it is not vacuous: the real helper, over a reference missing an ID.

    Everything in `src/` currently passes, so without this the check could be
    broken in any number of ways and still look green.
    """
    found = {"P2600": ["quickstatements.py:43"], "P9999": ["namelinks.py:47"]}

    undocumented = _undocumented(found, "the table mentions P2600 and nothing else")

    assert undocumented == {"P9999": ["namelinks.py:47"]}


def test_a_fully_documented_set_reports_nothing():
    found = {"P2600": ["quickstatements.py:43"], "Q5": ["somewhere.py:1"]}

    assert _undocumented(found, "P2600 and Q5 are both in the table") == {}
