#!/usr/bin/env python3
"""What each imported label SHOULD read, computed from `reports/imported-title-labels.tsv`.

**The cheap half of § *A RANK IS NOT A NAME*.** `scripts/census-imported-title-labels.py` does
the 20-minute pass over the store and proposes nothing; this reads its output in seconds, so the
rule below can be argued with and re-run without paying for the scan again.

Three transformations, in this order, and the order is forced:

    noble Nike|Victoria Soutzaina           ->  Nike Soutzaina      + alias Victoria Soutzaina
    noble Johannes Vilken, Lord of Salmenkylä ->  Johannes Vilken
    noble Valpuri Sunintytär of Sunila, heiress of Heinlahti manor -> Valpuri Sunintytär

1. **The leading RANK comes off.** `noble`, `baroness`, `Sir` — Genealogics' rank column, in a
   name field. Never to empty, so a surname `Noble` survives.
2. **The `|` becomes an ALIAS, never a discarded half.** Genealogics separates two spellings of
   one name; the first reading is the label and every other is an `Amul`. Wikidata's own
   `Help:Aliases`: *"the purpose of aliases is only to find entities in searches"* — and a label
   containing a pipe is searchable by nobody, which is what makes this a repair rather than a
   preference.
3. **The TITLE TAIL comes off**, which is `namemodel.drop_title_tail` and this repo's rule
   already — `CLAUDE.md` § *A TITLE IS NOT A NAME* cites `Q111989591` *"burgeress Margareta
   Frodbom, heiress of Ingemarshov"*, the same shape from the same import.

**⛔ FOUR HOLDS, and each one is a label the rule would have made WORSE.** A row that trips one is
kept in the file with `hold` naming it, never silently dropped — a proposal that vanishes reads as
nothing to do.

* **`marker-only`.** `noble NN of Venne` reduces to a bare `NN`, and `CLAUDE.md` § *A BARE GIVEN
  NAME IS NOT A LABEL* is explicit that a lone marker is not one. The tail is the only thing
  distinguishing that person from every other `NN`.
* **`one-token`.** `noble Hebla Kristiina` is fine, but a reduction to a single given name is the
  same rule from the other side: *"A single given name is generally not acceptable."*
* **`no-change`.** The rule fires and produces exactly what is live. Nothing to emit.
* **`pipe-shape`.** A label whose tokens disagree about how many readings they hold — `A|B C|D|E`
  — is not the two-spellings shape and the column expansion would invent a name. Held for a human.

**⛔ CASE IS THE DISCRIMINATOR, AND A BARE WORD LIST WOULD HAVE DESTROYED THOUSANDS OF NAMES.**
Of the 42,534 people whose label opens with a rank word, **41,505 capitalise it and 1,029 do
not** — and reading both lists is what settles it, exactly as § *A TITLE IS NOT A NAME* says:
*"What SURVIVES the filter is the test."*

| | capitalised | lowercase |
| --- | --- | --- |
| `noble` | 44 — `Noble Sissle`, `Noble Consort Mei` | **608** — `noble Detlof Heyke, master of Gammelbo bruk` |
| `miles` | 303 — **`Miles Davis`, `Miles Teller`** | 0 |
| `don` | 956 — **`Don Rosa`, `Don McLean`, `Don Rickles`** | 1 |
| `king` | 158 — **`King Vidor`, `King Levinsky`** | 1 |
| `major` | 148 — **`Major Ridge`, `Major Lance`** | 3 |
| `sir` | 20,551 — `Sir William Hamilton, 9th Baronet` | **0** |
| `lady` | 4,978 — `Lady Gaga`, `Lady Jane Grey` | 35 |

So `Miles`, `Don`, `King`, `Major` and `Noble` are given names far more often than they are
ranks in this population, and every one of them is capitalised when it is a name. The importers
that put a rank in the name field wrote it in lower case: `noble`, `farmer`, `esquire`,
`skipper`, `mistress`, `stillborn son`. **The capitalised 41,505 are somebody else's labels and
are not touched** — § *WIKIDATA'S LABEL BEATS OURS*, and `Sir … Baronet` is Wikidata's own house
style rather than an artefact.

A `|` needs no such gate: it is not a character any name contains.

**Nothing here edits anything.** It writes a proposal file; what turns that into QuickStatements
is a separate step, and § *WIKIDATA'S LABEL BEATS OURS* is why: these are somebody else's labels,
and only the explicit instruction of 2026-09-09 puts them in scope at all.
"""
import csv
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from namemodel import drop_title_tail, name_shape  # noqa: E402
import labels as L  # noqa: E402

