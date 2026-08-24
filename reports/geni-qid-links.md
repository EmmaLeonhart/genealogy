# The join key was in the data: a Wikidata URL in the Geni About Me

Emma, 2026-08-23: *"we have intentionally added actual join keys for the Samaritan high
priests, Izumo clan, and Tanba clan... The wikidata items linked in the descriptions."*

She is right, and it is exact. Geni exports the About Me as a `NOTE`:

    1 NAME Takamune /Senge/
    1 NOTE {geni:about_me} https://wikidata.org/wiki/Special:EntityPage/Q135579415#sitelinks-wikipedia

So the profile carries its own Wikidata identity, written by hand for exactly this purpose.
No name, no number, no position in a succession.

`scripts/build-geni-qid-links.py` extracts it. **Only `wikidata.org` URLs count** — a bare
`Q…` in free text is not a claim of identity, and treating it as one is how a loose pattern
starts inventing links again.

## What the corpus holds

**405 Geni profiles carry a Wikidata URL**, across 545 exports. 402 carry exactly one QID;
405 distinct QIDs, of which 3 sit on more than one profile — Geni's ordinary
duplicate-profile situation, reported and never merged.

| family | roster items | joined by the About Me URL |
| --- | ---: | ---: |
| **Izumo / Senge** | 204 with a QID | **111** |
| **Tanba** | 183 distinct QIDs | **179** |
| **Samaritan high priests** | 85 profiles | **0** |

### Izumo: 111, against 76 for the regnal-number join it replaces

| lineage | joined |
| --- | ---: |
| Izumo | 39 (all) |
| Senge | 22 (all) |
| Kitajima | 14 of 16 |
| other — En'ya, Sasaki, Higashi, Hiraoka, Ookuma, Takaoka | 36 |

The 36 "other" are the decisive difference: they carry **no regnal number at all**, so the
number join could never have reached them however well it worked.

**Two Kitajima are in the corpus but carry no About Me link** — `Kitajima no Tokitaka`
(`Q135579474`) and `Kitajima no Yasutaka` (`Q135579480`). They are not missing people; they
are profiles missing the link. Adding it on Geni is a one-line fix and Emma's to make.

**One duplicate:** `Senge no Naokatsu` (`Q135579476`) sits on `6000000227334350078` and
`6000000227335699823`. Both ids go in the pairing — `P2600` is multi-valued and a second
statement is the correct representation.

93 rostered items are not linked from any Geni profile we hold; `reports/izumo-unlinked.tsv`.

### Samaritans: the key IS there, and my "0 of 85" was the wrong population

**Corrected 2026-08-23, same day.** The line above said no Samaritan profile carries the
link. That was reading a true number as a false statement.

**15 Samaritan-side profiles in the corpus carry a `wikidata.org` About Me link**, and they
are the right people:

| | |
| --- | --- |
| high priests | Aaron I `Q51676` · Phinehas I `Q128063` · Eleazar I `Q159443` · Abishua I `Q2338482` · Bakhi ben Sashai `Q2836764` · Sashai ben Abishua `Q115804497` · Jonathan I `Q20502598` · Baba Rabba `Q2911644` |
| Pentateuch figures around them | Moses `Q9077` · Amram `Q477527` · Jochebed `Q594805` · Nadab `Q1941782` · Abihu `Q321166` · Itamar `Q1675214` |
| and | Sanballat the Horonite `Q751918` |

What carries no link is the **85 profiles named in `reports/wikidata-samaritan-priests.json`
and `reports/wikidata-samaritan-links.json`** — a different, later set of priests. "0 of 85"
was true of those 85 and says nothing about Samaritan profiles in general.

**A `Forest` export from `6000000227245553985` (Yitzhaq I ben Tsedaka) was run to test the
staleness hypothesis and was unnecessary: 5000 people, 0 new, 0 new links.** Every one of
the 15 was already in the corpus. The hypothesis was reasonable and the check was one grep
away — `grep -c wikidata.org` on the exports we already had would have answered it without
spending an export.

## Why this supersedes the regnal-number matcher

**Wikidata does not carry the regnal numbers.** Joining on them was never a join *to*
Wikidata — it was a join to the Shinto-wiki page's own column, which was then treated as
Wikidata's key. And extending it to the earlier kokuso matched on the stopword `no`, pairing
Ame no Hohi with a Swedish woman. Both are retracted; see `reports/izumo.md`.

Where the two overlap they agree: of the 76 rows the regnal join produced, **74 match the
About Me link exactly and 0 disagree**; the other 2 are the Kitajima with no link.

**Reach for this first.** An identifier written into the data on purpose beats any
reconstruction from names, numbers or positions.

## What that key is worth on Wikidata: 354 statements

