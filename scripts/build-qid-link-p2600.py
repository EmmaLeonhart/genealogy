"""Turn the About Me Wikidata links into `P2600` statements for 2026-09-01.

    python scripts/build-qid-link-p2600.py

`reports/geni-qid-links.tsv` is the identifier Emma wrote into these Geni profiles
herself. Every row is a claim that *this Geni profile is that Wikidata item*, and
`P2600` *Geni.com profile ID* is where that claim belongs on Wikidata.

Three populations, and only the last two are work:

* **already stated** -- Wikidata carries this exact pair. Nothing to do.
* **no `P2600` at all** -- a straight addition.
* **a different Geni id already** -- a *second* statement, not a conflict.
  `CLAUDE.md`: two Geni profiles for one person is a permanent feature of Geni,
  `P2600` is multi-valued, and 2861 stored items already carry more than one.
  Never replace, never withhold, never adjudicate.

**The comparison is against `out/wikidata/p2600-all.tsv`, which is a snapshot.** An
item that gained a `P2600` after that dump reads here as an addition; QuickStatements
is idempotent for an identical statement, so the cost of that staleness is a no-op,
not a wrong edit.

Writes `reports/wikidata-geni-qid-p2600.qs` and `reports/geni-qid-p2600-gap.tsv`.
"""
import sys
import csv
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


def existing():
    """(qid, geni id) pairs Wikidata already states, and the QIDs that have any."""
    pairs, qids = set(), set()
    with open(ROOT / 'out' / 'wikidata' / 'p2600-all.tsv', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter='\t'):
            if len(row) >= 2 and row[0].startswith('Q'):
                pairs.add((row[0].strip(), row[1].strip()))
                qids.add(row[0].strip())
    return pairs, qids


def main():
    pairs, qids = existing()
    print(f'{len(qids)} QIDs already carry a P2600 ({len(pairs)} pairs) in the snapshot')

    links = list(csv.DictReader(
        open(ROOT / 'reports' / 'geni-qid-links.tsv', encoding='utf-8'), delimiter='\t'))
    rows = []
    for r in links:
        for q in r['qids'].split(';'):
            if not q:
                continue
            g = r['geni_id']
            if (q, g) in pairs:
                kind = 'already stated'
            elif q in qids:
                kind = 'second geni id'
            else:
                kind = 'addition'
            rows.append((q, g, kind, r.get('geni_name', '')))

    counts = {}
    for _, _, k, _ in rows:
        counts[k] = counts.get(k, 0) + 1
    print(f'\n{len(rows)} pairs from the About Me links')
    for k in ('already stated', 'addition', 'second geni id'):
        print(f'  {k:<16} {counts.get(k, 0)}')

    todo = [r for r in rows if r[2] != 'already stated']

    qs = ROOT / 'reports' / 'wikidata-geni-qid-p2600.qs'
    with open(qs, 'w', encoding='utf-8', newline='\n') as f:
        for q, g, _kind, _name in todo:
            f.write(f'{q}\tP2600\t"{g}"\n')
    print(f'\nwrote {qs.relative_to(ROOT)} -- {len(todo)} statements, for 2026-09-01')

    gap = ROOT / 'reports' / 'geni-qid-p2600-gap.tsv'
    with open(gap, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'geni_id', 'kind', 'geni_name'])
        w.writerows(rows)
    print(f'wrote {gap.relative_to(ROOT)} -- all {len(rows)} pairs with their status')


if __name__ == '__main__':
    main()