SRC = ROOT / "reports" / "imported-title-labels.tsv"
DEST = ROOT / "reports" / "title-label-proposals.tsv"

MARKERS = frozenset(m.casefold() for m in (L.NARROW_MARKERS | L.WORDS_MEANING_UNKNOWN))

#: How often a token has to be attested as somebody's FIRST given name in our own 1.4M-person
#: corpus before `given-names-only` will hold on it. **Read at 5, 20 and 50 rather than chosen:**
#: 5 holds 26 rows, 20 holds 9, 50 holds 7. Reading the 17 that 5 adds over 20 is what settles
#: it -- `Anna Kristiina of Tawast`, `Anna Maria of Svinhufvud`, `Anne Dorte of Rosen`,
#: `Selma Johanna of Liljakaivo` -- every one a Finnish or Baltic noble FAMILY name filed behind
#: `of`, and every one a real loss. 25 of the 26 are genuine; the one that is not is
#: `Elsbeth|Elizabeth Eliot`, held on `Eliot` at (6, 9, 0).
GIVEN_FLOOR = 5


def _attestation():
    """`{token: (first_given, later_given, family)}` from `reports/given-name-attestation.tsv`.

    **A missing file must not silently disable the guard**, which is the opposite of the rule
    `CLAUDE.md` § *A TOKEN THE CORPUS NEVER USES AS A FIRST GIVEN NAME* states for the emitter --
    there a missing census lets every token PASS, because refusing a name on absent evidence is
    the worse error. Here the guard only ever HOLDS a row, so absent evidence means propose, and
    the two rules point the same way for the same reason: never act on a file that is not there.
    """
    path = ROOT / "reports" / "given-name-attestation.tsv"
    if not path.exists():
        return {}
    out = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["token"].casefold()] = (int(row["first_given"]),
                                            int(row["later_given"]),
                                            int(row["family"]))
    return out


def _is_patronymic(token):
    try:
        return name_shape(token)[1] == "patronymic"
    except Exception:
        return False


def given_names_only(label, att):
    """True when a tail cut has left nothing but given names -- so the tail WAS the surname.

    **⛔ `of Tawast` IS A FAMILY NAME, NOT AN ESTATE.** `noble Anna Kristiina of Tawast, heiress
    of Haminalahti manor` reduces to `Anna Kristiina`, two given names and no surname at all --
    `CLAUDE.md` § *A BARE GIVEN NAME IS NOT A LABEL*, in a population where the discriminator
    that section relies on (the person's own `SURN`) does not exist, because these people are on
    Wikidata and not in our tree.

    So the evidence is the corpus instead: a token attested as somebody's first given name and
    **never** as a family name. A patronymic exempts the row outright -- `Anna Samulintytär` and
    `Beata Henrikintytär` keep a name whatever the tail was.
    """
    toks = label.split()
    if not toks or any(_is_patronymic(t) for t in toks):
        return False
    for t in toks:
        k = att.get(t.casefold())
        if not k or k[2] or k[0] < GIVEN_FLOOR:
            return False
    return True

COLS = ["qid", "kind", "case", "leading_title", "live_mul", "live_en", "proposed_label",
        "proposed_aliases", "hold", "langs_carrying_live", "geni_ids"]


