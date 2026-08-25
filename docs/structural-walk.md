# What the structural walk actually does, and what it does not

**Emma, 2026-08-24:** *"I'm still not 100% sure how it is that you're doing the zipper
join... It's not clear to me that you've ever been doing the zipper join correctly,
especially since you never really explain how it is that you're doing it."*

She is right that it was never written down. This is the algorithm, exactly, read off
`scripts/walk-structural-merge.py` rather than described from memory.

## The algorithm

```
anchors = people carrying BOTH a Geni id and a QID, who also have a recorded parent
for each anchor, for up to 8 generations:
        compare our `father`  against the item's P22
        compare our `mother`  against the item's P25
        step to:  father  OR  mother      <- father wins when both exist
```

Four verdicts per position:

| verdict | condition |
| --- | --- |
| `AGREE` | our parent carries a QID and it is among the item's values for that property |
| `MERGE` | both sides name someone in that position, ours has no matching QID, **and Wikidata names exactly one person there** |
| `GENI ONLY` | we have a parent, Wikidata does not — a creation, not a problem |
| `WD ONLY` | Wikidata has a parent, we do not — costs us nothing |

`MERGE` is the one that writes a correspondence. **35,708 of them** at the 2026-08-24
build, of which 7,861 became rows in `reports/structural-correspondence.csv`.

## What it is not

**It is not a zipper join.** Calling it one oversold it.

- **It never looks at children (`P40`) or spouses (`P26`).** Neither property appears
  anywhere in the script. The hard cases Emma named — choosing among several children,
  choosing among spouses — are not done badly, they are **not done**.
- **It walks a single line.** `father or mother` means a person with both parents has
  only the father's line walked. The mother is *compared* at that step and then
  abandoned, so half the ancestry is never visited.
- **`MERGE` asserts identity from position alone.** The rule is *"one candidate in the
  same family position"* — no name, no date, nothing else is consulted. So when our tree
  and Wikidata **disagree about who someone's father was**, which is routine for medieval
  and ancient lines, the walk does not see a disagreement. It sees two names for one
  person and pairs them.

The one place it is careful: `len(theirs) == 1` means it declines to guess when Wikidata
records several people in a position. Multiple parent sets produce nothing rather than a
coin flip.

## How reliable is it? Two measurements that do NOT answer, and one that does

**`P2600` as ground truth — biased, do not quote it.** Checking the walk's pairs against
Wikidata's own `P2600` gives 4 agreements and 306 contradictions, an apparent 1.3%
precision. **That number is an artifact.** The walk only proposes a pair when our person's
QID is missing or does not match, so anyone with a usable `P2600` is excluded by
construction. The 310 checkable cases are exactly the disagreement cases. It measures the
selection, not the walk.

**Name-token overlap — too crude.** 78% of pairs share a name token and 12% share none,
but the 12% is dominated by legitimate variance: `Regintrude` ↔ `Ragnétrude`, `Katarzyna`
↔ `Catherine`, `Siemomysł` ↔ `Siemomysl`. The last differs only by `ł`, which the folding
did not normalise. It measures orthography.

**Dates — independent, and the one to use.** Dates play no part in making a pairing, so
they can judge one.

| | pairs |
| --- | ---: |
| dates agree within 15 years | 3,913 |
| **dates conflict by more than 15 years** | **271** |
| no dates on one side | 2,349 |
| no comparable year | 1,328 |

**Of the 4,184 pairs with comparable dates, 94% agree.** That is a real precision estimate
on a little over half the output. The 271 conflicts are demonstrably wrong and include the
cases that started this: `Eric Jedvardsson of Sweden IX` (1120–1160) paired with `Sigurd
Snake-in-the-Eye` (801–891), three centuries apart, and `Anna Eleonore` (1601–1659) with
`Frederika Louisa of Hesse-Darmstadt` (1751–1805).

**The remaining 3,677 cannot be validated with data we hold.** No dates, or dates too
partial to compare. That is 47% of the output resting on position alone with nothing
checking it.

## What follows

- `scripts/validate-structural-walk.py` writes the date verdict per correspondence, so
  the 271 can be dropped and the rest read with the right amount of trust.
- **A real zipper join — children and spouses, both parent lines, several candidates per
  position — is not built.** It is a different piece of work from this walk, and this
  document exists so nobody mistakes one for the other again.
