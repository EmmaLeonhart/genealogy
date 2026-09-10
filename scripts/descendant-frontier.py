"""Rank the people in a `Descendants` export by how much of the descent below them is THEIRS ALONE.

Your algorithm, 2026-09-09, in your own words:

    "For descendants of an individual, my thought is to do a kind of Monte Carlo-ish thing. I
    think, in order to make this less probabilistically have fewer issues, you look at the
    individuals in their descendants graph based on how many descendants they have within the
    graph. You aim for people who clearly have a large amount of descendants who are as disjoint
    from other descendants in the graph as possible. Since the descendants graph does actually
    reconnect, we're trying to find more disjoint people, or more disjoint descendants."

**THE POINT IS THE CAP.** A `Descendants` export comes back at `GENI_EXPORT_CAP` whenever there
is more below the seed than one export can hold -- Abul Hamza's came back at exactly 5,000 -- so
the file is a *ball*, not a lineage, and everything past its rim is invisible. The way to see
past the rim is to export again from further down. Which people to pick is what this ranks.

⛔ **THE DISJOINTNESS IS AT THE RIM, AND THERE IS NONE IN THE INTERIOR. MEASURED, NOT ARGUED.**
Two readings were built before the right one and both are in this file, because the refutations
are the finding:

    greedy   set-cover over descendant sets      1 pick, 4,998 of 5,000 -- a ball we already hold
    split    an antichain past the chokepoints   12 picks, exclusive 624 / 23 / 14 / 2 / 0 x8
    rim      one per cut-off family cluster      10 picks, 621 clusters to choose from

A descent is NESTED, so set-cover always answers "the top one, and nine that add nothing".
Splitting past the chokepoints fixes the nesting and then hits the real obstacle: Abul Hamza's
interior is Cilician Armenian nobility marrying each other for two centuries, so Smbat I (3,844
descendants) and Oshin (3,234) overlap almost totally and exporting from both buys one ball.

The rim is different in kind. The 1,959 people the cap cut off are no longer Armenian --
Provençal, Nuevo León, Georgian, Abkhazian, Venetian, Maltese, Albanian, Canarian -- and a Garza
and a Bagrationi share nothing below them. So the pick is one per largest family cluster at the
rim, which is disjoint BY CONSTRUCTION rather than by sampling luck. Your rule, 2026-09-09.

**AND THE RIM SELF-SELECTS FOR THE THING THE CAMPAIGN WANTS.** All ten picks are born 1595-1700,
which is the band `CLAUDE.md` § *A `Descendants` export reaches about twelve generations forward*
says a seed must be in to deliver people born after 1900. Nothing selected for that; it is where
twenty-five generations from a medieval seed lands.

**DISTINCT PEOPLE HERE, NOT DESCENT PATHS.** `CLAUDE.md` is explicit that the corpus-wide report
counts descent PATHS, on your ruling -- "somebody reachable down two lines counts twice" --
because the question there is how many lines come down from a person. The question HERE is how
many people an export would cover, and an export returns a person once however many lines reach
them. Two different questions, and this is the one where de-duplicating is the point: the whole
subject is the overlap.

Exact bitsets are affordable at this size and are not corpus-wide. 5,000 people is 625 bytes of
bitmask each, 3 MB in all -- the tens-of-gigabytes objection `CLAUDE.md` records against
`frontier`'s bitmask applies at 257,219 people and not at one export.

A cycle contributes the EMPTY SET rather than nothing, which truncates the measure instead of
falsifying it -- the same choice `_post_order` makes in `genimerge.descendants` and for the same
reason.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge.gedcom import parse_file
from genimerge.identity import geni_id_of

NL = chr(10)
TAB = chr(9)


def _gid(rec):
    try:
        found = geni_id_of(rec)
    except Exception:
        found = None
    if found:
        return found
    return (rec.xref or "").strip("@").lstrip("I")


def _name(rec):
    for node in rec.children:
        if node.tag == "NAME" and node.value:
            return node.value.replace("/", "").strip()
    return ""


def _year(rec):
    for node in rec.children:
        if node.tag == "BIRT":
            for sub in node.children:
                if sub.tag == "DATE" and sub.value:
                    return sub.value.strip()
    return ""


def load(paths):
    """parent -> children over every file given, keyed on the Geni id."""
    children = {}
    names = {}
    born = {}
    for path in paths:
        doc = parse_file(path)
        by_xref = doc.by_xref()
        for rec in doc.by_tag("INDI"):
            gid = _gid(rec)
            if not gid:
                continue
            names.setdefault(gid, _name(rec))
            born.setdefault(gid, _year(rec))
            children.setdefault(gid, set())
        for fam in doc.by_tag("FAM"):
            parents, kids = [], []
            for node in fam.children:
                if node.tag in ("HUSB", "WIFE") and node.value:
                    ref = by_xref.get(node.value.strip())
                    if ref is not None and _gid(ref):
                        parents.append(_gid(ref))
                elif node.tag == "CHIL" and node.value:
                    ref = by_xref.get(node.value.strip())
                    if ref is not None and _gid(ref):
                        kids.append(_gid(ref))
            for p in parents:
                children.setdefault(p, set()).update(kids)
            for k in kids:
                children.setdefault(k, set())
    return children, names, born


def descendant_sets(children):
    """Exact distinct-descendant bitmask per person, iterative post-order, cycle-safe."""
    index = {gid: i for i, gid in enumerate(sorted(children))}
    desc = {}
    for root in index:
        if root in desc:
            continue
        stack = [(root, False)]
        onstack = set()
        while stack:
            node, expanded = stack.pop()
            if expanded:
                onstack.discard(node)
                mask = 0
                for kid in children.get(node, ()):
                    if kid in desc:
                        mask |= desc[kid] | (1 << index[kid])
                    # a kid still being expanded is an ancestry cycle: contribute the
                    # EMPTY set, which truncates the measure rather than falsifying it
                desc[node] = mask
                continue
            if node in desc or node in onstack:
                continue
            onstack.add(node)
            stack.append((node, True))
            for kid in children.get(node, ()):
                if kid not in desc:
                    stack.append((kid, False))
    return desc, index


def greedy(desc, exclude, top):
    """Pick `top` people maximising what each ADDS to the union of everything picked before.

    ⛔ MEASURED AND REFUTED ON THE FIRST BALL IT WAS RUN AGAINST -- kept because the refutation
    is the finding. Abul Hamza's 5,000-person descent hangs off ONE person, Michke Ardzouni, who
    holds 4,998 of them; so rank 1 takes the whole graph, every other candidate has a marginal
    contribution of exactly zero, and the run stops at one pick. That pick is a ball we already
    have.

    Set-cover greedy answers "which ten sets cover the most", and the honest answer over a
    descent is always "the top one, and nine that add nothing", because a descent is NESTED. The
    question you asked is which ten to EXPORT FROM, and two picks where one is the other's
    ancestor buy one export's worth of people. `split_frontier` is that question.
    """
    covered = 0
    picked = []
    live = {g: m for g, m in desc.items() if g not in exclude and m}
    for _ in range(top):
        best, best_gain, best_mask = None, 0, 0
        for gid, mask in live.items():
            gain = (mask & ~covered).bit_count()
            if gain > best_gain:
                best, best_gain, best_mask = gid, gain, mask
        if best is None:
            break
        covered |= best_mask
        picked.append((best, desc[best].bit_count(), best_gain, covered.bit_count()))
        del live[best]
    return picked


def split_frontier(children, desc, seed, top):
    """Cut the descent into `top` pieces by walking PAST every chokepoint.

    Start at the seed and repeatedly replace the largest member of the frontier with its own
    children. The frontier stays an ANTICHAIN -- nobody on it is anybody else's descendant, which
    is the property `greedy` cannot hold and the one that makes ten picks worth ten exports.

    Splitting the largest is what walks past a chokepoint without needing to detect one: Michke
    Ardzouni holds 4,998 of 5,000, so she is split first, and her children after her, until the
    descent genuinely forks. A rope of single children costs one iteration per link and stops
    being the largest the moment it fans.

    The frontier can OVERLAP even though it is an antichain, because the descent reconnects --
    two people on it can share a grandchild through a marriage further down. That overlap is
    reported per member as `exclusive` rather than being designed away: it is the quantity your
    "as disjoint from other descendants in the graph as possible" is about, and a member whose
    descendants are wholly somebody else's is visible as `exclusive` 0.
    """
    frontier = {seed} if seed in children else set(children)
    # a childless seed cannot be split; fall back to everyone with no parent in the file
    while len(frontier) < top:
        biggest = max(frontier, key=lambda g: desc.get(g, 0).bit_count())
        kids = {k for k in children.get(biggest, ()) if k not in frontier}
        if not kids:
            break
        frontier.discard(biggest)
        frontier |= kids
        if len(frontier) == 0:
            break
    rows = []
    for gid in frontier:
        mine = desc.get(gid, 0) | (1 << 0) * 0
        others = 0
        for other in frontier:
            if other != gid:
                others |= desc.get(other, 0)
        rows.append((gid, desc.get(gid, 0).bit_count(), (desc.get(gid, 0) & ~others).bit_count()))
    rows.sort(key=lambda r: (-r[2], -r[1]))
    union = 0
    for gid in frontier:
        union |= desc.get(gid, 0)
    return rows, union.bit_count()


def rim_of(children, seed):
    """The people the CAP cut off: leaves in the deepest two rings of the breadth-first walk.

    ⛔ A LEAF IS TWO DIFFERENT THINGS AND DEPTH IS WHAT SEPARATES THEM. A `Descendants` export
    walks breadth-first, so it fills whole generations and stops mid-ring when it hits
    `GENI_EXPORT_CAP`. A leaf in a SHALLOW ring is a person Geni records no children for; a leaf
    in the DEEPEST ring is a person whose children exist and did not fit. Only the second is
    worth an export, and treating all 3,185 leaves alike would put 1,226 genuinely childless
    people into the pool.

    Measured on Abul Hamza: depth 25 holds 871 people and **871 of them are leaves, 100%**,
    which is what a cut ring looks like from inside the file. Depth 24 is 1,088 of 1,440, and
    every ring above it runs about half. So the cut is at 24-25 and the rim is 1,959 people.
    """
    depth = {seed: 0}
    queue = [seed]
    while queue:
        node = queue.pop(0)
        for kid in children.get(node, ()):
            if kid not in depth:
                depth[kid] = depth[node] + 1
                queue.append(kid)
    if not depth:
        return [], {}
    deepest = max(depth.values())
    rim = [g for g in children if not children.get(g) and depth.get(g, -1) >= deepest - 1]
    return rim, depth


def cluster_key(name):
    """The trailing token of the rendered name -- the house or family word Geni files them under.

    Deliberately crude, and it does not have to be better. It is not deciding anything about a
    person; it is spreading ten picks across the rim so they do not all land in one family. A
    wrong cluster costs one redundant export and is visible the moment the ball comes back.

    ⛔ CASE **AND DIACRITICS** BOTH FOLD HERE, AND THAT IS THE OPPOSITE OF THE WIKIDATA RULE.
    `CLAUDE.md` § *A diacritic makes a different name* forbids folding them, because `María`,
    `Mária` and `Marià` are three languages' names with three Wikidata items and folding
    manufactured ambiguity for 1,312 of them. **That rule is about IDENTIFYING a name. This is
    about SPREADING TEN PICKS**, and nothing here is identified, linked or created -- a cluster
    is a bucket that stops all ten landing in one family.

    Case alone was not enough and the rim says so: `Glandevès` 39 and `GLANDEVES` 15 are one
    Provençal house filed both ways, and they casefold APART because of the `è`. Left alone that
    is one family holding two buckets and, at a slightly different cut, two of the ten picks.

    A wrong cluster costs one redundant export and is visible the moment the ball comes back.
    """
    tokens = (name or "").split()
    if not tokens:
        return ""
    folded = unicodedata.normalize("NFKD", tokens[-1].casefold())
    return "".join(c for c in folded if not unicodedata.combining(c))


def random_picks(children, names, born, seed, top, rng_seed=0):
    """⛔ THE PICK RULE: RANDOM PEOPLE, then the CENSUS NUMBER decides. Ruled 2026-09-09.

    *"stop with the large family clusters. Just randomly pick people in the graph and find out if
    anybody has listed 5,000 descendants, and then you perform the operation on them."*

    This supersedes `rim_picks`, which sorted the rim by family cluster and therefore **could
    never select a single person** -- and every royal doorway in Abul Hamza's ball is a single
    person: Henriette Marie de Bourbon, James VII Stewart, Isabel Clara Eugenia Habsburg, Jan
    Kasimir Vasa, all sitting at the rim, none selectable by a rule that ranks families.

    **The decision is not made here.** This emits candidates to LOOK UP; the Geni profile's
    `descendants` statistic decides, and a **saturated** count (5,000 / 15,000) is the signal --
    it means Geni knows there is more below that person than one export can hold, which is
    exactly who is worth exporting from. A rule that picked on anything visible *inside* the ball
    would be guessing at the thing the census already states.

    Deterministic for a given `rng_seed`, per *SORTING MUST BE DETERMINISTIC*: the same ball and
    the same seed give the same candidates, so a run is reproducible and a re-run is not a
    different campaign.
    """
    import random
    pool = sorted(g for g in children if g != seed)
    rng = random.Random(rng_seed)
    return rng.sample(pool, min(top, len(pool)))


def rim_picks(children, names, born, desc, seed, top):
    """One representative per largest rim family cluster -- your rule, 2026-09-09.

    "One per largest family cluster": the biggest name-clusters at the rim are unrelated
    populations -- Provençal (Glandevès, Castellane, Forbin), Nuevo León (Garza, Flores, Abrego),
    Georgian and Abkhazian (Bagrationi, Амилахвари, Шервашидзе), Venetian (Pisani, Corner),
    Maltese (Saliba, Tabone) -- so one pick each is disjoint BY CONSTRUCTION rather than by
    sampling luck. That is what the interior antichain could not deliver: Smbat and Oshin are
    both Armenian and share ~100% of their descent.

    Within a cluster the representative is the member with a recorded birth year first, then the
    lowest id, so the pick is deterministic. A census read decides nothing here -- your ruling
    was that capping out is desirable and "if they don't, that's fine".
    """
    rim, depth = rim_of(children, seed)
    clusters = {}
    for gid in rim:
        clusters.setdefault(cluster_key(names.get(gid, "")), []).append(gid)
    ordered = sorted(clusters.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    picks = []
    for key, members in ordered:
        if not key or len(picks) >= top:
            continue
        member = sorted(members, key=lambda g: (born.get(g, "") == "", g))[0]
        picks.append((member, key, len(members), depth.get(member, -1)))
    return picks, len(rim), len(clusters)


def main() -> int:
    ap = argparse.ArgumentParser(description="rank a Descendants export by disjoint descent")
    ap.add_argument("gedcom", nargs="+", help="the Descendants export(s) to rank inside")
    ap.add_argument("--seed", default="", help="the export seed, excluded from the ranking")
    ap.add_argument("--top", type=int, default=10, help="how many to pick (your 'top 10')")
    ap.add_argument("--mode", choices=("random", "rim", "split", "greedy"), default="random",
                    help="random: RANDOM people to look up, and the Geni census number decides "
                         "-- the ruled pick rule. rim: one per cut-off family cluster, SUPERSEDED "
                         "(cannot select a single person). split/greedy: refuted, kept as record.")
    ap.add_argument("--rng-seed", type=int, default=0,
                    help="deterministic sampling: same ball + same seed = same candidates")
    ap.add_argument("-o", "--out", default="", help="TSV to write")
    args = ap.parse_args()

    children, names, born = load(args.gedcom)
    desc, index = descendant_sets(children)
    total = len(index)
    sys.stdout.reconfigure(encoding="utf-8")

    if args.mode == "random":
        picks = random_picks(children, names, born, args.seed, args.top, args.rng_seed)
        rim, _ = rim_of(children, args.seed)
        rimset = set(rim)
        header = TAB.join(["n", "geni_id", "name", "born",
                           "in_graph_descendants", "at_rim", "profile"])
        lines = [header]
        for n, gid in enumerate(picks, 1):
            lines.append(TAB.join([
                str(n), gid, names.get(gid, ""), born.get(gid, ""),
                str(desc.get(gid, 0).bit_count()), "yes" if gid in rimset else "",
                "https://www.geni.com/people/x/%s" % gid,
            ]))
        text = NL.join(lines) + NL
        if args.out:
            pathlib.Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        print("%d people in the ball; %d RANDOM candidates to look up. The Geni `descendants` "
              "statistic decides -- export from the SATURATED ones (5,000 / 15,000)."
              % (total, len(picks)))
        return 0

    if args.mode == "rim":
        picks, rim_n, cluster_n = rim_picks(children, names, born, desc, args.seed, args.top)
        header = ("rank\tgeni_id\tname\tborn\tcluster\tcluster_size\tdepth\tseed_url")
        lines = [header]
        for rank, (gid, key, size, d) in enumerate(picks, 1):
            lines.append("\t".join([
                str(rank), gid, names.get(gid, ""), born.get(gid, ""),
                key, str(size), str(d),
                "https://www.geni.com/family-tree/index/%s" % gid,
            ]))
        text = "\n".join(lines) + "\n"
        if args.out:
            pathlib.Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        print("%d people in the ball; %d cut off at the rim across %d family clusters; "
              "%d picks, one per cluster" % (total, rim_n, cluster_n, len(picks)))
        return 0

    if args.mode == "greedy":
        picked = greedy(desc, {args.seed} if args.seed else set(), args.top)
        header = ("rank\tgeni_id\tname\tborn\tdescendants_in_graph\tmarginal_new"
                  "\tcumulative\tcumulative_pct\tchildren")
        lines = [header]
        for rank, (gid, own, gain, cum) in enumerate(picked, 1):
            lines.append("\t".join([
                str(rank), gid, names.get(gid, ""), born.get(gid, ""),
                str(own), str(gain), str(cum), "%.1f%%" % (100.0 * cum / total),
                str(len(children.get(gid, ()))),
            ]))
        reach = picked[-1][3] if picked else 0
    else:
        rows, reach = split_frontier(children, desc, args.seed, args.top)
        header = ("rank\tgeni_id\tname\tborn\tdescendants_in_graph\texclusive"
                  "\texclusive_pct\tchildren")
        lines = [header]
        for rank, (gid, own, excl) in enumerate(rows, 1):
            lines.append("\t".join([
                str(rank), gid, names.get(gid, ""), born.get(gid, ""),
                str(own), str(excl),
                "%.0f%%" % (100.0 * excl / own) if own else "-",
                str(len(children.get(gid, ()))),
            ]))

    text = "\n".join(lines) + "\n"
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print("%d people in the graph; the %d picks cover %d of them (%.1f%%)"
          % (total, len(lines) - 1, reach, 100.0 * reach / total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