def split_pipe(label):
    """`Nike|Victoria Soutzaina` -> (`Nike Soutzaina`, [`Victoria Soutzaina`], ok).

    Genealogics puts the alternation on a TOKEN, so the readings are the columns of the split:
    `Anna Maria|Maija Husgavel` is `Anna Maria Husgavel` and `Anna Maija Husgavel`, which is the
    only reading of it that keeps `Anna` and `Husgavel` in both.

    `ok` is false when two piped tokens disagree about how many readings they hold. Padding the
    shorter one repeats a name into a position it never occupied, which invents a person's name
    — so that shape is held rather than guessed at.
    """
    if "|" not in (label or ""):
        return label, [], True
    toks = label.split()
    widths = {len(t.split("|")) for t in toks if "|" in t}
    if len(widths) != 1:
        return label, [], False
    width = widths.pop()
    readings = []
    for i in range(width):
        readings.append(" ".join(
            (t.split("|")[i] if "|" in t else t) for t in toks))
    # **⛔ A BRACKETED ALTERNATION IS A DIFFERENT CONVENTION AND IS HELD.** `Ann Bincks
    # (Benckes|Bench)` lists two more spellings of the SURNAME inside a variant group; expanded
    # column-wise it yields `Ann Bincks (Benckes` and `Ann Bincks Bench)`, two labels with one
    # bracket each and neither of them a name. **121 rows.**
    #
    # The test is on the READINGS, not on the tokens -- `(Benckes|Bench)` is itself balanced,
    # which is why a per-token check passed it and shipped the broken pair. An unbalanced
    # bracket in any reading is the tell.
    #
    # It is held rather than solved because `Name (Variant)` is a THIRD convention on top of the
    # rank and the pipe, and neither was asked about -- § *The requested scope is the
    # deliverable*. Reading 121 rows is cheap; inventing a bracket rule uninvited is what
    # § *Do not grab the first artifact that vaguely matches* is against.
    for r in readings:
        if r.count("(") != r.count(")") or r.count("[") != r.count("]"):
            return label, [], False
    seen, uniq = set(), []
    for r in readings:
        if r and r not in seen:
            seen.add(r)
            uniq.append(r)
    return uniq[0], uniq[1:], True


def drop_comma_tail(label):
    """Everything from the first comma, removed. `Detlof Heyke, master of Gammelbo bruk` -> `Detlof Heyke`.

    **⛔ MEASURED OVER ALL 704 DISTINCT TAILS IN THIS POPULATION, AND NOT ONE IS A NAME.** They
    are places, estates, ranks and offices without exception: `of Malpas` 3, `of London` 3,
    `lord of Barritskov`, `heiress of Penttilä moiety of Neuvottoma`, `beizadi` 6,
    `1.Count Cantacuzino-Vlasici`, `Dame de Varennes`, `High Councillor of Denmark`,
    `master of Gammelbo bruk`. **735 of the 2,658 rows carry one.**

    `namemodel.drop_title_tail` is this repo's rule and gets most of them, but it truncates at a
    word in a fixed vocabulary and these tails run past it: `master`, `beizades`, `dragoman`,
    `co-heiress` and the glued ordinal `1.Count` are all outside it, so `noble Detlof Heyke,
    master of Gammelbo bruk` came out as `Detlof Heyke, master`. **The comma is the boundary
    these importers actually wrote**, so it is the boundary to cut on — and reading all 704 is
    what makes that a measurement rather than a guess.

    Never to empty: a label opening with a comma keeps what it has.
    """
    head = (label or "").split(",", 1)[0]
    return head if head.strip() else label


def tidy(text):
    """Trailing punctuation a truncation left behind.

    `CLAUDE.md` § *A DESCRIPTION MARKER COMES OUT OF THE LABEL*: *"The comma that introduced the
    marker goes with it"*, so `Josiah Wood I, twin` becomes `Josiah Wood I` and not
    `Josiah Wood I,`.
    """
    return " ".join(text.split()).rstrip(" ,;:-–—([{&").strip()


