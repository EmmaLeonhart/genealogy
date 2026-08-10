"""What it would take to add Japanese (`ja`) Wikidata labels from Geni CJK names.

`reports/names-spec.md` names a tractable slice — *"4,500 already carry a CJK
string in Geni with an empty `ja` slot… addable with no language inference, only
a codepoint range."* This script makes that count reproducible and then tests
the "no inference" claim against the records. **The claim does not hold**, and
the finding is why.

**The rule is Emma's, 2026-08-10:** labels only for people carrying both a Geni
ID and a Wikidata item; never correct an existing label; never transliterate; a
`ja` label only where Wikidata's slot is empty.

**The finding.** For the Chinese profiles that make up this slice, Geni does not
put the name where a naive reader expects:

* the **family name** (孔, 曾, 高) sits in **`_MARNM`**, not `SURN`;
* the `SURN` slot holds a **place of origin / ancestral seat** (郡望) —
  `渤海蓨縣`, `湖南湘鄉`;
* `GIVN` holds the **personal name plus a courtesy name** (`紀鴻 粟誠`);
* and the written order is **surname-first**, so a `given + surname` join is
  also reversed.

So the slash-stripped display join — `白 孔` for Kong Bai (孔白), `紀鴻 粟誠
湖南湘鄉` for Zeng Jihong (曾紀鴻) — is a wrong label three ways over: reversed,
padded with a place, and missing the family name that is off in `_MARNM`.
Measured: of the people with a CJK `NAME`, **98% carry a CJK `_MARNM`** and
**85% carry a ≥3-character CJK `SURN`**. The "codepoint range is all you need"
path does not exist; forming the label needs a rule, and the rule is Emma's.

**This script therefore emits no QuickStatements.** There is no settled label
form to emit, and a batch of demonstrably-wrong labels is worse than none. It
writes the measurement, the decomposition, and a *candidate* assembly rule shown
next to the raw slots so its output can be judged — for review, not for sending.

Outputs (terminal, nothing leaves the machine):

* ``reports/ja-labels.md``   — the count, the finding, the decision
* ``reports/ja-labels.tsv``  — every addable person, raw slots and all forms

Inputs, all offline:

* ``out/merged.ged``               — the canonical Geni tree (``genimerge merge``)
* ``out/wikidata/p2600-all.tsv``   — qid<TAB>geni_id (``scripts/build-p2600-all.py``)
* ``wikidata/items/`` + its index  — the store (``genimerge wikidata-index``)
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

# The CJK codepoint range, taken from the one place that defines it so this
# stays consistent with `profilenames`' script classification.
_CJK_BODY = dict(profilenames.SCRIPT_RANGES)["cjk"]
CJK = re.compile(f"[{_CJK_BODY}]")


def _has_cjk(text: str | None) -> bool:
    return bool(text and CJK.search(text))


def _bears_cjk(name: model.Name) -> bool:
    """A record *bears CJK* if its value / given / surname slot has a CJK char."""
    return any(_has_cjk(t) for t in (name.full, name.given, name.surname))


def _cjk_form(name: model.Name) -> str:
    """The slash-stripped display join for one CJK record — one string, not three.

    Counting ``full``, ``given`` and ``surname`` separately made every record
    look self-contradictory (`誉田別命 /応神天皇/` splitting into three "distinct"
    forms), which is a decomposition of one name, not a disagreement.
    """
    return name.display.strip() or name.full.replace("/", "").strip()


def _candidate_label(name: model.Name) -> str:
    """A *candidate* ja label under the finding's rule — for review, not sending.

    Rule under test: the family name is in ``_MARNM``, the personal name is the
    first ``GIVN`` token, and the order is surname-first with no separator. So
    Kong Bai → 孔白, Zeng Jihong → 曾紀鴻, Lady Gao → 高. Shown beside the raw
    slots in the report so Emma can judge it; never applied in bulk here.
    """
    family = (name.married or "").strip()
    if not _has_cjk(family):
        return ""
    given_tokens = (name.given or "").split()
    personal = given_tokens[0] if given_tokens else ""
    if not _has_cjk(personal):
        return family  # place-of-origin only in GIVN/SURN; the family name alone
    return f"{family}{personal}"


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

    linked_geni = [g for g in tree.people if g in geni_to_qids]
    all_qids = sorted({q for g in linked_geni for q in geni_to_qids[g]})

    # Which items already carry a `ja` label (and `en`, for the report).
    ja_present: set[str] = set()
    en_label: dict[str, str] = {}
    with wikistore.StoreReader(STORE, INDEX) as reader:
        for qid, entity in reader.entities(all_qids).items():
            labels = entity.get("labels", {})
            if labels.get("ja", {}).get("value", "").strip():
                ja_present.add(qid)
            if labels.get("en", {}).get("value", ""):
                en_label[qid] = labels["en"]["value"]

    with_cjk = 0
    already_ja = 0
    rows: list[dict] = []             # the addable people (no `ja` yet)
    form_hist: dict[int, int] = defaultdict(int)
    cjk_marnm = 0                     # addable people with a CJK `_MARNM`
    surn_place = 0                    # addable people with a >=3-char CJK `SURN`

    for geni_id in linked_geni:
        person = tree.people[geni_id]
        cjk_records = [n for n in person.names if _bears_cjk(n)]
        if not cjk_records:
            continue
        with_cjk += 1

        qids = geni_to_qids[geni_id]
        if any(q in ja_present for q in qids):
            already_ja += 1
            continue

        forms: list[str] = []
        for n in cjk_records:
            f = _cjk_form(n)
            if f and f not in forms:
                forms.append(f)
        form_hist[len(forms)] += 1

        has_marnm = any(_has_cjk(n.married) for n in cjk_records)
        has_surn3 = any(
            sum(1 for c in (n.surname or "") if CJK.search(c)) >= 3
            for n in cjk_records
        )
        cjk_marnm += has_marnm
        surn_place += has_surn3

        rows.append({
            "geni_id": geni_id,
            "qids": qids,
            "en": next((en_label[q] for q in qids if q in en_label), ""),
            "n_forms": len(forms),
            "forms": forms,
            "records": [
                (n.given, n.surname, n.married, n.full) for n in cjk_records
            ],
            "candidate": _candidate_label(cjk_records[0]),
            "double": len(qids) > 1,
        })

    _write_tsv(rows)
    _write_report(len(linked_geni), with_cjk, already_ja, rows,
                  form_hist, cjk_marnm, surn_place)

    addable = len(rows)
    print(
        f"linked: {len(linked_geni)}  with CJK NAME: {with_cjk}  "
        f"already ja: {already_ja}  addable: {addable}"
    )
    print(f"  CJK _MARNM (family name): {cjk_marnm}  "
          f">=3-char CJK SURN (place): {surn_place}")
    print("  distinct CJK forms: " +
          ", ".join(f"{k}:{form_hist[k]}" for k in sorted(form_hist)))
    return 0


def _write_tsv(rows: list[dict]) -> None:
    TSV.parent.mkdir(parents=True, exist_ok=True)
    with TSV.open("w", encoding="utf-8") as fh:
        fh.write(
            "geni_id\tqid\ten_label\tn_cjk_forms\tcandidate_label\t"
            "given|surname|_MARNM per record\tdisplay_join_forms\n"
        )
        for r in rows:
            recs = " ;; ".join(
                f"{g}|{s}|{m}" for (g, s, m, _full) in r["records"]
            )
            fh.write(
                f"{r['geni_id']}\t{'|'.join(r['qids'])}\t{r['en']}\t"
                f"{r['n_forms']}\t{r['candidate']}\t{recs}\t"
                f"{' | '.join(r['forms'])}\n"
            )


def _decomp_sample(rows: list[dict], k: int = 12) -> str:
    lines = [
        "| geni_id | qid | en label | GIVN | SURN | `_MARNM` | display join | candidate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows[:k]:
        g, s, m, _full = r["records"][0]
        lines.append(
            f"| {r['geni_id']} | {'|'.join(r['qids'])} | {r['en'] or '—'} | "
            f"{g or '—'} | {s or '—'} | {m or '—'} | {r['forms'][0]} | "
            f"{r['candidate'] or '—'} |"
        )
    return "\n".join(lines)


def _write_report(
    linked: int,
    with_cjk: int,
    already_ja: int,
    rows: list[dict],
    form_hist: dict[int, int],
    cjk_marnm: int,
    surn_place: int,
) -> None:
    addable = len(rows)
    single = form_hist.get(1, 0)
    hist_rows = "\n".join(
        f"| {k} distinct CJK form{'s' if k != 1 else ''} | {form_hist[k]:,} |"
        for k in sorted(form_hist)
    )

    def pct(n: int) -> str:
        return f"{100 * n / addable:.1f}%" if addable else "—"

    REPORT.write_text(
        f"""# Japanese labels from Geni CJK names — what it would actually take

