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

**CJK descriptions ARE detected, since Emma ruled on 2026-08-17.** This file shipped
with them deliberately excluded — `陳母` is *Chen's mother*, and reading a trailing `母`
as a relationship marker is a claim about Chinese naming rather than a lookup. Measuring
the population and putting it to her got *"Descriptions, same as English"*: 室 2,565 ·
氏 1,613 · 娘 617 · 某 311 · 妻 210 · 母 100, about **5,400 people**, more than the 1,222
English ones. See `CJK_RELATIONSHIP`.

Every row carries `kind` — `marker` or `description` — so the two never merge in the
output. A marker wins when both are present: `NN wife of Aun` is reported as its marker
with `wife of Aun` as the remainder, which shows the description is there too.

### The vocabulary was three sets that disagreed, and Emma settled it

Her queue item says they *"should end up as one"*. They could not be merged silently,
because they were built to different rulings — and on 2026-08-17, asked directly, she
chose **words yes, punctuation no**. The three sets as they stood:

* `scripts/labels.py` — deliberately **narrow**: `private`, `<private>`, and the `NN`
  spellings. Its docstring records why `unknown` and `?` are absent — Emma refused them
  when they were added unasked: *"I didn't tell you to do that. I didn't tell you to
  avoid the NN people."*
* `scripts/build-relationship-label-preview.py` — **wide**: adds `unknown`, `?`, `ukjent`,
  `onbekend`, `namn okänt`, `(no name)`, punctuation-only forms. This is the set that
  shipped in the 39,299-edit placeholder batch.
* `scripts/walk-structural-merge.py` — a copy of the wide set.

The `vocabulary` column says which class matched — `narrow`, `word`, `punctuation`,
`letter`, or for a description `relationship`, `cjk`, `honorific` — so her ruling stays
legible in the output rather than being folded away into a boolean.

**Folding the other three onto this vocabulary is the remaining half of her item.**
The preview's set still contains the punctuation forms her ruling removes, so doing it
changes the 39,299-edit placeholder batch and has to re-run it.

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

#: Words meaning *unknown*. **Emma ruled on these on 2026-08-17: words yes,
#: punctuation no.** Asked whether `unknown` / `?` / `ukjent` / `*` are markers the
#: way `NN` and `Private` are, she chose *"Words yes, punctuation no"* — somebody
#: who typed a word meaning "I don't know" is making the same statement `NN` makes,
#: and bare punctuation is typography we would be guessing at.
#:
#: **Half of this list was found by measurement, not memory.** Ranking every label
#: string by how many *different* people carry it — a real name repeats a little, a
#: placeholder repeats hundreds of times — surfaced `Без име` (Bulgarian, *without
#: name*, 52 people) sitting above most genuine names. Each entry below is followed
#: by the number of people carrying it in the corpus, so the list is auditable
#: rather than aspirational.
WORDS_MEANING_UNKNOWN = {
    "unknown",        # 2,127
    "ukjent",         #   188 Norwegian
    "no name",        #    92
    "без име",        #    52 Bulgarian / Macedonian
    "ukendt",         #    18 Danish
    "okänd",          #    17 Swedish
    "not known",      #    15
    "desconocida",    #    13 Spanish
    "desconocido",
    "inconnu",        #     9 French
    "inconnue",       #     4
    "неизвестна",     #     6 Russian
    "неизвестно",
    "unbekannt",      #     6 German
    "ignota",         #     3 Italian
    "ignoto",
    "noname",         #     3
    "佚名",            #     3 Chinese
    "onbekend",       #     1 Dutch
    "namn okänt",     #     — Swedish, kept from the earlier set
    "(no name)",
    "ukj.",           #       Norwegian abbreviation of ukjent
    "未詳",            #     1 Japanese, "details unknown"
    "無名",            #       Japanese / Chinese, "nameless"
}

#: **Words that look like markers and are not.** Each cost is measured, and each
#: would have erased real names:
#:
#: * `anon` — **89 people**, and `Anon Olsen Syverstad` / `Anon Mathisen Lund` are
#:   Norwegians. `Anon` is a genuine Norwegian given name, not an abbreviation of
#:   *anonymous*.
#: * `子` — **2,091 people**. It ends a great many ordinary Japanese given names:
#:   `多恵子`, `英子`, `陳子玉`. Nothing about it means *unnamed*.
#:
#: Kept as an explicit set rather than simply omitted, so that adding either one
#: later is a decision somebody has to argue with rather than an oversight.
NOT_MARKERS = {"anon", "子"}

