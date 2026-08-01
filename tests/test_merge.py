from collections import Counter

from genimerge import gedcom, merge

# Ada has a birth date but no place.
A = """0 HEAD
1 SOUR Geni.com
0 @I100@ INDI
1 NAME Ada /Alpha/
2 GIVN Ada
1 SEX F
1 BIRT
2 DATE 1900
1 RFN geni:100
0 @F900@ FAM
1 CHIL @I100@
0 TRLR
"""

# Same Ada, same birth *event*, but a place instead of a date, plus a second
# name, a different child in the family, and a person A does not have.
B = """0 HEAD
1 SOUR Geni.com
0 @I100@ INDI
1 NAME Ada /Alpha/
2 SURN Alpha
1 NAME Ada /Beta/
1 SEX F
1 BIRT
2 PLAC Bergen
1 RFN geni:100
0 @I200@ INDI
1 NAME Bo /Beta/
1 RFN geni:200
0 @F900@ FAM
1 CHIL @I200@
0 TRLR
"""


def _merge(*texts):
    """Merge GEDCOM strings the same way `merge_files` merges paths."""
    docs = [gedcom.parse(t) for t in texts]

    worst = Counter()
    for doc in docs:
        for record in doc.records:
            merge._walk_multiplicity(record, "", worst)

    merger = merge.Merger(merge.collapse_single_valued(worst))
    for i, doc in enumerate(docs):
        merger.add_source(f"source{i}.ged", doc.records)
    return merger.result(), merger.report


def test_records_unique_to_one_source_are_all_kept():
    doc, report = _merge(A, B)

    assert sorted(r.xref for r in doc.records) == ["@F900@", "@I100@", "@I200@"]
    assert report.new_records["source0.ged"] == {"INDI": 1, "FAM": 1}
    assert report.new_records["source1.ged"] == {"INDI": 1}


def test_a_single_valued_event_gains_fields_from_both_sources():
    # This is the whole point: Ada's birth date comes from A and her birth place
    # from B, and they end up on one BIRT rather than two.
    doc, _ = _merge(A, B)
    ada = doc.by_xref()["@I100@"]

    assert len(ada.all("BIRT")) == 1
    assert ada.path_value("BIRT", "DATE") == "1900"
    assert ada.path_value("BIRT", "PLAC") == "Bergen"


def test_a_repeatable_path_keeps_distinct_values_and_merges_matching_ones():
    doc, _ = _merge(A, B)
    ada = doc.by_xref()["@I100@"]

    assert [n.value for n in ada.all("NAME")] == ["Ada /Alpha/", "Ada /Beta/"]
    # The two sources described "Ada /Alpha/" with different sub-fields; they
    # belong to one NAME, not two.
    alpha = ada.all("NAME")[0]
    assert alpha.value_of("GIVN") == "Ada"
    assert alpha.value_of("SURN") == "Alpha"


def test_pointers_are_matched_on_their_target():
    doc, _ = _merge(A, B)
    fam = doc.by_xref()["@F900@"]

    assert sorted(c.value for c in fam.all("CHIL")) == ["@I100@", "@I200@"]


def test_merging_a_file_with_itself_changes_nothing():
    once, _ = _merge(A)
    twice, report = _merge(A, A)

    # The header differs -- it names both sources -- but no record does.
    assert twice.records == once.records
    assert report.conflicts == []
    assert report.added_lines["source1.ged"] == 0


def test_a_tag_that_must_stay_repeatable_is_never_collapsed_by_measurement():
    # Every family here has exactly one child, so measurement alone would call
    # FAM.CHIL single-valued and start reporting siblings as conflicts.
    worst = Counter({"FAM.CHIL": 1, "INDI.FAMS": 1, "INDI.BIRT.DATE": 1})

    assert merge.collapse_single_valued(worst) == {"INDI.BIRT.DATE"}


def test_conflicting_single_valued_leaf_keeps_the_first_source_and_records_it():
    other = A.replace("2 DATE 1900", "2 DATE 1901")
    doc, report = _merge(A, other)
    ada = doc.by_xref()["@I100@"]

    assert ada.path_value("BIRT", "DATE") == "1900"
    assert len(report.conflicts) == 1
    conflict = report.conflicts[0]
    assert conflict.xref == "@I100@"
    assert conflict.path == "INDI.BIRT.DATE"
    assert (conflict.kept, conflict.kept_from) == ("1900", "source0.ged")
    assert (conflict.dropped, conflict.dropped_from) == ("1901", "source1.ged")


def test_merge_order_decides_which_conflicting_value_survives():
    other = A.replace("2 DATE 1900", "2 DATE 1901")
    first, _ = _merge(A, other)
    second, _ = _merge(other, A)

    assert first.by_xref()["@I100@"].path_value("BIRT", "DATE") == "1900"
    assert second.by_xref()["@I100@"].path_value("BIRT", "DATE") == "1901"


