# ------------------------------------------------------------------------
# Q4411612 -- identified on Geni, and given the mul label it lacked.
#
# Emma, 2026-08-27: "Look over this item it just piques my curiosity whether we
#   can identify it on geni and potentially add a mul label
#   https://www.wikidata.org/wiki/Q4411612"
#
# IDENTIFIED: Geni 6000000007716541890, "Swentepolk".
#
# THREE INDEPENDENT LINES AGREE, and none of them is a name match:
#
#   1. THE FATHER, by identifier. Wikidata gives Q4411612's father as Q470177,
#      and THAT item already carries P2600 6000000007718311626 -- asserted by
#      Wikidata, not by us. That Geni profile is "Henrik 31 th king of the
#      Heruli & Wenden" (1059-1126), which is the same person as Henry of
#      Alt-Lubeck: son of Gottschalk and Sigrid Estridsen.
#
#   2. POSITION IN A CLOSED SET. Wikidata records Q470177 as having exactly two
#      sons: Q4411612 Svantepolk and Q28045690 Canute. Geni's Henrik lists his
#      children as Swentepolk, Knud, Mistue and Waldemar, and Swentepolk's own
#      page reads "Brother of Knud". Two Wikidata sons against two Geni sons of
#      the same recorded father, matching pairwise.
#
#   3. THE DEATH YEAR. Wikidata 1129, Geni 1128 -- one year apart, which is
#      ordinary for a 12th-century Wendish prince and is corroboration rather
#      than a match on its own.
#
#   4. THE DYNASTY. Father and son both carry P53 family = Q467599, the
#      Nakonid dynasty, and both carry P97 noble title Q273613.
#
# WHY NOBODY CAN GOOGLE HIM. Q4411612 has NO English label and NO English
#   Wikipedia. Its labels are ru Svyatopolk, pl Swietopelk, sv "Sviatopolk av
#   obotriterna", cs "Svatopluk Obodritsky", nb/da Svantepolk; sitelinks exist
#   only on it, pl, ru, sv and uk. The descriptions agree across five languages:
#   "reigning prince of the Obotrites".
#
#   THE OBOTRITES ARE A PEOPLE, NOT A PERSON -- a West Slavic (Wendish)
#   confederation on the Baltic, around modern Mecklenburg. Geni calls the
#   father "31 th king of the Heruli & WENDEN", which is the German word for the
#   same group, so Geni and Wikidata describe one people in two vocabularies.
#   That is why nothing on the Geni page says "Obotrite" and why the word was
#   mine rather than either source's.
#
# WHAT WAS REJECTED: searching our tree for the name returns 19 people carrying
#   Svantepolk or Sviatopolk -- Kiev, Pomerania, several Svantepolksdotters --
#   and not one is "of the Obotrites". Picking from that list would have been
#   the fuzzy matching this repo refuses. The father's P2600 is what made this
#   an identifier join instead.
#
# NEITHER IS IN OUR CORPUS. 6000000007716541890 and 6000000007718311626 both
#   appear in zero exports, so the pairing is recorded here and the tree learns
#   it only when an export reaches them.
#
# P2600 FIRST, THEN THE LABEL -- CLAUDE.md: "The Geni ID is added first, and
#   then all the Geni-derived stuff is added after."
#
# The mul label: the item had NO mul and NO en. `nb` and `da` both read
#   "Svantepolk"; `sv` reads "Sviatopolk av obotriterna", a name plus a
#   disambiguator. Two languages agreeing on the bare form is what mul is for,
#   and nothing is overwritten because nothing is there.
# ------------------------------------------------------------------------
#   Q4411612: P2600 Geni.com profile ID = 6000000007716541890 Swentepolk
Q4411612	P2600	"6000000007716541890"	P1810	"Swentepolk"
#   Q4411612: set the mul label; the item has none, and nb and da both say this
Q4411612	Lmul	"Svantepolk"
#   Q4411612: set the en label from the GENI form. Emma, 2026-08-29: "make an
#     english label from geni stuff". Geni spells him Swentepolk, one letter from
#     the mul above, which is nb/da Svantepolk. Both are kept and sourced rather
#     than one being flattened into the other: mul is the cross-language
#     consensus, en is what our own source calls him. Collapse them if you would
#     rather they agreed.
Q4411612	Len	"Swentepolk"
