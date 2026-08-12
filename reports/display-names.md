# Display names, and whether they can be English labels

**The question, from Emma on 2026-08-11:** *"I don't know how bad it is to
have it so that all the display names just turn into English language labels
like this or whatever... My impression is that it's often kind of passable but
not good. But it's your job to figure it out."*

**It is answerable rather than arguable.** 14,157 of our people carry a Wikidata
item, and Wikidata already holds an English label a human chose. So the string
the rule would produce can be scored against the string somebody picked.

Built from `reports/display-names.csv` (444,874 rows, every `NAME` record in the
tree). Every scored person is in `reports/display-name-vs-label.csv` — no bucket
below has to be taken on trust.

## The scoreable population, and what falls out of it

| | people |
| --- | ---: |
| linked to a Wikidata item | 14,157 |
| …of which no English label on Wikidata | 501 |
| …of which **no Latin-script `NAME` at all** | 5,199 |
| **scored** | **8,457** |
| of the scored, carrying more than one Latin name | 4,167 |

**5,199 people have no Latin-script name whatsoever.** Those are the
translation cases Emma named — *"If there's only a name present in some sort of
other script, we have to do a translation"* — and they are not a fringe: they are
37% of the linked people.

## How well the rule does

**first** takes the first Latin `NAME` record. **best** takes the best-matching of
all the person's Latin names — an upper bound on any selection rule whatever, not
a proposal, since nothing can choose better than the best available.

| verdict | first | | best | |
| --- | ---: | ---: | ---: | ---: |
| identical | 1,546 | 18.3% | 2,009 | 23.8% |
| identical bar case/diacritics | 192 | 2.3% | 259 | 3.1% |
| Geni is a superset | 1,872 | 22.1% | 2,311 | 27.3% |
| Wikidata is a superset | 472 | 5.6% | 389 | 4.6% |
| overlap, half or more | 2,517 | 29.8% | 2,314 | 27.4% |
| overlap, under half | 946 | 11.2% | 617 | 7.3% |
| nothing in common | 912 | 10.8% | 558 | 6.6% |

**Exactly right: 1,738 of 8,457 (20.6%) taking the first name, 2,268 (26.8%) taking the best.**

## Scripts across all 444,874 name records

| script(s) | records |
| --- | ---: |
| Latin | 296,936 |
| Han | 94,444 |
| Han+Latin | 23,355 |
| (no letters) | 7,963 |
| Cyrillic | 7,874 |
| Hangul | 6,066 |
| Arabic | 3,921 |
| Cyrillic+Latin | 1,024 |
| Latin+Masculine | 735 |
| Han+Hiragana | 482 |
| Hebrew | 471 |
| Greek | 404 |
| Han+Ideographic | 250 |
| Arabic+Latin | 166 |
| Latin+Modifier | 104 |
| Feminine+Latin | 85 |
| Hiragana | 79 |
| Hebrew+Latin | 62 |
| Han+Katakana | 61 |
| Greek+Latin | 46 |
| Armenian | 46 |
| Katakana | 40 |
| Hangul+Latin | 36 |
| Latin+Tibetan | 34 |
| Han+Ideographic+Latin | 22 |

## What each verdict actually looks like

Raw, first-name measure, up to 15 each.

### identical

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `1825560` | Q112959102 | Samuel Wells | Samuel Wells |
| `289320932760007122` | Q6250312 | John Neville | John Neville |
| `301342753080007082` | Q21832326 | Per Olof Grönlund | Per Olof Grönlund |
| `302036169990003799` | Q2068391 | Rupilia Faustina | Rupilia Faustina |
| `302211628310006481` | Q674757 | Tiberius Claudius Severus Proculus | Tiberius Claudius Severus Proculus |
| `302224840050008242` | Q441706 | Annia Cornificia Faustina Minor | Annia Cornificia Faustina Minor |
| `302534501490001345` | Q567222 | Marcus Annius Verus Caesar | Marcus Annius Verus Caesar |
| `302889610110005663` | Q7241575 | Presley Neville | Presley Neville |
| `302893164200008270` | Q20822332 | Amelia Neville | Amelia Neville |
| `303021670170005628` | Q452705 | Domitia Paulina | Domitia Paulina |
| `307514259060008270` | Q105426953 | Margery Willard | Margery Willard |
| `310151979050001364` | Q735297 | Thomas Metcalfe | Thomas Metcalfe |
| `315336717180006465` | Q98050960 | Joseph Willard | Joseph Willard |
| `3153782` | Q101247694 | Peder Fleming | Peder Fleming |
| `328059704870005473` | Q6260751 | John Thornton Augustine Washington | John Thornton Augustine Washington |

