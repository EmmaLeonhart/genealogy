"""Resolve the Izumo kokuso by POSITION in the succession, not by spelling.

    python scripts/walk-izumo-succession.py

The roster and Geni romanise these men differently enough that name matching is
hopeless and, worse, *silently* hopeless. Three separate times on 2026-08-23 a
person reported absent turned out to be sitting in the corpus under another
spelling:

    roster                      Geni                         regnal
    Kushifusakinomikoto         Kushimikasaki-no-mikoto       5
    Kushitsukinomikoto          Kishitsuki-no-mikoto          6
    Kushichitoriuminomikoto     Kushimikatomi-no-mikoto       7

Every one of them is the same man in the same seat. So the join is the seat.

**Walk UP, never down.** A person has exactly one father, so each step up the
`FAMC` chain is unambiguous and decrements the regnal number by one. Walking down
would have to choose among children, which is a guess. Anchors are the kokuso the
regnal-number join already resolved exactly, and each contributes the chain above
itself; where two anchors' chains overlap they must agree, and a disagreement is
reported rather than silently preferred.

This creates nothing and edits nothing. It writes
`reports/izumo-succession-chain.tsv`.
"""
import sys
import csv
import collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
sys.stdout.reconfigure(encoding='utf-8')

from genimerge.sources import find_exports  # noqa: E402

#: Kokuso resolved exactly by the regnal-number join in `match-izumo-export.py`,
#: each `geni id -> regnal`. These are the feet of the chains walked upward.
ANCHORS = {
    '6000000012789332311': 8,    # Kushida-no-mikoto
    '6000000012789365875': 9,    # Chiri-no-mikoto
    '6000000227332010844': 12,   # Ukatsu Kunu
    '6000000227332010837': 13,   # Okimimi / Kanesune
    '6000000227332000825': 15,   # Mishima
    '6000000227332013831': 16,   # Ou
    '6000000227331911824': 17,   # Miyamukasu
    '6000000227331940873': 18,   # Funin -- the first with the Izumo surname
}


def load():
    """Father-of and name, over the whole corpus."""
    father = {}
    name = {}
    fam_husb = {}
    child_fam = collections.defaultdict(list)

    for p in find_exports():
        cur = kind = None
        with open(p, encoding='utf-8', errors='replace') as f:
            for line in f:
                if line.startswith('0 @'):
                    parts = line.split()
                    cur = parts[1][2:-1]   # @I123@ / @F123@ -> 123
                    kind = parts[2].strip() if len(parts) > 2 else ''
                elif cur and line.startswith('1 '):
                    tag, _, val = line[2:].strip().partition(' ')
                    if kind == 'FAM':
                        if tag == 'HUSB':
                            fam_husb[cur] = val[2:-1]
                    elif kind == 'INDI':
                        if tag == 'NAME' and cur not in name:
                            name[cur] = val.strip()
                        elif tag == 'FAMC':
                            child_fam[cur].append(val[2:-1])

    for child, fams in child_fam.items():
        for fam in fams:
            if fam in fam_husb:
                father[child] = fam_husb[fam]
                break
    return father, name


def main():
    father, name = load()
    print(f'{len(name)} people, {len(father)} with a father')

    # Each anchor walks its own chain. Comparing them afterwards is the whole
    # point: two chains landing DIFFERENT people on the same seat is the
    # duplicate-profile problem Emma described -- the clan is on Geni three times
    # over -- and it is flagged, never resolved here. The merges are hers.
    chains = {}
    for start, regnal in sorted(ANCHORS.items(), key=lambda kv: kv[1]):
        gid, r, walk, seen = start, regnal, {}, set()
        while gid and r >= 1 and gid not in seen:
            walk[r] = gid
            seen.add(gid)
            gid = father.get(gid)
            r -= 1
        chains[start] = walk

    by_regnal = collections.defaultdict(set)
    for walk in chains.values():
        for r, gid in walk.items():
            by_regnal[r].add(gid)

    contested = sorted(r for r, ids in by_regnal.items() if len(ids) > 1)

    roster = list(csv.DictReader(open('reports/izumo-roster.tsv', encoding='utf-8'),
                                 delimiter='\t'))
    rows, absent = [], []
    for row in roster:
        r = (row.get('regnal') or '').strip()
        if not r.isdigit() or int(r) > 18:
            continue
        ids = sorted(by_regnal.get(int(r), ()))
        if ids:
            rows.append((int(r), row.get('name'), (row.get('qid') or '').strip(),
                         ';'.join(ids), ' / '.join(name.get(g, '') for g in ids),
                         'CONTESTED' if len(ids) > 1 else 'single chain'))
        else:
            absent.append((int(r), row.get('name'), (row.get('qid') or '').strip()))

    rows.sort()
    absent.sort()
    print(f'\nseats 1-18 resolved by walking up: {len(rows)} of {len(rows) + len(absent)}')
    for r, nm, q, ids, geni, how in rows:
        print(f'  {r:>3}  {nm:<34} {q:<12} {how:<12} {geni}')
    if absent:
        print('\nstill absent:')
        for r, nm, q in absent:
            print(f'  {r:>3}  {nm:<34} {q}')
    if contested:
        print(f'\n{len(contested)} seats are CONTESTED -- two chains, different people: '
              + ', '.join(str(r) for r in contested))
        print('  Duplicate profile sets that disagree about who sits where.')
        print('  Flagged for Emma. Not resolved here, and not emitted as a pairing.')

    out = 'reports/izumo-succession-chain.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['regnal', 'roster_name', 'qid', 'geni_ids', 'geni_names', 'status'])
        for r, nm, q, ids, geni, how in rows:
            w.writerow([r, nm, q, ids, geni, how])
    print(f'\nwrote {out} -- {len(rows)} rows')


if __name__ == '__main__':
    main()
