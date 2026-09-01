"""The canonical view of the tree: people and families, not GEDCOM nodes.

Everything downstream — Wikidata reconciliation, the frontier analysis, the
eventual QuickStatements batches — reads this, not the GEDCOM. The GEDCOM stops
being the working format here.

Two things are deliberately *not* thrown away:

- the raw GEDCOM date text sits next to the parsed one, so a statement can always
  be traced back to what the export actually said;
- relationships are resolved both ways. GEDCOM stores them through families
  (``INDI.FAMC`` points at a family, the family points at parents), and Wikidata
  wants them person-to-person (P22 father, P25 mother), so :class:`Tree` resolves
  and caches both directions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator

from .dates import GedcomDate, parse_date
from .gedcom import Node
from .identity import geni_id_from_pointer, geni_id_from_xref, geni_id_of, profile_url

__all__ = ["Name", "Event", "Person", "Family", "Tree", "build_tree"]

#: GEDCOM event tags worth lifting into the model, and what to call them.
EVENT_TAGS = {
    "BIRT": "birth",
    "DEAT": "death",
    "BAPM": "baptism",
    "BURI": "burial",
}


@dataclass(frozen=True)
class Name:
    """One ``NAME`` line. People routinely have several."""

    #: the whole GEDCOM name, e.g. ``"Emma /Leonhart/"``
    full: str
    given: str = ""
    surname: str = ""
    suffix: str = ""
    married: str = ""
    nicknames: tuple[str, ...] = ()

    @property
    def display(self) -> str:
        """``"Empress Jingū"`` — the slashes around the surname removed."""
        if self.given or self.surname:
            return " ".join(p for p in (self.given, self.surname) if p)
        return self.full.replace("/", "").strip()

    @classmethod
    def from_node(cls, node: Node) -> "Name":
        return cls(
            full=node.value,
            given=node.value_of("GIVN"),
            surname=node.value_of("SURN"),
            suffix=node.value_of("NSFX"),
            married=node.value_of("_MARNM"),
            nicknames=tuple(n.value for n in node.all("NICK") if n.value),
        )


@dataclass(frozen=True)
class Event:
    """A dated and/or placed occurrence. Any field may be missing."""

    kind: str
    date: GedcomDate | None = None
    place: str = ""
    city: str = ""
    state: str = ""
    country: str = ""

    @property
    def year(self) -> int | None:
        return self.date.year if self.date else None

    @property
    def where(self) -> str:
        """The most specific place text available."""
        if self.place:
            return self.place
        return ", ".join(p for p in (self.city, self.state, self.country) if p)

    @property
    def is_empty(self) -> bool:
        return self.date is None and not self.where

    @classmethod
    def from_node(cls, kind: str, node: Node) -> "Event":
        address = node.get("ADDR")
        raw_date = node.value_of("DATE")
        return cls(
            kind=kind,
            date=parse_date(raw_date) if raw_date else None,
            place=node.value_of("PLAC"),
            city=address.value_of("CITY") if address else "",
            state=address.value_of("STAE") if address else "",
            country=address.value_of("CTRY") if address else "",
        )


@dataclass
class Person:
    geni_id: str
    names: list[Name] = field(default_factory=list)
    sex: str = ""
    events: dict[str, Event] = field(default_factory=dict)
    occupations: list[str] = field(default_factory=list)
    titles: list[str] = field(default_factory=list)
    #: families this person is a child in
    child_of: list[str] = field(default_factory=list)
    #: families this person is a spouse in
    spouse_in: list[str] = field(default_factory=list)
    photo_count: int = 0
    about: str = ""

    # -- resolved by Tree ---------------------------------------------
    #: the primary father and mother — what a P22/P25 statement would use
    father_id: str | None = None
    mother_id: str | None = None
    #: *every* parent across every parent family. A person can be a child in
    #: more than one family (adoption, or the same person entered twice), and
    #: keeping only the first would make the family graph asymmetric: the parent
    #: would list the child, the child would not list the parent.
    parent_ids: list[str] = field(default_factory=list)
    spouse_ids: list[str] = field(default_factory=list)
    child_ids: list[str] = field(default_factory=list)

    @property
    def name(self) -> Name | None:
        return self.names[0] if self.names else None

    @property
    def display_name(self) -> str:
        return self.name.display if self.name else ""

    @property
    def birth(self) -> Event | None:
        return self.events.get("birth")

    @property
    def death(self) -> Event | None:
        return self.events.get("death")

    @property
    def birth_year(self) -> int | None:
        return self.birth.year if self.birth else None

    @property
    def death_year(self) -> int | None:
        return self.death.year if self.death else None

    @property
    def url(self) -> str:
        return profile_url(self.geni_id)

    @property
    def has_known_parents(self) -> bool:
        return bool(self.parent_ids)

    def to_json(self) -> dict:
        """A flat, stable dict — this is what lands in `out/people.jsonl`."""
        return {
            "geni_id": self.geni_id,
            "url": self.url,
            "name": self.display_name,
            "names": [
                {
                    "full": n.full,
                    "given": n.given,
                    "surname": n.surname,
                    "suffix": n.suffix,
                    "married": n.married,
                    "nicknames": list(n.nicknames),
                }
                for n in self.names
            ],
            "sex": self.sex,
            "events": {
                kind: {
                    "date_raw": e.date.raw if e.date else None,
                    "year": e.year,
                    "month": e.date.month if e.date else None,
                    "day": e.date.day if e.date else None,
                    "modifier": e.date.modifier if e.date else None,
                    "place": e.where,
                }
                for kind, e in sorted(self.events.items())
            },
            "occupations": self.occupations,
            "titles": self.titles,
            "father_id": self.father_id,
            "mother_id": self.mother_id,
            "parent_ids": self.parent_ids,
            "spouse_ids": self.spouse_ids,
            "child_ids": self.child_ids,
            "child_of_families": self.child_of,
            "spouse_in_families": self.spouse_in,
            "photo_count": self.photo_count,
        }

    @classmethod
    def from_record(cls, record: Node) -> "Person | None":
        geni_id = geni_id_of(record)
        if geni_id is None:
            return None

        person = cls(geni_id=geni_id, sex=record.value_of("SEX"))
        person.names = [Name.from_node(n) for n in record.all("NAME")]

        for tag, kind in EVENT_TAGS.items():
            node = record.get(tag)
            if node is not None:
                event = Event.from_node(kind, node)
                if not event.is_empty:
                    person.events[kind] = event

        person.occupations = [n.value for n in record.all("OCCU") if n.value]
        person.titles = [n.value for n in record.all("TITL") if n.value]
        person.child_of = [
            fid
            for fid in (geni_id_from_pointer(n) for n in record.all("FAMC"))
            if fid
        ]
        person.spouse_in = [
            fid
            for fid in (geni_id_from_pointer(n) for n in record.all("FAMS"))
            if fid
        ]
        person.photo_count = len(record.all("OBJE"))
        for note in record.all("NOTE"):
            if note.value.startswith("{geni:about_me}"):
                person.about = note.value[len("{geni:about_me}") :].strip()
                break
        return person


@dataclass
class Family:
    geni_id: str
    husband_id: str | None = None
    wife_id: str | None = None
    child_ids: list[str] = field(default_factory=list)
    marriage: Event | None = None

    @property
    def parent_ids(self) -> list[str]:
        return [p for p in (self.husband_id, self.wife_id) if p]

    def to_json(self) -> dict:
        return {
            "geni_id": self.geni_id,
            "husband_id": self.husband_id,
            "wife_id": self.wife_id,
            "child_ids": self.child_ids,
            "marriage": (
                {
                    "date_raw": self.marriage.date.raw if self.marriage.date else None,
                    "year": self.marriage.year,
                    "place": self.marriage.where,
                }
                if self.marriage
                else None
            ),
        }

    @classmethod
    def from_record(cls, record: Node) -> "Family | None":
        geni_id = geni_id_of(record)
        if geni_id is None:
            return None
        marriage_node = record.get("MARR")
        marriage = Event.from_node("marriage", marriage_node) if marriage_node else None
        return cls(
            geni_id=geni_id,
            husband_id=geni_id_from_pointer(record.get("HUSB")),
            wife_id=geni_id_from_pointer(record.get("WIFE")),
            child_ids=[
                cid for cid in (geni_id_from_pointer(n) for n in record.all("CHIL")) if cid
            ],
            marriage=marriage,
        )


@dataclass
class Tree:
    people: dict[str, Person] = field(default_factory=dict)
    families: dict[str, Family] = field(default_factory=dict)

    def resolve_relationships(self) -> None:
        """Turn family membership into person-to-person links.

        GEDCOM routes every relationship through a family record; Wikidata wants
        P22/P25/P26/P40 directly between people. Both views are kept, because
        the family is where a marriage date lives and the direct links are what
        a statement needs.
        """
        for person in self.people.values():
            person.father_id = None
            person.mother_id = None
            person.parent_ids = []
            person.spouse_ids = []
            person.child_ids = []

        for family in self.families.values():
            for child_id in family.child_ids:
                child = self.people.get(child_id)
                if child is None:
                    continue
                if family.husband_id and child.father_id is None:
                    child.father_id = family.husband_id
                if family.wife_id and child.mother_id is None:
                    child.mother_id = family.wife_id
                for parent_id in family.parent_ids:
                    if parent_id not in child.parent_ids:
                        child.parent_ids.append(parent_id)

            for parent_id in family.parent_ids:
                parent = self.people.get(parent_id)
                if parent is None:
                    continue
                for other_id in family.parent_ids:
                    if other_id != parent_id and other_id not in parent.spouse_ids:
                        parent.spouse_ids.append(other_id)
                for child_id in family.child_ids:
                    if child_id not in parent.child_ids:
                        parent.child_ids.append(child_id)

    def __len__(self) -> int:
        return len(self.people)


def build_tree(records: Iterable[Node]) -> Tree:
    """Build the canonical model from level-0 GEDCOM records."""
    tree = Tree()
    for record in records:
        if record.tag == "INDI":
            person = Person.from_record(record)
            if person is not None:
                tree.people[person.geni_id] = person
        elif record.tag == "FAM":
            family = Family.from_record(record)
            if family is not None:
                tree.families[family.geni_id] = family
    tree.resolve_relationships()
    return tree
