"""Publish the daily batch to GitHub Pages. That is the whole site.

**The site is ONE thing, cut back on 2026-09-03: the daily batch.** The home page had carried
a pile of material that did not belong there, including a digest of rules from `CLAUDE.md` that
could go stale. The only purpose of the GitHub Pages site is to hand over the daily batch, and
that is all that should be on it.

So `index.html` **is** the batch — selectable text with a copy button, no login, no zip. There is
no landing page, no statistics block, no rules digest and no algorithm summary. Those were 27 KB
of prose nobody asked for sitting in front of the one file the site exists to hand over.

**The rules digest was the worst of it and is worth naming**: it lifted sections out of
`CLAUDE.md` and republished them, so a rule superseded in that file went on being displayed here
as current. A generated page that restates rules is a second, staler copy of them.

**There are TWO batch files and there always were**, which this docstring denied until
2026-09-09: `reports/wikidata-garborg-day.txt` (94 creations) and
`reports/wikidata-garborg-name-items.txt` (12), and the second is not inside the first --
zero `Den "patronymic"` lines appear in the day batch, which is the marker every name-item
creation carries. `build-garborg-day.py --compose` runs the name-item generator as its own step
and hard-fails the run if it fails, so the file is produced every time.

**Both get a page, because `pipeline.yml` has linked both since it was written.** Its issue body
offers `[name items](.../wikidata-garborg-name-items.html)` on every run and nothing ever built
that page, so the notification carried a 404 to a batch that has to be run by hand. The
sentence this replaces -- *"there is no second page to publish"* -- is why nobody looked: a
comment asserting a property nobody measured answers the question for the next reader, wrongly.

**The order between them is not this file's business.** `CLAUDE.md` § *THE DAILY ALGORITHM*
fixes it, the run order is printed by the generator, and both pages say which they are.

A short list of review pages is copied across beside it, so each keeps a **no-login URL** of its
own. GitHub Pages needs no sign-in, which a Claude artifact and an Actions artifact both do.
None of them is linked from the batch page: nothing should compete with the batch, and a page
whose URL has already been handed over does not need a link.
"""

from __future__ import annotations

import csv
import datetime
import gzip
import html
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "site" / "index.html"

#: The batch files the site exists to serve: (report, page name, title, subtitle).
#: The first is `index.html`, so the bare site URL is the daily batch and nothing else.
BATCHES = (
    # ⛔ THE MANUAL HALF, NOT THE WHOLE BATCH. Ruled 2026-09-14: *"Produce disjoint
    # quickstatements on the github page too."* The scheduled run sends
    # `wikidata-garborg-day-auto.txt` by itself; publishing the whole batch here would tell a
    # person to paste what the runner already sent, and a duplicate `CREATE` mints a second
    # item for somebody who now exists. `scripts/split-daily-batch.py` writes both halves and
    # asserts they are disjoint and complete.
    (ROOT / "reports" / "wikidata-garborg-day-manual.txt", "index.html",
     "The daily batch", "the half CI/CD does not send — run this one"),
    (ROOT / "reports" / "wikidata-garborg-name-items.txt",
     "wikidata-garborg-name-items.html",
     "Name items", "the name items the daily batch links to"),
    # ⛔ **FAMILYSEARCH, ITS OWN PAGE. Ruled 2026-09-27 (Emma):** the FamilySearch people are the
    # hard part and the pipeline's handling of them is not yet trusted, so their batch is on a
    # page of its own, to be looked over by hand. Ten of them also lead every loop batch.
    (ROOT / "reports" / "wikidata-familysearch-day.txt", "familysearch.html",
     "FamilySearch", "the FamilySearch people, their own batch: look it over before running"),
)

#: The one that must exist. A run with no day batch is a failed run; a run with no name items
#: is an ordinary day on which nothing needed minting, so that page is skipped rather than fatal.
BATCH = BATCHES[0][0]

#: Published beside it so a review page is never artifact-only, but deliberately unlinked.
#: Add a path here and it gets a Pages URL; also add it to `pages.yml`'s sparse checkout, or
#: the runner will not have the file and the copy silently does nothing.
ALONGSIDE = (
    ROOT / "out" / "parent-review.html",
    ROOT / "out" / "family-review.html",
    ROOT / "out" / "pick-one-review.html",
    ROOT / "out" / "patronymic-identifications.html",
    ROOT / "out" / "duplicate-surnames.html",
    ROOT / "out" / "duplicate-name-items-we-made.html",
)

