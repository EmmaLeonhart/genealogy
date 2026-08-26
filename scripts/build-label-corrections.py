"""Corrective QuickStatements: the married name is the PRIMARY label in `en` AND in `mul`.

    python scripts/build-label-corrections.py

**Emma, 2026-08-24, after running the first batches:** *"already it is clear that you are
treating the married name as an alias, apparently aen, but in reality, the married name is
the primary label and the birth name is amul, and ideally its transliterations should be
present for Chinese and Japanese."*

So the model is:

    en    Aagot Garborg          <- the MARRIED name, primary
    mul   Aagot Garborg          <- the MARRIED name again. `mul` is the real label.
    Amul  Aagot Nyvold           <- the BIRTH name, an ALIAS
    ja    オーゴット・ガルボルグ      <- transliteration of the PRIMARY (married) form
    zh    奥高特·加尔博格

**The married name is the "real" name.** Emma, 2026-08-26: *"married name is always the
'real' name and applied as the primary mul label (first amul added if applicable) and then
the birth name is next as an amul. No aen are ever supposed to be added."* This file had the
birth name as `Lmul` — a **label**, not an alias — which disagreed with
`build-garborg-day.py`, where the married name is both labels and the birth name is `Amul`.
Two emitters, two models; her message settles it in favour of the second.

**`(first amul added if applicable)`** is why the existing `mul` is preserved: a label
REPLACES, so whatever the item currently reads in `mul` is emitted as an `Amul` before the
new label overwrites it. Usually that is the birth name this batch would add anyway; where
she has hand-edited it, it is something neither side would have reconstructed.

What the very first batch did instead: `en` and `mul` both carried the **birth** name, and
the married name went out as an `Aen` alias. That is wrong in three places at once — wrong
primary label, wrong `mul`, and an alias that should not exist.

**This corrects items that are already on Wikidata**, so it is written against what they
actually hold, downloaded in full (`out/garborg-new-items.json`) rather than against what
the batch intended. Emma has already hand-fixed `en` and `mul` on some of them, and those
are exactly the ones whose `ja`/`zh` are now stale: `Q141168785` reads *Aagot Garborg* in
`en` and `オーゴット・ニーヴォル` — Aagot **Nyvold** — in `ja`.

**A label edit REPLACES.** So a correction is only emitted where the current value differs
from the intended one, and never to write a value the item already has.

Writes `reports/wikidata-garborg-label-fixes.qs`.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
#: **Full items, never a summary.** `out/garborg-new-items.json` is a SUMMARY -- `geni`,
#: `label`, `props` per item and no `labels`/`aliases`/`claims` at all -- so this script read
#: `0 carry a Geni ID`, found every `current` label empty, and emitted nothing. It printed
#: that as *"0 items need correcting"*, which is the empty-join failure `tests/test_join_sanity.py`
#: exists for, wearing the costume of finished work. `out/model-vs-reality-items.json` is the
#: full-entity snapshot and covers all 38.
ITEMS = ROOT / "out" / "model-vs-reality-items.json"


def qs(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def translit_table():
    out = {}
    with open(ROOT / "reports" / "garborg-name-transliterations.tsv",
              encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["token"]] = (row["ja"], row["zh"])
    return out


def render(tokens, table):
    """(ja, zh) for a list of name tokens, or (None, None) if any is unknown.

    Partial is worse than absent: half a name in katakana and half in Latin is not a
    Japanese label, it is a broken one.
    """
    ja, zh = [], []
    for token in tokens:
        pair = table.get(token)
        if not pair:
            return None, None
        ja.append(pair[0])
        zh.append(pair[1])
    return "・".join(ja), "·".join(zh)


def main():
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    table = translit_table()

    geni_of = {}
    for qid, item in items.items():
        for st in item.get("claims", {}).get("P2600", []):
            geni_of[st["mainsnak"]["datavalue"]["value"]] = qid
    print(f"{len(items)} items downloaded, {len(geni_of)} carry a Geni ID")
    if not geni_of:
        sys.exit(f"{ITEMS.name} yielded no P2600 at all -- that is an unreadable snapshot, "
                 f"not an item with no Geni id. A summary file has no `claims` key and this "
                 f"join silently returns nothing. Re-fetch through full_entities.")

    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in geni_of and row["geni_id"] not in fields:
                fields[row["geni_id"]] = row

    lines = [
        "# Label corrections. Emma, 2026-08-26: the MARRIED name is the \"real\" name and is",
        "# the primary label in `en` AND in `mul`; the BIRTH name is an `Amul` ALIAS; the",
        "# transliterations follow the primary form. No `Aen` is ever added.",
        "#",
        "# A label REPLACES, so whatever `mul` currently holds is emitted as an `Amul`",
        "# FIRST, on the line above the `Lmul` that overwrites it. Some of those are her",
        "# own hand-edits and nothing else in this repo could reconstruct them.",
        "#",
        "# A label edit REPLACES, so only differences are emitted.",
        "",
    ]
    changed = unchanged = 0
    notes = []

    for geni_id, qid in sorted(geni_of.items(), key=lambda kv: kv[1]):
        row = fields.get(geni_id)
        if not row:
            notes.append((qid, geni_id, "no name fields in display-names.csv"))
            continue

        givn = " ".join((row.get("givn") or "").split())
        surn = " ".join((row.get("surn") or "").split())
        marnm = " ".join((row.get("marnm") or "").split())

        # Strip Geni's quoted nickname out of the given name -- it is `P1449` nickname,
        # not part of any label.
        import re
        given_tokens = [t for t in re.split(r"\s+", re.sub(r'["""\'][^"""\']+["""\']|\([^)]+\)',
                                                           " ", givn)) if t]

        birth_tokens = given_tokens + surn.split()
        married_tokens = given_tokens + marnm.split()
        # **`SURN` must be non-empty for `_MARNM` to be a married name.** `CLAUDE.md`
        # measured that 43% of `_MARNM` values are the ONLY surname on the record
        # because `SURN` is empty -- there it is the family name, not a married one.
        # Samuel Eivindsen Garborg is the case: `surn` empty, `marnm` Garborg. Reading
        # that as married would have written `mul` = "Samuel Eivindsen" and dropped his
        # surname out of the label entirely.
        has_married = bool(marnm) and bool(surn) and marnm.casefold() != surn.casefold()

        primary = " ".join(married_tokens if has_married else birth_tokens)
        secondary = " ".join(birth_tokens)
        if not primary:
            notes.append((qid, geni_id, "no usable name"))
            continue

        labels = items[qid].get("labels", {})
        current = {k: v.get("value", "") for k, v in labels.items()}

        current_aliases = {a.get("value") for a in
                           items[qid].get("aliases", {}).get("mul", [])}

        block = []
        if qs(primary) and current.get("en") != qs(primary):
            block.append(f'{qid}\tLen\t"{qs(primary)}"')
        if qs(primary) and current.get("mul") != qs(primary):
            # Preserve what `mul` holds before replacing it -- a label REPLACES.
            held = qs(current.get("mul", ""))
            if held and held != qs(primary) and held not in current_aliases:
                block.append(f'{qid}\tAmul\t"{held}"')
                current_aliases.add(held)
            block.append(f'{qid}\tLmul\t"{qs(primary)}"')
        if (qs(secondary) and qs(secondary) != qs(primary)
                and qs(secondary) not in current_aliases):
            block.append(f'{qid}\tAmul\t"{qs(secondary)}"')

        ja, zh = render(married_tokens if has_married else birth_tokens, table)
        if ja:
            if current.get("ja") != ja:
                block.append(f'{qid}\tLja\t"{ja}"')
            if current.get("zh") != zh:
                block.append(f'{qid}\tLzh\t"{zh}"')
        else:
            missing = [t for t in (married_tokens if has_married else birth_tokens)
                       if t not in table]
            notes.append((qid, geni_id, f"no transliteration for {', '.join(missing)}"))

        # The alias the first batch wrote is now the primary label, so remove it.
        for alias in items[qid].get("aliases", {}).get("en", []):
            if alias.get("value") in (qs(primary), qs(secondary)):
                block.append(f'-{qid}\tAen\t"{qs(alias["value"])}"')

        if block:
            marker = "married" if has_married else "birth name only"
            lines.append(f"# {qid}  {primary}  ({marker}, Geni {geni_id})")
            lines.extend(block)
            lines.append("")
            changed += 1
        else:
            unchanged += 1

    out = ROOT / "reports" / "wikidata-garborg-label-fixes.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {out.relative_to(ROOT)}")
    print(f"  {changed} items need correcting, {unchanged} already correct")
    if notes:
        print(f"  {len(notes)} could not be fully handled:")
        for qid, geni_id, why in notes:
            print(f"     {qid}  {why}")


if __name__ == "__main__":
    main()
