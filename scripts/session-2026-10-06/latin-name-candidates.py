"""For each token in `reports/name-links-wrong-script-2026-10-06.tsv`, the Latin-script name items of the same
usage on Wikidata whose `mul` or `en` label is exactly the token (live SPARQL). Writes
`reports/name-links-latin-candidates-2026-10-06.tsv`.

    python scripts/session-2026-10-06/latin-name-candidates.py
"""
import csv, json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-audit (https://github.com/EmmaLeonhart/genealogy)",
      "Accept": "application/sparql-results+json"}
CLASSES = {"given": "wd:Q202444 wd:Q12308941 wd:Q11879590 wd:Q3409032",
           "family": "wd:Q101352", "patronymic": "wd:Q110874"}

rows = list(csv.DictReader(open(ROOT / "reports/name-links-wrong-script-2026-10-06.tsv", encoding="utf-8"),
                           delimiter="\t"))
out = []
for r in rows:
    tok = r["token"].replace("\\", "\\\\").replace('"', '\\"')
    q = f'''SELECT DISTINCT ?item ?mul ?en (GROUP_CONCAT(DISTINCT ?ws) AS ?p282) (GROUP_CONCAT(DISTINCT ?c) AS ?cls) WHERE {{
      VALUES ?c {{ {CLASSES[r["usage"]]} }}
      {{ ?item rdfs:label "{tok}"@mul }} UNION {{ ?item rdfs:label "{tok}"@en }}
      ?item wdt:P31 ?c .
      OPTIONAL {{ ?item rdfs:label ?mul FILTER(LANG(?mul)="mul") }}
      OPTIONAL {{ ?item rdfs:label ?en FILTER(LANG(?en)="en") }}
      OPTIONAL {{ ?item wdt:P282 ?ws }}
    }} GROUP BY ?item ?mul ?en'''
    data = {}
    for _ in range(4):
        try:
            data = json.load(urllib.request.urlopen(urllib.request.Request(
                "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q}), headers=UA), timeout=90))
            break
        except Exception:                                            # noqa: BLE001
            time.sleep(10)
    cands = []
    for b in data.get("results", {}).get("bindings", []):
        qid = b["item"]["value"].rsplit("/", 1)[1]
        if qid == r["linked_qid"]:
            continue
        ws = " ".join(x.rsplit("/", 1)[1] for x in b.get("p282", {}).get("value", "").split())
        cands.append(f'{qid}[mul={b.get("mul", {}).get("value", "")};P282={ws}]')
    out.append([r["token"], r["usage"], r["bearers"], r["linked_qid"], r["mul"], r["P282"], " ".join(cands)])
    time.sleep(1)
with open(ROOT / "reports/name-links-latin-candidates-2026-10-06.tsv", "w", encoding="utf-8", newline="") as f:
    f.write("token\tusage\tbearers\tlinked_qid\tlinked_mul\tlinked_P282\tcandidates\n")
    for x in out:
        f.write("\t".join(x) + "\n")
print(len(out), "tokens;", sum(1 for x in out if x[6]), "with a candidate")
