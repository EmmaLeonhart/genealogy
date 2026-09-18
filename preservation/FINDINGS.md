# What is in the preservation archive

Queue item 3, 2026-09-17: *"investigate if the pfinzing and reuss connections are there in that"*.

## Yes. Both, as real people, in a file that is not in the Geni corpus

The lead was *"I could have sworn that there was a connection to two Bavarian noble families here
that I can't actually find."* They are in `preservation/genealogy/dropbox/Hethel Pedigree.ged` —
**33,878 people** — which is why they could not be found: the corpus under `exports/` is Geni, and
this tree never came from Geni.

**`Pfinzing von Henfenfeld`, a lineage rather than a stray name** — Siboto, Berthold II,
Berthold III, Markward Merklin, Markward Sigfried, Endres/Andreas, Nicolaus, Elisabeth, Otildis.
34 name lines.

**`Reuss`** — Heinrich XXIV Count of Reuss-Ebersdorf, Augusta Reuss-Ebersdorf, Princess Augusta
Reuss-Köstritz, Charlotte Princess Heinrich XVIII Reuss of Köstritz. 9 name lines.

## And the same file carries the campaign's targets

| name | count | why it matters |
| --- | --- | --- |
| `Pfinzing von Henfenfeld` | 34 | the Bavarian family that could not be found |
| `Reuss` | 9 | the other one |
| `Lusignan` | 32 | the kings of Cyprus |
| `Ibelin` | 8 | the Cyprus hinge already in `exports/tiny-paths/` |
| `Bagration` | 2 | **Princess Leonida Bagration of Mukhrani**, and `Bagrationi` |
| `Flemming` | 1 | the Pomeranian cluster |

`Bagration` is the stated goal — *"that would get us to the Georgian royal family, who is the
goal"* — and it is sitting in the same 33,878-person pedigree as Cyprus and the two Bavarian
families.

## The other files

* `a.ged` — 33,877 people, a different md5 from `Hethel Pedigree.ged` and one person fewer. Two
  versions of one tree, not a duplicate.
* `Theogrammaticus.ged` / `Mannus.ged.doc` — 8,244 people each, different md5s. Carry Pfinzing
  (15) and Reuss (11) and Bagration (2), but **no Lusignan and no Ibelin**.
* `Gaiad.ged` — 62,294 people, the largest single tree in the archive.
* The three MyHeritage *Descent from Antiquity archive* snapshots — 1,550 / 4,033 / 4,093 people,
  late-antique Roman names, and **no Pfinzing and no Reuss at all**.

⛔ **PRESENCE IS NOT CONNECTION, AND NOTHING HERE CLAIMS IT IS.** These are counts of name lines in
a GEDCOM. Whether Pfinzing reaches Bagration *through* this pedigree is a separate question, and
`CLAUDE.md`'s rule for the campaign applies to it: the point is to **add** blood, not to find it in
a graph. What this file establishes is that the material exists and where it lives.

⛔ **THE XREFS HERE ARE NOT GENI IDS.** Nothing in `preservation/` is corpus. It must not be merged
into the synoptic tree on the assumption that its ids join.

## How the people connect into it

`Hethel Pedigree.ged` is **one tree**: 29,559 of its 31,320 people are in a single component,
94.4%, over 15,748 families. Every target family is inside it — Pfinzing 14, Reuss 13, Lusignan
31 of 32, Ibelin 8, Bagration 2, Flemming 1.

### Reuss reaches Bagration in 4 hops, and nothing in the path is invented

    Princess Augusta Reuss-Köstritz
    Duchess Marie of Mecklenburg-Schwerin
    Cyril Vladimirovich, Grand Duke of Russia
    Grand Duke Vladimir Kirillovich of Russia
    Princess Leonida Bagration of Mukhrani

This is the Russian route stated as the hypothesis — *"connection to like Russian nobility.
Either way, that would get us to the Georgian royal family"* — and it is documented royalty the
whole way.

### Pfinzing reaches Lusignan in 25 hops, through the Norwegian farm lines

    Pfinzing von Henfenfeld -> Geuschmidt -> Baron Henning von Rømer -> Ølver and Ingrid Rømer
      -> Tenga -> Underberge (seven generations of Tore) -> Gjesteland -> Osaland -> Kjosavik
      -> Foss-Vatne -> Borsheim Lye -> Vestly -> Orre -> Høyland
      -> Lejon / Bjälbo -> Canute Duke of Estonia -> Valdemar II of Denmark -> Welf
      -> Plantagenet -> Hugh XI of Lusignan, Count of La Marche

**That middle stretch is the account owner's own ancestry.** `Borsheim`, `Rømer` and `Underberge`
are the same names the `exports/tiny-paths/` chains run through, and all of them are already in
the Geni corpus in quantity:

    Borsheim   57,155 name lines      Hoknes      11,094
    Underberge    489                 Gjesteland     338
    Rømer         305                 Tenga          130
    Osaland       121

