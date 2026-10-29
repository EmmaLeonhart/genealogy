"""Houses/family names that occur both among Emma's synoptic-tree ancestors and among Abul Hamza's
descendants, in overlapping centuries: candidates for the missing link.
Usage: python closest.py MERGED TEST WIKIDATA_ANCESTORS_GED OUT_MD"""
import sys, re, collections, unicodedata
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, AH, PLACEHOLDER, ALIAS

GENERIC = {'nn', 'unknown', 'ii', 'iii', 'iv', 'vi', 'vii', 'viii', 'ix', 'xi', 'xii', 'graf', 'grafin', 'herr', 'count',
           'countess', 'duke', 'duchess', 'king', 'queen', 'lord', 'lady', 'sir', 'prince', 'princess', 'senhor', 'senhora',
           'dona', 'don', 'conde', 'condesa', 'herzog', 'herzogin', 'furst', 'furstin', 'vogt', 'vogtin', 'freiherr', 'freiin'}
def house(name):
    s = unicodedata.normalize('NFKD', name.replace('ß', 'ss'))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    m = re.search(r'\b(?:von|zu|de|of|van|da|di|af|av)\s+(?:der\s+|la\s+|le\s+)?([A-Za-z][\w-]+)', s)
    if m:
        h = m.group(1).lower().split('-')[0]
    else:
        toks = [t for t in re.findall(r'[a-z]+', s.lower()) if len(t) > 2]
        if len(toks) < 2: return None
        h = toks[-1]
    h = ALIAS.get(h, h)
    return None if h in GENERIC or len(h) < 3 or re.search(r'(dotter|datter|sson|sen|dottir)$', h) else h

merged, _, mpar, _ = load(sys.argv[1])
wd, _, wpar, _ = load(sys.argv[3]); wanc = ancestors('@I1@', wpar)
byname = collections.defaultdict(list)
for i, p in merged.items():
    k = tuple(norm(p['name']))
    if k: byname[k].append(i)
mtw = twins_index(merged); anc = {}
for w, g in wanc.items():
    wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
    hits = byname.get(wt, []) if len(wt) >= 2 else []
    if len(hits) == 1:
        anc.setdefault(hits[0], g)
        for a, d in walk(hits[0], lambda n: mpar.get(n, []), mtw).items():
            if a not in anc or anc[a] > g + d: anc[a] = g + d
test, _, _, tk = load(sys.argv[2]); desc = walk(AH, lambda n: tk.get(n, []), twins_index(test))
mine = collections.defaultdict(list); his = collections.defaultdict(list)
for a, g in anc.items():
    h = house(merged[a]['name'])
    if h and merged[a]['birt'] is not None: mine[h].append((merged[a]['birt'], g, merged[a]['name']))
for t, g in desc.items():
    h = house(test[t]['name'])
    if h and test[t]['birt'] is not None: his[h].append((test[t]['birt'], g, test[t]['name']))
rows = []
for h in set(mine) & set(his):
    # closest pair in time
    best = min(((abs(a[0] - b[0]), a, b) for a in mine[h] for b in his[h]), key=lambda x: x[0])
    if best[0] <= 60:
        rows.append((best[0], h, len(mine[h]), len(his[h]), best[1], best[2]))
rows.sort(key=lambda r: (r[0], -min(r[2], r[3])))
with open(sys.argv[4], 'w', encoding='utf-8') as f:
    f.write('# Where Emma\'s ancestors and Abul Hamza\'s descendants come closest\n\n')
    f.write('Houses or family names found on both sides, with the closest pair in birth year (within 60 years). '
            'Same house is not the same family line: each row is a lead to check, not a link.\n\n')
    f.write('| years apart | house | her ancestors | his descendants | closest of hers (gen up) | closest of his (gen below) |\n|---|---|---|---|---|---|\n')
    for d, h, nm, nh, a, b in rows[:150]:
        f.write(f'| {d} | {h} | {nm} | {nh} | {a[2]} ({a[0]}, {a[1]}) | {b[2]} ({b[0]}, {b[1]}) |\n')
print(len(rows), 'shared houses within 60 years', file=sys.stderr)
