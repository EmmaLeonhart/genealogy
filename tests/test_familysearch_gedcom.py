"""The FamilySearch render, and the one thing it exists to prevent.

⛔ **`getmyancestors` EMITS OUR FOUR XREF PREFIXES WITH SEQUENTIAL INTEGERS.** Measured
2026-09-21 on the first real export, `MBW7-P7H-a12-d2.ged`: `@I1@`, `@F1@`, `@N1@`, `@S1@`,
numbered from 1. `identity.GENI_ID_RE` is `^@[IFNS](\\d+)@$`, so **`@I1@` parses as Geni
profile 1** — and small Geni ids are real people, `1015359` among them. Merging that file as
written would fuse 3,103 Norwegians onto whoever holds ids 1..3103.

That is the `@NI04461@` trap `CLAUDE.md` § *The primary key* records, where a foreign xref
parsed as a Geni id and pointed at a stranger's profile. `build-wikidata-gedcom.py` hit the
same thing with `@F9<n>@` reading as Geni family 91 and fixed it with a letter that cannot
parse. This is that fix for a third identifier space.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

RENDERER = REPO / "scripts" / "render-familysearch-gedcom.py"

RAW = """0 HEAD
1 CHAR UTF-8
1 SUBM @SUBM@
0 @SUBM@ SUBM
1 NAME Emma Leonhart
0 @I1@ INDI
1 NAME Inger /Akselsdatter Gyntersberg/
2 NOTE @N1@
1 SEX F
1 FAMS @F376@
1 FAMC @F1@
1 _FSFTID MBW7-P7H
1 SOUR @S9@
0 @I2@ INDI
1 NAME Aksel /Gyntersberg/
1 _FSFTID LXM8-QYV
0 @F1@ FAM
1 HUSB @I2@
1 CHIL @I1@
1 _FSFTID 9QXF-YBW
0 @N1@ NOTE Standardized the birth record.
0 @S9@ SOUR
1 REFN 12345
0 TRLR
"""


@pytest.fixture()
def rendered():
    from importlib import util
    spec = util.spec_from_file_location("fsrender", RENDERER)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text, counts = mod.rewrite(RAW)
    return text, counts


def test_not_one_xref_survives_that_parses_as_a_geni_id(rendered):
    """⛔ The whole point. `@I1@` must not reach the corpus as Geni profile 1."""
    import re
    from genimerge.identity import GENI_ID_RE
    text, _ = rendered
    leaked = [tok for tok in re.findall(r"@[^@\s]+@", text) if GENI_ID_RE.match(tok)]
    assert not leaked, f"xrefs still parse as Geni ids: {leaked[:5]}"


def test_the_raw_file_WOULD_have_leaked(rendered):
    """The hazard is real, not theoretical -- asserted so the test cannot pass vacuously.

    If `getmyancestors` ever changes to emit safe xrefs, this fails and the renderer can be
    reconsidered. Until then it documents why the renderer exists.
    """
    import re
    from genimerge.identity import GENI_ID_RE
    leaked = sorted({tok for tok in re.findall(r"@[^@\s]+@", RAW) if GENI_ID_RE.match(tok)})
    assert leaked, "the raw sample no longer carries a dangerous xref; check getmyancestors"
    assert "@I1@" in leaked and "@F1@" in leaked


def test_every_pointer_is_rewritten_not_just_the_definitions(rendered):
    """A definition and a reference have the same shape, so both move or the file is broken."""
    text, _ = rendered
    assert "0 @IFS1@ INDI" in text
    assert "1 FAMS @FFS376@" in text      # a reference to a family not defined in the sample
    assert "1 FAMC @FFS1@" in text
    assert "1 CHIL @IFS1@" in text
    assert "2 NOTE @NFS1@" in text
    assert "1 SOUR @SFS9@" in text
    assert "0 @NFS1@ NOTE" in text
    assert "0 @SFS9@ SOUR" in text


def test_the_familysearch_id_is_carried_as_a_refn(rendered):
    """`_FSFTID` stays, and `REFN fs:<id>` is added beside it.

    `_FSFTID` is what FamilySearch writes and is left alone; the `REFN` makes the identifier
    legible by the same convention `build-wikidata-gedcom.py` uses for `REFN Q<digits>`.
    """
    text, counts = rendered
    assert "1 _FSFTID MBW7-P7H" in text
    assert "1 REFN fs:MBW7-P7H" in text
    assert "1 REFN fs:9QXF-YBW" in text          # families carry one too
    assert counts["REFN added"] == 3


def test_the_subm_pointer_is_left_alone(rendered):
    """`@SUBM@` carries no digits, so it cannot parse as a Geni id and must not be touched."""
    text, _ = rendered
    assert "1 SUBM @SUBM@" in text
    assert "0 @SUBM@ SUBM" in text


def test_the_record_counts_are_not_anchored_to_end_of_line(rendered):
    """⛔ A `NOTE` carries its text inline, and anchoring the count `$` under-reported 341x.

    `DEF_RE` was `^0 @([IFNS])(\\d+)@ (\\w+)\\s*$` and counted **19** NOTE records in a file
    holding **6,490**, because `0 @N1@ NOTE Standardized the birth record.` does not end after
    the tag. The rewriting was never wrong, but a summary off by that much is how a bad render
    gets waved through.
    """
    _, counts = rendered
    assert counts["NOTE"] == 1, "the inline-text NOTE must still be counted"
    assert counts["INDI"] == 2
    assert counts["FAM"] == 1
    assert counts["SOUR"] == 1


def test_the_renderer_refuses_to_overwrite(tmp_path):
    """⛔ `CLAUDE.md` § *Never overwrite an existing `.ged`*. A new render is a new file."""
    src = tmp_path / "in.ged"
    src.write_text(RAW, encoding="utf-8")
    dst = tmp_path / "out.ged"
    dst.write_text("existing", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(RENDERER), str(src), str(dst)],
                          capture_output=True, text=True)
    assert proc.returncode != 0
    assert "Never overwrite" in (proc.stdout + proc.stderr)
    assert dst.read_text(encoding="utf-8") == "existing"
