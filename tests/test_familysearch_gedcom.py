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
    text, counts = mod.rewrite(RAW, {"LXM8-QYV": "4976573922110117540"}, "MBW7-P7H")
    return text, counts


def test_not_one_xref_survives_that_parses_as_a_geni_id(rendered):
    """⛔ The whole point. `@I1@` must not reach the corpus as Geni profile 1."""
    import re
    from genimerge.identity import GENI_ID_RE
    text, _ = rendered
    meant = {"@I4976573922110117540@"}          # the one person the sample bridge resolves
    leaked = [tok for tok in re.findall(r"@[^@\s]+@", text)
              if GENI_ID_RE.match(tok) and tok not in meant]
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
    assert "0 @IFSMBW7P7H@ INDI" in text
    assert "1 FAMS @FFSMBW7P7HX376@" in text   # a family not defined in the sample: file-seeded
    assert "1 FAMC @FFS9QXFYBW@" in text
    assert "1 CHIL @IFSMBW7P7H@" in text
    assert "2 NOTE @NFSMBW7P7HX1@" in text
    assert "1 SOUR @SFSMBW7P7HX9@" in text
    assert "0 @NFSMBW7P7HX1@ NOTE" in text
    assert "0 @SFSMBW7P7HX9@ SOUR" in text


def test_a_bridged_person_is_written_on_their_geni_xref(rendered):
    """⛔ Found 2026-09-24 on Emma Olivia Andersdotter: a render with no Geni xref never attaches.

    A FamilySearch person the bridge resolves takes `@I<geni id>@` and `RFN geni:`, so the merge
    joins them to the corpus exactly, and it is not reported as a leak.
    """
    text, counts = rendered
    assert "0 @I4976573922110117540@ INDI\n1 RFN geni:4976573922110117540" in text
    assert "1 HUSB @I4976573922110117540@" in text
    assert counts["bridged"] == 1


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


# ---------------------------------------------------------------------------
# THE BATCH. `scripts/build-familysearch-day.py`.
#
# ⛔ Ruled 2026-09-21: *"I want to have a pipeline that creates duplicates of familysearch vs
# geni but we can manually merge it. Makes separate quickstatements."* The duplicates are the
# design, and the thing that makes them mergeable is `P2889` — so that is what is pinned here
# hardest. An item created without it cannot be joined by anyone later, including the person
# doing the merge it exists for.
# ---------------------------------------------------------------------------

BUILDER = REPO / "scripts" / "build-familysearch-day.py"

#: A tree with one of everything the emitter branches on: a married woman, a married man, a
#: person whose surname slot is a marker, and a person whose whole name is a Norwegian phrase
#: meaning *not known*.
BATCH_GED = """0 HEAD
1 CHAR UTF-8
0 @IFS1@ INDI
1 NAME Kirstine Trondsdatter /Benkestok/
1 NAME  /Henrikson Guntersberg/
2 TYPE married
1 NAME Kirsten /Benkestok/
2 TYPE aka
1 SEX F
1 BIRT
2 DATE about 1524
2 PLAC Nordland, Norway
1 DEAT
2 DATE 21 February 1572
2 PLAC Torget, Norway
1 FAMS @FFS1@
1 _FSFTID AAAA-111
0 @IFS2@ INDI
1 NAME Trond /Torleivsson/
1 NAME Trond /Benkestok/
2 TYPE married
1 SEX M
1 FAMS @FFS1@
1 _FSFTID BBBB-222
0 @IFS3@ INDI
1 NAME Olav /N. N/
1 SEX M
1 FAMC @FFS1@
1 _FSFTID CCCC-333
0 @IFS4@ INDI
1 NAME Ikke kjent
1 SEX F
1 FAMC @FFS1@
1 _FSFTID DDDD-444
0 @IFS5@ INDI
1 NAME Henrik /Guntersberg/
1 SEX M
1 FAMS @FFS2@
1 _FSFTID EEEE-555
0 @IFS6@ INDI
1 NAME Torleiv /Benkestok/
1 SEX M
1 FAMS @FFS3@
1 _FSFTID FFFF-666
0 @FFS1@ FAM
1 HUSB @IFS2@
1 WIFE @IFS1@
1 CHIL @IFS3@
1 CHIL @IFS4@
0 @FFS2@ FAM
1 HUSB @IFS5@
1 CHIL @IFS1@
0 @FFS3@ FAM
1 HUSB @IFS6@
1 CHIL @IFS2@
0 TRLR
"""

