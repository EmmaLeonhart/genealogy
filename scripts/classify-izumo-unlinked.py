"""What ARE the 93 Izumo roster items no Geni profile links?

    python scripts/classify-izumo-unlinked.py

`reports/izumo-unlinked.tsv` is the residue of the About Me join: rostered Wikidata
items that no Geni profile in the corpus points at. Before any of them is treated as
a person to find or create, the obvious question is whether they are people at all.

**Some are not.** `scripts/build-izumo-roster.py` parses every `{{ill|…|qid=…}}` on
the Shinto-wiki page, and that page names clans, districts, offices and a publisher
alongside the office-holders — `Amabe clan`, `Kamo district`, `Aogaki Publishing`,
and a row whose name is literally `2020`. A `P2600` *Geni.com profile ID* on a
district would be nonsense, and a Geni profile created for one would be worse.

So this reads `P31` *instance of* out of the local Wikidata store. **A bare "is it
`Q5`?" is the wrong test** and reported thirteen of them as non-people on the first
run: Wikidata models the legendary emperors as `Q124710051` *legendary human figure*,
which is a statement about the evidence for them and not about their kind. Amaterasu
really is different — `Q511056` *solar deity*.

The store is a Geni-shaped slice seeded from `P2600` holders and their neighbours, so
an item with no Geni link may never have entered it. **Absence from the store is a
limit on what we can see, never a statement about Wikidata.**

Offline. `CLAUDE.md`: never query Wikidata to check something.

Writes `reports/izumo-unlinked-classified.tsv`.
"""
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'out' / 'wikidata' / 'store-index.sqlite3'
SHARDS = ROOT / 'wikidata' / 'items'

HUMAN = 'Q5'
#: `P31` classes that still mean "a person", so that a bare `is it Q5?` does not
#: report the founders of this very genealogy as non-people. Wikidata models the
#: legendary emperors as `Q124710051` *legendary human figure* rather than `Q5`,
#: which is a statement about the evidence for them, not about their kind. Labels
#: from `reports/wikidata-labels.tsv`; never guessed.
PERSONISH = {
    'Q5': 'human',
    'Q124710051': 'legendary human figure',
}
#: Divine, and so genuinely a different kind of thing from an office-holder.
DIVINE = {
    'Q511056': 'solar deity',
    'Q178885': 'deity',
}


def shard_of(conn, qids):
    """qid -> shard number, for the ones the store holds."""
    out = {}
    cur = conn.cursor()
    for i in range(0, len(qids), 500):
        chunk = qids[i:i + 500]
        marks = ','.join('?' * len(chunk))
        for qid, shard in cur.execute(
                f'select qid, shard from items where qid in ({marks})', chunk):
            out[qid] = shard
    return out


def instances_of(by_shard):
    """qid -> (list of P31 values, label). One pass per shard, never per item."""
    found = {}
    for shard, wanted in sorted(by_shard.items()):
        path = SHARDS / f'items-{shard:05d}.jsonl.gz'
        if not path.exists():
            continue
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                qid = item.get('id')
                if qid not in wanted:
                    continue
                claims = (item.get('claims') or {}).get('P31') or []
                vals = []
                for c in claims:
                    v = (((c.get('mainsnak') or {}).get('datavalue') or {})
                         .get('value') or {})
                    if isinstance(v, dict) and v.get('id'):
                        vals.append(v['id'])
                label = ((item.get('labels') or {}).get('en')
                         or (item.get('labels') or {}).get('mul') or {})
                found[qid] = (vals, label.get('value', '') if isinstance(label, dict) else '')
    return found


def main():
    rows = list(csv.DictReader(
        open(ROOT / 'reports' / 'izumo-unlinked.tsv', encoding='utf-8'), delimiter='\t'))
    qids = [r['qid'] for r in rows if r['qid']]
    print(f'{len(rows)} unlinked roster items, {len(qids)} with a QID')

    if not INDEX.exists():
        raise SystemExit(f'no local store index at {INDEX}; nothing to classify offline')

    conn = sqlite3.connect(INDEX)
    placed = shard_of(conn, qids)
    print(f'{len(placed)} of them are in the local store, {len(qids) - len(placed)} are not')

    by_shard = {}
    for qid, shard in placed.items():
        by_shard.setdefault(shard, set()).add(qid)
    facts = instances_of(by_shard)

    out_rows, counts = [], {}
    for r in rows:
        qid = r['qid']
        if qid not in facts:
            verdict, p31, label = 'not in the local store', '', ''
        else:
            p31s, label = facts[qid]
            p31 = ';'.join(p31s)
            personish = [PERSONISH[v] for v in p31s if v in PERSONISH]
            divine = [DIVINE[v] for v in p31s if v in DIVINE]
            if personish:
                verdict = personish[0]
            elif divine:
                verdict = divine[0]
            elif p31s:
                verdict = 'other kind of thing'
            else:
                verdict = 'no P31 recorded' 
        counts[verdict] = counts.get(verdict, 0) + 1
        out_rows.append((qid, r.get('lineage', ''), r.get('name', ''),
                         verdict, p31, label))

    print()
    for v, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f'  {v:<24} {n}')

    odd = [r for r in out_rows
           if r[3] not in PERSONISH.values() and r[3] != 'not in the local store']
    if odd:
        print()
        print(f'the {len(odd)} the store says are not office-holders:')
        for qid, _lin, name, verdict, p31, label in odd:
            print(f'  {qid:<12} {name:<34} {verdict:<24} P31={p31}')

    # The unclassified 54 are the honest limit of this. They have no Geni link, so
    # they were never seeded into a store built from P2600 holders and their
    # neighbours -- their absence here is circular, not evidence. Some are plainly
    # not people from the roster name alone (`Amabe clan`, `Kamo district`,
    # `Aogaki Publishing`, and a row called `2020`), and that is a NAME reading,
    # flagged as such rather than acted on.
    missing = [r for r in out_rows if r[3] == 'not in the local store']
    print()
    print(f'{len(missing)} not in the local store, so unclassified here. '
          f'The store is a Geni-shaped slice; these have no Geni link, so their '
          f'absence from it is circular.')

    out = ROOT / 'reports' / 'izumo-unlinked-classified.tsv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['qid', 'lineage', 'roster_name', 'verdict', 'p31', 'wikidata_label'])
        w.writerows(out_rows)
    print(f'\nwrote {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
