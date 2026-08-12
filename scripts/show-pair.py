"""One person, both sides, readable — every QID and PID resolved to its label.

Emma, 2026-08-11: *"the Wikidata stuff is not human-readable at all. You
absolutely need to fetch the English-language labels of the stuff it's
referencing for both the properties and these other things."*

Nothing is summarised or dropped from the Wikidata side: every statement, every
qualifier, every reference snak, with `precision` decoded so a year-precision
date cannot be mistaken for a day-precision one.

The Geni side omits exactly four line types — `FAMS`, `RFN`, `SUBM`, `CHAN` —
Emma's rule of 2026-08-11, because the FAM records carry that information
directly and the pointer lines say nothing on their own. What is omitted is
printed as a count, never silently.

    py scripts/show-pair.py 6000000038740385839
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from genimerge import wikilabels, wikistore  # noqa: E402

importlib_source = __import__("importlib.util", fromlist=["util"])
_spec = importlib_source.spec_from_file_location("_fsp", REPO_ROOT / "scripts" / "find-small-pair.py")
_fsp = importlib_source.module_from_spec(_spec)
_spec.loader.exec_module(_fsp)

STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
LABELS = REPO_ROOT / "out" / "wikidata" / "labels.tsv"

#: Emma's rule, 2026-08-11. Ignored on the individual's own record only.
IGNORED_TAGS = ("FAMS", "RFN", "SUBM", "CHAN")


def render_time(value: dict) -> str:
    """A Wikidata time value, with its precision spelled out."""
    text = value.get("time", "")
    code = value.get("precision")
    name = wikilabels.PRECISION.get(code, f"precision {code}")
    calendar = value.get("calendarmodel", "").rsplit("/", 1)[-1]
    extra = "" if calendar == "Q1985727" else f", calendar {calendar}"
    return f"{text}  [{name}{extra}]"


def render_value(snak: dict, labels: wikilabels.LabelCache) -> str:
    kind = snak.get("snaktype")
    if kind == "somevalue":
        return "SOME VALUE (unknown value)"
    if kind == "novalue":
        return "NO VALUE"
    datavalue = snak.get("datavalue") or {}
    value = datavalue.get("value")
    if isinstance(value, dict):
        if "id" in value:
            return labels.describe(value["id"])
        if "time" in value:
            return render_time(value)
        if "text" in value:
            return f'"{value["text"]}"@{value.get("language")}'
        if "amount" in value:
            return str(value["amount"])
        return str(value)
    return str(value)


def render_item(entity: dict, labels: wikilabels.LabelCache) -> list[str]:
    out: list[str] = []
    claims = entity.get("claims") or {}
    for prop in sorted(claims):
        for statement in claims[prop]:
            main = statement.get("mainsnak") or {}
            rank = statement.get("rank", "")
            out.append(
                f"{labels.describe(prop)} = {render_value(main, labels)}"
                + (f"   [rank {rank}]" if rank != "normal" else "")
            )
            for qprop, snaks in (statement.get("qualifiers") or {}).items():
                for snak in snaks:
                    out.append(
                        f"    qualifier  {labels.describe(qprop)} = {render_value(snak, labels)}"
                    )
            for n, reference in enumerate(statement.get("references") or [], 1):
                for rprop, snaks in (reference.get("snaks") or {}).items():
                    for snak in snaks:
                        out.append(
                            f"    ref {n}      {labels.describe(rprop)} = "
                            f"{render_value(snak, labels)}"
                        )
            out.append("")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("geni_id")
    ap.add_argument(
        "--all-lines",
        action="store_true",
        help="keep FAMS/RFN/SUBM/CHAN instead of omitting them",
    )
    args = ap.parse_args()

    pairs = _fsp.read_pairs()
    qid = pairs.get(args.geni_id)

    lines = _fsp.extract_record(args.geni_id)
    kept, dropped = [], 0
    for line in lines:
        parts = line.split(None, 2)
        if not args.all_lines and len(parts) >= 2 and parts[0] == "1" and parts[1] in IGNORED_TAGS:
            dropped += 1
            continue
        # CHAN's DATE/TIME sit under it at level 2 and go with it.
        if not args.all_lines and kept and kept[-1].startswith("1 CHAN"):
            pass
        kept.append(line)

    # Drop the sub-lines of an omitted level-1 tag as well.
    pruned: list[str] = []
    skipping = False
    for line in lines:
        parts = line.split(None, 2)
        if len(parts) >= 2 and parts[0] == "1":
            skipping = not args.all_lines and parts[1] in IGNORED_TAGS
            if skipping:
                dropped += 0
                continue
        elif skipping:
            continue
        pruned.append(line)
    kept = pruned
    dropped = len(lines) - len(kept)

    print(f"GENI {args.geni_id}   WIKIDATA {qid or '(no link)'}")
    print()
    print("=" * 78)
    print("GENI — the INDI record")
    print("=" * 78)
    for line in kept:
        print(line)
    if dropped:
        print(f"\n(omitted {dropped} lines: {', '.join(IGNORED_TAGS)} — Emma's rule 2026-08-11)")

    fams = {
        parts[2]
        for parts in (l.split() for l in lines)
        if len(parts) >= 3 and parts[1] in {"FAMS", "FAMC"} and parts[2].startswith("@F")
    }
    for xref, body in _fsp.extract_families(fams).items():
        print()
        print("=" * 78)
        print(f"GENI — {xref}")
        print("=" * 78)
        for line in body:
            print(line)

    if not qid:
        return 0

    with wikistore.StoreReader(STORE, INDEX) as reader:
        entity = reader.entities([qid]).get(qid)
    if entity is None:
        print(f"\n{qid} is not in the store")
        return 0

    labels = wikilabels.LabelCache(LABELS)
    labels.resolve(wikilabels.collect_ids(entity))

    print()
    print("=" * 78)
    print(f"WIKIDATA — {qid}, every statement with qualifiers and references")
    print("=" * 78)
    for line in render_item(entity, labels):
        print(line)

    item_labels = entity.get("labels") or {}
    descriptions = entity.get("descriptions") or {}
    aliases = entity.get("aliases") or {}
    distinct = sorted({v["value"] for v in item_labels.values()})
    print("=" * 78)
    print("WIKIDATA — labels, descriptions, aliases, sitelinks")
    print("=" * 78)
    print(f"{len(item_labels)} labels, {len(distinct)} distinct string(s):")
    for text in distinct:
        langs = sorted(k for k, v in item_labels.items() if v["value"] == text)
        print(f"    {text!r}   in {len(langs)}: {', '.join(langs)}")
    print(f"{len(descriptions)} descriptions:")
    for lang in sorted(descriptions):
        print(f"    {lang}: {descriptions[lang]['value']}")
    print(f"{sum(len(v) for v in aliases.values())} aliases:")
    for lang in sorted(aliases):
        for entry in aliases[lang]:
            print(f"    {lang}: {entry['value']}")
    sitelinks = entity.get("sitelinks") or {}
    print(f"{len(sitelinks)} sitelinks:")
    for site in sorted(sitelinks):
        print(f"    {site}: {sitelinks[site]['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