PAGE = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "_batch_page.html"


def esc(s):
    return html.escape(str(s or ""), quote=True)


#: How every possible creation of the last run divides (`split-daily-batch.summarise_candidates`).
CANDIDATES = ROOT / "reports" / "creation-candidates-summary.tsv"


def render_candidates():
    """`candidates.html`: the table of possible creations by kind and by what became of them."""
    if not CANDIDATES.exists():
        print("no %s; candidates page not built" % CANDIDATES.name)
        return
    rows = list(csv.reader(io.open(CANDIDATES, encoding="utf-8"), delimiter="	"))
    head, body = rows[0], rows[1:]
    cells = "".join("<th>%s</th>" % esc(h) for h in head)
    lines = "".join("<tr>%s</tr>" % "".join(
        ("<td>%s</td>" if k == 0 else "<td class=n>%s</td>") % esc(v) for k, v in enumerate(r))
        for r in body)
    page = ("<!doctype html><meta charset=utf-8><meta name=viewport "
            "content='width=device-width,initial-scale=1'><title>Possible creations</title>"
            "<style>body{font:15px system-ui;margin:16px;max-width:900px}table{border-collapse:"
            "collapse;width:100%%}td,th{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left}"
            ".n{text-align:right;font-variant-numeric:tabular-nums}</style>"
            "<h1>Possible creations</h1><p>Every uncreated person one relationship from our items, "
            "plus the ancestor ring, by kind, against the batch of the last run "
            "(<a href='index.html'>the daily batch</a>, <a href='familysearch.html'>FamilySearch</a>)"
            ". Built %s.</p><div style='overflow-x:auto'><table><tr>%s</tr>%s</table></div>"
            % (datetime.date.today().isoformat(), cells, lines))
    io.open(OUT.parent / "candidates.html", "w", encoding="utf-8", newline="").write(page)
    print("candidates.html -> %s kinds" % len(body))


#: The patronymic audit (`reports/patronymic-audit.csv`, 2026-09-28): the live `P5056` that fail
#: Emma's surname tests, for her to review before anything live is changed (AskUserQuestion).
PATRONYMIC_AUDIT = ROOT / "reports" / "patronymic-audit.csv"
REVIEW_VERDICTS = ("father carries the same token (a surname)", "model reads it as a surname",
                   "father known, no match (kept as patronymic)")


def render_patronymic_review():
    """`patronymic-review.html`: the live patronymic statements our own tests now reject."""
    if not PATRONYMIC_AUDIT.exists():
        print("no %s; patronymic review not built" % PATRONYMIC_AUDIT.name)
        return
    rows = [r for r in csv.DictReader(io.open(PATRONYMIC_AUDIT, encoding="utf-8"))
            if r["source"] == "live" and r["verdict"] in REVIEW_VERDICTS]
    wd = "https://www.wikidata.org/wiki/"
    body = "".join(
        "<tr><td><a href='%s%s'>%s</a><br><small>%s</small></td><td><a href='%s%s'>%s</a></td>"
        "<td>%s</td><td>%s</td></tr>"
        % (wd, esc(r["qid"]), esc(r["person"] or r["qid"]), esc(r["qid"]), wd,
           esc(r["patronymic_qid"]), esc(r["token"] or r["patronymic_qid"]), esc(r["father"]),
           esc(r["verdict"])) for r in rows)
    page = ("<!doctype html><meta charset=utf-8><meta name=viewport "
            "content='width=device-width,initial-scale=1'><title>Patronymic review</title>"
            "<style>body{font:15px system-ui;margin:16px;max-width:1000px}table{border-collapse:"
            "collapse;width:100%%}td,th{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;"
            "vertical-align:top}small{color:#666}</style><h1>Patronymic review</h1>"
            "<p>%d live <code>P5056</code> patronymic statements on our items that fail the surname "
            "tests (the father carries the same token; the model reads it as a surname; the root "
            "does not match the father). Nothing changes on Wikidata until they are reviewed. "
            "Built %s from <code>reports/patronymic-audit.csv</code>.</p><div style='overflow-x:auto'>"
            "<table><tr><th>person</th><th>patronymic</th><th>father</th><th>why</th></tr>%s</table>"
            "</div>" % (len(rows), datetime.date.today().isoformat(), body))
    io.open(OUT.parent / "patronymic-review.html", "w", encoding="utf-8", newline="").write(page)
    print("patronymic-review.html -> %d rows" % len(rows))


