"""The daily audit-then-run loop's sheet (Emma, 2026-10-05): the talk page, 10 random items in the
universe, 10 random creations from the batch about to run.

It only lists and fetches. Every verdict is the session's own reading of the sheet, written
underneath it in the same file; a creation or item judged wrong is fixed (or held out of the batch)
before the batch is run. Usage:

    python scripts/daily-audit-sample.py [--seed N]

Writes reports/daily-audit/<UTC date>.md and prints its path.
"""
import argparse, datetime, json, os, random, re, time, urllib.error, urllib.parse, urllib.request

UA = {"User-Agent": "genealogy-daily-audit/1.0 (emma@topazcomputing.com)"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.path.join(ROOT, "reports", "wikidata-garborg-day-manual.txt")
UNIVERSE = os.path.join(ROOT, "out", "wikidata", "edit-universe.json")
TALK = "User talk:日巫女"
PROPS = ["P31", "P21", "P569", "P570", "P22", "P25", "P26", "P40", "P3373", "P2600", "P2889"]


def api(**p):
    p["format"] = "json"
    for t in range(8):
        try:
            time.sleep(1)
            u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(p)
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))
        except urllib.error.HTTPError as x:
            if x.code != 429:
                raise
            time.sleep(30)
    raise RuntimeError("Wikidata kept answering 429")


def entities(ids):
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 50):
        out.update(api(action="wbgetentities", ids="|".join(ids[i:i + 50]),
                       props="labels|descriptions|claims", languages="mul|en|ja|zh|ko")["entities"])
    return out


def label(e):
    l = e.get("labels", {})
    for k in ("mul", "en", "ja", "zh", "ko"):
        if k in l:
            return l[k]["value"]
    return "?"


def value(v):
    if isinstance(v, dict):
        return v.get("id") or v.get("time") or json.dumps(v, ensure_ascii=False)
    return str(v)


def talk_section():
    r = api(action="query", prop="revisions", titles=TALK, rvlimit=5,
            rvprop="timestamp|user|comment", redirects=1)
    page = next(iter(r["query"]["pages"].values()))
    lines = [f"## 1. Talk page: [{TALK}](https://www.wikidata.org/wiki/{urllib.parse.quote(TALK)})", ""]
    for rv in page.get("revisions", []):
        lines.append(f"- {rv['timestamp']} {rv.get('user', '?')}: {rv.get('comment', '')}")
    if "revisions" not in page:
        lines.append("- (no revisions)")
    return lines


def item_section(rng):
    pool = json.load(open(UNIVERSE, encoding="utf-8"))["universe"]
    pick = rng.sample(pool, 10)
    E = entities(pick)
    rel = [value(c["mainsnak"].get("datavalue", {}).get("value")) for q in pick if q in E
           for p in ("P22", "P25", "P26", "P40", "P3373") for c in E[q].get("claims", {}).get(p, [])]
    R = entities([q for q in rel if re.fullmatch(r"Q\d+", q)])
    lines = ["## 2. Ten items in the universe", ""]
    for q in pick:
        e = E.get(q, {})
        if "redirect" in e or "missing" in e:
            lines.append(f"### [{q}](https://www.wikidata.org/wiki/{q}): redirect or missing")
            continue
        labs = {k: v["value"] for k, v in e.get("labels", {}).items()}
        lines += [f"### [{q}](https://www.wikidata.org/wiki/{q}) {label(e)}",
                  f"- labels: {labs}", f"- description: {e.get('descriptions', {}).get('en', {}).get('value', '')}"]
        for p in PROPS:
            for c in e.get("claims", {}).get(p, []):
                v = value(c["mainsnak"].get("datavalue", {}).get("value"))
                name = f" {label(R[v])}" if v in R else ""
                lines.append(f"- {p} {v}{name}")
        lines.append("- verdict (session): ")
    return lines


def creation_section(rng):
    rows = open(BATCH, encoding="utf-8").read().split("\n")
    blocks, cur = [], None
    for row in rows:
        if row.startswith("#") or not row.strip():
            if cur is not None and not row.strip():
                cur = None
            continue
        if row == "CREATE":
            cur = []
            blocks.append(cur)
        elif cur is not None and row.startswith("LAST\t"):
            cur.append(row)
        elif cur is not None and "\tLAST" in row:
            cur.append(row)
        else:
            cur = None
    pick = rng.sample(range(len(blocks)), min(10, len(blocks)))
    qids = {q for i in pick for row in blocks[i] for q in re.findall(r"\bQ\d+\b", row)}
    E = entities(qids)
    lines = [f"## 3. Ten creations from the batch ({len(blocks)} creations in `reports/wikidata-garborg-day-manual.txt`)", ""]
    for i in sorted(pick):
        lines.append(f"### creation {i + 1}")
        for row in blocks[i]:
            named = re.sub(r"\b(Q\d+)\b", lambda m: f"{m.group(1)} ({label(E[m.group(1)])})" if m.group(1) in E else m.group(1), row)
            lines.append("    " + named.replace("\t", "  "))
        lines.append("- verdict (session): ")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=int(time.time()))
    a = ap.parse_args()
    rng = random.Random(a.seed)
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    out = [f"# Daily audit {day} (seed {a.seed})", "",
           "Verdicts are the session's, one per check. The batch runs only when all 20 are confirmed.", ""]
    out += talk_section() + [""] + item_section(rng) + [""] + creation_section(rng) + [""]
    d = os.path.join(ROOT, "reports", "daily-audit")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{day}.md")
    if os.path.exists(path):
        path = os.path.join(d, f"{day}-{a.seed}.md")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print(path)


if __name__ == "__main__":
    main()
