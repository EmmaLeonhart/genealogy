"""The merges page — one card per pair, worked from the browser instead of the markdown.

    py scripts/build-merges-page.py [--offline]

**Emma, 2026-09-01:** *"merges put them at the end of the queue with an html page for them"*, and
then on 2026-09-02, asked whether to build it: *"Build it from the template"*.

**Why a page at all, measured rather than assumed:** she cleared **207 pairs in one sitting** off
the parent-adjudication deck and had answered **none** off the equivalent TSV. The markdown
`reports/merges-to-do.md` is 8 sections she reads by hand; this is the same content as cards.

## Built FROM her template, not from scratch

`out/parent-review.template.html` is hers and hand-approved. Rebuilding a page from scratch
instead of reusing it was a mistake she named: *"did you regenerate it from scratch instead of
using the template you used yesterday lol"*. So the palette, the three-state theme handling, the
IBM Plex / Newsreader pairing, the keyboard flow and the `localStorage` key are taken from it.

## The card carries what actually decides a merge

Her verdict on the first deck was *"the problem with that html is it didn't give that good
feedback"*, and the queue item spells out the fix: a card without **sex and dates** is not worth
building. So each side shows label, description, sitelink count, statement count, and the Geni
`P2600` — and the Geni tree's own sex and birth–death sit above them, from `derived-facts.csv`.

**The live fetch is the point.** She merges by hand continuously, so a pair may already be done by
the time she opens the page. `wbgetentities` in batches of 50 answers that: an item that is now a
**redirect** is shown as already merged and is not offered again. `--offline` skips the fetch and
builds the page from the markdown alone, with the evidence columns blank.

**Nothing here performs a merge.** The action is a prefilled `Special:MergeItems` link in the
direction `Help:Merge` wants — the lower Q number survives — and a keypress that records a
decision locally.

Writes `out/merges.html`.
"""
from __future__ import annotations

import argparse
import collections
import csv
import html
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

MD = ROOT / "reports" / "merges-to-do.md"
FACTS = ROOT / "reports" / "derived-facts.csv"
TEMPLATE = ROOT / "out" / "parent-review.template.html"
OUT = ROOT / "out" / "merges.html"

API = "https://www.wikidata.org/w/api.php"
AGENT = "genimerge merges page (emma@topazcomputing.com)"

NAME_RE = re.compile(r"^- \*\*(.+?)\*\*(?:\s*-\s*Geni `(\d+)`)?")
MERGE_RE = re.compile(r"merge \*\*(Q\d+)\*\* into \*\*(Q\d+)\*\*")


