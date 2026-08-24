# The 257 Geni profiles mapping to more than one Wikidata item

Emma asked to see a sample rather than have a rule applied to them. The sample is
`reports/synoptic-conflicts-labelled.tsv` — every row with **names on both sides**, since
bare QIDs are unreadable. What the sample shows is that these are not one phenomenon but
three, and the largest is not a contradiction at all.

## The ten records

| Geni | candidate A | candidate B |
| --- | --- | --- |
| Katharina von Braunschweig-Wolfenbüttel | `Q434771` Catherine of Brunswick-Wolfenbüttel | `Q567039` **Henry IV, Duke of Brunswick** |
| Canute I Erikska King of Sweden | `Q320977` Canute I of Sweden | `Q442876` Harthacnut I of Denmark |
| Eric Jedvardsson of Sweden IX | `Q310152` Eric IX of Sweden | `Q41864` Sigurd Snake-in-the-Eye |
| Rikissa of Sweden of Poland | `Q2241510` Richeza of Poland, Queen of Sweden | `Q2616032` Christina Ingesdotter |
| Aldonza Hinojosa | `Q133284526` Isabel Rodríguez de Aguilar | `Q134986472` **Aldonza Hinojosa** |

In every one, **one candidate is the person and the other is a different human** — in the
first case not even the same sex. These are not two plausible readings of one identity.

## Three populations, by provenance

| | count | what it is |
| --- | ---: | --- |
| **structural inference vs Wikidata's own `P2600`** | **180** | our walk proposed a QID; Wikidata itself states a different one |
| **two Wikidata items both assert this Geni ID** | **70** | duplicates on the Wikidata side |
| other | 7 | mixed provenance, needs eyes |

**The 180 are not contradictions and should never have been counted as such.** `P2600`
*Geni.com profile ID* is a statement Wikidata carries; the structural walk is our
inference from tree position. Where they disagree the recorded identifier wins, and the
walk was simply wrong — which is the failure mode `reports/bureatten.md` already
documents, where intersection "confirmed" four wrong matches out of seven because a
position holds several people. **Drop the structural candidate, keep the `P2600` one.**
That is a correctness call, not a preference, so it is taken here rather than parked.

**The 70 are Wikidata-side duplicates and are NOT ours.** Two items each claiming the same
Geni profile means Wikidata has the person twice. `CLAUDE.md` settles the mirror image —
one item carrying several Geni IDs is correct and expected — but this direction is a
genuine duplication, and merging Wikidata items is exactly the kind of destructive edit
this project does not perform. Flagged, never merged.

**29 of the 257 have both items carrying the same label**, which is the signature of the
duplicate case rather than the mis-inference one.

## Files

- `reports/synoptic-conflicts-labelled.tsv` — all 257 with names on both sides.
- `reports/synoptic-conflicts.tsv` — the raw pairs.
