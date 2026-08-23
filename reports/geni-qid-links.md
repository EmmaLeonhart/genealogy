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

### Samaritans: the key is not in our corpus, and that is a bound not a conclusion

None of the 85 Samaritan profiles in `reports/wikidata-samaritan-priests.json` and
`reports/wikidata-samaritan-links.json` carries a `wikidata.org` URL in its About Me — not
even the nine whose QID↔Geni pairing is already recorded by hand.

**Our exports are a sample of Geni, so this cannot mean the links are absent from Geni.**
The Samaritan exports were taken in mid-August; if the links were added after that, no
export of ours would show them. One fresh `Forest` export from a Samaritan seed settles it
and costs one run.

## Why this supersedes the regnal-number matcher

**Wikidata does not carry the regnal numbers.** Joining on them was never a join *to*
Wikidata — it was a join to the Shinto-wiki page's own column, which was then treated as
Wikidata's key. And extending it to the earlier kokuso matched on the stopword `no`, pairing
Ame no Hohi with a Swedish woman. Both are retracted; see `reports/izumo.md`.

Where the two overlap they agree: of the 76 rows the regnal join produced, **74 match the
About Me link exactly and 0 disagree**; the other 2 are the Kitajima with no link.

**Reach for this first.** An identifier written into the data on purpose beats any
reconstruction from names, numbers or positions.
