"""Count every generated Wikidata batch, so the table in `todo.md` is not guesswork.

    python scripts/audit-built-batches.py

`todo.md` § *The built batches, and the 1 September date* is a list of what exists.
It was last counted by hand on 2026-08-17, and the note above it records that
**four of the ten rows were out of date and three batches were missing entirely**
the time before. A hand-maintained inventory of generated files drifts by
construction: every generator that runs changes a number nobody updates.

So count them. A JSON batch is a list of edit objects; a `.qs` batch is one
statement per non-comment line, with `CREATE` counted separately because a creation
is a different kind of act from a statement.

Prints a markdown table ready to paste, and writes `reports/built-batches.tsv`.
Reads nothing but `reports/`; talks to nothing.
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'reports'


def count_json(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, OSError) as e:
        return None, f'unreadable: {e}'
    if isinstance(data, list):
        return len(data), 'edit objects'
    if isinstance(data, dict):
        return len(data), 'keys'
    return None, 'not a list or object'


def count_qs(path):
    creates = statements = 0
    for raw in path.read_text(encoding='utf-8').split('\n'):
        line = raw.rstrip('\r').strip()
        if not line or line.startswith('#'):
            continue
        if line == 'CREATE':
            creates += 1
        else:
            statements += 1
    what = f'{statements} statements'
    if creates:
        what = f'{creates} creations + {what}'
    return statements + creates, what


def main():
    rows = []
    for path in sorted(REPORTS.glob('wikidata-*.json')) + sorted(REPORTS.glob('*.qs')):
        n, what = count_json(path) if path.suffix == '.json' else count_qs(path)
        rows.append((path.name, n if n is not None else -1, what))

    rows.sort(key=lambda r: (-r[1], r[0]))

    print(f'{len(rows)} generated batches in reports/\n')
    print('| batch | entries | shape |')
    print('| --- | ---: | --- |')
    for name, n, what in rows:
        print(f'| `reports/{name}` | {n if n >= 0 else "?"} | {what} |')

    out = REPORTS / 'built-batches.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['batch', 'entries', 'shape'])
        for name, n, what in rows:
            w.writerow([f'reports/{name}', n if n >= 0 else '', what])
    print(f'\nwrote {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
