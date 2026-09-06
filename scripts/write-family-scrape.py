"""Take a collector family scrape off stdin as JSON and write it into the repo.

**Emma, 2026-09-06:** *"Only the exports need downloading because you write stuff into files in
the repo you dummy."* This is the "write it into files in the repo" half. The collector returns
the scrape on a data attribute; this puts it where it belongs and updates the isolate ledger in
the same pass, so the two cannot drift.

It writes two things per person:

  `geni-families/<geni id>-family.tsv`   step 1 of `docs/per-individual-loop.md`
  a row in `reports/isolates.csv`        her instruction, 2026-09-03: *"you store these numbers
                                         even before a path is found or not, but you always stay
                                         on the page and request the path"*

**`path_found` is THREE-VALUED and the blank is load-bearing.** `yes` / `no` / empty-while-running.
A pending search folded into the miss column is the failure `geni-paths/README.md` § *THE SEARCH
IS ASYNCHRONOUS* records: nine targets read as *"0 steps"* when they had simply not finished.

**A MISSING STATISTICS ROW IS ZERO** -- Emma, 2026-09-03 on Dorothy Jeakins: *"geni is weird and
gives zero as not an option there"*. The collector already reads it that way; nothing here turns
a zero back into a blank.
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"
ISOLATES = ROOT / "reports" / "isolates.csv"

FIELDS = ["family_tree", "blood_relatives", "ancestors", "descendants", "followers"]

#: ⛔ THE BANNER CAN ONLY EVER PROVE A MISS. It cannot prove a hit, and the first version of this
#: function claimed otherwise: anything that was neither the pending sentence nor the miss
#: sentence fell through to `"yes"`.
#:
#: **That is FOUR states collapsed into three, and the fourth is the dangerous one.**
#: `geni-paths/README.md` records three — hit, miss, pending — and a fourth exists that the
#: harvester already names, `not_requested()`: the profile shows a **"How are you related?"**
#: button because no search has ever been asked for. Asser de Haan came back exactly that way and
#: was written down as `path_found=yes`, a connected hit on a search nobody had run.
#:
#: The pilot's entire deliverable is a reach rate, so a not-requested profile scored as a hit
#: inflates the one number the campaign produces — the same failure as the `/path/` URL, which
#: rendered the viewer's own chain and would have reported 100%.
#:
#: **So the mapping is asymmetric on purpose.** A miss is stated on the page in words and is
#: readable here. A HIT is not: it needs a parsed chain whose steps include the target, which is
#: what the `path` job's `state == "resolved_path"` with `hasTarget` establishes. Anything this
#: function does not positively recognise stays **blank** — come back later — because blank costs
#: a revisit and `yes` costs the measurement.
def path_state(banner: str) -> str:
    b = (banner or "").lower()
    if "no path found" in b or "could not be found" in b or "no blood relationship" in b:
        return "no"
    return ""   # pending, not-requested, or unrecognised -- never inferred as a hit


def parse_block(text: str) -> dict:
    """The collector's compact form: `@`-prefixed metadata lines, then one line per relative.

    JSON was the first shape and it does not survive the trip: a person with eight relatives
    overflows the tool-result limit and the last of them is silently truncated mid-object, which
    is the same absent-versus-narrowed failure as everything else in `CLAUDE.md` -- the answer
    still parses and is short by one person. Tab-separated lines are compact enough that a large
    family fits, and a truncated line is visibly a truncated line.
    """
    meta, rows = {}, []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("@"):
            key, _, rest = line.partition("	")
            meta[key[1:].lower()] = rest
            continue
        parts = line.split("	")
        if len(parts) == 4:
            rows.append(dict(zip(("relation", "phrase", "geni_id", "name"), parts)))
    stats = {"read": True}
    raw = meta.get("stats", "")
    if "=" in raw:
        for pair in raw.split("	"):
            k, _, v = pair.partition("=")
            if k:
                stats[k] = int(v or 0)
    else:
        # POSITIONAL, in the order Geni prints the block. The `key=value` form is still accepted
        # and is the readable one, but it cannot always be carried: the browser tool blocks a
        # result line containing `k=v` as query-string data, so a scrape transported that way
        # arrives empty. Positional survives the trip; `FIELDS` is the single definition of the
        # order and both forms land in the same dict.
        for field, value in zip(FIELDS, raw.split("	")):
            stats[field] = int(value or 0)
    return {
        "ext": {"geni_id": meta.get("id", ""), "name": meta.get("name", ""), "stats": stats},
        "relatives": rows,
        "prose": meta.get("prose", ""),
        "banner": meta.get("banner", ""),
    }


def main() -> int:
    raw = sys.stdin.read()
    blob = json.loads(raw) if raw.lstrip().startswith("{") else parse_block(raw)
    ext, relatives = blob["ext"], blob["relatives"]
    gid, name = ext["geni_id"], ext.get("name", "")
    stats = ext.get("stats", {})

    head = [
        "# Immediate family scraped from the Geni profile page. Step 1 of the per-individual loop.",
        "# subject\t%s\t%s" % (gid, name),
        "# prose\t%s" % blob.get("prose", "")[:400],
        "# statistics\t" + "\t".join(
            "%s=%s" % (f, "" if stats.get(f) is None else stats[f]) for f in FIELDS)
        + "\tread=%s" % ("1" if stats.get("read") else "0"),
        "\t".join(["subject_geni_id", "relation", "phrase", "relative_geni_id", "relative_name"]),
    ]
    for r in relatives:
        head.append("\t".join([gid, r["relation"], r["phrase"], r["geni_id"], r["name"]]))
    FAMILIES.mkdir(exist_ok=True)
    (FAMILIES / ("%s-family.tsv" % gid)).write_text("\n".join(head) + "\n", encoding="utf-8")

    rows = list(csv.reader(ISOLATES.open(encoding="utf-8")))
    header = rows[0]
    prior = next((r[8] for r in rows[1:] if r and r[0] == gid and len(r) > 8), "")
    body = [r for r in rows[1:] if r and r[0] != gid]

    # ⛔ A RECORDED VERDICT IS NEVER DOWNGRADED TO BLANK BY A REVISIT.
    #
    # A requested search DECAYS: Rudolf Beck read "Path search in progress" and two hours later
    # showed the "How are you related?" button again, and Hilde Kann's 2026-09-03 miss reads as
    # not-requested today. So a pass-two revisit sees a blank state on a person whose answer was
    # already observed -- and a wholesale row rewrite would erase it. Over a 185,327-target
    # campaign that is silent, cumulative data loss: every verdict quietly reverting to pending
    # as the campaign revisits, and the reach rate falling towards zero for a reason nothing
    # records.
    #
    # `no` and `yes` are OBSERVATIONS; blank is *we have not seen an answer yet*. An observation
    # is only ever replaced by a stronger one -- a chain found where a miss was recorded, which
    # is real news about a live site. Nothing here ever writes blank over a verdict.
    fresh = path_state(blob.get("banner", ""))
    verdict = fresh if fresh else prior
    if prior == "yes" and fresh == "no":
        verdict = "yes"   # a chain we hold is evidence; today's miss banner does not retract it
    body.append([gid, name] + [str(stats.get(f, 0) or 0) for f in FIELDS]
                + ["2026-09-06", verdict])
    body.sort(key=lambda r: r[0])
    with ISOLATES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(body)

    sys.path.insert(0, str(ROOT / "scripts"))
    from export_gate import decide
    d = decide(stats)
    # Print the verdict that was WRITTEN, not the one today's banner suggested. The first
    # version printed `fresh`, so a revisit that correctly preserved a recorded `no` announced
    # `pending` -- a summary contradicting the file it had just written, which is the shape of
    # every instrument failure in `CLAUDE.md`. `kept` says so explicitly rather than hiding it.
    kept = "" if fresh or not verdict else "  (kept, today's page shows no request)"
    print("%s  %s | %d relatives | path=%r%s | %s" % (
        gid, name, len(relatives), verdict or "pending", kept,
        ("EXPORT if it misses: " + d["why"]) if d["export"] else ("NO EXPORT: " + d["why"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
