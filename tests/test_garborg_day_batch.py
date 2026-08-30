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
    """Every item we can already point at -- the ledger PLUS `entity_resolution.md`.

    **The two must agree with the builder or this test measures a different thing.**
    `scripts/build-garborg-day.py`'s `ledger()` folds in the hand-asserted
    correspondences, because those are the only record of an item carrying no `P2600`
    yet -- Emma's own `Q232803` is the case, and without it the batch tried to create
    her a second item. Reading only `garborg-qids.tsv` here then flagged `Q232803`,
    `Q135579474`, `Q135579480` and three others as "do not exist yet" when they do.

    Widening this does not weaken the assertion: it still says every QID the batch points
    at must already exist. The set of KNOWN-EXISTING items grew, to match the builder.
    """
    out = set()
    with open(LEDGER, encoding="utf-8") as f:
        out |= {row["qid"] for row in csv.DictReader(f, delimiter="	")}
    import sys as _sys
    _sys.path.insert(0, str(REPO / "src"))
    try:
        from genimerge import entities
        out |= {r.qid for r in
                entities.read_file(REPO / "entity_resolution.md").resolutions if r.qid}
    except Exception:                                               # noqa: BLE001
        pass
    return out


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
    # **Name items already ON WIKIDATA, whether or not our plan knows them.** The plan's
    # universe came from `measure-name-resolution.py`, whose own universe is name items some
    # person in our store already links to -- so `Q36927172` *Tunheim* was invisible to it,
    # was created a second time, and was merged away by another editor. Since 2026-08-30 the
    # generator resolves against every name item in the local store, so this must too, or a
    # correct link reads here as a dangling pointer.
    store = REPO / "out" / "wikidata" / "name-items-in-store.tsv.gz"
    if store.exists():
        import gzip
        with gzip.open(store, "rt", encoding="utf-8") as fh:
            next(fh, None)
            out |= {line.split("	", 1)[0] for line in fh}

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


#: The eight items `SPINE_P2600_BLOCK` edits. They are **deliberately not in the ledger**: their
#: items carry no `P2600` *Geni.com profile ID*, so the contributions refresh cannot resolve
#: them, and the 2026-08-27 rebuild-not-merge ruling therefore drops them. The block exists to
#: put that `P2600` on Wikidata, after which they resolve on their own and this list can go with
#: it. Evidence for each pairing is in `reports/wikidata-spine-add-p2600.qs`; two were accepted
#: by Emma on 2026-08-26.
SPINE_BLOCK_QIDS = {"Q5915800", "Q101247444", "Q6197518", "Q3743799",
                    "Q4953376", "Q466257", "Q274606", "Q284400"}

#: The 177 items `CJK_CLAN_BLOCK` labels. Same situation as the spine block and the same
#: reasoning: they are not ledger members, the block exists to give them a `mul` label and
#: formulaic descriptions, and the list is **read from a file rather than pattern-matched**, so
#: an item that quietly appeared in the batch by some other route would still fail this test.
#: `reports/cjk-clan-block-qids.txt` is regenerated whenever the block is.
def _cjk_block_qids():
    path = REPO / "reports" / "cjk-clan-block-qids.txt"
    if not path.exists():
        return set()
    return {ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()}