def test_conflict_credits_the_source_that_actually_grafted_the_value():
    # A has no death; B adds one; C disagrees with B. The kept value came from
    # B even though the record itself originated in A.
    b = A.replace("1 RFN geni:100", "1 DEAT\n2 DATE 1980\n1 RFN geni:100")
    c = A.replace("1 RFN geni:100", "1 DEAT\n2 DATE 1981\n1 RFN geni:100")
    _, report = _merge(A, b, c)

    assert [(x.path, x.kept, x.kept_from, x.dropped) for x in report.conflicts] == [
        ("INDI.DEAT.DATE", "1980", "source1.ged", "1981")
    ]


def test_records_without_an_xref_are_dropped_rather_than_duplicated():
    doc, _ = _merge("0 HEAD\n0 NOTE loose text\n0 TRLR\n")

    assert doc.records == []


def test_merged_output_gets_a_fresh_header_naming_its_sources():
    doc, _ = _merge(A, B)

    assert doc.header.value_of("SOUR") == "Geni.com"
    assert "source0.ged" in doc.header.value_of("NOTE")
    assert "source1.ged" in doc.header.value_of("NOTE")
    assert doc.header.path_value("GEDC", "VERS") == "5.5.1"


def test_merged_output_round_trips_as_valid_gedcom():
    doc, _ = _merge(A, B)

    assert gedcom.parse(gedcom.serialize(doc)).records == doc.records


def test_records_are_ordered_by_type_then_numeric_id():
    doc, _ = _merge(A, B)

    assert [r.xref for r in doc.records] == ["@I100@", "@I200@", "@F900@"]


def test_two_repeatable_lines_sharing_a_value_stay_two_lines():
    # Real case from the exports: one person carries two NAME lines with the
    # same text and different married names. Matching on the value alone would
    # collapse them, invent a conflict, and drop one married name.
    twin = (
        "0 @I1@ INDI\n"
        "1 NAME Ragnhild /Eikeland/\n2 _MARNM Giljabrekken\n"
        "1 NAME Ragnhild /Eikeland/\n2 _MARNM Loland\n"
        "0 TRLR\n"
    )
    doc, report = _merge(twin, twin)
    names = doc.by_xref()["@I1@"].all("NAME")

    assert [n.value_of("_MARNM") for n in names] == ["Giljabrekken", "Loland"]
    assert report.conflicts == []


def test_a_repeatable_line_merges_into_a_compatible_twin_not_a_contradictory_one():
    left = "0 @I1@ INDI\n1 NAME A /B/\n2 _MARNM X\n1 NAME A /B/\n2 _MARNM Y\n0 TRLR\n"
    # Adds a GIVN to the Y-married one; it must land there, not on the X one.
    right = "0 @I1@ INDI\n1 NAME A /B/\n2 _MARNM Y\n2 GIVN A\n0 TRLR\n"
    doc, report = _merge(left, right)
    names = doc.by_xref()["@I1@"].all("NAME")

    assert len(names) == 2
    assert names[0].value_of("_MARNM") == "X" and names[0].get("GIVN") is None
    assert names[1].value_of("_MARNM") == "Y" and names[1].value_of("GIVN") == "A"
    assert report.conflicts == []


def test_an_incompatible_repeatable_line_is_added_rather_than_reported_as_a_conflict():
    left = "0 @I1@ INDI\n1 NAME A /B/\n2 SURN First\n0 TRLR\n"
    right = "0 @I1@ INDI\n1 NAME A /B/\n2 SURN Second\n0 TRLR\n"
    doc, report = _merge(left, right)

    assert [n.value_of("SURN") for n in doc.by_xref()["@I1@"].all("NAME")] == ["First", "Second"]
    assert report.conflicts == []


def test_dangling_pointers_are_counted_by_where_they_occur():
    doc, _ = _merge(A, B)
    # @F900@ names @I100@ and @I200@, both present; add one that is not.
    doc.by_xref()["@F900@"].add("HUSB", "@I999@")

    assert merge.dangling_pointers(doc) == {"FAM.HUSB": 1}


def test_a_fully_resolved_tree_has_no_dangling_pointers():
    doc, _ = _merge(A, B)

    assert merge.dangling_pointers(doc) == {}


def test_signature_distinguishes_subtrees_that_differ_deep_down():
    left = gedcom.parse("0 @I1@ INDI\n1 SOUR\n2 DATA\n3 TEXT one\n0 TRLR\n").records[0]
    right = gedcom.parse("0 @I1@ INDI\n1 SOUR\n2 DATA\n3 TEXT two\n0 TRLR\n").records[0]

    assert merge.signature(left) != merge.signature(right)
    assert merge.signature(left) == merge.signature(left.copy())


