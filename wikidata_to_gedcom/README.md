# wikidata_to_gedcom

> Started with [cleanvibe](https://github.com/EmmaLeonhart/cleanvibe) on 2026-10-03.

Exports a person's ancestors from Wikidata as GEDCOM files, one per language.
It follows father (P22) and mother (P25) links up a set number of generations.

- **Names:** each person's label in the requested language, falling back to the
  `mul` label and then the bare QID. The label is written as a given name with
  no surname.
- **Notes:** each person's NOTE is a link to their Wikidata page.
- **Sex:** taken from P21. Families come from father/mother pairs.
- Each file is opened with the system's default program as soon as it is
  written.

## Usage

```
python wikidata_to_gedcom.py Q140568870
python wikidata_to_gedcom.py Q140568870 --generations 30 --langs ja,ko --suffix -5
```

| Option | Default | Meaning |
|---|---|---|
| `--generations` | 15 | how many generations up from the person |
| `--langs` | `en,zh,ja,ko` | one GEDCOM per language |
| `--out` | `output` | output folder |
| `--suffix` | (none) | appended to file names, e.g. `-2`, so earlier exports are kept |
| `--no-open` | off | don't open the files after writing |

Output goes to `output/<QID>_ancestors_<lang><suffix>.ged`. For each file the
script prints how many people it holds and how many are named only by their QID
(no label in that language and no `mul` label). The script uses only
the Python standard library.

## Working on it

Run `cleanvibe` in this folder (or double-click `!runClaude.bat` on Windows) to
open a new Claude session here. It starts with Remote Control on, so you can
continue from the Claude app or web. Earlier sessions are in `sessions/`.
