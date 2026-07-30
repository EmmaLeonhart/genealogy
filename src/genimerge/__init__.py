"""genimerge — one canonical genealogy out of many Geni GEDCOM exports.

The whole package rests on one fact about Geni's GEDCOM export: it writes the
Geni profile ID as the record xref itself::

    0 @I6000000087535357291@ INDI
    1 RFN geni:6000000087535357291

so records carry a stable primary key across exports and the merge never needs
to guess whether two ``Ola Nordmann``s are the same person.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
