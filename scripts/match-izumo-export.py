"""Match one export's people against the Izumo roster on the REGNAL NUMBER.

    python scripts/match-izumo-export.py exports/izumo/export-Forest-<id>.ged

`walk-izumo-geni.py` matches romanised names against `out/merged.ged`, which
means it needs a re-merge before it can see a fresh export and it carries all the
risk of name matching. This does neither.

**Geni writes the regnal number inside the name** -- `Harutaka 64 /Kitajima/`,
`Takamune /Senge/` -- and the roster carries it in its own column. Number plus
lineage is an exact join and immune to romanisation: the 2008 Japanese, 2011
English and 2026 additions spell these men differently and number them
identically. Where Geni omits the number (the two men of the 1340 split are
written bare), the surname plus given name is used, tokens matching exactly.

Reports three populations: rostered people this export holds, rostered people it
does not, and numbered Izumo/Senge/Kitajima people in the export that the roster
does not list -- the last being succession the Shinto-wiki chart stops short of.
"""
import sys
import re
import csv
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

LINEAGES = ('Senge', 'Kitajima', 'Izumo-kokuso', 'Izumo')


def norm(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^0-9a-zA-Z]+', '', t).lower()


def parse_name(raw):
    """`Harutaka 64 /Kitajima/` -> ('harutaka', 64, 'Kitajima')."""
    m = re.match(r'^(.*?)\s*/([^/]*)/\s*$', raw)
    given, surname = (m.group(1), m.group(2)) if m else (raw, '')
    num = None
    toks = []
    for t in given.split():
        if t.isdigit():
            num = int(t)
        else:
            toks.append(t)
    return norm(' '.join(toks)), num, surname.strip()


def main():
    path = sys.argv[1]

    people = {}          # geni id -> (given, regnal, surname, raw)
    cur = None
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('0 @I'):
                cur = line.split()[1][2:-1]
            elif line.startswith('0 '):
                cur = None
            elif cur and line.startswith('1 NAME ') and cur not in people:
                raw = line[7:].strip()
                g, n, s = parse_name(raw)
                people[cur] = (g, n, s, raw)

    print(f'{len(people)} people in {path.split("/")[-1]}')

    by_num = {}          # (lineage, regnal) -> [ids]
    by_name = {}         # (lineage, given) -> [ids]
    for gid, (g, n, s, _) in people.items():
        lin = next((L for L in LINEAGES if L.lower() in s.lower()), None)
        if not lin:
            continue
        if lin == 'Izumo-kokuso':
            lin = 'Izumo'
        if n is not None:
            by_num.setdefault((lin, n), []).append(gid)
        if g:
            by_name.setdefault((lin, g), []).append(gid)

    numbered = sum(len(v) for v in by_num.values())
    print(f'{numbered} of them carry a regnal number in a lineage surname')

    roster = list(csv.DictReader(open('reports/izumo-roster.tsv', encoding='utf-8'),
                                 delimiter='\t'))
    hit, miss = [], []
    used = set()
    for row in roster:
        lin = (row.get('lineage') or '').strip()
        if lin not in ('Senge', 'Kitajima', 'Izumo'):
            continue
        name = row.get('name') or ''
        regnal = (row.get('regnal') or '').strip()
        given = norm(name.split(' no ')[-1]) if ' no ' in name else norm(name)

        ids = []
        how = ''
        if regnal.isdigit() and (lin, int(regnal)) in by_num:
            ids = by_num[(lin, int(regnal))]
            how = f'regnal {regnal}'
        elif (lin, given) in by_name:
            ids = by_name[(lin, given)]
            how = 'name'

        if ids:
            used.update(ids)
            hit.append((regnal, lin, name, ';'.join(ids), how))
        else:
            miss.append((regnal, lin, name))

    print(f'\n{len(hit)} rostered lineage people found in this export, {len(miss)} not')
    print('\nfound:')
    for r, lin, name, ids, how in hit:
        print(f'  {r or "-":>3}  {lin:<9} {name:<32} {ids}  [{how}]')
    print('\nnot in this export:')
    for r, lin, name in miss:
        print(f'  {r or "-":>3}  {lin:<9} {name}')

    extra = sorted(
        (people[g][1], people[g][2], people[g][3], g)
        for k, v in by_num.items() for g in v if g not in used)
    print(f'\n{len(extra)} numbered lineage people in the export the roster does NOT list:')
    for n, s, raw, g in extra:
        print(f'  {n:>3}  {s:<12} {raw:<34} {g}')

    # The pairings, for a P2600 batch once this repo's start date passes. A row
    # with more than one Geni id is a duplicate set on Geni -- emitted as it is,
    # because a second P2600 on one item is the correct representation of that
    # and the merges are Emma's.
    qid_of = {(r.get('regnal', '').strip(), r.get('name', '')): (r.get('qid') or '').strip()
              for r in roster}
    out = 'reports/izumo-p2600-pairs.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'regnal', 'lineage', 'name', 'geni_ids', 'matched_on'])
        n = 0
        for r, lin, name, ids, how in hit:
            q = qid_of.get((r, name), '')
            if not q:
                continue
            w.writerow([q, r, lin, name, ids, how])
            n += 1
    print(f'\nwrote {out} -- {n} of the {len(hit)} carry a Wikidata item to link')


if __name__ == '__main__':
    main()
