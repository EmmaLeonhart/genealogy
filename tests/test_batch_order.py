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
    # Ruled 2026-09-27 (evening): the ring first, then the names, then the other people one at a
    # time, each followed by a slice of the edits on existing items.
    out = ordered()
    heads = [l for l in out.splitlines() if l.startswith(split.HEADER)]
    assert [h.split(":")[0] for h in heads] == [
        "# ▶ THE RING", "# ▶ NAME ITEMS", "# ▶ THE OTHER INDIVIDUALS, ONE AT A TIME"]
    pos = {k: out.index(f'"{k}"') for k in ("Random One", "Random Two", "Ring One", "Ring Two",
                                             "Garborg", "Rest One")}
    assert max(pos["Ring One"], pos["Ring Two"]) < pos["Garborg"]
    assert pos["Garborg"] < min(pos["Random One"], pos["Random Two"], pos["Rest One"])


def test_existing_item_edits_are_spread_between_the_people():
    lines = ordered().splitlines()
    creates = [i for i, l in enumerate(lines) if l == "CREATE"]
    edits = [i for i, l in enumerate(lines) if l.startswith("Q") and "\t" in l and "LAST" not in l]
    last_ring_or_name = creates[2]             # two ring people, then the one name item
    between = [sum(1 for e in edits if a < e < b) for a, b in zip(creates[3:], creates[4:])]
    assert all(e > last_ring_or_name for e in edits)
    assert between and all(n >= 1 for n in between)


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


def test_a_batch_keeps_120_non_ring_people_or_enough_to_reach_180():
    # Ruled 2026-09-27 (Emma): max(120, 180 - ring) non-ring people; the rest wait for a later run.
    many = "\n".join(sum((person(str(1000 + k), f"Other {k}") for k in range(200)), [])
                     + person("300", "Ring One") + person("500", "Ring Two")) + "\n"
    out = split.order_file(many, first_people=2, ring_ids={"300", "500"}, seed="2026-09-27")
    others = sum(1 for k in range(200) if f'"Other {k}"' in out)
    assert others == 178                         # 180 - 2 ring people, above the floor of 120
    assert '"Ring One"' in out and '"Ring Two"' in out
    assert split.order_file(out, first_people=2, ring_ids={"300", "500"}, seed="2026-09-27") == out


def test_ten_familysearch_people_lead_the_batch():
    # Ruled 2026-09-27 (Emma): a separate population; ten at the start of every batch, as a test.
    fs = [["CREATE", f'LAST\tLmul\t"FS {k}"', "LAST\tP31\tQ5", f'LAST\tP2889\t"AB{k:02d}-XYZ"']
          for k in range(12)]
    out = split.order_file(BATCH, first_people=2, ring_ids={"300", "500"}, seed="2026-09-27",
                           familysearch=fs)
    heads = [l for l in out.splitlines() if l.startswith(split.HEADER)]
    assert heads[0].startswith("# ▶ FAMILYSEARCH: 10 people")
    assert sum(1 for k in range(12) if f'"FS {k}"' in out) == 10
    assert out.index('"FS 0"') < out.index('"Ring One"')
    again = split.order_file(out, first_people=2, ring_ids={"300", "500"}, seed="2026-09-27",
                             familysearch=fs)
    assert again == out


def test_familysearch_ring_people_join_the_ring():
    # Emma, 2026-09-27 (AskUserQuestion): the ring's FamilySearch-only people are created with
    # P2889 and go in THE RING, all of them; the ten-person test is the FamilySearch people who
    # are not on the ring. The tree keys a FamilySearch-only person as FS + the id without its dash.
    def fs(k, fsid):
        return ["CREATE", f'LAST\tLmul\t"FS {k}"', "LAST\tP31\tQ5", f'LAST\tP2889\t"{fsid}"',
                'LAST\tP40\tQ10\tS2889\t"' + fsid + '"', 'Q10\tP22\tLAST\tS2889\t"' + fsid + '"']
    ring_fs = [fs("ring a", "AAAA-111"), fs("ring b", "BBBB-222")]
    test_fs = [fs(k, f"CD{k:02d}-XYZ") for k in range(12)]
    ring_ids = {"300", "500", "FSAAAA111", "FSBBBB222"}
    assert split.ring_geni_ids(ring_fs[0]) == {"FSAAAA111"}
    out = split.order_file(BATCH, first_people=2, ring_ids=ring_ids, seed="2026-09-27",
                           familysearch=test_fs, familysearch_ring=ring_fs)
    heads = [l for l in out.splitlines() if l.startswith(split.HEADER)]
    assert heads[0].startswith("# ▶ FAMILYSEARCH: 10 people")
    assert heads[1].startswith("# ▶ THE RING: all 4 ancestor-ring people")
    ring_section = out.split("# ▶ THE RING")[1].split("# ▶ NAME ITEMS")[0]
    for name in ("FS ring a", "FS ring b", "Ring One", "Ring Two"):
        assert f'"{name}"' in ring_section
    assert 'Q10\tP22\tLAST' in ring_section            # the child's link back travels with them
    assert sum(1 for k in range(12) if f'"FS {k}"' in out) == 10
    # Idempotent on its own output: the FamilySearch ring people are now in the file, so a second
    # pass recognises them as ring people and copies nothing in twice.
    again = split.order_file(out, first_people=2, ring_ids=ring_ids, seed="2026-09-27",
                             familysearch=test_fs, familysearch_ring=ring_fs)
    assert again == out
    assert out.count('"AAAA-111"') == 3                 # P2889, the P40 source, the P22 source


def test_the_last_ring_person_may_be_a_familysearch_person():
    # ring-watch.yml waits for the LAST ring creation; a FamilySearch one is reported as
    # `fs:<id>` so the watcher searches P2889 instead of P2600.
    spec = importlib.util.spec_from_file_location("qs_loop_status",
                                                  REPO / "scripts" / "qs-loop-status.py")
    status = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(status)
    text = "\n".join(["# ▶ THE RING: all 2 ancestor-ring people, shuffled", "CREATE",
                      'LAST\tP2600\t"300"', "CREATE", 'LAST\tP2889\t"AAAA-111"',
                      "# ▶ NAME ITEMS: 0", "CREATE", 'LAST\tP2600\t"999"'])
    assert status.last_ring_geni(text) == "fs:AAAA-111"
    geni_last = text.replace('LAST\tP2889\t"AAAA-111"', 'LAST\tP2600\t"500"')
    assert status.last_ring_geni(geni_last) == "500"
    # A Geni ring person created with a FamilySearch id too (`P2600` then `P2889` in one block)
    # is reported by the Geni id: batch 58dfcdfc6 (2026-10-02) read as `fs:GGZR-Y2K` otherwise.
    both = text.replace('LAST\tP2889\t"AAAA-111"', 'LAST\tP2600\t"500"\nLAST\tP2889\t"GGZR-Y2K"')
    assert status.last_ring_geni(both) == "500"
