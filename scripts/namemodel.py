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
import unicodedata
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
#: **Emma, 2026-09-04, and it is the diagnosis of the whole class of defect:** *"there is no
#: real standardized representation of [patronymics] in our data… so we needed to do some level
#: of positional parsing… Names should not be positionally parsed lol, we should just be able to
#: fix the patronymic issue by parsing patronymics lol. Patronymics are extremely simple but
#: gedcom just sucks at representing them. 'x-son' 'x-sen' 'bin_x' 'ap_x' 'ben_x' 'bar_x'
#: 'fitz_x' 'ferch_x' — a bunch of patronymic forms exist. And they are numerous but extremely
#: regular for the most part."*
#:
#: **Measured over 5,416,925 name tokens**, which is what decides what is on this list:
#: `-son` 187,432 · `-sen` 162,015 · `-dotter` 106,075 · `-datter` 105,351 · `-dtr` 15,849 ·
#: `-søn` 2,072 · `-dóttir` 1,424 · `-ović` 961 · `-wicz` 873 · `-ovna/-evna` 198 ·
#: `-ovich/-evich` 186 · `-sønn` 118.
#:
#: **Three the census caught and this refuses**, because they are inherited surnames here rather
#: than live patronymics: `-es` 76,975 (`Jones`, `Alcides`), `-ez` 29,929 (`Ramirez`, `Perez`)
#: and `-ian` 9,800, which is mostly `Christian` and `Sebastian` — given names.
PATRONYMIC = re.compile(
    r".+?("
    r"sen|son|sson|søn|sønn|"                 # Scandinavian male
    r"datter|sdatter|dotter|sdotter|"          # Scandinavian female
    r"d[oó]ttir|"                              # Icelandic
    r"s(?:dtr|d|dr|dt|dtt|dttr)|"              # the abbreviations, genitive kept
    r"[oe]vich|[oe]vna|ovi[cć]|wicz"           # Slavic
    r")\.?$", re.I)

#: **A standalone token that makes the NEXT token a patronymic.** These are the forms her
#: message names that carry no suffix at all — the name is the father's, and a particle in
#: front says so. Measured: `ap` 6,702 · `verch` 1,881 · `ben` 1,558 · `bin` 1,477 · `ab` 1,261 ·
#: `ferch` 1,234 · `ibn` 865 · `bint` 465 · `bat` 342 · `bar` 315 · `ua`/`uí`/`ní`/`nic` 161.
#:
#: **`Mac`, `Mc`, `Fitz` and `O'` are deliberately NOT here**, though her message lists `fitz_x`.
#: In this corpus they are ATTACHED and inherited — `MacKinnon`, `McIntosh`, `Fitzalan`,
#: `O'Neill`, 9,670 occurrences and not one of them a separate token. They are surnames by the
#: time they reach us; treating them as live patronymics would put a `P5056` on people whose
#: great-grandfather is the one it names. A separate `Fitz` token would qualify and none occurs.
#: **The DAUGHTER forms alone**, which is a narrower question than `PATRONYMIC` and answers a
#: different one: *can this token possibly be a married name?* It cannot. A woman takes her
#: husband's name, and no husband is called `-dotter`.
#:
#: **Emma pointed at `Q136376387` on 2026-09-04 -- *"Check this persons mul label for what I
#: wanted"* -- and her `mul` reads `Ebba Kristina Siöblad`.** Ours read
#: `Ebba Kristina Carlsdotter`: her record is `Ebba Kristina /Siöblad/` with
#: `_MARNM Carlsdotter`, and § *The MARRIED name is the real name* flipped the `_MARNM` into
#: the primary label. But `Carlsdotter` is her PATRONYMIC -- her father is Carl -- mis-filed
#: in the married-name field, so the flip replaced a real surname with a daughter-of form and
#: then `ja`/`zh`/`ko` were transliterated from it.
#:
#: **`CLAUDE.md` already says the field cannot be trusted alone:** *"`_MARNM` is not reliably a
#: married name… 43% are the only surname on the record because `SURN` is empty, and the 25%
#: that differ are 53% male."* This is the part of that which is decidable by FORM, per
#: § *PARSE PATRONYMICS BY FORM*, and nothing else about `_MARNM` is touched.
#:
#: **Measured over `reports/display-names.csv`: 16,277 people carry a daughter-form `_MARNM`,
#: and on 2,483 of them it REPLACES a real `SURN` in the label** -- `Anna Rehnberg` becoming
#: `Anna Abrahamsdotter`, `Ranveg Lunde` becoming `Ranveg Mikkelsdatter`, `Brita Stina
#: Johansson` becoming `Brita Stina Larsdotter`. The other 13,794 have an empty `SURN`, so the
#: flip changed nothing and they are unaffected either way.
#:
#: **The male forms are deliberately NOT here.** A Swedish woman marrying a man called
#: `Petersson` does take `Petersson`, so `-son` in `_MARNM` is genuinely ambiguous and stays
#: with `patronymic_or_surname`, which has the father's name to go on. Only the daughter forms
#: are impossible.
DAUGHTER_PATRONYMIC = re.compile(
    r".+?s(?:datter|dotter|d[oó]ttir|dtr|dt|dtt|dttr|dr|d)\.?$", re.I)


def is_daughter_patronymic(token: str) -> bool:
    """True for `Carlsdotter`, `Ormsdatter`, `Vigfúsdóttir`, `Ljødelsdtr.`

    The genitive `s` is required, and `CLAUDE.md` § *An abbreviated patronymic is EXPANDED*
    records why: without it a bare `d` matches `Svend` 606, `Halvard` 322, `Hand` 92 and
    `Old` 19, which are given names whose stem happens to be attested with `datter`.
    """
    return bool(DAUGHTER_PATRONYMIC.match(token or ""))


