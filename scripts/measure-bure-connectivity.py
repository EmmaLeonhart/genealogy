"""Are the Bureätten people we hold connected to each other in our tree?

Emma, 2026-08-22: "we're just trying to connect them to each other... We're not
trying to run a gigantic export on all of them. We're trying to get them all
connected to each other on a family tree."

So the question is not coverage, it is components. Walk the merged tree and ask
which component each Bureätten person falls in.
"""
import sys, re, csv, collections
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(1 << 30)

targets = {}
for r in csv.DictReader(open('reports/bureatten.csv', encoding='utf-8')):
    for g in (r['geni_ids'] or '').split(';'):
        if g: targets[g] = r['sv_title']
print(f'{len(targets)} Bureätten Geni ids from the category')

fam_par = collections.defaultdict(list); fam_chil = collections.defaultdict(list)
i_fams = collections.defaultdict(list); i_famc = collections.defaultdict(list)
present = set()
cur = kind = None
with open('out/merged.ged', encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('0 @'):
            p = line.split(); cur, kind = p[1], (p[2].strip() if len(p) > 2 else '')
            if kind == 'INDI': present.add(cur)
        elif cur and line.startswith('1 '):
            tag, _, val = line[2:].strip().partition(' ')
            if kind == 'FAM':
                if tag in ('HUSB', 'WIFE'): fam_par[cur].append(val)
                elif tag == 'CHIL': fam_chil[cur].append(val)
            elif kind == 'INDI':
                if tag == 'FAMS': i_fams[cur].append(val)
                elif tag == 'FAMC': i_famc[cur].append(val)

xr = {g: '@I' + g + '@' for g in targets}
inside = {g: x for g, x in xr.items() if x in present}
print(f'{len(inside)} of them are in the merged tree (out/merged.ged, 19 Aug)')

def nbrs(i):
    o = set()
    for fc in i_famc.get(i, ()): o |= set(fam_par.get(fc, ())) | set(fam_chil.get(fc, ()))
    for fs in i_fams.get(i, ()): o |= set(fam_par.get(fs, ())) | set(fam_chil.get(fs, ()))
    o.discard(i); return o

# component id for each Bureätten person, walking the WHOLE tree
seen = {}; comp = 0; sizes = {}
for g, x in inside.items():
    if x in seen: continue
    comp += 1; n = 0
    stack = [x]; seen[x] = comp
    while stack:
        i = stack.pop(); n += 1
        for y in nbrs(i):
            if y not in seen:
                seen[y] = comp; stack.append(y)
    sizes[comp] = n

by = collections.Counter(seen[x] for x in inside.values())
print(f'\nthe {len(inside)} fall into {len(by)} connected component(s):')
for c, k in by.most_common():
    print(f'   component {c}: {k} Bureätten people, {sizes[c]} people in total')
if len(by) > 1:
    print('\nthe smaller components, and who is in them:')
    big = by.most_common(1)[0][0]
    for g, x in sorted(inside.items(), key=lambda kv: targets[kv[0]]):
        if seen[x] != big:
            print(f'   comp {seen[x]:>3}  {g}  {targets[g]}')
