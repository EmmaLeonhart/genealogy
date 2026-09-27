"""The batch files come out in Emma's cohort order, labelled, with comments beside their lines.

Ruled 2026-09-27 (*"it feels very odd and chaotic"*): edits that create nothing first, flagged as
relationship pairs or single-item properties; then the random individuals; the ring, shuffled;
the names; the rest of the individuals, shuffled. `split-daily-batch.py --order`.
"""
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location("split_daily_batch",
                                               REPO / "scripts" / "split-daily-batch.py")
split = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(split)


def person(geni, label):
    return [f"# create a new item", "CREATE",
            f'#   the item just created: set the mul label to "{label}"', f'LAST\tLmul\t"{label}"',
            f'#   set the fr label to "fils de {label}"',          # its line was dropped by a gate
            "LAST\tP31\tQ5", f'LAST\tP2600\t"{geni}"', ""]


BATCH = "\n".join(
    ["# ====", "# NAME ITEMS. an old banner", "# ===="]
    + ["# Garborg -- family, 2 bearer(s)", "# create a new item", "CREATE",
       'LAST\tLmul\t"Garborg"', "LAST\tP31\tQ101352", "Q10\tP734\tLAST", ""]
    + ["#   Q1 A: P26 spouse = Q2 B", 'Q1\tP26\tQ2\tS2600\t"1"',
       '#   Q7 G: add a mul alias "G old"', 'Q7\tAmul\t"G old"',
       '#   Q7 G: set the mul label to "G"', 'Q7\tLmul\t"G"',
       'Q2\tP26\tQ1\tS2600\t"2"', ""]
    + person("100", "Random One") + person("200", "Random Two") + person("300", "Ring One")
    + person("400", "Rest One") + person("500", "Ring Two")) + "\n"


def ordered(text=BATCH):
    return split.order_file(text, first_people=2, ring_ids={"300", "500"}, seed="2026-09-27")


def test_cohorts_in_order_with_headers():
    out = ordered()
    heads = [l for l in out.splitlines() if l.startswith(split.HEADER)]
    assert [h.split(":")[0] for h in heads] == [
        "# ▶ EDITS ON ITEMS THAT ALREADY EXIST", "# ▶ (a) relationships",
        "# ▶ (b) properties of one item", "# ▶ RANDOM INDIVIDUALS", "# ▶ THE RING",
        "# ▶ NAME ITEMS", "# ▶ THE REST OF THE INDIVIDUALS"]
    pos = {k: out.index(f'"{k}"') for k in ("Random One", "Random Two", "Ring One", "Ring Two",
                                             "Garborg", "Rest One")}
    assert pos["Random One"] < pos["Random Two"] < min(pos["Ring One"], pos["Ring Two"])
    assert max(pos["Ring One"], pos["Ring Two"]) < pos["Garborg"] < pos["Rest One"]


def test_a_relationship_pair_goes_together_and_amul_stays_above_lmul():
    lines = ordered().splitlines()
    i = lines.index('Q1\tP26\tQ2\tS2600\t"1"')
    assert lines[i + 1:i + 2] in (['#   Q2 B: P26 spouse = Q1 A'], ['Q2\tP26\tQ1\tS2600\t"2"'])
    assert 'Q2\tP26\tQ1\tS2600\t"2"' in lines[i + 1:i + 3]
    assert lines.index('Q7\tAmul\t"G old"') < lines.index('Q7\tLmul\t"G"')


def test_every_comment_describes_a_line_that_is_there():
    out = ordered()
    assert "fils de" not in out                       # the dropped label's comment went with it
    assert "NAME ITEMS. an old banner" not in out     # the old banner is replaced by the headers
    lines = out.splitlines()
    for a, b in zip(lines, lines[1:] + [""]):
        if a == "# create a new item":
            assert b == "CREATE"
    i = lines.index("# Garborg -- family, 2 bearer(s)")
    assert lines[i + 1:i + 3] == ["# create a new item", "CREATE"]


def test_commands_are_only_moved_and_the_pass_is_idempotent():
    out = ordered()
    cmds = lambda t: sorted(l for l in t.splitlines() if l.strip() and not l.startswith("#"))
    assert cmds(out) == cmds(BATCH)
    assert ordered(out) == out
