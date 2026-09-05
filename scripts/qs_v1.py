"""Read a QuickStatements V1 batch into typed edit objects.

**Why this exists.** Emma, 2026-09-05, chose that from the 15th the daily Garborg
batch runs itself, sent *"bot-password API, what exists"* -- i.e. through
`scripts/wikidata-edit-run.py` rather than pasted into QuickStatements by hand.
That runner takes JSON **edit objects** with a `requires` list; the daily batch is
`reports/wikidata-garborg-day.txt`, QuickStatements V1. This is the join between
them, and it is the only place that knows QS-V1 syntax.

**The whole difficulty is `LAST`, and it is positional.** `LAST` means *the item
the CREATE immediately above minted* -- so the order of the file is load-bearing in
a way `genimerge.editorder` deliberately destroys: that module picks at random from
whatever is ready, which is right for independent edits and fatal for `LAST`. The
fix is not to preserve file order. It is to make the dependency **explicit**, which
is what `requires` is for:

- a `CREATE` and every `LAST`-subject line under it fuse into **one** edit object,
  sent as a single `wbeditentity new=item`. They cannot be reordered because they
  are no longer separate things.
- a line whose *subject* is a QID and whose *value* is `LAST` becomes its own edit
  object carrying `requires: [<the create's id>]`, and the QID `LAST` resolves to
  is substituted at send time. `CLAUDE.md` § *THE THREE LINES*: `Q… P22 LAST` is
  ordinary QuickStatements, and calling it impossible cost weeks of one-way links.

**Ids are a hash of the command, not the line number.** The batch is regenerated
every day and lines shift; an id that moved would make `--satisfied` name the wrong
edit on a resumed run.

**The grammar implemented is the one the corpus actually uses**, measured over
`reports/wikidata-garborg-day.txt` on 2026-09-05 -- 18 distinct command shapes, all
of the form `subject / target / value` plus zero or more `P<n> value` qualifier
pairs and `S<n> value` reference pairs. Anything outside it **raises**, per
`CLAUDE.md` § *GEDCOM dates have a specification*: a parser that silently drops
what it does not understand is how 4,459 events lost their year. A batch that will
not parse is a batch that does not run.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

__all__ = ["ParseError", "Command", "parse", "edit_objects"]

_QID = re.compile(r"Q[1-9]\d*\Z")
_PROP = re.compile(r"P[1-9]\d*\Z")
_SOURCE = re.compile(r"S[1-9]\d*\Z")
_TERM = re.compile(r"([LAD])([a-z]{2,3}(?:-[a-z0-9]{2,8})*)\Z")
_STR = re.compile(r'"(.*)"\Z', re.S)
_MONO = re.compile(r'([a-z]{2,3}(?:-[a-z0-9]{2,8})*):"(.*)"\Z', re.S)
_TIME = re.compile(r"([+-]\d{4,}-\d\d-\d\dT\d\d:\d\d:\d\dZ)/(\d+)\Z")


class ParseError(ValueError):
    """A line the grammar does not cover. Never swallowed, never guessed at."""


@dataclass
class Command:
    """One QuickStatements V1 line, with its qualifiers and references."""

    subject: str                      # "LAST" or "Q123"
    target: str                       # "P31", "Lmul", "Amul", "Den"
    value: dict
    qualifiers: list = field(default_factory=list)   # [(prop, value)]
    references: list = field(default_factory=list)   # [(prop, value)]
    line: int = 0
    text: str = ""

    @property
    def is_term(self) -> bool:
        return bool(_TERM.match(self.target))


def _value(field_: str) -> dict:
    """One QS value, typed. The type is read off the syntax, never inferred later."""
    if field_ == "LAST":
        return {"type": "item", "id": "LAST"}
    if _QID.match(field_):
        return {"type": "item", "id": field_}
    m = _TIME.match(field_)
    if m:
        return {"type": "time", "time": m.group(1), "precision": int(m.group(2))}
    m = _MONO.match(field_)
    if m:
        return {"type": "monolingualtext", "language": m.group(1), "text": m.group(2)}
    m = _STR.match(field_)
    if m:
        return {"type": "string", "value": m.group(1)}
    raise ParseError(f"not a QuickStatements value: {field_!r}")


def parse(text: str):
    """The batch as a list of `"CREATE"` markers and `Command`s, in file order.

    Comments and blank lines are dropped -- they carry no instruction, and
    `CLAUDE.md` § *NO descriptions and NO edit summaries* records that a `#` in a
    `.qs` never reaches Wikidata.
    """
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) == 1:
            if fields[0].strip().upper() == "CREATE":
                out.append("CREATE")
                continue
            raise ParseError(f"line {n}: lone field that is not CREATE: {line!r}")
        if len(fields) < 3:
            raise ParseError(f"line {n}: {len(fields)} fields, expected 3 or more")

        subject, target = fields[0], fields[1]
        if subject != "LAST" and not _QID.match(subject):
            raise ParseError(f"line {n}: subject is neither LAST nor a QID: {subject!r}")
        if not (_PROP.match(target) or _TERM.match(target)):
            raise ParseError(f"line {n}: not a property or term code: {target!r}")

        cmd = Command(subject=subject, target=target, value=_value(fields[2]),
                      line=n, text=line)

        rest = fields[3:]
        if len(rest) % 2:
            raise ParseError(f"line {n}: trailing field with no value: {rest[-1]!r}")
        for prop, val in zip(rest[0::2], rest[1::2]):
            if _SOURCE.match(prop):
                cmd.references.append(("P" + prop[1:], _value(val)))
            elif _PROP.match(prop):
                cmd.qualifiers.append((prop, _value(val)))
            else:
                raise ParseError(f"line {n}: not a qualifier or source: {prop!r}")
        if cmd.is_term and (cmd.qualifiers or cmd.references):
            raise ParseError(f"line {n}: a label/alias/description takes no qualifiers")
        if cmd.is_term and cmd.value["type"] != "string":
            raise ParseError(f"line {n}: a label/alias/description takes a string")
        out.append(cmd)
    return out


def _ident(kind: str, canonical: str, taken: set) -> str:
    """A stable id: the hash of what the edit says, not where it sits in the file."""
    base = f"qs-{kind}-{hashlib.sha1(canonical.encode('utf-8')).hexdigest()[:12]}"
    if base not in taken:
        taken.add(base)
        return base
    for i in range(2, 1000):
        cand = f"{base}-{i}"
        if cand not in taken:
            taken.add(cand)
            return cand
    raise ParseError(f"cannot make a unique id for {base}")


def _claim(cmd: Command) -> dict:
    return {
        "property": cmd.target,
        "value": cmd.value,
        "qualifiers": [{"property": p, "value": v} for p, v in cmd.qualifiers],
        "references": [{"property": p, "value": v} for p, v in cmd.references],
        "line": cmd.line,
    }


def edit_objects(commands) -> list:
    """The parsed batch as edit objects `wikidata-edit-run.py` can order and send.

    Three kinds, and the split is forced by what one API call can do atomically:

    - ``create`` -- a `CREATE` plus every `LAST`-subject line beneath it, as one
      `wbeditentity new=item`.
    - ``statement`` -- a QID subject with claims, one `wbeditentity` merge.
    - ``terms`` -- a QID subject with labels/aliases/descriptions.

    A statement or term block that mentions `LAST` gains ``requires`` naming the
    create above it, and `resolve` records which value fields need substituting.
    """
    # PASS 1 -- group. `LAST` is resolved to a block INDEX here, before any id
    # exists, because a block's id is a hash of its finished text and the real
    # batch interleaves: measured on 2026-09-05, LAST-subject lines resume after a
    # `Q… P… LAST` line 15 times in one day's file. A one-pass reader that closed
    # the create on the first such line would reject the batch it is written for.
    blocks: list = []
    others: list = []              # (command, block index or None)
    current = None
    for item in commands:
        if item == "CREATE":
            current = len(blocks)
            blocks.append({"kind": "create", "labels": {}, "aliases": {},
                           "descriptions": {}, "claims": [], "_lines": ["CREATE"]})
            continue
        cmd = item
        if cmd.subject == "LAST":
            if current is None:
                raise ParseError(f"line {cmd.line}: LAST with no CREATE above it")
            _apply(cmd, blocks[current])
            blocks[current]["_lines"].append(cmd.text)
            continue
        uses_last = cmd.value.get("id") == "LAST" or any(
            v.get("id") == "LAST" for _, v in cmd.qualifiers + cmd.references)
        if uses_last and current is None:
            raise ParseError(f"line {cmd.line}: LAST as a value with no CREATE above it")
        others.append((cmd, current if uses_last else None))

    # PASS 2 -- identify. A block's id is the hash of the whole block, so it is
    # stable across a regeneration that moves it up or down the file.
    taken: set = set()
    for blk in blocks:
        blk["id"] = _ident("create", "\n".join(blk["_lines"]), taken)

    objects: list = list(blocks)
    by_key: dict = {}
    for cmd, block in others:
        requires = blocks[block]["id"] if block is not None else None
        # One object per (qid, kind, dependency). Splitting on the dependency
        # matters: an edit needing today's create must not be fused with one that
        # could run regardless, or a failed create would take unrelated statements
        # down with it.
        key = (cmd.subject, "terms" if cmd.is_term else "statement", requires)
        obj = by_key.get(key)
        if obj is None:
            obj = {"kind": key[1], "qid": cmd.subject, "_lines": []}
            if key[1] == "statement":
                obj["claims"] = []
            else:
                obj["labels"], obj["aliases"], obj["descriptions"] = {}, {}, {}
            if requires:
                obj["requires"] = [requires]
            by_key[key] = obj
            objects.append(obj)
        _apply(cmd, obj)
        obj["_lines"].append(cmd.text)

    for obj in objects:
        lines = obj.pop("_lines")
        if "id" not in obj:
            obj["id"] = _ident(obj["kind"], "\n".join(lines), taken)
    return objects


def _apply(cmd: Command, obj: dict) -> None:
    m = _TERM.match(cmd.target)
    if m:
        code, lang = m.group(1), m.group(2)
        text = cmd.value["value"]
        if code == "L":
            obj["labels"][lang] = text
        elif code == "D":
            obj["descriptions"][lang] = text
        else:
            obj["aliases"].setdefault(lang, []).append(text)
        return
    obj["claims"].append(_claim(cmd))
