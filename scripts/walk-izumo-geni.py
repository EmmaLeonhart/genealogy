"""Find the Izumo clan's Geni-side lineage by walking our own tree.

Emma's seed, 6000000012789160423, is already in the merged tree, so the Geni
profiles for this clan do not have to be searched for one at a time -- they are
reachable by walking outward from her seed.

Matching is by NAME against the roster, and that is only defensible here because
the names are unique in a way `Adolf Ludvig Piper` was not: `Kushichitoriuminomikoto`
and `Izumo no Ihohiku` have no namesakes. Every match is still reported with the
graph distance from the seed so a wrong one is visible, and a roster name matching
more than one profile in the ball is reported as AMBIGUOUS rather than resolved.

**Word order is the whole difficulty and the first run got it wrong.** The roster
writes `Senge no Takamune`, the Japanese order with the `no` particle; Geni writes
`Takamune Senge`, given name first. A plain normalised comparison misses every
one of them, which is why the first run reported 10 of 214 present when
Takamune Senge, Sadataka Kitajima, Naokuni Senge and Kunimaro Senge were all
sitting in the tree. `variants()` generates both orders so the match is on the
same name written two ways, not on a fuzzy similarity -- the tokens must still
agree exactly.

Writes reports/izumo-geni-candidates.tsv. Creates nothing and edits nothing.
"""
import sys, re, csv, collections, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(1 << 30)

SEED = '@I6000000012789160423@'
HOPS = int(sys.argv[1]) if len(sys.argv) > 1 else 6

roster = list(csv.DictReader(open('reports/izumo-roster.tsv', encoding='utf-8'), delimiter='\t'))
print(f'{len(roster)} rostered people')

def _clean(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'\s*\([^)]*\)', '', t)
    t = re.sub(r'<[^>]*>', ' ', t)
    return t

def norm(t):
    return re.sub(r'[^0-9a-zA-Z　-鿿]+', '', _clean(t)).lower()

def variants(t):
    """Both word orders for a `X no Y` name, plus the bare forms.

    `Senge no Takamune` and `Takamune Senge` are the same man written the
    Japanese way and the Geni way. Nothing here is fuzzy: the tokens must match
    exactly, only their order and the `no` particle move.
    """
    c = _clean(t).strip()
    out = {norm(c)}
    parts = [p for p in re.split(r'\s+', c) if p]
    low = [p.lower() for p in parts]
    if 'no' in low:
        i = low.index('no')
        head, tail = parts[:i], parts[i + 1:]
        if head and tail:
            out.add(norm(' '.join(tail + head)))   # Takamune Senge
            out.add(norm(' '.join(head + tail)))   # Senge Takamune
            out.add(norm(' '.join(tail)))          # Takamune
    if len(parts) >= 2:
        out.add(norm(' '.join(reversed(parts))))
    return {v for v in out if v}

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

# Index the WHOLE tree, not just the ball. The ball is only used to report how
# far a match sits from Emma's seed -- restricting the search to it was the second
# error of the first run: the Senge and Kitajima profiles are real and present but
# are reached through the modern imperial line, not through the founder end, so no
# radius around Tsusa 4 contains them.
idx = collections.defaultdict(list)
for x in names:
    for nm in names.get(x, ()):
        for k in variants(nm):
            idx[k].append(x)

gid = lambda x: x.strip('@').lstrip('I')
rows = []; stats = collections.Counter()
for r in roster:
    hits = sorted({x for k in variants(r['name']) for x in idx.get(k, ())})
    if not hits:
        stats['not in the ball'] += 1
        rows.append((r['regnal'], r['name'], r['qid'], r['lineage'], '', '', 'not found'))
    elif len(hits) == 1:
        x = hits[0]
        stats['matched'] += 1
        d = dist.get(x)
        rows.append((r['regnal'], r['name'], r['qid'], r['lineage'],
                     gid(x), names[x][0],
                     f'match (hop {d})' if d is not None else 'match (outside the ball)'))
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
