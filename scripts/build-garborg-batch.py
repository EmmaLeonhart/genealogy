"""QuickStatements for the Garborg family, built to the model Emma actually uses.

**The previous version of this file was dangerous and is replaced.** It was written
on 2026-08-22, when nobody around Arne Garborg (`Q467497`) had an item. Emma has
since created four of them by hand, so that batch's opening `CREATE` for Eivind and
Ane Oline would have minted **duplicate items** for people who already exist. It
also cited every statement with `P854` *reference URL* + `P813` *retrieved*, which
is not what she does.

`docs/wikidata-item-template.md` is the model, read off her own items:

* **The reference is `P2600` itself** -- `S2600 "<geni id>"`, not a URL.
* **Only some statements carry it.** Referenced: `P569`, `P570`, `P22`, `P25`,
  `P26`, `P40`. Unreferenced: `P31`, `P21`, `P2600`, `P734`, `P735`, `P5056`.
* **No descriptions at all.** All five of her items are description-empty.
* **`P3373` *sibling* is used**, both ways. The old batch argued against it.
* Labels are `en` and `mul`, the same string.

**The parents now exist, which changes the shape.** The old batch had to defer every
link to a commented second pass, because QuickStatements V1 cannot point at a QID a
`CREATE` in the same run has just minted. `Q141152512` and `Q141152523` are real
QIDs today, so each new sibling gets `P22`, `P25` and `P3373` immediately. What still
needs a second pass is only what points *at* the new items: the parents' `P40` and
the existing siblings' reciprocal `P3373`.

**What is deliberately not emitted: name properties.** Eivind carries `P735`, `P734`
and a `P5056` patronym item she created. Doing the same for the others needs the QID
of each given-name item and a new patronymic item per patronym, and guessing a
name-item QID is exactly the error this repo keeps paying for. Listed in the trailer
for her instead.

Offline: reads `reports/derived-facts.csv` and `reports/derived-labels.csv`. Emits
`reports/wikidata-garborg.qs`. Nothing here runs an edit.
"""
import csv
import sys
from pathlib import Path

csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

#: Already on Wikidata. Geni id -> QID. Never `CREATE` these.
EXISTING = {
    '6000000003492005116': 'Q467497',      # Aadne (Arne) Eivindson Garborg
    '6000000003492005111': 'Q141152512',   # Eivind Aadnesson Garborg, father
    '6000000003491986946': 'Q141152523',   # Ane Oline Jonsdatter Raugstad, mother
    '6000000003492005121': 'Q141152600',   # Stena Eivindsdatter Garborg
    '6000000003492005126': 'Q141152614',   # Jon Eivindson Garborg
}
FATHER, MOTHER = '6000000003492005111', '6000000003491986946'

#: Of the five existing items, only these three still lack P569/P570.
#: `docs/wikidata-item-template.md`: Eivind is "full: dates, names, spouse, 3
#: children" and Arne carries ~120 properties. Emitting dates for those two would
#: add a duplicate statement with a different reference, and on Arne it could put a
#: second birth date on a well-sourced item -- noise at best.
NEED_DATES = ['6000000003491986946', '6000000003492005121', '6000000003492005126']

#: The six siblings with no item yet, in birth order.
TO_CREATE = [
    '6000000003492005131',   # Samuel Eivindsen Garborg
    '6000000003492005136',   # Even Eivindson Garborg
    '6000000003492005141',   # Inger Marie "Mary" Eivindsdatter Garborg
    '6000000003492005146',   # Abel Eivindsen Garborg
    '6000000003492005151',   # Ole Eivindsen Garborg
    '6000000003492005156',   # Ane Oline "Lena" Eivindsdatter Garborg
]

SEX = {'M': 'Q6581097', 'F': 'Q6581072'}    # male / female
HUMAN = 'Q5'


def qs_string(text):
    """QuickStatements V1 has no escape for a double quote inside a string.

    Geni writes a nickname in quotes -- `Stine "Stena" Eivindsdatter Garborg` --
    which would end the string early and shift every field after it. The quote
    characters go, the nickname stays, so no name token is lost.
    """
    return (text or '').replace('"', '').strip()


def load(path, keys):
    out = {}
    for row in csv.DictReader(open(ROOT / path, encoding='utf-8')):
        if row['geni_id'] in keys:
            out[row['geni_id']] = row
    return out


def time_value(iso, precision):
    return f'{iso}/{precision}' if iso and precision else None


