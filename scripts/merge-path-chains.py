"""Merge the browser's `path-chains-NNN.tsv` dumps into one committed file.

    python scripts/merge-path-chains.py <dump> [<dump> ...]

**What a dump is.** `window.__chains` fetches a saved `/paths` permalink and pulls the chain
straight out of the raw HTML -- one row per step, with the profile id and the relation word
Geni renders in `span.subtext`. It accumulates rows in the page and blob-downloads them, because
javascript_tool cannot carry tens of thousands of rows back through the agent.

**⛔ THE PERMALINK IS NOT A CONSTRUCTED `/path/` URL.** `scripts/build-isolate-path-targets.py`
carries the refutation of the constructed form -- it redirects to Charlemagne and renders his own
chain, so a harvest scoring on step count reads 100% reach made of one path repeated. A permalink
taken off `/paths` is a saved object and returns the real chain. Measured 2026-09-13: 56
segments, ending on exactly the profile id in `to=`.

**Dedupe is on `(to_id, kind, step)` and the LAST dump wins**, matching `CLAUDE.md` § *later
sources win value conflicts*: Geni is live and a re-fetched chain holds the correction.

**Step 0 is the viewer and carries no profile id.** It is kept, because a chain that does not say
where it starts is not a chain. A row whose step is `-1` and whose relation is `EMPTY` records a
permalink that rendered no segments -- kept too, so the absence is bounded rather than silent.
"""
import glob
import io
import os
import re
import sys

HEADER = ["to_id", "kind", "step", "profile_id", "name", "relation"]

#: ⛔ **THE COMMITTED CHAINS ARE SHARDED, AND IT IS NOT A TIDINESS CHOICE.** One
#: `reports/path-chains.tsv` reached **65 MB** on 2026-09-19 and GitHub warned on the push --
#: past the 50 MB advisory, against a 100 MB hard limit -- while the requester's own harvest
#: adds ~5,000 rows per dump. The four big derived CSVs solve this by being gitignored and
#: committed gzipped, which costs every reader a `pack-derived.py --unpack` on a clean clone.
#: Sharding costs readers one glob and keeps the rows in plain text, which is what every reader
#: here actually wants: *"There is a simple solution: path-chains-1.tsv lol"*, ruled 2026-09-19.
#:
#: **A chain is never split across shards.** The boundary is `(to_id, kind)`, so a reader that
#: takes one shard at a time still sees whole chains and `split-path-chains.py` cannot emit a
#: truncated `paths/*.tsv`.
SHARD_ROWS = 150000


def shard_paths():
    """Every `reports/path-chains-N.tsv` on disk, in numeric order."""
    found = glob.glob(os.path.join("reports", "path-chains-*.tsv"))
    return sorted(found, key=lambda p: int(re.search(r"-(\d+)\.tsv$", p).group(1)))


def write_shards(merged, order):
    """Replace the shard set with `order`, breaking only between chains."""
    for stale in shard_paths():
        os.remove(stale)
    part, n, fh = 0, 0, None
    prev_chain = None
    for k in order:
        chain = (k[0], k[1])
        if fh is None or (n >= SHARD_ROWS and chain != prev_chain):
            if fh is not None:
                fh.close()
            part += 1
            n = 0
            fh = io.open(os.path.join("reports", "path-chains-%d.tsv" % part),
                         "w", encoding="utf-8", newline="\n")
            fh.write("\t".join(HEADER) + "\n")
        fh.write("\t".join(merged[k]) + "\n")
        n += 1
        prev_chain = chain
    if fh is not None:
        fh.close()
    return part


def read(path):
    rows = {}
    if not os.path.exists(path):
        return rows
    with io.open(path, encoding="utf-8") as fh:
        first = True
        for line in fh:
            line = line.rstrip("\r\n")
            if not line:
                continue
            if first:
                first = False
                if line.split("\t")[:2] == HEADER[:2]:
                    continue
            parts = line.split("\t")
            while len(parts) < len(HEADER):
                parts.append("")
            rows[(parts[0], parts[1], parts[2])] = parts[:len(HEADER)]
    return rows


def main(argv):
    if not argv:
        print("usage: merge-path-chains.py <dump> [<dump> ...]")
        return 2
    merged = {}
    for shard in shard_paths():
        merged.update(read(shard))
    before = len(merged)
    chains_before = len({(k[0], k[1]) for k in merged})
    for dump in argv:
        got = read(dump)
        merged.update(got)
        print("%s -> %d rows" % (dump, len(got)))
    order = sorted(merged, key=lambda k: (k[0], k[1], int(k[2])))
    parts = write_shards(merged, order)
    chains = {(k[0], k[1]) for k in merged}
    people = {merged[k][3] for k in merged if merged[k][3]}
    print("reports/path-chains-*.tsv: %d shards, %d rows (+%d), %d chains (+%d), %d distinct people"
          % (parts, len(merged), len(merged) - before,
             len(chains), len(chains) - chains_before, len(people)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
