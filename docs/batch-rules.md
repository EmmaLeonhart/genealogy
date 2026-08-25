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

## What goes in one batch

**Always both parents.** *"We always make both parents, if both parents exist, as a part of the
generation."* A couple goes in together or not at all.

| # | content |
| ---: | --- |
| 1 | **The spine couple** — the two parents of one individual on the line, working up from Arne toward Bergitte, then Bergitte toward Charlemagne |
| 2 | **One couple on Arne's side** — the two parents of an individual at the bottom end |
| 3 | **10 mutual sibling links** — chosen at random across the data. Reciprocal, so **20 statements** |
| 4 | **4 random sets of parents** — anywhere in the subgraph |
| 5 | **4 random families** — a solitary individual gets their spouse and all their children added |

Emma on the sibling arithmetic: *"we are actually mixing together 10 sibling links. Each sibling
link here is actually 20 fixed statements, but it's 10 being linked together."* That is the same
10-a-day cap `CLAUDE.md` records — ten *links*, twenty *statements*.

## The spouse problem, and why the shape looks wrong

A pair of parents created in the same run **cannot be married to each other in that run**. `LAST`
is only valid as a QuickStatements subject, never as a value, so neither new item can cite the
other. Emma: *"the parents cannot actually be linked to each other because of a technical
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
