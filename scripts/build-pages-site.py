"""Publish the daily batch to GitHub Pages. That is the whole site.

**Emma, 2026-09-03, cutting it back to one thing:** *"The home page has a bunch of bullshit on it
that should not be there. A bunch of random rules from CLAUDE.md that might also even be stale...
who the fuck cares what these rules are? The only purpose of the GitHub pages is to give the daily
batch... all that should be present is very simply the daily batch."*

So `index.html` **is** the batch — selectable text with a copy button, no login, no zip. There is
no landing page, no statistics block, no rules digest and no algorithm summary. Those were 27 KB
of prose nobody asked for sitting in front of the one file she comes here to copy.

**The rules digest was the worst of it and is worth naming**: it lifted sections out of
`CLAUDE.md` and republished them, so a rule superseded in that file went on being displayed here
as current. A generated page that restates rules is a second, staler copy of them.

**Name items are already inside the daily batch** -- one file since 2026-08-30, her instruction --
so there is no second page to publish and nothing to run in a particular order.

A short list of review pages is copied across beside it, so each keeps a **no-login URL** of its
own -- Emma, 2026-09-04: *"github pages is best since I don't need to sign in"*, an artifact and an
Actions artifact both being unreachable to her. None of them is linked from the batch page:
nothing should compete with the batch, and a page she was handed a URL for does not need a link.
"""

from __future__ import annotations

import datetime
import html
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "site" / "index.html"

#: The one file the site exists to serve.
BATCH = ROOT / "reports" / "wikidata-garborg-day.txt"

#: Published beside it so a review page is never artifact-only, but deliberately unlinked.
#: Add a path here and it gets a Pages URL; also add it to `pages.yml`'s sparse checkout, or
#: the runner will not have the file and the copy silently does nothing.
ALONGSIDE = (
    ROOT / "out" / "parent-review.html",
    ROOT / "out" / "patronymic-identifications.html",
    ROOT / "out" / "duplicate-surnames.html",
    ROOT / "out" / "duplicate-name-items-we-made.html",
)

PAGE = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "_batch_page.html"


def esc(s):
    return html.escape(str(s or ""), quote=True)


def main() -> int:
    if not BATCH.exists():
        print("no batch at %s" % BATCH, file=sys.stderr)
        return 1
    text = BATCH.read_text(encoding="utf-8", errors="replace")
    stmts = sum(1 for l in text.splitlines()
                if l.strip() and not l.lstrip().startswith("#"))
    creates = sum(1 for l in text.splitlines() if l.strip() == "CREATE")

    tpl = PAGE.read_text(encoding="utf-8")
    page = tpl % ("The daily batch", "The daily batch",
                  "%s creations · %s" % (creates, format(stmts, ",")),
                  datetime.date.today().isoformat(), esc(text))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(page)

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
    if "CREATE" not in built or len(built) < len(text):
        print("the batch did not reach the page", file=sys.stderr)
        return 1
    print("%s -> %s creations, %s statement lines, %s bytes"
          % (OUT, creates, stmts, len(built)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
