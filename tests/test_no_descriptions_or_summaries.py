"""No batch carries a description, and nothing anywhere sets an edit summary.

**It is a hard rule that items are never created with descriptions**, widened the same day to
cover edit summaries: those are categorically never used either.

`CLAUDE.md` § *NO descriptions and NO edit summaries* is the rule. This is the guard, because
the rule is categorical and a single slip is the kind that is only noticed by somebody else.

A `#` comment inside a `.qs` file is not an edit summary -- it never reaches Wikidata -- so the
description check reads statement lines only.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

#: QuickStatements sets a description with `D<lang>`, exactly as it sets a label with `L<lang>`.
DESCRIPTION = re.compile(r"^(?:LAST|-?Q[1-9][0-9]*)\t(D[a-z][a-z-]*)\t")

#: Ways an edit summary reaches WIKIDATA -- an API parameter or a QuickStatements flag.
#:
#: **Narrowed on a false positive, deliberately named here.** `build-orderlife-batch.py` takes
#: `--summary reports/orderlife-batch-summary.csv`: a local CSV of what the run did, which
#: never leaves the disk. Matching that would have made the guard noisy enough to be disabled,
#: which is how a categorical rule stops being enforced. A line is only an offence when the
#: summary is being SENT -- a URL parameter, a request payload key, or an assignment whose
#: value is not a path.
SUMMARY = re.compile(r"&summary=|[?&]summary|summary\s*=\s*[\"']"
                     r"|[\"']summary[\"']\s*:|EDIT_SUMMARY")
#: A match is forgiven when the line is plainly about a local file.
LOCAL_FILE = re.compile(r"\.csv|\.tsv|\.json|\.md|reports/|out/|add_argument")


#: **The one exception, and it is narrow.** All patronymics get the description
#: *patronymic* so they deduplicate properly, because duplicate patronymics were being
#: created to the point of intolerability. All surnames get *family name*, and any
#: matronymics get *matronymic*.
#:
#: The description is what makes Wikidata itself refuse the duplicate -- a label and description
#: must be unique together per language. So this test is NARROWED rather than weakened: exactly
#: these three strings, only in `Den`, and nothing else anywhere.
ALLOWED_DESCRIPTIONS = {"patronymic", "family name", "matronymic"}

#: ⛔ **`Den` ON AN EXISTING ITEM COUNTS, NOT ONLY ON A `CREATE`.** This was `^LAST	Den	...`,
#: which reads the exception too narrowly: a name item ALREADY on Wikidata is described now, and
#: the four rows that do it -- `Q112261760`, `Q124785549`, `Q131994301`, `Q98139923` -- were ruled
#: intentional on 2026-09-09, asked directly: *"both are intentional lol and matronymic too"*.
DEN = re.compile(r'^(?:LAST|Q[1-9][0-9]*)	Den	"([^"]*)"$')

#: ⛔ **THE DAILY BATCH IS NOT A `.qs` FILE, AND IT WAS OUTSIDE EVERY DESCRIPTION GUARD.**
#: This test globbed `reports/*.qs`; the batch the pipeline actually composes and sends is
#: `reports/wikidata-garborg-day.txt`, so a description in it -- intentional or not -- was
#: unchecked. Found 2026-09-09 while reading why the batch carried `Den "family name"`.
#: Measured before widening: all 16 `Den` lines in today's batch are already allowed, so this
#: catches nothing today and would catch the next one.
BATCHES = ["reports/*.qs", "reports/wikidata-garborg-day.txt"]


def test_no_batch_carries_a_description():
    offenders = []
    for path in sorted({p for pattern in BATCHES for p in REPO.glob(pattern)}):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            m = DESCRIPTION.match(line)
            if not m:
                continue
            allowed = DEN.match(line)
            if allowed and allowed.group(1) in ALLOWED_DESCRIPTIONS:
                continue
            offenders.append(f"{path.name}:{n} sets {m.group(1)}  {line.strip()[:60]}")
    assert not offenders, (
        "descriptions are emitted ONLY as Den on a name item, and only "
        f"{sorted(ALLOWED_DESCRIPTIONS)} -- ruled 2026-09-01: {offenders[:8]}")


def test_nothing_sets_an_edit_summary():
    offenders = []
    for pattern in ("scripts/*.py", "src/genimerge/*.py", ".github/workflows/*.yml"):
        for path in sorted(REPO.glob(pattern)):
            # This file names the thing it forbids, which is not the same as setting one.
            if path.name == Path(__file__).name:
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith(("#", "*")) or '"""' in line:
                    continue
                if SUMMARY.search(line) and not LOCAL_FILE.search(line):
                    offenders.append(f"{path.relative_to(REPO)}:{n}  {line.strip()[:80]}")
    assert not offenders, (
        "an edit summary is never set, categorically -- ruled 2026-08-30. "
        f"{offenders[:8]}")
