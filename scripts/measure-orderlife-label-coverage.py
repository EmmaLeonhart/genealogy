"""How many of OUR people could take a label straight from order.life?

**Queue item 13. Emma, 2026-08-15:** asked whether order.life feeds the
seven-language work, and answered *"Yes — measure it properly first."*

She had said order.life *"doesn't have a whole lot of them"*. Sampled over 40,000
of its items it carries `ja` on 73%, plus `ko`, `he`, `zh`, `es` and `ru`. That is
a lot, and it matters because **a copied label is free and a transliterated one is
hand-built agentically**, name by name. If order.life covers a large share of the
people item 1 has to label, item 1 gets much smaller.

**What this does NOT do is reopen the rule.** The seven-language labels are
*made*, not copied, for everybody order.life does not cover — Emma's ruling
stands. This only measures the part that need not be made.

**Joined on BOTH identifiers.** `orderlife/analysis/persons.tsv` carries a
`geni_id` column *and* a `wikidata_qid` column, and a row may have either, both or
neither. Emma, 2026-08-15: *"WHY THE FUCK DID YOU JOIN ON THE GENI ID RATHER THAN
JOINING ON THE WIKIDATA ID? THE ORDER.LIFE THING HAS WIKIDATA IDS AS A PROPERTY ON
ITS OWN ITEMS."*

The first version joined on `geni_id` alone and reached **35,139** of the
**87,802** joinable rows — 27,727 Geni-only, **52,663 QID-only**, 7,412 both.
Those 52,663 were invisible to it, **60% of the joinable population**, and every
figure it produced was a floor rather than a measurement.

Never on names: `correspondence.md` forbids it and the 2026-08-14 session lost a
day to exactly that.

Writes `reports/orderlife-label-coverage.md` and `.csv`.

    py scripts/measure-orderlife-label-coverage.py
"""

from __future__ import annotations

import csv
import glob
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PERSONS = REPO / "orderlife" / "analysis" / "persons.tsv"
ITEMS = REPO / "orderlife" / "items"
OURS = REPO / "reports" / "derived-family.csv"
NAMES = REPO / "reports" / "display-names.csv"
OUT_MD = REPO / "reports" / "orderlife-label-coverage.md"
OUT_CSV = REPO / "reports" / "orderlife-label-coverage.csv"

csv.field_size_limit(10_000_000)

#: The seven Emma named, plus `mul`. Everything else is counted but not reported
#: per-language, because it is not what item 1 needs.
WANTED = ("en", "ja", "zh", "hi", "ar", "ru", "el", "mul")


def main() -> int:
    # -- our side ---------------------------------------------------------
    ours: set[str] = set()
    our_qid: dict[str, str] = {}          # our QID -> our geni id
    with OURS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ours.add(row["geni_id"])
            qid = (row.get("qid") or "").strip()
            if qid:
                our_qid.setdefault(qid, row["geni_id"])
    print(f"{len(ours):,} people in our tree, {len(our_qid):,} carrying a QID",
          flush=True)

    # -- the join, on the Geni ID and nothing else ------------------------
    # `persons.tsv` is QUOTE_NONE: a double quote in it is DATA, an epithet
    # inside a name. Reading it any other way glues rows together - 107,037
    # parsed as 106,909 before this was fixed.
    shared: dict[str, str] = {}           # our geni id -> order.life qid
    via: Counter[str] = Counter()
    joinable = 0
    with PERSONS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="	", quoting=csv.QUOTE_NONE):
            ol = (row.get("qid") or "").strip()
            if not ol:
                continue
            gid = (row.get("geni_id") or "").strip()
            wqid = (row.get("wikidata_qid") or "").strip()
            if gid or wqid:
                joinable += 1
            # Geni ID first where present - it is this repo's primary key - and
            # the Wikidata QID otherwise. Both are exact; neither is a name.
            if gid and gid in ours:
                if gid not in shared:
                    shared[gid] = ol
                    via["geni id"] += 1
            elif wqid and wqid in our_qid:
                mine = our_qid[wqid]
                if mine not in shared:
                    shared[mine] = ol
                    via["wikidata qid"] += 1
    print(f"{joinable:,} order.life rows carry at least one identifier", flush=True)
    print(f"{len(shared):,} matched to our people: "
          f"{via['geni id']:,} by Geni ID, {via['wikidata qid']:,} by Wikidata QID",
          flush=True)

    # -- what labels those order.life items actually have -----------------
    need = set(shared.values())
    labels: dict[str, dict[str, str]] = {}
    for path in sorted(glob.glob(str(ITEMS / "*.jsonl.gz"))):
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entity = json.loads(line)
                except json.JSONDecodeError:
                    continue
                qid = entity.get("id")
                if qid in need:
                    got = {}
                    for lang, value in (entity.get("labels") or {}).items():
                        text = value.get("value") if isinstance(value, dict) else value
                        if text:
                            got[lang] = text
                    labels[qid] = got
    print(f"{len(labels):,} of those order.life items are in the vendored store",
          flush=True)

    # -- which of OUR people still lack a label, and could take one -------
    have_en: set[str] = set()
    with NAMES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if (row.get("wikidata_en") or "").strip():
                have_en.add(row["geni_id"])

    per_lang: Counter[str] = Counter()
    rows = []
    for gid, qid in sorted(shared.items()):
        got = labels.get(qid, {})
        for lang in WANTED:
            if got.get(lang):
                per_lang[lang] += 1
        rows.append([gid, qid,
                     *[got.get(lang, "") for lang in WANTED]])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "orderlife_qid", *WANTED])
        writer.writerows(rows)

    L: list[str] = []
    add = L.append
    add("# What order.life could label for us, for free")
    add("")
    add("**Queue item 13.** Emma, 2026-08-15, on whether order.life feeds the")
    add("seven-language work: *\"Yes — measure it properly first.\"*")
    add("")
    add("**Joined on the Geni ID where present and the Wikidata QID otherwise**,")
    add("never on names. Joining on the Geni ID alone reached 35,139 of 87,802")
    add("joinable rows and missed the 52,663 that carry only a QID.")
    add("")
    add("| | count |")
    add("| --- | ---: |")
    add(f"| people in our tree | {len(ours):,} |")
    add(f"| order.life rows carrying either identifier | {joinable:,} |")
    add(f"| …matched by Geni ID | {via['geni id']:,} |")
    add(f"| …matched by Wikidata QID | {via['wikidata qid']:,} |")
    add(f"| **people on both sides** | **{len(shared):,}** |")
    add(f"| …whose order.life item is in the vendored store | {len(labels):,} |")
    add("")
    add("## Labels available on the shared people")
    add("")
    add("| language | our people who could take it from order.life |")
    add("| --- | ---: |")
    for lang in WANTED:
        add(f"| `{lang}` | {per_lang[lang]:,} |")
    add("")
    add("**This does not reopen the rule.** The seven-language labels are *made*,")
    add("not copied, for everybody order.life does not cover — Emma's ruling stands.")
    add("This measures only the part that need not be made.")
    add("")
    add("Every shared person is a row in `reports/orderlife-label-coverage.csv`")
    add("with whatever order.life has for them.")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\nwrote {OUT_MD} and {OUT_CSV}")
    for lang in WANTED:
        print(f"  {lang:<5} {per_lang[lang]:>8,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
