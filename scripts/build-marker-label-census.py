"""Every label that carries a placeholder marker inside it, on both sides.

**Emma, 2026-08-17:** *"Put an item at the end of the queue that finds these kinds of
ones where the label has this stuff already in it, and normalizes them into proper
things based on our rules."*

This is the census that item needs, and it is a census rather than a fix because
`CLAUDE.md` § *"Analyse this" means build a CSV* asks for every instance first: *"you
run a script to build a CSV of every single instance of the phenomenon that I'm asking
you about, and then do an analysis on it, and then make a decision explicitly."*

**Both stores, named separately**, per § *"Is X present?"*: the Geni corpus by way of
`reports/derived-labels.csv`, and the local Wikidata store by a full scan of
`wikidata/items/`. A row says which side it came from. Nothing is asked of the network.

### What counts as marker-bearing, and why it is token matching and nothing cleverer

A label is reported when **any whitespace token of it** is placeholder vocabulary. That
finds the three shapes that matter and keeps them apart in the output:

* `whole` — the label **is** the marker. `NN`, `Private`, `ukj.`
* `head` — the marker leads and something real follows. `NN Hildesheim`,
  `nn Pedersdatter`, `N.N. Andersdatter Skeel` — the surname is real data and
  `CLAUDE.md` is explicit that throwing it away loses 3,605 surnames.
* `inside` / `tail` — the label is a **description**, not a name. `NN wife of Aun`,
  `Unknown Wife`, `Wife of רבי משה`, `Maka till Brynjolf Brandsson`.

**A second class carries no marker at all** — `Maka till Brynjolf Brandsson`,
`Wife of Moshe Lazers`, `hija de Pedro` — a description sitting in the name slot. Those
are found by `description_in`, whose vocabulary is **read out of
`scripts/build-nn-label-batch.py`'s own ten-language table** rather than written from
memory: a label that already reads like a phrase this project *generates* is a
description by construction. 154 `(word, of)` pairs, required adjacent, which is what
keeps `hija de` apart from `Rodrigo de Vivar`.

**CJK descriptions are NOT detected and that is deliberate.** `陳母` is *Chen's
mother* and there is no table for it. Treating a trailing `母` as a relationship marker
is a real decision about Chinese naming, not a lookup, and the `remainder` column is
where the evidence for making it will come from.

Every row carries `kind` — `marker` or `description` — so the two never merge in the
output. A marker wins when both are present: `NN wife of Aun` is reported as its marker
with `wife of Aun` as the remainder, which shows the description is there too.

### The vocabulary is three sets that disagree, and the disagreement is the point

Her queue item says they *"should end up as one"*. They cannot be merged silently,
because they were built to different rulings:

* `scripts/labels.py` — deliberately **narrow**: `private`, `<private>`, and the `NN`
  spellings. Its docstring records why `unknown` and `?` are absent — Emma refused them
  when they were added unasked: *"I didn't tell you to do that. I didn't tell you to
  avoid the NN people."*
* `scripts/build-relationship-label-preview.py` — **wide**: adds `unknown`, `?`, `ukjent`,
  `onbekend`, `namn okänt`, `(no name)`, punctuation-only forms. This is the set that
  shipped in the 39,299-edit placeholder batch.
* `scripts/walk-structural-merge.py` — a copy of the wide set.

So this reports **which set each match belongs to**, in the `vocabulary` column:
`narrow` for the forms all three agree on, `wide` for the ones only the preview and the
walk treat as markers. Deciding whether `wide` is right is Emma's call and the counts
are what it should be decided on.

Writes `reports/marker-labels.csv` (every instance) and prints the analysis.

    PYTHONPATH=src python scripts/build-marker-label-census.py
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
STORE = REPO / "wikidata" / "items"
OUT = REPO / "reports" / "marker-labels.csv"

csv.field_size_limit(10 ** 7)

#: The forms all three vocabularies agree on. `scripts/labels.py` is the authority
#: for this set and it is narrow on purpose.
NARROW = {
    "private", "<private>",
    "nn", "n n", "n.n.", "n. n.", "n.n", "n-n",
}

#: Forms only the preview and the walk treat as markers. Emma has never ruled on
#: these; they shipped in the 39,299-edit placeholder batch, which is a reason to
#: put the counts in front of her rather than to keep them or drop them quietly.
WIDE = {
    "n", "?", "??", "???", "????", "_", "-", "--", ".", "*", "**", "***", "'",
    "unknown", "(no name)", "no name", "not known", "namn okänt", "ukjent",
    "ukj.", "onbekend",
}

VOCABULARY = {form: "narrow" for form in NARROW}
VOCABULARY.update({form: "wide" for form in WIDE})

#: Forms made only of punctuation, which mean "absent" **at the end of a label or
#: as the whole of it, and nowhere else**.
#:
#: This is a false positive the first run of this census produced and it would have
#: corrupted real labels: `George Clark, II - farmer` and
#: `Birch, Charles Weldon (1821 - 1894), Naturalist` are hyphenated prose, not
#: people with a missing name, and stripping the `-` mangles both. 289 rows over
#: 112 Wikidata items.
#:
#: `Toeloes .` and `Siti Komara .` are the shape that is real — an Indonesian name
#: with no surname, the dot standing in for one — and those sit at the tail. So the
#: rule is positional rather than a shorter list: punctuation is a marker where a
#: name would end, never mid-label.
PUNCTUATION_ONLY = {"-", "--", ".", "_", "*", "**", "***", "'",
                    "?", "??", "???", "????"}

#: …**unless it is parenthesised**, which is a stand-in wherever it sits.
#:
#: `Nechama (?) Heller` and `Theodechildis (Unknown)` are a real given name with a
#: bracketed hole where a patronymic or surname goes; `George Clark, II - farmer` is
#: prose. Brackets are the difference, and they are in the data rather than inferred
#: — which is why this is a second rule and not a shorter `PUNCTUATION_ONLY`.
def _parenthesised(token: str) -> bool:
    return token.startswith("(") and token.endswith(")") and len(token) > 2

#: Languages worth reporting on the Wikidata side. `mul` is where a marker is
#: allowed to live, so it is included precisely so the report can show that the
#: marker is in the *right* place for those rows rather than omitting them.
WD_LANGUAGES = ("mul", "en", "nl", "de", "da", "sv", "nb", "es", "pt", "it", "ca",
                "cy", "be", "pl", "ru", "uk", "ja", "zh")


def _relationship_phrases() -> set[tuple[str, str]]:
    """`(relationship word, "of" word)` pairs, taken from the repo's own tables.

    **Nothing is invented here and that is the whole point.** The second class of
    marker-bearing label is the one that carries no marker at all — `Maka till
    Brynjolf Brandsson`, `Wife of Moshe Lazers` — a *description* sitting in the
    name slot. Writing a list of relationship words from memory is how a
    vocabulary ends up being a guess, so this reads `WORDS` out of
    `scripts/build-nn-label-batch.py`: the ten-language table this project uses to
    **generate** exactly these phrases. A label that already reads like something
    we would emit is a description by construction.

    The pair is required adjacent — the word and then the language's *of* — which
    keeps `hija de` apart from `Rodrigo de Vivar`, and keeps `datter` (a patronymic
    suffix, never a standalone token) out of it entirely.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "nn_label_batch", REPO / "scripts" / "build-nn-label-batch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    skip = {"eller", "o", "ou", "of", "och"}
    pairs: set[tuple[str, str]] = set()
    for table in module.WORDS.values():
        of = str(table.get("of") or "").casefold()
        if not of:
            continue
        for key, value in table.items():
            if key == "of":
                continue
            forms = value.values() if isinstance(value, dict) else [value]
            for form in forms:
                for token in str(form).casefold().split():
                    if token and token not in skip:
                        pairs.add((token, of))
    return pairs


