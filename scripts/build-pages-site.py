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

import datetime
import html
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "site" / "index.html"

#: The batch files the site exists to serve: (report, page name, title, subtitle).
#: The first is `index.html`, so the bare site URL is the daily batch and nothing else.
BATCHES = (
    (ROOT / "reports" / "wikidata-garborg-day.txt", "index.html",
     "The daily batch", "run this one first"),
    (ROOT / "reports" / "wikidata-garborg-name-items.txt",
     "wikidata-garborg-name-items.html",
     "Name items", "the name items the daily batch links to"),
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


def main() -> int:
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
