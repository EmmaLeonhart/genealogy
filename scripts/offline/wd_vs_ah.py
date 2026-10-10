"""Emma's Wikidata ancestors (dated) vs Abul Hamza's descendants, strict name+date matching.
Usage: python wd_vs_ah.py WD_DATED.ged TEST.ged"""
import sys, re, collections
from ged_lib import load, ancestors
from compare_ah import keys, twins_index, walk, AH
wd, _, wpar, _ = load(sys.argv[1]); wanc = ancestors('@I1@', wpar)
test, _, _, tkids = load(sys.argv[2]); desc = walk(AH, lambda n: tkids.get(n, []), twins_index(test))
idx = collections.defaultdict(list)
for t in desc:
    toks, ks = keys(test[t])
    for k in ks: idx[k].append((t, set(toks)))
rows = []
for a, g in wanc.items():
    toks, ks = keys(wd[a]); best = None
    for k in ks:
        for t, tt in idx.get(k, []):
            sh = set(toks) & tt; j = len(sh) / len(set(toks) | tt)
            if len(sh) >= 2 and j >= 0.5 and (best is None or j > best[1]): best = (t, j)
    if best: rows.append((g, desc[best[0]], round(best[1], 2), wd[a]['name'], wd[a]['birt'], test[best[0]]['name'], test[best[0]]['birt']))
reuss = [a for a in wanc if re.search(r'reu(ss|ß)|plauen', wd[a]['name'], re.I)]
print('wikidata ancestors', len(wanc), '| Reuss/Plauen among them', len(reuss), '| matches with Abul Hamza descendants', len(rows))
for r in sorted(rows): print(*r, sep=' | ')
