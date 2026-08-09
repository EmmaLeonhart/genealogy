"""Parents Wikidata records for our people that our own tree does not have.

`todo.md` § 8b calls this the thing neither tree can do alone, and it is the
only measurement here that produces *both* an export target and an
entity-resolution input:

- a parent whose item carries a **Geni ID we have never exported** is a profile
  that exists on Geni, sits one hop above somebody we already hold, and is
  therefore a doorway `frontier` cannot see — `frontier` ranks *our* parentless
  people and knows nothing about what Wikidata says is above them;
- a parent whose item carries **no Geni ID at all** is the other case entirely.
  Wikidata knows a person Geni may not, and linking them is entity resolution
  rather than exporting.

**This is deliberately not `crosscheck`.** That module compares matched pairs
and only calls a relationship comparable when *both* ends are linked to items —
so "Wikidata names a father we do not hold" is invisible to it by construction,
which is the right call there and is exactly the question here.

**Offline.** Everything comes from `wikidata/items/` through
:mod:`genimerge.wikistore`. Nothing in this module may query Wikidata; see
`CLAUDE.md` § *Never query Wikidata to check something*.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .model import Tree
from .wikistore import StoreReader

__all__ = [
    "FATHER",
    "MOTHER",
    "Finding",
    "Result",
    "find_missing_parents",
    "render_markdown",
]

#: Wikidata's parent properties. Documented in `CLAUDE.md` § *Identity and
#: structure*; `P22` is father and `P25` is mother.
FATHER = "P22"
MOTHER = "P25"

PARENT_PROPERTIES = (FATHER, MOTHER)

#: What we can say about a parent Wikidata names.
EXPORTABLE = "exportable"      # has a Geni ID, and we have never exported it
UNLINKED = "unlinked"          # Wikidata knows the person, no Geni ID on the item
HELD = "held"                  # we already have this person


def _parent_qids(entity: dict) -> list[tuple[str, str]]:
    """``[(property, parent QID)]`` for one item, guarding the empty shapes.

    Same guards as :func:`genimerge.wikidownload.relatives`: a
    ``novalue``/``somevalue`` snak has no ``datavalue``, and a datavalue that is
    not an entity id occurs and is malformed rather than fatal.
    """
    found: list[tuple[str, str]] = []
    claims = entity.get("claims") or {}
    for prop in PARENT_PROPERTIES:
        for statement in claims.get(prop) or []:
            snak = statement.get("mainsnak") or {}
            if snak.get("snaktype") != "value":
                continue
            value = (snak.get("datavalue") or {}).get("value")
            qid = value.get("id") if isinstance(value, dict) else None
            if isinstance(qid, str) and qid.startswith("Q"):
                found.append((prop, qid))
    return found


@dataclass(frozen=True)
class Finding:
    """One parent Wikidata names for one of our people."""

    child_geni_id: str
    child_qid: str
    relation: str
    parent_qid: str
    status: str
    #: Set only when the parent's item carries one. More than one is possible
    #: and is kept whole for the same reason the P2600 map keeps pairs.
    parent_geni_ids: tuple[str, ...] = ()

    @property
    def is_father(self) -> bool:
        return self.relation == FATHER


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)
    #: Our people that carry a QID and were actually looked at.
    matched: int = 0
    #: Of those, how many the store could not produce an item for. Not an
    #: error: the map lists every P2600 on Wikidata and the download stopped
    #: short of some of them.
    not_stored: int = 0
    counts: Counter = field(default_factory=Counter)

    def by_status(self, status: str) -> list[Finding]:
        return [f for f in self.findings if f.status == status]


def find_missing_parents(
    tree: Tree,
    reader: StoreReader,
    qid_by_geni_id: dict[str, str],
    *,
    progress: Callable[[int, int], None] | None = None,
    batch: int = 5000,
) -> Result:
    """Every parent a matched person's item names that our tree does not hold.

    ``qid_by_geni_id`` is the join, normally read from the P2600 map. Where one
    Geni ID has several items the caller decides which to pass; this function
    does not choose, because picking one silently is exactly the thing
    `reports/wikidata-doubles.md` exists to stop.
    """
    result = Result()
    ours = tree.people

    wanted = [(geni_id, qid) for geni_id, qid in qid_by_geni_id.items() if geni_id in ours]
    result.matched = len(wanted)

    for start in range(0, len(wanted), batch):
        chunk = wanted[start : start + batch]
        entities = reader.entities([qid for _, qid in chunk])

        # Two passes over the chunk: gather every parent QID first so the
        # QID -> Geni ID join is one batched query rather than one per parent.
        claimed: list[tuple[str, str, str, str]] = []  # child geni, child qid, relation, parent qid
        for geni_id, qid in chunk:
            entity = entities.get(qid)
            if entity is None:
                result.not_stored += 1
                continue
            for relation, parent_qid in _parent_qids(entity):
                claimed.append((geni_id, qid, relation, parent_qid))

        geni_by_parent = reader.geni_ids_of_qids(p for _, _, _, p in claimed)

        for geni_id, qid, relation, parent_qid in claimed:
            person = ours[geni_id]
            parent_geni = tuple(geni_by_parent.get(parent_qid, ()))
            if not parent_geni:
                status = UNLINKED
            elif any(g in ours for g in parent_geni):
                status = HELD
            else:
                status = EXPORTABLE
            # Only report what we lack. A parent we already hold is the normal
            # case and would bury the two that matter.
            if status != HELD:
                result.findings.append(
                    Finding(
                        child_geni_id=geni_id,
                        child_qid=qid,
                        relation=relation,
                        parent_qid=parent_qid,
                        status=status,
                        parent_geni_ids=parent_geni,
                    )
                )
            result.counts[status] += 1
            # Whether *our* record already gives them that parent is the
            # difference between "Wikidata knows more" and "we know it by
            # another route", and it is what makes a finding an export target
            # rather than a curiosity.
            has_ours = person.father_id if relation == FATHER else person.mother_id
            result.counts["ours_blank" if not has_ours else "ours_present"] += 1
        if progress is not None:
            progress(min(start + batch, len(wanted)), len(wanted))

    return result


def render_markdown(result: Result, tree: Tree, limit: int = 400) -> str:
    exportable = result.by_status(EXPORTABLE)
    unlinked = result.by_status(UNLINKED)

    lines = [
        "# Parents Wikidata records that our tree does not have",
        "",
        "Generated by `genimerge.wikidata-ancestors` — re-run "
        "`python -m genimerge wikidata-ancestors`. Offline: every figure comes "
        "from the downloaded store, never from a query.",
        "",
        f"Measured over the **{len(tree.people):,}-person merge**, across the "
        f"**{result.matched:,}** of our people carrying a Wikidata item.",
        "",
        "## What Wikidata says is above us",
        "",
        "| | count |",
        "| --- | ---: |",
        f"| parent statements read | {sum(result.counts[s] for s in (EXPORTABLE, UNLINKED, HELD)):,} |",
        f"| …parent we already hold | {result.counts[HELD]:,} |",
        f"| **…parent with a Geni ID we have never exported** | {result.counts[EXPORTABLE]:,} |",
        f"| …parent with no Geni ID on the item | {result.counts[UNLINKED]:,} |",
        f"| items the map lists but the store lacks | {result.not_stored:,} |",
        "",
        "**The two middle rows are different problems.** A parent carrying a "
        "Geni ID is a profile that exists on Geni one hop above somebody we "
        "already hold — a doorway `frontier` cannot see, because `frontier` "
        "ranks our own parentless people and knows nothing about what Wikidata "
        "says is above them. A parent with no Geni ID is a person Wikidata "
        "knows and Geni may not, which is entity resolution, not exporting.",
        "",
    ]

    if exportable:
        lines += [
            f"## Geni profiles one hop above us — {len(exportable):,}",
            "",
            "Each row is an export target: the Geni ID exists and no export "
            "here has reached it.",
            "",
            "| our person | relation | Wikidata parent | parent's Geni ID |",
            "| --- | :-: | --- | --- |",
        ]
        for finding in exportable[:limit]:
            person = tree.people.get(finding.child_geni_id)
            name = person.display_name if person else finding.child_geni_id
            relation = "father" if finding.is_father else "mother"
            ids = ", ".join(f"`{g}`" for g in finding.parent_geni_ids)
            lines.append(
                f"| [{name}](https://www.geni.com/people/x/{finding.child_geni_id}) "
                f"| {relation} "
                f"| [{finding.parent_qid}](https://www.wikidata.org/wiki/{finding.parent_qid}) "
                f"| {ids} |"
            )
        if len(exportable) > limit:
            lines.append("")
            lines.append(f"*{len(exportable) - limit:,} further rows not shown.*")
        lines.append("")

    lines += [
        f"## Parents with no Geni link — {len(unlinked):,}",
        "",
        "Wikidata knows these people; nothing here says Geni does. Linking "
        "them is entity resolution and needs a human, so they are counted "
        "rather than listed.",
        "",
    ]
    return "\n".join(lines) + "\n"
