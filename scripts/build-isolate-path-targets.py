"""The roster for mass-exporting Geni relationship paths to disconnected Wikidata people.

**Emma's idea, 2026-09-02:** *"what if we mass exported the paths to the disconnected
wikidata people on geni? ... the mass export of the path lists might be feasible and help
with getting wikidata generally connected even if we have a bunch of 'sinews' only linking
people in."*

A Geni relationship path is the only evidence in this repo that comes from **outside** our
own data --- it names people whether or not any export has reached them (`CLAUDE.md`
§ *Relationship paths: save the page, never the pasted text*). So a path to an isolated
Wikidata item is a chain that can be created on Wikidata and joins that item to the graph,
without needing an export of its neighbourhood. That is the sinew.

**The target population, measured 2026-09-02:** 185,327 --- Wikidata items carrying a Geni
ID, stating no `P22`/`P25`/`P40`/`P26`, whose Geni profile is **not in our merged tree**,
and having no saved path yet. `out/wikidata/relations.tsv` carries no `P3373` *sibling*
column, so this over-counts slightly: an item whose only stated relation is a sibling reads
as isolated here.

**Why it is worth doing, and it is measured rather than argued.** The 663 paths already in
`paths/isolate-geni-*.tsv` name 10,645 distinct people over 26,762 steps, and the yield does
not saturate --- 20.7 new people per path over the first 100, still **13.8** over paths
501-600, in random order.

**The path is a URL, not a page save.** Taken off the saved pages themselves:

    https://www.geni.com/path/x?from=<FROM>&path_type=blood&to=<target>
    https://www.geni.com/path/x?from=<FROM>&path_type=inlaw&to=<target>

The slug between `/path/` and `?` is cosmetic. So no profile page load and no expand click ---
a blob-saved profile page carries only 3 `span.segment` anchors (the collapsed *You -> X*),
against 118 on a saved path page, which is why the profile-page capture cannot be reused here.

**`FROM` is Charlemagne, and the 663 existing paths do NOT follow this rule.** Every one of
them is anchored on Emma (`6000000087535357291`, step 1 "You" on 679 saved paths) because they
were saved from her own profile view. Her 2026-09-03 correction moves the anchor to Charlemagne
for everything new. The old paths stay --- they are evidence of what Geni said --- but they
answer a different question.

**Both path types, always --- Emma's call, 2026-09-02.** `blood` follows descent only;
`inlaw` allows marriage steps and reaches people no blood path can. Two fetches per target.

**This is a PILOT of 100, her call the same day.** The hit rate for the general population is
the one thing not measured: her own batches ran **34-39%** for academics filtered by
occupation alone and **92%** for Nordic academics, so a uniform sample is what says which end
of that range a 185k campaign sits at. The sample is uniform over the whole population rather
than over the un-rostered part of it, so it projects to the campaign as a whole; the
`in_nordic_roster` column lets the result be split back out.

**Labels are best-effort and mostly blank.** `out/wikidata/labels.tsv` and the store index are
both gitignored rebuilds and are absent from a clean clone, so the label is joined from the
three isolate rosters in `reports/` where it happens to be there. The pilot needs the ids.

    python scripts/build-isolate-path-targets.py [--all] [-n N]

`--all` writes the whole roster instead of the pilot sample.
"""

from __future__ import annotations

import argparse
import csv
import glob
import gzip
import random
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

csv.field_size_limit(10_000_000)

# **The anchor is CHARLEMAGNE, not Emma --- her correction, 2026-09-03:** *"I believe
# Charlemagne is the most central person in the Jenny graph, so it would be going through
# Charlemagne. We pin relationships to Charlemagne, and we go to each individual."* An
# Emma-anchored path measures distance from her; a Charlemagne-anchored one runs through the
# densest part of the World Tree, which is where the surface area is.
#
# `6000000002457013227` is `Q3044` Charlemagne in `reports/derived-labels.csv`, and is step 34
# --- the far end --- of `paths/charlemagne-to-arne-garborg.tsv`.
FROM = "6000000002457013227"
PATH_URL = "https://www.geni.com/path/x?from={frm}&path_type={kind}&to={to}"
PATH_TYPES = ("blood", "inlaw")

RELATIONS = REPO / "out" / "wikidata" / "relations.tsv"
LABELS_GZ = REPO / "reports" / "derived-labels.csv.gz"
LABELS_CSV = REPO / "reports" / "derived-labels.csv"
ROSTERS = ("nordic-isolates.csv", "academic-isolates.csv", "east-asia-isolates.csv")
NORDIC = "nordic-isolates.csv"