#: **A GENERATION SUFFIX, and the two forms Emma wants it written in.** Her ruling, 2026-09-04,
#: with `Q106206114` as the worked example — Wikidata has him as `Elias Lagerheim den yngre`:
#:
#:     Lmul  Elias Lagerheim II
#:     Len   Elias Lagerheim Jr.
#:
#: *"d.y. I think is their version of Junior so in English it should be Jr."*, *"I think II and I
#: might be better mul versions"*, and the load-bearing half: ***"the local language version
#: should not be used"***. `d.y.` is Swedish, `den yngre` is Swedish, `nuorempi` is Finnish —
#: none of them belongs in a language-neutral label or in an English one.
#:
#: **`mul` takes the Roman numeral because `mul` is language-neutral**, and the numeral says the
#: same thing in every language: the junior is the SECOND of the name, so `Jr.` is `II` and `Sr.`
#: is `I`. Her sentence listed the numerals and the abbreviations in the opposite order; the
#: worked example is what settles it and it is unambiguous.
#:
#: **It also makes the CJK labels fall out for free.** `mul` reading `II` goes through
#: `labels.ordinal_readings` and becomes `2世` / `二世` / `2세` — the convention she set by hand on
#: `Q141223436` — rather than the `ジュニア` that a transliteration of the Swedish would give. That
#: earlier answer of hers is superseded by this one, and the table rows are left in place only as
#: a fallback for a label that still literally reads `Jr.`
#:
#: **Bare `de` is NOT here and never can be.** It is the particle, 102,336 occurrences, and
#: `CLAUDE.md` § *A TITLE IS NOT A NAME* records `d.e.` being matched onto it once already:
#: *"matching on a dot-stripped form put `d.e.` (369, Swedish den äldre) onto the particle de"*.
#: Every surface form here carries a dot, a space, or a letter `de` does not have.
#:
#: Counts are over `reports/derived-labels.csv` and `reports/garborg-live-labels.tsv`.
GENERATION_SUFFIX = {
    # junior — 3,359 occurrences
    "jr": ("II", "Jr."),          # 512 + 41
    "jr.": ("II", "Jr."),         # 1,742 + 37
    "d.y.": ("II", "Jr."),        # 643
    "d.y": ("II", "Jr."),         # 203
    "d. y.": ("II", "Jr."),       # 93
    "d y": ("II", "Jr."),         # 26
    "dy": ("II", "Jr."),          # 62
    "den yngre": ("II", "Jr."),   # 22 ours + 8 on Wikidata
    "the younger": ("II", "Jr."),  # 5 on Wikidata
    "nuorempi": ("II", "Jr."),    # 11 on Wikidata, Finnish
    # senior — 3,014 occurrences
    "sr": ("I", "Sr."),           # 561
    "sr.": ("I", "Sr."),          # 1,591 + 1
    "d.e.": ("I", "Sr."),         # 445 + 2
    "d.e": ("I", "Sr."),          # 181
    "d. e.": ("I", "Sr."),        # 83
    "d.ä.": ("I", "Sr."),         # 113 + 8
    "d.ä": ("I", "Sr."),
    "d. ä.": ("I", "Sr."),
    "dä": ("I", "Sr."),           # 39
    "den äldre": ("I", "Sr."),
    "den eldre": ("I", "Sr."),
    "the elder": ("I", "Sr."),
    "vanhempi": ("I", "Sr."),     # 1 on Wikidata, Finnish
}

#: **Which languages a suffix form belongs to.** Emma, 2026-09-05: *"the dy will be present
#: wherever for the languages that use it but the suffixes we have will be always at the end"*.
#: So a `nb` label keeps `d.y.` where Norwegian puts it, and a language that does NOT use the
#: form is one of the *"inappropriate languages"* she named on the same subject — those take the
#: `mul` form, `Elias Lagerheim II`.
#:
#: **Keyed on the form, not on a flat list of languages**, because the two Scandinavian pairs
#: differ by one letter and mean the same thing in different places: `d.ä.`/`den äldre` are
#: Swedish and `d.e.`/`den eldre` are Norwegian and Danish. A single "Scandinavian keeps
#: everything" rule would leave a Swedish `den eldre` and a Norwegian `d.ä.` in place, each of
#: which is the other language's spelling.
#:
#: `nn` and `no` sit beside `nb` because Wikidata uses all three for Norwegian.
SUFFIX_LANGUAGES = {
    "d.y.": {"nb", "nn", "no", "da", "sv"}, "d.y": {"nb", "nn", "no", "da", "sv"},
    "d. y.": {"nb", "nn", "no", "da", "sv"}, "d y": {"nb", "nn", "no", "da", "sv"},
    "dy": {"nb", "nn", "no", "da", "sv"},
    "den yngre": {"nb", "nn", "no", "da", "sv"},
    "d.e.": {"nb", "nn", "no", "da"}, "d.e": {"nb", "nn", "no", "da"},
    "d. e.": {"nb", "nn", "no", "da"}, "den eldre": {"nb", "nn", "no", "da"},
    "d.ä.": {"sv"}, "d.ä": {"sv"}, "d. ä.": {"sv"}, "dä": {"sv"}, "den äldre": {"sv"},
    "nuorempi": {"fi"}, "vanhempi": {"fi"},
    "the younger": {"en"}, "the elder": {"en"},
    "jr": {"en"}, "jr.": {"en"}, "sr": {"en"}, "sr.": {"en"},
}


def suffix_is_native(label: str, language: str) -> bool:
    """Is every generation suffix in `label` one that `language` actually uses?

    `True` when there is no suffix at all, so a label this does not govern is never touched.
    """
    found = _SUFFIX_RE.findall(label or "")
    if not found:
        return True
    # **A region subtag inherits its base language.** Wikidata carries `en-ca` and `en-us`
    # beside `en`, and `Jr.` is native English in all three -- without this the two variants
    # were the only English labels being rewritten to `II`, which is the `mul` form and not
    # what Emma asked English to read. Measured: 2 of the 60 rewrites, both of them wrong.
    codes = {language, language.split("-")[0]}
    return all(codes & SUFFIX_LANGUAGES.get(f.casefold(), frozenset()) for f in found)


#: Longest first, so `d. y.` is matched before `d` could be, and `den yngre` before `den`.
_SUFFIX_RE = re.compile(
    r"(?<![\w.])(" + "|".join(
        re.escape(k) for k in sorted(GENERATION_SUFFIX, key=len, reverse=True)
    ) + r")(?![\w.])", re.I)


def normalise_generation_suffix(label: str, style: str) -> str:
    """Move a generation suffix to the END of the label, in its `mul` or `en` form.

    `style` is `"mul"` or `"en"`. See `GENERATION_SUFFIX` for where both forms come from.

    **THE SUFFIX GOES LAST. It is not rewritten where it stands.** Emma, 2026-09-05, on a first
    version that substituted in place and produced `Lars Jonson II Skrudland`: *"Lars Jonson
    Skrudland Jr. I didn't tell you to do that. Regnal numbers can come after the first name,
    regular ones go Sr Jr III etc always as a suffix in English and in mul always as a suffix
    I, II, III."*

    So the two things are different and only one of them moves:

    - **A generation suffix** -- `d.y.`, `d.e.`, `den yngre`, `Jr.`, `Sr.` -- is a suffix, and
      belongs at the end whatever position Geni wrote it in. `Lars Jonson d.y. Skrudland`
      becomes `Lars Jonson Skrudland II` in `mul` and `Lars Jonson Skrudland Jr.` in `en`.
    - **A regnal ordinal** may sit after the given name and stays exactly where it is. Nothing
      here touches one: `GENERATION_SUFFIX` holds no bare Roman numeral, so `Abisha III ben
      Phinhas` is not a match and does not move. That is `name modelling.txt` § *edge cases*
      and `P7338` *regnal ordinal*, which is a different property from this entirely.

    **A label already carrying the target numeral does not gain a second one.** `Daniel Ström
    II, dy` is written with both; the `dy` is removed and the existing `II` is left in place
    rather than a second suffix being appended. The comma that introduced the suffix goes with
    it, so nothing is left reading `Welhaven, II`.
    """
    if not label or not _SUFFIX_RE.search(label):
        return label
    index = 0 if style == "mul" else 1

    want = ""

    def take(match):
        nonlocal want
        # The LAST one wins, which matters only for a label carrying two; they mean the same
        # thing and one suffix is emitted either way.
        want = GENERATION_SUFFIX[match.group(1).casefold()][index]
        return " "

    out = _SUFFIX_RE.sub(take, label)
    # The comma that introduced the suffix goes with the suffix, not with the name before it.
    out = re.sub(r"\s*,\s*(?=\s|$)", " ", out)
    out = " ".join(out.split()).rstrip(",").strip()
    if not out:
        return label

    # **Across BOTH styles, because `II` and `Jr.` say the same thing.** A numeral already in the
    # label is what the person is called; the converted suffix is dropped rather than stacked
    # beside it, which is what left the `en` form reading `Daniel Ström II Jr.`
    targets = {v[0] for v in GENERATION_SUFFIX.values()} | {
        v[1] for v in GENERATION_SUFFIX.values()}
    if any(token in targets for token in out.split()):
        return out
    return f"{out} {want}".strip()


