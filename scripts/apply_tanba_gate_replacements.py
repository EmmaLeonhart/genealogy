#!/usr/bin/env python3
"""Apply the Tanba day-batch gate replacements to build-garborg-day.py."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "scripts" / "build-garborg-day.py"
REPL = ROOT / "scripts" / "tanba_gate_replacements.json"

def main() -> None:
    data = json.loads(REPL.read_text(encoding="utf-8"))
    text = TARGET.read_text(encoding="utf-8")
    if "from tanba_batch_block import tanba_blocked_qids" in text and 'if "tanba" in line.lower():' in text:
        print("gate already present")
        return
    for i, r in enumerate(data["replacements"]):
        if r["old"] not in text:
            raise SystemExit(f"replacement {i} old text not found")
        text = text.replace(r["old"], r["new"], 1)
        print(f"applied replacement {i}")
    TARGET.write_text(text, encoding="utf-8")
    print(f"wrote {TARGET}")

if __name__ == "__main__":
    main()
