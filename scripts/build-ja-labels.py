"""Propose Japanese (`ja`) Wikidata labels from Geni CJK name records.

This makes reproducible the measurement `reports/names-spec.md` states from an
ad-hoc pass — of the linked people, how many carry a CJK Geni ``NAME`` and lack
a ``ja`` label on Wikidata — and turns it into a candidate list.

**The rule is Emma's, 2026-08-10, and this script does not exceed it.** Labels
are proposed only for people carrying **both** a Geni ID and a Wikidata item; an
existing label is never touched; nothing is transliterated. A ``ja`` label is
proposed only where the slot is **empty** and the string is **already present in
CJK** in the Geni record — no language inference beyond "does this contain a CJK
codepoint", which is a property of the bytes.

**Ambiguity is shown, never resolved.** Per the spec's step 3, a person whose
CJK ``NAME`` records disagree (more than one distinct CJK string) is listed for
Emma rather than assigned a label here.

**One decision is still open and this script flags rather than hides it:** what
string forms the label. Geni writes ``誉田別命 /応神天皇/`` — given ``誉田別命`` and
surname ``応神天皇`` (a reign name, not a family name), slashes and all. The raw
value, the slash-stripped display join, and either slot alone are all different
labels, and nothing in the data ranks them. The QuickStatements batch uses the
display join as a first cut and says so; the report foregrounds the choice.

Terminal output only, never sent to Wikidata:

* ``reports/ja-labels.md``          — the measurement and the split, with samples
* ``reports/ja-labels.tsv``         — every candidate, both buckets, full detail
* ``out/wikidata/ja-labels.qs``     — QuickStatements for the unambiguous subset

Inputs, all offline:

* ``out/merged.ged``                — the canonical Geni tree (``genimerge merge``)
* ``out/wikidata/p2600-all.tsv``    — qid<TAB>geni_id (``scripts/build-p2600-all.py``)
* ``wikidata/items/`` + its index   — the store (``genimerge wikidata-index``)
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import gedcom, model, profilenames, wikistore  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MERGED = ROOT / "out" / "merged.ged"
P2600_ALL = ROOT / "out" / "wikidata" / "p2600-all.tsv"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
STORE = ROOT / "wikidata" / "items"

REPORT = ROOT / "reports" / "ja-labels.md"
TSV = ROOT / "reports" / "ja-labels.tsv"
QS = ROOT / "out" / "wikidata" / "ja-labels.qs"

# The CJK codepoint range, taken from the one place that defines it so this
# stays consistent with `profilenames`' script classification.
_CJK_BODY = dict(profilenames.SCRIPT_RANGES)["cjk"]
CJK = re.compile(f"[{_CJK_BODY}]")


def _cjk_strings(name: model.Name) -> list[str]:
    """The CJK-bearing forms of one NAME record, de-duplicated, order kept.

    Checks the whole value and the given/surname slots. ``_MARNM`` is skipped:
    in CJK records it is the *romanised* slot, so it carries Latin, not the
    native string this is looking for.
    """
    out: list[str] = []
    for text in (name.full, name.given, name.surname):
        text = (text or "").strip()
        if text and CJK.search(text) and text not in out:
            out.append(text)
    return out


def _display_label(name: model.Name) -> str:
    """A first-cut ``ja`` label: the slash-stripped display join.

    This is *a* reading of the record, not the reading — see the module
    docstring. Reported and emitted so the shape exists; the choice is Emma's.
    """
    return name.display.strip()


def load_geni_to_qids(path: Path) -> dict[str, list[str]]:
    """geni_id -> [qid, ...] from the positional ``qid<TAB>geni_id`` file."""
    mapping: dict[str, list[str]] = defaultdict(list)
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, geni_id = line.split("\t")
            if geni_id.startswith("geni:"):
                geni_id = geni_id[len("geni:"):]
            if qid not in mapping[geni_id]:
                mapping[geni_id].append(qid)
    return dict(mapping)


def main() -> int:
    for needed, hint in (
        (MERGED, "run `genimerge merge`"),
        (P2600_ALL, "run `scripts/build-p2600-all.py`"),
        (INDEX, "run `genimerge wikidata-index`"),
    ):
        if not needed.exists():
            print(f"{needed} not found - {hint}", file=sys.stderr)
            return 1

    tree = model.build_tree(gedcom.stream_file(MERGED))
    geni_to_qids = load_geni_to_qids(P2600_ALL)

    # The linked population: our people who carry a Wikidata item via P2600.
    linked_geni = [g for g in tree.people if g in geni_to_qids]
    all_qids = sorted({q for g in linked_geni for q in geni_to_qids[g]})

    # Which of those items already carry a `ja` label (and `en`, for the report).
    ja_present: set[str] = set()
    en_label: dict[str, str] = {}
    with wikistore.StoreReader(STORE, INDEX) as reader:
        for qid, entity in reader.entities(all_qids).items():
            labels = entity.get("labels", {})
            if "ja" in labels and labels["ja"].get("value", "").strip():
                ja_present.add(qid)
            en = labels.get("en", {}).get("value", "")
            if en:
                en_label[qid] = en

    # Rows. One per linked person that carries at least one CJK NAME.
    proposals: list[dict] = []  # exactly one distinct CJK string, no `ja` yet
    ambiguous: list[dict] = []  # >1 distinct CJK string, no `ja` yet
    already_ja = 0              # has a CJK NAME but Wikidata already has `ja`
    with_cjk = 0

    for geni_id in linked_geni:
        person = tree.people[geni_id]
        qids = geni_to_qids[geni_id]

        cjk_records = [n for n in person.names if _cjk_strings(n)]
        if not cjk_records:
            continue
        with_cjk += 1

        # A person is "already labelled" if any of their items carries `ja`.
        if any(q in ja_present for q in qids):
            already_ja += 1
            continue

        distinct = []
        for n in cjk_records:
            for s in _cjk_strings(n):
                if s not in distinct:
                    distinct.append(s)

        en = next((en_label[q] for q in qids if q in en_label), "")
        row = {
            "geni_id": geni_id,
            "qids": qids,
            "en": en,
            "n_cjk_records": len(cjk_records),
            "distinct": distinct,
            "label": _display_label(cjk_records[0]),
            "double": len(qids) > 1,
        }
        # "Unambiguous" = one distinct CJK string across all CJK records, and the
        # person maps to a single item. Everything else is Emma's to look at.
        if len(distinct) == 1 and len(qids) == 1:
            proposals.append(row)
        else:
            ambiguous.append(row)

    _write_tsv(proposals, ambiguous)
    n_qs = _write_qs(proposals)
    _write_report(
        len(linked_geni), with_cjk, already_ja, proposals, ambiguous, n_qs
    )

    print(
        f"linked: {len(linked_geni)}  with CJK NAME: {with_cjk}  "
        f"already ja: {already_ja}  proposals: {len(proposals)}  "
        f"ambiguous: {len(ambiguous)}  qs statements: {n_qs}"
    )
    return 0


def _write_tsv(proposals: list[dict], ambiguous: list[dict]) -> None:
    TSV.parent.mkdir(parents=True, exist_ok=True)
    with TSV.open("w", encoding="utf-8") as fh:
        fh.write("bucket\tgeni_id\tqid\ten_label\tn_cjk_records\tproposed_label\tdistinct_cjk\n")
        for bucket, rows in (("propose", proposals), ("ambiguous", ambiguous)):
            for r in rows:
                fh.write(
                    f"{bucket}\t{r['geni_id']}\t{'|'.join(r['qids'])}\t{r['en']}\t"
                    f"{r['n_cjk_records']}\t{r['label']}\t{' | '.join(r['distinct'])}\n"
                )


def _write_qs(proposals: list[dict]) -> int:
    QS.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with QS.open("w", encoding="utf-8") as fh:
        fh.write(
            "# ja labels proposed from Geni CJK NAME records. Provisional label\n"
            "# form: the slash-stripped display join. See reports/ja-labels.md -\n"
            "# the label string is Emma's open decision. Nothing here is sent.\n"
        )
        for r in proposals:
            label = r["label"].replace('"', '\\"')
            fh.write(f'{r["qids"][0]}\tLja\t"{label}"\n')
            n += 1
    return n


def _sample(rows: list[dict], k: int = 15) -> str:
    lines = ["| geni_id | qid | en label | CJK NAME record(s) | proposed `ja` |",
             "| --- | --- | --- | --- | --- |"]
    for r in rows[:k]:
        distinct = " · ".join(r["distinct"])
        lines.append(
            f"| {r['geni_id']} | {'|'.join(r['qids'])} | {r['en'] or '—'} | "
            f"{distinct} | {r['label']} |"
        )
    return "\n".join(lines)


def _write_report(
    linked: int,
    with_cjk: int,
    already_ja: int,
    proposals: list[dict],
    ambiguous: list[dict],
    n_qs: int,
) -> None:
    doubles = sum(1 for r in ambiguous if r["double"])
    REPORT.write_text(
        f"""# Japanese labels proposable from Geni CJK names

