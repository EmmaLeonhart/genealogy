# ------------------------------------------------------------------------
# Q141198548 -- Deokjang's WIFE, not a duplicate of him.
#
# Emma, 2026-08-29, was about to run  Q141198548|Lko|"부여덕장"  and stopped to
#   ask, because the two items looked like near-duplicates. She was right to stop:
#   부여덕장 is her HUSBAND'S name. Writing it on her asserts his identity on a
#   different, real woman.
#
# WHAT THE TREE ACTUALLY SAYS -- read from reports/derived-family.csv, three rows:
#
#   6000000186285688253  Buyeo Deokjang  father+mother, spouse …269, 3 children
#   6000000186285688269  덕장 부여        spouse …253, THE SAME 3 children, NO parents
#   6000000186285688286  Buyeo Taebi     father …253, mother …269
#
#   So they are husband and wife with three shared children, and she is the
#   mother of Buyeo Taebi. Not one person entered twice.
#
# WHY SHE CARRIES HIS NAME: she has no parents and no name of her own on Geni --
#   an unnamed wife entered to hold the marriage, with the husband's name written
#   on her. That is the NN population, and CLAUDE.md's algorithm covers it:
#   the marker stays in mul, and every other language gets a formulaic
#   description built from the nearest named relative.
#
# mul = "NN Buyeo" per Emma: the marker plus the house name, which is the part of
#   부여덕장 that is hers -- she married into Buyeo. The given name 덕장 is his.
#
# THE TEN LATIN LANGUAGES come from scripts/build-nn-label-batch.py's own table,
#   imported rather than restated, with the female word and the per-language
#   preposition it already encodes.
#
# ja/zh/ko ARE emitted here, which the table normally omits. CLAUDE.md: they are
#   excluded "only because the relative's name is usually not transliterated --
#   where it is, they are emitted." Here it is: Emma supplied his labels, ja and
#   zh 扶餘德璋 and ko 부여덕장. The Korean one is the corrected form of the very
#   statement she was about to run.
# ------------------------------------------------------------------------
#   Q141198548: mul label = NN plus the house name
Q141198548	Lmul	"NN Buyeo"
#   set the ca label
Q141198548	Lca	"esposa de Buyeo Deokjang"
#   set the da label
Q141198548	Lda	"hustru til Buyeo Deokjang"
#   set the de label
Q141198548	Lde	"Ehefrau von Buyeo Deokjang"
#   set the en label
Q141198548	Len	"wife of Buyeo Deokjang"
#   set the es label
Q141198548	Les	"esposa de Buyeo Deokjang"
#   set the it label
Q141198548	Lit	"moglie di Buyeo Deokjang"
#   set the nb label
Q141198548	Lnb	"hustru til Buyeo Deokjang"
#   set the nl label
Q141198548	Lnl	"echtgenote van Buyeo Deokjang"
#   set the pt label
Q141198548	Lpt	"esposa de Buyeo Deokjang"
#   set the sv label
Q141198548	Lsv	"maka till Buyeo Deokjang"
#   set the ja label
Q141198548	Lja	"扶餘德璋の妻"
#   set the zh label
Q141198548	Lzh	"扶餘德璋之妻"
#   set the ko label -- the corrected form of the statement she was about to run
Q141198548	Lko	"부여덕장의 아내"
