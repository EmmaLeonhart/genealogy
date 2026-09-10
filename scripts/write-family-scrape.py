"""Take a collector family scrape off stdin as JSON and write it into the repo.

**Only the exports need downloading; everything else is written into files in the repo.**
This is the write-it-into-the-repo half. The collector returns
the scrape on a data attribute; this puts it where it belongs and updates the isolate ledger in
the same pass, so the two cannot drift.

It writes three things per person:

  `geni-families/<geni id>-family.tsv`   step 1 of `docs/per-individual-loop.md`
  a row in `reports/isolates.csv`        the numbers are stored before a path is found or
                                         not, and the page is stayed on to request the path
  `last_attempted` in the worklist       `reports/unconnected-p2600.tsv`, piece 6 of
                                         `docs/unconnected-worklist.md` — see `attempt_ledger.py`

**`path_found` is THREE-VALUED and the blank is load-bearing.** `yes` / `no` / empty-while-running.
A pending search folded into the miss column is the failure `geni-paths/README.md` § *THE SEARCH
IS ASYNCHRONOUS* records: nine targets read as *"0 steps"* when they had simply not finished.

**A MISSING STATISTICS ROW IS ZERO.** Dorothy Jeakins is the worked case: Geni does not offer
zero as a value there. The collector already reads it that way; nothing here turns a zero back
into a blank.

⛔ **`path_found` MEANS *ANY* PATH. IN-LAW COUNTS.** In-law connections are just as valid; blood
is not required.

**AND EVERY `no` WRITTEN BEFORE EXTENSION 1.6.3 MEANS *NO BLOOD PATH* AND NOTHING MORE.** The
collector only ever dispatched `runPath` with `kind: "blood"`; Geni offers a second search behind
a *Show Me* button that nothing clicked, so those rows record an answer to a narrower question
than the column is read as asking. They are not final and must not be totalled as if they were.

`via` says which search answered, and **blank means unrecorded rather than blood** -- the 80 rows
that predate this column were written when only one question was ever asked, and back-filling
them with `blood` would assert that the other one had been tried. Anna Hørlück
`297536201290008921` is the one checked by hand: *"No in-law relationship was found."* as well.
"""

from __future__ import annotations

import csv
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"
ISOLATES = ROOT / "reports" / "isolates.csv"

FIELDS = ["family_tree", "blood_relatives", "ancestors", "descendants", "followers"]

#: Which profile Geni's relationship search is anchored on RIGHT NOW. Set on Charlemagne
#: 2026-09-06 via `docs/anchor-protocol.md`; everything captured before that is `viewer`. If the
#: anchor is ever moved, this moves with it -- a row written under the wrong label is worse than
#: no label, because it is silently counted in the wrong reach rate.
#: ⛔ **NO PIN. PATHS GO TO WHOEVER GENI DEFAULTS TO.** Ruled 2026-09-10: *"We are not centering
#: the paths on Charlemagne anymore ... We just request paths to whoever it defaults to."*
#:
#: The pin protocol is retired with it: `docs/anchor-protocol.md`'s check-set-verify, the
#: two-click re-pin from a third person, and the per-capture rule that step 1 of a resolved chain
#: must read `geni:6000000002457013227` or the capture answers a different question. None of that
#: applies to a run that asks for the default and records what comes back.
#:
#: Rows already reading `charlemagne` or `viewer` were taken while a pin was live and keep their
#: own value -- the anchor belongs to the observation that made it, which is why it was preserved
#: across revisits in the first place. `@ANCHOR` overrides where a caller knows better.
ANCHOR = "default"

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
    # ⛔ `read` IS NOT ALWAYS TRUE, AND HARD-CODING IT MANUFACTURES FIVE ZEROS.
    #
    # `GC.statistics` returns `{read: false}` and NOTHING ELSE when the block never rendered,
    # which is the whole point of that flag: a row missing from a block that IS present is a
    # real zero, and a block that never appeared is not data at all. This function asserted
    # `read: True` unconditionally, so a scrape of a profile with no statistics block arrived
    # as `family_tree=0 ... followers=0  read=1` -- five fabricated measurements, indexed in
    # `reports/isolates.csv`, indistinguishable from a person who genuinely has none.
    #
    # Found 2026-09-06 on Jan Luis Castellanos `6000000145513239986`: a real profile, no
    # CAPTCHA, no statistics block, `family tree` followed by no digit anywhere on the page.
    # `@READ` carries the flag across; absent, it defaults true, which is what every block
    # written before today meant.
    stats = {"read": (meta.get("read", "1").strip() != "0")}
    raw = meta.get("stats", "")
    if "=" in raw:
        for pair in raw.split("	"):
            k, _, v = pair.partition("=")
            if k:
                stats[k] = int(v or 0)
    elif not raw.strip():
        # ⛔ AN EMPTY `@STATS` PARSES TO ONE ZERO, NOT TO NOTHING. `"".split("	")` is `[""]`,
        # so the positional zip below sets `family_tree=0` and leaves the other four absent --
        # a single fabricated figure on a person whose block never rendered, which is the exact
        # thing `read` exists to prevent. Caught 2026-09-06 by reading the file that was written
        # rather than the summary line, which said the right thing either way.
        pass
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
        "path": meta.get("path", ""),
        "via": meta.get("via", ""),
        "anchor": meta.get("anchor", ""),
    }


