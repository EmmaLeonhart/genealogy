"""Candidate missing parents for Emma's dead ends, taken from Abul Hamza's descendants.

A dead end is one of her synoptic-tree ancestors with no parents (and no duplicate profile with
parents). A candidate parent is one of his synoptic-tree descendants who was born 16-55 years
before the dead end, shares a real family or farm name with the dead end (not a patronymic, not a
title), and, when the dead end carries a patronymic (Olsdatter, Andersson, Petersen...), has the
matching given name. Candidates are leads for Emma to judge, never links to apply.

Usage: python dead_ends.py MERGED SETS.pkl OUT_MD"""
import sys, re, pickle, collections
from ged_lib import load
from compare_ah import norm, twins_index, PLACEHOLDER, ALIAS
from family_confirmed import strong

PATRO = re.compile(r'^(.+?)(?:sdotter|sdatter|sdottir|sdatter|dotter|datter|dottir|sson|ssen|sen|son)$')

def words(p):
    return [x for x in norm(p['name']) if x not in PLACEHOLDER]

def patronym_father(ws):
    # "anders olsdatter" -> "ol"; matched by prefix against the father's given name
    for w in ws[1:]:
        m = PATRO.match(w)
        if m and len(m.group(1)) >= 2:
            return m.group(1)
    return None

GIVEN = set()  # filled after loading: words that are someone's first name 20+ times

def family_names(ws):
    # the last name word only, when it is not a patronymic, title or common first name
    if len(ws) < 2:
        return set()
    w = ws[-1]
    return {w} if w in strong({w}) and not PATRO.match(w) and len(w) >= 4 and w not in GIVEN else set()

merged, mfam, mpar, mkids = load(sys.argv[1])
sets = pickle.load(open(sys.argv[2], 'rb'))
anc, his = sets['anc'], sets['his']
mtw = twins_index(merged)
_c = collections.Counter(words(p)[0] for p in merged.values() if words(p))
GIVEN.update(w for w, n in _c.items() if n >= 20)

dead = [a for a in anc if not mpar.get(a) and not any(mpar.get(t) for t in mtw(a))
        and merged[a]['birt'] is not None]
print('her dead ends with a birth year:', len(dead), file=sys.stderr)

byname = collections.defaultdict(list)
for h in his:
    p = merged[h]
    if p['birt'] is None:
        continue
    for w in family_names(words(p)):
        byname[w].append(h)

rows = []
for a in dead:
    pa = merged[a]; wa = words(pa)
    fams = family_names(wa)
    if not fams:
        continue
    pf = patronym_father(wa)
    seen = set()
    for w in fams:
        for h in byname.get(w, []):
            if h in seen:
                continue
            seen.add(h)
            ph = merged[h]; gap = pa['birt'] - ph['birt']
            if not 16 <= gap <= 55:
                continue
            wh = words(ph)
            if pf and ph['sex'] == 'M' and not (wh and ALIAS.get(wh[0], wh[0]).startswith(pf[:3])):
                continue
            shared = fams & family_names(wh)
            rows.append((anc[a], a, h, gap, sorted(shared)))

rows.sort(key=lambda r: (r[0], r[3]))
by_dead = collections.defaultdict(list)
for r in rows:
    by_dead[r[1]].append(r)
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    f.write('# Candidate missing parents for Emma\'s dead ends, from Abul Hamza\'s descendants\n\n')
    f.write(f'{len(dead)} dead ends with a birth year; {len(by_dead)} have at least one candidate. '
            'Each candidate shares a family or farm name, was born 16-55 years earlier, and fits any '
            'patronymic. These are leads to judge, not links.\n\n')
    for a, rs in sorted(by_dead.items(), key=lambda kv: kv[1][0][0]):
        pa = merged[a]
        f.write(f"## {pa['name']} ({pa['birt']}), {anc[a]} generations above Emma, no parents recorded\n\n")
        for _, _, h, gap, shared in rs[:8]:
            ph = merged[h]
            f.write(f"- {ph['name']} ({ph['birt']}–{ph['deat']}), {gap} years older, shares {', '.join(shared)}\n")
        if len(rs) > 8:
            f.write(f'- … {len(rs) - 8} more\n')
        f.write('\n')
print('dead ends with candidates:', len(by_dead), 'candidate rows:', len(rows), file=sys.stderr)