def married_name_of(fields) -> str:
    """The `_MARNM` where it really is a married name, else `""`.

    A `_MARNM` every token of which is a daughter patronymic is the person's own patronymic in
    the wrong field -- see `DAUGHTER_PATRONYMIC`. It must not become the primary label, must
    not become a `P734` *family name* with the `Q28418670` *married name* role, and must not
    make a "married full name" alias.
    """
    married = " ".join((fields.get("marnm") or "").split())
    if not married:
        return ""
    if all(is_daughter_patronymic(t) for t in married.split()):
        return ""
    return married


PATRONYMIC_PARTICLE = frozenset({
    "ap", "ab", "ferch", "verch",              # Welsh
    "ben", "bin", "ibn", "bint", "bar", "bat",  # Semitic
    "ua", "uí", "ní", "nic",                   # Gaelic
})
#: **Unaccented `ni` and `ui` are NOT here, and the census is why.** Capitalised `Ni` heads
#: `Ni Choon`, a Chinese name, as often as it heads a Gaelic one; the accented forms are
#: unambiguous. It costs 17 occurrences and buys never renaming a Chinese person's father.
#:
#: **Case is NOT a discriminator for the Semitic particles**, which was checked rather than
#: assumed: `Ben Alan`, `Ben Zev`, `Nethanel Ben Yehiel` and `Yitzhak Ben Shmuel` are all
#: Hebrew *ben*, not the English given name — 168 capitalised against 1,346 lower, and reading
#: them settles it. `Bar` is the one with a real residue: `van Bar Opper-Lotharingen` is a place
#: in Lorraine, 10 occurrences of 185.

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


#: **A TITLE IS NOT A NAME, and Geni already says so -- in `NSFX`.** Emma, 2026-09-03, on
#: `Q2183430` *Benedicta Ebbesdotter of Hvide*: *"There was a bit of a disaster of her names in
#: an earlier quickstatements batch where 'Queen' and 'Sweden' were treated as names."* She is
#: right and it was live: the batch carried
#: `Q2183430 P735 Q20899047` -- given name **Queen**, as middle name 3 -- and
#: `Q2183430 P734 Q37437749` for **Sweden**.
#:
#: **The GEDCOM was correct the whole way.** Her record reads
#: `1 NAME Bengta Ebbesdotter /Ebbesdatter Galen/` with `2 NSFX Queen of Sweden` -- the title
#: in the name-SUFFIX field, exactly where it belongs. `build-display-names.py` concatenates
#: every piece into `display_name`, `derive-labels.py` appends `nsfx` again building the
#: married-name alias, and the name model then parses that rendered string positionally. So a
#: field whose whole purpose is *this part is not a name* became two name items.
#:
#: **Measured over 1,856,150 name records: 86,947 carry an `NSFX`, and it holds two different
#: things.** 30,730 are a single token -- `II` 2,224, `I` 1,836, `Jr.` 1,693, `Sr.` 1,436,
#: `Graf` 464, `Knight` 274 -- where the regnal ordinals genuinely ARE part of the name
#: (`CLAUDE.md`: `P7338` *regnal ordinal* is a qualifier on the given name). **42,391 are a
#: multi-word phrase carrying a connective** -- `Pharaoh of Egypt` 107, `Queen of Egypt` 53,
#: `King of Assyria` 30, `i København` 35, `til Gullaug` 22 -- and not one of those is a name.
#:
#: **So only the phrase form is dropped here**, which is total precision on the population it
#: touches and leaves the single-token question where `name modelling.txt` puts it: *"for the
#: edge cases I am going to want you to tell me about the edge cases."* The 13,826 multi-word
#: values with no connective (`d. y.`, `Patrizio Napoletano`, `132, 91, 44, 9`) wait with them.
#:
#: This is the same mechanism as `DESCRIPTION_MARKERS` above and as
#: `build-garborg-day._drop_territorial`, which does it for the transliterated label and now
#: delegates here so the words live in one place.
TITLE_WORDS = {
    "queen", "king", "prince", "princess", "emperor", "empress", "duke", "duchess",
    "earl", "count", "countess", "baron", "baroness", "lord", "lady", "dame", "sir",
    "saint", "bishop", "archbishop", "pope", "tsar", "tsarina", "pharaoh", "consul",
    "drottning", "drotting", "dronning", "kung", "konge", "kong", "konung",
    "prins", "prinsessa", "prinsesse", "prinz", "prinzessin",
    "hertig", "hertug", "hertiginna", "herzog", "herzogin",
    "greve", "grevinna", "grevinde", "friherre", "friherrinna",
    "kejsare", "kejsarinna", "biskop", "ärkebiskop", "erkebiskop",
    "könig", "königin", "kaiser", "kaiserin", "graf", "gräfin", "markgraf", "markgräfin",
    "fürst", "furst", "jarl", "reine", "roi", "duc", "duchesse", "comte", "comtesse",
    "kuningas", "kuningatar", "maestre",
}

#: What turns a title word into a title PHRASE, and what opens a territorial tail on its own.
#: `till Krageholm` is Swedish for *of Krageholm*, an estate -- `CLAUDE.md` records Emma
#: catching `カール・フレドリク・パイパー・ティル・クラゲホルム` and correcting the item by hand.
TITLE_CONNECTIVES = {"of", "von", "van", "de", "des", "der", "du", "di", "da",
                     "af", "av", "zu", "the"}
