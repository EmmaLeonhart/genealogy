# Where the two cut-off clusters touch Wikidata

Emma found `Kadin Harding` and `Jacqueline Crispin` inside them by hand, and
read it as the seeds having failed rather than the people being unreachable.
That reading is right, and it goes further than expected.

**The clusters are cut off from our Geni merge, not from Wikidata.**

| cluster | people | carry a QID | inside the world tree |
| --- | ---: | ---: | ---: |
| wife of Baruch Jafe | 4,088 | 130 | **69** |
| wife of Samuel Standen | 4,084 | 2 | **1** |

The world tree is the 1,116,499-person Wikidata component from
`reports/wikidata-components.csv` — the one the Charlemagne priority chain
is aimed at. A cluster member already in it is a person our Geni data cannot
reach and Wikidata already connects.

## The two Emma found

| who | geni id | cluster | born | died |
| --- | --- | --- | ---: | ---: |
| Kadin Harding | `6000000176095890839` | wife of Baruch Jafe | 1998 | 2012 |
| Jacqueline Crispin | `6000000005082335522` | wife of Samuel Standen | 1969 | 1971 |

One in each cluster, which is why each looked unreachable separately.
Neither carries a QID; both have parents recorded inside their own cluster.

## Anchors already in the world tree

Every row of `reports/cluster-anchors.csv` is one QID-carrying person in one
of the clusters. The ones marked `in_world_tree` are where an edit could
attach without creating anything first:

