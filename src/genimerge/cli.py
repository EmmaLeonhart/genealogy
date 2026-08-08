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
    connectors,
    consistency,
    doubles as doubles_mod,
    coverage,
    crosscheck,
    density,
    descendants as descendants_mod,
    distant,
    entities,
    frontier,
    gedcom,
    genipage,
    inventory,
    merge as merge_mod,
    model,
    namelinks,
    names as names_mod,
    profilenames,
    overlap as overlap_mod,
    paths as paths_mod,
    quickstatements,
    reconcile,
    remote,
    seeds,
    sources,
    wikidata,
    wikidownload,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPORTS_DIR = sources.EXPORTS_DIR
REPORTS = REPO_ROOT / "reports"
OUT = REPO_ROOT / "out"

#: Where downloaded Wikidata items live. Not under `out/` on purpose — `out/` is
#: gitignored generated data, and these are collected source material, kept the
#: way `exports/` keeps the GEDCOMs.
WIKIDATA_STORE = REPO_ROOT / "wikidata" / "items"

#: Values of the ``source`` column in ``out/wikidata/matched_all.csv``, which
#: `expand` writes and `coverage`, `crosscheck`, `name-links` and
#: `quickstatements` all read back. Named because a writer and a reader in
#: different functions should not agree by coincidence of spelling.
#:
#: ``SOURCE_EXACT`` is spelled like the property it refers to, but it is a token
#: in a CSV rather than a property ID and never reaches a Wikidata edit.
SOURCE_EXACT = "P2600"
SOURCE_EXPANSION = "expansion"


@dataclass(frozen=True)
class Workspace:
    """Where a run reads its inputs and writes its outputs.

    These were module constants pinned to the repo, which meant the pipeline
    could only ever be run against one dataset — a second run would overwrite
    the first, and a test could not run it at all without writing into the
    working tree. Every command now resolves them from its arguments.
    """

    exports_dir: Path = EXPORTS_DIR
    out: Path = OUT
    reports: Path = REPORTS

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Workspace":
        return cls(
            exports_dir=Path(getattr(args, "exports_dir", None) or EXPORTS_DIR),
            out=Path(getattr(args, "out", None) or OUT),
            reports=Path(getattr(args, "reports", None) or REPORTS),
        )

    def exports(self) -> list[Path]:
        """Every distinct export under `exports_dir`, recursively.

        Recursive and content-deduped because the exports live in per-batch
        subdirectories and the same file can arrive twice — see
        :mod:`genimerge.sources`.
        """
        return sources.find_exports(self.exports_dir)

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
        print(f"no .ged files given and none found under {ws.exports_dir}", file=sys.stderr)
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
        print(f"no .ged files given and none found under {ws.exports_dir}", file=sys.stderr)
        return 1

    doc, report = merge_mod.merge_files(paths)

    output = args.output or ws.merged
    output.parent.mkdir(parents=True, exist_ok=True)
    gedcom.write_file(doc, output)

    # The reports describe *this* merge, so they follow the file they describe.
    # Sending the GEDCOM elsewhere and leaving the reports in the workspace
    # overwrites the workspace's description of a different merge, which is
    # tracked in git — that is how `reports/merge.md` spent twelve commits
    # claiming 8766 people while `out/merged.ged` held 12422.
    detail_dir, summary_dir = (
        (output.parent, output.parent) if args.output else (ws.out, ws.reports)
    )
    detail = _write(
        detail_dir / "merge-report.md", merge_mod.render_report(report, detail=True, doc=doc)
    )
    _write(summary_dir / "merge.md", merge_mod.render_report(report, detail=False, doc=doc))

    totals = ", ".join(f"{n} {tag}" for tag, n in sorted(report.totals.items()))
    print(f"wrote {output}: {totals}")
    print(f"{len(report.conflicts)} conflicts -> {detail}")
    # Conflicts say whether the exports disagree; this says whether they joined
    # up. An export seeded outside everything we hold merges without a single
    # conflict and still leaves two trees.
    print(frontier.describe_connectivity(frontier.components(model.build_tree(doc.records))))
    return 0


def _load_tree(source: Path | None, ws: Workspace) -> model.Tree:
    """The canonical tree, from a given GEDCOM or by merging the exports."""
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