VOCABULARY = {form: "narrow" for form in NARROW}
VOCABULARY.update({form: "word" for form in WORDS_MEANING_UNKNOWN})

#: Punctuation, which is a marker **only when it is the whole label** — Emma's
#: ruling of 2026-08-17, *"words yes, punctuation no"*.
#:
#: The first run of this census treated bare punctuation as a marker wherever it
#: sat, and would have corrupted real labels: `George Clark, II - farmer` and
#: `Birch, Charles Weldon (1821 - 1894), Naturalist` are hyphenated prose, 289 rows
#: over 112 Wikidata items. Her ruling goes further than that fix and leaves
#: `Toeloes .` and `Nechama (?) Heller` alone as well — 3,102 `?`-at-tail rows that
#: an earlier pass would have rewritten.
#:
#: A label that is *nothing but* punctuation still has no name in it, and
#: `derive-labels.ABSENT` has always read it that way.
PUNCTUATION_ONLY = {"-", "--", ".", "_", "*", "**", "***", "'",
                    "?", "??", "???", "????"}

#: `n` alone, which is a marker at the **start** of a label and not inside one.
#:
#: `N Пузына`, `N Lozinska`, `N Naruszewicz` are a placeholder given name in front
#: of a real surname — 917 of them. `Gunteroda N` and `Laura N` are 205 more where
#: it trails, and a trailing or interior single letter is a **middle initial**,
#: which is the mistake this repo has already made once at scale: `f9b9f86` records
#: 283 middle initials nearly invented out of a regnal ordinal.
#:
#: Neither a word nor punctuation, so Emma's ruling does not reach it. Decided here
#: rather than put to her, per `CLAUDE.md`: a judgement call is mine to take and
#: record.
SINGLE_LETTER = {"n"}

#: CJK relationship suffixes. **Emma's ruling, 2026-08-17: descriptions, the same as
#: the English ones.** Shown the measurement — 室 2,565 · 氏 1,613 · 娘 617 · 某 311 ·
#: 妻 210 · 母 100, about 5,400 people, more than the 1,222 English descriptions —
#: she chose to treat them as the CJK arm of the description class.
#:
#: What they mean, since a bare character is unreadable to most readers of this file:
#:
#: * `室` — consort. `正室` principal wife, `側室` concubine. `信秀正室 織田` is
#:   *principal wife of Nobuhide, of the Oda*.
#: * `氏` — the clan-only woman. `謝氏` is *the Xie-clan woman*, a real surname with
#:   the given name never recorded.
#: * `娘` — daughter of. `織田敏信娘`.
#: * `某` — a certain unnamed one. `古河某妻` is *wife of a certain Kogawa*.
#: * `妻` — wife of. `母` — mother of.
#:
#: `子` is **not** here and must not be added: it ends ordinary given names.
CJK_RELATIONSHIP = ("正室", "側室", "室", "氏", "娘", "某", "妻", "母")

#: **`氏` attaches to HER OWN surname; the rest attach to the relative.** This is the
#: distinction the first version missed, and `盧氏 Chan` is what exposed it: the
#: remainder came out `Chan` and threw away `盧`, the woman's actual clan.
#:
#: * `謝氏` is *the Xie-clan woman* — `謝` is **her** surname and must survive, so the
#:   suffix comes off its own token and everything else stays: `盧氏 Chan` → `盧 Chan`.
#: * `信秀正室 織田` is *principal wife of Nobuhide, of the Oda* — `信秀` is her
#:   **husband's** given name, and carrying it into her `mul` would label her with
#:   somebody else's name. The whole token goes: → `織田`.
#:
#: Getting this wrong is silent in both directions — one drops a real surname, the
#: other adopts a stranger's — which is why it is two lists rather than a flag.
CLAN_SUFFIX = ("氏",)

