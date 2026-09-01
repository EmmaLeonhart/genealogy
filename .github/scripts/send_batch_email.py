"""Email the day's QuickStatements batch to Emma, as an attachment.

**Her instruction, 2026-08-31:** *"not wikidata editing but instead emailing me the daily
quickstatements file to me every day so I can run it."* Nothing here touches Wikidata.

**It sends the FILE, not a summary** — the batch is what she runs, and a description of it is
not something anyone can paste into QuickStatements.

Stdlib only, like everything else here: `smtplib` and `email` ship with Python.

Credentials come from the environment, set by the workflow from repository secrets. There is no
fallback and no default recipient hard-coded anywhere but here.
"""

from __future__ import annotations

import datetime
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

BATCH = Path("reports/wikidata-garborg-day.qs")
TO = "emma@topazcomputing.com"


def main() -> int:
    server = os.environ.get("SMTP_SERVER", "").strip()
    user = os.environ.get("SMTP_USERNAME", "").strip()
    password = os.environ.get("SMTP_PASSWORD", "")
    if not (server and user and password):
        print("SMTP credentials incomplete; nothing sent.")
        return 0
    if not BATCH.exists() or not BATCH.stat().st_size:
        print(f"{BATCH} is missing or empty; nothing sent.")
        return 1

    today = datetime.date.today().isoformat()
    creates = os.environ.get("CREATES", "?")
    lines = os.environ.get("LINES", "?")
    carried = os.environ.get("CARRIED", "?")

    msg = EmailMessage()
    msg["Subject"] = f"Garborg batch {today} — {creates} creations"
    msg["From"] = user
    msg["To"] = TO
    # Plain, factual, no instructions: she knows what to do with it.
    msg.set_content(
        f"Today's QuickStatements batch is attached.\n\n"
        f"  {creates} CREATE blocks\n"
        f"  {lines} statement lines\n"
        f"  {carried} people carried forward to a later day\n\n"
        f"Name items come first in the file, then the day's people, so it runs top to bottom\n"
        f"as one paste.\n")
    msg.add_attachment(BATCH.read_bytes(), maintype="text", subtype="plain",
                       filename=f"wikidata-garborg-{today}.qs")

    context = ssl.create_default_context()
    # Port 465 is implicit TLS; 587 is STARTTLS. Try the explicit one first and fall back,
    # because which a provider wants is not something to guess wrong silently at 06:05.
    try:
        with smtplib.SMTP_SSL(server, 465, context=context, timeout=60) as s:
            s.login(user, password)
            s.send_message(msg)
    except Exception as first:                                      # noqa: BLE001
        print(f"implicit TLS on 465 failed ({first}); trying STARTTLS on 587")
        with smtplib.SMTP(server, 587, timeout=60) as s:
            s.starttls(context=context)
            s.login(user, password)
            s.send_message(msg)
    print(f"sent {BATCH} to {TO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