#: **English `of` is one of these IN THE NAME MODEL, and only there.** Measured over the
#: 1,295,226 labelled people: 16,165 carry a non-initial bare `of` with something after it,
#: and the tails are places without exception — `of Egypt` 324, `of Axum` 126, `of Armenia` 83,
#: `of Burgundy` 77, `of Denmark` 55, `of Sweden` 44, `of that Ilk` 58, `of Kinderton`,
#: `of Swinton`. **No family name in this corpus is introduced by English `of`**, so
#: `Guaimar II of Salerno` emitting `P734` *family name* `Salerno` is simply wrong.
#:
#: It stays out of `build-garborg-day._drop_territorial`, which trims the label before
#: transliteration — whether `Anne of Denmark` should read `アン・オフ・ダンマーク` is a question
#: about her LABEL and is hers. This is only about what becomes a name item.
TERRITORIAL_OPENERS = {"till", "til", "i", "på", "paa", "of"}


#: **A single-token `NSFX` is a TITLE or an ORDINAL, and only the titles are dropped.**
#: Emma, 2026-09-04, choosing between four readings of the 30,730 single-token suffixes:
#: *drop titles, keep ordinals*. So `Graf`, `Knight`, `Donna` and `Kt.` stop becoming `P735`
#: *given name* and `P734` *family name* items, while `II`, `I`, `Jr.`, `Sr.`, `d.y.` and the
#: CJK generation numerals stay in the name — the ordinals carry `P7338` *regnal ordinal* and
#: are part of what the person is called.
#:
#: **Built by reading the values with their counts, not by reasoning about what a title is.**
#: 5,204 distinct values; this list drops **7,917 occurrences, 25.8%**. What SURVIVES the
#: filter is the whole test and was read by eye: `II` 2,224 · `I` 1,836 · `Jr.` 1,693 ·
#: `Sr.` 1,436 · `III` 1,154 · 一 800 · `d.y.` 598 · `d.e.` 369 · `fils` 26 · `Filho` 17 ·
#: `Junior` 17 · `Senior` 14 · `younger` 13 — and then Norwegian farm surnames, `Ytteren` 26,
#: `Altermark` 26, `Skonseng` 17, `Sandnes` 16, `Sveen` 16, `Kjærulf` 15. **Those farms are
#: why this is a list and not a rule:** they are ordinary surnames sitting in the suffix
#: field, and anything that dropped what it did not recognise would have deleted them.
#:
#: **Two collisions were found by measuring and both would have been silent.** `i` casefolds
#: together with the Roman numeral `I`, which is 1,836 people — the trap `_drop_territorial`
#: already carries a comment about — so `i` is not on this list at all, for the 21 occurrences
#: it would have bought. And matching on a dot-stripped form put `d.e.` (369, Swedish *den
#: äldre*) onto the particle `de`. **Nothing is dot-stripped here**; every surface form the
#: corpus actually holds is listed instead.
#:
#: A token carrying no letter and no digit is also not a name — `*` 66, `♊` 45 (the Gemini
#: sign, a twin marker), `?` 22, `.` 19, `+` 18 — and `is_suffix_title` says so without
#: needing them enumerated.

#: nobility, rank and courtesy
_NOBILITY = (
    'baron', 'barone', 'barones', 'baronesa', 'baroness',
    'baronesse', 'baronet', 'baronica', 'boyar', 'bsse',
    'bsse.', 'bt.', 'burggraf', 'burggräfin', 'chevalier',
    'comte', 'comtesse', 'conde', 'condesa', 'conte',
    'contesa', 'count', 'countess', 'coya', 'dame',
    'don', 'dona', 'donna', 'doña', 'duc',
    'duca', 'duchess', 'duchesse', 'duke', 'duque',
    'duquesa', 'elector', 'erbkurprinz', 'erbprinz', 'erzherzog',
    'erzherzogin', 'exilarch', 'freifrau', 'freiherr', 'freiin',
    'friherre', 'friherrinna', 'furst', 'fürst', 'graaf',
    'graf', 'grafaitė', 'grafas', 'grafienė', 'grafin',
    'gravin', 'greve', 'grevinde', 'grevinna', 'grevinne',
    'grof', 'gräfin', 'gräfinne', 'gróf', 'herr',
    'herrin', 'herzog', 'herzogin', 'hrabia', 'inca',
    'infant', 'infanta', 'jarl', 'k.b.', 'kb',
    'kg', 'khatun', 'king', 'királyné', 'knight',
    'knt', 'knt.', 'knyaz', 'kníže', 'komtesse',
    'konge', 'koning', 'královna', 'książę', 'kt',
    'kt.', 'kung', 'kunigaikštienė', 'kunigaikštis', 'kunigaikštytė',
    'kurfürst', 'lady', 'landgraf', 'landgräfin', 'lensgreve',
    'lensgrevinde', 'lord', 'marchesa', 'marchese', 'markgraf',
    'markgräfin', 'marquesa', 'marquis', 'miles', 'nasi',
    'nobil', 'nobile', 'orkneyjarl', 'pangeran', 'pfalzgraf',
    'pfalzgräfin', 'podestà', 'prince', 'princess', 'princesse',
    'principessa', 'prins', 'prinsesse', 'prinz', 'prinzessin',
    'procer', 'queen', 'reichsfreiherr', 'reichsgraf', 'ridder',
    'ritter', 'seigneur', 'sir', 'княжна', 'князь',
    '殿下', '親王', '陛下',
)

#: clerical and religious
_CLERICAL = (
    'abade', 'abbess', 'archbishop', 'badessa', 'bischof',
    'bishop', 'biskop', 'canónigo', 'cardinal', 'cardinale',
    'clerigo', 'clérigo', 'erzbischof', 'frade', 'franciscano',
    'fray', 'frei', 'freira', 'hacohen', 'hakohen',
    'halevi', 'halevy', 'hy"d', 'irmã', 'kanonik',
    'kanoniker', 'katz', 'licenciado', 'monaca', 'monaco',
    'monja', 'monje', 'nonne', 'nun', 'padre',
    'pbro', 'pbro.', 'presbitero', 'presbítero', 'rabbi',
    'religiosa', 'religioso', 'rev', 'rev.', 's.j.',
    'sacerdote', 'saint', 'segal', 'sj', 'sogneprest',
    'sognepræst', 'sor', 'vescovo', 'הי"ד', 'הי״ד',
    'הכהן', 'הלוי', 'זצ"ל', 'ע"ה',
)

#: office, rank, profession and post-nominal
_OFFICE = (
    'alferez', 'alférez', 'bagermester', 'bonde', 'br',
    'cap.', 'capitan', 'capitán', 'capitão-mor', 'capt',
    'capt.', 'captain', 'conquistador', 'consul', 'csa',
    'd.d.', 'dd', 'dds', 'diputado', 'dr',
    'dr.', 'dup', 'eidsvollsmann', 'esq', 'esq.',
    'esquire', 'farmer', 'frs', 'general', 'generalmajor',
    'gent', 'gent.', 'godsejer', 'jp', 'kaptein',
    'kjøpmann', 'lic.', 'm.d.', 'major', 'md',
    'mp', 'mr', 'mr.', 'mrs', 'mrs.',
    'nauta', 'obe', 'oberst', 'ph.d', 'ph.d.',
    'phd', 'professor', 'ra', 'regidor', 'rno',
    'rso', 'rvo', 'sargento', 'senator', 'skipper',
    'statsminister', 'styrmann', 'usa',
)

