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

The other rule here is hers too: a **redacted** profile is created and gets **no label**.
`CLAUDE.md`: *"Private is a redaction marker, not a name, and an item labelled that
asserts something false while being impossible to find. The P2600 is what makes it
retrievable."*
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
    plan = REPO / "reports" / "name-item-plan.csv"
    if not plan.exists():
        return set()
    with open(plan, encoding="utf-8") as f:
        return {(row.get("existing_qid") or "").strip()
                for row in csv.DictReader(f)} - {""}


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


def test_a_redacted_person_is_created_and_carries_no_label():
    """Emma's rule, and both halves matter: created, and deliberately unlabelled."""
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


def test_an_existing_item_gets_its_parent_links_when_the_parents_have_qids():
    """The omission this section was rewritten for, kept as a regression.

    `Q467497` *Arne Garborg* had no `P22` *father* and no `P25` *mother* on Wikidata
    while both his parents already carried QIDs — because section 1 emitted `P40`,
    `P3373` and `P26` and simply never emitted the parent direction. That is a large
    part of what Emma meant by *"not remotely comprehensive"*.
    """
    text = BATCH.read_text(encoding="utf-8")
    for prop, parent in (("P22", "Q141152512"), ("P25", "Q141152523")):
        assert f"Q467497\t{prop}\t{parent}" in text, (
            f"Arne Garborg is missing his {prop} link to {parent}, which exists")


#: Properties where "the item carries this" implies "it carries the value we would emit".
#: The relationship properties are deliberately absent -- see the test's docstring.
SINGLE_VALUED = {"P31", "P21", "P2600", "P569", "P570", "P735", "P734", "P5056",
                 "P22", "P25"}


def live_state_rows():
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
