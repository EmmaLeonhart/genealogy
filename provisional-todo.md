# Provisional to-do

**Emma, 2026-08-15.** A holding file, the same shape as `provisional-queue.md`
was: things that belong in `todo.md` but go here first, because *"I don't know if
the to-do is being properly done."* The **last item of `queue.md`** is the audit
that folds this in and deletes it.

Everything here is **future modelling**, not work anyone is about to do.

---

## 1 · Cladoplast — a property plus a role qualifier, once the item exists

The Gaiad's `P59 Cladoplast of` has no Wikidata equivalent
(`reports/orderlife-properties.md` § *Genuinely novel*). Emma's model for it, when
the time comes:

> some sort of other Wikidata property, with a qualifier of *object of statement
> has role* → **Cladoplast**, for when a Cladoplast item exists on Wikidata

So the shape is `<some property>` + **`P3831`** → *Cladoplast*, exactly the
pattern already used for patronymics (`P3831` → `Q110874`). The base property is
**not chosen** and must not be guessed.

**Her own estimate of when: not soon.** *"The Cladoplast item is probably going to
take a really long time to be made, so it's not exactly something that's that
relevant."* Nothing is blocked on it.

**Note the distinction that has already been got wrong once:** the Cladoplast
*property* is not the Cladoplast *object*. `queue.md` § 0 lists that among the
corrections a transcript audit has to respect.

## 2 · Gaiad characters — individual citations, eventually

*"Gaiad characters, I don't know what's going to happen with them. My thought is,
eventually, once the Gaiad stuff is better sorted out, the Gaiad stuff is going to
have individual citations."*

**They are not a separate class of person.** Emma, same message: *"Everybody is a
human, basically."* So `P31` → `Q5` stays, and no Gaiad-specific typing is
emitted.

## 3 · `T999999` — a Gaiad reference that is MEANT to fail

The interim mechanism, and the deliberate part is the point:

> Right now, I am going to say that the best way to do it would be that
> `T999999` is going to be the property for a Gaiad reference. It's going to be
> the thing that's given as a reference for anything that specifically comes out
> of the Gaiad in the JSON files. **This one's going to throw an error, and it's
> intentionally throwing an error.** Because they would be intentionally throwing
> an error, as I understand it, the JSON editor is just going to not be able to
> add it.

So: anything sourced from the Gaiad carries a reference on `T999999`, which does
not exist on Wikidata, so the edit **cannot execute**. That is a fence, not a bug
— it keeps Gaiad-derived statements in the batch, visible and countable, while
making it impossible for one to reach Wikidata before the citation system is
designed. **Do not "fix" it, do not substitute a real property, and do not filter
these entries out of the batch to make it run clean.**

**It is `T`, not `P`, and that was checked.** Written as `P999999` at first on
the reasoning that properties are `P`; Emma, 2026-08-15: *"It is not P."* So the
`T` is deliberate and is part of why the reference cannot resolve. Do not
"correct" it back.

*"We'll figure out the Gaiad citation system at a later point."*

## 4 · The `gaiad` flag as currently computed is not trustworthy

Not a modelling question — a defect, recorded here because it is what surfaced
the three items above.

`scripts/build-orderlife-batch.py` sets `"gaiad": true` by **searching the raw
JSON text of each order.life item for the string `Q153802`**. Emma: *"You
shouldn't be doing a raw substring search."* It is also the method she rejected on
2026-08-14 — *"random text searches almost always show up false positives"* — and
it currently marks **51,050 of 52,233** batch entries, 98%, which is high enough
to suspect on its own.

The flag has to be read from the **instance-of claim**, which in order.life is
`P39` on person items — **not `P31`**, despite `reports/orderlife-properties.md`
documenting only `P31`. order.life defines both, with identical labels and
datatypes. Kenan (`Q10`) carries `P39` and no `P31` at all.
