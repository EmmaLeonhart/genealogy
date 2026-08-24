"""Is the edit graph the batches declare actually resolvable?

    python scripts/audit-edit-graph.py

Every JSON batch in `reports/` carries a `requires` list naming the `id`s of edits
that must land first. `CLAUDE.md` leans on that ordering in the one place it matters
most: the `NN` label fix is **two** edits per item, the `mul` one declared as a
dependency of the `en` one, *"so the marker is written before the slot holding it is
reused"*. Get that order wrong on the 1,271 items whose only `NN` lives in `en` and
the marker is gone.

So the graph is worth checking, and this checks three things:

* **Dangling `requires`** — a dependency naming an `id` no batch emits. The edit can
  never be unblocked by anything in this repo.
* **Duplicate `id`s** — two edits claiming the same name, so a `requires` pointing at
  it is ambiguous and a run that skips "already done" ids may skip the wrong one.
* **Cycles** — A before B before A.

Writes `reports/edit-graph.md`. Reads only `reports/`; sends nothing anywhere.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'reports'


def load():
    """(file name, edit) for every edit object in every JSON batch."""
    for path in sorted(REPORTS.glob('wikidata-*.json')):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except ValueError:
            continue
        items = data if isinstance(data, list) else data.get('edits', [])
        for item in items:
            if isinstance(item, dict):
                yield path.name, item


def main():
    edits = list(load())
    print(f'{len(edits)} edit objects across the JSON batches')

    owner, dupes = {}, Counter()
    for name, e in edits:
        i = e.get('id')
        if i in owner:
            dupes[i] += 1
        owner[i] = name
    print(f'{len(owner)} distinct ids; {len(dupes)} appear more than once')

    dangling = defaultdict(Counter)      # file -> Counter of missing prefix
    example = {}
    total_dangling = 0
    for name, e in edits:
        for r in e.get('requires') or []:
            if r not in owner:
                total_dangling += 1
                prefix = r.split(':', 1)[0]
                dangling[name][prefix] += 1
                example.setdefault((name, prefix), r)
    print(f'{total_dangling} `requires` entries name an id no batch emits')

    lines = ['# The edit graph the batches declare', '',
             f'{len(edits)} edit objects, {len(owner)} distinct ids.', '']

    if dupes:
        lines += ['## Duplicate ids', '',
                  'Two edits claiming one name. A `requires` pointing at it is '
                  'ambiguous, and a run that skips ids it has already done may skip '
                  'the wrong one.', '',
                  '| id | extra copies | file |', '| --- | ---: | --- |']
        for i, n in dupes.most_common(20):
            lines.append(f'| `{i}` | {n} | `{owner[i]}` |')
        if len(dupes) > 20:
            lines.append(f'| … | | {len(dupes) - 20} more |')
        lines.append('')

    if dangling:
        lines += ['## Dependencies nothing emits', '',
                  'A `requires` naming an id no batch produces. Nothing in this repo '
                  'can ever satisfy it.', '',
                  '| batch | missing prefix | count | example |',
                  '| --- | --- | ---: | --- |']
        for name in sorted(dangling, key=lambda n: -sum(dangling[n].values())):
            for prefix, n in dangling[name].most_common():
                lines.append(f'| `{name}` | `{prefix}:` | {n} | '
                             f'`{example[(name, prefix)]}` |')
        lines.append('')

    # Cycles, over the edges that do resolve.
    graph = {e.get('id'): [r for r in (e.get('requires') or []) if r in owner]
             for _n, e in edits}
    colour, cycles = {}, []

    def walk(node, stack):
        if colour.get(node) == 2:
            return
        if colour.get(node) == 1:
            cycles.append(stack[stack.index(node):] + [node])
            return
        colour[node] = 1
        for nxt in graph.get(node, ()):
            walk(nxt, stack + [nxt])
        colour[node] = 2

    sys.setrecursionlimit(100000)
    for node in graph:
        if colour.get(node) is None:
            walk(node, [node])

    lines += ['## Cycles', '',
              (f'**{len(cycles)} cycles** among the edges that resolve.'
               if cycles else 'None among the edges that resolve.'), '']
    for c in cycles[:10]:
        lines.append(f'- {" → ".join(c)}')

    print(f'{len(cycles)} cycles among the resolvable edges')

    out = REPORTS / 'edit-graph.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'wrote {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
