# Remove a P2600 that names the SON on an item describing the FATHER.
#
# Emma, 2026-08-26, on both of these: "Remove the son's P2600 from the item."
#
# These are the only two of the 70 multi-P2600 pairs where our tree says one profile is the
# other's PARENT -- a generation collapsed into a single item. The other 68 are shapes
# CLAUDE.md already calls ordinary: 41 unrelated (the Zerubbabel shape) and 27 siblings.
#
# A leading `-` removes the statement. QUEUED, NEVER RUN -- editing starts 2026-09-01.
#
# --- Q104755784, labelled "Ruben Wulff" -------------------------------------------------
# Ruben Wulff        6000000035017580401  b.1748 d.1828  father Seeb Wulff,
#                    spouse Beata Bela Levin, children Lovisa/Wolf/Amalia/Levi Rubenson
# Wolf Rubensson     5477503367560083505  b.1796 d.1860  HIS SON -- father Ruben Wulff,
#                    spouse Jenny Levin, children Albert/Betty/Joseph/Rosalia Rubenson
# Forty-eight years apart, different spouses, different children. The item is labelled for
# the father, so the son's id is the one that does not belong.
-Q104755784	P2600	"5477503367560083505"

# --- Q96985053, labelled "John Loomis" --------------------------------------------------
# John Loomis  6000000006376446567  b.1622 d.1688  spouse Elizabeth Scott of Hartford,
#              sixteen recorded children
# John Loomis  6000000003617703553  b.1649 d.1715  ONE OF THOSE CHILDREN -- his father is
#              the first John and his mother is Elizabeth Scott
# Father and son sharing a name, one generation apart. The item carries the father's spouse
# and children, so the son's id is the one that does not belong.
-Q96985053	P2600	"6000000003617703553"
