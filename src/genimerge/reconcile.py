"""Second-pass reconciliation: expand outward from the people we already matched.

Matching by Geni ID gets 209 of 8766. The obvious next move — search Wikidata for
each remaining name — means thousands of blind queries and would return mostly
noise, because "Ola Nilsson, born about 1620" matches nothing or matches
everything.

Structure is far better evidence than names. If our Sverker I is Wikidata's
Q357435, then *our* Sverker's father and Wikidata's ``P22`` of Q357435 are the
same person, and the only question left is whether the names and dates agree
well enough to say so out loud. So this walks outward from the confirmed
matches — parents, spouses, children — one ring at a time, and stops when a ring
adds nothing.

Nothing here is written back to Wikidata and nothing is auto-accepted into the
final answer. High-confidence links are used to keep walking, and every
proposal — accepted or not — lands in the candidate file with its evidence, for
a human to judge.
"""

from __future__ import annotations

import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .model import Person, Tree
from .wikidata import WikidataClient

__all__ = [
    "Candidate",
    "Relative",
    "ExpansionResult",
    "normalise_name",
    "name_score",
    "expand_from_matches",
    "fetch_relatives",
    "distance_from_matched",
    "search_targets",
    "search_candidates",
    "label_candidates",
    "name_variants",
    "LABEL_LANGUAGES",
]

#: Languages whose labels and aliases are worth checking. This tree is
#: Norwegian, Swedish and Danish with a medieval European fringe, and Wikidata
#: labels those people in whichever language wrote about them.
LABEL_LANGUAGES = ("en", "no", "nb", "nn", "sv", "da", "de", "is")

#: Relationship properties, and what each means when read from the item.
ROLE_BY_PROPERTY = {
    "P22": "father",
    "P25": "mother",
    "P26": "spouse",
    "P40": "child",
}

#: Words that carry no identifying weight when comparing a Geni name with a
#: Wikidata label. Deliberately short: dropping too much makes everything match.
_STOPWORDS = frozenset(
    {"of", "av", "van", "von", "de", "der", "den", "the", "og", "and", "til", "a"}
)

