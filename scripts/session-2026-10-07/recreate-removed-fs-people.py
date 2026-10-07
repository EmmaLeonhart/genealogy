"""New items for the FamilySearch people whose ids were removed from wrong items (Emma, 2026-10-07).

Emma, 2026-10-07: "And recreate new items for the familysearch people", then by AskUserQuestion
"All removed, ever": every FamilySearch id any removal file took off an item. And: "sometimes the
family search people are not really disputed parents because the disputed parents are only like in
one generation". So a new item links ONLY to relatives whose own FamilySearch id is on an item live
right now (reviewed ids), never through the positional walk's pairs: the dispute stays in the one
generation where the trees differ, and above and below it the FamilySearch record joins our items
wherever its ids already sit.

Skipped (carried, with the reason): an id that is on any item today (re-added, or held elsewhere),
an id not in the FamilySearch corpus, a person the pipeline's own gates refuse (no label, NN, no
ja/zh/ko), and a person with no relative on Wikidata (an isolate, never shipped).
Labels, descriptions, dates and the frozen description logic come from build-familysearch-day.py's
own functions; this file only chooses who and links them.

    python scripts/session-2026-10-07/recreate-removed-fs-people.py
"""
import csv
import importlib.util
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
fsday = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fsday)
import descriptions  # noqa: E402  (on sys.path through fsday)
import qs_v1  # noqa: E402

OUT = ROOT / "reports" / "familysearch-recreate-removed-2026-10-07.qs"
CARRY = ROOT / "reports" / "familysearch-recreate-removed-2026-10-07-carried.tsv"
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
REMOVAL = re.compile(r'^-(Q\d+)\tP2889\t"([^"]+)"')


def removed_ids():
    out = {}
    files = sorted((ROOT / "reports").glob("familysearch-id-review-removals-*.qs")) + [
        ROOT / "reports" / n for n in ("wikidata-p2889-removals.qs", "wikidata-p2889-reremovals.qs",
                                       "zipper-review-id-removals-2026-10-05.qs", "wikidata-q272148-undo.qs")]
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            m = REMOVAL.match(line)
            if m:
                out.setdefault(m.group(2), m.group(1))
    return out


def live_holders():
    """`{fs_id: qid}` for every item carrying P2889 now (query service)."""
    q = "SELECT ?item ?id WHERE { ?item wdt:P2889 ?id }"
    url = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)
    for i in range(5):
        try:
            data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300))
            break
        except Exception:
            time.sleep(20 * (i + 1))
    else:
        sys.exit("query service failed")
    out = {}
    for b in data["results"]["bindings"]:
        out.setdefault(b["id"]["value"], b["item"]["value"].rsplit("/", 1)[1])
    return out


def main():
    G = fsday.garborg()
    table, qs = G.translit(), G.qs
    removed = removed_ids()
    holders = live_holders()
    people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    key_of, by_fs = {}, {}
    for key, rec in people.items():
        fs = rec["fs_id"]
        if fs:
            key_of.setdefault(fs, []).append(key)
            by_fs.setdefault(fs, rec)

    def item_of(key):
        fs = people.get(key, {}).get("fs_id") if key else None
        return holders.get(fs) if fs and fs not in removed else None

    lines = ["# New items for FamilySearch people whose ids were removed from wrong items (Emma, 2026-10-07).",
             "# Linked only to relatives whose own FamilySearch id is live on an item. Run with Run, never background.", ""]
    carried, made = [], 0
    for fs in sorted(removed):
        if fs in holders:
            carried.append((fs, "", f"on an item today: {holders[fs]}"))
            continue
        if fs not in by_fs:
            carried.append((fs, "", "not in the FamilySearch corpus"))
            continue
        rec = by_fs[fs]
        primary, aliases = fsday.name_plan(rec)
        if not primary or primary == fsday.labelmod.UNNAMED_MARKER or fsday.labelmod.leads_with_a_marker(primary) \
                or primary.split()[-1] == fsday.labelmod.UNNAMED_MARKER:
            carried.append((fs, primary or "", "no usable name (redacted or NN)"))
            continue
        primary = qs(primary)
        ja, zh, ko = G.label_in(primary, table)
        if not ja:
            carried.append((fs, primary, "GATE: no ja/zh/ko label"))
            continue
        desc = G.life_description(
            {"birth_date_raw": fsday.to_gedcom(rec["birth_date"]), "death_date_raw": fsday.to_gedcom(rec["death_date"])},
            {"birth_place": rec["birth_place"], "death_place": rec["death_place"]})
        desc = desc or descriptions.id_description(fsday.FS_PROP, fs)
        block = ["CREATE", f'LAST\tLmul\t"{primary}"', f'LAST\tLen\t"{primary}"', f'LAST\tDen\t"{qs(desc)}"',
                 f'LAST\tLja\t"{ja}"', f'LAST\tLzh\t"{zh}"', f'LAST\tLko\t"{ko}"']
        block += [f'LAST\tAmul\t"{qs(a)}"' for a in aliases]
        block.append(f"LAST\tP31\t{G.HUMAN}")
        if rec["sex"] in G.SEX:
            block.append(f"LAST\tP21\t{G.SEX[rec['sex']]}")
        block.append(f'LAST\tP2889\t"{fs}"')
        ref = f'\tS2889\t"{fs}"'
        for prop, raw in (("P569", rec["birth_date"]), ("P570", rec["death_date"])):
            _g, iso, prec, mod, end = fsday.date_row(raw)
            if iso and prec:
                block.append(f"LAST\t{prop}\t{iso}/{prec}{fsday.date_quals(mod, iso, prec, end)}{ref}")
        links, back = set(), []
        for key in key_of[fs]:
            for prop, target, other in (("P22", father.get(key), "P40"), ("P25", mother.get(key), "P40")):
                q = item_of(target)
                if q and (prop, q) not in links:
                    links.add((prop, q)); block.append(f"LAST\t{prop}\t{q}{ref}"); back.append((q, other))
            for sp in sorted(spouses.get(key, ())):
                q = item_of(sp)
                if q and ("P26", q) not in links:
                    links.add(("P26", q)); block.append(f"LAST\tP26\t{q}{ref}"); back.append((q, "P26"))
            for kid in sorted(children.get(key, ())):
                q = item_of(kid)
                if q and ("P40", q) not in links:
                    links.add(("P40", q)); block.append(f"LAST\tP40\t{q}{ref}")
                    if rec["sex"] in ("M", "F"):
                        back.append((q, "P22" if rec["sex"] == "M" else "P25"))
        if not links:
            carried.append((fs, primary, "no relative's FamilySearch id is live on an item: would be an isolate"))
            continue
        block = [f"# {fs}, removed from {removed[fs]}"] + block + [f"{s}\t{p}\tLAST{ref}" for s, p in back]
        lines += block + [""]
        made += 1
    collided = descriptions.deduplicate(lines, fsday.FS_PROP)
    lines, orphaned = qs_v1.drop_orphaned_creations(lines)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    with open(CARRY, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["fs_id", "label", "reason"])
        w.writerows(carried)
    print(f"{len(removed)} removed ids; {len(holders)} live P2889 holders; {made} created; "
          f"{len(carried)} carried; {collided} descriptions deduplicated; {len(orphaned)} orphans dropped")
    reasons = {}
    for _f, _l, r in carried:
        k = r.split(":")[0]
        reasons[k] = reasons.get(k, 0) + 1
    for k, v in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  {v:4}  {k}")


if __name__ == "__main__":
    main()
