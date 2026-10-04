"""Three-batch pipeline for putting the Ono Inbe pedigree on Wikidata
(QuickStatements 3.0, V1 syntax). Nothing here edits Wikidata: it writes
batches for the user to review and run, and looks up what earlier batches
created with SPARQL. See research/notes/wikidata-import-plan.md.

  python genealogy/ono_wikidata_pipeline.py batch1
      -> genealogy/wikidata/batch1_source.qs   (create the source item)
  python genealogy/ono_wikidata_pipeline.py batch2
      finds the source item (P9836 = 2538213), then
      -> genealogy/wikidata/batch2_people.qs   (create people, unlinked)
  python genealogy/ono_wikidata_pipeline.py batch3
      finds everyone via P1343 = source with qualifier P1545 = pedigree id, then
      -> genealogy/wikidata/batch3_links.qs    (cited family links)

Every claim except the dates cites the source item. Dates are estimates from
the pedigree's own reign placements (make_ono_gedcom.DATES), entered at decade
precision as circa, with deprecated rank and a reason.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_ono_gedcom as g  # noqa: E402

OUT = HERE / "wikidata"
NDL_PID = "2538213"
NDL = f"https://dl.ndl.go.jp/pid/{NDL_PID}"

# Verified on Wikidata 2026-10-03.
MANUSCRIPT, FAMILY_TREE = "Q87167", "Q189977"
LEGENDARY, KAMI = "Q13002315", "Q524158"
MALE, FEMALE = "Q6581097", "Q6581072"
CIRCA = "Q5727902"
CANNOT_CONFIRM = "Q25895909"   # reason for deprecated rank: cannot be confirmed by other sources
ALLEGEDLY, DISPUTED = "Q32188232", "Q18912752"
SUZUKI, KOSUGI, JAPANESE = "Q6536470", "Q6536257", "Q5287"

# Labels (user, 2026-10-03): the characters in Japanese and Chinese; the
# romanised name in English, multilingual, French, Indonesian and Spanish.
# No Korean label.
CJK_LANGS = ("ja", "zh")
ROMAN_LANGS = ("en", "mul", "fr", "id", "es")

GODS = {"1", "2", "W2", "3", "4", "5"}|{f"H{i}" for i in range(1, 11)}
REAL = {"21", "21b"}  # real people (Kobito, Shikobuchi); linked like everyone else


def sparql(query):
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode(
        {"query": query, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": "INBE-research/0.1"})
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))["results"]["bindings"]
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5)


SOURCE_QID = "Q141627872"  # created by the user 2026-10-03


def find_source():
    return SOURCE_QID


def find_source_sparql():
    rows = sparql(f'SELECT ?s WHERE {{ ?s wdt:P9836 "{NDL_PID}" ; wdt:P31 wd:{MANUSCRIPT} . }}')
    qids = sorted({r["s"]["value"].rsplit("/", 1)[1] for r in rows})
    if len(qids) != 1:
        sys.exit(f"Expected one source item with P9836={NDL_PID}, found {qids}. Run batch 1 first.")
    return qids[0]


def frame(key):
    return g.by_seq.get(key, {}).get("ndl_image", "")


def cite(src, key):
    """Reference: stated in the source, frame number, and a direct frame URL."""
    f = frame(key)
    ref = f"|S248|{src}"
    if f:
        ref += f'|S958|"NDL frame {f}"|S854|"{NDL}/1/{f}"'
    return ref


def wd_date(y):
    return f"{'-' if y < 0 else '+'}{abs(y):04d}-00-00T00:00:00Z/8"  # decade precision


def write(name, lines):
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    lines = [l for l in lines if not l.startswith("/*")]  # plain QuickStatements: no comment lines
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {path} ({sum(1 for l in lines if l and l != 'CREATE')} commands)")


def batch1():
    write("batch1_source.qs", [
        "CREATE",
        'LAST|Len|"Inbe no Sukune honkeichō"',
        'LAST|Lja|"斎部宿禰本系帳"',
        'LAST|Den|"1870 genealogy of the Ono family, claimed descendants of the Inbe clan; judged a forgery in 1876"',
        'LAST|Dja|"小野家の斎部氏系譜（明治3年）。明治9年に小杉榲邨が偽作と判定"',
        f"LAST|P31|{MANUSCRIPT}",
        f"LAST|P31|{FAMILY_TREE}",
        f"LAST|P407|{JAPANESE}",
        f'LAST|P9836|"{NDL_PID}"|P958|"NDL frames 50-73 of the bound volume"',
        f"LAST|P571|+1870-00-00T00:00:00Z/9|P1480|{CIRCA}",
        f"LAST|P50|{SUZUKI}|P1480|{ALLEGEDLY}|P1310|{KOSUGI}|S854|\"{NDL}/1/50\"",
    ])


def batch2():
    src = find_source()
    lines = [f"/* source item: {src} */"]
    for key, p in g.people.items():
        ordinal = f'|P1545|"{key}"'
        if key in g.WIKIDATA:  # already on Wikidata: just attach the source
            lines.append(f"{g.WIKIDATA[key]}|P1343|{src}{ordinal}{cite(src, key)}")
            continue
        en = g.EN[key].rstrip("?")
        alias = ""
        if " (" in en:  # "Tanate (Takenadeko)": label + alias
            en, alias = en.rstrip(")").split(" (", 1)
        lines.append("CREATE")
        lines += [f'LAST|L{lang}|"{p["name"]}"' for lang in CJK_LANGS]
        lines += [f'LAST|L{lang}|"{en}"' for lang in ROMAN_LANGS]
        if alias:
            lines.append(f'LAST|Aen|"{alias}"')
        lines += [
            'LAST|Den|"figure in the 1870 Ono family Inbe pedigree"',
            f"LAST|P31|{KAMI if key in GODS else LEGENDARY}{cite(src, key)}",
            f"LAST|P21|{FEMALE if key in g.FEMALE else MALE}{cite(src, key)}",
            f"LAST|P1343|{src}{ordinal}{cite(src, key)}",
        ]
    write("batch2_people.qs", lines)


def dates(q):
    """Estimated dates for the deprecated-rank step. Standard QuickStatements
    (quickstatements.toolforge.org) cannot set rank, so these are kept apart."""
    lines = ["/* estimated dates: circa, decade precision, to be given deprecated rank */"]
    for key in g.people:
        if key in g.DATES and key not in g.WIKIDATA:
            b, d, _basis = g.DATES[key]
            for prop, y in (("P569", b), ("P570", d)):
                lines.append(f"{q[key]}|{prop}|{wd_date(y)}|P1480|{CIRCA}|P2241|{CANNOT_CONFIRM}")
    write("batch4_dates_to_deprecate.qs", lines)


def batch3(link_real=True):
    src = find_source()
    rows = sparql(f"""SELECT ?item ?ord WHERE {{
      ?item p:P1343 ?st . ?st ps:P1343 wd:{src} ; pq:P1545 ?ord . }}""")
    q = {r["ord"]["value"]: r["item"]["value"].rsplit("/", 1)[1] for r in rows}
    missing = [k for k in g.people if k not in q]
    if missing:
        sys.exit(f"Not found yet (run batch 2 first, or wait for the query service): {missing}")
    lines = [f"/* source item: {src}; disputed family links, cited to it */"]

    def dq(a, b):
        # Between two items that existed before this import, the claim may already
        # be on Wikidata from other sources: add the citation only, not "disputed".
        return "" if a in g.WIKIDATA and b in g.WIKIDATA else f"|P1480|{DISPUTED}"

    for (father, mother), kids in g.families.items():
        for kid in kids:
            if kid in REAL and not link_real:
                lines.append(f"/* skipped parents of real person {g.EN[kid]} (use --link-real) */")
                continue
            for par, prop in ((father, "P22"), (mother, "P25")):
                if par:
                    lines.append(f"{q[kid]}|{prop}|{q[par]}{dq(kid, par)}{cite(src, kid)}")
                    lines.append(f"{q[par]}|P40|{q[kid]}{dq(kid, par)}{cite(src, kid)}")
        if father and mother:
            lines.append(f"{q[father]}|P26|{q[mother]}{dq(father, mother)}{cite(src, mother)}")
            lines.append(f"{q[mother]}|P26|{q[father]}{dq(father, mother)}{cite(src, mother)}")
    write("batch3_links.qs", lines)
    dates(q)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "batch1":
        batch1()
    elif step == "batch2":
        batch2()
    elif step == "batch3":
        batch3(link_real="--no-link-real" not in sys.argv)
    else:
        sys.exit(__doc__)