#: An honorific leading a label, which makes the label a description of somebody
#: else. `Mrs. Isaak Guggenheim` is a woman named by her husband; 249 of them.
#: `Wife` and `Daughter` are here as well as in the relationship table, because
#: `Daughter Charif` and `Daughter II Probus` carry no *of* for the pair rule to
#: find.
HONORIFICS = {"mrs.", "mrs", "miss", "frau", "fru", "madame", "señora", "sra.",
              "hustru", "wife", "daughter", "widow"}


#: A parenthesised stand-in — kept as a concept because the brackets are in the
#: data, but no longer a marker: her ruling leaves `Nechama (?) Heller` alone.
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
        vocab = VOCABULARY.get(marker)
        if vocab is None:
            vocab = "punctuation" if marker in PUNCTUATION_ONLY else "letter"
        return ("marker", marker, vocab, position, remainder)
    described = description_in(label)
    if described:
        phrase, remainder = described
        return ("description", phrase, "relationship", "inside", remainder)
    cjk = cjk_relationship_in(label)
    if cjk:
        suffix, remainder = cjk
        return ("description", suffix, "cjk", "tail", remainder)
    honorific = honorific_in(label)
    if honorific:
        head, remainder = honorific
        return ("description", head, "honorific", "head", remainder)
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

    whole = " ".join(folded)
    if whole in PUNCTUATION_ONLY:
        # Punctuation is a marker only as the whole label. Her ruling.
        return (whole, "whole", "")

    # A two-word form like `n n` or `no name` has to be matched before the single
    # tokens, or `n n` reports as two separate `n` hits.
    for size in (3, 2):
        for i in range(len(folded) - size + 1):
            joined = " ".join(folded[i:i + size])
            if joined in VOCABULARY and joined not in NOT_MARKERS:
                rest = tokens[:i] + tokens[i + size:]
                return (joined, _position(i, size, len(tokens)), " ".join(rest))
    for i, token in enumerate(folded):
        if token in NOT_MARKERS:
            continue
        position = _position(i, 1, len(tokens))
        if token in SINGLE_LETTER:
            if position not in ("whole", "head"):
                continue
        elif token not in VOCABULARY:
            continue
        rest = tokens[:i] + tokens[i + 1:]
        return (token, position, " ".join(rest))
    return None


def cjk_relationship_in(label: str) -> tuple[str, str] | None:
    """`(suffix, remainder)` when a CJK label names somebody by relationship.

    The remainder drops whichever token carries the suffix, which usually leaves
    the surname standing on its own — `信秀正室 織田` leaves `織田`. When the label
    is a single token the suffix comes off it instead, so `謝氏` leaves `謝`, which
    is the real surname and the thing `CLAUDE.md` insists is not thrown away.
    """
    tokens = (label or "").split()
    if not tokens:
        return None
    for suffix in CJK_RELATIONSHIP:
        hits = [t for t in tokens if suffix in t]
        if not hits:
            continue
        rest = [t for t in tokens if suffix not in t]
        # **Every suffix comes off the carrying token, not just the matched one.**
        # `古河某妻` is *wife of a certain Kogawa* and carries two; stripping only
        # `某` left `古河妻`, which is neither a name nor a description.
        residue = hits[0]
        for other in CJK_RELATIONSHIP:
            residue = residue.replace(other, "")
        residue = residue.strip()
        if suffix in CLAN_SUFFIX:
            # Her own surname is in the carrying token. Keep it, in place.
            rest = [residue if suffix in t else t for t in tokens]
        elif not rest:
            # Nothing else to fall back on, so the residue is all there is — and
            # for a relative-suffix that residue is the relative, which is why this
            # is the last resort rather than the rule.
            rest = [residue]
        return (suffix, " ".join(t for t in rest if t))
    return None


def honorific_in(label: str) -> tuple[str, str] | None:
    """`(honorific, remainder)` when a label leads with one.

    `Mrs. Isaak Guggenheim` names a woman by her husband. Only the leading
    position counts: `Anna Miss` is not a description of anybody.
    """
    tokens = (label or "").split()
    if len(tokens) < 2:
        return None
    head = tokens[0].strip(",;:()[]").casefold()
    if head in HONORIFICS:
        return (head, " ".join(tokens[1:]))
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
