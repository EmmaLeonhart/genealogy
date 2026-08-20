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
