"""Match one export's people against the Izumo roster on the REGNAL NUMBER.

    python scripts/match-izumo-export.py exports/izumo/export-Forest-<id>.ged

`walk-izumo-geni.py` matches romanised names against `out/merged.ged`, which
means it needs a re-merge before it can see a fresh export and it carries all the
risk of name matching. This does neither.

**Geni writes the regnal number inside the name** -- `Harutaka 64 /Kitajima/`,
`Takamune /Senge/` -- and the roster carries it in its own column. Number plus
lineage is an exact join and immune to romanisation: the 2008 Japanese, 2011
English and 2026 additions spell these men differently and number them
identically. Where Geni omits the number (the two men of the 1340 split are
written bare), the surname plus given name is used, tokens matching exactly.

Two passes, because the roster holds two shapes of person:

* the **lineage** rows, whose Geni surname is `Izumo`, `Senge` or `Kitajima` --
  joined on lineage plus number.
* the **kokuso** rows from before those surnames existed, written
  `Mishima 15 /Ashinazu-ni-Mikoto/` -- joined on the number plus an exactly
  matching name token, and where Geni omits the number, on the whole name matching
  exactly once punctuation and case are normalised away (`Kushidanomikoto` is
  `Kushida-no-mikoto`). Neither is a similarity judgement, and a name landing on
  more than `AMBIGUITY_LIMIT` people is reported rather than resolved.

Running only the first pass and reporting its total is how "76 of 77, complete"
came to be said on 2026-08-23 while fifteen numbered kokuso had never been looked
at at all.

Also reports numbered Izumo/Senge/Kitajima people the roster does NOT list -- the
succession the Shinto-wiki chart stops short of.
"""
import sys
import re
import csv
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

LINEAGES = ('Senge', 'Kitajima', 'Izumo-kokuso', 'Izumo')
ASCII_DIGITS = re.compile(r'[0-9]+')
#: A name landing on more people than this is reported rather than resolved.
AMBIGUITY_LIMIT = 3


def norm(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^0-9a-zA-Z]+', '', t).lower()


def norm_spaced(t):
    """Like `norm` but keeps token boundaries, so a name can be split into tokens."""
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^0-9a-zA-Z]+', ' ', t).lower()


def parse_name(raw):
    """`Harutaka 64 /Kitajima/` -> ('harutaka', 64, 'Kitajima')."""
    m = re.match(r'^(.*?)\s*/([^/]*)/\s*$', raw)
    given, surname = (m.group(1), m.group(2)) if m else (raw, '')
    num = None
    toks = []
    for t in given.split():
        # ASCII digits only. `str.isdigit()` is true for superscripts and other
        # Unicode numerals that `int()` then refuses -- which crashed the corpus
        # run at export 100 on a name carrying one. A regnal number is written in
        # plain digits, so nothing is lost by being strict.
        if ASCII_DIGITS.fullmatch(t):
            num = int(t)
        else:
            toks.append(t)
    return norm(' '.join(toks)), num, surname.strip()


def read(path, people):
    cur = None
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('0 @I'):
                cur = line.split()[1][2:-1]
            elif line.startswith('0 '):
                cur = None
            elif cur and line.startswith('1 NAME ') and cur not in people:
                raw = line[7:].strip()
                g, n, s = parse_name(raw)
                people[cur] = (g, n, s, raw)
    return people


