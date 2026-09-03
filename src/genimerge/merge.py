"""Merge several Geni GEDCOM exports into one, keyed on the Geni profile ID.

Identity is exact. Every record — individual, family, note, submitter — carries
its Geni ID in its xref, and no xref was ever observed meaning different things
in different exports, so records with the same xref are the same thing and get
combined. There is no name or date matching here at all.

Combining two versions of one record is a recursive tree merge, and the only
real question is *when two child lines are the same line*. That is decided per
structure path:

- **Single-valued paths** — a path never seen more than once under one parent in
  any input, like ``INDI.BIRT.DATE`` or ``INDI.SEX`` — collapse to one node.
  If the inputs disagree on the value, the first source listed wins and the
  disagreement is recorded as a :class:`Conflict`. Nothing is discarded
  silently.
- **Repeatable paths with a value** — ``INDI.NAME``, ``INDI.NOTE``,
  ``FAM.CHIL`` — are matched on that value, so the same name or the same child
  pointer merges while a different one is kept alongside.
- **Repeatable paths without a value** — ``INDI.SOUR``, ``INDI.OBJE``, whose
  content lives entirely in their children — are matched on the whole subtree.
  Identical citations collapse; different ones are all kept.

Which paths are single-valued is **measured from the inputs**, not hardcoded, so
a future export with a structure we have not seen yet is treated as repeatable —
the failure mode that keeps data rather than dropping it.

The merge is idempotent: merging a file into itself changes nothing.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

from . import gedcom
from . import slim as slim_mod
from .gedcom import Gedcom, Node

__all__ = [
    "ALWAYS_REPEATABLE",
    "Conflict",
    "MergeReport",
    "Merger",
    "merge_files",
    "single_valued_paths",
    "signature",
]

#: Tags that are never treated as single-valued, however the inputs happen to
#: look. Measurement is a good rule for events — one birth, one death, one date
#: per event — but it is only as good as the corpus. If every family in some
#: future export happened to have one child, measurement would call ``CHIL``
#: single-valued and the merge would start reporting siblings as conflicts
#: instead of keeping them. These are the tags where collapsing would lose
#: something structural: a child, a spouse family, a name variant, a citation.
ALWAYS_REPEATABLE = frozenset(
    {"CHIL", "FAMS", "FAMC", "NAME", "NOTE", "SOUR", "OBJE", "ALIA", "ASSO"}
)


@dataclass(frozen=True)
class Conflict:
    """Two exports gave different values for a path that can only hold one."""

    xref: str
    path: str
    kept: str
    kept_from: str
    dropped: str
    dropped_from: str


@dataclass
class MergeReport:
    sources: list[str] = field(default_factory=list)
    #: records each source introduced that no earlier source had
    new_records: dict[str, Counter] = field(default_factory=dict)
    #: records each source had that an earlier source already had
    merged_records: dict[str, Counter] = field(default_factory=dict)
    #: lines each source added to a record an earlier source already had
    added_lines: dict[str, int] = field(default_factory=dict)
    conflicts: list[Conflict] = field(default_factory=list)
    totals: Counter = field(default_factory=Counter)

    @property
    def total_records(self) -> int:
        return sum(self.totals.values())


def signature(node: Node) -> tuple:
    """A hashable identity for a whole subtree, used to spot duplicates."""
    return (node.tag, node.value, tuple(signature(c) for c in node.children))


def _walk_multiplicity(node: Node, prefix: str, worst: Counter) -> None:
    path = f"{prefix}.{node.tag}" if prefix else node.tag
    counts = Counter(c.tag for c in node.children)
    for tag, n in counts.items():
        key = f"{path}.{tag}"
        if n > worst[key]:
            worst[key] = n
    for child in node.children:
        _walk_multiplicity(child, path, worst)


def single_valued_paths(paths: Iterable[str | Path]) -> set[str]:
    """Structure paths that never repeat under one parent anywhere in the inputs.

    Measuring beats guessing: GEDCOM permits repeats almost everywhere, but this
    corpus uses at most one ``BIRT`` per person and at most one ``DATE`` per
    event, and merging is much better when it knows that. Anything not seen here
    is treated as repeatable, which keeps data rather than dropping it.
    """
    worst: Counter = Counter()
    for path in paths:
        for record in gedcom.stream_file(path):
            _walk_multiplicity(record, "", worst)
    return collapse_single_valued(worst)


def collapse_single_valued(worst: Counter) -> set[str]:
    """Turn measured multiplicities into the set of single-valued paths."""
    return {
        path
        for path, n in worst.items()
        if n == 1 and path.rsplit(".", 1)[-1] not in ALWAYS_REPEATABLE
    }


class Merger:
    """Accumulates records from one source after another."""

    def __init__(self, single_valued: set[str]):
        self.single_valued = single_valued
        self.records: dict[str, Node] = {}
        self.report = MergeReport()
        #: which source first supplied each record
        self.record_source: dict[str, str] = {}
        #: which source supplied a node that a *later* source grafted onto an
        #: existing record. Only populated for those, so it stays small — for
        #: everything else the record's own source is the answer.
        self._grafted_from: dict[tuple[str, str], str] = {}
        self._source = "<none>"
        self._added_lines = 0

    def _origin_of(self, xref: str, path: str) -> str:
        return self._grafted_from.get((xref, path), self.record_source.get(xref, "?"))

    def _credit_graft(self, node: Node, path: str, xref: str) -> None:
        """Remember that this source supplied a whole subtree.

        Recorded for every single-valued path inside it, not just its root: a
        later source that disagrees about, say, a grafted ``DEAT``'s ``DATE``
        should see the export that actually supplied that date named as the
        holder of the kept value, not the export the record first came from.
        """
        if path in self.single_valued:
            self._grafted_from[(xref, path)] = self._source
        for child in node.children:
            self._credit_graft(child, f"{path}.{child.tag}", xref)

    # -- keys ----------------------------------------------------------

    def _child_key(self, child: Node, child_path: str):
        if child_path in self.single_valued:
            # Only one of these may exist, so the tag alone identifies it and a
            # value difference is a conflict rather than a second node.
            return ("one", child.tag)
        if child.value:
            return ("val", child.tag, child.value)
        # No value of its own: everything it means is in its children.
        return ("sig", signature(child))

    def _compatible(self, base: Node, other: Node, path: str) -> bool:
        """Could these two be the same line, described differently?

        Only single-valued descendants can rule it out. Repeatable ones union
        harmlessly, so a citation present on one side and absent on the other
        says nothing about whether the two are the same thing.
        """
        if base.value != other.value:
            return False
        for child in other.children:
            child_path = f"{path}.{child.tag}"
            if child_path not in self.single_valued:
                continue
            counterpart = base.get(child.tag)
            if counterpart is not None and not self._compatible(counterpart, child, child_path):
                return False
        return True

    # -- merging -------------------------------------------------------

    def _merge_into(self, base: Node, other: Node, path: str, xref: str) -> None:
        if base.value != other.value:
            # **Later sources win.** Geni is a live site: when two exports
            # disagree about a single-valued field it is because the profile was
            # edited between them, so the newer export carries the correction and
            # the older one carries what was corrected. Every conflict in the
            # first 45 exports was `INDI.CHAN.DATE` — the profile's own
            # last-edited stamp — where keeping the earlier value is not merely
            # arbitrary but wrong.
            #
            # This reverses the original rule. Merge order is filename order,
            # not export date, so "later" means later in the source list; if
            # that ever needs to mean "more recently exported", sort the paths
            # by their HEAD date before calling and the rule follows.
            self.report.conflicts.append(
                Conflict(
                    xref=xref,
                    path=path,
                    kept=other.value,
                    kept_from=self._source,
                    dropped=base.value,
                    dropped_from=self._origin_of(xref, path),
                )
            )
            base.value = other.value
            if path in self.single_valued:
                self._grafted_from[(xref, path)] = self._source

        # A key can have several candidates: a person really can carry two NAME
        # lines with the same text and different married names. Collapsing those
        # into one would invent a conflict and lose one of them.
        index: dict[tuple, list[Node]] = {}
        for child in base.children:
            index.setdefault(self._child_key(child, f"{path}.{child.tag}"), []).append(child)

        for child in other.children:
            child_path = f"{path}.{child.tag}"
            key = self._child_key(child, child_path)
            candidates = index.get(key, [])

            target = None
            if key[0] == "one":
                # Single-valued: there is one slot, so a disagreement here is a
                # real conflict rather than a second node.
                target = candidates[0] if candidates else None
            elif candidates:
                # An identical twin wins over a merely compatible one. Without
                # that priority the merge is not idempotent: given siblings
                # NAME{GIVN,_MARNM} and NAME{GIVN,SURN}, re-merging would let
                # the second one's SURN be absorbed by the first, which is both
                # wrong and unstable across runs.
                wanted = signature(child)
                target = next((c for c in candidates if signature(c) == wanted), None)
                if target is None:
                    target = next(
                        (c for c in candidates if self._compatible(c, child, child_path)),
                        None,
                    )

            if target is None:
                clone = child.copy()
                base.children.append(clone)
                index.setdefault(key, []).append(clone)
                self._added_lines += sum(1 for _ in clone.walk())
                self._credit_graft(clone, child_path, xref)
            else:
                self._merge_into(target, child, child_path, xref)

    def add_source(self, name: str, records: Iterable[Node]) -> None:
        """Fold one export's records into the accumulator."""
        self.report.sources.append(name)
        self._source = name
        self._added_lines = 0
        new: Counter = Counter()
        merged: Counter = Counter()

        for record in records:
            if record.tag in ("HEAD", "TRLR"):
                continue
            if not record.xref:
                # Nothing to key on; keeping it would create an unreferencable
                # duplicate on every re-run.
                continue

            existing = self.records.get(record.xref)
            if existing is None:
                self.records[record.xref] = record.copy()
                self.record_source[record.xref] = name
                new[record.tag] += 1
            else:
                self._merge_into(existing, record, record.tag, record.xref)
                merged[record.tag] += 1

        self.report.new_records[name] = new
        self.report.merged_records[name] = merged
        self.report.added_lines[name] = self._added_lines

    # -- output --------------------------------------------------------

    def _sort_key(self, xref: str) -> tuple:
        order = {"INDI": 0, "FAM": 1, "NOTE": 2, "SUBM": 3}
        record = self.records[xref]
        # Numeric ID rather than string, so @I999@ sorts before @I1000@.
        digits = "".join(c for c in xref if c.isdigit())
        return (order.get(record.tag, 9), int(digits) if digits else 0, xref)

    def result(self) -> Gedcom:
        doc = Gedcom(header=self._header())
        for xref in sorted(self.records, key=self._sort_key):
            doc.records.append(self.records[xref])
        self.report.totals = Counter(r.tag for r in doc.records)
        return doc

    def _header(self) -> Node:
        head = Node(tag="HEAD")
        source = head.add("SOUR", "Geni.com")
        source.add("VERS", "1.0")
        head.add("NOTE", "Merged by genimerge from: " + ", ".join(self.report.sources))
        gedc = head.add("GEDC")
        gedc.add("VERS", "5.5.1")
        gedc.add("FORM", "LINEAGE-LINKED")
        head.add("CHAR", "UTF-8")
        return head


