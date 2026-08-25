"""Labels, aliases and every genealogy identifier, out of the store, once.

    python scripts/extract-wikidata-labels.py

**Emma, 2026-08-25:** *"we didn't actually establish in any meaningful sense that the people are
absent in that chain... I want you to actually at least make some effort in trying to do text
searches on the names or variants of the names on Wikidata... We might basically find that that
one single daughter is the only person absent in the line in Wikidata, but it's just that the
Wikidata ones are not genealogically linked."*

**She is right that nothing established the absences.** The chain was called absent because no
`P2600` *Geni.com profile ID* carries those Geni ids. That is the same reasoning that called
`Q2183430` *Benedicta Ebbesdotter of Hvide* absent while she sat in our store with thirty
properties — **absence of a Geni id is not absence of an item.**

Two ways a chain member could be present and invisible, and this file supports both:

**1. Under a name we have not looked for.** `Lagmann Gunnbjørn Toresson Tengs` might be
`Gunnbjørn Toresson` or `Gunnbjørn på Tengs` on Wikidata. Names are useless for *deciding*
identity — `CLAUDE.md` deleted a module for that and it stays deleted — but they are exactly right
for *finding candidates a human then judges*, which is what Emma asked for.

**2. Through another genealogy database.** Wikidata carries a dozen genealogical identifiers, and
they cross-reference each other. Emma: *"I think Wikidata does the best at entity resolution
across different genealogical databases... if those things have cross-references with Geni, we
could potentially go down that chain."* An item with a Genealogics or Rodovid id for a person our
chain names is the same evidence a `P2600` would be, arriving by a different route.

Identifiers pulled, chosen from what actually appears on medieval Scandinavian nobility in this
store:

| property | database |
| --- | --- |
| `P2600` | Geni.com |
| `P1819` | Genealogics |
| `P1185` | Rodovid |
| `P7929` | Geneanet |
| `P8172` | Roglo |
| `P4159` | WeRelate |
| `P535` | Find a Grave |
| `P3217` | Sandrart |
| `P9324` | Norwegian historical population register |
| `P4638` | The Peerage |
| `P3222` | NE.se |
| `P646` | Freebase |

Output is one row per item, tab-separated, with labels and aliases joined by `|`:

    qid  en  mul  no  nb  sv  da  aliases  ids

`ids` is `prop=value` pairs joined by `;`.

Writes `out/wikidata/labels.tsv`. Reads only the store; makes no request.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
DEST = ROOT / "out" / "wikidata" / "labels.tsv"

LANGS = ("en", "mul", "no", "nb", "sv", "da")
IDS = ("P2600", "P1819", "P1185", "P7929", "P8172", "P4159", "P535",
       "P3217", "P9324", "P4638", "P3222", "P646")


def clean(text):
    return (text or "").replace("\t", " ").replace("\n", " ").replace("|", "/").strip()


def main():
    shards = sorted(STORE.glob("items-*.jsonl.gz"))
    print(f"{len(shards)} shards")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    items = rows = 0
    with open(DEST, "w", encoding="utf-8", newline="\n") as out:
        out.write("qid\t" + "\t".join(LANGS) + "\taliases\tids\n")
        for n, shard in enumerate(shards, 1):
            with gzip.open(shard, "rt", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("{"):
                        continue
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    qid = item.get("id")
                    if not qid:
                        continue
                    items += 1
                    labels = item.get("labels", {})
                    cols = [clean(labels.get(l, {}).get("value")) for l in LANGS]
                    # Any label at all, in any language, as a fallback for the search.
                    if not any(cols):
                        first = next((v.get("value") for v in labels.values()), "")
                        cols[0] = clean(first)
                    al = []
                    for vs in item.get("aliases", {}).values():
                        for a in vs:
                            v = clean(a.get("value"))
                            if v and v not in al:
                                al.append(v)
                    claims = item.get("claims", {})
                    ids = []
                    for p in IDS:
                        for st in claims.get(p, []):
                            dv = st["mainsnak"].get("datavalue", {}).get("value")
                            if isinstance(dv, str):
                                ids.append(f"{p}={clean(dv)}")
                    if not any(cols) and not al and not ids:
                        continue
                    out.write(qid + "\t" + "\t".join(cols) + "\t"
                              + "|".join(al[:12]) + "\t" + ";".join(ids) + "\n")
                    rows += 1
            if n % 300 == 0:
                print(f"  {n}/{len(shards)} shards, {items:,} items, {rows:,} written",
                      flush=True)
    print(f"\n{items:,} items read, {rows:,} written")
    print(f"wrote {DEST} in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
