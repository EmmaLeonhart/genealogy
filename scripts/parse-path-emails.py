"""Turn Geni relationship-notification emails into `reports/path-permalinks.tsv`.

    python scripts/parse-path-emails.py <export.mbox | bodies.txt> [more ...]

⛔ **THIS IS THE THIRD OF THE PATH REQUESTS WE WERE THROWING AWAY.** Measured on the
4,432-attempt drain, 2026-09-19: `queued/queued` is **2,969, 67%**. A queued search's
answer never comes back in the response, and it reaches `/paths` only when a path is
FOUND -- so the only record of a completed search living outside the browser is the
notification email. Emma, 2026-09-19: *"my email contains all of the requested paths ...
you can recover them from my email."*

**What the email is worth.** Each one carries a full degree sentence and a
`https://www.geni.com/c/<64 hex>` permalink. That permalink is **a saved path object** --
the same kind `pathchains.js` spends 28 minutes walking `/paths` to collect thirty at a
time. Harvesting them off email costs no Geni traffic at all, which is the whole point
when § *GENI IS ACTIVELY HOSTILE* governs every other route.

**Two routes in, and MBOX IS THE ONE THAT SCALES.** The session's Gmail connector fetches
one message per round trip, so N notifications cost N round trips -- fine for topping up,
useless for the backlog. A Google Takeout export of the mailbox is a single file this
reads in seconds, and no credential passes through the agent to get it. Either input
works; it merges into the TSV on the hash, so overlapping runs add nothing and lose
nothing.

⛔ **AND QUOTED-PRINTABLE IS WHY THIS USES `email` RATHER THAN A REGEX OVER THE FILE.** A
mbox body is encoded, and quoted-printable inserts a soft line break -- an `=` at the end
of a line -- every 76 characters, straight through a 64-character hex permalink. A regex over
the raw file finds a fraction of them and looks like it worked. `email.message_from_*`
decodes the part before anything is matched, and the HTML alternative is stripped only
when there is no plain-text part.

**The count Gmail reports is not a count.** `resultCountEstimate` came back as exactly
**201** for `from:geni.com subject:relationship`, for `from:no-reply@geni.com "View the
full"`, and for the bare query `in:anywhere` which matches the whole mailbox -- measured
2026-09-19. It is a cap. Notifications older than that window exist (09-12, 09-13 checked
by hand), so any figure of "about 200" taken from that field describes the cap and not
the mail.

⛔ **THE ANCHOR IS NOT ALWAYS THE ACCOUNT OWNER AND THAT IS RECORDED, NOT SOLVED.** These
bodies read *"is Private User's ..."* and a `/path/` page has been seen anchored on a
third party. `queue.md` says not to investigate it without being asked, so the anchor
sentence is stored verbatim in `degree` rather than parsed into endpoints. Whoever walks
the permalink gets the truth from the page.
"""
from __future__ import annotations

import csv
import email
import email.policy
import mailbox
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reports" / "path-permalinks.tsv"

FIELDS = ["hash", "kind", "subject_name", "degree", "url"]

#: The permalink. 64 hex, and the `?u=%2Fpaths` variant two lines below it in every mail
#: is the SAME hash -- matching greedily across both is how a one-line parser ends up with
#: half the set.
URL_RE = re.compile(r"https://www\.geni\.com/c/([0-9a-f]{64})")

#: `email_type=blood_path_search_notification` / `..._inlaw_...`. Taken from the
#: unsubscribe link rather than the subject line, because the subject is free text with
#: the person's name in it and the query parameter is not.
KIND_RE = re.compile(r"email_type=(\w*?)_?path_search_notification")

#: `<Name> is <anchor>'s <degree>.` -- the whole sentence, kept whole. See the anchor note
#: in the module docstring for why this is not split into endpoints.
DEGREE_RE = re.compile(r"^(.+? is .+?(?:'s|s') .+?\.)\s*$", re.M)