⛔ **SO THE JOIN IS BY THOSE PEOPLE, NOT BY ID.** The file carries `RIN MH:I3` and `_UID` and **no
Geni ids at all**, so there is no exact key — `CLAUDE.md` § *Merging is an exact join, never fuzzy
name matching* means this tree cannot simply be merged. The Norwegian farm people are where the
two trees touch, and they are the ones to identify by hand.

### ⛔ AND ONE ROUTE MUST NOT BE TRUSTED

Pfinzing reaches Bagration in 35 hops, but the path runs through
`Hethelo I (Carlos Hethelo Diaz Trones) — 2000th Kroll (arbitrary number until it can actually be
calculated)` and on through the Safavids. That is an explicit placeholder. The same file carries
`Audumbla I` with `DATE 1345294336 BC` and a `_MARNM` of `4th Kroll consort`.

**This is a descent-from-antiquity PROJECT tree and it contains speculative and mythological
connector nodes.** The Reuss route above needs none of them; the Pfinzing-to-Bagration route
depends on one. Treat presence in this file as a lead, never as attestation.

## Corrections, and which routes survive scrutiny

⛔ **`Hethelo` IS NOT A REAL PERSON.** Stated directly, 2026-09-17. Nor are the other filler
nodes this pedigree uses to span gaps: `A few generations`, `Several generations Diaz`,
`Sophia II — 2000th Kroll (arbitrary number until it can actually be calculated)`, `Audumbla I`
at `1345294336 BC`. **Any path through one of them is not a path.**

⛔ **THE "Reuss 13" COUNT ABOVE WAS WRONG. IT IS 4.** Nine of the thirteen are Greek patronymics
ending `-reusson` that a `Reuss` substring match swallowed: Menelaos *Atreusson*, Evippus
*Megareusson*, Itys *Tereusson*, Periphetes *Copreusson*, Althaemenes *Catreusson*, Hermoine
*Atreusson*, Pleisthenes *Atreusson*, Eteocles *Andreusson*, Timalcus *Megareusson*. The House of
Reuss is:

    Heinrich XXIV, Count of Reuss-Ebersdorf
    Augusta Reuss-Ebersdorf
    Princess Augusta Reuss-Köstritz
    Charlotte, Princess Heinrich XVIII Reuss of Köstritz

### The routes that hold

**Reuss → Cyprus, 17 hops, nothing invented** — and it passes through Bavaria:

    Augusta Reuss-Ebersdorf -> Leopold I of Belgium -> Louise of Orléans
      -> Maria Amalia of Naples and Sicily -> Ferdinand I of the Two Sicilies
      -> Charles III of Spain -> Philip V of Spain -> Duchess Maria Anna OF BAVARIA
      -> Henriette Adelaide of Savoy -> Victor Amadeus I -> Charles Emmanuel I
      -> Emmanuel Philibert -> Charles III -> Philip II of Savoy
      -> Anne of Cyprus -> Janus of Cyprus -> James I of Cyprus -> Philip of Lusignan

**Reuss → Pfinzing, 34 hops, also clean**, and it reaches the Norwegian farm lines on the way:
Erbach-Schönberg, Stolberg-Gedern, Mecklenburg-Güstrow, Holstein-Gottorp, Saxony, Prussia,
Brandenburg, the Burgraves of Nuremberg, Brunswick-Lüneburg, Denmark, Lejon/Bjälbo, **Tore Gardson
Underberge, Ragnhild Rømer, Brynhild Tenga, Ingrid Rømer, Henning von Rømer**, Geuschmidt,
Elisabeth Pfinzing von Henfenfeld.

### The routes that do not

**Reuss → Borsheim, 14 hops** and **Reuss → Underberge, 23 hops** both run through
`A few generations`, `Sophia II — 2000th Kroll` and `Several generations Diaz`. The SHORT way into
the account owner's own line is filler; the LONG way, through Denmark and Sweden above, is not.
**Where a short path and a long path disagree, prefer the one with no placeholder in it.**

## Paths from Eric Borsheim

Asked for directly. Computed twice each: the plain shortest path, and the shortest path that
**excludes every placeholder node**. `2,570 of the 31,320 people in this file match a placeholder
pattern` — 8% of the tree — so the two answers differ sharply and only the second one means
anything.

| target | shortest | avoiding placeholders |
| --- | --- | --- |
| Cyprus (Lusignan / of Cyprus) | 18 hops, **through Hethelo** | **35 hops** |
| Reuss (the 4 real ones) | 15 hops, **through Hethelo and "A few generations"** | **44 hops** |
| Pfinzing von Henfenfeld | 25 hops | **25 hops — identical, needs no placeholder** |

Both junk routes leave by the same door: `Eric Borsheim -> Helen Frisk -> Elly Olivia Andersson ->
Carl Andersson -> Several generations Diaz -> Hethelo I`. That is why Cyprus and Reuss *looked*
closer than Pfinzing.

### ⛔ THE UNDERBERGE SPINE CARRIES ALL THREE

