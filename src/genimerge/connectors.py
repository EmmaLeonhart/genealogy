"""The people missing from the middle of our relationship paths.

A *connector* is a person Geni names on a relationship path that no export has
reached. `genimerge.paths` already reports these one path at a time; this module
reads every path at once and asks the question that only makes sense across
them: **which missing people block more than one path?**

That question turned out to matter. Measured over 26 paths on 2026-08-06, 265
absent step-slots sat on 196 distinct people, but 29 of those people carried 98
of the slots — two clusters, the Alemannian ten and the Jurhumid/Qahtani
nineteen, accounting for about 37% of every gap in the corpus. Ranking a gap by
its length gets that backwards: a 52-person run private to one path is worth
less than a 10-person run five paths cross.

**A bridge is a run of consecutive absent steps**, bounded by the last held
person before it (the *doorway* — the profile to seed an export on or near) and
the first held person after it (the *resume*). Bridges from different paths are
merged into one `Cluster` when they share any person at all, by union-find. That
is deliberately looser than requiring identical member sets: `psamtik-ii`
overlaps the Jurhumid nineteen partially rather than exactly, and treating that
as a separate problem would double-count the export that closes both.

**The style hint is not decoration.** `CLAUDE.md` records that reading the
relation column before choosing an export style is what closed the Jimmu gap:
two of its six bridging steps are reachable only through a marriage, so
`Ancestors` and `BloodTree` would have walked straight past them. Any cluster
whose relations include a spouse or sibling link is flagged `Forest` here for
the same reason.

Nothing in this module reaches the network or writes to Wikidata. It reads the
merged tree and the path files, both of which are already on disk.
"""

from __future__ import annotations

import html as _html
from dataclasses import dataclass, field
from pathlib import Path

from . import paths as paths_mod
from .model import Tree

__all__ = [
    "Bridge",
    "Cluster",
    "bridges",
    "cluster",
    "collect",
    "render_html",
    "render_markdown",
]

#: Relation wordings that only a spouse-following export style will cross.
#: Geni writes the relation of a row to the row before it, in its own words.
_MARRIAGE_WORDS = ("wife", "husband", "partner", "spouse")
_SIBLING_WORDS = ("brother", "sister", "sibling")

_GENI_URL = "https://www.geni.com/people/x/{}"


@dataclass
class Bridge:
    """One run of consecutive absent steps within a single path."""

    path: str
    #: the last held person before the run — where an export would be seeded
    doorway: paths_mod.StepResult | None
    #: the first held person after the run; ``None`` means the path ends in the
    #: gap, which is a frontier rather than a bridge
    resume: paths_mod.StepResult | None
    members: list[paths_mod.StepResult] = field(default_factory=list)

    @property
    def first_step(self) -> int:
        return self.members[0].step.step

    @property
    def last_step(self) -> int:
        return self.members[-1].step.step

    @property
    def ids(self) -> set[str]:
        return {r.step.geni_id for r in self.members if r.step.geni_id}


@dataclass
class Cluster:
    """Bridges from one or more paths that share at least one missing person."""

    bridges: list[Bridge] = field(default_factory=list)

    @property
    def slots(self) -> int:
        """Absent step-slots closed — the payoff, counting a shared person once
        per path that needs them."""
        return sum(len(b.members) for b in self.bridges)

    @property
    def people(self) -> list[paths_mod.StepResult]:
        """Distinct missing people, in the order they are first walked."""
        seen: set[str] = set()
        out: list[paths_mod.StepResult] = []
        for bridge in self.bridges:
            for result in bridge.members:
                key = result.step.geni_id or f"name:{result.step.name}"
                if key in seen:
                    continue
                seen.add(key)
                out.append(result)
        return out

    @property
    def path_names(self) -> list[str]:
        return sorted({b.path for b in self.bridges})

    @property
    def doorways(self) -> list[paths_mod.StepResult]:
        """Distinct doorways, one per bridge where the path has one."""
        seen: set[str] = set()
        out: list[paths_mod.StepResult] = []
        for bridge in self.bridges:
            door = bridge.doorway
            if door is None:
                continue
            key = door.step.geni_id or f"name:{door.step.name}"
            if key in seen:
                continue
            seen.add(key)
            out.append(door)
        return out

    @property
    def relations(self) -> list[str]:
        return [r.step.relation for r in self.people if r.step.relation]

    @property
    def style(self) -> str:
        """The export style the relation column calls for.

        `Forest` whenever a spouse or sibling link has to be crossed, because a
        blood-only walk cannot reach the people on the far side of one.
        """
        joined = " ".join(self.relations).casefold()
        if any(word in joined for word in _MARRIAGE_WORDS):
            return "Forest"
        if any(word in joined for word in _SIBLING_WORDS):
            return "Forest"
        return "Ancestors or Forest"

    @property
    def style_reason(self) -> str:
        joined = " ".join(self.relations).casefold()
        hits = [w for w in _MARRIAGE_WORDS + _SIBLING_WORDS if w in joined]
        if not hits:
            return "no spouse or sibling link to cross; a blood-only style reaches all of these"
        return "crosses a " + "/".join(sorted(set(hits))) + " link, which a blood-only style walks past"

    @property
    def ends_a_path(self) -> bool:
        """True when some path simply runs out here rather than resuming."""
        return any(b.resume is None for b in self.bridges)


