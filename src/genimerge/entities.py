"""Read Emma's hand-made Geni-to-Wikidata resolutions out of `entity_resolution.md`.

Everything else in this project derives links by machine — the exact P2600 join,
then structural expansion outward from it. This file is the other direction: a
human looked at a Geni profile and a Wikidata item and *knew* they were the same
person, which is evidence no query here can produce. It is also where label
corrections go, since noticing that Q11443857 should read "Mononobe no Futohime"
is the same act of recognition.

**The source file is prose and is expected to stay prose.** Emma wrote "they're
a bit unstructured" at the top of it, and a format that demands structure would
turn a scratchpad into a chore and stop getting used. So this parser reads what
is unambiguously machine-readable — Geni URLs, Wikidata URLs, and a small set of
label instructions — and **reports every line it could not understand** rather
than dropping it. An entry written in a shape this does not know is a visible
`unparsed` row in the report, never a silent omission.

**This module writes a file. It does not write to Wikidata.** Same rule as
:mod:`genimerge.quickstatements`: a batch is executed by a human who is
accountable for it.

**The grouping rule is "one of each, greedily", not "split on blank lines".**
Blank lines were the obvious rule and are the wrong one: Emma's last entry puts
the item, the profile and the label instruction in three separate blocks, and
splitting there reported a complete entry as two unparsable halves. So instead
this walks the file and starts a new entry exactly when the next line would give
the current one a *second* Geni profile or a *second* Wikidata item. Every entry
therefore holds at most one of each, blank lines or not, and an entry holding
one of each is a resolution.

That is still proximity, but it is deterministic and it cannot pair the wrong
two: the moment a second profile appears the entry has already ended. What it
will not do is untangle a genuinely interleaved block — that is reported
unparsed, because pairing several by order would be exactly the kind of
plausible-looking inference this repo refuses everywhere else.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .identity import profile_url

__all__ = [
    "Resolution",
    "LabelEdit",
    "Unparsed",
    "ResolutionFile",
    "parse",
    "read_file",
    "render_markdown",
]

#: A Geni profile URL, in the shapes the site actually emits. The ID is the last
#: path segment before any query string; the slug before it may be
#: percent-encoded CJK and is deliberately not interpreted.
GENI_URL_RE = re.compile(r"geni\.com/people/[^/\s]*/(\d{6,})")

#: A Wikidata item URL or a bare QID.
QID_URL_RE = re.compile(r"wikidata\.org/wiki/(Q\d+)")
BARE_QID_RE = re.compile(r"\bQ\d+\b")

#: Label instructions. Each must name the language, because a label written into
#: the wrong language overwrites someone else's work and is not recoverable by
#: anyone who does not read that language.
#:
#: ``eng?\w*`` rather than ``english``: the source file already contains
#: "engligh", and a typo in a scratchpad should not cost a real edit. It stays
#: anchored to "en" so it can never match a different language's name.
_LABEL_PATTERNS = (
    re.compile(r'^\s*(?:set|add)\s+eng?\w*\s*label\s+"?(?P<text>[^"]+)"?\s*$', re.I),
    re.compile(r'^\s*change\s+(?:his|her|their|the)\s+name\s+to\s+"?(?P<text>[^"]+)"?\s*$', re.I),
)

#: Corrections to the **Geni** side, not to a Wikidata label.
#:
#: An export is a snapshot: a profile renamed on Geni afterwards keeps its old
#: name in every GEDCOM already taken, and no re-parse fixes that. Emma,
#: 2026-08-12, on her own profile: *"the name on that one is 'Emma Leonhart' …
#: already corrected on geni, the exports here are just old."*
#:
#: Keyed by **Geni ID**, because that is what is wrong — the person may have no
#: Wikidata item at all, and `LabelEdit` cannot express a correction to a record
#: that exists only on our side.
#:
#: The quotes are required. A correction that silently swallowed the rest of a
#: sentence would rename somebody to a fragment of prose.
_NAME_CORRECTION_PATTERNS = (
    re.compile(
        r'^\s*the name (?:on |for |of )?(?:that one|this one|them|him|her|it|this)?\s*'
        r'is\s+"(?P<text>[^"]+)"',
        re.I,
    ),
    re.compile(r'^\s*(?:the )?real name (?:is|was)\s+"(?P<text>[^"]+)"', re.I),
    re.compile(r'^\s*rename (?:to|as)\s+"(?P<text>[^"]+)"', re.I),
)


@dataclass(frozen=True)
class Resolution:
    """One asserted identity: this Geni profile is this Wikidata item."""

    geni_id: str
    qid: str
    #: the block this came from, verbatim, so a reviewer can see the context
    context: str = ""

    @property
    def url(self) -> str:
        return profile_url(self.geni_id)


@dataclass(frozen=True)
class LabelEdit:
    """A label correction on an item, in one language."""

    qid: str
    language: str
    text: str
    context: str = ""


@dataclass(frozen=True)
class NameCorrection:
    """The Geni record's name is stale; this is the current one.

    Distinct from :class:`LabelEdit`, which asks for an edit *on Wikidata*. This
    asks for our own derived data to stop repeating something an old export
    said. Nothing is edited anywhere; the correction overrides at derivation.
    """

    geni_id: str
    text: str
    context: str = ""

    @property
    def url(self) -> str:
        return profile_url(self.geni_id)


@dataclass(frozen=True)
class Unparsed:
    """A line that named something but was not understood.

    Kept and reported. The whole point of tolerating a free-form source file is
    that unrecognised entries stay visible instead of vanishing.
    """

    text: str
    reason: str


@dataclass
class ResolutionFile:
    resolutions: list[Resolution] = field(default_factory=list)
    labels: list[LabelEdit] = field(default_factory=list)
    name_corrections: list[NameCorrection] = field(default_factory=list)
    unparsed: list[Unparsed] = field(default_factory=list)

    def corrected_names(self) -> dict[str, str]:
        """``geni_id -> corrected name``, last entry winning.

        Later wins for the same reason merges do: a second correction on one
        profile is a further correction, not a competing one.
        """
        return {c.geni_id: c.text for c in self.name_corrections}

    @property
    def qids(self) -> set[str]:
        return {r.qid for r in self.resolutions} | {e.qid for e in self.labels}


def _entries(text: str) -> list[str]:
    """Greedy runs holding at most one Geni profile and at most one Wikidata item.

    See the module docstring for why this is not a blank-line split. Blank lines
    are kept inside an entry and are not boundaries; the boundary is the second
    profile or the second item.
    """
    out: list[str] = []
    current: list[str] = []
    geni: set[str] = set()
    qids: set[str] = set()

    def flush() -> None:
        if any(line.strip() for line in current):
            out.append("\n".join(current).strip("\n"))

    for line in text.splitlines():
        line_geni = set(GENI_URL_RE.findall(line))
        line_qids = set(QID_URL_RE.findall(line)) or set(BARE_QID_RE.findall(line))
        starts_new = (line_geni and geni and not (line_geni <= geni)) or (
            line_qids and qids and not (line_qids <= qids)
        )
        if starts_new:
            flush()
            current, geni, qids = [], set(), set()
        current.append(line)
        geni |= line_geni
        qids |= line_qids

    flush()
    return out


def _label_edit_in(line: str) -> str | None:
    for pattern in _LABEL_PATTERNS:
        found = pattern.match(line)
        if found:
            return found.group("text").strip()
    return None


def _name_correction_in(line: str) -> str | None:
    for pattern in _NAME_CORRECTION_PATTERNS:
        found = pattern.match(line)
        if found:
            return found.group("text").strip()
    return None


def parse(text: str) -> ResolutionFile:
    """Read resolutions, label edits and anything unrecognised out of the prose.

    A block yields a resolution when it names exactly one Geni profile and
    exactly one Wikidata item. Anything else about it — headings, nicknames,
    "This guy:" — is ignored as context rather than treated as a failure, since
    the file is written for a human first.
    """
    result = ResolutionFile()

    for block in _entries(text):
        geni = list(dict.fromkeys(GENI_URL_RE.findall(block)))
        qids = list(dict.fromkeys(QID_URL_RE.findall(block)))
        if not qids:
            # A bare QID counts only when no URL form is present, so that a
            # block quoting both does not double-count the same item.
            qids = list(dict.fromkeys(BARE_QID_RE.findall(block)))

        labels = [t for line in block.splitlines() if (t := _label_edit_in(line))]
        corrections = [
            t for line in block.splitlines() if (t := _name_correction_in(line))
        ]

        if not geni and not qids:
            continue  # prose with nothing machine-readable in it: the preamble

        if len(geni) == 1 and len(qids) == 1:
            result.resolutions.append(Resolution(geni[0], qids[0], context=block))
        elif geni or qids:
            result.unparsed.append(
                Unparsed(
                    block,
                    f"names {len(geni)} Geni profile(s) and {len(qids)} Wikidata item(s); "
                    "a resolution needs exactly one of each, and pairing several by "
                    "order would be a guess",
                )
            )

        for text_value in corrections:
            if len(geni) == 1:
                result.name_corrections.append(
                    NameCorrection(geni[0], text_value, context=block)
                )
            else:
                result.unparsed.append(
                    Unparsed(
                        block,
                        f"a name correction needs exactly one Geni profile to apply to; "
                        f"this block names {len(geni)}",
                    )
                )

        for text_value in labels:
            if len(qids) == 1:
                result.labels.append(
                    LabelEdit(qids[0], "en", text_value, context=block)
                )
            else:
                result.unparsed.append(
                    Unparsed(
                        block,
                        f"label edit {text_value!r} but the block names {len(qids)} "
                        "Wikidata items, so which one to edit is not determined",
                    )
                )

    return result


def read_file(path: str | Path) -> ResolutionFile:
    return parse(Path(path).read_text(encoding="utf-8"))


def render_markdown(
    parsed: ResolutionFile, source: str, retrieved: str, known: set[str] | None = None
) -> str:
    known = known or set()
    lines = [
        "# Entity resolutions from `entity_resolution.md`",
        "",
        "Generated by `genimerge.entity-resolution` — re-run",
        "`python -m genimerge entity-resolution`.",
        "",
        f"Read from `{source}`, retrieved date `{retrieved}`.",
        "",
        "These links are **asserted by a human**, not derived. That is what makes",
        "them worth having — a person recognised the same individual on both",
        "sites, which no query in this repo can do — and also what makes them",
        "unverifiable from here. Nothing below has been checked against Wikidata.",
        "",
        "**Nothing has been sent to Wikidata.** Review before running the batch.",
        "",
    ]

    lines += ["## Geni to Wikidata", ""]
    if parsed.resolutions:
        rows = []
        for r in parsed.resolutions:
            held = "yes" if r.geni_id in known else "**not in our tree**"
            rows.append(
                f"| [{r.geni_id}]({r.url}) | "
                f"[{r.qid}](https://www.wikidata.org/wiki/{r.qid}) | {held} |"
            )
        lines += [
            "| Geni profile | Wikidata item | in the merged tree |",
            "| --- | --- | --- |",
            *rows,
            "",
        ]
        missing = [r for r in parsed.resolutions if r.geni_id not in known]
        if missing:
            lines += [
                f"**{len(missing)} of these name a profile the merged tree does not "
                "hold.** That does not make the link wrong — Emma can resolve someone "
                "no export has reached — but it does mean this repo cannot corroborate "
                "it, so the P2600 value rests entirely on the source file.",
                "",
            ]
    else:
        lines += ["None found.", ""]

    lines += ["## Label edits", ""]
    if parsed.labels:
        lines += [
            "| item | language | new label |",
            "| --- | --- | --- |",
            *[
                f"| [{e.qid}](https://www.wikidata.org/wiki/{e.qid}) | {e.language} | {e.text} |"
                for e in parsed.labels
            ],
            "",
            "**A label edit overwrites what someone else wrote.** Each of these was",
            "requested explicitly in the source file; none is inferred. The language",
            "is English in every case because that is the only language the source",
            "file names, and applying a label to the wrong language is not a",
            "recoverable mistake worth risking on a guess.",
            "",
        ]
    else:
        lines += ["None found.", ""]

    lines += ["## Not understood", ""]
    if parsed.unparsed:
        lines += [
            f"**{len(parsed.unparsed)} entries were not understood** and are in no",
            "batch. They are listed rather than dropped, which is the whole reason",
            "the source file is allowed to stay unstructured.",
            "",
        ]
        for item in parsed.unparsed:
            lines += [f"- {item.reason}", "", "  ```", *[f"  {l}" for l in item.text.splitlines()], "  ```", ""]
    else:
        lines += ["Nothing. Every entry naming a profile or an item was understood.", ""]

    return "\n".join(lines) + "\n"
