"""Tanba QIDs that must never appear in a QuickStatements day batch.

Ruled 2026-09-22: the live garborg day batch must not edit Tanba people.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def tanba_blocked_qids() -> set[str]:
    """Every Tanba clan QID on disk."""
    out: set[str] = set()
    qids_path = ROOT / "reports" / "tanba-qids.json"
    if qids_path.exists():
        data = json.loads(qids_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for vals in data.values():
                for v in vals if isinstance(vals, list) else [vals]:
                    s = str(v)
                    if s.startswith("Q"):
                        out.add(s)
        elif isinstance(data, list):
            for v in data:
                s = v if isinstance(v, str) else str((v or {}).get("qid", ""))
                if s.startswith("Q"):
                    out.add(s)
    pairs = ROOT / "reports" / "tanba-p2600-pairs.tsv"
    if pairs.exists():
        pat = re.compile(r"Q\d+")
        for line in pairs.read_text(encoding="utf-8").splitlines():
            out.update(pat.findall(line))
    return out