_TRANSLITERATE = str.maketrans(
    {"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "å": "a", "Å": "a", "ß": "ss", "þ": "th", "ð": "d"}
)

#: How far apart two birth or death years may be and still corroborate. Wider
#: for dates the export itself marked approximate.
YEAR_TOLERANCE = 3
YEAR_TOLERANCE_APPROX = 10
#: Beyond this, the years actively contradict each other and veto the match.
YEAR_CONTRADICTION = 25

HIGH, MEDIUM, LOW = "high", "medium", "low"


@dataclass(frozen=True)
class Relative:
    """A Wikidata item related to one we have already matched."""

    qid: str
    role: str
    label: str = ""
    birth_year: int | None = None
    death_year: int | None = None
    geni_id: str | None = None


@dataclass
class Candidate:
    """A proposed Geni-to-Wikidata link, with the evidence for it."""

    geni_id: str
    qid: str
    confidence: str
    role: str
    via_geni_id: str
    via_qid: str
    geni_name: str = ""
    wikidata_label: str = ""
    name_score: float = 0.0
    year_evidence: str = ""
    accepted: bool = False

    def to_row(self) -> list:
        return [
            self.geni_id,
            self.qid,
            self.confidence,
            "yes" if self.accepted else "no",
            self.role,
            self.via_geni_id,
            self.via_qid,
            self.geni_name,
            self.wikidata_label,
            f"{self.name_score:.2f}",
            self.year_evidence,
        ]


CANDIDATE_COLUMNS = [
    "geni_id",
    "qid",
    "confidence",
    "used_to_expand",
    "role",
    "via_geni_id",
    "via_qid",
    "geni_name",
    "wikidata_label",
    "name_score",
    "year_evidence",
]


@dataclass
class ExpansionResult:
    candidates: list[Candidate] = field(default_factory=list)
    #: geni_id -> qid, seeds plus everything accepted along the way
    confirmed: dict[str, str] = field(default_factory=dict)
    rings: int = 0
    #: how many new links each ring added, for the report
    per_ring: list[int] = field(default_factory=list)


def normalise_name(text: str) -> list[str]:
    """Fold a name to comparable tokens.

    Geni names and Wikidata labels are written very differently — "Sigurd II
    Munn Haraldsøn Konge av Norge" against "Sigurd II of Norway" — so this
    strips diacritics and punctuation and drops a few connective words, leaving
    the parts that actually identify someone.
    """
    text = text.translate(_TRANSLITERATE)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
    return [t for t in cleaned.split() if t and t not in _STOPWORDS]


def name_score(left: str, right: str) -> float:
    """Overlap of the two names, relative to the shorter one.

    Containment rather than Jaccard, because one side is routinely much longer:
    a Geni name piles on patronymics and titles that the Wikidata label omits,
    and penalising that would reject good matches.
    """
    a, b = set(normalise_name(left)), set(normalise_name(right))
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _year_of(value: str | None) -> int | None:
    """Pull the year out of a Wikidata time literal like ``+1130-01-01T00:00:00Z``.

    Wikidata sometimes returns a blank node instead of a date ("some value"), so
    anything that is not a plain literal has to be discarded rather than parsed.
    """
    if not value or "genid" in value:
        return None
    text = value.lstrip("+")
    negative = value.startswith("-")
    head = text.split("-", 1)[0] if not negative else text.split("-", 2)[1]
    try:
        year = int(head)
    except ValueError:
        return None
    return -year if negative else year


def _compare_years(
    person_year: int | None,
    other_year: int | None,
    approximate: bool,
    label: str,
) -> tuple[int, str]:
    """Score one year pair: +1 agrees, -1 contradicts, 0 says nothing."""
    if person_year is None or other_year is None:
        return 0, ""
    gap = abs(person_year - other_year)
    tolerance = YEAR_TOLERANCE_APPROX if approximate else YEAR_TOLERANCE
    if gap <= tolerance:
        return 1, f"{label} {person_year}~{other_year}"
    if gap >= YEAR_CONTRADICTION:
        return -1, f"{label} {person_year} vs {other_year} (differ by {gap})"
    return 0, f"{label} {person_year} vs {other_year}"


def _is_approximate(person: Person, kind: str) -> bool:
    event = person.events.get(kind)
    return bool(event and event.date and event.date.modifier)


def score_pair(
    person: Person,
    relative: Relative,
    *,
    person_name: str | None = None,
    structural: bool = True,
) -> tuple[str | None, float, str]:
    """Judge one proposed link. Returns (confidence or None, name score, evidence).

    ``structural`` says whether a relationship stands behind the proposal. It
    matters a great deal. When we already know this is the father of a matched
    person, a good name is strong corroboration. When all we have is a matching
    string, it is much weaker — this tree is full of Scandinavian patronymics,
    and "Peder Christensen" is four different people on Wikidata. So without a
    relationship, a name alone never reaches high confidence; a date has to
    agree too.
    """
    score = name_score(person_name or person.display_name, relative.label)

    birth_vote, birth_note = _compare_years(
        person.birth_year, relative.birth_year, _is_approximate(person, "birth"), "birth"
    )
    death_vote, death_note = _compare_years(
        person.death_year, relative.death_year, _is_approximate(person, "death"), "death"
    )
    evidence = "; ".join(n for n in (birth_note, death_note) if n)

    if birth_vote < 0 or death_vote < 0:
        # The dates say these are different people. The relationship being right
        # does not outrank that, so the pair is dropped rather than downgraded.
        return None, score, evidence or "dates contradict"

    agreeing = max(birth_vote, 0) + max(death_vote, 0)

    if not structural:
        # No relationship behind this — only a string matched.
        if agreeing and score >= 0.6:
            return HIGH, score, evidence
        if agreeing or score >= 0.6:
            return MEDIUM, score, evidence or "name matches, no dates to check"
        return LOW, score, evidence

    if agreeing and score >= 0.34:
        return HIGH, score, evidence
    if score >= 0.6:
        return HIGH, score, evidence or "names agree strongly"
    if score >= 0.34 or agreeing:
        return MEDIUM, score, evidence
    if score > 0:
        return LOW, score, evidence
    return None, score, evidence or "nothing in common"


#: Label languages the SPARQL form asked for, in the order it asked. Kept
#: identical so the offline port picks the same label the endpoint would have.
LABEL_LANGUAGES = ("en", "no", "nb", "nn", "sv", "da", "de", "fr")


def _best_label(entity: dict) -> str:
    labels = entity.get("labels") or {}
    for lang in LABEL_LANGUAGES:
        value = (labels.get(lang) or {}).get("value")
        if value:
            return value
    return ""


def _truthy_values(entity: dict, prop: str) -> list:
    """Statement values for ``prop`` under ``wdt:`` semantics.

    Preferred rank if any exist, otherwise normal; never deprecated. The SPARQL
    form used ``wdt:`` throughout, so reading every statement here would widen
    what reconciliation sees and quietly change its scoring.
    """
    statements = (entity.get("claims") or {}).get(prop) or []
    live = [s for s in statements if s.get("rank") != "deprecated"]
    chosen = [s for s in live if s.get("rank") == "preferred"] or live
    out = []
    for statement in chosen:
        snak = statement.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if value is not None:
            out.append(value)
    return out


def relatives_from_store(reader, qids: Iterable[str]) -> dict[str, list[Relative]]:
    """:func:`fetch_relatives`, answered from the downloaded store.

    `queue.md` 2.B. This is the call site the store is *best* suited to: the
    download grew the set by walking P22/P25/P26/P40/P3373, so a matched item's
    relatives are in the store by construction — they are why it was fetched.

    Two shapes are reproduced deliberately rather than approximated:

    * **Label choice.** The query asked for `en,no,nb,nn,sv,da,de,fr` in that
      order; :data:`LABEL_LANGUAGES` keeps it, so the label a candidate is
      scored on does not change with the data source.
    * **Truthy ranks.** ``wdt:`` is preferred-rank-if-any, else normal, never
      deprecated — see :func:`_truthy_values`.

    A relative the download never reached is still returned, with its QID and
    role and no label or dates, exactly as the endpoint would have done for an
    item carrying no label in those languages. Dropping it instead would hide a
    real edge from the reconciler.
    """
    ordered = sorted({str(q) for q in qids})
    out: dict[str, list[Relative]] = defaultdict(list)

    items = reader.entities(ordered)
    wanted: set[str] = set()
    edges: list[tuple[str, str, str]] = []
    for qid, entity in items.items():
        for prop, role in ROLE_BY_PROPERTY.items():
            for value in _truthy_values(entity, prop):
                other = value.get("id") if isinstance(value, dict) else None
                if isinstance(other, str) and other.startswith("Q"):
                    edges.append((qid, role, other))
                    wanted.add(other)

    others = reader.entities(wanted)
    seen: set[tuple[str, str, str]] = set()
    for qid, role, other in edges:
        if (qid, role, other) in seen:
            continue
        seen.add((qid, role, other))
        entity = others.get(other) or {}
        births = _truthy_values(entity, "P569")
        deaths = _truthy_values(entity, "P570")
        genis = _truthy_values(entity, "P2600")
        out[qid].append(
            Relative(
                qid=other,
                role=role,
                label=_best_label(entity),
                birth_year=_year_of(births[0].get("time")) if births else None,
                death_year=_year_of(deaths[0].get("time")) if deaths else None,
                geni_id=next((g for g in genis if isinstance(g, str)), None),
            )
        )
    return dict(out)


def fetch_relatives(
    client: WikidataClient, qids: Iterable[str], batch_size: int = 150
) -> dict[str, list[Relative]]:
    """Parents, spouses and children of each item, from one query per batch."""
    ordered = sorted(set(qids))
    out: dict[str, list[Relative]] = defaultdict(list)
    properties = " ".join(f"wdt:{p}" for p in ROLE_BY_PROPERTY)

    for start in range(0, len(ordered), batch_size):
        batch = ordered[start : start + batch_size]
        values = " ".join(f"wd:{q}" for q in batch)
        query = (
            "SELECT ?item ?rel ?other ?otherLabel ?birth ?death ?geni WHERE {\n"
            f"  VALUES ?item {{ {values} }}\n"
            f"  VALUES ?rel {{ {properties} }}\n"
            "  ?item ?rel ?other.\n"
            "  OPTIONAL { ?other wdt:P569 ?birth }\n"
            "  OPTIONAL { ?other wdt:P570 ?death }\n"
            "  OPTIONAL { ?other wdt:P2600 ?geni }\n"
            '  SERVICE wikibase:label { bd:serviceParam wikibase:language '
            '"en,no,nb,nn,sv,da,de,fr". }\n'
            "}"
        )
        merged: dict[tuple[str, str, str], Relative] = {}
        for row in client.sparql(query):
            item = row["item"].rsplit("/", 1)[-1]
            role = ROLE_BY_PROPERTY.get(row["rel"].rsplit("/", 1)[-1])
            other = row["other"].rsplit("/", 1)[-1]
            if role is None or not other.startswith("Q"):
                continue
            key = (item, role, other)
            existing = merged.get(key)
            # One item can carry several birth dates; keep the first real value
            # of each field rather than letting a later blank node erase it.
            merged[key] = Relative(
                qid=other,
                role=role,
                label=row.get("otherLabel") or (existing.label if existing else ""),
                birth_year=_year_of(row.get("birth"))
                or (existing.birth_year if existing else None),
                death_year=_year_of(row.get("death"))
                or (existing.death_year if existing else None),
                geni_id=row.get("geni") or (existing.geni_id if existing else None),
            )
        for (item, _role, _other), relative in merged.items():
            out[item].append(relative)

    return dict(out)


def _neighbour_ids(person: Person, tree: Tree) -> list[str]:
    # parent_ids rather than father_id/mother_id: a child in two families keeps
    # only the first family's father in the primary fields, which would make
    # this relation asymmetric and distort the distance measure.
    ids = person.spouse_ids + person.child_ids + person.parent_ids
    return [i for i in ids if i in tree.people]


def distance_from_matched(tree: Tree, matched: Iterable[str]) -> dict[str, int]:
    """How many family steps each person is from the nearest matched person."""
    from collections import deque

    distance = {geni_id: 0 for geni_id in matched if geni_id in tree.people}
    queue = deque(distance)
    while queue:
        current = queue.popleft()
        for neighbour in _neighbour_ids(tree.people[current], tree):
            if neighbour not in distance:
                distance[neighbour] = distance[current] + 1
                queue.append(neighbour)
    return distance


def search_targets(
    tree: Tree,
    matched: dict[str, str],
    *,
    max_distance: int = 3,
    born_before: int = 1500,
) -> list[Person]:
    """Which unmatched people are worth spending a search request on.

    Searching all 8500 unmatched people by name would mostly return noise: an
    18th-century Norwegian farmer named Ola Nilsson is not on Wikidata, and
    whatever a search returns for him is wrong. Three groups are worth asking
    about — people close to someone we already matched, people the export gave a
    title to, and people old enough that surviving records tend to mean
    prominence.
    """
    distance = distance_from_matched(tree, matched)
    targets = []
    for person in tree.people.values():
        if person.geni_id in matched or not person.display_name:
            continue
        close = distance.get(person.geni_id, 10**6) <= max_distance
        old = person.birth_year is not None and person.birth_year < born_before
        if close or old or person.titles:
            targets.append(person)
    return sorted(targets, key=lambda p: (distance.get(p.geni_id, 10**6), p.geni_id))


def search_candidates(
    client: WikidataClient,
    tree: Tree,
    targets: Iterable[Person],
    matched: dict[str, str],
    *,
    hits_per_person: int = 7,
    progress: Callable[[int, int], None] | None = None,
) -> list[Candidate]:
    """Propose links by searching Wikidata for each target's name.

    These are proposals only. Unlike the structural pass there is no
    relationship to corroborate them, so nothing found here is ever marked
    accepted — the point is to hand a human a short, evidenced list.
    """
    targets = list(targets)
    found: dict[str, list[str]] = {}

    for index, person in enumerate(targets, start=1):
        found[person.geni_id] = client.search_people(person.display_name, hits_per_person)
        if progress is not None:
            progress(index, len(targets))

    details = _fetch_person_details(client, {q for qids in found.values() for q in qids})
    taken = set(matched.values())
    candidates: list[Candidate] = []

    for person in targets:
        for qid in found.get(person.geni_id, []):
            if qid in taken:
                continue
            detail = details.get(qid)
            if detail is None:
                continue
            confidence, score, evidence = score_pair(person, detail)
            if confidence is None or confidence == LOW:
                continue
            candidates.append(
                Candidate(
                    geni_id=person.geni_id,
                    qid=qid,
                    confidence=confidence,
                    role="name-search",
                    via_geni_id="",
                    via_qid="",
                    geni_name=person.display_name,
                    wikidata_label=detail.label,
                    name_score=score,
                    year_evidence=evidence,
                    accepted=False,
                )
            )
    return candidates


def name_variants(person: Person) -> list[str]:
    """The name strings worth looking up for one person.

    Geni names carry patronymics, titles and place phrases that a Wikidata label
    will not have, so the exact-label lookup gets several shots: every ``NAME``
    record the person has, and a plain "first given name + surname" form.

    Single-token variants are dropped. A lookup for "Olof" would match hundreds
    of unrelated people, and nothing downstream could tell them apart — so
    mononyms are simply not reachable this way, which is a real limit of this
    pass rather than something hidden.
    """
    seen: list[str] = []

    def add(text: str) -> None:
        text = " ".join(text.replace("/", " ").split())
        if len(text.split()) >= 2 and text not in seen:
            seen.append(text)

    for name in person.names:
        add(name.display)
        add(name.full)
        if name.given and name.surname:
            add(f"{name.given.split()[0]} {name.surname}")

    return seen


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def label_candidates(
    client: WikidataClient,
    tree: Tree,
    targets: Iterable[Person],
    matched: dict[str, str],
    *,
    languages: Iterable[str] = LABEL_LANGUAGES,
    literals_per_query: int = 600,
    progress: Callable[[int, int], None] | None = None,
) -> list[Candidate]:
    """Propose links by looking each target's name up in Wikidata's label index.

    This replaced a per-name call to the search API, which the endpoint
    rate-limited to roughly one request every twenty seconds — hours for this
    corpus. Exact label and alias matching goes through an index instead, so
    hundreds of names fit in one query and the whole pass takes minutes.

    The trade is recall: exact matching only finds names written the same way on
    both sides, where full-text search tolerated variation. Structural expansion
    is the pass that is meant to catch the rest.

    Proposals only. Nothing here is ever marked accepted — there is no
    relationship behind these, just a string that matched.
    """
    targets = list(targets)
    languages = list(languages)

    wanted: dict[str, list[str]] = {}
    for person in targets:
        variants = name_variants(person)
        if variants:
            wanted[person.geni_id] = variants

    literals = sorted({v for variants in wanted.values() for v in variants})
    found: dict[str, list[Relative]] = defaultdict(list)

    per_batch = max(1, literals_per_query // max(len(languages), 1))
    batches = [literals[i : i + per_batch] for i in range(0, len(literals), per_batch)]

    for index, batch in enumerate(batches, start=1):
        values = " ".join(
            f'"{_escape(name)}"@{lang}' for name in batch for lang in languages
        )
        query = (
            "SELECT ?item ?label ?birth ?death WHERE {\n"
            f"  VALUES ?label {{ {values} }}\n"
            "  ?item rdfs:label|skos:altLabel ?label.\n"
            "  ?item wdt:P31 wd:Q5.\n"
            "  OPTIONAL { ?item wdt:P569 ?birth }\n"
            "  OPTIONAL { ?item wdt:P570 ?death }\n"
            "}"
        )
        merged: dict[tuple[str, str], Relative] = {}
        for row in client.sparql(query):
            qid = row["item"].rsplit("/", 1)[-1]
            label = row["label"]
            key = (label, qid)
            existing = merged.get(key)
            merged[key] = Relative(
                qid=qid,
                role="name-match",
                label=label,
                birth_year=_year_of(row.get("birth"))
                or (existing.birth_year if existing else None),
                death_year=_year_of(row.get("death"))
                or (existing.death_year if existing else None),
            )
        for (label, _qid), relative in merged.items():
            found[label].append(relative)
        if progress is not None:
            progress(index, len(batches))

    taken = set(matched.values())
    candidates: list[Candidate] = []

    for person in targets:
        proposed: set[str] = set()
        mine: list[Candidate] = []
        for variant in wanted.get(person.geni_id, ()):
            for relative in found.get(variant, ()):
                if relative.qid in taken or relative.qid in proposed:
                    continue
                confidence, score, evidence = score_pair(
                    person, relative, person_name=variant, structural=False
                )
                if confidence is None or confidence == LOW:
                    continue
                proposed.add(relative.qid)
                mine.append(
                    Candidate(
                        geni_id=person.geni_id,
                        qid=relative.qid,
                        confidence=confidence,
                        role="name-match",
                        via_geni_id="",
                        via_qid="",
                        geni_name=person.display_name,
                        wikidata_label=relative.label,
                        name_score=score,
                        year_evidence=evidence,
                        accepted=False,
                    )
                )

        # Several Wikidata people answering to one name is itself evidence: the
        # name is not identifying. "Peder Christensen" matches four items, and
        # calling all four high-confidence would be worse than useless to
        # whoever has to review them.
        if len(mine) > 1:
            for candidate in mine:
                if candidate.confidence == HIGH:
                    candidate.confidence = MEDIUM
                candidate.year_evidence = (
                    f"{len(mine)} Wikidata people share this name"
                    + (f"; {candidate.year_evidence}" if candidate.year_evidence else "")
                )
        candidates += mine

    return candidates


def _fetch_person_details(
    client: WikidataClient, qids: Iterable[str], batch_size: int = 200
) -> dict[str, Relative]:
    """Label, birth year, death year and any P2600, for scoring search hits."""
    ordered = sorted(set(qids))
    out: dict[str, Relative] = {}

    for start in range(0, len(ordered), batch_size):
        batch = ordered[start : start + batch_size]
        values = " ".join(f"wd:{q}" for q in batch)
        query = (
            "SELECT ?item ?itemLabel ?birth ?death ?geni WHERE {\n"
            f"  VALUES ?item {{ {values} }}\n"
            "  OPTIONAL { ?item wdt:P569 ?birth }\n"
            "  OPTIONAL { ?item wdt:P570 ?death }\n"
            "  OPTIONAL { ?item wdt:P2600 ?geni }\n"
            '  SERVICE wikibase:label { bd:serviceParam wikibase:language '
            '"en,no,nb,nn,sv,da,de,fr". }\n'
            "}"
        )
        for row in client.sparql(query):
            qid = row["item"].rsplit("/", 1)[-1]
            existing = out.get(qid)
            out[qid] = Relative(
                qid=qid,
                role="name-search",
                label=row.get("itemLabel") or (existing.label if existing else ""),
                birth_year=_year_of(row.get("birth"))
                or (existing.birth_year if existing else None),
                death_year=_year_of(row.get("death"))
                or (existing.death_year if existing else None),
                geni_id=row.get("geni") or (existing.geni_id if existing else None),
            )
    return out


def _relatives_of(person: Person, tree: Tree, role: str) -> list[Person]:
    if role == "father":
        ids = [person.father_id] if person.father_id else []
    elif role == "mother":
        ids = [person.mother_id] if person.mother_id else []
    elif role == "spouse":
        ids = person.spouse_ids
    else:
        ids = person.child_ids
    return [tree.people[i] for i in ids if i in tree.people]


def expand_from_matches(
    client: WikidataClient,
    tree: Tree,
    seeds: dict[str, str],
    *,
    max_rings: int = 12,
    progress: Callable[[int, int], None] | None = None,
) -> ExpansionResult:
    """Walk outward from ``seeds`` (geni_id -> qid) along family links."""
    result = ExpansionResult(confirmed=dict(seeds))
    taken_qids = set(seeds.values())
    frontier = dict(seeds)
    proposed: set[tuple[str, str]] = set()

    for ring in range(1, max_rings + 1):
        if not frontier:
            break
        relatives_by_qid = fetch_relatives(client, frontier.values())
        accepted_this_ring: dict[str, str] = {}

        for geni_id, qid in frontier.items():
            person = tree.people.get(geni_id)
            if person is None:
                continue
            by_role: dict[str, list[Relative]] = defaultdict(list)
            for relative in relatives_by_qid.get(qid, []):
                by_role[relative.role].append(relative)

            for role, wd_relatives in by_role.items():
                ours = [
                    p
                    for p in _relatives_of(person, tree, role)
                    if p.geni_id not in result.confirmed
                ]
                theirs = [r for r in wd_relatives if r.qid not in taken_qids]
                if not ours or not theirs:
                    continue

                scored = []
                for candidate_person in ours:
                    for relative in theirs:
                        confidence, score, evidence = score_pair(candidate_person, relative)
                        if confidence is not None:
                            scored.append((score, candidate_person, relative, confidence, evidence))
                # Best-scoring pairs first, and each side used at most once, so
                # two siblings cannot both claim the same Wikidata item.
                scored.sort(key=lambda row: row[0], reverse=True)
                used_people: set[str] = set()
                used_items: set[str] = set()

                for score, candidate_person, relative, confidence, evidence in scored:
                    if candidate_person.geni_id in used_people or relative.qid in used_items:
                        continue
                    if (candidate_person.geni_id, relative.qid) in proposed:
                        continue
                    used_people.add(candidate_person.geni_id)
                    used_items.add(relative.qid)
                    proposed.add((candidate_person.geni_id, relative.qid))

                    accept = confidence == HIGH and relative.qid not in taken_qids
                    result.candidates.append(
                        Candidate(
                            geni_id=candidate_person.geni_id,
                            qid=relative.qid,
                            confidence=confidence,
                            role=role,
                            via_geni_id=geni_id,
                            via_qid=qid,
                            geni_name=candidate_person.display_name,
                            wikidata_label=relative.label,
                            name_score=score,
                            year_evidence=evidence,
                            accepted=accept,
                        )
                    )
                    if accept:
                        accepted_this_ring[candidate_person.geni_id] = relative.qid
                        taken_qids.add(relative.qid)

        result.confirmed.update(accepted_this_ring)
        result.per_ring.append(len(accepted_this_ring))
        result.rings = ring
        if progress is not None:
            progress(ring, len(accepted_this_ring))
        frontier = accepted_this_ring

    return result