RELATIONSHIP_PHRASES = _relationship_phrases()


def description_in(label: str) -> tuple[str, str] | None:
    """`(phrase, remainder)` when the label reads as a relationship description."""
    tokens = (label or "").split()
    folded = [t.strip(",;:()[]").casefold() for t in tokens]
    for i in range(len(folded) - 1):
        if (folded[i], folded[i + 1]) in RELATIONSHIP_PHRASES:
            phrase = folded[i] + " " + folded[i + 1]
            return (phrase, " ".join(tokens[:i] + tokens[i + 2:]))
    return None


def _classify(label: str):
    """`(kind, marker, vocabulary, position, remainder)`, marker first.

    A marker beats a description when both are present: `NN wife of Aun` reports as
    the marker it leads with, and its remainder — `wife of Aun` — is what shows the
    description is there as well.
    """
    hit = marker_in(label)
    if hit:
        marker, position, remainder = hit
        return ("marker", marker, VOCABULARY[marker], position, remainder)
    described = description_in(label)
    if described:
        phrase, remainder = described
        return ("description", phrase, "relationship", "inside", remainder)
    return None


def marker_in(label: str) -> tuple[str, str, str] | None:
    """`(marker, position, remainder)` for a marker-bearing label, else `None`.

    Position is `whole`, `head`, `tail` or `inside`. The remainder is the label
    with the matched token removed, which is what says whether real data survives:
    `NN Hildesheim` leaves `Hildesheim`, and `NN` leaves nothing.
    """
    text = (label or "").strip()
    if not text:
        return None
    tokens = text.split()
    folded = [t.strip(",;:()[]").casefold() for t in tokens]

    # A two-word form like `n n` or `no name` has to be matched before the
    # single tokens, or `n n` reports as two separate `n` hits.
    for size in (3, 2):
        for i in range(len(folded) - size + 1):
            joined = " ".join(folded[i:i + size])
            if joined in VOCABULARY:
                position = _position(i, size, len(tokens))
                if (joined in PUNCTUATION_ONLY
                        and position not in ("whole", "tail")
                        and not any(_parenthesised(t) for t in tokens[i:i + size])):
                    continue
                rest = tokens[:i] + tokens[i + size:]
                return (joined, position, " ".join(rest))
    for i, token in enumerate(folded):
        if token in VOCABULARY:
            position = _position(i, 1, len(tokens))
            if (token in PUNCTUATION_ONLY
                    and position not in ("whole", "tail")
                    and not _parenthesised(tokens[i])):
                continue
            rest = tokens[:i] + tokens[i + 1:]
            return (token, position, " ".join(rest))
    return None