### identical bar case/diacritics

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `283181900190003966` | Q271376 | Amestris . | Amestris |
| `283896414940007239` | Q125472016 | John Sargent Jr. | John Sargent, Jr. |
| `294414873430006408` | Q1346964 | Lambert margrave of Tuscany | Lambert, Margrave of Tuscany |
| `300537894950005354` | Q692265 | Jérôme Napoléon Bonaparte | Jérôme Napoleon Bonaparte |
| `331624398740011365` | Q104537663 | Levi Moss Sr. | Levi Moss, Sr. |
| `3825252` | Q112958671 | Samuel S. Terry Sr. | Samuel S. Terry, Sr. |
| `4924875649300067216` | Q43899851 | Filippo Lante Montefeltro Della Rovere IV duca di Bomarzo | Filippo Lante Montefeltro della Rovere, IV duca di Bomarzo |
| `4956444637700125722` | Q136411203 | Anders Nielsen Sehested Broholm Linjen | Anders Nielsen Sehested, Broholm Linjen |
| `4973001485280125785` | Q140761504 | Niels Jensen Sehested Oberstløjtnant, til Broholm | Niels Jensen Sehested, Oberstløjtnant, til Broholm |
| `4973011274330029032` | Q136411204 | Elisabeth Andersdatter Skeel til Broholm og Mullerup | Elisabeth Andersdatter Skeel, til Broholm og Mullerup |
| `5414792841960084676` | Q101423826 | Benjamin Wright Jr. | Benjamin Wright, Jr. |
| `5432947433130027698` | Q16063735 | Frederik Christian Michaëlsen | Frederik Christian Michaelsen |
| `5657833973450023638` | Q101537627 | Charles “Charley” Phelps I | Charles “Charley” Phelps, I |
| `6000000000112073804` | Q123702048 | Robert Douglas of New London | Robert Douglas, of New London |
| `6000000000115658620` | Q2601233 | Robert de Ferrers 2nd Earl of Derby | Robert de Ferrers, 2nd Earl of Derby |

### Geni is a superset

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `2233799` | Q7174248 | Peter Robin Gimbel | Peter Gimbel |
| `2399880` | Q12317087 | Holger "Den Rige" Rosenkrantz | Holger Rosenkrantz |
| `2434385` | Q2121164 | Wolfert van Brederode heer van Cloetinge en Zwammerdam | Wolfert van Brederode |
| `289226275560008023` | Q11959866 | Axel Andersson Mowat | Axel Mowat |
| `2915061` | Q273773 | Rollo Ragnvaldsson "the Walker Rolf" | Rollo |
| `298740371650007964` | Q1819709 | Leopold II of Habsburg 2nd Duke of of Austria | Leopold II, Duke of Austria |
| `298742409800006343` | Q156404 | Rudolf IV. "the Ingenious" Habsburg Herzog von Österreich | Rudolf IV |
| `300340430900007929` | Q604419 | Infanta Maria Josefa Carmela of Spain | Infanta Maria Josefa of Spain |
| `305332989800002467` | Q116150300 | Cecilie Ebbesdatter Hvide | Cecilie Ebbesdatter |
| `306650341960001516` | Q2221910 | Samuel Symon Willard Sr. | Samuel Willard |
| `312479826640001569` | Q168674 | Sophie Frederika Mathilde von Württemberg Queen consort of the Netherlands | Sophie of Württemberg |
| `317651825030005113` | Q350220 | Magnus III Ladulås Birgersson King of Sweden | Magnus III of Sweden |
| `337578418680004010` | Q172471 | Flavius Julius Valens | Valens |
| `339435131070013659` | Q1663709 | Johannes Johannis Rudbeckius d.ä. | Johannes Rudbeckius |
| `339493353880007732` | Q98108235 | William Bassett of Sandwich | William Bassett |

