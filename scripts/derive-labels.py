"""Plan item 1 — derive labels from the GEDCOM, and catalogue what we have.

Emma, 2026-08-12: *"First thing is deriving labels from gedcom. Something that's
very easy."* And: *"Every individual needs an English, Japanese, and Chinese
label but really we gotta catalogue these things a bit better too as a bulk
operation."*

So this does both halves: derives what the rules already settle, and counts what
is present per person so the cataloguing is a measurement rather than a guess.

**The rules applied, each one hers and quoted where it was given:**

* The label is the `NAME` line **rendered** — slashes removed. GEDCOM 5.5.1 puts
  the name in spoken order with the surname in slashes, and says systems must
  construct from this line rather than from the pieces.
* **Group by script, never by language.** *"We are sorting by scripts. We are not
  sorting by languages. We will sort by languages later."*
* **The Latin-alphabet name becomes both the `mul` and the `en` label**, with any
  noble suffix left in: *"a noble suffix or a noble particle is a legitimately
  common thing in English."*
* **A lone `.` means the field is absent.** *"If the surname is just a single dot
  … we just pretend it doesn't exist because that is the convention on Geni."*
* **`_MARNM` identical to `SURN` is ignored.**
* **A differing `_MARNM` produces an alias.** *"Married name plugs into name to
  produce an alias."*

**What is deliberately not done.** No Japanese/Chinese split — that needs the
cataloguing this script produces, and guessing it from codepoints alone would
mis-assign Han characters shared by both. No name items are resolved: they are
*derived, never created*, and resolving a string to an existing item needs the
download that has not run.

Writes `reports/derived-labels.csv` (one row per person) and
`reports/labels.md`. Offline; reads `reports/display-names.csv`.

    py scripts/derive-labels.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from namemodel import (  # noqa: E402
    married_name_of, normalise_generation_suffix, without_nickname,
)
from labels import (  # noqa: E402
    drop_marker_surname, label_for, normalise_marker_spelling, strip_wedged_marker,
    is_description, mul_for_description)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

SOURCE = REPO_ROOT / "reports" / "display-names.csv"
OUT_CSV = REPO_ROOT / "reports" / "derived-labels.csv"
OUT_MD = REPO_ROOT / "reports" / "labels.md"
#: Emma's scratchpad. Holds identities and corrections no query here can produce.

csv.field_size_limit(10_000_000)

#: Scripts that carry Han characters. Kept as one bucket on purpose: telling
#: Japanese from Chinese is the cataloguing question, not a codepoint question.
CJK_SCRIPTS = {"Han", "Hiragana", "Katakana", "Hangul", "Ideographic"}

#: A name field holding only this means "absent", by Geni convention.
ABSENT = {".", "..", "?", "-", "_"}


def script_group(scripts: str) -> str:
    """`Latin`, `CJK`, `mixed`, `other`, or `none` — never a language."""
    if not scripts:
        return "none"
    parts = set(scripts.split("+"))
    has_latin = "Latin" in parts
    has_cjk = bool(parts & CJK_SCRIPTS)
    others = parts - {"Latin"} - CJK_SCRIPTS
    if has_latin and has_cjk:
        return "mixed"
    if has_cjk:
        return "CJK"
    if has_latin and not others:
        return "Latin"
    if has_latin and others:
        return "mixed"
    return "other"


#: Everything that is not a letter, a digit or a space. Used only to ask whether two renderings
#: of a name differ ONLY in punctuation; nothing is ever emitted through it.
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def _bare(text: str) -> str:
    """The name with punctuation removed, case KEPT. See the note at its call site."""
    return " ".join(_PUNCT.sub(" ", text or "").split())


def clean(text: str) -> str:
    """Drop tokens that Geni uses to mean 'no value', per Emma's dot rule."""
    return " ".join(t for t in text.split() if t not in ABSENT)


