from genimerge import inventory

FOREST = """0 HEAD
1 SOUR Geni.com
0 @I100@ INDI
1 NAME Ada /Alpha/
1 SEX F
1 BIRT
2 DATE 1900
1 RFN geni:100
0 @I200@ INDI
1 NAME Bo /Beta/
1 RFN geni:200
0 @F900@ FAM
1 CHIL @I100@
0 TRLR
"""

# Overlaps Forest on @I200@ only, and adds a third person.
ANCESTORS = """0 HEAD
1 SOUR Geni.com
0 @I200@ INDI
1 NAME Bo /Beta/
1 RFN geni:200
0 @I300@ INDI
1 NAME Cyd /Gamma/
1 SEX M
1 RFN geni:300
0 @F900@ FAM
1 CHIL @I200@
0 TRLR
"""


def _write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def test_profile_counts_records_and_collects_ids(tmp_path):
    profile = inventory.profile_file(_write(tmp_path, "forest.ged", FOREST))

    assert profile.name == "forest.ged"
    assert profile.records_by_tag == {"INDI": 2, "FAM": 1}
    assert profile.individuals == {"100", "200"}
    assert profile.families == {"900"}
    assert profile.warnings == []


def test_profile_counts_structure_paths_not_just_top_level_tags(tmp_path):
    profile = inventory.profile_file(_write(tmp_path, "forest.ged", FOREST))

    assert profile.tag_paths["INDI"] == 2
    assert profile.tag_paths["INDI.NAME"] == 2
    assert profile.tag_paths["INDI.BIRT.DATE"] == 1
    assert profile.tag_paths["INDI.SEX"] == 1
    assert profile.tag_paths["FAM.CHIL"] == 1


def test_inventory_unions_intersects_and_isolates(tmp_path):
    inv = inventory.build_inventory(
        [
            _write(tmp_path, "forest.ged", FOREST),
            _write(tmp_path, "ancestors.ged", ANCESTORS),
        ]
    )

    assert inv.union("INDI") == {"100", "200", "300"}
    assert inv.intersection("INDI") == {"200"}
    assert inv.unique_to("INDI", "forest.ged") == {"100"}
    assert inv.unique_to("INDI", "ancestors.ged") == {"300"}
    # The same family ID in both files is one family, not two.
    assert inv.union("FAM") == {"900"}


def test_headline_calls_out_an_identical_count_across_exports(tmp_path):
    # Both files have two individuals but only one in common — the shape that
    # means "export cap", which is the single most important thing in the report.
    inv = inventory.build_inventory(
        [
            _write(tmp_path, "forest.ged", FOREST),
            _write(tmp_path, "ancestors.ged", ANCESTORS),
        ]
    )
    text = inventory.render_markdown(inv)

    assert "exactly 2 individuals" in text
    assert "cap" in text
    assert "3 distinct individuals" in text


def test_headline_stays_quiet_when_counts_differ(tmp_path):
    smaller = FOREST.replace("0 @I200@ INDI\n1 NAME Bo /Beta/\n1 RFN geni:200\n", "")
    inv = inventory.build_inventory(
        [
            _write(tmp_path, "small.ged", smaller),
            _write(tmp_path, "ancestors.ged", ANCESTORS),
        ]
    )

    assert "cap" not in inventory.render_markdown(inv)


def test_render_is_markdown_with_the_expected_sections(tmp_path):
    inv = inventory.build_inventory([_write(tmp_path, "forest.ged", FOREST)])
    text = inventory.render_markdown(inv)

    for heading in ("# Export inventory", "## Files", "## Headline",
                    "## Records by type", "## Tag vocabulary"):
        assert heading in text


def test_render_handles_an_empty_inventory():
    assert "No exports profiled." in inventory.render_markdown(inventory.Inventory())
