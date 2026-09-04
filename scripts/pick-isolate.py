"""One random Wikidata isolate that our synoptic tree does not connect --- and it heals itself.

**Emma, 2026-09-03**, after watching profile-picking take far too long: *"you probably should
have a script that spits out a random one whenever you need one."* Her specification, in her
words:

    my vision would be that you have some kind of a csv file storing all of the wikidata
    isolates, and the script randomly selects one, checks if it is connected into the synoptic
    tree (geni links in the big mass), and if it is not then it returns it, and if it does not
    then it randomly selects another one and does the same, with a later option to with the
    script to refresh things so that the isolates csv is updated in cases where it is stale and
    a large portion of the unconnected people are skipped over, maybe even actually just removing
    the one that was found to be connected as soon as it is skipped over, making the script
    automatically heal it

    python scripts/pick-isolate.py            # one person
    python scripts/pick-isolate.py -n 5       # five
    python scripts/pick-isolate.py --refresh  # rebuild the roster and the component first

**THE SELF-HEALING IS THE POINT, and it is a WRITE on an ordinary read.** A draw that lands on
somebody the tree now reaches is not merely skipped --- that person is *deleted from the roster*
and another is drawn. So the file gets more accurate every time it is used and needs no
maintenance pass. `--refresh` is for when staleness has grown past what incidental use clears.

**Two files, two different kinds of staleness, refreshed by different things:**

  * `reports/wikidata-isolate-roster.csv` --- every Wikidata item carrying a `P2600` and stating
    no `P22`/`P25`/`P40`/`P26`. Built from `out/wikidata/relations.tsv`, which is a **download
    snapshot**: an item that gained a parent on Wikidata since the download still reads as
    isolated here. That is the staleness the healing erodes.
  * `out/main-component.txt.gz` --- the Geni ids reachable from Charlemagne over
    `reports/derived-family.csv`. Rebuilt when that file's size changes, which is what happens
    when the tree is re-merged.

**`relations.tsv` carries no `P3373` column**, so an item whose only stated relation is a sibling
reads as isolated. The roster therefore over-counts slightly, exactly as
`build-isolate-path-targets.py` records for the same file. Stated rather than silently corrected.

**Connectivity needs no sibling handling, even though `CLAUDE.md` § *A sibling step is the worked
example* warns about it.** That rule is about walking a *path*, where two siblings are one step
apart on Geni and two hops apart in our data. Component membership is unaffected: siblings reach
each other through the shared parent either way, so parent, child and spouse edges settle it.

**A blank label means `out/wikidata/labels.tsv` was absent, NOT that the item has no label.**
That file is 187 MB and gitignored, so a clean clone does not have it --- `CLAUDE.md` § *THE
PARENT DECK* is the same trap, where a missing labels file published a page of bare QIDs. The
roster keeps the ids, which is what a draw is answered with.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import os
import random
import sys
from importlib import import_module
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

csv.field_size_limit(1 << 30)

RELATIONS = REPO / "out" / "wikidata" / "relations.tsv"
LABELS_WD = REPO / "out" / "wikidata" / "labels.tsv"
FAMILY_CSV = REPO / "reports" / "derived-family.csv"
FAMILY_GZ = REPO / "reports" / "derived-family.csv.gz"
ROSTER = REPO / "reports" / "wikidata-isolate-roster.csv"
COMPONENT = REPO / "out" / "main-component.txt.gz"

#: `6000000002457013227` is `Q3044` Charlemagne --- her anchor, per
#: `build-isolate-path-targets.py`: *"I believe Charlemagne is the most central person in the
#: Jenny graph."* The component containing him is what she calls the big mass.
CHARLEMAGNE = "6000000002457013227"

#: The relationship columns of `out/wikidata/relations.tsv`. No `P3373`; see the docstring.
STATED = ("p22", "p25", "p40", "p26")


def _atomic_write(path: Path, text: str, *, binary: bytes | None = None) -> None:
    """Write via a temp file and `os.replace`.

    `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* records why: `open(path, "w")` truncates
    *before* a writer can raise, so a failed write destroys the file it was replacing. An atomic
    replace makes a failure a no-op instead. This one rewrites the roster on an ordinary read,
    so it is the healing path rather than a rare one.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    if binary is None:
        tmp.write_text(text, encoding="utf-8", newline="\n")
    else:
        tmp.write_bytes(binary)
    os.replace(tmp, path)


def _family_size() -> int:
    """The size of whichever form of the tree is on disk --- the component cache's staleness key.

    Not an mtime: a fresh clone gives every file the checkout time, so mtimes would report
    *everything changed* on a tree nobody rebuilt.
    """
    src = FAMILY_CSV if FAMILY_CSV.exists() else FAMILY_GZ
    return src.stat().st_size if src.exists() else 0


def build_component() -> set[str]:
    """Every Geni id reachable from Charlemagne, via the eccentricity walker.

    Imported rather than re-derived: that module already builds the undirected adjacency, already
    knows the ` | ` separator, and already dedupes the both-directions double count. Re-deriving
    adjacency is how `CLAUDE.md` keeps collecting separator bugs.
    """
    ecc = import_module("measure-eccentricity")
    index, neighbours = ecc.load_graph()
    start = index.get(CHARLEMAGNE)
    if start is None:
        sys.exit("Charlemagne %s is not in the tree; the component cannot be anchored"
                 % CHARLEMAGNE)
    dist = ecc.bfs(start, neighbours)
    back = [""] * len(index)
    for g, i in index.items():
        back[i] = g
    return {back[i] for i, d in enumerate(dist) if d >= 0}


def write_component(members: set[str]) -> None:
    body = "# source_bytes=%d people=%d\n%s\n" % (
        _family_size(), len(members), "\n".join(sorted(members)))
    _atomic_write(COMPONENT, "", binary=gzip.compress(body.encode("utf-8")))


def load_component(*, refresh: bool) -> set[str]:
    """The cached component, rebuilt when the tree has changed under it."""
    if not refresh and COMPONENT.exists():
        with gzip.open(COMPONENT, "rt", encoding="utf-8") as fh:
            head = fh.readline()
            if "source_bytes=%d" % _family_size() in head:
                return {line.strip() for line in fh if line.strip()}
        print("the tree has changed since the component was cached; rebuilding", file=sys.stderr)
    members = build_component()
    write_component(members)
    print("main component: %s people reachable from Charlemagne" % format(len(members), ","),
          file=sys.stderr)
    return members


def wikidata_labels(wanted: set[str]) -> dict[str, str]:
    if not LABELS_WD.exists():
        print("out/wikidata/labels.tsv absent (gitignored) -- the roster keeps ids, not names",
              file=sys.stderr)
        return {}
    out: dict[str, str] = {}
    with io.open(LABELS_WD, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 1 and parts[0] in wanted:
                out.setdefault(parts[0], parts[1])
    return out


def build_roster() -> list[dict[str, str]]:
    rows: list[tuple[str, str]] = []
    with io.open(RELATIONS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            geni = (row.get("p2600") or "").strip()
            if not geni:
                continue
            if any((row.get(k) or "").strip() for k in STATED):
                continue
            # A second Geni ID on one item is not a conflict -- `CLAUDE.md` says so -- and the
            # first is the one a draw is answered about.
            rows.append((row["qid"], geni.split("|")[0].strip()))
    rows.sort()                       # a qid is unique, so this is a total order
    labels = wikidata_labels({q for q, _ in rows})
    return [{"qid": q, "geni_id": g, "label": labels.get(q, "")} for q, g in rows]


def write_roster(rows: list[dict[str, str]]) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["qid", "geni_id", "label"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    _atomic_write(ROSTER, buf.getvalue())


def load_roster(*, refresh: bool) -> list[dict[str, str]]:
    if refresh or not ROSTER.exists():
        rows = build_roster()
        write_roster(rows)
        print("roster: %s Wikidata isolates -> %s"
              % (format(len(rows), ","), ROSTER.relative_to(REPO)), file=sys.stderr)
        return rows
    with io.open(ROSTER, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-n", type=int, default=1, help="how many to hand back (default 1)")
    ap.add_argument("--refresh", action="store_true",
                    help="rebuild the roster and the component before drawing")
    ap.add_argument("--seed", type=int, help="fix the draw, for a reproducible run")
    args = ap.parse_args()

    rows = load_roster(refresh=args.refresh)
    if not rows:
        print("the roster is empty; run with --refresh", file=sys.stderr)
        return 1
    component = load_component(refresh=args.refresh)

    rng = random.Random(args.seed)
    by_qid = {r["qid"]: r for r in rows}
    picks: list[dict[str, str]] = []
    healed: list[str] = []
    pool = list(by_qid)
    tried = 0
    while pool and len(picks) < args.n:
        tried += 1
        q = pool.pop(rng.randrange(len(pool)))
        row = by_qid[q]
        if row["geni_id"] in component:
            # Connected after all: DELETE rather than skip. That is the healing.
            healed.append(q)
            del by_qid[q]
            continue
        picks.append(row)

    if healed:
        write_roster(sorted(by_qid.values(), key=lambda r: r["qid"]))
        print("healed: %s drawn people were in the big mass and are out of the roster (%s left)"
              % (format(len(healed), ","), format(len(by_qid), ",")), file=sys.stderr)

    if not picks:
        print("no unconnected isolate found in %s draws" % format(tried, ","), file=sys.stderr)
        return 1

    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(["qid", "geni_id", "label", "wikidata", "geni"])
    for r in picks:
        w.writerow([r["qid"], r["geni_id"], r["label"],
                    "https://www.wikidata.org/wiki/" + r["qid"],
                    "https://www.geni.com/people/x/" + r["geni_id"]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
