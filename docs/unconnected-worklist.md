# The unconnected-`P2600` worklist — the specification

**Dictated 2026-09-09, after a first attempt was lost to a flat phone battery. Written down
before any of it is built, because that is the thing that was lost.**

---

## 0. THE PREMISE THAT IS NOT YET TRUE

> *"I don't think that the CI/CD currently combines the WikiData tree with the geni trees. The
> WikiData tree doesn't go into the synoptic tree."*

**Checked, and it is correct.** `scripts/rebuild-everything.py`'s merge step is

    genimerge merge --also out/manual-parental-correspondences.ged

over `exports/**/*.ged`. That is the Geni corpus plus one small hand-correspondence GEDCOM.
**Wikidata's relationship edges — 5,041,567 of them across `P22`, `P25`, `P40`, `P26` and
`P3373` — never enter `out/merged.ged`.** `scripts/p2600-connectivity.py` does the union in
memory with union-find and writes no tree, so it is not that either.

**So the first thing this needs is a build step that does not exist:** Wikidata's tree goes
INTO the synoptic tree.

## 1. THE CANONICAL FORM IS NATIVELY A GEDCOM

> *"The syntactic tree now has a canonical form that is natively a Gedcom because that means
> that it preserves the family IDs, which is important for some stuff."*

So the Wikidata side is rendered as a GEDCOM and merged, rather than joined in memory — the
`FAM` records and their ids survive that way, and a union-find over edges destroys them.

## 2. THE FILE

Produced **after** the synoptic tree is built, from both halves. **Columns in this order:**

    1. Wikidata QID
    2. Geni id
    3. neighbourhood size
    4. last date attempted

## 3. WHO IS IN IT

**Every `P2600` person on Wikidata is considered.** Then:

    linked to Charlemagne, or linked to a person who is linked to Charlemagne  ->  NOT in the file
    not linked to Charlemagne                                                 ->  in the file

Membership is **recalculated every run** and never stored. Success therefore needs no state:

> *"they just wouldn't be generated into the TSV file so we don't really have to statefully
> store whether we've been successful. The synoptic tree build is just going to say whether
> we're successful or not."*

## 4. NEIGHBOURHOOD SIZE

**One number: the size of the person's combined Wikidata-and-Geni neighbourhood in the synoptic
tree.** Not two columns, not one per source.

**It is the ranking key, and the reason is leverage:**

> *"something in a very large neighborhood, if it gets connected, it'll just connect the entire
> neighborhood and that's very good."*

Some of these people truly have no relatives; some sit in large clusters. The number separates
them.

## 5. LAST DATE ATTEMPTED

**Written by the extension**, automatically, every time it runs on somebody to try to connect
them. Nothing hand-maintained.

**Seed values, explicitly placeholders:**

    a path capture has been attempted   ->  2026-09-01
    everything else                     ->  2026-01-01

## 6. WHAT THE CI REGENERATES AND WHAT IT CARRIES FORWARD

> *"The CI/CD is going to, after regenerating this TSV file, use the dates from the older
> version but everything else is going to be essentially recalculated."*

| column | on each run |
| --- | --- |
| Wikidata QID | **fixed** |
| Geni id | **fixed** |
| neighbourhood size | **recalculated** |
| last date attempted | **read from the previous version of this file** |
| membership | **recalculated** |

**⛔ THERE IS NO SECOND FILE.** *"Actually I don't think we even need a separate file."* The
TSV carries its own state, so the previous commit of it is the input to the next run.

## 7. THE ORDER — deterministic, nothing random

> *"there is actually going to be a specific algorithm that we're going to use, nothing random.
> It's all deterministic."*

**Two blocks:**

    ELIGIBLE     at the top
    INELIGIBLE   below, ordered by WHEN THEY BECOME ELIGIBLE

**Within either block:**

    neighbourhood size DESCENDING
    then Wikidata QID ASCENDING

Take from the top. Eligibility is a **30-day cooldown**: *"If they are not connected then we
wait 30 days."*

> *"This might be a bit excessive in one file but I think that this sorting thing is going to be
> useful because it would give a good idea of the stuff here."*

## 8. WHY IT DRAINS — the part that makes it work

* **A failure costs one attempt.** *"if we fail on an individual, we've attempted it and we move
  on."* The person goes to the back and the graph keeps moving underneath them.
* **Collateral connection is the main mechanism.** People hit as a side effect — on somebody
  else's path, or scraped as somebody else's relative — *"are just going to not be in this list
  anymore because they're connected."* They leave without ever being worked.
* **Both ties exist for surface area.** *"This is part of the reason why we're wanting to do
  in-law and blood relationship: it provides more surface area for these tiny edges to
  potentially hit new people and get more connectivity."*
* **A `Forest` export takes a neighbourhood to 5,000**, which is *"generally enough that they
  will be pretty easily connected in"* — and it raises OTHER people's neighbourhood sizes,
  pulling them up the ranking. Stated with deliberate uncertainty: *"I'm not going to say this
  with the biggest confidence. There might be some people who are in the 5,000 and not in
  there."*
* **Truly isolated people never leave.** *"They're going to be constantly attempted and then
  moved to the end because of the failure."* That is the design working, not a defect.

**The worked case:** a person in a neighbourhood of 5,000 whose QID sorts first is certainly
chosen. Connected → they leave the file. Not connected → 30 days.

## 9. SCOPE

> *"we're calculating based off of every single P2,600 person on Wikidata."*

Measured 2026-09-09 by `scripts/p2600-connectivity.py`, over the union graph but **without** the
Wikidata GEDCOM merge above: 518,889 holders, 252,688 connected, **266,201 not**. That is the
order of magnitude the file starts at; the real number comes from the tree once § 0 is built.

---

## What exists, and what does not

| | |
| --- | --- |
| the connected/disconnected split | **exists** — `scripts/p2600-connectivity.py`, in memory |
| Wikidata as a GEDCOM in the merge | **does not exist** |
| neighbourhood size | **does not exist** |
| the TSV, its four columns, the ordering | **does not exist** |
| the date carry-forward | **does not exist** |
| the extension writing a date on each attempt | **does not exist** |
| CI running any of it | **does not exist** |
