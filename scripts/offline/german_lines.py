"""Emma's synoptic-tree ancestors with German names: which houses, which centuries, and the ones
from the Reuss neighbourhood (Vogtland, Thuringia, Saxony).
Usage: python german_lines.py MERGED WIKIDATA_ANCESTORS_GED OUT_MD"""
import sys, re, collections
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, PLACEHOLDER

NEAR = r'schwarzburg|schönburg|schonburg|wettin|meissen|meißen|orlamünde|lobdeburg|lobdaburg|weida|gera\b|plauen|henneberg|mansfeld|beichlingen|kirchberg|hohnstein|stolberg|querfurt|wildenfels|leisnig|waldenburg|gleichen|reuss|reuß|vogt|thüring|sachsen|saxony|anhalt|schwarzenberg|everstein|kevernburg|käfernburg|hohenlohe|solms|isenburg|ysenburg'
GERMAN = r'\bvon\b|\bzu\b|graf|gräfin|herzog|fürst|freiherr|freiin|markgraf|landgraf|vogt|herr zu|ritter'

merged, _, mpar, _ = load(sys.argv[1])
wd, _, wpar, _ = load(sys.argv[2])
wanc = ancestors('@I1@', wpar)
byname = collections.defaultdict(list)
for i, p in merged.items():
    k = tuple(norm(p['name']))
    if k: byname[k].append(i)
mtw = twins_index(merged)
anc = {}
for w, g in wanc.items():
    wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
    hits = byname.get(wt, []) if len(wt) >= 2 else []
    if len(hits) == 1:
        h = hits[0]
        anc.setdefault(h, g)
        for a, d in walk(h, lambda n: mpar.get(n, []), mtw).items():
            if a not in anc or anc[a] > g + d: anc[a] = g + d
ger = [a for a in anc if re.search(GERMAN, merged[a]['name'], re.I)]
near = [a for a in anc if re.search(NEAR, merged[a]['name'], re.I)]
cent = collections.Counter((merged[a]['birt'] // 100) * 100 for a in ger if merged[a]['birt'] is not None)
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    f.write(f'# Emma\'s German-named ancestors in the synoptic tree\n\n{len(anc)} ancestors; {len(ger)} with German titles or particles (von, zu, Graf, Herzog, Vogt...).\n\n')
    f.write('## By century of birth\n\n| century | people |\n|---|---|\n')
    for c in sorted(cent): f.write(f'| {c} | {cent[c]} |\n')
    f.write(f'\n## From the Reuss neighbourhood ({len(near)})\n\nHouses of Vogtland, Thuringia and Saxony, by generation above Emma.\n\n')
    for a in sorted(near, key=lambda a: anc[a]):
        p = merged[a]; f.write(f"- gen {anc[a]}: {p['name']} ({p['birt']}–{p['deat']})\n")
    houses = collections.Counter()
    for a in ger:
        m = re.search(r'\b(?:von|zu)\s+([A-ZÄÖÜ][\wäöüß-]+)', merged[a]['name'])
        if m: houses[m.group(1)] += 1
    f.write('\n## Most common houses (von/zu)\n\n')
    for h, n in houses.most_common(40): f.write(f'- {h}: {n}\n')
print(len(anc), 'ancestors;', len(ger), 'German-named;', len(near), 'from the Reuss neighbourhood', file=sys.stderr)