def main():
    keys = set(TO_CREATE) | set(EXISTING)
    facts = load('reports/derived-facts.csv', keys)
    labels = load('reports/derived-labels.csv', keys)

    def ref(geni_id):
        """Her reference form: the Geni ID as a reference snak."""
        return f'\tS2600\t"{geni_id}"'

    lines, notes = [], []

    # ---- 1. dates the four existing items still lack -------------------------
    lines.append('# Dates for the three existing items that lack them. No CREATE here')
    lines.append('# -- these items exist, and a CREATE would mint duplicates. Eivind and')
    lines.append('# Arne are skipped: both already carry P569/P570.')
    for geni_id in NEED_DATES:
        qid = EXISTING[geni_id]
        f = facts.get(geni_id)
        if not f:
            notes.append(f'no derived facts for {geni_id} ({qid})')
            continue
        for prop, iso, prec in (('P569', f['birth_date_iso'], f['birth_date_precision']),
                                ('P570', f['death_date_iso'], f['death_date_precision'])):
            v = time_value(iso, prec)
            if v:
                lines.append(f'{qid}\t{prop}\t{v}{ref(geni_id)}')
    lines.append('')

    # ---- 2. the sibling links among the items that already exist -------------
    # P3373 runs both ways; she does this, and the old batch argued against it.
    lines.append('# Sibling links among the existing items. P3373 both ways.')
    existing_children = ['Q467497', 'Q141152600', 'Q141152614']
    child_geni = {'Q467497': '6000000003492005116',
                  'Q141152600': '6000000003492005121',
                  'Q141152614': '6000000003492005126'}
    for a in existing_children:
        for b in existing_children:
            if a != b:
                lines.append(f'{a}\tP3373\t{b}{ref(child_geni[a])}')
    lines.append('')

    # ---- 3. the six siblings with no item ------------------------------------
    lines.append('# The six siblings with no Wikidata item. Parents already exist,')
    lines.append('# so P22/P25/P3373 go on in the same pass.')
    for geni_id in TO_CREATE:
        f, l = facts.get(geni_id), labels.get(geni_id)
        if not f or not l:
            notes.append(f'skipped {geni_id}: no derived facts or labels')
            continue
        name = qs_string(l['label_en'] or l['label_mul'])
        lines.append('CREATE')
        lines.append(f'LAST\tLen\t"{name}"')
        lines.append(f'LAST\tLmul\t"{name}"')
        lines.append(f'LAST\tP31\t{HUMAN}')
        lines.append(f'LAST\tP21\t{SEX[f["sex"]]}') if f['sex'] in SEX else None
        lines.append(f'LAST\tP2600\t"{geni_id}"')
        b = time_value(f['birth_date_iso'], f['birth_date_precision'])
        if b:
            lines.append(f'LAST\tP569\t{b}{ref(geni_id)}')
        d = time_value(f['death_date_iso'], f['death_date_precision'])
        if d:
            lines.append(f'LAST\tP570\t{d}{ref(geni_id)}')
        lines.append(f'LAST\tP22\t{EXISTING[FATHER]}{ref(geni_id)}')
        lines.append(f'LAST\tP25\t{EXISTING[MOTHER]}{ref(geni_id)}')
        for sib in existing_children:
            lines.append(f'LAST\tP3373\t{sib}{ref(geni_id)}')
        lines.append('')

    # ---- 4. what can only be done once the six have QIDs ---------------------
    lines.append('# --- second pass: needs the QIDs the CREATEs above return ---')
    lines.append('# QuickStatements V1 cannot point at an item minted in the same run,')
    lines.append('# so these are the statements that point AT the six new siblings.')
    lines.append('# Substitute each minted QID for <name> and drop the leading #.')
    lines.append('#')
    for geni_id in TO_CREATE:
        n = qs_string((labels.get(geni_id) or {}).get('label_en', geni_id))
        lines.append(f'# {EXISTING[FATHER]}\tP40\t<{n}>{ref(FATHER)}')
        lines.append(f'# {EXISTING[MOTHER]}\tP40\t<{n}>{ref(MOTHER)}')
        for sib in existing_children:
            lines.append(f'# {sib}\tP3373\t<{n}>{ref(child_geni[sib])}')
        lines.append('#')
    lines.append('# And P3373 among the six themselves, once all six have QIDs.')
    lines.append('#')
    lines.append('# NAME PROPERTIES ARE NOT EMITTED. Eivind carries P735 given name,')
    lines.append('# P734 family name and P5056 patronym (Q141152710 Aadnesson, which')
    lines.append('# Emma created). Doing the same here needs the QID of each given-name')
    lines.append('# item and a new patronymic item per patronym -- Jonsdatter,')
    lines.append('# Eivindsdatter, Eivindsen, Eivindson. Guessing a name-item QID is the')
    lines.append('# error this repo keeps paying for, so they are listed, not emitted.')

    out = ROOT / 'reports' / 'wikidata-garborg.qs'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    live = [x for x in lines if x and not x.startswith('#') and x != 'CREATE']
    print(f'wrote {out.relative_to(ROOT)}: '
          f'{lines.count("CREATE")} creations, {len(live)} statements')
    for n in notes:
        print(' ', n)


if __name__ == '__main__':
    main()
