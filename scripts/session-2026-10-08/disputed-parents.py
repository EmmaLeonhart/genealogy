"""FamilySearch's parent as a second, disputed parent of an anchored child (Emma, 2026-10-07 queue item).

The shape, and only this one: a FamilySearch id R was removed from an item Q_old (the id-review removal groups),
R's person is FamilySearch's parent of a child whose FamilySearch id is live on item C, C also carries a Geni id
(the child is the anchor), and Q_old is C's father or mother on Wikidata (our parent, the Geni side). Then R gets a
new item linked to C ONLY: `P40` C, and C's `P22`/`P25` to it with `P1480` sourcing circumstances = `Q18912752`
disputed. No spouse, no parents of R: one generation, nothing positional.

Labels, descriptions and dates come from build-familysearch-day.py's own functions (the frozen logic). Every
candidate goes to the TSV; only the first --limit go into the batch ("not all at once").

    python scripts/session-2026-10-08/disputed-parents.py --limit 10
"""
import argparse
import csv
import importlib.util
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
fsday = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fsday)
spec2 = importlib.util.spec_from_file_location("recreate", ROOT / "scripts" / "session-2026-10-07" / "recreate-removed-fs-people.py")
recreate = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(recreate)
import descriptions  # noqa: E402
import qs_v1  # noqa: E402

OUT = ROOT / "reports" / "session-2026-10-08" / "disputed-parents-2026-10-08-DRAFT-not-run.qs"
LIST = ROOT / "reports" / "session-2026-10-08" / "disputed-parents-2026-10-08.tsv"
UA = {"User-Agent": "genealogy-check/1.0 (emma@topazcomputing.com)"}
DISPUTED = "\tP1480\tQ18912752"
#: Read one by one and refused, with the reason.
SKIP = {"9KM9-392": "Anders Kruckow in the mother slot, no sex on the record: a FamilySearch entry error"}


def entities(qids):
    out = {}
    qids = sorted(qids)
    for i in range(0, len(qids), 50):
        u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&props=claims&format=json&ids="
             + "|".join(qids[i:i + 50]))
        for t in range(5):
            try:
                out.update(json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["entities"])
                break
            except Exception:
                time.sleep(15 * (t + 1))
        time.sleep(0.5)
    return out


def vals(ent, prop):
    return [(s["mainsnak"].get("datavalue") or {}).get("value") for s in ent.get("claims", {}).get(prop, [])]