#: ⛔ **THE SAMPLE NEEDS AN ANCHOR THE BRIDGE RESOLVES, OR NOBODY IS CREATED AT ALL.**
#: `build-familysearch-day` carries a person forward when no relationship can be emitted for
#: them -- the isolate rule of 2026-08-29, restated 2026-09-21 on three live isolates -- and in
#: a sample where nobody has a QID that is EVERYBODY. The first version of these tests was
#: written before that guard existed and went green on a file it then emptied.
#:
#: `EEEE-555` and `FFFF-666` are the fathers of the two people the label assertions are about,
#: so each of them has exactly one QID-bearing relative and is created with a `P22` to it. That
#: is also the real shape of the campaign: a wavefront out from the eleven bridge points.
BATCH_BRIDGE = """fs_id	qid	geni_id
EEEE-555	Q88888888	
FFFF-666	Q77777777	
"""
BATCH_UNIVERSE = '{"universe": ["Q88888888", "Q77777777"], "one_step": []}'


@pytest.fixture(scope="module")
def builder():
    from importlib import util
    spec = util.spec_from_file_location("fsday", BUILDER)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def batch(builder, tmp_path_factory):
    """The emitted file for `BATCH_GED`, with the two anchors of `BATCH_BRIDGE` resolved.

    The bridge is not empty, and it cannot be: a creation with no relationship is carried, not
    shipped, so an empty bridge produces an empty batch and every assertion below would be
    checking a header. See `BATCH_BRIDGE`.
    """
    import argparse
    tmp = tmp_path_factory.mktemp("fsbatch")
    src = tmp / "sample.ged"
    src.write_text(BATCH_GED, encoding="utf-8")
    builder.OUT = tmp / "out.txt"
    builder.CARRY = tmp / "carry.tsv"
    builder.BRIDGE = tmp / "bridge.tsv"
    builder.BRIDGE.write_text(BATCH_BRIDGE, encoding="utf-8")
    builder.UNIVERSE = tmp / "universe.json"
    builder.UNIVERSE.write_text(BATCH_UNIVERSE, encoding="utf-8")
    builder.build(argparse.Namespace(gedcom=[str(src)], limit=0))
    return builder.OUT.read_text(encoding="utf-8")


def test_every_created_item_carries_P2889(batch):
    """⛔ THE POINT OF THE WHOLE FILE. One `P2889` per `CREATE`, never fewer.

    The FamilySearch id is the only identifier these people have. Ruled 2026-09-21: it is what
    turns this pipeline into the bridge rather than a consumer of one — the next
    `bridge-familysearch-qids.py` run resolves against the ids we ourselves published.
    """
    creates = batch.count("\nCREATE\n") + batch.startswith("CREATE\n")
    ids = [l for l in batch.splitlines() if l.startswith("LAST\tP2889\t")]
    assert creates > 0
    assert len(ids) == creates, "an item was created that nobody can ever join"


def test_a_woman_goes_under_her_maiden_name_and_a_man_under_his_married_one(batch):
    """⛔ Ruled 2026-09-21, and the two sexes read opposite ends of the same pair of fields.

    FamilySearch writes the maiden form as the untyped `1 NAME` and the married one as
    `2 TYPE married`, so getting this backwards is one character of code and 215 women.
    """
    assert 'LAST\tLmul\t"Kirstine Trondsdatter Benkestok"' in batch
    assert 'LAST\tAmul\t"Henrikson Guntersberg"' in batch
    assert 'LAST\tLmul\t"Trond Benkestok"' in batch
    assert 'LAST\tAmul\t"Trond Torleivsson"' in batch


def test_the_description_is_the_life_description_with_the_gedcom_qualifier_written_out(batch):
    """`ABT` reads out as `circa`, and the description is what the human merger reads.

    `CLAUDE.md` § *DESCRIPTIONS ARE WRITTEN NOW, AND THE REASON IS THE DEDUPLICATION* — here
    it works *for* the intentional duplicate: it is how the person merging sees that the
    FamilySearch item and the Geni item are the same human.
    """
    assert ('LAST\tDen\t"circa 1524 Nordland, Norway - 21 Feb 1572 Torget, Norway"'
            in batch)


