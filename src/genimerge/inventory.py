"""What is actually inside the exports, measured rather than assumed.

The merge rules and the Wikidata mapping both depend on facts about these files
— which tags exist, how often, and whether the three exports describe the same
people — so those facts get measured once, here, and written to a committed
report instead of being rediscovered by each step.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import gedcom
from .gedcom import Node
from .identity import geni_id_of

__all__ = ["FileProfile", "Inventory", "profile_file", "build_inventory", "render_markdown"]

# Note bodies are free text and their sub-structure is not interesting for
# modelling; counting paths inside them would bury the signal.
_PATH_DEPTH_LIMIT = 4


@dataclass
class FileProfile:
    """One export, measured."""

    name: str
    size_bytes: int
    records_by_tag: Counter = field(default_factory=Counter)
    tag_paths: Counter = field(default_factory=Counter)
    ids_by_tag: dict[str, set[str]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def individuals(self) -> set[str]:
        return self.ids_by_tag.get("INDI", set())

    @property
    def families(self) -> set[str]:
        return self.ids_by_tag.get("FAM", set())


@dataclass
class Inventory:
    """Every export, plus how they overlap."""

    files: list[FileProfile] = field(default_factory=list)

    def union(self, tag: str) -> set[str]:
        return set().union(*(f.ids_by_tag.get(tag, set()) for f in self.files)) if self.files else set()

    def intersection(self, tag: str) -> set[str]:
        if not self.files:
            return set()
        sets = [f.ids_by_tag.get(tag, set()) for f in self.files]
        return set.intersection(*sets) if sets else set()

    def unique_to(self, tag: str, name: str) -> set[str]:
        """IDs of ``tag`` records that only one export has."""
        mine: set[str] = set()
        others: set[str] = set()
        for profile in self.files:
            target = mine if profile.name == name else others
            target |= profile.ids_by_tag.get(tag, set())
        return mine - others


def _count_paths(node: Node, prefix: str, counter: Counter, depth: int) -> None:
    path = f"{prefix}.{node.tag}" if prefix else node.tag
    counter[path] += 1
    if depth >= _PATH_DEPTH_LIMIT:
        return
    for child in node.children:
        _count_paths(child, path, counter, depth + 1)


def profile_file(path: str | Path) -> FileProfile:
    path = Path(path)
    doc = gedcom.parse_file(path)

    profile = FileProfile(
        name=path.name,
        size_bytes=path.stat().st_size,
        warnings=list(doc.warnings),
    )

    for record in doc.records:
        profile.records_by_tag[record.tag] += 1
        _count_paths(record, "", profile.tag_paths, 1)
        geni_id = geni_id_of(record)
        if geni_id is not None:
            profile.ids_by_tag.setdefault(record.tag, set()).add(geni_id)

    return profile


def build_inventory(paths: list[str | Path]) -> Inventory:
    return Inventory(files=[profile_file(p) for p in paths])


def _pct(part: int, whole: int) -> str:
    return f"{100.0 * part / whole:.1f}%" if whole else "n/a"


def _table(header: list[str], rows: list[list[str]], align_right_from: int = 1) -> list[str]:
    sep = ["---" if i < align_right_from else "---:" for i in range(len(header))]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def _headline(inv: Inventory) -> list[str]:
    """The two or three sentences someone reading this report actually needs."""
    if not inv.files:
        return ["No exports profiled."]

    counts = [len(f.individuals) for f in inv.files]
    union = inv.union("INDI")
    shared = inv.intersection("INDI")
    lines = []

    if len(set(counts)) == 1 and len(inv.files) > 1 and counts[0] > 0:
        lines.append(
            f"**Every export here contains exactly {counts[0]} individuals.** An "
            "identical count across differently-scoped exports suggests Geni is "
            "truncating each to that size rather than it being coincidence — but "
            "read it as a lower bound, not a cap. The first three exports agreed "
            "on 3836 exactly and every export since has held more, so agreement "
            "across the exports in hand has already failed once to mean a limit. "
            "See `genimerge.seeds.GENI_EXPORT_CAP` for what 28 exports say about "
            "that bound."
        )
        lines.append("")

    biggest = max(counts) if counts else 0
    lines.append(
        f"The exports together describe **{len(union)} distinct individuals** and "
        f"**{len(inv.union('FAM'))} distinct families**, against {biggest} in the "
        f"largest single export. Only **{len(shared)}** individuals "
        f"({_pct(len(shared), len(union))}) appear in all of them."
    )

    if biggest and len(union) > biggest:
        lines += [
            "",
            f"So merging is worth {len(union) - biggest} individuals over the best "
            "single export — the exports are overlapping slices of one tree, not "
            "copies of it.",
        ]

    return lines


def render_markdown(inv: Inventory) -> str:
    names = [f.name for f in inv.files]
    lines: list[str] = [
        "# Export inventory",
        "",
        "Generated by `genimerge.inventory` — do not hand-edit; re-run",
        "`python -m genimerge inventory` instead.",
        "",
        "## Files",
        "",
    ]

    lines += _table(
        ["file", "size", "warnings"],
        [
            [f"`{f.name}`", f"{f.size_bytes / 1e6:.1f} MB", str(len(f.warnings))]
            for f in inv.files
        ],
    )

    lines += ["", "## Headline", "", *_headline(inv)]

    lines += ["", "## Records by type", ""]
    all_tags = sorted({t for f in inv.files for t in f.records_by_tag})
    lines += _table(
        ["record", *names],
        [[tag, *[str(f.records_by_tag.get(tag, 0)) for f in inv.files]] for tag in all_tags],
    )

    for tag, label in (("INDI", "Individuals"), ("FAM", "Families")):
        union = inv.union(tag)
        shared = inv.intersection(tag)
        lines += [
            "",
            f"## {label} — Geni ID overlap",
            "",
            f"Union across all exports: **{len(union)}**. "
            f"Present in every export: **{len(shared)}** ({_pct(len(shared), len(union))}).",
            "",
        ]
        lines += _table(
            ["export", "count", "unique to it", "shared with all"],
            [
                [
                    f"`{f.name}`",
                    str(len(f.ids_by_tag.get(tag, set()))),
                    str(len(inv.unique_to(tag, f.name))),
                    str(len(f.ids_by_tag.get(tag, set()) & shared)),
                ]
                for f in inv.files
            ],
        )

        if len(inv.files) > 1:
            lines += ["", f"Pairwise overlap ({label.lower()}):", ""]
            rows = []
            for f in inv.files:
                row = [f"`{f.name}`"]
                for g in inv.files:
                    row.append(str(len(f.ids_by_tag.get(tag, set()) & g.ids_by_tag.get(tag, set()))))
                rows.append(row)
            lines += _table(["", *names], rows)

    lines += [
        "",
        "## Tag vocabulary",
        "",
        f"Every structure path down to depth {_PATH_DEPTH_LIMIT}, with the number of",
        "times it occurs in each export. This is the field list the canonical",
        "model and the Wikidata mapping are built from.",
        "",
    ]
    all_paths = sorted({p for f in inv.files for p in f.tag_paths})
    lines += _table(
        ["path", *names],
        [[f"`{p}`", *[str(f.tag_paths.get(p, 0)) for f in inv.files]] for p in all_paths],
    )

    return "\n".join(lines) + "\n"
