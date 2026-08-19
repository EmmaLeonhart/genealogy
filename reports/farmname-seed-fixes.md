# Placeholder seeds that need a surname, not `father of X`

Emma, 2026-08-18: *"uhh farm names are surnames here lol"* --- and *"add a task in the queue to fix the surnames of these people before the synoptic tree is built. I will do the editing on geni for this."*

**She does the Geni edits.** This file is the worklist, not an instruction to touch anything.

**11 placeholders** carry `father of <child>` where the child has a real surname the father should have taken. A further **36** were checked and left alone because the child's surname *is* their patronymic (`Barbro /Endresdatter/`, `Sigrid /Larsdotter/`), where tier 2 was correct --- tier 1 is explicit that the patronymic must not survive into the father's surname.

| Geni ID | placeholder now | should be | child |
| --- | --- | --- | --- |
| [6000000227313059848](https://www.geni.com/people/x/6000000227313059848) | `Elias /father of Maja Stina/` | `Elias /Nyberg/` | Maja Stina Eliasdotter /Nyberg/ |
| [6000000008807359308](https://www.geni.com/people/x/6000000008807359308) | `Gunnar /father of Guri/` | `Gunnar /Thu/` | Guri Gunnarsdatter /Thu/ |
| [6000000227290969847](https://www.geni.com/people/x/6000000227290969847) | `Karl /father of Carl/` | `Karl /Karl Kristian/` | Carl C / Karl Kristian /Carlsen / Karlsen/ |
| [6000000173283214584](https://www.geni.com/people/x/6000000173283214584) | `Kawkabi Egachi /mother of Toqanchuk Khanum/` | `Kawkabi Egachi /of the Oirats/` | Toghanchuk Khatun /of the Oirats/ |
| [6000000227315747834](https://www.geni.com/people/x/6000000227315747834) | `Lars /father of Ole/` | `Lars /Tjaland/` | Ole LarsenLauritsen /Tjaland/ * |
| [6000000227289886830](https://www.geni.com/people/x/6000000227289886830) | `Lewis /father of Hugh/` | `Lewis /ap Lewis/` | Hugh /ap Lewis/ |
| [6000000227312306880](https://www.geni.com/people/x/6000000227312306880) | `Ole /father of Ingeborg/` | `Ole /Gilja/` | Ingeborg Olsdotter /Gilja/ |
| [6000000047655332033](https://www.geni.com/people/x/6000000047655332033) | `Oljei Khatun /mother of Ghiasoddin/` | `Oljei Khatun /Timurid/` | Ghias ud-Din Muhamedas Džahangiras /Timurid/ |
| [6000000227295719853](https://www.geni.com/people/x/6000000227295719853) | `Wojsław /father of Sulisława/` | `Wojsław /nn/` | Sulisława /nn/ |
| [6000000227289508960](https://www.geni.com/people/x/6000000227289508960) | `Ølver /father of Ingrid/` | `Ølver /Rømer/` | Ingrid Ølversdatter /Rømer/ |
| [6000000227289663852](https://www.geni.com/people/x/6000000227289663852) | `Øystein /father of Berta/` | `Øystein /Riveland/` | Berta Øysteinsdatter /Riveland/ |

## 2026-08-19 — one more placeholder to correct: `Lorent father of Anne Maria Lorentzen`

Created during the chain-seed campaign. The given name should be **`Lorentz`**,
not `Lorent`.

The patronymic stripper matched `zen` as a suffix and removed all three letters.
`Lorentzen` is *Lorentz* + *-en*, so only the `-en` comes off. `zen` has been
dropped from the suffix list, which sends names like this to the tier 4
`NN <surname>` form instead of guessing a given name — safe, and one letter is
not worth a wrong name.

* <https://www.geni.com/people/x/6000000227324100822>

The other placeholders created tonight are all `NN <surname>` or a patronymic
that stripped cleanly (`Anders father of Anders Brodin`, `Jon father of Olof
Jonsson`, `Hans Thon`, `Александр Синайский`) and need no correction.

## 2026-08-19 — `NN Balchen` should be `NN Foss`

Created as the father of **Birgitte Johanne Balchen (Foss)** (1867–). Her birth
surname is **Foss**; Balchen is her husband's. Her father is a Foss.

* <https://www.geni.com/people/x/6000000227324494828>

The dialog heading Geni shows when you click "Add father" is
`Add father of Birgitte Johanne Balchen` — it drops the parenthesised birth
surname that the tree node itself displays. So the automatic surname derivation,
which reads that heading, cannot see it. The tree node is the place to read a
married woman's birth surname from; the dialog heading is not.

This is the same failure the NN Goddard and NN Stevenson entries above were
created to avoid, arriving through a different door.
