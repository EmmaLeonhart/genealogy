# What one QuickStatements batch contains

**Emma dictated this on 2026-08-25** after seeing batches that tried to do the whole spine at once.
It is the shape of every run from here. `CLAUDE.md` § *THE THREE LINES* is what is being built;
this is how much of it moves per day.

## It is SLOW on purpose. This is the point that keeps being missed

> *"I'm not trying to make all of them immediately. You do understand that, right? I would consider
> maybe two links per day to be acceptable, but really, probably one link a day. This should be
> taking about 18 days, or at least 18 quick statement generations."*

And:

> *"This isn't intended as being a quick thing that just establishes the connection. I think the
> problem is you tend to think that it's supposed to be a quick thing. It's not a quick thing. It
> is specifically built here in this form so that it runs slowly. It could theoretically be run
> daily, not really making a big scene about itself."*

**18 runs, one a day, is the plan.** It can be shorter or longer, several batches in a day, or a
day skipped. What it must not be is one big batch that does the lot.

> *"The quick statements are part of our transitional period towards eventually moving towards more
> full-on automation. The quick statements are intended as being bad. Our full-on automation is
> intended as having roughly a similar form, but there are some notable characteristic
> differences."*

## The subgraph is Arne's component ON WIKIDATA — clarified 2026-08-25

Asked what radius over our Geni tree should bound the random draws, Emma: *"Uhh what the fuck. You
misunderstand it completely if you're even asking the question."* The bound is not a radius over
our tree at all. It is **Arne's connected component on Wikidata, as it currently stands** — 42
items today, larger after every run, because the runs are what build it. Each batch draws its
random work from what exists and enlarges the pool the next batch draws from.

That is what makes the programme self-bootstrapping, and it is why it takes ~18 runs rather than
one: the pool has to grow before there is more to draw from.

**And it is why Bure needs its own algorithm rather than a bigger radius.** Emma: *"bure is a bunch
of unlinked people with entity resolutions to geni, so it isn't dense it's a different kind of area
though which needs its own algorithm."* There the items already exist and carry `P2600`, so the
work is linking QIDs that both exist — which has no `LAST` constraint and therefore does not need
this pacing at all. `queue.md` § *Bure kinship as random-walk start points*.

## What goes in one batch

**Always both parents.** *"We always make both parents, if both parents exist, as a part of the
generation."* A couple goes in together or not at all.

| # | content |
| ---: | --- |
| 1 | **The spine couple** — the next chain person **and their spouse**, working up from Arne toward Bergitte, then Bergitte toward Charlemagne |
| 2 | **4 random sets of parents** — drawn from the ball |
| 3 | **4 random families** — a solitary individual gets their spouse and all their children added |
| 4 | **1 random existing couple** — all of their children, properly linked |
| 5 | **≤10 mutual sibling links** — reciprocal, so **20 statements** |

**Three readings settled by Emma on 2026-08-25, each of which the first draft had wrong:**

- **The spine couple is the chain person plus their spouse**, not the two parents of the chain
  person. One run advances the line by exactly one step and brings the off-chain partner with it.
- **"One couple on Arne's side" is not its own component.** Her words: *"this is just part of the
  add 4 sets of parents randomly in the neighborhood not its own thing. But one thing that is
  worth doing imo is randomly choose an existing couple and add all the children. Properly linked
  and everything."* So it was replaced by the existing-couple component above.
- **Solitary means an item with no `P26` spouse and no `P40` child** — *"Has an item and no SPOUSE
  or CHILD specifically"* — and it **counts the people our own earlier runs created**, since a
  fresh `CREATE` starts with neither. Without that this component starves: almost nothing in the
  ball has family statements yet.

`scripts/build-garborg-day.py --compose` implements exactly this. Every component reduces to
*which people go in the frontier*, because the emitter already owns labels, names, dates, sex,
`S2600` references and the duplicate guard. `--seed` makes a run reproducible.

Emma on the sibling arithmetic: *"we are actually mixing together 10 sibling links. Each sibling
link here is actually 20 fixed statements, but it's 10 being linked together."* That is the same
10-a-day cap `CLAUDE.md` records — ten *links*, twenty *statements*.

## The spouse problem, and why the shape looks wrong

A pair of parents created in the same run **cannot be married to each other in that run**,
because `LAST` names only the most recently created item and neither of them can refer to the
other.

**`LAST` IS valid as a value; the limit is narrower than this repo long claimed.**
`Q141178381 P22 LAST` is ordinary QuickStatements — the subject already exists and `LAST`
resolves to the item created just above. What cannot be done is linking **two items created
in the same run** to each other, because `LAST` names only the most recent one.

Emma, 2026-08-25: *"you never actually did the 2-way relationship addin qith the creation of
items that is completely possible but you just decide to fuck off and no do it because it goes
QID PID LAST instead of LAST PID QID."* The general claim was mine, not hers, and it cost her
weeks of one-way links to repair by hand.

**This distinction was lost for weeks and it changes the shape of the batch.** Everything a new
person is related to that ALREADY has a QID — parents, spouses, siblings, children — is linked
both ways in the same run. Only new-to-new links wait. Emma: *"the parents cannot actually be linked to each other because of a technical
limitation in terms of quick statements, but the quick statement batch is supposed to be this
way."*

So the links land one run late, and she has accepted that deliberately:

> *"This is a bit of an unnatural arrangement because the children aren't linked to the spouse or
> spouses... but then the next run, the spouse gets linked to them, and the children get linked to
> that one. This is a bit of an unnatural way of doing things, but the idea behind the unnatural
> way of doing things is that it goes as fast as it can like this."*

**Each batch therefore opens by closing the previous batch's spouse and child links** before
creating anything new. `scripts/build-missing-reciprocals.py` is that half.

## When Bergitte is reached, the direction flips

> *"once we reach the point where Bergitte is in the graph thing, we then do the thing of creating
> the family. We create the family going down, with the descent going down, and we have the family
> going down until it reaches me."*

Up from Arne to Bergitte, up from Bergitte to Charlemagne, then **down from Bergitte to Emma** —
line 2, the one not yet captured.

## Deterministic and random, mixed on purpose

> *"The quick statement batch essentially finds a random individual with their parents, and it has
> all of the chokes. It has these 18 chosen couples, and it will have one of them each day. Plus,
> it will randomly create parents throughout the specific subgraph somewhere."*

**The 18 spine couples are the deterministic part** — chosen, ordered, one per run. Everything else
is drawn at random from the subgraph. The random work is not filler: it thickens the neighbourhood
the spine runs through, which is what `CLAUDE.md` § *The practical goal is EMMA densely linked*
asks for.

## Lower priority, named as such

The nearest-blood and nearest-in-law chains between Emma and Arne — `queue.md` § *Connect Emma and
Arne Garborg to Bergitte Aukland* — are *"ones that I don't care about as much, but they're ones
that we could be filling in over time."* Fill them opportunistically; never at the cost of a spine
step.
