"""Emma's ancestors (synoptic tree, out/merged.ged) vs Abul Hamza's descendants
(rootsmagic/test_2026-10-09.ged). Matches people by normalized name + birth/death year.
Usage: python compare_ah.py MERGED TEST OUT_TSV WIKIDATA_ANCESTORS_GED"""
import sys, re, unicodedata, collections
from ged_lib import load, ancestors

ME = '@I6000000001846508982@'
AH = '@I1@'  # Gregory-Abuhamza Artsruni, root of test.ged
PLACEHOLDER = {'nn', 'unknown', 'ukjent', 'okand', 'okänd', 'unbekannt', 'desconocido', 'mrs', 'mr', 'daughter', 'son', 'wife', 'nnn'}
STOP = {'von', 'zu', 'de', 'of', 'the', 'der', 'die', 'van', 'da', 'di', 'du', 'la', 'le', 'y', 'und', 'and', 'af', 'av'}

def norm(s):
    s = s.replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return [t for t in re.findall(r'[a-z]+', s) if t not in STOP and len(t) > 1]

def keys(p):
    # birth year against birth year (+-1); death year only when there is no birth year
    toks = [x for x in norm(p['name']) if x not in PLACEHOLDER]
    if not toks:
        return toks, []
    if p['birt'] is not None:
        return toks, [(toks[0], 'b', p['birt'] + d) for d in (-1, 0, 1)]
    if p['deat'] is not None:
        return toks, [(toks[0], 'd', p['deat'] + d) for d in (-1, 0, 1)]
    return toks, []

def twins_index(people):
    # same person under several IDs: same name tokens (at least two, no placeholders), same birth
    # year, and death years that do not disagree. With no birth year, the death year must match.
    ix = collections.defaultdict(list)
    def tk(p):
        toks = [x for x in norm(p['name']) if x not in PLACEHOLDER]
        return tuple(sorted(set(toks))) if len(toks) >= 2 else None
    for i, p in people.items():
        k = tk(p)
        if k is None:
            continue
        if p['birt'] is not None:
            ix[(k, 'b', p['birt'])].append(i)
        elif p['deat'] is not None:
            ix[(k, 'd', p['deat'])].append(i)
    def twins(i):
        p = people[i]; k = tk(p)
        if k is None:
            return set()
        key = (k, 'b', p['birt']) if p['birt'] is not None else ((k, 'd', p['deat']) if p['deat'] is not None else None)
        if key is None:
            return set()
        out = set()
        for j in ix.get(key, []):
            q = people[j]
            if j != i and not (p['deat'] is not None and q['deat'] is not None and p['deat'] != q['deat']):
                out.add(j)
        return out
    return twins

def walk(start, step, twins):
    # breadth-first over step() links; a dead end continues through the person's duplicates
    seen = {start: 0}; front = [start]
    while front:
        nxt = []
        for n in front:
            d = seen[n]
            links = step(n)
            if not links:
                for tw in twins(n):
                    if tw not in seen:
                        seen[tw] = d; nxt.append(tw)
            for q in links:
                if q not in seen:
                    seen[q] = d + 1; nxt.append(q)
        front = nxt
    seen.pop(start)
    return seen

def main():
    merged, mfam, mpar, mkids = load(sys.argv[1])
    mtwins = twins_index(merged)
    # seeds: Emma's own ancestors from Wikidata (her parents and up), matched by exact name into the synoptic tree
    wd, _, wpar, _ = load(sys.argv[4])
    wanc = ancestors('@I1@', wpar)
    byname = collections.defaultdict(list)
    for i, p in merged.items():
        k = tuple(norm(p['name']))
        if k:
            byname[k].append(i)
    anc = {}
    seeded = 0
    for w, g in wanc.items():
        wt = tuple(x for x in norm(wd[w]['name']) if x not in PLACEHOLDER)
        hits = byname.get(wt, []) if len(wt) >= 2 else []
        if len(hits) == 1:
            seeded += 1
            for h in hits:
                if h not in anc or anc[h] > g:
                    anc[h] = g
                for a, d in walk(h, lambda n: mpar.get(n, []), mtwins).items():
                    if a not in anc or anc[a] > g + d:
                        anc[a] = g + d
    print('wikidata ancestors:', len(wanc), 'found in synoptic tree:', seeded, file=sys.stderr)
    print('my ancestors in synoptic tree:', len(anc), file=sys.stderr)

    test, tfam, tpar, tkids = load(sys.argv[2])
    desc = walk(AH, lambda n: tkids.get(n, []), twins_index(test))
    print('Abul Hamza descendants in test.ged:', len(desc), file=sys.stderr)

    idx = collections.defaultdict(list)
    for t in desc:
        toks, ks = keys(test[t])
        for k in ks:
            idx[k].append((t, set(toks)))

    rows = []
    for a, gen in anc.items():
        toks, ks = keys(merged[a])
        best = None
        for k in ks:
            for t, tt in idx.get(k, []):
                shared = set(toks) & tt
                j = len(shared) / len(set(toks) | tt)
                if len(shared) >= 2 and j >= 0.5 and (best is None or j > best[1]):
                    best = (t, j)
        if best:
            t, j = best
            rows.append((gen, desc[t], round(j, 2), a, merged[a]['name'], merged[a]['birt'], t, test[t]['name'], test[t]['birt']))

    rows.sort()
    with open(sys.argv[3], 'w', encoding='utf-8') as f:
        f.write('gens_above_me\tgens_below_abul_hamza\tname_score\tgeni_id\tsynoptic_name\tsynoptic_birth\ttest_id\ttest_name\ttest_birth\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    print('matched people:', len(rows), file=sys.stderr)

if __name__ == '__main__':
    main()