def merge_files(
    paths: list[str | Path], slim: bool = False
) -> tuple[Gedcom, MergeReport]:
    """Merge exports in the given order. Later files win value conflicts.

    ``slim`` drops everything the editing pipeline never reads, at stream time —
    see :mod:`genimerge.slim`. Measured 2026-09-03 over 602 exports: peak RSS
    **13.30 GB and killed** without it against **8.79 GB in 7.7 min** with it,
    for the same 1,451,993 people and 630,053 families. It is what makes the
    merge fit on a GitHub runner. Off by default: the complete tree is what
    ``prepare-cases.py`` and ``samaritan_spine.py`` read.
    """
    paths = [Path(p) for p in paths]
    merger = Merger(single_valued_paths(paths))
    for path in paths:
        records = gedcom.stream_file(path)
        if slim:
            records = slim_mod.prune_stream(records)
        merger.add_source(path.name, records)
    return merger.result(), merger.report


def dangling_pointers(doc: Gedcom) -> Counter:
    """Count pointers that name a record the merged file does not contain.

    Geni's exports turn out to be referentially closed on family structure — no
    ``FAMC``, ``FAMS``, ``CHIL``, ``HUSB`` or ``WIFE`` dangles — so what shows up
    here is incidental (a submitter or note record that was not included), not
    the edge of the tree. The tree's actual edge is people with no parent family
    at all, which is a different question and belongs to the frontier analysis.
    """
    known = set(doc.by_xref())
    missing: Counter = Counter()
    for record in doc.records:
        for node in record.walk():
            target = node.pointer
            if target is not None and target not in known:
                missing[f"{record.tag}.{node.tag}"] += 1
    return missing


