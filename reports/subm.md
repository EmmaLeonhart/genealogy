# What `SUBM` is

**The question.** Emma parked `SUBM` on 2026-08-11 — *"may theoretically exist,
may theoretically be useful. I have no idea how it's going to be useful"* — then
unparked it the same day: *"agentic RAG to figure it out."*

**The answer: `SUBM` is the Geni user who manages the profile, and that user is
themselves a Geni profile in the same ID namespace.**

Census in `reports/subm-census.csv`, one row per distinct submitter, built from
`out/merged.ged` by `scripts/build-subm-census.py`. Offline; nothing queried.

## What the records contain

    0 @S44865@ SUBM
    1 NAME Noah Tutak
    1 ADDR
    2 CITY Los Angeles
    2 STAE CA
    2 POST 90012
    2 CTRY United States

A name, and sometimes a postal address. **Nothing else** — across all 12,176
records there is no subtag other than `NAME` and `ADDR`.

| | |
| --- | ---: |
| distinct `SUBM` records | 12,176 |
| referenced by at least one `INDI` | 12,013 |
| `INDI` references in total | 297,452 |
| people in the tree | 298,591 |
| carrying a postal address | 639 |

So **99.6% of people carry a submitter**. It is not a sparse field.

## The decisive test: the IDs share the namespace with people

`SUBM` xrefs come in two shapes — `@S2043333@` and `@S6000000002973566792@` —
which are exactly the two shapes Geni **profile** IDs come in. That is a testable
claim rather than a resemblance, and the test is whether a `SUBM` id also occurs
as an `INDI` id.

**657 of the 12,176 do.** 645 long-form, 12 short-form.

That settles what a submitter is: not an opaque label but a **person**, in the
same identifier space as everybody else in the file. A manager we have exported
is a manager we can resolve to a profile; the other 11,519 are people whose
profiles we simply have not exported.

## Who the big managers are

| submitter | manages | also in our tree |
| --- | ---: | --- |
| `@S6000000001748382692@` 秋篠宮文仁親王 | 14,090 | **yes** |
| `@S5465477880020118059@` Ir. Dr. TAN Chee Lin, Philip 陳志仁 | 7,874 | no |
| `@S6000000009765734452@` Liu Yao 刘杳 (🇨🇳 Geni Curator) | 6,859 | no |
| `@S6000000003120624112@` Lúcia Pilla | 6,388 | no |
| `@S6000000072442334055@` CBDB (China Biographical Database) | 6,038 | no |
| `@S4802755408520052492@` Erni Muthalib | 4,945 | no |
| `@S6000000179366352856@` Aep Saepul Rohman | 4,742 | no |
| `@S6000000014901320131@` Peter Buvik | 4,684 | no |

Two things are visible here and neither should be over-read. **Geni curators and
institutional accounts appear as submitters** — one is explicitly labelled `Geni
Curator`, another is the *China Biographical Database*. And the largest single
manager carries the name of a living member of the Japanese imperial family; that
is what the record says, and **what kind of account it is has not been
established** — a name in a `NAME` field is not an identification.

## What it is good for

- **Provenance at the row level.** Every fact in this corpus came from somebody,
  and this is the only field that says who. A statement sourced to Geni is really
  sourced to one of 12,176 people.
- **A concentration measure.** The top eight manage 55,620 profiles between them.
  Whether a region of the tree is one enthusiast's work or many people's is
  answerable from this column and from nothing else in the file.
- **It is not a Wikidata field.** Nothing on Wikidata records who typed a fact
  into a third-party site. This is ingestion metadata, and the ignore rule for
  the individual's own record stands.

## The thing worth Emma's attention

**639 postal addresses of living people are in this corpus**, with cities,
postcodes and countries — 187 United States, 99 Norway, 45 Sweden, 24 Canada, 20
Indonesia, 18 Denmark, 15 United Kingdom, 15 Brazil. Plus 12,176 names of living
Geni users.

This is third-party personal data, and it is already committed — it arrived
inside the GEDCOMs, which the repo tracks by design. The census does not disclose
anything new, but it does make it trivially extractable, and that is a difference
worth naming rather than leaving implicit. **NEEDS-DECISION — Emma:** whether
that matters given the repository is private, and whether anything derived from
this corpus that ever becomes public must strip `SUBM`.

## One measurement that came back empty, recorded rather than dropped

**0 `HEAD`-level `SUBM` references.** `CLAUDE.md` notes that an export's `SUBM`
xref is the account owner, which is a fact about the *original exports*;
`out/merged.ged` is written by `genimerge merge` with its own header, so the
account-owner reference does not survive into the merged file. The 297,452
references counted above are all from `INDI` records. If the account owner is
ever wanted, it has to be read from `exports/`, not from the merge.