def _cmd_overlap(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    cached = ws.wikidata / "p2600-all.tsv"

    if args.offline:
        # The expensive half of this command is sixteen partitions over a live
        # endpoint, and it answers "what does Wikidata hold?" — which barely
        # moves between our merges. Our own side moves every time an export
        # lands, so re-asking Wikidata to watch our coverage climb is wasted
        # traffic. This reuses the map the last online run wrote.
        if not cached.exists():
            print(
                f"{cached} not found. Run `python -m genimerge overlap` once "
                "without --offline to fetch it.",
                file=sys.stderr,
            )
            return 1
        tree = _load_tree(args.source, ws)
        pairs = doubles_mod.load_pairs(cached)
        stamp = date.fromtimestamp(cached.stat().st_mtime).isoformat()
        print(f"offline: {len(pairs):,} P2600 statements cached {stamp}")
        # No `reported`: those counts come from the endpoint. Passing the
        # fetched totals instead would print a number that looks like Wikidata
        # answering and is really our own file counting itself.
        result = overlap_mod.measure(pairs, tree.people)
        report = _write(
            args.output or ws.reports / "wikidata-overlap.md",
            overlap_mod.render_markdown(
                result,
                people=len(tree.people),
                exports=len(ws.exports()),
                names={gid: p.display_name for gid, p in tree.people.items()},
                fetched=stamp,
            ),
        )
        print(f"wrote {report}")
        print(
            f"{len(result.both):,} of {len(result.theirs):,} Geni IDs on Wikidata "
            f"are in our tree ({100 * len(result.both) / len(result.theirs):.2f}%); "
            f"{len(result.both) / len(result.ours):.2%} of our tree is on Wikidata"
        )
        return 0

    tree = _load_tree(args.source, ws)
    client = make_client(ws, args)

    reported = {}
    for name, query in overlap_mod.COUNT_QUERIES.items():
        reported[name] = int(client.sparql(query)[0]["n"])
        print(f"  wikidata {name}: {reported[name]:,}")

    def progress(done: int, total: int) -> None:
        print(f"  partition {done}/{total}", end="\r", flush=True)

    pairs = overlap_mod.fetch_all_p2600(client, progress=progress)
    print(" " * 30, end="\r")

    # Fetched rows against what the endpoint says it holds. A partition that
    # came back short would otherwise read as a smaller Wikidata.
    if len(pairs) != reported["statements"]:
        print(
            f"warning: fetched {len(pairs):,} statements but the endpoint reports "
            f"{reported['statements']:,}. Wikidata is live, so a small drift is "
            "ordinary; a large one means a partition failed.",
            file=sys.stderr,
        )

    result = overlap_mod.measure(pairs, tree.people, reported=reported)

    pairs_path = _write(
        ws.wikidata / "p2600-all.tsv",
        "\n".join(f"{qid}\t{gid}" for qid, gid in sorted(pairs)) + "\n",
    )
    report = _write(
        args.output or ws.reports / "wikidata-overlap.md",
        overlap_mod.render_markdown(
            result,
            people=len(tree.people),
            exports=len(ws.exports()),
            names={gid: p.display_name for gid, p in tree.people.items()},
        ),
    )
    print(f"wrote {pairs_path} and {report}")
    print(
        f"{len(result.both):,} in both; {len(result.ours_only):,} ours only; "
        f"{len(result.theirs_only):,} Wikidata only"
    )
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
                    SOURCE_EXACT if geni_id in seeds else SOURCE_EXPANSION,
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
                if row["source"] != SOURCE_EXACT:
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
            if row["source"] == SOURCE_EXPANSION:
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


def _cmd_distant(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    pairs = distant.far_pairs(tree, count=args.count)

    output = args.output or (ws.reports / "distant-pairs.md")
    _write(output, distant.render_markdown(pairs, len(tree.people)))
    page = ws.out / "distant-pairs.html"
    _write(page, distant.render_html(pairs, len(tree.people)))

    print(f"wrote {output}")
    print(f"wrote {page}")
    if pairs:
        widest = pairs[0]
        print(
            f"{len(pairs)} pairs; the widest is {widest.distance} hops: "
            f"{widest.a_name} to {widest.b_name}"
        )
    else:
        print("no usable pairs found")
    return 0


#: Where the generated relationship paths live. A sibling of `reports/` rather
#: than inside it, because a path file is an *input* — it comes out of a saved
#: Geni page and is the only evidence here originating outside our own exports.
PATHS_DIR = REPO_ROOT / "paths"


def _cmd_connectors(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    directory = args.paths_dir or PATHS_DIR
    files = [Path(p) for p in args.paths] or sorted(Path(directory).glob("*.tsv"))
    if not files:
        print(f"no path files given and none found under {directory}", file=sys.stderr)
        return 1

    tree = _load_tree(args.source, ws)
    clusters, reports = connectors.collect(tree, files)

    output = args.output or (ws.reports / "connectors.md")
    _write(output, connectors.render_markdown(clusters, reports, len(tree.people)))
    page = ws.out / "connectors.html"
    _write(page, connectors.render_html(clusters, reports, len(tree.people)))
    print(f"wrote {output}")
    print(f"wrote {page}")

    # The per-path reports come free: `collect` has already checked every path
    # against this tree, and a second `genimerge path` run would pay the whole
    # cost of loading the merge again for each one.
    if args.write_paths:
        for name, report in reports.items():
            md = _write(
                ws.reports / f"path-{name}.md",
                paths_mod.render_markdown(report, f"Relationship path: {name}"),
            )
            _write(
                ws.reports / f"path-{name}.json",
                json.dumps(paths_mod.to_json(report), ensure_ascii=False, indent=2) + "\n",
            )
            print(f"wrote {md} and its .json")

    steps = sum(len(r.results) for r in reports.values())
    held = sum(len(r.held) for r in reports.values())
    complete = sum(1 for r in reports.values() if not r.absent)
    print(
        f"{len(reports)} paths, {held} of {steps} steps held "
        f"({held / steps:.1%}); {complete} complete end to end"
        if steps
        else f"{len(reports)} paths, no steps"
    )
    print(
        f"{sum(len(c.bridges) for c in clusters)} bridges in {len(clusters)} clusters"
    )
    for i, c in enumerate(clusters[:5], 1):
        door = c.doorways[0] if c.doorways else None
        where = f"{door.step.name} {door.step.geni_id}" if door else "(path starts absent)"
        print(
            f"  {i}. {c.slots} slots, {len(c.people)} people, "
            f"{len(c.path_names)} path(s) — seed on {where} [{c.style}]"
        )
    return 0


def _cmd_doubles(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    pairs_file = args.pairs or (ws.wikidata / "p2600-all.tsv")
    if not Path(pairs_file).exists():
        print(
            f"{pairs_file} not found. Run `python -m genimerge overlap` first — "
            "that is the command that fetches P2600 from Wikidata. This one is "
            "offline and reads what it wrote.",
            file=sys.stderr,
        )
        return 1

    tree = _load_tree(args.source, ws)
    found = doubles_mod.find_doubles(doubles_mod.load_pairs(Path(pairs_file)), tree)

    output = args.output or (ws.reports / "wikidata-doubles.md")
    _write(output, doubles_mod.render_markdown(found, tree, len(tree.people)))
    page = ws.out / "wikidata-doubles.html"
    _write(page, doubles_mod.render_html(found, tree, len(tree.people)))

    print(f"wrote {output}")
    print(f"wrote {page}")
    kin = sum(1 for d in found if d.shares_a_relative)
    named = sum(1 for d in found if d.same_name)
    clash = sum(1 for d in found if d.years_conflict)
    print(
        f"{len(found)} items claim two or more people we hold; "
        f"{kin} share a relative, {named} share a name, "
        f"{clash} have births over 120 years apart"
    )
    print("Nothing was decided and nothing was edited. This is a page to read.")
    return 0


def _cmd_remote(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    people = remote.most_remote(tree, count=args.count, landmark_count=args.landmarks)

    output = args.output or (ws.reports / "remote-people.md")
    _write(output, remote.render_markdown(people, len(tree.people)))
    page = ws.out / "remote-people.html"
    _write(page, remote.render_html(people, len(tree.people)))

    print(f"wrote {output}")
    print(f"wrote {page}")
    if people:
        first = people[0]
        print(
            f"{len(people)} people, separated by at least "
            f"{getattr(remote.most_remote, 'separation', '?')} hops; the most "
            f"remote is {first.name} at {first.remoteness} hops from "
            f"{first.partner_name}"
        )
    else:
        print("no one to report")
    return 0


def _cmd_density(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    exports = [Path(p) for p in args.exports] or ws.exports()
    if not exports:
        print("no exports found", file=sys.stderr)
        return 1

    tree = _load_tree(args.source, ws)
    counts = density.presence_counts(exports)
    regions = density.sparse_regions(
        tree, counts, threshold=args.threshold, min_size=args.min_size
    )

    output = args.output or (ws.reports / "density.md")
    _write(
        output,
        density.render_markdown(
            tree, counts, regions, export_count=len(exports), threshold=args.threshold
        ),
    )
    listed = [r for r in regions if r.size >= args.seed_list_min]
    seed_list = ws.out / "sparse-cluster-seeds.txt"
    _write(seed_list, density.render_seed_list(listed))

    thin = sum(1 for g in tree.people if counts.get(g, 0) <= args.threshold)
    print(f"wrote {output}")
    # Seeds, not regions: a region larger than one export ball gets one seed per
    # export it needs, so the two counts stopped being the same number.
    seed_total = sum(len(r.seeds) for r in listed)
    multi = sum(1 for r in listed if r.exports_needed > 1)
    print(
        f"wrote {seed_list}: {seed_total} seeds across {len(listed)} regions of "
        f"{args.seed_list_min}+, {multi} of which need more than one export"
    )
    print(
        f"{thin} of {len(tree.people)} people are in <= {args.threshold} export(s), "
        f"forming {len(regions)} regions of {args.min_size}+"
    )
    if regions:
        biggest = regions[0]
        print(
            f"largest thin region: {biggest.size} people, {biggest.parentless} doorways"
            + (f" — {biggest.sample[0]}" if biggest.sample else "")
        )
    return 0


def _cmd_descendants(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    present = args.present or descendants_mod.present_year()

    lines = descendants_mod.build_lines(tree)
    parents = descendants_mod.parent_map(tree)
    by_birth, by_generation = descendants_mod.bands(
        lines,
        present=present,
        small=args.small,
        width=args.band,
        per_band=args.per_band,
        min_stall=args.min_stall,
        parents=parents,
    )

    output = args.output or (ws.reports / "descendants.md")
    _write(
        output,
        descendants_mod.render_markdown(
            tree, lines, by_birth, by_generation,
            present=present, small=args.small, width=args.band,
            min_stall=args.min_stall, per_band=args.per_band,
            target=args.target_year, parents=parents,
        ),
    )
    seed_list = ws.out / "stalled-line-seeds.txt"
    _write(seed_list, descendants_mod.render_seed_list(by_birth))

    # The campaign list is the one to paste from, so it gets its own file rather
    # than being mixed into the survey. **Same order as the report's § Seeds
    # that can reach section** — they disagreed once, the file leading with a
    # 1973 profile holding three open ends while the report led with an 1858 one
    # holding twenty, and the file is the one that actually gets used.
    reachable = sorted(
        (
            line for line in descendants_mod.candidates(
                lines, present=present, small=args.small,
                min_stall=args.min_stall, parents=parents,
            )
            if line.birth is not None and line.can_reach(args.target_year)
        ),
        key=lambda line: (-line.open_paths, -(line.birth or 0), int(line.geni_id)),
    )
    # One seed per couple: both parents of the same children give the identical
    # ball, and the ranking rewards a large family so both score alike.
    reachable = descendants_mod.drop_duplicate_balls(reachable)
    reach_list = ws.out / f"reach-{args.target_year}-seeds.txt"
    _write(
        reach_list,
        "".join(
            f"{descendants_mod.profile_url(line.geni_id)} | Geni - "
            f"{line.name or 'NN'} (b. {line.birth}, {line.open_paths} open)\n"
            for line in reachable[:200]
        ),
    )

    total = sum(band.total_candidates for band in by_birth)
    print(f"wrote {output}")
    print(
        f"{len(reachable)} candidates are born late enough for a ball to reach "
        f"{args.target_year}; everything else cannot arrive whatever else is "
        f"true of it"
    )
    page = ws.out / f"reach-{args.target_year}-seeds.html"
    _write(page, descendants_mod.render_html(reachable, args.target_year, len(tree.people)))
    print(f"wrote {reach_list}: the best {min(200, len(reachable))} of them")
    print(f"wrote {page}: sortable and filterable, to look over and pick by eye")
    # Which century the campaign seeds actually live in, rather than an argument
    # about which one they ought to.
    from collections import Counter as _Counter
    by_century = _Counter((line.birth // 100) * 100 for line in reachable)
    for century in sorted(by_century):
        share = by_century[century] / len(reachable)
        print(f"  born {century}s: {by_century[century]:>5} ({share:.0%})")
    print(
        f"wrote {seed_list}: "
        f"{sum(len(band.picks) for band in by_birth)} picks across "
        f"{sum(1 for band in by_birth if band.picks)} periods"
    )
    print(
        f"{total} of {len(tree.people)} people have 1-{args.small} recorded "
        f"descent paths and nobody above them in the same period who does"
    )
    # The most recent band with a pick, because that is what the campaign is
    # aiming at — not the worst-ranked line anywhere, which is always ancient.
    newest = max(
        (b for b in by_birth if b.picks and not b.is_undated),
        key=lambda b: b.order,
        default=None,
    )
    if newest is not None:
        pick = newest.picks[0]
        print(
            f"nearest the present: {pick.name or pick.geni_id} ({newest.label}), "
            f"{pick.paths} descent path(s) over {pick.depth} generation(s), "
            f"{pick.open_paths} open"
        )
    return 0


def _cmd_entity_resolution(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    source = args.file or (REPO_ROOT / "entity_resolution.md")
    if not source.exists():
        print(f"no such file: {source}", file=sys.stderr)
        return 1

    parsed = entities.read_file(source)

    # Corroboration only: a resolution for a profile we do not hold is still
    # emitted, because the assertion is Emma's and does not depend on our
    # coverage. Reading the tree is skipped when nothing would use it.
    known: set[str] = set()
    if parsed.resolutions:
        try:
            known = set(_load_tree(args.source, ws).people)
        except Exception as exc:  # pragma: no cover - depends on the exports
            print(f"could not load the tree to corroborate ({exc}); continuing", file=sys.stderr)

    out_dir = ws.wikidata
    _write(
        out_dir / "entity-resolution.qs",
        entities.render_quickstatements(parsed, retrieved=args.retrieved, known=known),
    )
    report = args.output or (ws.reports / "entity-resolution.md")
    _write(
        report,
        entities.render_markdown(
            parsed, source=source.name, retrieved=args.retrieved, known=known
        ),
    )

    missing = [r for r in parsed.resolutions if r.geni_id not in known]
    print(
        f"wrote {out_dir / 'entity-resolution.qs'}: "
        f"{len(parsed.resolutions)} P2600 statements, {len(parsed.labels)} label edits"
    )
    if missing:
        print(f"{len(missing)} name a Geni profile the merged tree does not hold")
    if parsed.unparsed:
        print(
            f"{len(parsed.unparsed)} entries were NOT understood and are in no batch "
            f"— see {report}",
            file=sys.stderr,
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
    _write(output, crosscheck.render_markdown(result, exact_links=exact))

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


def _cmd_wikidata_download(args: argparse.Namespace) -> int:
    """Download whole Wikidata items into the shard store.

    Prints the four numbers `queue.md` item 4 exists to get — rate, batch
    behaviour, bytes per item, and what those project to over the whole seed
    set — because a pilot that stores items and reports nothing has measured
    nothing.
    """
    ws = Workspace.from_args(args)
    seed_file = args.seeds or (ws.wikidata / "p2600-all.tsv")
    if not seed_file.exists():
        print(
            f"{seed_file} not found. Run `python -m genimerge overlap` once to fetch "
            "the P2600 map, or pass --seeds.",
            file=sys.stderr,
        )
        return 1

    # The shards go to a *tracked* directory and the index to `out/`, which is
    # gitignored. That is the § 8a-revised split made concrete: the items are
    # the thing being collected and are committed; the index is derived from
    # them and is rebuilt rather than stored. Defaulting the shards under `out/`
    # would have quietly produced a download nobody kept.
    store = wikidownload.ItemStore(args.store or WIKIDATA_STORE)
    index = wikidownload.StateIndex(args.index or (ws.wikidata / "download-state.sqlite3"))

    if args.rebuild_index:
        found = index.rebuild(store)
        print(f"index rebuilt from {len(store.shards())} shards: {found:,} items")

    # Single run at a time. The whole point of the supervisor is that this
    # command gets started again automatically, and two copies appending to the
    # same shard corrupts the store rather than merely wasting requests.
    if not args.dry_run and not index.claim():
        print("another wikidata-download holds the lock (its heartbeat is fresh) — nothing to do")
        index.close()
        return 0

    # Seeding is idempotent: a QID already known keeps its status, so re-running
    # after the map is refreshed adds only what is genuinely new.
    seeded = index.enqueue(wikidownload.seed_qids(seed_file))
    index.commit()
    # Anything a previous run's outage marked failed goes back on the queue.
    # Without this a dropped connection leaves QIDs neither held nor queued and
    # the next run reports "complete" with holes in it.
    retried = index.requeue_errors()
    if retried:
        print(f"re-queued {retried:,} QIDs that failed on an earlier run")
    counts = index.counts()
    print(
        f"seed file {seed_file.name}: {seeded:,} QIDs added to the fetch queue; "
        f"queue now {counts.get('queued', 0):,}, held {counts.get('done', 0):,}, "
        f"missing {counts.get('missing', 0):,}, errored {counts.get('error', 0):,}"
    )

    if args.dry_run:
        queued = counts.get("queued", 0)
        print(
            f"dry run: would request {queued:,} items in "
            f"{-(-queued // wikidownload.FETCH_BATCH):,} batches of "
            f"{wikidownload.FETCH_BATCH}, and would grow the queue as it scans"
        )
        index.close()
        return 0

    client = make_client(ws, args)

    def progress(stats: wikidownload.WalkStats) -> None:
        if stats.batches % args.report_every == 0:
            print(
                f"  {stats.stored:,} stored, {stats.scanned:,} scanned, "
                f"{stats.discovered:,} discovered, queue {index.queue_length():,}, "
                f"{stats.items_per_second:.1f}/s",
                flush=True,
            )

    try:
        stats = wikidownload.walk(
            client,
            store,
            index,
            limit=args.limit,
            scan_per_round=args.scan_per_round,
            progress=progress,
        )
    finally:
        # A clean exit — including Ctrl-C — drops the lock so the supervisor's
        # next tick starts at once instead of waiting for the heartbeat to go
        # stale. A kill -9 skips this, which is what the staleness is for.
        index.release()
    total_known = len(index.known())
    remaining = index.queue_length()
    index.close()

    if stats.stopped_early:
        print(f"\nSTOPPED: {stats.stopped_early}", file=sys.stderr)
    print(
        f"\n{stats.stored:,} stored, {stats.missing:,} missing, {stats.errors:,} errored "
        f"in {stats.batches:,} requests over {stats.seconds:,.0f}s"
    )
    print(
        f"scanned {stats.scanned:,} stored items for relatives and discovered "
        f"{stats.discovered:,} QIDs not already known"
    )
    print(f"throttled {client.throttled} times; {stats.items_per_second:.1f} items/s")
    if stats.stored:
        print(f"{stats.bytes_per_item:,.0f} bytes of JSON per item (uncompressed)")
        shards = store.shards()
        on_disk = sum(p.stat().st_size for p in shards)
        print(f"{len(shards)} shard(s), {on_disk / 1e6:,.1f} MB gzipped on disk")
        full = stats.projection(total_known)
        print(
            f"projected over {full['items']:,.0f} known QIDs: "
            f"{full['requests']:,.0f} requests, {full['hours']:,.1f} hours, "
            f"{full['gigabytes_json']:,.1f} GB of JSON"
        )
        print("  — a floor, not an estimate: a short run has not met a long run's throttling.")
    print(f"{remaining:,} QIDs still queued — re-run the same command to continue")
    return 1 if stats.stopped_early else 0


def _cmd_profile_names(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    cov = profilenames.measure(tree)
    output = args.output or ws.reports / "profile-names.md"
    _write(output, profilenames.render_markdown(cov))
    cjk = cov.cjk_only + cov.cjk_and_latin
    print(f"{cov.people:,} people; {cjk:,} carry a CJK name ({cov.cjk_only:,} native-only)")
    print(f"wrote {output}")
    return 0


def _cmd_frontier(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    output = args.output or ws.reports / "frontier.md"
    _write(output, frontier.render_markdown(tree, limit=args.top))
    print(f"wrote {output}")
    return 0


def _cmd_path(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    steps = paths_mod.load_path(args.path)
    report = paths_mod.check(tree, steps)

    name = Path(args.path).stem
    output = args.output or ws.reports / f"path-{name}.md"
    title = args.title or f"Relationship path: {name}"
    _write(output, paths_mod.render_markdown(report, title))

    as_json = args.json or ws.reports / f"path-{name}.json"
    _write(as_json, json.dumps(paths_mod.to_json(report), ensure_ascii=False, indent=2) + "\n")

    held = len(report.held)
    print(f"wrote {output}")
    print(f"wrote {as_json}")
    print(f"{held} of {len(steps)} steps held")
    end = report.run_ends_at
    if end is not None and held < len(steps):
        print(f"unbroken run stops at step {end.step.step}, {end.step.name}")
    beyond = report.held_beyond_the_gap
    if beyond:
        print(f"{len(beyond)} further steps held past the gap")
    if any(not r.step.geni_id for r in report.results):
        print(paths_mod.NAME_MATCHING_IS_ADVISORY)
    return 0


PATH_FILE_HEADER = """\
# Geni relationship path: {title}
#
# GENERATED by `python -m genimerge path-from-html` out of a Geni profile page
# saved from the browser. Do not hand-edit: re-run the command instead.
#
# Source: {source}
#
# Every row carries its Geni profile ID, taken from the `href` on the page's
# relationship panel. That is what makes checking this path an exact join on
# this repo's primary key rather than a name match --- see `genimerge.paths`,
# which falls back to matching names only for rows with no ID.
#
# The relation column is Geni's own wording and describes how THIS person
# relates to the PREVIOUS row.
#
# Columns: step, name, relation_to_previous, note\
"""


def _cmd_path_from_html(args: argparse.Namespace) -> int:
    links = genipage.read_relationship_path(args.html)
    if not links:
        print(f"no relationship path found in {args.html}", file=sys.stderr)
        print(
            "The panel is only on a profile page saved while signed in, and only "
            "when Geni could connect the two people.",
            file=sys.stderr,
        )
        return 1

    header = PATH_FILE_HEADER.format(
        title=args.title or links[-1].name, source=Path(args.html).name
    )
    _write(args.output, genipage.to_tsv(links, header=header))
    print(f"wrote {args.output}: {len(links)} steps, all with profile IDs")
    print(f"  {links[0].name} -> {links[-1].name}")
    return 0


def _cmd_consistency(args: argparse.Namespace) -> int:
    ws = Workspace.from_args(args)
    tree = _load_tree(args.source, ws)
    report = consistency.check(tree)

    output = args.output or ws.reports / "consistency.md"
    _write(output, consistency.render_markdown(tree, report, top=args.top))

    impossible = len(report.of_kind(consistency.IMPOSSIBLE))
    implausible = len(report.of_kind(consistency.IMPLAUSIBLE))
    likely = len(report.of_tier(consistency.LIKELY))
    possible = len(report.of_tier(consistency.POSSIBLE))
    print(f"wrote {output}")
    print(
        f"{report.people_checked} people, {report.people_with_a_year} with a year: "
        f"{impossible} impossible, {implausible} implausible"
    )
    print(
        f"duplicate profiles: {likely} likely, {possible} possible "
        f"({report.reused_names} groups excluded as reused sibling names)"
    )
    print("These are errors in Geni's data. Nothing here has been changed.")
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
            "--exports-dir", type=Path, default=None,
            help=f"where the exports live, searched recursively (default: {EXPORTS_DIR})",
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
    p_inv.add_argument("exports", nargs="*", help="GEDCOM files (default: every distinct .ged under exports/)")
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
    p_merge.add_argument("exports", nargs="*", help="GEDCOM files (default: every distinct .ged under exports/)")
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
        description="Reads out/merged.ged if it exists, otherwise merges the exports.",
    )
    p_export.add_argument(
        "--source", type=Path, default=None, help="a GEDCOM to read instead of merging"
    )
    p_export.add_argument(
        "-o", "--output", type=Path, default=None,
        help="directory for the JSONL files (default: <out>)"
    )
    p_export.set_defaults(func=_cmd_export)

    p_over = sub.add_parser(
        "overlap",
        help="our tree against every Wikidata item carrying a Geni ID",
        description=(
            "Fetches all ~517,000 P2600 statements in sixteen MD5 partitions and "
            "intersects them with the tree, so the overlap is counted from both "
            "sides. Responses are cached under out/wikidata/cache."
        ),
    )
    p_over.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_over.add_argument(
        "--offline",
        action="store_true",
        help=(
            "reuse the cached out/wikidata/p2600-all.tsv instead of fetching. "
            "Our side moves with every export and Wikidata's barely moves "
            "between them, so this is the one to run after a merge."
        ),
    )
    p_over.add_argument(
        "--delay", type=float, default=1.0, help="seconds between requests (default: 1.0)"
    )
    p_over.add_argument(
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/wikidata-overlap.md)"
    )
    p_over.set_defaults(func=_cmd_overlap)

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

    p_path = sub.add_parser(
        "path",
        help="check a Geni relationship path against the merged tree",
        description=(
            "Geni will show a chain of relationships between two profiles. That "
            "chain names people Geni knows about whether or not any export has "
            "reached them, which makes it the one piece of evidence here that "
            "comes from outside our own data. This reports, step by step, which "
            "of them the merge holds — and where the unbroken run stops, which "
            "is a doorway with a known payoff behind it. Steps are matched by "
            "NAME unless the path file carries profile IDs, so the result is "
            "advisory; see the module docstring."
        ),
    )
    p_path.add_argument("path", type=Path, help="a path file, e.g. paths/jimmu.tsv")
    p_path.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_path.add_argument("--title", default=None, help="heading for the report")
    p_path.add_argument(
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/path-<name>.md)"
    )
    p_path.add_argument(
        "--json", type=Path, default=None,
        help="machine-readable form (default: <reports>/path-<name>.json)"
    )
    p_path.set_defaults(func=_cmd_path)

    p_from_html = sub.add_parser(
        "path-from-html",
        help="extract a relationship path from a saved Geni profile page",
        description=(
            "A Geni profile page shows the chain of relationships from you to "
            "that person, and every name in it is a link carrying the profile "
            "ID. Copying the panel as text loses those; saving the page keeps "
            "them. This turns a saved page into a path file whose every row has "
            "a real ID, which is what lets `path` join on the primary key "
            "instead of matching names."
        ),
    )
    p_from_html.add_argument("html", type=Path, help="a Geni profile page saved from the browser")
    p_from_html.add_argument(
        "-o", "--output", type=Path, required=True, help="the path file to write"
    )
    p_from_html.add_argument("--title", default=None, help="name for the file's header")
    p_from_html.set_defaults(func=_cmd_path_from_html)

    p_cons = sub.add_parser(
        "consistency",
        help="find dates in the tree that contradict each other",
        description=(
            "Whether this tree's own dates can all be true at once — someone born "
            "before a parent, or after their mother died. These are errors in "
            "Geni's data, not in the merge, and nothing is changed: the report is "
            "a list to work from, with links to both people."
        ),
    )
    p_cons.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_cons.add_argument("--top", type=int, default=100, help="how many findings to list per kind")
    p_cons.add_argument(
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/consistency.md)"
    )
    p_cons.set_defaults(func=_cmd_consistency)

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

    p_dist = sub.add_parser(
        "distant",
        help="pairs of people far apart in our tree — ask Geni for the path between them",
        description=(
            "Finds people our tree connects only by a very long walk. Geni "
            "probably connects them by a much shorter one, and the people on "
            "that route are ones we do not hold — so each pair is a prediction "
            "that a community is missing, and the Geni relationship path "
            "between them is the test."
        ),
    )
    p_dist.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_dist.add_argument("--count", type=int, default=10, help="how many pairs (default: 10)")
    p_dist.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/distant-pairs.md"
    )
    p_dist.set_defaults(func=_cmd_distant)

    p_rem = sub.add_parser(
        "remote",
        help="the most remote people, ranked — each one a pair to ask Geni about",
        description=(
            "Ranks people by how far they are from the person they are "
            "furthest from, rather than emitting pairs in the order a greedy "
            "search happened to find them. Row 1 is the most remote person the "
            "measurement can find, and any two rows are provably far apart. "
            "Each row is a pair to open on Geni: our tree says this many hops, "
            "Geni will very likely show far fewer, and the people on that "
            "shorter chain are ones we do not hold."
        ),
    )
    p_rem.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_rem.add_argument("--count", type=int, default=20, help="how many people (default: 20)")
    p_rem.add_argument(
        "--landmarks",
        type=int,
        default=remote.LANDMARKS,
        help=f"landmarks to place; each costs one sweep (default: {remote.LANDMARKS})",
    )
    p_rem.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/remote-people.md"
    )
    p_rem.set_defaults(func=_cmd_remote)

    p_dbl = sub.add_parser(
        "doubles",
        help="Wikidata items claiming two of our people are the same person",
        description=(
            "Lists every Wikidata item whose P2600 statements name two or more "
            "Geni profiles that are both in our tree. Our merge keys on the "
            "profile ID so it cannot see these. Not a duplicate list: a row is "
            "either one person with two Geni profiles, or two people one of "
            "whose statements is wrong. Offline — reads the map that "
            "`overlap` wrote rather than re-fetching it."
        ),
    )
    p_dbl.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_dbl.add_argument(
        "--pairs", type=Path, default=None, help="default: <out>/wikidata/p2600-all.tsv"
    )
    p_dbl.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/wikidata-doubles.md"
    )
    p_dbl.set_defaults(func=_cmd_doubles)

    p_con = sub.add_parser(
        "connectors",
        help="the missing people that block our relationship paths, ranked by payoff",
        description=(
            "Checks every path file at once and groups the missing people into "
            "bridges — runs of consecutive absent steps, each with the doorway "
            "to seed an export on. Bridges sharing a person are one cluster, so "
            "a ten-person gap that blocks five paths outranks a fifty-person "
            "gap private to one. Writes reports/connectors.md and "
            "out/connectors.html."
        ),
    )
    p_con.add_argument("paths", nargs="*", help="path .tsv files (default: every one under paths/)")
    p_con.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_con.add_argument(
        "--paths-dir", type=Path, default=None, help=f"where to look for path files (default: {PATHS_DIR})"
    )
    p_con.add_argument(
        "--write-paths",
        action="store_true",
        help="also refresh reports/path-<name>.md and .json, which this run computes anyway",
    )
    p_con.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/connectors.md"
    )
    p_con.set_defaults(func=_cmd_connectors)

    p_den = sub.add_parser(
        "density",
        help="find regions of the tree that few exports have reached",
        description=(
            "Counts how many exports contain each person, then finds connected "
            "runs of people almost no export reached. Regions are neighbourhoods "
            "in the family graph, never geographic."
        ),
    )
    p_den.add_argument("exports", nargs="*", help="GEDCOM files (default: every distinct .ged under exports/)")
    p_den.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_den.add_argument(
        "--threshold", type=int, default=1, help="a person is thin at or below this many exports"
    )
    p_den.add_argument(
        "--min-size", type=int, default=2, help="ignore thin runs smaller than this"
    )
    p_den.add_argument(
        "--seed-list-min",
        type=int,
        default=100,
        help="smallest region to put in the seed list (default: 100)",
    )
    p_den.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/density.md"
    )
    p_den.set_defaults(func=_cmd_density)

    p_desc = sub.add_parser(
        "descendants",
        help="rank lines that stop early, by period, to reach modern times",
        description=(
            "Ranks people with few but not zero lines of descent running down "
            "from them — the line demonstrably continues and we have barely "
            "followed it — bucketed by birth-year period and by generations of "
            "recorded ancestry. The downward counterpart to `frontier`. Counts "
            "descent paths, not distinct people: somebody reached down two "
            "lines is two lines."
        ),
    )
    p_desc.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_desc.add_argument(
        "--small",
        type=int,
        default=descendants_mod.SMALL,
        help=f"most descent paths a line may hold and still count as barely followed (default: {descendants_mod.SMALL})",
    )
    p_desc.add_argument(
        "--band", type=int, default=descendants_mod.BAND_YEARS, help="width of a birth-year band in years"
    )
    p_desc.add_argument(
        "--per-band", type=int, default=5, help="how many candidates to show per band"
    )
    p_desc.add_argument(
        "--min-stall",
        type=int,
        default=0,
        help="drop lines already followed to within this many years of now (default: 0, off)",
    )
    p_desc.add_argument(
        "--target-year",
        type=int,
        default=descendants_mod.REACH_TARGET,
        help=(
            "the year a seed must be able to reach to be listed as a campaign "
            f"seed (default: {descendants_mod.REACH_TARGET})"
        ),
    )
    p_desc.add_argument(
        "--present",
        type=int,
        default=None,
        help="the year to measure stall against (default: this year)",
    )
    p_desc.add_argument(
        "-o", "--output", type=Path, default=None, help="default: <reports>/descendants.md"
    )
    p_desc.set_defaults(func=_cmd_descendants)

    p_er = sub.add_parser(
        "entity-resolution",
        help="turn the hand-written entity_resolution.md into a reviewable batch",
        description=(
            "Reads Emma's free-form Geni-to-Wikidata resolutions and label edits "
            "and writes a QuickStatements batch. Entries it cannot parse are "
            "reported, never dropped. Nothing is sent to Wikidata."
        ),
    )
    p_er.add_argument(
        "file", type=Path, nargs="?", default=None, help="default: entity_resolution.md at the repo root"
    )
    p_er.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_er.add_argument(
        "-o", "--output", type=Path, default=None, help="report path (default: <reports>/entity-resolution.md)"
    )
    p_er.add_argument(
        "--retrieved",
        default=date.today().isoformat(),
        help="date for the reference qualifier, YYYY-MM-DD (default: today)",
    )
    p_er.set_defaults(func=_cmd_entity_resolution)

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

    p_dl = sub.add_parser(
        "wikidata-download",
        help="download whole Wikidata items for the P2600 seed set, resumably",
        description=(
            "Two queues. The fetch queue starts as the whole P2600 seed set and "
            "is drained 50 items at a time into gzipped JSONL shards; the scan "
            "reads stored items for the relatives they name (P22/P25/P26/P40/"
            "P3373) and queues any not already known, so the set grows outward "
            "to people Wikidata has and Geni does not. Networked, resumable, and "
            "never asks for the same item twice. Start with --limit 1000 and "
            "read the numbers before running it long (todo.md 8a-revised). This "
            "is the ONLY command permitted to query Wikidata."
        ),
    )
    p_dl.add_argument(
        "--limit", type=int, default=None,
        help="stop after this many NEW items (the pilot; default: no limit)"
    )
    p_dl.add_argument(
        "--dry-run", action="store_true",
        help="say how many items and requests remain, and make none of them"
    )
    p_dl.add_argument(
        "--seeds", type=Path, default=None,
        help="QID list, one per line or TSV with the QID first (default: <out>/wikidata/p2600-all.tsv)"
    )
    p_dl.add_argument(
        "--store", type=Path, default=None,
        help="shard directory (default: wikidata/items — tracked, not under out/)"
    )
    p_dl.add_argument(
        "--index", type=Path, default=None,
        help="state index (default: <out>/wikidata/download-state.sqlite3)"
    )
    p_dl.add_argument(
        "--rebuild-index", action="store_true",
        help="re-derive the index from the shards first; the shards are the truth"
    )
    p_dl.add_argument(
        "--delay", type=float, default=1.0,
        help="seconds between requests (default: 1.0 — start slow, measure, only then consider faster)"
    )
    p_dl.add_argument(
        "--scan-per-round", type=int, default=500,
        help=(
            "stored items to read for relatives between fetches (default: 500). "
            "Higher than the fetch batch on purpose — reading local JSON is free "
            "and the job of the scan is to keep the fetch queue supplied."
        ),
    )
    p_dl.add_argument(
        "--report-every", type=int, default=10, help="print progress every N batches"
    )
    p_dl.set_defaults(func=_cmd_wikidata_download)

    p_profile = sub.add_parser(
        "profile-names",
        help="measure what the profiles actually contain: field fill rates and name scripts",
        description=(
            "Per-person fill rate of every enrichment field against its Wikidata "
            "property, and which scripts the names use — including how many CJK "
            "people carry no romanised form. Offline; proposes nothing."
        ),
    )
    p_profile.add_argument("--source", type=Path, default=None, help="a GEDCOM to read instead of merging")
    p_profile.add_argument(
        "-o", "--output", type=Path, default=None,
        help="where to write (default: <reports>/profile-names.md)"
    )
    p_profile.set_defaults(func=_cmd_profile_names)

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


def _survive_a_cp1252_console() -> None:
    """Stop a non-ASCII name in a progress line from killing the command.

    Every report this package writes is opened with an explicit UTF-8 encoding,
    so the files are never at risk. The console is another matter: on Windows
    `sys.stdout` defaults to the system codepage, and printing a summary line
    naming 蘇瑗 or 'A'idhullah al-'Ashiri raises `UnicodeEncodeError` *after*
    the work is done and the files are written — a command that succeeded
    exiting non-zero over a progress message.

    Seen for real on 2026-08-06, from `connectors`. Replacing unencodable
    characters is right here because this is chatter, not data: the same names
    are exact in `reports/` and in the HTML.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(errors="replace")
        except (ValueError, OSError):  # a stream that cannot be reconfigured
            pass


def main(argv: list[str] | None = None) -> int:
    _survive_a_cp1252_console()
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
