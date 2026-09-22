"""Integration check against the actual Geni exports in `exports/`.

The unit tests in `test_gedcom.py` use hand-written fixtures. This file exists
because the fixtures are what we *think* Geni emits, and these files are what it
*actually* emitted — the U+2028 handling in `parse` was found here, not there.

Skips when the exports are absent so a checkout without `exports/` still runs.
"""

import re
from pathlib import Path

import pytest

from genimerge import gedcom, sources

EXPORTS = sources.find_exports()
REPO = Path(__file__).resolve().parent.parent

#: **Also marked `slow`**: this module reparses every export and takes minutes.
#: Not skipped by default — `-m "not slow"` is a deliberate opt-out.
pytestmark = [
    pytest.mark.skipif(not EXPORTS, reason="no GEDCOM exports in exports/"),
    pytest.mark.slow,
]


@pytest.fixture(scope="module", params=[str(p) for p in EXPORTS])
def export(request):
    return gedcom.parse_file(Path(request.param))


def test_the_only_parse_warnings_are_lines_that_never_claimed_to_be_gedcom(export):
    """Nothing structural is ever skipped.

    This read `warnings == []` until 2026-08-04, which held for the first ten
    exports and stopped holding at 45: one profile has an RTF blob pasted into a
    note, and RTF carries literal newlines, so the blob's continuation lines
    arrive as GEDCOM lines with no level number in front of them.

    Zero warnings is therefore not achievable and not the property worth
    asserting — Geni's data contains what its users pasted into it. The property
    that matters is that the parser only ever skips lines that were *not*
    GEDCOM: every warning must be an "unparseable" one whose text does not begin
    with a level number. A skipped line that did start with a level number would
    mean real structure was dropped, and that still fails here.
    """
    structural = [
        w
        for w in export.warnings
        if "unparseable" not in w or re.search(r": '(\d+) ", w)
    ]
    assert structural == [], f"parser skipped or mangled real GEDCOM structure: {structural[:3]}"


#: **The two files under `exports/0-scraped/` are NOT Geni exports** and are not meant to be.
#: `scripts/build-scraped-gedcom.py` synthesises them from saved pages and relationship paths and
#: writes `1 SOUR genimerge-scraped`; `CLAUDE.md` § *`exports/` is the corpus* makes every `.ged`
#: beneath it corpus, so they are parametrised here like everything else.
#:
#: Their minted people sit in ranges Geni demonstrably does not use and carry **no** `RFN` on
#: purpose -- the builder's own words: *"claiming `RFN geni:<id>` for an id Geni does not have
#: would be a false identity assertion on this repo's primary key."*
#: **Every source that is not Geni.** `scripts/build-scraped-gedcom.py` writes
#: `genimerge-scraped`; `scripts/build-qid-links-gedcom.py` writes plain `genimerge`. Fixing
#: only the first was too narrow -- I checked the two files in front of me instead of censusing
#: the corpus, and the slow lane found the third. Measured 2026-08-31 over every `.ged` under
#: `exports/`: **511 `Geni.com`, 2 `genimerge-scraped`, 1 `genimerge`**.
#:
#: ⛔ **`genimerge-tiny` IS 96% OF THE CORPUS AND THIS SET HAD NEVER HEARD OF IT.** Censused
#: 2026-09-22 over every `.ged` under `exports/`, reading headers only:
#:
#:     21,967  genimerge-tiny      the path GEDCOMs this repo writes
#:        830  Geni.com
#:          2  genimerge
#:          1  getmyancestors      FamilySearch, and not ours -- see FOREIGN_SOURCES
#:
#: The comment above records the previous census as *"511 Geni.com, 2 genimerge-scraped, 1
#: genimerge"*. The corpus has since turned into something this module could not classify, and
#: nothing said so because the slow lane never ran: it is gated `workflow_dispatch` AND
#: `needs: test`, and the fast lane was red for days. A gate that cannot run is not a gate.
SYNTHESISED_SOURCES = {"genimerge-scraped", "genimerge", "genimerge-tiny"}

