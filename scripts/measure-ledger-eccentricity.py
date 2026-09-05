"""Eccentricity inside the LEDGER graph -- who is furthest out among her own Wikidata items.

    PYTHONPATH=src python scripts/measure-ledger-eccentricity.py

**Emma, 2026-09-05:** *"Is 'Emma Leonhart' the most eccentric person in the graph as saved from
wikidata please just tell me. Most eccentric in the ledger."* Answer, measured: **no** --
eccentricity 37, rank 128 of 733, against a maximum of 44 held jointly by Charlemagne `Q3044`,
Carl Gustaf Wennerstedt `Q6235986` and Conrad von Braunjohan `Q141250225`.

**⛔ HER ITEM IS `Q140568870`, NOT `Q232803`.** `Q232803` is *Empress Jingū*, which is the name her
GENI profile carries -- `CLAUDE.md` § *Her name is Empress Jingū* -- and it is a different item
about a different person. Reaching for it gives a completely wrong answer rather than a slightly
wrong one: `Q232803` holds **0** edges in this graph and sits outside the 733-person component
entirely, so it reads as maximally disconnected. Her own item has 2 edges and is inside.

**The graph is the one `wikidata_subgraph()` walks**, and it is not Wikidata: an edge counts only
when **both ends are items she has edited**. Unrestricted, Bureus sits in Wikidata's 1.34-million
genealogical component and the answer would be about the world tree. See that function for why.

**Eccentricity here is distance within her own contributions**, so it moves as she edits. A person
at the maximum is one the rest of her work has not reached round to, which is the same reading
`reports/eccentricity.md` gives for the Geni tree -- and § *Eccentricity is PARTLY A RECENCY
MEASURE* applies identically: a recently created item sits wherever its one edge left it.
"""
import collections, csv, importlib.util, pathlib, sys
ROOT = pathlib.Path("/home/user/genealogy"); sys.path.insert(0,str(ROOT/"scripts"))
sp=importlib.util.spec_from_file_location('bg',ROOT/'scripts'/'build-garborg-day.py')
bg=importlib.util.module_from_spec(sp); sp.loader.exec_module(bg)
led = bg.ledger()
universe=set(led.values())
adj=collections.defaultdict(set)
def link(a,b):
    if a in universe and b in universe: adj[a].add(b); adj[b].add(a)
P=("P22","P25","P26","P40","P3373")
with open(ROOT/"out"/"wikidata"/"relations.tsv",encoding="utf-8") as fh:
    for row in csv.DictReader(fh,delimiter="\t"):
        if row["qid"] in universe:
            for p in P:
                for v in (row.get(p) or "").split(): link(row["qid"],v)
with open(ROOT/"reports"/"garborg-live-values.tsv",encoding="utf-8") as fh:
    for row in csv.DictReader(fh,delimiter="\t"):
        if row.get("property") in P: link(row["qid"],(row.get("value") or "").strip())
lab={}
with open(ROOT/"reports"/"garborg-qids.tsv",encoding="utf-8") as fh:
    for r in csv.DictReader(fh,delimiter="\t"):
        if r.get("qid"): lab[r["qid"]]=r.get("label","")
EMMA="Q140568870"
print(f"Emma Leonhart {EMMA}: {len(adj.get(EMMA,()))} edges")
# component containing Emma
seen={EMMA}; st=[EMMA]; comp=[]
while st:
    n=st.pop(); comp.append(n)
    for m in adj[n]:
        if m not in seen: seen.add(m); st.append(m)
print(f"her component: {len(comp):,} people")
def bfs(s):
    d={s:0}; q=collections.deque([s])
    while q:
        n=q.popleft()
        for m in adj[n]:
            if m not in d: d[m]=d[n]+1; q.append(m)
    return d
comp_set=set(comp)
ecc={}
for n in comp:
    d=bfs(n)
    ecc[n]=max(d.values())
order=sorted(ecc.items(), key=lambda kv:-kv[1])
mx=order[0][1]
top=[q for q,e in order if e==mx]
print(f"\nmax eccentricity in her component: {mx}")
print(f"people tied at it: {len(top)}")
for q in top[:12]: print(f"   {q:12} {lab.get(q,'')[:44]}")
rank=[q for q,_ in order].index(EMMA)+1
print(f"\nEmma: eccentricity {ecc[EMMA]}, rank {rank} of {len(order)}")
print(f"IS SHE THE MOST ECCENTRIC? {'YES' if ecc[EMMA]==mx and len(top)==1 else ('TIED at the max' if ecc[EMMA]==mx else 'NO')}")
