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


def test_the_backfill_never_cites_geni_for_a_familysearch_only_link():
    src = (REPO / "scripts" / "build-relationship-sources-backfill.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(
        ast.get_source_segment(src, n) for n in tree.body
        if (isinstance(n, ast.FunctionDef) and n.name in ("reference_for", "qs"))
        or (isinstance(n, ast.Assign) and any(getattr(t, "id", "") in ("TAB", "RELATION_OF")
                                              for t in n.targets)))
    ns = {}
    exec(code, ns)
    ref = ns["reference_for"]
    links = {("2", "father", "1"): "both", ("2", "mother", "3"): "fs", ("5", "mother", "3"): "fs"}
    fs_ids = {"2": "BBB"}
    father, mother = {"2": "1", "4": "1"}, {"2": "3", "5": "3"}
    args = (links, fs_ids, father, mother)
    assert ref("P22", "2", "1", *args) == '\tS2600\t"2"\tS2889\t"BBB"'
    assert ref("P25", "2", "3", *args) == '\tS2889\t"BBB"'
    assert ref("P26", "2", "9", *args) == '\tS2600\t"2"'
    # siblings: a database gives the link only when it links BOTH to the shared parent
    assert ref("P3373", "2", "4", *args) == '\tS2600\t"2"'
    assert ref("P3373", "2", "5", *args) == '\tS2889\t"BBB"'


def test_the_backfill_siblings_share_a_father_or_a_mother():
    """Emma, 2026-10-02: people who share a father or a mother are siblings ("I think the
    change is the problem"), reverting the family-object reading of 2026-09-27."""
    src = (REPO / "scripts" / "build-relationship-sources-backfill.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = [ast.get_source_segment(src, n) for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "sibling_index"][0]
    ns = {}
    exec(code, ns)
    # 1 and 2 share father 10; 2 and 3 share mother 20 only (half-siblings); 4 shares nobody
    sib = ns["sibling_index"]({"1": "10", "2": "10"}, {"2": "20", "3": "20", "4": "21"})
    assert sib == {"1": {"2"}, "2": {"1", "3"}, "3": {"2"}}


GENI = """0 HEAD
0 @I1@ INDI
1 RFN geni:1
1 BIRT
2 DATE 1700
1 DEAT
2 DATE 1760
0 @I2@ INDI
1 RFN geni:2
1 BIRT
2 DATE 1701
0 TRLR
"""
FAMILYSEARCH = """0 HEAD
0 @I1@ INDI
1 RFN geni:1
1 REFN fs:AAA
1 BIRT
2 DATE 1700
1 DEAT
2 DATE ABT 1761
0 @IFSX9@ INDI
1 BIRT
2 DATE 1650
0 TRLR
"""


def test_the_merge_records_which_database_gives_each_date(tmp_path):
    import sys
    sys.path.insert(0, str(REPO / "src"))
    from genimerge import merge
    (tmp_path / "familysearch").mkdir()
    (tmp_path / "geni").mkdir()
    (tmp_path / "familysearch" / "r.ged").write_text(FAMILYSEARCH, encoding="utf-8")
    (tmp_path / "geni" / "a.ged").write_text(GENI, encoding="utf-8")
    _doc, report = merge.merge_files([tmp_path / "familysearch" / "r.ged",
                                      tmp_path / "geni" / "a.ged"], slim=True)
    got = {k: sorted(v) for k, v in report.date_sources.items()}
    # only the people a FamilySearch render puts on a Geni xref are tracked
    assert got == {("1", "BIRT", "1700"): ["fs", "geni"],
                   ("1", "DEAT", "1760"): ["geni"],
                   ("1", "DEAT", "ABT 1761"): ["fs"]}


def test_a_date_cites_the_database_that_gives_it(tmp_path):
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(ast.get_source_segment(src, n) for n in tree.body
                         if isinstance(n, ast.FunctionDef)
                         and n.name in ("family_source", "cite_date"))
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "derived-family-sources.csv").write_text(
        "geni_id,relation,relative,source\n1,fs_id,AAA,fs\n", encoding="utf-8")
    (tmp_path / "reports" / "derived-date-sources.csv").write_text(
        "geni_id,event,date,source\n1,BIRT,1700,both\n1,DEAT,ABT 1761,fs\n1,DEAT,1760,geni\n",
        encoding="utf-8")
    ns = {"csv": csv, "ROOT": tmp_path, "_FAMILY_SOURCES": None, "_FS_IDS": {},
          "_DATE_SOURCES": None}
    exec(code, ns)
    cite_date = ns["cite_date"]
    assert cite_date("1", "BIRT", "1700") == '\tS2600\t"1"\tS2889\t"AAA"'
    assert cite_date("1", "DEAT", "ABT  1761") == '\tS2889\t"AAA"'
    assert cite_date("1", "DEAT", "1760") == '\tS2600\t"1"'
    assert cite_date("2", "BIRT", "1701") == '\tS2600\t"2"'