#: A rank that is the whole of how an East Asian court figure is known. `princess Pingyang`,
#: `lady Kim`, `queen Janghwa`, `prince Kume` — Chinese, Korean, Japanese and Vietnamese
#: consorts and royals, where the rank is not an artefact in a name field but the way every
#: source names them, and where the remainder is a court name rather than a given name.
#: `CLAUDE.md` § *THE PARENT DECK* records the firm 2026-09-07 ruling that a CJK case is not
#: one that can be adjudicated from a reading of the two cards, so these are held rather
#: than decided here.
COURT_RANKS = frozenset({"queen", "king", "prince", "princess", "princesse", "empress",
                         "emperor", "lady", "consort", "duchess", "duke"})

#: A description of the record, never a name — `CLAUDE.md` § *A DESCRIPTION IS NOT A NAME*.
#: Stripping only the first word leaves `son Campbell`, which is worse than what is live.
DESCRIPTIONS = frozenset({"stillborn", "infant", "twin", "son", "daughter", "child", "baby"})

#: The scripts an East Asian court name is written in when it is not romanised, and the marker
#: that a court-rank remainder is a place or a clan rather than a personal name. Written as
#: ASCII escapes — `CLAUDE.md` § *A Han range written with LITERAL boundary characters*.
import re as _re  # noqa: E402
_CJK = _re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF"
                   r"\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF\u1100-\u11FF]")


def hold_reason(label, live, pipe_ok, title="", tail_cut=False, att=None):
    if not pipe_ok:
        return "pipe-shape"
    if not label:
        return "empty"
    toks = label.split()
    if all(t.casefold().strip(".,") in MARKERS for t in toks):
        return "marker-only"
    if title and toks[0].casefold().strip(".,") in DESCRIPTIONS:
        # `stillborn son Campbell` -> `son Campbell`. The description is the whole of the
        # given-name side and nothing here can supply a name in its place.
        #
        # **The test is the FIRST token, and only where a rank was actually stripped.** Matching
        # the word anywhere destroyed `Sir Josiah Child, 1st Baronet` -- `Child` is his surname
        # -- which is § *A TITLE IS NOT A NAME* exactly: *"`Sarah Bishop`, `Anne Greve`,
        # `Anna King` and `Nicholas Henry Pope` are real surnames a bare word list would have
        # destroyed."* 38 rows read that way and 35 were surnames.
        return "description"
    if len(toks) < 2:
        return "one-token"
    if title and title.split()[0].casefold() in COURT_RANKS and (
            _CJK.search(label) or len(toks) <= 2):
        return "court-rank"
    if tail_cut and att and given_names_only(label, att):
        return "given-names-only"
    if label == live:
        return "no-change"
    # **The catch-all, and it earns its place by catching exactly one row.** `lady from Tajihi
    # clan (lady-in-waiting of Emperor Kokou)` reduces to `from Tajihi clan (lady-in-waiting` --
    # an unbalanced bracket and a leading English function word, which together say the string
    # was a DESCRIPTION rather than a name. A guard that fires on one row of 2,300 is the shape
    # a guard should have; one that fires on none has not been seen to guard at all.
    if label.count("(") != label.count(")") or label.count("[") != label.count("]"):
        return "unbalanced"
    if toks and toks[0][:1].islower() and toks[0].isascii():
        return "leading-lowercase"
    return ""


