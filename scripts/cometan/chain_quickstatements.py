# Cometan's chains, the daily run (Emma, 2026-11-26: "we're intended to be like, essentially, a daily run of Comiton
# edits"; "there should be only one batch at all that's ever published"). Moved here from Emma's inochi-no-michikyo repo
# with his tree (targets/brandon-reese-taylor). Chains from his relatives on Wikidata down to Cometan (Q142094657): each
# day's ring creates the next person on each chain, linked to an item that already exists; living people are never
# created. Daily, by .github/workflows/cometan-daily.yml:
#   1. each chain's next person is looked up on Wikidata by FamilySearch id (haswbstatement:P2889); a hit goes into the
#      ledger reports/cometan/chain-qids.tsv, so the chain advances once a batch has been run, with no hand step;
#   2. the reverse links between people who both have items are written with Q numbers. NEVER LAST after a line naming
#      another item: QuickStatements' new server moves LAST on every command (inochi-no-michikyo research/last-explained.md);
#   3. reports/wikidata-cometan-day.txt = reports/wikidata-corrections.txt (on top) + the day's ring, no comment lines:
#      the one batch published at genealogy.order.life.
#   4. nobody is created without a FamilySearch or Geni id: the chain stops at such a person;
#   5. every statement but P31 cites the person's Geni (S2600) and FamilySearch (S2889) ids, as Garborg does.
#   PYTHONPATH= python scripts/cometan/chain_quickstatements.py
import csv, datetime, os, re, runpy

G = runpy.run_path("scripts/cometan/synoptic.py")
anc, A_par, A_ch, A_sp = G["anc"], G["A_par"], G["A_ch"], G["A_sp"]
a2f, a2g, year, TARGETS, find, path_to = G["a2f"], G["a2g"], G["year"], G["TARGETS"], G["find"], G["path_to"]
ME = G["ANC_ME"]
COMETAN_QID = "Q142094657"
THIS_YEAR = datetime.date.today().year
OUT = "reports/cometan"
LEDGER = f"{OUT}/chain-qids.tsv"

qid_of = {}   # Ancestry id -> QID, for people who already have an item
if os.path.exists(LEDGER):
    for row in csv.DictReader(open(LEDGER, encoding="utf-8"), delimiter="\t"):
        if row.get("qid", "").startswith("Q"):
            qid_of[row["ancestry"]] = row["qid"]

import json, time, urllib.parse, urllib.request
UA = {"User-Agent": "genealogy-cometan-daily/1.0 (github.com/EmmaLeonhart/genealogy; read-only lookups)"}


def wd_by_familysearch(fs_id):
    """The item carrying this FamilySearch id, if exactly one does."""
    q = urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": f"haswbstatement:P2889={fs_id}",
                                "srlimit": "2", "format": "json"})
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://www.wikidata.org/w/api.php?{q}", headers=UA), timeout=60))
    except Exception:
        return None
    hits = [h["title"] for h in r.get("query", {}).get("search", [])]
    return hits[0] if len(hits) == 1 else None


def living(i):
    p = anc[i]
    if p["dt"]:
        return False
    by = year(p["bt"])
    return by is None or by > THIS_YEAR - 100   # no dates at all: treated as possibly living

def rel(x, y):
    """y's relation to x: father, mother, child or spouse."""
    if A_par[x]["F"] == y: return "father"
    if A_par[x]["M"] == y: return "mother"
    if y in A_ch[x]: return "child"
    if y in A_sp[x]: return "spouse"
    return "?"

PROP = {"father": "P22", "mother": "P25", "child": "P40", "spouse": "P26"}

def qs_date(s):
    y = year(s)
    return f"+{y:04d}-00-00T00:00:00Z/9" if y else None