Generated by `scripts/build-ja-labels.py`, offline. The reproducible form of the
slice `reports/names-spec.md` named, and a test of its central claim.

**Emma's rule, 2026-08-10:** labels only for people carrying both a Geni ID and a
Wikidata item; never correct an existing label; never transliterate; a `ja` label
only where Wikidata's slot is empty.

## The count — reproduces the spec exactly

| | people |
| --- | ---: |
| linked (both IDs) | {linked:,} |
| …with a CJK `NAME` record | **{with_cjk:,}** |
| …of those, Wikidata already has a `ja` label | {already_ja:,} |
| …**no `ja` label — the addable slice** | **{addable:,}** |

`reports/names-spec.md` gave 5,383 and 4,500; this run reproduces both, so the
number is confirmed. What it means is the problem.

## The finding — "only a codepoint range" does not hold

The spec calls the slice *"addable without inferring anything… only a codepoint
range."* Against the records that is not true. For the Chinese profiles that fill
this slice, Geni stores the name where a naive reader will not look:

- the **family name** (孔, 曾, 高) is in **`_MARNM`**, not `SURN`;
- the `SURN` slot holds a **place of origin / ancestral seat** (郡望) —
  `渤海蓨縣`, `湖南湘鄉`;
- `GIVN` holds the **personal name and a courtesy name** (`紀鴻 粟誠`);
- the written order is **surname-first**, so a `given + surname` join is reversed.

