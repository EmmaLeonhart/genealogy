# Tanba clan chart — parent → child edges, read visually

Source: <https://shinto.miraheze.org/wiki/Tanba_clan> § Genealogy.
Roster: `roster-extraction/data_lake/roster.tanba.tsv`, 185 people, 183 with a QID,
built by a separate session. This file is the relationships, read off screenshots of
the rendered chart, never from the page text — the same split as the Izumo work.

**This chart states its own convention**, which the Izumo one did not:
*"Solid lines are biological children, dotted lines (vertical) are adopted children."*
So `adopted` in the `kind` column is read, not inferred.

**Two box labels are not people:**

- `〔中略〕` — *generations omitted*. Appears twice near the top, between Emperor Ling
  of Han and Sakanoue no Shina and again before Ōkuni.
- `〔傍流へ〕` — *to the collateral branch*, and `〔嫡流へ〕` — *to the main line*.
  These are cross-references to another part of the chart, so a person carrying one is
  **not childless**; their descent is drawn elsewhere.

## Where it attaches to Geni

`Sakanoue no Ōkuni` `6000000210408834830` (`Q97341863`) is on Geni already, with his
father `Okina 坂上老` and his son `Inukai`, and the Sakanoue line continues below Inukai
into Karitamaro and Tamuramaro. **The Tanba line is not attached to any of it** — the
chart makes `Tanba no Yasuyori` a second son of Ōkuni and Geni gives Ōkuni only Inukai.

Emma, 2026-08-20, after this survey: *"the tanba clan is simply absent and we can just
mass add going down from Tanba no Yasuyori as a child of Sakanoue no Okuni"*, and
*"as the tanba line is so unattested the adding of the descendants en masse will be
much cleaner"*.

**Name search does not find these people and that is not evidence of absence.**
`Tanba Yasuyori`, `Yasuyori Tanba`, `Yasuyori`, `丹波康頼` and `康頼` all return nothing,
while `Tanba` returns hits and a kanji control (`忍立毛比`) returns its profile — so the
search works and simply does not match. What settled the question was walking Ōkuni's
actual children by id.

## Read so far — Yasuyori down

Every edge below was read zoomed. Three edges taken at low zoom were **removed** rather
than kept, because they gave `Hiromoto`, `Naganaga` and `Kanehira` two parents each:
the low-zoom reading put them under `Yoriyuki`, `Yoshimoto` and `Ienaga`, and the zoomed
reading puts them under `Naganaga`, `Tsunenaga` and `Hisayasu`. **Kanehira is worth a
second look before he is created** — the two readings came from screenshots at different
horizontal offsets and I did not re-check him directly.

The chart is ~7,500px tall and ~2,830px wide, so it is read in bands; `Tsunenaga` and
`Motokane` are the tops of columns whose own parents are in a band not yet read.
