"""Find the Scandinavian patronymics in whatever the sweep has collected so far.

Ruled 2026-09-19: *"the Scandinavian people are the only ones I actually care about here ...
drop these French people ... move on to the Scandinavian people, since they're the people
that matter."*

The root's OWN descendant list yielded exactly two real patronymics and both are childless,
so the Scandinavians have to come from a level down -- the descendants-of-descendants that
`scripts/list-sweep.js` is writing one file per person. This reads those files and pulls the
hits out, newest rows first, so the sweep can be re-pointed at them.

Matching is `build_list_worklist.is_patronymic`, imported rather than copied: it already
knows that a `-sson` after a particle is a French place and that a hyphenated compound is one
token, and a second copy of that rule would drift.
"""

from __future__ import annotations

import glob
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_mod = __import__("build-list-worklist".replace("-", "_")) if False else None

# The builder's filename has hyphens, so it cannot be imported by name.
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "wl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-list-worklist.py"))
wl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wl)


def main() -> int:
    pattern = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/Downloads/sweep-descendants-*.tsv")
    dst = sys.argv[2] if len(sys.argv) > 2 else "reports/sweep-patronymics.tsv"
    files = sorted(glob.glob(pattern))
    hits, seen, rows_read = [], set(), 0
    for path in files:
        focus = os.path.basename(path).replace("sweep-descendants-", "").replace(".tsv", "")
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            fh.readline()
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) < 9:
                    continue
                rows_read += 1
                gid, name, hrefs = f[1], f[7], f[8]
                if not gid or gid in seen:
                    continue
                if wl.is_patronymic(name):
                    seen.add(gid)
                    hits.append((gid, name, focus, hrefs.split(" | ")[0] if hrefs else ""))
    with io.open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write("geni_id\tname\tfound_under\thref\n")
        for h in hits:
            fh.write("\t".join(h) + "\n")
    print("%d files, %d rows read, %d patronymic hits -> %s"
          % (len(files), rows_read, len(hits), dst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