#: a description of the person, never a name
_DESCRIPTION = (
    'b.l.', 'concubine', 'fictional', 'fictitious', 'heiress',
    'infant', 'legendary', 'mistress', 'ogift', 'oä',
    'solteira', 'stillborn', 'tv', 'tvill', 'tvill.',
    'tvilling', 'twin', 'u.b.', 'ug', 'ug.',
    'ugift', '殤',
)

#: a dynasty or clan tag
_DYNASTY = (
    'bagratids', 'bjälboätten', 'folkungaätten', 'riurikaitis', 'rurikid',
    'rurykowicz', 'български', 'рюрикович', 'рюриковичи', 'чингизид',
)

#: a particle stranded in the suffix field
_PARTICLE = (
    'fon', 'og', 'pl.', 'v.', 'von',
    'фон',
)


NAME_SUFFIX_TITLES = frozenset(
    t.casefold() for group in (_NOBILITY, _CLERICAL, _OFFICE,
                               _DESCRIPTION, _DYNASTY, _PARTICLE)
    for t in group)

#: **`_PARTICLE` is deliberately absent here.** `Graf von Maltzahn` must lose `Graf` and keep
#: `von Maltzahn`: `von` is *"an integral part of what the people are called"* — Emma,
#: 2026-08-26 — and `name_shape` already classifies it as a particle so it never becomes a
#: `P734` *family name* of its own. Stripping it from the front would renumber the name
#: instead of cleaning it.
_LEADING_TITLES = frozenset(
    t.casefold() for group in (_NOBILITY, _CLERICAL, _OFFICE, _DESCRIPTION, _DYNASTY)
    for t in group)


def is_suffix_title(token: str) -> bool:
    """True when this `NSFX` token is a title rather than part of the name."""
    if not token:
        return False
    if not any(ch.isalnum() for ch in token):
        return True
    low = token.casefold()
    return low in NAME_SUFFIX_TITLES or token.strip("()[]{}").casefold() in NAME_SUFFIX_TITLES


def drop_leading_title(field: str) -> str:
    """A name field with its LEADING title tokens removed. `Graf von Maltzahn` -> `von Maltzahn`.

    **The other end from `drop_title_tail`, and it needs its own rule.** `Q110410743` carries
    `_MARNM` = `Graf von Maltzahn, Freiherr zu Wartenberg und Penzlin`, so the title comes
    FIRST and the name follows it; truncating from the title, as the tail rule does, would
    have emptied the field. It emitted `P734` *family name* `Q1158367` **Graf**.

    **Never to empty.** A field whose only token is a title keeps it — `Anna King` has `King`
    as her whole surname, and 17 people carry `King` as a suffix while far more carry it as a
    name. One token left is where this stops.
    """
    toks = (field or "").split()
    while len(toks) > 1 and toks[0].strip("()[]{}").casefold() in _LEADING_TITLES:
        toks.pop(0)
    return " ".join(toks)


def drop_leading_territorial(field: str) -> str:
    """`""` when a name FIELD opens with a territorial word — the whole field is a place.

    **A field may be emptied; a label may not.** `drop_title_tail` skips index 0 on purpose,
    because truncating a whole label leaves a person with no name at all. A `SURN` or `_MARNM`
    is different: `Q2705969` *Guaimar II of Salerno Gybbosus* carries `_MARNM` = `of Salerno`,
    which is entirely a territorial designation, and skipping its first token let `Salerno`
    through as a `P734` *family name*. Nobody's family name is `Salerno` here.

    Case decides `i` from `I` exactly as everywhere else, and a lone opener with nothing after
    it is a name token that happens to look like the preposition.
    """
    toks = (field or "").split()
    if len(toks) < 2:
        return field
    first = toks[0].strip(",")
    if first == "I":
        return field
    return "" if first.casefold() in TERRITORIAL_OPENERS else field


def drop_name_suffix(label: str, nsfx: str) -> str:
    """`label` with its whole `NSFX` removed. The suffix is never a name component.

    **Emma, 2026-09-04:** *"our general thing should be basically the name suffix never is
    anything involved… there never should be anything that is ever translated within the name
    suffix. It is just it in terms of, like, the father name, the middle name, the first name,
    last name."* Those four are the components; `NSFX` is none of them.

    **This supersedes `drop_title_suffix`, which kept the ordinals in the name.** Her 09-04
    ruling *drop titles, keep ordinals* is not contradicted: an ordinal stays available as
    `P7338` *regnal ordinal*, a QUALIFIER on the given name, and stays in the rendered label.
    What it stops being is a `P735` or `P734` of its own, which it never should have been —
    `II` is not a name.

    Removal is by exact trailing match against the person's own suffix, so nothing else can be
    taken, and never to empty.
    """
    if not label or not nsfx:
        return label
    toks = label.split()
    suffix = nsfx.split()
    while len(toks) > 1 and suffix and toks[-1] == suffix[-1]:
        toks.pop()
        suffix.pop()
    return " ".join(toks).strip() or label


def drop_title_suffix(label: str, nsfx: str) -> str:
    """`label` with the TITLE part of its own `NSFX` removed, and nothing else.

    **The exactness is the safety.** Only a trailing token that the person's OWN `NSFX` holds
    is considered, so `Anna King` keeps her surname while
    `Dániel IV Esterházy de Galántha Graf` loses the `Graf` Geni put in the suffix field. A
    word list applied to any trailing token would have taken `King`: 17 people carry it as a
    suffix and far more carry it as a surname.

    An ordinal in the suffix stays where it is — `Robert VII` keeps its `VII` — which is the
    half of her 2026-09-04 ruling that says *keep ordinals*.
    """
    if not label or not nsfx:
        return label
    toks = label.split()
    suffix = nsfx.split()
    while toks and suffix and toks[-1] == suffix[-1]:
        if not is_suffix_title(toks[-1]):
            break
        toks.pop()
        suffix.pop()
    return " ".join(toks).strip() or label


