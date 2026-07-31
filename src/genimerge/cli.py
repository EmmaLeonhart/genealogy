"""Command line entry points: ``python -m genimerge <command>``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import csv
import json

from . import gedcom, inventory, merge as merge_mod, model, wikidata

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_LAKE = REPO_ROOT / "data_lake"
REPORTS = REPO_ROOT / "reports"
OUT = REPO_ROOT / "out"


def _default_exports() -> list[Path]:
    return sorted(DATA_LAKE.glob("*.ged"))


def _cmd_inventory(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in args.exports] or _default_exports()
    if not paths:
        print(f"no .ged files given and none found in {DATA_LAKE}", file=sys.stderr)
        return 1

    inv = inventory.build_inventory(paths)
    text = inventory.render_markdown(inv)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {args.output} ({len(inv.files)} exports)")
    return 0


def _cmd_merge(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in args.exports] or _default_exports()
    if not paths:
        print(f"no .ged files given and none found in {DATA_LAKE}", file=sys.stderr)
        return 1

    doc, report = merge_mod.merge_files(paths)

    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    gedcom.write_file(doc, args.output)
    (OUT / "merge-report.md").write_text(
        merge_mod.render_report(report, detail=True, doc=doc), encoding="utf-8", newline="\n"
    )
    (REPORTS / "merge.md").write_text(
        merge_mod.render_report(report, detail=False, doc=doc), encoding="utf-8", newline="\n"
    )

    totals = ", ".join(f"{n} {tag}" for tag, n in sorted(report.totals.items()))
    print(f"wrote {args.output}: {totals}")
    print(f"{len(report.conflicts)} conflicts -> out/merge-report.md")
    return 0


def _load_tree(source: Path | None) -> model.Tree:
    """The canonical tree, from a given GEDCOM or by merging the data lake."""
    if source is not None:
        return model.build_tree(gedcom.stream_file(source))
    merged = OUT / "merged.ged"
    if merged.exists():
        return model.build_tree(gedcom.stream_file(merged))
    doc, _ = merge_mod.merge_files(_default_exports())
    return model.build_tree(doc.records)


def _write_jsonl(path: Path, rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def _cmd_export(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)

    people = _write_jsonl(
        OUT / "people.jsonl",
        (tree.people[k].to_json() for k in sorted(tree.people, key=int)),
    )
    families = _write_jsonl(
        OUT / "families.jsonl",
        (tree.families[k].to_json() for k in sorted(tree.families, key=int)),
    )
    print(f"wrote out/people.jsonl ({people}) and out/families.jsonl ({families})")
    return 0


def _cmd_reconcile(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)
    client = wikidata.WikidataClient(cache_dir=OUT / "wikidata" / "cache", delay=args.delay)

    def progress(done: int, total: int) -> None:
        print(f"  batch {done}/{total}", end="\r", flush=True)

    matches = wikidata.match_by_geni_id(client, tree.people, progress=progress)
    print(" " * 30, end="\r")
    matches = wikidata.add_labels(client, matches)

    out_path = OUT / "wikidata" / "matched_p2600.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "wikidata_label", "wikidata_description",
                         "geni_name", "birth_year", "death_year"])
        for match in sorted(matches, key=lambda m: (m.geni_id, m.qid)):
            person = tree.people.get(match.geni_id)
            writer.writerow(
                [
                    match.geni_id,
                    match.qid,
                    match.label,
                    match.description,
                    person.display_name if person else "",
                    person.birth_year if person else "",
                    person.death_year if person else "",
                ]
            )

    people_matched = len({m.geni_id for m in matches})
    print(f"wrote {out_path}")
    print(
        f"{people_matched} of {len(tree.people)} people matched by P2600 "
        f"({100.0 * people_matched / len(tree.people):.1f}%); "
        f"{len(matches)} item links; "
        f"{client.requests_made} requests, {client.cache_hits} cache hits"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genimerge", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("inventory", help="measure the exports and write a report")
    p_inv.add_argument("exports", nargs="*", help="GEDCOM files (default: data_lake/*.ged)")
    p_inv.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPORTS / "inventory.md",
        help="where to write the report (default: reports/inventory.md)",
    )
    p_inv.set_defaults(func=_cmd_inventory)

    p_merge = sub.add_parser(
        "merge",
        help="merge exports into one GEDCOM keyed on the Geni profile ID",
        description="Earlier files win value conflicts on single-valued paths.",
    )
    p_merge.add_argument("exports", nargs="*", help="GEDCOM files (default: data_lake/*.ged)")
    p_merge.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUT / "merged.ged",
        help="where to write the merged GEDCOM (default: out/merged.ged)",
    )
    p_merge.set_defaults(func=_cmd_merge)

    p_export = sub.add_parser(
        "export",
        help="write the canonical people/families JSONL dataset",
        description="Reads out/merged.ged if it exists, otherwise merges the data lake.",
    )
    p_export.add_argument(
        "--source", type=Path, default=None, help="a GEDCOM to read instead of merging"
    )
    p_export.set_defaults(func=_cmd_export)

    p_rec = sub.add_parser(
        "reconcile",
        help="match people to Wikidata items by P2600 (Geni.com profile ID)",
        description="Responses are cached under out/wikidata/cache; delete it to refresh.",
    )
    p_rec.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_rec.add_argument(
        "--delay", type=float, default=1.0, help="seconds between requests (default: 1.0)"
    )
    p_rec.set_defaults(func=_cmd_reconcile)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
