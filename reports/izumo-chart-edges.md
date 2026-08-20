# Izumo chart — parent → child edges, read visually

**Read off screenshots of the rendered `{{familytree}}`, never from the page text.**
Emma, 2026-08-19: *"you can only look at it visually it's basically an image"*, and
again on 2026-08-20 when she allowed the text for the roster: *"You just cannot use
the text as a way to get the relationships."* So `reports/izumo-chart-roster.tsv`
says who exists; this file says who descends from whom, and the two are built by
different means on purpose.

Column alignment alone is not enough here — the Kitajima headship repeatedly passes
through a cadet house, and the person directly *above* a box in the grid is often not
the parent. Two cases caught by zooming in rather than by reading the column:

- **Kitajima no Masataka 60** sits under Kitajima no Yoshitaka 59 by eye at low zoom.
  The connector runs from **Inaoka no Nobutaka**.
- **Kitajima no Hidetaka 61** likewise descends from **Takahama no Tomotaka**, two
  steps down the Takahama branch, not from the Kitajima box beside him.

## Generation 53 onward

    Izumo no Takatoki 53
      Izumo no Kiyotaka 54
      Senge no Takamune 55
      Kitajima no Sadataka 55

    Senge no Takamune 55 -> Senge no Naokuni 56
    Senge no Naokuni 56 ~~> Senge no Takakuni 57      (dashed = adopted; the solid
                                                       line into Takakuni comes from
                                                       Ookuma no Hiro, via Matsujo)
    Senge no Takakuni 57
      Senge no Mochikuni 58
      Akatsuka no Masatoki
    Senge no Mochikuni 58 -> Senge no Naonobu 59
    Senge no Naonobu 59
      Senge no Takatoshi 60
      Senge no Takakatsu 62
    Senge no Takatoshi 60 -> Senge no Toyotoshi 61

    Akatsuka no Masatoki -> Akatsuka no Masakuni -> Akatsuka no Tokinobu
      -> Akatsuka no Kazunobu -> Akatsuka no Nagatoshi -> Senge no Motokatsu 66
    Senge no Motokatsu 66 -> Senge no Takanou 67 -> Senge no Takamitsu 68
      -> Senge no Hiromitsu 72

## The Kitajima line, 55 to 79 — complete

    Kitajima no Sadataka 55  -> Kitajima no Yoshitaka 56
    Kitajima no Yoshitaka 56 -> Kitajima no Yukitaka 57
    Kitajima no Yukitaka 57  -> Kitajima no Takataka 58
    Kitajima no Takataka 58
      Kitajima no Yoshitaka 59
      Inaoka no Nobutaka
      Takahama no Yoshitaka
    Kitajima no Yoshitaka 59 -> Kitashima no Saburou
    Inaoka no Nobutaka       -> Kitajima no Masataka 60
    Takahama no Yoshitaka    -> Takahama no Tomotaka -> Kitajima no Hidetaka 61
    Kitashima no Saburou     -> Kitajima no Tokitaka -> Kitajima no Yasutaka
                             -> Kitajima no Hisataka 62
    Kitajima no Hisataka 62  -> Kitajima no Hirokatsu 63
    Kitajima no Hirokatsu 63 -> Kitajima no Harutaka 64
    Kitajima no Harutaka 64  -> Kitajima no Tsunetaka 65
    Kitajima no Tsunetaka 65
      Kitajima no Kanetaka 66
      Kitajima no Michitaka 67
      Hisayama no Mototaka
    Kitajima no Michitaka 67 -> Kitajima no Naotaka 68
    Kitajima no Naotaka 68   -> Kitajima no Yoritaka 69
    Kitajima no Yoritaka 69
      Kitajima no Akitaka 70
      Kitajima no Okitaka 72
      Kitajima no Yoritaka 73
    Kitajima no Akitaka 70   -> Kitajima no Nobutaka 71
    Kitajima no Yoritaka 73  -> Kitajima no Zentaka 74
    Kitajima no Zentaka 74   -> Kitashima no Naotaka 75
    Kitashima no Naotaka 75  -> Kitajima no Naritaka 76   (charted as its bare QID)
    Kitajima no Naritaka 76  -> Yoshinori Kitajima 77
    Yoshinori Kitajima 77    -> Kitajima no Eitaka 78
    Kitajima no Eitaka 78    -> Kitajima no Takataka 79
    Kitajima no Takataka 79  -> Kitajima no Daikou

    Hisayama no Mototaka -> Yakura no Motonori -> Yakura no Kazutaka

**One edge that is a judgement rather than a reading.** `Kitajima no Yoritaka 73`
sits in the same grid column as `Yakura no Kazutaka` directly above him, and the
sibling bar from Yoritaka 69 ends on that same column, so two lines land on one
point. Taken as **child of Yoritaka 69**, because he carries a Kitajima regnal
number and Yakura is a cadet house that the chart does not otherwise route the
headship through. What would settle it: the `{{familytree}}` source line for that
row, or Emma saying which.

