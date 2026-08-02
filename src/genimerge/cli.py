"""Command line entry points: ``python -m genimerge <command>``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import csv
import json
from dataclasses import dataclass
from datetime import date

from . import (
    coverage,
    crosscheck,
    frontier,
    gedcom,
    inventory,
    merge as merge_mod,
    model,
    namelinks,
    names as names_mod,
    quickstatements,
    reconcile,
    seeds,
    wikidata,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_LAKE = REPO_ROOT / "data_lake"
REPORTS = REPO_ROOT / "reports"
OUT = REPO_ROOT / "out"


@dataclass(frozen=True)
class Workspace:
    """Where a run reads its inputs and writes its outputs.

    These were module constants pinned to the repo, which meant the pipeline
    could only ever be run against one dataset — a second run would overwrite
    the first, and a test could not run it at all without writing into the
    working tree. Every command now resolves them from its arguments.
    """

    data_lake: Path = DATA_LAKE
    out: Path = OUT
    reports: Path = REPORTS

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Workspace":
        return cls(
            data_lake=Path(getattr(args, "data_lake", None) or DATA_LAKE),
            out=Path(getattr(args, "out", None) or OUT),
            reports=Path(getattr(args, "reports", None) or REPORTS),
        )

    def exports(self) -> list[Path]:
        return sorted(self.data_lake.glob("*.ged"))

    @property
    def wikidata(self) -> Path:
        return self.out / "wikidata"

    @property
    def cache(self) -> Path:
        return self.wikidata / "cache"

    @property
    def merged(self) -> Path:
        return self.out / "merged.ged"


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def make_client(ws: Workspace, args: argparse.Namespace) -> wikidata.WikidataClient:
    """The Wikidata client every network command uses.

    One function rather than six identical constructions, and — more to the
    point — a seam. `WikidataClient` was given an injectable ``fetch`` so it
    could be tested offline, but the commands built their own inline, so nothing
    could reach it and every one of their bodies went untested. Substitute this
    to run them without a network.
    """
    return wikidata.WikidataClient(cache_dir=ws.cache, delay=args.delay)


def _cmd_inventory(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    paths = [Path(p) for p in args.exports] or ws.exports()
    if not paths:
        print(f"no .ged files given and none found in {ws.data_lake}", file=sys.stderr)
        return 1

    inv = inventory.build_inventory(paths)
    output = args.output or ws.reports / "inventory.md"
    _write(output, inventory.render_markdown(inv))
    print(f"wrote {output} ({len(inv.files)} exports)")
    return 0


def _cmd_merge(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    paths = [Path(p) for p in args.exports] or ws.exports()
    if not paths:
        print(f"no .ged files given and none found in {ws.data_lake}", file=sys.stderr)
        return 1

    doc, report = merge_mod.merge_files(paths)

    output = args.output or ws.merged
    output.parent.mkdir(parents=True, exist_ok=True)
    gedcom.write_file(doc, output)
    detail = _write(
        ws.out / "merge-report.md", merge_mod.render_report(report, detail=True, doc=doc)
    )
    _write(ws.reports / "merge.md", merge_mod.render_report(report, detail=False, doc=doc))

    totals = ", ".join(f"{n} {tag}" for tag, n in sorted(report.totals.items()))
    print(f"wrote {output}: {totals}")
    print(f"{len(report.conflicts)} conflicts -> {detail}")
    return 0


def _load_tree(source: Path | None, ws: Workspace) -> model.Tree:
    """The canonical tree, from a given GEDCOM or by merging the data lake."""
    if source is not None:
        return model.build_tree(gedcom.stream_file(source))
    if ws.merged.exists():
        return model.build_tree(gedcom.stream_file(ws.merged))
    doc, _ = merge_mod.merge_files(ws.exports())
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
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    out_dir = args.output or ws.out

    people_path = out_dir / "people.jsonl"
    families_path = out_dir / "families.jsonl"
    people = _write_jsonl(
        people_path, (tree.people[k].to_json() for k in sorted(tree.people, key=int))
    )
    families = _write_jsonl(
        families_path, (tree.families[k].to_json() for k in sorted(tree.families, key=int))
    )
    print(f"wrote {people_path} ({people}) and {families_path} ({families})")
    return 0


def _cmd_reconcile(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    client = make_client(ws, args)

    def progress(done: int, total: int) -> None:
        print(f"  batch {done}/{total}", end="\r", flush=True)

    matches = wikidata.match_by_geni_id(client, tree.people, progress=progress)
    print(" " * 30, end="\r")
    matches = wikidata.add_labels(client, matches)

    out_path = ws.wikidata / "matched_p2600.csv"
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


def _read_seed_matches(ws: Workspace) -> dict[str, str]:
    """The confirmed P2600 matches written by `reconcile`."""
    path = ws.wikidata / "matched_p2600.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as handle:
        return {row["geni_id"]: row["qid"] for row in csv.DictReader(handle)}


def _cmd_expand(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    seeds = _read_seed_matches(ws)
    if not seeds:
        print("no P2600 matches found; run `genimerge reconcile` first", file=sys.stderr)
        return 1

    client = make_client(ws, args)
    result = reconcile.expand_from_matches(
        client,
        tree,
        seeds,
        max_rings=args.max_rings,
        progress=lambda ring, added: print(f"  ring {ring}: +{added} matched", flush=True),
    )

    out_dir = ws.wikidata
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
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    seeds = _read_seed_matches(ws)

    all_path = ws.wikidata / "matched_all.csv"
    expansion: dict[str, str] = {}
    if all_path.exists():
        with open(all_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["source"] != "P2600":
                    expansion[row["geni_id"]] = row["qid"]

    proposals: list[tuple[str, str, str, str]] = []
    candidates_path = ws.wikidata / "candidates.csv"
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
    output = args.output or ws.reports / "wikidata-coverage.md"
    _write(output, text)
    print(f"wrote {output}")
    return 0


def _cmd_quickstatements(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)

    all_path = ws.wikidata / "matched_all.csv"
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

    client = make_client(ws, args)
    batch = quickstatements.build_batch(client, tree, links, retrieved=args.retrieved)

    out_dir = ws.wikidata
    _write(out_dir / "add-p2600.qs", quickstatements.render_quickstatements(batch))
    _write(out_dir / "add-p2600.md", quickstatements.render_markdown(batch))

    print(f"wrote {out_dir / 'add-p2600.qs'}: {len(batch.edits)} statements")
    print(
        f"{len(batch.already_present)} already correct, "
        f"{len(batch.conflicting)} contradict an existing ID (excluded, listed in the .md)"
    )
    print("Nothing has been sent to Wikidata. Review the .md before running the batch.")
    return 0


def _read_all_matches(ws: Workspace) -> dict[str, str]:
    path = ws.wikidata / "matched_all.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8", newline="") as handle:
        return {row["geni_id"]: row["qid"] for row in csv.DictReader(handle)}


def _cmd_crosscheck(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    linked = _read_all_matches(ws)
    if not linked:
        print("no linked people found; run `genimerge reconcile` and `expand` first",
              file=sys.stderr)
        return 1
    exact = set(_read_seed_matches(ws))

    client = make_client(ws, args)
    claims = crosscheck.fetch_claims(client, linked.values())
    result = crosscheck.cross_check(tree, linked, claims)

    output = args.output or ws.reports / "wikidata-crosscheck.md"
    _write(output, crosscheck.render_markdown(result))

    batch = crosscheck.build_claim_batch(result, tree, exact, retrieved=args.retrieved)
    out_dir = ws.wikidata
    _write(out_dir / "add-claims.qs", quickstatements.render_statements(batch.statements))
    _write(out_dir / "add-claims.md", crosscheck.render_claim_markdown(batch))

    counts = result.counts()
    conflicts = sum(c[crosscheck.CONFLICT] for c in counts.values())
    agrees = sum(c[crosscheck.AGREES] for c in counts.values())
    gaps = sum(c[crosscheck.GAP] for c in counts.values())
    print(f"wrote {output}")
    print(f"{result.people_checked} people: {agrees} agree, {gaps} gaps, {conflicts} conflicts")
    print(
        f"wrote {out_dir / 'add-claims.qs'}: {len(batch.statements)} statements, "
        f"{len(batch.withheld)} gaps withheld"
    )
    print("Nothing has been sent to Wikidata.")
    return 0


def _cmd_name_links(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    linked = _read_all_matches(ws)
    if not linked:
        print("no linked people found; run `genimerge reconcile` and `expand` first",
              file=sys.stderr)
        return 1

    client = make_client(ws, args)

    # Only the names of people we have actually linked need looking up.
    vocabulary = names_mod.build_vocabulary(tree, people=linked)
    items = names_mod.find_name_items(
        client,
        vocabulary.all_strings(),
        progress=lambda done, total: print(f"  names {done}/{total}", end="\r", flush=True),
    )
    print()

    batch = namelinks.build_name_links(
        client, tree, linked, items, retrieved=args.retrieved
    )

    out_dir = ws.wikidata
    _write(out_dir / "add-names.qs", namelinks.render_quickstatements(batch))
    _write(out_dir / "add-names.md", namelinks.render_markdown(batch))

    print(
        f"wrote {out_dir / 'add-names.qs'}: {len(batch.links)} statements "
        f"covering {batch.people_touched} of {batch.considered} people"
    )
    print(f"{len(batch.skipped)} names set aside; see add-names.md for why")
    print("Nothing has been sent to Wikidata. Review the .md before running the batch.")
    return 0


def _cmd_names(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    vocabulary = names_mod.build_vocabulary(tree)
    strings = vocabulary.all_strings()
    print(f"{len(strings)} distinct name strings; checking Wikidata")

    client = make_client(ws, args)
    items = names_mod.find_name_items(
        client,
        strings,
        progress=lambda done, total: print(f"  batch {done}/{total}", end="\r", flush=True),
    )
    print()

    output = args.output or ws.reports / "names.md"
    _write(output, names_mod.render_markdown(vocabulary, items, top=args.top))

    summary = names_mod.summarise(vocabulary)
    for which in ("surnames", "given_tokens"):
        store = getattr(vocabulary, which)
        have = sum(1 for name in store if items.get(name))
        print(f"{which}: {have} of {summary[which]['distinct']} have a Wikidata name item")
    print(f"wrote {output}")
    return 0


def _cmd_frontier(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    output = args.output or ws.reports / "frontier.md"
    _write(output, frontier.render_markdown(tree, limit=args.top))
    print(f"wrote {output}")
    return 0


def _cmd_seeds(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    output = args.output or ws.reports / "seeds.md"
    _write(
        output,
        seeds.render_markdown(
            tree, style=args.style, radius=args.radius, exports=args.exports, top=args.top
        ),
    )

    kept, rejected = seeds.rank_seeds(tree, style=args.style, radius=args.radius)
    picks = seeds.choose_export_set(kept, args.exports)
    csv_path = ws.out / "seeds.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order", "geni_id", "name", "url", "ball", "doorways", "openness", "adds"])
        for order, pick in enumerate(picks, 1):
            person = tree.people[pick.profile.seed]
            writer.writerow(
                [
                    order,
                    pick.profile.seed,
                    person.display_name,
                    person.url,
                    pick.profile.size,
                    pick.profile.open_count,
                    f"{pick.profile.openness:.4f}",
                    pick.fresh_count,
                ]
            )

    print(f"{len(kept)} candidates kept, {len(rejected)} rejected as saturated")
    print(f"{len(picks)} exports planned, reaching {sum(p.fresh_count for p in picks)} doorways")
    print(f"wrote {output}")
    print(f"wrote {csv_path}")
    return 0


def _add_workspace_options(sub: argparse._SubParsersAction) -> None:
    """Give every subcommand the workspace options.

    Added in a loop rather than threaded through each ``add_parser`` call, so a
    new command cannot be added without them by forgetting a ``parents=``.
    """
    for parser in sub.choices.values():
        group = parser.add_argument_group("workspace")
        group.add_argument(
            "--data-lake", type=Path, default=None, help=f"inputs (default: {DATA_LAKE})"
        )
        group.add_argument(
            "--out", type=Path, default=None, help=f"generated data (default: {OUT})"
        )
        group.add_argument(
            "--reports", type=Path, default=None, help=f"generated reports (default: {REPORTS})"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genimerge", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("inventory", help="measure the exports and write a report")
    p_inv.add_argument("exports", nargs="*", help="GEDCOM files (default: data_lake/*.ged)")
    p_inv.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="where to write the report (default: <reports>/inventory.md)",
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
        default=None,
        help="where to write the merged GEDCOM (default: <out>/merged.ged)",
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
    p_export.add_argument(
        "-o", "--output", type=Path, default=None,
        help="directory for the JSONL files (default: <out>)"
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
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/frontier.md)"
    )
    p_front.set_defaults(func=_cmd_frontier)

    p_seeds = sub.add_parser(
        "seeds",
        help="plan the next exports: seeds whose breadth-first ball reaches the most new material",
        description=(
            "A Geni export is a breadth-first ball from one profile, modelled as "
            f"holding {seeds.GENI_EXPORT_CAP} people — the largest seen, not a known "
            "cap. This ranks candidate seeds by the people in "
            "their ball with no parents recorded, and picks a sequence whose balls "
            "overlap as little as possible."
        ),
    )
    p_seeds.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_seeds.add_argument(
        "--style", choices=seeds.STYLES, default="blood",
        help="which links the export walks (default: blood)",
    )
    p_seeds.add_argument(
        "--radius", type=int, default=seeds.SCREEN_RADIUS,
        help=f"hops in the screening ball (default: {seeds.SCREEN_RADIUS})",
    )
    p_seeds.add_argument("--exports", type=int, default=10, help="how many exports to plan")
    p_seeds.add_argument("--top", type=int, default=40, help="how many ranked candidates to list")
    p_seeds.add_argument(
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/seeds.md)"
    )
    p_seeds.set_defaults(func=_cmd_seeds)

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
        default=None,
        help="where to write (default: <reports>/wikidata-coverage.md)",
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
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/names.md)"
    )
    p_names.set_defaults(func=_cmd_names)

    p_links = sub.add_parser(
        "name-links",
        help="propose P735/P734 links to name items that already exist",
        description=(
            "Writes a reviewable batch. Creates no name items, resolves no "
            "ambiguous name, and touches no item that already states a name."
        ),
    )
    p_links.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_links.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p_links.add_argument(
        "--retrieved",
        default=date.today().isoformat(),
        help="date for the reference qualifier, YYYY-MM-DD (default: today)",
    )
    p_links.set_defaults(func=_cmd_name_links)

    p_cross = sub.add_parser(
        "crosscheck",
        help="compare our parents, spouses and dates against Wikidata's",
        description=(
            "Reports agreements, gaps and conflicts, and writes a reviewable "
            "batch for the eligible gaps only. Nothing is sent to Wikidata."
        ),
    )
    p_cross.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_cross.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p_cross.add_argument(
        "--retrieved",
        default=date.today().isoformat(),
        help="date for the reference qualifier, YYYY-MM-DD (default: today)",
    )
    p_cross.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="where to write the report (default: <reports>/wikidata-crosscheck.md)",
    )
    p_cross.set_defaults(func=_cmd_crosscheck)

    _add_workspace_options(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
