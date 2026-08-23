"""Roster of the Izumo clan genealogy from the Shinto-wiki page.

Emma's queue item: build the family tree that is visually on
https://shinto.miraheze.org/wiki/Izumo_clan onto Geni, and carry the Wikidata
links. The rendered page mangles the {{familytree}} template into unusable prose;
the wikitext does not, so this parses the wikitext.

Each person is an {{ill|Name|lang|...|qid=Q...}} inside a familytree cell. A
bolded name with a <sup>N</sup> is an Izumo no Kuni no Miyatsuko and N is their
REGNAL NUMBER, not a middle name -- Emma flagged that specifically. Lineage is
read off the name prefix once the clan splits in 1340 into Senge and Kitajima.

Writes reports/izumo-roster.tsv. Nothing here touches Geni or Wikidata.
"""
import re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')

wt = open(sys.argv[1], encoding='utf-8').read()
i = wt.find('== Genealogy ==')
j = wt.find('== See also ==', i)
gen = wt[i:j if j > 0 else len(wt)]
print(f'genealogy section: {len(gen)} chars')

# {{ill|Display|...|qid=Qnnn|...}}  -- take the display name and the qid
ILL = re.compile(r'\{\{ill\|([^|}]+)((?:\|[^{}]*?)*)\}\}')
SUP = re.compile(r'<sup>(\d+)</sup>')

rows = []
seen = set()
for m in ILL.finditer(gen):
    name = m.group(1).strip()
    rest = m.group(2) or ''
    q = ''
    mq = re.search(r'\|qid=(Q\d+)', rest)
    if mq: q = mq.group(1)
    # regnal number: a <sup>N</sup> immediately following this template
    tail = gen[m.end():m.end() + 40]
    ms = SUP.search(tail)
    regnal = ms.group(1) if ms and tail.index(ms.group(0)) < 12 else ''
    bold = gen[max(0, m.start() - 3):m.start()].endswith("'''")
    key = (name, q, regnal)
    if key in seen: continue
    seen.add(key)
    lin = ('Senge' if name.startswith(('Senge', 'Sengeno')) else
           'Kitajima' if name.startswith(('Kitajima', 'Kitashima')) else
           'Izumo' if name.startswith('Izumo') else
           'other')
    rows.append((regnal, name, q, lin, 'kokuso' if (bold or regnal) else ''))

def keyf(r):
    return (int(r[0]) if r[0] else 9999, r[1])
rows.sort(key=keyf)

with open('reports/izumo-roster.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['regnal', 'name', 'qid', 'lineage', 'role'])
    w.writerows(rows)

withq = sum(1 for r in rows if r[2])
regn = sum(1 for r in rows if r[0])
print(f'{len(rows)} people, {withq} with a Wikidata qid, {regn} carrying a regnal number')
import collections
print('lineage:', dict(collections.Counter(r[3] for r in rows)))
print('\nfirst 20 by regnal number:')
for r in rows[:20]:
    print(f"  {r[0] or '-':>4}  {r[3]:<9} {r[2] or '-':>12}  {r[1][:44]}")
