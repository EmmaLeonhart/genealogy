"""The `P2600` batches are the only files here that will edit Wikidata.

From 2026-09-01 the QuickStatements files in `reports/` get run against the live
site, so a malformed line is not a failed parse — it is a wrong statement on a real
item, or a silent no-op that looks like success. Nothing else in this suite guards
them, and until now nothing did.

The invariants are deliberately narrow, because the risk is narrow:

* **The shape.** `Q…<TAB>P2600<TAB>"…"`. QuickStatements V1 has no escape for an
  embedded double quote, which already bit this project once — nine Bureätten
  labels carried `Stine "Stena"` and would have ended the string early.
* **Every statement traces to the source.** `reports/wikidata-geni-qid-p2600.qs`
  is generated from `reports/geni-qid-links.tsv`, and every pair in it must be in
  that file. A row that cannot be traced is a row nobody can check.
* **The Geni id is a Geni id.** Digits only, and one this repo could actually parse
  back out of a GEDCOM xref. `GENI_ID_RE` is the single place that knows the form.
* **No duplicate lines.** Harmless to run, but a duplicate means the generator
  double-counted, and the count is what gets reported.

`P2600` is multi-valued on purpose -- two Geni profiles for one person is a
permanent feature of Geni, per `CLAUDE.md` -- so **a QID appearing more than once
is correct and is not tested against.**
"""
import csv
import re
from pathlib import Path

import pytest

from genimerge.identity import GENI_ID_RE

REPORTS = Path(__file__).resolve().parent.parent / "reports"
BATCH = REPORTS / "wikidata-geni-qid-p2600.qs"
SOURCE = REPORTS / "geni-qid-links.tsv"

LINE = re.compile(r'^(Q[1-9][0-9]*)\tP2600\t"([0-9]+)"$')


def batch_lines():
    text = BATCH.read_text(encoding="utf-8")
    return [ln for ln in text.split("\n") if ln.strip()]


pytestmark = pytest.mark.skipif(
    not BATCH.exists(), reason="no P2600 batch generated yet"
)


def test_every_line_is_a_well_formed_p2600_statement():
    bad = [(i, ln) for i, ln in enumerate(batch_lines(), 1) if not LINE.match(ln)]
    assert not bad, "malformed QuickStatements lines: " + "; ".join(
        f"line {i}: {ln!r}" for i, ln in bad[:5]
    )


def test_no_line_carries_a_character_quickstatements_cannot_escape():
    """A double quote inside the value ends the string early and shifts every field."""
    offenders = [
        (i, ln) for i, ln in enumerate(batch_lines(), 1)
        if ln.count('"') != 2
    ]
    assert not offenders, "unbalanced quotes: " + "; ".join(
        f"line {i}: {ln!r}" for i, ln in offenders[:5]
    )


def test_the_geni_id_is_one_this_repo_could_parse_back_out_of_a_gedcom():
    bad = []
    for i, ln in enumerate(batch_lines(), 1):
        m = LINE.match(ln)
        if m and not GENI_ID_RE.match(f"@I{m.group(2)}@"):
            bad.append((i, m.group(2)))
    assert not bad, "not parseable as a Geni xref: " + "; ".join(
        f"line {i}: {g}" for i, g in bad[:5]
    )


def test_every_statement_traces_back_to_the_about_me_links():
    assert SOURCE.exists(), f"{SOURCE.name} is the source of the batch and is missing"
    allowed = set()
    with open(SOURCE, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            for qid in row["qids"].split(";"):
                if qid:
                    allowed.add((qid, row["geni_id"]))

    untraceable = []
    for i, ln in enumerate(batch_lines(), 1):
        m = LINE.match(ln)
        if m and (m.group(1), m.group(2)) not in allowed:
            untraceable.append((i, m.group(1), m.group(2)))
    assert not untraceable, "statements not in geni-qid-links.tsv: " + "; ".join(
        f"line {i}: {q} -> {g}" for i, q, g in untraceable[:5]
    )


def test_no_statement_is_repeated():
    lines = batch_lines()
    seen, dupes = set(), []
    for ln in lines:
        if ln in seen:
            dupes.append(ln)
        seen.add(ln)
    assert not dupes, f"{len(dupes)} repeated statements, e.g. {dupes[:3]}"


def test_the_batch_is_not_empty():
    """An empty batch passes every check above while doing nothing at all."""
    assert batch_lines(), "the batch has no statements"


# The checks above only prove the current batch is clean. These prove the checks
# would notice if it were not -- the same shape as the trigger-reader tests in
# `test_repo_invariants.py`, and the reason those exist.

@pytest.mark.parametrize("line", [
    'Q123\tP2600\t"6000000000000000001"',
    'Q1\tP2600\t"1"',
])
def test_the_line_reader_accepts_a_real_statement(line):
    assert LINE.match(line)


@pytest.mark.parametrize("line,why", [
    ('Q123\tP2600\t6000000000000000001', "value is not quoted"),
    ('Q123 P2600 "6000000000000000001"', "spaces instead of tabs"),
    ('Q0123\tP2600\t"6000000000000000001"', "QID with a leading zero"),
    ('123\tP2600\t"6000000000000000001"', "no Q prefix"),
    ('Q123\tP2600\t"600000 000"', "space inside the id"),
    ('Q123\tP735\t"6000000000000000001"', "wrong property"),
    ('Q123\tP2600\t"Stine "Stena" Garborg"', "embedded quotes -- the Bureatten case"),
])
def test_the_line_reader_rejects_what_would_go_wrong(line, why):
    assert not LINE.match(line), why
