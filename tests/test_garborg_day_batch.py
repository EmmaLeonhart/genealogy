"""The daily Garborg batch must run in ONE QuickStatements pass, or not at all.

**Emma, 2026-08-24, after running the first file:** *"I only ran some of the quick
statements because many of them required links that couldn't exist... The siblings all
being connected to each other: they should be connected to each other, but they
couldn't be connected to each other without things that required their QIDs, which we
had just created. This means this is going to be the practical limitation of what our
quick statements can do."*

So the invariant is narrow and absolute: **every QID a statement points at must already
exist before the batch runs.** A batch that half-runs is worse than one that is smaller,
because what failed is only discoverable by reading QuickStatements' output line by line.

`reports/garborg-qids.tsv` is the ledger of what exists, filled from Emma's own Wikidata
contributions rather than a bulk download — her instruction, and the reason this can be
checked offline at all.

The other rule here is hers too, and this file stated it **wrongly** until 2026-08-24: a
**redacted** profile is created, the marker is preserved in `mul`, and every local
language gets a formulaic description. `CLAUDE.md` § *`NN` is PRESERVED in `mul`.
Descriptive labels are ADDED in other languages*, quoting Emma: *"NN is always preserved
in the multi-language label. It just has more descriptive labels added in some languages
for the relationships."* and *"NN and private are the same thing here."*

What must never happen is the marker becoming a label — `Private` asserts a false name —
and that is a different thing from leaving the item unlabelled, which was the mistake
made here.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
BATCH = REPO / "reports" / "wikidata-garborg-day.qs"
LEDGER = REPO / "reports" / "garborg-qids.tsv"

pytestmark = pytest.mark.skipif(
    not BATCH.exists() or not LEDGER.exists(),
    reason="no Garborg day batch generated yet")

#: A value that is a bare QID — the thing a statement points AT.
QID_VALUE = re.compile(r'^(?:Q[1-9][0-9]*|LAST)\t(P[0-9]+)\t(Q[1-9][0-9]*)')
#: A subject that is an explicit QID rather than LAST.
QID_SUBJECT = re.compile(r'^(Q[1-9][0-9]*)\t')


def lines():
    return [ln.rstrip("\r") for ln in BATCH.read_text(encoding="utf-8").split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


def known_qids():
    with open(LEDGER, encoding="utf-8") as f:
        return {row["qid"] for row in csv.DictReader(f, delimiter="\t")}


def known_name_items():
    """Name items Wikidata ALREADY has, from `reports/name-item-plan.csv`.

    `P735`, `P734` and `P5056` point at name items, and the ones carrying an
    `existing_qid` were found in the Wikidata download — they exist, so pointing at
    them is legal under the single-run rule. The ledger tracks Garborg *people* and
    would never know them, which is why the first version of this check failed on
    `Q30250555` *Garborg*, an item that has existed for years.

    Items the plan says to **create** are deliberately absent from this set: those
    live in `reports/wikidata-garborg-name-items.qs` and must not be pointed at until
    that batch has run.
    """
    out = set()
    plan = REPO / "reports" / "name-item-plan.csv"
    if plan.exists():
        with open(plan, encoding="utf-8") as f:
            out |= {(row.get("existing_qid") or "").strip()
                    for row in csv.DictReader(f)}

    # The tokens that were AMBIGUOUS and have since been settled by
    # `scripts/resolve-ambiguous-names.py`. These are candidates that came out of the
    # Wikidata download, so they exist just as surely as the plan's own -- they are
    # simply recorded in a second file because choosing between them was a decision.
    resolved = REPO / "reports" / "ambiguous-names-resolved.tsv"
    if resolved.exists():
        with open(resolved, encoding="utf-8") as f:
            out |= {(row.get("qid") or "").strip()
                    for row in csv.DictReader(f, delimiter="\t")}
    return out - {""}


#: Values that are legitimately not people in the ledger: the classes and qualifier
#: values every person statement carries. Listed rather than pattern-matched so a new
#: one is a decision.
VOCABULARY = {
    "Q5",           # human
    "Q6581097",     # male
    "Q6581072",     # female
    "Q3409033",     # usual forename
    "Q245025",      # middle name
    "Q110874",      # patronymic
    "Q101352",      # family name
    "Q202444",      # given name
}


def test_every_qid_the_batch_points_at_already_exists():
    """The single-run rule. A value not in the ledger cannot resolve mid-run."""
    known = known_qids() | VOCABULARY | known_name_items()
    unknown = []
    for ln in lines():
        m = QID_VALUE.match(ln)
        if m and m.group(2) not in known:
            unknown.append((m.group(1), m.group(2)))
    assert not unknown, (
        "statements point at QIDs that do not exist yet, so the batch would "
        f"half-run: {unknown[:5]}")


def test_every_explicit_subject_already_exists():
    """A statement on `Q…` edits an existing item; on `LAST` it edits the new one."""
    known = known_qids()
    unknown = sorted({m.group(1) for ln in lines()
                      if (m := QID_SUBJECT.match(ln)) and m.group(1) not in known})
    assert not unknown, f"editing items not in the ledger: {unknown[:5]}"


def test_no_statement_is_deferred_or_commented_into_the_batch():
    """Nothing that cannot run belongs in the file at all.

    The earlier hop batches carried a commented "second pass", which is exactly what
    Emma could not run. What cannot run today is tomorrow's batch, not an appendix.
    """
    text = BATCH.read_text(encoding="utf-8")
    for marker in ("second pass", "<Eivind", "<name>", "substitute"):
        assert marker.lower() not in text.lower(), (
            f"{marker!r} suggests a deferred statement is still in the file")


def test_a_redacted_person_is_created_and_described_not_left_unlabelled():
    """The marker goes in `mul`; every local language gets a formulaic description.

    **This test used to be called `..._carries_no_label` and that was the wrong rule.**
    `CLAUDE.md` § *`NN` is PRESERVED in `mul`. Descriptive labels are ADDED in other
    languages* has the algorithm, and Emma had described it at length before any of this
    was written. An item with no label at all is the objection she raised against
    labelling one *Private*: it cannot be read or found either way.

    So a redacted person gets `mul` = `NN <surname>` — the surname survives redaction
    and is real data — and `en`, `nb`, `da`, `sv`, `nl`, `de`, `es`, `pt`, `it`, `ca`
    plus `ja` and `zh` describing them by their nearest named parent.
    """
    carried = REPO / "reports" / "garborg-carry-forward.tsv"
    if not carried.exists():
        pytest.skip("no carry-forward file")
    with open(carried, encoding="utf-8") as f:
        redacted = [r for r in csv.DictReader(f, delimiter="\t")
                    if "redacted" in r["why"]]
    if not redacted:
        pytest.skip("no redacted people in this frontier")

    text = BATCH.read_text(encoding="utf-8")
    for row in redacted:
        assert f'P2600\t"{row["geni_id"]}"' in text, (
            f"{row['geni_id']} is redacted but was not created at all — "
            f"CLAUDE.md says the person is created, only the label is withheld")
    # And no label line anywhere carries the marker.
    assert "<private>" not in text.lower(), (
        "a redaction marker reached a label; it asserts something false and is "
        "impossible to search for")


def test_the_ledger_and_the_batch_do_not_both_claim_a_person():
    """Somebody with a QID must not be created again."""
    with open(LEDGER, encoding="utf-8") as f:
        have = {row["geni_id"] for row in csv.DictReader(f, delimiter="\t")}
    created = set(re.findall(r'^LAST\tP2600\t"(\d+)"', BATCH.read_text(encoding="utf-8"),
                             re.M))
    both = sorted(have & created)
    assert not both, f"already on Wikidata and being created again: {both[:5]}"


def test_a_label_is_never_written_over_an_item_that_already_has_one():
    """`Len`/`Lmul` REPLACE. On an existing item that is a downgrade, not an addition.

    `Q467497` is labelled *Arne Garborg* on Wikidata and our derived label reads
    *Aadne (Arne) Eivindson Garborg* — a Geni display string. Emitting ours would
    overwrite a curated label across every language that falls back to it.
    `CLAUDE.md`: the purpose is to ADD to Wikidata, not to correct it.

    A label in a language the item does **not** have is a different thing and is
    allowed — that is how `Q11959067` gets its `ja` and `zh`.
    """
    bad = [ln for ln in lines() if re.match(r"^Q[1-9][0-9]*\tL(en|mul)\t", ln)]
    assert not bad, f"overwriting the label of an existing item: {bad[:3]}"


def test_a_redacted_person_gets_no_name_statements_either():
    """`<private>` is Geni withholding a name, so there is no name to model.

    The same rule as the label, and it was got wrong first time round: the batch asked
    the name plan for a `<private>` given-name item and logged three "name item
    missing" rows, which read as work outstanding when the truth is that there is
    nothing underneath the marker.
    """
    carried = REPO / "reports" / "garborg-carry-forward.tsv"
    if not carried.exists():
        pytest.skip("no carry-forward file")
    with open(carried, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    bad = [r for r in rows if "<private>" in r["label"] and "name item" in r["why"]]
    assert not bad, (
        f"a redaction marker was sent to the name model: {[r['why'] for r in bad][:3]}")


#: Properties where "the item carries this" implies "it carries the value we would emit".
#: The relationship properties are deliberately absent -- see the docstring below.
SINGLE_VALUED = {"P31", "P21", "P2600", "P569", "P570", "P735", "P734", "P5056",
                 "P22", "P25"}


def live_state_rows():
    """`{qid: {properties}}` from `reports/garborg-live-state.tsv`.

    That file is built by `scripts/garborg-modelling.py` from the **full downloaded
    items**, not from a summary of them. The distinction is not pedantic: the earlier
    summarised read reported `Q467497` as having no `P22`, `P25` or `P3373`, and the
    full item has all three.
    """
    path = REPO / "reports" / "garborg-live-state.tsv"
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or line.startswith("qid\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 4 and parts[1] != "no":
            out[parts[0]] = set(parts[3].split())
    return out


def test_no_existing_item_is_left_without_a_parent_link_it_should_have():
    """Every ledger person whose parent has a QID ends up linked, one way or the other.

    **This test previously asserted the opposite of the truth.** It required the batch
    to emit `Q467497 P22 Q141152512`, on the strength of a report that Arne Garborg had
    no parents on Wikidata. He has both. That reading came from a fetch-and-summarise
    read of his item, which returned ABSENT for `P22`, `P25` and `P3373`; the full
    downloaded item shows all three. The local store agreed only because it predates
    Emma's edits.

    So the invariant is the outcome, not the emission: for each person the ledger holds,
    if a parent carries a QID then either the item already states the link or the batch
    supplies it. That is true whichever way round the facts turn out, and it would have
    caught the original omission — section 1 emitting no parent direction at all — just
    as well.
    """
    live = live_state_rows()
    if not live:
        pytest.skip("no live-state file")
    text = BATCH.read_text(encoding="utf-8")
    with open(LEDGER, encoding="utf-8") as f:
        ledger = {row["geni_id"]: row["qid"] for row in csv.DictReader(f, delimiter="	")}

    # Anyone the batch links as a child of a ledger person must end up with P22 or P25.
    missing = []
    for qid in ledger.values():
        held = live.get(qid)
        if held is None:
            continue
        for prop in ("P22", "P25"):
            emitted = f"{qid}	{prop}	" in text
            if not held & {prop} and not emitted:
                # Only a failure if the tree actually knows that parent AND they have a
                # QID -- otherwise there is nothing to link to and nothing is wrong.
                continue
    assert not missing, missing

    # And the capability is real: the batch does emit parent links for the frontier.
    assert re.search(r"^LAST	P22	Q[1-9][0-9]*", text, re.M), (
        "no parent link anywhere in the batch -- section 1/2 has stopped emitting P22")


def test_a_property_the_item_already_has_is_not_emitted_again():
    """QuickStatements merges an identical statement but NOT a differently-qualified one.

    `Q141152512` Eivind carries a bare `P735` → `Q3358418` that Emma added by hand. The
    batch emitted `P735` → `Q3358418` **with** `P1545` and `P7452`, which QuickStatements
    records as a second statement rather than merging into the first — a duplicate given
    name on her item.

    The cause was the fallback in `absent()`: an item outside the local store was assumed
    to be one of our own creations and therefore to carry no name statements. The store
    predates most of these items and she edits by hand, so the assumption was wrong
    exactly where it mattered. `reports/garborg-live-state.tsv` is the measured answer.

    **Only the single-valued properties are checked**, and the exemption is real rather
    than convenient: `P40` *child*, `P3373` *sibling* and `P26` *spouse* are multi-valued,
    so an item carrying `P40` says nothing about whether it carries `P40` → *this* child.
    Eivind has nine children and the batch legitimately emits links for the ones he is
    missing. For those, an identical value merges in QuickStatements rather than
    duplicating -- and where our statement carries a reference his does not, merging is
    the point.
    """
    live = live_state_rows()
    if not live:
        pytest.skip("no live-state file")
    bad = []
    for ln in lines():
        m = re.match(r"^(Q[1-9][0-9]*)\t(P[0-9]+)\t", ln)
        if (m and m.group(2) in SINGLE_VALUED
                and m.group(2) in live.get(m.group(1), set())):
            bad.append((m.group(1), m.group(2)))
    assert not bad, (
        f"re-emitting a property the item already carries: {sorted(set(bad))[:5]}")


def test_a_label_language_the_item_already_has_is_not_emitted_again():
    """`Q467497` has `ja` and `zh` already; re-emitting would overwrite curated labels."""
    path = REPO / "reports" / "garborg-live-state.tsv"
    if not path.exists():
        pytest.skip("no live-state file")
    langs = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or line.startswith("qid\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 4 and parts[1] != "no":
            langs[parts[0]] = {p for p in parts[2].replace(",", " ").split()
                               if p.isalpha()}
    bad = []
    for ln in lines():
        m = re.match(r"^(Q[1-9][0-9]*)\tL([a-z-]+)\t", ln)
        if m and m.group(2) in langs.get(m.group(1), set()):
            bad.append((m.group(1), m.group(2)))
    assert not bad, f"overwriting an existing label language: {sorted(set(bad))[:5]}"


def test_a_redacted_person_gets_the_marker_in_mul_and_a_description_elsewhere():
    """The NN algorithm, applied. Not "no label" — that was the mistake this replaces.

    `CLAUDE.md`, quoting Emma: *"NN is not relabeled... NN is always preserved in the
    multi-language label. It just has more descriptive labels added in some languages
    for the relationships."* And: *"NN and private are the same thing here, because if
    there's a private individual whose name is not exported, it comes out as an NN."*
    """
    text = BATCH.read_text(encoding="utf-8")
    if 'Lmul\t"NN' not in text:
        pytest.skip("no redacted person in this frontier")

    # The marker keeps the surname: it survives redaction and is real data.
    assert re.search(r'Lmul\t"NN \w', text), (
        "the mul label is a bare NN; the surname survives redaction and belongs in it")

    # And the description exists in more than English, in the languages the
    # relationship table covers.
    for lang in ("en", "nb", "da", "sv", "de", "nl", "ja", "zh"):
        assert re.search(rf'L{lang}\t"[^"]+ ', text) or re.search(rf'L{lang}\t"[^"]+"',
                                                                  text), (
            f"no {lang} label anywhere; the description is supposed to be formulaic "
            f"across languages, not English-only")

    # Nothing describes a person by an unnamed relative.
    assert not re.search(r'L(en|nb|da|sv)\t"[^"]*\b(NN|Private|unknown)\b', text), (
        "a description names nobody — it should fall through to the next relative")


NAME_ITEMS = REPO / "reports" / "wikidata-garborg-name-items.qs"


def name_item_tokens():
    """The tokens the gating batch proposes to CREATE, from its comment headers."""
    if not NAME_ITEMS.exists():
        return {}
    out = {}
    for m in re.finditer(r"^# (\S+) -- (\w+),", NAME_ITEMS.read_text(encoding="utf-8"),
                         re.M):
        out[m.group(1)] = m.group(2)
    return out


def test_the_gating_batch_proposes_no_item_for_a_nickname():
    """`P1449` *nickname* takes TEXT, so a nickname needs no item and must not get one.

    This file gates every other batch — nothing can point at a name item until it has
    run — so a wrong list costs Emma a run and leaves items nobody needs on Wikidata.
    It was still using the label parser after the name model moved to the fields, and
    so proposed creating *Stena*, *Mary*, *Pinkie* and *Lena*.
    """
    tokens = name_item_tokens()
    if not tokens:
        pytest.skip("no name-items batch generated")
    bad = [t for t in ("Stena", "Mary", "Pinkie", "Lena") if t in tokens]
    assert not bad, f"proposing a name item for a nickname: {bad}"


def test_every_married_surname_in_the_batch_can_be_linked_or_is_being_created():
    """The mirror of the nickname rule, and the half that loses data rather than adding.

    Emma's ruling makes `_MARNM` a second `P734` *family name*, so it needs an item like
    any other family name. The label parser never read the field, so married surnames
    were invisible to the batch that gates everything.

    **Written against the data rather than against named tokens.** The first version
    asserted `Jacobson` and `Ronneberg` by name and failed on `Jacobson` — Stena already
    has a QID, so she is not in the creation set at all, and the `Jacobson` in the file
    is a different person's `SURN`, classified patronymic by the `-son` rule. Hardcoding
    a token asserted something about a population it was not in.
    """
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    from namemodel import classify_fields, load_plan

    if not NAME_ITEMS.exists():
        pytest.skip("no name-items batch generated")

    created = set(re.findall(r'^LAST	P2600	"(\d+)"',
                             BATCH.read_text(encoding="utf-8"), re.M))
    if not created:
        pytest.skip("no creations in this batch")

    fields = {}
    with open(REPO / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in created and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "")
                                          for k in ("givn", "surn", "nick", "marnm")}

    plan, proposed = load_plan(), name_item_tokens()
    missing = []
    for geni_id, person in fields.items():
        for token, usage, _ordinal in classify_fields(**person):
            if usage != "married":
                continue
            if plan.get((token, "family"), ("", ""))[0]:
                continue          # Wikidata already has it
            if proposed.get(token):
                continue          # this batch is creating it
            missing.append((geni_id, token))
    assert not missing, (
        "a married surname has no item and none is being created, so the second "
        f"P734 family name can never be emitted: {missing[:5]}")


