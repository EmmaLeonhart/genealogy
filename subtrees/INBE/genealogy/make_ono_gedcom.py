"""Build genealogy/ono_inbe_honkeicho.ged (Japanese names),
ono_inbe_honkeicho_en.ged (English names, Japanese in notes) and
ono_inbe_honkeicho_en_dated.ged (English, with estimated years and Wikidata links) from genealogy/ono_inbe_honkeicho.csv.

The Ono family's 斎部宿禰本系帳 (1870; NDL pid 2538213, images 50-56), judged a
Suzuki Masatoshi forgery by Kosugi Sugimura in 1876. Parent links follow the
transcription order: each numbered row is the child of the previous numbered
row, a "b" row is a sibling of the same-numbered row, and H rows are the
second (Ame no Hiwashi) line. Run: python genealogy/make_ono_gedcom.py
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "ono_inbe_honkeicho.csv"
OUT = HERE / "ono_inbe_honkeicho.ged"

rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
by_seq = {r["seq"]: r for r in rows}

# Extra people named in the pedigree but not rows of their own.
EXTRA = {
    "W2": {"name": "天比理乃咩命", "note": "Wife of 天太玉命 (Ame no Hiritome)."},
}

people = {}  # key -> dict(name, note, sex)
for r in rows:
    note = "; ".join(x for x in [
        r["alias_or_note"] and f"Alias/note: {r['alias_or_note']}",
        r["reign_or_date_given"] and f"Reign/date given: {r['reign_or_date_given']}",
        r["matches_chronicle_person"] and f"Matches chronicle person: {r['matches_chronicle_person']}",
        r["notes"],
        f"NDL pid 2538213 image {r['ndl_image']}",
    ] if x)
    people[r["seq"]] = {"name": r["name"].split(" / ")[0], "note": note}
people.update(EXTRA)

# English (romanised) names for the English-first file. "?" marks a reading of
# rare man'yōgana spellings that is a best guess, not attested.
EN = {
    "1": "Takamimusubi", "2": "Ame no Futodama", "W2": "Ame no Hiritome",
    "3": "Ame no Kushimimi", "4": "Ame no Tomi", "5": "Iinagahime",
    "6": "Wakafunu?", "7": "Sakumimi?", "8": "Akasako?", "9": "Tamakushiko?",
    "10": "Kosamazuchi", "10b": "Hamimi?", "11": "Tarashitomi?", "11b": "Ōkuma",
    "12": "Mazunumi no Sukune?", "13": "Saki no Ōhito no Sukune?",
    "14": "Tahiko no Sukune?", "15": "Namiko?", "16": "Kotone?",
    "17": "Tanate (Takenadeko)?", "18": "Toyotomi?", "19": "Utsuniwamaro?",
    "20": "Sagashi?", "21": "Inbe no Kobito", "21b": "Inbe no Shikobuchi",
    "22": "Nashiro?", "23": "Fukimaro?",
    "H1": "Kamimusubi", "H2": "Tsunokorimusubi", "H3": "Ame no Sokotachi",
    "H4": "Isafutama?", "H5": "Ikashihotama?", "H6": "Ame no Seo",
    "H7": "Kotonomachi?", "H8": "Ame no Hiwashi", "H9": "Ōasahiko",
    "H10": "Yufutsunushi", "H11": "Katatanushi", "H12": "Inasakao",
    "H13": "Sakikuwake", "H14": "Fuyurawake", "H15": "Hihita no Omi",
    "H16": "Tomimi no Ōhito?", "H17": "Iwabiko", "H18": "Shimanafu?",
    "H19": "Murahi?", "H20": "Ukei?", "H21": "Itsuhiko", "H22": "Kuzumi?",
}
ROLE = {
    "1": "god", "2": "god; ancestor of the Inbe", "W2": "goddess; Futodama's wife",
    "3": "god", "4": "god; led the Awa Inbe east to Bōsō", "5": "goddess; priestess of Futodama's shrine",
    "H1": "god", "H8": "god; ancestor of the Awa Inbe", "H9": "god",
    "H10": "god; hemp cultivation in Awa", "H11": "'first ancestor of the Awa Inbe'",
    "21": "real person: Nihon Shoki compiler, d. 719",
    "21b": "real person: Jingikan official, Jinshin War 672",
}
assert set(EN) == set(people), set(people) ^ set(EN)

# Wikidata items: those the user linked in her MyHeritage edits,
# plus three confirmed in research/notes/wikidata-survey.md.
WIKIDATA = {
    "1": "Q125400", "2": "Q11059539", "3": "Q110064736", "4": "Q24899653",
    "21": "Q11490720", "21b": "Q11490725", "H8": "Q10939697", "W2": "Q85879124",
    # Added by the user in ono_inbe_honkeicho_en_dated2_additional_qid.ged:
    "14": "Q141627252", "H1": "Q3275901", "H9": "Q134846383",
}

# Approximate (birth, death) years implied by the pedigree; negative = BC.
# Anchored on the reign each entry names, using the traditional Nihon Shoki
# reign dates (legendary before the 6th century); entries without a reign are
# interpolated. Real dates only for Kobito and Shikobuchi. Gods get none.
DATES = {
    "4": (-700, -620, "Jimmu (trad. 660-585 BC)"),
    "5": (-680, -600, "wife of Yufutsunushi, Jimmu's reign"),
    "6": (-610, -540, "interpolated"), "7": (-460, -390, "interpolated"),
    "8": (-310, -240, "interpolated"), "9": (-40, 30, "Suinin 25 (trad. 5 BC)"),
    "10": (20, 90, "interpolated"), "10b": (20, 90, "interpolated"),
    "11": (80, 150, "Keikō 53 (trad. AD 123)"), "11b": (80, 150, "interpolated"),
    "12": (180, 250, "Jingū (trad. 201-269)"),
    "13": (260, 340, "Ōjin to Nintoku (trad. 270-399)"),
    "14": (370, 430, "Richū (trad. 400-405)"),
    "15": (430, 490, "Yūryaku (trad. 456-479)"),
    "16": (470, 530, "interpolated"), "17": (500, 560, "interpolated"),
    "18": (520, 580, "Kinmei (539-571)"), "19": (570, 630, "Suiko (593-628)"),
    "20": (610, 670, "Hakuchi 4 (653)"),
    "21": (650, 719, "real: died Yōrō 3 (719); birth year approximate"),
    "21b": (640, 701, "real: Jinshin War 672; death year approximate"),
    "22": (680, 740, "interpolated"), "23": (670, 730, "Monmu 4 (700)"),
    "H10": (-690, -610, "Jimmu (trad. 660-585 BC)"),
    "H11": (-610, -545, "Suizei (trad. 581-549 BC)"),
    "H12": (-570, -475, "Annei to Itoku (trad. 549-477 BC)"),
    "H13": (-500, -400, "Kōshō (trad. 475-393 BC)"),
    "H14": (-420, -320, "Kōan (trad. 392-291 BC)"),
    "H15": (-360, -290, "Kōan (same palace)"),
    "H16": (-300, -220, "Kōrei (trad. 290-215 BC)"),
    "H17": (-240, -160, "Kōgen (trad. 214-158 BC)"),
    "H18": (-180, -100, "Kaika (trad. 158-98 BC)"),
    "H19": (-120, -40, "Sujin (trad. 97-30 BC)"),
    "H20": (-50, 30, "Suinin (trad. 29 BC-AD 70)"),
    "H21": (-10, 100, "Suinin to Keikō (trad. to AD 130)"),
    "H22": (100, 170, "Seimu (trad. 131-190)"),
}
assert set(DATES) <= set(people)


def gdate(y):
    return f"{-y} B.C." if y < 0 else f"{y}"

FEMALE = {"5", "W2"}


def parent_of(seq):
    """Previous generation's key for a row, per the transcription order."""
    m = re.fullmatch(r"(H?)(\d+)(b?)", seq)
    prefix, n = m.group(1), int(m.group(2))
    if n == 1:
        return None
    prev = f"{prefix}{n - 1}"
    return prev if prev in by_seq else None


