# ------------------------------------------------------------------------
# Q4411612 -- a mul label for the item Emma asked about.
#
# Emma, 2026-08-27: "Look over this item it just piques my curiosity whether we
#   can identify it on geni and potentially add a mul label
#   https://www.wikidata.org/wiki/Q4411612"
#
# Two questions, and they have different answers.
#
# THE MUL LABEL: yes, and it is uncontroversial. The item has NO mul and NO en.
#   `nb` and `da` both read "Svantepolk"; `sv` reads "Sviatopolk av obotriterna",
#   which is a name plus a disambiguator rather than a name. Two languages
#   agreeing on the bare form is what mul is for -- CLAUDE.md calls mul the
#   language-neutral label -- and nothing is overwritten, because there is
#   nothing there.
#
# IDENTIFYING HIM ON GENI: no, not from our data, and it is worth saying why
#   rather than guessing. Searching our tree for the name returns 19 people --
#   Sviatopolk of Kiev, Swantepolk II of Pomerania, several Svantepolksdotters --
#   and none of them is "of the Obotrites". A name match here would be exactly
#   the fuzzy matching this repo refuses.
#
#   The structural route exists and stops one step short. Wikidata records his
#   father as Q470177, Henry of Alt-Lubeck, and THAT item already carries
#   P2600 6000000007718311626 -- so his father's Geni profile is known. But
#   6000000007718311626 is not in our corpus, so we cannot see the sibling set
#   and cannot say which Geni profile is this son.
#
#   That makes it an export question, not a matching question: a Forest export
#   seeded on 6000000007718311626 would bring the family in and settle it by
#   structure. Recorded in queue.md rather than run here -- the Chrome extension
#   is not connected.
# ------------------------------------------------------------------------
#   Q4411612: set the mul label; the item has none, and nb and da both say this
Q4411612	Lmul	"Svantepolk"
