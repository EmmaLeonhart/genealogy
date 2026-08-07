"""Wikidata items carrying two Geni IDs that are both people in our tree.

Our merge keys on the Geni profile ID, so it cannot see these by construction:
two IDs are two people to it. Wikidata has noticed something we cannot — that
one item claims both — and that claim comes from outside our data, which makes
it the only signal here of its kind.

**It is not a duplicate list, and reading it as one is the mistake to avoid.**
Two readings fit every row and nothing in this repo separates them:

- One person with two Geni profiles that Geni itself has not merged.
  `Брячислав Васильевич` against `Bracheslav Vasylkovich Polozki` is the same
  man in two languages.
- Two different people, one of whose P2600 statements is simply wrong.
  `Q233444` carries Scribonia and Clodia Pulchra, who are two of Octavian's
  wives.

So this module reports and does not decide. It puts the two profiles side by
side with everything the tree knows that would distinguish them — dates, sex,
parents, spouses, children — and leaves the judgement to a human. Nothing here
edits Wikidata, edits Geni, or changes the merge.

**Offline.** The P2600 side is read from `out/wikidata/p2600-all.tsv`, which
`genimerge overlap` writes; this module never calls the network. That matters
because the overlap fetch is sixteen partitions over a live endpoint and should
not be re-run to redraw a page.
"""

from __future__ import annotations

import html as _html
from dataclasses import dataclass
from pathlib import Path

from .identity import profile_url
from .model import Person, Tree

__all__ = [
    "Double",
    "load_pairs",
    "find_doubles",
    "render_html",
    "render_markdown",
]

WIKIDATA_URL = "https://www.wikidata.org/wiki/{}"

#: Where `genimerge overlap` leaves the full QID-to-Geni-ID map.
DEFAULT_PAIRS = Path("out/wikidata/p2600-all.tsv")


@dataclass
class Double:
    """One Wikidata item and the people in our tree it claims are the same."""

    qid: str
    people: list[Person]
    #: Geni IDs on the item that are *not* in our tree, kept because an item
    #: claiming three IDs of which we hold two is a different situation from one
    #: claiming exactly the two we hold.
    absent_ids: list[str]

    @property
    def url(self) -> str:
        return WIKIDATA_URL.format(self.qid)

    @property
    def same_name(self) -> bool:
        """Whether every profile shares a display name.

        A weak signal deliberately kept as one: matching names make the
        one-person reading likelier and prove nothing, and differing names are
        exactly what a translation pair looks like.
        """
        names = {(p.display_name or "").strip().casefold() for p in self.people}
        return len(names) == 1 and bool(names.pop())

    @property
    def shares_a_relative(self) -> bool:
        """Whether any two of the profiles name a relative in common.

        This is the strongest thing available without leaving our own data. Two
        profiles for one person usually keep some of the same family; two
        genuinely different people generally do not, unless they are relatives
        of each other.
        """
        seen: list[set[str]] = []
        for person in self.people:
            kin = set(person.parent_ids) | set(person.spouse_ids) | set(person.child_ids)
            if any(kin & other for other in seen):
                return True
            seen.append(kin)
        return False

    @property
    def years_conflict(self) -> bool:
        """Whether two profiles carry birth years more than a lifetime apart.

        Where it is true the one-person reading is hard to sustain. Where it is
        false it says nothing, because most of these profiles have no year.
        """
        years = [p.birth_year for p in self.people if p.birth_year is not None]
        return len(years) > 1 and (max(years) - min(years)) > 120


