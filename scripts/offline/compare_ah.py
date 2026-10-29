"""Emma's ancestors (synoptic tree, out/merged.ged) vs Abul Hamza's descendants
(rootsmagic/test_2026-10-09.ged). Matches people by normalized name + birth/death year.
Usage: python compare_ah.py MERGED TEST OUT_TSV WIKIDATA_ANCESTORS_GED"""
import sys, re, unicodedata, collections
from ged_lib import load, ancestors

ME = '@I6000000001846508982@'
AH = '@I1@'  # Gregory-Abuhamza Artsruni, root of test.ged
PLACEHOLDER = {'nn', 'unknown', 'ukjent', 'okand', 'okänd', 'unbekannt', 'desconocido', 'mrs', 'mr', 'daughter', 'son', 'wife', 'nnn'}
STOP = {'von', 'zu', 'de', 'of', 'the', 'der', 'die', 'van', 'da', 'di', 'du', 'la', 'le', 'y', 'und', 'and', 'af', 'av'}

ALIAS = {'henry': 'henry', 'heinrich': 'henry', 'henrique': 'henry', 'enrique': 'henry', 'henri': 'henry', 'enrico': 'henry', 'hendrik': 'henry', 'john': 'john', 'johann': 'john', 'johannes': 'john', 'jean': 'john', 'joao': 'john', 'juan': 'john', 'giovanni': 'john', 'jan': 'john', 'hans': 'john', 'johan': 'john', 'william': 'william', 'wilhelm': 'william', 'guillaume': 'william', 'guilherme': 'william', 'guillermo': 'william', 'guglielmo': 'william', 'charles': 'charles', 'karl': 'charles', 'carlos': 'charles', 'carlo': 'charles', 'louis': 'louis', 'ludwig': 'louis', 'luis': 'louis', 'luiz': 'louis', 'ludovico': 'louis', 'lodewijk': 'louis', 'frederick': 'frederick', 'friedrich': 'frederick', 'frederico': 'frederick', 'federico': 'frederick', 'conrad': 'conrad', 'konrad': 'conrad', 'corrado': 'conrad', 'albert': 'albert', 'albrecht': 'albert', 'alberto': 'albert', 'peter': 'peter', 'pedro': 'peter', 'pierre': 'peter', 'pietro': 'peter', 'peder': 'peter', 'alfonso': 'alfonso', 'afonso': 'alfonso', 'alphonse': 'alfonso', 'alfons': 'alfonso', 'ferdinand': 'ferdinand', 'fernando': 'ferdinand', 'fernao': 'ferdinand', 'margaret': 'margaret', 'margarethe': 'margaret', 'margarete': 'margaret', 'margareta': 'margaret', 'margarita': 'margaret', 'margarida': 'margaret', 'marguerite': 'margaret', 'margherita': 'margaret', 'catherine': 'catherine', 'katharina': 'catherine', 'katharine': 'catherine', 'catarina': 'catherine', 'catalina': 'catherine', 'caterina': 'catherine', 'katarina': 'catherine', 'elizabeth': 'elizabeth', 'elisabeth': 'elizabeth', 'isabel': 'elizabeth', 'isabella': 'elizabeth', 'elisabetta': 'elizabeth', 'isabelle': 'elizabeth', 'elisabet': 'elizabeth', 'agnes': 'agnes', 'ines': 'agnes', 'mary': 'mary', 'maria': 'mary', 'marie': 'mary', 'anne': 'anne', 'anna': 'anne', 'ana': 'anne', 'joan': 'joan', 'johanna': 'joan', 'juana': 'joan', 'joana': 'joan', 'jeanne': 'joan', 'giovanna': 'joan', 'beatrice': 'beatrice', 'beatrix': 'beatrice', 'beatriz': 'beatrice', 'eleanor': 'eleanor', 'leonor': 'eleanor', 'eleonore': 'eleanor', 'alienor': 'eleanor', 'eleonora': 'eleanor', 'matilda': 'matilda', 'mathilde': 'matilda', 'mafalda': 'matilda', 'mechthild': 'matilda', 'sophia': 'sophia', 'sophie': 'sophia', 'sofia': 'sophia', 'rudolph': 'rudolph', 'rudolf': 'rudolph', 'rodolfo': 'rudolph', 'george': 'george', 'georg': 'george', 'jorge': 'george', 'giorgio': 'george', 'philip': 'philip', 'philipp': 'philip', 'felipe': 'philip', 'filipe': 'philip', 'philippe': 'philip', 'filippo': 'philip', 'stephen': 'stephen', 'stefan': 'stephen', 'esteban': 'stephen', 'estevao': 'stephen', 'etienne': 'stephen', 'stefano': 'stephen', 'theodoric': 'theodoric', 'dietrich': 'theodoric', 'thierry': 'theodoric', 'baldwin': 'baldwin', 'balduin': 'baldwin', 'baudouin': 'baldwin', 'godfrey': 'godfrey', 'gottfried': 'godfrey', 'godefroy': 'godfrey', 'hugh': 'hugh', 'hugo': 'hugh', 'hugues': 'hugh', 'raymond': 'raymond', 'raimund': 'raymond', 'ramon': 'raymond', 'raimundo': 'raymond', 'thuringia': 'thuringia', 'thuringen': 'thuringia', 'saxony': 'saxony', 'sachsen': 'saxony', 'bavaria': 'bavaria', 'bayern': 'bavaria', 'austria': 'austria', 'osterreich': 'austria', 'bohemia': 'bohemia', 'bohmen': 'bohemia', 'brunswick': 'brunswick', 'braunschweig': 'brunswick', 'hesse': 'hesse', 'hessen': 'hesse', 'lorraine': 'lorraine', 'lothringen': 'lorraine', 'burgundy': 'burgundy', 'burgund': 'burgundy', 'bourgogne': 'burgundy', 'borgogna': 'burgundy', 'swabia': 'swabia', 'schwaben': 'swabia', 'franconia': 'franconia', 'franken': 'franconia', 'cologne': 'cologne', 'koln': 'cologne', 'castile': 'castile', 'castilla': 'castile', 'castela': 'castile', 'braganza': 'braganza', 'braganca': 'braganza', 'navarre': 'navarre', 'navarra': 'navarre', 'brittany': 'brittany', 'bretagne': 'brittany', 'flanders': 'flanders', 'flandre': 'flanders', 'vlaanderen': 'flanders', 'normandy': 'normandy', 'normandie': 'normandy', 'savoy': 'savoy', 'savoie': 'savoy', 'savoia': 'savoy', 'aragon': 'aragon', 'arago': 'aragon', 'portugal': 'portugal', 'denmark': 'denmark', 'danemark': 'denmark', 'danmark': 'denmark', 'norway': 'norway', 'norwegen': 'norway', 'norge': 'norway', 'sweden': 'sweden', 'schweden': 'sweden', 'sverige': 'sweden', 'hungary': 'hungary', 'ungarn': 'hungary', 'hongrie': 'hungary', 'poland': 'poland', 'polen': 'poland', 'pologne': 'poland'}

TRANS = str.maketrans({'ł': 'l', 'Ł': 'L', 'ø': 'o', 'Ø': 'O', 'æ': 'ae', 'Æ': 'Ae', 'đ': 'd', 'Đ': 'D', 'þ': 'th', 'Þ': 'Th', 'ð': 'd', 'œ': 'oe', 'ı': 'i'})

def norm(s):
    s = re.sub(r'(?:h\.|herbu)\s*\S+', ' ', s.translate(TRANS))
    s = s.replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return [ALIAS.get(t, t) for t in re.findall(r'[a-z]+', s) if t not in STOP and len(t) > 1]

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
