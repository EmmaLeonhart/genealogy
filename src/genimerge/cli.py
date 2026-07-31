"""Command line entry points: ``python -m genimerge <command>``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import csv
import json
from datetime import date

from . import (
    coverage,
    frontier,
    gedcom,
    inventory,
    merge as merge_mod,
    model,
    names as names_mod,
    quickstatements,
    reconcile,
    wikidata,
)

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


def _read_seed_matches() -> dict[str, str]:
    """The confirmed P2600 matches written by `reconcile`."""
    path = OUT / "wikidata" / "matched_p2600.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as handle:
        return {row["geni_id"]: row["qid"] for row in csv.DictReader(handle)}


def _cmd_expand(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)
    seeds = _read_seed_matches()
    if not seeds:
        print("no P2600 matches found; run `genimerge reconcile` first", file=sys.stderr)
        return 1

    client = wikidata.WikidataClient(cache_dir=OUT / "wikidata" / "cache", delay=args.delay)
    result = reconcile.expand_from_matches(
        client,
        tree,
        seeds,
        max_rings=args.max_rings,
        progress=lambda ring, added: print(f"  ring {ring}: +{added} matched", flush=True),
    )

    out_dir = OUT / "wikidata"
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates = list(result.candidates)

    if args.search or args.api_search:
        targets = reconcile.search_targets(tree, result.confirmed)
        print(f"looking up {len(targets)} unmatched people by name")

        def note(done: int, total: int) -> None:
            print(f"  batch {done}/{total}", end="\r", flush=True)

        if args.api_search:
            # The search API is rate-limited to roughly one request every 20
            # seconds for this corpus, so it is opt-in only.
            candidates += reconcile.search_candidates(
                client, tree, targets, result.confirmed, progress=note
            )
        else:
            candidates += reconcile.label_candidates(
                client, tree, targets, result.confirmed, progress=note
            )
        print()

    with open(out_dir / "candidates.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(reconcile.CANDIDATE_COLUMNS)
        for candidate in sorted(candidates, key=lambda c: (-c.name_score, c.geni_id)):
            writer.writerow(candidate.to_row())

    with open(out_dir / "matched_all.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "source", "geni_name"])
        for geni_id, qid in sorted(result.confirmed.items()):
            person = tree.people.get(geni_id)
            writer.writerow(
                [
                    geni_id,
                    qid,
                    "P2600" if geni_id in seeds else "expansion",
                    person.display_name if person else "",
                ]
            )

    gained = len(result.confirmed) - len(seeds)
    print(f"wrote {out_dir / 'candidates.csv'} ({len(candidates)} proposals)")
    print(
        f"{len(result.confirmed)} of {len(tree.people)} people now linked "
        f"({100.0 * len(result.confirmed) / len(tree.people):.1f}%): "
        f"{len(seeds)} by P2600 + {gained} by expansion over {result.rings} rings"
    )
    print(f"{client.requests_made} requests, {client.cache_hits} cache hits")
    return 0


def _cmd_coverage(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)
    seeds = _read_seed_matches()

    all_path = OUT / "wikidata" / "matched_all.csv"
    expansion: dict[str, str] = {}
    if all_path.exists():
        with open(all_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["source"] != "P2600":
                    expansion[row["geni_id"]] = row["qid"]

    proposals: list[tuple[str, str, str, str]] = []
    candidates_path = OUT / "wikidata" / "candidates.csv"
    if candidates_path.exists():
        with open(candidates_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["used_to_expand"] == "yes":
                    continue
                proposals.append(
                    (row["geni_id"], row["qid"], row["confidence"], row["role"])
                )

    if not seeds and not expansion:
        print("no matches found; run `genimerge reconcile` first", file=sys.stderr)
        return 1

    text = coverage.render_markdown(
        coverage.CoverageInput(
            tree=tree, by_p2600=seeds, by_expansion=expansion, proposals=proposals
        ),
        top_gaps=args.top,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")
    return 0


def _cmd_quickstatements(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)

    all_path = OUT / "wikidata" / "matched_all.csv"
    if not all_path.exists():
        print("run `genimerge expand` first", file=sys.stderr)
        return 1

    # Structure-confirmed links only. Name-search proposals live in
    # candidates.csv and deliberately never reach a batch file.
    links: dict[str, str] = {}
    with open(all_path, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["source"] == "expansion":
                links[row["geni_id"]] = row["qid"]

    if not links:
        print("no expansion-confirmed links to propose", file=sys.stderr)
        return 1

    client = wikidata.WikidataClient(cache_dir=OUT / "wikidata" / "cache", delay=args.delay)
    batch = quickstatements.build_batch(client, tree, links, retrieved=args.retrieved)

    out_dir = OUT / "wikidata"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "add-p2600.qs").write_text(
        quickstatements.render_quickstatements(batch), encoding="utf-8", newline="\n"
    )
    (out_dir / "add-p2600.md").write_text(
        quickstatements.render_markdown(batch), encoding="utf-8", newline="\n"
    )

    print(f"wrote {out_dir / 'add-p2600.qs'}: {len(batch.edits)} statements")
    print(
        f"{len(batch.already_present)} already correct, "
        f"{len(batch.conflicting)} contradict an existing ID (excluded, listed in the .md)"
    )
    print("Nothing has been sent to Wikidata. Review the .md before running the batch.")
    return 0


def _cmd_names(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)
    vocabulary = names_mod.build_vocabulary(tree)
    strings = vocabulary.all_strings()
    print(f"{len(strings)} distinct name strings; checking Wikidata")

    client = wikidata.WikidataClient(cache_dir=OUT / "wikidata" / "cache", delay=args.delay)
    items = names_mod.find_name_items(
        client,
        strings,
        progress=lambda done, total: print(f"  batch {done}/{total}", end="\r", flush=True),
    )
    print()

    text = names_mod.render_markdown(vocabulary, items, top=args.top)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")

    summary = names_mod.summarise(vocabulary)
    for which in ("surnames", "given_tokens"):
        store = getattr(vocabulary, which)
        have = sum(1 for name in store if items.get(name))
        print(f"{which}: {have} of {summary[which]['distinct']} have a Wikidata name item")
    print(f"wrote {args.output}")
    return 0


def _cmd_frontier(args: argparse.Namespace) -> int:
    tree = _load_tree(args.source)
    text = frontier.render_markdown(tree, limit=args.top)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")
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

    p_exp = sub.add_parser(
        "expand",
        help="walk outward from the P2600 matches along family links",
        description=(
            "Proposes further Geni-to-Wikidata links from relationship structure. "
            "Nothing is written to Wikidata; candidates.csv is for human review."
        ),
    )
    p_exp.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_exp.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p_exp.add_argument("--max-rings", type=int, default=12, help="how far to walk (default: 12)")
    p_exp.add_argument(
        "--search",
        action="store_true",
        help="also look unmatched people up by name in Wikidata's label index",
    )
    p_exp.add_argument(
        "--api-search",
        action="store_true",
        help="use the full-text search API instead: better recall, but the "
        "endpoint throttles it to roughly one name every 20 seconds",
    )
    p_exp.set_defaults(func=_cmd_expand)

    p_front = sub.add_parser(
        "frontier",
        help="rank profiles worth exporting from next",
        description="Where the tree stops, and which Geni profiles would extend it most.",
    )
    p_front.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_front.add_argument("--top", type=int, default=40, help="how many branch points to list")
    p_front.add_argument(
        "-o", "--output", type=Path, default=REPORTS / "frontier.md", help="where to write"
    )
    p_front.set_defaults(func=_cmd_frontier)

    p_cov = sub.add_parser(
        "coverage",
        help="report how much of the tree is connected to Wikidata",
    )
    p_cov.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_cov.add_argument("--top", type=int, default=25, help="how many unlinked gaps to list")
    p_cov.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPORTS / "wikidata-coverage.md",
        help="where to write",
    )
    p_cov.set_defaults(func=_cmd_coverage)

    p_qs = sub.add_parser(
        "quickstatements",
        help="write a reviewable QuickStatements batch adding P2600 to matched items",
        description=(
            "Writes a file for you to review and run yourself. Nothing is sent to "
            "Wikidata. Structure-confirmed links only; name-search proposals are "
            "excluded."
        ),
    )
    p_qs.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_qs.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p_qs.add_argument(
        "--retrieved",
        default=date.today().isoformat(),
        help="date for the reference qualifier, YYYY-MM-DD (default: today)",
    )
    p_qs.set_defaults(func=_cmd_quickstatements)

    p_names = sub.add_parser(
        "names",
        help="measure the tree's name vocabulary against Wikidata's name items",
        description=(
            "Which surnames and given names already have a Wikidata item, and "
            "which do not. Read-only; proposes nothing."
        ),
    )
    p_names.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_names.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p_names.add_argument("--top", type=int, default=40, help="rows per table")
    p_names.add_argument(
        "-o", "--output", type=Path, default=REPORTS / "names.md", help="where to write"
    )
    p_names.set_defaults(func=_cmd_names)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