# Families: (father, mother) -> children
families = {}


def add_child(father, mother, child):
    families.setdefault((father, mother), []).append(child)


for seq in by_seq:
    if seq == "H11":
        # Text: 訶多々主命 is the son of 由布津主命 (H10) and 飯長媛命 (5).
        add_child("H10", "5", seq)
        continue
    if seq == "6":
        # The Futodama line continues through 飯長媛命 and her husband H10.
        add_child("H10", "5", seq)
        continue
    p = parent_of(seq)
    if p is None:
        continue
    if p == "2":
        add_child("2", "W2", seq)
    elif p == "5":
        continue  # handled above
    else:
        add_child(p, None, seq)
families.setdefault(("2", "W2"), [])

ids = {k: f"@I{i}@" for i, k in enumerate(people, 1)}
fam_ids = {k: f"@F{i}@" for i, k in enumerate(families, 1)}

OUT_EN = HERE / "ono_inbe_honkeicho_en.ged"
OUT_DATED = HERE / "ono_inbe_honkeicho_en_dated.ged"
OUT_EN_QID = HERE / "ono_inbe_honkeicho_en_qids.ged"
QIDS_JSON = HERE / "wikidata" / "ono_qids.json"


def write(out, english, dated=False, qids=None):
    head_note = ("Ono family Inbe pedigree (Inbe no Sukune honkeicho, 1870). "
                 "Judged forged by Kosugi Sugimura in 1876, who attributed it to Suzuki "
                 "Masatoshi; not evidence of real descent. Parent links follow transcription "
                 "order; see genealogy/ono_inbe_honkeicho.csv and "
                 "research/notes/inbe-pedigrees.md.")
    if not english:
        head_note = "斎部宿禰本系帳. " + head_note
    if dated:
        head_note += (" Years are rough estimates of when each person would have lived "
                      "according to the pedigree itself, anchored on the emperor each entry "
                      "names, using the traditional Nihon Shoki reign dates; those are "
                      "legendary before the 6th century. Only Inbe no Kobito and Inbe no "
                      "Shikobuchi are real people with known dates. Gaps of a century or more "
                      "between parent and child are the pedigree's own, a sign it was "
                      "constructed.")
    L = ["0 HEAD", "1 SOUR INBE-research", "2 NAME make_ono_gedcom.py",
         "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8",
         f"1 NOTE {head_note}",
         "0 @S1@ SOUR",
         "1 TITL Inbe no Sukune honkeicho (斎部宿禰本系帳), bound in the Awa no kuni Inbe kakei volume, NDL Digital Collections",
         "1 PUBL National Diet Library, pid 2538213, doi 10.11501/2538213",
         "1 NOTE Kosugi Sugimura's 1876 headnote attributes it to Suzuki Masatoshi."]
    for key, p in people.items():
        if english:
            en = EN[key]
            parts = [f"Japanese: {p['name']}"]
            if en.endswith("?"):
                parts.append("English reading is a best guess")
            if key in ROLE:
                parts.append(ROLE[key])
            name, note = en.rstrip("?"), "; ".join(parts + [p["note"]])
        else:
            name, note = p["name"], p["note"]
        if dated and key in WIKIDATA:
            note += f"; Wikidata: https://www.wikidata.org/wiki/{WIKIDATA[key]}"
        L += [f"0 {ids[key]} INDI", f"1 NAME {name}",
              f"1 SEX {'F' if key in FEMALE else 'M'}"]
        if dated and key in DATES:
            b, d, basis = DATES[key]
            L += ["1 BIRT", f"2 DATE {gdate(b)}", "1 DEAT", f"2 DATE {gdate(d)}"]
            note += f"; Dates estimated from: {basis}"
        elif dated:
            note += "; No dates: mythological figure"
        for fk, kids in families.items():
            if key in kids:
                L.append(f"1 FAMC {fam_ids[fk]}")
            if key in fk:
                L.append(f"1 FAMS {fam_ids[fk]}")
        if qids and key in qids:
            url = f"https://www.wikidata.org/wiki/{qids[key]}"
            note += f'; Wikidata: <a href="{url}">{url}</a>'  # clickable in MyHeritage, as in the user's edits
        L += [f"1 NOTE {note}", "1 SOUR @S1@", "2 QUAY 0"]
    for fk, kids in families.items():
        father, mother = fk
        L.append(f"0 {fam_ids[fk]} FAM")
        if father:
            L.append(f"1 HUSB {ids[father]}")
        if mother:
            L.append(f"1 WIFE {ids[mother]}")
        L += [f"1 CHIL {ids[c]}" for c in kids]
        L += ["1 SOUR @S1@", "2 QUAY 0"]
    L.append("0 TRLR")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(people)} people, {len(families)} families)")


if __name__ == "__main__":
    write(OUT, english=False)
    write(OUT_EN, english=True)
    write(OUT_DATED, english=True, dated=True)
    import json
    write(OUT_EN_QID, english=True, qids=json.loads(QIDS_JSON.read_text(encoding="utf-8")))
