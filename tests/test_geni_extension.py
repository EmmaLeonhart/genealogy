"""`geni-extension/` is the instrument for every Geni action now, and nothing checked it.

It is JavaScript in a Python repo, so CI ran nothing against it at all: a broken manifest or a
mangled file would have been discovered by Emma, in her browser, in the middle of a run.

**These are build checks, not behaviour tests.** They assert the things whose failure is silent.
What the collector actually *does* is verified the way `CLAUDE.md` § *"Analyse this" means build
a CSV* asks -- the naming algorithm was measured over 400,000 corpus names into
`reports/seed-naming-sample.tsv`, and the path parser was run against a live page and matched
`paths/charlemagne-to-arne-garborg.tsv` at 34 steps. Neither of those belongs in a unit test.

**⛔ THE CONTROL-CHARACTER CHECK IS HERE BECAUSE IT HAPPENED TWICE ON 2026-09-05.** Writing a
file through a non-raw Python string turns `\\b` into U+0008 BACKSPACE, and the result is a
regex that silently matches nothing:

    harvest-isolate-paths.py   `<[^>]*\\bid=` became `<[^>]*\\x08id=`  -- pending() kept lying
    geni-extension/export.js   `/^forest\\b/i`  became `/^forest\\x08/i` -- would have exported
                                                                          the DEFAULT walk

Both were invisible on screen: `sed` prints a backspace as nothing, and the second was found
only by running `cat -A`. The first printed *exactly the same wrong answer* as the bug it was
meant to fix, which is why a fix has to be measured rather than read. A byte-level check costs
nothing and is the only thing that sees them.
"""

from __future__ import annotations

import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
EXT = REPO / "geni-extension"

#: Tab, newline and carriage return are the legitimate ones. Everything else in this range is a
#: control character that no source file should contain.
LEGAL_CONTROLS = {"\t", "\n", "\r"}


def js_files() -> list[pathlib.Path]:
    return sorted(EXT.rglob("*.js"))


pytestmark = pytest.mark.skipif(not EXT.is_dir(), reason="geni-extension/ is absent")


def test_the_manifest_is_valid_and_every_file_it_names_exists():
    """A manifest naming a file that is not there makes Chrome refuse the WHOLE extension.

    Not the one script -- the extension. So a typo in a path is indistinguishable from the
    extension never having been loaded, which on 2026-09-05 was a real question that took a
    check of Chrome's own `Preferences` to answer.
    """
    manifest = json.loads((EXT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == 3

    named = [manifest["background"]["service_worker"]]
    for block in manifest.get("content_scripts", []):
        named.extend(block.get("js", []))
        named.extend(block.get("css", []))
    if "action" in manifest and "default_popup" in manifest["action"]:
        named.append(manifest["action"]["default_popup"])

    missing = [n for n in named if not (EXT / n).is_file()]
    assert not missing, f"manifest.json names files that do not exist: {missing}"


def test_the_extension_only_reaches_geni():
    """Host permissions stay pinned to Geni.

    The collector runs inside her logged-in browser, so its match patterns are the whole of its
    blast radius. A widened pattern would put a content script on every page she visits.
    """
    manifest = json.loads((EXT / "manifest.json").read_text(encoding="utf-8"))
    patterns = list(manifest.get("host_permissions", []))
    for block in manifest.get("content_scripts", []):
        patterns.extend(block.get("matches", []))
    assert patterns, "no host patterns at all"
    for p in patterns:
        assert "geni.com" in p, f"host pattern reaches beyond Geni: {p}"
        assert not p.startswith("*://*/"), f"host pattern matches every site: {p}"


def test_no_source_file_carries_a_control_character():
    """The backspace-in-a-regex bug, which happened twice in one day and was invisible both times.

    `\\b` written into a non-raw generator string becomes U+0008, the pattern then matches
    nothing, and the code goes on returning a plausible answer. `pending()` kept reporting every
    page as still searching; `export.js` would have submitted a `Blood Relatives` walk while
    reporting `Forest`.
    """
    offenders = []
    for path in js_files() + [EXT / "manifest.json", EXT / "popup.html"]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            bad = {c for c in line if ord(c) < 32 and c not in LEGAL_CONTROLS}
            if bad:
                codes = ", ".join(f"U+{ord(c):04X}" for c in sorted(bad))
                offenders.append(f"{path.relative_to(REPO)}:{n} carries {codes}")
    assert not offenders, (
        "a control character in source is almost always `\\b` written through a non-raw string, "
        f"which makes a regex match nothing without saying so: {offenders[:8]}")


def test_the_pushpin_is_never_toggled():
    """Emma, 2026-09-03: *"You do not pin Charlemagne, it needs to be done exactly once and I
    did it."*

    Toggling the anchor mid-run silently re-anchors every later search to *"You"*, which is how
    a batch of profiles came to be queued against the wrong endpoint. The collector reads the
    anchor and never sets it, and that is worth pinning because the call is one line away in
    Geni's own page API.
    """
    for path in js_files():
        text = path.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith(("*", "//", "/*")):
                continue
            assert "toggleRelationshipAnchor" not in line, (
                f"{path.relative_to(REPO)}:{n} toggles the relationship anchor, which is hers "
                "and is set exactly once")


def test_exports_are_never_concurrent_and_never_cancellable():
    """Two of Geni's limits, encoded as limits rather than as settings.

    Emma, 2026-08-18: *"There's no way that you can do an export concurrently. That isn't my
    decision thats geni."* And on cancelling: *"you think you can kill a geni export read the
    fucking docs you can't."* A control implying either is possible offers a choice that cannot
    be carried out, which `CLAUDE.md` § *She answers `AskUserQuestion`* calls worse than a
    missing option.
    """
    background = (EXT / "background.js").read_text(encoding="utf-8")
    assert "EXPORT_CONCURRENCY = 1" in background, (
        "export concurrency is Geni's limit and is not a setting"
    )
    popup = (EXT / "popup.html").read_text(encoding="utf-8")
    assert "EXPORT_CONCURRENCY" not in popup, "export concurrency must not be exposed as a control"
    for word in ("cancel export", "kill export", "abort export"):
        assert word not in popup.lower(), f"the panel offers {word!r}, which Geni cannot do"