Measured over the {addable:,} addable people:

| | people | share |
| --- | ---: | ---: |
| carry a **CJK `_MARNM`** (the real family name) | {cjk_marnm:,} | **{pct(cjk_marnm)}** |
| carry a **≥3-char CJK `SURN`** (a place, not a surname) | {surn_place:,} | **{pct(surn_place)}** |

So the slash-stripped display join is a wrong label three ways over — reversed,
padded with a place, and missing the family name. `白 孔` for Kong Bai (孔白);
`紀鴻 粟誠 湖南湘鄉` for Zeng Jihong (曾紀鴻).

And the forms disagree *within* a person too — the "romanised" record commonly
embeds the Han characters again, plus generation markers (`86, 53G`; `139,25世`):

| | people |
| --- | ---: |
{hist_rows}

Only **{single:,}** carry a single CJK form, and even those decompose the wrong
way — see the sample below.

## A candidate rule, shown for judging — NEEDS-DECISION, Emma

Under the finding, one rule fits the records: **label = `_MARNM` (family name) +
first `GIVN` token (personal name), surname-first, no separator.** Its output is
the `candidate` column below. It is **not applied and no batch is written** — a
QuickStatements file of labels this uncertain would be worse than none. This is
the case-by-case material for a decision, not the decision.

Open questions the rule does not settle: the courtesy name (`粟誠`) and place
(`湖南湘鄉`) are dropped — right for a label, but confirm; a person with only a
place in `SURN`/`GIVN` and a family name in `_MARNM` (Lady Gao → `高`) gets a
one-character label; and this rule is Chinese-shaped — whether the same profiles'
Japanese and Korean records behave the same way is unmeasured here.

## Decomposition sample — raw slots, nothing collapsed

{_decomp_sample(rows)}

…every addable person, with all raw slots, is in `reports/ja-labels.tsv`.

## What this deliberately does not do

Correct an existing label · transliterate · apply the candidate rule in bulk ·
emit a QuickStatements batch · touch `P735`/`P734` name items · send anything to
Wikidata.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
