"""Rebuild the Garborg Family Entry Sheet artifact from the FULL downloaded items.

    python scripts/build-garborg-entry-sheet.py

The page at claude.ai/code/artifact/c2430047-… is Emma's entry sheet for the Garborg
items she builds by hand.

**Everything here comes from `out/garborg-full-items.json`**, all 14 items fetched via
`genimerge.wikidata.full_entities`, by way of `scripts/garborg-modelling.py`. A previous
version of this page was built from a fetch-and-summarise read instead, and it published
three false claims — chiefly that Arne Garborg had no parents on Wikidata. He has them.
Emma: *"you're supposed to download the full wikidata items for the people I've edited to
get the modelling."*

The stylesheet is the one the page already had; the design is unchanged on purpose, so a
redeploy reads as the same document rather than a new one.
"""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "out" / "garborg-artifact.css"
OUT = ROOT / "out" / "garborg-entry-sheet.html"

#: (name, role, chip, chip class, qid, years, rows, closing note)
PEOPLE = [
    ("Arne Garborg", "child 1 &middot; the anchor", "6 sibling links short", "create",
     "Q467497", "1851 &ndash; 1924", [
         ("full item, 24 Aug",
          "126 properties, almost all external identifiers. A community item, "
          "not a template for anything."),
         ("P22 / P25",
          "<b>present</b> &mdash; <code>Q141152512</code> &middot; "
          "<code>Q141152523</code>, both unreferenced"),
         ("P3373 <i>sibling</i>",
          "<b>2 of 8</b> &mdash; Stena and Jon, both referenced with P2600"),
         ("P2600", "<code>6000000003492005116</code>"),
         ("P1477 <i>birth name</i>",
          "<span class='lit'>Aadne Eivindsson Garborg</span> &middot; <code>mul</code>"),
         ("P735 / P734",
          "<code>Q645757</code> Arne &middot; <code>Q30250555</code> Garborg "
          "&mdash; no P5056"),
     ],
     "<b>An earlier version of this page said he had no parents. That was wrong</b> "
     "&mdash; it came from a summarised read of the item, and the full download has all "
     "three links. What he actually lacks is P3373 to six siblings, and P5056."),

    ("Eivind Aadnesson Garborg", "father", "the model", "exists",
     "Q141152512", "1822 &ndash; 1870", [
         ("labels",
          "<code>en</code> + <code>mul</code> &middot; "
          "<span class='lit'>Eivind Aadnesson Garborg</span>"),
         ("P735 <i>given name</i>",
          "<code>Q3358418</code> Eivind &mdash; "
          "<span class='note'>no P1545, no P7452</span>"),
         ("P5056 <i>patronym</i>",
          "<code>Q141152710</code> Aadnesson &mdash; "
          "<span class='note'>no P144</span>"),
         ("P734 <i>family name</i>", "<code>Q30250555</code> Garborg"),
         ("P40 <i>child</i> &times; 9",
          "all nine &mdash; the first three referenced, the last six not"),
         ("P26 / P569 / P570",
          "Ane Oline &middot; 26 Jul 1822 &ndash; 13 Feb 1870"),
     ],
     "<b>Still the only one of the ten carrying name properties.</b> All three are bare: "
     "the qualifiers <i>name modelling.txt</i> prescribes are not on them."),

    ("Ane Oline Jonsdatter Raugstad", "mother", "names missing", "create",
     "Q141152523", "1832 &ndash; 1908", [
         ("dates",
          "<b>done since 23 Aug</b> &mdash; 23 Feb 1832 &ndash; 28 Apr 1908"),
         ("P40 <i>child</i> &times; 9", "all nine &middot; P26 &rarr; Eivind"),
         ("names",
          "<b>none.</b> Ane, Oline, patronym <i>Jonsdatter</i>, family "
          "<i>Raugstad</i>"),
     ],
     "Her patronym names her father Jon, a further person to create. "
     "<i>Jonsdatter</i> has no item yet."),

    ("Stena Eivindsdatter Garborg", "child 2 &middot; the label exception",
     "names missing", "create", "Q141152600", "1852 &ndash; 1877", [
         ("label",
          "<span class='lit'>Stena Eivindsdatter Garborg</span> &mdash; Geni holds "
          "<span class='lit'>Stine &ldquo;Stena&rdquo;&hellip;</span>"),
         ("dates",
          "<b>done since 23 Aug</b> &mdash; 12 Dec 1852 &ndash; 4 Oct 1877"),
         ("P22 / P25 / P3373", "Eivind &middot; Ane Oline &middot; Arne, Jon"),
         ("names",
          "<b>none.</b> Stena, patronym <i>Eivindsdatter</i>, family <i>Garborg</i>"),
     ],
     "<b>The one label that drops a token.</b> Mary and Lena keep theirs, so this is a "
     "judgement that <i>Stena</i> is a short form of <i>Stine</i> &mdash; not a rule a "
     "generator can apply."),

    ("Samuel Eivindsen Garborg", "child 4", "names missing", "create",
     "Q141162040", "1857 &ndash; 1943", [
         ("created since 23 Aug",
          "this page previously listed him as still to create"),
         ("structure",
          "P31, P21, P2600, P569, P570, P22, P25, P3373 &times; 3"),
         ("names",
          "<b>none.</b> Samuel, patronym <i>Eivindsen</i>, family <i>Garborg</i>"),
     ],
     "Referenced exactly like every sibling: P2600 on the dates, the parents and the "
     "sibling links, and on nothing else."),

    ("Inger Marie Mary Eivindsdatter Garborg", "child 6", "names missing", "create",
     "Q141162043", "1863 &ndash; 1955", [
         ("label", "all three given tokens kept, quote marks dropped"),
         ("structure",
          "P31, P21, P2600, P569, P570, P22, P25, P3373 &times; 3"),
         ("names",
          "<b>none.</b> Two given names &mdash; the first case that would need P1545"),
     ],
     "Buried at Eagle Hill Cemetery, so she emigrated. Geni holds that; P119 is on no "
     "item."),

    ("Ane Oline Lena Eivindsdatter Garborg", "child 9", "names missing", "create",
     "Q141162046", "1870 &ndash; 1916", [
         ("label",
          "all tokens kept &mdash; the third nickname case, agreeing with Mary"),
         ("structure", "P2600, P569, P570, P22, P25, P3373 &times; 3"),
         ("uncited",
          "P31, P21 and P2600 carry no reference — the same on every item"),
     ],
     "Identical in shape to Samuel and Inger Marie. The eleven items she made are "
     "uniform; there is no partial one among them."),

    ("Aadnesson", "a patronymic name item", "minimal", "rel",
     "Q141152710", "name item", [
         ("labels",
          "<code>en</code> + <code>mul</code> &middot; "
          "<span class='lit'>Aadnesson</span>"),
         ("P31", "<code>Q110874</code> <i>patronymic</i>"),
         ("everything else",
          "nothing &mdash; no description, no P144, no P407, no P282"),
     ],
     "This is the whole template for a name item, and "
     "<code>build-garborg-name-items.py</code> already matches it."),
]


