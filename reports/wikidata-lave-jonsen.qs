# ------------------------------------------------------------------------
# Q141189080 -- "Lave" becomes "Lave Jonsen", in every language the item has.
#
# Emma, 2026-08-28: "I think this person https://www.wikidata.org/wiki/Q141189080
#   should be corrected to 'Lave Jonsen' in all languages and on geni. Just havin
#   a first name is weird and has no rationale, they should be given the
#   patronymic 'Jonsen' too"
#
# The patronymic is CHECKED, not assumed. His father on our tree is Geni
# 5101295410550070399 = Q116150299, whose live label is "Jon Reimatsen" -- so the
# son of Jon is Jonsen. Fetched live 2026-08-29 with full_entities, one batched
# request, because a correction built on a snapshot rewrites work she has already
# done by hand.
#
# What the item held at that moment, and it is all four of these that change:
#   en  Lave      mul Lave      ja ラーヴェ      zh 拉弗
# No aliases, no descriptions.
#
# ja/zh come from reports/garborg-name-transliterations.tsv, which already holds
# both tokens: Lave -> ラーヴェ / 拉弗, Jonsen -> ヨンセン / 永森 (composed Jon + -sen).
# So the CJK forms are the existing label plus the existing patronymic token, not
# a fresh rendering of the whole name.
#
# The outgoing label goes out as an Amul FIRST. A label REPLACES, and CLAUDE.md
# is explicit that the value being overwritten is preserved as an alias on the
# line above -- "Lave" is also a plausible thing to search for on its own.
#
# NOT DONE HERE: the Geni half of her instruction. Editing Geni is an outward
# action on a live site and CLAUDE.md currently says Geni is not edited; that
# half is a separate queue item awaiting her word.
# ------------------------------------------------------------------------

#   Q141189080: preserve the outgoing label as an alias before replacing it
Q141189080	Amul	"Lave"
#   set the mul label to "Lave Jonsen"
Q141189080	Lmul	"Lave Jonsen"
#   set the en label to "Lave Jonsen"
Q141189080	Len	"Lave Jonsen"
#   set the ja label to "ラーヴェ・ヨンセン"
Q141189080	Lja	"ラーヴェ・ヨンセン"
#   set the zh label to "拉弗·永森"
Q141189080	Lzh	"拉弗·永森"