def render(source, name, title, note, tpl):
    """Write one batch page. Returns (creations, statement lines, bytes) or None if absent."""
    if not source.exists():
        return None
    text = source.read_text(encoding="utf-8", errors="replace")
    stmts = sum(1 for l in text.splitlines()
                if l.strip() and not l.lstrip().startswith("#"))
    creates = sum(1 for l in text.splitlines() if l.strip() == "CREATE")
    page = tpl % (title, title,
                  "%s creations · %s · %s" % (creates, format(stmts, ","), note),
                  datetime.date.today().isoformat(), esc(text))
    target = OUT.parent / name
    target.parent.mkdir(parents=True, exist_ok=True)
    io.open(target, "w", encoding="utf-8", newline="").write(page)
    return creates, stmts, len(page)



# ---------------------------------------------------------------------------------------
# ⛔ **ONE PAGE PER PERSON, adapted from order.life.** `queue.md`, 2026-09-26: the repo builds a
# family tree for Wikidata, and later one for the Gaiad at genealogy.order.life; add per-individual
# pages, adapted from how order.life already generates its pages. order.life's `build.py` writes
# `gaiad/characters/<name>/index.html` from one JSON per character, with father, mother and
# children linked when THEY have a page too, and the Wikidata QID. Same shape here, stdlib only,
# keyed on the QID because a name is not unique in a genealogy.
#
# **Who gets one: everybody the ledger pairs with a Wikidata item** (`reports/garborg-qids.tsv`).
# Built by `pages.yml` at deploy time with `--people` and never committed: `out/site/people/` is
# gitignored, since twelve thousand files churned on every pipeline run would be the opposite of a
# minimal repo. The batch page stays the site's front door, as the item says, for now.
PEOPLE = OUT.parent / "people"

