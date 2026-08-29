# ------------------------------------------------------------------------
# ITEMS EMMA EDITED BUT DID NOT CREATE -- one real edit each, to put them on
#   her watchlist.
#
# Emma, 2026-08-27: "Look over all of the items that I have edited but did no
#   create. These are a bit of a weak point for me since they are potentially
#   items that are no in my watchlist and might cause me issues. Create a batch
#   of quickstatements that does some kind of minor edit on all of them if
#   possible preferable settin their mul labels or something"
#
# THE 27 ARE FROM THE LEDGER, not guessed: refresh-garborg-ledger.py reads the
#   `new` flag on her contributions and marks the rest "(P2600 added to an
#   existing item)". Those 27 are items she touched without creating.
#
# "PREFERABLY SETTING THEIR MUL LABELS" IS ONLY POSSIBLE FOR 6 OF THEM, and the
#   reason is worth having in front of you:
#
#     6   have no mul at all      -> Lmul, additive, done below
#    10   mul differs from ours   -> NOT TOUCHED. These are other people's
#                                    labels, and her own rule is that we may
#                                    overwrite only a label we added. The list
#                                    includes Q467497 "Arne Garborg" against our
#                                    "Aadne Eivindson Garborg" -- the case
#                                    CLAUDE.md names as the thing not to do --
#                                    and Q12598947 "Buyeo Taebi", which is her
#                                    OWN word ordering from entity_resolution.md.
#     9   mul already matches     -> setting it again is a no-op on Wikidata, so
#                                    it makes no edit and no watchlist entry.
#                                    Listed at the bottom as the ones this batch
#                                    cannot help.
#     2   we hold no label        -> nothing to offer.
#
# SO THE 10 GET AN ALIAS INSTEAD. An Amul carrying our form is additive, never
#   destructive, is a real edit (hence a watchlist entry), and is independently
#   useful: Help:Aliases says aliases exist to find entities in searches, and
#   somebody looking for "Aadne Eivindson Garborg" currently cannot find him.
#
# 16 items get an edit. Her standing cap of 15 label edits a batch is about the
#   DAILY Garborg batch; this is the one-off she asked for. Split it if you would
#   rather stay under the cap -- the file is ordered so the 6 label additions
#   come first.
# ------------------------------------------------------------------------


# --- 6 items with no mul label at all: add one -------------------------
#   Q16650154 Ericus Olai Plantin: set the mul label
Q16650154	Lmul	"Ericus Olai Plantin"
#   Q1814297 Carl Erik Mannerheim: set the mul label
Q1814297	Lmul	"Carl Erik Mannerheim"
#   Q274606 Berengar I of Italy: set the mul label
Q274606	Lmul	"Berengar I margrave of Friuli, king of Italy"
#   Q3743799 Canute, Duke of Estonia: set the mul label
Q3743799	Lmul	"Knut Valdemarsson Duke of Estland, Blekinge and Lolland"
#   Q466257 Rozala of Italy: set the mul label
Q466257	Lmul	"Rozala d'Ivrea"
#   Q5975022 Lars Augustin Mannerheim: set the mul label
Q5975022	Lmul	"Lars August Mannerheim"

# --- 10 whose mul is someone else's: add our form as an ALIAS ----------
#   Q109266155: Wikidata says 'Magdalena Bureus'; add our 'Magdalena Johansdotter Bure' as a searchable alias
Q109266155	Amul	"Magdalena Johansdotter Bure"
#   Q116150299: Wikidata says 'Jon Reimatsen'; add our 'Jon Reinmodsen' as a searchable alias
Q116150299	Amul	"Jon Reinmodsen"
#   Q116150300: Wikidata says 'Cecilie Ebbesdatter'; add our 'Cecilie Ebbesdatter Hvide' as a searchable alias
Q116150300	Amul	"Cecilie Ebbesdatter Hvide"
#   Q12598947: Wikidata says 'Buyeo Taebi'; add our 'Taebi Buyeo' as a searchable alias
Q12598947	Amul	"Taebi Buyeo"
#   Q19657284: Wikidata says 'Buyeo Deokjang'; add our 'Deokjang Buyeo' as a searchable alias
Q19657284	Amul	"Deokjang Buyeo"
#   Q2183430: Wikidata says 'Bengta Ebbesdotter Ebbesdatter Hvide'; add our 'Bengta Ebbesdotter Ebbesdatter Hvide Queen of Sweden' as a searchable alias
Q2183430	Amul	"Bengta Ebbesdotter Ebbesdatter Hvide Queen of Sweden"
#   Q284400: Wikidata says 'Gisela'; add our 'Giséle de Cysoing' as a searchable alias
Q284400	Amul	"Giséle de Cysoing"
#   Q467497: Wikidata says 'Arne Garborg'; add our 'Aadne Eivindson Garborg' as a searchable alias
Q467497	Amul	"Aadne Eivindson Garborg"
#   Q6197518: Wikidata says 'Svantepolk Knutsson'; add our 'Svantepolk Knutsson Knutsson Skarsholmsätten' as a searchable alias
Q6197518	Amul	"Svantepolk Knutsson Knutsson Skarsholmsätten"
#   Q633094: Wikidata says 'Johannes Bureus'; add our 'Johannes Thomæ Agrivillensis Bureus' as a searchable alias
Q633094	Amul	"Johannes Thomæ Agrivillensis Bureus"

# --- this batch cannot help these, and they are listed so nobody looks ---
#     for them later:
#   Q101247444 Ingegerd Svantepolksdotter of Viby, heiress, lady of Händelöö: mul already says exactly what we would write -- a no-op
#   Q10608167 Olaus Petri Niurenius: mul already says exactly what we would write -- a no-op
#   Q11959067 Arne Olaus Fjørtoft Garborg: mul already says exactly what we would write -- a no-op
#   Q138474188 Hans Syvertsen Nyvold: mul already says exactly what we would write -- a no-op
#   Q16165426 Catharina Burea: mul already says exactly what we would write -- a no-op
#   Q3143008 Hulda Garborg: mul already says exactly what we would write -- a no-op
#   Q4953376 Helena Guttormsdatter: mul already says exactly what we would write -- a no-op
#   Q4981287 Benedicta of Bjelbo: mul already says exactly what we would write -- a no-op
#   Q5915800 Knut Algotsson: mul already says exactly what we would write -- a no-op
#   Q10411463 Andreas Olai: we hold no label for this person
#   Q109660986 Eva Walaas: we hold no label for this person