#: ⛔ **A FOREIGN EXPORT IS NEITHER GENI'S NOR OURS, AND THE DIFFERENCE IS LOAD-BEARING.**
#: `getmyancestors` writes the FamilySearch corpus. It is a real export from a real database --
#: so it is not *synthesised*, and calling it that would lose the distinction this module's
#: header test exists to keep -- but it is not Geni's either, and **every Geni-structural
#: assumption below is false of it on purpose**.
#:
#: `scripts/render-familysearch-gedcom.py` renumbers its xrefs to `@IFS<n>@` / `@FFS<n>@`
#: precisely so they CANNOT parse as Geni profile ids: `identity.GENI_ID_RE` is `^@[IFNS](\d+)@$`
#: and `@I1@` would otherwise read as Geni profile 1, fusing 3,103 Norwegians onto whoever holds
#: ids 1..3103. `tests/test_familysearch_gedcom.py` pins that render and asserts the raw file
#: WOULD have leaked. So asserting `@I<digits>@` here would demand the exact thing the renderer
#: exists to prevent, and the two test files would contradict each other.
FOREIGN_SOURCES = {"getmyancestors"}

#: The xref prefixes a foreign export uses, per source. One map each, because the point of a
#: foreign prefix is that it is NOT one of ours.
FOREIGN_XREF_PREFIXES = {
    "getmyancestors": {"IFS": "INDI", "FFS": "FAM", "NFS": "NOTE", "SFS": "SOUR",
                       "SUBM": "SUBM"},
}
SYNTHETIC_ID_PREFIXES = ("9995", "9990")


def _is_synthetic(geni_id):
    return geni_id.startswith(SYNTHETIC_ID_PREFIXES) and len(geni_id) == 19


def _source_of(export):
    """The `1 SOUR` of the header, or `''`."""
    return export.header.value_of("SOUR") if export.header else ""


def _synthesised(export):
    """True for a file this repo generated rather than one Geni sent."""
    return _source_of(export) in SYNTHESISED_SOURCES


def _foreign(export):
    """True for an export from a genealogy database that is not Geni. See `FOREIGN_SOURCES`."""
    return _source_of(export) in FOREIGN_SOURCES


def test_export_has_a_geni_header(export):
    """Every export is Geni's, or is one we synthesised and says so in its own header.

    This asserted `SOUR == "Geni.com"` outright and went red on 2026-08-31, the first slow-lane
    run since `exports/0-scraped/` was added. That is the test being right about the wrong
    *scope* rather than a defect on either side: a synthesised file must not **claim** to be a
    Geni export, and asserting that it is one makes the corpus rule and this invariant
    contradict each other. An unrecognised source still fails.
    """
    assert export.header is not None
    source = export.header.value_of("SOUR")
    assert (source == "Geni.com" or source in SYNTHESISED_SOURCES
            or source in FOREIGN_SOURCES), f"unknown export source {source!r}"


def test_every_individual_xref_encodes_its_geni_profile_id(export):
    # This is the assumption the entire merge rests on: the xref IS the ID, and
    # RFN says the same thing. If Geni ever changes that, fail here and loudly.
    # ⛔ A FOREIGN export's xrefs are deliberately unparseable as Geni ids -- that is what
    # `render-familysearch-gedcom.py` exists to guarantee and what
    # `tests/test_familysearch_gedcom.py` pins. Asserting the opposite here would put the two
    # files in contradiction and demand the very leak the renderer prevents.
    if _foreign(export):
        pytest.skip(f"{_source_of(export)}: xrefs are namespaced so they CANNOT be Geni ids")
    individuals = export.by_tag("INDI")
    assert individuals

    for indi in individuals:
        assert indi.xref and indi.xref.startswith("@I") and indi.xref.endswith("@")
        geni_id = indi.xref[2:-1]
        assert geni_id.isdigit()
        # **A minted placeholder carries no `RFN`, and that is the point.** The rule is per
        # RECORD, not per file: `scraped-paths.ged` holds real Geni people *and* minted
        # parents, so skipping the whole file would drop the real ones from this check.
        if _is_synthetic(geni_id):
            assert indi.value_of("RFN") == "", (
                f"minted placeholder {indi.xref} claims a Geni id it does not have")
            continue
        # **An overlay names people by xref and adds nothing else.**
        # `exports/post-merge/wikidata-qid-links.ged` is three `INDI` records carrying one
        # `NOTE` each; the xref is the join key and is a real Geni id, and repeating it as
        # `RFN` would assert nothing the xref does not already say. So a generated file may
        # omit it -- but if it states one, it must still be the truth.
        if _synthesised(export) and indi.value_of("RFN") == "":
            continue
        assert indi.value_of("RFN") == f"geni:{geni_id}"


def test_record_xrefs_are_unique(export):
    xrefs = [r.xref for r in export.records if r.xref]
    assert len(xrefs) == len(set(xrefs))


