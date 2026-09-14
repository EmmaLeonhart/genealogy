"""Turn `reports/path-chains.tsv` into one `paths/*.tsv` per chain, so the tiny-GEDCOM
writer can read them.

    python scripts/split-path-chains.py

**Why a split rather than a new emitter.** `scripts/build-tiny-gedcoms.py` already turns a
`paths/<name>.tsv` into `exports/tiny-paths/<name>.ged`, and it already knows the things that are
easy to get wrong: a sibling hop becomes a `CHIL`-only family and **invents no parents**, an
`ex-husband` becomes a divorced family, `fiance` becomes an engagement. Writing a second emitter
would duplicate all of that and then drift from it. So this script only changes the shape.

    reports/path-chains.tsv     to_id  kind  step  profile_id  name  relation
    paths/<name>.tsv            step   name  relation_to_previous   geni:<id>

**Step 0 is the viewer and the harvest records no id for her**, because the rendered page prints
her name without a profile link. The id is in the permalink's `from=` on every row of
`reports/geni-paths-harvest.tsv`, and it is filled in here — otherwise the writer skips the row
for having no `geni:` field and the first edge of every chain is lost.

**The relation words come through as Geni renders them** — *your father*, *his wife*, *her 3rd
great grandson*. `build-tiny-gedcoms.PATH_REL` reads the last word, so *your father* and *his
father* both map to `parent`, and a distance phrase like *3rd great grandson* maps on `grandson`,
which is not in the table and is skipped rather than guessed. That is the existing behaviour and
this script does not second-guess it.
"""
import csv
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAINS = os.path.join(ROOT, "reports", "path-chains.tsv")
HARVEST = os.path.join(ROOT, "reports", "geni-paths-harvest.tsv")
OUT = os.path.join(ROOT, "paths")

SLUG = re.compile(r"[^a-z0-9]+")


def viewer_ids():
    """`from=` on every harvested permalink -- the viewer the chain starts at."""
    seen = {}
    if not os.path.exists(HARVEST):
        return seen
    with io.open(HARVEST, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            m = re.search(r"[?&]from=(\d+)", row.get("permalink") or "")
            t = re.search(r"[?&]to=(\d+)", row.get("permalink") or "")
            if m and t:
                seen[(t.group(1), (row.get("kind") or "").strip())] = m.group(1)
    return seen


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not os.path.exists(CHAINS):
        print("no %s" % CHAINS)
        return 2
    froms = viewer_ids()
    chains = {}
    with io.open(CHAINS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            chains.setdefault((row["to_id"], row["kind"]), []).append(row)

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    written = skipped = 0
    for (to_id, kind), rows in sorted(chains.items()):
        rows.sort(key=lambda r: int(r["step"]))
        if any(r["step"] == "-1" for r in rows) or len(rows) < 2:
            skipped += 1
            continue
        if not rows[0]["profile_id"]:
            rows[0]["profile_id"] = froms.get((to_id, kind), "")
        if not rows[0]["profile_id"]:
            skipped += 1
            continue
        # ⛔ NOT `isolate-geni-`. These are HARVESTED paths, and 224 of the first 294 are
        # not isolates at all -- they are saved paths from the viewer to notable people, off
        # `/paths`. Filing them under the isolate prefix put two populations in one namespace
        # and a `find exports -name "*<id>*"` then reported d'Esneval and Bettencourt as having
        # balls on disk when what it had found was these files. That misread came within one
        # step of deleting two live queue items on 2026-09-13.
        name = "harvested-path-geni-%s-%s" % (to_id, kind.replace("-", ""))
        body = [
            "# Geni relationship path to %s (%s)" % (to_id, kind),
            "#",
            "# READ FROM THE SAVED /paths PERMALINK, not re-requested. Split out of",
            "# reports/path-chains.tsv by scripts/split-path-chains.py.",
            "#",
            "step\tname\trelation_to_previous\tnote",
        ]
        for r in rows:
            if not r["profile_id"]:
                continue
            body.append("%s\t%s\t%s\tgeni:%s"
                        % (int(r["step"]) + 1, r["name"], r["relation"] or "-", r["profile_id"]))
        with io.open(os.path.join(OUT, name + ".tsv"), "w",
                     encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(body) + "\n")
        written += 1
    print("%d chain(s) -> paths/, %d skipped (empty, single-step or no viewer id)"
          % (written, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
