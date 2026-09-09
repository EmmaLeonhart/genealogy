"""Emit the family-scrape as a self-contained snippet, built FROM `family.js`'s own phrase table.

**Why this exists at all.** The collector's `family` job is the right implementation and it stays
the right one. But an unpacked Chrome extension serves its cached copy until it is reloaded, and
a reload is browser chrome -- unreachable from the automation surface, so it is Emma's action.
Between an edit and that reload the extension in the tab is the OLD code, whose `family` result
does not carry the payload.

**So the snippet is a bridge, and the thing that keeps it honest is that it does not restate the
phrase table.** `GC.family.PHRASES` is parsed out of `geni-extension/content/family.js` and
injected verbatim. `CLAUDE.md` § *Code that is WRITTEN but never CALLED* and the two-emitters
failures behind § *A nickname alias carries the SURNAME* are the same shape: two copies of one
rule drift, and the drift is silent. There is one copy here; this file transports it.

**Delete this once the extension is reloaded and the `family` job returns `tsv`.** It is scaffolding
with a specific end condition, which is what `CLAUDE.md` § *LEGACY CODE IS DELETED* wants named.
"""

from __future__ import annotations

import pathlib
import re

FAMILY_JS = pathlib.Path(__file__).resolve().parent.parent / "geni-extension" / "content" / "family.js"


def phrase_table() -> str:
    """The literal `[...]` of `GC.family.PHRASES`, lifted from the extension source."""
    text = FAMILY_JS.read_text(encoding="utf-8")
    start = text.index("GC.family.PHRASES = [")
    end = text.index("];", start) + 2
    return text[start:end].replace("GC.family.PHRASES =", "const PHRASES =")


def snippet(geni_id: str) -> str:
    """The compact form: `@`-prefixed metadata, then one tab-separated line per relative.

    The statistics come from the collector's own `GC.statistics()` and are pasted into the
    `@STATS` line by the caller, never re-read here -- a second reader written in this snippet
    returned all five zeros on a page the extension read as 11 / 10 / 5 / 0 / 1, and all-zeros is
    indistinguishable from an empty block.
    """
    return (
        phrase_table()
        + r"""
const classify = (t) => {
  t = (t || "").trim();
  for (const p of PHRASES) if (p[0].test(t)) return { relation: p[1], phrase: t.split(" of")[0].trim() };
  return null;
};
const lead = [...document.querySelectorAll("*")].filter(
  (e) => e.children.length === 0 && classify(e.textContent));
let relatives = [], prose = "";
if (lead.length) {
  let block = lead[0].parentElement;
  const last = lead[lead.length - 1];
  let guard = 0;
  while (block && !block.contains(last) && guard++ < 12) block = block.parentElement;
  if (block) {
    prose = (block.innerText || "").replace(/\s+/g, " ").trim();
    const seen = new Set();
    let current = null;
    const walk = document.createTreeWalker(block, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    for (let n = walk.nextNode(); n; n = walk.nextNode()) {
      if (n.nodeType === Node.TEXT_NODE) { const h = classify(n.textContent); if (h) current = h; continue; }
      if (n.tagName === "A" && n.hasAttribute("data-profile-id")) {
        const pid = n.getAttribute("data-profile-id");
        const key = (current ? current.relation : "") + "|" + pid;
        if (seen.has(key)) continue;
        seen.add(key);
        relatives.push({ relation: current ? current.relation : "", phrase: current ? current.phrase : "",
                         geni_id: pid, name: (n.textContent || "").trim() });
      }
    }
  }
}
/* ⛔ THE STATISTICS ARE NOT RE-READ HERE. `GC.statistics()` in the extension already does it,
 * waiting on a label-followed-by-digit sentinel because the block fills in after the page does.
 * A second reader written here returned **all five zeros** on a page where the extension read
 * 11 / 10 / 5 / 0 / 1 -- and all-zeros is indistinguishable from a genuinely empty block, which
 * is the absent-versus-zero confusion `CLAUDE.md` warns about in this exact context. So the
 * caller runs the `family` job for the statistics and this snippet for the relatives, and there
 * is one statistics reader rather than two that disagree. */
const banner = [...document.querySelectorAll("*")].filter((e) => e.children.length === 0)
  .map((e) => e.textContent.trim())
  .find((t) => /No path found|could not be found|Path search in progress|relative\?|is [A-Z].*'s /i.test(t)) || "";
({ geni_id: """
        + repr(geni_id)
        + r""", name: ((document.querySelector("h1")||{}).textContent||"").trim(),
  relatives, prose: prose.slice(0, 1200), stats, banner: banner.slice(0, 300),
  segments: document.querySelectorAll("span.segment > span.name a[data-profile-id]").length })
"""
    )


if __name__ == "__main__":
    import sys
    print(snippet(sys.argv[1] if len(sys.argv) > 1 else "0"))
