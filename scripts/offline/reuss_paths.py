"""Reuss/Plauen ancestors of Emma in the synoptic tree, the line down to her, and strict
matches between her ancestors and Abul Hamza's descendants (test.ged).
Usage: python reuss_paths.py MERGED TEST WIKIDATA_ANCESTORS_GED OUT_MD"""
import sys, re, collections
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, PLACEHOLDER  # noqa  (compare_ah runs on import only under __main__)

PAT = sys.argv[5] if len(sys.argv) > 5 else r"reu(ss|ß)|plauen"
merged, mfam, mpar, mkids = load(sys.argv[1])
mtw = twins_index(merged)
wd, _, wpar, wkids = load(sys.argv[3])
wanc = ancestors('@I1@', wpar)
byname = collections.defaultdict(list)
for i, p in merged.items():
    k = tuple(norm(p['name']))
    if k: byname[k].append(i)
# walk up with predecessor links so each ancestor knows the child it was reached from
prev = {}; gen = {}; seedof = {}
front = []
for w, g in wanc.items():
    wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
    hits = byname.get(wt, []) if len(wt) >= 2 else []
    if len(hits) == 1:
        for h in hits:
            if h not in gen or gen[h] > g:
                gen[h] = g; prev[h] = None; seedof[h] = w; front.append(h)
front.sort(key=lambda h: gen[h])
while front:
    nxt = []
    for n in front:
        links = mpar.get(n, [])
        cand = [(q, 1) for q in links] if links else [(q, 0) for q in mtw(n)]
        for q, step in cand:
            if q not in gen or gen[q] > gen[n] + step:
                gen[q] = gen[n] + step; prev[q] = n; seedof[q] = seedof[n]; nxt.append(q)
    front = nxt
def line_down(a):
    out = []
    while a is not None:
        p = merged[a]; out.append(f"{p['name']} ({p['birt'] if p['birt'] is not None else '?'}–{p['deat'] if p['deat'] is not None else '?'})")
        last = a; a = prev[a]
    w = seedof[last]
    # wikidata chain from the seed down to Emma
    chain = []
    cur = w
    wprev = {}
    q = ['@I1@']; seen = {'@I1@'}
    while q:
        n = q.pop(0)
        for pa in wpar.get(n, []):
            if pa not in seen: seen.add(pa); wprev[pa] = n; q.append(pa)
    while cur in wprev:
        cur = wprev[cur]; chain.append(wd[cur]['name'])
    return out + ['— (Wikidata) —'] + chain
R = [a for a in gen if re.search(PAT, merged[a]["name"], re.I)]
R.sort(key=lambda a: gen[a])
with open(sys.argv[4], 'w', encoding='utf-8') as f:
    f.write(f'# Reuss / Plauen ancestors of Emma in the synoptic tree\n\n{len(R)} people. Generation = steps above Emma.\n\n')
    for a in R:
        p = merged[a]
        f.write(f"## {p['name']} ({p['birt']}–{p['deat']}), generation {gen[a]}\n\n")
        for s in line_down(a): f.write(f'- {s}\n')
        f.write('\n')
print('Reuss/Plauen ancestors:', len(R), file=sys.stderr)
for a in R[:15]: print(gen[a], merged[a]['name'], merged[a]['birt'], file=sys.stderr)