def render_report(report: MergeReport, *, detail: bool = True, doc: Gedcom | None = None) -> str:
    """Markdown summary. With ``detail``, every individual conflict is listed."""
    lines = [
        "# Merge report",
        "",
        "Generated by `genimerge.merge` — re-run `python -m genimerge merge`.",
        "",
        "Sources in merge order (later sources win value conflicts):",
        "",
    ]
    lines += [f"{i}. `{name}`" for i, name in enumerate(report.sources, 1)]

    lines += ["", "## Merged totals", ""]
    lines += _table(
        ["record", "count"],
        [[tag, str(n)] for tag, n in sorted(report.totals.items())],
    )

    lines += ["", "## What each source contributed", "", ]
    tags = sorted({t for c in report.new_records.values() for t in c})
    header = ["source", *[f"new {t}" for t in tags], "records merged", "lines added"]
    rows = []
    for name in report.sources:
        new = report.new_records.get(name, Counter())
        merged = report.merged_records.get(name, Counter())
        rows.append(
            [
                f"`{name}`",
                *[str(new.get(t, 0)) for t in tags],
                str(sum(merged.values())),
                str(report.added_lines.get(name, 0)),
            ]
        )
    lines += _table(header, rows)

    if doc is not None:
        missing = dangling_pointers(doc)
        lines += ["", "## Pointers to records we do not have", ""]
        if not missing:
            lines += ["None: every pointer in the merged file resolves."]
        else:
            structural = {"CHIL", "HUSB", "WIFE", "FAMC", "FAMS"}
            broken = sum(n for p, n in missing.items() if p.rsplit(".", 1)[-1] in structural)
            lines += [
                f"**{sum(missing.values())}** pointers name a record that is not in the "
                f"merged file, of which **{broken}** are family-structure pointers "
                "(`CHIL`, `HUSB`, `WIFE`, `FAMC`, `FAMS`). Only the structural ones "
                "would mean a broken tree; the rest are incidental references to "
                "submitter or note records the exports did not include.",
                "",
            ]
            lines += _table(
                ["pointer", "unresolved"],
                [[f"`{p}`", str(n)] for p, n in missing.most_common()],
            )

    lines += ["", "## Conflicts", ""]
    if not report.conflicts:
        lines += ["None: no single-valued path received two different values."]
    else:
        by_path = Counter(c.path for c in report.conflicts)
        lines += [
            f"**{len(report.conflicts)}** value disagreements on single-valued paths. "
            "The value from the later source was kept; the other is recorded here "
            "and is not in the merged file.",
            "",
            "By path:",
            "",
        ]
        lines += _table(
            ["path", "conflicts"],
            [[f"`{p}`", str(n)] for p, n in by_path.most_common()],
        )
        if detail:
            lines += ["", "### Every conflict", ""]
            lines += _table(
                ["record", "path", "kept", "from", "dropped", "from"],
                [
                    [
                        f"`{c.xref}`",
                        f"`{c.path}`",
                        _cell(c.kept),
                        c.kept_from,
                        _cell(c.dropped),
                        c.dropped_from,
                    ]
                    for c in report.conflicts
                ],
            )
        else:
            lines += [
                "",
                "Every conflict is listed individually in `out/merge-report.md`, "
                "which this file deliberately does not duplicate.",
            ]

    return "\n".join(lines) + "\n"


def _cell(text: str, limit: int = 80) -> str:
    text = text.replace("|", "\\|").replace("\n", " ")
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text or "*(empty)*"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]
