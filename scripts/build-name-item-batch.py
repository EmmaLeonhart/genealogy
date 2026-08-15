"""Name items: link the ones that exist, create the ones that do not.

Queue item 10, and the prerequisite for everything downstream — Emma's ruling on
transliteration, 2026-08-16: *"the name objects can actually be used in this
because we can build the name objects first of all and establish all the labels
for them… We then only need to potentially not have that many raw things that we
need to do for the transliteration."* Label a **token** once in its name item and
every bearer inherits it; per-person work would be the same job multiplied by
bearer count.

**One item per USAGE, not per string.** `CLAUDE.md` § *"Jackson Jackson
Jackson"*: a token used as a given name, a surname **and** a patronymic is three
items that happen to share a spelling. Nothing here adjudicates between them —
that was the dominance ratio Emma threw out on 2026-08-15.

**Three usages, three item types:**

| usage | `P31` of the name item | linked by |
| --- | --- | --- |
| given name | `Q202444` | `P735` |
| family name | `Q101352` | `P734` |
| patronymic | `Q110874` | `P735` + `P3831` → `Q110874` |

**Nothing is created that already exists**, which is the failure mode that
damages Wikidata rather than wasting a run. **A name whose label is `ambiguous`
counts as existing** — several items share it, and the first run of this script
treated only `resolved` that way and would have created a tenth `Maria`. Those
are held for review; choosing among nine items is a judgement, and so is deciding
there are none. Two sources are checked:
`reports/name-resolution.csv` (labels matched offline against the downloaded
store, 15,831 resolved) and `reports/patronymic-items.csv` (**all 633** Wikidata
patronymic items).

**A created patronymic carries its derivation.** `P31` → `Q110874`, `P144` →
*based on* the name it derives from, and the derivation in the description too —
Emma wanted both. 119 of the 633 existing ones already do this, which is where
the shape comes from.

**Particles, ordinals and placeholders are excluded and counted.** `de`, `von`,
`van`, `y`, `la` are `SPFX` and not names; `I`/`II`/`III` in a given slot are
regnal numerals; `NN`, `???` are the placeholder vocabulary. Together they are
the loudest tokens in the corpus and none of them is a name.

Writes `reports/wikidata-name-items.json` and `reports/name-item-plan.csv`.

    py scripts/build-name-item-batch.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CLASSES = REPO / "reports" / "name-classes.csv"
RESOLUTION = REPO / "reports" / "name-resolution.csv"
PATRONYMICS = REPO / "reports" / "patronymic-items.csv"
JSON_OUT = REPO / "reports" / "wikidata-name-items.json"
CSV_OUT = REPO / "reports" / "name-item-plan.csv"

csv.field_size_limit(10 ** 7)

GIVEN_NAME_ITEM, FAMILY_NAME_ITEM, PATRONYMIC_ITEM = "Q202444", "Q101352", "Q110874"
INSTANCE_OF, BASED_ON = "P31", "P144"

#: Reliable patronymic morphology. `-son`/`-sen` are deliberately absent: they
#: also end ordinary inherited surnames and a few real given names (`Jefferson`,
#: 30 bearers). `reports/name-classes.md` has the per-suffix measurement.
RELIABLE_PATRONYMIC = ("sdottir", "sdóttir", "sdatter", "sdotter", "dottir",
                       "dóttir", "datter", "dotter", "ovich", "evich", "ovna",
                       "evna", "ivna", "ovych", "yevich")

PARTICLES = {"de", "di", "da", "del", "della", "des", "du", "van", "von", "der",
             "den", "ten", "ter", "la", "le", "y", "i", "of", "af", "av", "til",
             "zu", "dos", "das", "do", "el", "al", "ul", "bin", "bint", "ibn",
             "ap", "abu"}
ORDINALS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII"}
PLACEHOLDERS = {"nn", "n.n.", "n", "?", "??", "???", "????", "*", "**", "***",
                "unknown", "private", "<private>", "'", "-", "--", ".",
                # A bare quote character reached the batch as a name item on the
                # first run. Geni's nickname field puts quotes round a value and
                # the tokeniser split one off on its own.
                '"', "''", '""', "``", "--", "---"}

#: Below this many bearers a token is not worth an item of its own yet. Not a
#: confidence threshold — a workload one; the tail is 70% single-use strings.
MIN_BEARERS = 5


def patronymic_marker(token: str) -> str:
    low = token.lower()
    for suffix in RELIABLE_PATRONYMIC:
        if low.endswith(suffix) and len(low) > len(suffix) + 1:
            return suffix
    return ""


def main() -> int:
    for path in (CLASSES, RESOLUTION, PATRONYMICS):
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            return 1

    # What already exists, by name string.
    # **`ambiguous` means an item EXISTS, and must never become a creation.**
    # The first run of this script treated only `resolved` as existing and would
    # have created a tenth `Maria` given-name item on top of the nine Wikidata
    # already has, and duplicates are the one failure mode `CLAUDE.md` says
    # damages Wikidata rather than merely wasting a run. Ambiguous names are held
    # for review instead: choosing between nine items is a judgement, but so is
    # deciding there are none.
    resolved: dict[str, dict[str, str]] = {}
    ambiguous: dict[str, set] = {}
    for r in csv.DictReader(RESOLUTION.open(encoding="utf-8", newline="")):
        if r["verdict"] == "resolved" and r["qids"]:
            resolved.setdefault(r["name"], {})[r["kind"]] = r["qids"].split("|")[0].strip()
        elif r["verdict"].startswith("ambiguous"):
            ambiguous.setdefault(r["name"], set()).add(r["kind"])
    patro_items = {}
    for r in csv.DictReader(PATRONYMICS.open(encoding="utf-8", newline="")):
        for key in (r["label"], r["native_label"]):
            if key:
                patro_items[key.lower()] = r["qid"]
    print(f"{len(resolved):,} name strings already resolve to an item; "
          f"{len(patro_items):,} patronymic items exist")

    rows, edits = [], []
    counts: Counter = Counter()
    for r in csv.DictReader(CLASSES.open(encoding="utf-8", newline="")):
        token = r["token"]
        low = token.lower()
        if r["placeholder"] or low in PLACEHOLDERS:
            counts["excluded: placeholder"] += 1
            continue
        if low in PARTICLES or token in ORDINALS:
            counts["excluded: particle or ordinal"] += 1
            continue

        marker = patronymic_marker(token)
        usages = []
        if marker:
            usages.append(("patronymic", PATRONYMIC_ITEM, int(r["bearers"])))
        else:
            if int(r["as_given"]):
                usages.append(("given", GIVEN_NAME_ITEM, int(r["as_given"])))
            if int(r["as_surname"]):
                usages.append(("family", FAMILY_NAME_ITEM, int(r["as_surname"])))

        for usage, type_qid, bearers in usages:
            if bearers < MIN_BEARERS:
                counts[f"below {MIN_BEARERS} bearers"] += 1
                continue
            if usage == "patronymic":
                existing = patro_items.get(low)
            else:
                existing = resolved.get(token, {}).get(
                    "given" if usage == "given" else "family")
            kind = "given" if usage == "given" else "family"
            is_ambiguous = (usage != "patronymic"
                            and kind in ambiguous.get(token, set()))
            action = ("link" if existing
                      else "AMBIGUOUS - review, do not create" if is_ambiguous
                      else "create")
            rows.append({"token": token, "usage": usage, "bearers": bearers,
                         "script": r["script"], "marker": marker,
                         "existing_qid": existing or "",
                         "action": action})
            if existing:
                counts[f"{usage}: link"] += 1
                continue
            if is_ambiguous:
                counts[f"{usage}: ambiguous, held"] += 1
                continue
            counts[f"{usage}: create"] += 1
            entry = {
                "id": f"name_item:{usage}:{token}",
                "type": "create_name_item",
                "source": "reports/name-classes.csv",
                "subject": {"qid": None},
                "requires": [],
                "labels": {"mul": token},
                "statements": [{"property": INSTANCE_OF, "value": type_qid,
                                "references": []}],
                "usage": usage,
                "bearers": bearers,
                "script": r["script"],
            }
            if usage == "patronymic":
                # The base name, if we can see it. `P144` is what 119 of the 633
                # existing patronymic items use; the description carries it too,
                # which is what Emma asked for.
                base = re.sub(r"(s?d[oó]tt?ir|s?datter|s?dotter|ovich|evich|"
                              r"ovna|evna|ivna|ovych|yevich)$", "", token,
                              flags=re.I)
                entry["derived_from_text"] = base
                base_qid = resolved.get(base, {}).get("given")
                if base_qid:
                    entry["statements"].append(
                        {"property": BASED_ON, "value": base_qid, "references": []})
                entry["descriptions"] = {
                    "en": f"patronymic derived from {base}" if base else "patronymic"}
            edits.append(entry)

    rows.sort(key=lambda r: -r["bearers"])
    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    JSON_OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    print(f"\nwrote {CSV_OUT} ({len(rows):,} name items planned)")
    print(f"wrote {JSON_OUT} ({len(edits):,} to create)\n")
    for k, v in counts.most_common():
        print(f"  {v:>7,}  {k}")
    linked = sum(1 for r in rows if r["action"] == "link")
    print(f"\n  {linked:,} link an item that already exists, "
          f"{len(edits):,} create one")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