# The standard description, as scripts/build-garborg-day.py's life_description writes it (Emma, 2026-11-28: "Give
# actual standardized descriptions"; 2026-09-19: "($DATE_OF_BIRTH - $DATE_OF_DEATH) should be the descriptions we make
# on individuals. Include the gedcom qualifiers"): `11 May 1783 Eccleston, Lancashire, England, United Kingdom - 17 Aug
# 1841 Zarahelma, ...`, `born circa 1415 Sizergh Castle, ...`, `died 1758`. Qualifiers written out (ABT and Ancestry's
# "Abt."/"About" -> circa), the raw place string, no relationship phrase, at most 240 characters.
MONTHS = {m.upper(): m for m in ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")}
QUAL = {"ABT": "circa", "ABOUT": "circa", "C": "circa", "CA": "circa", "CIRCA": "circa", "AFT": "Aft", "AFTER": "Aft",
        "BEF": "Bef", "BEFORE": "Bef", "EST": "Est", "CAL": "Cal", "BET": "Bet", "AND": "and", "FROM": "From", "TO": "to"}
def desc_date(s):
    s = re.sub(r"-00-00\b|-00\b", "", (s or "").replace(":", " "))          # Ancestry's "About:1510-00-00"
    s = re.sub(r"^[cC](?=\d)", "c ", s.strip())                              # "c1480"
    out = []
    for tok in s.split():
        t = tok.rstrip(".").upper()
        if t in ("UNKNOWN", "DECEASED"): return ""
        out.append(QUAL.get(t) or MONTHS.get(t[:3] if t[:3] in MONTHS and t.isalpha() else t) or tok)
    return " ".join(out)
PLACE_RELATION_RE = re.compile(r"[\s,;-]*(?:\?\s*)?\b(?:son|daughter|child|father|mother|wife|husband|spouse|brother|"
                               r"sister|widow|widower)\s+(?:of|av|til|till)\b.*$", re.I)
def life_description(p):
    def side(d, pl):
        pl = PLACE_RELATION_RE.split(" ".join((pl or "").split()), 1)[0].rstrip(" -,;?.")
        pl = ", ".join(x.strip() for x in pl.split(",") if x.strip())       # "Yorkshire, , England"
        return " ".join(x for x in (desc_date(d), pl) if x)
    born, died = side(p["bt"], p.get("bp")), side(p["dt"], p.get("dp"))
    out = f"{born} - {died}" if born and died else f"born {born}" if born else f"died {died}" if died else ""
    return out[:240].rstrip(" -,")

def ref(i):
    """The citation for a statement about i: its Geni id (S2600) and FamilySearch id (S2889), as the Garborg generator
    cites (scripts/build-garborg-day.py). External ids are what becomes the citation (2026-11-27)."""
    return (f'\tS2600\t"{a2g[i]}"' if i in a2g else "") + (f'\tS2889\t"{a2f[i]}"' if i in a2f else "")


def creation(i, link_prop, link_qid, comment):
    p = anc[i]
    r = ref(i)
    assert r, f"{i} has no external id: never created"
    lines = [f"# {comment}", "CREATE", f'LAST\tLen\t"{p["name"]}"', "LAST\tP31\tQ5"]
    desc = life_description(p)
    if desc:
        lines.append(f'LAST\tDen\t"{desc}"')
    if p["sex"] in ("M", "F"):
        lines.append(f"LAST\tP21\t{'Q6581097' if p['sex'] == 'M' else 'Q6581072'}{r}")
    for prop, s in (("P569", p["bt"]), ("P570", p["dt"])):
        d = qs_date(s)
        if d: lines.append(f"LAST\t{prop}\t{d}{r}")
    if i in a2f: lines.append(f'LAST\tP2889\t"{a2f[i]}"')
    if i in a2g: lines.append(f'LAST\tP2600\t"{a2g[i]}"')
    lines.append(f"LAST\t{link_prop}\t{link_qid}{r}")
    return lines

# every relative with an item is known on every chain, and nobody is created twice
target_qid = {}
for qid, label_, pre, y, why in TARGETS:
    t = find(pre, y)
    if t:
        target_qid[t] = qid
created = set()
new_ledger, back = [], []

plan, batch = [], ["# Cometan chains, today's ring. Each item is created linked to an item that already exists;",
                   "# the reverse links and the next ring come in the next batch, once these QIDs are in the ledger."]
for qid, label_, pre, y, why in TARGETS:
    t = find(pre, y)
    p = path_to(t) if t else None
    if not p:
        continue
    chain = p[::-1]                      # relative ... Cometan
    known = {chain[0]: qid, ME: COMETAN_QID}
    known.update({i: q for i, q in target_qid.items() if i in chain})
    known.update({i: q for i, q in qid_of.items() if i in chain})
    for i in chain:                      # the chain's next unknown person: created yet?
        if i not in known and i in a2f:
            q = wd_by_familysearch(a2f[i]); time.sleep(1)
            if q:
                known[i] = qid_of[i] = q
                new_ledger.append((i, q, anc[i]["name"]))
                continue
            break
    for k in range(1, len(chain)):       # reverse links between neighbours that both have items, Q numbers only
        a, b = chain[k - 1], chain[k]
        if a in known and b in known and known[a] != known[b]:
            r = rel(a, b)                # b's relation to a
            inv = {"father": "child", "mother": "child", "spouse": "spouse"}.get(r) or                   ({"M": "father", "F": "mother"}.get(anc[a]["sex"]) if r == "child" else None)
            src = ref(b) or ref(a)       # cited to the newer end's record, else the older's; never uncited
            if not src:
                continue
            if r in PROP: back.append(f"{known[a]}\t{PROP[r]}\t{known[b]}{src}")
            if inv in PROP: back.append(f"{known[b]}\t{PROP[inv]}\t{known[a]}{src}")
    stop = None
    for k, i in enumerate(chain):
        status = ("has item " + known[i]) if i in known else ("living: not created" if living(i) else
                  "to create" if (i in a2f or i in a2g) else "no FamilySearch or Geni id: not created")
        if status.startswith("living") and stop is None and i != ME:
            stop = k
        plan.append({"relative": label_, "relative_qid": qid, "step": k, "ancestry": i, "name": anc[i]["name"],
                     "born": year(anc[i]["bt"]) or "", "died": year(anc[i]["dt"]) or "",
                     "familysearch": a2f.get(i, ""), "geni": a2g.get(i, ""),
                     "relation_to_previous": "" if k == 0 else rel(chain[k - 1], i), "status": status})
    # today's ring: the first person without an item, next to one who has an item, before any living person
    end = stop if stop is not None else len(chain) - 1
    for k in range(1, end + 1):
        i, prev = chain[k], chain[k - 1]
        if i in known:
            continue
        if i in created:
            break
        # Nobody is created without an external identifier (Emma, 2026-11-27, of Thomas Moon, Hannah Moon and others
        # created "with no external identifiers whatsoever": "It's kind of baffling that you are doing that."): a person
        # with neither a FamilySearch nor a Geni id is not created, and the chain waits there.
        if prev in known and not living(i) and (i in a2f or i in a2g):
            r = rel(i, prev)             # prev's relation to i, stated on the new item i
            if r in PROP:
                created.add(i)
                batch += creation(i, PROP[r], known[prev], f"{label_} chain, step {k}: {anc[i]['name']}, "
                                                            f"{r} is {anc[prev]['name']} ({known[prev]})")
        break
    # once the chain is created down to the living gap, link Cometan to the nearest dead ancestor on it
    if stop is not None and stop > 0 and chain[stop - 1] in known:
        anc_q = known[chain[stop - 1]]
        batch += [f"# {label_} chain: living gap after {anc[chain[stop - 1]]['name']}; Cometan linked as a relative",
                  f"{COMETAN_QID}\tP1038\t{anc_q}"]

with open(f"{OUT}/chains.tsv", "w", encoding="utf-8", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=list(plan[0]), delimiter="\t")
    w.writeheader(); w.writerows(plan)
if not os.path.exists(LEDGER):
    open(LEDGER, "w", encoding="utf-8", newline="\n").write("ancestry\tqid\tname\n")
with open(LEDGER, "a", encoding="utf-8", newline="\n") as fh:
    for row in new_ledger:
        fh.write("\t".join(row) + "\n")
back = list(dict.fromkeys(back))
ring = [l for l in batch if l.strip() and not l.lstrip().startswith("#")]
fix = "reports/wikidata-corrections.txt"
top = [l for l in open(fix, encoding="utf-8").read().splitlines() if l.strip()] if os.path.exists(fix) else []
open("reports/wikidata-cometan-day.txt", "w", encoding="utf-8", newline="\n").write("\n".join(top + back + ring) + "\n")
print(f"{len(plan)} chain rows; {len(new_ledger)} found on Wikidata today; {len(back)} reverse links; "
      f"{sum(1 for l in ring if l == 'CREATE')} creations; {len(top)} correction lines on top")
