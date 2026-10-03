"""
Generate P14005 (Japanese court rank) QuickStatements for PEOPLE, from the
ja.wikipedia rank-recipient category tree under
[[Category:日本の位階受位者]] (Japanese court-rank recipients).

Pipeline
--------
1. Enumerate the subcategories of the parent category on ja.wikipedia. Each
   per-rank subcategory is named "<rank>受位者" (e.g. 正一位受位者, 従四位上受位者).
2. Resolve <rank> -> the Wikidata rank ITEM QID by matching the rank's ja label
   against the items already used as P14005 values (WDQS). No hardcoded QID
   table to drift. This match is ALSO the exclusion filter: the special
   subcategories (失位・返上を命じられた者, 位階を持たない者, etc.) do not name a
   court-rank item, so they resolve to nothing and are skipped automatically.
3. For each rank subcategory, recursively collect its ns=0 member pages (all
   descendants of a rank category still hold that rank), resolve each page to
   its Wikidata QID (ja.wp pageprops wikibase_item), and emit
       QID|P14005|<rank-item-QID>|S143|Q177837|S4656|"<jawiki url>"
   The reference is the ja.wikipedia article the rank was read from — the same
   S143/S4656 shape the saijin and honzon generators use.
4. Add-only / non-destructive: a person whose P14005 = that rank ALREADY CARRIES
   A REFERENCE is skipped. An existing BARE statement is re-emitted with the
   reference, which QuickStatements attaches to the matching statement rather
   than duplicating it. Nothing is ever removed here — consistent with the
   repo's add-first, two-scripts rule.

   ⚠ The skip used to be "has the rank at all", and the emitted line carried no
   reference. That combination left P14005 at **39% referenced — 2,026 of 5,180
   statements — against 98.9% for P13723 and 96.8% for temple P825**
   (`audit_model_adoption.py`, 2026-09-15): the generator produced unreferenced
   statements and then refused to ever look at them again.

Output: reports/wikidata-court-rank.qs, tab-separated QuickStatements, which
`pipeline.yml` appends to the manual half of the day batch. It only writes the file.

IN THIS REPOSITORY (ported 2026-10-01 from shintowiki-scripts, see README.md here):
the shrine-repo helpers are replaced by `genimerge.wikidata` (User-Agent from
BOT_CONTACT, 429/503 waited out), and a person is kept only when they are in the
edit universe or one step beyond it (`out/wikidata/edit-universe.json`), until
`wikidata_lockout.COURT_RANK_ANYONE_FROM` (2027-06-01), after which anyone holding
a rank gets it (Emma, 2026-09-26).

Flags
-----
--highest-only   emit only each person's single highest rank instead of every
                 rank they ever held (default: every rank held).
--max N          cap emitted lines (smoke tests).
--dry-run        print a summary, do not write the .txt.

429 from WDQS => bail immediately (repo rule). Read-only against both wikis.

STATUS 2026-07-28 — WIRED IN. The 26 sub-rank items exist (created by Emma,
Q140679480…Q140679509) and WDQS has indexed them: the live rerun this day reported
"42 rank categories resolved", which was the wire-in condition. The rank map is by
primary ja label under the court-rank class; 无位 is skipped; recursion no longer
double-tags a coarser parent rank; every rank a person held is emitted. The step now
runs in generate-quickstatements.yml and court_rank_people.txt is registered in
direct_daily_edits.ATOMIC_FILES (uncapped — ~10% of the daily draw, the same share
as its size peers). Current output: 12,326 people -> 12,605 statements.

Nothing edits yet: a week-long Wikidata freeze runs to 2026-08-04
(FREEZE_WIKIDATA_UNTIL in cleanup-loop.yml's window-gate forces
wikidata-daily-fire=false), so the first court-rank lines can land no earlier than
that. Confirmed still in force by Emma on 2026-07-28.
"""

import datetime
import json
import os
import re
import sys
import time
import argparse
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from genimerge.wikidata import SPARQL_ENDPOINT, _http_fetch  # noqa: E402
import wikidata_lockout  # noqa: E402

OUT = os.path.join(ROOT, "reports", "wikidata-court-rank.qs")
RANK_ITEMS = os.path.join(ROOT, "reports", "court-rank-items.tsv")
UNIVERSE = os.path.join(ROOT, "out", "wikidata", "edit-universe.json")