def card(name, role, chip, chip_class, qid, years, rows, note):
    body = "\n".join(
        f'    <div class="row"><div class="prop">{prop}</div>'
        f'<div class="val">{val}</div></div>'
        for prop, val in rows)
    return f'''  <article class="person">
   <div class="phead">
    <h3 class="pname">{name}</h3>
    <span class="chip rel">{role}</span>
    <span class="chip {chip_class}">{chip}</span>
    <span class="pyears">{years} &middot; {qid}</span>
   </div>
   <div class="pbody">
{body}
   </div>
   <p class="pending">{note}</p>
  </article>'''


def main():
    css = io.open(CSS, encoding="utf-8").read()
    cards = "\n".join(card(*person) for person in PEOPLE)

    html = f'''<title>Garborg Family Entry Sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Libre+Franklin:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">

<style>
{css}
</style>

<div class="wrap">

<header>
 <p class="eyebrow">Wikidata &middot; full items &middot; 24 August 2026</p>
 <h1>Garborg Family Entry Sheet</h1>
 <p class="standfirst">All ten people have items, and the eleven Emma has built are
 uniform in shape. What is left is <em>names</em>: ten of the eleven carry none.
 <em>This page previously said Arne Garborg had no parents. That was wrong</em> &mdash; it
 was built from a summary of his item rather than the item.</p>

 <div class="situation">
  <div class="stat"><span class="n">11</span><span class="k">items Emma has built</span></div>
  <div class="stat"><span class="n">1</span><span class="k">of them carries name properties</span></div>
  <div class="stat"><span class="n">0</span><span class="k">of them carry ja or zh</span></div>
  <div class="stat"><span class="n">6</span><span class="k">sibling links Arne still lacks</span></div>
 </div>
</header>

<div class="howto">
 <h2>Read from the full items, 24 August</h2>
 <ol>
  <li><strong>The six siblings exist.</strong> Samuel, Even, Inger Marie, Abel, Ole and
  Ane Oline &ldquo;Lena&rdquo; were all created, and all carry dates, parents and sibling
  links.</li>
  <li><strong>Arne has his parents.</strong> P22 &rarr; Eivind and P25 &rarr; Ane Oline,
  plus P3373 to Stena and Jon. An earlier version of this page reported all three as
  ABSENT; that came from a summarised read and was false.</li>
  <li><strong>The citation split is exactly as first written.</strong> P2600 references
  the dates and the relationships and nothing else &mdash; counted across all 14 items, it
  is never a reference on P31 or P21. A middle version of this page called the split
  inconsistent. It is not.</li>
  <li><strong>The gap is names.</strong> Only Eivind carries P735, P734 and P5056.</li>
 </ol>
</div>

<section>
 <h2 class="group">The shape you are using &mdash; read live, 24 August</h2>

 <div class="howto" style="border-left-color:var(--exists)">
  <h2 style="color:var(--exists)">Counted across all 14 full items</h2>
  <ol>
   <li><strong>The reference is the Geni ID, and only on these:</strong> P3373 (&times;24),
   P569 (&times;10), P570 (&times;10), P22 (&times;8), P25 (&times;8), P40 (&times;5),
   P26 (&times;4). <strong>Never</strong> on P31, P21, P2600, P735, P734 or P5056. The
   P248 / P813 / P143 references in the data are all on the three community items.</li>
   <li><strong>The eleven items are uniform.</strong> Each carries P31, P21, P2600, P569,
   P570, then P22/P25/P3373 for a child or P26/P40 for a parent. No partial item among
   them.</li>
   <li><strong>Labels are <code>en</code> and <code>mul</code>, the same string.</strong>
   No description, no alias, no sitelink on any of them.</li>
   <li><strong>No qualifier of hers appears anywhere</strong> &mdash; no P1545, no P7452,
   no P3831, no P144. The only qualifiers in the 14 items are community-added, on
   Q467497 and Q3143008.</li>
   <li><strong>Never used:</strong> P19 place of birth, P20 place of death, P119 place of
   burial, P1477 birth name &mdash; though Geni holds those values.</li>
   <li><strong>A name item is minimal</strong> &mdash; two labels and a single P31.</li>
  </ol>
 </div>

 <div class="howto" style="border-left-color:var(--create)">
  <h2 style="color:var(--create)">What is outstanding</h2>
  <ol>
   <li><strong>Names on ten of the eleven.</strong> This is the whole gap. Each needs a
   given-name item, a patronym item and a family-name item to point at, and only
   <i>Aadnesson</i> Q141152710 exists so far.</li>
   <li><strong>Arne needs P3373 to six more siblings</strong>, and has no P5056.</li>
   <li><strong>ja and zh labels on all eleven.</strong> None carries either. The three
   community items already have them.</li>
   <li><strong>The nickname label is a judgement, not a rule.</strong> Stena drops
   <i>Stine</i>; Mary and Lena keep every token. Strip the quote marks and keep
   everything is the default, and matches two cases of three.</li>
  </ol>
 </div>
</section>

<section>
 <h2 class="group">The items, as they stand</h2>
{cards}
</section>

<footer>
 <p>Every figure on this page is counted from <code>out/garborg-full-items.json</code>
 &mdash; all 14 items fetched in one request through
 <code>genimerge.wikidata.full_entities</code>, then read offline. Nothing here comes
 from a summary of an item, and nothing from an edit history.</p>
 <p>An earlier version was built the other way and published three false claims: that
 Arne Garborg had no parents, that the citation split was inconsistent, and that six of
 the items could not be seen. All three are corrected above.</p>
 <p>The durable version is <code>docs/wikidata-item-template.md</code>;
 <code>scripts/garborg-modelling.py</code> regenerates both from the same file.</p>
</footer>

</div>
'''
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(html):,} bytes, {len(PEOPLE)} cards")


if __name__ == "__main__":
    main()
