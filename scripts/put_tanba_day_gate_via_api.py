import base64, json, os, urllib.request, urllib.error, time

owner, repo = os.environ["OWNER"], os.environ["REPO"]
path = "scripts/build-garborg-day.py"
content = open(path, "rb").read()
token = os.environ["GH_TOKEN"]

def put(sha):
    body = {
        "message": (
            "Wire Tanba day-batch gate: drop Tanba lines entirely; never comment them out\n\n"
            "Apply scripts/tanba-day-gate.patch to build-garborg-day.py via Contents API "
            "(no full checkout). tanba_batch_block.tanba_blocked_qids wired into excluded; "
            "names_excluded drops ANY line with tanba/Tanba QIDs including annotation "
            "comments. Given-NN usable() token fix included."
        ),
        "content": base64.b64encode(content).decode("ascii"),
        "sha": sha,
        "branch": "main",
    }
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
        data=json.dumps(body).encode(),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

sha = os.environ["FILE_SHA"]
data = None
for attempt in range(3):
    try:
        data = put(sha)
        break
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        print("PUT failed", e.code, raw[:800])
        if e.code != 409 or attempt == 2:
            raise
        meta_req = urllib.request.Request(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref=main",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(meta_req) as resp:
            sha = json.load(resp)["sha"]
        time.sleep(2)

print("commit", data["commit"]["sha"])
print("blob", data["content"]["sha"])
print("html", data["commit"]["html_url"])
open("gate-commit-sha.txt", "w").write(data["commit"]["sha"])
