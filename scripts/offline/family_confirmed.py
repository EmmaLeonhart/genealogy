"""Same person on both sides, with loose dates but confirmed by family: name shares 2+ words,
birth years within 40 (or one missing), and a parent or spouse of one matches a parent or spouse of
the other (2+ shared name words). Her side: synoptic-tree ancestors; his side: Abul Hamza's
descendants. Usage: python family_confirmed.py MERGED TEST WIKIDATA_ANCESTORS_GED OUT_MD"""
import sys, collections
from ged_lib import load, ancestors
from compare_ah import norm, twins_index, walk, AH, PLACEHOLDER

import re
WEAK = {'graf','grafin','count','countess','herr','herzog','herzogin','duke','duchess','king','queen','prince','princess',
        'lord','lady','sir','senhor','senhora','dona','don','conde','condesa','comte','comtesse','vogt','vogtin','freiherr',
        'freiin','furst','furstin','markgraf','landgraf','baron','baroness','dame','seigneur','sire','im','in','von','zu'}
def strong(ts): return {x for x in ts if x not in WEAK and not re.fullmatch(r'[ivxl]+', x)}
def toks(p): return set(x for x in norm(p['name']) if x not in PLACEHOLDER)
def first(p):
    n = [x for x in norm(p['name']) if x not in PLACEHOLDER]
    return n[0] if n else None
def kin(i, ind, fam, par):
    sp = [q for f in ind[i]['fams'] if f in fam for q in fam[f]['par'] if q != i]
    return [('parent', q) for q in par.get(i, [])] + [('spouse', q) for q in sp]

def main():
    merged, mfam, mpar, _ = load(sys.argv[1])
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
    for c in sys.argv[5:]:  # control: known profiles added to her side to prove the check can find them
        anc[c] = -1
    test, tfam, tpar, tk = load(sys.argv[2]); desc = walk(AH, lambda n: tk.get(n, []), twins_index(test))
    idx = collections.defaultdict(list)
    for t in desc:
        tt = toks(test[t])
        for w in tt: idx[w].append(t)
    found = []
    for a, g in anc.items():
        ta = toks(merged[a])
        if len(ta) < 2: continue
        cands = collections.Counter(t for w in ta for t in idx.get(w, []))
        for t, n in cands.items():
            if n < 2 or first(merged[a]) != first(test[t]): continue
            if not (strong(ta & toks(test[t])) - {first(merged[a])}): continue
            ya, yb = merged[a]['birt'], test[t]['birt']
            if ya is not None and yb is not None and abs(ya - yb) > 40: continue
            if ya is None and yb is None: continue
            conf = []
            for ra, ka in kin(a, merged, mfam, mpar):
                for rb, kb in kin(t, test, tfam, tpar):
                    if ra == rb and first(merged[ka]) == first(test[kb]) and (strong(toks(merged[ka]) & toks(test[kb])) - {first(merged[ka])}):
                        conf.append(f"{ra}: {merged[ka]['name']} = {test[kb]['name']}")
            if conf:
                found.append((g, desc[t], a, t, conf))
    found.sort()
    with open(sys.argv[4], 'w', encoding='utf-8') as f:
        f.write('# Same person on both sides, confirmed by family\n\n')
        f.write(f'{len(found)} people who are both among Emma\'s synoptic-tree ancestors and among Abul Hamza\'s descendants, '
                'matched with loose dates (within 40 years) but confirmed by a matching parent or spouse.\n\n')
        for g, h, a, t, conf in found:
            f.write(f"## {merged[a]['name']} ({merged[a]['birt']}) = {test[t]['name']} ({test[t]['birt']})\n\n")
            f.write(f"{g} generations above Emma; {h} generations below Abul Hamza.\n\n")
            for c in conf[:4]: f.write(f'- {c}\n')
            f.write('\n')
    print(len(found), 'family-confirmed', file=sys.stderr)
    for g, h, a, t, conf in found[:20]: print(g, h, merged[a]['name'], merged[a]['birt'], '=', test[t]['name'], test[t]['birt'], '|', conf[0], file=sys.stderr)

if __name__ == '__main__':
    main()
