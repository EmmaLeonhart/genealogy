"""`derive-family.py` records which source gives each link (citation queue item, 2026-09-27).

A FamilySearch family is `@FFS…@`, a Geni family `@F<digits>@`. A link only a FamilySearch family
gives is `fs`, one both give is `both`, and one only Geni gives has no row.
"""
import csv
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

MERGED = """0 @I1@ INDI
1 REFN fs:AAA-111
0 @I2@ INDI
0 @I3@ INDI
0 @I4@ INDI
0 @F9@ FAM
1 HUSB @I1@
1 CHIL @I2@
0 @F10@ FAM
1 HUSB @I4@
1 CHIL @I3@
0 @FFSX1@ FAM
1 HUSB @I1@
1 WIFE @I3@
1 CHIL @I2@
"""


def test_sources_by_family_xref(tmp_path):
    spec = importlib.util.spec_from_file_location("derive_family", REPO / "scripts" / "derive-family.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    (tmp_path / "merged.ged").write_text(MERGED, encoding="utf-8")
    mod.MERGED = tmp_path / "merged.ged"
    mod.PAIRS = tmp_path / "absent.tsv"
    mod.LABELS = tmp_path / "absent.csv"
    mod.OUT_PEOPLE = tmp_path / "family.csv"
    mod.OUT_INVENTED = tmp_path / "invented.csv"
    mod.OUT_SOURCES = tmp_path / "sources.csv"
    mod.main()
    with open(tmp_path / "sources.csv", encoding="utf-8", newline="") as f:
        rows = {(r["geni_id"], r["relation"], r["relative"]): r["source"] for r in csv.DictReader(f)}
    assert rows == {
        ("1", "child", "2"): "both", ("2", "father", "1"): "both",
        ("1", "spouse", "3"): "fs", ("3", "spouse", "1"): "fs",
        ("2", "mother", "3"): "fs", ("3", "child", "2"): "fs",
        ("1", "fs_id", "AAA-111"): "fs",
    }