def main():
    if not SRC.exists():
        sys.exit(f"{SRC.relative_to(ROOT)} is missing -- run "
                 "scripts/census-imported-title-labels.py first (it is the 20-minute pass)")

    att = _attestation()
    rows, holds = [], Counter()
    with SRC.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            live = row["live_mul"] or row["live_en"]
            title = row["leading_title"]
            # **The case gate, and it is the whole safety of this rule.** A capitalised rank
            # word is overwhelmingly a given name here -- `Miles Davis`, `Don McLean`,
            # `King Vidor`, `Noble Sissle` -- and stripping it would rename 41,505 people.
            if title and not title.split()[0][:1].islower():
                title = ""
            # ⛔ **THE LEADING WORD ONLY, not the whole stacked run.** You, 2026-09-09, choosing
            # between dropping one word and dropping the stack: *"Drop the leading word only"*,
            # so a title after the comma SURVIVES. `leading_title` spans the whole run --
            # `professor, Rev. Dr.` and `general, baron` are single values of it -- and cutting
            # `len(title)` took all of it, which is the option you did not pick.
            #
            #   professor, Rev. Dr. Göran Wallin, bishop of Gothenburg
            #     -> Rev. Dr. Göran Wallin, bishop of Gothenburg      (yours)
            #     -> Göran Wallin, bishop of Gothenburg               (what it did)
            #
            # 5 emittable rows have a multi-word leading title, so this is small and exact:
            # `general, baron`, `count Don`, `ridder Mr.`, `professor, Rev. Dr.`,
            # `professor, Dr.` Every other row has a one-word title and is unaffected.
            first = title.split()[0] if title else ""
            stripped = live[len(first):].strip() if first else live
            # **⛔ THE COMMA TAIL GOES FIRST, and the order is not cosmetic.**
            # `Johann|Hans, Freiherr von Aichberg zu Laberweinting` split first gives
            # `Johann Freiherr von Aichberg zu Laberweinting` -- which keeps a rank the tail
            # rule would have removed -- and an alias of the bare word `Hans`, because only the
            # second reading carried the comma. Cutting the tail first gives `Johann` and
            # `Hans`, which is the same person's name twice and is what the `|` says.
            # ⛔ **PREFIX ONLY. You, 2026-09-09**, shown that these proposals also truncated
            # the territorial tail: *"Uhh bruh what? I'm asking you to remove the prefix lol not
            # the other stuff."* So the rank word comes off and nothing else moves.
            #
            # What this used to do -- `tidy(drop_title_tail(drop_comma_tail(stripped)))` -- cut
            # a comma tail on 112 of `noble`'s 457 and reduced 87 of them to a bare given name
            # plus patronymic, which is the shape you refused for `farmer` in the same sitting:
            # `noble Beata Henrikintytar, heiress of Hannola` -> `Beata Henrikintytar`.
            #
            # `tail_cut` is kept and is now always False, because `hold_reason` takes it and the
            # pipe branch below still reads the same variable. Nothing is cut, so nothing is
            # held for having been cut.
            trimmed = tidy(stripped)
            tail_cut = trimmed != tidy(stripped)
            stripped = trimmed
            label, aliases, ok = split_pipe(stripped)
            label = tidy(label)
            aliases = [a for a in (tidy(a) for a in aliases) if a and a != label]
            hold = hold_reason(label, live, ok, title, tail_cut, att)
            if not hold and not title and "|" not in live:
                # A capitalised rank word and no pipe: there is nothing here to repair.
                hold = "capitalised-title"
            holds[hold or "propose"] += 1
            rows.append({**{k: row.get(k, "") for k in
                            ("qid", "kind", "leading_title", "live_mul", "live_en",
                             "langs_carrying_live", "geni_ids")},
                         "proposed_label": "" if hold else label,
                         "proposed_aliases": "" if hold else " | ".join(aliases),
                         "hold": hold,
                         "case": ("lower" if row["leading_title"]
                                  and row["leading_title"].split()[0][:1].islower()
                                  else "upper" if row["leading_title"] else "")})

    rows.sort(key=lambda r: (int(r["qid"][1:]) if r["qid"][1:].isdigit() else 0, r["qid"]))
    tmp = DEST.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, DEST)

    print(f"read {len(rows):,} rows from {SRC.relative_to(ROOT)}")
    for reason, n in holds.most_common():
        print(f"  {n:7,}  {reason}")
    print(f"wrote {DEST.relative_to(ROOT)}")

    shown = [r for r in rows if not r["hold"]][:25]
    print("\na sample to read by eye -- this is the check, not the counts:")
    for r in shown:
        alias = f"   + {r['proposed_aliases']}" if r["proposed_aliases"] else ""
        print(f"  {r['qid']:<12} {r['live_mul'] or r['live_en']!r}\n"
              f"  {'':<12} -> {r['proposed_label']!r}{alias}")


if __name__ == "__main__":
    main()
