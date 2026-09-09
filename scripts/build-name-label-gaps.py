"""Which name items to add a label to first, ranked by how many of our people it unlocks.

Emma, 2026-08-18: *"We're going to be, of course, having to add labels in other languages
to the name objects."* This is the worklist for that, and its whole point is the
**ordering**: a name item is worth a label in proportion to how many people in this
corpus bear it, so `Olsdatter` outranks a surname carried by six.

`reports/mechanical-translation.md` measured the ceiling -- of the name-uses that resolve
to exactly one Wikidata name item, 71.0% already carry a Japanese label and can be
rendered with no transliteration at all. This report is the **complement**: the resolved
name-uses whose item has no label in the target language, which is exactly the work that
would move that number.

**It proposes no labels and invents no transliterations.** What katakana `Leonhart` takes
is not something to derive from a rule -- `CLAUDE.md` § *name modelling.txt* sends edge
cases to Emma rather than to a guess, and a wrong reading of a name is the kind of thing
that is painful to correct on Wikidata afterwards (§ *The purpose is to ADD to Wikidata,
not to correct it*). So every row is a question with a size attached, never an answer.

Two columns exist to make each row answerable without a lookup: `mul` and `en` carry
whatever the item is already labelled, because a `mul` label is often the native-script
form and is the natural seed for a rendering.

Reads `reports/name-item-languages.csv` and `reports/name-resolution.csv`. Offline, no
request, no merge.

    python scripts/build-name-label-gaps.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LANGS_CSV = REPO / "reports" / "name-item-languages.csv"
RES_CSV = REPO / "reports" / "name-resolution.csv"
OUT_CSV = REPO / "reports" / "name-label-gaps.csv"
OUT_MD = REPO / "reports" / "name-label-gaps.md"

#: Emma's label ladder, 2026-08-18: `mul`, then `en`, then `ja`, then `zh`, then the
#: rest. Only the languages the ladder actually names are ranked here; the wider set
#: lives in `name-item-languages.csv` for anyone who wants it.
TARGETS = ["mul", "en", "ja", "zh"]

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def main() -> None:
    have: dict[str, dict[str, str]] = {}
    with LANGS_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            have[row["qid"]] = row

    # qid -> (bearers, the token as we hold it, what kind of name it is)
    bearers: Counter = Counter()
    label_of: dict[str, tuple[str, str]] = {}
    with RES_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if (row.get("verdict") or "").strip() != "resolved":
                continue
            qids = [q for q in (row.get("qids") or "").replace(";", " ")
                    .replace(",", " ").split() if q.startswith("Q")]
            if len(qids) != 1:
                continue
            occ = int(row["occurrences"] or 0)
            bearers[qids[0]] += occ
            label_of.setdefault(qids[0], (row.get("name", ""), row.get("kind", "")))

    rows = []
    for qid, n in bearers.items():
        item = have.get(qid)
        if not item:
            continue
        missing = [l for l in TARGETS if not item.get(l)]
        if not missing:
            continue
        token, kind = label_of.get(qid, ("", ""))
        rows.append({
            "qid": qid,
            "our_token": token,
            "kind": kind,
            "bearers": n,
            "missing": " ".join(missing),
            "n_missing": len(missing),
            "mul": item.get("mul", ""),
            "en": item.get("en", ""),
            "ja": item.get("ja", ""),
            "zh": item.get("zh", ""),
        })

    rows.sort(key=lambda r: -r["bearers"])
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    per_lang = {l: [r for r in rows if l in r["missing"].split()] for l in TARGETS}
    total_uses = sum(bearers.values())

    lines = [
        "# Name items that need a label, ranked by how many of our people they unlock",
        "",
        f"**{len(rows):,} name items** carry our people's names but are missing a label "
        f"in at least one of {', '.join('`'+l+'`' for l in TARGETS)}. Ranked by bearers, "
        "because a label on a name 900 people carry is worth more than one on a name six "
        "people carry.",
        "",
        "This report proposes no labels. What katakana a name takes is a reading, not a "
        "derivation, and `name modelling.txt` sends that to Emma rather than to a rule.",
        "",
        "| language | items missing it | name-uses behind them |",
        "| --- | ---: | ---: |",
    ]
    for l in TARGETS:
        n = sum(r["bearers"] for r in per_lang[l])
        lines.append(f"| `{l}` | {len(per_lang[l]):,} | {n:,} |")
    lines += [
        "",
        f"For scale, {total_uses:,} name-uses resolve to exactly one name item at all.",
        "",
        "## The fifty that would unlock the most people",
        "",
        "`mul` and `en` are shown because an existing label is the natural seed for a "
        "rendering — often the native-script form.",
        "",
        "| our token | kind | bearers | missing | `mul` | `en` |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for r in rows[:50]:
        lines.append(f"| {r['our_token']} | {r['kind']} | {r['bearers']:,} | "
                     f"`{r['missing']}` | {r['mul']} | {r['en']} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(rows):,} name items missing at least one target label")
    for l in TARGETS:
        n = sum(r["bearers"] for r in per_lang[l])
        print(f"  {l:<4} {len(per_lang[l]):>7,} items   {n:>9,} name-uses behind them")
    print(f"wrote {OUT_CSV.relative_to(REPO)} and {OUT_MD.relative_to(REPO)}")


if __name__ == "__main__":
    main()
