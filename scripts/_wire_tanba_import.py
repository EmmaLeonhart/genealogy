"""Prefer tanba_batch_block import over inline tanba_blocked_qids in build-garborg-day.py."""
from __future__ import annotations

import re
from pathlib import Path

path = Path("scripts/build-garborg-day.py")
text = path.read_text(encoding="utf-8")
if "def tanba_blocked_qids(" in text and "from tanba_batch_block import tanba_blocked_qids" not in text:
    text2, n = re.subn(
        r"\ndef tanba_blocked_qids\(\):.*?^\n(?=def kluge_blocked_from_universe)",
        "\n",
        text,
        count=1,
        flags=re.S | re.M,
    )
    if n != 1:
        raise SystemExit(f"could not strip inline tanba_blocked_qids (n={n})")
    lines = text2.splitlines(keepends=True)
    out, inserted = [], False
    for ln in lines:
        out.append(ln)
        if (not inserted) and ln.startswith("import qs_v1"):
            out.append(
                "from tanba_batch_block import tanba_blocked_qids  "
                "# noqa: E402 - day batch must never edit Tanba\n"
            )
            inserted = True
    if not inserted:
        raise SystemExit("qs_v1 import not found")
    path.write_text("".join(out), encoding="utf-8")
    print("replaced inline with import")
elif "from tanba_batch_block import tanba_blocked_qids" in text:
    print("import already present")
else:
    if 'if "tanba" in line.lower():' not in text:
        raise SystemExit("gate missing after install")
    print("inline gate present (ok)")
