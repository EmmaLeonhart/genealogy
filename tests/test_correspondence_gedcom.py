"""The manual parental zipper correspondences as a merge input.

**What is worth pinning here is the ADDITIVE-ness, and nothing about the file's contents.**
`genimerge merge` takes positional paths that REPLACE the corpus; `--also` appends to it. The two
are one keystroke apart and the wrong one silently merges 314 records and nothing else — a tree
that is 314 people, written to `out/merged.ged`, looking like a successful run.

The other thing pinned is that a person the tree does not hold is never emitted: an `INDI` whose
xref the merge has not seen is a NEW person, which is what `exports/0-scraped/` was deleted for
(4,928 invented `NN` people).
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location(
        "_corr", ROOT / "scripts" / "build-correspondence-gedcom.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_render_is_a_valid_note_overlay_and_sorts_totally():
    mod = _module()
    text = mod.render({"200": {"Q2"}, "100": {"Q9", "Q1"}})
    lines = text.splitlines()
    assert lines[0] == "0 HEAD"
    assert lines[-1] == "0 TRLR"
    # Sorted on the id, and on the QID within a person: `CLAUDE.md` § *SORTING MUST BE
    # DETERMINISTIC* — same inputs, byte-identical output, whatever order the CSV arrived in.
    assert [l for l in lines if l.startswith("0 @I")] == ["0 @I100@ INDI", "0 @I200@ INDI"]
    assert lines.index("1 NOTE https://www.wikidata.org/wiki/Q1") < \
           lines.index("1 NOTE https://www.wikidata.org/wiki/Q9")
    assert mod.render({"200": {"Q2"}, "100": {"Q9", "Q1"}}) == text


def test_also_adds_to_the_corpus_rather_than_replacing_it(tmp_path):
    """`--also` is additive. A positional argument is not, and that is the whole point of it."""
    exports = tmp_path / "exports"
    exports.mkdir()
    (exports / "a.ged").write_text(
        "0 HEAD\n1 CHAR UTF-8\n0 @I111@ INDI\n1 NAME Someone\n0 @I222@ INDI\n1 NAME Other\n0 TRLR\n",
        encoding="utf-8")
    overlay = tmp_path / "overlay.ged"
    overlay.write_text(
        "0 HEAD\n1 CHAR UTF-8\n0 @I111@ INDI\n1 NOTE https://www.wikidata.org/wiki/Q1\n0 TRLR\n",
        encoding="utf-8")
    out = tmp_path / "merged.ged"

    rc = subprocess.call(
        [sys.executable, "-m", "genimerge", "merge",
         "--exports-dir", str(exports), "--also", str(overlay), "-o", str(out)],
        cwd=ROOT, env={**_env(), "PYTHONPATH": str(ROOT / "src")})
    assert rc == 0

    text = out.read_text(encoding="utf-8")
    # Both corpus people survive -- the overlay did not replace them...
    assert "0 @I111@ INDI" in text and "0 @I222@ INDI" in text
    # ...and the overlay's NOTE joined the record it names rather than making a second one.
    assert text.count("0 @I111@ INDI") == 1
    assert "1 NOTE https://www.wikidata.org/wiki/Q1" in text


def test_a_missing_also_file_refuses_rather_than_merging_without_it(tmp_path):
    exports = tmp_path / "exports"
    exports.mkdir()
    (exports / "a.ged").write_text("0 HEAD\n1 CHAR UTF-8\n0 @I111@ INDI\n0 TRLR\n", encoding="utf-8")
    rc = subprocess.call(
        [sys.executable, "-m", "genimerge", "merge",
         "--exports-dir", str(exports), "--also", str(tmp_path / "absent.ged"),
         "-o", str(tmp_path / "merged.ged")],
        cwd=ROOT, env={**_env(), "PYTHONPATH": str(ROOT / "src")})
    assert rc == 1


def _env():
    import os
    return dict(os.environ)
