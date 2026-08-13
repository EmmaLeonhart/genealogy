# Edit objects

Emma's specification, 2026-08-12. **We emit JSON objects describing edits.** A
later pipeline executes them; roughly a hundred a day. Nothing here sends
anything.

## The four kinds

| type | what it does |
| --- | --- |
| `add_geni_id` | put `P2600` on an existing Wikidata item |
| `create_individual` | create a person with their names and link them to parents or children **already on Wikidata** |
| `link_siblings` | connect two people **both already on Wikidata** with `P3373` |
| `add_statement` | add one property to an individual |

## Not every object is valid to run when it is written

This is the part that makes them objects rather than a batch. **Emma: *"not all
of the JSONs are valid to run initially. This is a bit of an important thing."***

The dependency that drives it: **we cite claims to the person's Geni ID, so the
Geni ID has to be on the item first.** An `add_statement` carrying a Geni
reference is invalid until the matching `add_geni_id` has run. Every object
therefore carries `requires`, naming what must already be true.

## Citations

**The Geni profile ID is a reference, never a qualifier.** *"In the references
thing, as a reference, not a qualifier … we have the Geni external identifier."*

| edit | cited to Geni? |
| --- | --- |
| a fact Geni supports — dates, places, addresses, relationships | **yes** |
| a **bidirectional** relationship | **yes, both parties' Geni IDs**, on either side |
| everything on a created individual | **yes** — all of it comes from Geni |
| a **label** | **no — labels cannot carry a citation** |
| a sibling link where neither party has a Geni ID | **no** — nothing to cite |

*"For a person's bidirectional relationships, we cite the Geni IDs of both
parties of the relationship on either side."*

## What runs without a Geni ID

Most edits require the subject to have a Geni ID. Two do not:

- **Labels.** Added regardless.
- **Sibling links where neither party has a Geni ID.** This is a **Wikidata
  fix**, not an import: Wikidata's `P3373` is symmetric and frequently only
  stated on one side. *"Our thing kind of systematically goes through and would
  be fixing instances of the symmetrical relationships not being present."*
  Uncited, because Geni is not the source.

If **one** party has a Geni ID, fixing the symmetry still carries no citation —
the missing direction is Wikidata's own claim, not ours.

## Geni is not the source of labels

*"Geni just doesn't label people… Geni is not the source of labels, except in
items that actually lack an English-language label on Wikidata, or possibly some
other things, or in situations where we're creating the individual from
scratch."*

So a label is emitted only when:

1. the item **has no English label at all**, or
2. we are **creating the individual**, or
3. it is a language the item lacks and we have a name in that script.

Never to overwrite a label Wikidata already has. And *"they can't actually have a
citation put on them."*

## The shape

```json
{
  "id": "add_geni_id:Q16164886",
  "type": "add_geni_id",
  "subject": {"qid": "Q16164886", "geni_id": "6000000038740385839"},
  "requires": [],
  "statement": {"property": "P2600", "value": "6000000038740385839"}
}
```

```json
{
  "id": "add_statement:Q16164886:P569",
  "type": "add_statement",
  "subject": {"qid": "Q16164886", "geni_id": "6000000038740385839"},
  "requires": ["add_geni_id:Q16164886"],
  "statement": {
    "property": "P569",
    "value": {"time": "+1894-04-25T00:00:00Z", "precision": 11},
    "qualifiers": [],
    "references": [{"property": "P2600", "value": "6000000038740385839"}]
  }
}
```

```json
{
  "id": "link_siblings:Q1:Q2",
  "type": "link_siblings",
  "subjects": [{"qid": "Q1", "geni_id": null}, {"qid": "Q2", "geni_id": null}],
  "requires": [],
  "wikidata_fix": true,
  "statements": [
    {"qid": "Q1", "property": "P3373", "value": "Q2", "references": []},
    {"qid": "Q2", "property": "P3373", "value": "Q1", "references": []}
  ]
}
```

```json
{
  "id": "create_individual:6000000038740385839",
  "type": "create_individual",
  "subject": {"qid": null, "geni_id": "6000000038740385839"},
  "requires": ["Q…", "…"],
  "labels": {"en": "Arne Olson Anda", "mul": "Arne Olson Anda"},
  "aliases": {},
  "statements": [
    {"property": "P31", "value": "Q5", "references": [...]},
    {"property": "P2600", "value": "6000000038740385839", "references": []},
    {"property": "P21", "value": "Q6581097", "references": [...]}
  ],
  "links": [{"property": "P22", "value": "Q…", "references": [...]}]
}
```

`requires` on a creation names the QIDs of the parents or children it links to —
they must exist before the link can be made.

## Fields

| field | meaning |
| --- | --- |
| `id` | stable, so an object can be referenced by another's `requires` |
| `type` | one of the four |
| `subject` / `subjects` | `qid` may be `null` for a creation; `geni_id` may be `null` for a Wikidata fix |
| `requires` | ids of objects that must run first, or QIDs that must exist |
| `wikidata_fix` | true when the edit is not sourced from Geni at all |
| `references` | always the Geni profile ID, as a reference; empty where a citation is not permitted |

## Status

The emitter is `scripts/build-edit-objects.py` → `out/wikidata/edits.json`.
**Executing them is not built and is not being built yet.**
