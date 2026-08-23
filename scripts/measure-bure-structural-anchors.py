"""Can the unlinked Bureätten people be resolved STRUCTURALLY, offline?

The Google route works but its top hit is often the wrong person: searching
"Adolf Ludvig Piper" returns Axel Adolf Piper first, because the man himself is
"Adolf Ludvig Piper, till Ängsö" and appears in everyone else's page as "son of".
Taking the first hit would be exactly the name matching this repo refuses.

The structural route instead: a person's Wikidata item names their parents,
spouse and children. Where one of THOSE carries a P2600 we already hold, the
unlinked person sits in a known position beside a known Geni profile, and the
Geni side of that position is the candidate. Structure picks the pair; the label
only checks it is not absurd.

This measures how much of the 198 that route can reach.
"""
import sys, json, csv, sqlite3, gzip, os, collections
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(1 << 30)

rows = list(csv.DictReader(open('reports/bureatten-unlinked.tsv', encoding='utf-8'), delimiter='\t'))
qids = [r['qid'] for r in rows]
print(f'{len(qids)} unlinked Bureätten people')

db = sqlite3.connect('out/wikidata/store-index.sqlite3')
shard = {}
for q in qids:
    r = db.execute('select shard from items where qid=?', (q,)).fetchone()
    if r: shard[q] = r[0]
print(f'{len(shard)} of them are in the local Wikidata store')

by = collections.defaultdict(set)
for q, s in shard.items(): by[s].add(q)
REL = ('P22', 'P25', 'P26', 'P40', 'P3373')
links = {}
for s, qs in by.items():
    p = f'wikidata/items/items-{s:05d}.jsonl.gz'
    if not os.path.exists(p): continue
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        for line in f:
            if not any(q in line[:120] for q in qs): continue
            it = json.loads(line)
            if it.get('id') not in qs: continue
            out = []
            for pr in REL:
                for st in (it.get('claims') or {}).get(pr, []):
                    dv = (st.get('mainsnak', {}).get('datavalue') or {}).get('value')
                    if isinstance(dv, dict) and dv.get('id'):
                        out.append((pr, dv['id']))
            links[it['id']] = out
print(f'read relationship claims for {len(links)}')

# which linked relatives carry a P2600?
need = {q for v in links.values() for _, q in v}
rel_geni = {}
for q in need:
    gs = [g for (g,) in db.execute('select geni_id from geni where qid=?', (q,))]
    if gs: rel_geni[q] = gs
print(f'{len(rel_geni)} of the {len(need)} related items carry a Geni ID')

resolvable = {q: [(pr, r, rel_geni[r]) for pr, r in v if r in rel_geni]
              for q, v in links.items()}
resolvable = {q: v for q, v in resolvable.items() if v}
print()
print(f'*** {len(resolvable)} of the {len(rows)} unlinked people have at least one')
print(f'    Wikidata relative that already carries a Geni ID ***')
print()
title = {r['qid']: r['sv_title'] for r in rows}
n = collections.Counter(len(v) for v in resolvable.values())
print('anchors per person:', dict(sorted(n.items())))
print()
for q, v in list(resolvable.items())[:12]:
    print(f'  {q}  {title[q]}')
    for pr, r, gs in v[:3]:
        print(f'      {pr} -> {r}  geni {gs[0]}')
json.dump({q: [[pr, r, gs] for pr, r, gs in v] for q, v in resolvable.items()},
          open(sys.argv[1], 'w'))