def test_every_explicit_subject_already_exists():
    """A statement on `Q…` edits an existing item; on `LAST` it edits the new one.

    **The spine block is the one exemption and it is named rather than pattern-matched.** Every
    other `Q…` subject must be a ledger member — that is the guard against editing an item we
    cannot vouch for. These eight are vouched for by `wikidata-spine-add-p2600.qs`, and the only
    reason they are outside the ledger is that the pairing is not yet on Wikidata, which is the
    thing the block fixes. When the block is deleted this set goes with it, and if it is ever
    emptied the assertion tightens back to what it always was.
    """
    known = known_qids() | SPINE_BLOCK_QIDS | _cjk_block_qids()
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
        rows = list(csv.DictReader(f, delimiter="\t"))
    # `--skip-nn` is a choice Emma made for ONE QuickStatements run: *"for this
    # quickstatements run the NN people are not worth creating"*. With it on they are
    # deliberately absent and there is nothing here to check. The standing rule that
    # redacted people DO go in, marker in `mul` and a description elsewhere, is
    # untouched — which is why this skips rather than being deleted.
    if any("--skip-nn" in r["why"] for r in rows):
        pytest.skip("this batch was built with --skip-nn")
    redacted = [r for r in rows if "redacted" in r["why"]]
    if not redacted:
        pytest.skip("no redacted people in this frontier")

    text = BATCH.read_text(encoding="utf-8")
    for row in redacted:
        assert f'P2600\t"{row["geni_id"]}"' in text, (
            f"{row['geni_id']} is redacted but was not created at all — "
            f"CLAUDE.md says the person is created, only the label is withheld")
    # And no LABEL line anywhere carries the marker -- but `P1810` *subject named as* may,
    # and must. Emma ruled on 2026-08-29 that the qualifier carries the literal Geni string:
    # a label asserts what the person is called, `P1810` asserts what the source displays,
    # and only the first is falsified by `<private> Garborg`. Her `mul` stays `NN Garborg`.
    #
    # This was a blanket ban on the string until then, which is why it is worth being exact:
    # the ban is on labels and aliases, not on the file.
    leaked = [ln for ln in text.splitlines()
              if "<private>" in ln.lower() and "P1810" not in ln]
    assert not leaked, (
        f"a redaction marker reached a label; it asserts something false and is "
        f"impossible to search for: {leaked[:3]}")


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
    # **`CJK_CLAN_BLOCK` sets `mul` on 177 items that have none, which this rule allows and the
    # blanket regex cannot see.** Checked live on 2026-08-28 via `full_entities`: `mul` is empty
    # on all 177, and `en` is occupied on all 177 — which is why the block writes no `en` for
    # them at all. The exemption is `Lmul` only, and only for ids the block actually names, read
    # from `reports/cjk-clan-block-qids.txt`. An `Len` on one of them, or an `Lmul` on anybody
    # else, still fails.
    # **A label WE put there may be overwritten. Emma, 2026-08-29:** *"If I added the label we
    # can overwrite it lol"* — asked to choose between this test and the corrections she ordered
    # on the same day. So the rule is not "never"; it is "never somebody else's".
    #
    # **What proves we added it: the batch preserves the outgoing value as an `Amul` first.**
    # `_label_corrections` emits `Amul "<what Wikidata holds>"` immediately above its `Lmul`, and
    # it only fires where that outgoing value matches a **birth-name alias from our own tree** —
    # i.e. a string our pipeline generated. A curated label nobody here wrote can never satisfy
    # that, so `Q467497` *Arne Garborg* is still protected and the original case of this test
    # still fails.
    #
    # The exemption is therefore narrow and self-evidencing: an `Lmul`/`Len` is allowed only when
    # this same file carries an `Amul` for that QID rescuing the value being replaced. Drop the
    # `Amul` and the overwrite fails again, which is the property worth having.
    preserved = {m.group(1) for m in
                 (re.match(r"^(Q[1-9][0-9]*)\tAmul\t", ln) for ln in lines()) if m}
    cjk = _cjk_block_qids()
    bad = []
    for ln in lines():
        m = re.match(r"^(Q[1-9][0-9]*)\tL(en|mul)\t", ln)
        if not m:
            continue
        if m.group(2) == "mul" and m.group(1) in cjk:
            continue
        if m.group(1) in preserved:
            continue
        bad.append(ln)
    assert not bad, (
        "overwriting the label of an existing item with nothing preserving the old value: "
        f"{bad[:3]}")


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
    #
    # **Either direction counts.** This asserted `LAST<TAB>P22<TAB>Q…` only, which was the
    # sole form that existed when it was written. Since 2026-08-25 a created person's
    # relationships are emitted BOTH ways in the same run -- `Q… P22 LAST` names the new item
    # as the parent of somebody who already exists -- and a roster batch can legitimately
    # produce only the reciprocal form, when none of the created people have a parent who
    # already carries a QID. Requiring the subject form alone made a correctly two-way batch
    # look like a regression.
    assert (re.search(r"^LAST	P22	Q[1-9][0-9]*", text, re.M)
            or re.search(r"^Q[1-9][0-9]*	P22	LAST", text, re.M)), (
        "no parent link anywhere in the batch, in either direction -- "
        "section 1/2 has stopped emitting P22")


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

    # The marker keeps the surname WHERE THERE IS ONE: it survives redaction and is
    # real data. A bare `NN` is correct for somebody who has no Latin name at all,
    # which is not the same thing as a redacted surname being dropped.
    #
    # **The case that forced the distinction**: `6000000186285688241` has `label_en`
    # and `label_mul` both EMPTY, their name living only in `cjk_names`. The redacted
    # branch fires and there is no surname to preserve. Asserting a surname on every
    # `NN` claimed a defect that was not there -- while hiding a real one, now queued:
    # a CJK-only person is created as `NN` and their recorded name is never consulted.
    bare_only = re.findall(r'Lmul\t"NN"', text)
    with_surname = re.findall(r'Lmul\t"NN \w', text)
    assert with_surname or bare_only, "an NN label of neither shape"
    if not with_surname:
        pytest.skip("every NN person here has no Latin name to preserve")

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
            # The parenthesised exclusion that stood here is GONE, and deliberately.
            # `classify_fields` now strips the brackets upstream and Emma has ruled that
            # every name-shaped bracketed token is an ordinary coequal `P734` *family
            # name*, so `hjorthorn` is subject to this assertion exactly like `Tunheim`.
            # Nothing here needs to know about brackets any more.
            if plan.get((token, "family"), ("", ""))[0]:
                continue          # Wikidata already has it
            if proposed.get(token):
                continue          # this run is creating it
            missing.append((geni_id, token))

    # **Since 2026-08-26 the name batch is capped at 10 items a run**, so a married
    # surname may legitimately have no item today and get one in three days -- Emma's
    # spec, `docs/daily-algorithm.md`. The claim this test makes is therefore not
    # "every surname has an item" but the stronger and still-checkable one: **a surname
    # that cannot be linked today must be RECORDED as carried, never silently dropped.**
    # Carrying without recording is what the assertion below would let through if it
    # simply stopped asserting.
    carried = set()
    cf = REPO / "reports" / "garborg-carry-forward.tsv"
    if cf.exists():
        for row in csv.reader(open(cf, encoding="utf-8"), delimiter="	"):
            if row and "name item missing" in row[-1]:
                carried.add(row[-1].split("name item missing:")[1].split("(")[0].strip())
    unrecorded = [(g, t) for g, t in missing if t not in carried]
    assert not unrecorded, (
        "a married surname has no item, none is being created, and the drop is NOT in "
        f"reports/garborg-carry-forward.tsv -- so the second P734 family name is lost "
        f"rather than deferred: {unrecorded[:5]}")




