"""Where the RootsMagic fetch has got to. RootsMagic person IDs (kept as @I<n>@ in the GEDCOM) run
roughly in fetch order, a breadth-first search out from Abul Hamza (I1), so the newest IDs are the
frontier. Compares two snapshots: who was added, their birth years and places, how many hops from
Abul Hamza, and whether the ring people / home regions appear.
Usage: python fetch_progress.py OLD.ged NEW.ged"""
import sys, re, collections
from ged_lib import load
RING = r'pfinzing|g(u|ü)ntersberg|axelsdatter|\bR(ø|oe)mer\b'
HOME = r'östergötland|ostergotland|rogaland|stavanger|høgsfjord|forsand|sandnes|västerbotten|vasterbotten|skellefte|bureå'
old, _, _, _ = load(sys.argv[1])
new, nf, npar, nkids = load(sys.argv[2])
num = lambda x: int(re.sub(r'\D', '', x) or 0)
# hops from Abul Hamza over parent, child and spouse links (the fetch's breadth-first search)
nb = collections.defaultdict(set)
for f in nf.values():
    ps, cs = f['par'], f['chil']
    for a in ps:
        for b in ps:
            if a != b: nb[a].add(b)
        for c in cs: nb[a].add(c); nb[c].add(a)
hop = {'@I1@': 0}; front = ['@I1@']
while front:
    nxt = []
    for n in front:
        for m in nb.get(n, ()):
            if m not in hop: hop[m] = hop[n] + 1; nxt.append(m)
    front = nxt
added = sorted((x for x in new if x not in old), key=num)
print(f'old {len(old)}, new {len(new)}, added {len(added)}; ID range of added: {num(added[0]) if added else "-"}–{num(added[-1]) if added else "-"}')
ys = [new[x]['birt'] for x in added if new[x]['birt'] is not None]
print(f'added with a birth year: {len(ys)}')
c = collections.Counter((y // 50) * 50 for y in ys)
for k in sorted(c): print(f'  {k}–{k+49}: {c[k]}')
if ys: print('  median', sorted(ys)[len(ys)//2], 'min', min(ys), 'max', max(ys))
h = collections.Counter(hop.get(x) for x in added)
print('hops from Abul Hamza (added):', sorted(h.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))
pl = collections.Counter()
for x in added:
    p = new[x]['bplac']
    if p: pl[[s.strip() for s in p.split(',') if s.strip()][-1]] += 1
print('added, birth country/region (last part of place):', pl.most_common(12))
print('-- frontier (last 25 by ID):')
for x in sorted(new, key=num)[-25:]:
    print(f"  {x} hop {hop.get(x)} | {new[x]['name'][:45]} | {new[x]['birt']} | {new[x]['bplac'][:45]}")
print('-- ring people in the new GEDCOM:')
for x in sorted((x for x in new if re.search(RING, new[x]['name'], re.I)), key=num)[:20]:
    print(f"  {x} hop {hop.get(x)} | {new[x]['name']} | {new[x]['birt']}")
hr = [x for x in new if re.search(HOME, new[x]['bplac'] or '', re.I)]
print(f'-- born in her home regions (Östergötland, Rogaland, Västerbotten…): {len(hr)}')
for x in sorted(hr, key=lambda x: hop.get(x, 999))[:15]:
    print(f"  {x} hop {hop.get(x)} | {new[x]['name'][:40]} | {new[x]['birt']} | {new[x]['bplac'][:50]}")