def read_stdin() -> str:
    """⛔ READ STDIN AS UTF-8 EXPLICITLY. `sys.stdin.read()` is the mojibake bug in a new place.

    On Windows `sys.stdin` decodes with the LOCALE encoding -- cp1252 here -- so a scrape piped
    in as UTF-8 arrives already wrong and is written back out as UTF-8, double-encoded.
    Measured 2026-09-09 on Ellen Margrethe Charlotte Jessen: `Børge` became `BÃ¸rge` and
    `Kröncke` became `KrÃ¶ncke`, in a file whose whole job is to preserve what Geni said.

    This is the same failure `queue.md` warns about for shell heredocs --- *"it double-encodes
    UTF-8 and silently destroyed 4 of 14 scrapes"* --- so the warning was right about the shape
    and wrong about the cause being the shell. Anything that decodes by locale does it, and this
    script was the one thing the loop is supposed to pipe a scrape THROUGH.

    Nothing on disk was damaged by it: every family file written before today came from a file
    tool rather than this pipe, so `geni-families/` had no mojibake in it when this was found.
    """
    buf = getattr(sys.stdin, "buffer", None)
    if buf is not None:
        return buf.read().decode("utf-8")
    return sys.stdin.read()


def main() -> int:
    # ⛔ THE FINAL `print` DIES ON A CJK NAME UNDER cp1252, AFTER THE FILES ARE WRITTEN.
    # Windows gives stdout the locale codepage, so `Zhu Jingze 朱敬則` raises
    # `UnicodeEncodeError` on the summary line — with the family file and the isolates row
    # already on disk. A traceback that arrives AFTER the work succeeded reads as a failed
    # capture and invites a re-run. Measured 2026-09-09 on the first CJK person off the
    # 266,201-row worklist; that population is full of them.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raw = read_stdin()
    blob = json.loads(raw) if raw.lstrip().startswith("{") else parse_block(raw)
    ext, relatives = blob["ext"], blob["relatives"]
    gid, name = ext["geni_id"], ext.get("name", "")
    stats = ext.get("stats", {})

    head = [
        "# Immediate family scraped from the Geni profile page. Step 1 of the per-individual loop.",
        "# subject\t%s\t%s" % (gid, name),
        "# prose\t%s" % blob.get("prose", "")[:400],
        # ⛔ How many relatives the prose NAMES but the block does not LINK.
        #
        # "and N others" reads like an expander and is not one. Measured 2026-09-06 on Julius
        # Hohenberger and on Arne Garborg: clicking it adds no anchor, a real MouseEvent adds no
        # anchor, and `<< less` is already displayed on both -- the list is expanded and those
        # people simply carry no `href`, which is what a redacted profile looks like in this
        # block. So the shortfall is a limit of the source, not a defect to fix.
        #
        # It is recorded because a row count would otherwise imply completeness: Arne's scrape
        # holds 12 rows and names 15 relatives. `GC.family.unlinked` computes the same sum on the
        # collector's side, so both writers of this file agree.
        "# unlinked\t%d\trelatives the prose names that carry no link, and that no click reveals"
        % sum(int(n) for n in re.findall(r"and (\d+) others?", blob.get("prose", ""))),
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
    if "via" not in header:
        header = header + ["via"]
    # ⛔ WHETHER AN EXPORT WAS RUN ON THIS PERSON, and it is a gap the ledger had from the start.
    #
    # Ruled 2026-09-10: *"The tsv file should save all of the statistics on the people and have a
    # thing for whether a gedcom export was done on them."* The statistics were already here; the
    # export was not, so nothing on disk distinguished a person the gate demanded an export from
    # and got one, from a person it demanded an export from and never got. Over a 266,201-person
    # campaign that is the difference between a backlog and a silence.
    #
    # Three values. `warranted` is written here, by the gate, on every capture that clears the
    # floor -- so the backlog is a column query rather than a reconstruction. `done` is written
    # when the export lands and is filed. Blank means the gate did not ask.
    if "exported" not in header:
        header = header + ["exported"]
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
    # ⛔ A HIT CANNOT COME FROM THE BANNER, AND THE COLLECTOR IS THE ONLY THING THAT KNOWS ONE.
    #
    # `path_state` is asymmetric on purpose: a miss is stated on the page in words, a hit is
    # not. Its own docstring says what does establish one -- *"a parsed chain whose steps
    # include the target, which is what the `path` job's `state == \"resolved_path\"` with
    # `hasTarget` establishes"* -- and nothing carried that verdict here, so a confirmed hit
    # arrived with an empty banner and was written as PENDING.
    #
    # Measured 2026-09-06: Viktor Georg Frhr. von Wolff `6000000040539833345` and Louise von
    # Renngarten `6000000029392019410` both came back `resolved_path` with the target in the
    # chain, both carrying a 32-step and a 64-step Charlemagne descent, and both landed in the
    # ledger as pending. A hit recorded as pending is the mirror of the failure the asymmetry
    # exists against: it deflates the reach rate instead of inflating it, and it queues a
    # revisit for a person whose chain is already on disk.
    #
    # `@PATH` carries the job's verdict and ONLY the job may set it to `yes`. Absent, the
    # banner decides exactly as before, so every block written before today is unaffected.
    declared = (blob.get("path") or "").strip().lower()
    fresh = declared if declared in ("yes", "no") else path_state(blob.get("banner", ""))
    verdict = fresh if fresh else prior
    if prior == "yes" and fresh == "no":
        verdict = "yes"   # a chain we hold is evidence; today's miss banner does not retract it
    # ⛔ A VERDICT IS MEANINGLESS WITHOUT THE ANCHOR IT WAS TAKEN UNDER.
    #
    # With the pushpin on the viewer a capture answers *how is this person related to the
    # account owner*; on Charlemagne, *how is this person related to Charlemagne*. Same page,
    # same wording, different
    # question — and the pilot's deliverable is a reach rate to Charlemagne, so mixing the two
    # produces a number that answers neither. `docs/anchor-protocol.md`.
    #
    # The anchor moved to Charlemagne on 2026-09-06 and every row taken before it is marked
    # `viewer`. A row carries the anchor that was live when its VERDICT was observed, so a
    # preserved verdict keeps its own anchor rather than inheriting today's.
    prior_anchor = next((r[9] for r in rows[1:] if r and r[0] == gid and len(r) > 9), "")
    anchor = prior_anchor if (verdict and verdict == prior and prior_anchor) else (
        (blob.get("anchor") or ANCHOR) if verdict else "")
    # ⛔ A BLOCK THAT NEVER RENDERED IS BLANK HERE, NOT ZERO.
    #
    # The rule is that a row MISSING FROM A PRESENT BLOCK is a real zero, because Geni does
    # not offer zero as a value there -- and that is unchanged. A block that never appeared
    # at all is the other thing, and writing it as five zeros makes an unmeasured person
    # indistinguishable from a person who genuinely has nobody. The ledger has no `read`
    # column, so blank is how it says *not measured*, exactly as it already does for
    # `path_found`.
    read = stats.get("read", True)
    figures = [(str(stats.get(f, 0) or 0) if read else "") for f in FIELDS]
    # ⛔ WHICH SEARCH ANSWERED. Blank means UNRECORDED, never "blood".
    #
    # `path_found` is now *any* path -- ruled 2026-09-07 -- so a bare `yes`/`no` no longer
    # says which question Geni was asked. `via` says it. A revisit preserves a recorded `via` for
    # the same reason `anchor` is preserved: the observation belongs to the run that made it, and
    # a later pass that asked a different question must not relabel it.
    prior_via = next((r[10] for r in rows[1:] if r and r[0] == gid and len(r) > 10), "")
    via = (blob.get("via") or "").strip().lower()
    # ⛔ ALL FOUR ARE VERDICTS. The first version listed only `blood` and `inlaw`, so `neither`
    # -- the one that says BOTH searches ran and both missed -- was silently discarded, and
    # `collector-worklist.py` would have re-queued that person forever. Caught on Anna Hørlück
    # `297536201290008921`, the first person the two-search loop ever finished.
    if via not in ("blood", "inlaw", "both", "neither"):
        via = prior_via if (verdict and verdict == prior) else ""
    # ⛔ `requested_at` WAS A LITERAL, so every row ever written claimed to have been observed on
    # 2026-09-06 whatever day it was written. 103 of the file's rows carry that date and three of
    # them were written on 2026-09-08. A column whose whole job is to say *when we asked* cannot
    # be a constant: it makes a fresh observation indistinguishable from a two-day-old one, which
    # is the stale-photograph failure `CLAUDE.md` records against downloaded items and derived
    # tables. Rows already carrying the literal are left alone -- back-dating them to today would
    # assert the opposite error.
    # The gate's verdict, so the row itself says whether an export is owed. A row that already
    # reads `done` is never downgraded by a revisit, for the same reason a recorded path verdict
    # is not: the export happened, and today's gate reading does not un-happen it.
    prior_exported = next((r[11] for r in rows[1:] if r and r[0] == gid and len(r) > 11), "")
    sys.path.insert(0, str(ROOT / "scripts"))
    from export_gate import decide as _decide
    exported = "done" if prior_exported == "done" else (
        "warranted" if _decide(stats).get("export") else prior_exported)
    body.append([gid, name] + figures
                + [datetime.date.today().isoformat(), verdict, anchor, via, exported])
    body.sort(key=lambda r: r[0])
    with ISOLATES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(body)

    sys.path.insert(0, str(ROOT / "scripts"))
    from export_gate import decide
    d = decide(stats)

    # ⛔ THE ATTEMPT IS STAMPED HERE BECAUSE NOTHING ELSE CAN STAMP IT.
    #
    # `docs/unconnected-worklist.md` § 5 wants `last_attempted` written "by the extension,
    # automatically, every time it runs on somebody" — and the extension cannot write into the
    # repo at all (`queue.md` § *Nothing downloads*). This script is the one thing that runs
    # exactly once per person the collector runs on, so this is where *every time* lives.
    #
    # An attempt is RUNNING ON SOMEBODY, not succeeding: a failure costs one attempt and 30 days,
    # and a hit leaves the file at the next build because membership is recalculated. A Geni id
    # the worklist holds no row for is reported, never invented — `scripts/attempt_ledger.py`.
    from attempt_ledger import describe, stamp
    today = datetime.date.today()
    attempt = stamp([gid], today=today)
    # Print the verdict that was WRITTEN, not the one today's banner suggested. The first
    # version printed `fresh`, so a revisit that correctly preserved a recorded `no` announced
    # `pending` -- a summary contradicting the file it had just written, which is the shape of
    # every instrument failure in `CLAUDE.md`. `kept` says so explicitly rather than hiding it.
    kept = "" if fresh or not verdict else "  (kept, today's page shows no request)"
    print("%s  %s | %d relatives | path=%r%s | %s" % (
        gid, name, len(relatives), verdict or "pending", kept,
        ("EXPORT if it misses: " + d["why"]) if d["export"] else ("NO EXPORT: " + d["why"])))
    print("  worklist: %s" % describe(attempt, today.isoformat()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
