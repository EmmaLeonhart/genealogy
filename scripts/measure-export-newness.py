"""How many people does one export bring that no other export has?

    python scripts/measure-export-newness.py exports/dir/export-Forest-<id>.ged

Answers the one question asked of every export as it lands: was this seed worth
running? It compares the target file's `INDI` xrefs against the union of every
other GEDCOM in the corpus, so the count is *new to the corpus*, not new to the
merged tree -- which is the same thing, and is cheap. `out/merged.ged` is a
1.6 GB artefact of a merge that takes over ten minutes; nothing here needs it.

`genimerge.sources` decides what the corpus is, so `exports/excluded/` and
byte-identical repeats are skipped for free.

Prints one line per person for `--names` so a seed that landed in the wrong
neighbourhood is visible as names rather than as a percentage.
"""
import sys
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
sys.stdout.reconfigure(encoding='utf-8')

from genimerge.sources import find_exports  # noqa: E402

XREF = re.compile(r'^0 (@I[0-9]+@) INDI')


def individuals(path):
    """The INDI xrefs in one GEDCOM, and the NAME line of each."""
    ids, names, cur = set(), {}, None
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            m = XREF.match(line)
            if m:
                cur = m.group(1)
                ids.add(cur)
            elif line.startswith('0 '):
                cur = None
            elif cur and line.startswith('1 NAME ') and cur not in names:
                names[cur] = line[7:].strip()
    return ids, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('--names', action='store_true',
                    help='print every new person, not just the count')
    ap.add_argument('--roster', help='a TSV with a geni_id column to intersect against')
    args = ap.parse_args()

    target = Path(args.target).resolve()
    mine, names = individuals(target)
    print(f'{target.name}: {len(mine)} people')

    others = [p for p in find_exports() if Path(p).resolve() != target]
    print(f'comparing against {len(others)} other exports')

    seen = set()
    for i, p in enumerate(others, 1):
        got, _ = individuals(p)
        seen |= got
        if i % 50 == 0:
            print(f'  ...{i}/{len(others)}, {len(seen)} distinct so far', flush=True)

    new = mine - seen
    pct = 100.0 * len(new) / len(mine) if mine else 0.0
    print(f'\n{len(new)} new ({pct:.1f}%) out of {len(mine)}')
    print(f'corpus was {len(seen)} distinct people; now {len(seen | mine)}')

    if args.names:
        for x in sorted(new):
            print(f'  {x[2:-1]}\t{names.get(x, "")}')

    if args.roster:
        import csv
        want = set()
        with open(args.roster, encoding='utf-8') as f:
            for row in csv.DictReader(f, delimiter='\t'):
                for gid in (row.get('geni_id') or '').split(';'):
                    if gid.strip():
                        want.add(f'@I{gid.strip()}@')
        print(f'\nroster: {len(want)} known Geni ids; '
              f'{len(want & mine)} of them are in this export, '
              f'{len(want & new)} of those brought in by it')


if __name__ == '__main__':
    main()