def load_pairs(path: Path = DEFAULT_PAIRS) -> list[tuple[str, str]]:
    """Read the QID/Geni-ID map `genimerge overlap` wrote."""
    out: list[tuple[str, str]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        qid, _, geni_id = line.partition("\t")
        if qid and geni_id:
            out.append((qid, geni_id))
    return out


def find_doubles(pairs: list[tuple[str, str]], tree: Tree) -> list[Double]:
    """Items whose Geni IDs include two or more people we actually hold."""
    by_item: dict[str, list[str]] = {}
    for qid, geni_id in pairs:
        ids = by_item.setdefault(qid, [])
        if geni_id not in ids:
            ids.append(geni_id)

    doubles: list[Double] = []
    for qid, ids in by_item.items():
        if len(ids) < 2:
            continue
        held = [tree.people[i] for i in sorted(ids) if i in tree.people]
        if len(held) < 2:
            continue
        doubles.append(
            Double(
                qid=qid,
                people=held,
                absent_ids=sorted(i for i in ids if i not in tree.people),
            )
        )

    # Rows a human can settle fastest first: a shared relative is the strongest
    # evidence either way, then a shared name, then everything else by QID so
    # two runs list them in the same order.
    doubles.sort(
        key=lambda d: (
            not d.shares_a_relative,
            not d.same_name,
            int(d.qid[1:]) if d.qid[1:].isdigit() else 0,
        )
    )
    return doubles


def _year(person: Person) -> str:
    birth = person.birth_year
    death = person.death.year if person.death else None
    if birth is None and death is None:
        return "no dates"
    return f"{birth if birth is not None else '?'} – {death if death is not None else '?'}"


def _kin(person: Person, tree: Tree, ids: list[str], limit: int = 4) -> str:
    named = []
    for geni_id in ids[:limit]:
        other = tree.people.get(geni_id)
        named.append(other.display_name or geni_id if other else geni_id)
    extra = f" +{len(ids) - limit}" if len(ids) > limit else ""
    return ", ".join(named) + extra if named else "—"


def render_markdown(doubles: list[Double], tree: Tree, people: int) -> str:
    lines = [
        "# Wikidata items claiming two of our people are one",
        "",
        "Generated by `genimerge.doubles` — re-run `python -m genimerge doubles`.",
        "",
        f"**{len(doubles)} items**, measured over the {people:,}-person merge "
        "against every P2600 statement on Wikidata.",
        "",
        "Our merge keys on the Geni profile ID, so it cannot see these: two IDs "
        "are two people to it. **This is not a duplicate list.** Each row is "
        "either one person with two Geni profiles, or two different people one "
        "of whose P2600 statements is wrong, and nothing here separates them.",
        "",
        "| Wikidata | shares kin | same name | our people |",
        "| --- | :-: | :-: | --- |",
    ]
    for d in doubles:
        who = "<br>".join(
            f"[{p.display_name or p.geni_id}]({profile_url(p.geni_id)}) "
            f"`{p.geni_id}` — {_year(p)}"
            for p in d.people
        )
        lines.append(
            f"| [{d.qid}]({d.url}) | {'yes' if d.shares_a_relative else ''} "
            f"| {'yes' if d.same_name else ''} | {who} |"
        )
    return "\n".join(lines) + "\n"


def render_html(doubles: list[Double], tree: Tree, people: int) -> str:
    """A page to work through one item at a time."""
    blocks = []
    for i, d in enumerate(doubles, 1):
        cards = []
        for p in d.people:
            cards.append(
                "<div class=card>"
                f'<a class=who href="{profile_url(p.geni_id)}" target=_blank>'
                f"{_html.escape(p.display_name or p.geni_id)}</a>"
                f"<code>{p.geni_id}</code>"
                f"<dl><dt>dates</dt><dd>{_html.escape(_year(p))}</dd>"
                f"<dt>sex</dt><dd>{_html.escape(p.sex or '—')}</dd>"
                f"<dt>parents</dt><dd>{_html.escape(_kin(p, tree, p.parent_ids))}</dd>"
                f"<dt>spouses</dt><dd>{_html.escape(_kin(p, tree, p.spouse_ids))}</dd>"
                f"<dt>children</dt><dd>{_html.escape(_kin(p, tree, p.child_ids))}</dd>"
                "</dl></div>"
            )
        tags = []
        if d.shares_a_relative:
            tags.append("<span class='t kin'>shares a relative</span>")
        if d.same_name:
            tags.append("<span class='t name'>same name</span>")
        if d.years_conflict:
            tags.append("<span class='t bad'>births &gt;120 years apart</span>")
        if d.absent_ids:
            tags.append(
                f"<span class=t>{len(d.absent_ids)} more ID(s) not in our tree</span>"
            )
        blocks.append(
            f"<section><h2><span class=rank>{i}</span>"
            f'<a href="{d.url}" target=_blank>{d.qid}</a> '
            f"{''.join(tags)}</h2><div class=pair>{''.join(cards)}</div></section>"
        )

    return (
        "<!doctype html><html><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>Wikidata items claiming two of our people are one</title><style>"
        ":root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--line:#ddd;--muted:#666;"
        "--link:#0b5cad;--card:#fafafa;--tag:#e7f0fb;--bad:#f6d7d7;--badfg:#7a1f1f}"
        "@media(prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e8e8e8;--line:#33383e;"
        "--muted:#9aa0a6;--link:#79b8ff;--card:#1c1f23;--tag:#23303f;--bad:#4a2323;--badfg:#f0b8b8}}"
        "body{margin:0 auto;padding:2rem 1.25rem 4rem;max-width:1000px;background:var(--bg);"
        "color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}"
        "h1{font-size:1.5rem;margin:0 0 .5rem}p{margin:.2rem 0 1rem}"
        ".note{color:var(--muted);font-size:.9rem}"
        "section{margin:0 0 1.5rem;padding:.9rem 1rem;border:1px solid var(--line);border-radius:8px}"
        "h2{font-size:1rem;margin:0 0 .7rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}"
        ".rank{display:inline-flex;align-items:center;justify-content:center;min-width:1.6rem;"
        "height:1.6rem;border-radius:50%;background:var(--tag);font-size:.8rem}"
        ".t{background:var(--tag);border-radius:4px;padding:.05rem .4rem;font-size:.75rem;font-weight:600}"
        ".t.bad{background:var(--bad);color:var(--badfg)}"
        ".pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.75rem}"
        ".card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:.7rem .8rem}"
        ".who{display:block;font-weight:700;margin-bottom:.1rem}"
        "dl{display:grid;grid-template-columns:auto 1fr;gap:.15rem .6rem;margin:.5rem 0 0;font-size:.85rem}"
        "dt{color:var(--muted)}dd{margin:0}"
        "code{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}"
        "a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}"
        "</style></head><body>"
        "<h1>Wikidata items claiming two of our people are one</h1>"
        f"<p><b>{len(doubles)} items</b>, over the {people:,}-person merge against "
        "every P2600 statement on Wikidata.</p>"
        "<p class=note><b>This is not a duplicate list.</b> Each row is either one "
        "person with two Geni profiles Geni has not merged, or two different people "
        "one of whose P2600 statements is wrong — nothing in this repo separates "
        "them, which is why it is a page to read rather than a change to apply. Our "
        "merge keys on the Geni profile ID and cannot see these at all: two IDs are "
        "two people to it. Rows that share a relative come first, since those are "
        "the fastest to settle either way.</p>" + "".join(blocks) + "</body></html>"
    )
