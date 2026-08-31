# Blocked creations — is our Geni person the same as this Wikidata item?

**Emma, 2026-08-31:** *"just ask if geni == wikidata for all the blocked creations from the current network. You should be adding the geni id and treating as an existing network member if I approve."*

Each row is a creation the duplicate guard is holding. The **candidate** is a Wikidata item that
our person's parent already names as a child, which is why the guard will not create a possible
second copy. A candidate that already carries its own `P2600` is a **different** person and is
shown struck through — those are not the question.

| # | our Geni person | b/d (ours) | candidate | candidate label | b/d | already has P2600? |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Hedvig Catharina Charlotta De la Gardie `6000000001515228463` |  /  | `Q2066886` | Hedvig Catharina von Fersen | +1732-01-01 / +1800-01-01 | no |
| 2 | Anna Sofia Bäck `6000000024161876529` |  /  | `Q66316940` | Anna Sophia Ihre | +1762-00-00 /  | no |
| 3 | Sven Torsteinson Lima `6000000002836313613` |  /  | `Q141225714` | Ingeborg Simonsdatter Ytre Lima | +1677-00-00 / +1738-00-00 | **6000000002836363103** |
| 4 | Eva Helena Adelswärd `6000000006127732211` |  /  | `Q109829800` | Eva Helena von Fersen | +1759-01-01 / +1807-01-01 | no |
| 5 | Anna Tersera `6000000007311831371` |  /  | `Q110231041` | Anna Terserus | +1653-07-17 / +1723-04-24 | no |
| 6 | Ulrika Catharina Koskull `6000000006127576609` |  /  | `Q109296043` | Ulrika Catharina Koskull | +1759-05-19 / +1805-01-25 | no |
| 7 | Margareta Jacobsdotter Jernstedt `6000000007755407668` |  /  | `Q108615809` | Margareta Jernstedt | +1640-00-00 / +1680-00-00 | no |
| 8 | Emma Andersson `6000000178279770847` |  /  | `Q141225694` | Carl Andersson |  /  | **6000000178279141871** |
| 9 | Margareta Gyllenstierna af Fogelvik `6000000011637291315` |  /  | `Q4951688` | Margareta Gyllenstierna | +1680-01-01 / +1740-01-01 | no |
| 10 | Magdalena Christina Appelbom `6000000008889872098` |  /  | `Q109835400` | Magdalena Christina Appelbom | +1698-05-16 / +1777-04-01 | no |
| 11 | Catharina Funck `6000000009401513008` |  /  | `Q110547956` | Catharina Funck | +1723-00-00 / +1801-04-11 | no |
| 12 | Anna Christina Bruncrona `6000000017425559123` |  /  | `Q66711908` | Anna Kristina Bruncrona | +1739-00-00 / +1827-00-00 | no |
| 13 | Charlotta Eleonora Hedvig von Krassow `6000000007948266424` |  /  | `Q110395711` | Charlotta Eleonora Hedvig von Krassow | +1779-02-07 / +1855-11-24 | no |
| 14 | Margareta Frodbom `6000000011533226330` |  /  | `Q111989591` | Margareta Fordbohm |  /  | no |
| 15 | Maria Sofia Stierncrona `6000000013296788468` |  /  | `Q113007770` | Maria Sofia Stierncrona | +1716-11-26 / +1749-01-02 | no |

**How to answer:** for each row, same person or not. A `yes` means we add `P2600` to that item and treat it as an existing network member — no creation, and it becomes an anchor everything else can link to.

