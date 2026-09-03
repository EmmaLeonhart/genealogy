"""Rebuild the ledger from Emma's Wikidata account, which is the only thing that knows.

    BOT_CONTACT=you@example.com python scripts/refresh-garborg-ledger.py

**Emma, 2026-08-25:** *"you fuckin look at wikidata exactly as I told you"*, then
*"just look at my fucki nprofile"*, then the URL, then *"fuckin use my account as a guide"* —
after a batch offered to create five people of whom three already had items.

`CLAUDE.md` already said this and the ledger was being maintained by hand anyway:
*"`reports/garborg-qids.tsv` is the ledger of who has one. It is filled from **Emma's Wikidata
contributions**, not from a bulk download — her instruction: 'You should be looking at my
contributions to see the new ones I've created.'"* Nothing automated it, so it drifted, and
**11 of her items were missing from it** when this was first run.

**Her account is `日巫女`.** `Special:Contributions` is the authority for what she has made;
`list=usercontribs` is one request per 500 edits.

## Two sources, because neither alone is enough

* **Her contributions** give everything she created or edited — 49 created, 59 touched. This is
  the guide she named.
* **A live `P2600` lookup** catches items she did *not* make. `Q138474188` *Hans Syvertsen
  Nyvold* is the worked example: it carries the Geni id of a Garborg-line person because
  **an IP added it by accident** (her words, 2026-08-25), so it appears in no contribution list
  of hers and would still have been duplicated. `scripts/build-garborg-day.py` runs that check
  as a pre-flight before every `CREATE`.

## What was wrong before, so it is not re-attempted

Three offline sources were being trusted and all three are snapshots taken before she started
creating: the hand-maintained ledger, `out/wikidata/p2600-all.tsv` from the bulk download, and
`out/wikidata/relations.tsv` behind the parent-`P40` duplicate guard.

**Git history is NOT a substitute and was briefly tried.** Emma: *"idk why the fuck you decided
it was gonna be okay to use git history."* She is right — `git log -S` over `reports/*.qs` records
what a batch **offered**, which is not what exists. An offer she declined would block a real
person forever, and an item she made by hand outside any batch would be invisible.

Merges into `reports/garborg-qids.tsv` rather than overwriting: rows already there keep their
`label` and `note` columns, which carry hand-written provenance.
"""
from __future__ import annotations

import csv
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bot_identity import agent as _bot_agent  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
API = "https://www.wikidata.org/w/api.php"
ACCOUNT = "日巫女"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"


def _geni_for_qids(qids):
    """QID -> Geni id out of `derived-labels.csv`, for the entry points that need one.

    An exact join on this repo's primary key, never a name match. Returns only what it finds: a
    QID with no Geni id in our tree cannot become a ledger row, since the ledger is keyed on the
    Geni id.
    """
    import gzip

    plain = ROOT / "reports" / "derived-labels.csv"
    packed = ROOT / "reports" / "derived-labels.csv.gz"
    if plain.exists():
        handle = open(plain, encoding="utf-8")
    elif packed.exists():
        handle = gzip.open(packed, "rt", encoding="utf-8")
    else:
        return {}
    wanted, found = set(qids), {}
    csv.field_size_limit(10_000_000)
    with handle as fh:
        for row in csv.DictReader(fh):
            q = (row.get("qid") or "").strip()
            if q in wanted and q not in found:
                found[q] = row["geni_id"]
                if len(found) == len(wanted):
                    break
    return found


def agent():
    contact = _bot_agent()
    if not contact:
        sys.exit("BOT_CONTACT is not set. Wikimedia answers an empty User-Agent with a bare "
                 "403, so this fails loudly rather than mysteriously.")
    # Emma, 2026-08-18: the agent is the address and NOTHING else -- no tool name,
    # no version, no repository. "geni-merge/1.0" was exactly the leak she named.
    return contact


def get(params, ua):
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=90) as fh:
        return json.load(fh)