Generated by `scripts/build-ja-labels.py`, offline. This is the reproducible
form of the count `reports/names-spec.md` gave from an ad-hoc pass, and the
candidate list that follows from it.

**The rule, Emma 2026-08-10:** labels only for people carrying both a Geni ID
and a Wikidata item; never correct an existing label; never transliterate. A
`ja` label is proposed only where Wikidata's slot is **empty** and the Geni
record **already holds a CJK string** — no language inference beyond a codepoint
range.

## The count

| | people |
| --- | ---: |
| linked (both IDs) | {linked:,} |
| …with a CJK `NAME` record | **{with_cjk:,}** |
| …of those, Wikidata already has a `ja` label | {already_ja:,} |
| …**no `ja` label — the addable slice** | **{len(proposals) + len(ambiguous):,}** |
| of that slice: one distinct CJK string (proposable) | {len(proposals):,} |
| of that slice: several distinct CJK strings (for Emma) | {len(ambiguous):,} |

`reports/names-spec.md` gave 5,383 with a CJK `NAME` and 4,500 addable from an
earlier tree; this run measures the current merged tree. The split into
proposable vs. ambiguous is new here — the spec's step 3 (*"if more than one, do
not choose"*) is a real bucket, not a footnote.

## The open decision, before any of these ships — NEEDS-DECISION, Emma

**What string forms the `ja` label.** Geni writes e.g. `誉田別命 /応神天皇/`: given
`誉田別命`, surname `応神天皇`, which is a reign name rather than a family name. The
raw value, the slash-stripped join (`誉田別命 応神天皇`), and either slot alone are
all different labels, and nothing in the data ranks them. `out/wikidata/ja-labels.qs`
uses the **slash-stripped display join** as a first cut so the batch exists in a
runnable shape — it is not a decision that the join is right.

## Proposable — one distinct CJK string ({len(proposals):,})

{_sample(proposals)}

…{max(0, len(proposals) - 15):,} more in `reports/ja-labels.tsv`.

## Ambiguous — shown, not resolved ({len(ambiguous):,})

{doubles:,} of these are people whose Geni ID maps to more than one Wikidata
item (the `doubles` case), where "does Wikidata have a `ja` label" is itself
per-item. The rest carry more than one distinct CJK string across their `NAME`
records.

{_sample(ambiguous)}

…full list in `reports/ja-labels.tsv`.

## What this deliberately does not do

Correct an existing label · transliterate · pick between name variants · touch
`P735`/`P734` name items · send anything to Wikidata.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
