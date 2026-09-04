# Anvilaquarius

Emma, 2026-09-03: *"Anvilaquarius is a user I want to study the behaviour of."* Then, pointing at
her screen: *"Actually just this pastebin it"* — <https://pastebin.com/v4UcMx36>, which is the
material she named.

**The pastebin resolves** (checked 2026-09-04) and is a **watchlist dump**, not a page about this
user: recent changes by other editors across the items this project has created, late August into
September 2026. Anvilaquarius is one of several editors in it — `OBender12`, `Einar Myre`,
`Epìdosis`, `Samoasambia`, `DeltaBot`, `MS Sakib`, `Poro26`, `Lesko987a` also appear.

## What Anvilaquarius does, from their own contributions

Three edits touching our items, and they fall into two kinds:

| when | what |
| --- | --- |
| 2026-08-30 12:00 | **merged a duplicate we created**: `Q141198489` → `Q139651594` *Sigrid Garborg*, +3,808 bytes, `merge.js` |
| 2026-08-29 11:06 | opened `Talk:Q141180409` — *Birth and death dates are possibly wrong* |
| 2026-08-29 11:06 | opened `Talk:Q141180413` — the same, on the spouse |

So: a merge, and a **talk-page report of a data problem**. Not a revert, not a deletion, not a
complaint about the account.

## The thing worth knowing: there is a channel nobody reads

Both talk threads say, verbatim:

> **Birth and death dates are possibly wrong** — since they are the same as those of the spouse
> {{Q|Q141180409}} / {{Q|Q141180413}}

They were opened on 2026-08-29 and were still unanswered when this was written six days later.
**Nothing in this repo looks at talk pages on the items it creates**, so a human taking the
trouble to write one is not heard. That is the finding; whether to monitor it is Emma's call and
nothing has been built for it.

## Their report is correct, and the dates are GENI's

`Q141180413` **Thomas Matthiæ** (`6000000004334768506`) and `Q141180409` **Magdalena
Andersdotter** (`6000000006127859575`) both carry birth `29 JAN 1541` and death `27 SEP 1580` in
`reports/derived-facts.csv` — which comes from the Geni GEDCOM. So this is not an emission bug
putting one spouse's dates on the other; Geni records them identically and our snapshot matches.

`CLAUDE.md` § *The question is whether OUR TREE MATCHES GENI — never whether Geni is right*: we
are current, and the correction belongs on Geni. § *The purpose is to ADD to Wikidata* keeps it
out of her decision queue.

## How common it is — measured over the whole corpus

`363,615` distinct spouse pairs in `reports/derived-family.csv`:

| | pairs |
| --- | ---: |
| both spouses have a birth date | 232,749 |
| **identical birth dates** | 7,554 |
| identical death dates | 4,062 |
| **identical on BOTH** | **330** |
| identical on both, at day precision | **24** |

So the shape Anvilaquarius spotted is **0.09%** of pairs, and the day-precision form — the
unmistakable one, where a copy-paste is the only plausible cause — is **24 pairs in the whole
tree**. It is not systematic and there is nothing mechanical to fix. They found one of the 24 by
eye.