def drop_title_tail(label: str) -> str:
    """`label` with a trailing title or territorial phrase removed. See `TITLE_WORDS`.

    A title word counts only when a connective follows it, which is what separates
    `Óláfr Guðrøðarson king of Man` from `Sarah Bishop`, `Anne Greve` and `Anna King` --
    real surnames that a bare word list would have destroyed. Measured over the 1,295,226
    labelled people: **10,619 truncate and 5,945 are left alone**, and reading the second
    list is what established that the connective is doing the work.

    Truncation is at the EARLIEST title word once ANY of them qualifies, so a stack ending
    in a qualifying phrase takes the whole stack -- `Prins, Hertig av Västergötland` goes as
    one. That was checked rather than assumed: **171 labels stack titles that way and every
    one is genuine**, with no `Anna King` among them.

    `I` is never a territorial opener: it is the Roman numeral one, and Norwegian `i` means
    *in*. Case decides, exactly as `build-garborg-day._drop_territorial` had it.
    """
    toks = (label or "").split()
    idx = None
    for i, t in enumerate(toks):
        if not i:
            continue
        stripped = t.strip(",")
        bare = _bare_word(t)
        # A territorial opener needs something after it: a trailing `i` with nothing following
        # is a name token that looks like the preposition, and truncating there deletes a real
        # name. Case is what separates Norwegian `i` (*in*) from the regnal `I`, and is never
        # folded -- `Reinoud I van Brederode` lost its whole name to that once.
        if bare in TERRITORIAL_OPENERS and i + 1 < len(toks):
            if stripped == "i" or (stripped != "I" and stripped.casefold() in TERRITORIAL_OPENERS):
                idx = i if idx is None else min(idx, i)
                break
        if bare in TITLE_WORDS:
            if idx is None:
                idx = i
            nxt = _bare_word(toks[i + 1]) if i + 1 < len(toks) else ""
            if nxt in TITLE_CONNECTIVES:
                break
    else:
        # No qualifying phrase: every title word seen was a bare one, so keep the name whole.
        return label
    return " ".join(toks[:idx]).strip() or label



def is_patronymic(token: str) -> bool:
    """True for a suffix form (`Jonsdatter`) or a joined particle form (`ben Phinhas`)."""
    if not token:
        return False
    if " " in token:
        return token.split(" ", 1)[0].casefold() in PATRONYMIC_PARTICLE
    return bool(PATRONYMIC.match(token))


#: A Latin GENITIVE ending, longest first. `Olai` is *of Olaus*, `Petri` *of Petrus*,
#: `Johannis` *of Johannes*, `Andreae` *of Andreas*, `Svenonis` *of Sveno*. Swedish and
#: Finnish clergy of the 16th to 18th centuries are named this way as a matter of course --
#: `Olaus Petri Niurenius`, `Nicolaus Olai Plantin`, `Johannes Benedicti`, `Petrus Martini`.
LATIN_GENITIVE_ENDINGS = ("onis", "ii", "is", "ae", "æ", "i")

#: The nominative endings a stem is put back into, to be checked against the father's own given
#: name: `petr` -> `petrus`, `johann` -> `johannes`, `jon` -> `jonas`, `sven` -> `sveno`,
#: `laurent` -> `laurentius`, and `samuel` -> `samuel` for the third declension, where the
#: nominative IS the stem.
LATIN_NOMINATIVE_ENDINGS = ("us", "ius", "es", "as", "os", "a", "o", "")

#: A Roman numeral, which `-i`/`-ii` otherwise matches: `VIII` reduced to a stem `vi` and was
#: confirmed 29 times before this was here.
ROMAN_NUMERAL = re.compile(r"^[ivxlcdm]+$", re.I)


def _fold(word: str) -> str:
    """Casefold, decompose and drop the diacritics, and spell `æ` out.

    `Andreæ` and `Andreae` are the same name written twice, and neither is `andrea`.
    """
    low = (word or "").casefold().replace("æ", "ae").replace("ø", "o")
    return "".join(c for c in unicodedata.normalize("NFD", low)
                   if not unicodedata.combining(c))


def latin_genitive_stems(token: str) -> list[str]:
    """Every nominative stem `token` could be the Latin genitive of, folded.

    `Petri` -> `petr` (Petrus), `Johannis` -> `johann` (Johannes), `Svenonis` -> `sven`
    (Sveno), `Andreae` -> `andre` (Andreas). More than one ending can match, so all are
    returned and the caller keeps whichever the father's own name confirms.
    """
    out, low = [], _fold(token)
    if " " in low or len(low) < 4 or ROMAN_NUMERAL.match(low):
        return out
    for end in LATIN_GENITIVE_ENDINGS:
        if low.endswith(_fold(end)) and len(low) - len(_fold(end)) >= 2:
            stem = low[: -len(_fold(end))]
            if stem not in out:
                out.append(stem)
    return out


def latin_patronymic(token: str, father_given: str) -> bool:
    """Whether `token` is a Latin genitive patronymic, CONFIRMED by the father's given name.

    **Emma, 2026-09-05**, having linked `Olofsson` and `Olai` by hand and been shown the model
    reading `Olai` as a family name: *"detect the form, then confirm it against the father's
    own given name so `Petri` on an Italian is not swept up."*

    **The confirmation reconstructs the NOMINATIVE and compares it as a string.** `Olai` ->
    `olaus`, and the father must be recorded `Olaus`. Nothing is folded but case and
    diacritics, and that strictness is the whole discriminator -- `_skeleton`, which
    `patronymic_or_surname` uses, is far too permissive here: it confirmed `Morris` from a
    father `Meir`, `Zachris` from `Zacharias`, `Kylili` from `Kylilis` and `Maakebzgi` from
    `MAKebzgi`, none of which is a Latin genitive of anything.

    **The father's GIVEN name, not his whole label**, for the same reason. Matching any token
    of the label let a Cypriot `-is` surname confirm its own inherited form.

    **A token the father carries himself is inherited, not derived**, and returns `False`: the
    son of `Olaus Petri` is `Olai`, never `Petri`, so a `Petri` whose father is also `Petri`
    is a family name that began as a patronymic a generation or more back. Same rule, and the
    same reasoning, as `patronymic_or_surname` applies to the `-son` forms.

    Measured over the corpus: **98,459 tokens match the shape** and this confirms **3,264**.
    """
    return bool(latin_patronymic_source(token, father_given))


def latin_patronymic_source(token: str, father_given: str) -> str:
    """The father's given name `token` is the Latin genitive of, or `""`.

    The same test as `latin_patronymic` and the answer it found: `Olai` against a father
    recorded `Olaus Olof` returns `Olaus`, which is the name the patronymic derives from and
    so the `P144` *based on* target for the name item.
    """
    stems = latin_genitive_stems(token)
    if not stems or not father_given:
        return ""
    givens = {}
    for t in re.split(r"\s+", father_given.strip()):
        if t:
            givens.setdefault(_fold(t), t)
    if _fold(token) in givens:
        return ""
    for stem in stems:
        for end in LATIN_NOMINATIVE_ENDINGS:
            if stem + end in givens:
                return givens[stem + end]
    return ""


