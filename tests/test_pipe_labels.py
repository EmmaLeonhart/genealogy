"""Every ruled situation for a `|` in an imported label, pinned one at a time.

`name modelling.txt` § *A PIPE IN AN IMPORTED LABEL* is the authority and it beats `CLAUDE.md`
and the rules pages. 1,640 labels carry a pipe; they were ruled as three shapes, and the
bracketed shape has fourteen situations that were each put up separately because they are not
the same question and guessing any of them would have been a positional parse.

**These are pinned individually rather than as a table** because the rulings disagree with each
other in ways a table would smooth over -- a comma-separated tail leaves `mul`, an un-comma'd
`of X` stays in it, and those were decided in opposite directions in the same sitting.

Loaded by path; the script's name is not importable as a package.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def pipes():
    spec = importlib.util.spec_from_file_location(
        "pipelabels", str(REPO / "scripts" / "pipelabels.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- the three shapes ----------------------------------------------------------------


def test_two_given_names_share_the_surname(pipes):
    """1,372 rows. `Mary|Maria Butler` -- the pipe offers two given names and both keep Butler."""
    read = pipes.read("Mary|Maria Butler")
    assert read.mul == "Mary Butler"
    assert read.aliases == ["Maria Butler"]


def test_a_pipe_with_no_space_after_it_splits_the_whole_string(pipes):
    """136 rows, and the consequence was stated before it was ruled: the alias is BARE.

    `Daniel Tichenor|Titchenal` gives the alias `Titchenal`, a surname with no given name on
    it. That is the ruling, not an accident, and a "fix" that carried the given name across
    would be reversing a decision that was taken with its cost in view.
    """
    read = pipes.read("Daniel Tichenor|Titchenal")
    assert read.mul == "Daniel Tichenor"
    assert read.aliases == ["Titchenal"]


def test_a_mononym_pair_is_the_same_shape(pipes):
    read = pipes.read("Beatriz|Beatrice")
    assert read.mul == "Beatriz"
    assert read.aliases == ["Beatrice"]


def test_the_discriminator_is_the_space_and_nothing_else(pipes):
    """The two shapes differ only by whether the text after the pipe group has a space."""
    assert pipes.read("Mary|Maria Butler").aliases == ["Maria Butler"]
    assert pipes.read("Mary|Maria").aliases == ["Maria"]


# --- the bracketed shape, situation by situation --------------------------------------


def test_base_case_the_bracket_replaces_the_surname(pipes):
    """69 rows. Each bracketed spelling becomes an alias CARRYING THE GIVEN NAME."""
    read = pipes.read("Ann Bincks (Benckes|Bench)")
    assert read.mul == "Ann Bincks"
    assert read.aliases == ["Ann Benckes", "Ann Bench"]
    assert read.en is None


def test_a_comma_tail_stays_in_en_and_never_enters_mul(pipes):
    """34 rows. ⛔ THE COMMA IS THE TELL -- compare the two `of X` tests below."""
    read = pipes.read("Isabel Fraunceys (Francis|Frauncis), Heiress of Giffords Hall")
    assert read.mul == "Isabel Fraunceys"
    assert read.en == "Isabel Fraunceys, Heiress of Giffords Hall"
    assert read.aliases == ["Isabel Francis", "Isabel Frauncis"]


def test_three_or_more_variants_all_become_aliases(pipes):
    """14 rows, no cap."""
    read = pipes.read("Sarah Kilkam (Killem|Killum|Killam)")
    assert read.aliases == ["Sarah Killem", "Sarah Killum", "Sarah Killam"]


def test_a_pipe_outside_the_bracket_gives_the_cross_product(pipes):
    """10 rows. Six names, not four: every given name against every surname spelling."""
    read = pipes.read("Judith|Godith Bosom (Bozon|Bosun)")
    assert read.mul == "Judith Bosom"
    assert read.aliases == ["Judith Bozon", "Judith Bosun",
                            "Godith Bosom", "Godith Bozon", "Godith Bosun"]


def test_a_bracket_that_is_the_whole_name(pipes):
    """5 rows. No surname anywhere; first is the label, the rest are aliases."""
    read = pipes.read("(Thorkild|Tyrgils)")
    assert read.mul == "Thorkild"
    assert read.aliases == ["Tyrgils"]


def test_a_bracket_on_the_given_name_is_the_same_rule_mirrored(pipes):
    """5 rows."""
    assert pipes.read("(Maria|Antiza) Golescu").mul == "Maria Golescu"
    assert pipes.read("(Maria|Antiza) Golescu").aliases == ["Antiza Golescu"]


def test_a_bracket_in_the_middle_inserts_rather_than_replaces(pipes):
    """`Purcirto (Artinide|Hartneid) de Attems` keeps Purcirto AND takes the variant.

    This is the counterpart to the base case: there the bracket sits at the end and REPLACES
    the token in front of it, here it sits mid-name and is a slot of its own. Both outputs
    were ruled, and they are what settle which binding applies where.
    """
    read = pipes.read("Purcirto (Artinide|Hartneid) de Attems")
    assert read.mul == "Purcirto Artinide de Attems"
    assert read.aliases == ["Purcirto Hartneid de Attems"]


def test_nn_survives_into_every_alias(pipes):
    """5 rows. The marker is not a name and is not dropped by the variant expansion."""
    read = pipes.read("NN de Haselrick (Hazelrigg|Hesilrige)")
    assert read.mul.startswith("NN ")
    assert all(alias.startswith("NN ") for alias in read.aliases)


def test_a_negation_is_dropped_and_never_becomes_an_alias(pipes):
    """1 row. `(not Cecily)` is a description marker -- somebody recording that she is NOT
    Cecily -- so emitting `Cecily Francis` as an alias would assert the opposite of the record.
    """
    read = pipes.read("Margaret (not Cecily) Francis (Frauncis|Franceys|Frauncys)")
    assert read.mul == "Margaret Francis"
    assert read.aliases == ["Margaret Frauncis", "Margaret Franceys", "Margaret Frauncys"]
    assert not any("Cecily" in name for name in read.labels())


def test_an_empty_variant_slot_means_the_token_in_front_of_it(pipes):
    """1 row, ruled on its own. `(|Kunigunda)` means *Kone, or Kunigunda*.

    ⛔ And `of (Hastevere)` STAYS IN `mul`, with no comma before it -- the opposite of the
    comma-tail rule above, decided in the same sitting on exactly that difference.
    """
    read = pipes.read("Kone (|Kunigunda) of (Hastevere)")
    assert read.mul == "Kone of Hastevere"
    assert read.aliases == ["Kunigunda of Hastevere"]
    assert read.en is None


def test_square_brackets_read_as_round_ones(pipes):
    """1 row, ruled on its own."""
    read = pipes.read("(Teppana|Tahvana) of [Husu]")
    assert read.mul == "Teppana of Husu"
    assert read.aliases == ["Tahvana of Husu"]


# --- the guard -----------------------------------------------------------------------


def test_an_unclosed_bracket_is_held_not_emitted(pipes):
    """⛔ The fifteenth situation, and nobody ruled it: `Q99707312` is truncated mid-bracket.

    Exactly one row of the 1,640 does this. Without the guard it emits
    `Alice Willisham (Wellasham` -- a label with half a bracket in it, which succeeds silently
    and looks right in every count.
    """
    read = pipes.read("Alice Willisham (Wellasham|Wyllasham")
    assert read.note.startswith("HELD")
    assert read.mul == "Alice Willisham (Wellasham|Wyllasham"


def test_no_emitted_label_ever_carries_punctuation(pipes):
    """The property, over every ruled example at once."""
    samples = [
        "Ann Bincks (Benckes|Bench)", "Mary|Maria Butler", "Daniel Tichenor|Titchenal",
        "Judith|Godith Bosom (Bozon|Bosun)", "(Thorkild|Tyrgils)", "(Maria|Antiza) Golescu",
        "Kone (|Kunigunda) of (Hastevere)", "(Teppana|Tahvana) of [Husu]",
        "Margaret (not Cecily) Francis (Frauncis|Franceys|Frauncys)",
    ]
    for text in samples:
        read = pipes.read(text)
        assert not read.note.startswith("HELD"), text
        for label in read.labels():
            assert not pipes.UNRESOLVED.search(label), (text, label)


def test_a_label_with_no_pipe_is_returned_untouched(pipes):
    """The reader is only ever asked about piped labels, but it must not mangle anything else."""
    read = pipes.read("Arne Garborg")
    assert read.mul == "Arne Garborg"
    assert read.aliases == []


def test_the_whole_committed_file_reads(pipes):
    """Over the real 1,640: every row resolves except the one unclosed bracket."""
    import csv
    path = REPO / "reports" / "title-label-proposals.tsv"
    if not path.exists():
        pytest.skip("the proposals file is not in this checkout")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [r for r in csv.DictReader(handle, delimiter="\t")
                if "|" in (r.get("live_mul") or r.get("live_en") or "")]
    held = [r["qid"] for r in rows
            if pipes.read(r.get("live_mul") or r.get("live_en")).note.startswith("HELD")]
    assert len(rows) > 1000, len(rows)
    assert held == ["Q99707312"], held


# --- the protocol form ---------------------------------------------------------------


def test_the_label_is_mul_and_every_alternative_is_an_amul(pipes):
    """⛔ *The MARRIED name is the real name* -- `mul` carries it, alternatives go on as `Amul`,
    NEVER as an `Aen`. A variant spelling is not an English fact."""
    rows = pipes.statements("Q96213638", pipes.read("Ann Bincks (Benckes|Bench)"))
    assert rows == [("Q96213638", "Lmul", "Ann Bincks"),
                    ("Q96213638", "Amul", "Ann Benckes"),
                    ("Q96213638", "Amul", "Ann Bench")]
    assert not any(target.startswith("Aen") for _, target, _ in rows)


def test_len_is_written_only_where_english_differs(pipes):
    """34 rows of the 1,640 carry a comma tail. Everywhere else English inherits `mul`, and
    writing it again would be a second copy that can drift."""
    plain = pipes.statements("Q1", pipes.read("Ann Bincks (Benckes|Bench)"))
    assert not any(target == "Len" for _, target, _ in plain)
    tailed = pipes.statements(
        "Q2", pipes.read("Isabel Fraunceys (Francis|Frauncis), Heiress of Giffords Hall"))
    assert ("Q2", "Len", "Isabel Fraunceys, Heiress of Giffords Hall") in tailed
    assert ("Q2", "Lmul", "Isabel Fraunceys") in tailed


def test_a_held_reading_emits_nothing_at_all(pipes):
    """The guard must not be papered over by writing the raw string as a label."""
    assert pipes.statements("Q99707312",
                            pipes.read("Alice Willisham (Wellasham|Wyllasham")) == []


def test_the_cross_product_reaches_the_batch(pipes):
    """Six names means one Lmul and five Amul, not four."""
    rows = pipes.statements("Q3", pipes.read("Judith|Godith Bosom (Bozon|Bosun)"))
    assert sum(1 for _, t, _ in rows if t == "Lmul") == 1
    assert sum(1 for _, t, _ in rows if t == "Amul") == 5


def test_rendering_is_tab_separated_and_quoted(pipes):
    rows = pipes.statements("Q4", pipes.read("(Thorkild|Tyrgils)"))
    text = pipes.render(rows)
    assert text == 'Q4\tLmul\t"Thorkild"\nQ4\tAmul\t"Tyrgils"\n'
