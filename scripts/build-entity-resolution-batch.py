"""`entity_resolution.md` as JSON edit objects.

Emma's scratchpad of Geni-to-Wikidata identities she recognised **by hand**, plus
label edits she wants. No query in this repo could produce these: they are
judgements about who is who.

**This replaces a renderer that was deleted without one.** `entities.render_quickstatements`
went with the rest of QuickStatements on 2026-08-15, leaving the file parsed but
with nothing to emit. The format here is the one Emma's 2026-08-12 spec asks for
— JSON edit objects — so the deletion removed a superseded serialiser; the gap
was that no replacement was written the same day.

**The file itself was never touched.** `git diff` on `entity_resolution.md`
across every commit of 2026-08-15 is empty; it was last edited on 08-12, by her.
`CLAUDE.md`: *do not reformat the file to suit the parser* — when an entry is not
understood, the parser is taught, and `tests/test_entities.py` pins that by
asserting the real file parses with **zero** unparsed entries.

**Two kinds of edit come out:**

* `add_geni_id` — a `P2600` on an existing item, cited to the Geni profile it
  names. Measured 2026-08-15: **all 7 are absent from their item**, so every one
  is real work, and all 7 Geni profiles are in the corpus.
* `set_label` — an English label. Two of the three are **additions** to items
  with no English label at all (`Q19657284`, `Q12598947`); one is a **change**,
  `Q11443857` from `Futohime` to `Mononobe no Futohime`. Emma, asked whether
  `CLAUDE.md`'s add-don't-correct rule blocks that: *"Emit it — you asked for it
  specifically."* The rule is about bulk contradiction resolution, not about a
  correction she made by hand and wrote down.

**A resolution naming a profile the corpus does not hold is still emitted** — the
assertion is hers and does not depend on our coverage — but it is flagged, which
is the behaviour the deleted renderer had and this keeps.

The name correction (`Emma Leonhart` for Geni `6000000087535357291`) is **not**
emitted here: it is applied at derivation by `scripts/labels.py`, not by an edit
to Wikidata.

    py scripts/build-entity-resolution-batch.py
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import entities, sources, wikistore  # noqa: E402

SOURCE = REPO / "entity_resolution.md"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
STORE = REPO / "wikidata" / "items"
OUT = REPO / "reports" / "wikidata-entity-resolution.json"

INDI = re.compile(r"^0 @I(\d+)@ INDI")
GENI_ID = "P2600"


def corpus_geni_ids() -> set[str]:
    ids: set[str] = set()
    for path in sources.find_exports():
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            for raw in fh:
                m = INDI.match(raw)
                if m:
                    ids.add(m.group(1))
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--retrieved", default="2026-08-15")
    args = ap.parse_args()

    parsed = entities.read_file(SOURCE)
    if parsed.unparsed:
        # Never silently drop one. CLAUDE.md: teach the parser, do not reformat
        # the file, and do not let an entry vanish because it was not understood.
        print(f"{len(parsed.unparsed)} entries were NOT understood:", file=sys.stderr)
        for entry in parsed.unparsed:
            print(f"  {entry!r}", file=sys.stderr)
    print(f"{len(parsed.resolutions)} resolutions, {len(parsed.labels)} label edits, "
          f"{len(parsed.corrected_names())} name corrections, "
          f"{len(parsed.unparsed)} unparsed")

    ours = corpus_geni_ids()

    pairs: dict[str, set[str]] = {}
    if INDEX.exists():
        conn = sqlite3.connect(INDEX)
        for qid, geni_id in conn.execute("select qid, geni_id from geni"):
            pairs.setdefault(qid, set()).add(geni_id)
        conn.close()

    qids = sorted({r.qid for r in parsed.resolutions} | {e.qid for e in parsed.labels})
    stored: dict[str, dict] = {}
    if INDEX.exists():
        with wikistore.StoreReader(STORE, INDEX) as reader:
            stored = reader.entities(qids)

    edits, already, unheld = [], 0, 0
    for r in parsed.resolutions:
        if r.geni_id in pairs.get(r.qid, set()):
            already += 1
            continue
        in_corpus = r.geni_id in ours
        if not in_corpus:
            unheld += 1
        edits.append({
            "id": f"entity_resolution:{r.qid}",
            "type": "add_geni_id",
            "source": "entity_resolution.md",
            "subject": {"qid": r.qid, "geni_id": r.geni_id},
            "requires": [],
            "statements": [{
                "property": GENI_ID,
                "value": r.geni_id,
                "references": [
                    {"property": "P854",
                     "value": f"https://www.geni.com/people/x/{r.geni_id}"},
                    {"property": "P813",
                     "value": f"+{args.retrieved}T00:00:00Z/11"},
                ],
            }],
            "geni_id_in_our_corpus": in_corpus,
        })

    for e in parsed.labels:
        current = ((stored.get(e.qid) or {}).get("labels") or {}).get(e.language)
        current = current.get("value") if isinstance(current, dict) else current
        if current == e.text:
            already += 1
            continue
        edits.append({
            "id": f"entity_resolution_label:{e.qid}:{e.language}",
            "type": "set_label",
            "source": "entity_resolution.md",
            "subject": {"qid": e.qid},
            "requires": [],
            "label": {"language": e.language, "value": e.text},
            # Stated so a reviewer can see whether this replaces something.
            "replaces": current,
            "kind": "change" if current else "addition",
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT} ({len(edits)} edits)")
    print(f"  {sum(1 for e in edits if e['type'] == 'add_geni_id')} add_geni_id")
    for e in edits:
        if e["type"] == "set_label":
            print(f"  set_label {e['subject']['qid']} {e['label']['language']} "
                  f"-> {e['label']['value']!r} ({e['kind']}"
                  f"{', replacing ' + repr(e['replaces']) if e['replaces'] else ''})")
    if already:
        print(f"  {already} already correct on Wikidata, nothing emitted")
    if unheld:
        print(f"  {unheld} name a Geni profile the corpus does not hold - "
              "emitted anyway, the assertion is Emma's")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