def test_a_sibling_cites_the_database_that_links_both_to_a_shared_parent(tmp_path):
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(ast.get_source_segment(src, n) for n in tree.body
                         if isinstance(n, ast.FunctionDef)
                         and n.name in ("family_source", "cite_sibling", "_parents"))
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "derived-family-sources.csv").write_text(
        "geni_id,relation,relative,source\n"
        "2,father,1,both\n5,mother,3,fs\n6,mother,3,fs\n6,fs_id,FFF,fs\n", encoding="utf-8")
    ns = {"csv": csv, "ROOT": tmp_path, "_FAMILY_SOURCES": None, "_FS_IDS": {}}
    exec(code, ns)
    rows = {"2": {"fathers": "1"}, "4": {"fathers": "1"}, "5": {"mothers": "3"},
            "6": {"mothers": "3"}, "7": {}}
    sib = ns["cite_sibling"]
    assert sib("2", "4", rows) == '\tS2600\t"2"'           # only child 2 is linked in FamilySearch
    assert sib("6", "5", rows) == '\tS2889\t"FFF"'         # FamilySearch links both to mother 3
    assert sib("2", "7", rows) == '\tS2600\t"2"'           # no shared parent on record


def test_the_merge_records_places_beside_dates(tmp_path):
    import sys
    sys.path.insert(0, str(REPO / "src"))
    from genimerge import merge
    (tmp_path / "familysearch").mkdir()
    (tmp_path / "geni").mkdir()
    (tmp_path / "familysearch" / "r.ged").write_text(
        "0 HEAD\n0 @I1@ INDI\n1 BIRT\n2 DATE 1700\n2 PLAC Klepp, Norway\n0 TRLR\n", encoding="utf-8")
    (tmp_path / "geni" / "a.ged").write_text(
        "0 HEAD\n0 @I1@ INDI\n1 BIRT\n2 PLAC Klepp,  Norway\n0 TRLR\n", encoding="utf-8")
    _doc, report = merge.merge_files([tmp_path / "familysearch" / "r.ged",
                                      tmp_path / "geni" / "a.ged"], slim=True)
    got = {k: sorted(v) for k, v in report.date_sources.items()}
    assert got[("1", "BIRT PLAC", "Klepp, Norway")] == ["fs", "geni"]
    assert got[("1", "BIRT", "1700")] == ["fs"]


def test_a_hand_label_row_retires_once_it_is_live(tmp_path):
    # Ruled 2026-09-27: applied until live, then removed, so a later hand correction stands.
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = [ast.get_source_segment(src, n) for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "retire_applied_labels"][0]
    ns = {}
    exec(code, ns)
    f = tmp_path / "label-applications.tsv"
    f.write_text("qid\tkind\tlang\tvalue\tsource\n"
                 "Q1\tL\tmul\tOls Orre\tEmma\n"        # live: retires
                 "Q2\tL\tmul\tJans\tEmma\n"            # live differs: stays
                 "Q3\tL\ten\tX\tEmma\n"                # live unknown: stays
                 "Q4\tA\tmul\tAlias\tEmma\n", encoding="utf-8")  # alias: stays
    live = {("Q1", "mul"): "Ols Orre", ("Q2", "mul"): "Jans abu Anna"}
    assert ns["retire_applied_labels"](f, live) == 1
    rows = f.read_text(encoding="utf-8").splitlines()
    assert [r.split("\t")[0] for r in rows[1:]] == ["Q2", "Q3", "Q4"]
    assert ns["retire_applied_labels"](f, live) == 0