### Wikidata is a superset

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `1077061` | Q108743024 | Marguerite Blosset | Marguerite de Blosset |
| `348889594040013469` | Q100327211 | Ermengarde | Ermengarde of Provence |
| `353442154280012039` | Q75930730 | Anne Radcliffe | Lady Anne Radcliffe |
| `359281527140013083` | Q210564 | Michael Doukas | Michael VII Doukas |
| `3736500` | Q103955422 | Ann Moncure | Ann Conway (Moncure) |
| `377208681320011176` | Q121464332 | Mercy Porter | Mercy Fitch (Porter) |
| `3996823052360126946` | Q1032321 | Maria Karoline Maria of Austria | Archduchess Maria Karoline of Austria |
| `4194887957440076070` | Q111490 | Geoffrey | Geoffrey Plantagenet, Count of Anjou |
| `4764222` | Q600581 | Leuthard | Leuthard I of Paris |
| `4927794328070059657` | Q60171 | Henry | Henry IX, Duke of Bavaria |
| `4927821238910067084` | Q273181 | Judith of Flanders | Judith of Flanders, Countess of Northumbria |
| `4957925890120125479` | Q451377 | Otto of Savoy | Otto I, Count of Savoy |
| `5020469289250100933` | Q60094 | Henry | Henry IV |
| `5364986739170034579` | Q220994 | Robert | Robert Curthose |
| `5365042495540103778` | Q102005 | William II | William II of England |

### overlap, half or more

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `1064102` | Q108743020 | Jean d'O Seigneur d'O & de Maillebois | Jean d'O, Seigneur d'O, Fresnes, Baillet, Maillebois, Franconville |
| `1077060` | Q108743022 | Robert VII dit Robin D'O Seigneur d'O & de Maillebois | Robert VII d'O, seigneur d'O et de Maillebois |
| `1354801` | Q434077 | Napoléon Joseph Charles Paul Bonaparte 3rd prince de Montfort | Prince Napoléon-Jérôme, Prince Napoléon |
| `1656804` | Q107145462 | Frances Walker | Frances Lucy Baylor |
| `2399215` | Q110303305 | Mogens Mogensen Gyldenstierne | Mogens Mogensen Gyldenstjerne |
| `2430192` | Q182840 | Louis II | Louis the Stammerer |
| `2434135` | Q19914243 | Yolande de Lalaing | Yolande van Lalaing |
| `288390320120001964` | Q3301 | Charles "Martel" Mayor of the Palace | Charles Martel |
| `290615137410002629` | Q11986923 | Ludwig Holgersen Holgersen Rosenkrantz auf Rosendal | Ludvig Holgersen Rosenkrantz |
| `299079241680007968` | Q651883 | Charles Joseph Jean Antoine Ignace Felix de Lorraine | Charles Joseph of Lorraine |
| `302888257510001064` | Q109536562 | Winifred Anne Oldham | Winifred Anne Neville |
| `304435320540004195` | Q57989 | Charles Louis Wittelsbach Elector of the Palatine, K.G. | Charles I Louis, Elector Palatine |
| `3080341` | Q1621801 | Bengt Folkesson | Bengt Snivil |
| `310787864080006466` | Q65878 | Johann VI. zu Anhalt-Zerbst | John VI of Anhalt-Zerbst |
| `312473166720001563` | Q170398 | Wilhelm Friedrich Karl of Württemberg King of Württemberg | Wilhelm I of Württemberg |