| qid | who | born | cluster |
| --- | --- | ---: | --- |
| [`Q122258936`](https://www.wikidata.org/wiki/Q122258936) | Hannah Brüll | 1746 | wife of Baruch Jafe |
| [`Q138808460`](https://www.wikidata.org/wiki/Q138808460) | Mayer Bernheimer | 1784 | wife of Baruch Jafe |
| [`Q30346415`](https://www.wikidata.org/wiki/Q30346415) | Elcha (Elsa) Weil | 1789 | wife of Baruch Jafe |
| [`Q136314043`](https://www.wikidata.org/wiki/Q136314043) | David Isaac Seligmann | 1790 | wife of Baruch Jafe |
| [`Q106188910`](https://www.wikidata.org/wiki/Q106188910) | Koppel Haas | 1801 | wife of Baruch Jafe |
| [`Q106188899`](https://www.wikidata.org/wiki/Q106188899) | Fanny Berg | 1809 | wife of Baruch Jafe |
| [`Q75286`](https://www.wikidata.org/wiki/Q75286) | Emanuel Maximilian Eduard Lilienthal | 1814 | wife of Baruch Jafe |
| [`Q138808469`](https://www.wikidata.org/wiki/Q138808469) | Emanuel Bernheimer | 1817 | wife of Baruch Jafe |
| [`Q1708000`](https://www.wikidata.org/wiki/Q1708000) | Joseph Seligmann | 1819 | wife of Baruch Jafe |
| [`Q136314366`](https://www.wikidata.org/wiki/Q136314366) | William Wolf Seligman | 1822 | wife of Baruch Jafe |
| [`Q29880672`](https://www.wikidata.org/wiki/Q29880672) | Simon Koschland | 1825 | wife of Baruch Jafe |
| [`Q106188902`](https://www.wikidata.org/wiki/Q106188902) | Rosine Frauenthal | 1829 | wife of Baruch Jafe |
| [`Q98594935`](https://www.wikidata.org/wiki/Q98594935) | Sigmund Steinhardt | 1832 | wife of Baruch Jafe |
| [`Q6077095`](https://www.wikidata.org/wiki/Q6077095) | Isaac Seligmann | 1834 | wife of Baruch Jafe |
| [`Q136400561`](https://www.wikidata.org/wiki/Q136400561) | Marcel Bernstein | 1840 | wife of Baruch Jafe |
| [`Q98594908`](https://www.wikidata.org/wiki/Q98594908) | Ignatz "Igne" Steinhardt | 1840 | wife of Baruch Jafe |
| [`Q16740111`](https://www.wikidata.org/wiki/Q16740111) | Abraham Haas | 1847 | wife of Baruch Jafe |
| [`Q51094866`](https://www.wikidata.org/wiki/Q51094866) | Philip Lilienthal | 1849 | wife of Baruch Jafe |
| [`Q131118132`](https://www.wikidata.org/wiki/Q131118132) | Frances (Fanny) Seligman | 1852 | wife of Baruch Jafe |
| [`Q136314538`](https://www.wikidata.org/wiki/Q136314538) | Ida Seligman | 1854 | wife of Baruch Jafe |
| [`Q6076874`](https://www.wikidata.org/wiki/Q6076874) | Isaac Newton Seligman | 1855 | wife of Baruch Jafe |
| [`Q47946`](https://www.wikidata.org/wiki/Q47946) | Henry Morgenthau Sr. | 1856 | wife of Baruch Jafe |
| [`Q73597271`](https://www.wikidata.org/wiki/Q73597271) | Leopold Hirsch | 1857 | wife of Baruch Jafe |
| [`Q139674944`](https://www.wikidata.org/wiki/Q139674944) | Marcus Simon Koshland | 1858 | wife of Baruch Jafe |
| [`Q2743673`](https://www.wikidata.org/wiki/Q2743673) | Edwin Robert Anderson Seligman | 1861 | wife of Baruch Jafe |
| [`Q138416717`](https://www.wikidata.org/wiki/Q138416717) | Charles Robert Baur | 1862 | wife of Baruch Jafe |
| [`Q106188898`](https://www.wikidata.org/wiki/Q106188898) | Frances Koshland | 1865 | wife of Baruch Jafe |
| [`Q455187`](https://www.wikidata.org/wiki/Q455187) | Benjamin Guggenheim | 1865 | wife of Baruch Jafe |
| [`Q102288750`](https://www.wikidata.org/wiki/Q102288750) | Sybyl Beddington | 1868 | wife of Baruch Jafe |
| [`Q138416797`](https://www.wikidata.org/wiki/Q138416797) | Rachel Weill | 1869 | wife of Baruch Jafe |
| [`Q75760041`](https://www.wikidata.org/wiki/Q75760041) | Jesse Koshland | 1871 | wife of Baruch Jafe |
| [`Q3189704`](https://www.wikidata.org/wiki/Q3189704) | Julien Isaïe Weill | 1873 | wife of Baruch Jafe |
| [`Q1465068`](https://www.wikidata.org/wiki/Q1465068) | George Frederick Myddelton Cornwallis-West | 1874 | wife of Baruch Jafe |
| [`Q713011`](https://www.wikidata.org/wiki/Q713011) | Henri Léon Gustave Charles Bernstein | 1876 | wife of Baruch Jafe |
| [`Q59628926`](https://www.wikidata.org/wiki/Q59628926) | George Sidney Hellman | 1878 | wife of Baruch Jafe |
| [`Q139863629`](https://www.wikidata.org/wiki/Q139863629) | Aline Françoise Lucy Coignet | 1884 | wife of Baruch Jafe |
| [`Q13562995`](https://www.wikidata.org/wiki/Q13562995) | Helen Morgenthau | 1884 | wife of Baruch Jafe |
| [`Q47240104`](https://www.wikidata.org/wiki/Q47240104) | Bernard Feustman Gimbel | 1885 | wife of Baruch Jafe |
| [`Q6588759`](https://www.wikidata.org/wiki/Q6588759) | Meyer Robert (M. Robert) Guggenheim | 1885 | wife of Baruch Jafe |
| [`Q139675000`](https://www.wikidata.org/wiki/Q139675000) | Edith R. Guggenheim | 1887 | wife of Baruch Jafe |
| [`Q7964125`](https://www.wikidata.org/wiki/Q7964125) | Walter Abraham Haas Sr. | 1889 | wife of Baruch Jafe |
| [`Q450751`](https://www.wikidata.org/wiki/Q450751) | Henry Morgenthau Jr. | 1891 | wife of Baruch Jafe |
| [`Q21176719`](https://www.wikidata.org/wiki/Q21176719) | Elinor Fatman | 1892 | wife of Baruch Jafe |
| [`Q76545670`](https://www.wikidata.org/wiki/Q76545670) | Margaret Valentine Seligman | 1895 | wife of Baruch Jafe |
| [`Q75350198`](https://www.wikidata.org/wiki/Q75350198) | Charles John Frederick Winn | 1896 | wife of Baruch Jafe |
| [`Q138415666`](https://www.wikidata.org/wiki/Q138415666) | Marcel Nathan Baur | 1896 | wife of Baruch Jafe |
| [`Q233806`](https://www.wikidata.org/wiki/Q233806) | Marguerite Guggenheim | 1898 | wife of Baruch Jafe |
| [`Q138857863`](https://www.wikidata.org/wiki/Q138857863) | Marie Apollonie Baur | 1900 | wife of Baruch Jafe |
| [`Q139674953`](https://www.wikidata.org/wiki/Q139674953) | Eleanor Haas | 1901 | wife of Baruch Jafe |
| [`Q3421006`](https://www.wikidata.org/wiki/Q3421006) | Raymond Lindon | 1901 | wife of Baruch Jafe |
| [`Q138415491`](https://www.wikidata.org/wiki/Q138415491) | Therese Baur | 1902 | wife of Baruch Jafe |
| [`Q2847231`](https://www.wikidata.org/wiki/Q2847231) | ANDRE Baur | 1904 | wife of Baruch Jafe |
| [`Q5534920`](https://www.wikidata.org/wiki/Q5534920) | Geoffrey Theodore Hellman | 1907 | wife of Baruch Jafe |
| [`Q139675022`](https://www.wikidata.org/wiki/Q139675022) | Edith "Didi" May Koshland | 1910 | wife of Baruch Jafe |
| [`Q687282`](https://www.wikidata.org/wiki/Q687282) | Henry Benjamin "Hank" Greenberg | 1911 | wife of Baruch Jafe |
| [`Q5344059`](https://www.wikidata.org/wiki/Q5344059) | Edward Lasker | 1912 | wife of Baruch Jafe |
| [`Q47358720`](https://www.wikidata.org/wiki/Q47358720) | Bruce Alva Gimbel | 1913 | wife of Baruch Jafe |
| [`Q138910168`](https://www.wikidata.org/wiki/Q138910168) | Ruth F. Koshland | 1913 | wife of Baruch Jafe |
| [`Q113799767`](https://www.wikidata.org/wiki/Q113799767) | Caral Glazier Gimbel | 1914 | wife of Baruch Jafe |
| [`Q113799472`](https://www.wikidata.org/wiki/Q113799472) | Hope Alva Gimbel | 1914 | wife of Baruch Jafe |
| [`Q7964126`](https://www.wikidata.org/wiki/Q7964126) | Walter Abraham Haas Jr. | 1916 | wife of Baruch Jafe |
| [`Q20737580`](https://www.wikidata.org/wiki/Q20737580) | Henry B Morgenthau III | 1917 | wife of Baruch Jafe |
| [`Q585081`](https://www.wikidata.org/wiki/Q585081) | Daniel Edward Koshland Jr. | 1920 | wife of Baruch Jafe |
| [`Q6761921`](https://www.wikidata.org/wiki/Q6761921) | Marian Elliot | 1921 | wife of Baruch Jafe |
| [`Q132730940`](https://www.wikidata.org/wiki/Q132730940) | Joseph Lebworth | 1922 | wife of Baruch Jafe |
| [`Q138857934`](https://www.wikidata.org/wiki/Q138857934) | Nicole Dreyfus | 1925 | wife of Baruch Jafe |
| [`Q7174248`](https://www.wikidata.org/wiki/Q7174248) | Peter Robin Gimbel | 1927 | wife of Baruch Jafe |
| [`Q76399`](https://www.wikidata.org/wiki/Q76399) | Elga Andersen | 1935 | wife of Baruch Jafe |
| [`Q139795274`](https://www.wikidata.org/wiki/Q139795274) | Lavinia Bernheimer | — | wife of Baruch Jafe |
| [`Q74698102`](https://www.wikidata.org/wiki/Q74698102) | Helen Smith | 1882 | wife of Samuel Standen |

## What this changes

The question was "which Geni edge was removed". The answer is that it does
not have to be found to connect these people: the Wikidata side is already
joined at the points above. What the Geni exports failed at was reaching the
clusters from our own tree, and that is a sampling gap — both balls stopped
at the export size bound rather than exhausting the neighbourhood.

Components smaller than the world tree are counted too, because they are the
opposite case — a QID with no genealogical edges on Wikidata is a person
whose links we would be *adding*, not following:

| wikidata component size | people |
| ---: | ---: |
| 1,116,499 | 70 |
| 1 | 48 |
| 2 | 6 |
| 6 | 5 |
| 3 | 1 |
| 5 | 1 |
| 4 | 1 |
