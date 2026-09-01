# How the synoptic correspondence is actually made

**Emma, 2026-08-25:** *"Put into the queue also an analysis of how the synoptic tree is actually
made."* And the framing that makes this a survey rather than a blocker: *"I'm going to treat the
synoptic tree as though it is perfect, and we are going to address whether the synoptic tree is
well functioning later."* So nothing waits on this; it is a description of what
`scripts/build-synoptic-correspondence.py` does, and a list of the places it is doing something
nobody chose.

Measured by running it, 2026-08-31.

## What comes out

    565,348 distinct (qid, geni) pairs
    561,999 QIDs · 564,931 Geni profiles
      3,225 QIDs carrying more than one Geni id   — ordinary, P2600 is multi-valued
        410 Geni profiles claiming more than one QID — contradictions, hers to settle

`reports/synoptic-correspondence.tsv` is the union; `reports/synoptic-conflicts.tsv` is the 410.

## The eight sources, and what each is worth

| source | pairs | what its evidence is |
| --- | ---: | --- |
| `wikidata-p2600` | **518,941** | Wikidata's own `P2600` statement. Not our inference at all. |
| `zipper` | **45,898** | Our positional join, all eight rounds. Inference, with provenance. |
| `structural` | 7,606 | The relationship walk: both sides have a person in the same slot. |
| `geni-about-me` | 405 | **Her own QID links written into Geni bios.** Her statement of identity. |
| `tanba-roster` | 181 | Hand-built clan roster. |
| `geni-wikidata-pairs` | 126 | |
| `izumo-sister-roster` | 121 | |
| `izumo-roster` | 111 | |

**Two sources are 99.9% of the volume and they are of completely different kinds.** `P2600` is
Wikidata asserting the identifier; the zipper is us inferring it from position. Anything reading
this file and treating a pair as one thing is flattening that distinction — the `sources` column
is what keeps it, and it should never be dropped.

**The long tail is not noise.** 405 + 181 + 126 + 121 + 111 = 944 pairs that no automated method
found, most of them from her own hands. `geni-about-me` in particular is the only source here that
names people whether or not any inference reaches them.

## The `date_refuted` filter, and what it deliberately does not touch

**235 structural pairs dropped.** A pair like `Eufemia von Hirscher` 1166–1229 against
`Margaret of Nuremberg` 1359–1390 is not a judgement call — Emma, 2026-08-24: *"All these ones
look easy."*

**It refutes OUR OWN inference and nothing else.** A `wikidata-p2600` pair whose dates disagree is
Wikidata stating an identifier we do not get to overrule; that is a disagreement to record, not a
pair to delete. The filter therefore keys on the *pair* rather than on the Geni id, so the same
person can be refuted as a structural guess and kept as a Wikidata statement.

Absent `reports/structural-walk-validation.tsv` it is an empty set and the build still runs — a
missing validation file costs 235 bad pairs, not a crash.

## `ROUND_CAP` is 8, and the reason it is 8 is a correction

The zipper contributes all eight rounds. It was **3** on a date-based error curve that rose 3.9%
at round 1 to 27.1% at round 8 — and that curve was a **coverage artefact**: the share of pairs
carrying a birth year on *both* sides falls 65% → 20% with depth, so the "error" was tracking the
decline of the measuring instrument rather than the join.

Measured instead against `P21` *sex or gender*, which has 86–100% coverage at every round and is
corrected for the father/mother slots where sex can never refute, the real rise is **2.8% → 4.8%**.
Hence 8. `scripts/zipper-join.py` § `ROUND_CAP` carries the full working.

This is the clearest case in the repo of a metric that looked like a finding and was about the
instrument.

## Where it is doing something nobody chose

- **`Onakatomi` is absent and it is deliberate**, but the reason is recorded only as a comment in
  the source list: 0 of its 97 QIDs has an About Me link, so there is nothing to join on. It will
  become joinable the moment those links exist, and nothing will notice.
- **The multi-valued cell split is per-source.** `izumo-roster`, `tanba-roster` and
  `izumo-sister-roster` read a `geni_ids` column and the others read `geni_id`. That is four
  places that have to agree about a separator, which is the exact shape of the ` | ` bug
  `CLAUDE.md` § *Our side could never have two children* records.
- **410 Geni profiles claim more than one QID and the file records them without resolving them.**
  That is right — they are hers to settle — but nothing downstream is required to look at
  `synoptic-conflicts.tsv`, so a consumer of the correspondence gets both pairs silently.
- **No source is weighted.** A `zipper` round-8 pair and a `wikidata-p2600` pair are the same row
  with a different `sources` value, and any consumer that does not read that column treats an
  inference as an identifier.
