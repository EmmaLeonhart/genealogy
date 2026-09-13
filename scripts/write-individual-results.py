"""Write the collector's `individual`-job results into the repo.

    python scripts/write-individual-results.py < results.json

**The extension already does the whole loop and the repo could not read the answer.**
`geni-extension/content/individual.js` runs `docs/collector-run-loop.md` end to end — family
scrape, blood path, in-law path, statistics gate — and returns a result carrying `family_tsv`
and `family_filename` ready to write. Nothing in `scripts/` consumed either: `family_filename`
appears in the extension and **nowhere else in the repository**. `CLAUDE.md` § *Code that is
WRITTEN but never CALLED is not done*, from the other side — the caller was the missing half.

`scripts/write-family-scrape.py` is the writer for the OTHER shape, the raw
`{"ext": …, "relatives": […]}` block a hand-driven family scrape returns. It renders the TSV
itself and cannot take one already rendered, so it is not this and is left alone.

## What it writes, per person, and it is the same three things

    geni-families/<geni id>-family.tsv   the TSV the extension rendered
    a row in reports/isolates.csv        the statistics, the verdict, the anchor, and `via`
    last_attempted in the worklist       via attempt_ledger.stamp -- one call for the batch

## ⛔ `via` IS THE RECORD OF WHICH SEARCH ANSWERED, AND BOTH ARE ALWAYS RUN

`CLAUDE.md` § *BOTH TIES, ALWAYS*. The result carries `path_state` and `inlaw_state`
independently, so `via` is derived from the two rather than assumed: `blood`, `inlaw`, `both`, or
`neither` when both resolved with nothing. **A search still running writes an EMPTY verdict**,
never `no` — `write-family-scrape.py`'s § *`path_found` is THREE-VALUED and the blank is
load-bearing* is the same rule and the same failure it was written against.

## ⛔ A ROW IS REPLACED IN PLACE, AND A `yes` IS NEVER RETRACTED

Re-running a person overwrites their row rather than appending a second one. The one asymmetry is
the one already in the ledger: a chain we hold is evidence, and today's miss does not withdraw it,
so a prior `yes` survives a fresh `no` — and it keeps the anchor it was observed under.

Input is a JSON array of result objects, or a single object. Escaped `\\uXXXX` is fine and is the
safe way to get it out of the browser: `CLAUDE.md` § *Never retype a scrape through a shell
heredoc. It double-encodes UTF-8*.
"""

from __future__ import annotations

import csv
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import attempt_ledger  # noqa: E402

FAMILIES = ROOT / "geni-families"
ISOLATES = ROOT / "reports" / "isolates.csv"

#: The anchor every verdict here is taken under — `docs/anchor-protocol.md`. Charlemagne, by
#: Geni id, and NOT the viewer's profile.
ANCHOR = "6000000002457013227"

HEADER = ["geni_id", "label", "family_tree", "blood_relatives", "ancestors", "descendants",
          "followers", "requested_at", "path_found", "anchor", "via", "exported"]

#: The states a search reports. Anything else means it is still running, and a running search
#: writes a BLANK verdict rather than a miss.
FOUND = "resolved_path"
NONE = "resolved_none"


def verdict_and_via(result):
    """`(path_found, via)` from the two searches, read independently."""
    blood, inlaw = result.get("path_state", ""), result.get("inlaw_state", "")
    hits = [name for name, state in (("blood", blood), ("inlaw", inlaw)) if state == FOUND]
    if hits:
        return "yes", "both" if len(hits) == 2 else hits[0]
    if blood == NONE and inlaw == NONE:
        return "no", "neither"
    return "", ""          # at least one search had not finished: not an answer


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    blob = json.loads(sys.stdin.read())
    results = blob if isinstance(blob, list) else [blob]
    results = [r for r in results if r.get("job") == "individual" and r.get("geni_id")]
    if not results:
        print("no individual results on stdin")
        return 0

    FAMILIES.mkdir(exist_ok=True)
    rows = list(csv.reader(ISOLATES.open(encoding="utf-8"))) if ISOLATES.exists() else [HEADER]
    by_id = {r[0]: r for r in rows[1:] if r}
    today = datetime.date.today().isoformat()
    wrote_family = 0

    for result in results:
        gid = str(result["geni_id"])
        tsv = result.get("family_tsv") or ""
        if tsv:
            name = result.get("family_filename") or ("%s-family.tsv" % gid)
            (FAMILIES / name).write_text(tsv, encoding="utf-8", newline="\n")
            wrote_family += 1

        stats = result.get("stats") or {}
        read = stats.get("read")
        # A block that never rendered is BLANK, not zero -- the rule write-family-scrape.py
        # carries. A row missing from a block that DID render is a real zero.
        def figure(key):
            return "" if read is False else str(stats.get(key, 0))

        found, via = verdict_and_via(result)
        prior = by_id.get(gid)
        if prior and len(prior) > 8 and prior[8] == "yes" and found == "no":
            found, via = "yes", (prior[10] if len(prior) > 10 else via)
            anchor = prior[9] if len(prior) > 9 else ANCHOR
        else:
            anchor = ANCHOR if found else ""
        by_id[gid] = [gid, result.get("name", ""), figure("family_tree"),
                      figure("blood_relatives"), figure("ancestors"), figure("descendants"),
                      figure("followers"), today, found, anchor, via,
                      "yes" if result.get("export_decision", "").startswith("export") else ""]

    with ISOLATES.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        for gid in sorted(by_id):
            writer.writerow(by_id[gid])

    stamped = attempt_ledger.stamp([r["geni_id"] for r in results])
    tally = {}
    for r in results:
        tally[r.get("state", "?")] = tally.get(r.get("state", "?"), 0) + 1
    print("wrote %d family file(s), %d isolate row(s), stamped %d"
          % (wrote_family, len(results), stamped["stamped"]))
    print("  " + ", ".join("%s %d" % kv for kv in sorted(tally.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
