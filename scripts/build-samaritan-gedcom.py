"""Emit a GEDCOM of the Samaritan genealogy the published sources give.

**This is not a Geni export and must never be mistaken for one.** It carries no
`RFN geni:` lines and lives outside `exports/`, so the corpus tests
(`tests/test_gedcom_real_exports.py`, which asserts the four Geni xref prefixes)
never see it. It is source-derived material for Emma to open in a tree editor and
enter into Geni by hand.

Everything here comes from `reports/samaritan-priesthood.md` and
`reports/samaritan-families.md`, which are transcriptions of:

  * A.B. — The Samaritan News / The Samaritan Update, March–April 2012,
    "The High Priesthood and the Israelite Samaritan Priests", Benyamim Tsedaka
  * "Ratson b. Benyamim Tsedaka — 90 Years to His Birthday", Benyamim Tsedaka, 2012
  * The Israelite Samaritan Information Institute's families page
  * "The Tsedaka Family", theSamaritanUpdate.com, 2008

**Placeholders are marked as placeholders.** The 'Abtah line between Itamar ben
Aaron and Shalma has no names in any source; those people are emitted as unnamed
individuals whose NOTE says so, with the generation count borrowed from the
parallel Phinhas line. No name is ever invented.

    py scripts/build-samaritan-gedcom.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = REPO / "gedcom" / "samaritan-sources.ged"

#: Generations father-to-son in the parallel Phinhas line, Aaron to 1624, as the
#: community records it. The yardstick for the 'Abtah line's unnamed stretch.
PHINHAS_GENERATIONS = 112

SRC_AB = ("A.B. - The Samaritan News / The Samaritan Update, March-April 2012, "
          "'The High Priesthood and the Israelite Samaritan Priests', "
          "by Benyamim Tsedaka")
SRC_RATSON = ("'Ratson b. Benyamim Tsedaka - 90 Years to His Birthday', "
              "Benyamim Tsedaka, 2012")
SRC_FAMILIES = "Israelite Samaritan Information Institute, families page"
SRC_TSEDAKA08 = "'The Tsedaka Family', theSamaritanUpdate.com, 2008"

PLACEHOLDER_NOTE = (
    "PLACEHOLDER - no source names this person. Position derived from the "
    "generation count of the parallel Phinhas line (112 generations, Aaron to "
    "1624). Do not treat the count as measured for this line."
)


class Tree:
    def __init__(self) -> None:
        self.people: list[dict] = []
        self.families: list[dict] = []
        self.by_key: dict[str, str] = {}

    def person(self, key, name=None, sex="M", birt=None, deat=None,
               occu=None, note=None, title=None) -> str:
        xref = f"I{len(self.people) + 1}"
        self.by_key[key] = xref
        self.people.append({"xref": xref, "key": key, "name": name, "sex": sex,
                            "birt": birt, "deat": deat, "occu": occu,
                            "note": note, "title": title})
        return xref

    def child_of(self, parent_key, child_key) -> None:
        self.families.append({"husb": parent_key, "chil": [child_key]})

    def render(self) -> str:
        # collapse families that share a father
        merged: dict[str, list[str]] = {}
        for f in self.families:
            merged.setdefault(f["husb"], []).extend(f["chil"])

        out = [
            "0 HEAD",
            "1 SOUR genimerge",
            "2 NAME genimerge samaritan-sources",
            "2 CORP Emma Leonhart",
            "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED",
            "1 CHAR UTF-8",
            "1 NOTE Israelite Samaritan genealogy transcribed from published sources.",
            "2 CONT NOT a Geni export. No profile IDs. See reports/samaritan-priesthood.md",
            "2 CONT and reports/samaritan-families.md for the sources and the reasoning.",
            "2 CONT Individuals with no NAME are explicit placeholders; read their NOTE.",
        ]

        fam_of_child: dict[str, str] = {}
        fam_records = []
        for i, (husb, kids) in enumerate(merged.items(), 1):
            fx = f"F{i}"
            fam_records.append((fx, husb, kids))
            for k in kids:
                fam_of_child[k] = fx

        fams_of_parent: dict[str, list[str]] = {}
        for fx, husb, _ in fam_records:
            fams_of_parent.setdefault(husb, []).append(fx)

        for p in self.people:
            out.append(f"0 @{p['xref']}@ INDI")
            if p["name"]:
                out.append(f"1 NAME {p['name']}")
            else:
                out.append("1 NAME //")
            out.append(f"1 SEX {p['sex']}")
            if p["title"]:
                out.append(f"1 TITL {p['title']}")
            if p["birt"]:
                out.append("1 BIRT")
                out.append(f"2 DATE {p['birt']}")
            if p["deat"]:
                out.append("1 DEAT")
                out.append(f"2 DATE {p['deat']}")
            if p["occu"]:
                out.append(f"1 OCCU {p['occu']}")
            if p["note"]:
                lines = p["note"].split("\n")
                out.append(f"1 NOTE {lines[0]}")
                for extra in lines[1:]:
                    out.append(f"2 CONT {extra}")
            for fx in fams_of_parent.get(p["key"], []):
                out.append(f"1 FAMS @{fx}@")
            if p["key"] in fam_of_child:
                out.append(f"1 FAMC @{fam_of_child[p['key']]}@")

        for fx, husb, kids in fam_records:
            out.append(f"0 @{fx}@ FAM")
            out.append(f"1 HUSB @{self.by_key[husb]}@")
            for k in kids:
                out.append(f"1 CHIL @{self.by_key[k]}@")

        out.append("0 TRLR")
        return "\n".join(out) + "\n"


def main() -> int:
    t = Tree()

    # ---- the 'Abtah / Haftawi priestly line -------------------------------
    t.person("aaron", "Aaron /ben Amram/", occu="High Priest",
             note=f"The priest, brother of Moses. Head of both priestly lines.\n"
                  f"Source: {SRC_AB}")
    t.person("itamar", "Itamar /ben Aaron/", occu="priest",
             note="Younger son of Aaron. The 'Abtah (Haftawi) priests descend from "
                  "him; the Phinhas high-priestly line descends from his brother\n"
                  "Eleazar. Source: " + SRC_AB)
    t.child_of("aaron", "itamar")

    named_count = 6  # aaron, itamar, shalma, abed-ela, yusef, tabia
    gaps = PHINHAS_GENERATIONS - named_count - 1  # one gap sits lower down
    prev = "itamar"
    for i in range(1, gaps + 1):
        key = f"gap{i:03d}"
        t.person(key, None, note=PLACEHOLDER_NOTE)
        t.child_of(prev, key)
        prev = key

    t.person("shalma-damascus", "Shalma //", occu="priest",
             note="Father of 'Abed Ela. Named only through his son's patronymic.\n"
                  "Source: " + SRC_AB)
    t.child_of(prev, "shalma-damascus")

    t.person("abed-ela", "'Abed Ela /ben Shalma/", occu="priest, poet, translator",
             title="President of the House of 'Abtah",
             note="Forefather of the current Israelite Samaritan priestly families.\n"
                  "Born and active in Damascus, then moved to Nablus to serve the\n"
                  "high priests. Great poet, translator and teacher of religion.\n"
                  "'Abtah means Translator (Arabic: Haftawi) - the Itamar priests\n"
                  "rendered the Phinhas High Priest's Hebrew reading of the\n"
                  "Pentateuch into Aramaic, and are named for that duty.\n"
                  "Source: " + SRC_AB)
    t.child_of("shalma-damascus", "abed-ela")

    t.person("gap-abed-yusef", None,
             note="PLACEHOLDER - carries the distance between 'Abed Ela ben Shalma\n"
                  "and Yusef, which the source does not state. It may be zero: "
                  "'Abed Ela\nmay be Yusef's own father. Do not treat this "
                  "generation as attested.")
    t.child_of("abed-ela", "gap-abed-yusef")

    t.person("yusef", "Yusef //", occu="priest",
             note="Father of Tabia. Named in the patronymic of the first Itamar-line\n"
                  "High Priest: 'the priest Tsedaka b. Tabia b. Yusef'.\n"
                  "Source: " + SRC_AB)
    t.child_of("gap-abed-yusef", "yusef")

    t.person("tabia", "Tabia /ha'Abta'i/", occu="priest",
             note="Father of Tsedaka b. Tabia, first High Priest of the Itamar line\n"
                  "(1624). On Geni as profile 6000000220294810877, where he is the\n"
                  "root of a component of 33 people disconnected from the main tree.\n"
                  "Source: " + SRC_AB)
    t.child_of("yusef", "tabia")

    # ---- the Itamar high priests, 1624-2010 -------------------------------
    # Descent only where the source's patronymics state it. The office passes to
    # "the eldest priest of his brothers", NOT father to son, so office order is
    # deliberately not rendered as descent.
    hp = [
        ("hp-tsedaka", "Tsedaka /ben Tabia/", "1624-1650", "tabia"),
        ("hp-yitzhaq1", "Yitzhaq /ben Tsedaka/", "1650-1694", "hp-tsedaka"),
        ("hp-abraham", "Abraham /ben Yitzhaq/", "1694-1732", "hp-yitzhaq1"),
        ("hp-levi", "Levi /ben Abraham/", "1733-1752", "hp-abraham"),
        ("hp-tabia2", "Tabia /ben Yitzhaq/", "1752-1787", "hp-abraham"),
        ("hp-shalma", "Shalma /ben Tabia/", "1798-1855", "hp-tabia2"),
        ("hp-amram1", "'Amram /ben Shalma/", "1855-1874", "hp-shalma"),
        ("hp-jacob1", "Jacob /ben Aaron/", "1874-1916", "hp-aaron-b-shalma"),
        ("hp-yitzhaq2", "Yitzhaq /ben 'Amram/", "1916-1932", "hp-amram1"),
        ("hp-matzliach", "Matzliach /ben Phinhas/", "1933-1943", "hp-phinhas-b-yitzhaq"),
        ("hp-abisha", "Abisha /ben Phinhas/", "1943-1961", "hp-phinhas-b-yitzhaq"),
        ("hp-amram2", "'Amram /ben Yitzhaq/", "1961-1980", "hp-yitzhaq2"),
        ("hp-asher", "Asher /ben Matzliach/", "1980-1982", "hp-matzliach"),
        ("hp-phinhas2", "Phinhas /ben Matzliach/", "1982-1984", "hp-matzliach"),
        ("hp-jacob2", "Jacob /ben 'Azzi/", "1984-1987", "hp-azzi"),
        ("hp-yusef2", "Yusef /ben Ab-Hisda/", "1987-1998", "hp-abhisda"),
        ("hp-levi2", "Levi /ben Abisha/", "1998-2001", "hp-abisha"),
        ("hp-shalom", "Shalom /ben 'Amram/", "2001-2004", "hp-amram2"),
        ("hp-eleazar", "Eleazar /ben Tsedaka/", "2004-2010", "hp-tsedaka-b-yitzhaq"),
        ("hp-aaron2", "Aaron /ben Ab-Hisda/", "2010-", "hp-abhisda"),
    ]
    # intermediate men named only as patronymics in the succession list
    for key, name, note in [
        ("hp-aaron-b-shalma", "Aaron /ben Shalma/", "Named in his son's patronymic."),
        ("hp-phinhas-b-yitzhaq", "Phinhas /ben Yitzhaq/",
         "Named in his sons' patronymics. Eponym of the 'House of Phinhas', the\n"
         "largest of the three 'Abtah branches."),
        ("hp-azzi", "'Azzi /ben Jacob/", "Named in his son's patronymic."),
        ("hp-abhisda", "Ab-Hisda /ben Jacob/",
         "Named in his sons' patronymics; father of two High Priests."),
        ("hp-tsedaka-b-yitzhaq", "Tsedaka /ben Yitzhaq/", "Named in his son's patronymic."),
    ]:
        t.person(key, name, occu="priest", note=note + "\nSource: " + SRC_AB)

    for key, name, term, father in hp:
        extra = ""
        if key == "hp-shalma":
            extra = ("\nBorn 1783: he was four years old when his father Tabia died "
                     "in 1787,\nand was educated by the Samaritan sages until he was "
                     "fifteen.")
        t.person(key, name, occu="High Priest",
                 title=f"Samaritan High Priest {term}",
                 birt="1783" if key == "hp-shalma" else None,
                 note=f"Samaritan High Priest, {term}. The office passes to the "
                      f"eldest priest\nof his brothers, not father to son, so the "
                      f"order of office is not descent.{extra}\nSource: {SRC_AB}")
        if father in t.by_key:
            t.child_of(father, key)

    # ---- the Phinhas line's end ------------------------------------------
    t.person("ph-eleazar", "Eleazar //", occu="priest",
             note="Named in his grandson's patronymic.\nSource: " + SRC_AB)
    t.person("ph-phinhas", "Phinhas /ben Eleazar/", occu="priest",
             note="Named in his son's patronymic.\nSource: " + SRC_AB)
    t.child_of("ph-eleazar", "ph-phinhas")
    t.person("ph-shalmaiah", "Shalmaiah /ben Phinhas/", occu="High Priest",
             deat="1624", title="Samaritan High Priest",
             note="The LAST High Priest of the family of Phinhas. Died 1624 after\n"
                  "serving eleven years, leaving only one daughter, which ended the\n"
                  "line of Eleazar son of Aaron. He disappeared travelling from\n"
                  "Nablus to the Samaritans of Gaza; the 17th-century poet Marchiv\n"
                  "ben Jacob wrote to Europe that 'the last Rabban died in our time'.\n"
                  "Source: " + SRC_AB)
    t.child_of("ph-phinhas", "ph-shalmaiah")
    t.person("ph-daughter", None, sex="F",
             note="The only child of Shalmaiah ben Phinhas, and the reason the\n"
                  "Phinhas high-priestly line ended in 1624. Unnamed in the source.\n"
                  "Source: " + SRC_AB)
    t.child_of("ph-shalmaiah", "ph-daughter")

    # ---- Tsedaka Hassafari ------------------------------------------------
    t.person("safar", "Safar /ben Jacob/",
             note="Founder of the Tsedaka Hassafari household, tribe of Menasseh.\n"
                  "Lived in the 14th century CE.\nSource: " + SRC_FAMILIES)
    t.person("abzauta", "Ab-Za'uta //",
             note="Named through his sons' patronymics.\nSource: " + SRC_FAMILIES)
    t.person("tsedaka-abzauta", "Tsedaka /ben Ab-Za'uta/",
             note="18th-century forefather. The family took the name Tsedaka after\n"
                  "him when it moved to Jaffa in the early 20th century.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("abzauta", "tsedaka-abzauta")
    t.person("tabia-abzauta", "Tabia /ben Ab-Za'uta/", occu="poet, commentator, governor",
             note="A great poet and commentator who served as governor of Jaffa in\n"
                  "the 18th century. Listed with the tribe of Benyamin, while his\n"
                  "apparent brother Tsedaka is listed with Menasseh - the source does\n"
                  "not reconcile this, and the shared patronymic may be coincidence.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("abzauta", "tabia-abzauta")

    t.person("marchiv-t", "Marchiv //",
             note="Father of Abraham ben Marchiv. Named through the patronymic.\n"
                  "Source: " + SRC_TSEDAKA08)
    t.person("abraham-marchiv", "Abraham /ben Marchiv/", occu="writer, merchant",
             deat="1928",
             note="Moved from Shechem (Nablus) to Jaffa: failed 1894 and 1902,\n"
                  "succeeded 1905. Eight children. The move broke the community's\n"
                  "isolation in Nablus and the settlement he founded now holds half\n"
                  "the nation. A prominent literary figure of the household in the\n"
                  "19th century. Died 1928; his sons moved to Tel Aviv, then Holon\n"
                  "in 1951.\nSources: " + SRC_TSEDAKA08 + "; " + SRC_FAMILIES)
    t.child_of("marchiv-t", "abraham-marchiv")
    t.person("yefet-abraham", "Yefet /ben Abraham/", deat="1982",
             occu="head of the Samaritans outside Shechem",
             note="Established the Samaritan neighbourhood in Holon and directed its\n"
                  "development; bought the sandy ground the community first camped on\n"
                  "in 1951. Head of the Samaritans outside Shechem until his death in\n"
                  "1982.\nSources: " + SRC_FAMILIES + "; " + SRC_TSEDAKA08)
    t.child_of("abraham-marchiv", "yefet-abraham")
    t.person("batia", "Batia /bat Yefet/", sex="F", birt="ABT 1926",
             occu="teacher, school principal in the Dan District",
             note="First daughter of Yefet ben Abraham. About four years younger than\n"
                  "her husband Ratson, whom she married in 1943, moving from Tel Aviv\n"
                  "to Nablus. Completed teachers' seminary and became a school\n"
                  "principal in the Dan District. The best-documented Samaritan woman\n"
                  "found in these sources.\nSource: " + SRC_RATSON)
    t.child_of("yefet-abraham", "batia")

    t.person("shelach", "Shelach //",
             note="Named through his sons' patronymics.\nSource: " + SRC_RATSON)
    t.person("asher-shelach", "Asher /ben Shelach/",
             note="Uncle of Ratson, and the man who raised him.\nSource: " + SRC_RATSON)
    t.child_of("shelach", "asher-shelach")
    t.person("benyamim-shelach", "Benyamim //", occu="shopkeeper",
             note="Father of Ratson. Kept a materials shop in Nablus market; an eye\n"
                  "illness ended his work, which forced Ratson out of school to help.\n"
                  "Source: " + SRC_RATSON)
    t.child_of("shelach", "benyamim-shelach")
    t.person("ratson", "Ratson /ben Benyamim/", birt="22 FEB 1922", deat="20 JAN 1990",
             occu="writer, poet, reader of the Law, singer",
             note="Born Nablus. Read the entire Torah at six; sang his first poem\n"
                  "before the worshippers at eight. Married Batia bat Yefet in 1943.\n"
                  "Moved to Tel Aviv 1951 under the Israel-Jordan family unification\n"
                  "agreement, then Holon 1955. Ran a camping-equipment business from\n"
                  "the early 1970s. Prof. Zeev Ben-Hayyim called him 'my teacher and\n"
                  "mentor' and 'the sea of knowledge and traditions of the Samaritan\n"
                  "Community'; Prof. Dov Noy called him the reviver of the Samaritan\n"
                  "cultural renaissance. Recorded 400 hours of Samaritan tradition.\n"
                  "Died on Shabbat, 20 January 1990.\nSource: " + SRC_RATSON)
    t.child_of("benyamim-shelach", "ratson")
    t.person("benyamim-ratson", "Benyamim /ben Ratson/", birt="1944",
             occu="historian, editor",
             note="Born Nablus 1944. With his brother Yefet founded the bi-weekly\n"
                  "A.B. - The Samaritan News in December 1969, and has been its chief\n"
                  "editor since. Opened the A.B. Institute of Samaritan Studies at his\n"
                  "home in Holon in 1981. Author of the sources this file is built\n"
                  "from.\nSources: " + SRC_FAMILIES + "; " + SRC_RATSON)
    t.child_of("ratson", "benyamim-ratson")
    t.person("yefet-ratson", "Yefet /ben Ratson/", occu="editor",
             note="With his brother Benyamim founded A.B. - The Samaritan News in\n"
                  "December 1969.\nSource: " + SRC_RATSON)
    t.child_of("ratson", "yefet-ratson")

    t.person("gamliel", "Gamliel //",
             note="Named through his son's patronymic.\nSource: " + SRC_FAMILIES)
    t.person("yisrael-gamliel", "Yisrael /ben Gamliel/", birt="1932",
             occu="sage, printer of Samaritan texts",
             note="Born 1932. Worked at the Israeli Society for the Production of\n"
                  "Coins and Medals. Published Samaritan texts, prayer books and a\n"
                  "detailed edition of the Samaritan Pentateuch; long association with\n"
                  "Prof. Zeev Ben-Hayyim and Prof. Abraham Tal. With Ratson and\n"
                  "Abraham ben Marchiv Hamarchivi printed copied manuscripts for\n"
                  "community use.\n"
                  "HAS FOUR SONS, ALL OF WHOM MARRIED JEWISH WOMEN WHO JOINED THE\n"
                  "COMMUNITY - his own words to Sean Ireton. None of the four sons\n"
                  "and none of the four wives is named in any source found. Those\n"
                  "eight people are the most promising route from this genealogy to\n"
                  "the wider world tree.\n"
                  "Note also: Ireton calls him a Cohen (priestly), while the\n"
                  "Institute places him in Tsedaka Hassafari, tribe of Menasseh.\n"
                  "Unresolved.\nSources: " + SRC_FAMILIES + "; Sean Ireton, 'The "
                  "Samaritans - A Jewish Sect in Israel'")
    t.child_of("gamliel", "yisrael-gamliel")

    t.person("nor", "Nor //", note="Named through his son's patronymic.\n"
                                   "Source: " + SRC_RATSON)
    t.person("abraham-nor", "Abraham /ben Nor/",
             note="Cousin of Ratson. Together they published the first comparative\n"
                  "edition of the Jewish and Samaritan versions of the Torah,\n"
                  "1962-1965.\nSource: " + SRC_RATSON)
    t.child_of("nor", "abraham-nor")

    t.person("arieh-shalma", "Arieh Nimr Yisaschar /ben Shalma/",
             note="Also given as Yisaschar. A cousin of Abraham ben Marchiv's father.\n"
                  "Moved to Tul Karm, where his family lived nearly two generations\n"
                  "without taking root. His branch, Dar Elnimir, ended when its last\n"
                  "member died on 25 March 2012.\n"
                  "Sources: " + SRC_TSEDAKA08 + "; " + SRC_FAMILIES)

    # ---- Dinfi, including the Altif branch --------------------------------
    t.person("absikuwwa", "Ab-Sikuwwa //",
             note="Named through his sons' patronymics.\nSource: " + SRC_FAMILIES)
    t.person("yishmael", "Yishmael /ben Ab-Sikuwwa/", occu="secretary (Kateb Sirri)",
             note="Served as a secretary in the Shechem administration (Arabic:\n"
                  "Kateb Sirri), and gave his name to Dar Sirrawi, the oldest branch\n"
                  "of the Dinfi household.\nSource: " + SRC_FAMILIES)
    t.child_of("absikuwwa", "yishmael")
    t.person("amshallemaa", "Amshallemaa /ben Ab-Sikuwwa/",
             note="Eponym of Dar Imsallam, a Dinfi branch now extinct.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("absikuwwa", "amshallemaa")
    t.person("jacob-dinfi", "Jacob /Hadinfi/",
             note="Named through his sons' patronymics.\nSource: " + SRC_FAMILIES)
    t.person("abed-hanuna", "'Abed Hanuna /ben Jacob Hadinfi/",
             note="Nicknamed 'Iltafe' - handsome - and the branch took its name from\n"
                  "the nickname: ALTIF (Dar Iltafe). This is the origin of the Altif\n"
                  "family, into which the Ukrainian marriages of the 2000s were made\n"
                  "(Alexandra Kraskuk to Wadah Altif, c.2003; Alla Evdokimova to\n"
                  "Azzam Altif, c.2011).\nSource: " + SRC_FAMILIES)
    t.child_of("jacob-dinfi", "abed-hanuna")
    t.person("sadaqa-jacob", "Sadaqa /ben Jacob/",
             note="Eponym of Dar Elshalabi, a Dinfi branch now extinct.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("jacob-dinfi", "sadaqa-jacob")
    t.person("taor-jacob", "Ta'or /ben Jacob/",
             note="A 19th-century figure of the Dinfi household.\n"
                  "Source: " + SRC_FAMILIES)
    t.person("absikkuwa-saed", "Ab-Sikkuwwa /ben Saed Hadinfi/", occu="poet",
             note="A Samaritan poet of the 19th-20th centuries whose compositions\n"
                  "Ratson collected.\nSource: " + SRC_RATSON)

    # ---- Marchiv ----------------------------------------------------------
    t.person("marchiv-abraham-f", "Abraham //",
             note="Named through his sons' patronymics.\nSource: " + SRC_FAMILIES)
    t.person("marchiv-ben-abraham", "Marchiv /ben Abraham/",
             note="Eponym of Dar Mfarreg, one of the two Marchiv families after the\n"
                  "18th-century split.\nSource: " + SRC_FAMILIES)
    t.child_of("marchiv-abraham-f", "marchiv-ben-abraham")
    t.person("yehoshua", "Yehoshua /ben Abraham/",
             note="Brother of Marchiv ben Abraham, and eponym of Dar Aosh'a.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("marchiv-abraham-f", "yehoshua")
    t.person("yusef-yehoshua", "Yusef /ben Yehoshua/",
             note="An 18th-century figure of the Marchiv household.\n"
                  "Source: " + SRC_FAMILIES)
    t.child_of("yehoshua", "yusef-yehoshua")
    t.person("marchiv-jacob-yusef", "Marchiv /ben Jacob ben Yusef/", occu="poet, writer",
             note="17th century. Wrote many letters to Europe, and in one of them\n"
                  "settled the mystery of the last Phinhas High Priest's\n"
                  "disappearance: 'the last Rabban died in our time'.\n"
                  "Sources: " + SRC_FAMILIES + "; " + SRC_AB)
    t.person("abraham-yashishakar", "Abraham /ben Yashishakar/",
             note="A named figure of the Marchiv household.\nSource: " + SRC_FAMILIES)
    t.person("abraham-marchiv-hamarchivi", "Abraham /ben Marchiv Hamarchivi/",
             occu="sage",
             note="A Samaritan wise man of Holon and a close friend of Ratson ben\n"
                  "Benyamim; with him and Yisrael ben Gamliel printed copied Torah\n"
                  "manuscripts and prayer books for community use. Distinct from\n"
                  "Abraham ben Marchiv Hassafari of the Tsedaka household.\n"
                  "Source: " + SRC_RATSON)

    # ---- deputy high priest ----------------------------------------------
    t.person("nethanel", "Nethanel /ben Abraham/", birt="ABT 1930", occu="priest",
             title="Deputy High Priest",
             note="Deputy High Priest in 2012, aged 82, so born about 1930.\n"
                  "Full patronymic: Nethanel b. Abraham b. Phinhas b. Yitzhaq.\n"
                  "Source: " + SRC_AB)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(t.render(), encoding="utf-8")

    named = sum(1 for p in t.people if p["name"] and p["name"] != "//")
    print(f"{len(t.people)} individuals, {len(t.families)} parent-child links")
    print(f"  {named} named, {len(t.people) - named} explicit placeholders")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