def same_name_item(label):
    """A live item whose label is exactly this name, or ''. A FamilySearch parent can already have an item of its
    own (Torgrim Ormsson `Q141571152`), and only the FamilySearch id was checked before (2026-10-08)."""
    u = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&type=item&language=en&limit=10&format=json&search="
         + urllib.parse.quote(label))
    for t in range(5):
        try:
            hits = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["search"]
            break
        except Exception:
            time.sleep(10 * (t + 1))
    else:
        return "lookup failed"
    return next((h["id"] for h in hits if (h.get("label") or "").casefold() == label.casefold()), "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()
    G = fsday.garborg()
    table, qs = G.translit(), G.qs
    removed = recreate.removed_ids()
    holders = recreate.live_holders()
    people, father, mother, _spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    by_fs, keys_of = {}, {}
    for key, rec in people.items():
        if rec["fs_id"]:
            by_fs.setdefault(rec["fs_id"], rec)
            keys_of.setdefault(rec["fs_id"], []).append(key)

    # (R, child item C, child fs, prop) for every removed parent whose FamilySearch child is live on an item
    pairs = []
    for r, q_old in removed.items():
        if r in holders or r not in by_fs:
            continue
        for key in keys_of[r]:
            for kid in children.get(key, ()):
                kfs = people.get(kid, {}).get("fs_id")
                c = holders.get(kfs) if kfs and kfs not in removed else None
                if c:
                    prop = "P22" if (father.get(kid) == key) else "P25" if (mother.get(kid) == key) else None
                    if prop:
                        pairs.append((r, q_old, c, kfs, prop))
    pairs = sorted(set(pairs))
    ents = entities({c for _r, _q, c, _k, _p in pairs})
    rows, chosen = [], []
    for r, q_old, c, kfs, prop in pairs:
        ent = ents.get(c, {})
        parents = {v.get("id") for p in ("P22", "P25") for v in vals(ent, p) if isinstance(v, dict)}
        why = ("child has no Geni id" if not vals(ent, "P2600") else
               "the removed id's item is not the child's parent" if q_old not in parents else "")
        rows.append((r, q_old, c, kfs, prop, why or "candidate"))
        if not why:
            chosen.append((r, q_old, c, kfs, prop))

    lines = ["# FamilySearch's parent as a second, disputed parent of an anchored child (Emma, 2026-10-07).",
             "# One generation only: each new item links to the child and nothing else. Run with Run, never background.", ""]
    made, done = 0, set()
    for r, q_old, c, kfs, prop in chosen:
        if made >= args.limit or r in done:
            continue
        rec = by_fs[r]
        primary, aliases = fsday.name_plan(rec)
        if not primary or primary == fsday.labelmod.UNNAMED_MARKER or fsday.labelmod.leads_with_a_marker(primary) \
                or primary.split()[-1] == fsday.labelmod.UNNAMED_MARKER:
            rows.append((r, q_old, c, kfs, prop, "skipped: no usable name"))
            continue
        # First groups touch our own items only (Emma: risky, not all at once); a name in capitals is a place or a
        # note more often than a name (MADLA); a man's name in the mother slot is a FamilySearch entry error.
        if not (c.startswith("Q141") and len(c) == 10):
            rows.append((r, q_old, c, kfs, prop, "later: the child is an established item other editors keep"))
            continue
        if primary.isupper():
            rows.append((r, q_old, c, kfs, prop, "skipped: label in capitals"))
            continue
        if r in SKIP:
            rows.append((r, q_old, c, kfs, prop, "skipped: " + SKIP[r]))
            continue
        if (prop == "P25" and rec["sex"] == "M") or (prop == "P22" and rec["sex"] == "F"):
            rows.append((r, q_old, c, kfs, prop, "skipped: sex does not fit the parent slot"))
            continue
        twin = same_name_item(primary)
        if twin:
            rows.append((r, q_old, c, kfs, prop, f"skipped: an item with this name exists ({twin}); review by hand"))
            continue
        primary = qs(primary)
        ja, zh, ko = G.label_in(primary, table)
        if not ja:
            rows.append((r, q_old, c, kfs, prop, "skipped: no ja/zh/ko label"))
            continue
        desc = G.life_description(
            {"birth_date_raw": fsday.to_gedcom(rec["birth_date"]), "death_date_raw": fsday.to_gedcom(rec["death_date"])},
            {"birth_place": rec["birth_place"], "death_place": rec["death_place"]})
        desc = desc or descriptions.id_description(fsday.FS_PROP, r)
        ref = f'\tS2889\t"{r}"'
        block = [f"# {r}: FamilySearch's {'father' if prop == 'P22' else 'mother'} of {c} (FamilySearch {kfs}); "
                 f"the Geni-side parent is {q_old}",
                 "CREATE", f'LAST\tLmul\t"{primary}"', f'LAST\tLen\t"{primary}"', f'LAST\tDen\t"{qs(desc)}"',
                 f'LAST\tLja\t"{ja}"', f'LAST\tLzh\t"{zh}"', f'LAST\tLko\t"{ko}"']
        block += [f'LAST\tAmul\t"{qs(a)}"' for a in aliases]
        block.append(f"LAST\tP31\t{G.HUMAN}")
        if rec["sex"] in G.SEX:
            block.append(f"LAST\tP21\t{G.SEX[rec['sex']]}")
        block.append(f'LAST\tP2889\t"{r}"')
        for p, raw in (("P569", rec["birth_date"]), ("P570", rec["death_date"])):
            _g, iso, prec, mod, end = fsday.date_row(raw)
            if iso and prec:
                block.append(f"LAST\t{p}\t{iso}/{prec}{fsday.date_quals(mod, iso, prec, end)}{ref}")
        block.append(f"LAST\tP40\t{c}{ref}")
        block.append(f"{c}\t{prop}\tLAST{DISPUTED}{ref}")
        lines += block + [""]
        done.add(r)
        made += 1
        rows.append((r, q_old, c, kfs, prop, "in this batch"))
    descriptions.deduplicate(lines, fsday.FS_PROP)
    lines, _orph = qs_v1.drop_orphaned_creations(lines)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    with open(LIST, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["removed_fs", "removed_from", "child_item", "child_fs", "prop", "status"])
        w.writerows(rows)
    print(f"{len(removed)} removed ids; {len(pairs)} parent-of-live-child pairs; {len(chosen)} candidates; "
          f"{made} in the batch")


if __name__ == "__main__":
    sys.exit(main())
