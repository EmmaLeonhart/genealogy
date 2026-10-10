import re
def load(path):
    ind={}; fam={}; cur=None; kind=None; ev=None
    for line in open(path,encoding='utf-8',errors='replace'):
        p=line.rstrip('\n').split(' ',2); lvl=p[0]
        if lvl=='0':
            ev=None
            if len(p)>2 and p[2].startswith('INDI'): cur=p[1]; kind='I'; ind[cur]={'name':'','birt':None,'deat':None,'bplac':'','famc':[],'fams':[],'sex':'','fs':''}
            elif len(p)>2 and p[2].startswith('FAM'): cur=p[1]; kind='F'; fam[cur]={'par':[],'chil':[]}
            else: kind=None
        elif kind=='I':
            if lvl=='1': ev=p[1]
            v=p[2] if len(p)>2 else ''
            if lvl=='1' and p[1]=='NAME' and not ind[cur]['name']: ind[cur]['name']=v.replace('/','').strip()
            if lvl=='1' and p[1]=='SEX': ind[cur]['sex']=v
            if lvl=='1' and p[1]=='FAMC': ind[cur]['famc'].append(v)
            if lvl=='1' and p[1]=='FAMS': ind[cur]['fams'].append(v)
            if lvl=='1' and p[1]=='_FSFTID': ind[cur]['fs']=v
            if lvl=='2' and p[1]=='PLAC' and ev=='BIRT': ind[cur]['bplac']=v
            if lvl=='2' and p[1]=='DATE' and ev in('BIRT','DEAT'):
                m=re.search(r'(\d{1,4})\s*(B\.?C\.?|BCE)?\s*$',v.strip())
                if m:
                    y=int(m.group(1)); y=-y if m.group(2) else y
                    ind[cur]['birt' if ev=='BIRT' else 'deat']=y
        elif kind=='F' and lvl=='1':
            if p[1] in('HUSB','WIFE'): fam[cur]['par'].append(p[2])
            if p[1]=='CHIL': fam[cur]['chil'].append(p[2])
    par={i:[q for f in v['famc'] if f in fam for q in fam[f]['par']] for i,v in ind.items()}
    kids={i:[c for f in v['fams'] if f in fam for c in fam[f]['chil']] for i,v in ind.items()}
    return ind,fam,par,kids
def ancestors(i,par):
    seen={}; front=[(i,0)]
    while front:
        n,d=front.pop()
        for q in par.get(n,[]):
            if q not in seen or seen[q]>d+1: seen[q]=d+1; front.append((q,d+1))
    return seen