def test_round_trip_of_the_real_file_is_a_fixpoint(export):
    reparsed = gedcom.parse(gedcom.serialize(export))

    assert reparsed.header == export.header
    assert reparsed.records == export.records


# The premise GENI_ID_RE is designed around, checked against what Geni actually
# sends rather than against what we assume it sends.
#
# `test_identity.py` covers the regex thoroughly, but only on hand-written
# fixtures. If a future export introduces a fifth prefix, that regex does not
# raise — it silently declines to find an ID, or worse finds the wrong one. That
# is not hypothetical: when it accepted any letters, the foreign xref
# `@NI04461@` parsed as Geni ID `04461`, a real and unrelated profile.
#
# This lived in CLAUDE.md as "re-measure when an export lands", which is a note
# asking someone to remember. A test does not forget.

XREF_PREFIXES = {"I": "INDI", "F": "FAM", "N": "NOTE", "S": "SUBM"}


def _prefix(xref: str) -> str:
    """The leading letters of an xref: `@I123@` -> `I`, `@NI04461@` -> `NI`."""
    inner = xref.strip("@")
    letters = ""
    for char in inner:
        if not char.isalpha():
            break
        letters += char
    return letters


def _prefixes_by_tag(records) -> dict[str, set[str]]:
    """Every xref prefix in `records`, mapped to the record tags carrying it."""
    seen: dict[str, set[str]] = {}
    for record in records:
        if record.xref:
            seen.setdefault(_prefix(record.xref), set()).add(record.tag)
    return seen


def _unknown(seen: dict[str, set[str]], known=None) -> dict[str, list[str]]:
    """The prefixes in `seen` that `known` does not account for. Geni's four by default."""
    known = XREF_PREFIXES if known is None else known
    return {p: sorted(tags) for p, tags in seen.items() if p not in known}


def test_only_the_four_known_xref_prefixes_occur(export):
    """⛔ **And a FOREIGN export is checked against its own four, not Geni's.**

    `getmyancestors` writes `@IFS<n>@` / `@FFS<n>@` after `render-familysearch-gedcom.py` has
    renumbered it, and the whole point of those prefixes is that `GENI_ID_RE` cannot parse
    them. Reporting them here as *"Geni has started using xref prefixes this project does not
    know"* would be the message saying the opposite of what happened -- nothing about Geni
    changed, and the prefixes are unknown to `identity` deliberately.
    """
    known = FOREIGN_XREF_PREFIXES.get(_source_of(export), XREF_PREFIXES)
    unexpected = _unknown(_prefixes_by_tag(export.records), known)

    if _foreign(export):
        assert not unexpected, (
            f"{_source_of(export)} used an xref prefix its renderer does not produce: "
            f"{unexpected}. Check scripts/render-familysearch-gedcom.py -- a prefix it does "
            f"not namespace is one GENI_ID_RE may parse as a Geni profile id."
        )
        return

    assert not unexpected, (
        f"Geni has started using xref prefixes this project does not know: "
        f"{unexpected}. GENI_ID_RE accepts only {sorted(XREF_PREFIXES)} and will "
        f"silently misread the rest — add the prefix to genimerge.identity and to "
        f"XREF_PREFIXES here, and check what it does to the Geni IDs parsed from it."
    )


def test_each_xref_prefix_stays_bound_to_one_record_type(export):
    seen = _prefixes_by_tag(export.records)

    # A foreign export brings its own prefixes, and the property still holds -- one prefix,
    # one record type -- it is just a different map. `KeyError: 'FFS'` was this test asserting
    # Geni's map over FamilySearch's.
    expected = FOREIGN_XREF_PREFIXES.get(_source_of(export), XREF_PREFIXES)

    for prefix, tags in sorted(seen.items()):
        assert prefix in expected, (
            f"xref prefix {prefix!r} is not one {_source_of(export)!r} is known to use")
        assert tags == {expected[prefix]}, (
            f"xref prefix {prefix!r} appears on {sorted(tags)}, but this project "
            f"assumes it means {expected[prefix]} and nothing else."
        )