## The Senge headship after 62 leaves the Senge column entirely

Read at full width, generations 61-74. The chart routes the Senge succession out
through two other houses and back, which is why the numbers in the Senge column
jump around:

    Hiraoka no Naotaka -> Hiraoka no Naokiyo -> Senge no Naokatsu 63
    Higashiyasunori    -> Higashianatsuu     -> Senge no Yoshikatsu 64
    Senge no Yoshikatsu 64
      Senge no Yoshihiro 65
      Higashiyoshiakira
    Higashiyoshiakira -> Higashisadanobu
    Akatsuka no Nagatoshi -> Senge no Motokatsu 66
    Senge no Motokatsu 66 -> Senge no Takanou 67 -> Senge no Takamitsu 68
                          -> Senge no Hiromitsu 72
    Sakusa no Jisei -> Senge no Munetoshi 71
    Senge no Munetoshi 71
      Senge no Toyomasa 73
      Senge no Toyomi 74

**Senge no Naokatsu 63 is on the wrong parent on Geni, and I put him there.**
`6000000227334689929` sits as a child of `Senge no Naonobu 59`, alongside Takatoshi 60
and Takakatsu 62. He was created in the 2026-08-19 run of this job, by me, from a
low-zoom reading of the chart's Senge column.

The chart puts him under **Hiraoka no Naokiyo**, and that has now been checked at a
resolution where the connector is unambiguous: a single vertical runs
`Hiraoka no Naotaka` -> `Hiraoka no Naokiyo` -> the `Senge no Naokatsu 63` box.
Takakatsu 62 under Naonobu 59 *is* what the chart draws, so only the one edge is wrong.

This was written up here first as "Geni disagrees with the chart, and the disagreement
is Emma's call". That was wrong twice over: it presented my own bad edit as a property
of her data, and it parked a fix I had caused on her. Emma, 2026-08-20:
*"Naokatsu 63 Senge is fucking hallucinated in his placement"*.

## The in-law columns are read UPWARD only

Emma, 2026-08-20: *"GO UP the in-laws line"*, and *"the in-laws line is absurd if you
go the other direction"*. The chart draws each in-law house as an **ancestor chain
feeding into one marriage** - Sasaki down to En'ya down to Kakunin, who marries
Yasutaka 52. Following those people *downward* on Geni leaves the chart immediately
and walks into the whole Sasaki clan, which the chart never claims anything about.

    Sasaki Yasukiyo
      Toda Yoshiyasu -> Takaoka Muneyoshi -> Ookunishinomikoto
      En'ya Yoriyasu
        En'ya Sadakiyo
        Kakunin            = Yasutaka 52's wife, so Takatoki 53's mother
      Takaoka Muneyasu

    Izumo no Masataka 50 -> Izumo no Yoshitaka 51 -> Izumo no Yasutaka 52

This is corroborated from the Geni side without any name being consulted: Geni gives
Takatoki 53 exactly two parents, `Yasutaka Izumo-kokuso` and `Kakujitsu ni En'ya`,
which is the position the chart puts Kakunin in.

**The repeated rows Emma warned about are visible here.** Chart rows 95-97 recur as
rows 99-101 - `En'ya Yoriyasu`, `En'ya Sadakiyo`, `Kakunin` and
`Takaoka Muneyoshi` / `Takao Muneyoshi` each appear twice, and the roster carries
both copies. They are one person each, not two, and a count of "people still to
create" that treats them as distinct is wrong by that many.

## Where the two sources disagree, position invents an identity

Worked example, 2026-08-20, caught by Emma: *"how the fuck did Hiraoka no Naokiyo get
forced in like that looks very sus"*.

The resolver paired `Hiraoka no Naokiyo` with a Geni profile called
`daughter of Kinunobu Koshi Koshi`. Checking rather than theorising: `Naotaka Hiraoka`
`6000000227334516908` has exactly one child, `Naokiyo Hiraoka` `6000000227334350078`,
so the downward edge was never in doubt and Naokiyo was there all along.

The bad pair came from the **upward** edge. The chart says
`Hiraoka no Naokiyo -> Senge no Naokatsu 63`. On Geni, the parent in that slot is
`daughter of Kinunobu Koshi Koshi`, whose three children are Takatoshi, Takakatsu and
Naokatsu Senge - she is **Naonobu 59's wife**, a person the chart does not draw. So
the slot held exactly one unclaimed profile and the position "forced" a pair that is
nonsense.

**The position was only forced because Geni holds a parent I put there wrongly** - the
Naokatsu 63 edit recorded above. So the hazard is not "the two sources disagree"; it is
that a bad edge on either side leaves exactly one open slot, and matching by position
will then fill it confidently with whoever happens to be standing there.

Two things stop this one recurring: a forced pair is rejected when the two names share
no token at all, which is the name used as a **veto** and never as a chooser; and
Naokiyo is now anchored by his real id, so the slot is not open to be filled.
