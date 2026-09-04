"""What each ledger item ALREADY states, by value, so the batch stops re-emitting it.

    BOT_CONTACT=you@example.com python scripts/refresh-live-values.py

**Emma, 2026-08-27**, on the relationship section never shrinking: *"the relationship one is
questionable that it's always gonna be so huge and growing."* Measured the same day: **229 of
306** statements on existing items in that day's batch were **already on Wikidata**. Only 77
were new. The section is three-quarters noise.

## Two defects, and the stale file is only one

* **`P40` *child*, `P26` *spouse* and `P3373` *sibling* were emitted with no check at all.**
  The additions loop tests `absent()` for `P22` *father* and `P25` *mother* and for nothing
  else, so every child link the ledger implies went out every single run.
* **`absent()` is property-level and stale.** `reports/garborg-live-state.tsv` records which
  *properties* an item carries, not which values, and was frozen at **2026-08-24**. Property
  level cannot tell a second father from an existing one; a frozen file cannot tell that Emma
  ran yesterday's batch.

This writes the missing half: `qid`, `property`, `value`, one row per statement actually on
the item, read through `genimerge.wikidata.full_entities` — whole items, never a summary, per
`CLAUDE.md` § *A SUMMARY of a Wikidata item is not the item*.

**QuickStatements merges a duplicate rather than failing on it**, which is exactly why this went
unnoticed: nothing broke, the batches were simply three-quarters things she had already done.

Writes `reports/garborg-live-values.tsv`.
"""
from __future__ import annotations

import csv
import gzip
import json
import os
import pathlib
import sys
from pathlib import Path

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bot_identity import agent as _bot_agent  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
OUT = ROOT / "reports" / "garborg-live-values.tsv"

#: **The live LABEL of each ledger item, in the languages we write.**
#:
#: **Emma, 2026-08-30:** *"Every single label gets redone and if they disagree then they go
#: onto the quickstatements that are generated."* A disagreement can only be seen against the
#: value, and until now nothing recorded it: `garborg-existing-gaps.existing_state` reads the
#: offline store and yields the label *languages* an item has, not what they say, and the store
#: predates every item Emma has made. So the batch could only ever ask "is `ja` missing", never
#: "is `ja` right".
#:
#: Same fetch, same items, no extra requests -- `full_entities` already returns labels and they
#: were being thrown away.
LABELS_OUT = ROOT / "reports" / "garborg-live-labels.tsv"

#: **Every ledger item's WHOLE entity, as fetched, one JSON object per line sorted by qid.**
#: See the block that writes it for why the two TSVs above are not a substitute.
#: `read_live_items()` is the reader; `gzip -dc` and a grep also work.
ITEMS_OUT = ROOT / "reports" / "garborg-live-items.jsonl.gz"


