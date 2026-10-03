# INBE: Inbe clan genealogy

> Started with [cleanvibe](https://github.com/EmmaLeonhart/cleanvibe) on 2026-10-02.

Research on the **Inbe clan (忌部氏 / 斎部氏, Imbe)**, the hereditary ritual
specialists of the ancient Japanese court: their origins, their regional
branches (Awa, Sanuki, Kii, Izumo, Tsukushi, Ise), how they spread, and a
**GEDCOM genealogy** that traces named Inbe people back toward their divine
ancestor Futodama no Mikoto, as far as the sources allow.

Every person and parent–child link in the genealogy cites its source and
carries a confidence level. Links that no source gives are left out, not
invented.

## Layout

- `research/SUMMARY.md`: the current answer, how sure, what is open.
- `research/sources.md`: sources consulted and how far to trust each.
- `research/notes/`: one file per sub-question.
- `genealogy/`: the GEDCOM file and the data it is built from.
- `data_lake/`: source material (`downloads/` is what the agent fetched).
- `INTENT.md`, `queue.md`: what the project is for and what is next.

## Working on it

Run `cleanvibe` in this folder (or double-click `!runClaude.bat` on Windows) to
open a new Claude session here. It starts with Remote Control on, so you can
continue from the Claude app or web. Earlier sessions are in `sessions/`.
