"""Label slots that have been REVERTED, so the generator stops re-asserting them.

    BOT_CONTACT=you@example.com PYTHONPATH=src python scripts/refresh-reverted-labels.py

Ruled 2026-09-15, from `queue.md` section *Unintentional edit wars*: *"our algorithm is
relatively resistant to editors fixing its mistakes and this is drawing attention."*

## THE STATEMENT FIX DID NOT COVER LABELS, AND LABELS ARE WHERE IT IS HAPPENING

`read_suppressed` closed the 2026-08-30 war over `P734`: an editor removed a statement, the next
build saw a gap and filled it, indefinitely. **Labels have exactly the same shape and no guard.**
The generator emits `L<lang>` when the live label differs from ours, and an editor's correction is
precisely what "differs from ours" looks like.

**Measured over the last 7,500 of the account's mainspace edits: 100 carry a revert tag**, and
they are overwhelmingly `wbsetlabel` on `ja`, `zh` and `ko`, every one `#quickstatements`. On
`Q313883` in a single run the `ko` label was a `mw-manual-revert` while `zh` and `ja` were
`mw-reverted` -- the batch restoring its own earlier value on one slot while being undone on two
others.

## BOTH TAGS MARK A CONTESTED SLOT, AND THE SECOND ONE IS THE DAMNING ONE

    mw-reverted        somebody undid OUR edit
    mw-manual-revert   OUR edit restored an exact previous revision -- we undid THEIRS

The second is the one that draws attention. A bot being reverted is ordinary; a bot that reverts a
human back, on a schedule, is what gets noticed. Both mean the same thing for our purposes: a
human has expressed an opinion about this `(item, language)` and we must stop overwriting it.

## THIS READS OUR OWN CONTRIBUTIONS, WHICH IS NOT THE THING THAT WAS RULED AGAINST

`refresh-suppressed-statements.py` carries an explicit ruling -- *"It is extremely stupid that you
wrote it as something that actively watches the editor's edits ... I want to watch their edits once
and then leave it"* -- and that is about watching ANOTHER editor continuously. This reads the
account's OWN contribution list, which is already how `reports/garborg-qids.tsv` is built, and it
names nobody. It is also bounded: one `usercontribs` walk, 500 a page.

## The safe direction is to SUPPRESS

A suppressed slot costs one label we might have been right about. An unsuppressed one costs
another round of the war. `read_suppressed` chose the same way and says why: a missing file there
warns loudly rather than shrugging.

Writes `reports/reverted-labels.tsv`: `qid`, `lang`, `when`, `tag`, `value`.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import _http_fetch, require_agent  # noqa: E402

OUT = ROOT / "reports" / "reverted-labels.tsv"

#: The account that runs the batches. Its own contributions are the input.
OURS = "日巫女"

#: The tags MediaWiki puts on a revision that undid something or was undone. Both mark the slot
#: as contested; see the module docstring for why the second is the one that draws attention.
REVERT_TAGS = ("mw-reverted", "mw-undo", "mw-rollback", "mw-manual-revert")

#: `/* wbsetlabel-set:1|zh */ 約翰·巴列奧略, #quickstatements` -- the language is in the comment's
#: machine-readable head and the value follows it. `wbsetlabel-remove` counts too: a removal is an
#: opinion about the slot exactly as much as a change is.
LABEL_EDIT = re.compile(r"/\* wbsetlabel-(?:set|remove):\d+\|([a-z][a-z0-9-]*) \*/\s*([^,]*)")

#: How many contribution pages to walk. 500 per page, so this covers the account's recent history
#: without paging years of it -- the same bound and the same reason as
#: `refresh-suppressed-statements.removals_by`.
MAX_PAGES = 30


def reverted_label_slots(ua):
    """`[{qid, lang, when, tag, value}]` for every contested label slot found."""
    out, cont, pages, scanned = [], None, 0, 0
    while pages < MAX_PAGES:
        url = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=usercontribs"
               "&ucuser=" + urllib.parse.quote(OURS) +
               "&uclimit=500&ucnamespace=0&ucprop=title|timestamp|comment|tags")
        if cont:
            url += "&uccontinue=" + urllib.parse.quote(cont)
        data = json.loads(_http_fetch(url, headers=ua))
        contribs = (data.get("query") or {}).get("usercontribs") or []
        pages += 1
        scanned += len(contribs)
        for c in contribs:
            tags = c.get("tags") or []
            hit = [t for t in tags if t in REVERT_TAGS]
            if not hit:
                continue
            m = LABEL_EDIT.search(c.get("comment") or "")
            if not m:
                continue
            out.append({"qid": c["title"], "lang": m.group(1),
                        "when": c["timestamp"][:10], "tag": hit[0],
                        "value": m.group(2).strip()})
        cont = (data.get("continue") or {}).get("uccontinue")
        if not cont:
            break
        time.sleep(0.3)
    print(f"   scanned {scanned:,} of the account's edits over {pages} page(s)")
    return out


def main() -> int:
    ua = {"User-Agent": require_agent()}
    rows = reverted_label_slots(ua)

    # **Deduplicated on the SLOT, not the edit.** The same `(item, language)` is reverted more
    # than once -- that is what a war is -- and the generator asks one question per slot.
    best = {}
    for r in rows:
        key = (r["qid"], r["lang"])
        if key not in best or r["when"] > best[key]["when"]:
            best[key] = r

    tab = chr(9)
    nl = chr(10)
    lines = [tab.join(("qid", "lang", "when", "tag", "value"))]
    for (qid, lang), r in sorted(best.items()):
        lines.append(tab.join((qid, lang, r["when"], r["tag"], r["value"])))
    OUT.write_text(nl.join(lines) + nl, encoding="utf-8", newline=nl)

    by_tag, by_lang = {}, {}
    for r in best.values():
        by_tag[r["tag"]] = by_tag.get(r["tag"], 0) + 1
        by_lang[r["lang"]] = by_lang.get(r["lang"], 0) + 1
    print(f"wrote {OUT.relative_to(ROOT)} -- {len(best)} contested label slot(s) "
          f"over {len({q for q, _ in best})} item(s)")
    for tag, n in sorted(by_tag.items(), key=lambda kv: -kv[1]):
        print(f"   {tag:<20} {n}")
    print("   languages: " + ", ".join(f"{k} {v}" for k, v in
                                       sorted(by_lang.items(), key=lambda kv: -kv[1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
