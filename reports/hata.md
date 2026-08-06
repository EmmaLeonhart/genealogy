# The Hata clan in the merged tree

Measured 2026-08-06 against `out/merged.ged` (98 exports, 202,433 people).
Written to answer Emma's "import the Hata clan — surprised it is not all there
already". It is not all there, and the shape of what *is* there says why.

## What we hold: 27 people, in a thread

| | |
| --- | ---: |
| people carrying a Hata clan name | **27** |
| of those, with **no spouse recorded** | **26** |
| with no recorded sibling | 18 |
| with 0 or 1 recorded child | 20 |
| branch points (more than one child) | **1** — Hata no Kawakatsu |

That is not a clan. It is a single father-to-son thread running from Fusu 嬴姓
down through 孝武王 → Yuzuki no Kimi 弓月君 → 普洞王 → 酒君/酒公 → 意美 → 宇志 →
Tanshō → Kawa → Kunikatsu → **秦河勝 Hata no Kawakatsu**, where it forks once
into 広国 and 石勝, and each fork continues as another single thread.

**Every one of the 26 is in a marriage family with no other spouse in it.** Not
"the wives are unnamed" — the wives are not in our data at all. A clan of 27
people with zero recorded marriages is the fingerprint of a blood-only walk:
`Ancestors` and `BloodTree` follow parent links and step over every spouse. That
is the same trap that nearly cost the Jimmu bridge, recorded in `CLAUDE.md`, and
here it cost the entire lateral structure of the clan.

## What the kanji screen gets wrong, and why it is called out

Matching 秦 anywhere in a name returns **58** people. **31 of them are not
Hata**: they carry 秦州成紀 or 秦州清水 — Chengji and Qingshui *in Qinzhou*, a
Chinese place used as a surname field. They are excluded above. This is the
usual failure of name matching and it is why the count is stated with its screen
attached rather than as a bare number.

## The Koremune gap — eight people, and they are the clan's own branch

惟宗 (Koremune) is the Hata clan's later name. The tree holds **exactly two**
Koremune people, 具範 and 永厚, and they are precisely the two that
`reports/path-hata.md` reports as held at steps 41–42. The eight people between
them and the 安達 line are all absent:

| step | name | relation to previous | Geni ID |
| ---: | --- | --- | --- |
| 33 | 安達景盛 | his father | [6000000008141407248](https://www.geni.com/people/x/6000000008141407248) |
| 34 | 丹後内侍 | his mother | [6000000002933557025](https://www.geni.com/people/x/6000000002933557025) |
| 35 | 惟宗広言 | **her husband** | [6000000002934660014](https://www.geni.com/people/x/6000000002934660014) |
| 36 | 惟宗基言 | his father | [6000000004668892191](https://www.geni.com/people/x/6000000004668892191) |
| 37 | 惟宗孝言 | his father | [6000000004668782525](https://www.geni.com/people/x/6000000004668782525) |
| 38 | 惟宗孝近 | his father | [6000000004668811321](https://www.geni.com/people/x/6000000004668811321) |
| 39 | 惟宗貴重 | his father | [6000000004668647969](https://www.geni.com/people/x/6000000004668647969) |
| 40 | 惟宗広孝 | his father | [6000000004668691541](https://www.geni.com/people/x/6000000004668691541) |

Both ends are anchored — step 32 安達義景 is held, steps 41–42 are held — so this
is a bridge of eight, inside the 6–9 steps a single targeted export has actually
been observed to span.

Worth noting alongside it: the tree holds **51 島津 (Shimazu)** people, and
Shimazu descends from Koremune. We hold the Shimazu and we hold the Hata, and
the eight-person Koremune stretch that would join them to each other is the
piece missing.

## Two exports, and both must be `Forest`

1. **秦河勝 Hata no Kawakatsu `6000000001952260956`** — the clan's
   best-documented figure and our only branch point. The target here is not
   depth, which we already have; it is the **width** the blood walks discarded:
   wives, brothers, and the collateral houses. A `Descendants` export would also
   fan out, but it would fan out from a man with no recorded wife and so would
   propagate the same defect; `Forest` picks up the marriages.
2. **惟宗広言 `6000000002934660014`** — closes the eight-step gap above.
   `Forest` is not a preference here, it is required: step 34 → 35 is
   **"her husband"**, a marriage link. `Ancestors` and `BloodTree` seeded
   anywhere in this window walk straight past 惟宗広言 and never bridge.

## What this predicts

The first export should raise the Hata count well past 27 while adding few or no
generations — the depth is already there and it is the breadth that is missing.
If a `Forest` export from Kawakatsu comes back with the count barely moved, the
explanation is not our sampling: it means Geni's 秦氏 is itself recorded as a
patriline, and "import the Hata clan" has no more clan to import. Recording the
prediction here so `git show` supplies it when the export lands.
