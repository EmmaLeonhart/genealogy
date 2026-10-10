"""Abul Hamza's descendants found inside the synoptic tree (family-confirmed identity), walked down
there; any of those descendants who is among Emma's ancestors is a link.
Usage: python his_lines_down.py MERGED TEST WD_DATED_GED OUT_MD"""
import sys, collections
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, AH, PLACEHOLDER
from family_confirmed import toks, first, strong, kin

merged, mfam, mpar, mkids = load(sys.argv[1])
test, tfam, tpar, tk = load(sys.argv[2])
wd, wfam, wpar, wkids = load(sys.argv[3]); wanc = ancestors('@I1@', wpar)
def same(p, q, window):
    if first(p) is None or first(p) != first(q) or not (strong(toks(p) & toks(q)) - {first(p)}): return False
    a, b = p['birt'], q['birt']
    return not (a is not None and b is not None and abs(a - b) > window) and not (a is None and b is None)
# her ancestors (same entry-point method as grow_side.py)
byname = collections.defaultdict(list); byfirst = collections.defaultdict(list)
for i, p in merged.items():
    k = tuple(norm(p['name']))
    if k: byname[k].append(i)
    f = first(p)
    if f and p['birt'] is not None: byfirst[(f, p['birt'] // 10)].append(i)
mtw = twins_index(merged)
entry = {}
for w, g in wanc.items():
    wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
    hits = byname.get(wt, []) if len(wt) >= 2 else []
    if len(hits) == 1: entry[hits[0]] = g
anc = {}
for h, g in entry.items():
    anc.setdefault(h, g)
    for a, d in walk(h, lambda n: mpar.get(n, []), mtw).items():
        if a not in anc or anc[a] > g + d: anc[a] = g + d
print('her ancestors:', len(anc), file=sys.stderr)
# his descendants located in the synoptic tree
desc = walk(AH, lambda n: tk.get(n, []), twins_index(test))
located = {}
for t, h in desc.items():
    p = test[t]; f = first(p)
    if not f or p['birt'] is None: continue
    cands = [m for d in (-1, 0, 1) for m in byfirst.get((f, p['birt'] // 10 + d), []) if same(p, merged[m], 40)]
    for m in cands:
        if any(ra == rb and same(test[kb], merged[ka], 40) for rb, kb in kin(t, test, tfam, tpar) for ra, ka in kin(m, merged, mfam, mpar)):
            located.setdefault(m, (t, h))
print('his descendants located in synoptic tree:', len(located), file=sys.stderr)
# walk down inside the synoptic tree, remembering the route
prev = {m: None for m in located}; front = list(located)
while front:
    nxt = []
    for n in front:
        kids = mkids.get(n, [])
        for c in (kids if kids else mtw(n)):  # a dead end continues through the person's duplicates
            if c not in prev: prev[c] = n; nxt.append(c)
    front = nxt
print('his descendants reached in the synoptic tree:', len(prev), file=sys.stderr)
hits = [a for a in anc if a in prev]
print('links (his synoptic-tree descendants who are her ancestors):', len(hits), file=sys.stderr)
def route(a):
    r = []
    while a is not None: r.append(a); a = prev[a]
    return r[::-1]
hits.sort(key=lambda a: -anc[a])
with open(sys.argv[4], 'w', encoding='utf-8') as f:
    f.write(f'# His lines followed down in the synoptic tree\n\nHer ancestors: {len(anc)}. His descendants located in the synoptic tree (family-confirmed): {len(located)}. Links: {len(hits)}.\n\n')
    for a in hits[:50]:
        r = route(a); top = r[0]; t, h = located[top]
        f.write(f"## {merged[a]['name']} ({merged[a]['birt']}), {anc[a]} generations above Emma\n\n")
        f.write(f"Enters the synoptic tree at {merged[top]['name']} ({merged[top]['birt']}) = test.ged {test[t]['name']} ({test[t]['birt']}), {h} generations below Abul Hamza.\n\n")
        for x in r: f.write(f"- {merged[x]['name']} ({merged[x]['birt']}–{merged[x]['deat']})\n")
        f.write('\n')
for a in hits[:15]: print(anc[a], merged[a]['name'], merged[a]['birt'], '<- via', merged[route(a)[0]]['name'], file=sys.stderr)
