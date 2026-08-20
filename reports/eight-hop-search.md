# Every relative within eight hops, searched

**Emma's item, 2026-08-18:** *"look at all my relatives that are within eight hops of me.
Do some level of web searching for them… or probably wikidata searching."*

Offline graph, then the Wikidata search API. No writes, no exports.

## The set

| | |
| --- | ---: |
| people within 8 hops | **1,015** |
| with a usable name | 1,010 |
| …and a birth year — the searchable set | **852** |
| carrying a QID via the `P2600` map | **0** |
| plausibly living (born ≥ 1930, no death year) | **54** |

## What the search found

852 names went to `wbsearchentities`, giving 349 distinct items. Name alone is worthless
here — Karl Johan Johansson matches half of Sweden — so every hit was checked against
**birth year**, and 8 survived within ±2 years. Seven of those are coincidences of common
Scandinavian names. **One is real.**

### Jonas Salte — 8 hops — `Q138696805`

| | our record | Wikidata |
| --- | --- | --- |
| born | **1 JUN 1920** | **1920-06-01** |
| died | **7 MAY 1944** | **1944-05-07** |

**Both dates match to the day.** Norwegian (`P27` Norway), occupation *gårdsarbeider*
(farm worker), description *"killed during WWII"*. No sitelinks, no `P2600`.

    Emma Leonhart ← Richard Wade Borsheim ← Randolph Paulus Borsheim
      ← Reinhert Borsheim ← Rasmus (Paulson) Borsheim
      ← Berta Serina Rasmusdatter Kolnes ← Berta Maria Paulsdatter Borsheim
      ← Inga Lauritsdatter Erga ← Jonas Salte

**This is nearer than the previous best.** `nearest-wikidata.md` reported Racin Hansen
Kolnes at 9 hops, because the map only sees items carrying a Geni ID. **An item without
`P2600` is invisible to it**, and that is what this search is for: 8 beats 9.

### The seven that are not

`Gabriel Gabrielsson` b.1795 against *Gabriel Borg* b.1797 — different surname.
`Hans Gundersen` b.1851 against *Hans Jørgen Gundersen* b.1850 — different man.
`Robert Henry` b.1934 against an American painter b.1933, and against *Bobby Timmons*.
`Karl Johan Karlsson`, `Carl Johan Johansson`, `Karl Johan Johansson` — three of the
commonest names in Sweden, each with a near-miss year. **Recorded so nobody re-runs the
search and re-finds them as new.**

## What this does not answer

**Nobody in the 1,015 has a publication record yet, because that is a different search.**
The Wikidata pass answers *"does an item already exist"*. Emma's goal is someone she can
*make* notable, and for that the target is the **54 living people**, none of whom Wikidata
knows:

    1 hop   Richard Wade Borsheim 1963
    2       Jared Borsheim 1998
    3       Stephen Borsheim 1949 · Heidi Joan Borsheim 1969
    4       Ilene (Eileen) Hoknes 1931 · Barney Borsheim 1936 · Floyd Olaf Hoknes 1938
    5       Milton Francis Schwan 1951 · Heather Heppner 1953
    6       Henry Stangeland 1932 · Elizabeth Ashley Schwan 1984 ·
            Cory Francis Schwan 1986 · Amy Jean Schwan 1989
    7       nine Stangelands, Darlene Mae Yausie, three Holbirds, Olivia Schwan
    8       twenty-five, mostly Norwegian: Håland, Gjesdal, Lillebø, Lunde, Reime,
            Undheim, Grøtteland, Hogstad, plus Yausie and Buchanan in North America

**Jonas Salte does not help that goal** — he died in 1944 and his item exists already.
He improves the *measurement*, not the objective.
