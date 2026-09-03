"""Turn saved Geni `/path/` pages into path TSVs, and measure the hit rate.

The other half of `scripts/build-isolate-path-targets.py`. That one writes the URLs; the
browser fetches them; this one reads what came back.

**A hit** renders the relationship pathway --- anchors inside ``span.segment > span.name``,
which `genimerge.genipage` already parses and which `paths/isolate-geni-*.tsv` was built from.
The discriminator is the parsed step count, and the threshold is deliberate: a page yielding
fewer than `MIN_STEPS` rows carries no chain, because the `from` profile alone is a segment.

**A MISS IS NOT A STATEMENT THAT THE TWO ARE UNRELATED --- Emma, 2026-09-03:** *"not related
to is not actually a statement that the person is not related. It superficially appears that
way, but it is not that way. It sometimes gives a not related to from a query timeout."* So
`no_chain` is what the column means and what it is named. Reading it as *unrelated* is a
`CLAUDE.md` § *"Is X present?"* failure in a new costume: it measures Geni's query budget and
reports it as Geni's content.

**And the timeout is informative in the other direction.** Her reading: a timeout *"usually
indicates that the person is very eccentric on the World Tree graph"* --- so a `no_chain` is
weak evidence the target sits somewhere sparse, not evidence they are unreachable. There are
*"plenty of people that have verifiable relationships but which it does not show up for."*

**The route for those, and it is expensive so it is for high-value targets only.** Build a
seed individual from the person's ancestry per `docs/export-seed-rules.md`, run a `Forest`
export, and read the size: *"if the forest export returns five thousand people, then they
generally are connected"* --- in an odd cluster rather than off the graph. Random `Forest`
sampling on high-eccentricity individuals, biased toward earlier generations, then reliably
joins them to the World Tree. Time-consuming, *"but it is very possible."*

**The rate the pilot measures is therefore a REACH rate, not a connectivity rate.** Emma's own
batches ran **34-39%** for academics filtered by occupation and **92%** for Nordic academics.
What it decides is the request budget for a 185,327-target campaign, not who is related.

**Both path types, always --- Emma, 2026-09-02.** `blood` follows descent only; `inlaw`
allows marriage steps and reaches people no blood path can.

**And the quantity is PEOPLE, not reachability --- Emma, 2026-09-03:** *"Both helps as it
gives a more diverse set of connections. More places to add more people onto."* So a target
the two types both reach is **not** a duplicate fetch: the second chain runs through
different people, and every one of them is another place to hang a creation on. Counting
targets with a chain would score that second chain at zero.

Hence three people-columns beside the per-type step counts: `people_union` (distinct people
the pair names), `inlaw_only_people` (what the second fetch buys that the first did not), and
`people_new` --- those in neither the merged tree nor any path already held, which is the
sinew proper. If `inlaw_only_people` runs near zero the campaign can halve its fetches; that
is the thing the pilot settles, and it is not the hit rate.

**Page naming.** `<geni_id>-<blood|inlaw>.html`, the same blob-of-`outerHTML` capture
`scripts/sweep-scraped-pages.sh` already files, with the type appended so the two do not
collide. A bare `<geni_id>.html` is read as `blood`.

**This has NOT been run against a real `/path/` page.** The parser is the one that built the
663 existing paths, and the path page is where that panel lives, but no page of this exact
shape has been fetched --- Geni is not reachable from the session this was written in. The
first pilot page is the thing that establishes it, and a run reporting 0 steps on every page
means the markup differs, not that nothing is connected.

    python scripts/harvest-isolate-paths.py [--pages DIR] [--write-paths]

`--write-paths` writes `paths/isolate-<qid>-<kind>.tsv` for every hit. Without it the run
only measures, which is what a pilot wants before 185k of anything is committed to.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

sys.path.insert(0, str(REPO / "scripts"))

import importlib  # noqa: E402

from genimerge import genipage  # noqa: E402

targets_mod = importlib.import_module("build-isolate-path-targets")

csv.field_size_limit(10_000_000)

PAGES = REPO / "geni-paths"
PILOT = REPO / "reports" / "isolate-path-pilot.tsv"
RESULTS = REPO / "reports" / "isolate-path-pilot-results.tsv"
PATH_TYPES = ("blood", "inlaw")

# `from` and `to` are both segments on a rendered path, so two rows is the shortest real chain
# and anything under that is Geni returning none. **Returning none is not the same as there
# being none** --- see the docstring; a query timeout renders identically.
MIN_STEPS = 2


def read_page(p: Path) -> list:
    raw = p.read_text(encoding="utf-8", errors="replace")
    return genipage.parse_relationship_path(genipage.html_of_saved_page(raw))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=str(PAGES), help="directory of saved path pages")
    ap.add_argument("--roster", default=str(PILOT), help="target roster TSV")
    ap.add_argument("--results", default=str(RESULTS), help="where to write the results TSV")
    ap.add_argument("--write-paths", action="store_true", help="also write paths/*.tsv for hits")
    args = ap.parse_args()

    pages = Path(args.pages)
    pilot, results = Path(args.roster), Path(args.results)
    if not pilot.exists():
        print(f"no {pilot} --- run build-isolate-path-targets.py", file=sys.stderr)
        return 1

    # The two "do we already have this person?" sets come from the roster builder rather than
    # being rebuilt here, so the harvest and the roster can never disagree about what is held.
    held = targets_mod.tree_members() | targets_mod.already_pathed()
    new_people: set[str] = set()

    targets = list(csv.DictReader(open(pilot, encoding="utf-8"), delimiter="\t"))
    rows = []
    for t in targets:
        gid, qid = t["geni_id"], t["qid"]
        row = {
            "qid": qid,
            "geni_id": gid,
            "label": t["label"],
            "in_nordic_roster": t["in_nordic_roster"],
        }
        walked: dict[str, set[str]] = {}
        for kind in PATH_TYPES:
            candidates = [pages / f"{gid}-{kind}.html"]
            if kind == "blood":
                candidates.append(pages / f"{gid}.html")
            page = next((c for c in candidates if c.exists()), None)
            if page is None:
                row[f"{kind}_steps"] = ""
                continue
            links = read_page(page)
            row[f"{kind}_steps"] = len(links)
            if len(links) >= MIN_STEPS:
                walked[kind] = {l.geni_id for l in links if l.geni_id}
            if args.write_paths and len(links) >= MIN_STEPS:
                out = REPO / "paths" / f"isolate-{qid.lower()}-{kind}.tsv"
                header = (
                    f"# Geni relationship path to {t['label'] or qid} ({kind})\n"
                    f"#\n"
                    f"# GENERATED by scripts/harvest-isolate-paths.py from {page.name}.\n"
                    f"# Do not hand-edit: re-run the command instead.\n"
                )
                out.write_text(genipage.to_tsv(links, header=header), encoding="utf-8")

        # **The union is the quantity, not reachability --- Emma, 2026-09-03:** *"Both helps as
        # it gives a more diverse set of connections. More places to add more people onto."* So a
        # target with a chain of both types is not a duplicate: the second chain is more surface to
        # hang people on, and `inlaw_only_people` is what the second fetch actually buys.
        blood, inlaw = walked.get("blood", set()), walked.get("inlaw", set())
        union = blood | inlaw
        row["people_union"] = len(union) if union else ""
        row["inlaw_only_people"] = len(inlaw - blood) if union else ""
        # Everyone the pair names who is in neither the tree nor any path we already hold. This
        # is the sinew proper --- the people the campaign exists to reach.
        row["people_new"] = len(union - held) if union else ""
        new_people.update(union - held)
        rows.append(row)

    fetched = [r for r in rows if r["blood_steps"] != "" or r["inlaw_steps"] != ""]

    def hit(r, kind):
        v = r[f"{kind}_steps"]
        return v != "" and v >= MIN_STEPS

    for r in rows:
        r["chain_found"] = "1" if (hit(r, "blood") or hit(r, "inlaw")) else "0"

    results.parent.mkdir(parents=True, exist_ok=True)
    tmp = results.with_suffix(".tsv.tmp")
    cols = [
        "qid", "geni_id", "label", "in_nordic_roster",
        "blood_steps", "inlaw_steps", "chain_found",
        "people_union", "inlaw_only_people", "people_new",
    ]
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["qid"]):
            w.writerow(r)
    tmp.replace(results)

    print(f"targets in roster : {len(rows)}", file=sys.stderr)
    print(f"pages fetched     : {len(fetched)}", file=sys.stderr)
    if not fetched:
        print("nothing fetched yet --- no hit rate to report", file=sys.stderr)
        return 0

    found = sum(1 for r in fetched if r["chain_found"] == "1")
    print(f"chain found (either): {found}/{len(fetched)} = {found / len(fetched):.0%}"
          "   <- a miss is NO CHAIN RETURNED, never 'unrelated'", file=sys.stderr)
    for kind in PATH_TYPES:
        tried = [r for r in fetched if r[f"{kind}_steps"] != ""]
        if tried:
            h = sum(1 for r in tried if hit(r, kind))
            print(f"  {kind:<6}          : {h}/{len(tried)} = {h / len(tried):.0%}", file=sys.stderr)
    only_inlaw = sum(1 for r in fetched if hit(r, "inlaw") and not hit(r, "blood"))
    print(f"  chain ONLY via inlaw: {only_inlaw}", file=sys.stderr)

    # What the campaign is actually buying. Reachability counts targets; this counts people, and
    # people are the places to add more people onto.
    print(f"NEW people (not in tree, not on any held path): {len(new_people)}", file=sys.stderr)
    both = [r for r in fetched if hit(r, "blood") and hit(r, "inlaw")]
    if both:
        extra = sum(r["inlaw_only_people"] for r in both)
        print(
            f"  targets with BOTH chains: {len(both)}; people the inlaw chain adds "
            f"beyond the blood one: {extra} ({extra / len(both):.1f} per target)",
            file=sys.stderr,
        )
    steps = [r["blood_steps"] for r in fetched if hit(r, "blood")]
    if steps:
        print(f"  blood steps: median {sorted(steps)[len(steps) // 2]}, max {max(steps)}", file=sys.stderr)
    print(f"wrote {results}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
