# Collecting surname LEADS for an unrecorded descent

⛔ **THIS COLLECTS LEADS. IT DOES NOT FIND ANSWERS, AND FALSE POSITIVES ARE THE EXPECTED
OUTPUT.** Ruled 2026-09-20: *"the point of this is generally for collecting leads. Not for
finding stuff. So the false positives were expected."*

So a lead that does not survive investigation has not failed -- it has been worked. The first two
(`furman`, `hagman`) were both run to ground and both turned out to carry no Yuri descent; that
is the method operating normally, not a defect in it. Do not report a worked lead as a loss, and
do not tighten the matching until it stops producing them, because the tightening is what loses
the real ones.

Likewise `on_descent_path` is computed for ONE example descendant rather than for every bearer of
the surname. That is intended: the surname is the unit of a lead, and one bearer sitting on the
descent path is enough to make the surname worth a look.


**How the Furman and Hagman leads were found, 2026-09-20.** Written down to be repeated, and to
be repeated *exactly*, because three of the four passes it took produced confident nonsense.

## The question, and the three questions it is not

**Is there a marriage the tree does not record that would make the account owner a DESCENDANT of
a given person?** Here that person is Yuri Vladimirovich Dolgorukiy (`6000000002187826932`,
`Q275106`).

⛔ **Not "is she related to him".** She already is: the harvested blood path runs up through
Ingeborg of Kiev → Mstislav → Vladimir Monomakh, and Yuri is Monomakh's son. Yuri is an
ancestor's brother. Reporting that as a finding wastes the reader's time.

⛔ **Not "are any of his descendants among her ancestors".** A descendant of Yuri cannot be an
ancestor of somebody who does not already descend from him, so the intersection is empty **by
construction**. It was run anyway, returned 0, and 0 meant nothing.

⛔ **Not a reachability count.** § *THE POINT IS TO ADD BLOOD, NOT TO FIND IT IN THE GRAPH*: in a
1.4M-person tree almost any two noble lines connect at some hop count.

## The method

1. **Descendants of the target**, walked DOWN `reports/derived-family.csv` — 152,365 for Yuri.
2. **Plus the raw sweep**, `reports/sweep/*.tsv`, `name_text` as Geni renders it. ⛔ **This is the
   half that matters**: those people are NOT in the synoptic tree, and anybody already in it
   needs no name evidence at all.
3. **The owner's ancestors, SPLIT BY PARENT.** Walk UP from the father and the mother separately.
   The sides are not equivalent — the Swedish maternal line is where Baltic German families
   married in; the Norwegian paternal line far less. Averaging them hides the answer.
4. **Surnames only**, extracted as below.
5. **Rank by rarity**: `len(ancestors_with_it) * len(descendants_with_it)`, smallest first. One
   person on each side is a lead; forty on each side is a common word.
6. **Then read the RECORDS** — dates, places, parents — for the top hits. This is the step that
   separated Hagman from Olai, and skipping it is how a latinised patronymic gets reported as a
   discovery.

## ⛔ Surname extraction, and the three ways it failed first

Each of these produced output that looked like evidence and was not:

| pass | what it did | what it reported |
|---|---|---|
| 1 | every token of 4+ characters | `adeliza`, `agnar`, `agota`, `alienor` — forename to forename |
| 2 | the last token | `Agatha`, `Alan`, `Basil` — labels that ARE a single given name |
| 3 | popped a trailing patronymic, took what was left | `Anna Brita Nilsdotter` → `brita`, a forename |
| 4 | **correct** | `furman`, `hagman`, `von rosen` |

The rules that survived:

- **A trailing patronymic means there is NO family name.** Every Erik's daughter is an
  `Eriksdotter`; it links nothing.
- **But a patronymic in the MIDDLE is ignored** — `Helga Toresdatter Fosse` really does carry the
  farm name `Fosse` after it. A Norwegian farm name sits *after* the patronymic, which is why
  pass 3 could not simply be reversed.
- **A surname needs a surname POSITION**: the last token of a name that has something in front of
  it. A label that is one word is a forename, not a family.
- **Keep the particle phrase whole** — `von rosen`, `van hoogwoud`. Dropping the particle loses
  the entire Baltic German set, which is the population being looked for.
