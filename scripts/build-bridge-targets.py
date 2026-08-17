"""Who blocks the most paths, and who sits nearest the middle of one.

**Both files this writes had no generator.** `reports/path-bridge-targets.csv` and
`reports/path-midpoint-seeds.csv` are the artefacts Emma's first agenda item runs on
— *"find people that are in multiple bridges and are also not in"* our data — and
they were produced by one-off code in a session that ended. Nothing in the repo could
rebuild them, and `scripts/build-trunk-batch.py` reads one of them, so the trunk
batch was derived from a file no command could reproduce. They were also measured
over 560 paths and a smaller tree, before the corpus reached 586 and 448,665 people.

**Positions are per chain, not per file.** Emma, 2026-08-16: *"as long as you treat
it as being two paths and not one."* A saved page carries a blood path and an in-law
path; `PathStep.chain` separates them. Measuring position within the file would put
the head of the second path at the middle of the first, which is precisely the
midpoint this ranks on — so a seam would manufacture the best candidate on the page.

### `path-bridge-targets.csv` — how many paths each person is on

One row per person named by any path, whether we hold them or not. The first five
columns are the ones `build-trunk-batch.py` reads and keep their names and order.

* `paths_through` — distinct path **chains** naming this person.
* `held` / `bridges_through` — new, and they are what makes her question answerable
  from one file: *"in multiple bridges and… also not in"* our data is two conditions
  and the old file only carried the first. **Emma is row 1** — 818 chains, because
  *"You"* opens every path — with `held` yes and `bridges_through` 0, so she reads
  correctly as the opposite of a bridge person.

  `held` is deliberately **not** a filter on creation: somebody we hold who has no
  Wikidata item is exactly who `build-trunk-batch.py` should create. It is a filter
  on *seeding an export*, which is the other file.

### `path-midpoint-seeds.csv` — where to seed an export

Missing people only, because a seed is a gap: *"The way we create exports is that
they have to find gaps in the family trees, fill them in with a placeholder
individual, and then run a traversal."*

**`midpointness` is the mean of `min(position, 1 - position)`** over every chain the
person appears on, where `position` is their normalised index in that chain. It peaks
at **0.5** for somebody exactly halfway along and falls to 0 at either end.

**The definition is stated, not recovered**, and the evidence for it is partial: of
the three rows sampled from the file the lost code produced, `Alice de Lucy` came out
0.423 against 0.422 here and `Joan Dacre` 0.412 against 0.407, while `Ingeborg
Bengtsdotter Sparre över blad` moved 0.373 → 0.443. The two near-matches are what
recommend the formula; the third moved in the direction the **chain split** predicts,
since her position inside one path is not her position inside a file holding two. So
this is a formula that agrees with the old numbers where the inputs agree, not a
reproduction of them.

Why the middle: *"we're supposed to get ones ideally at the midpoint of the chain, so
the forest will expand and grab as much of it as possible… the accessibility to what
we already have is basically irrelevant."*

Offline. Loads the merge once; nothing is asked of the network.

    PYTHONPATH=src python scripts/build-bridge-targets.py --source out/merged.ged
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import connectors, sources  # noqa: E402
from genimerge.gedcom import parse  # noqa: E402
from genimerge.model import build_tree  # noqa: E402

PATHS_DIR = REPO / "paths"
LABELS = REPO / "reports" / "derived-labels.csv"
OUT_BRIDGE = REPO / "reports" / "path-bridge-targets.csv"
OUT_MIDPOINT = REPO / "reports" / "path-midpoint-seeds.csv"

csv.field_size_limit(10 ** 7)


def load_tree(source: Path | None):
    if source:
        print(f"reading {source}")
        records = parse(source.read_text(encoding="utf-8", errors="replace")).records
    else:
        from genimerge.merge import merge_files

        files = sources.find_exports(REPO / "exports")
        print(f"merging {len(files)} exports")
        records = merge_files(files).records
    tree = build_tree(records)
    tree.resolve_relationships()
    print(f"{len(tree.people):,} people")
    return tree


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path,
                    help="a merged GEDCOM to read instead of re-merging")
    ap.add_argument("--paths-dir", type=Path, default=PATHS_DIR)
    args = ap.parse_args()

    files = sorted(args.paths_dir.glob("*.tsv"))
    if not files:
        print(f"no path files under {args.paths_dir}", file=sys.stderr)
        return 1

    # The Geni -> QID map, from `P2600` *Geni.com profile ID* as derived. `Person`
    # carries no QID, so this cannot come off the tree.
    qids: dict[str, str] = {}
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("qid") or "").strip():
                qids[row["geni_id"]] = row["qid"].strip()
    print(f"{len(qids):,} people carry a Wikidata item")

    tree = load_tree(args.source)
    _, reports = connectors.collect(tree, files)
    print(f"{len(reports):,} path files checked")

    # (geni_id) -> the facts we aggregate over. `chains` counts distinct
    # (file, chain) pairs, `files` distinct files, so a person walked twice on one
    # page counts once per path rather than once per step.
    chains_of: dict[str, set[tuple[str, int]]] = defaultdict(set)
    files_of: dict[str, set[str]] = defaultdict(set)
    positions: dict[str, list[float]] = defaultdict(list)
    steps_of: dict[str, list[int]] = defaultdict(list)
    held_of: dict[str, bool] = {}
    name_of: dict[str, str] = {}
    qid_of: dict[str, str] = {}
    bridged: dict[str, set[tuple[str, int]]] = defaultdict(set)

    for name, report in reports.items():
        for chain in report.chains:
            results = chain.results
            last = len(results) - 1
            index = results[0].step.chain
            for i, result in enumerate(results):
                gid = result.step.geni_id
                if not gid:
                    continue
                chains_of[gid].add((name, index))
                files_of[gid].add(name)
                positions[gid].append(0.0 if last == 0 else i / last)
                steps_of[gid].append(result.step.step)
                # Held anywhere means held: the tree does not vary by path, and a
                # `REPEAT` on one path is the same person we hold on another.
                held_of[gid] = held_of.get(gid, False) or result.held
                name_of.setdefault(gid, result.step.name)
                if gid in qids:
                    qid_of[gid] = qids[gid]
                if not result.held:
                    bridged[gid].add((name, index))

    rows = []
    for gid, chains in chains_of.items():
        rows.append({
            "paths_through": len(chains),
            "geni_id": gid,
            "name": name_of.get(gid, ""),
            "qid": qid_of.get(gid, ""),
            "nearest_step": min(steps_of[gid]),
            "held": "yes" if held_of.get(gid) else "",
            "bridges_through": len(bridged.get(gid, ())),
            "files_through": len(files_of[gid]),
            "midpointness": round(
                sum(min(p, 1 - p) for p in positions[gid]) / len(positions[gid]), 3),
            "mean_position": round(sum(positions[gid]) / len(positions[gid]), 3),
        })
    rows.sort(key=lambda r: (-r["paths_through"], r["geni_id"]))

    with OUT_BRIDGE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT_BRIDGE} ({len(rows):,} people named by a path)")

    missing = [r for r in rows if not r["held"]]
    missing.sort(key=lambda r: (-r["bridges_through"], -r["midpointness"], r["geni_id"]))
    with OUT_MIDPOINT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["paths", "midpointness", "geni_id", "name", "mean_position"])
        for r in missing:
            w.writerow([r["bridges_through"], r["midpointness"], r["geni_id"],
                        r["name"], r["mean_position"]])
    print(f"wrote {OUT_MIDPOINT} ({len(missing):,} missing people)")

    held = sum(1 for r in rows if r["held"])
    print(f"\n  {held:,} of {len(rows):,} people named by a path are held")
    print(f"  {len(missing):,} are not, and are the bridge population")
    print("\ntop of the midpoint ranking:")
    for r in missing[:8]:
        print(f"  {r['bridges_through']:>3} paths  midpointness {r['midpointness']:.3f}"
              f"  {r['geni_id']:<20} {r['name'][:40]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