#: ⛔ **A `/c/` LINK IS NOT A PATH OBJECT, AND WITHOUT THIS 636 OF THEM WERE NOT.** `/c/<hash>`
#: is Geni's generic content permalink, so it turns up in mail that has nothing to do with a
#: relationship search -- the one that exposed it was subject *"StrangerChat sent you a
#: message"*. Over the whole mailbox that was **636 rows of 48,328**, every one of them with a
#: valid-looking hash, a blank kind and a blank degree, and every one of them would have sent
#: the chain walker at a URL that is not a path. So a block counts only when it carries the
#: notification's own marker: the `email_type` parameter, or the `View the full X
#: relationship:` line that precedes the permalink in every real one.
NOTIFICATION_RE = re.compile(
    r"path_search_notification|View the full (blood|in-?law) relationship")


_TAG_RE = re.compile(r"<[^>]+>")


def body_text(msg) -> str:
    """The decoded plain-text body of one message, or the HTML with its tags stripped."""
    if msg.is_multipart():
        plain = [p for p in msg.walk() if p.get_content_type() == "text/plain"]
        html = [p for p in msg.walk() if p.get_content_type() == "text/html"]
        part = (plain or html or [None])[0]
        if part is None:
            return ""
    else:
        part = msg
    try:
        text = part.get_content()
    except Exception:
        payload = part.get_payload(decode=True) or b""
        text = payload.decode(part.get_content_charset() or "utf-8", "replace")
    if part.get_content_type() == "text/html":
        text = _TAG_RE.sub(" ", text)
    return text


def read_source(path: Path) -> str:
    """One file of message text, whether it is an mbox, one raw message, or pasted bodies.

    An mbox is detected by its `From ` separator -- the one thing the format guarantees --
    rather than by the extension, because a Takeout file is named after the LABEL and not
    the format.
    """
    raw = path.read_bytes()
    if raw[:5] == b"From ":
        box = mailbox.mbox(str(path))
        try:
            return chr(10).join(body_text(m) for m in box)
        finally:
            box.close()
    text = raw.decode("utf-8", "replace")
    if re.match(r"(?im)^(?:Delivered-To|Received|MIME-Version|Content-Type):", text):
        return body_text(email.message_from_string(text, policy=email.policy.default))
    return text


def parse(text: str) -> list[dict]:
    """Every notification in `text`, split on the permalink that ends each one.

    A file of concatenated bodies has no reliable separator -- the signature block is
    identical in all of them -- so the split is on the first URL of each mail, which is
    the one field guaranteed present and unique.
    """
    rows, skipped = [], []
    for block in re.split(r"(?=Dear Emma,)", text):
        m = URL_RE.search(block)
        if not m:
            continue
        marker = NOTIFICATION_RE.search(block)
        if not marker:
            skipped.append(m.group(1))
            continue
        kind = KIND_RE.search(block)
        degree = DEGREE_RE.search(block)
        rows.append({
            "hash": m.group(1),
            # `email_type` first: the subject and the body line are free text with a
            # person's name in them, the query parameter is not. The `View the full ...`
            # line is the fallback for a mail that carries no unsubscribe footer.
            "kind": ((kind.group(1) or "blood") if kind
                     else (marker.group(1) or "").replace("-", "") or ""),
            "subject_name": (degree.group(1).split(" is ", 1)[0].strip()
                             if degree else ""),
            "degree": degree.group(1).strip() if degree else "",
            "url": f"https://www.geni.com/c/{m.group(1)}",
        })
    if skipped:
        print(f"  skipped {len(skipped):,} /c/ links that are not path notifications")
    return rows


def merge(rows: list[dict]) -> tuple[int, int]:
    """Merge into the TSV on the hash. Returns `(added, total)`.

    Sorted on the hash: a total order over a fixed-width hex key, so the same set of
    permalinks always writes the same bytes no matter what order they were harvested in
    -- `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*.
    """
    held: dict[str, dict] = {}
    if OUT.exists():
        with OUT.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                held[row["hash"]] = row
    before = len(held)
    for row in rows:
        held.setdefault(row["hash"], row)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for key in sorted(held):
            w.writerow(held[key])
    return len(held) - before, len(held)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    rows = []
    for arg in sys.argv[1:]:
        rows += parse(read_source(Path(arg)))
    added, total = merge(rows)
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r["kind"] or "?"] = kinds.get(r["kind"] or "?", 0) + 1
    print(f"{len(rows):,} notifications parsed, {added:,} new, {total:,} held "
          f"-> {OUT.relative_to(REPO)}")
    for k, n in sorted(kinds.items()):
        print(f"  {n:>5}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
