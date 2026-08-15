# What the superseded Samaritan exports still hold alone

**Emma, 2026-08-15:** *"I am just gonna do imports until all items found in
the Tsedaka II ones are also present in later exports."* This is the gap
remaining. Re-run it after each import; the target is **0 uncovered**.

`Yitzhaq I ben Tsedaka` (`6000000227245553985`) was missing from Geni, so Geni
linked **Tsedaka II → Abram** directly. Four exports predate the fix and still
carry that edge. GEDCOMs are never deleted here and the merge unions `FAMC`
links, so the superseded edge cannot be removed by dropping a file — **it is
retired by covering every person in those files with a newer export.**

## The gap

| superseded export | people | not yet covered |
| --- | ---: | ---: |
| `export-Ancestors-6000000227240714964.ged` | 348 | **24** |
| `export-BloodTree-6000000227240714964.ged` | 4,830 | **3,290** |
| `export-Forest-6000000178794141887.ged` | 4,806 | **0** |
| `export-Forest-6000000227240691895.ged` | 4,854 | **0** |
| **distinct across all four** | **8,182** | **3,290** |

Covered means: present in an export listed as `CORRECTED` in
`scripts/measure-superseded-coverage.py`. **Add each new export to that list**
— it is the only place recency is recorded, because Geni writes the *seed's*
dates into the `HEAD` (`ABT 2010`, `1732`) rather than the export time, so the
header cannot order these files.

Every uncovered person is a row in `reports/superseded-coverage.csv`, with the
father the superseded export gives them — which is what a re-export has to
either confirm or correct.

## The two remaining gaps are not the same problem

Both `Forest` exports are **fully covered already**, and the other two are not
uncovered in the same place:

- **`export-Ancestors-…240714964` — 24 people, and they are the relevant ones.**
  Eight are the `Nth generation Samaritan Itamar line` placeholders; the rest are
  Assyrian kings, plus Amram and Jochebed. This is a small, targeted export away
  from zero.
- **`export-BloodTree-…240714964` — 3,290 people, and they are Javanese.** The
  `BloodTree` walked up out of the Samaritan cluster entirely: the uncovered
  head is Mataram and Demak royalty — Senapati, Sunan Giri, Raden Patah. None of
  them carries the superseded `Tsedaka II → Abram` edge, because none of them is
  anywhere near it. **1,069 of the 3,290 appear in no other export at all**, so
  covering them is real work that buys nothing towards this particular fix.

**That distinction is worth making before doing the imports.** The criterion
here — cover everything in the superseded files — is Emma's and is stated
bluntly on purpose. But its *purpose* is retiring one stale edge, and the
Javanese 3,290 are a `BloodTree` side-effect rather than part of it.

## Where to seed next — **per export, because they differ completely**

The uncovered people grouped by the father they hang from: a seed reaching
one of these fathers covers that whole group in a single export. Grouped
per superseded export rather than merged, because the two remaining files
are uncovered in **different parts of the tree** and merging the tables
hides that.

### `export-Ancestors-6000000227240714964.ged` — 24 uncovered

| father in the superseded export | uncovered children | example |
| --- | ---: | --- |
| (no father recorded) | 3 | Amram |
| Ashur-nirari II King of Assyria | 1 | Aššūr-bēl-nīšēšu |
| 9th generation Samaritan Itamar line | 1 | 10th generation Samaritan Itamar line |
| Enlil-Nasir II King of Assyria | 1 | Ashur-nirari II King of Assyria |
| 8th generation Samaritan Itamar line | 1 | 9th generation Samaritan Itamar line |
| Ashur-rabi I King of Assyria | 1 | Enlil-Nasir II King of Assyria |
| 7th generation Samaritan Itamar line | 1 | 8th generation Samaritan Itamar line |
| Enlil-nasir I King of Assyria | 1 | Ashur-rabi I King of Assyria |
| 6th generation Samaritan Itamar line | 1 | 7th generation Samaritan Itamar line |
| Puzur-Ashur III King of Assyria | 1 | Enlil-nasir I King of Assyria |
| 5th generation Samaritan Itamar line | 1 | 6th generation Samaritan Itamar line |
| Ashur-nirari I King of Assyria | 1 | Puzur-Ashur III King of Assyria |

…and 10 more fathers with fewer children each.

### `export-BloodTree-6000000227240714964.ged` — 3,290 uncovered

| father in the superseded export | uncovered children | example |
| --- | ---: | --- |
| (no father recorded) | 919 | Amram |
| Pnbhn. Senapati Danang Suta Wijaya / R. Bagus (1587-1601) Senapati /Da | 49 | Mas Jolang Kanjeng Susuhunan Prabu Hanyokrow |
| Raden Umar Said "Sunan Muria" -25 [Karnaka] Walisongo-8 | 42 | Pangeran Santri (Sunan Kadilangu) /Sunan Nga |
| R. Paku / Jaka Samudra Sunan Giri-1 (1481–1506) | 42 | Nyi Ageng Giri Kidul |
| Ki Gedhe Pemanahan,Ki Gedhe Mataram Ageng /Pemanahan/ | 33 | [65] Pangeran Arya Tanduran Bin /Ki Ageng Pa |
| Mas Jolang Kanjeng Susuhunan Prabu Hanyokrowati | 26 | Tumenggung Maduseno (Kertiwongso) |
| 1 Angkawijaya Prabu Geusan Ulun (1579-1601 Kusumahdinata) | 25 | Kiai Rangga Patra Kelana /./ |
| {18} Maulana Hasanudin "Pangeran Sebakingking" | 24 | 1 Maulana Yusuf Panembahan Pangkalan Gede Su |
| R. Jin Bun / R. Praba R. Patah Demak-1 (1478-1501) | 22 | P. Adipati Trenggono Raja Demak Bintoro-2 (1 |
| Sri Prabu Kertawijaya (Bhre Kertabhumi) Brawijaya-5 | 17 | Raden Ayu Ratna Pembayun /./ |
| Sri Maharajadiraja Sri Kertanegara Wikrama Dharmatunggadewa Raja Singa | 16 | Bhre Daha I |
| Sang Aji Kala | 16 | Awang /Alak Betatar/ |

…and 952 more fathers with fewer children each.