def bridges(report: paths_mod.PathReport, path_name: str) -> list[Bridge]:
    """Split one checked path into its runs of absent steps."""
    out: list[Bridge] = []
    results = report.results
    run: list[paths_mod.StepResult] = []
    doorway: paths_mod.StepResult | None = None
    last_held: paths_mod.StepResult | None = None

    for result in results:
        if result.held:
            if run:
                out.append(Bridge(path_name, doorway, result, run))
                run = []
            last_held = result
            continue
        if not run:
            doorway = last_held
        run.append(result)
    if run:
        # No resume: the path ends inside the gap. That is a frontier, and the
        # distinction is load-bearing — an export at a frontier walks outward
        # into unknown territory, where one at a bridge has a named far side.
        out.append(Bridge(path_name, doorway, None, run))
    return out


def cluster(all_bridges: list[Bridge]) -> list[Cluster]:
    """Union-find over shared missing people, biggest payoff first.

    Two bridges join when they share a single profile ID. Sharing one person is
    strong evidence of sharing the export that would supply them, which is the
    thing being ranked.
    """
    parent: dict[int, int] = {i: i for i in range(len(all_bridges))}

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    owner: dict[str, int] = {}
    for i, bridge in enumerate(all_bridges):
        for geni_id in bridge.ids:
            if geni_id in owner:
                union(owner[geni_id], i)
            else:
                owner[geni_id] = i

    grouped: dict[int, Cluster] = {}
    for i, bridge in enumerate(all_bridges):
        grouped.setdefault(find(i), Cluster()).bridges.append(bridge)

    clusters = list(grouped.values())
    # Payoff first; then distinct people, so a cluster spanning more of the
    # graph outranks a shorter one with the same slot count. The path name is
    # the final tie-break so two runs settle the same way every time.
    clusters.sort(key=lambda c: (-c.slots, -len(c.people), c.path_names[0]))
    return clusters


def collect(
    tree: Tree, path_files: list[Path]
) -> tuple[list[Cluster], dict[str, paths_mod.PathReport]]:
    """Check every path file against one loaded tree.

    Returns the clusters and the per-path reports, so a caller that wants to
    refresh `reports/path-*.md` as well does not pay for a second tree load —
    which over a 200,000-person merge is the whole cost of the run.
    """
    reports: dict[str, paths_mod.PathReport] = {}
    found: list[Bridge] = []
    for file in sorted(path_files):
        name = file.stem
        report = paths_mod.check(tree, paths_mod.load_path(file))
        reports[name] = report
        found.extend(bridges(report, name))
    return cluster(found), reports


def _totals(reports: dict[str, paths_mod.PathReport]) -> tuple[int, int, int]:
    steps = sum(len(r.results) for r in reports.values())
    held = sum(len(r.held) for r in reports.values())
    complete = sum(1 for r in reports.values() if not r.absent)
    return steps, held, complete


_LEDE = (
    "Every person Geni names on one of our relationship paths that no export "
    "has reached. These are the connectors — the missing middles. Each block "
    "is one bridge: seed an export on the doorway, and the people under it are "
    "what it should bring back."
)


