"""The join key Emma put in the data herself: a Wikidata URL in the Geni About Me.

    python scripts/build-geni-qid-links.py

Emma, 2026-08-23: *"we have intentionally added actual join keys for the Samaritan
high priests, Izumo clan, and Tanba clan... The wikidata items linked in the
descriptions."*

She is right and it is exact. Geni exports the About Me as
``1 NOTE {geni:about_me} https://wikidata.org/wiki/Special:EntityPage/Q135579415#…``
so the profile carries its own Wikidata identity. No name is consulted, no
number, no position in a succession -- an identifier written by hand for exactly
this purpose.

**This supersedes the regnal-number matcher for these families.** Wikidata does
not carry the regnal numbers at all, so joining on them was never a join *to*
Wikidata; it was a join to the Shinto-wiki page's own column. And the pass that
extended it to the earlier kokuso matched on the stopword ``no``, pairing Ame no
Hohi with a Swedish woman. Both are gone. Reach for this first.

**Only wikidata.org URLs count.** A bare ``Q…`` in free text is not a claim of
identity -- it could be a catalogue number, a road, a quotation -- and treating it
as one is how a loose pattern starts inventing links again. The URL form is what
Geni's editor produces when a Wikidata item is linked, so it is both tighter and
what is actually there.

Writes `reports/geni-qid-links.tsv`.
"""
import sys
import re
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
sys.stdout.reconfigure(encoding='utf-8')

from genimerge.sources import find_exports  # noqa: E402

#: `https://wikidata.org/wiki/Q123`, `.../wiki/Special:EntityPage/Q123`, with or
#: without `www.`, and whatever fragment Geni appends.
WD_URL = re.compile(
    r'https?://(?:www\.)?wikidata\.org/wiki/(?:Special:EntityPage/)?(Q[1-9][0-9]*)',
    re.I)


def main():
    qids = {}      # geni id -> set of QIDs
    names = {}     # geni id -> first NAME
    cur = None
    paths = list(find_exports())

    for i, p in enumerate(paths, 1):
        with open(p, encoding='utf-8', errors='replace') as f:
            for line in f:
                if line.startswith('0 @I'):
                    cur = line.split()[1][2:-1]
                elif line.startswith('0 '):
                    cur = None
                elif cur:
                    if line.startswith('1 NAME ') and cur not in names:
                        names[cur] = line[7:].strip()
                    found = WD_URL.findall(line)
                    if found:
                        qids.setdefault(cur, set()).update(q.upper() for q in found)
        if i % 100 == 0:
            print(f'  ...{i}/{len(paths)}, {len(qids)} linked so far', flush=True)

    print(f'\n{len(qids)} Geni profiles carry a Wikidata URL, over {len(paths)} exports')
    one = sum(1 for v in qids.values() if len(v) == 1)
    print(f'  {one} carry exactly one QID; {len(qids) - one} carry more than one')

    # A QID on two profiles is Geni's duplicate-profile situation, which is
    # ordinary here and is Emma's to merge -- never ours. Reported, not resolved.
    holders = {}
    for g, qs in qids.items():
        for q in qs:
            holders.setdefault(q, []).append(g)
    dupes = {q: g for q, g in holders.items() if len(g) > 1}
    print(f'  {len(holders)} distinct QIDs; {len(dupes)} of them sit on more than one profile')

    out = 'reports/geni-qid-links.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['geni_id', 'qids', 'geni_name'])
        for g in sorted(qids):
            w.writerow([g, ';'.join(sorted(qids[g])), names.get(g, '')])
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