def test_a_marker_never_reaches_a_label(batch):
    """`Olav /N. N/` and `Ikke kjent` are not names, and both went out as labels once.

    Neither is dropped — they are counted into the carry-forward with a named reason, because
    `CLAUDE.md` § *Redacted people go in* and the treatment they need (`NN` in `mul`, prose in
    every other language) is keyed on the Geni tree this corpus has no ids for.
    """
    assert "N. N" not in batch
    assert "Ikke kjent" not in batch
    assert "Olav\"" not in batch


def test_a_date_keeps_its_qualifier_and_an_unreadable_one_asserts_nothing(builder):
    """The normaliser feeds `genimerge.dates`; it never decides what a date means itself."""
    assert builder.to_gedcom("about 1520") == "ABT 1520"
    assert builder.to_gedcom("21 February 1572") == "21 FEB 1572"
    assert builder.to_gedcom("from 1500 to 1520") == "BET 1500 AND 1520"
    assert builder.to_gedcom("omkring 1350") == "ABT 1350"
    # Unrecognised text survives as itself and parses to nothing — a date we cannot read
    # must never become a date we guessed.
    assert builder.to_gedcom("w czasie wojny") == "w czasie wojny"
    assert builder.date_row("w czasie wojny")[1] == ""
    assert builder.date_row("about 1520")[1:4] == ("+1520-00-00T00:00:00Z", "9", "about")


def test_nothing_lands_on_an_existing_item_outside_the_universe(builder, tmp_path):
    """⛔ Ruled 2026-09-17, and read HERE rather than trusted from the composer.

    With a bridge that resolves the father but a universe that does not contain him, the
    reciprocal `Q… P40 LAST` must not be written — `CLAUDE.md`: *a gate that lives only in the
    composer is one stale artifact away from being no gate*.
    """
    import argparse
    src = tmp_path / "sample.ged"
    src.write_text(BATCH_GED, encoding="utf-8")
    bridge = tmp_path / "bridge.tsv"
    bridge.write_text("fs_id\tqid\tgeni_id\nBBBB-222\tQ99999999\t\n", encoding="utf-8")
    universe = tmp_path / "universe.json"
    universe.write_text('{"universe": [], "one_step": []}', encoding="utf-8")

    builder.OUT = tmp_path / "out.txt"
    builder.CARRY = tmp_path / "carry.tsv"
    builder.BRIDGE = bridge
    builder.UNIVERSE = universe
    builder.build(argparse.Namespace(gedcom=[str(src)], limit=0))
    text = builder.OUT.read_text(encoding="utf-8")
    assert "Q99999999" not in text

    universe.write_text('{"universe": ["Q99999999"], "one_step": []}', encoding="utf-8")
    builder.build(argparse.Namespace(gedcom=[str(src)], limit=0))
    text = builder.OUT.read_text(encoding="utf-8")
    assert "LAST\tP26\tQ99999999" in text, "the forward statement"
    assert "Q99999999\tP26\tLAST" in text, "and the other direction, in the same run"


def test_a_multi_word_marker_leading_a_label_is_caught(builder):
    """⛔ `leads_with_a_marker` read `tokens[0]` and the vocabulary has held phrases all along.

    `n n`, `n. n.`, `no name`, `not known`, `name not known`, `unknown wife`, `namn okänt` —
    every one of them was unreachable. Found 2026-09-21 on eleven FamilySearch people labelled
    `N. N. Harniktsdatter`, `N. N Bødal`; a scan of `derived-labels.csv` then found **504
    label strings** on the Geni side in the same state.

    The whole marker comes off, not its first token, or the label keeps half of it as a given
    name.
    """
    import labels as L
    assert L.leads_with_a_marker("N. N. Harniktsdatter")
    assert L.marker_prefix_length("N. N. Harniktsdatter") == 2
    assert L.labels_for("N. N. /Harniktsdatter/")["mul"] == "NN Harniktsdatter"
    assert L.labels_for("Name not known /Olsen/")["mul"] == "NN Olsen"
    # And the guards that were already there still hold: a real name is not a marker, and a
    # trailing single letter is a middle initial.
    assert not L.leads_with_a_marker("Nils Nilsson")
    assert L.labels_for("Laura /N/")["mul"] == "Laura N"
