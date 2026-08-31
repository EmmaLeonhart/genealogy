# Minor edits on the items Emma has EDITED BUT NOT CREATED, so they land on her
#    watchlist. Emma, 2026-08-28: "These are a bit of a weak point for me since they are
#    potentially items that are not in my watchlist and might cause me issues."
#
#    Every edit here is ADDITIVE. A mul label is only set where the item has none, so
#    nothing she may have written by hand is overwritten -- CLAUDE.md: a label REPLACES.
#    Aliases are only added where our Geni label differs and is not already an alias.
#    No Aen is ever emitted. Non-human items she edited are left alone entirely.

# --- REMOVED 2026-08-31: four `Lmul` lines that would have written an ENGLISH label into `mul`.
#     Q6197518 is the worked case -- see reports/audit-q6197518.md. The comment on each read
#     "(it had none)", which was false for Q6197518: she set that mul by hand on 08-28 and this
#     batch overwrote it on 08-30. Checked live on 08-31: Q274606 and Q3743799 still have no mul
#     and would have received "Berengar I of Italy" and "Canute, Duke of Estonia"; Q101247444's
#     mul is already the clean "Ingegerd Svantepolksdotter" and the line would have replaced it
#     with the en form carrying "heiress, lady of Handeloo".
#     Each line carried the generator's own NOTE that the en label was a title rather than a
#     name, so the check fired and did not gate the emission.
#     The right mul for Q274606 and Q3743799 is a native form with the title stripped, which is
#     a naming decision and not made here.

#   Q284400: set the mul label to "Gisela" (it had none)
Q284400	Lmul	"Gisela"
#   Q467497: set the mul label to "Arne Garborg" (it had none)
Q467497	Lmul	"Arne Garborg"
#   Q4953376: set the mul label to "Helena Guttormsdatter" (it had none)
Q4953376	Lmul	"Helena Guttormsdatter"
#   Q5915800: set the mul label to "Knut Algotsson" (it had none)
Q5915800	Lmul	"Knut Algotsson"
#   Q109266155: add a mul alias "Magdalena Johansdotter Bure" (its mul reads "Magdalena Bureus")
Q109266155	Amul	"Magdalena Johansdotter Bure"
#   Q116150299: add a mul alias "Jon Reinmodsen" (its mul reads "Jon Reimatsen")
Q116150299	Amul	"Jon Reinmodsen"
#   Q116150300: add a mul alias "Cecilie Ebbesdatter Hvide" (its mul reads "Cecilie Ebbesdatter")
Q116150300	Amul	"Cecilie Ebbesdatter Hvide"
#   Q2183430: SKIPPED an alias "Bengta Ebbesdotter Ebbesdatter Galen Queen of Sweden" -- it carries an office word, and a
#      title is not a name (CLAUDE.md). Nothing emitted for this item.
#   Q3143008: add a mul alias "Karen Hulda Bergersen" (its mul reads "Karen Hulda Garborg")
Q3143008	Amul	"Karen Hulda Bergersen"
#   Q633094: add a mul alias "Johannes Tomasson" (its mul reads "Johannes Bureus")
Q633094	Amul	"Johannes Tomasson"
#   Q19657284 Buyeo Deokjang: P2600 Geni.com profile ID = 6000000186285688253
#      Found STRUCTURALLY, not by name: it is the spouse of Geni 6000000186285688269
#      (덕장 부여), the profile behind Q141198548, and the batch already emitted
#      Q19657284 P26 spouse = that item. The pairing was known; the id was never written.
Q19657284	P2600	"6000000186285688253"
#   Q12598947 Buyeo Taebi: P2600 Geni.com profile ID = 6000000186285688286
#      Same basis: it is a child of Geni 6000000186285688269, and the batch emitted
#      Q12598947 P40 child = that item.
Q12598947	P2600	"6000000186285688286"
