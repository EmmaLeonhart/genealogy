"""The office-holders Geni carries past the end of the Shinto-wiki chart.

    python scripts/build-izumo-beyond-chart.py

The chart stops at Senge 76 and Kitajima 68. Geni goes further: Kitajima 69-74 and
Senge 77-81, eleven men `reports/izumo-roster.tsv` has no row for. Emma, 2026-08-23,
asked whether to create Wikidata items for them: *"Yes lol that's the point of why I
made it? They are part of the geni individual creation pipeline."*

**Ten of the eleven already have items, and she linked them herself.** Their About Me
carries a `wikidata.org` URL, so they are already in `reports/geni-qid-links.tsv` and
already in the 354-statement `P2600` batch. Nothing to create.

**One is genuinely missing: `Takanori 81 /Senge/`, `6000000227331629828`.** No About
Me link, no Wikidata item. This script emits the single `create_individual` object
for him, in the shape `reports/wikidata-samaritan-priests.json` already uses.

**His succession is the counter-example to a mistake made the same day.** A deleted
script walked the office up the father chain, decrementing the number one generation
per step. Takanori 81 and Takatomi 80 are *brothers* -- both sons of Takasumi 79 --
so the office passed sideways and every number that walk produced above such a step
would have been wrong. Read from `FAMC`, not assumed.

Writes `reports/wikidata-izumo-beyond-chart.json`.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

GENI = '6000000227331629828'

#: Read off the GEDCOM, not inferred: `1 SEX M`, `1 FAMC @F…591845@` which is the
#: family Takasumi 79 heads and Takatomi 80 is also a child of.
FATHER_QID = 'Q135579518'      # Takasumi 79 Senge
FATHER_GENI = '6000000227331591841'
BROTHER_QID = 'Q11405449'      # Takatomi 80 Senge
BROTHER_GENI = '6000000227331651847'


def ref(geni_id):
    return {'property': 'P2600', 'value': geni_id}


def main():
    obj = {
        'id': f'create_individual:{GENI}',
        'type': 'create_individual',
        'priority': False,
        'subject': {'qid': None, 'geni_id': GENI},
        'requires': [],
        'anchor': None,
        # The regnal number is NOT part of the name -- Emma flagged that when the
        # roster was built, and the roster keeps it in its own column. It goes on
        # the given name as P7338 regnal ordinal, per CLAUDE.md, not into the label.
        # The label form follows the roster's for this lineage; worth her glance.
        'labels': {'en': 'Senge no Takanori', 'mul': 'Senge no Takanori'},
        'descriptions': {},
        'statements': [
            {'property': 'P31', 'value': 'Q5', 'references': [ref(GENI)]},
            {'property': 'P2600', 'value': GENI, 'references': []},
            {'property': 'P21', 'value': 'Q6581097', 'references': [ref(GENI)]},
        ],
        'links': [
            {'property': 'P22', 'value': FATHER_QID,
             'references': [ref(GENI), ref(FATHER_GENI)]},
            {'property': 'P3373', 'value': BROTHER_QID,
             'references': [ref(GENI), ref(BROTHER_GENI)]},
        ],
        'notes': [
            'Only one of the eleven office-holders past the end of the Shinto-wiki '
            'chart lacks a Wikidata item; the other ten already carry one in their '
            'Geni About Me and are in reports/wikidata-geni-qid-p2600.qs.',
            'No dates: the GEDCOM record carries no BIRT or DEAT.',
            'Label form is a guess following the roster style for this lineage. The '
            'regnal ordinal 81 belongs on the given name as P7338, not in the label.',
        ],
    }

    out = ROOT / 'reports' / 'wikidata-izumo-beyond-chart.json'
    out.write_text(json.dumps([obj], indent=2, ensure_ascii=False) + '\n',
                   encoding='utf-8')
    print(f'wrote {out.relative_to(ROOT)} -- 1 create_individual')
    print('the other ten already have items and are in the P2600 batch')


if __name__ == '__main__':
    main()
