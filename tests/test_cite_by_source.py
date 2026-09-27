"""A relationship is cited to the database that gives it (citation queue item, 2026-09-27).

`cite()` in `build-garborg-day.py` reads `reports/derived-family-sources.csv`: a link only
FamilySearch gives is `S2889`, one both give carries both snaks in one reference, and anything
else stays `S2600`. The two functions are run on their own, off the source, so the test does not
pay for importing the composer.
"""
import ast
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SOURCES = """geni_id,relation,relative,source
1,child,2,both
2,father,1,both
2,mother,3,fs
3,child,2,fs
3,fs_id,BBB-222,fs
1,fs_id,AAA-111,fs
"""


def _cite(tmp_path):
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(ast.get_source_segment(src, n) for n in tree.body
                       if isinstance(n, ast.FunctionDef) and n.name in ("family_source", "cite"))
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "derived-family-sources.csv").write_text(SOURCES, encoding="utf-8")
    ns = {"csv": csv, "ROOT": tmp_path, "_FAMILY_SOURCES": None, "_FS_IDS": {}}
    exec(code, ns)
    return ns["cite"]


def test_each_link_cites_its_source(tmp_path):
    cite = _cite(tmp_path)
    assert cite("2") == '\tS2600\t"2"'                                  # not a traced link
    assert cite("2", "spouse", "9") == '\tS2600\t"2"'                   # Geni's alone
    assert cite("2", "father", "1") == '\tS2600\t"2"\tS2889\t"AAA-111"'  # both, one reference
    assert cite("2", "mother", "3") == '\tS2889\t"BBB-222"'             # FamilySearch alone
    assert cite("3", "child", "2") == '\tS2889\t"BBB-222"'


def test_the_relationship_lines_go_through_it():
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    assert "ref(g, RELATION_OF.get(prop), _geni_of_qid.get(value))" in src
    assert "{ref(g, 'spouse', sp)}" in src and "{ref(g, 'child', kid)}" in src
    assert "{ref(g, *_rel)}" in src and "{ref(source, *rel)}" in src