def alias_from_married_name(givn: str, marnm: str, nsfx: str) -> str:
    """The married name plugged into the name.

    Emma: *"Married name plugs into name to produce an alias."* Read as: the
    married name takes the surname's place in the rendered name. `Judith
    /de France/` carrying `_MARNM Flandre` gives `Judith Flandre`.

    **This reading is an interpretation of one sentence** and is flagged as such
    in `reports/labels.md` rather than presented as settled.
    """
    # **A daughter-form `_MARNM` is the person's own patronymic, not a married name**, and
    # flipping onto it replaces a real surname with a `-dotter` form. Emma pointed at
    # `Q136376387`, whose `mul` she has as `Ebba Kristina Siöblad` where ours read
    # `Ebba Kristina Carlsdotter`. `namemodel.DAUGHTER_PATRONYMIC` is the reasoning and the
    # census: 2,483 people have a real `SURN` replaced this way.
    marnm = married_name_of({"marnm": marnm})
    if not marnm:
        return ""
    parts = [clean(givn), clean(marnm), clean(nsfx)]
    return " ".join(p for p in parts if p)


def main() -> int:
    # A Geni export is a snapshot. A profile renamed afterwards keeps its old
    # name in every GEDCOM already taken, and no amount of re-parsing fixes it —
    # only a correction recorded by hand can. Applying it here, at derivation,
    # leaves the exports untouched as the record of what Geni actually said.
    #
    # **But nothing replaced it, so a correction of hers had nowhere to go.** This dict sat
    # empty from that deletion until 2026-09-04, when Emma said of `Q141283774`: *"Name should
    # be … Jacobus Bothniensis"*. Geni records him as `Jakob` and no re-derivation can produce
    # anything else; only a recorded correction can. `reports/label-corrections.tsv` is that
    # file -- tracked, one row per person, carrying who said it and why.
    #
    # It is applied HERE, at derivation, so the exports stay the record of what Geni actually
    # said and every one of the 48 readers of `label_en`/`label_mul` sees the corrected form.
    # The superseded name is not erased: it stays visible in `further_latin_names`.
    corrected: dict[str, str] = {}
    corrections_path = REPO_ROOT / "reports" / "label-corrections.tsv"
    if corrections_path.exists():
        with open(corrections_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                gid, label = (row.get("geni_id") or "").strip(), (row.get("label") or "").strip()
                if gid and label:
                    corrected[gid] = label
        print(f"{len(corrected):,} hand-recorded label corrections")

    # **Farm-name abbreviations, expanded only where the corpus attests the full form.** Emma,
    # 2026-09-04, on `Q141216388` *Jon Hansson St. Vatne*: *"I think in this one St. Stands for
    # Store"*, and *"St. Gives a misinpression"* -- it reads as *Saint*. `Store Vatne` is written
    # out 42 times in this tree, so the corpus settles it; `St. Laurent` and `St. Leger` are left
    # alone because `Store Laurent` is attested nowhere. `scripts/build-farm-abbreviations.py`
    # writes the table and carries the reasoning.
    farm: dict[str, str] = {}
    farm_path = REPO_ROOT / "reports" / "farm-abbreviations.tsv"
    if farm_path.exists():
        with open(farm_path, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                farm[row["abbreviated"]] = row["expanded"]
        print(f"{len(farm):,} attested farm-name abbreviations")

    def expand_farm(text: str) -> str:
        for short, full in farm.items():
            if short in text:
                text = text.replace(short, full)
        return text
    by_person: dict[str, list[dict]] = defaultdict(list)
    with open(SOURCE, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            by_person[row["geni_id"]].append(row)

    print(f"{len(by_person):,} people", flush=True)

    groups: Counter[str] = Counter()
    coverage: Counter[str] = Counter()
    alias_count = 0
    corrections_applied: list[str] = []
    rows = []

    for geni_id, records in by_person.items():
        labels: dict[str, list[str]] = defaultdict(list)
        aliases: list[str] = []
        qid = records[0]["qid"]
        wd_en = records[0]["wikidata_en"]
        wd_mul = records[0]["wikidata_mul"]

        for record in records:
            rendered = clean(record["display_name"])
            if not rendered:
                continue
            group = script_group(record["scripts"])
            groups[group] += 1
            if rendered not in labels[group]:
                labels[group].append(rendered)

            surn = clean(record["surn"])
            marnm = clean(record["marnm"])
            # Identical means ignore it — 31% of the corpus's _MARNM records.
            if marnm and marnm != surn:
                alias = alias_from_married_name(record["givn"], marnm, record["nsfx"])
                if alias and alias != rendered and alias not in aliases:
                    aliases.append(alias)

        # `en` and `mul` come from a *strictly* Latin name. A mixed Latin+CJK
        # string is not a usable English label — it carries CJK characters — and
        # falling back to it was a defect in the first version of this script:
        # it admitted 4,990 more people and gained 8 exact matches against
        # Wikidata, which is what gave it away.
        latin = labels.get("Latin") or []
        mixed = labels.get("mixed") or []

        # A hand-recorded correction outranks every name in the export, and goes
        # to the front rather than replacing the list: the stale names stay
        # visible in `further_latin_names` instead of being erased.
        correction = corrected.get(geni_id)
        if correction:
            latin = [correction] + [n for n in latin if n != correction]
            corrections_applied.append(geni_id)
        cjk = labels.get("CJK") or []
        other = labels.get("other") or []
        if aliases:
            alias_count += 1

        if latin and cjk:
            coverage["Latin and CJK"] += 1
        elif latin:
            coverage["Latin only"] += 1
        elif cjk:
            coverage["CJK only — needs translation for en"] += 1
        elif mixed:
            coverage["mixed-script only — no clean Latin label"] += 1
        elif other:
            coverage["other script only — needs translation for en"] += 1
        else:
            coverage["no usable name at all"] += 1

        # **THE MARRIED NAME IS THE PRIMARY LABEL. The birth name is an alias.**
        #
        # Emma, 2026-08-29: *"I don't know what I actually even want to use the birth names
        # of the women here. I feel like the only thing that I think has any business
        # actually using the birth name is the alias thing and certain things specifically
        # related to attaching names, like attaching the birth name vs. the surname."*
        # And: *"the pipeline is so broken with married names right now that it's kind of
        # worth just doing any of this stuff."*
        #
        # This file used to emit the BIRTH form as `label_en`/`label_mul` and push the
        # married form into an alias column -- 251,707 people, 185,426 of them women. That
        # is backwards from `CLAUDE.md` § *The MARRIED name is the real name*, and it made
        # this file disagree with `build-garborg-day.py`, which recomputes from raw
        # `SURN`/`_MARNM` and had it right: one run created a woman as
        # `Thelma Geraldine Bagby` while calling a man "husband of Mona Beth Tunheim".
        #
        # **It also fixes the CJK complaint, which was the same bug wearing a hat.** The
        # `ja`/`zh` labels are transliterated from `label_mul`, so every woman was being
        # rendered into Japanese and Chinese under her BIRTH name. Nothing about the
        # transliterator was wrong; it was handed the wrong string.
        #
        # **A hand correction still outranks everything.** `reports/label-corrections.tsv` carries
        # names nothing here could reconstruct, and § *Emma edits the tree BY HAND* makes
        # those decisions rather than drift -- so a corrected name stays primary and the
        # married form, if any, stays an alias beside it.
        # **Strip the nickname from the LABEL here, at the source.** `CLAUDE.md`
        # § *A nickname alias carries the SURNAME*: *"quotes never go in a label"*.
        # `without_nickname` used to live in `build-garborg-day.py` and was applied at the
        # point of emission, so this file kept `Ingvold (Pinkie) Remmie` and **all 48 readers
        # of `label_en`/`label_mul` saw the bracketed form** -- 21,550 of them. Fixing it at
        # source is what the married-name flip did, for the same reason.
        #
        # It reads the `GIVN` field, never the rendered label, so a parenthesised *surname*
        # is untouched: `Katarina Magnusdotter (Aspenäs)` keeps its brackets because they are
        # in `SURN`, and `Jean d'O Seigneur d'O` keeps its apostrophes.
        # **Every record's `GIVN`, not the first.** A person can carry several `NAME`
        # records and some hold no fields at all -- `1554340` has one record that is a bare
        # display string with an empty `givn` and a second that carries
        # `Wilhelmina (Mina) Eva Christina`. Reading only `records[0]` left 8,214 labels
        # bracketed, including that one, because the nickname lived in the record the label
        # did not come from.
        givns = [r["givn"] for r in records if (r["givn"] or "").strip()]

        def strip_nick(text):
            for givn in givns:
                text = without_nickname(text, {"givn": givn})
            return text

        latin = [strip_nick(x) for x in latin]
        aliases = [strip_nick(x) for x in aliases]

        # **Normalise the unknown-name marker HERE, at the source, for the same reason the
        # nickname strip moved here.** `scripts/labels.strip_markers` has produced `NN` from
        # `nn`, `N.N.`, `unknown`, `ukjent`, `某` and `dødfødt` since 2026-08-27, and nothing in
        # this file ever called it -- so `derived-labels.csv` carried `nn Gunnarsdatter Frafjord`
        # and every reader downstream saw it. The label-correction pass could not fix those two
        # live items either, because it fires when our label differs from Wikidata's and ours
        # *was* the mangled form.
        #
        # **`normalise_marker_spelling`, not `strip_markers`, and the difference is 94,231
        # people.** The unscreened call also turns `Private` and `<private>` into `NN`, which is
        # a redaction decision Emma has twice corrected an attempt to settle. The screened one
        # changes **8,053** labels, every one a marker spelled inconsistently.
        latin = [normalise_marker_spelling(x) for x in latin]
        aliases = [normalise_marker_spelling(x) for x in aliases]

        # **Then remove a marker wedged INSIDE a name**, which is the second of the three marker
        # populations and the only mechanical one — her words: *"strip the marker, keep the rest…
        # mechanical, no judgement."* `Hadaburg NN Gräfin im Saalgau` → `Hadaburg Gräfin im
        # Saalgau`, `Viki (Unknown)` → `Viki`.
        #
        # **Order matters and this must come second.** `normalise_marker_spelling` regularises the
        # spelling first, so `n.n.` and `N.N.` are already `NN` when this looks for whole tokens.
        #
        # It never touches a HEAD marker — that is population one, `unknown Bloomfield` →
        # `mul: NN Bloomfield`, which decides what the person is called and is Emma's ruling to
        # make. `reports/marker-label-normalisation.tsv` is the report of what this does.
        latin = [strip_wedged_marker(x) for x in latin]
        aliases = [strip_wedged_marker(x) for x in aliases]

        # **A redaction marker is not a label, and this file was emitting one as the primary.**
        # Emma, 2026-08-29, asked why `geni.com/people/private/6000000021223635839` "was added
        # as Garborg" instead of the labels she had hand-added to `Q141199845`. The answer is
        # here: this file took `clean(display_name)` and never called `labels.label_for`, which
        # `CLAUDE.md` § *Redacted people go in* calls **the single place that decides this** and
        # which returns `''` for `Private` and `<private>`. So `<private> /Garborg/` came out as
        # the literal label `<private> Garborg` -- for **14,449 people**, 12 of whom already had
        # items, several of them hers.
        #
        # That is the *"logic that never gets in"* pattern in its purest form: the decider
        # existed, was correct, was documented as authoritative, and the generator feeding every
        # label emitter did not call it.
        #
        # **This drops the marker; it does not decide the `NN` question.** Emptying the label is
        # exactly what `label_for` does and is her stated rule -- an item labelled `<private>`
        # *"asserts something false while being impossible to find"*. Whether the person then
        # reads `NN Garborg` is `build-placeholder-label-batch.py`'s job, which already handles
        # this population and already keeps the surname. `normalise_marker_spelling` is left
        # alone: whether a redaction marker BECOMES `NN` is a decision she has corrected twice
        # and it stays hers.
        latin = [drop_marker_surname(x) for x in latin if label_for(x)]
        aliases = [drop_marker_surname(x) for x in aliases if label_for(x)]

        # The abbreviation is expanded last, so it applies to whatever survived the marker
        # handling above and to the married-name aliases alike.
        if farm:
            latin = [expand_farm(x) for x in latin]
            aliases = [expand_farm(x) for x in aliases]

        birth = latin[0] if latin else ""
        married = aliases[0] if aliases else ""

        # **A RECONSTRUCTION never overrules a RECORDED rendering of the same name.** The
        # married-name flip is built from `GIVN + _MARNM + NSFX`, so any punctuation Geni put
        # in the `NAME` line is lost -- Emma, 2026-09-04: *"Idk why the comma was actively
        # dropped before the ordinal"*. `Q141223436` is recorded
        # `Tore Underberge, III` and went out as `Tore Underberge III`; she has since set both
        # `en` and `mul` back to the comma form by hand, which is what fixes the reading.
        #
        # Where the flip and a recorded name are the same tokens differing only in
        # punctuation, the recorded one is the evidence and wins. **2,254 people**, and the
        # damage runs both ways: `Inger Marie Dyster-Aas` was losing its hyphen while
        # `Alana Chinn fung` was gaining a slash the `NAME` line does not have.
        #
        # **Case is not punctuation and is not folded here.** Folding it would hand
        # `Ethel Violet Gale` back as the recorded `Ethel violet gale`.
        if married:
            same = next((d for d in latin if _bare(d) == _bare(married) and d != married), None)
            if same:
                married = same
        if correction or not married:
            primary, alias_out = birth, list(aliases)
        else:
            primary = married
            alias_out = ([birth] if birth else []) + aliases[1:]

        # **A description is not a name, so `mul` gets `NN` and the description stays in `en`.**
        # Emma, 2026-08-17: *"And NN for mul there"* — plus the real surname where the description
        # leaves one standing, `謝氏` → `NN 謝`, `信秀正室 織田` → `NN 織田`.
        #
        # **The surname is only taken when it is HERS.** `Wife of William Ryves` gets a bare `NN`,
        # because `William Ryves` is her husband; `織田敏信娘` likewise, because those characters
        # are her father. `labels.mul_for_description` is the one place that knows the difference.
        mul_label = mul_for_description(primary) if is_description(primary) else primary

        # **`mul` takes the Roman numeral and `en` the English abbreviation.** Emma, 2026-09-04,
        # on `Q106206114`, whose Wikidata label is `Elias Lagerheim den yngre`:
        #
        #     Lmul  Elias Lagerheim II
        #     Len   Elias Lagerheim Jr.
        #
        # *"the local language version should not be used"* — `d.y.`, `den yngre` and `nuorempi`
        # are Swedish and Finnish and belong in neither a language-neutral label nor an English
        # one. `namemodel.GENERATION_SUFFIX` carries the forms and the reasoning.
        #
        # This is also why the two columns can now differ where they used to be the same string.
        primary = normalise_generation_suffix(primary, "en")
        mul_label = normalise_generation_suffix(mul_label, "mul")

        rows.append([
            geni_id,
            qid,
            # en keeps the description — it is real information and already in the right slot.
            primary,
            mul_label,
            " | ".join(latin[1:]),
            " | ".join(cjk),
            " | ".join(other + mixed),
            " | ".join(alias_out),
            len(records),
            wd_en,
            wd_mul,
            "yes" if (wd_en and primary and wd_en == primary) else "no",
        ])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "geni_id", "qid", "label_en", "label_mul", "further_latin_names",
            "cjk_names", "other_script_names", "alias_names",
            "name_records", "wikidata_en", "wikidata_mul", "matches_wikidata_en",
        ])
        writer.writerows(rows)

    total = len(by_person)
    L: list[str] = []
    add = L.append
    add("# Derived labels, and the catalogue behind them")
    add("")
    add("Plan item 1. Emma, 2026-08-12: *\"First thing is deriving labels from gedcom.")
    add("Something that's very easy.\"* And: *\"Every individual needs an English,")
    add("Japanese, and Chinese label but really we gotta catalogue these things a bit")
    add("better too as a bulk operation.\"*")
    add("")
    add(f"One row per person in `reports/derived-labels.csv` — **{total:,} people**.")
    add("")
    add("## What each person has to build a label from")
    add("")
    add("| | people | share |")
    add("| --- | ---: | ---: |")
    for kind, n in coverage.most_common():
        add(f"| {kind} | {n:,} | {100.0*n/max(total,1):.1f}% |")
    add("")
    add("**This is the catalogue.** The `en` and `mul` labels come from the Latin name,")
    add("so everyone in a *needs translation* row has no derivable English label at all —")
    add("that is the population Emma's *\"if there's only a name present in some sort of")
    add("other script, we have to do a translation\"* applies to, sized.")
    add("")
    add("## Name records by script group")
    add("")
    add("| script group | name records |")
    add("| --- | ---: |")
    for group, n in groups.most_common():
        add(f"| {group} | {n:,} |")
    add("")
    add("Grouped by **script, never language** — her rule. `CJK` deliberately holds Han,")
    add("Hiragana, Katakana and Hangul together: **the Japanese/Chinese split is not")
    add("attempted here**, because Han characters are shared and a codepoint test would")
    add("mis-assign them. That split is what the cataloguing is *for*, and it needs a")
    add("decision rather than a rule.")
    add("")
    add(f"## Aliases from married names — {alias_count:,} people")
    add("")
    add("Emma: *\"Married name plugs into name to produce an alias.\"*")
    add("")
    add("**Read as:** the married name takes the surname's place in the rendered name, so")
    add("`Judith /de France/` carrying `_MARNM Flandre` yields the alias `Judith Flandre`.")
    add("A `_MARNM` identical to `SURN` is ignored, per her earlier rule, which is 31% of")
    add("the 244,392 records carrying the tag.")
    add("")
    add("**That reading is an interpretation of one sentence and is flagged rather than")
    add("settled.** The alternative — appending the married name to the full rendered")
    add("name — produces a different string, and nothing she has said chooses between")
    add("them.")
    add("")
    add("## Against Wikidata, where both exist")
    add("")
    matched = sum(1 for r in rows if r[11] == "yes")
    have_both = sum(1 for r in rows if r[9] and r[2])
    add(f"{have_both:,} people have both a derived Latin label and a Wikidata English")
    add(f"label. **{matched:,} match exactly ({100.0*matched/max(have_both,1):.1f}%).**")
    add("")
    add("`reports/display-names.md` has the breakdown of the rest: the failures")
    add("concentrate in royalty, where Geni holds the native birth name and Wikidata the")
    add("English regnal form, and a perfect oracle picking among a person's Latin names")
    add("reaches only 26.8%. Deriving the label is easy; the derived label disagreeing")
    add("with Wikidata's is the normal case, not the exception.")
    add("")
    if corrections_applied:
        add(f"## Name corrections applied — {len(corrections_applied)}")
        add("")
        add("A Geni export is a snapshot: a profile renamed afterwards keeps its old name")
        add("in every GEDCOM already taken. `reports/label-corrections.tsv` records the")
        add("name by hand, and it is applied **here, at derivation** — the exports stay")
        add("untouched as the record of what Geni actually said, and the superseded name")
        add("stays visible in `further_latin_names` rather than being erased.")
        add("")
        add("| geni | corrected to |")
        add("| --- | --- |")
        for gid in corrections_applied:
            add(f"| `{gid}` | {corrected[gid]} |")
        add("")
    add("## Not done here")
    add("")
    add("- **No Japanese/Chinese split.** Needs the catalogue above plus a decision.")
    add("- **No name items resolved.** They are *derived, never created* — and resolving")
    add("  a string to an existing item needs the download that has not run.")
    add("- **Nothing emitted to Wikidata.** This is ingestion.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")
    print(f"wrote {OUT_MD}")
    print()
    for kind, n in coverage.most_common():
        print(f"  {n:>8,}  {kind}")
    print(f"\n  {alias_count:,} people gain an alias from a married name")
    print(f"  {matched:,} of {have_both:,} derived labels match Wikidata's exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
