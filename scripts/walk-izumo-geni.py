"""Find the Izumo clan's Geni-side lineage by walking our own tree.

Emma's seed, 6000000012789160423, is already in the merged tree, so the Geni
profiles for this clan do not have to be searched for one at a time -- they are
reachable by walking outward from her seed.

Matching is by NAME against the roster, and that is only defensible here because
the names are unique in a way `Adolf Ludvig Piper` was not: `Kushichitoriuminomikoto`
and `Izumo no Ihohiku` have no namesakes. Every match is still reported with the
graph distance from the seed so a wrong one is visible, and a roster name matching
more than one profile in the ball is reported as AMBIGUOUS rather than resolved.

Writes reports/izumo-geni-candidates.tsv. Creates nothing and edits nothing.
"""
import sys, re, csv, collections, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(1 << 30)

SEED = '@I6000000012789160423@'
HOPS = int(sys.argv[1]) if len(sys.argv) > 1 else 6

roster = list(csv.DictReader(open('reports/izumo-roster.tsv', encoding='utf-8'), delimiter='\t'))
print(f'{len(roster)} rostered people')

def norm(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'\s*\([^)]*\)', '', t)
    t = re.sub(r'[^0-9a-zA-Z　-鿿]+', '', t)
    return t.lower()

fam_par = collections.defaultdict(list); fam_chil = collections.defaultdict(list)
i_fams = collections.defaultdict(list); i_famc = collections.defaultdict(list)
names = {}
cur = kind = None
with open('out/merged.ged', encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('0 @'):
            p = line.split(); cur, kind = p[1], (p[2].strip() if len(p) > 2 else '')
        elif cur and line.startswith('1 '):
            tag, _, val = line[2:].strip().partition(' ')
            if kind == 'FAM':
                if tag in ('HUSB', 'WIFE'): fam_par[cur].append(val)
                elif tag == 'CHIL': fam_chil[cur].append(val)
            elif kind == 'INDI':
                if tag == 'FAMS': i_fams[cur].append(val)
                elif tag == 'FAMC': i_famc[cur].append(val)
                elif tag == 'NAME': names.setdefault(cur, []).append(val.replace('/', ' ').strip())
print(f'tree loaded, {len(names)} named people')

def nbrs(i):
    o = set()
    for fc in i_famc.get(i, ()): o |= set(fam_par.get(fc, ())) | set(fam_chil.get(fc, ()))
    for fs in i_fams.get(i, ()): o |= set(fam_par.get(fs, ())) | set(fam_chil.get(fs, ()))
    o.discard(i); return o

dist = {SEED: 0}; frontier = [SEED]
for d in range(1, HOPS + 1):
    nxt = []
    for i in frontier:
        for n in nbrs(i):
            if n not in dist: dist[n] = d; nxt.append(n)
    frontier = nxt
print(f'{len(dist)} people within {HOPS} hops of the seed')

# index the ball by normalised name
idx = collections.defaultdict(list)
for x in dist:
    for nm in names.get(x, ()):
        k = norm(nm)
        if k: idx[k].append(x)

gid = lambda x: x.strip('@').lstrip('I')
rows = []; stats = collections.Counter()
for r in roster:
    k = norm(r['name'])
    hits = sorted(set(idx.get(k, ())))
    if not hits:
        stats['not in the ball'] += 1
        rows.append((r['regnal'], r['name'], r['qid'], r['lineage'], '', '', 'not found'))
    elif len(hits) == 1:
        x = hits[0]
        stats['matched'] += 1
        rows.append((r['regnal'], r['name'], r['qid'], r['lineage'],
                     gid(x), names[x][0], f'match (hop {dist[x]})'))
    else:
        stats['ambiguous'] += 1
        rows.append((r['regnal'], r['name'], r['qid'], r['lineage'],
                     ';'.join(gid(x) for x in hits), '', f'AMBIGUOUS ({len(hits)})'))

with open('reports/izumo-geni-candidates.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['regnal', 'roster_name', 'qid', 'lineage', 'geni_id', 'geni_name', 'status'])
    w.writerows(rows)
print()
for k, v in stats.most_common(): print(f'  {v:>4}  {k}')
print('\nwrote reports/izumo-geni-candidates.tsv')
print('\nfirst 25 matches:')
n = 0
for r in rows:
    if r[6].startswith('match') and n < 25:
        print(f"  {r[0] or '-':>4}  {r[1][:34]:<34} -> {r[4]}  {r[6]}")
        n += 1
