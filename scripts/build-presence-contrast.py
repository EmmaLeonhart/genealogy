"""People imported far less often than the people standing next to them.

Emma, 2026-08-22: "this isn't to say people very central to areas with only one
export to them. It's just people central to areas with few exports and,
particularly, people who are starkly imported less than the people around them.
If there's a section in the medieval tree where there's a person born in the
year 500 that was imported exactly once and everybody around them was imported
five times, they are an example of this."

That is a LOCAL CONTRAST, not absolute thinness, and it is a different
instrument from `genimerge.density`. Density asks "how many exports reached
this neighbourhood"; this asks "how far below its own neighbourhood does this
person sit". A person on 1 among neighbours on 5 scores 4 and is interesting.
A person on 1 among neighbours on 1 scores 0 and is just an unexplored region,
which density already ranks.

Why the contrast should predict yield: every export is a breadth-first ball, so
a person surrounded by well-covered people who is themselves barely covered is
usually sitting just outside where the balls stopped -- there is structure
behind them that nothing has walked. Untested; this run is the test.

Writes reports/presence-contrast.csv (every person with contrast >= 2) and
reports/presence-contrast.md (the pre-1600 and undated head of it).
"""
import sys, re, csv, collections
sys.path.insert(0, 'src')
sys.stdout.reconfigure(encoding='utf-8')
from genimerge import sources
from genimerge.dates import parse_date

XR = re.compile(r'^0 (@I\d+@) INDI')
MIN_CONTRAST = 2

def main():
    exports = sources.find_exports()
    print(f'{len(exports)} exports', flush=True)

    # ---- presence: how many exports hold each person ----------------------
    presence = collections.Counter()
    for p in exports:
        seen = set()
        with open(p, encoding='utf-8', errors='replace') as f:
            for line in f:
                m = XR.match(line)
                if m:
                    seen.add(m.group(1))
        presence.update(seen)
    print(f'{len(presence)} distinct people', flush=True)

    # ---- adjacency + birth years from the merged tree ---------------------
    fam_par = collections.defaultdict(list)   # fam -> [parents]
    fam_chil = collections.defaultdict(list)  # fam -> [children]
    i_fams = collections.defaultdict(list)
    i_famc = collections.defaultdict(list)
    year = {}
    cur = kind = None
    inbirt = False
    with open('out/merged.ged', encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('0 @'):
                parts = line.split()
                cur, kind = parts[1], (parts[2].strip() if len(parts) > 2 else '')
                inbirt = False
            elif cur and line.startswith('1 '):
                tag, _, val = line[2:].strip().partition(' ')
                if kind == 'FAM':
                    if tag in ('HUSB', 'WIFE'): fam_par[cur].append(val)
                    elif tag == 'CHIL': fam_chil[cur].append(val)
                elif kind == 'INDI':
                    inbirt = (tag == 'BIRT')
                    if tag == 'FAMS': i_fams[cur].append(val)
                    elif tag == 'FAMC': i_famc[cur].append(val)
            elif cur and kind == 'INDI' and inbirt and line.startswith('2 DATE '):
                d = parse_date(line[7:].strip())
                if d and d.year is not None: year[cur] = d.year
                inbirt = False
    print(f'{len(year)} people carry a birth year', flush=True)

    def neighbours(i):
        out = set()
        for fc in i_famc.get(i, ()):
            out |= set(fam_par.get(fc, ())) | set(fam_chil.get(fc, ()))
        for fs in i_fams.get(i, ()):
            out |= set(fam_par.get(fs, ())) | set(fam_chil.get(fs, ()))
        out.discard(i)
        return out

    rows = []
    for i in presence:
        ns = neighbours(i)
        if len(ns) < 2:            # one edge is not a neighbourhood
            continue
        vals = sorted(presence.get(n, 0) for n in ns)
        med = vals[len(vals) // 2]
        contrast = med - presence[i]
        if contrast >= MIN_CONTRAST:
            rows.append((contrast, presence[i], med, len(ns), i, year.get(i)))
    rows.sort(reverse=True)
    print(f'{len(rows)} people sit {MIN_CONTRAST}+ below their neighbourhood median', flush=True)

    gid = lambda x: x.strip('@').lstrip('I')
    with open('reports/presence-contrast.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['contrast', 'own_presence', 'neighbour_median', 'neighbours',
                    'geni_id', 'birth_year'])
        for c, own, med, n, i, y in rows:
            w.writerow([c, own, med, n, gid(i), y if y is not None else ''])
    print('wrote reports/presence-contrast.csv')

if __name__ == '__main__':
    main()