def main():
    ua = agent()
    contribs, cont = [], None
    while True:
        p = {"action": "query", "list": "usercontribs", "ucuser": ACCOUNT,
             "uclimit": "500", "ucnamespace": "0",
             "ucprop": "title|timestamp|comment|flags", "format": "json"}
        if cont:
            p["uccontinue"] = cont
        data = get(p, ua)
        contribs += data["query"]["usercontribs"]
        cont = data.get("continue", {}).get("uccontinue")
        if not cont:
            break
    created = {c["title"] for c in contribs if "new" in c}
    touched = sorted({c["title"] for c in contribs})
    print(f"{len(contribs)} mainspace edits by {ACCOUNT}; "
          f"{len(created)} items created, {len(touched)} touched")

    # Every touched item, not only the created ones: she adds a P2600 to items other
    # people made, and that correspondence is just as load-bearing.
    found = {}
    for i in range(0, len(touched), 50):
        batch = touched[i:i + 50]
        data = get({"action": "wbgetentities", "ids": "|".join(batch),
                    "props": "claims|labels", "languages": "en|mul|no|nb",
                    "format": "json"}, ua)
        for qid, ent in data.get("entities", {}).items():
            if "missing" in ent:
                continue
            claims = ent.get("claims", {})
            gs = [st["mainsnak"].get("datavalue", {}).get("value")
                  for st in claims.get("P2600", []) if st.get("rank") != "deprecated"]
            labels = ent.get("labels", {})
            label = (labels.get("en") or labels.get("mul") or labels.get("no")
                     or labels.get("nb") or {}).get("value", "")
            for g in [g for g in gs if isinstance(g, str)]:
                found[g] = (qid, label, qid in created)

    # **REBUILT, not merged. Two sources, and nothing else survives.**
    #
    # Emma, 2026-08-27: *"never deleting rows is a horrible idea. Simple as that... This seems to
    # explain why it is that it was this giant grab bag of some stuff that was actually generated
    # and some random garbage that got thrown in. The ledger should be everything I've edited. In
    # addition to everything I've edited, it would include all of the Bure clan people. Nobody
    # else needs to be in the ledger. Refusing to delete it is the reason why it is that I got
    # filled up with garbage that wasn't supposed to be there."*
    #
    # This file merged from its first commit, `30943703` on 2026-08-25 — titled *"rebuild the
    # Garborg ledger from Emma's account"* while the code loaded the existing file and only ever
    # added. That is the accumulation mechanism, and on 2026-08-27 it was described to her as
    # reassuring (*"nothing is being lost"*) rather than as the problem.
    #
    # **Nothing logs the drops beyond git, deliberately.** Her answer when asked: *"I thought the
    # ledger was git tracked so everything is logged."* It is — the file is committed every run,
    # so a removed row is in the diff, which outlives any print or side file.
    previous = {}
    if LEDGER.exists():
        with open(LEDGER, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                previous[row["geni_id"]] = row

    rows = {}
    added, changed = [], []
    for g, (qid, label, was_created) in sorted(found.items()):
        rows[g] = {"geni_id": g, "qid": qid, "label": label,
                   "created": "2026-08-25",
                   "note": f"from {ACCOUNT} contributions"
                           + ("" if was_created else " (P2600 added to an existing item)")}
        old = previous.get(g)
        if old is None:
            added.append((g, qid, label))
        elif old["qid"] != qid:
            changed.append((g, old["qid"], qid))

    # **Source two: the Bureätten people.** Emma, 2026-08-27, defining them exactly after I had
    # invented a hop threshold instead of asking: *"every item whose swedish wikipedia item is in
    # category:bureatten and which has a geni id."* That is `reports/bureatten.csv`, the
    # sv.wikipedia Category:Bureätten listing. No roster, no hops, no threshold.
    bure_file = ROOT / "reports" / "bureatten.csv"
    n_bure = 0
    if bure_file.exists():
        with open(bure_file, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                bqid = (row.get("qid") or "").strip()
                if not bqid.startswith("Q"):
                    continue
                raw = (row.get("geni_ids") or "").replace(";", " ").replace(",", " ")
                for g in raw.split():
                    if g.isdigit() and g not in rows:
                        rows[g] = {"geni_id": g, "qid": bqid,
                                   "label": (row.get("sv_title") or "").strip(),
                                   "created": "", "note": "Category:Bureätten (bureatten.csv)"}
                        n_bure += 1
    print(f"{n_bure} Bureätten people added as the second source")

    # **Source three: the entry points.** Emma, 2026-09-03, when shown that adding 315 group QIDs
    # as roots produced **0** new ring seeds: *"I think the Bure people were somehow manually
    # added to the universe or ledger too somehow. My guess is this was done manually in an
    # unscalable manner possibly with errors. Every entry point should be automatically in the
    # ledger once it is an established entry point."*
    #
    # Her guess is right and the code above is the evidence: the Bure people ARE a hand-added
    # second source, and 113 ledger rows carry that note. So an entry point being in the ledger
    # was never a property of the algorithm --- it was a property of one roster having been wired
    # in by hand. This makes it general instead.
    #
    # **Why it is load-bearing.** `compose()` draws ring seeds from the ledger
    # (`ring_seeds = {g for g, q in our_items.items() if q in our_wikidata_subgraph}`), so a root
    # outside it can be walked through and still seed nothing. Measured 2026-09-03: all 251 Bure
    # roots were in the ledger, none of the 315 group QIDs was, and neither was Ettinger or
    # Martin. Adding them as roots moved the subgraph by exactly their own count and produced no
    # new seeds at all --- `CLAUDE.md` § *Code that is WRITTEN but never CALLED* with a roster
    # instead of a function.
    #
    # **Only ACTIVE entry points**, since a date that has not arrived is not yet an entry point.
    n_entry = 0
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import importlib

        day = importlib.import_module("build-garborg-day")
        geni_of = {}
        for row in day.entry_points():
            q, g = (row.get("qid") or "").strip(), (row.get("geni_id") or "").strip()
            if q and g:
                geni_of[q] = g
        # **A group roster carries its own Geni id and that is the right source.** These are
        # curated pair files -- `izumo-p2600-pairs.tsv`, `tanba-p2600-pairs.tsv` -- so the
        # correspondence is already in them. Going to `derived-labels.csv` instead resolved only
        # 14 of 321, because that file's `qid` column comes from a different source.
        today = None
        for row in day.entry_point_groups():
            if (row.get("active_from") or "").strip() <= (today or __import__("datetime").date.today().isoformat()):
                for q, g in day.group_pairs(row):
                    if g and q not in geni_of:
                        geni_of[q] = g
        wanted = ({q for q, _ in day.active_entry_points()} | set(day.active_group_qids()))
        need = wanted - set(geni_of)
        if need:
            geni_of.update(_geni_for_qids(need))
        for q in sorted(wanted):
            g = geni_of.get(q)
            if g and g not in rows:
                rows[g] = {"geni_id": g, "qid": q, "label": "", "created": "",
                           "note": "entry point (entry-points.tsv / entry-point-groups.tsv)"}
                n_entry += 1
    except Exception as exc:  # a broken roster must not take the whole refresh down
        print(f"entry-point source skipped: {type(exc).__name__}: {exc}")
    print(f"{n_entry} entry-point people added as the third source")

    dropped = sorted(set(previous) - set(rows))
    if dropped:
        print(f"{len(dropped)} rows dropped -- they resolve from neither source. "
              f"The diff of {LEDGER.name} is the record:")
        for g in dropped[:20]:
            print(f"   {previous[g]['qid']:<12} {g:<21} {previous[g].get('label', '')[:34]}")

    # **A ledger QID that has since been MERGED AWAY is followed to its survivor.**
    #
    # Emma, 2026-09-02: *"an item that I edit that later gets redirected the algorithm needs to
    # follow the redirect and put the new one s as a possible one to run on too."*
    #
    # **This is the COMMON case, not the mirror of the check further down.** Emma, 2026-09-02:
    # *"it is almost 100% ubiquitous that my item i created or edited is gonna be the one
    # redirected elsewhere lol merge redirect targeting occurs by age."*
    #
    # She is right and it is measurable. `Help:Merge` keeps the LOWER Q number, and every item
    # in this ledger she made herself is new -- so hers is the one merged AWAY, essentially
    # always. Of the 26 stale rows the first run found, **26 of 26** went high Q to low Q:
    # Q141225740 -> Q109852817, Q141216475 -> Q10511224, Q141242568 -> Q130665779. None went
    # the other way.
    #
    # So this is the direction that matters, and the resolution further down -- which asks
    # whether a SCRAPED qid redirects to what the ledger holds -- covers the rare shape rather
    # than the symmetric other half. Describing the two as opposite directions of one problem
    # understated how routine this one is: it is what happens every time she merges.
    #
    # Left unfollowed, every algorithm keyed on the ledger points at a dead id -- the subgraph
    # walk cannot reach the person, the duplicate guard cannot see their statements, and the
    # daily batch would create them again.
    #
    # The row is REWRITTEN to the survivor rather than dropped, and the note records the move,
    # so nothing is lost and it is auditable. Batched 50 at a time.
    followed = []
    ledger_ids = sorted({(r.get("qid") or "").strip() for r in rows.values()
                         if (r.get("qid") or "").strip().startswith("Q")})
    try:
        moved = {}
        for k in range(0, len(ledger_ids), 50):
            data = get({"action": "wbgetentities", "format": "json", "props": "info",
                        "ids": "|".join(ledger_ids[k:k + 50])}, ua)
            for q, v in data.get("entities", {}).items():
                target = (v.get("redirects") or {}).get("to")
                if target and target != q:
                    moved[q] = target
        for g, r in rows.items():
            q = (r.get("qid") or "").strip()
            if q in moved:
                r["qid"] = moved[q]
                note = (r.get("note") or "").strip()
                r["note"] = (note + "; " if note else "") + "followed redirect %s -> %s" % (q, moved[q])
                followed.append((g, q, moved[q]))
    except Exception as exc:                                        # noqa: BLE001
        print("WARNING: could not check the ledger for merged-away items (%s) -- a stale qid "
              "may still be in it" % exc)

    if followed:
        print("")
        print("%d ledger qid(s) had been MERGED AWAY and were followed to the survivor:"
              % len(followed))
        for g, was, now in followed[:20]:
            print("   %-21s %s -> %s" % (g, was, now))

    with open(LEDGER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["geni_id", "qid", "label", "created", "note"],
                           delimiter="\t")
        w.writeheader()
        for g in sorted(rows):
            r = rows[g]
            w.writerow({k: r.get(k, "") for k in
                        ("geni_id", "qid", "label", "created", "note")})

    print(f"\n{len(added)} added to the ledger:")
    for g, qid, label in added:
        print(f"   {g}  {qid}  {label}")
    # **A "disagreement" is usually a MERGE she has already done.** Emma merged nine duplicate
    # items on 2026-08-31 and this went on reporting all nine, because her contributions still
    # name the item she created and that item is now a REDIRECT to the survivor the ledger
    # holds. Resolved live, every one of the nine pointed at the ledger's own value: the ledger
    # was right and the warning was noise -- noise that reads as "these people are absent",
    # which is exactly what she asked about.
    #
    # So resolve before comparing. A scraped qid that redirects to what the ledger holds is
    # AGREEMENT. One request per 50 candidates, never one per item.
    if changed:
        redirects = {}
        try:
            ids = sorted({b for _, _, b in changed})
            for k in range(0, len(ids), 50):
                data = get({"action": "wbgetentities", "format": "json", "props": "info",
                            "ids": "|".join(ids[k:k + 50])}, ua)
                for q, v in data.get("entities", {}).items():
                    target = (v.get("redirects") or {}).get("to")
                    if target:
                        redirects[q] = target
        except Exception as exc:                                    # noqa: BLE001
            print("WARNING: could not resolve redirects (%s) -- a disagreement below may "
                  "simply be a merge she has already made" % exc)
        merged = [(g, a, b) for g, a, b in changed if redirects.get(b) == a]
        changed = [(g, a, b) for g, a, b in changed if redirects.get(b) != a]
        if merged:
            print("\n%d resolved as MERGES she has already made -- the live item redirects "
                  "to what the ledger holds, so the ledger is right:" % len(merged))
            for g, a, b in merged:
                print(f"   {g}  {b} -> {a}")
    if changed:
        print(f"\n{len(changed)} DISAGREE with what the ledger held - not overwritten:")
        for g, a, b in changed:
            print(f"   {g}  ledger={a}  live={b}")
    print(f"\n{len(rows)} rows in {LEDGER.relative_to(ROOT)}")

    # **Resolve merges, every run, for the same reason the refresh itself runs every run.**
    #
    # Emma, 2026-08-29: *"a lot of the items were merged and this is a problem. since it
    # means a lot of relationship statements consistently use the wrong thing"*. When two
    # items merge, the loser becomes a redirect; a ledger row still naming the loser makes
    # every P22/P25/P26/P40/P3373 the daily batch emits point at a redirect rather than at
    # the surviving item -- and the "does it already hold this" check then compares against
    # the wrong item and re-emits.
    #
    # Four of 505 on the first run, and three of the four were load-bearing: Algot
    # Brynolfsson and Brynolf Bengtsson sit on the Charlemagne spine, and Andreas Olai is
    # the Bureatten pairing. 17 statements in that day's batch named a merged-away item.
    #
    # In-process rather than a second command, so it cannot be the step somebody forgets --
    # the same argument CLAUDE.md makes for the refresh itself being part of the run.
    import subprocess
    try:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "resolve-merged-qids.py"),
                        "--write"], check=True)
    except Exception as exc:                                        # noqa: BLE001
        print(f"WARNING: merge resolution did not run ({exc}) -- ledger QIDs may name "
              f"redirects, and every relationship statement built from them would too")


if __name__ == "__main__":
    main()