def render_markdown(
    clusters: list[Cluster], reports: dict[str, paths_mod.PathReport], tree_size: int
) -> str:
    steps, held, complete = _totals(reports)
    pct = f"{held / steps:.1%}" if steps else "—"
    lines = [
        "# The connectors we lack",
        "",
        "Generated by `genimerge.connectors` — re-run `python -m genimerge connectors`.",
        "",
        f"Measured against a {tree_size:,}-person merge, over {len(reports)} paths.",
        "",
        "| | |",
        "| --- | ---: |",
        f"| paths | {len(reports)} |",
        f"| steps | {steps:,} |",
        f"| held | **{held:,} ({pct})** |",
        f"| absent step-slots | {steps - held:,} |",
        f"| distinct missing people | {len({p.step.geni_id or p.step.name for c in clusters for p in c.people}):,} |",
        f"| paths held end to end | **{complete} of {len(reports)}** |",
        f"| bridges | {sum(len(c.bridges) for c in clusters)} in {len(clusters)} clusters |",
        "",
        "## Ranked by what one export would buy",
        "",
        "A cluster is a set of bridges sharing at least one missing person, so",
        "the slot count is the payoff across every path it blocks — not the",
        "length of any one gap.",
        "",
        "| rank | slots | people | paths | doorway | style |",
        "| ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for i, c in enumerate(clusters, 1):
        door = c.doorways[0] if c.doorways else None
        door_text = (
            f"{door.step.name} `{door.step.geni_id}`" if door else "*(path starts absent)*"
        )
        lines.append(
            f"| {i} | {c.slots} | {len(c.people)} | {len(c.path_names)} "
            f"| {door_text} | {c.style} |"
        )
    lines += ["", "## Every cluster, with its missing people", ""]
    for i, c in enumerate(clusters, 1):
        lines.append(f"### {i}. {len(c.people)} people, {c.slots} slots, {len(c.path_names)} path(s)")
        lines.append("")
        for door in c.doorways:
            lines.append(
                f"- **doorway** [{door.step.name}]({_GENI_URL.format(door.step.geni_id)}) "
                f"`{door.step.geni_id}`"
            )
        lines.append(f"- **style** `{c.style}` — {c.style_reason}")
        lines.append(f"- **paths** {', '.join('`' + n + '`' for n in c.path_names)}")
        if c.ends_a_path:
            lines.append("- **frontier** — at least one path ends here rather than resuming")
        lines.append("")
        lines.append("| step | who | relation to the previous person |")
        lines.append("| ---: | --- | --- |")
        for person in c.people:
            step = person.step
            link = (
                f"[{step.name}]({_GENI_URL.format(step.geni_id)})"
                if step.geni_id
                else step.name
            )
            lines.append(f"| {step.step} | {link} `{step.geni_id}` | {step.relation} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_html(
    clusters: list[Cluster], reports: dict[str, paths_mod.PathReport], tree_size: int
) -> str:
    """A page to work through, one bridge at a time."""
    steps, held, complete = _totals(reports)
    pct = f"{held / steps:.1%}" if steps else "—"
    missing = len({p.step.geni_id or p.step.name for c in clusters for p in c.people})

    blocks = []
    for i, c in enumerate(clusters, 1):
        doors = "".join(
            f'<a class=door href="{_GENI_URL.format(d.step.geni_id)}" target="_blank">'
            f"{_html.escape(d.step.name)}</a><code>{d.step.geni_id}</code>"
            for d in c.doorways
        ) or "<span class=muted>path starts absent</span>"
        rows = "\n".join(
            f"<tr><td class=num>{p.step.step}</td>"
            + (
                f'<td><a href="{_GENI_URL.format(p.step.geni_id)}" target="_blank">'
                f"{_html.escape(p.step.name)}</a><br><code>{p.step.geni_id}</code></td>"
                if p.step.geni_id
                else f"<td>{_html.escape(p.step.name)}<br><code class=muted>no id</code></td>"
            )
            + f"<td class=rel>{_html.escape(p.step.relation)}</td></tr>"
            for p in c.people
        )
        frontier = (
            "<span class=tag-f>ends a path</span>" if c.ends_a_path else ""
        )
        blocks.append(
            f"<section><h2><span class=rank>{i}</span> {len(c.people)} people "
            f"&middot; {c.slots} slots &middot; {len(c.path_names)} path"
            f"{'s' if len(c.path_names) != 1 else ''} {frontier}</h2>"
            f"<p class=meta><b>Seed an export on:</b> {doors}</p>"
            f"<p class=meta><b>Style:</b> <span class=tag>{_html.escape(c.style)}</span> "
            f"<span class=muted>{_html.escape(c.style_reason)}</span></p>"
            f"<p class=meta><b>Blocks:</b> "
            + " ".join(f"<span class=path>{_html.escape(n)}</span>" for n in c.path_names)
            + "</p>"
            "<table><thead><tr><th>step</th><th>who we lack</th>"
            "<th>relation to the previous person</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></section>"
        )

    return (
        "<!doctype html><html><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>The connectors we lack</title><style>"
        ":root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--line:#d8d8d8;"
        "--muted:#666;--link:#0b5cad;--card:#fafafa;--tag:#e7f0fb}"
        "@media(prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e8e8e8;"
        "--line:#33383e;--muted:#9aa0a6;--link:#79b8ff;--card:#1c1f23;--tag:#23303f}}"
        "body{margin:0 auto;padding:2rem 1.25rem 4rem;max-width:1000px;background:var(--bg);"
        "color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}"
        "h1{font-size:1.6rem;margin:0 0 .5rem}p{margin:.2rem 0 1rem}"
        ".note{color:var(--muted);font-size:.9rem}"
        ".stats{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;margin:1rem 0 2rem;"
        "padding:.9rem 1.1rem;background:var(--card);border:1px solid var(--line);border-radius:8px}"
        ".stats div{font-size:.85rem;color:var(--muted)}"
        ".stats b{display:block;font-size:1.25rem;color:var(--fg);font-variant-numeric:tabular-nums}"
        "section{margin:0 0 2.5rem;padding:1rem 1.1rem;background:var(--card);"
        "border:1px solid var(--line);border-radius:8px}"
        "h2{font-size:1.05rem;margin:0 0 .6rem;display:flex;align-items:center;gap:.5rem}"
        ".rank{display:inline-flex;align-items:center;justify-content:center;min-width:1.7rem;"
        "height:1.7rem;border-radius:50%;background:var(--tag);font-size:.85rem}"
        ".meta{font-size:.9rem;margin:.25rem 0}"
        ".door{font-weight:600;margin-right:.35rem}"
        ".tag,.path,.tag-f{display:inline-block;background:var(--tag);border-radius:4px;"
        "padding:.05rem .4rem;font-size:.82rem;margin-right:.25rem}"
        ".tag-f{background:#f6d7d7;color:#7a1f1f}"
        "@media(prefers-color-scheme:dark){.tag-f{background:#4a2323;color:#f0b8b8}}"
        ".muted{color:var(--muted)}"
        "table{border-collapse:collapse;width:100%;font-size:.94rem;margin-top:.6rem}"
        "th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid var(--line);"
        "vertical-align:top}"
        "th{font-size:.75rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}"
        "td.num{text-align:right;font-variant-numeric:tabular-nums;color:var(--muted)}"
        "td.rel{color:var(--muted)}"
        "code{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}"
        "a{color:var(--link);text-decoration:none;font-weight:600}a:hover{text-decoration:underline}"
        "</style></head><body>"
        "<h1>The connectors we lack</h1>"
        f"<p>{_LEDE}</p>"
        "<div class=stats>"
        f"<div><b>{missing:,}</b>people missing</div>"
        f"<div><b>{steps - held:,}</b>step-slots blocked</div>"
        f"<div><b>{len(clusters)}</b>bridges to close</div>"
        f"<div><b>{pct}</b>of steps held</div>"
        f"<div><b>{complete}/{len(reports)}</b>paths complete</div>"
        "</div>"
        f"<p class=note>Measured against a {tree_size:,}-person merge over "
        f"{len(reports)} relationship paths. Ranked by slots — a person who "
        "blocks five paths counts five times, because that is what one export "
        "would buy. Presence here measures our own sampling, never Geni's "
        "content: every one of these people is somebody Geni already names.</p>"
        + "".join(blocks)
        + "</body></html>"
    )