### overlap, under half

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `2434772` | Q31191805 | Georg Wolfgang Wilhelm von Sayn-Wittgenstein-Berleburg | George William, Count of Sayn-Wittgenstein-Berleburg |
| `284138677450001022` | Q6082487 | Nicolaus Iohannis Johansson Jr. | Nicolaus Johannis Rudbeckius |
| `294507970270007973` | Q155473 | Katharine of Luxembourg Herzogin von Österreich, Markgräfin von Brandenburg | Catherine of Bohemia |
| `298741096650002960` | Q664454 | Henryk VI Dobry Wrocławski książę z Wrocławski | Henry VI the Good |
| `299466839860007954` | Q793616 | Carl Oscar (Carl) Wilhelm Bernadotte prins av Sverige och Norge, arvfurste, hertig av Västgötland | Prince Carl, Duke of Västergötland |
| `302030903370006491` | Q234734 | Annia Galeria Faustina Major Faustina | Faustina the Elder |
| `302106850500001332` | Q261802 | Januária Maria Joana Carlota Leopoldina Cândida Francisca Xavier de Paula Micaela Gabriela Rafaela de Bragança | Januária, Countess of Aquila |
| `302107417920002914` | Q2720659 | Luigi Carlo Maria Giuseppe di Borbone delle Due Sicilie Conde de Áquila | Prince Louis, Count of Aquila |
| `304433105310001815` | Q57195 | Friedrich V Wittelsbach, Pfalz-Simmern Kürfürst von der Pfalz, König zu Böhmen | Frederick V of the Palatinate |
| `310818848820003860` | Q67155 | Johann I Von Brunswick-Lüneburg Herzog | John, Duke of Brunswick-Lüneburg |
| `310819047470008278` | Q100723 | Otto prins af von Braunschweig-Lüneburg | Otto I of Brunswick-Lüneburg |
| `310870261240004530` | Q519036 | Beatrice de Aragón | Beatrice of Sicily |
| `311695983200008268` | Q77557 | Heinrich Julius Welf Herzog, Fürst zu Braunschweig-Wolfenbüttel Fürst zu Calenberg | Henry Julius, Duke of Brunswick-Lüneburg |
| `311701678080003943` | Q91542 | Elizabeth of Brunswick-Luneburg Braunschweig-Lüneburg , Welf Herzogin zu Sachsen-Altenburg | Elisabeth of Brunswick-Wolfenbüttel, Duchess of Saxe-Altenburg |
| `311713752450007086` | Q819778 | Ulrik Johann Oldenburg Prins, Prinz-bishof von Schwerin | Ulrik of Denmark |

### nothing in common

| geni | item | the rule would produce | Wikidata's English label |
| --- | --- | --- | --- |
| `1354718` | Q168691 | Vittorio Emanuele Maria Alberto Eugenio Ferdinando Tommaso di Savoia | Victor Emmanuel II of Italy |
| `311714621730004586` | Q452932 | Hedvig af Slesvig-Holsteen & Oldenborg Kurfürstin zu Sachsen | Hedwig of Denmark |
| `312468491750006446` | Q170179 | Friedrich Wilhelm Karl | Frederick I of Württemberg |
| `312474987850005822` | Q57662 | Karoline Charlotte Auguste Wittelsbach Kronprinzessin von Württemberg, Kaiserin zu Österreich und HRR | Caroline Augusta of Bavaria |
| `331816214990005036` | Q108935419 | Theoda Porter | Theodia Walbridge |
| `3381491` | Q16130364 | Abraham Joshua Levenshtam Head, Cracow Yeshiva | Avraham Yehoshua Heschel |
| `347868854190012671` | Q266495 | Oluf Hunger Svendsøn | Olaf I of Denmark |
| `353440830330013057` | Q122961015 | Tora Guttormsdotter Vik | Thora |
| `361890384880013875` | Q6146474 | Vasily Dmitriyevich "Kirdyapa" of Suzdal | Vasiliy Kirdyapa |
| `3624121` | Q6032078 | Ingeborga Tryggvės duktė | Ingeborg Tryggvasdotter |
| `365447742810013159` | Q10795576 | Jeanne de la Marche | Joan of Lusignan |
| `367922923820005107` | Q394552 | Agnieszka Władysławówna | Agnes I, Abbess of Quedlinburg |
| `376469227150012924` | Q150642 | Vittorio Emanuele Ferdinando Maria Gennaro di Savoia | Victor Emmanuel III of Italy |
| `376470307830012909` | Q459441 | Ferdinando Maria Alberto Amedeo Filiberto Vincenzo di Savoia duca di Genova | Prince Ferdinand, Duke of Genoa |
| `385953397470012188` | Q41608 | Constantine Porphyrogennetos | Konstantinos VII |

