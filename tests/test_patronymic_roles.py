"""The Spak model on what is already live and on the patronymic items (Emma, 2026-09-27).

`Q141562457` *Johan Erici Ersson Spak*: each patronymic of a person with more than one carries
`P3831` its culture, and each patronymic item is `P31` its culture class. `statements_for` does
new statements (`tests/test_namemodel.py::test_spak_*`); these cover the live statements
(`build-garborg-day.patronymic_role_repairs`) and the items (`build-garborg-name-items._finer_classes`).
The functions are run off the source, so the test does not pay for importing the composers.
"""
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from namemodel import patronymic_culture  # noqa: E402

LATIN, SCANDINAVIAN = "Q141584748", "Q141584760"


def _function(script, name, **ns):
    src = (REPO / "scripts" / script).read_text(encoding="utf-8")
    code = "\n\n".join(ast.get_source_segment(src, n) for n in ast.parse(src).body
                       if isinstance(n, ast.FunctionDef) and n.name == name)
    ns = {"patronymic_culture": patronymic_culture, **ns}
    exec(code, ns)
    return ns[name]


def _claim(qid, qualifiers=None, rank="normal"):
    return {"mainsnak": {"datavalue": {"value": {"id": qid}}}, "rank": rank,
            "qualifiers": qualifiers or {}}


LABELS = {"Q1": "Erici", "Q2": "Ersson", "Q3": "Olofsson"}


def test_two_live_patronymics_get_their_culture_roles():
    repair = _function("build-garborg-day.py", "patronymic_role_repairs")
    ents = [("Q10", {"claims": {"P5056": [_claim("Q1"), _claim("Q2")]}})]
    assert repair(ents, {"Q10"}, LABELS.get, 100) == [
        f"Q10\tP5056\tQ1\tP3831\t{LATIN}", f"Q10\tP5056\tQ2\tP3831\t{SCANDINAVIAN}"]


def test_a_role_already_live_one_patronymic_or_someone_elses_item_is_left_alone():
    repair = _function("build-garborg-day.py", "patronymic_role_repairs")
    done = [("Q10", {"claims": {"P5056": [_claim("Q1", {"P3831": [{}]}),
                                          _claim("Q2", {"P3831": [{}]})]}})]
    one = [("Q11", {"claims": {"P5056": [_claim("Q2")]}})]
    deprecated = [("Q12", {"claims": {"P5056": [_claim("Q1"), _claim("Q2", rank="deprecated")]}})]
    theirs = [("Q13", {"claims": {"P5056": [_claim("Q1"), _claim("Q2")]}})]
    assert repair(done + one + deprecated + theirs, {"Q10", "Q11", "Q12"}, LABELS.get, 100) == []


def test_the_repair_stops_at_its_cap():
    repair = _function("build-garborg-day.py", "patronymic_role_repairs")
    ents = [(f"Q{n}", {"claims": {"P5056": [_claim("Q1"), _claim("Q3")]}}) for n in range(10, 20)]
    assert len(repair(ents, {q for q, _e in ents}, LABELS.get, 5)) == 5


def test_a_created_patronymic_item_is_its_culture_class():
    src = (REPO / "scripts" / "build-garborg-name-items.py").read_text(encoding="utf-8")
    consts = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in (
                "MASCULINE_PATRONYMIC", "FEMININE_PATRONYMIC", "SON_NAME", "DAUGHTER_NAME",
                "MALE_SUFFIXES", "SON_WORD_SUFFIXES", "FEMALE_SUFFIXES"):
            consts[n.targets[0].id] = ast.literal_eval(n.value)
    finer = _function("build-garborg-name-items.py", "_finer_classes", **consts)
    assert LATIN in finer("Erici", "patronymic")
    assert SCANDINAVIAN in finer("Ersson", "patronymic")
    assert finer("Spak", "family") == []