def test_valueless_repeatable_nodes_are_matched_on_their_whole_subtree(tmp_path):
    # INDI.SOUR carries no value of its own, so two different citations must not
    # collapse into one -- but an identical citation in both sources must.
    one = "0 @I1@ INDI\n1 SOUR\n2 DATA\n3 TEXT alpha\n1 SOUR\n2 DATA\n3 TEXT beta\n0 TRLR\n"
    two = "0 @I1@ INDI\n1 SOUR\n2 DATA\n3 TEXT beta\n1 SOUR\n2 DATA\n3 TEXT gamma\n0 TRLR\n"
    doc, _ = _merge(one, two)

    texts = [s.path_value("DATA", "TEXT") for s in doc.by_xref()["@I1@"].all("SOUR")]
    assert texts == ["alpha", "beta", "gamma"]


def test_the_report_counts_every_record_it_merged():
    _, report = _merge(A, B)

    assert report.total_records == sum(report.totals.values()) == 3


# The report branches below only run when an export contradicts one already
# merged, or points at a record nobody supplied. Neither has happened yet --
# all three current exports agree -- so these paths have never executed on real
# data, and the first export that disagrees would be running them for the first
# time in the report a human is reading to decide whether to trust the merge.


def test_only_family_structure_pointers_are_reported_as_a_broken_tree():
    doc, report = _merge(A, B)
    # A missing spouse breaks the tree. A missing submitter record is an
    # incidental reference the exports simply did not include.
    doc.by_xref()["@F900@"].add("HUSB", "@I999@")
    doc.by_xref()["@I100@"].add("SUBM", "@S1@")
    text = merge.render_report(report, doc=doc)

    assert "**2** pointers name a record that is not in the merged file" in text
    assert "of which **1** are family-structure pointers" in text
    assert "| `FAM.HUSB` | 1 |" in text
    assert "| `INDI.SUBM` | 1 |" in text


def test_a_report_whose_pointers_all_resolve_says_so():
    doc, report = _merge(A, B)

    assert "None: every pointer in the merged file resolves." in merge.render_report(report, doc=doc)


def test_the_detailed_report_lists_every_conflict_and_where_each_value_came_from():
    _, report = _merge(A, A.replace("2 DATE 1900", "2 DATE 1901"))
    text = merge.render_report(report, detail=True)

    assert "**1** value disagreements on single-valued paths." in text
    assert "| `INDI.BIRT.DATE` | 1 |" in text  # the by-path summary
    assert (
        "| `@I100@` | `INDI.BIRT.DATE` | 1900 | source0.ged | 1901 | source1.ged |" in text
    )


def test_the_summary_report_points_at_the_detailed_one_instead_of_repeating_it():
    _, report = _merge(A, A.replace("2 DATE 1900", "2 DATE 1901"))
    text = merge.render_report(report, detail=False)

    assert "`out/merge-report.md`" in text
    assert "### Every conflict" not in text
    assert "source0.ged | 1901" not in text


def test_conflicts_on_the_same_path_are_summarised_together():
    other = A.replace("2 DATE 1900", "2 DATE 1901").replace("1 SEX F", "1 SEX M")
    _, report = _merge(A, other)
    text = merge.render_report(report, detail=False)

    assert "**2** value disagreements" in text
    assert "| `INDI.BIRT.DATE` | 1 |" in text
    assert "| `INDI.SEX` | 1 |" in text


def test_a_pipe_in_a_disputed_value_is_escaped_rather_than_splitting_the_table():
    # GEDCOM does not reserve `|`, Markdown does. An unescaped one would shift
    # every later column of that row silently.
    left = A.replace("2 DATE 1900", "2 DATE 1900\n2 PLAC Bergen | Oslo")
    right = A.replace("2 DATE 1900", "2 DATE 1900\n2 PLAC Trondheim")
    _, report = _merge(left, right)
    row = [ln for ln in merge.render_report(report, detail=True).splitlines() if "Bergen" in ln]

    assert len(row) == 1
    assert r"Bergen \| Oslo" in row[0]
    assert row[0].count("|") - row[0].count(r"\|") == 7  # 6 columns, 7 delimiters


def test_a_long_value_is_truncated_and_an_empty_one_is_visible():
    assert merge._cell("x" * 100) == "x" * 79 + "…"
    assert len(merge._cell("x" * 100)) == 80
    assert merge._cell("x" * 80) == "x" * 80  # exactly at the limit, left alone
    assert merge._cell("") == "*(empty)*"
    assert merge._cell("two\nlines") == "two lines"


def test_single_valued_paths_are_measured_from_the_files(tmp_path):
    path = tmp_path / "x.ged"
    path.write_text(
        "0 @I1@ INDI\n1 NAME a\n1 NAME b\n1 SEX M\n1 BIRT\n2 DATE 1900\n0 TRLR\n",
        encoding="utf-8",
        newline="\n",
    )
    paths = merge.single_valued_paths([path])

    assert "INDI.SEX" in paths
    assert "INDI.BIRT.DATE" in paths
    assert "INDI.NAME" not in paths  # seen twice under one INDI
