"""Rebuild the Garborg Family Entry Sheet artifact from the live re-read.

    python scripts/build-garborg-entry-sheet.py

The page at claude.ai/code/artifact/c2430047-… is Emma's entry sheet for the Garborg
items she is building by hand. It was written 2026-08-23 and the items moved under it:
all ten people exist now, and one thing the page reported as finished is not.

Content here is what `docs/wikidata-item-template.md` records, in the page's own shape.
The stylesheet is the one the page already had — the design is unchanged on purpose, so
a redeploy reads as the same document rather than a new one.
"""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "out" / "garborg-artifact.css"
OUT = ROOT / "out" / "garborg-entry-sheet.html"

#: (name, role, chip, chip class, qid, years, rows, closing note)
PEOPLE = [
    ("Arne Garborg", "child 1 &middot; the anchor", "no parents", "create",
     "Q467497", "1851 &ndash; 1924", [
         ("read live 24 Aug",
          "~120 properties, almost all external identifiers. A community item, "
          "not a template for anything."),
         ("P22 / P25",
          "<b>ABSENT.</b> Both parents have items and neither is linked."),
         ("P3373 <i>sibling</i>",
          "<b>ABSENT.</b> Eight siblings have items; none is linked from him."),
         ("P2600", "<code>6000000003492005116</code>"),
         ("P1477 <i>birth name</i>",
          "<span class='lit'>Aadne Eivindsson Garborg</span> &middot; <code>mul</code>"),
         ("P735 / P734",
          "<code>Q645757</code> Arne &middot; <code>Q30250555</code> Garborg "
          "&mdash; no P5056"),
     ],
     "<b>This is the outstanding edit on the page.</b> The previous version said his "
     "parent and sibling links had gone in by hand and that nothing was outstanding on "
     "him. They have not. A targeted read of his claims object returns ABSENT for P22, "
     "P25 and P3373."),

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
     "P21 <i>sex or gender</i> carries no reference here. On Stena it does."),

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
          "<b>P31 and P21 carry no reference</b>, unlike Samuel and Inger Marie"),
     ],
     "Made in the same sitting as Samuel and Inger Marie and referenced differently, "
     "which is what settles the citation split as habit rather than rule."),

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
 <p class="eyebrow">Wikidata &middot; read live &middot; 24 August 2026</p>
 <h1>Garborg Family Entry Sheet</h1>
 <p class="standfirst">All ten people have items now &mdash; the six this page listed as
 &ldquo;still to create&rdquo; were created. What is left is <em>names</em>, and one thing
 this page reported as finished and is not: <em>Arne Garborg is still not linked to his
 parents.</em></p>

 <div class="situation">
  <div class="stat"><span class="n">10</span><span class="k">of 10 people have items</span></div>
  <div class="stat"><span class="n">1</span><span class="k">of 10 carries name properties</span></div>
  <div class="stat"><span class="n">0</span><span class="k">carry a ja or zh label</span></div>
  <div class="stat"><span class="n">1</span><span class="k">patronym item exists &mdash; Aadnesson</span></div>
 </div>
</header>

<div class="howto">
 <h2>What changed since 23 August</h2>
 <ol>
  <li><strong>The six siblings exist.</strong> Samuel, Even, Inger Marie, Abel, Ole and
  Ane Oline &ldquo;Lena&rdquo; were all created. The second half of this page was a
  to-create list and is now a record.</li>
  <li><strong>Dates are done.</strong> Ane Oline, Stena and Jon all carry P569 and P570.
  This page said they were outstanding.</li>
  <li><strong>Arne still has no parents.</strong> This page said the links went in by hand
  and that nothing was outstanding on him. A targeted read of his claims object returns
  <strong>ABSENT</strong> for P22, P25 and P3373.</li>
  <li><strong>The citation split is not a rule.</strong> This page called it consistent
  across every item. It is not.</li>
 </ol>
</div>

<section>
 <h2 class="group">The shape you are using &mdash; read live, 24 August</h2>

 <div class="howto" style="border-left-color:var(--exists)">
  <h2 style="color:var(--exists)">Confirmed unchanged</h2>
  <ol>
   <li><strong>The reference is the Geni ID.</strong> Statements carry P2600 as their
   reference snak, never P854 or P813. P2600 itself is never referenced &mdash; it
   <em>is</em> the reference.</li>
   <li><strong>Labels are <code>en</code> and <code>mul</code>, the same string.</strong>
   No descriptions, no aliases and no sitelinks on any of the ten.</li>
   <li><strong>P3373 <i>sibling</i> is used</strong>, both ways, three links on each of
   the newer items.</li>
   <li><strong>A name item is minimal</strong> &mdash; two labels and a single P31,
   nothing else.</li>
   <li><strong>No P19, P20 or P119</strong> on any item, though Geni holds birthplaces,
   deathplaces and burials.</li>
  </ol>
 </div>

 <div class="howto" style="border-left-color:var(--create)">
  <h2 style="color:var(--create)">Corrected by this read</h2>
  <ol>
   <li><strong>The citation split is habit, not rule.</strong> P31 is referenced on Stena,
   Samuel and Inger Marie, and not on Eivind or Lena. P21 is referenced on Stena alone.
   Lena was made in the same sitting as Samuel and Inger Marie and is referenced
   differently, so it does not track creation order either. What does hold: every date and
   every relationship is cited, and P2600 never is.</li>
   <li><strong>The name qualifiers are not in the items.</strong>
   <i>name modelling.txt</i> prescribes P1545 and P7452 on the given name and P144 on the
   patronym. Eivind &mdash; the only item with name statements &mdash; carries none of
   them. He has one given name, so that is weak evidence about ordinals; it is strong
   evidence about P144, which would name his father Aadne and is simply absent.</li>
   <li><strong>The nickname label has one exception, not a rule.</strong> Stena drops
   <i>Stine</i>; Mary and Lena keep every token. Stripping the quote marks and keeping
   everything is the default and matches two cases of three.</li>
   <li><strong>P5056 is emittable now.</strong> The daily batch emits zero patronyms
   because it assumes no patronym item exists. <i>Aadnesson</i> does.</li>
  </ol>
 </div>
</section>

<section>
 <h2 class="group">The items, as they stand</h2>
{cards}
</section>

<footer>
 <p>Eight items were read live on 24 August 2026: <code>Q467497</code>,
 <code>Q141152512</code>, <code>Q141152523</code>, <code>Q141152600</code>,
 <code>Q141162040</code>, <code>Q141162043</code>, <code>Q141162046</code> and the name
 item <code>Q141152710</code>.</p>
 <p><strong>Not re-read, so not reported on here:</strong> <code>Q141152614</code> Jon,
 <code>Q141162041</code> Even, <code>Q141162044</code> Abel, <code>Q141162045</code> Ole,
 <code>Q3143008</code> Hulda and <code>Q11959067</code> Arne Olaus. What this page says
 about them is from the 23 August read and may have moved since.</p>
 <p>The durable version is <code>docs/wikidata-item-template.md</code> in the repo, which
 carries the per-item reference table.</p>
</footer>

</div>
'''
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(html):,} bytes, {len(PEOPLE)} cards")


if __name__ == "__main__":
    main()