def read_live_items(qids=None):
    """`{qid: entity}` from `ITEMS_OUT`, or `{}` when the file is absent.

    `qids` limits what is parsed, which matters: the file is every ledger item and a caller
    usually wants one. A missing file returns empty rather than raising, so a fresh clone that
    has not run the refresh degrades to today's behaviour instead of crashing — but callers
    must treat empty as *we have not looked*, never as *the items hold nothing*, which is the
    trap `CLAUDE.md` § *Our side could never have two children* is written against.
    """
    if not ITEMS_OUT.exists():
        return {}
    want = set(qids) if qids is not None else None
    out = {}
    with gzip.open(ITEMS_OUT, "rt", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            if want is not None:
                # Cheap pre-filter: the id is the only place a `"id":"Q…"` pair appears at the
                # top level, and parsing 1,464 whole items to find one is the thing to avoid.
                if not any(f'"id":"{q}"' in line for q in want):
                    continue
            item = json.loads(line)
            if want is None or item.get("id") in want:
                out[item["id"]] = item
    return out

#: **EVERY language, not the ones we write.** Emma, 2026-08-30, specifying how `mul` should be
#: chosen: *"they have a consistent Latin label across two or more languages… whichever one is
#: the most common"*. That is a count over all the item's labels, so restricting the capture to
#: the fifteen languages this project emits would make the consensus a measure of our own
#: output. `None` means no filter.
LABEL_LANGS = None

#: `full_entities` returns `{}` above this many ids rather than erroring, which reads as
#: "these items hold nothing" -- the absence-versus-broken-join trap. Chunked well under it.
CHUNK = 40


def main():
    if not _bot_agent():
        sys.exit("BOT_CONTACT is not set; Wikimedia answers an empty User-Agent with a 403")
    from genimerge.wikidata import WikidataClient

    qids = sorted({r["qid"] for r in csv.DictReader(open(LEDGER, encoding="utf-8"),
                                                    delimiter="\t")
                   if (r.get("qid") or "").startswith("Q")})
    # **`entity_resolution.md` was deleted in `12f3134a` and its readers were not.**
    # Emma, 2026-08-31: *"no files should read it lol."* The block that stood here
    # folded that file's hand-asserted pairs into this lookup; the file has been gone
    # since 2026-08-29, so the block contributed nothing and only reported its own
    # absence. `CLAUDE.md` § *LEGACY CODE IS DELETED* is the rule and § *Systematic
    # review for legacy code* is the other half of it -- deleting the file is half the
    # job, and a reader that degrades quietly is the worse half.
    qids = sorted(set(qids))
    print(f"{len(qids)} items to read")

    client = WikidataClient(ROOT / "out" / "wikidata" / "livecache")
    items = {}
    for i in range(0, len(qids), CHUNK):
        items.update(client.full_entities(qids[i:i + CHUNK]))
        print(f"  {min(i + CHUNK, len(qids))}/{len(qids)}", flush=True)
    if not items:
        sys.exit("no items came back at all -- that is a broken fetch, not empty items")
    print(f"{len(items)} of {len(qids)} fetched")

    rows = []
    for qid, item in sorted(items.items()):
        for prop, statements in sorted(item.get("claims", {}).items()):
            for st in statements:
                if st.get("rank") == "deprecated":
                    continue
                v = st.get("mainsnak", {}).get("datavalue", {}).get("value")
                if isinstance(v, dict):
                    value = v.get("id") or v.get("text") or (
                        v["time"].split("T")[0] if v.get("time") else "")
                elif isinstance(v, str):
                    value = v
                else:
                    value = ""
                if value:
                    rows.append({"qid": qid, "property": prop, "value": value})

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "property", "value"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows):,} statements over {len(items)} items "
          f"-> {OUT.resolve().relative_to(ROOT)}")

    # The labels, from the same fetch. See `LABELS_OUT`.
    label_rows = []
    for qid, item in sorted(items.items()):
        labels = item.get("labels", {})
        for lang in (LABEL_LANGS or sorted(labels)):
            value = (labels.get(lang) or {}).get("value")
            if value:
                label_rows.append({"qid": qid, "lang": lang, "label": value})
    with open(LABELS_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "lang", "label"], delimiter="\t")
        w.writeheader()
        w.writerows(label_rows)
    print(f"{len(label_rows):,} labels over {len(items)} items "
          f"-> {LABELS_OUT.resolve().relative_to(ROOT)}")

    # **⛔ THE WHOLE ITEMS, COMMITTED. Emma, 2026-09-04:** *"Github actions is supposed to
    # download jsons of the current revisions of the entire ledger all at once and commit them,
    # so the information is supposed to always be present in the repository lol. My guess is you
    # never actually added that functionality"*. Her guess was right.
    #
    # **The download was already happening and the JSON was being thrown away.** `full_entities`
    # above fetches whole items for every ledger qid, on every pipeline run, and the two TSVs
    # above are flattened summaries of them — `qid/property/value` and `qid/lang/label`. Neither
    # carries qualifiers, references, ranks or sitelinks, and `CLAUDE.md` § *A SUMMARY of a
    # Wikidata item is not the item* records three false findings published from exactly that
    # gap, plus § *Reading a Wikidata statement: the value is not the statement*, where a
    # marriage date and place lived in qualifiers a mainsnak-only reader reported as absent.
    #
    # **What it cost, the same evening this was written.** A session whose egress proxy denies
    # `www.wikidata.org` had to dispatch a workflow to answer *"do these 161 items carry a
    # `P2600`?"*, *"what does `Q136376387` hold in `mul`?"* and *"what do these four items
    # read?"* — every one of which is a question about the ledger, whose answer had been fetched
    # and discarded minutes earlier. With this file present those are a `zcat` and a grep.
    #
    # **JSONL sorted by qid**, so one item can be read without loading the lot, and gzipped with
    # `mtime=0` so identical content produces identical bytes — a timestamp in the header would
    # make the file differ on every run and the diff meaningless, which is
    # § *SORTING MUST BE DETERMINISTIC* in its other clothes.
    tmp = ITEMS_OUT.with_suffix(".jsonl.gz.tmp")
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            for qid, item in sorted(items.items()):
                gz.write((json.dumps(item, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
    os.replace(tmp, ITEMS_OUT)
    size = ITEMS_OUT.stat().st_size
    print(f"{len(items):,} whole items -> {ITEMS_OUT.resolve().relative_to(ROOT)} "
          f"({size / 1024 / 1024:.1f} MB gzipped)")


if __name__ == "__main__":
    main()