def _position(index: int, size: int, total: int) -> str:
    if size == total:
        return "whole"
    if index == 0:
        return "head"
    if index + size == total:
        return "tail"
    return "inside"


def geni_side(writer) -> Counter:
    tally = Counter()
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            for slot in ("label_en", "label_mul", "other_script_names"):
                for label in (row.get(slot) or "").split(" | "):
                    found = _classify(label)
                    if not found:
                        continue
                    kind, marker, vocab, position, remainder = found
                    tally[(kind, position, vocab)] += 1
                    writer.writerow({
                        "store": "geni",
                        "geni_id": row["geni_id"],
                        "qid": row.get("qid", ""),
                        "language": slot,
                        "label": label,
                        "kind": kind,
                        "marker": marker,
                        "vocabulary": vocab,
                        "position": position,
                        "remainder": remainder,
                    })
    return tally


def wikidata_side(writer) -> Counter:
    tally = Counter()
    shards = wikistore.shards(STORE)
    print(f"scanning {len(shards):,} shards of the Wikidata store")
    for n, shard in enumerate(shards, start=1):
        if n % 250 == 0:
            print(f"  {n:,} of {len(shards):,} shards")
        for entity in wikistore.read_shard(shard):
            labels = entity.get("labels") or {}
            if not labels:
                continue
            geni_ids = wikistore.geni_ids_of(entity)
            for language in WD_LANGUAGES:
                value = labels.get(language)
                value = value.get("value") if isinstance(value, dict) else value
                found = _classify(value or "")
                if not found:
                    continue
                kind, marker, vocab, position, remainder = found
                tally[(kind, position, vocab)] += 1
                writer.writerow({
                    "store": "wikidata",
                    "geni_id": " | ".join(geni_ids),
                    "qid": entity.get("id", ""),
                    "language": language,
                    "label": value,
                    "kind": kind,
                    "marker": marker,
                    "vocabulary": vocab,
                    "position": position,
                    "remainder": remainder,
                })
    return tally


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-wikidata", action="store_true",
                    help="Geni side only; the store scan is the slow half")
    args = ap.parse_args()

    fields = ["store", "geni_id", "qid", "language", "label", "kind", "marker",
              "vocabulary", "position", "remainder"]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        geni = geni_side(writer)
        print(f"geni side: {sum(geni.values()):,} marker-bearing labels")
        wd = Counter() if args.skip_wikidata else wikidata_side(writer)
        if not args.skip_wikidata:
            print(f"wikidata side: {sum(wd.values()):,} marker-bearing labels")

    print(f"\nwrote {OUT}")
    for name, tally in (("geni", geni), ("wikidata", wd)):
        if not tally:
            continue
        print(f"\n{name} — by kind, position and vocabulary:")
        for (kind, position, vocab), count in tally.most_common():
            print(f"  {count:>8,}  {kind:<11} {position:<7} {vocab}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
