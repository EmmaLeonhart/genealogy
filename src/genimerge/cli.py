"""Command line entry points: ``python -m genimerge <command>``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import inventory

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_LAKE = REPO_ROOT / "data_lake"
REPORTS = REPO_ROOT / "reports"
OUT = REPO_ROOT / "out"


def _default_exports() -> list[Path]:
    return sorted(DATA_LAKE.glob("*.ged"))


def _cmd_inventory(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in args.exports] or _default_exports()
    if not paths:
        print(f"no .ged files given and none found in {DATA_LAKE}", file=sys.stderr)
        return 1

    inv = inventory.build_inventory(paths)
    text = inventory.render_markdown(inv)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {args.output} ({len(inv.files)} exports)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genimerge", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("inventory", help="measure the exports and write a report")
    p_inv.add_argument("exports", nargs="*", help="GEDCOM files (default: data_lake/*.ged)")
    p_inv.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPORTS / "inventory.md",
        help="where to write the report (default: reports/inventory.md)",
    )
    p_inv.set_defaults(func=_cmd_inventory)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
