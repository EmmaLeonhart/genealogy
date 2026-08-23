"""Walk the Bureätten structural anchors into the merged tree and name candidates.

An unlinked person's Wikidata item names relatives; where a relative already
carries a P2600 we hold, that relative is an ANCHOR. The relation inverts to say
where the unlinked person must sit on the Geni side:

    their P22/P25 is X   ->  they are a CHILD of Geni(X)
    their P26 is X       ->  they are a SPOUSE of Geni(X)
    their P40 is X       ->  they are a PARENT of Geni(X)
    their P3373 is X     ->  they are a SIBLING of Geni(X)

Each anchor therefore yields a candidate SET from the tree. **Confirmation is
intersection**: a person confirmed by every one of their anchors, and alone in
that intersection, is a match. That is the answer to what happens when anchors
disagree -- an empty intersection is a disagreement and is reported, never
resolved by picking the more plausible name.

A candidate already carrying a P2600 that maps to a DIFFERENT Wikidata item is
dropped: that Geni profile is somebody else's, already resolved.

Intersection turned out to be NECESSARY BUT NOT SUFFICIENT. On the first run it
"confirmed" Olof Kolmodin den yngre as Johanna Helena Dahl and Hans Fredrik
Harald Strömfelt as Brita Lovisa Strömfelt -- four of seven were wrong. A
position holds several people, siblings above all, and the intersection
collapsing to one only means the others were already claimed.

So a SANITY GATE follows the intersection, and it is the thing CLAUDE.md means by
"the label is read to check the pair is not absurd": sex must agree, and the
first given token must match. The structure still chooses; the gate only rejects.
A pair that fails the gate is reported as rejected, never silently dropped and
never replaced by a better-looking name.
"""
import sys, json, csv, collections, re
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(1 << 30)

anchors = json.load(open(sys.argv[1]))
wd_sex = json.load(open(sys.argv[2]))   # qid -> M/F from Wikidata P21          # qid -> [[prop, relqid, [geni...]], ...]
title = {r['qid']: r['sv_title'] for r in
         csv.DictReader(open('reports/bureatten-unlinked.tsv', encoding='utf-8'), delimiter='\t')}
print(f'{len(anchors)} anchored people')

# ---- merged tree adjacency ------------------------------------------------
fam_par = collections.defaultdict(list); fam_chil = collections.defaultdict(list)
i_fams = collections.defaultdict(list); i_famc = collections.defaultdict(list)
name = {}; sex = {}
cur = kind = None
with open('out/merged.ged', encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('0 @'):
            p = line.split(); cur, kind = p[1], (p[2].strip() if len(p) > 2 else '')
        elif cur and line.startswith('1 '):
            tag, _, val = line[2:].strip().partition(' ')
            if kind == 'FAM':
                if tag in ('HUSB', 'WIFE'): fam_par[cur].append(val)
                elif tag == 'CHIL': fam_chil[cur].append(val)
            elif kind == 'INDI':
                if tag == 'FAMS': i_fams[cur].append(val)
                elif tag == 'FAMC': i_famc[cur].append(val)
                elif tag == 'SEX': sex[cur] = val.strip()[:1]
                elif tag == 'NAME' and cur not in name:
                    name[cur] = val.replace('/', ' ').strip()
print(f'tree loaded, {len(name)} named people')

def children_of(x):
    return {c for fs in i_fams.get(x, ()) for c in fam_chil.get(fs, ())}
def parents_of(x):
    return {p for fc in i_famc.get(x, ()) for p in fam_par.get(fc, ())}
def spouses_of(x):
    return {s for fs in i_fams.get(x, ()) for s in fam_par.get(fs, ())} - {x}
def siblings_of(x):
    return {c for fc in i_famc.get(x, ()) for c in fam_chil.get(fc, ())} - {x}

INVERT = {'P22': children_of, 'P25': children_of,
          'P26': spouses_of, 'P40': parents_of, 'P3373': siblings_of}

# ---- who is already claimed by some other Wikidata item -------------------
claimed = {}
for line in open('out/wikidata/p2600-all.tsv', encoding='utf-8'):
    q, _, g = line.rstrip('\n').partition('\t')
    claimed.setdefault(g, set()).add(q)

def first_token(t):
    t = re.sub(r'\s*\([^)]*\)', '', t or '')
    t = re.sub(r'[^\w\sÀ-ɏ-]', ' ', t)
    parts = [p for p in t.split() if p]
    return parts[0].lower() if parts else ''

def sane(q, x):
    """Reject an absurd pair. Never used to choose between candidates."""
    ws = wd_sex.get(q)
    gs = sex.get(x)
    if ws and gs and ws != gs:
        return False, f'sex {ws} vs {gs}'
    a, b = first_token(title.get(q, '')), first_token(name.get(x, ''))
    if a and b and a != b:
        return False, f'given name {a} vs {b}'
    return True, ''

rows = []; stats = collections.Counter()
for q, ans in anchors.items():
    sets = []; used = []
    for prop, relq, gs in ans:
        fn = INVERT.get(prop)
        if not fn: continue
        cand = set()
        for g in gs:
            x = '@I' + g + '@'
            if x in name or x in i_fams or x in i_famc:
                cand |= fn(x)
        if cand:
            sets.append(cand); used.append((prop, relq))
    if not sets:
        stats['no anchor resolved in our tree'] += 1
        rows.append((q, title.get(q, ''), len(ans), 0, 'anchor not in tree', '', ''))
        continue
    inter = set.intersection(*sets)
    # drop candidates already resolved to a different Wikidata item
    inter = {x for x in inter
             if not (claimed.get(x.strip('@').lstrip('I'), set()) - {q})}
    gid = lambda x: x.strip('@').lstrip('I')
    if len(inter) == 1:
        x = next(iter(inter))
        ok, why = sane(q, x)
        if not ok:
            stats['rejected by sanity gate'] += 1
            rows.append((q, title.get(q, ''), len(ans), len(sets),
                         f'rejected: {why}', gid(x), name.get(x, '')))
        else:
            verdict = 'CONFIRMED' if len(sets) > 1 else 'single-anchor'
            stats[verdict] += 1
            rows.append((q, title.get(q, ''), len(ans), len(sets), verdict,
                         gid(x), name.get(x, '')))
    elif not inter:
        stats['anchors disagree'] += 1
        rows.append((q, title.get(q, ''), len(ans), len(sets), 'anchors disagree', '', ''))
    else:
        stats['ambiguous'] += 1
        rows.append((q, title.get(q, ''), len(ans), len(sets), f'ambiguous ({len(inter)})',
                     ';'.join(sorted(gid(x) for x in inter))[:200],
                     ' | '.join(sorted(name.get(x, '') for x in inter))[:200]))

print()
for k, v in stats.most_common(): print(f'  {v:>4}  {k}')
with open('reports/bureatten-geni-matches.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['qid', 'sv_title', 'anchors', 'anchors_in_tree', 'verdict',
                'geni_id', 'geni_name'])
    w.writerows(sorted(rows, key=lambda r: (r[4], r[1])))
print('\nwrote reports/bureatten-geni-matches.tsv')
print('\n--- CONFIRMED (two or more anchors agreeing on one person) ---')
for r in sorted(rows, key=lambda r: r[1]):
    if r[4] == 'CONFIRMED':
        print(f'  {r[0]:>12}  {r[1][:38]:<38} -> {r[5]}  {r[6][:34]}')