def test_every_link_to_an_existing_item_is_emitted_in_BOTH_directions():
    """A created person's links to items that already exist must be two-way, same run.

    **Emma, 2026-08-25:** *"you never actually did the 2-way relationship addin qith the
    creation of items that is completely possible but you just decide to fuck off and no do
    it because it goes QID PID LAST instead of LAST PID QID."*

    `LAST` cannot be the value in a statement whose subject is **also** newly created --
    two items minted in one run cannot point at each other, because `LAST` names only the
    most recent. That narrow limit was generalised into "no reciprocals at all", which left
    her repairing one-way links by hand for weeks.

    `Q141178381 P22 LAST` is ordinary QuickStatements. This test pins that every
    `LAST<TAB>P<TAB>Q…` inside a CREATE block has its partner going the other way, so the
    generalisation cannot creep back.
    """
    text = BATCH.read_text(encoding="utf-8")
    #: property -> the property that states the same fact from the other side.
    INVERSE = {"P22": "P40", "P25": "P40", "P26": "P26", "P3373": "P3373", "P40": ("P22", "P25")}

    # **The one exemption, and it is a list of specific pairs rather than a rule.** The
    # single-value guard drops a `Q… P22/P25 LAST` when that item already declares a parent:
    # `P25` is single-valued and a second trips the constraint. Its `LAST P40 Q…` partner
    # stays, deliberately, because `P40` is multi-valued and states the same fact from the
    # side that permits it. `build-garborg-day.py` records every such drop in
    # `reports/single-value-drops.tsv`, and only those subjects are exempt here -- so this
    # cannot widen into "one-way links are acceptable", which is the thing being pinned.
    exempt = set()
    drops = REPO / "reports" / "single-value-drops.tsv"
    if drops.exists():
        import csv as _csv
        for row in _csv.DictReader(drops.open(encoding="utf-8"), delimiter="\t"):
            exempt.add(row["subject"])

    missing = []
    for block in text.split("CREATE")[1:]:
        body = block.split("\nCREATE")[0]
        for line in body.splitlines():
            parts = line.split("\t")
            if len(parts) < 3 or parts[0] != "LAST":
                continue
            prop, value = parts[1], parts[2]
            if prop not in INVERSE or not value.startswith("Q"):
                continue
            wanted = INVERSE[prop]
            wanted = wanted if isinstance(wanted, tuple) else (wanted,)
            if value in exempt:
                continue
            if not any(f"{value}\t{w}\tLAST" in body for w in wanted):
                missing.append((prop, value))

    assert not missing, (
        "these links to an already-existing item were emitted one-way only; the reciprocal "
        f"`Q… P… LAST` is what makes the batch two-way: {missing[:6]}")


