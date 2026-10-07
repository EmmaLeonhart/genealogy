"""Offline tests for wikidata_to_gedcom: no network, entities are built by hand."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wikidata_to_gedcom as w2g  # noqa: E402


def item(qid):
    return {"value": {"entity-type": "item", "id": qid}}


def claim(qid, rank="normal"):
    return {"mainsnak": {"datavalue": item(qid)}, "rank": rank}


def ent(qid, labels=None, father=None, mother=None, sex=None):
    claims = {}
    if father:
        claims["P22"] = [claim(father)]
    if mother:
        claims["P25"] = [claim(mother)]
    if sex:
        claims["P21"] = [claim(sex)]
    return {"id": qid, "labels": {k: {"language": k, "value": v} for k, v in (labels or {}).items()},
            "claims": claims}


# Child Q1 with father Q2 and mother Q3; Q2's father is Q4 (no mother known).
PEOPLE = {
    "Q1": ent("Q1", {"en": "Child", "ja": "子"}, father="Q2", mother="Q3", sex="Q6581072"),
    "Q2": ent("Q2", {"mul": "Father"}, father="Q4", sex="Q6581097"),
    "Q3": ent("Q3", {"en": "Mother"}, sex="Q6581072"),
    "Q4": ent("Q4", {}),
}


def test_label_prefers_requested_language():
    assert w2g.label(PEOPLE["Q1"], "ja") == "子"


def test_label_falls_back_to_mul_then_qid():
    assert w2g.label(PEOPLE["Q2"], "ja") == "Father"
    assert w2g.label(PEOPLE["Q3"], "ja") == "Q3"
    assert w2g.label(PEOPLE["Q4"], "en") == "Q4"


def test_claim_targets_skips_deprecated_and_novalue():
    e = {"claims": {"P22": [claim("Q9", rank="deprecated"),
                            {"mainsnak": {"snaktype": "novalue"}, "rank": "normal"},
                            claim("Q8")]}}
    assert w2g.claim_targets(e, "P22") == ["Q8"]


def test_gedcom_structure():
    text = w2g.to_gedcom("Q1", PEOPLE, "en")
    lines = text.splitlines()
    assert lines[0] == "0 HEAD" and lines[-1] == "0 TRLR"
    assert "1 CHAR UTF-8" in lines
    assert "1 NAME Child" in lines and "2 GIVN Child" in lines
    assert "1 NAME Father" in lines  # mul fallback
    assert "1 NOTE https://www.wikidata.org/wiki/Q4" in lines
    assert lines.count("1 SEX M") == 1 and lines.count("1 SEX F") == 2
    # Two families: (Q2, Q3) -> Q1 and (Q4, None) -> Q2.
    assert lines.count("0 @F1@ FAM") == 1 and lines.count("0 @F2@ FAM") == 1
    assert "1 WIFE" not in text.split("0 @F2@ FAM")[1]


EXPECTED_EN = """0 HEAD
1 SOUR wikidata_to_gedcom
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
1 LANG en
1 NOTE Ancestors of https://www.wikidata.org/wiki/Q1
0 @I1@ INDI
1 NAME Child
2 GIVN Child
1 SEX F
1 FAMC @F1@
1 NOTE https://www.wikidata.org/wiki/Q1
0 @I2@ INDI
1 NAME Father
2 GIVN Father
1 SEX M
1 FAMS @F1@
1 FAMC @F2@
1 NOTE https://www.wikidata.org/wiki/Q2
0 @I3@ INDI
1 NAME Mother
2 GIVN Mother
1 SEX F
1 FAMS @F1@
1 NOTE https://www.wikidata.org/wiki/Q3
0 @I4@ INDI
1 NAME Q4
2 GIVN Q4
1 FAMS @F2@
1 NOTE https://www.wikidata.org/wiki/Q4
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I3@
1 CHIL @I1@
0 @F2@ FAM
1 HUSB @I4@
1 CHIL @I2@
0 TRLR
"""


def test_gedcom_exact_output():
    """Pins the exact text so refactors cannot change what the user gets."""
    assert w2g.to_gedcom("Q1", PEOPLE, "en") == EXPECTED_EN
