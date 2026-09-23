#!/usr/bin/env python3
"""One-shot: wire pipeline.yml + drop done queue.md items via Contents API.

Run in Actions with GITHUB_TOKEN (no checkout of the giant tree). Safe to re-run:
skips steps already applied.
"""
from __future__ import annotations

import base64
import json
import os
import re
import urllib.error
import urllib.request

OWNER = "EmmaLeonhart"
REPO = "genealogy"
TOKEN = os.environ["GITHUB_TOKEN"]
API = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
H = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get(path: str) -> dict:
    req = urllib.request.Request(f"{API}/{path}?ref=main", headers=H)
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def put(path: str, message: str, text: str, sha: str) -> dict:
    body = json.dumps(
        {
            "message": message,
            "content": base64.b64encode(text.encode()).decode(),
            "sha": sha,
            "branch": "main",
        }
    ).encode()
    req = urllib.request.Request(
        f"{API}/{path}",
        data=body,
        method="PUT",
        headers={**H, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def delete(path: str, message: str, sha: str) -> dict:
    body = json.dumps({"message": message, "sha": sha, "branch": "main"}).encode()
    req = urllib.request.Request(
        f"{API}/{path}",
        data=body,
        method="DELETE",
        headers={**H, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def wire_pipeline() -> None:
    meta = get(".github/workflows/pipeline.yml")
    text = base64.b64decode(meta["content"]).decode()
    if "build-patronymic-pairs.py" in text:
        print("pipeline already wired")
        return
    needle = (
        "      - name: CJK readings for the name items this corpus bears\n"
        "        continue-on-error: true\n"
        "        env:\n"
        "          PYTHONPATH: src\n"
        "        run: python scripts/build-name-item-cjk.py\n"
        "\n"
        "      - name: Refresh the batch inventory\n"
    )
    insert = (
        "      - name: CJK readings for the name items this corpus bears\n"
        "        continue-on-error: true\n"
        "        env:\n"
        "          PYTHONPATH: src\n"
        "        run: python scripts/build-name-item-cjk.py\n"
        "\n"
        "      # Patronymics in pairs + description uniqueness measurement (META queue).\n"
        "      - name: Patronymic gendered pairs\n"
        "        continue-on-error: true\n"
        "        env:\n"
        "          PYTHONPATH: src\n"
        "        run: python scripts/build-patronymic-pairs.py\n"
        "\n"
        "      - name: Description uniqueness measurement\n"
        "        continue-on-error: true\n"
        "        env:\n"
        "          PYTHONPATH: src\n"
        "        run: python scripts/build-description-audit.py\n"
        "\n"
        "      - name: Refresh the batch inventory\n"
    )
    if needle not in text:
        raise SystemExit("pipeline insertion needle not found")
    text = text.replace(needle, insert, 1)
    out = put(
        ".github/workflows/pipeline.yml",
        "Wire patronymic-pairs and description-audit into pipeline.yml",
        text,
        meta["sha"],
    )
    print("pipeline committed", out["commit"]["sha"])


def patch_queue() -> None:
    meta = get("queue.md")
    text = base64.b64decode(meta["content"]).decode()
    changed = False

    pages = (
        "- **⛔ PUT A LINK ON THE GITHUB PAGES SITE TO THE ACTION THAT REDOES EVERYTHING.** "
        "One workflow,\n"
        "  one link, running the whole chain: *\"synoptic tree rebuilding, checking, "
        "refreshing the ledger,\n"
        "  building the quick statements, and running them on Wikidata.\"*\n"
        "\n"
    )
    if pages in text:
        text = text.replace(pages, "", 1)
        changed = True
        print("removed Pages META bullet")

    m = re.search(
        r"### ⛔ PATRONYMICS ARE MADE IN PAIRS\. STANDING ORDER, AND IT IS NOT BEING FOLLOWED\n"
        r".*?"
        r"(?=### ⛔ THE BATCH IS PUTTING)",
        text,
        flags=re.S,
    )
    if m:
        text = text[: m.start()] + text[m.end() :]
        changed = True
        print("removed patronymic-pairs standing-order section")

    old = (
        "Top to bottom.* below — first bullet, the Pages link to the redo-everything "
        "action. No further\ncheck-in."
    )
    new = (
        "Top to bottom.* below — first remaining bullet (description uniqueness review). "
        "No further\ncheck-in."
    )
    if old in text:
        text = text.replace(old, new, 1)
        changed = True
        print("updated CI-green next-bullet prose")

    if not changed:
        print("queue already up to date")
        return
    out = put(
        "queue.md",
        "queue.md: drop done Pages redo-link + patronymic-pairs standing-order",
        text,
        meta["sha"],
    )
    print("queue committed", out["commit"]["sha"])


def self_delete() -> None:
    path = ".github/workflows/apply-meta-wiring.yml"
    try:
        meta = get(path)
    except urllib.error.HTTPError as e:
        print("self-delete skipped:", e)
        return
    out = delete(path, "Remove one-shot apply-meta-wiring.yml after landing", meta["sha"])
    print("self-deleted", out["commit"]["sha"])


def main() -> int:
    wire_pipeline()
    patch_queue()
    self_delete()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
