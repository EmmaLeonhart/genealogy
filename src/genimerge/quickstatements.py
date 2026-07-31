"""Emit a QuickStatements batch adding P2600 to Wikidata items that lack it.

Every link found by structural expansion is a Wikidata item that describes
somebody with a Geni profile, where the item does not say so. Adding the Geni
ID is the smallest useful edit this project can offer back: it costs one
statement, it is checkable against the profile it names, and once it exists the
*exact* P2600 join finds that person on every future run — so each edit here
makes the next reconciliation cheaper.

**This module writes a file. It does not write to Wikidata**, and nothing here
should be run unreviewed. QuickStatements batches are executed by a human who
is accountable for them.

Two safety rules, both enforced rather than assumed:

- only links confirmed by *structure* are eligible. Name-search proposals never
  reach this file, however good their score looked;
- the current P2600 of every target item is fetched first. An item that already
  carries the same ID needs no edit; an item carrying a *different* one is a
  contradiction that a human has to resolve, and it is reported rather than
  overwritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .identity import profile_url
from .model import Tree
from .wikidata import WikidataClient

__all__ = [
    "Statement",
    "render_statements",
    "Edit",
    "Batch",
    "build_batch",
    "render_quickstatements",
    "render_markdown",
]

PROPERTY = "P2600"


@dataclass(frozen=True)
class Statement:
    """One QuickStatements v1 line.

    ``value`` is already in QS form — a bare ``Q123`` for an item, a quoted
    string for anything else — because the caller knows the datatype and this
    does not.
    """

    qid: str
    prop: str
    value: str
    #: (property, value) pairs written after the claim
    qualifiers: tuple[tuple[str, str], ...] = ()
    #: (S-property, value) pairs; QS marks reference parts with an S prefix
    references: tuple[tuple[str, str], ...] = ()

    def to_line(self) -> str:
        fields = [self.qid, self.prop, self.value]
        for prop, value in self.qualifiers:
            fields += [prop, value]
        for prop, value in self.references:
            fields += [prop, value]
        return "\t".join(fields)


def render_statements(statements: list[Statement]) -> str:
    """Render lines, tab-separated, with a trailing newline only if non-empty."""
    lines = [s.to_line() for s in statements]
    return "\n".join(lines) + ("\n" if lines else "")


def geni_reference(geni_id: str, retrieved: str) -> tuple[tuple[str, str], ...]:
    """The reference every statement here carries: where it came from, and when."""
    return (
        ("S854", f'"{profile_url(geni_id)}"'),
        ("S813", f"+{retrieved}T00:00:00Z/11"),
    )


@dataclass(frozen=True)
class Edit:
    qid: str
    geni_id: str
    name: str = ""

    @property
    def url(self) -> str:
        return profile_url(self.geni_id)


@dataclass
class Batch:
    edits: list[Edit] = field(default_factory=list)
    #: item already carries exactly this Geni ID — nothing to do
    already_present: list[Edit] = field(default_factory=list)
    #: item carries a *different* Geni ID; (edit, the ID already there)
    conflicting: list[tuple[Edit, str]] = field(default_factory=list)
    retrieved: str = ""


def _existing_p2600(client: WikidataClient, qids: list[str], batch_size: int = 200) -> dict[str, str]:
    found: dict[str, str] = {}
    for start in range(0, len(qids), batch_size):
        batch = qids[start : start + batch_size]
        values = " ".join(f"wd:{q}" for q in batch)
        query = (
            "SELECT ?item ?geni WHERE {\n"
            f"  VALUES ?item {{ {values} }}\n"
            f"  ?item wdt:{PROPERTY} ?geni.\n"
            "}"
        )
        for row in client.sparql(query):
            found[row["item"].rsplit("/", 1)[-1]] = row["geni"]
    return found


def build_batch(
    client: WikidataClient,
    tree: Tree,
    links: dict[str, str],
    *,
    retrieved: str,
) -> Batch:
    """Turn ``geni_id -> qid`` links into edits, checking what is already there.

    ``retrieved`` is the date for the reference qualifier, as ``YYYY-MM-DD``.
    It is passed in rather than read from the clock so a re-run reproduces the
    same file.
    """
    batch = Batch(retrieved=retrieved)
    existing = _existing_p2600(client, sorted(set(links.values())))

    for geni_id, qid in sorted(links.items(), key=lambda kv: kv[1]):
        person = tree.people.get(geni_id)
        edit = Edit(qid=qid, geni_id=geni_id, name=person.display_name if person else "")
        current = existing.get(qid)
        if current is None:
            batch.edits.append(edit)
        elif current == geni_id:
            batch.already_present.append(edit)
        else:
            batch.conflicting.append((edit, current))

    return batch


def render_quickstatements(batch: Batch) -> str:
    """QuickStatements v1: tab-separated, one statement per line.

    Each statement carries a reference — S854 the Geni profile URL, S813 the
    date retrieved — so the edit can be checked against its source rather than
    landing unattributed.
    """
    return render_statements(
        [
            Statement(
                qid=edit.qid,
                prop=PROPERTY,
                value=f'"{edit.geni_id}"',
                references=geni_reference(edit.geni_id, batch.retrieved),
            )
            for edit in batch.edits
        ]
    )


def render_markdown(batch: Batch) -> str:
    lines = [
        "# QuickStatements batch: add Geni profile IDs",
        "",
        "Generated by `genimerge.quickstatements` — re-run",
        "`python -m genimerge quickstatements`.",
        "",
        "**Nothing here has been sent to Wikidata.** `add-p2600.qs` is a file to",
        "read, check and — if you agree with it — run yourself at",
        "<https://quickstatements.toolforge.org/>. Every row names a Geni profile",
        "you can open and compare against the Wikidata item.",
        "",
        "Only links confirmed by family structure are included. Name-search",
        "proposals are excluded however good their score looked, because a",
        "matching string is not evidence that two records are the same person.",
        "",
        f"| | count |",
        "| --- | ---: |",
        f"| statements to add | {len(batch.edits)} |",
        f"| already correct, skipped | {len(batch.already_present)} |",
        f"| **contradicting an existing ID — for you to resolve** | {len(batch.conflicting)} |",
        "",
    ]

    if batch.conflicting:
        lines += [
            "## Contradictions",
            "",
            "These Wikidata items already carry a *different* Geni profile ID than",
            "the one we matched. That means either our match is wrong or the item",
            "already points at a duplicate Geni profile. Neither is safe to",
            "overwrite, so none of these are in the batch file.",
            "",
            "| item | our match | already on Wikidata | person |",
            "| --- | --- | --- | --- |",
        ]
        for edit, current in batch.conflicting:
            lines.append(
                f"| [{edit.qid}](https://www.wikidata.org/wiki/{edit.qid}) "
                f"| [{edit.geni_id}]({edit.url}) "
                f"| [{current}]({profile_url(current)}) "
                f"| {edit.name} |"
            )
        lines.append("")

    if batch.edits:
        lines += [
            "## Statements in the batch",
            "",
            "| item | Geni profile | person |",
            "| --- | --- | --- |",
        ]
        for edit in batch.edits:
            lines.append(
                f"| [{edit.qid}](https://www.wikidata.org/wiki/{edit.qid}) "
                f"| [{edit.geni_id}]({edit.url}) "
                f"| {edit.name} |"
            )
        lines.append("")

    return "\n".join(lines)
