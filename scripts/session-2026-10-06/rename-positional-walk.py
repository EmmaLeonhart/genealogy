"""Rename the outward walk from "zipper" to "positional walk" (queue item, Emma 2026-10-04).

A zipper merge (Emma's definition) identifies a path of people between two people who were already
entity-resolved independently. `zipper-join.py` never did that: it walked outward from anchors. So
the walk, its files and its source tag stop being called a zipper.

Live files only. History keeps its words: devlog.md, docs/queue-archive/, the dated session
scripts and reports (session-2026-10-0*, the dated zipper-split/-review/-ebec batches), CLAUDE.md
(edited by hand: it also describes the intended zipper merge).

    python scripts/session-2026-10-06/rename-positional-walk.py            # dry run
    python scripts/session-2026-10-06/rename-positional-walk.py --apply
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv

MOVES = {
    "scripts/zipper-join.py": "scripts/positional-walk.py",
    "scripts/census-zipper-evidence.py": "scripts/census-positional-walk-evidence.py",
    "scripts/measure-zipper-reliability.py": "scripts/measure-positional-walk-reliability.py",
    "scripts/zipper-provenance.py": "scripts/positional-walk-provenance.py",
    "tests/test_zipper_no_solo.py": "tests/test_positional_walk_no_solo.py",
    "out/zipper-sample20.json": "out/positional-walk-sample20.json",
    "reports/sweep-parsed-zipper.tsv": "reports/sweep-parsed-positional-walk.tsv",
}
for stem in ("pairs", "ambiguous", "conflicts", "sex-refuted"):
    MOVES[f"reports/zipper-{stem}.tsv"] = f"reports/positional-walk-{stem}.tsv"
    MOVES[f"reports/familysearch-zipper-{stem}.tsv"] = f"reports/familysearch-positional-walk-{stem}.tsv"
for name in ("zipper-evidence.tsv", "zipper-provenance.tsv", "zipper-provenance-chains.md",
             "zipper-reliability.md", "zipper-driven-links.csv", "zipper-only-links-on-wikidata.csv"):
    MOVES[f"reports/{name}"] = "reports/" + name.replace("zipper", "positional-walk")

HISTORY = re.compile(r"^(devlog\.md|CLAUDE\.md|docs/queue-archive/|scripts/session-2026-10-0|"
                     r"reports/session-2026-10-0|reports/zipper-split-batch-|reports/zipper-review-|"
                     r"reports/zipper-ebec-|reports/zipper-links-batch-|reports/daily-audit/|"
                     r"exports/|gedcom/|sessions/|harvested-paths/|queue\.md|todo\.md|reports/emma-judgments|"
                     r"reports/user-turns|reports/.*-2026-\d\d-\d\d)")

#: Code and docs get the prose rules too; every other file (data) only the lowercase file-name and
#: source-tag forms, so people named Zipper (Herbert Zipper Q214870, Wilhelm von Zipperlen) are untouched.
PROSE = re.compile(r"^(scripts/|src/|tests/|\.github/|docs/|README\.md|handoff/|\.gitignore)")

IDENT_RULES = [
    (re.compile(r"zipper-join"), "positional-walk"),                  # the script's own new name
    (re.compile(r"zipper_join"), "positional_walk"),
    (re.compile(r"""(["'])zipper\1"""), r"\1positional-walk\1"),      # the source tag / file prefix
    (re.compile(r"ZIPPER_"), "POSITIONAL_WALK_"),
    (re.compile(r"zipper_"), "positional_walk_"),
    (re.compile(r"_zipper"), "_positional_walk"),
    (re.compile(r"zipper-"), "positional-walk-"),
    (re.compile(r"-zipper"), "-positional-walk"),
    (re.compile(r"(?<![A-Za-z;])zipper(?=;)|(?<=;)zipper(?![A-Za-z-])"), "positional-walk"),  # a;b tags
    (re.compile(r"(?<=\t)zipper(?=[\t\r\n])"), "positional-walk"),     # a bare TSV cell
]
PROSE_RULES = [
    (re.compile(r"ZIPPER(ING|ED)? (MERGE|JOIN)"), "POSITIONAL WALK"),
    (re.compile(r"[Zz]ipper(ing|ed)? (merge|join)"), lambda m: ("P" if m.group(0)[0] == "Z" else "p") + "ositional walk"),
    (re.compile(r"ZIPPERING|ZIPPER"), "POSITIONAL WALK"),
    (re.compile(r"\b[Zz]ippering\b|\b[Zz]ippered\b"), lambda m: ("P" if m.group(0)[0] == "Z" else "p") + "ositional walk"),
    (re.compile(r"\b[Zz]ipper(?![a-z])"), lambda m: ("P" if m.group(0)[0] == "Z" else "p") + "ositional walk"),
]


def tracked():
    out = subprocess.run(["git", "-c", "diff.ignoreSubmodules=all", "grep", "-l", "-I", "-i", "zipper",
                          "--", "."], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    return [p for p in out.splitlines() if p and not HISTORY.match(p)]


#: Emma's words are quoted as *"..."*; a quotation keeps its words.
QUOTE = re.compile(r'\*"[^"\n]*"\*')


def rewrite(text, prose):
    parts, last = [], 0
    for m in QUOTE.finditer(text):
        parts += [(text[last:m.start()], True), (m.group(0), False)]
        last = m.end()
    parts.append((text[last:], True))
    out = []
    for chunk, editable in parts:
        if editable:
            for rx, rep in IDENT_RULES + (PROSE_RULES if prose else []):
                chunk = rx.sub(rep, chunk)
        out.append(chunk)
    return "".join(out)


def rewrite_python(text):
    """A .py file token by token: a name `zipper`/`ZIPPER` becomes `positional_walk`/
    `POSITIONAL_WALK`, other names take the identifier rules, and only strings and comments take
    the prose rules (a plain-text pass turned the variable `zipper` into `positional walk`)."""
    import io
    import tokenize
    lines = text.splitlines(keepends=True)
    starts = [0]
    for ln in lines:
        starts.append(starts[-1] + len(ln))
    edits = []
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if "zipper" not in tok.string.lower():
            continue
        if tok.type == tokenize.NAME:
            new = {"zipper": "positional_walk", "ZIPPER": "POSITIONAL_WALK"}.get(
                tok.string, rewrite(tok.string, False))
        elif tok.type in (tokenize.STRING, tokenize.COMMENT) or tok.type == getattr(tokenize, "FSTRING_MIDDLE", -1):
            new = rewrite(tok.string, True)
        else:
            continue
        a = starts[tok.start[0] - 1] + tok.start[1]
        b = starts[tok.end[0] - 1] + tok.end[1]
        edits.append((a, b, new))
    for a, b, new in sorted(edits, reverse=True):
        text = text[:a] + new + text[b:]
    return text


def main():
    for src, dst in MOVES.items():
        if (ROOT / src).exists():
            print(f"mv {src} -> {dst}")
            if APPLY:
                subprocess.run(["git", "-c", "diff.ignoreSubmodules=all", "mv", src, dst], cwd=ROOT, check=True)
    for rel in tracked():
        p = ROOT / rel
        try:
            text = p.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            print(f"SKIP (not UTF-8) {rel}")
            continue
        new = rewrite_python(text) if rel.endswith(".py") else rewrite(text, bool(PROSE.match(rel)))
        if new != text:
            print(f"edit {rel}: {text.lower().count('zipper')} -> {new.lower().count('zipper')}")
            if APPLY:
                p.write_bytes(new.encode("utf-8"))


if __name__ == "__main__":
    main()
