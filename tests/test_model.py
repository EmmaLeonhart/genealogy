from genimerge import gedcom
from genimerge.model import Name, build_tree

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Richard Wade /Borsheim/
2 GIVN Richard Wade
2 SURN Borsheim
1 SEX M
1 BIRT
2 DATE 20 OCT 1963
2 PLAC Canada
1 FAMS @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME Helen /Frisk/
2 GIVN Helen
2 SURN Frisk
2 _MARNM Borsheim
1 NAME Helen /Borsheim/
1 SEX F
1 BIRT
2 ADDR
3 CITY Vancouver
3 CTRY Canada
1 DEAT
2 DATE ABT 2010
1 OCCU Teacher
1 FAMS @F1@
1 RFN geni:2
0 @I3@ INDI
1 NAME Empress /Jingū/
1 SEX M
1 FAMC @F1@
1 OBJE
2 FILE a.jpg
1 NOTE {geni:about_me} Some prose about Eric.
1 RFN geni:3
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
1 MARR
2 DATE 1990
2 PLAC Vancouver
0 TRLR
"""


def tree():
    return build_tree(gedcom.parse(TREE).records)


def test_people_and_families_are_keyed_on_the_geni_id():
    t = tree()

    assert sorted(t.people) == ["1", "2", "3"]
    assert sorted(t.families) == ["1"]
    assert len(t) == 3


def test_a_person_carries_every_name_not_just_the_first():
    helen = tree().people["2"]

    assert [n.full for n in helen.names] == ["Helen /Frisk/", "Helen /Borsheim/"]
    assert helen.names[0].married == "Borsheim"
    assert helen.display_name == "Helen Frisk"


def test_display_name_falls_back_to_stripping_the_gedcom_slashes():
    assert Name(full="Empress /Jingū/").display == "Empress Jingū"


def test_events_keep_both_the_raw_date_and_the_parsed_one():
    richard = tree().people["1"]

    assert richard.birth.date.raw == "20 OCT 1963"
    assert richard.birth_year == 1963
    assert richard.birth.where == "Canada"


def test_a_place_can_come_from_the_address_block_when_there_is_no_plac():
    helen = tree().people["2"]

    assert helen.birth.where == "Vancouver, Canada"


def test_a_modified_date_keeps_its_modifier():
    helen = tree().people["2"]

    assert (helen.death_year, helen.death.date.modifier) == (2010, "about")


def test_empty_events_are_left_out_entirely():
    eric = tree().people["3"]

    assert eric.birth is None
    assert eric.events == {}


def test_family_membership_becomes_person_to_person_links():
    t = tree()
    eric, richard, helen = t.people["3"], t.people["1"], t.people["2"]

    assert (eric.father_id, eric.mother_id) == ("1", "2")
    assert richard.spouse_ids == ["2"] and helen.spouse_ids == ["1"]
    assert richard.child_ids == ["3"] and helen.child_ids == ["3"]


def test_the_family_view_is_kept_alongside_the_person_view():
    t = tree()

    assert t.people["3"].child_of == ["1"]
    assert t.people["1"].spouse_in == ["1"]
    assert t.families["1"].parent_ids == ["1", "2"]
    assert t.families["1"].marriage.year == 1990
    assert t.families["1"].marriage.where == "Vancouver"


def test_a_person_with_no_parents_is_visible_as_such():
    t = tree()

    assert not t.people["1"].has_known_parents
    assert t.people["3"].has_known_parents


def test_occupations_photos_and_about_text_are_carried_over():
    t = tree()

    assert t.people["2"].occupations == ["Teacher"]
    assert t.people["3"].photo_count == 1
    assert t.people["3"].about == "Some prose about Eric."


def test_resolving_relationships_twice_does_not_double_them():
    t = tree()
    t.resolve_relationships()

    assert t.people["1"].child_ids == ["3"]
    assert t.people["1"].spouse_ids == ["2"]


def test_json_form_is_flat_and_carries_the_profile_url():
    blob = tree().people["3"].to_json()

    assert blob["geni_id"] == "3"
    assert blob["url"].endswith("/3")
    assert blob["father_id"] == "1"
    assert blob["name"] == "Empress Jingū"
    assert blob["names"][0]["full"] == "Empress /Jingū/"


def test_family_json_keeps_the_marriage():
    blob = tree().families["1"].to_json()

    assert blob["husband_id"] == "1"
    assert blob["child_ids"] == ["3"]
    assert blob["marriage"]["year"] == 1990