def pairs_from_markdown():
    """`[(section, name, geni_id, from_qid, to_qid)]` in file order."""
    section, current, out = None, None, []
    for line in io.open(MD, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = NAME_RE.match(line)
        if m:
            current = (m.group(1), m.group(2) or "")
            continue
        mm = MERGE_RE.search(line)
        if mm and current:
            out.append((section, current[0], current[1], mm.group(1), mm.group(2)))
    return out


def geni_facts(ids):
    """`{geni_id: (sex, birth, death)}` from the merged tree."""
    out = {}
    if not FACTS.exists():
        return out
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r.get("geni_id")
            if g in ids:
                out[g] = (r.get("sex", ""), (r.get("birth_date_iso") or "")[:10],
                          (r.get("death_date_iso") or "")[:10])
    return out


def fetch_items(qids):
    """`{qid: {...}}` with the few fields a card needs, plus redirect detection.

    `wbgetentities` takes 50 ids a call, which `CLAUDE.md` § *Querying Wikidata is ALLOWED* names
    as the polite shape. Only the summary fields are kept -- but they are read off the **full
    entity**, never a summarising channel, which is the distinction § *A SUMMARY of a Wikidata
    item is not the item* draws.
    """
    out = {}
    qids = sorted(set(qids))
    for i in range(0, len(qids), 50):
        chunk = qids[i:i + 50]
        q = urllib.parse.urlencode({
            "action": "wbgetentities", "ids": "|".join(chunk),
            "props": "labels|descriptions|sitelinks|claims", "languages": "en|mul",
            "format": "json"})
        req = urllib.request.Request(API + "?" + q, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(req, timeout=90) as fh:
                data = json.loads(fh.read().decode("utf-8"))
        except Exception as exc:                                       # noqa: BLE001
            print("  chunk %d failed (%s); those cards lose their evidence" % (i, exc),
                  file=sys.stderr)
            continue
        for qid, item in (data.get("entities") or {}).items():
            if "missing" in item:
                out[qid] = {"missing": True}
                continue
            labels = item.get("labels") or {}
            descs = item.get("descriptions") or {}
            claims = item.get("claims") or {}
            out[qid] = {
                "label": (labels.get("en") or labels.get("mul") or {}).get("value", ""),
                "desc": (descs.get("en") or {}).get("value", ""),
                "sitelinks": len(item.get("sitelinks") or {}),
                "statements": sum(len(v) for v in claims.values()),
                "properties": len(claims),
                "p2600": [s.get("mainsnak", {}).get("datavalue", {}).get("value")
                          for s in claims.get("P2600", [])],
                # A redirected id comes back under its TARGET's id, so an id we asked for and
                # did not get back at its own key has already been merged away.
                "id": item.get("id", qid),
            }
        time.sleep(0.3)
    return out


def esc(s):
    return html.escape(str(s or ""), quote=True)


def style_from_template():
    """Her palette and type, lifted verbatim from the approved template."""
    if not TEMPLATE.exists():
        return ""
    text = io.open(TEMPLATE, encoding="utf-8").read()
    a = text.find("<link rel=\"stylesheet\"")
    b = text.find("</style>")
    return text[a:b + len("</style>")] if a >= 0 and b > a else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true",
                    help="skip the Wikidata fetch; evidence columns stay blank")
    args = ap.parse_args()

    if not MD.exists():
        print("no %s; run scripts/build-merges-to-do.py first" % MD.relative_to(ROOT),
              file=sys.stderr)
        return 1
    pairs = pairs_from_markdown()
    print("%d merge pairs over %d sections"
          % (len(pairs), len({p[0] for p in pairs})))

    facts = geni_facts({p[2] for p in pairs if p[2]})
    print("%d of them have sex/dates in the tree" % len(facts))

    items = {}
    if not args.offline:
        want = {q for p in pairs for q in (p[3], p[4])}
        print("fetching %d items from Wikidata, 50 at a time" % len(want))
        items = fetch_items(want)
        got = sum(1 for v in items.values() if not v.get("missing"))
        print("   %d returned, %d missing or redirected" % (got, len(want) - got))

    by_section = collections.OrderedDict()
    for p in pairs:
        by_section.setdefault(p[0], []).append(p)

    done = 0
    cards = []
    for section, rows in by_section.items():
        cards.append('<h2 class="sec">%s</h2>' % esc(section))
        for _s, name, geni, frm, to in rows:
            a, b = items.get(frm, {}), items.get(to, {})
            # An id absent from the response, or returned under a different id, is already merged.
            already = bool(items) and (frm not in items or a.get("id", frm) != frm
                                       or a.get("missing"))
            if already:
                done += 1
            sex, born, died = facts.get(geni, ("", "", ""))
            life = " – ".join(x for x in (born, died) if x) or "no dates in the tree"
            sexlab = {"M": "male", "F": "female"}.get(sex, "sex not recorded")

            def side(qid, d, role):
                if not d or d.get("missing"):
                    return ('<div class="side"><div class="q">%s</div>'
                            '<div class="mut">%s</div></div>'
                            % (esc(qid), "already merged away" if items else "not fetched"))
                return ('<div class="side"><div class="q">%s <span class="role">%s</span></div>'
                        '<div class="lab">%s</div><div class="mut">%s</div>'
                        '<div class="nums"><b>%d</b> sitelinks · <b>%d</b> statements ·'
                        ' <b>%d</b> properties%s</div></div>'
                        % (esc(qid), role, esc(d.get("label") or "(no label)"),
                           esc(d.get("desc") or ""), d.get("sitelinks", 0),
                           d.get("statements", 0), d.get("properties", 0),
                           " · P2600 " + esc(", ".join(x for x in d.get("p2600") or [] if x))
                           if d.get("p2600") else ""))

            link = ("https://www.wikidata.org/wiki/Special:MergeItems?from=%s&to=%s"
                    % (frm, to))
            cards.append(
                '<article class="card%s" data-id="%s">'
                '<div class="hd"><h3>%s</h3>%s</div>'
                '<div class="meta">%s · %s%s</div>'
                '<div class="sides">%s<div class="arrow">→</div>%s</div>'
                '<div class="act"><a class="go" href="%s" target="_blank" rel="noopener">'
                'Merge %s into %s</a>'
                '<button class="mark" data-v="done">done <kbd>d</kbd></button>'
                '<button class="mark" data-v="skip">skip <kbd>s</kbd></button></div>'
                '</article>'
                % (" is-done" if already else "", esc(frm + "-" + to), esc(name),
                   '<span class="pill">already merged</span>' if already else "",
                   esc(sexlab), esc(life),
                   (' · Geni <a href="https://www.geni.com/people/x/%s" target="_blank"'
                    ' rel="noopener">%s</a>' % (esc(geni), esc(geni))) if geni else "",
                   side(frm, a, "merge away"), side(to, b, "keep"),
                   esc(link), esc(frm), esc(to)))

    page = """%s
<style>
.sec{font:600 13px/1 "IBM Plex Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);margin:30px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;margin:0 0 12px}
.card.is-done{opacity:.5}
.card.marked-done{border-color:var(--yes);background:var(--yes-soft)}
.card.marked-skip{border-color:var(--skip);background:var(--skip-soft)}
.hd{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.hd h3{font:600 17px/1.3 "Newsreader",Georgia,serif;margin:0}
.pill{font-size:11px;background:var(--yes-soft);color:var(--yes);border-radius:99px;
  padding:2px 9px;font-weight:600}
.meta{color:var(--muted);font-size:13px;margin:3px 0 12px}
.sides{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center}
.side{background:var(--raise);border-radius:9px;padding:11px 13px;min-width:0}
.q{font:500 13px/1 "IBM Plex Mono",monospace;margin-bottom:5px}
.role{color:var(--muted);font-family:"IBM Plex Sans",sans-serif;font-size:11px;
  text-transform:uppercase;letter-spacing:.06em;margin-left:5px}
.lab{font-weight:600;font-size:14px;overflow-wrap:anywhere}
.mut{color:var(--muted);font-size:12.5px;overflow-wrap:anywhere}
.nums{color:var(--muted);font-size:12px;margin-top:5px;font-variant-numeric:tabular-nums}
.arrow{color:var(--muted);font-size:20px}
.act{display:flex;gap:8px;align-items:center;margin-top:13px;flex-wrap:wrap}
.go{background:var(--accent);color:#fff;text-decoration:none;border-radius:8px;
  padding:8px 14px;font-size:13.5px;font-weight:500}
.mark{background:var(--raise);color:var(--ink);border:1px solid var(--line);border-radius:8px;
  padding:8px 12px;font:500 13px "IBM Plex Sans",sans-serif;cursor:pointer}
kbd{font:500 11px "IBM Plex Mono",monospace;color:var(--muted);margin-left:4px}
@media (max-width:720px){.sides{grid-template-columns:1fr;gap:8px}.arrow{display:none}}
</style>
<div class="wrap">
<header><h1>Merges to do</h1><span class="sub">%d pairs · %d already merged · nothing here
performs a merge</span></header>
<div class="bar"><i id="prog"></i></div>
%s
</div>
<script>
var KEY = "geni-merges-v1", D = {};
try { D = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { D = {}; }
var cards = [].slice.call(document.querySelectorAll(".card")), cur = 0;
function paint() {
  cards.forEach(function (c) {
    var v = D[c.dataset.id];
    c.classList.toggle("marked-done", v === "done");
    c.classList.toggle("marked-skip", v === "skip");
  });
  var n = Object.keys(D).length;
  document.getElementById("prog").style.width = (100 * n / (cards.length || 1)) + "%%";
}
function save() { try { localStorage.setItem(KEY, JSON.stringify(D)); } catch (e) {} paint(); }
document.addEventListener("click", function (e) {
  var b = e.target.closest(".mark"); if (!b) return;
  var c = b.closest(".card"); D[c.dataset.id] = b.dataset.v; save();
});
addEventListener("keydown", function (e) {
  if (e.target.tagName === "INPUT" || e.metaKey || e.ctrlKey) return;
  var c = cards[cur]; if (!c) return;
  if (e.key === "d" || e.key === "s") { D[c.dataset.id] = e.key === "d" ? "done" : "skip"; save(); }
  else if (e.key === "j" || e.key === "ArrowDown") cur = Math.min(cur + 1, cards.length - 1);
  else if (e.key === "k" || e.key === "ArrowUp") cur = Math.max(cur - 1, 0);
  else return;
  e.preventDefault();
  cards[cur].scrollIntoView({block: "center", behavior: "smooth"});
});
paint();
</script>
""" % (style_from_template(), len(pairs), done, "\n".join(cards))

    io.open(OUT, "w", encoding="utf-8", newline="").write(page)
    print("\nwrote %s - %s pairs, %d already merged"
          % (OUT.relative_to(ROOT), format(len(pairs), ","), done))
    for s, rows in by_section.items():
        print("   %-52s %3d" % (s[:52], len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