PERSON_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(name)s</title>
<style>
body{margin:0;background:#fbfaf7;color:#1f1d1a;font:16px/1.55 Georgia,serif}
.wrap{max-width:720px;margin:0 auto;padding:24px 16px}
h1{font-size:28px;margin:0 0 4px}.sub{color:#6b6660;font-size:14px}
h2{font-size:18px;margin:24px 0 6px}ul{margin:0;padding-left:20px}
a{color:#7a3b12}
@media (prefers-color-scheme:dark){body{background:#181715;color:#ece8e1}.sub{color:#a39d94}a{color:#e0a36f}}
</style></head><body><div class="wrap">
<p class="sub"><a href="index.html">People</a> · <a href="../index.html">the daily batch</a></p>
<h1>%(name)s</h1>
<p class="sub">%(life)s</p>
%(family)s
<h2>Records</h2>
<ul>%(records)s</ul>
</div></body></html>
"""


def _read_csv(path, **kw):
    """Rows of a report, plain or committed gzipped."""
    plain = path.with_suffix("") if path.suffix == ".gz" else path
    if plain.exists():
        fh = open(plain, encoding="utf-8", newline="")
    elif path.exists():
        fh = gzip.open(path, "rt", encoding="utf-8", newline="")
    else:
        return []
    csv.field_size_limit(1 << 30)
    with fh:
        return list(csv.DictReader(fh, **kw))


def _ids(cell):
    """`reports/derived-family.csv` separates with ` | `, spaces included (CLAUDE.md)."""
    return [x.strip() for x in (cell or "").split(" | ") if x.strip()]


def build_people():
    rep = ROOT / "reports"
    ledger = {}
    for r in _read_csv(rep / "garborg-qids.tsv", delimiter="\t"):
        if (r.get("qid") or "").startswith("Q") and r.get("geni_id"):
            ledger.setdefault(r["geni_id"], (r["qid"], r.get("label") or r["qid"]))
    if not ledger:
        print("no ledger; no people pages")
        return 0
    family = {r["geni_id"]: r for r in _read_csv(rep / "derived-family.csv.gz")
              if r["geni_id"] in ledger}
    facts = {r["geni_id"]: r for r in _read_csv(rep / "derived-facts.csv.gz")
             if r["geni_id"] in ledger}
    fs = {}
    for r in _read_csv(rep / "familysearch-zipper-pairs.tsv", delimiter="\t"):
        fs.setdefault(r.get("geni_id"), r.get("fs_id"))
    # Relatives outside the ledger are named from the derived labels and simply not linked.
    wanted = {i for f in family.values()
              for c in ("fathers", "father", "mothers", "mother", "spouses", "children")
              for i in _ids(f.get(c))} - set(ledger)
    names = {r["geni_id"]: r.get("label_mul") or r.get("label_en") or ""
             for r in _read_csv(rep / "derived-labels.csv.gz") if r["geni_id"] in wanted}
    names.update({g: lab for g, (_q, lab) in ledger.items()})

    def who(g):
        if g in ledger:
            q, lab = ledger[g]
            return '<a href="%s.html">%s</a>' % (esc(q), esc(lab))
        return esc(names.get(g) or "an unnamed relative")

    PEOPLE.mkdir(parents=True, exist_ok=True)
    rows = []
    done = set()
    for g, (q, name) in sorted(ledger.items(), key=lambda kv: (kv[1][1].casefold(), kv[1][0], kv[0])):
        # Two Geni profiles on one item make one page, not two that overwrite each other.
        if q in done:
            continue
        done.add(q)
        f = family.get(g, {})
        fa = facts.get(g, {})
        life = " – ".join(x for x in ((fa.get("birth_date_raw") or "").strip(),
                                       (fa.get("death_date_raw") or "").strip()) if x)
        blocks = []
        for title, ids in (("Parents", _ids(f.get("fathers") or f.get("father"))
                            + _ids(f.get("mothers") or f.get("mother"))),
                           ("Spouses", _ids(f.get("spouses"))),
                           ("Children", _ids(f.get("children")))):
            if ids:
                blocks.append("<h2>%s</h2><ul>%s</ul>"
                              % (title, "".join("<li>%s</li>" % who(i) for i in dict.fromkeys(ids))))
        records = ['<li>Wikidata <a href="https://www.wikidata.org/wiki/%s">%s</a></li>'
                   % (esc(q), esc(q))]
        if fs.get(g):
            records.append('<li>FamilySearch <a href="https://www.familysearch.org/tree/person/'
                           'details/%s">%s</a></li>' % (esc(fs[g]), esc(fs[g])))
        records.append('<li>Geni <a href="https://www.geni.com/people/%s">%s</a></li>'
                       % (esc(g), esc(g)))
        page = PERSON_PAGE % {"name": esc(name), "life": esc(life),
                              "family": "".join(blocks), "records": "".join(records)}
        io.open(PEOPLE / ("%s.html" % q), "w", encoding="utf-8", newline="").write(page)
        rows.append('<li><a href="%s.html">%s</a> <span class="sub">%s</span></li>'
                    % (esc(q), esc(name), esc(life)))
    index = PERSON_PAGE % {"name": "People", "life": "%s people with a Wikidata item" % format(len(rows), ","),
                           "family": "<ul>%s</ul>" % "".join(rows), "records": ""}
    index = index.replace("<h2>Records</h2>\n<ul></ul>\n", "")
    io.open(PEOPLE / "index.html", "w", encoding="utf-8", newline="").write(index)
    print("people pages: %s" % format(len(rows), ","))
    return len(rows)

def main() -> int:
    if "--people" in sys.argv[1:]:
        return 0 if build_people() else 1
    if not BATCH.exists():
        print("no batch at %s" % BATCH, file=sys.stderr)
        return 1

    tpl = PAGE.read_text(encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for source, name, title, note in BATCHES:
        got = render(source, name, title, note, tpl)
        if got is None:
            # Only the day batch is required, and it was checked above.
            print("no batch to publish at %s" % source.name)
            continue
        print("%s -> %s creations, %s statement lines, %s bytes"
              % (name, got[0], format(got[1], ","), format(got[2], ",")))

    render_candidates()
    render_patronymic_review()

    for extra in ALONGSIDE:
        if not extra.exists():
            print("not published (absent here): %s" % extra.name)
            continue
        io.open(OUT.parent / extra.name, "w", encoding="utf-8", newline="").write(
            extra.read_text(encoding="utf-8", errors="replace"))
        print("published alongside, unlinked: %s" % extra.name)

    # Fail loudly rather than deploying a page with no batch on it: a site that builds to
    # nothing looks exactly like a working deploy.
    built = OUT.read_text(encoding="utf-8")
    text = BATCH.read_text(encoding="utf-8", errors="replace")
    if "CREATE" not in built or len(built) < len(text):
        print("the batch did not reach the page", file=sys.stderr)
        return 1
    print("%s -> %s bytes" % (OUT, format(len(built), ",")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
