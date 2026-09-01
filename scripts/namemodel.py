"""Split a Norwegian name into the properties `name modelling.txt` asks for.

Emma, 2026-08-24, on the Garborg batches: *"we should be modelling the names
properly, which he didn't do."* The batches carried labels and no `P735`, `P734` or
`P5056` at all.

**Her model, from `name modelling.txt`, not invented here:**

    P735  given name            first token, + P1545 ordinal 1
                                                + P7452 -> Q3409033 usual forename
    P735  given name            later tokens, + P1545 ordinal n
                                              + P3831 -> Q245025 middle name
    P5056 patronym or matronym  a -sen/-son/-datter token, its own property
                                and NOT a P735 with a qualifier
    P734  family name           the last token

`CLAUDE.md`: *"A middle name is a given name after the first that is NOT a
patronymic."* So the order of the tests matters — patronymic first, then position.

**Both fields, always — and that means READING the fields.** Until 2026-08-24 this
module took `label_en`, a rendered display string, and guessed by whitespace position.
Emma caught it: *"I thought we were resolving name objects but now we're determining
which name field to use as a source of the label?"* The GEDCOM fields are in
`reports/display-names.csv` — `givn`, `surn`, `nick`, `marnm` — and the label is a
separate output that happens to describe the same person.

What positional parsing got wrong, on four real people:

* `surn` is **recorded**; the parser inferred it as "the last token unless it looks
  patronymic". Agreeing by luck is not the same as reading it.
* `Stine "Stena" Eivindsdatter` → *Stena* came out a second given name carrying
  `P1545` *series ordinal* 2 and `P3831` → `Q245025` *middle name*. It is a nickname.
* `marnm` was never read at all, so Stena's *Jacobson* and Inger Marie's *Ronneberg*
  did not exist to the model.

**Emma's rulings, 2026-08-24.** A quoted token inside `givn` becomes `P1449`
*nickname*. A `_MARNM` becomes a **second** `P734` *family name*, emitted only where it
differs from `surn` and where `surn` is actually populated.

**Sex screens the ROLE, not the statement.** She first said sex was not a screen, then
corrected on seeing a man carrying `Q28418670` *married name*: *"ontologically married
name on a man means more like adopted surname. So men's 'married names' should not have
the role of married name."* So a man still gets the second `P734`; it simply carries no
`P3831` role. Not `Q118383793` *adoptive name* either — in this material the second
surname is usually a **farm name** taken by residence, and `Q141169072` is the case:
*Ådne Olsen Grøtheim* became *Ådne Olsen Garborg* by moving to the Garborg farm.

**CJK stays out of scope and is a known hazard.** `CLAUDE.md` records `SURN` holding a
place name (`陳郡陽夏`) while `_MARNM` held the real clan name. Reading `surn` as a
surname is right for this material and is not established corpus-wide.

**Nothing is guessed.** A token's item comes from `reports/name-item-plan.csv`, which
carries `existing_qid` where Wikidata already has one and `create` where it does not.
A token the plan calls `AMBIGUOUS` is **emitted as a note and never as a statement** —
that is the `Maria` case, where nine items exist and only the person's sex separates
the two that matter.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items. Written out so a reader never meets
#: a bare Q-number.
GIVEN_NAME = "P735"          # given name
FAMILY_NAME = "P734"         # family name
PATRONYM = "P5056"           # patronym or matronym
SERIES_ORDINAL = "P1545"     # series ordinal
PREFERRED_REASON = "P7452"   # reason for preferred rank
USUAL_FORENAME = "Q3409033"  # usual forename
HAS_ROLE = "P3831"           # object of statement has role
MIDDLE_NAME = "Q245025"      # middle name
PATRONYMIC_CLASS = "Q110874"  # patronymic
NICKNAME = "P1449"           # nickname
BIRTH_NAME_ROLE = "Q2507958"   # birth name
MARRIED_NAME_ROLE = "Q28418670"  # married name

#: `-sen`, `-son`, `-sson`, `-datter`, `-sdatter`. Emma, on the Norwegian material:
#: *"The daughter and son would be the same thing"* — one category, not two.
#: **`dotter` is the Swedish form and was missing.** `datter` is Norwegian and Danish;
#: `-dotter` is Swedish and means the same thing. Leaving it out classified **60,085 people**
#: as carrying a family name -- `Johansdotter` 5,612 bearers, `Andersdotter` 5,472,
#: `Olofsdotter` 3,157, `Nilsdotter` 2,868 -- when every one is a patronymic.
#:
#: The disagreement was internal: `scripts/build-name-item-batch.py`'s `RELIABLE_PATRONYMIC`
#: has listed `dotter` and `sdotter` all along, so the plan builder and the classifier have
#: been reading the same token two different ways. Found because `PATRONYMIC_PARTS` below
#: included it and this did not, and the father test disagreed with itself on
#: `Jakobsdotter`.
PATRONYMIC = re.compile(r".+(sen|son|sson|datter|sdatter|dotter)$", re.I)

#: A token wholly inside brackets, as Geni writes an alternative or a house:
#: `Turesson (Bielke)`, `Weirman (Weyerman)`, `Levine (?)`.
PAREN = re.compile(r"^\((.+)\)$")

#: **Particles and honorifics go into the LABEL and never become items.** Emma, 2026-08-26:
#: *"These should be parts of the mul labels because they are integral parts of what the
#: people are called."* The nine bracketed ones are the whole bracketed population measured in
#: `reports/paren-tokens.md`; the unbracketed forms are far commoner -- bare `de` occurs
#: **125,328** times and bare `von` 60,951 -- and until now every one of them became a `P734`
#: *family name* lookup of its own.
PARTICLES = {
    "de", "d.", "du", "des", "del", "della", "di", "da", "das", "dos", "van", "von",
    "vander", "le", "la", "el", "af", "av", "ap", "ben", "ibn", "bin", "mac", "mc",
    "st.", "san", "santa", "dom", "don",
}

#: **Words meaning the name is not known.** They join `Private`/`NN`/`Ukjent`, which
#: `scripts/labels.py` owns -- `CLAUDE.md` § *`NN` is PRESERVED in `mul`*. Emma, 2026-08-26,
#: shown `(anonyma)`, `(incognita)` and `(?)`: *"Treat as NN markers."*
#:
#: **`ben` is in `PARTICLES`, not here.** It is the Samaritan patronymic particle --
#: `Abisha III ben Phinhas` -- so it belongs in the label and must never become a `P734`
#: *family name* item of its own, which is what it used to do.
UNKNOWN_MARKERS = {
    "?", "??", "???", "anonyma", "anonymus", "anonym", "incognita", "incognito",
    "okänd", "ukjent", "ukendt", "unknown", "n.n.", "nn", "no name", "namn okänt",
}

#: **A stillborn child is DESCRIBED, not named, and the description is not a name.**
#: Emma, 2026-08-30, on `Q141224141`: *"please stop trying to assign names to this person
#: who does not in fact have any names at all."* Geni records him as
#: `En dödfödd son Bielke` -- Swedish for *a stillborn son* -- and the batch emitted
#: `P735` *given name* `En`, the indefinite article, carrying `P7452` *usual forename*.
#:
#: **This is stronger than `UNKNOWN_MARKERS` and that is the point.** A marker suppresses
#: its own token; a description marker suppresses the WHOLE given-name field, because the
#: words around it -- `En`, `son`, `barn`, `gossebarn` -- are the rest of one phrase rather
#: than names that happen to sit nearby. Her sentence is the authority for going that far:
#: the person has no names at all.
#:
#: **Measured over `reports/display-names.csv`, 2026-08-31: 475 people.** `dødfød` 212,
#: `dødfødt` 208, `stillborn` 135, `dödfödd` 112, `dödfött` 19, `dødfødte` 1, `dödfödda` 1
#: (a `GIVN` can hold more than one form, so these sum past 475). The surname is untouched
#: and still becomes a `P734` *family name*, which is why `Bielke` survives.
#:
#: **The reading taken rather than asked** (`CLAUDE.md` § *Working the queue: GUESS*): a real
#: given name recorded beside a stillborn word would be dropped with it. It would be
#: falsified by a `GIVN` such as `Anna dödfödd`, and there is none -- the co-occurring tokens
#: measured are all structural (`son` 43, `barn` 17, `gossebarn` 15, `daughter` 14).
DESCRIPTION_MARKERS = {
    "dødfød", "dødfødt", "dødfødte", "dødfodt",
    "dödfödd", "dödfött", "dödfödda", "dodfodd",
    "stillborn", "stillbirth",
}


def _bare_word(token: str) -> str:
    """The token stripped of the punctuation Geni wraps these in.

    `(--stillborn--)` occurs 11 times and `(dødfødt)` 6, so a plain casefold misses both.
    """
    return re.sub(r"[^0-9A-Za-zÀ-ÿ]+", "", token).casefold()


def is_description(givn: str) -> bool:
    """True when this `GIVN` field is a description of a stillbirth rather than a name."""
    return any(_bare_word(t) in DESCRIPTION_MARKERS
               for t in re.split(r"\s+", (givn or "").strip()) if t)


def name_shape(token):
    """`(bare_token, usage_or_None)` -- brackets stripped, particles and markers named.

    Emma's rulings of 2026-08-26, `CLAUDE.md` § *A parenthesised token in `SURN`/`_MARNM` is
    THREE different things*. A `usage` of `None` means "an ordinary name token, carry on";
    `particle` and `unknown` are terminal and never reach the name plan.

    The brackets are stripped whether or not the token is a particle, because
    `(de) Worms` and `de Worms` are the same name written twice.
    """
    m = PAREN.match(token)
    bare = m.group(1) if m else token
    low = bare.casefold()
    if low in UNKNOWN_MARKERS:
        return bare, "unknown"
    if low in PARTICLES:
        return bare, "particle"
    return bare, None


def load_plan(path: Path | None = None) -> dict:
    """(token, usage) -> (existing_qid or '', action).

    `reports/ambiguous-names-resolved.tsv` is overlaid on top, where it has an answer.
    Those are the tokens the plan marks AMBIGUOUS and therefore refuses to emit;
    `scripts/resolve-ambiguous-names.py` settles them by the bearer's sex (Emma's rule)
    and then by which candidate's `mul` label is the token itself, which is what
    separates the Russian `Мартин` from the Latin `Martin`. A token it cannot settle
    stays AMBIGUOUS and is still not emitted.
    """
    path = path or ROOT / "reports" / "name-item-plan.csv"
    out = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[(row["token"], row["usage"])] = (
                (row.get("existing_qid") or "").strip(),
                (row.get("action") or "").strip(),
            )

    resolved = ROOT / "reports" / "ambiguous-names-resolved.tsv"
    if resolved.exists():
        with open(resolved, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                qid = (row.get("qid") or "").strip()
                if qid:
                    out[(row["token"], "given")] = (qid, "link (ambiguity resolved)")

    # **Does WIKIDATA have this name item -- not, does one of OUR people already link to one.**
    #
    # Emma, 2026-08-29 on Tunheim: *"some of these names got merged in with an existing item.
    # I'm extremely confused how this happened, and it seems to me to indicate maybe you're not
    # actually checking the existence of the names correctly in our data."* She was right, and
    # it is measurable: of the **10 name items she has created**, `Tunheim`, `Ronneberg`, `Bø`,
    # `Heigre` and `Nyvold` were all merged away by other editors as duplicates. The five that
    # stood are patronymics and a farm name -- names that genuinely did not exist.
    #
    # The plan's `existing_qid` comes from `measure-name-resolution.py`, whose universe is
    # `reports/name-items.csv`: name items **some person in our own store already points at**,
    # 132,569 of them. `Q36927172` *Tunheim* is in our store and nobody in our corpus links to
    # it, so it was invisible and the plan said `create`.
    #
    # `out/wikidata/name-items-in-store.tsv.gz` is the other question asked directly --
    # **823,907** name items, every one on disk, built by `scripts/extract-name-items.py`.
    # Joined against the plan it turns **5,212 of 14,351 planned creations (36%) into links**.
    #
    # Kind is never collapsed, per `CLAUDE.md` § *One name item per USAGE*: a `Q202444` given
    # name sharing a label does not make a family-name creation a duplicate. Labels fold on
    # case only, per the `María`/`Mária`/`Marià` rule.
    # Only entries with no QID yet: a hand resolution and Emma's ambiguity rulings still win.
    out.update(_store_name_items({k for k, (qid, _a) in out.items() if not qid}))
    return out


#: `P31` value -> the usage a person links to it with, for the store lookup below.
_NAME_ITEM_CLASS = {"Q101352": "family", "Q202444": "given", "Q12308941": "given",
                    "Q11879590": "given", "Q3409032": "given", "Q110874": "patronymic"}


_STORE_INDEX = None


def store_name_item(token, usage):
    """The QID of a name item Wikidata already has for `(token, usage)`, or `''`.

    **This must answer ANY token, not only one the plan holds.** The first version filtered to
    plan entries and `Ronneberg` walked straight past it -- it is not in
    `reports/name-item-plan.csv` at all, so `load_plan` returned nothing and the generator
    created a duplicate of `Q37504456` for the second time. Emma had already created it once
    and another editor had already merged it away.

    Kind is never collapsed (`CLAUDE.md` § *One name item per USAGE*) and labels fold on case
    only (the `María`/`Mária`/`Marià` rule).
    """
    global _STORE_INDEX
    if _STORE_INDEX is None:
        _STORE_INDEX = _load_store_index()
    return _STORE_INDEX.get((token.casefold(), usage), "")


def _load_store_index():
    """`{(folded label, kind): qid}` — name items Emma has CREATED, then the local store.

    **Her own creations come first, and leaving them out cost eleven duplicate items.** The
    store is the offline Wikidata download, so an item created *today* is not in it, and the
    Garborg ledger tracks people (keyed on `P2600`, which a name item does not have). A token
    created in one run was therefore invisible to the next, and `CREATE` always mints a new
    item rather than checking — so running the same regenerated file three times made three
    `Jonsdatter`s. Measured over her 581 creations: 29 name items, 18 distinct labels, **10
    labels created more than once**, all eleven duplicates merged away by another editor.

    Not only patronymics — `Gennäs`, `Morlanda` and `Sør-Reime` are family names.

    `scripts/refresh-created-name-items.py` writes the file and follows redirects, so a merged
    duplicate resolves to its survivor and the survivor is what a future run links to.
    """
    index = {}
    created = ROOT / "reports" / "created-name-items.tsv"
    if created.exists():
        with open(created, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if row["label"] and row["qid"]:
                    index[(row["label"].casefold(), row["kind"])] = row["qid"]
    else:
        print("WARNING: reports/created-name-items.tsv missing -- the generator cannot see "
              "name items already created and will propose them again. "
              "Run scripts/refresh-created-name-items.py", file=sys.stderr)

    import gzip
    path = ROOT / "out" / "wikidata" / "name-items-in-store.tsv.gz"
    if not path.exists():
        print(f"WARNING: {path.name} missing -- the name plan cannot see the name items "
              f"already on disk and will propose duplicates. "
              f"Run scripts/extract-name-items.py", file=sys.stderr)
        return index          # her creations still apply; do not discard them
    # `setdefault` below, so a label she has already created is never overwritten by the
    # store's answer for the same label.
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 4:
                continue
            qid, kinds, _p31, labels = parts
            for kind in kinds.split("|"):
                for label in labels.split("|"):
                    index.setdefault((label.casefold(), kind), qid)
    return index


def _store_name_items(planned):
    """`{(token, usage): (qid, action)}` for plan entries the store can already satisfy."""
    return {(t, u): (store_name_item(t, u), "link (already on Wikidata)")
            for (t, u) in planned if store_name_item(t, u)}


#: A token Geni wrapped in quotes inside `GIVN` — `Stine "Stena" Eivindsdatter`.
#:
#: **The apostrophe branch is load-bearing and was nearly deleted.** `Jean d'O Seigneur d'O`
#: matched `'O Seigneur d'` and produced a `P1449` *nickname* of `O Seigneur d`, which looked
#: like grounds for dropping `'` as a delimiter altogether. Measured first, over
#: `reports/display-names.csv`: **963 apostrophe-delimited spans**, and most are genuine —
#: `Illugi svarte i Gilsbakki 'svarti'`, `Ivan II Ivanovich 'the Fair'`,
#: `Hanna Jørgine 'Gina'`, `Philip I 'The handsome'`. Geni really does use single quotes for
#: bynames, so removing the branch would have destroyed 900-odd real nicknames to fix a handful
#: of French names.
#:
#: **Emma, 2026-08-29, named the actual discriminator:** *"d' can be an escaped substring lol"* —
#: an apostrophe bound into a word is elision, not a delimiter. So a quoted span now requires:
#:
#: * the opening `'` at a word boundary — start of string or after whitespace. This rejects
#:   `d'O`, `O'Brien`, `l'Enfant`.
#: * the closing `'` preceded by a non-space and followed by whitespace or end. This rejects
#:   `Sultan 'Omar 'Ali Saifuddin`, where the transliterated ayn opens twice and closes never,
#:   and the span `'Omar '` is an artefact of pairing two openers.
#:
#: The double-quote and parenthesis branches are unchanged: they are unambiguous and carry the
#: other 23,005 matches.
QUOTED = re.compile(
    r'["“”](?P<token>[^"“”]+)["“”]'
    r"|(?<![^\s])'(?P<apos>[^'\n]*[^\s'])'(?![^\s])"
    r"|\((?P<paren>[^)]+)\)")


#: A `-sen`/`-son`/`-datter` token, split into stem and suffix.
PATRONYMIC_PARTS = re.compile(r"^(.+?)(sen|son|sson|datter|sdatter|dotter)$", re.I)


#: Spelling pairs that are the SAME Scandinavian name, applied before the skeleton is taken.
#: Each is a real variant seen in the corpus, not a general phonetic theory: `Mathias`/`Matts`,
#: `Niclas`/`Niklas`, `Christen`/`Kristen`, `Qvist`/`Kvist`, `Wilhelm`/`Vilhelm`.
#:
#: **`d`/`t` was added 2026-08-31 after measuring, not before.** It is the commonest remaining
#: alternation -- `Peder`/`Petter`, `Mads`/`Mats`, `Laurids`/`Laurits`, `Godskalk`/`Gotskalk` --
#: and it rescues **1,410** tokens wrongly classified as inherited surnames. Emma's objection was
#: that folding it would also merge `Anders` with `Antti`, which are cognates and not one name.
#: Checked: it does not. Their skeletons are `andrs` and `ant`, which the fold leaves apart, and
#: 8 of 8 sampled rescues are genuine (`Pedersdatter` of `Petter Jacobsen Falch`, `Madsdotter` of
#: `Mats Nilsen Odder`). The worry was real and the measurement retired it.
_SPELLING = (("th", "t"), ("ph", "f"), ("ch", "k"), ("ck", "k"), ("qu", "kv"),
             ("c", "k"), ("w", "v"), ("z", "s"), ("j", "i"), ("d", "t"))


def _skeleton(word: str) -> str:
    """First letter plus the consonants, with the usual Scandinavian spellings folded.

    **Why a skeleton and not the letters.** A patronymic is built from the father's given name,
    and the two are spelled apart far more often than they are spelled alike: `Nielsdatter` from
    `Nils`, `Pettersdotter` from `Peter`, `Mattsdotter` from `Mathias`, `Olsdatter` from `Ole`.
    Comparing letters calls every one of those a surname. Dropping the vowels and folding `c/k`,
    `th/t` and doubled consonants makes them agree, and leaves `Jackson` against `Badgley` as far
    apart as it was.

    **This is NOT the fuzzy matching `CLAUDE.md` forbids, and the boundary is the candidate set.**
    That rule is about *searching* for a name across a population. Here the father is already
    fixed by the tree -- exactly one person -- and the comparison only asks whether this token was
    built from that one man's name. The same boundary the zipper's name step runs on: position has
    chosen, the letters only confirm.
    """
    w = word.casefold()
    for a, b in _SPELLING:
        w = w.replace(a, b)
    out = [w[0]] if w else []
    out += [c for c in w[1:] if c not in "aeiouyáàâäåæéèêëíìîïóòôöøúùûü"]
    # collapse doubles: `petter` -> `ptr`, not `pttr`
    folded = []
    for c in out:
        if not folded or folded[-1] != c:
            folded.append(c)
    return "".join(folded)


def _same_name(stem: str, given: str) -> bool:
    """Whether a patronymic stem and a father's given name are the same name.

    Anchored on the first letter and requiring a skeleton of at least two characters, so a stem
    that reduces to almost nothing cannot match everything: `Dison` -> `d` matches no father, and
    that is the point -- it is an inherited surname.

    **Equal, or equal but for a trailing `s`, and nothing looser.** The first version accepted a
    prefix either way and over-matched badly, which the plan file made visible: `Hansdatter` took
    `Heinrich` as a source (`hn` is a prefix of `hnrk`) and `Andersson` took `Andrew`
    (`andr` of `andrv`). Both are different names. The genitive `s` is the only real difference
    between a stem and its given name — `Anders` -> `Andersson`, `Petter` -> `Pettersdotter` —
    so allowing exactly that and nothing else separates `Anders`/`Andreas`, which agree, from
    `Anders`/`Andrew`, which do not.

    Casualties, and they look right: `Olav` and `Oluf` stop attesting `Olsdatter`. Their own
    patronymics are `Olavsen` and `Olufsen`; `Olsen` is son of `Ole` or `Ola`.
    """
    a, b = _skeleton(stem), _skeleton(given)
    if len(a) < 2 or len(b) < 2 or a[0] != b[0]:
        return False
    return a == b or a.rstrip("s") == b.rstrip("s")


def patronymic_or_surname(token: str, father_name: str) -> str:
    """`"patronymic"` or `"family"` for a `-sen`/`-son` token, using the FATHER.

    **Emma's test, 2026-08-26:** *"If father has -son or -sen then it's a surname lol that's
    the test same with other patronymic surnames."*

    **The literal reading of that is 91% wrong** and measuring it is what caught it. In a
    patronymic-naming society the father almost always carries one too: `Einar Jonsen Vestad`
    has father `John Kristiansen Jevne`, and `Maria Christina Jakobsdotter` has father `Jakob
    Jakobsson`. Both are textbook patronymics, and "father has a `-sen`" is true of nearly
    everybody, so it discriminates nothing.

    **What discriminates is whether the father carries the SAME token.** Over the 286,536
    people who have such a token and a known father:

    | | tokens | share |
    | --- | ---: | ---: |
    | father has the same token -> inherited **surname** | 40,872 | 14% |
    | stem matches the father's **given** name -> **patronymic** | 213,898 | 75% |
    | neither -> undecided, kept as patronymic | 31,766 | 11% |

    `James Slawson` son of `James Slawson`, whose children are all `Slawson`, is the surname
    case. `John Kristiansen` son of `Kristian` is the patronymic case. The undecided 11% are
    mostly spelling variants -- `Jonsen`/`John`, `Jakobsdotter`/`Jacob` -- and they keep
    today's morphological answer rather than being guessed at the other way.

    Without a father this returns `"patronymic"`, which is the behaviour every existing caller
    already has.
    """
    if not father_name:
        return "patronymic"
    parts = [t for t in re.split(r"\s+", father_name.strip()) if t]
    fathers_patronymics = {t.casefold() for t in parts if PATRONYMIC.match(t)}
    if token.casefold() in fathers_patronymics:
        return "family"
    m = PATRONYMIC_PARTS.match(token)
    if not m:
        return "patronymic"
    raw = m.group(1).casefold()
    stem = raw.rstrip("s")
    givens = [t.casefold() for t in parts if not PATRONYMIC.match(t)]
    for given in givens:
        g = given.rstrip("s")
        # `_same_name` gets the RAW stem: the genitive `s` is the whole difference it is built to
        # tolerate, and stripping it first is what let `Anders` match `Andrew`.
        if g == stem or _same_name(raw, given):
            return "patronymic"
    # **The stem matched nothing in the father's name, so this is NOT a patronymic.**
    #
    # Emma, 2026-08-31: *"patronymics aren't a middle name they are a specific thing our
    # pipeline should generate based on the given name property on the father matching a
    # substring."* Until then this line returned `"patronymic"` -- the same value as the branch
    # above it -- so the whole loop was decorative and had been since the function was written.
    # `Kristiansen` with father `Kristian Olsen` and `Kristiansen` with father `Bartholomew
    # Smith` classified identically.
    #
    # **The case that proves it, and it cost a real edit.** `Q141205900` *Bertrand Olav Olsen
    # Vigdel*, father `John Jonassen Hegre`. `Olsen` is not John's patronymic -- John's own
    # patronymic is `Jonassen`, son of Jonas -- so the `P5056` we emitted asserted something
    # false. `Epìdosis` removed it on 2026-08-31 and merged the item away.
    #
    # **A morphological suffix is not attestation.** `-sen` on a token whose stem appears
    # nowhere in the father's name is an inherited surname that happens to end like a
    # patronymic, which is exactly the `Slawson` case one branch up seen without the father
    # carrying the token himself.
    return "family"


def without_nickname(label, fields):
    """`Ingvold (Pinkie) Remmie` -> `Ingvold Remmie`. A nickname is not part of the label.

    **Emma, 2026-08-27, on `Q141199868`:** *"analyze https://www.wikidata.org/wiki/Q141199868 and
    why it came out as brackets instead of what it is supposed to be too"*. Geni records her as
    `Ingvold (Pinkie) /Remmie/` and the brackets went straight into `mul` and `en`.
    `CLAUDE.md` § *A nickname alias carries the SURNAME*: *"quotes never go in a label"*.

    **Read off the FIELD, never off the rendered label.** Regexing the label matches the
    apostrophe in `Jean d'O Seigneur d'O` and mangles French names -- 27,211 labels match that
    way against **22,707** genuine nickname tokens in `GIVN` (16,742 parenthesised, 5,965
    quoted).

    **Only spans present in the label verbatim are removed**, so a married surname the `GIVN`
    knows nothing about survives: this deletes what it can find rather than rebuilding the name.
    That is also why a parenthesised *surname* token is safe -- `Katarina Magnusdotter
    (Aspenäs)` has its brackets in `SURN`, which this never reads.

    **Lives here because this is the module that models a name.** It sat in
    `build-garborg-day.py` and was applied at the point of emission, so `derived-labels.csv`
    kept the bracketed form and all 48 readers of `label_en`/`label_mul` saw it -- the same
    shape as the `P1449` drop, which `CLAUDE.md` records had to move here for the same reason.
    """
    if not label or not fields:
        return label
    out = label
    for m in QUOTED.finditer(fields.get("givn") or ""):
        if m.group(0) in out:
            out = out.replace(m.group(0), " ")
    return " ".join(out.split())


def classify_fields(givn: str, surn: str, nick: str = "",
                    marnm: str = "", father_name: str = "") -> list[tuple[str, str, int]]:
    """`(token, usage, ordinal)` from the GEDCOM name FIELDS.

    This is the one to call. `classify()` below takes a rendered label and survives
    only for callers that have nothing else; it guesses where this reads.

    Usages emitted:

    * `given`      — a `GIVN` token that is not quoted and not patronymic
    * `patronymic` — a `-sen`/`-son`/`-datter` token, **from either field**
    * `family`     — `SURN`, the birth family name
    * `married`    — `_MARNM`, only where it differs from `SURN`
    * `nickname`   — a quoted token inside `GIVN`, or the `NICK` field

    Emma, 2026-08-24, on the quoted case: it becomes `P1449` *nickname*, not a given
    name and not a middle name. `Stena` is what `Stine` was called, not her second
    forename.

    The married name carries no ordinal. Sex does not decide whether it is emitted --
    it decides only whether the `P3831` role says *married name*; see `statements_for`.
    """
    out: list[tuple[str, str, int]] = []

    raw_givn = givn or ""
    # Three branches now -- double quote, apostrophe, parenthesis -- because the apostrophe
    # one had to be narrowed to exclude elision (`d'O`) without losing the 963 real bynames
    # Geni writes as `Illugi 'svarti'`. See `QUOTED`.
    nicknames = [m.group("token") or m.group("apos") or m.group("paren")
                 for m in QUOTED.finditer(raw_givn)]
    plain = QUOTED.sub(" ", raw_givn)

    # **A stillbirth description yields no given names at all.** `DESCRIPTION_MARKERS`
    # carries the reasoning; `Bielke` still reaches `SURN` below, so the person keeps a
    # family name and an `NN` label and loses only the words that were never names.
    ordinal = 0
    for token in ([] if is_description(raw_givn)
                  else [t for t in re.split(r"\s+", plain.strip()) if t]):
        # **`name_shape` runs on `GIVN` too.** It did not until 2026-08-31, so every marker
        # already in `UNKNOWN_MARKERS` became a `given` name when it sat in the given-name
        # field: `NN`, `Unknown`, `okänd` and `anonyma` each produced a `P735` proposal.
        # The set existed and the field simply never consulted it.
        token, shape = name_shape(token)
        if shape:
            out.append((token, shape, 0))
            continue
        if PATRONYMIC.match(token):
            out.append((token, patronymic_or_surname(token, father_name), 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))

    # `SURN` is data, not the last whitespace token of anything. It can still hold a
    # patronym -- `name modelling.txt`: *"We have to check in the given names and in
    # the surname whether it is a patronym"* -- so the same test runs on it.
    for raw in [t for t in re.split(r"\s+", (surn or "").strip()) if t]:
        token, shape = name_shape(raw)
        if shape:
            out.append((token, shape, 0))
            continue
        if PATRONYMIC.match(token):
            out.append((token, patronymic_or_surname(token, father_name), 0))
        else:
            out.append((token, "family", 0))

    married = " ".join((marnm or "").split())
    if married and married.casefold() != " ".join((surn or "").split()).casefold():
        for raw in married.split():
            token, shape = name_shape(raw)
            out.append((token, shape or "married", 0))

    # A description yields no nickname either. `(--stillborn--)` occurs 11 times and the
    # bracket makes `QUOTED` read it as a byname, so without this it survives the
    # suppression above and reaches Wikidata as an `Amul` alias instead of a `P735`.
    if is_description(raw_givn):
        nicknames = []
    for token in nicknames + [t for t in [" ".join((nick or "").split())] if t]:
        out.append((token, "nickname", 0))

    return out


def classify(label: str) -> list[tuple[str, str, int]]:
    """`(token, usage, ordinal)` for each token of a rendered LABEL.

    **Prefer `classify_fields`.** This guesses what that reads: it takes the last
    token as the family name and cannot see `_MARNM`, `NICK`, or which field a
    patronym came from. It is kept for callers holding only a display string — the
    relationship-label work, and any report keyed on `label_en`.

    `Ane Oline Jonsdatter Raugstad` ->
        (Ane, given, 1) (Oline, given, 2) (Jonsdatter, patronymic, 0)
        (Raugstad, family, 0)

    The last token is the family name **unless it is itself patronymic**, which is
    the ordinary Norwegian case one generation earlier: `Jon Samuelsen` has no family
    name at all and `Samuelsen` must not become one.
    """
    # Geni wraps a nickname in quotes -- `Stine "Stena" Eivindsdatter Garborg` -- and
    # sometimes in parentheses: `Ingvold (Pinkie) Remmie`. The punctuation is Geni's
    # formatting and the name inside it is real, so it is stripped and the token kept.
    # `CLAUDE.md` on Stena: Emma took the nickname, not the quotes.
    cleaned = re.sub(r'[\"“”()]', " ", label or "")
    tokens = [t for t in re.split(r"\s+", cleaned.strip()) if t]
    if not tokens:
        return []

    # A single token is a GIVEN name, not a family name. `Amaterasu`, `Ninigi`,
    # `NN` -- a mononym is a forename, and calling it a surname would put a personal
    # name in `P734` and leave the person with no `P735` at all. A family name needs
    # something in front of it to be the family name OF.
    if len(tokens) == 1:
        return [(tokens[0], "patronymic" if PATRONYMIC.match(tokens[0]) else "given",
                 0 if PATRONYMIC.match(tokens[0]) else 1)]

    out: list[tuple[str, str, int]] = []
    last = tokens[-1]
    family = last if not PATRONYMIC.match(last) else None
    body = tokens[:-1] if family else tokens

    ordinal = 0
    for token in body:
        if PATRONYMIC.match(token):
            out.append((token, "patronymic", 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))
    if family:
        out.append((family, "family", 0))
    return out


def statements_for(label, plan, geni_id, father_qid=None, fields=None,
                   sex="", father_name=""):
    """(statement lines, notes) for one person's name.

    Each line is `(property, value, qualifiers)` with qualifiers as
    `[(property, value), ...]`, ready for whatever emitter wants them.

    Pass `fields` -- a mapping with `givn`, `surn` and optionally `nick`, `marnm` --
    and the name is read from the GEDCOM fields. Without it the rendered `label` is
    parsed positionally, which is the old behaviour and is worse; see `classify`.

    `father_qid` is the `P144` *based on* target for a patronym -- `name
    modelling.txt` points it at **the person the link names**, not at a name item.
    Omitted when the father has no item yet rather than guessed.

    A `nickname` produces an **alias only** and no statement -- see the block that handles it
    for Emma's 2026-08-29 ruling and why the drop lives here rather than in a caller.

    `sex` is `"M"` or `"F"` and decides one thing only: whether a `_MARNM` family name
    carries `P3831` -> `Q28418670` *married name*. On a man it does not -- see below.
    """
    lines, notes = [], []
    aliases = []
    given_count = 0

    if fields:
        # **`father_name` is what turns a `-sen` token into the right kind of statement.**
        # Emma's test: the same token as the father means an inherited surname (`P734`), a
        # stem matching the father's GIVEN name means a patronymic (`P5056`). Without it the
        # morphology alone decides, which is what every caller did until 2026-08-27 and is
        # still the answer when the father is unknown.
        tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                                 fields.get("nick", ""), fields.get("marnm", ""),
                                 father_name=father_name)
    else:
        tokens = classify(label)

    given_count = sum(1 for _t, u, _o in tokens if u == "given")

    for token, usage, ordinal in tokens:
        # **A particle and an unknown marker never reach the name plan.** Emma, 2026-08-26:
        # a particle is *"integral parts of what the people are called"* and so belongs in
        # the LABEL, and a marker joins the `NN` population `scripts/labels.py` owns. Looking
        # either up would find nothing and file a spurious "not in the plan" note; emitting
        # either would mint an item for `de` or for `?`.
        if usage in ("particle", "unknown"):
            continue

        # **A nickname produces an ALIAS and no statement. Emma, 2026-08-29:** *"the nicknames
        # (listed in English????) are not something that's good. Just drop the nickname
        # functionality because the nicknames being listed in English is unacceptable. Just
        # lmul vs amul."*
        #
        # `P1449` is monolingual text, so it needs a language tag, and the one being emitted was
        # `en` -- declaring `Byre` and `Christophersdatter` to be English words. There is no
        # right tag available either: the nickname is Norwegian on a person whose label is
        # language-neutral `mul`, and guessing a language per person is the inference this repo
        # refuses everywhere else.
        #
        # **The drop belongs HERE, in the model, and not in the emitter.** It lived in
        # `build-garborg-day.py` from 2026-08-29 until 2026-08-30, so the model went on
        # producing `P1449` while nothing could ever emit it -- and `model-vs-reality.py`, which
        # reads the model, reported **66 people missing a nickname** that no batch would ever
        # add. A phantom gap is worse than a silent one: it reads as work.
        #
        # **The nickname is not lost and its classification is untouched.** The token is still
        # recognised, still kept out of the given names, and still reaches Wikidata through
        # `aliases_for` -- an `Amul` carrying the nickname form beside the `Lmul` carrying the
        # primary name, which is exactly the *"just lmul vs amul"* she asked for.
        if usage == "nickname":
            aliases.append(token)
            continue

        # The married name is looked up as a family name -- it IS one, just a later
        # one -- so it shares Garborg's or Jacobson's item rather than needing a
        # separate "married" kind.
        lookup = "family" if usage == "married" else usage
        qid, action = plan.get((token, lookup), ("", "not in the plan"))
        if not qid:
            notes.append(f"{token} ({usage}): {action or 'no item'}")
            continue

        if usage == "given":
            # **`P1545` *series ordinal* only where there is more than one given name.**
            # Emma, 2026-08-25, on why she has been running batches only in part:
            # *"they have consistently included things I did not want, such as the series
            # orginal 1 on peoples given names when there is only one given name"*.
            #
            # It orders a person's several given names against each other. On somebody with
            # one, there is nothing to order and the qualifier asserts a sequence that does
            # not exist -- the same objection that already restricts `P7452` *reason for
            # preferred rank* to people who have a middle name.
            quals = [(SERIES_ORDINAL, str(ordinal))] if given_count > 1 else []
            # **`P7452` -> `Q3409033` *usual forename* only where there IS a middle
            # name.** Emma, 2026-08-24: *"usual forename only applies when there is a
            # middle name"*. It exists to say which of several given names is the one
            # actually used, so on a person with a single given name it distinguishes
            # nothing and asserts a contrast that does not exist.
            if ordinal == 1:
                if given_count > 1:
                    quals.append((PREFERRED_REASON, USUAL_FORENAME))
            else:
                quals.append((HAS_ROLE, MIDDLE_NAME))
            lines.append((GIVEN_NAME, qid, quals))
        elif usage == "patronymic":
            quals = [("P144", father_qid)] if father_qid else []
            lines.append((PATRONYM, qid, quals))
        elif usage == "married":
            # Emma, 2026-08-24: a SECOND `P734`, qualified married against birth.
            # **`Q28418670` *married name* only on a woman.** Emma, 2026-08-24:
            # *"married name on a man ... ontologically married name on a man means
            # more like adopted surname. So men's 'married names' should not have the
            # role of married name."*
            #
            # And it gets **no role at all** rather than `Q118383793` *adoptive name*,
            # because in this material the second surname is usually a **farm name**
            # taken by residence, not by adoption or marriage. `Q141169072` is the
            # case: *Ådne Olsen Grøtheim* became *Ådne Olsen Garborg* by moving to the
            # Garborg farm. Calling that adoption asserts something false, and
            # `reports/garborg-name-transliterations.tsv` already marks Aabø, Fjørtoft,
            # Heigre and Raugstad as farm names. An unqualified `P734` says only that
            # he bore the name, which is all we know.
            if sex == "F":
                lines.append((FAMILY_NAME, qid, [(HAS_ROLE, MARRIED_NAME_ROLE)]))
            else:
                lines.append((FAMILY_NAME, qid, []))
        else:
            # Only qualify the birth family name when a married one sits beside it;
            # a lone surname needs no role and none of her items carries one.
            has_married = any(u == "married" for _t, u, _o in tokens)
            quals = [(HAS_ROLE, BIRTH_NAME_ROLE)] if has_married else []
            lines.append((FAMILY_NAME, qid, quals))

    # **One fact, one statement.** A token can sit in two FIELDS and still be one name:
    # `Hans Erikson` carries `Erikson` in both `GIVN` and `SURN`, so `classify_fields`
    # rightly returns it twice and this loop would emit the identical `P5056` twice.
    # `tests/test_p2600_batches.py::test_no_statement_is_repeated` is the invariant, and it
    # went red the moment the father fix changed which token today's batch reached.
    #
    # **This is NOT the duplication `CLAUDE.md` protects.** That rule is about values on
    # Wikidata Emma duplicates deliberately to attract bot edits, and about not adding a
    # general de-duplication pass over the data. This drops a byte-identical repeat of one
    # statement inside one generated batch, which asserts nothing the first did not.
    # Leaving it in was the call made earlier today and the suite was right to refuse it.
    deduped, seen = [], set()
    for prop, value, quals in lines:
        key = (prop, value, tuple(quals))
        if key in seen:
            continue
        seen.add(key)
        deduped.append((prop, value, quals))
    return deduped, notes


def aliases_for(fields, surn="", marnm=""):
    """Alias strings for an item: the nicknames, and the married full name.

    Emma asked for aliases alongside the second `P734` *family name*. A married
    surname makes the person findable under a name no statement spells out, which is
    what an alias is for.
    """
    out = []
    tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                             fields.get("nick", ""), fields.get("marnm", ""))
    surn = surn or fields.get("surn", "")
    marnm = marnm or fields.get("marnm", "")
    given = [t for t, u, _o in tokens if u == "given"]

    # **A nickname alias carries the SURNAME, or it finds nobody.** Emma, 2026-08-26, on
    # `Q141189102`: *"this person was given an alias of 'Sally' instead of 'Sally Ekman'"*.
    # Her record is `GIVN 'Sigrid "Sally" Manilva'`, `SURN Tunheim`, `_MARNM Ekman`, and a
    # bare `Sally` is not a name anybody could look her up by.
    #
    # The surname used is the **married** one where there is one, because § *The MARRIED
    # name is the real name* makes that the form her primary label takes -- so the alias is
    # the same person's name with the nickname swapped in, not a different person's.
    #
    # `P1449` *nickname* keeps the BARE token, and must: `Sally` is the nickname. It is the
    # alias, whose job is retrieval, that needs the full form.
    # **Unless the nickname ALREADY carries the surname.** Geni's `nick` field is not always a
    # nickname: it frequently holds the person's whole name, often in an abbreviated spelling.
    # `Guri Pedersdatter Foss` has `nick` = `Guri Pedersdtr.Foss`, and appending her surname
    # produced the alias `Guri Pedersdtr.Foss Foss`.
    #
    # **18,759 of 139,080 nickname aliases had the surname doubled** -- 13% -- measured over
    # `reports/display-names.csv`. `Crocker Crocker`, `Rebecca Kaplan Kaplan`,
    # `Johannes Nilsson Nilsson`, `Thorbjørn Lekve Magelssen Magelssen`.
    #
    # The test is `endswith`, not "contains": a nickname that merely mentions the surname
    # somewhere still wants it appended in the ordinary position, and Emma's own case is
    # untouched -- `Sally` does not end with `Ekman`, so it still becomes `Sally Ekman`, which
    # is the whole point of the alias.
    surname = " ".join((marnm or surn or "").split())
    for token, usage, _ordinal in tokens:
        if usage == "nickname":
            bare = token.strip()
            if surname and bare.casefold().endswith(surname.casefold()):
                full = bare
            else:
                full = f"{bare} {surname}".strip()
            if full not in out:
                out.append(full)
    married = " ".join((fields.get("marnm") or "").split())
    if married and married.casefold() != " ".join(
            (fields.get("surn") or "").split()).casefold():
        if given:
            out.append(f"{' '.join(given)} {married}")

    # **The bracketed form itself is an alias.** Emma, 2026-08-26: *"Amul for the brackets"*.
    # The two `P734` *family name* statements are coequal and unqualified, so nothing in the
    # statements records how Geni actually writes the name; the alias does, and it is what
    # makes the person findable by what is on their profile page.
    for field in ("surn", "marnm"):
        raw = " ".join((fields.get(field) or "").split())
        if raw and any(PAREN.match(t) for t in raw.split()):
            full = f"{' '.join(given)} {raw}".strip() if given else raw
            if full not in out:
                out.append(full)
    return out
