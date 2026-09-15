"""Read the immediate-family CARD GRID out of the saved `geni-scraping/*.html` pages.

    python scripts/read-saved-family-cards.py            # writes the manifest and the TSV
    python scripts/read-saved-family-cards.py --sample 20

## ⛔ WHY THIS IS ALLOWED WHEN THE OLD SAVED-PAGE PARSER WAS DELETED

`scripts/build-tiny-gedcoms.py` carries: *⛔ THE SAVED-PAGE SECTIONS ARE GONE. Ruled 2026-09-10,
"structured only, delete the prose parser".* That ruling killed a reader which took an **opener
phrase governing a run of anchors** -- "son of X and Y, brother of A, B, C" -- and every defect it
had came from that shape. `scripts/scraped_pages.py` and two others went with it.

**This is not that reader.** The saved pages contain the same card grid the extension reads, and
the relation is an attribute of each individual card:

    <li class="unit size_1of3 media small" itemscope>
      <a data-profile-id="6000000001333348128">Johan Mathesius</a>
      <div class="quiet">husband</div>
    </li>

One card, one person, one relation word, no opener and no run. That is the structured form the
ruling asked for, so the pages can be read without a browser, a rate limit or a CAPTCHA.

**Emma, 2026-09-14:** *"we definitely need to be on these items, on all these pages that we have
locally saved, running the immediate relatives scraping thing on them, but we'd be deleting
them."* The deletion is the point; this is what has to happen first.

⛔ **THE MANIFEST IS THE POINT, NOT A BY-PRODUCT.** 232 MB is about to be deleted. Every page gets
a row saying what came out of it, so the deletion is auditable per file rather than asserted.
"""
import html as _html
import io
import os
import re
import sys

CARD = re.compile(
    r'<li class="unit size_1of3 media small"[^>]*>(.*?)</li>', re.S)
PID = re.compile(r'data-profile-id="(\d+)"')
NAME = re.compile(r'<span itemprop="name"[^>]*>(.*?)</span>', re.S)
QUIET = re.compile(r'<div class="quiet">(.*?)</div>', re.S)
TITLE = re.compile(r"<title>(.*?)</title>", re.S)


def detag(s):
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ").strip()


def read(path):
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    out = []
    for m in CARD.finditer(raw):
        c = m.group(1)
        pid = PID.search(c)
        if not pid:
            continue
        nm = NAME.search(c)
        rel = QUIET.search(c)
        out.append((pid.group(1), detag(nm.group(1)) if nm else "", detag(rel.group(1)) if rel else ""))
    # de-duplicate: the grid is rendered twice, photo view and text view
    seen = set(); uniq = []
    for pid, nm, rel in out:
        if (pid, rel) in seen:
            continue
        seen.add((pid, rel)); uniq.append((pid, nm, rel))
    return uniq


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sample = 0
    if "--sample" in argv:
        sample = int(argv[argv.index("--sample") + 1])
    d = "geni-scraping"
    files = sorted(f for f in os.listdir(d) if f.endswith(".html") and f[:-5].isdigit())
    if sample:
        files = files[:sample]
    rows = []; man = []
    for fn in files:
        subject = fn[:-5]
        cards = read(os.path.join(d, fn))
        withrel = sum(1 for _, _, r in cards if r)
        man.append((fn, subject, len(cards), withrel))
        for pid, nm, rel in cards:
            rows.append([subject, pid, nm, rel])
    if sample:
        for fn, s, n, w in man:
            print("  %-22s %3d cards, %3d with a relation" % (fn, n, w))
        print("\nrelation words seen:")
        import collections
        c = collections.Counter(r[3] for r in rows if r[3])
        for k, v in c.most_common(25):
            print("   %5d  %s" % (v, k))
        return 0
    with io.open("reports/saved-page-family.tsv", "w", encoding="utf-8", newline="") as fh:
        fh.write("subject\tprofile_id\tname\trelation\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    with io.open("reports/geni-scraping-extraction-manifest.tsv", "w", encoding="utf-8", newline="") as fh:
        fh.write("file\tsubject\tcards\twith_relation\n")
        for fn, s, n, w in man:
            fh.write("%s\t%s\t%d\t%d\n" % (fn, s, n, w))
    print("%d page(s) -> reports/saved-page-family.tsv, %d relation rows" % (len(man), len(rows)))
    print("pages yielding nothing: %d" % sum(1 for _, _, n, _ in man if n == 0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