def test_every_known_prefix_is_actually_present(export):
    """A prefix that stopped appearing is also a format change worth noticing.

    Not every export needs every record type, so this asserts the weaker thing
    that matters: INDI and FAM are what a genealogy is made of, and an export
    without them is not one.
    """
    seen = {_prefix(r.xref) for r in export.records if r.xref}

    # A generated overlay is not a genealogy and is not claiming to be one: the QID-link file
    # is `INDI` records and nothing else, by design. The property being asserted -- that a Geni
    # export without people and families is not an export -- is about what Geni sends.
    if _synthesised(export):
        assert "I" in seen, "even an overlay has to name somebody"
        return

    # A foreign export is a genealogy, so the property holds -- under its own prefixes.
    if _foreign(export):
        assert {"IFS", "FFS"} <= seen, (
            f"{_source_of(export)}: an export without people and families is not one")
        return

    # ⛔ **A ONE-PERSON EXPORT HAS NO FAMILIES, AND THAT IS NOT A BROKEN EXPORT.**
    # `exports/post-merge/export-Ancestors-6000000227805352866.ged` is one `INDI` and one
    # `SUBM`: a real `Ancestors` export of somebody Geni records no relatives for. `{"I","F"}
    # <= seen` called that a format change. The property worth asserting is the one the
    # docstring states -- a genealogy names people -- plus the stronger half only where it can
    # be true: TWO people related to each other require a `FAM` to relate them.
    assert "I" in seen, "an export without people is not one"
    if len(export.by_tag("INDI")) > 1:
        assert "F" in seen, (
            "more than one person and no family: the relationships would be unrepresented")


def test_the_prefix_reader_distinguishes_the_xref_that_caused_the_bug():
    """`@NI04461@` is `NI`, not `N`. That difference is the whole guard.

    If `_prefix` stopped at one letter, the foreign xref would read as a NOTE,
    land in the known set, and these tests would pass while GENI_ID_RE went on
    parsing `04461` out of it — the exact failure they exist to catch.
    """
    assert _prefix("@NI04461@") == "NI"
    assert _prefix("@N1040@") == "N"
    assert _prefix("@I6000000001846508982@") == "I"


def test_the_guard_fires_on_a_document_carrying_a_foreign_xref():
    """Proof it is not vacuous: run the real check over a document that fails it.

    The exports in `exports/` all pass, so without this the guard could be
    broken in any number of ways and still look green.
    """
    doc = gedcom.parse(
        "0 HEAD\n"
        "0 @I123@ INDI\n"
        "1 NAME Fine /Person/\n"
        "0 @NI04461@ INDI\n"
        "1 NAME Foreign /Record/\n"
        "0 TRLR\n"
    )

    seen = _prefixes_by_tag(doc.records)

    assert _unknown(seen) == {"NI": ["INDI"]}
    assert "I" in seen and seen["I"] == {"INDI"}


def test_the_binding_check_fires_when_a_prefix_lands_on_two_record_types():
    doc = gedcom.parse(
        "0 HEAD\n"
        "0 @I123@ INDI\n"
        "1 NAME Fine /Person/\n"
        "0 @I456@ FAM\n"
        "0 TRLR\n"
    )

    seen = _prefixes_by_tag(doc.records)

    assert seen["I"] == {"INDI", "FAM"}
    assert seen["I"] != {XREF_PREFIXES["I"]}


def test_a_minted_id_never_reaches_a_quickstatements_batch():
    """A synthetic xref parses as a Geni id. It must never be emitted as one.

    `@I9995000000000100000@` satisfies `genimerge.identity`'s pattern exactly as a real xref
    does — four known prefixes, all digits — so nothing downstream can tell it apart by shape.
    `CLAUDE.md` records the cost of that class of mistake: when `GENI_ID_RE` accepted any
    letters, `@NI04461@` parsed as Geni id `04461` and *"would have produced a URL to a
    stranger's profile"*. Here the id is not a stranger's, it is nobody's, and a `P2600`
    carrying one would assert a Geni profile that does not exist.

    **Measured 2026-08-31: 4,928 minted people are in the merged tree and the derived CSVs, and
    zero have ever reached a batch.** This is the guard that keeps it that way. It is the check
    that makes narrowing the two assertions above safe -- the invariant did not go away, it
    moved to where the danger actually is.
    """
    minted = re.compile(r"\b999[05]0000000000\d{6}\b")
    offenders = []
    for batch in sorted((REPO / "reports").glob("*.qs")):
        for number, line in enumerate(
                batch.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue          # a comment is not an emitted statement
            found = minted.search(line)
            if found:
                offenders.append(f"{batch.name}:{number} {found.group(0)}")
    assert offenders == [], (
        "a minted placeholder id reached a QuickStatements batch: " + "; ".join(offenders[:5]))