def main():
    """`--corpus` asks the question that actually matters, and it is not the same one.

    Run against one file, this says what that export holds. Run with `--corpus` it
    says what **we** hold, across every GEDCOM `genimerge.sources` recognises.
    Confusing the two cost an export on 2026-08-23: the file view reported Izumo
    18-33 absent, an export was run to fetch them, and all sixteen were already in
    the corpus under a different export.
    """
    arg = sys.argv[1]
    people = {}          # geni id -> (given, regnal, surname, raw)

    if arg == '--corpus':
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
        from genimerge.sources import find_exports
        paths = list(find_exports())
        for i, p in enumerate(paths, 1):
            read(p, people)
            if i % 100 == 0:
                print(f'  ...{i}/{len(paths)}', flush=True)
        print(f'{len(people)} people across {len(paths)} exports')
        path = 'the corpus'
    else:
        path = arg
        read(path, people)
        print(f'{len(people)} people in {path.split("/")[-1]}')

    by_num = {}          # (lineage, regnal) -> [ids]
    by_name = {}         # (lineage, given) -> [ids]
    for gid, (g, n, s, _) in people.items():
        lin = next((L for L in LINEAGES if L.lower() in s.lower()), None)
        if not lin:
            continue
        if lin == 'Izumo-kokuso':
            lin = 'Izumo'
        if n is not None:
            by_num.setdefault((lin, n), []).append(gid)
        if g:
            by_name.setdefault((lin, g), []).append(gid)

    numbered = sum(len(v) for v in by_num.values())
    print(f'{numbered} of them carry a regnal number in a lineage surname')

    # The kokuso before the lineage surnames existed. Geni writes them
    # `Mishima 15 /Ashinazu-ni-Mikoto/`, `Ou 16 /Ashinazu-ni-Mikoto/` -- the regnal
    # number is there but the surname is a divine epithet, not `Izumo`, so the
    # lineage index above cannot see them. Fifteen of the 89 numbered roster rows
    # are these, and reporting "76 of 77" while never looking at them is the
    # single-file mistake in another costume: a complete answer to a narrower
    # question.
    #
    # The join is the number AND an exactly-matching name token. The number alone
    # would collide across 1.3M people; a token alone is name matching. Both
    # together are as exact as the lineage join and use no similarity at all.
    any_num = {}
    for gid, (g, n, s, raw) in people.items():
        if n is None:
            continue
        toks = {t for t in re.split(r'[^0-9a-zA-Z]+', norm_spaced(raw)) if t and not t.isdigit()}
        any_num.setdefault(n, []).append((gid, toks, raw))

    whole_name = {}
    for gid, (g, n, s_, raw) in people.items():
        whole_name.setdefault(norm(raw.replace('/', ' ')), []).append(gid)

    roster = list(csv.DictReader(open('reports/izumo-roster.tsv', encoding='utf-8'),
                                 delimiter='\t'))
    hit, miss = [], []
    used = set()
    for row in roster:
        lin = (row.get('lineage') or '').strip()
        if lin not in ('Senge', 'Kitajima', 'Izumo'):
            continue
        name = row.get('name') or ''
        regnal = (row.get('regnal') or '').strip()
        given = norm(name.split(' no ')[-1]) if ' no ' in name else norm(name)

        ids = []
        how = ''
        if regnal.isdigit() and (lin, int(regnal)) in by_num:
            ids = by_num[(lin, int(regnal))]
            how = f'regnal {regnal}'
        elif (lin, given) in by_name:
            ids = by_name[(lin, given)]
            how = 'name'

        if ids:
            used.update(ids)
            hit.append((regnal, lin, name, ';'.join(ids), how))
        else:
            miss.append((regnal, lin, name))

    where = path if path == 'the corpus' else path.split('/')[-1]
    print(f'\n{len(hit)} rostered lineage people found in {where}, {len(miss)} not')
    print('\nfound:')
    for r, lin, name, ids, how in hit:
        print(f'  {r or "-":>3}  {lin:<9} {name:<32} {ids}  [{how}]')
    print(f'\nnot in {where}:')
    for r, lin, name in miss:
        print(f'  {r or "-":>3}  {lin:<9} {name}')

    extra = sorted(
        (people[g][1], people[g][2], people[g][3], g)
        for k, v in by_num.items() for g in v if g not in used)
    print(f'\n{len(extra)} numbered lineage people here the roster does NOT list:')
    for n, s, raw, g in extra:
        print(f'  {n:>3}  {s:<12} {raw:<34} {g}')

    # The 15 numbered kokuso whose Geni surname is not a lineage name.
    khit, kmiss = [], []
    for row in roster:
        lin = (row.get('lineage') or '').strip()
        if lin in ('Senge', 'Kitajima', 'Izumo'):
            continue
        regnal = (row.get('regnal') or '').strip()
        if not regnal.isdigit():
            continue
        want = {t for t in norm_spaced(row.get('name') or '').split() if t}
        ids = [gid for gid, toks, _ in any_num.get(int(regnal), []) if want & toks]
        how = f'regnal {regnal} + name token'

        if not ids:
            # Geni often omits the number for the earliest kokuso -- it writes
            # `Kushida-no-mikoto`, not `Kushida 8 ...`. Fall back to the whole name
            # matching EXACTLY once punctuation and case are normalised away:
            # `Kushidanomikoto` and `Kushida-no-mikoto` are the same string written
            # two ways, which is not a similarity judgement. A name landing on more
            # than AMBIGUITY_LIMIT people is reported ambiguous rather than resolved,
            # the rule `genimerge.paths` already applies for the same reason.
            ids = whole_name.get(norm(row.get('name') or ''), [])
            how = 'whole name, exact after normalising'
            if len(ids) > AMBIGUITY_LIMIT:
                kmiss.append((regnal, row.get('name'), (row.get('qid') or '').strip(),
                              f'AMBIGUOUS ({len(ids)})'))
                continue

        if ids:
            khit.append((regnal, row.get('name'), (row.get('qid') or '').strip(),
                         ';'.join(ids), how))
        else:
            kmiss.append((regnal, row.get('name'), (row.get('qid') or '').strip(), 'absent'))

    print(f'\nnumbered kokuso outside the three lineages: '
          f'{len(khit)} found, {len(kmiss)} not')
    for r, name, q, ids, how in khit:
        print(f'  {r:>3}  {name:<34} {q:<12} {ids}  [{how}]')
    print('  --- not resolved ---')
    for r, name, q, why in kmiss:
        print(f'  {r:>3}  {name:<34} {q:<12} {why}')

    # The pairings, for a P2600 batch once this repo's start date passes. A row
    # with more than one Geni id is a duplicate set on Geni -- emitted as it is,
    # because a second P2600 on one item is the correct representation of that
    # and the merges are Emma's.
    qid_of = {(r.get('regnal', '').strip(), r.get('name', '')): (r.get('qid') or '').strip()
              for r in roster}
    out = 'reports/izumo-p2600-pairs.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'regnal', 'lineage', 'name', 'geni_ids', 'matched_on'])
        n = 0
        for r, lin, name, ids, how in hit:
            q = qid_of.get((r, name), '')
            if not q:
                continue
            w.writerow([q, r, lin, name, ids, how])
            n += 1
        for r, name, q, ids, how in khit:
            if not q:
                continue
            w.writerow([q, r, 'kokuso', name, ids, how])
            n += 1
    print(f'\nwrote {out} -- {n} rows ({len(hit)} lineage + {len(khit)} kokuso), '
          f'every one carrying a Wikidata item')


if __name__ == '__main__':
    main()