JA_API = "https://ja.wikipedia.org/w/api.php"
PARENT_CAT = "Category:日本の位階受位者"
RANK_SUFFIX = "受位者"


def allowed_people(today=None):
    """`None` when anyone may get a court rank, else the universe and its one-step ring.

    Fails closed: before the date, a missing or empty universe file means nobody."""
    if wikidata_lockout.court_rank_anyone(today):
        return None
    try:
        with open(UNIVERSE, encoding="utf-8") as fh:
            d = json.load(fh)
    except OSError:
        return set()
    return set(d.get("universe") or ()) | set(d.get("one_step") or ())


def qs_line(person, rank, url):
    """One tab-separated QuickStatements line with the jawiki reference."""
    return f'{person}\tP14005\t{rank}\tS143\tQ177837\tS4656\t"{url}"'


def _utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _sparql(query):
    """WDQS through this repository's own fetch (User-Agent, 429/503 waited out).

    The history below is shintowiki-scripts', kept as it was handed over.

    ⛔ THIS FILE'S OWN TRANSPORT SPACED ITS QUERIES 0.5s APART. That is not a
    near-miss on the 2.5s floor — 0.5s is the exact figure CLAUDE.md names when it
    explains where the floor came from: `match_jinjacho_shrines.py` fired ~365
    queries per run "at 0.5s spacing, three times in one evening, and drew repeated
    503/504 which were then blamed on the endpoint." This generator issues only
    three queries per run, so it never produced that damage, but it carried the
    pattern the rule exists to stop.

    Its backoff was 5/10/15s, which is also weaker than the documented 15/45/135 —
    so unlike the ten callers that already escalate harder than a flat policy, this
    one is strictly improved by adopting the shared module. That is the test the
    queue item sets for a migration, and this file met it on the tick after its
    reference fix, which is exactly the "rides with the file's next real change"
    cadence the item prescribes.

    Safe on the GET-only constraint: all three call sites send short fixed queries
    with no VALUES clause, so nothing here can hit the 414 the module documents.
    Same endpoint (`query-main.wikidata.org`), so nothing else changes.
    """
    time.sleep(2.5)
    body = urllib.parse.urlencode({"query": query, "format": "json"}).encode()
    raw = _http_fetch(SPARQL_ENDPOINT, data=body,
                      headers={"Accept": "application/sparql-results+json",
                               "Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(raw)["results"]["bindings"]


def _ja_api(params):
    params = dict(params, format="json")
    time.sleep(0.3)
    return json.loads(_http_fetch(JA_API + "?" + urllib.parse.urlencode(params)))


COURT_RANK_CLASS = "Q99196082"  # "court rank in Japan"
# "no rank" — a member of the class but NOT a rank to tag people with; skip it.
NO_RANK_QID = "Q11504610"       # 无位


def rank_label_to_qid():
    """{primary ja label of a court-rank item -> QID}, for every item under the
    court-rank class. This is broader than "items used as P14005 values" (which
    misses ranks not yet used) and now covers the sub-rank items created
    2026-07-23, so every ja.wp per-rank recipient category resolves. 无位 (no
    rank) is excluded."""
    rows = _sparql(
        'SELECT ?item ?lab WHERE { '
        '?item (wdt:P31|wdt:P279)/wdt:P279* wd:%s . '
        '?item rdfs:label ?lab . FILTER(LANG(?lab)="ja") }' % COURT_RANK_CLASS
    )
    m = {}
    for b in rows:
        qid = b["item"]["value"].rsplit("/", 1)[1]
        if qid == NO_RANK_QID:
            continue
        m[b["lab"]["value"]] = qid
    return m


def existing_pairs():
    """Set of (person_qid, rank_qid) already stated, so we never re-add."""
    rows = _sparql("SELECT ?p ?r WHERE { ?p wdt:P14005 ?r }")
    out = set()
    for b in rows:
        out.add((b["p"]["value"].rsplit("/", 1)[1],
                 b["r"]["value"].rsplit("/", 1)[1]))
    return out


def referenced_pairs():
    """(person, rank) pairs whose P14005 statement ALREADY carries a reference.

    ⛔ THIS IS THE SKIP SET, not `existing_pairs()`. Skipping every pair that
    merely exists is what left this property at **39% referenced (2,026 of
    5,180) while P13723 sits at 98.9% and temple P825 at 96.8%** — measured by
    `audit_model_adoption.py` on 2026-09-15. The generator emitted a bare
    `QID|P14005|<rank>` with no reference, then refused to touch the statement
    again, so an unreferenced court rank was unreachable for good.

    Re-emitting the same statement WITH a reference does not duplicate it:
    QuickStatements matches the existing (item, property, value) and attaches
    the reference to it. That is the same enrichment shape as `c121509e`, which
    fixed three generators that created statements but never enriched the ones
    already there.
    """
    rows = _sparql("""
      SELECT ?p ?r WHERE {
        ?p p:P14005 ?st .
        ?st ps:P14005 ?r .
        ?st prov:wasDerivedFrom ?ref .
      }
    """)
    out = set()
    for b in rows:
        out.add((b["p"]["value"].rsplit("/", 1)[1],
                 b["r"]["value"].rsplit("/", 1)[1]))
    return out


def subcategories(cat):
    """Direct subcategory titles (ns=14) of a category on ja.wikipedia."""
    subs, cont = [], {}
    while True:
        data = _ja_api({"action": "query", "list": "categorymembers",
                        "cmtitle": cat, "cmtype": "subcat", "cmlimit": "500", **cont})
        subs += [m["title"] for m in data["query"]["categorymembers"]]
        if "continue" in data:
            cont = data["continue"]
        else:
            break
    return subs


def category_pages(cat, seen_cats):
    """All ns=0 page titles under a category, recursing into NON-rank
    subcategories only. A subcategory that is itself a rank-recipient category
    (name ends in 受位者) is a DIRECT child of the parent tree and is crawled on
    its own top-level pass; recursing into it here would tag its people with the
    coarser parent rank too (e.g. 従八位上受位者's members also getting 従八位).
    Other subcats (by-era groupings etc.) share this category's rank, so recurse."""
    if cat in seen_cats:
        return []
    seen_cats.add(cat)
    titles, cont = [], {}
    while True:
        data = _ja_api({"action": "query", "list": "categorymembers",
                        "cmtitle": cat, "cmnamespace": "0|14", "cmlimit": "500", **cont})
        for m in data["query"]["categorymembers"]:
            if m["ns"] == 0:
                titles.append(m["title"])
            elif m["ns"] == 14:
                name = m["title"].split(":", 1)[1] if ":" in m["title"] else m["title"]
                if not name.endswith(RANK_SUFFIX):
                    titles += category_pages(m["title"], seen_cats)
        if "continue" in data:
            cont = data["continue"]
        else:
            break
    return titles


def titles_to_qids(titles):
    """{ja.wp title -> Wikidata QID} via pageprops wikibase_item, 50/batch."""
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        data = _ja_api({"action": "query", "prop": "pageprops",
                        "ppprop": "wikibase_item", "titles": "|".join(batch),
                        "redirects": "1"})
        pages = data.get("query", {}).get("pages", {})
        # map any redirect-normalised titles back is unnecessary; we key by the
        # returned page title, and only need the QID set per rank anyway.
        for p in pages.values():
            qid = p.get("pageprops", {}).get("wikibase_item")
            if qid:
                out[p["title"]] = qid
    return out


def main():
    _utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--highest-only", action="store_true",
                    help="emit only each person's highest rank (default: every rank held)")
    ap.add_argument("--max", type=int, default=0, help="cap emitted lines")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print(f"Rank label->QID map (P14005 values)...", flush=True)
    rank_map = rank_label_to_qid()
    print(f"  {len(rank_map)} court-rank items.", flush=True)
    # The rank items as queried, for the batch test: a P14005 value is a live item of the
    # court-rank class, which no ledger lists (2026-10-03: CI failed on 従三位 Q11071123).
    with open(RANK_ITEMS, "w", encoding="utf-8", newline="\n") as f:
        f.write("qid\tja\n")
        for lab, qid in sorted(rank_map.items(), key=lambda kv: (kv[1], kv[0])):
            f.write(f"{qid}\t{lab}\n")

    print("Existing person->rank pairs...", flush=True)
    have = existing_pairs()
    print(f"  {len(have)} existing P14005 statements.", flush=True)
    print("Which of them already carry a reference (the real skip set)...", flush=True)
    referenced = referenced_pairs()
    print(f"  {len(referenced)} referenced; {len(have) - len(referenced)} bare "
          f"and reachable for enrichment.", flush=True)

    print(f"Subcategories of {PARENT_CAT}...", flush=True)
    subs = subcategories(PARENT_CAT)
    # keep only per-rank recipient categories that resolve to a rank item;
    # this drops the 失位/返上/no-rank specials automatically.
    rank_cats = []
    for c in subs:
        name = c.split(":", 1)[1] if ":" in c else c
        if not name.endswith(RANK_SUFFIX):
            continue
        rank_name = name[: -len(RANK_SUFFIX)]
        qid = rank_map.get(rank_name)
        if qid:
            rank_cats.append((c, rank_name, qid))
        else:
            print(f"  [skip] {name}: no P14005 item matches '{rank_name}'", flush=True)
    print(f"  {len(rank_cats)} rank categories resolved.", flush=True)

    # person_qid -> list of (rank_qid, rank_name), ordered as discovered
    person_ranks = {}
    # rank "strength" for --highest-only: senior(正)>junior(従), then lower N first.
    def strength(rank_name):
        grade = 0 if rank_name.startswith("正") else 1  # 正 senior beats 従 junior
        mnum = re.search(r"[一二三四五六七八九十]", rank_name)
        order = "一二三四五六七八九十"
        n = order.index(mnum.group()) if mnum else 99
        upper = 0 if rank_name.endswith("上") else 1  # 上 upper beats 下
        return (n, grade, upper)  # smaller = higher rank

    for cat, rank_name, rank_qid in rank_cats:
        titles = category_pages(cat, set())
        qmap = titles_to_qids(titles)
        print(f"  {rank_name}: {len(titles)} pages, {len(qmap)} with QIDs", flush=True)
        for title, pq in qmap.items():
            # Carry the ja.wikipedia TITLE through: it is the source the rank was
            # read from, so it is what the S4656 reference URL has to name. It was
            # dropped here before, which is why the emitted lines had no reference
            # they could have cited.
            person_ranks.setdefault(pq, []).append((rank_qid, rank_name, title))

    allowed = allowed_people()
    if allowed is not None:
        before = len(person_ranks)
        person_ranks = {pq: r for pq, r in person_ranks.items() if pq in allowed}
        print(f"  universe gate (until {wikidata_lockout.COURT_RANK_ANYONE_FROM}): "
              f"{len(person_ranks)} of {before} people are in the universe or one step beyond",
              flush=True)

    lines = []
    new_stmts = enriched = 0
    for pq, ranks in person_ranks.items():
        chosen = ranks
        if args.highest_only:
            chosen = [min(ranks, key=lambda rr: strength(rr[1]))]
        for rank_qid, rank_name, title in chosen:
            # Skip only what is already REFERENCED. A pair in `have` but not in
            # `referenced` is an existing bare statement, and re-emitting it with
            # the reference is how it gets one — QuickStatements attaches the
            # reference to the matching statement rather than duplicating it.
            if (pq, rank_qid) in referenced:
                continue
            if (pq, rank_qid) in have:
                enriched += 1
            else:
                new_stmts += 1
            url = ("https://ja.wikipedia.org/wiki/"
                   + urllib.parse.quote(title.replace(" ", "_")))
            lines.append(qs_line(pq, rank_qid, url))

    # de-dup lines while preserving order
    seen, uniq = set(), []
    for ln in lines:
        if ln not in seen:
            seen.add(ln); uniq.append(ln)
    if args.max:
        uniq = uniq[: args.max]

    print(f"{len(person_ranks)} people -> {len(uniq)} P14005 lines "
          f"({new_stmts} new statements, {enriched} references onto statements "
          f"that already exist).", flush=True)
    if args.dry_run:
        for ln in uniq[:20]:
            print("   ", ln)
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for ln in uniq:
            f.write(ln + "\n")
    print(f"Wrote {len(uniq)} lines -> {OUT}")


if __name__ == "__main__":
    main()