OUT_TSV = REPO / "reports" / "isolate-path-pilot.tsv"
OUT_URLS = REPO / "reports" / "isolate-path-pilot-urls.txt"
OUT_ALL = REPO / "reports" / "isolate-path-targets.tsv"

# The pilot must be the same 100 on every rebuild, or a re-run silently asks Geni for a
# different sample and the hit rate stops being comparable. Sorting is on the qid, which is
# unique --- `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* wants a total key, and a qid is one.
SEED = 20260902


def tree_members() -> set[str]:
    """Every Geni id in the merged tree, from whichever of the two derived-labels forms exists."""
    src = LABELS_CSV if LABELS_CSV.exists() else LABELS_GZ
    opener = open if src is LABELS_CSV else gzip.open
    with opener(src, "rt", encoding="utf-8") as fh:
        return {row["geni_id"] for row in csv.DictReader(fh)}


def already_pathed() -> set[str]:
    """Every Geni id named on a saved path --- a fetch for one of these buys nothing new."""
    seen: set[str] = set()
    for f in sorted(glob.glob(str(REPO / "paths" / "*.tsv"))):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("#") or line.startswith("step\t"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 4:
                    m = re.match(r"geni:(\d+)", parts[3])
                    if m:
                        seen.add(m.group(1))
    return seen


def roster_labels() -> tuple[dict[str, str], set[str]]:
    """Labels off the three isolate rosters, and which qids are on the Nordic one."""
    labels: dict[str, str] = {}
    nordic: set[str] = set()
    for name in ROSTERS:
        p = REPO / "reports" / name
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                qid = row.get("qid", "")
                if not qid:
                    continue
                if row.get("label"):
                    labels.setdefault(qid, row["label"])
                if name == NORDIC:
                    nordic.add(qid)
    return labels, nordic


def population(have: set[str], pathed: set[str]) -> list[tuple[str, str]]:
    """(qid, geni_id) for every isolated, un-held, un-pathed item, sorted by qid."""
    out: list[tuple[str, str]] = []
    with open(RELATIONS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            geni = row["p2600"].strip()
            if not geni:
                continue
            if any(row[k].strip() for k in ("p22", "p25", "p40", "p26")):
                continue
            # A second Geni ID on one item is not a conflict --- `CLAUDE.md` says so --- and the
            # first is the one the path is fetched for. The rest ride along on later rounds.
            gid = geni.split("|")[0].strip()
            if gid in have or gid in pathed:
                continue
            out.append((row["qid"], gid))
    out.sort()
    return out


def write(rows, labels, nordic, dest: Path, urls: Path | None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["qid", "geni_id", "label", "in_nordic_roster", "blood_url", "inlaw_url"])
        for qid, gid in rows:
            w.writerow([
                qid,
                gid,
                labels.get(qid, ""),
                "1" if qid in nordic else "0",
                PATH_URL.format(frm=FROM, kind="blood", to=gid),
                PATH_URL.format(frm=FROM, kind="inlaw", to=gid),
            ])
    tmp.replace(dest)

    if urls is None:
        return
    tmp = urls.with_suffix(urls.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        for qid, gid in rows:
            for kind in PATH_TYPES:
                fh.write(PATH_URL.format(frm=FROM, kind=kind, to=gid) + "\n")
    tmp.replace(urls)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="write the whole roster, not the pilot")
    ap.add_argument("-n", type=int, default=100, help="pilot size (default 100)")
    args = ap.parse_args()

    have = tree_members()
    pathed = already_pathed()
    pop = population(have, pathed)
    labels, nordic = roster_labels()

    print(f"tree: {len(have)} people", file=sys.stderr)
    print(f"already named on a saved path: {len(pathed)}", file=sys.stderr)
    print(f"target population: {len(pop)}", file=sys.stderr)

    if args.all:
        write(pop, labels, nordic, OUT_ALL, None)
        print(f"wrote {OUT_ALL.relative_to(REPO)} ({len(pop)} rows)", file=sys.stderr)
        return 0

    n = min(args.n, len(pop))
    sample = sorted(random.Random(SEED).sample(pop, n))
    write(sample, labels, nordic, OUT_TSV, OUT_URLS)
    in_nordic = sum(1 for qid, _ in sample if qid in nordic)
    print(
        f"wrote {OUT_TSV.relative_to(REPO)} ({n} targets, {n * 2} URLs; "
        f"{in_nordic} on the Nordic roster)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
