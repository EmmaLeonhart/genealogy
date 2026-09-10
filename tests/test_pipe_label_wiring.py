"""The `|` ruling reaching a batch. `pipelabels.py` reads it; these pin that something CALLS it.

`tests/test_pipe_labels.py` pins the READER, situation by situation. This file pins the two
things that were missing on 2026-09-10 and that `CLAUDE.md` § *Code that is WRITTEN but never
CALLED is not done* is about:

* `scripts/apply-pipe-labels.py` writes the reader's output into
  `reports/title-label-proposals.tsv`, and is a step in `rebuild-everything.py`.
* `build-garborg-day._piped_label_fixes` emits those rows as `Lmul`/`Len`/`Amul`.

Both scripts are loaded by path; their filenames are not importable as packages.
"""

from __future__ import annotations

import csv
import importlib.util

import pytest

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROPOSALS = REPO / "reports" / "title-label-proposals.tsv"


def _by_path(name, filename):
    spec = importlib.util.spec_from_file_location(name, str(REPO / "scripts" / filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def applier():
    return _by_path("apply_pipe_labels", "apply-pipe-labels.py")


@pytest.fixture(scope="module")
def day():
    return _by_path("build_garborg_day", "build-garborg-day.py")


@pytest.fixture(scope="module")
def rows():
    with PROPOSALS.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


# --- the applier ran, and its output is what is committed ----------------------------------


def test_the_proposals_file_carries_the_en_column(rows):
    """Situation A gives an item two labels and `proposed_label` can only carry one.

    `Isabel Fraunceys (Francis|Frauncis), Heiress of Giffords Hall` is `Lmul Isabel Fraunceys`
    and `Len Isabel Fraunceys, Heiress of Giffords Hall`. Without the column the comma tail is
    either lost or dragged into `mul`, and both were ruled against.
    """
    assert "proposed_en" in rows[0]


def test_every_pipe_held_row_is_resolved_except_the_unclosed_bracket(rows):
    """201 rows were held for the pipe. 200 resolve; `Q99707312` has half a bracket.

    A fifteenth situation nobody ruled on -- `Alice Willisham (Wellasham|Wyllasham`. `read()`
    refuses it on OUTPUT, which is what stops `Alice Willisham (Wellasham` shipping as a label
    and counting as a success.
    """
    held = [r for r in rows
            if r["hold"] in ("pipe-shape", "one-token")
            and "|" in (r["live_mul"] or r["live_en"] or "")]
    assert [r["qid"] for r in held] == ["Q99707312"]


def test_no_resolved_proposal_still_carries_punctuation(rows):
    """A leftover `|`, `(` or `[` means the string was not understood.

    Emitting one puts punctuation on Wikidata, and it looks like a success in every count.
    """
    bad = [r["qid"] for r in rows
           if r["proposed_label"] and any(c in r["proposed_label"] for c in "|()[]")]
    assert bad == []


def test_the_applier_is_idempotent(applier, rows):
    """It reads `live_mul` and `leading_title`, never its own `proposed_label`.

    A second run over its own output has to compute the same strings, or the rebuild step walks
    the label somewhere new every day.
    """
    pipes = _by_path("pipelabels", "pipelabels.py")
    again = [dict(r) for r in rows]
    applier.apply(again, pipes)
    for before, after in zip(rows, again):
        assert (after["proposed_label"], after["proposed_en"], after["proposed_aliases"],
                after["hold"]) == (before["proposed_label"], before["proposed_en"],
                                   before["proposed_aliases"], before["hold"])


def test_the_leading_title_comes_off_before_the_pipe_is_read(applier):
    """Every other `proposed_label` in the file is built from the stripped string.

    10 of the 201 are `title+pipe` and all ten carry `Sir`. Reading the pipe off the raw label
    would put the title back into `proposed_label` on exactly those rows -- § *A TITLE IS NOT A
    NAME* undone by the fix for a different defect.
    """
    assert applier.strip_title("Sir Hugh Fraunceys (Frauncis|Francis)", "Sir") == \
        "Hugh Fraunceys (Frauncis|Francis)"
    # not a prefix: left alone rather than cut out of the middle, which would be a positional parse
    assert applier.strip_title("Hugh Sir Fraunceys", "Sir") == "Hugh Sir Fraunceys"


def test_the_applier_is_a_step_in_the_rebuild():
    """§ *Code that is WRITTEN but never CALLED is not done*, which is the whole of this item."""
    source = (REPO / "scripts" / "rebuild-everything.py").read_text(encoding="utf-8")
    assert "apply-pipe-labels.py" in source
    assert source.index("apply-pipe-labels.py") < source.index("build-garborg-day.py")


# --- the emitter ---------------------------------------------------------------------------


def test_the_batch_emits_the_ruled_shape_for_the_base_case(day):
    """`Ann Bincks (Benckes|Bench)` -- the base case, 69 rows.

        Lmul  Ann Bincks
        Amul  Ann Benckes
        Amul  Ann Bench
    """
    lines = day._piped_label_fixes({})
    block = _block(lines, "Q96213638")
    assert 'Q96213638\tLmul\t"Ann Bincks"' in block
    assert 'Q96213638\tAmul\t"Ann Benckes"' in block
    assert 'Q96213638\tAmul\t"Ann Bench"' in block


def test_the_comma_tail_is_emitted_as_en_and_never_as_mul(day):
    """Situation A, 34 rows. THE COMMA IS THE TELL; an un-comma'd `of X` stays in both."""
    block = _block(day._piped_label_fixes({}), "Q98967470")
    assert 'Q98967470\tLen\t"Isabel Fraunceys, Heiress of Giffords Hall"' in block
    assert 'Q98967470\tAmul\t"Isabel Francis"' in block
    assert not any("Lmul" in ln and "Heiress" in ln for ln in block)


def test_no_alias_is_ever_emitted_as_aen(day):
    """§ *The MARRIED name is the real name* -- *"No aen are ever supposed to be added."*"""
    assert not [ln for ln in day._piped_label_fixes({}) if "\tAen\t" in ln]


def test_no_description_is_emitted(day):
    """§ *NO descriptions and NO edit summaries, categorically*. The one exception is a name item."""
    assert not [ln for ln in day._piped_label_fixes({}) if ln[:1] == "Q" and "\tD" in ln]


def test_every_language_carrying_the_pipe_is_corrected(day):
    """Emitting on one language while another holds the same string leaves the defect live.

    `Q98967470` carries it in `en` and `nl`; the batch has to reach both.
    """
    block = _block(day._piped_label_fixes({}), "Q98967470")
    assert any(ln.startswith('Q98967470\tLnl\t') for ln in block)


def test_a_language_already_holding_the_fixed_value_is_skipped(day):
    """A label REPLACES, so re-writing a value already live is noise in the batch."""
    plain = _block(day._piped_label_fixes({}), "Q96213638")
    skipped = _block(day._piped_label_fixes({("Q96213638", "en"): "Ann Bincks"}), "Q96213638")
    assert any(ln.startswith('Q96213638\tLen\t') for ln in plain)
    assert not any(ln.startswith('Q96213638\tLen\t') for ln in skipped)


def test_the_whole_piped_population_is_emitted_and_not_only_the_newly_read_rows(day, rows):
    """1,640 labels carry a pipe and the queue item is to emit ALL of them.

    1,428 of them already had a proposal from `propose-title-label-fixes.split_pipe` and nothing
    emitted those either -- `build-noble-label-batch.py` skips them as `carries-a-pipe`, and
    `build-pipe-label-batch.py` writes a `.qs` no workflow reads. The 200 this session read are
    the rest, not the job.

    The arithmetic is the check: 1,640 = 1,628 emitted + `Q99707312` + 11 rows held for an
    unruled lowercase rank word, which the pipe ruling does not answer.
    """
    piped = [r for r in rows if "|" in (r["live_mul"] or r["live_en"] or "")]
    emitted = {ln.split("\t")[0] for ln in day._piped_label_fixes({}) if ln[:1] == "Q"}
    held = [r["qid"] for r in piped if r["hold"]]
    assert len(piped) == 1640
    assert len(emitted) + len(held) == len(piped)
    assert sorted(r["hold"] for r in piped if r["hold"]).count("leading-lowercase") == 11


def test_english_is_corrected_wherever_english_carries_the_pipe(day, rows):
    """A language-specific label beats `mul`, so an `Lmul` alone leaves the defect live in `en`.

    `pipelabels.statements` renders `Len` on 36 rows only, reasoning that English inherits
    `mul` -- true for an item with no `en` label, and these items have one holding the pipe.
    """
    lines = day._piped_label_fixes({})
    block = _block(lines, "Q96213638")
    assert 'Q96213638\tLen\t"Ann Bincks"' in block


def test_the_emitter_is_wired_into_the_derived_label_block():
    """Wired, not merely written: it has to reach `_cap_label_edits` to go out under the cap."""
    source = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    assert "_piped_label_fixes(live_labels)" in source


def _block(lines, qid):
    """The emitted lines for one QID, comments dropped."""
    return [ln for ln in lines if ln.startswith(qid + "\t")]
