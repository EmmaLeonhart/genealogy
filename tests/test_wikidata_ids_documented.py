"""Every Wikidata ID the code can emit must be documented in the RULES.

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

⛔ **THE TABLE MOVED, AND THIS TEST WAS STILL READING THE OLD ADDRESS.** `CLAUDE.md` was cut
from 5,548 lines to 239 on 2026-09-09 and the property table went with it, onto the pages the
rules now link to — *"nothing was deleted, it was moved"*. This file read `CLAUDE.md` alone, so
the first CI run on a post-cut sha reported **24 IDs as undocumented when every one of them is
documented**, which is the same stale-path failure as `background.js` in
`test_geni_extension.py`: a real invariant pointed at a file that no longer holds the thing.

So the reference is the rules, all of them — `CLAUDE.md` plus `docs/rules/*.md`. `REFERENCE_FILES`
is asserted to exist below, so a later move fails loudly here instead of silently widening what
counts as documented.

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

#: The rules, which is where the property table lives since the 2026-09-09 cut. `CLAUDE.md`
#: carries the ones its own rules name; the rest are on the page each rule links to.
REFERENCE_FILES = [REPO_ROOT / "CLAUDE.md"] + sorted((REPO_ROOT / "docs" / "rules").glob("*.md"))


def _reference() -> str:
    """Every rules page concatenated. An ID documented on any of them is documented."""
    return chr(10).join(p.read_text(encoding="utf-8") for p in REFERENCE_FILES if p.exists())


#: A Wikidata property or item ID written as a string literal in the source.
#: Quoted deliberately: bare `P123` in prose or a docstring is a mention, while
#: a quoted one is a value the code can put in a statement.
ID_LITERAL = re.compile(r"""["'](P\d+|Q\d+)["']""")

pytestmark = pytest.mark.skipif(
    not (REPO_ROOT / "CLAUDE.md").exists(), reason="CLAUDE.md absent from this checkout"
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


def test_the_reference_pages_are_all_present():
    """The cut moved the table onto these pages; a rename must fail here, not pass quietly."""
    missing = [p.name for p in REFERENCE_FILES if not p.exists()]
    assert not missing, f"the rules pages this check reads are gone: {missing}"
    assert len(REFERENCE_FILES) >= 2, (
        "only CLAUDE.md was found -- docs/rules/ is where the property table lives"
    )


def test_every_wikidata_id_in_the_code_is_documented():
    reference = _reference()
    found = _ids_in_source()

    undocumented = _undocumented(found, reference)

    assert not undocumented, (
        "Wikidata IDs used in the code but missing from the rules' property table "
        f"({', '.join(p.name for p in REFERENCE_FILES)}): "
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