def test_a_live_familysearch_id_gets_its_subject_named_as():
    """Emma, 2026-10-01: every `P2889` carries `P1810`, the FamilySearch name, as a Geni id carries
    the Geni name. Live statements without it are repeated WITH it (the sender attaches it by
    GUID); one that has it, a deprecated one, someone else's item and a name the reader refuses
    are left alone, and the pass stops at its cap."""
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(ast.get_source_segment(src, n) for n in tree.body
                       if isinstance(n, ast.FunctionDef) and n.name == "fs_named_as_repairs")
    ns = {}
    exec(code, ns)
    repair = ns["fs_named_as_repairs"]

    def claim(fs, quals=None, rank="normal"):
        return {"mainsnak": {"datavalue": {"value": fs}}, "rank": rank, "qualifiers": quals or {}}
    names = {"AAAA-111": '\tP1810\t"Kari Toresdatter"', "BBBB-222": '\tP1810\t"Ola"'}
    ents = [("Q1", {"claims": {"P2889": [claim("AAAA-111")]}}),
            ("Q2", {"claims": {"P2889": [claim("BBBB-222", {"P1810": [{}]})]}}),
            ("Q3", {"claims": {"P2889": [claim("BBBB-222", rank="deprecated")]}}),
            ("Q4", {"claims": {"P2889": [claim("AAAA-111")]}}),
            ("Q5", {"claims": {"P2889": [claim("CCCC-333")]}})]
    named = lambda fs: names.get(fs, "")
    assert repair(ents, {"Q1", "Q2", "Q3", "Q5"}, named, 10) == [
        'Q1\tP2889\t"AAAA-111"\tP1810\t"Kari Toresdatter"']
    assert repair(ents, {"Q1", "Q4"}, named, 1) == ['Q1\tP2889\t"AAAA-111"\tP1810\t"Kari Toresdatter"']


def test_a_composed_label_fills_only_an_empty_slot_in_a_switched_on_language(tmp_path):
    """Emma, 2026-10-02: English labels come from the name items now, ja/zh/ko not yet. A
    composed label goes out only where the item has none live, only for our items, and nothing
    goes out when the live labels are unknown."""
    src = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    code = "\n\n".join(ast.get_source_segment(src, n) for n in tree.body
                       if isinstance(n, ast.FunctionDef) and n.name == "_composed_en_labels")
    report = tmp_path / "composed.tsv"
    report.write_text("qid\tlang\tcomposed\tlive\n"
                      "Q1\ten\tSara Behm\t\n"
                      "Q2\ten\tWilliam Zouche\tWilliam Zouche, 1st Lord Zouche\n"
                      "Q3\tja\tサラ・ベーム\t\n"
                      "Q4\ten\tOscar Oldberg\t\n"
                      "Q5\ten\tHans Nyvold\t\n", encoding="utf-8")
    ns = {"csv": csv, "COMPOSED_LABELS_OUT": report, "COMPOSED_LANGS_LIVE": ("en",),
          "qs": lambda s: s}
    exec(code, ns)
    fill = ns["_composed_en_labels"]
    live = {("Q5", "en"): "Hans Syvertsen Nyvold"}
    assert fill({"g1": "Q1", "g2": "Q2", "g3": "Q3", "g5": "Q5"}, live) == ['Q1\tLen\t"Sara Behm"']
    assert fill({"g1": "Q1"}, {}) == []