- Drop titles (`herzog`, `grevinde`, `ridder`, `condesa`) and the comma tail after a name.

## ⛔ A SURNAME IS ONLY A DESCENT LEAD IF IT SITS ON THE DESCENT PATH

Both of the first two leads died this way, and the check is now a column rather than a filter.

`Christina Gustaviana von Furman` **is** a Yuri descendant and **does** carry a surname the
owner's maternal line carries. Both true, and it proved nothing: her Yuri blood comes through her
MOTHER, `Margareta Charlotta von Essen`, and runs

    von Essen -> von Wrangell -> von Ritter -> von Krüdener -> von Rosen x7
      -> von Buxhoeveden -> NN Rurykwicz -> Volodimir Yaroslavich -> Olga Yurievna -> Yuri

Her father `Gustaf Adolf von Furman` is **not a descendant of Yuri at all**. So even if he
descends from the owner's Mårten Furman, no Yuri blood moves.

`von Hagmann` died worse: it is a **married name** over a `von Maydell`, which is exactly what
`CLAUDE.md` § *The MARRIED name is the real name* says Geni does. Her line is von Maydell ->
von Wolfframsdorff, Baltic German nobility, nothing to do with `Per Persson Hagman` of Hedensbyn.

A surname travels down the PATERNAL line, so the test is whether the descendant's father is also
a descendant of the target. `on_descent_path` reports `yes`, `no`, or `no father recorded` --
and **a missing father is the thing being looked for, not evidence against**.

⛔ **BUT `no` IS NOT `DISCARD`.** Ruled 2026-09-20: *"these connections are worth preserving.
Connecting the trees will help."* A Furman-to-von-Furman bridge carries no Yuri descent and still
joins two trees, which is the whole campaign. So the column classifies and nothing is dropped:
`yes` rows answer the descent question, `no` rows are tree-connection candidates.

## What it found


    furman   Mårten Furman, abt 1619-1708, Hjoggböle/Bergsbyn, 17 children
             von Furman: Christina Gustaviana b.1736, Eva Johanna b.1740
    hagman   Per Persson Hagman, 1754-1840, Hedensbyn, 19 children
             Hedwig Wilhelmine von Hagmann, b. 26 Aug 1780 at REVAL (Tallinn)

Both maternal ancestors sit in the same district — Hjoggböle, Bergsbyn and Hedensbyn are all
Skellefteå, Västerbotten. `von Hagmann` born in Reval is a Baltic German; `von Furman` is the
ennobled form of a Swedish name. Large sibling counts (17, 19) are what make a descent plausible
rather than a coincidence of spelling.

## ⛔ IT DOES NOT GENERALISE TO THE WHOLE DISCONNECTED POPULATION. MEASURED.

Connecting people who are genuinely unconnected is a way to find connections in its own right --
*"if we can connect people who legit are not connected that's alone a way to find connections"* --
so the obvious next move is to point this at `reports/unconnected-p2600.tsv`. It was tried on
2026-09-20 and it does not work:

    251,607 disconnected P2600 holders
      sharing a surname with the owner's 8,254 ancestors:  51 people, 37 surnames

and the hits are Salvador Dalí, Cameron Diaz, Anita Loos, Kiele Sanchez. **Modern people with
common surnames.**

The reason is structural and will not be fixed by better matching: the owner's ancestry is
pre-modern Scandinavian and European, the disconnected `P2600` population is largely modern, and
a shared `dahl` or `brown` across six centuries is noise. Surname evidence needs two populations
that plausibly overlap in TIME AND PLACE. Yuri's descendants against her ancestry gave 472 leads
because both sides are the same centuries and the same corner of Europe.

So: aim it at a named descendant roster, not at the disconnected corpus.

## ⛔ The limit to state every time

**570 maternal ancestors against 7,684 paternal.** The Swedish side — the one that matters for
this question — is barely in the tree. Only 5 of 472 shared surnames landed there, and that is a
property of the corpus, not of the method. Growing the maternal side is worth more than any
refinement of the matching.

    scripts/yuri-descent-candidates.py      the run
    reports/yuri-descent-candidates.md      the output