def join_particles(tokens: list[str]) -> list[str]:
    """`['ap', 'Thomas']` -> `['ap Thomas']`, so a particle patronymic is ONE token.

    **Why joining rather than a per-loop special case.** The particle and the father's name are
    one patronymic — `name modelling.txt` models `Abisha III ben Phinhas ben Yittzhaq` as one
    `P5056` *patronym or matronym* per link — and every classifier here walks tokens one at a
    time. Joining first means `classify` and `classify_fields` need no lookahead and cannot
    disagree about it.

    **It also stops `ben` being thrown away.** `ben` is in `PARTICLES`, so `name_shape` dropped
    it and left `Phinhas` to be read as an ordinary name; `CLAUDE.md` records that it *"must
    never become a `P734` family name of its own"*, which was true and left it as nothing at
    all. Joined, the pair is the patronymic the model always specified.

    A trailing particle with nothing after it is left alone — it names nobody.
    """
    out: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.strip(".,").casefold() in PATRONYMIC_PARTICLE and i + 1 < len(tokens):
            # **The particle takes everything up to the NEXT particle, not one token.**
            # Emma, 2026-09-04: *"'bin Haji Muhammad' is a single patronymic."* `Haji` is an
            # honorific and the father is `Haji Muhammad`, so stopping after one token names
            # the wrong man. Stopping at the next particle is what keeps the chain intact:
            # `ben Phinhas ben Yittzhaq ben Shalma` stays three links rather than collapsing
            # into one, which is `name modelling.txt`'s worked example.
            j = i + 1
            while j < len(tokens) and tokens[j].strip(".,").casefold() not in PATRONYMIC_PARTICLE:
                j += 1
            out.append(" ".join(tokens[i:j]))
            i = j
            continue
        out.append(t)
        i += 1
    return out


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
    # **`h` counts only in first position.** `Pehr` and `Per` are one name, as are
    # `Johannes`/`Joannes`, `Tohl`/`Thol`, `Brynhild`/`Brynild` and `Jens`/`Johannes`; an inner
    # `h` is a spelling, not a consonant that distinguishes anybody. It stays in first position
    # because there it is real -- `Hans`, `Halvor`, `Haakon` -- and dropping it there would make
    # every H-name collide with its vowel-initial neighbours. Measured before applying: 1,705
    # tokens rescued, 14 of 14 sampled genuine.
    out += [c for c in w[1:] if c not in "aeiouyáàâäåæéèêëíìîïóòôöøúùûüh"]
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