def test_the_contiguous_group_matches_what_emma_says_is_outside_it():
    """Her own knowledge, 2026-08-28, used as the fixture.

    She listed the humans she has edited that are **not** in the contiguous group. The
    unrestricted walk — following Wikidata relationships wherever they lead — put four of the
    seven *inside* it, because Johannes Bureus `Q633094` sits in the 1,339,227-item world tree
    and one edge into that swallows everything. Restricting the walk to items she has edited
    (*"the subgraph is stored and added to with my contributions"*) reproduces her list exactly.

    A test that only checked the roots were in would pass on the 1.34-million version too.
    """
    import importlib.util
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        "_gday", root / "scripts" / "build-garborg-day.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    have = mod.ledger()
    group = mod.wikidata_subgraph(universe=set(have.values()))

    inside = {"Q11959067": "Arne Olaus Fjørtoft Garborg",
              "Q633094": "Johannes Bureus",
              "Q141180409": "Magdalena Andersdotter"}
    outside = {"Q232803": "Emma Leonhart",
               "Q12598947": "Buyeo Taebi",
               "Q116150300": "Cecilie Ebbesdatter",
               "Q19657284": "Buyeo Deokjang",
               "Q116150298": "Jon Jonsen",
               "Q141189062": "Cecilie Jonsdatter",
               "Q141189110": "Tøre Jonsen",
               "Q141189080": "Lave"}
    for qid, who in inside.items():
        assert qid in group, f"{qid} {who} must be in the contiguous group"
    for qid, who in outside.items():
        assert qid not in group, (
            f"{qid} {who} is in the group and Emma says it is not — the walk has escaped her "
            f"own items, most likely through Bureus into the world tree")
    assert len(group) < 10_000, (
        f"the group is {len(group):,} items; that is the world tree, not her neighbourhood")


def _carries_marker():
    """`build-garborg-day._carries_marker`, loaded by path — the script is not importable."""
    import importlib.util
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "_bgd", REPO / "scripts" / "build-garborg-day.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._carries_marker


@pytest.mark.parametrize("label", [
    "nn Gunnarsdatter Frafjord",   # Q141198538 -- the one Emma caught
    "NN Gunnarsdatter Frafjord",
    "Nn Gunnarsdatter Frafjord",
    "NN Jonsdotter",
    "unknown Bloomfield",
    "Ukjent Garborg",
])
def test_a_marker_beside_a_real_name_still_takes_the_nn_path(label):
    """A marker plus a surname is an NN person, whatever the marker's case.

    **Emma, 2026-08-27, on `Q141198538`:** *"clearly has 'nn' as its first name however it was
    not produced as an NN person, so what happened, can you please fix the algorithm so it does
    no do this in the future?"*

    Her Geni name is `nn Gunnarsdatter /Frafjord/` — lowercase, and only the **first token** is
    the marker. The test that decided this once looked for Geni's redaction markers alone, so a
    label that merely *began* with one took the ordinary-name path and `nn` went out as part of
    her label. She then fixed the item by hand to *Daughter of Gunnar Torsteinson Frafjord*.

    `reports/partial-nn.csv` counts **9,539** people with a marker in one name field and a real
    name in the other, so this is a population rather than a curiosity. The fix landed in
    `_carries_marker`; this is what stops it regressing, which is the half of her instruction a
    code change alone does not satisfy.
    """
    assert _carries_marker()(label), (
        f"{label!r} contains an unknown-name marker and must take the NN path: "
        f"marker in mul, formulaic descriptions in the other languages")


@pytest.mark.parametrize("label", [
    "Ann Gunnarsdatter",      # 'Ann' merely starts with the letters of a marker
    "Nils Larsen Raunes",
    "Bergitte Gunnbjørnsdatter Aukland",
])
def test_an_ordinary_name_is_not_read_as_a_marker(label):
    """The other half: matching is on whole tokens, never on a prefix of one.

    `Ann` is the case that would break first — it starts with `nn`'s letters reversed and shares
    a prefix with nothing, but a substring test on markers is exactly the kind of widening that
    would swallow it. Real names must keep the ordinary path.
    """
    assert not _carries_marker()(label)


def test_no_redaction_marker_reaches_the_P1810_qualifier():
    """Neither form of private gets a `subject named as`. Emma, 2026-08-30.

    She had ruled on 08-29 that the marker went in verbatim, because `P1810` records what the
    source *displays*. `Q141223549` broke that: it carried `P1810 "Private"` while Geni's site
    shows `<private> Paulson` — a surname in none of the five exports holding her.

    > *"there are two different kinds of private on Jenny… this is some weird-ass backend
    > difference that affects the Gedcom export, but they display identically… so neither form
    > of private should be present as the qualifier."*

    Both forms are in the corpus — `<private> /Surname/` 19,945 and bare `Private` 99,645 — so
    which one a profile exports as is a backend artefact, and a qualifier built from it records
    our export rather than the display. `P1810` on a named person is untouched, which the
    second assertion pins so this cannot turn into "drop the qualifier".
    """
    marker = re.compile(r'\tP1810\t"(?:<private>|Private|NN|Ukjent|Unknown)\b', re.I)
    bad = [ln for ln in lines() if marker.search(ln)]
    assert not bad, f"a redaction marker reached P1810: {bad[:4]}"
    assert any("\tP1810\t" in ln for ln in lines()), (
        "P1810 vanished entirely -- named people must still carry what Geni renders")
