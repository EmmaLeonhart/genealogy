# Emma's dictation, 2026-08-26 — the daily QuickStatements algorithm

**Verbatim. Do not summarise this file, do not tidy it, do not reformat it.** Her standing
instruction, 2026-08-25: *"Really save my dictation somewhere verbatim so you can't summarize it
and have to use it directly."* `docs/daily-algorithm.md` is a reading of this and loses in any
disagreement.

---

The current preferences that I have haven't really been met. The idea is that, in our model, the
algorithm for creating quick statements should:
- Check my wiki data profile for all the things that I've edited.
- Grab the things that I've been editing and add them to a thing.
- Take out the things that I've edited and check the actual state of them against a state of wiki
  data that is considered the ideal according to our model.

Our model has a certain conception of an ideal state of wikidata, which comes from the union of
the synoptic tree and the janny tree. In the arnie area, it's really clear. It finds, within this
thing, individuals that it can create based on certain criteria. It creates four parent pairs plus
one person who is a part of the high-upgoing ancestry, like one ancestral pair and four random
pairs. The ancestral pair is shuffled in, so there are five pairs generated. There are also four
people whose spouse and children are randomly filled in.

Once we get to a certain point, the descendant chain that we're actually trying to put in gets
built. From there, we're doing a bit of a step further: we are randomly finding five parent pairs
and then filling them in with their entire children. This is an additional step, although it could
be in the same line as the descendants one.

We also find and do a similar thing with generating 10 name items based upon the missing name
items from the ideal state, with the links as a thing that specifically is made. We do 10 sibling
pair relationships and all of the spouse, parent, etc., relationships between existing items,
because this is a thing that is Because siblings is really massive, these ones are not. Creation of
individuals comes first, then creation of names, then the relationships between the individuals.

The reason why I'm specifically telling you, pretty rigidly, to go in this order is that the order
itself is structurally rigid. The order itself is structurally rigid because it depends on certain
things being capable of being referenced in certain situations. You need an individual to exist for
their name object to be linked to them.

We end up in this weird situation where we create a lot of individuals who are not exactly linked
in the most sensible ways because of this. Situations like:
- Somebody has a link to all of their children and has reciprocal links to all their children and
  reciprocal links with all their spouses, but their spouses are not linked to any of their
  children.
- A person has two parents who are not linked to each other as spouses.

These things aren't how things should work. They're not sensible, but specifically, they are very
intentional. Those intentional parts of this algorithm are there because the algorithm is dependent
on this. The algorithm is highly path-dependent, and we are trying to optimise for the fastest
creation that we possibly can within quick statement batches.

---

The algorithm is a bit weird, and the weirdness isn't something to be sanded off and tried to be
made sensible. The weirdness exists because we are structurally forced into the weirdness by the
nature of the API that we're using.

---

## Two words this transcription mangles, recorded so nobody re-derives them

* **"janny tree"** is the **Geni** tree. Dictation renders *Geni* as *janny* / *Jenny* throughout
  this project's transcripts; `CLAUDE.md` already quotes *"The Jenny ID needs to be present…"*
  meaning the Geni ID.
* **"the arnie area"** is the neighbourhood around **Arne Garborg** `Q467497` — the hyperlocal
  target the whole programme builds out from.

Nothing else here is interpreted. `docs/daily-algorithm.md` is where the reading lives.
