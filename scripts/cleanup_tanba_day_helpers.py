import base64, json, os, urllib.request, urllib.error

owner, repo = os.environ["OWNER"], os.environ["REPO"]
token = os.environ["GH_TOKEN"]

def api(method, url, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return {}
            return json.load(resp)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        if e.code == 404:
            return None
        print(method, url, e.code, raw[:500])
        raise

base = f"https://api.github.com/repos/{owner}/{repo}/contents"
for path in [
    "scripts/_build_garborg_day_micro_00.txt",
    "scripts/_build_garborg_day_part_0.txt",
    "scripts/_build_garborg_day_part_1.txt",
    "scripts/_build_garborg_day_part_2.txt",
    "scripts/_wire_tanba_import.py",
    "scripts/_tanba_gate_probe.txt",
    "scripts/apply_tanba_gate_replacements.py",
    "scripts/tanba_gate_replacements.json",
    ".github/workflows/assemble-tanba-gated-build.yml",
    ".github/workflows/apply-tanba-day-gate.yml",
    "scripts/put_tanba_day_gate_via_api.py",
    "scripts/cleanup_tanba_day_helpers.py",
]:
    meta = api("GET", f"{base}/{path}?ref=main")
    if not meta or "sha" not in meta:
        print("skip missing", path)
        continue
    api(
        "DELETE",
        f"{base}/{path}",
        {
            "message": f"Remove one-shot Tanba helper after gate landed: {path}",
            "sha": meta["sha"],
            "branch": "main",
        },
    )
    print("deleted", path)

readme = """# Tanba day-batch gate (wired 2026-09-23)

Emma: QuickStatements must not edit Tanba people. **Drop matching lines entirely** —
never leave them as `#`-prefixed CREATE/LAST/Q comments or annotate walls.

## Live on main
- `scripts/tanba_batch_block.py` — roster-backed denylist
- `scripts/build-garborg-day.py` drops ANY line with `tanba` / Tanba QIDs **including comments**
- `usable()` rejects relative names with NN as a token (`Margreta NN`)
- `scripts/tanba-day-gate.patch` — the applied unified diff
- `scripts/install_tanba_day_gate.py` — prefers import of `tanba_blocked_qids`
"""
path = "scripts/README-tanba-fix.md"
meta = api("GET", f"{base}/{path}?ref=main")
body = {
    "message": "Document Tanba day-batch composer gate on main",
    "content": base64.b64encode(readme.encode()).decode("ascii"),
    "branch": "main",
}
if meta and "sha" in meta:
    body["sha"] = meta["sha"]
api("PUT", f"{base}/{path}", body)
print("wrote", path)