Every clean path runs the same first eighteen steps:

    Eric -> Richard -> Randolph -> Reinhert -> Rasmus Paulson -> Paul Pederson Borsheim
      -> Berta Karlsdottir Myklebost -> Gunhild Rasmusdotter Foss-Vatne
      -> Berit Endresdotter Kjosavik -> Endre Toreson Osaland -> Tore Endreson Gjesteland
      -> Endre Toreson Osaland Gjesteland
      -> Tore Toreson VII, Tore Toresen VI, Tore Toresen V, Tore Gardson IV,
         Gard Toreson II, Tore Toreson III  [Underberge]

and only then diverges:

* **Pfinzing** — Ragnhild Rømer, Brynhild Tenga, Ingrid Rømer, Ølver Rømer, Henning von Rømer,
  Margaretha and Heinrich Geuschmidt, Elisabeth Pfinzing von Henfenfeld.
* **Cyprus** — Tore Gardson Underberge (Gard), Ramborg Knutsdatter Lejon, Knut Algotsson Lejon,
  Algot Bryniolfsson, Ingegerd Svantepolksdatter Bjälbo, Svantepolk Knutsson, Canute Duke of
  Estonia, Valdemar II of Denmark, Sophia of Minsk, Helena of Denmark, William of Winchester
  Welf, Matilda and Henry II and John Lackland Plantagenet, Isabella of Angoulême, Alice of
  Courtenay, Hugh XI of Lusignan.
* **Reuss** — as Cyprus to Helena of Denmark, then Otto I of Brunswick-Lüneburg, Adelheid of
  Brunswick-Lüneburg, Adelheid of Hesse, Elisabeth of Henneberg-Schleusingen, Frederick V Burgrave
  of Nuremberg, Frederick I and Albrecht III of Brandenburg, Frederick I of Brandenburg-Ansbach,
  Albert and Albert Frederick of Prussia, Magdalene Sibylle of Prussia, Marie Elisabeth of Saxony,
  Magdalene Sibylle of Holstein-Gottorp, Christine of Mecklenburg-Güstrow, Ferdinande Henriette of
  Stolberg-Gedern, Karoline Ernestine of Erbach-Schönberg, Heinrich XXIV of Reuss-Ebersdorf.

**So `Underberge` is the junction, and the seven generations of Tore are what everything real
depends on.** That is where the exports should be aimed and where the identification work is worth
doing, because a break there breaks all three routes at once.

## What Hethel adds to Richard Borsheim's ancestry

Asked directly: does Richard have ancestors in this file he does not have in the others,
excluding the Hethelo line.

**Ancestors only** — walked upward through `FAMC` to parents, not the undirected kinship graph —
and every branch reached *through* a placeholder is cut at the boundary.

    2,131 ancestor records, 1,834 distinct names, excluding anything through a placeholder
    9,604 if placeholders are allowed

**So the Hethelo line accounts for roughly 7,500 of his apparent ancestors, over three quarters
of the depth.** 51 placeholder parents sit on the boundary where the real tree stops.

### Coverage by the other archive files

    1,831 / 1,834   a.ged                  <- a near-copy of Hethel; comparing to it is circular
    1,025 / 1,834   Mannus.ged.doc
    1,025 / 1,834   Theogrammaticus.ged
      574 / 1,834   Perkwunos r.ged
      222 / 1,834   Gaiad.ged
       16 / 1,834   DescentFromAntiquity 16-36-40
        0 / 1,834   ITIS.ged, American Presidents.ged, Family Historian Sample Project.ged

**Excluding `a.ged`: 684 of his ancestors appear nowhere else.** The list is
`preservation/richard-unique-ancestors.txt`.

### ⛔ BUT ONLY ABOUT 196 OF THE 684 ARE PLAUSIBLE PEOPLE

    196   Nordic farm / patronymic
    113   biblical / antiquity
    375   other, overwhelmingly more antiquity

The Nordic 196 are the real gain and they are Rogaland: Peder Monsen Engelsvåg (Klepp), Tore
Karlson Kalberg (Time), Anders Anderson Auglend, Asbjørn Sigvardson Todneim, Anna Andersdtr.
Austrått, Anfinn Halvardsson, Omund Nilsson Reime, Rasmus Jonson Nærland, Samuel Pederson Vatne,
Sven Torson Rott, Tørres Tørresen Grannes, Helga Vestre Bore, Gjermund Hansson Tu, Laurit Torland.

The remainder is descent-from-antiquity scaffolding and it does not hide what it is: Alulim (the
first king of Sumer), Mattathias Maccabeus, Isaiah the Exilarch, Mar Abba Abra Exilarch — and
records that are not names at all but **haplogroups**: `Abus A0*`, `Adataneses N`, `Noam L3`,
`Barakil CT`, `NO Southeast Asia or Southern China [1]`.

**Three names are unique against the entire archive including `a.ged`**, and one of them matters:
`Rogvolod of Polotsk` (Ragnvald, Рогволод, Рогъволодъ, gamle Ulfsson) — Polotsk is Rurikid, which
is the Russian half of the hypothesis. The other two are `Frotmund Frimitel Ascyla` and
`Unknown Genebald`.
