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
import io
import os
import sys

OUT = os.path.join("reports", "path-chains.tsv")
HEADER = ["to_id", "kind", "step", "profile_id", "name", "relation"]


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
    merged = read(OUT)
    before = len(merged)
    chains_before = len({(k[0], k[1]) for k in merged})
    for dump in argv:
        got = read(dump)
        merged.update(got)
        print("%s -> %d rows" % (dump, len(got)))
    order = sorted(merged, key=lambda k: (k[0], k[1], int(k[2])))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(HEADER) + "\n")
        for k in order:
            fh.write("\t".join(merged[k]) + "\n")
    chains = {(k[0], k[1]) for k in merged}
    people = {merged[k][3] for k in merged if merged[k][3]}
    print("%s: %d rows (+%d), %d chains (+%d), %d distinct people"
          % (OUT, len(merged), len(merged) - before,
             len(chains), len(chains) - chains_before, len(people)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
