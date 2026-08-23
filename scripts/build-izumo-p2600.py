"""Izumo `P2600` pairings, joined on the Wikidata URL in the Geni About Me.

    python scripts/build-izumo-p2600.py

`reports/geni-qid-links.tsv` holds the identifier Emma wrote into these profiles
by hand. This intersects it with `reports/izumo-roster.tsv` and writes
`reports/izumo-p2600-pairs.tsv`: for each roster person, the Geni profile whose
About Me points at that person's Wikidata item.

**Nothing here looks at a name.** The previous version of this file joined on the
regnal number Geni writes inside the name, which worked for the three lineage
surnames and produced nonsense outside them. Wikidata does not carry those
numbers at all, so that was never a join to Wikidata.

A QID sitting on more than one Geni profile is Geni's duplicate-profile
situation. Both ids go in the row: `P2600` is multi-valued and a second one is
the correct representation, per `CLAUDE.md`. The merges are Emma's.
"""
import sys
import csv
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


def load_links():
    """QID -> [geni ids], from the About Me URLs."""
    q2g = {}
    path = ROOT / 'reports' / 'geni-qid-links.tsv'
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            for q in row['qids'].split(';'):
                if q:
                    q2g.setdefault(q, []).append(row['geni_id'])
    return q2g


def main():
    q2g = load_links()
    print(f'{len(q2g)} QIDs linked from a Geni About Me')

    roster = list(csv.DictReader(
        open(ROOT / 'reports' / 'izumo-roster.tsv', encoding='utf-8'), delimiter='\t'))
    with_qid = [r for r in roster if (r.get('qid') or '').strip()]
    print(f'{len(roster)} rostered, {len(with_qid)} carrying a Wikidata item')

    hit, miss = [], []
    for r in with_qid:
        q = r['qid'].strip()
        ids = q2g.get(q)
        (hit if ids else miss).append((r, ids))

    print(f'\n{len(hit)} joined, {len(miss)} rostered items with no Geni profile linking them')

    by_lineage = {}
    for r, ids in hit:
        by_lineage[r.get('lineage', '')] = by_lineage.get(r.get('lineage', ''), 0) + 1
    for lin, n in sorted(by_lineage.items(), key=lambda kv: -kv[1]):
        print(f'  {lin or "(none)":<10} {n}')

    dupes = [(r, ids) for r, ids in hit if len(ids) > 1]
    if dupes:
        print(f'\n{len(dupes)} roster people whose QID sits on more than one Geni profile '
              f'-- both ids emitted, merges are Emma\'s:')
        for r, ids in dupes:
            print(f'  {r["name"]:<34} {r["qid"]:<12} {";".join(ids)}')

    out = ROOT / 'reports' / 'izumo-p2600-pairs.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'regnal', 'lineage', 'name', 'geni_ids'])
        for r, ids in hit:
            w.writerow([r['qid'].strip(), (r.get('regnal') or '').strip(),
                        r.get('lineage', ''), r.get('name', ''), ';'.join(ids)])
    print(f'\nwrote {out.relative_to(ROOT)} -- {len(hit)} rows')

    unlinked = ROOT / 'reports' / 'izumo-unlinked.tsv'
    with open(unlinked, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'regnal', 'lineage', 'name'])
        for r, _ in miss:
            w.writerow([r['qid'].strip(), (r.get('regnal') or '').strip(),
                        r.get('lineage', ''), r.get('name', '')])
    print(f'wrote {unlinked.relative_to(ROOT)} -- {len(miss)} rows')


if __name__ == '__main__':
    main()
