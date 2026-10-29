"""Find more of Emma's Wikidata ancestors in the synoptic tree: same first name, a shared real name
word, birth years within 10 (Wikidata dates), and a parent or child that also matches. Then walk up
from all entry points and rerun the family-confirmed check against Abul Hamza's descendants.
Usage: python grow_side.py MERGED TEST WD_DATED_GED OUT_MD"""
import sys, collections, re
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, AH, PLACEHOLDER
from family_confirmed import toks, first, strong  # noqa (module guarded below)
from family_confirmed import kin

merged, mfam, mpar, mkids = load(sys.argv[1])
wd, wfam, wpar, wkids = load(sys.argv[3]); wanc = ancestors('@I1@', wpar)
byname = collections.defaultdict(list); byfirst = collections.defaultdict(list)
for i, p in merged.items():
    k = tuple(norm(p['name']))
    if k: byname[k].append(i)
    f = first(p)
    if f and p['birt'] is not None: byfirst[(f, p['birt'] // 10)].append(i)
def same(wp, mp, window):
    if first(wp) != first(mp) or not (strong(toks(wp) & toks(mp)) - {first(wp)}): return False
    a, b = wp['birt'], mp['birt']
    return a is not None and b is not None and abs(a - b) <= window
entry = {}
for w, g in wanc.items():
    wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
    hits = byname.get(wt, []) if len(wt) >= 2 else []
    if len(hits) == 1: entry[hits[0]] = g; continue
    p = wd[w]; f = first(p)
    if not f or p['birt'] is None: continue
    cands = [m for d in (-1, 0, 1) for m in byfirst.get((f, p['birt'] // 10 + d), []) if same(p, merged[m], 10)]
    ok = []
    for m in cands:
        wk = [wd[q] for q in wpar.get(w, []) + wkids.get(w, [])]
        mk = [merged[q] for q in mpar.get(m, []) + mkids.get(m, [])]
        if any(same(a, b, 15) for a in wk for b in mk): ok.append(m)
    if len(ok) == 1: entry.setdefault(ok[0], g)
print('entry points:', len(entry), file=sys.stderr)
mtw = twins_index(merged); anc = {}
for h, g in entry.items():
    anc.setdefault(h, g)
    for a, d in walk(h, lambda n: mpar.get(n, []), mtw).items():
        if a not in anc or anc[a] > g + d: anc[a] = g + d
print('ancestors in synoptic tree:', len(anc), file=sys.stderr)
test, tfam, tpar, tk = load(sys.argv[2]); desc = walk(AH, lambda n: tk.get(n, []), twins_index(test))
idx = collections.defaultdict(list)
for t in desc:
    for x in toks(test[t]): idx[x].append(t)
found = []
for a, g in anc.items():
    ta = toks(merged[a])
    if len(ta) < 2: continue
    for t, n in collections.Counter(t for x in ta for t in idx.get(x, [])).items():
        if n < 2 or first(merged[a]) != first(test[t]) or not (strong(ta & toks(test[t])) - {first(merged[a])}): continue
        ya, yb = merged[a]['birt'], test[t]['birt']
        if (ya is None and yb is None) or (ya is not None and yb is not None and abs(ya - yb) > 40): continue
        conf = [f"{ra}: {merged[ka]['name']} = {test[kb]['name']}" for ra, ka in kin(a, merged, mfam, mpar) for rb, kb in kin(t, test, tfam, tpar)
                if ra == rb and first(merged[ka]) == first(test[kb]) and (strong(toks(merged[ka]) & toks(test[kb])) - {first(merged[ka])})]
        if conf: found.append((g, desc[t], merged[a]['name'], merged[a]['birt'], test[t]['name'], test[t]['birt'], conf[0]))
found.sort()
with open(sys.argv[4], 'w', encoding='utf-8') as f:
    f.write(f'# Growing her side: {len(entry)} entry points, {len(anc)} ancestors, {len(found)} family-confirmed links\n\n')
    for r in found: f.write('- ' + ' | '.join(str(x) for x in r) + '\n')
print('family-confirmed links:', len(found), file=sys.stderr)
for r in found[:20]: print(*r, sep=' | ', file=sys.stderr)
