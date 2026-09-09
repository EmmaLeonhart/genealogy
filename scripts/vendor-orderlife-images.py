"""Vendor only the order.life images the wikibase actually references.

Emma, 2026-08-15: *"I want images used by the wikibase to be preserved but not
ones not used by it."*

`order.life/wikibase/images/` holds 377 files and 217.8 MB, and a good deal of it
is not genealogy at all — `1NF_video_fixing.png`,
`A-Guide-to-the-Cloud-Computing-Pyramid.jpg`. Those are leftovers in the same
directory, not pictures of people.

**Referenced means: named by a `commonsMedia` claim on some item.** order.life
has three such properties, read from its own property definitions rather than
assumed:

- `P58` Historical Image
- `P68` Official portrait
- `P94` coat of arms image

**Emma's guess was right, and the numbers say so rather than the other way
round.** Of the 20 files that survive, **19 are blazons** (`*_Arms.svg`) and one
is a `Historical Image`. The 357 left behind are database-normalisation tutorial
diagrams and cloud-computing charts sharing the directory — `1NF_video_fixing.png`,
`A-Guide-to-the-Cloud-Computing-Pyramid.jpg`.

**The 77,785 filenames named by a claim with no such file are not missing data.**
order.life's `P94` generates a `<name> Arms.svg` filename for every person, so
`Aster_Arms.svg` is referenced 12,855 times and most of the rest point at blazons
nobody ever drew — including empty-named ones like `  Arms.svg`. They are listed
in the CSV rather than counted and dropped.

Reads the vendored shards under `orderlife/items/`, so run
`vendor-orderlife-items.py` first. Copies matches to `orderlife/images/` and
writes `reports/orderlife-images.csv` — **one row per image file on disk**,
referenced or not, so the ones being left behind are listed rather than silently
dropped.

    py scripts/vendor-orderlife-images.py --source <path to order.life/wikibase>
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHARDS = REPO / "orderlife" / "items"
DEST = REPO / "orderlife" / "images"
CSV_OUT = REPO / "reports" / "orderlife-images.csv"

#: order.life's `commonsMedia` properties. Not guessed — these are every property
#: in `orderlife/properties/` whose datatype is `commonsMedia`.
MEDIA_PROPERTIES = {"P58": "Historical Image",
                    "P68": "Official portrait",
                    "P94": "coat of arms image"}


def referenced() -> dict[str, list[tuple[str, str]]]:
    """filename -> [(item qid, property)] for every commonsMedia claim."""
    out: dict[str, list[tuple[str, str]]] = {}
    shards = sorted(SHARDS.glob("items-*.jsonl.gz"))
    if not shards:
        print(f"no shards in {SHARDS}; run vendor-orderlife-items.py first",
              file=sys.stderr)
        raise SystemExit(1)
    for n, path in enumerate(shards, 1):
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                claims = item.get("claims") or {}
                for prop in MEDIA_PROPERTIES:
                    for st in claims.get(prop, []):
                        value = ((st.get("mainsnak") or {})
                                 .get("datavalue", {}).get("value"))
                        if isinstance(value, str) and value:
                            out.setdefault(value, []).append(
                                (item.get("id", ""), prop))
        if n % 40 == 0:
            print(f"  read {n}/{len(shards)} shards, "
                  f"{len(out):,} distinct filenames")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source",
                    default="C:/Users/Emma/Documents/GitHub/order.life/wikibase")
    args = ap.parse_args()

    src = Path(args.source) / "images"
    if not src.is_dir():
        print(f"no such directory: {src}", file=sys.stderr)
        return 1

    refs = referenced()
    print(f"{len(refs):,} distinct filenames referenced by a commonsMedia claim")

    on_disk = {p.name: p for p in src.iterdir() if p.is_file()}
    # Wikibase writes media names with spaces where the file uses underscores.
    lookup = {name.replace("_", " "): p for name, p in on_disk.items()}

    DEST.mkdir(parents=True, exist_ok=True)
    rows, copied, missing = [], 0, 0
    used_files: set[str] = set()

    for name, users in sorted(refs.items()):
        path = on_disk.get(name) or lookup.get(name.replace("_", " "))
        if path is None:
            missing += 1
            rows.append({"file": name, "on_disk": "", "referenced": "yes",
                         "n_items": len(users), "properties": "",
                         "example_item": users[0][0], "action": "named by a claim, no such file"})
            continue
        used_files.add(path.name)
        props = ";".join(sorted({MEDIA_PROPERTIES[p] for _q, p in users}))
        shutil.copy2(path, DEST / path.name)
        copied += 1
        rows.append({"file": path.name, "on_disk": "yes", "referenced": "yes",
                     "n_items": len(users), "properties": props,
                     "example_item": users[0][0], "action": "vendored"})

    for name in sorted(on_disk):
        if name in used_files:
            continue
        rows.append({"file": name, "on_disk": "yes", "referenced": "",
                     "n_items": 0, "properties": "", "example_item": "",
                     "action": "left behind - nothing references it"})

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "on_disk", "referenced",
                                           "n_items", "properties",
                                           "example_item", "action"])
        w.writeheader()
        w.writerows(rows)

    kept = sum(p.stat().st_size for p in DEST.iterdir() if p.is_file())
    total = sum(p.stat().st_size for p in on_disk.values())
    by_prop = Counter(p for users in refs.values() for _q, p in users)
    print(f"\n{len(on_disk):,} image files on disk, {total / 1e6:.1f} MB")
    print(f"  vendored:     {copied:,} files, {kept / 1e6:.1f} MB")
    print(f"  left behind:  {len(on_disk) - copied:,} files, "
          f"{(total - kept) / 1e6:.1f} MB")
    if missing:
        print(f"  named by a claim but no such file: {missing:,}")
        print("    order.life's P94 generates a `<name> Arms.svg` filename per")
        print("    person; almost none of those blazons were ever drawn.")
    for prop, n in by_prop.most_common():
        print(f"  {prop} {MEDIA_PROPERTIES[prop]}: {n:,} claims")
    print(f"\nwrote {CSV_OUT} ({len(rows):,} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
