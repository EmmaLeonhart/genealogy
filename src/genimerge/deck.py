"""The machinery both manual-zipper decks are built out of.

`CLAUDE.md` § *⛔ "MANUAL ENTITY RESOLUTION" IS A MISLEADING NAME* --- these are the **manual
zipper merge correspondences**: the same job `scripts/zipper-join.py` does by position, done by
eye where position is not enough. Two generators sit on top of this module:

* `scripts/build-parent-candidates.py` --- the PARENT slot, live since 2026-08-31;
* `scripts/build-family-candidates.py` --- the CHILD and SIBLING slots, added 2026-09-09.

**It exists because the two would otherwise be the same 300 lines twice.** `CLAUDE.md` records
what that costs: *"Two emitters disagreed on this until 2026-08-26"*, and the parent deck's own
history is three published decks whose cards named nobody, each from a helper that was right in
one copy and wrong in another --- the ` | ` separator, the gitignored label file, the CJK-only
person with no `label_en`. Every one of those fixes lives here now, once.

Nothing in this module decides anything. It reads, it renders, and it refuses to publish a card
that names nobody.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

csv.field_size_limit(1 << 30)

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

RELATIONS = ROOT / "out" / "wikidata" / "relations.tsv"
LABELS_WD = ROOT / "out" / "wikidata" / "labels.tsv"
SEXES_WD = ROOT / "out" / "wikidata" / "sex.tsv"
STORE_INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
STORE_ITEMS = ROOT / "wikidata" / "items"
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
FACTS = ROOT / "reports" / "derived-facts.csv"
JUDGMENTS = ROOT / "reports" / "emma-judgments.tsv"
SYNOPTIC = ROOT / "reports" / "synoptic-correspondence.tsv"
TEMPLATE = ROOT / "out" / "review-deck.template.html"

#: **`out/wikidata/relations.tsv` separates with a SEMICOLON**, and `reports/derived-family.csv`
#: separates with ` | `. Two files, two separators, and one helper served both once ---
#: `CLAUDE.md` § *Our side could never have two children*: a person with three fathers arrived as
#: the single glued token, resolved to no name, and reached the deck as a card naming nobody.
SEP = ";"
FAMILY_SEP = "|"

WD_API = "https://www.wikidata.org/w/api.php"
WD_AGENT = "genimerge review deck (emma@topazcomputing.com)"

#: The languages a name may be recorded in, best first. An `en|mul` fetch published a bare QID
#: facing `藤原遠宗の娘`, a real name in `ja`. `CLAUDE.md` § *CJK INCLUDES KOREAN*.
LABEL_LANGS = ("en", "mul", "sv", "nb", "no", "da", "de", "fi", "fr", "zh", "ko", "ja")

SEX_OF_QID = {"Q6581097": "M", "Q6581072": "F"}

#: Han, kana and Hangul. **Written as ASCII escapes on purpose** --- `CLAUDE.md` § *A Han range
#: written with LITERAL boundary characters is a bug waiting to happen*: NFC folds U+F900 onto
#: U+8C48, which silently swallowed the whole Hangul block and cost 5,338 Korean people.
_CJK = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF"
                  r"\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF\u1100-\u11FF]")


def has_cjk(text):
    """True when the name is written in Han, kana or Hangul.

    **A CJK case is not in any deck.** Emma, 2026-09-07: *"I'm making a firm ruling here that
    effectively all these cjk people are undoable for me in my current situation."* A card is
    judged by reading two people's spouses and children, which she cannot do for a Heian
    courtier. They stay in the census TSV; only the deck she reads is filtered.
    """
    return bool(_CJK.search(text or ""))


def cell(row, column):
    """A ` | `-separated column of `reports/derived-family.csv`, split and stripped.

    The `.strip()` matters as much as the `|`: splitting without it yields `"1050090 "`, which
    misses every index just as silently as not splitting at all.
    """
    return [x.strip() for x in (row.get(column) or "").split(FAMILY_SEP) if x.strip()]


def fold(w):
    w = w.lower()
    for a, b in (("æ", "a"), ("ä", "a"), ("å", "a"), ("ö", "o"),
                 ("ø", "o"), ("é", "e"), ("ü", "u")):
        w = w.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", w)


def words(names):
    """Folded tokens of length > 2 across a list of names.

    An aid to reading, highlighted on the card, and **never a decision** --- `CLAUDE.md`
    no-name-similarity governs and nothing here proposes anything.
    """
    out = set()
    for n in names:
        for tok in str(n).split():
            f = fold(tok)
            if len(f) > 2:
                out.add(f)
    return out


# ---------------------------------------------------------------- Wikidata, offline ----

def load_relations(props=("p22", "p25", "p40", "p26", "p3373")):
    """`{prop: {qid: [ids]}}` plus `{qid: geni_id}`, read from `out/wikidata/relations.tsv`.

    A column the file does not carry comes back empty rather than raising, so a checkout whose
    table predates `p3373` degrades to the arms that do not need it instead of failing.
    """
    got = {p: {} for p in props}
    geni_of = {}
    if not RELATIONS.exists():
        return got, geni_of
    with io.open(RELATIONS, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        have = [p for p in props if p in (reader.fieldnames or ())]
        for row in reader:
            qid = row["qid"]
            if row.get("p2600"):
                geni_of[qid] = row["p2600"].split(SEP)[0].strip()
            for p in have:
                v = [x for x in (row.get(p) or "").split(SEP) if x]
                if v:
                    got[p][qid] = v
    return got, geni_of


def load_correspondence():
    """`(qids spoken for, geni ids spoken for, {geni_id: qid})` from the synoptic union.

    **`P2600` is not the only thing that identifies somebody.** Emma, 2026-08-31, on nine cases
    that survived a slot fix: *"I think literally all these people were identified earlier and
    some are very stale."* Seven of the nine were already in
    `reports/synoptic-correspondence.tsv` --- known through the structural walk, the zipper, her
    bio links or her own verdicts, none of which puts a `P2600` on Wikidata.
    """
    qids, genis, qid_of = set(), set(), {}
    if not SYNOPTIC.exists():
        return qids, genis, qid_of
    with io.open(SYNOPTIC, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("qid") and r.get("geni_id"):
                qids.add(r["qid"])
                genis.add(r["geni_id"])
                qid_of.setdefault(r["geni_id"], r["qid"])
    return qids, genis, qid_of


def load_wikidata_sex():
    """`{qid: "M"|"F"}` from `out/wikidata/sex.tsv`, which is offline and tracked.

    Sex is the one free discriminator in a child slot and it is not decoration:
    `scripts/census-solo-children.py` measured `P21` refuting **10.0%** of solo-child pairs
    against 0.0% for solo father and mother slots.
    """
    out = {}
    if not SEXES_WD.exists():
        return out
    with io.open(SEXES_WD, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            s = (r.get("sex") or "").strip().upper()[:1]
            if s in ("M", "F"):
                out[r["qid"]] = s
    return out


def labels_from_store(wanted):
    """Labels for `wanted` read out of the local store, via the QID-to-shard index.

    The offline middle path. It opens only the shards the index names, which is what makes it
    seconds rather than a full pass over 4.3 GB.

    **The store writes `"id": "Q123"` WITH A SPACE**, and a matcher looking for `'"id":"Q'` finds
    nothing --- which reads as *these items are not in the store* when all of them are. So the id
    is taken from the parsed record and never from a substring guess.
    """
    if not (STORE_INDEX.exists() and STORE_ITEMS.is_dir()):
        return {}
    import collections

    shards = collections.defaultdict(set)
    try:
        db = sqlite3.connect("file:%s?mode=ro" % STORE_INDEX, uri=True)
        for q in wanted:
            row = db.execute("SELECT shard FROM items WHERE qid=?", (q,)).fetchone()
            if row:
                shards[row[0]].add(q)
        db.close()
    except sqlite3.Error as exc:
        sys.stderr.write("store index unreadable (%s)\n" % exc)
        return {}

    out = {}
    for shard, qs in sorted(shards.items()):
        path = STORE_ITEMS / ("items-%05d.jsonl.gz" % shard)
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                if not any(q in line for q in qs):
                    continue
                rec = json.loads(line)
                if rec.get("id") not in qs:
                    continue
                lab = rec.get("labels") or {}
                for lng in LABEL_LANGS:
                    if lng in lab:
                        out[rec["id"]] = lab[lng]["value"]
                        break
                else:
                    if lab:
                        out[rec["id"]] = next(iter(lab.values()))["value"]
    if out:
        print("%s Wikidata labels read from the store index across %s shards"
              % (format(len(out), ","), format(len(shards), ",")), file=sys.stderr)
    return out


def store_scan(wanted):
    """One pass over the whole store for `wanted`: `{qid: (label, sex, born, died)}`.

    **The third offline path, and in some containers the ONLY one.** `wbgetentities` is what the
    parent deck falls back to, and the sandbox this repo's cloud sessions run in answers
    `CONNECT www.wikidata.org:443` with a 403 --- so a deck built here had no Wikidata names at
    all and every card would have named a bare QID. `labels_from_store` cannot help without
    `out/wikidata/store-index.sqlite3`, which is gitignored and derived.

    It is also the cheaper path once a deck is large: 3,500 candidates and their relatives are
    ~600 API requests against one 6-minute read of files already on disk.

    **The id is taken from the parsed record, never from a substring guess** --- the store writes
    `"id": "Q123"` WITH A SPACE, and a matcher looking for `'"id":"Q'` finds nothing, which reads
    as *these items are not in the store* when all of them are. The cheap `find` below only
    decides whether to parse the line; membership is settled on `rec["id"]`.
    """
    wanted = {q for q in wanted if q}
    if not (STORE_ITEMS.is_dir() and wanted):
        return {}
    shards = sorted(STORE_ITEMS.glob("items-*.jsonl.gz"))
    if not shards:
        return {}
    out = {}
    started = time.time()
    for n, shard in enumerate(shards, 1):
        with gzip.open(shard, "rt", encoding="utf-8") as fh:
            for line in fh:
                i = line.find('"id": "', 0, 400)
                if i < 0:
                    continue
                j = line.find('"', i + 7)
                if line[i + 7:j] not in wanted:
                    continue
                rec = json.loads(line)
                qid = rec.get("id")
                if qid not in wanted:
                    continue
                lab = rec.get("labels") or {}
                label = ""
                for lng in LABEL_LANGS:
                    if lng in lab:
                        label = lab[lng]["value"]
                        break
                else:
                    if lab:
                        label = next(iter(lab.values()))["value"]
                claims = rec.get("claims") or {}
                out[qid] = (label, SEX_OF_QID.get(first_id(claims, "P21"), ""),
                            first_year(claims, "P569"), first_year(claims, "P570"))
        if n % 600 == 0:
            print("  store scan %d/%d shards, %s of %s found"
                  % (n, len(shards), format(len(out), ","), format(len(wanted), ",")),
                  file=sys.stderr)
    print("store scan: %s of %s items found in %.0fs"
          % (format(len(out), ","), format(len(wanted), ","), time.time() - started),
          file=sys.stderr)
    return out


def fetch_labels(ids):
    """`{qid: label}` from the live API, batched 50 at a time.

    **`out/wikidata/labels.tsv` is GITIGNORED, so in Actions it does not exist** --- and Actions
    is what publishes. Reading that file and nothing else meant every published deck showed a
    bare `Q5290415` where the Wikidata name belongs, while a local run with the 187 MB file
    present looked perfect.
    """
    out, ids = {}, [q for q in ids if q]
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        url = WD_API + "?" + urllib.parse.urlencode({
            "action": "wbgetentities", "ids": "|".join(chunk), "props": "labels",
            "languages": "|".join(LABEL_LANGS), "format": "json"})
        req = urllib.request.Request(url, headers={"User-Agent": WD_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=90) as fh:
                data = json.loads(fh.read().decode("utf-8"))
        except Exception as exc:                                          # noqa: BLE001
            sys.stderr.write("label fetch failed for %d ids: %s\n" % (len(chunk), exc))
            continue
        time.sleep(0.4)
        for q, e in (data.get("entities") or {}).items():
            labs = e.get("labels") or {}
            for lang in LABEL_LANGS:
                if labs.get(lang, {}).get("value"):
                    out[q] = labs[lang]["value"]
                    break
            else:
                if labs:
                    out[q] = next(iter(labs.values()))["value"]
    return out


def wikidata_labels(wanted):
    """Names for `wanted`, cheapest source first: the 187 MB file, the store, then the API."""
    wanted = {q for q in wanted if q}
    out = {}
    if LABELS_WD.exists():
        with io.open(LABELS_WD, encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if parts[0] in wanted and len(parts) > 1:
                    out.setdefault(parts[0], parts[1])
    if not out:
        out.update(labels_from_store(wanted))
    missing = sorted(q for q in wanted if not out.get(q))
    if missing:
        if not LABELS_WD.exists():
            sys.stderr.write(
                "out/wikidata/labels.tsv absent (gitignored, so this is normal in Actions)"
                " -- fetching %s names from the API instead\n" % format(len(missing), ","))
        out.update(fetch_labels(missing))
    still = sum(1 for q in wanted if not out.get(q))
    print("Wikidata names: %s of %s resolved%s"
          % (format(len(wanted) - still, ","), format(len(wanted), ","),
             ("; %s still a bare QID" % format(still, ",")) if still else ""),
          file=sys.stderr)
    return out


def wikidata_facts(label_ids, chip_ids):
    """`(labels, sex, life, gone)` for a whole deck, cheapest source first, in ONE store pass.

    `label_ids` is everyone whose name appears on a card --- the candidate and their relatives.
    `chip_ids` is the candidates themselves, who also need sex and dates.

    Order: the 187 MB `labels.tsv` where it exists, then a single pass over the local store for
    whatever is left, then `wbgetentities` for the remainder. Each layer is absent in some
    environment the deck actually runs in --- the file locally, the store in Actions, the API in
    the cloud sandbox --- and the deck must build in all three.

    **`gone` is API-only, and that is a real limit rather than an oversight.** The store is a
    Geni-shaped slice of Wikidata, so an item missing from it is usually just outside the
    download; only Wikidata itself can say an item has been deleted. With no API reachable the
    set is empty and a dead candidate reaches the card without its warning.
    """
    labels, sex, life, gone = {}, {}, {}, set()
    label_ids = {q for q in label_ids if q}
    chip_ids = {q for q in chip_ids if q}

    if LABELS_WD.exists():
        with io.open(LABELS_WD, encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if parts[0] in label_ids and len(parts) > 1:
                    labels.setdefault(parts[0], parts[1])

    need = {q for q in label_ids if not labels.get(q)} | chip_ids
    if need:
        found = labels_from_store(need) if STORE_INDEX.exists() else {}
        for q, lab in found.items():
            labels.setdefault(q, lab)
        need = {q for q in label_ids if not labels.get(q)} | (chip_ids - set(sex))
        if need:
            for q, (lab, sx, born, died) in store_scan(need).items():
                if lab:
                    labels.setdefault(q, lab)
                if q in chip_ids:
                    sex[q], life[q] = sx, (born, died)

    missing_labels = sorted(q for q in label_ids if not labels.get(q))
    if missing_labels:
        if not LABELS_WD.exists():
            sys.stderr.write("%s names not on disk -- asking the API\n"
                             % format(len(missing_labels), ","))
        labels.update(fetch_labels(missing_labels))
    missing_chips = sorted(chip_ids - set(sex))
    if missing_chips:
        api_sex, api_life, gone = candidate_chips(missing_chips)
        sex.update(api_sex)
        life.update(api_life)

    still = sum(1 for q in label_ids if not labels.get(q))
    print("Wikidata names: %s of %s resolved%s; chips for %s of %s candidates"
          % (format(len(label_ids) - still, ","), format(len(label_ids), ","),
             ("; %s still a bare QID" % format(still, ",")) if still else "",
             format(len(sex), ","), format(len(chip_ids), ",")), file=sys.stderr)
    return labels, sex, life, gone


def fetch_claims(ids):
    """`(claims by qid, ids Wikidata no longer has)`, splitting around the dead ones.

    **One bad id fails the WHOLE batch.** `wbgetentities` answers a batch containing a single
    deleted or merged-away item with `no-such-entity` and returns *nothing* --- so 5 dead ids
    among 501 returned 201 items and printed no error at all. Halving the chunk isolates the
    offender in log(n) requests instead of losing 49 good items beside it.
    """
    if not ids:
        return {}, set()
    url = WD_API + "?" + urllib.parse.urlencode({
        "action": "wbgetentities", "ids": "|".join(ids), "props": "claims", "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": WD_AGENT})
    with urllib.request.urlopen(req, timeout=90) as fh:
        data = json.loads(fh.read().decode("utf-8"))
    time.sleep(0.4)
    if not (data.get("error") or {}).get("code"):
        return {q: (e.get("claims") or {}) for q, e in data.get("entities", {}).items()}, set()
    if len(ids) == 1:
        return {}, set(ids)
    half = len(ids) // 2
    a, am = fetch_claims(ids[:half])
    b, bm = fetch_claims(ids[half:])
    a.update(b)
    return a, am | bm


def first_id(claims, prop):
    """The item id of the first `prop` statement, or `""`."""
    for st in claims.get(prop, ()):
        try:
            return st["mainsnak"]["datavalue"]["value"]["id"]
        except (KeyError, TypeError):
            continue
    return ""


def first_year(claims, prop):
    """`"1729"` for a year-or-finer date, `"17c"` for a century, `""` for nothing.

    Precision is the whole point. Wikidata stores *17th century* as `+1650-00-00` at precision 7,
    and reading that as the year 1650 invents a disagreement with a real 1600 --- which an audit
    of her verdicts did, flagging two clean pairs. A coarse date is rendered as coarse and never
    compared.
    """
    for st in claims.get(prop, ()):
        try:
            v = st["mainsnak"]["datavalue"]["value"]
            t, prec = v["time"], int(v.get("precision", 11))
        except (KeyError, TypeError, ValueError):
            continue
        neg = t.startswith("-")
        year = int(t[1:5])
        if prec <= 6:
            return ""
        if prec == 7:
            return "%dc" % ((year - 1) // 100 + 1)
        if prec == 8:
            return "%ds" % (year // 10 * 10)
        return ("-%d" if neg else "%d") % year
    return ""


def candidate_chips(qids):
    """`({qid: sex}, {qid: (born, died)}, {qids Wikidata no longer has})`, from one live read.

    **Fail soft, loudly.** A deck with no chips is far better than no deck, so a network failure
    degrades the card rather than the run.
    """
    sex, life, gone = {}, {}, set()
    fetch = sorted({q for q in qids if q})
    if not fetch:
        return sex, life, gone
    try:
        claims, gone = fetch_claims(fetch)
        for q, cl in claims.items():
            sex[q] = SEX_OF_QID.get(first_id(cl, "P21"), "")
            life[q] = (first_year(cl, "P569"), first_year(cl, "P570"))
        sys.stderr.write("sex and dates for %s of %s candidate items%s\n"
                         % (format(len(claims), ","), format(len(fetch), ","),
                            ("; %d no longer exist on Wikidata" % len(gone)) if gone else ""))
        if len(claims) + len(gone) != len(fetch):
            sys.stderr.write("WARNING: %d items unaccounted for -- the fetch is short and the "
                             "cards for them will carry no chips\n"
                             % (len(fetch) - len(claims) - len(gone)))
    except Exception as exc:                                              # noqa: BLE001
        sys.stderr.write("WARNING: could not fetch candidate sex/dates (%s) -- the cards will "
                         "carry names and relationships only\n" % exc)
    return sex, life, gone


# --------------------------------------------------------------------- our own tree ----

def load_our_family():
    """`(fathers, mothers, children, spouses)`, each `{geni_id: [geni_id]}`."""
    fathers, mothers, children, spouses = {}, {}, {}, {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            for col, dest in (("fathers", fathers), ("mothers", mothers),
                              ("children", children), ("spouses", spouses)):
                v = cell(row, col)
                if v:
                    dest[g] = v
    return fathers, mothers, children, spouses


def load_our_labels():
    """`{geni_id: name}`, falling back to the CJK form.

    **A CJK-only person has NO `label_en` and NO `label_mul`** --- their name is in `cjk_names`,
    ` | `-separated. Reading the first two columns only left the card blank on our side, which is
    the one thing Emma says makes a case unanswerable: *"no relationships means I can't make a
    judgment."*
    """
    out = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            name = row.get("label_en") or row.get("label_mul") or ""
            if not name:
                name = (row.get("cjk_names") or "").split(FAMILY_SEP)[0].strip()
            out[row["geni_id"]] = name
    return out


def load_our_facts(wanted=None):
    """`({geni_id: sex}, {geni_id: (born, died)})` from `reports/derived-facts.csv`."""
    sex, life = {}, {}
    if not FACTS.exists():
        return sex, life
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            if wanted is not None and g not in wanted:
                continue
            s = (r.get("sex") or "").strip().upper()[:1]
            if s in ("M", "F"):
                sex[g] = s
            life[g] = (r.get("birth_date_year") or "", r.get("death_date_year") or "")
    return sex, life


def answered_pairs():
    """`{(geni_id, qid)}` she has settled, and the count still open.

    **A DECIDED pair never comes back. An UNSURE one does.** An `UNSURE` is *I cannot tell from
    this*, and retiring it was something I invented and she did not ask for. Those come back, so
    a later run with more evidence can put a better version of the same question to her.
    """
    answered, unsure = set(), 0
    if not JUDGMENTS.exists():
        return answered, unsure
    with io.open(JUDGMENTS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if not (row.get("geni_id") and row.get("qid")):
                continue
            if (row.get("verdict") or "").strip().upper() == "UNSURE":
                unsure += 1
                continue
            answered.add((row["geni_id"].strip(), row["qid"].strip()))
    return answered, unsure


# ------------------------------------------------------------------------ the deck ----

def mark_also_offered(cases):
    """Say so on every card when one item is offered against more than one person.

    **The Engeström shape, detectable with no name matching at all.** `Q5712230` was put to her
    twice --- once for Johan Mattias von Engeström and once for his wife --- and only one of them
    can be it.
    """
    offered = {}
    for c in cases:
        offered.setdefault(c["qid"], []).append(c)
    for group in offered.values():
        if len(group) > 1:
            for c in group:
                c["also_offered"] = ", ".join(o["our"] for o in group if o is not c)


def render(cases, html_path, json_path, title, sub, key):
    """Write the deck JSON and the rendered page. Returns the cases that reached the deck.

    `key` is the deck's `localStorage` namespace, and it must differ between decks: two decks
    sharing one key would show each other's answers and export each other's rows.

    **A CJK CASE IS HELD OUT.** See `has_cjk`.
    """
    held = [c for c in cases if has_cjk(c.get("our")) or has_cjk(c.get("cand"))]
    deck = [c for c in cases if c not in held]
    if held:
        print("%d CJK case(s) held out of the deck, per her ruling of 2026-09-07: %s"
              % (len(held), ", ".join(c["qid"] for c in held[:8])), file=sys.stderr)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(deck, io.open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not TEMPLATE.exists():
        sys.exit("no template at %s" % TEMPLATE)
    html = TEMPLATE.read_text(encoding="utf-8")
    for token in ("__DATA__", "__TITLE__", "__SUB__", "__KEY__"):
        if token not in html:
            sys.exit("template has no %s placeholder" % token)
    html = (html.replace("__TITLE__", title).replace("__SUB__", sub).replace("__KEY__", key)
                .replace("__DATA__", json.dumps(deck, ensure_ascii=False)))
    io.open(html_path, "w", encoding="utf-8").write(html)
    return deck


def nameless(deck):
    """The cards that name nobody on one side --- the tell a count never shows.

    Three separate bugs each published a deck whose cards were a name facing an empty box or a
    bare QID, while the generator printed a healthy candidate count every run. Emma, 2026-09-04,
    on what reached the site: *"a weird-ass page ... in a way that made it useless"*.
    """
    return [c for c in deck
            if not (c.get("our") or "").strip()
            or not (c.get("cand") or "").strip()
            or re.fullmatch(r"Q\d+", (c.get("cand") or "").strip())]