`scripts/build-qid-link-p2600.py` compares the 408 pairs against
`out/wikidata/p2600-all.tsv`:

| | pairs |
| --- | ---: |
| already stated on Wikidata | 54 |
| **item carries no `P2600` at all — a straight addition** | **349** |
| item has a `P2600` with a different Geni id — a *second* statement | 5 |

**354 statements**, in `reports/wikidata-geni-qid-p2600.qs`, for 2026-09-01.

**None of the 5 is a conflict**, and one of them proves the rule: `Q51676` Aaron against
`6000000227239142939` (`Aaron I /Samaritan High Priest/`) is exactly the unmergeable pair
`CLAUDE.md` documents. `P2600` is multi-valued, 2861 stored items already carry more than
one, and a second statement is the correct representation. Never replaced, never withheld.

The other four: `Q60109288` Olof Nobelius, `Q75446688` Jennette MacKenzie, `Q120564`
Meishō, `Q87470638` Catharina Elisabet Elfstrand.

**The comparison is against a snapshot taken 2026-08-09**, so an item that gained a `P2600`
since reads here as an addition. QuickStatements is idempotent for an identical statement,
so that staleness costs a no-op rather than a wrong edit.


## How the four batches relate — checked 2026-08-23, no conflicts

Four `.qs` files in `reports/` assert `P2600` *Geni.com profile ID*, between them **364
distinct QIDs**. Running all four is safe; here is why, so nobody has to re-derive it.

| file | statements | not covered by `wikidata-geni-qid-p2600.qs` |
| --- | ---: | ---: |
| `wikidata-geni-qid-p2600.qs` | 354 | — |
| `wikidata-add-geni-id.qs` | 36 | **7** |
| `wikidata-bureatten-p2600.qs` | 7 | **7** |

**29 of the 36 in `wikidata-add-geni-id.qs` are byte-identical claims** already in the new
batch — the About Me links rediscovered what an earlier pass had found by other means, and
agreeing is the good outcome. QuickStatements is idempotent for an identical statement, so
the overlap costs a no-op.

**No QID is given a different Geni id by two different files.** Four QIDs carry two Geni
ids, and every one is the multi-valued case `CLAUDE.md` describes rather than a
disagreement: `Q135524854`, `Q135524952`, `Q135579476` *Senge no Naokatsu* and `Q694696` are
each one person with two unmergeable Geni profiles. `P2600` is multi-valued; both
statements belong.

**So all four still have work to do** — the two older files are not superseded, they carry
7 pairs each that the About Me links do not reach. Their statements have no `S2600`
reference at all, which the template permits: `P2600` is in the uncited group.


## The synoptic correspondence: five sources, now one file

**Emma, 2026-08-23, and she was right to worry:** *"there was a tsv qid correspondence
quickstatement thing is that represented in our data?… I'm afraid it isn't properly
represented in our synoptic tree."*

Five files held QID↔Geni pairings and **nothing joined them**, which is exactly the
artefact `CLAUDE.md` says the synoptic tree is for. `scripts/build-synoptic-correspondence.py`
now writes `reports/synoptic-correspondence.tsv`, every pair carrying its provenance.

| source | pairs |
| --- | ---: |
| `out/wikidata/p2600-all.tsv` — what Wikidata already states | 517,823 |
| `reports/structural-correspondence.csv` — found by walking relationships | 3,902 |
| `reports/geni-qid-links.tsv` — the URL Emma wrote into the Geni About Me | 405 |
| `reports/geni-wikidata-pairs.csv` | 126 |
| `reports/izumo-p2600-pairs.tsv` | 112 |
| **distinct pairs after the join** | **522,086** |

518,680 QIDs against 521,823 Geni profiles.

### Two kinds of multiplicity, and only one is a problem

**3,257 QIDs carry more than one Geni id, and that is correct.** Two Geni profiles for
one person is a permanent structural feature of Geni, `P2600` is multi-valued, and the
local store already holds 2,861 items with more than one. Not flagged, not adjudicated.

**257 Geni profiles claim more than one QID, and that is a contradiction** — one person
cannot be two Wikidata items. `reports/synoptic-conflicts.tsv` lists them with the
sources that disagree. **67 are Wikidata disagreeing with itself** (both QIDs already
carry that `P2600`), so they are not ours to have caused. The other **190 involve one of
our own sources**, and **183 of those are `structural` against `wikidata-p2600`** — the
relationship walk proposing a pairing for a profile Wikidata already links elsewhere.

**Nothing here is resolved.** Identity calls and merges are Emma's, and a contradiction
is a note rather than a work item — `CLAUDE.md` § *The purpose is to ADD to Wikidata*.
What changed is that the disagreements are now visible in one place instead of implicit
across five.