def patronymic_or_surname(token: str, father_name: str, also_known_as: str = "") -> str:
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

    **`also_known_as` is EVERY OTHER SPELLING the father is recorded under, and it feeds the
    given-name half ONLY.** Emma, 2026-09-05, on `Q141312682` *Zacharias Olai Plantin*:
    *"he got Olofsson as a fucking surname"*. His father is `Olaus Petri Niurenius` — the
    Latin form Swedish clergy are recorded under — and `_skeleton("olof")` is `olf` against
    `_skeleton("olaus")` `ols`, so the stem matched nothing and a textbook patronymic came out
    as a `P734` *family name* with the *birth name* role. Geni held the answer the whole time:
    the same father's record carries `Olaus Persson` as an alias and `Olof Persson` in `nick`.

    **Only the given-name half, and the split is what makes it safe.** Run over the whole
    corpus, feeding the extra spellings to *both* halves moved **1,430 tokens family ->
    patronymic and 1,351 the other way**, and the second direction was wrong every time it was
    read: the father's aliases can carry a patronymic of his own spelled differently
    (`Ola Olsen Løland` also recorded `Olson`), and the *"father carries the same token, so it
    is inherited"* test then fires on a spelling rather than on the name he went by. Feeding
    them to the given-name test alone gives **1,480 family -> patronymic and 0 the other way**
    — monotone, in the direction that can only recognise a patronymic it was missing.

    The sample reads as one phenomenon, Latin and vernacular for one man: `Israel Olofsson` of
    `Olaus Andreæ Angermannus` (also `Olof Andersson`), `Brita Nilsdotter Plantin` of
    `Nicolaus Olai Plantin` (also `Nils`), `Kerstin Hansdotter Benedicti` of
    `Johannes Benedicti` (also `Hans`), `Cnut Sweynsson` of `Svend Haraldssøn` (also `Sweyn`).
    """
    if not father_name:
        return "patronymic"
    parts = [t for t in re.split(r"\s+", father_name.strip()) if t]
    fathers_patronymics = {t.casefold() for t in parts if is_patronymic(t)}
    if token.casefold() in fathers_patronymics:
        return "family"
    m = PATRONYMIC_PARTS.match(token)
    if not m:
        return "patronymic"
    raw = m.group(1).casefold()
    stem = raw.rstrip("s")
    # The other spellings join the GIVEN names and nothing else -- see the docstring: they are
    # evidence about which name the father bore, never about which token he was called by.
    parts += [t for t in re.split(r"\s+", (also_known_as or "").strip()) if t]
    givens = [t.casefold() for t in parts if not is_patronymic(t)]
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
                    marnm: str = "", father_name: str = "",
                    father_aka: str = "",
                    father_given: str = "") -> list[tuple[str, str, int]]:
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
    # **The Latin genitive test needs the father's GIVEN name and nothing else** -- see
    # `latin_patronymic`, where matching any token of his label let a Cypriot surname confirm
    # its own inherited form. A caller that has the field passes it; one that has only a label
    # falls back to its first token, which is the given name in every Latin clergy name this
    # governs (`Olaus Petri Niurenius`).
    if not father_given and father_name:
        father_given = father_name.split()[0]

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
                  else join_particles([t for t in re.split(r"\s+", plain.strip()) if t])):
        # **`name_shape` runs on `GIVN` too.** It did not until 2026-08-31, so every marker
        # already in `UNKNOWN_MARKERS` became a `given` name when it sat in the given-name
        # field: `NN`, `Unknown`, `okänd` and `anonyma` each produced a `P735` proposal.
        # The set existed and the field simply never consulted it.
        token, shape = name_shape(token)
        if shape:
            out.append((token, shape, 0))
            continue
        if is_patronymic(token):
            out.append((token, patronymic_or_surname(token, father_name, father_aka), 0))
        elif latin_patronymic(token, father_given):
            # `Nicolaus Iohannis Johansson`, `Magnus Jonæ Uhr`, `Georgius Andreae Troninus`:
            # the Latin genitive stands where a middle name would and is not one.
            out.append((token, "patronymic", 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))

    # `SURN` is data, not the last whitespace token of anything. It can still hold a
    # patronym -- `name modelling.txt`: *"We have to check in the given names and in
    # the surname whether it is a patronym"* -- so the same test runs on it.
    for raw in join_particles([t for t in re.split(r"\s+", (surn or "").strip()) if t]):
        token, shape = name_shape(raw)
        if shape:
            out.append((token, shape, 0))
            continue
        if is_patronymic(token):
            out.append((token, patronymic_or_surname(token, father_name, father_aka), 0))
        elif latin_patronymic(token, father_given):
            out.append((token, "patronymic", 0))
        else:
            out.append((token, "family", 0))

    married = " ".join((marnm or "").split())
    if married and married.casefold() != " ".join((surn or "").split()).casefold():
        for raw in married.split():
            token, shape = name_shape(raw)
            # **`_MARNM` gets the patronymic test too, and it did not until 2026-09-04.**
            # `GIVN` and `SURN` both run `is_patronymic` above -- `name modelling.txt`:
            # *"We have to check in the given names and in the surname whether it is a
            # patronym"* -- and the married field was the one that did not, so
            # `Carlsdotter` in `_MARNM` became a `P734` *family name* carrying the
            # `Q28418670` *married name* role. Only the DAUGHTER forms, which cannot be a
            # married name at all; see `DAUGHTER_PATRONYMIC`.
            if not shape and is_daughter_patronymic(token):
                out.append((token, "patronymic", 0))
                continue
            # **`Olai Plantin` is a patronymic and a family name, in that order.** Emma's own
            # `Q141312682` *Zacharias Olai Plantin* carries both in `_MARNM`, and without this
            # the Latin genitive became a second `P734`.
            if not shape and latin_patronymic(token, father_given):
                out.append((token, "patronymic", 0))
                continue
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
    tokens = join_particles([t for t in re.split(r"\s+", cleaned.strip()) if t])
    if not tokens:
        return []

    # A single token is a GIVEN name, not a family name. `Amaterasu`, `Ninigi`,
    # `NN` -- a mononym is a forename, and calling it a surname would put a personal
    # name in `P734` and leave the person with no `P735` at all. A family name needs
    # something in front of it to be the family name OF.
    if len(tokens) == 1:
        return [(tokens[0], "patronymic" if is_patronymic(tokens[0]) else "given",
                 0 if is_patronymic(tokens[0]) else 1)]

    out: list[tuple[str, str, int]] = []
    last = tokens[-1]
    family = last if not is_patronymic(last) else None
    body = tokens[:-1] if family else tokens

    ordinal = 0
    for token in body:
        if is_patronymic(token):
            out.append((token, "patronymic", 0))
        else:
            ordinal += 1
            out.append((token, "given", ordinal))
    if family:
        out.append((family, "family", 0))
    return out


def statements_for(label, plan, geni_id, father_qid=None, fields=None,
                   sex="", father_name="", father_aka="", father_given=""):
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

    # **A title never reaches the plan, whichever path builds the tokens.** `Queen of Sweden`
    # lives in Geni's `NSFX` and only becomes a name because the rendered label concatenates
    # it; `surn` picks up its tail the same way. Trimming both here rather than at the callers
    # is `CLAUDE.md` § *Code that is WRITTEN but never CALLED* -- there are two emitters and
    # they have disagreed before.
    # **The TITLE half of the suffix goes first, then the title PHRASE.** `NSFX` is where Geni
    # puts a title, and `build-display-names.py` concatenates it into the rendered name, so a
    # caller that has the field can say exactly which trailing token came from there.
    # `drop_title_tail` cannot: it sees one string with no field boundaries.
    if fields and fields.get("nsfx"):
        label = drop_name_suffix(label, fields["nsfx"])
    label = drop_title_tail(label)
    if fields:
        fields = dict(fields)
        for _f in ("givn", "surn", "marnm"):
            if fields.get(_f):
                if fields.get("nsfx"):
                    fields[_f] = drop_name_suffix(fields[_f], fields["nsfx"])
                fields[_f] = drop_leading_territorial(
                    drop_leading_title(drop_title_tail(fields[_f])))
        # **`father_name` is what turns a `-sen` token into the right kind of statement.**
        # Emma's test: the same token as the father means an inherited surname (`P734`), a
        # stem matching the father's GIVEN name means a patronymic (`P5056`). Without it the
        # morphology alone decides, which is what every caller did until 2026-08-27 and is
        # still the answer when the father is unknown.
        tokens = classify_fields(fields.get("givn", ""), fields.get("surn", ""),
                                 fields.get("nick", ""), fields.get("marnm", ""),
                                 father_name=father_name, father_aka=father_aka,
                                 father_given=father_given)
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
    # **The `NICK` FIELD is not a nickname and never takes the surname.** Emma,
    # 2026-09-04, on `Carolina Gustafsdotter Wittfooth`: *"This persons last name is
    # re[pe]ated twice in a mul alias"* -- the item went out carrying
    # `Amul "Wittfoth Wittfooth"`. Her record is `NICK Karolina`, `NICK Wittfoth`,
    # `SURN Wittfooth`, `_MARNM Wittfooth`: the `NICK` holds an alternate SPELLING of the
    # surname, so appending the surname spells it twice.
    #
    # `classify_fields` gives both sources the usage `nickname` and this function could
    # not tell them apart. They are different things, and the census says so --
    # 152,447 name records carry a `NICK` and the field is overwhelmingly Geni's *also
    # known as*, an alternate NAME rather than a byname: `Sally Miller`,
    # `Bethiah Lathrop`, `Rebecca Kaplan`, `Thorbjørn Lekve Magelssen`,
    # `Ludvig II Änkyttäjä`, `Jägerhorn af Spurila`. Every one of those reads correctly
    # on its own and badly with a surname stapled on.
    #
    # **Emma's own case is the OTHER source and is untouched.** `Q141189102` is
    # `GIVN 'Sigrid "Sally" Manilva'`, `SURN Tunheim`, `_MARNM Ekman` -- and her `nick`
    # column is EMPTY. `Sally` is a quoted token inside `GIVN`, which is a genuine byname
    # and is not findable bare, so it still becomes `Sally Ekman`; that is what
    # `CLAUDE.md` § *A nickname alias carries the SURNAME* is about and it still holds.
    #
    # The `endswith` guard stays on the quoted path. It was written for the doubling in
    # the `NICK` field -- 18,759 of 139,080 nickname aliases, 13% -- and matching on the
    # SOURCE rather than on the string catches the variant spellings it could not:
    # `Eccleston` against `Eggleston`, `Monradi` against `Monrad`, `Slason` against
    # `Slawson`. A similarity threshold would have been the other way to reach those, and
    # this repo does not have one.
    surname = " ".join((married_name_of({"marnm": marnm}) or surn or "").split())
    quoted = {(m.group("token") or m.group("apos") or m.group("paren")).strip()
              for m in QUOTED.finditer(fields.get("givn", "") or "")}
    for token, usage, _ordinal in tokens:
        if usage == "nickname":
            bare = token.strip()
            if bare not in quoted:
                full = bare
            elif surname and bare.casefold().endswith(surname.casefold()):
                full = bare
            else:
                full = f"{bare} {surname}".strip()
            if full and full not in out:
                out.append(full)
    married = married_name_of(fields)
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
