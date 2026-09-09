"""Remove the `S2600` reference from `P2600` statements in a QuickStatements file.

    python scripts/strip-p2600-self-cites.py <in.qs> [-o <out.qs>]

**Emma, 2026-08-31:** *"geni ids do not get sources"*, and then *"Just have a script to remove
the fucking self-cites"*.

`Q6014618 P2600 "4198641" S2600 "4198641"` cites the Geni id statement to the Geni id. `S2600`
is right on every statement *derived* from a Geni profile -- there the profile is external
evidence for a claim about the person. On `P2600` the profile IS the claim, so the reference
restates the value and nothing else.

**This is a filter, not a rebuild, and that distinction is the whole point of it existing.**
Regenerating the batch to fix this also re-draws the label cap and the carry-forward, so the
file changes in ways nobody asked for -- which is exactly what went wrong when I did it. This
touches only the offending lines and leaves every other byte alone.

The generator no longer emits them (`build-garborg-day.add`), so this is for files already in
hand.
"""

import argparse
import io
import pathlib
import sys


def strip(line):
    """Drop a trailing `\tS2600\t"..."` when the statement's property is `P2600`."""
    parts = line.split("\t")
    if len(parts) < 3 or parts[1] != "P2600":
        return line, False
    out, dropped = [], False
    i = 0
    while i < len(parts):
        if parts[i] == "S2600" and i + 1 < len(parts):
            i += 2
            dropped = True
            continue
        out.append(parts[i])
        i += 1
    return "\t".join(out), dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=pathlib.Path)
    ap.add_argument("-o", "--out", type=pathlib.Path)
    args = ap.parse_args()

    text = io.open(args.path, encoding="utf-8", newline="").read()
    lines = text.split("\n")
    fixed, n = [], 0
    for ln in lines:
        new, dropped = strip(ln)
        n += dropped
        fixed.append(new)

    out = args.out or args.path
    io.open(out, "w", encoding="utf-8", newline="").write("\n".join(fixed))

    # A count that does not match is a filter that did something else; say so rather than
    # reporting success.
    remaining = sum(1 for ln in fixed if ln.split("\t")[1:2] == ["P2600"] and "S2600" in ln)
    print(f"{n} self-citation(s) removed -> {out}")
    print(f"{len(lines)} lines in, {len(fixed)} out (must be equal)")
    print(f"{remaining} P2600 statements still carrying S2600 (must be 0)")
    if remaining or len(lines) != len(fixed):
        sys.exit("FAILED -- the file was not written as intended")


if __name__ == "__main__":
    main()
