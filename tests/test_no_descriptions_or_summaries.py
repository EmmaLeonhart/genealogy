"""No batch carries a description, and nothing anywhere sets an edit summary.

**Emma, 2026-08-30:** *"It's a hard rule that we never create items with descriptions."* Then,
widening it: *"edit summaries and descriptions are the easiest ways to get caught we
categorically never use them."*

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


def test_no_batch_carries_a_description():
    offenders = []
    for path in sorted(REPO.glob("reports/*.qs")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            m = DESCRIPTION.match(line)
            if m:
                offenders.append(f"{path.name}:{n} sets {m.group(1)}")
    assert not offenders, (
        "descriptions are categorically never emitted -- Emma, 2026-08-30: "
        f"{offenders[:8]}")


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
        "an edit summary is never set -- *\"edit summaries and descriptions are the easiest "
        f"ways to get caught we categorically never use them\"*: {offenders[:8]}")
