"""QuickStatements for the first iteration around Arne Garborg (Q467497).

Q467497 carries ~120 properties and *no parents*: no P22 father, no P25 mother.
His father, his mother and his nine siblings have no Wikidata item at all -- only
3 of the 277 people within three hops of him are on Wikidata. So the first
iteration is create-then-link, in CLAUDE.md's order: the Geni ID goes on first,
then everything Geni supports, each statement cited to that Geni ID.

Emits reports/wikidata-garborg.qs. Offline: reads reports/derived-facts.csv,
reports/derived-labels.csv and out/wikidata/p2600-all.tsv. Nothing here talks to
Wikidata, and nothing here runs an edit -- the file is for Emma to run.
"""
import csv, sys
csv.field_size_limit(1 << 30)

ARNE = '6000000003492005116'
ARNE_QID = 'Q467497'
FATHER = '6000000003492005111'
MOTHER = '6000000003491986946'
SIBLINGS = [
    '6000000003492005121', '6000000003492005126', '6000000003492005131',
    '6000000003492005136', '6000000003492005141', '6000000003492005146',
    '6000000003492005151', '6000000003492005156',
]
CREATE = [FATHER, MOTHER] + SIBLINGS

SEX = {'M': 'Q6581097', 'F': 'Q6581072'}          # male / female
HUMAN = 'Q5'
RETRIEVED = '+2026-08-22T00:00:00Z/11'

def geni_url(g):
    return f'https://www.geni.com/people/x/{g}'

def qs_string(text):
    """QuickStatements V1 has no escape for a double quote inside a string.

    Nine of these labels carry a Geni nickname in quotes -- `Stine "Stena"
    Eivindsdatter Garborg` -- which would end the string early and corrupt the
    rest of the line. The quote characters are dropped and the nickname kept,
    so no name token is lost.
    """
    return text.replace('"', '').strip()

def load(path, keys):
    out = {}
    for row in csv.DictReader(open(path, encoding='utf-8')):
        if row['geni_id'] in keys:
            out[row['geni_id']] = row
    return out

def time_value(iso, precision):
    """GEDCOM-derived ISO plus a Wikidata precision digit (11 day, 9 year)."""
    return f'{iso}/{precision}' if iso and precision else None

def main():
    keys = set(CREATE) | {ARNE}
    facts = load('reports/derived-facts.csv', keys)
    labels = load('reports/derived-labels.csv', keys)

    lines, notes = [], []

    def ref(g):
        # every statement is cited to the Geni profile it came from
        return f'\tS854\t"{geni_url(g)}"\tS813\t{RETRIEVED}'

    for g in CREATE:
        f, l = facts.get(g), labels.get(g)
        if not f or not l:
            notes.append(f'skipped {g}: no derived facts or labels')
            continue
        name = qs_string(l['label_en'] or l['label_mul'])
        lines.append('CREATE')
        lines.append(f'LAST\tLen\t"{name}"')
        lines.append(f'LAST	Lmul	"{qs_string(l["label_mul"]) or name}"')
        lines.append(f'LAST\tP31\t{HUMAN}{ref(g)}')
        lines.append(f'LAST\tP2600\t"{g}"{ref(g)}')
        if f['sex'] in SEX:
            lines.append(f'LAST\tP21\t{SEX[f["sex"]]}{ref(g)}')
        b = time_value(f['birth_date_iso'], f['birth_date_precision'])
        if b:
            lines.append(f'LAST\tP569\t{b}{ref(g)}')
        d = time_value(f['death_date_iso'], f['death_date_precision'])
        if d:
            lines.append(f'LAST\tP570\t{d}{ref(g)}')
        lines.append('')

    # The links. QuickStatements cannot point a statement at a QID that an
    # earlier CREATE in the same batch has just minted, so every link is a
    # second pass Emma runs once the creations return their QIDs.
    #
    # Siblinghood is NOT emitted as P3373. Both parents are being created here,
    # so giving each of the ten children P22 and P25 states the same fact once
    # and lets Wikidata derive the rest; an explicit P3373 on top would be
    # redundant and would have to be maintained in n^2 pairs.
    lines.append('# --- second pass: run once the CREATEs above return QIDs ---')
    lines.append('# Substitute the minted QID for each <...> and drop the leading #.')
    lines.append('#')
    lines.append(f'# {ARNE_QID}	P22	<Eivind Aadnesson Garborg>{ref(ARNE)}')
    lines.append(f'# {ARNE_QID}	P25	<Ane Oline Jonsdatter Raugstad>{ref(ARNE)}')
    lines.append('#')
    for s_id in SIBLINGS:
        n = qs_string((labels.get(s_id) or {}).get('label_en', s_id))
        lines.append(f'# <{n}>	P22	<Eivind Aadnesson Garborg>{ref(s_id)}')
        lines.append(f'# <{n}>	P25	<Ane Oline Jonsdatter Raugstad>{ref(s_id)}')
    lines.append('#')
    lines.append(f'# <Eivind Aadnesson Garborg>	P26	<Ane Oline Jonsdatter Raugstad>{ref(FATHER)}')
    lines.append(f'# <Ane Oline Jonsdatter Raugstad>	P26	<Eivind Aadnesson Garborg>{ref(MOTHER)}')

    out = 'reports/wikidata-garborg.qs'
    with open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    print(f'wrote {out}: {len([x for x in lines if x == "CREATE"])} creations, '
          f'{len([x for x in lines if x and not x.startswith("#") and x != "CREATE"])} statements')
    for n in notes:
        print(' ', n)

if __name__ == '__main__':
    main()
