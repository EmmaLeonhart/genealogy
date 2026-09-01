"""The full Samaritan high-priest succession, from the English Wikipedia list.

    python scripts/fetch-samaritan-succession.py

**Emma, 2026-08-31**, asked which source she meant for the Samaritans and answering *the English
Wikipedia list*: `Samaritan High Priest`, which `List of Samaritan High Priests` redirects to. It
carries **133 numbered rows**, 1 to 133, which is the whole line from `Sashai ben Abishua` to
`Aabed-El V ben Asher ben Matzliach`.

**Why it is the easy source, having tried three that were not:**

- `wdt:P39 wd:Q678510` returns **7 items**. That is the very inconsistency her `samaritans/
  wikidata.txt` describes -- *"it doesn't even say who is the Samaritan high priest... they're
  not very well documented"* -- so the office property cannot enumerate the office.
- `samaritans/wikidata.txt` is her dictation about the work, not a list.
- `samaritans/The Samaritan Update.html` covers the **modern line only**, 20 priests. Useful for
  a different reason: its own prose says *"the 132nd High Priest since Aaron... for 112
  generations the high priesthood was inherited... till 1624 CE"*, which independently confirms
  the **offset of 112** between that table's local numbering and the absolute count, derived
  earlier from four rows of `reports/wikidata-samaritan-succession.json`.

**The link target is the QID route.** Each row is a wiki-link, and a title resolves to an item
through `wbgetentities` with `sites=enwiki` -- an exact sitelink lookup, never a name search. That
is what closes the QID gap the other sources could not.

**A row may carry two names**: `Elazar ben Tsedaka ben Yitzhaq|Elazar XX ben Tsedaka ben Yitzhaq`
is a link target and a display form. The display form is the one carrying the regnal ordinal, so
both are kept.

Writes `reports/samaritan-succession-list.tsv`.
"""

import io
import json
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from genimerge.wikidata import _http_fetch, require_agent          # noqa: E402

OUT = ROOT / "reports" / "samaritan-succession-list.tsv"
PAGE = "List of Samaritan High Priests"


def main():
    ua = {"User-Agent": require_agent()}
    url = ("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions"
           "&rvprop=content&rvslots=main&redirects=1&titles=" + urllib.parse.quote(PAGE))
    data = json.loads(_http_fetch(url, headers=ua))["query"]
    page = next(iter(data["pages"].values()))
    if "missing" in page:
        sys.exit("page missing: %s" % PAGE)
    text = page["revisions"][0]["slots"]["main"]["*"]
    print("%s: %d chars" % (page["title"], len(text)))

    rows = []
    for n, rest in re.findall(r"\|\s*(\d{1,3})\s*\n\|\s*(.+)", text):
        rest = rest.strip()
        # `[[Target|Display]]` -- the display half is where the regnal ordinal lives.
        link = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", rest)
        target = link.group(1).strip() if link else ""
        display = (link.group(2) or link.group(1)).strip() if link else \
            re.sub(r"[\[\]]", "", rest)
        rows.append({"number": int(n), "title": target, "name": display, "qid": ""})
    print("%d numbered rows, %d..%d" % (len(rows), rows[0]["number"], rows[-1]["number"]))

    # ---- titles -> QIDs by SITELINK, which is exact ----------------------------------
    titles = sorted({r["title"] for r in rows if r["title"]})
    qid_by_title = {}
    for k in range(0, len(titles), 50):
        chunk = titles[k:k + 50]
        u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
             "&sites=enwiki&props=sitelinks&titles=" + urllib.parse.quote("|".join(chunk)))
        for qid, v in json.loads(_http_fetch(u, headers=ua)).get("entities", {}).items():
            if not qid.startswith("Q"):
                continue
            sl = (v.get("sitelinks") or {}).get("enwiki", {}).get("title")
            if sl:
                qid_by_title[sl] = qid
    for r in rows:
        r["qid"] = qid_by_title.get(r["title"], "")

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write("number\ttitle\tname\tqid\n")
        for r in rows:
            fh.write("%d\t%s\t%s\t%s\n" % (r["number"], r["title"], r["name"], r["qid"]))
    print("%d of %d resolved to a QID -> %s"
          % (sum(1 for r in rows if r["qid"]), len(rows), OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
