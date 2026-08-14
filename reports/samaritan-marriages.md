# Marriages, wives and mothers in the Samaritan priestly families

**Asked for by Emma, 2026-08-14: the marriage records of the priestly families —
the mothers, the wives, the children, in the contemporary period.**

Census: `reports/samaritan-marriages.csv` (one row per family per export) and
`reports/samaritan-people.csv` (one row per person per export), built by
`scripts/build-samaritan-marriage-census.py` over all 199 distinct exports.

---

## The measurement

| | count |
| --- | ---: |
| people in the priestly families, as Geni holds them | **113** |
| male | 109 |
| **female** | **4** |
| distinct family records | **99** |
| **family records naming a wife** | **2** |
| **marriage dates** | **0** |
| **marriage places** | **0** |
| birth years | 7 |
| death years | 30 |

Ninety-nine families, two wives, no marriage dates at all. The priestly
genealogy on Geni is a chain of fathers and sons with the women left out.

## The two wives are ancient, and neither of them has a name

| family | husband | "wife" |
| --- | --- | --- |
| `6000000178918116836` | Manasseh, Samaritan High Priest | **daughter of Sanballat the Horonite** |
| `6000000178917712851` | Hillel II/Hanan, Samaritan High Priest | **daughter of the king of Assyria** |

Both are recorded only as somebody's daughter — the name field holds a
relationship, not a name. The Sanballat one is the marriage Josephus describes;
Nehemiah 13:28 is the other end of the same story. Neither is contemporary and
neither is a person Geni can say anything else about.

## In the contemporary family there are no wives at all

The post-1624 Itamar component — Tabia ha'Abta'i's descent, the family that
holds the high priesthood today — is 33 people:

- **31 male, 2 female**
- the two women are `NN /bint Aabed-El ben Asher ben Matzliach/`
  (`6000000178794082883`, `6000000178794141887`) — **daughters** of the current
  High Priest, both unnamed
- **0 `WIFE` lines. 0 `MARR` lines.**

Not one mother, not one wife, not one wedding, across four hundred years and
twenty high priests.

**That absence is evidence rather than a gap.** The export it comes from,
`exports/archive/export-geni/export-Forest-51.ged`, is a `Forest` export seeded
on Tabia himself, and `Forest` follows spouse links — see CLAUDE.md § *Zero
recorded marriages after a `Forest` export is evidence, not a gap*. A `Forest`
ball that returns no marriages has found none to follow. Geni does not hold these
women; it is not that our sampling missed them.

## What the published record does hold, and it is a lot

The community's marriage practice in the contemporary period is well documented
in the general press, none of it on Geni:

- **1973** — the high priest permits marriage to **Jewish** women.
- **2002** — permitted to **Ukrainian** women. About **10–11** Ukrainian women
  are in the community, and brides have also come from **Kazakhstan, Turkey and
  Russia**.
- **Males outnumber females roughly three to one**, which is the reason for all
  of the above.
- Every marriage needs the **High Priest's approval**, and the bride serves a
  trial period of up to a year in the community.
- Community size **766** (2012) against **146** in 1917.

**The priestly family takes foreign brides too.** The Christian Science Monitor,
2014, names **Yousef Cohen, a Samaritan priest, whose son married a Ukrainian
woman**. No source found states a separate endogamy rule confining priests to
priestly wives — the restriction that is documented is the general one against
divorcées, and first-cousin marriage is described as the Samaritan norm.

**Every foreign marriage found by name is Altif, not priestly.** Tanya
Onischenko → Tami Altif; Alexandra Kraskuk → Wadah Altif; Alla Evdokimova →
Azzam Altif — all of them the Altif branch of the Dinfi household
(`reports/samaritan-families.md`). The one priestly instance is Yousef Cohen's
son and the sources do not name either party.

## The decision

**The women are not recoverable from Geni, and no amount of exporting will
change that.** A `Forest` ball from the root of the family found none. So:

1. **Do not model the priestly line as if the marriages were merely unexported.**
   For anything generated from this material — Wikidata creations included — the
   priestly chain is P22 father-to-son, with no P26 and no P25, because that is
   what the data says.
2. **The two ancient "wives" must not become people.** "daughter of Sanballat the
   Horonite" is a description, not a name, and creating a Wikidata item labelled
   that would be inventing a person. If either is ever wanted, she is a
   qualifier or a described statement, not an item.
3. **The two `NN bint Aabed-El` daughters are the live case.** They are the
   current High Priest's daughters, they exist on Geni, and they are unnamed.
   They are also the only contemporary women in the entire priestly dataset.
4. **Contemporary wives need record access, not more exports.** This is the same
   conclusion `reports/samaritan-families.md` reached for the four wives of the
   sons of Yisrael ben Gamliel: a woman who married into a 750-person community
   between 1960 and 2015 is in Israeli civil records and in `A.B. — The Samaritan
   News`, and in neither Geni nor Wikidata.

## Two corrections to earlier statements in this session

**The pre-1624 chain is 78 people in the corpus, not 35.** The 35 were what one
`Bio` export happened to hold. Across all exports the line runs unbroken from
**Uzzi ben Bakhi** (`6000000178918814849`, no father recorded) down through
Hezekiah IV and Baba Rabba, 78 generations of it.

**Hezekiah IV's father is in the corpus.** He is **Hillel II/Hanan**
(`6000000178917712846`), 33rd in that chain. The `Bio` export's family record for
him had a wife and no husband, which was truncation in that file rather than the
top of the tree.

## Sources

- [In West Bank, good Samaritans seek foreign brides](https://www.csmonitor.com/World/Middle-East/2014/0430/In-West-Bank-good-Samaritans-seek-foreign-brides) — Christian Science Monitor, 30 April 2014
- ['Good Samaritans' seek Ukrainian wives](https://www.aljazeera.com/features/2013/1/8/good-samaritans-seek-ukrainian-wives) — Al Jazeera, 8 January 2013
- [In West Bank Hamlet, Ukrainian Brides Help Samaritan Faith Stay Afloat](https://www.rferl.org/a/west-bank-hamlet-ukrainian-brides-help-samaritans/28069338.html) — RFE/RL
- [Ukrainian women marry, give hope to Israel's Samaritans](https://archive.kyivpost.com/article/content/ukraine-politics/ukrainian-women-marry-give-hope-to-israels-samaritans-321827.html) — Kyiv Post, 18 March 2013
- [Samaritans](https://en.wikipedia.org/wiki/Samaritans) — Wikipedia, for the succession: since 2013 the 133rd High Priest is **Aabed-El ben Asher ben Matzliach**, who is on Geni as `6000000178795554821` and is the father of the two unnamed daughters above
- [Samaritan Sect](https://jwa.org/encyclopedia/article/samaritan-sect) — Jewish Women's Archive (403 to this tool; listed because it is the obvious next read on the women specifically)
- `reports/sources/ratson-2012.pdf` — the one fully documented contemporary
  Samaritan marriage in our own files: **Ratson b. Benyamim m. Batia bat Yefet
  ben Abraham, 1943**, two children, Benyamim and Yefet. Tsedaka family, not
  priestly.
