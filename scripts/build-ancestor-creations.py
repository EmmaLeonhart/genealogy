"""Load Geni↔Wikidata-safe ancestor creations from zlib+base64 payload parts.

Temporary MCP-sized landing. Decompressed source is the real emitter; inline later.
"""
from __future__ import annotations

import base64
import zlib
from pathlib import Path

_dir = Path(__file__).resolve().parent
_b64 = (_dir / "_ac_payload_0.b64").read_text(encoding="ascii") + (
    _dir / "_ac_payload_1.b64"
).read_text(encoding="ascii")
_SRC = zlib.decompress(base64.b64decode(_b64.encode("ascii")))
exec(compile(_SRC, str(Path(__file__).resolve()), "exec"), globals())
