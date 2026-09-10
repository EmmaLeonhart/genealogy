"""Does parsing a SAVED PAGE give the same family as scraping that page LIVE?

Emma, 2026-09-10: *"we need something that we can prove gives 100% identical results to scraping
those ones."* This is the differential that answers it, and it is a comparison rather than an
assertion: for every person who has BOTH a live extension scrape and a saved `.html`, the saved
page is re-parsed offline and the two families are compared edge by edge.

    reference   the extension's own scrape -- `geni-families/<id>-family.tsv`
    candidate   `scraped_pages.parse_family` over `geni-scraping/<id>.html`

An edge is `(phrase, relative_geni_id, relative_name)`. The phrase is Geni's own word for the tie.

⛔ **ONE MAPPING IS APPLIED AND IT IS A RE-ENCODING, NOT A NORMALISATION.** The two readers store
the same field differently: the live scraper writes the opener with the connective dropped
(`Son`, `Wife`, `Half brother`), the offline one keeps it whole and lower-cased (`son of`,
`wife of`, `half brother of`). Both are reading the identical DOM token, so the trailing ` of` is
stripped and the case folded to put them in one encoding.

Nothing else is touched. A mapping applied to both sides until they agree is how a differential is
made to pass without meaning anything, so the ids and the names are compared exactly as each
reader produced them -- and it is the ids and names, not the phrase, that carry the family.

⛔ **A PERSON IS ONLY COUNTED WHERE BOTH SIDES EXIST.** A missing saved page is not a mismatch and
a missing scrape is not one either; both are simply outside the population that can be compared.
The number this prints is the agreement rate over the comparable set and the size of that set,
and both halves have to be quoted together for it to mean anything.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from genimerge.genipage import html_of_saved_page          # noqa: E402
from scraped_pages import parse_family                      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "saved-page-equivalence.tsv"


def _tie(phrase: str) -> str:
    """One encoding for the tie: lower-cased, with the trailing ` of` connective dropped."""
    s = " ".join(phrase.split()).lower()
    return s[:-3].strip() if s.endswith(" of") else s


def read_reference(path: pathlib.Path) -> set[tuple[str, str, str]]:
    """The live scrape's edges, out of the family TSV the extension wrote."""
    edges = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 5 or parts[0] == "subject_geni_id":
            continue
        _subject, _relation, phrase, rid, rname = parts[:5]
        edges.add((_tie(phrase), rid.strip(), rname.strip()))
    return edges


def read_candidate(path: pathlib.Path) -> set[tuple[str, str, str]]:
    """The saved page's edges, parsed offline."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    _names, edges = parse_family(html_of_saved_page(raw))
    out = set()
    for phrase, people in edges:
        for rid, rname in people:
            out.add((_tie(phrase), rid.strip(), rname.strip()))
    return out


def main() -> int:
    fam_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "geni-families"
    pages = {p.stem: p for p in (ROOT / "geni-scraping").glob("*.html") if p.stem.isdigit()}

    rows, exact, compared = [], 0, 0
    for fam in sorted(fam_dir.glob("*-family.tsv")):
        gid = fam.name.split("-family")[0]
        page = pages.get(gid)
        if page is None:
            continue
        compared += 1
        try:
            ref, cand = read_reference(fam), read_candidate(page)
        except Exception as exc:                       # a page that will not parse is a FAILURE
            rows.append((gid, "parse-error", 0, 0, 0, 0, str(exc)[:120]))
            continue
        missing, extra = ref - cand, cand - ref
        if not missing and not extra:
            exact += 1
            rows.append((gid, "identical", len(ref), len(cand), 0, 0, ""))
        else:
            detail = "; ".join(
                ["-%s|%s|%s" % e for e in sorted(missing)][:4]
                + ["+%s|%s|%s" % e for e in sorted(extra)][:4])
            rows.append((gid, "differs", len(ref), len(cand), len(missing), len(extra), detail))

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("geni_id\tverdict\tlive_edges\tsaved_edges\tmissing\textra\tdetail\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    print("comparable people (both a live scrape and a saved page): %d" % compared)
    print("  identical      %d" % exact)
    print("  differs        %d" % sum(1 for r in rows if r[1] == "differs"))
    print("  parse-error    %d" % sum(1 for r in rows if r[1] == "parse-error"))
    if compared:
        print("agreement: %d/%d = %.1f%%" % (exact, compared, 100.0 * exact / compared))
    print("-> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
