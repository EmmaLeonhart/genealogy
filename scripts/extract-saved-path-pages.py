"""Pull relationship chains out of locally-saved Geni HTML pages.

    python scripts/extract-saved-path-pages.py <dir> [<dir> ...]

**Why these files exist at all.** Emma saved them by hand — *"I am just gonna say I am saving them
manually in a directory and you solve it later"* — because the agent was failing to capture long
rendered chains. They are the only copy of some of them: Emperor Jimmu at 109 steps, Solomon at
240, 孔垂長 at 252.

**The markup is identical to a live page**, which is the whole reason this works:

    <span class="segment">
      <span class="name"><a data-profile-id="6000000019395171839">Olof Ericsson</a></span>
      <span class="subtext"><span class="clipboard-only">(</span>his son<span class="clipboard-only">)</span></span>
    </span>

⛔ **THE PARENTHESES ARE NESTED SPANS, NOT TEXT.** A regex for `>\(...\)</span>` matches nothing
here and reports every page as having zero relations, which is exactly what it did on the first
attempt. Strip tags inside the subtext instead of trying to match around them.

**`span.subtext.clipboard-hide` is the viewer's own blank subtext** and is skipped, the same way
the live fetcher skips it, so step 0 is the viewer with no relation word.

Writes the same six columns as `reports/path-chains.tsv` so the rows merge straight in with
`scripts/merge-path-chains.py`: `to_id, kind, step, profile_id, name, relation`.
"""
import html
import io
import os
import re
import sys

SEG = re.compile(r'<span class="segment"[^>]*>(.*?)</span>\s*</span>', re.S)
SEGMENTS = re.compile(r'<span class="segment"(?![^>]*white-space)[^>]*>(.*?)(?=<span class="segment"|<span id="connecting_path_toggle"|</div>)', re.S)
NAME = re.compile(r'<span class="name"[^>]*>(.*?)</span>', re.S)
SUBTEXT = re.compile(r'<span class="subtext(?! clipboard-hide)"[^>]*>(.*?)</span>\s*$', re.S)
SUB_ANY = re.compile(r'<span class="subtext(?![^"]*clipboard-hide)[^"]*"[^>]*>(.*)', re.S)
PID = re.compile(r'data-profile-id="(\d+)"')


def detag(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace("\xa0", " ").strip().strip("()").strip()


def extract(path):
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    rows = []
    step = 0
    for m in SEGMENTS.finditer(raw):
        chunk = m.group(1)
        nm = NAME.search(chunk)
        if not nm:
            continue
        name = detag(nm.group(1))
        if not name:
            continue
        pid = PID.search(chunk)
        sub = SUB_ANY.search(chunk)
        rel = detag(sub.group(1)) if sub else ""
        if "clipboard-hide" in chunk[:200] and not rel:
            rel = ""
        rows.append((pid.group(1) if pid else "", name, rel))
        step += 1
    return rows


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not argv:
        print("usage: extract-saved-path-pages.py <dir> [<dir> ...]")
        return 2
    out = []
    n_files = 0
    for d in argv:
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith((".htm", ".html")):
                continue
            p = os.path.join(d, fn)
            rows = extract(p)
            if len(rows) < 2:
                print("  %-58s %d segments -- skipped" % (fn[:58], len(rows)))
                continue
            n_files += 1
            # the chain's target is its last person; the kind is in the page title
            to_id = next((r[0] for r in reversed(rows) if r[0]), "")
            kind = "in-law" if re.search(r"in-?law", raw_title(p), re.I) else "blood"
            for i, (pid, name, rel) in enumerate(rows):
                out.append([to_id, kind, str(i), pid, name, rel])
            print("  %-58s %3d steps, %3d with a relation word"
                  % (fn[:58], len(rows), sum(1 for r in rows if r[2])))
    dest = os.path.join("reports", "saved-page-chains.tsv")
    with io.open(dest, "w", encoding="utf-8", newline="") as fh:
        fh.write("to_id\tkind\tstep\tprofile_id\tname\trelation\n")
        for r in out:
            fh.write("\t".join(r) + "\n")
    print("\n%d file(s) -> %s, %d rows" % (n_files, dest, len(out)))
    return 0


def raw_title(p):
    t = io.open(p, encoding="utf-8", errors="replace").read(4000)
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    return m.group(1) if m else ""


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
