# Genealogics separates two spellings of ONE name with `|`, and GZWDer's semi-automatic
# import of January 2022 carried the separator into the label. The first reading becomes
# the label and every other becomes an `Amul` alias -- which is the fix you made by hand
# on `Q105815062` (`Gerard|Gerald de Furnival` -> `Gerard de Furnival` + `Gerald de
# Furnival`), applied to the rest.
#
# The comma tail is deliberately NOT touched here: 373 of these also carry one, and
# removing it is `build-noble-label-batch.py`'s job under a scope you set to `noble`.
# Bracketed variant groups -- `Ann Bincks (Benckes|Bench)`, 140 of them -- are held in
# `reports/pipe-labels-held.tsv` because they are a different shape.

# Q3119942  Gallehaut|Guillaume de Rougé, baron de Derval  ->  Gallehaut de Rougé, baron de Derval   + Guillaume de Rougé, baron de Derval
Q3119942	Lmul	"Gallehaut de Rougé, baron de Derval"
Q3119942	Amul	"Guillaume de Rougé, baron de Derval"

# Q62732269  Hans|Johann Greiffenclau zu Vollrads  ->  Hans Greiffenclau zu Vollrads   + Johann Greiffenclau zu Vollrads
Q62732269	Len	"Hans Greiffenclau zu Vollrads"
Q62732269	Amul	"Johann Greiffenclau zu Vollrads"

# Q75251732  Beatriz|Beatrice  ->  Beatriz   + Beatrice
Q75251732	Lmul	"Beatriz"
Q75251732	Amul	"Beatrice"

# Q75462501  Mary|Maria Butler  ->  Mary Butler   + Maria Butler
Q75462501	Lmul	"Mary Butler"
Q75462501	Amul	"Maria Butler"

# Q75582559  Honora|Slaney O'Brien  ->  Honora O'Brien   + Slaney O'Brien
Q75582559	Lmul	"Honora O'Brien"
Q75582559	Amul	"Slaney O'Brien"

# Q76337609  Margaret|Anne Skipwith  ->  Margaret Skipwith   + Anne Skipwith
Q76337609	Lmul	"Margaret Skipwith"
Q76337609	Amul	"Anne Skipwith"

# Q96201734  Elizabeth|Hannah Wheeler  ->  Elizabeth Wheeler   + Hannah Wheeler
Q96201734	Len	"Elizabeth Wheeler"
Q96201734	Lnl	"Elizabeth Wheeler"
Q96201734	Amul	"Hannah Wheeler"

# Q96201964  Joseph|Moses LaFount  ->  Joseph LaFount   + Moses LaFount
Q96201964	Len	"Joseph LaFount"
Q96201964	Lnl	"Joseph LaFount"
Q96201964	Amul	"Moses LaFount"

# Q96209120  William|Richard Hill, of Blore & Court of Hill  ->  William Hill, of Blore & Court of Hill   + Richard Hill, of Blore & Court of Hill
Q96209120	Len	"William Hill, of Blore & Court of Hill"
Q96209120	Lnl	"William Hill, of Blore & Court of Hill"
Q96209120	Amul	"Richard Hill, of Blore & Court of Hill"

# Q96209125  Margaret|Elizabeth Savage, of Kinderton  ->  Margaret Savage, of Kinderton   + Elizabeth Savage, of Kinderton
Q96209125	Len	"Margaret Savage, of Kinderton"
Q96209125	Lnl	"Margaret Savage, of Kinderton"
Q96209125	Amul	"Elizabeth Savage, of Kinderton"

# Q96209131  Thomas|Robert Thimbleby, of Polham-by-Horncastle  ->  Thomas Thimbleby, of Polham-by-Horncastle   + Robert Thimbleby, of Polham-by-Horncastle
Q96209131	Len	"Thomas Thimbleby, of Polham-by-Horncastle"
Q96209131	Lnl	"Thomas Thimbleby, of Polham-by-Horncastle"
Q96209131	Amul	"Robert Thimbleby, of Polham-by-Horncastle"

# Q96210045  Mercy|Mary Littlefield  ->  Mercy Littlefield   + Mary Littlefield
Q96210045	Len	"Mercy Littlefield"
Q96210045	Lnl	"Mercy Littlefield"
Q96210045	Amul	"Mary Littlefield"

# Q96213483  Asahael|Ashael C. Denison  ->  Asahael C. Denison   + Ashael C. Denison
Q96213483	Len	"Asahael C. Denison"
Q96213483	Lnl	"Asahael C. Denison"
Q96213483	Amul	"Ashael C. Denison"

# Q96213497  Mercy|Mary Thomas  ->  Mercy Thomas   + Mary Thomas
Q96213497	Len	"Mercy Thomas"
Q96213497	Lnl	"Mercy Thomas"
Q96213497	Les	"Mercy Thomas"
Q96213497	Amul	"Mary Thomas"

# Q96213527  Ruthella Adelaide|Nettie Delande  ->  Ruthella Adelaide Delande   + Ruthella Nettie Delande
Q96213527	Len	"Ruthella Adelaide Delande"
Q96213527	Lnl	"Ruthella Adelaide Delande"
Q96213527	Amul	"Ruthella Nettie Delande"

# Q96213566  Johanna|Joan Greeneslade  ->  Johanna Greeneslade   + Joan Greeneslade
Q96213566	Len	"Johanna Greeneslade"
Q96213566	Lnl	"Johanna Greeneslade"
Q96213566	Amul	"Joan Greeneslade"

# Q96216881  Jane|Joane Newton  ->  Jane Newton   + Joane Newton
Q96216881	Len	"Jane Newton"
Q96216881	Lnl	"Jane Newton"
Q96216881	Amul	"Joane Newton"

# Q96217392  Elizabeth|Alice Hall  ->  Elizabeth Hall   + Alice Hall
Q96217392	Len	"Elizabeth Hall"
Q96217392	Lnl	"Elizabeth Hall"
Q96217392	Amul	"Alice Hall"

# Q96221454  Johannes|Hans Keller  ->  Johannes Keller   + Hans Keller
Q96221454	Len	"Johannes Keller"
Q96221454	Lnl	"Johannes Keller"
Q96221454	Amul	"Hans Keller"

# Q96221918  Dietrich Metzler|Seckel|Büttel  ->  Dietrich Metzler   + Dietrich Seckel | Dietrich Büttel
Q96221918	Len	"Dietrich Metzler"
Q96221918	Lnl	"Dietrich Metzler"
Q96221918	Amul	"Dietrich Seckel"
Q96221918	Amul	"Dietrich Büttel"

# Q96223603  David|Samuel Stone  ->  David Stone   + Samuel Stone
Q96223603	Len	"David Stone"
Q96223603	Lnl	"David Stone"
Q96223603	Amul	"Samuel Stone"

# Q96223762  Louisa|Elizabeth Long  ->  Louisa Long   + Elizabeth Long
Q96223762	Len	"Louisa Long"
Q96223762	Lnl	"Louisa Long"
Q96223762	Amul	"Elizabeth Long"

# Q96223808  Sarah|Sally Whitcher (Whicher)  ->  Sarah Whitcher (Whicher)   + Sally Whitcher (Whicher)
Q96223808	Len	"Sarah Whitcher (Whicher)"
Q96223808	Amul	"Sally Whitcher (Whicher)"

# Q96224008  Austin|Augustine Kilham (Killam)  ->  Austin Kilham (Killam)   + Augustine Kilham (Killam)
Q96224008	Len	"Austin Kilham (Killam)"
Q96224008	Amul	"Augustine Kilham (Killam)"

# Q96224299  Isabel|Anne  ->  Isabel   + Anne
Q96224299	Len	"Isabel"
Q96224299	Lnl	"Isabel"
Q96224299	Amul	"Anne"

# Q96224387  Joanne|Joyce White  ->  Joanne White   + Joyce White
Q96224387	Len	"Joanne White"
Q96224387	Lnl	"Joanne White"
Q96224387	Amul	"Joyce White"

# Q96224429  Mary|Joan Thomas  ->  Mary Thomas   + Joan Thomas
Q96224429	Len	"Mary Thomas"
Q96224429	Lnl	"Mary Thomas"
Q96224429	Amul	"Joan Thomas"

# Q96235871  Katherine|Catherine Debnam  ->  Katherine Debnam   + Catherine Debnam
Q96235871	Len	"Katherine Debnam"
Q96235871	Lnl	"Katherine Debnam"
Q96235871	Amul	"Catherine Debnam"

# Q96235875  Katherine|Catherine  ->  Katherine   + Catherine
Q96235875	Len	"Katherine"
Q96235875	Lnl	"Katherine"
Q96235875	Amul	"Catherine"

# Q96237703  Ellyne|Ellen  ->  Ellyne   + Ellen
Q96237703	Len	"Ellyne"
Q96237703	Lnl	"Ellyne"
Q96237703	Amul	"Ellen"

# Q96238052  Matilda|Mabilla Falwell (Fawell)  ->  Matilda Falwell (Fawell)   + Mabilla Falwell (Fawell)
Q96238052	Len	"Matilda Falwell (Fawell)"
Q96238052	Amul	"Mabilla Falwell (Fawell)"

# Q96238106  Margaret|Mary Hamley  ->  Margaret Hamley   + Mary Hamley
Q96238106	Len	"Margaret Hamley"
Q96238106	Lnl	"Margaret Hamley"
Q96238106	Amul	"Mary Hamley"

# Q96238111  Elizabeth|Margaret Reynell  ->  Elizabeth Reynell   + Margaret Reynell
Q96238111	Len	"Elizabeth Reynell"
Q96238111	Lnl	"Elizabeth Reynell"
Q96238111	Amul	"Margaret Reynell"

# Q96238144  Joan|Julian (or Minell) Sambnel  ->  Joan (or Minell) Sambnel   + Julian (or Minell) Sambnel
Q96238144	Len	"Joan (or Minell) Sambnel"
Q96238144	Amul	"Julian (or Minell) Sambnel"

# Q96238938  Mihály|Frank Héderváry de Hédervár  ->  Mihály Héderváry de Hédervár   + Frank Héderváry de Hédervár
Q96238938	Lmul	"Mihály Héderváry de Hédervár"
Q96238938	Len	"Mihály Héderváry de Hédervár"
Q96238938	Lnl	"Mihály Héderváry de Hédervár"
Q96238938	Amul	"Frank Héderváry de Hédervár"

# Q96240714  Berete|Birgitte til Krogholm  ->  Berete til Krogholm   + Birgitte til Krogholm
Q96240714	Len	"Berete til Krogholm"
Q96240714	Lnl	"Berete til Krogholm"
Q96240714	Lnb	"Berete til Krogholm"
Q96240714	Amul	"Birgitte til Krogholm"

# Q96240751  Kirstine|Christina de Ager (af Aagaard)  ->  Kirstine de Ager (af Aagaard)   + Christina de Ager (af Aagaard)
Q96240751	Len	"Kirstine de Ager (af Aagaard)"
Q96240751	Amul	"Christina de Ager (af Aagaard)"

# Q96241643  Elisabeth|Lisbeth Smeyers alias de Meyere  ->  Elisabeth Smeyers alias de Meyere   + Lisbeth Smeyers alias de Meyere
Q96241643	Len	"Elisabeth Smeyers alias de Meyere"
Q96241643	Lnl	"Elisabeth Smeyers alias de Meyere"
Q96241643	Amul	"Lisbeth Smeyers alias de Meyere"

# Q96241680  Ida|Aleydis Stas  ->  Ida Stas   + Aleydis Stas
Q96241680	Len	"Ida Stas"
Q96241680	Lnl	"Ida Stas"
Q96241680	Amul	"Aleydis Stas"

# Q96241703  Nicolas|Claes van Aelteren  ->  Nicolas van Aelteren   + Claes van Aelteren
Q96241703	Len	"Nicolas van Aelteren"
Q96241703	Lnl	"Nicolas van Aelteren"
Q96241703	Amul	"Claes van Aelteren"

# Q96242317  Hans|Quirin|Kaspar von Sack  ->  Hans von Sack   + Quirin von Sack | Kaspar von Sack
Q96242317	Len	"Hans von Sack"
Q96242317	Lnl	"Hans von Sack"
Q96242317	Amul	"Quirin von Sack"
Q96242317	Amul	"Kaspar von Sack"

# Q96242393  Cuntz|Konrad von Gross gen. Pfersfelder  ->  Cuntz von Gross gen. Pfersfelder   + Konrad von Gross gen. Pfersfelder
Q96242393	Len	"Cuntz von Gross gen. Pfersfelder"
Q96242393	Lnl	"Cuntz von Gross gen. Pfersfelder"
Q96242393	Amul	"Konrad von Gross gen. Pfersfelder"

# Q96243012  Nicholas|John Bray, of Middlesex  ->  Nicholas Bray, of Middlesex   + John Bray, of Middlesex
Q96243012	Len	"Nicholas Bray, of Middlesex"
Q96243012	Lnl	"Nicholas Bray, of Middlesex"
Q96243012	Amul	"John Bray, of Middlesex"

# Q96243432  Daniel Tichenor|Titchenal  ->  Daniel Tichenor   + Daniel Titchenal
Q96243432	Len	"Daniel Tichenor"
Q96243432	Lnl	"Daniel Tichenor"
Q96243432	Amul	"Daniel Titchenal"

# Q96243684  Béatrix|Isabelle de Clisson, Comtesse de Porhöet  ->  Béatrix de Clisson, Comtesse de Porhöet   + Isabelle de Clisson, Comtesse de Porhöet
Q96243684	Len	"Béatrix de Clisson, Comtesse de Porhöet"
Q96243684	Lnl	"Béatrix de Clisson, Comtesse de Porhöet"
Q96243684	Amul	"Isabelle de Clisson, Comtesse de Porhöet"

# Q96244770  Marguerite|Marie de Créquy  ->  Marguerite de Créquy   + Marie de Créquy
Q96244770	Len	"Marguerite de Créquy"
Q96244770	Lnl	"Marguerite de Créquy"
Q96244770	Amul	"Marie de Créquy"

# Q96245029  Jolande|Yolande de Bar, Heiress of Ancerville  ->  Jolande de Bar, Heiress of Ancerville   + Yolande de Bar, Heiress of Ancerville
Q96245029	Len	"Jolande de Bar, Heiress of Ancerville"
Q96245029	Lnl	"Jolande de Bar, Heiress of Ancerville"
Q96245029	Amul	"Yolande de Bar, Heiress of Ancerville"

# Q96290622  Capt. Henry|John Davidge  ->  Capt. Henry Davidge   + Capt. John Davidge
Q96290622	Len	"Capt. Henry Davidge"
Q96290622	Lnl	"Capt. Henry Davidge"
Q96290622	Amul	"Capt. John Davidge"

# Q96290639  William|Wilhelmina Hathorn Stewart  ->  William Hathorn Stewart   + Wilhelmina Hathorn Stewart
Q96290639	Len	"William Hathorn Stewart"
Q96290639	Lnl	"William Hathorn Stewart"
Q96290639	Amul	"Wilhelmina Hathorn Stewart"

# Q96304881  Agnes|Anne Griffith of Plas Newydd  ->  Agnes Griffith of Plas Newydd   + Anne Griffith of Plas Newydd
Q96304881	Len	"Agnes Griffith of Plas Newydd"
Q96304881	Lnl	"Agnes Griffith of Plas Newydd"
Q96304881	Amul	"Anne Griffith of Plas Newydd"

# Q96305259  Urania|Lurany De Forest  ->  Urania De Forest   + Lurany De Forest
Q96305259	Len	"Urania De Forest"
Q96305259	Lnl	"Urania De Forest"
Q96305259	Amul	"Lurany De Forest"

# Q96316545  Georg Philipp Sommerlath|Sommerlad  ->  Georg Philipp Sommerlath   + Georg Philipp Sommerlad
Q96316545	Len	"Georg Philipp Sommerlath"
Q96316545	Lnl	"Georg Philipp Sommerlath"
Q96316545	Lcs	"Georg Philipp Sommerlath"
Q96316545	Amul	"Georg Philipp Sommerlad"

# Q96317833  Anna Margarete Werner|Woerner  ->  Anna Margarete Werner   + Anna Margarete Woerner
Q96317833	Len	"Anna Margarete Werner"
Q96317833	Lnl	"Anna Margarete Werner"
Q96317833	Amul	"Anna Margarete Woerner"

# Q96317839  Johann Ludwig Betulius|Birkner  ->  Johann Ludwig Betulius   + Johann Ludwig Birkner
Q96317839	Len	"Johann Ludwig Betulius"
Q96317839	Lnl	"Johann Ludwig Betulius"
Q96317839	Amul	"Johann Ludwig Birkner"

# Q96337610  Jane|Joanna Syms  ->  Jane Syms   + Joanna Syms
Q96337610	Len	"Jane Syms"
Q96337610	Lnl	"Jane Syms"
Q96337610	Amul	"Joanna Syms"

# Q96375588  Anne|Agnes Welsh  ->  Anne Welsh   + Agnes Welsh
Q96375588	Len	"Anne Welsh"
Q96375588	Lnl	"Anne Welsh"
Q96375588	Amul	"Agnes Welsh"

# Q96480441  Alexander|Stephen Cope  ->  Alexander Cope   + Stephen Cope
Q96480441	Len	"Alexander Cope"
Q96480441	Lnl	"Alexander Cope"
Q96480441	Amul	"Stephen Cope"

# Q96480443  Sybill|Sibyl Fowler  ->  Sybill Fowler   + Sibyl Fowler
Q96480443	Len	"Sybill Fowler"
Q96480443	Lnl	"Sybill Fowler"
Q96480443	Amul	"Sibyl Fowler"

# Q96621681  Mary Flood|fford  ->  Mary Flood   + Mary fford
Q96621681	Len	"Mary Flood"
Q96621681	Lnl	"Mary Flood"
Q96621681	Amul	"Mary fford"

# Q96621684  Elizabeth Bayinn|Bavin  ->  Elizabeth Bayinn   + Elizabeth Bavin
Q96621684	Len	"Elizabeth Bayinn"
Q96621684	Lnl	"Elizabeth Bayinn"
Q96621684	Amul	"Elizabeth Bavin"

# Q96739460  Michal|Michell|Micaell Jennison  ->  Michal Jennison   + Michell Jennison | Micaell Jennison
Q96739460	Len	"Michal Jennison"
Q96739460	Lnl	"Michal Jennison"
Q96739460	Amul	"Michell Jennison"
Q96739460	Amul	"Micaell Jennison"

# Q96778115  John|Thomas Stottusbury, of Sulgrave  ->  John Stottusbury, of Sulgrave   + Thomas Stottusbury, of Sulgrave
Q96778115	Len	"John Stottusbury, of Sulgrave"
Q96778115	Lnl	"John Stottusbury, of Sulgrave"
Q96778115	Amul	"Thomas Stottusbury, of Sulgrave"

# Q96778566  Isaak Lambert Thyssen|Thissen  ->  Isaak Lambert Thyssen   + Isaak Lambert Thissen
Q96778566	Len	"Isaak Lambert Thyssen"
Q96778566	Lnl	"Isaak Lambert Thyssen"
Q96778566	Amul	"Isaak Lambert Thissen"

# Q97008391  Helen|Ellen Skipwith  ->  Helen Skipwith   + Ellen Skipwith
Q97008391	Len	"Helen Skipwith"
Q97008391	Lnl	"Helen Skipwith"
Q97008391	Amul	"Ellen Skipwith"

# Q97014050  Gerotheus|Jerotheus von Rathsamhausen zum Stein  ->  Gerotheus von Rathsamhausen zum Stein   + Jerotheus von Rathsamhausen zum Stein
Q97014050	Len	"Gerotheus von Rathsamhausen zum Stein"
Q97014050	Lnl	"Gerotheus von Rathsamhausen zum Stein"
Q97014050	Amul	"Jerotheus von Rathsamhausen zum Stein"

# Q97089419  Ellen|Eleanor|Helen Pell  ->  Ellen Pell   + Eleanor Pell | Helen Pell
Q97089419	Len	"Ellen Pell"
Q97089419	Lnl	"Ellen Pell"
Q97089419	Amul	"Eleanor Pell"
Q97089419	Amul	"Helen Pell"

# Q97568624  Ela|Eleanor Spelman  ->  Ela Spelman   + Eleanor Spelman
Q97568624	Len	"Ela Spelman"
Q97568624	Lnl	"Ela Spelman"
Q97568624	Amul	"Eleanor Spelman"

# Q97568630  Ellen|Ela Narborough (Narborow)  ->  Ellen Narborough (Narborow)   + Ela Narborough (Narborow)
Q97568630	Len	"Ellen Narborough (Narborow)"
Q97568630	Amul	"Ela Narborough (Narborow)"

# Q97568633  Elizabeth|Alicia Clere, of Stokesby  ->  Elizabeth Clere, of Stokesby   + Alicia Clere, of Stokesby
Q97568633	Len	"Elizabeth Clere, of Stokesby"
Q97568633	Lnl	"Elizabeth Clere, of Stokesby"
Q97568633	Amul	"Alicia Clere, of Stokesby"

# Q97570404  Mary|Maria Clitheroe (Cliderow)  ->  Mary Clitheroe (Cliderow)   + Maria Clitheroe (Cliderow)
Q97570404	Len	"Mary Clitheroe (Cliderow)"
Q97570404	Amul	"Maria Clitheroe (Cliderow)"

# Q97783235  Ysoul|Iseul de Sully, Dame de Varennes  ->  Ysoul de Sully, Dame de Varennes   + Iseul de Sully, Dame de Varennes
Q97783235	Len	"Ysoul de Sully, Dame de Varennes"
Q97783235	Lnl	"Ysoul de Sully, Dame de Varennes"
Q97783235	Amul	"Iseul de Sully, Dame de Varennes"

# Q97783426  Susanna|Giovanna Tocco  ->  Susanna Tocco   + Giovanna Tocco
Q97783426	Len	"Susanna Tocco"
Q97783426	Lnl	"Susanna Tocco"
Q97783426	Amul	"Giovanna Tocco"

# Q98072376  Joan Tue|Tew  ->  Joan Tue   + Joan Tew
Q98072376	Len	"Joan Tue"
Q98072376	Lnl	"Joan Tue"
Q98072376	Amul	"Joan Tew"

# Q98072377  Thomas Tue|Tew  ->  Thomas Tue   + Thomas Tew
Q98072377	Len	"Thomas Tue"
Q98072377	Lnl	"Thomas Tue"
Q98072377	Amul	"Thomas Tew"

# Q98100982  Macuth|Matthew Pratt  ->  Macuth Pratt   + Matthew Pratt
Q98100982	Len	"Macuth Pratt"
Q98100982	Lnl	"Macuth Pratt"
Q98100982	Amul	"Matthew Pratt"

# Q98101021  Phoebe|Phebe Hicks  ->  Phoebe Hicks   + Phebe Hicks
Q98101021	Len	"Phoebe Hicks"
Q98101021	Lnl	"Phoebe Hicks"
Q98101021	Amul	"Phebe Hicks"

# Q98103245  Amy|Amicia Danvers  ->  Amy Danvers   + Amicia Danvers
Q98103245	Len	"Amy Danvers"
Q98103245	Lnl	"Amy Danvers"
Q98103245	Amul	"Amicia Danvers"

# Q98697686  Estrid|Sestrid Knudsdotter  ->  Estrid Knudsdotter   + Sestrid Knudsdotter
Q98697686	Len	"Estrid Knudsdotter"
Q98697686	Lnl	"Estrid Knudsdotter"
Q98697686	Amul	"Sestrid Knudsdotter"

# Q98697698  Merete|Margareta Pedersdotter af Dollefjelde  ->  Merete Pedersdotter af Dollefjelde   + Margareta Pedersdotter af Dollefjelde
Q98697698	Len	"Merete Pedersdotter af Dollefjelde"
Q98697698	Lnl	"Merete Pedersdotter af Dollefjelde"
Q98697698	Amul	"Margareta Pedersdotter af Dollefjelde"

# Q98697706  knight Knud|Knut Gislason 'April'  ->  knight Knud Gislason 'April'   + knight Knut Gislason 'April'
Q98697706	Len	"knight Knud Gislason 'April'"
Q98697706	Lnl	"knight Knud Gislason 'April'"
Q98697706	Amul	"knight Knut Gislason 'April'"

# Q98697729  Aage|Åke Ingvarsson [Bät], Lord of Bjerghusaholm  ->  Aage Ingvarsson [Bät], Lord of Bjerghusaholm   + Åke Ingvarsson [Bät], Lord of Bjerghusaholm
Q98697729	Len	"Aage Ingvarsson [Bät], Lord of Bjerghusaholm"
Q98697729	Lnl	"Aage Ingvarsson [Bät], Lord of Bjerghusaholm"
Q98697729	Amul	"Åke Ingvarsson [Bät], Lord of Bjerghusaholm"

# Q98698463  Hannes|Johannes Maydel, Lord of Valtu  ->  Hannes Maydel, Lord of Valtu   + Johannes Maydel, Lord of Valtu
Q98698463	Len	"Hannes Maydel, Lord of Valtu"
Q98698463	Lnl	"Hannes Maydel, Lord of Valtu"
Q98698463	Amul	"Johannes Maydel, Lord of Valtu"

# Q98698468  Maia|Maret Tuve  ->  Maia Tuve   + Maret Tuve
Q98698468	Len	"Maia Tuve"
Q98698468	Lnl	"Maia Tuve"
Q98698468	Amul	"Maret Tuve"

# Q98698633  Eylart|Elert von Kruse  ->  Eylart von Kruse   + Elert von Kruse
Q98698633	Len	"Eylart von Kruse"
Q98698633	Lnl	"Eylart von Kruse"
Q98698633	Amul	"Elert von Kruse"

# Q98960270  Godeheut|Godehold de Toeni  ->  Godeheut de Toeni   + Godehold de Toeni
Q98960270	Len	"Godeheut de Toeni"
Q98960270	Lnl	"Godeheut de Toeni"
Q98960270	Amul	"Godehold de Toeni"

# Q98960285  Grace|Grecia  ->  Grace   + Grecia
Q98960285	Len	"Grace"
Q98960285	Lnl	"Grace"
Q98960285	Amul	"Grecia"

# Q98960292  Grace|Gracia  ->  Grace   + Gracia
Q98960292	Len	"Grace"
Q98960292	Lnl	"Grace"
Q98960292	Amul	"Gracia"

# Q98961125  Anne|Ann Mellish  ->  Anne Mellish   + Ann Mellish
Q98961125	Len	"Anne Mellish"
Q98961125	Lnl	"Anne Mellish"
Q98961125	Amul	"Ann Mellish"

# Q98961229  Agnes|Anne Parker  ->  Agnes Parker   + Anne Parker
Q98961229	Len	"Agnes Parker"
Q98961229	Lnl	"Agnes Parker"
Q98961229	Amul	"Anne Parker"

# Q98961978  Jane|Joan Gifford, of Itchell  ->  Jane Gifford, of Itchell   + Joan Gifford, of Itchell
Q98961978	Len	"Jane Gifford, of Itchell"
Q98961978	Lnl	"Jane Gifford, of Itchell"
Q98961978	Amul	"Joan Gifford, of Itchell"

# Q98962450  Jos|Jodokus Alber  ->  Jos Alber   + Jodokus Alber
Q98962450	Len	"Jos Alber"
Q98962450	Lnl	"Jos Alber"
Q98962450	Amul	"Jodokus Alber"

# Q98967461  Isabel|Elizabeth Bendysshe  ->  Isabel Bendysshe   + Elizabeth Bendysshe
Q98967461	Len	"Isabel Bendysshe"
Q98967461	Lnl	"Isabel Bendysshe"
Q98967461	Amul	"Elizabeth Bendysshe"

# Q98967474  Matilda|Maud Cooke, of Lavenham  ->  Matilda Cooke, of Lavenham   + Maud Cooke, of Lavenham
Q98967474	Len	"Matilda Cooke, of Lavenham"
Q98967474	Lnl	"Matilda Cooke, of Lavenham"
Q98967474	Amul	"Maud Cooke, of Lavenham"

# Q98971057  Mary|Elizabeth|Mariot|Marion Douglas, of Parkhead  ->  Mary Douglas, of Parkhead   + Elizabeth Douglas, of Parkhead | Mariot Douglas, of Parkhead | Marion Douglas, of Parkhead
Q98971057	Len	"Mary Douglas, of Parkhead"
Q98971057	Lnl	"Mary Douglas, of Parkhead"
Q98971057	Amul	"Elizabeth Douglas, of Parkhead"
Q98971057	Amul	"Mariot Douglas, of Parkhead"
Q98971057	Amul	"Marion Douglas, of Parkhead"

# Q99021436  Agnes|Jane Launcelyn  ->  Agnes Launcelyn   + Jane Launcelyn
Q99021436	Len	"Agnes Launcelyn"
Q99021436	Lnl	"Agnes Launcelyn"
Q99021436	Amul	"Jane Launcelyn"

# Q99022881  Margaret|Joanna Pert  ->  Margaret Pert   + Joanna Pert
Q99022881	Len	"Margaret Pert"
Q99022881	Lnl	"Margaret Pert"
Q99022881	Amul	"Joanna Pert"

# Q99023088  Joan|Juliana de Stainton  ->  Joan de Stainton   + Juliana de Stainton
Q99023088	Len	"Joan de Stainton"
Q99023088	Lnl	"Joan de Stainton"
Q99023088	Amul	"Juliana de Stainton"

# Q99066584  Elsbeth|Elizabeth ferch Thomas ap Watkin Vaughan  ->  Elsbeth ferch Thomas ap Watkin Vaughan   + Elizabeth ferch Thomas ap Watkin Vaughan
Q99066584	Len	"Elsbeth ferch Thomas ap Watkin Vaughan"
Q99066584	Lnl	"Elsbeth ferch Thomas ap Watkin Vaughan"
Q99066584	Amul	"Elizabeth ferch Thomas ap Watkin Vaughan"

# Q99067235  Elisabeth|Elsbeth Wogan  ->  Elisabeth Wogan   + Elsbeth Wogan
Q99067235	Len	"Elisabeth Wogan"
Q99067235	Lnl	"Elisabeth Wogan"
Q99067235	Amul	"Elsbeth Wogan"

# Q99067261  Elinor|Eleanor Whitney  ->  Elinor Whitney   + Eleanor Whitney
Q99067261	Len	"Elinor Whitney"
Q99067261	Lnl	"Elinor Whitney"
Q99067261	Amul	"Eleanor Whitney"

# Q99067844  Jenet|Elinor ferch Jenkin Horton, of Llandoch  ->  Jenet ferch Jenkin Horton, of Llandoch   + Elinor ferch Jenkin Horton, of Llandoch
Q99067844	Len	"Jenet ferch Jenkin Horton, of Llandoch"
Q99067844	Lnl	"Jenet ferch Jenkin Horton, of Llandoch"
Q99067844	Amul	"Elinor ferch Jenkin Horton, of Llandoch"

# Q99068149  Matilda|Janet? Dennis  ->  Matilda Dennis   + Janet? Dennis
Q99068149	Len	"Matilda Dennis"
Q99068149	Lnl	"Matilda Dennis"
Q99068149	Amul	"Janet? Dennis"

# Q99069983  Maud|Alice Bostock  ->  Maud Bostock   + Alice Bostock
Q99069983	Len	"Maud Bostock"
Q99069983	Lnl	"Maud Bostock"
Q99069983	Amul	"Alice Bostock"

# Q99070448  Eleanor|Elen Puleston  ->  Eleanor Puleston   + Elen Puleston
Q99070448	Len	"Eleanor Puleston"
Q99070448	Lnl	"Eleanor Puleston"
Q99070448	Amul	"Elen Puleston"

# Q99072547  Generys|Angharad ferch Gruffudd ab Owain ap Bleddyn  ->  Generys ferch Gruffudd ab Owain ap Bleddyn   + Angharad ferch Gruffudd ab Owain ap Bleddyn
Q99072547	Len	"Generys ferch Gruffudd ab Owain ap Bleddyn"
Q99072547	Lnl	"Generys ferch Gruffudd ab Owain ap Bleddyn"
Q99072547	Amul	"Angharad ferch Gruffudd ab Owain ap Bleddyn"

# Q99082377  Gwenhwyfar|Gwenllian verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor  ->  Gwenhwyfar verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor   + Gwenllian verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor
Q99082377	Len	"Gwenhwyfar verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor"
Q99082377	Lnl	"Gwenhwyfar verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor"
Q99082377	Amul	"Gwenllian verch Adda Gôch ab Ieuaf ab Adda ab Awr of Trevor"

# Q99084357  Gwenthellean|Gwenllian Talbot  ->  Gwenthellean Talbot   + Gwenllian Talbot
Q99084357	Len	"Gwenthellean Talbot"
Q99084357	Lnl	"Gwenthellean Talbot"
Q99084357	Amul	"Gwenllian Talbot"

# Q99085454  Philip|Wilcock Wiriot  ->  Philip Wiriot   + Wilcock Wiriot
Q99085454	Len	"Philip Wiriot"
Q99085454	Lnl	"Philip Wiriot"
Q99085454	Amul	"Wilcock Wiriot"

# Q99091059  Margaret|Mary Stephenson (FitzStephen)  ->  Margaret Stephenson (FitzStephen)   + Mary Stephenson (FitzStephen)
Q99091059	Len	"Margaret Stephenson (FitzStephen)"
Q99091059	Amul	"Mary Stephenson (FitzStephen)"

# Q99100433  Roger|Robert Debden, of Brampton, Suffolk  ->  Roger Debden, of Brampton, Suffolk   + Robert Debden, of Brampton, Suffolk
Q99100433	Len	"Roger Debden, of Brampton, Suffolk"
Q99100433	Lnl	"Roger Debden, of Brampton, Suffolk"
Q99100433	Amul	"Robert Debden, of Brampton, Suffolk"

# Q99100463  Margaret Doreward|Durward  ->  Margaret Doreward   + Margaret Durward
Q99100463	Len	"Margaret Doreward"
Q99100463	Lnl	"Margaret Doreward"
Q99100463	Amul	"Margaret Durward"

# Q99100470  William|Richard|Roger Doreward, of Doreward, Essex  ->  William Doreward, of Doreward, Essex   + Richard Doreward, of Doreward, Essex | Roger Doreward, of Doreward, Essex
Q99100470	Len	"William Doreward, of Doreward, Essex"
Q99100470	Lnl	"William Doreward, of Doreward, Essex"
Q99100470	Amul	"Richard Doreward, of Doreward, Essex"
Q99100470	Amul	"Roger Doreward, of Doreward, Essex"

# Q99100477  Margaret|Joan Arsic (Harsicke)  ->  Margaret Arsic (Harsicke)   + Joan Arsic (Harsicke)
Q99100477	Len	"Margaret Arsic (Harsicke)"
Q99100477	Amul	"Joan Arsic (Harsicke)"

# Q99154226  Margaret|?Katherine  ->  Margaret   + ?Katherine
Q99154226	Len	"Margaret"
Q99154226	Lnl	"Margaret"
Q99154226	Amul	"?Katherine"

# Q99177445  Joan|Margaret Newdigate  ->  Joan Newdigate   + Margaret Newdigate
Q99177445	Len	"Joan Newdigate"
Q99177445	Lnl	"Joan Newdigate"
Q99177445	Amul	"Margaret Newdigate"

# Q99183331  Margaret|Cicely de Bromhall (Bramhall)  ->  Margaret de Bromhall (Bramhall)   + Cicely de Bromhall (Bramhall)
Q99183331	Len	"Margaret de Bromhall (Bramhall)"
Q99183331	Amul	"Cicely de Bromhall (Bramhall)"

# Q99186837  Mary|Mercy Carew, of Beddington  ->  Mary Carew, of Beddington   + Mercy Carew, of Beddington
Q99186837	Len	"Mary Carew, of Beddington"
Q99186837	Lnl	"Mary Carew, of Beddington"
Q99186837	Amul	"Mercy Carew, of Beddington"

# Q99199164  Margery|Margaret  ->  Margery   + Margaret
Q99199164	Len	"Margery"
Q99199164	Lnl	"Margery"
Q99199164	Amul	"Margaret"

# Q99204339  Margaret|Margery Billingford  ->  Margaret Billingford   + Margery Billingford
Q99204339	Len	"Margaret Billingford"
Q99204339	Lnl	"Margaret Billingford"
Q99204339	Amul	"Margery Billingford"

# Q99204570  George|John Tourney, of Motcombe  ->  George Tourney, of Motcombe   + John Tourney, of Motcombe
Q99204570	Len	"George Tourney, of Motcombe"
Q99204570	Lnl	"George Tourney, of Motcombe"
Q99204570	Amul	"John Tourney, of Motcombe"

# Q99204581  Jane|Joan  ->  Jane   + Joan
Q99204581	Len	"Jane"
Q99204581	Lnl	"Jane"
Q99204581	Amul	"Joan"

# Q99208467  Margaret|Margred Kemeys  ->  Margaret Kemeys   + Margred Kemeys
Q99208467	Len	"Margaret Kemeys"
Q99208467	Lnl	"Margaret Kemeys"
Q99208467	Amul	"Margred Kemeys"

# Q99208871  Isabel|Elizabeth  ->  Isabel   + Elizabeth
Q99208871	Len	"Isabel"
Q99208871	Lnl	"Isabel"
Q99208871	Amul	"Elizabeth"

# Q99210266  Niklaus|Claus von Diesbach  ->  Niklaus von Diesbach   + Claus von Diesbach
Q99210266	Len	"Niklaus von Diesbach"
Q99210266	Lnl	"Niklaus von Diesbach"
Q99210266	Amul	"Claus von Diesbach"

# Q99210288  Johanna|Jonatha von Mömpelgard  ->  Johanna von Mömpelgard   + Jonatha von Mömpelgard
Q99210288	Len	"Johanna von Mömpelgard"
Q99210288	Lnl	"Johanna von Mömpelgard"
Q99210288	Amul	"Jonatha von Mömpelgard"

# Q99210290  Veronika|Vérène von Hunwyl (Hunwill)  ->  Veronika von Hunwyl (Hunwill)   + Vérène von Hunwyl (Hunwill)
Q99210290	Len	"Veronika von Hunwyl (Hunwill)"
Q99210290	Amul	"Vérène von Hunwyl (Hunwill)"

# Q99210308  Marguerite|Magdalena Bugniet  ->  Marguerite Bugniet   + Magdalena Bugniet
Q99210308	Len	"Marguerite Bugniet"
Q99210308	Lnl	"Marguerite Bugniet"
Q99210308	Amul	"Magdalena Bugniet"

# Q99210313  Nikolaus|Nikod Buginet  ->  Nikolaus Buginet   + Nikod Buginet
Q99210313	Len	"Nikolaus Buginet"
Q99210313	Lnl	"Nikolaus Buginet"
Q99210313	Amul	"Nikod Buginet"

# Q99210418  Niclaus|Niklaus von Wattenwyl  ->  Niclaus von Wattenwyl   + Niklaus von Wattenwyl
Q99210418	Len	"Niclaus von Wattenwyl"
Q99210418	Lnl	"Niclaus von Wattenwyl"
Q99210418	Amul	"Niklaus von Wattenwyl"

# Q99210452  Henman|Hans von Rüssegg  ->  Henman von Rüssegg   + Hans von Rüssegg
Q99210452	Len	"Henman von Rüssegg"
Q99210452	Lnl	"Henman von Rüssegg"
Q99210452	Amul	"Hans von Rüssegg"

# Q99210457  Elisabeth|Anna von Rinach (Reinach)  ->  Elisabeth von Rinach (Reinach)   + Anna von Rinach (Reinach)
Q99210457	Len	"Elisabeth von Rinach (Reinach)"
Q99210457	Amul	"Anna von Rinach (Reinach)"

# Q99211407  Joan|Elizabeth Stanhope, of Shelford  ->  Joan Stanhope, of Shelford   + Elizabeth Stanhope, of Shelford
Q99211407	Len	"Joan Stanhope, of Shelford"
Q99211407	Lnl	"Joan Stanhope, of Shelford"
Q99211407	Amul	"Elizabeth Stanhope, of Shelford"

# Q99211427  Jane|Joan Beler  ->  Jane Beler   + Joan Beler
Q99211427	Len	"Jane Beler"
Q99211427	Lnl	"Jane Beler"
Q99211427	Amul	"Joan Beler"

# Q99211430  Francis|John Clarke, of Whissendine  ->  Francis Clarke, of Whissendine   + John Clarke, of Whissendine
Q99211430	Len	"Francis Clarke, of Whissendine"
Q99211430	Lnl	"Francis Clarke, of Whissendine"
Q99211430	Amul	"John Clarke, of Whissendine"

# Q99211460  Jenkin|John ap John ap Henry Kemeys, of Began  ->  Jenkin ap John ap Henry Kemeys, of Began   + John ap John ap Henry Kemeys, of Began
Q99211460	Len	"Jenkin ap John ap Henry Kemeys, of Began"
Q99211460	Lnl	"Jenkin ap John ap Henry Kemeys, of Began"
Q99211460	Amul	"John ap John ap Henry Kemeys, of Began"

# Q99211462  Crisli|Elizabeth ferch Morgan ap Llywelyn ab Ifor of Tredegar  ->  Crisli ferch Morgan ap Llywelyn ab Ifor of Tredegar   + Elizabeth ferch Morgan ap Llywelyn ab Ifor of Tredegar
Q99211462	Len	"Crisli ferch Morgan ap Llywelyn ab Ifor of Tredegar"
Q99211462	Lnl	"Crisli ferch Morgan ap Llywelyn ab Ifor of Tredegar"
Q99211462	Amul	"Elizabeth ferch Morgan ap Llywelyn ab Ifor of Tredegar"

# Q99211664  Jenkin|John ap Henry ap Meurig Kemys/Kemeys  ->  Jenkin ap Henry ap Meurig Kemys/Kemeys   + John ap Henry ap Meurig Kemys/Kemeys
Q99211664	Len	"Jenkin ap Henry ap Meurig Kemys/Kemeys"
Q99211664	Lnl	"Jenkin ap Henry ap Meurig Kemys/Kemeys"
Q99211664	Amul	"John ap Henry ap Meurig Kemys/Kemeys"

# Q99211667  Henry ap Meurig Kemys|Kemeys  ->  Henry ap Meurig Kemys   + Henry ap Meurig Kemeys
Q99211667	Len	"Henry ap Meurig Kemys"
Q99211667	Lnl	"Henry ap Meurig Kemys"
Q99211667	Amul	"Henry ap Meurig Kemeys"

# Q99211669  Meurig Kemys|Kemeys  ->  Meurig Kemys   + Meurig Kemeys
Q99211669	Len	"Meurig Kemys"
Q99211669	Lnl	"Meurig Kemys"
Q99211669	Amul	"Meurig Kemeys"

# Q99239037  Alswn|Alice Malephant  ->  Alswn Malephant   + Alice Malephant
Q99239037	Len	"Alswn Malephant"
Q99239037	Lnl	"Alswn Malephant"
Q99239037	Amul	"Alice Malephant"

# Q99239118  Margaret|Margred Fleming  ->  Margaret Fleming   + Margred Fleming
Q99239118	Len	"Margaret Fleming"
Q99239118	Lnl	"Margaret Fleming"
Q99239118	Amul	"Margred Fleming"

# Q99240367  John|Thomas Rich  ->  John Rich   + Thomas Rich
Q99240367	Len	"John Rich"
Q99240367	Lnl	"John Rich"
Q99240367	Amul	"Thomas Rich"

# Q99301896  Dorothea|Dordi Delwig  ->  Dorothea Delwig   + Dordi Delwig
Q99301896	Len	"Dorothea Delwig"
Q99301896	Lnl	"Dorothea Delwig"
Q99301896	Amul	"Dordi Delwig"

# Q99301905  knight Jens|Jon|Jöns|Johannes 'Bonde', lord of Traneberg & Stensholmen  ->  knight Jens 'Bonde', lord of Traneberg & Stensholmen   + knight Jon 'Bonde', lord of Traneberg & Stensholmen | knight Jöns 'Bonde', lord of Traneberg & Stensholmen | knight Johannes 'Bonde', lord of Traneberg & Stensholmen
Q99301905	Len	"knight Jens 'Bonde', lord of Traneberg & Stensholmen"
Q99301905	Lnl	"knight Jens 'Bonde', lord of Traneberg & Stensholmen"
Q99301905	Amul	"knight Jon 'Bonde', lord of Traneberg & Stensholmen"
Q99301905	Amul	"knight Jöns 'Bonde', lord of Traneberg & Stensholmen"
Q99301905	Amul	"knight Johannes 'Bonde', lord of Traneberg & Stensholmen"

# Q99304143  Astrige|Eustorge  ->  Astrige   + Eustorge
Q99304143	Len	"Astrige"
Q99304143	Lnl	"Astrige"
Q99304143	Amul	"Eustorge"

# Q99658654  Mary|Margery Yewelton (Yeovilton)  ->  Mary Yewelton (Yeovilton)   + Margery Yewelton (Yeovilton)
Q99658654	Len	"Mary Yewelton (Yeovilton)"
Q99658654	Amul	"Margery Yewelton (Yeovilton)"

# Q99674911  Ellen|Margaret Warburton  ->  Ellen Warburton   + Margaret Warburton
Q99674911	Len	"Ellen Warburton"
Q99674911	Lnl	"Ellen Warburton"
Q99674911	Amul	"Margaret Warburton"

# Q99674963  Robert|Roger Barrow, of Flookers Brook  ->  Robert Barrow, of Flookers Brook   + Roger Barrow, of Flookers Brook
Q99674963	Len	"Robert Barrow, of Flookers Brook"
Q99674963	Lnl	"Robert Barrow, of Flookers Brook"
Q99674963	Amul	"Roger Barrow, of Flookers Brook"

# Q99707355  Alice|Elizabeth Barrington  ->  Alice Barrington   + Elizabeth Barrington
Q99707355	Len	"Alice Barrington"
Q99707355	Lnl	"Alice Barrington"
Q99707355	Les	"Alice Barrington"
Q99707355	Amul	"Elizabeth Barrington"

# Q99707421  Margaret|Mary Blyant  ->  Margaret Blyant   + Mary Blyant
Q99707421	Len	"Margaret Blyant"
Q99707421	Lnl	"Margaret Blyant"
Q99707421	Amul	"Mary Blyant"

# Q99707425  Margaret|Margery Alcocke  ->  Margaret Alcocke   + Margery Alcocke
Q99707425	Len	"Margaret Alcocke"
Q99707425	Lnl	"Margaret Alcocke"
Q99707425	Amul	"Margery Alcocke"

# Q99735761  Margery|Margeria  ->  Margery   + Margeria
Q99735761	Len	"Margery"
Q99735761	Lnl	"Margery"
Q99735761	Amul	"Margeria"

# Q99800478  Sir David|Miles Skull  ->  Sir David Skull   + Sir Miles Skull
Q99800478	Len	"Sir David Skull"
Q99800478	Lnl	"Sir David Skull"
Q99800478	Amul	"Sir Miles Skull"

# Q99803748  Denise|Dionisia Tempest, of Studley  ->  Denise Tempest, of Studley   + Dionisia Tempest, of Studley
Q99803748	Len	"Denise Tempest, of Studley"
Q99803748	Lnl	"Denise Tempest, of Studley"
Q99803748	Amul	"Dionisia Tempest, of Studley"

# Q99803886  Laura|Lora FitzHugh  ->  Laura FitzHugh   + Lora FitzHugh
Q99803886	Len	"Laura FitzHugh"
Q99803886	Lnl	"Laura FitzHugh"
Q99803886	Amul	"Lora FitzHugh"

# Q99804016  Joan|Jane  ->  Joan   + Jane
Q99804016	Len	"Joan"
Q99804016	Lnl	"Joan"
Q99804016	Amul	"Jane"

# Q99804414  Dionysia|Denise  ->  Dionysia   + Denise
Q99804414	Len	"Dionysia"
Q99804414	Lnl	"Dionysia"
Q99804414	Amul	"Denise"

# Q99804421  Jane|Joan Tunstall  ->  Jane Tunstall   + Joan Tunstall
Q99804421	Len	"Jane Tunstall"
Q99804421	Lnl	"Jane Tunstall"
Q99804421	Amul	"Joan Tunstall"

# Q99805205  Thomas|John Towers, of Somerby  ->  Thomas Towers, of Somerby   + John Towers, of Somerby
Q99805205	Len	"Thomas Towers, of Somerby"
Q99805205	Lnl	"Thomas Towers, of Somerby"
Q99805205	Amul	"John Towers, of Somerby"

# Q99805262  William|Henry de Tunstall  ->  William de Tunstall   + Henry de Tunstall
Q99805262	Len	"William de Tunstall"
Q99805262	Lnl	"William de Tunstall"
Q99805262	Amul	"Henry de Tunstall"

# Q99806018  Ivette|Juette de Ros  ->  Ivette de Ros   + Juette de Ros
Q99806018	Len	"Ivette de Ros"
Q99806018	Lnl	"Ivette de Ros"
Q99806018	Amul	"Juette de Ros"

# Q99807109  Sir William|Ralph Babthorp  ->  Sir William Babthorp   + Sir Ralph Babthorp
Q99807109	Len	"Sir William Babthorp"
Q99807109	Lnl	"Sir William Babthorp"
Q99807109	Amul	"Sir Ralph Babthorp"

# Q100152977  Margaret|Joan? Billing  ->  Margaret Billing   + Joan? Billing
Q100152977	Lmul	"Margaret Billing"
Q100152977	Len	"Margaret Billing"
Q100152977	Lnl	"Margaret Billing"
Q100152977	Amul	"Joan? Billing"

# Q100153029  Alison|Alice Dauncey (Dauntsey)  ->  Alison Dauncey (Dauntsey)   + Alice Dauncey (Dauntsey)
Q100153029	Len	"Alison Dauncey (Dauntsey)"
Q100153029	Amul	"Alice Dauncey (Dauntsey)"

# Q100153041  Joan|Jane Fabian  ->  Joan Fabian   + Jane Fabian
Q100153041	Lmul	"Joan Fabian"
Q100153041	Len	"Joan Fabian"
Q100153041	Lnl	"Joan Fabian"
Q100153041	Amul	"Jane Fabian"

# Q100326000  Joan|Jane Fairfax, of Walton  ->  Joan Fairfax, of Walton   + Jane Fairfax, of Walton
Q100326000	Lmul	"Joan Fairfax, of Walton"
Q100326000	Len	"Joan Fairfax, of Walton"
Q100326000	Lnl	"Joan Fairfax, of Walton"
Q100326000	Amul	"Jane Fairfax, of Walton"

# Q100326022  Agnes|Anne Ingleby  ->  Agnes Ingleby   + Anne Ingleby
Q100326022	Lmul	"Agnes Ingleby"
Q100326022	Len	"Agnes Ingleby"
Q100326022	Lnl	"Agnes Ingleby"
Q100326022	Amul	"Anne Ingleby"

# Q100326382  Matilda|Alice Hamerton  ->  Matilda Hamerton   + Alice Hamerton
Q100326382	Lmul	"Matilda Hamerton"
Q100326382	Len	"Matilda Hamerton"
Q100326382	Lnl	"Matilda Hamerton"
Q100326382	Amul	"Alice Hamerton"

# Q100326388  Sir Richard|Thomas Radcliffe (Radclyffe), of Winmarleigh  ->  Sir Richard Radcliffe (Radclyffe), of Winmarleigh   + Sir Thomas Radcliffe (Radclyffe), of Winmarleigh
Q100326388	Lmul	"Sir Richard Radcliffe (Radclyffe), of Winmarleigh"
Q100326388	Len	"Sir Richard Radcliffe (Radclyffe), of Winmarleigh"
Q100326388	Lnl	"Sir Richard Radcliffe (Radclyffe), of Winmarleigh"
Q100326388	Amul	"Sir Thomas Radcliffe (Radclyffe), of Winmarleigh"

# Q100326468  Ellen|Eleanor|Marion Holme  ->  Ellen Holme   + Eleanor Holme | Marion Holme
Q100326468	Lmul	"Ellen Holme"
Q100326468	Len	"Ellen Holme"
Q100326468	Lnl	"Ellen Holme"
Q100326468	Amul	"Eleanor Holme"
Q100326468	Amul	"Marion Holme"

# Q100326474  Joan|Jane Orrell  ->  Joan Orrell   + Jane Orrell
Q100326474	Lmul	"Joan Orrell"
Q100326474	Len	"Joan Orrell"
Q100326474	Lnl	"Joan Orrell"
Q100326474	Amul	"Jane Orrell"

# Q100326482  Jeannette|Janet Percival, of Ripon  ->  Jeannette Percival, of Ripon   + Janet Percival, of Ripon
Q100326482	Lmul	"Jeannette Percival, of Ripon"
Q100326482	Len	"Jeannette Percival, of Ripon"
Q100326482	Lnl	"Jeannette Percival, of Ripon"
Q100326482	Amul	"Janet Percival, of Ripon"

# Q100326508  Elizabeth|Isabella Eure  ->  Elizabeth Eure   + Isabella Eure
Q100326508	Lmul	"Elizabeth Eure"
Q100326508	Len	"Elizabeth Eure"
Q100326508	Lnl	"Elizabeth Eure"
Q100326508	Amul	"Isabella Eure"

# Q100326554  Englesia|Engaret Dymoke  ->  Englesia Dymoke   + Engaret Dymoke
Q100326554	Lmul	"Englesia Dymoke"
Q100326554	Len	"Englesia Dymoke"
Q100326554	Lnl	"Englesia Dymoke"
Q100326554	Amul	"Engaret Dymoke"

# Q100389061  Elizabeth|Ellen Alcock  ->  Elizabeth Alcock   + Ellen Alcock
Q100389061	Lmul	"Elizabeth Alcock"
Q100389061	Len	"Elizabeth Alcock"
Q100389061	Lnl	"Elizabeth Alcock"
Q100389061	Amul	"Ellen Alcock"

# Q100390584  Maud|Matilda Fleming, of Slane  ->  Maud Fleming, of Slane   + Matilda Fleming, of Slane
Q100390584	Lmul	"Maud Fleming, of Slane"
Q100390584	Len	"Maud Fleming, of Slane"
Q100390584	Lnl	"Maud Fleming, of Slane"
Q100390584	Amul	"Matilda Fleming, of Slane"

# Q100439895  Sylvestre|Silventro Gondi  ->  Sylvestre Gondi   + Silventro Gondi
Q100439895	Lmul	"Sylvestre Gondi"
Q100439895	Len	"Sylvestre Gondi"
Q100439895	Lnl	"Sylvestre Gondi"
Q100439895	Amul	"Silventro Gondi"

# Q100440671  Despoina Eirene|Irina  ->  Despoina Eirene   + Despoina Irina
Q100440671	Lmul	"Despoina Eirene"
Q100440671	Len	"Despoina Eirene"
Q100440671	Lnl	"Despoina Eirene"
Q100440671	Amul	"Despoina Irina"

# Q100447015  Mercy|Marcy Freeman  ->  Mercy Freeman   + Marcy Freeman
Q100447015	Lmul	"Mercy Freeman"
Q100447015	Len	"Mercy Freeman"
Q100447015	Lnl	"Mercy Freeman"
Q100447015	Amul	"Marcy Freeman"

# Q100447118  Azariah|Hezekiah Boody  ->  Azariah Boody   + Hezekiah Boody
Q100447118	Lmul	"Azariah Boody"
Q100447118	Len	"Azariah Boody"
Q100447118	Lnl	"Azariah Boody"
Q100447118	Amul	"Hezekiah Boody"

# Q100447585  Anna|Hannah  ->  Anna   + Hannah
Q100447585	Lmul	"Anna"
Q100447585	Len	"Anna"
Q100447585	Lnl	"Anna"
Q100447585	Amul	"Hannah"

# Q100447924  Isabelle|Elizabeth  ->  Isabelle   + Elizabeth
Q100447924	Lmul	"Isabelle"
Q100447924	Len	"Isabelle"
Q100447924	Lnl	"Isabelle"
Q100447924	Amul	"Elizabeth"

# Q100727120  Margaret|Katherine  ->  Margaret   + Katherine
Q100727120	Lmul	"Margaret"
Q100727120	Len	"Margaret"
Q100727120	Lnl	"Margaret"
Q100727120	Amul	"Katherine"

# Q100727444  Sir William|Robert Bradshagh, of Blackrod et al  ->  Sir William Bradshagh, of Blackrod et al   + Sir Robert Bradshagh, of Blackrod et al
Q100727444	Lmul	"Sir William Bradshagh, of Blackrod et al"
Q100727444	Len	"Sir William Bradshagh, of Blackrod et al"
Q100727444	Lnl	"Sir William Bradshagh, of Blackrod et al"
Q100727444	Amul	"Sir Robert Bradshagh, of Blackrod et al"

# Q100727512  Maud|Mathilde de Legh, of Booths & Sandbach  ->  Maud de Legh, of Booths & Sandbach   + Mathilde de Legh, of Booths & Sandbach
Q100727512	Lmul	"Maud de Legh, of Booths & Sandbach"
Q100727512	Len	"Maud de Legh, of Booths & Sandbach"
Q100727512	Lnl	"Maud de Legh, of Booths & Sandbach"
Q100727512	Amul	"Mathilde de Legh, of Booths & Sandbach"

# Q100900274  Eleanor|Alianor Conyers, of Hornby  ->  Eleanor Conyers, of Hornby   + Alianor Conyers, of Hornby
Q100900274	Lmul	"Eleanor Conyers, of Hornby"
Q100900274	Len	"Eleanor Conyers, of Hornby"
Q100900274	Lnl	"Eleanor Conyers, of Hornby"
Q100900274	Amul	"Alianor Conyers, of Hornby"

# Q100900294  Reginald|Reynald Conyers, of Wakerley  ->  Reginald Conyers, of Wakerley   + Reynald Conyers, of Wakerley
Q100900294	Lmul	"Reginald Conyers, of Wakerley"
Q100900294	Len	"Reginald Conyers, of Wakerley"
Q100900294	Lnl	"Reginald Conyers, of Wakerley"
Q100900294	Amul	"Reynald Conyers, of Wakerley"

# Q100900295  Anne|Alice Norwich  ->  Anne Norwich   + Alice Norwich
Q100900295	Lmul	"Anne Norwich"
Q100900295	Len	"Anne Norwich"
Q100900295	Lnl	"Anne Norwich"
Q100900295	Amul	"Alice Norwich"

# Q100900507  Piers|Peter Corbet  ->  Piers Corbet   + Peter Corbet
Q100900507	Lmul	"Piers Corbet"
Q100900507	Len	"Piers Corbet"
Q100900507	Lnl	"Piers Corbet"
Q100900507	Amul	"Peter Corbet"

# Q100900719  Doda|Gouda de Cornailles  ->  Doda de Cornailles   + Gouda de Cornailles
Q100900719	Lmul	"Doda de Cornailles"
Q100900719	Len	"Doda de Cornailles"
Q100900719	Lnl	"Doda de Cornailles"
Q100900719	Amul	"Gouda de Cornailles"

# Q100900854  Alice|Alicia Harley  ->  Alice Harley   + Alicia Harley
Q100900854	Lmul	"Alice Harley"
Q100900854	Len	"Alice Harley"
Q100900854	Lnl	"Alice Harley"
Q100900854	Amul	"Alicia Harley"

# Q100901144  Sir Lawrence|Laurence de Warren, of Poynton, Ches  ->  Sir Lawrence de Warren, of Poynton, Ches   + Sir Laurence de Warren, of Poynton, Ches
Q100901144	Lmul	"Sir Lawrence de Warren, of Poynton, Ches"
Q100901144	Len	"Sir Lawrence de Warren, of Poynton, Ches"
Q100901144	Lnl	"Sir Lawrence de Warren, of Poynton, Ches"
Q100901144	Amul	"Sir Laurence de Warren, of Poynton, Ches"

# Q100901145  Margaret|Margery Bulkeley, of Cheadle  ->  Margaret Bulkeley, of Cheadle   + Margery Bulkeley, of Cheadle
Q100901145	Lmul	"Margaret Bulkeley, of Cheadle"
Q100901145	Len	"Margaret Bulkeley, of Cheadle"
Q100901145	Lnl	"Margaret Bulkeley, of Cheadle"
Q100901145	Amul	"Margery Bulkeley, of Cheadle"

# Q100901203  Sir Randall|Randle Brereton, of Malpas  ->  Sir Randall Brereton, of Malpas   + Sir Randle Brereton, of Malpas
Q100901203	Lmul	"Sir Randall Brereton, of Malpas"
Q100901203	Len	"Sir Randall Brereton, of Malpas"
Q100901203	Lnl	"Sir Randall Brereton, of Malpas"
Q100901203	Amul	"Sir Randle Brereton, of Malpas"

# Q100901215  Isabel|Elizabeth de Beeston  ->  Isabel de Beeston   + Elizabeth de Beeston
Q100901215	Lmul	"Isabel de Beeston"
Q100901215	Len	"Isabel de Beeston"
Q100901215	Lnl	"Isabel de Beeston"
Q100901215	Amul	"Elizabeth de Beeston"

# Q101163165  Jeffrey|Geoffrey Okes, of Shrubland, Suffolk  ->  Jeffrey Okes, of Shrubland, Suffolk   + Geoffrey Okes, of Shrubland, Suffolk
Q101163165	Lmul	"Jeffrey Okes, of Shrubland, Suffolk"
Q101163165	Len	"Jeffrey Okes, of Shrubland, Suffolk"
Q101163165	Lnl	"Jeffrey Okes, of Shrubland, Suffolk"
Q101163165	Amul	"Geoffrey Okes, of Shrubland, Suffolk"

# Q101163986  Alice|Ellen de Meriet  ->  Alice de Meriet   + Ellen de Meriet
Q101163986	Lmul	"Alice de Meriet"
Q101163986	Len	"Alice de Meriet"
Q101163986	Lnl	"Alice de Meriet"
Q101163986	Amul	"Ellen de Meriet"

# Q101164552  Philippe|Philippa Lovel  ->  Philippe Lovel   + Philippa Lovel
Q101164552	Lmul	"Philippe Lovel"
Q101164552	Len	"Philippe Lovel"
Q101164552	Lnl	"Philippe Lovel"
Q101164552	Amul	"Philippa Lovel"

# Q101228256  Anna|Barbara von Bystram  ->  Anna von Bystram   + Barbara von Bystram
Q101228256	Lmul	"Anna von Bystram"
Q101228256	Len	"Anna von Bystram"
Q101228256	Lnl	"Anna von Bystram"
Q101228256	Amul	"Barbara von Bystram"

# Q101231618  Mazera|Macerie Marmion  ->  Mazera Marmion   + Macerie Marmion
Q101231618	Lmul	"Mazera Marmion"
Q101231618	Len	"Mazera Marmion"
Q101231618	Lnl	"Mazera Marmion"
Q101231618	Amul	"Macerie Marmion"

# Q101231732  Sybil|Juliana Darset (Dorset)  ->  Sybil Darset (Dorset)   + Juliana Darset (Dorset)
Q101231732	Len	"Sybil Darset (Dorset)"
Q101231732	Amul	"Juliana Darset (Dorset)"

# Q101231743  Margery|Margaret Popham  ->  Margery Popham   + Margaret Popham
Q101231743	Lmul	"Margery Popham"
Q101231743	Len	"Margery Popham"
Q101231743	Lnl	"Margery Popham"
Q101231743	Amul	"Margaret Popham"

# Q101231759  Audrey|Ethelreda Hampden  ->  Audrey Hampden   + Ethelreda Hampden
Q101231759	Lmul	"Audrey Hampden"
Q101231759	Len	"Audrey Hampden"
Q101231759	Lnl	"Audrey Hampden"
Q101231759	Amul	"Ethelreda Hampden"

# Q101231791  Thomas|Richard Hexstall, of Hexstall's Court  ->  Thomas Hexstall, of Hexstall's Court   + Richard Hexstall, of Hexstall's Court
Q101231791	Lmul	"Thomas Hexstall, of Hexstall's Court"
Q101231791	Len	"Thomas Hexstall, of Hexstall's Court"
Q101231791	Lnl	"Thomas Hexstall, of Hexstall's Court"
Q101231791	Amul	"Richard Hexstall, of Hexstall's Court"

# Q101231836  Dorothy|Elizabeth Arundell  ->  Dorothy Arundell   + Elizabeth Arundell
Q101231836	Lmul	"Dorothy Arundell"
Q101231836	Len	"Dorothy Arundell"
Q101231836	Lnl	"Dorothy Arundell"
Q101231836	Amul	"Elizabeth Arundell"

# Q101247128  Måns|Magnus Hakansson  ->  Måns Hakansson   + Magnus Hakansson
Q101247128	Len	"Måns Hakansson"
Q101247128	Lnl	"Måns Hakansson"
Q101247128	Amul	"Magnus Hakansson"

# Q101247164  squire Jens|Johannes Abjörnson av Hjälmaryd  ->  squire Jens Abjörnson av Hjälmaryd   + squire Johannes Abjörnson av Hjälmaryd
Q101247164	Lmul	"squire Jens Abjörnson av Hjälmaryd"
Q101247164	Len	"squire Jens Abjörnson av Hjälmaryd"
Q101247164	Lnl	"squire Jens Abjörnson av Hjälmaryd"
Q101247164	Amul	"squire Johannes Abjörnson av Hjälmaryd"

# Q101247188  Ermegård|Armgard Fikkesdotter Bylow, heiress of Sundby & Brokind  ->  Ermegård Fikkesdotter Bylow, heiress of Sundby & Brokind   + Armgard Fikkesdotter Bylow, heiress of Sundby & Brokind
Q101247188	Len	"Ermegård Fikkesdotter Bylow, heiress of Sundby & Brokind"
Q101247188	Lnl	"Ermegård Fikkesdotter Bylow, heiress of Sundby & Brokind"
Q101247188	Amul	"Armgard Fikkesdotter Bylow, heiress of Sundby & Brokind"

# Q101247331  Karin|Katarina Magnusdotter  ->  Karin Magnusdotter   + Katarina Magnusdotter
Q101247331	Lmul	"Karin Magnusdotter"
Q101247331	Len	"Karin Magnusdotter"
Q101247331	Lnl	"Karin Magnusdotter"
Q101247331	Amul	"Katarina Magnusdotter"

# Q101247632  Karin|Catharina Magnusdotter av Tjuk  ->  Karin Magnusdotter av Tjuk   + Catharina Magnusdotter av Tjuk
Q101247632	Lmul	"Karin Magnusdotter av Tjuk"
Q101247632	Len	"Karin Magnusdotter av Tjuk"
Q101247632	Lnl	"Karin Magnusdotter av Tjuk"
Q101247632	Amul	"Catharina Magnusdotter av Tjuk"

# Q101247653  Ingerd|Ingrid Toresdotter av Stola  ->  Ingerd Toresdotter av Stola   + Ingrid Toresdotter av Stola
Q101247653	Lmul	"Ingerd Toresdotter av Stola"
Q101247653	Len	"Ingerd Toresdotter av Stola"
Q101247653	Lnl	"Ingerd Toresdotter av Stola"
Q101247653	Amul	"Ingrid Toresdotter av Stola"

# Q101247737  (squire) Antrei|Anders  ->  (squire) Antrei   + (squire) Anders
Q101247737	Lmul	"(squire) Antrei"
Q101247737	Len	"(squire) Antrei"
Q101247737	Amul	"(squire) Anders"

# Q101247780  Hamfrid|Holmfrid Jonsdotter i Stola  ->  Hamfrid Jonsdotter i Stola   + Holmfrid Jonsdotter i Stola
Q101247780	Lmul	"Hamfrid Jonsdotter i Stola"
Q101247780	Len	"Hamfrid Jonsdotter i Stola"
Q101247780	Lnl	"Hamfrid Jonsdotter i Stola"
Q101247780	Amul	"Holmfrid Jonsdotter i Stola"

# Q101247851  Johan|Jons Knutsson [Tre Rosor]  ->  Johan Knutsson [Tre Rosor]   + Jons Knutsson [Tre Rosor]
Q101247851	Lmul	"Johan Knutsson [Tre Rosor]"
Q101247851	Len	"Johan Knutsson [Tre Rosor]"
Q101247851	Lnl	"Johan Knutsson [Tre Rosor]"
Q101247851	Amul	"Jons Knutsson [Tre Rosor]"

# Q101247939  Katrine|Katharina Jonsdottir av Sudreim, heiress of Manvik & Soerum  ->  Katrine Jonsdottir av Sudreim, heiress of Manvik & Soerum   + Katharina Jonsdottir av Sudreim, heiress of Manvik & Soerum
Q101247939	Lmul	"Katrine Jonsdottir av Sudreim, heiress of Manvik & Soerum"
Q101247939	Len	"Katrine Jonsdottir av Sudreim, heiress of Manvik & Soerum"
Q101247939	Lnl	"Katrine Jonsdottir av Sudreim, heiress of Manvik & Soerum"
Q101247939	Amul	"Katharina Jonsdottir av Sudreim, heiress of Manvik & Soerum"

# Q101248441  Emil|Erengisle Kettilbjörnsson [Gren på Ål]  ->  Emil Kettilbjörnsson [Gren på Ål]   + Erengisle Kettilbjörnsson [Gren på Ål]
Q101248441	Len	"Emil Kettilbjörnsson [Gren på Ål]"
Q101248441	Lnl	"Emil Kettilbjörnsson [Gren på Ål]"
Q101248441	Amul	"Erengisle Kettilbjörnsson [Gren på Ål]"

# Q101248660  Karin|Catharina Algotsdotter de Westrogothia  ->  Karin Algotsdotter de Westrogothia   + Catharina Algotsdotter de Westrogothia
Q101248660	Lmul	"Karin Algotsdotter de Westrogothia"
Q101248660	Len	"Karin Algotsdotter de Westrogothia"
Q101248660	Lnl	"Karin Algotsdotter de Westrogothia"
Q101248660	Amul	"Catharina Algotsdotter de Westrogothia"

# Q101248672  Jon|Johan Hemmingsson [Lejonansikte]  ->  Jon Hemmingsson [Lejonansikte]   + Johan Hemmingsson [Lejonansikte]
Q101248672	Lmul	"Jon Hemmingsson [Lejonansikte]"
Q101248672	Len	"Jon Hemmingsson [Lejonansikte]"
Q101248672	Lnl	"Jon Hemmingsson [Lejonansikte]"
Q101248672	Amul	"Johan Hemmingsson [Lejonansikte]"

# Q101248686  Maunu|Magnus Olafsson [Kase], Castellan of Häme  ->  Maunu Olafsson [Kase], Castellan of Häme   + Magnus Olafsson [Kase], Castellan of Häme
Q101248686	Lmul	"Maunu Olafsson [Kase], Castellan of Häme"
Q101248686	Len	"Maunu Olafsson [Kase], Castellan of Häme"
Q101248686	Lnl	"Maunu Olafsson [Kase], Castellan of Häme"
Q101248686	Amul	"Magnus Olafsson [Kase], Castellan of Häme"

# Q101249015  Catuna|Criejna?  ->  Catuna   + Criejna?
Q101249015	Lmul	"Catuna"
Q101249015	Len	"Catuna"
Q101249015	Lnl	"Catuna"
Q101249015	Amul	"Criejna?"

# Q101249093  Agnes 'Anne|Annis' Cater  ->  Agnes 'Anne Cater   + Agnes Annis' Cater
Q101249093	Lmul	"Agnes 'Anne Cater"
Q101249093	Len	"Agnes 'Anne Cater"
Q101249093	Lnl	"Agnes 'Anne Cater"
Q101249093	Amul	"Agnes Annis' Cater"

# Q101348684  Guta|Gutchen von Rheinberg  ->  Guta von Rheinberg   + Gutchen von Rheinberg
Q101348684	Lmul	"Guta von Rheinberg"
Q101348684	Len	"Guta von Rheinberg"
Q101348684	Lnl	"Guta von Rheinberg"
Q101348684	Amul	"Gutchen von Rheinberg"

# Q101349585  Maria|Margarethe Hase von Dievelich  ->  Maria Hase von Dievelich   + Margarethe Hase von Dievelich
Q101349585	Lmul	"Maria Hase von Dievelich"
Q101349585	Len	"Maria Hase von Dievelich"
Q101349585	Lnl	"Maria Hase von Dievelich"
Q101349585	Amul	"Margarethe Hase von Dievelich"

# Q101353962  Anna|Adelheid von Saarbrücken  ->  Anna von Saarbrücken   + Adelheid von Saarbrücken
Q101353962	Lmul	"Anna von Saarbrücken"
Q101353962	Len	"Anna von Saarbrücken"
Q101353962	Lnl	"Anna von Saarbrücken"
Q101353962	Amul	"Adelheid von Saarbrücken"

# Q101354054  Elise|Elisabeth de Moncler  ->  Elise de Moncler   + Elisabeth de Moncler
Q101354054	Lmul	"Elise de Moncler"
Q101354054	Len	"Elise de Moncler"
Q101354054	Lnl	"Elise de Moncler"
Q101354054	Amul	"Elisabeth de Moncler"

# Q101354074  Jakob|Jacques de Moncler  ->  Jakob de Moncler   + Jacques de Moncler
Q101354074	Lmul	"Jakob de Moncler"
Q101354074	Len	"Jakob de Moncler"
Q101354074	Lnl	"Jakob de Moncler"
Q101354074	Amul	"Jacques de Moncler"

# Q101354234  Lisa|Liza Bayer von Boppard, Heiress of Bayon  ->  Lisa Bayer von Boppard, Heiress of Bayon   + Liza Bayer von Boppard, Heiress of Bayon
Q101354234	Len	"Lisa Bayer von Boppard, Heiress of Bayon"
Q101354234	Lnl	"Lisa Bayer von Boppard, Heiress of Bayon"
Q101354234	Amul	"Liza Bayer von Boppard, Heiress of Bayon"

# Q101402724  Isabella|Elvira de Guzmán, Señora de Gibraleon  ->  Isabella de Guzmán, Señora de Gibraleon   + Elvira de Guzmán, Señora de Gibraleon
Q101402724	Lmul	"Isabella de Guzmán, Señora de Gibraleon"
Q101402724	Len	"Isabella de Guzmán, Señora de Gibraleon"
Q101402724	Lnl	"Isabella de Guzmán, Señora de Gibraleon"
Q101402724	Amul	"Elvira de Guzmán, Señora de Gibraleon"

# Q101403711  Condesa Aldonza|Ildonca Gonzalez  ->  Condesa Aldonza Gonzalez   + Condesa Ildonca Gonzalez
Q101403711	Lmul	"Condesa Aldonza Gonzalez"
Q101403711	Len	"Condesa Aldonza Gonzalez"
Q101403711	Lnl	"Condesa Aldonza Gonzalez"
Q101403711	Amul	"Condesa Ildonca Gonzalez"

# Q101404581  Catherine|Katherine Cumberworth  ->  Catherine Cumberworth   + Katherine Cumberworth
Q101404581	Lmul	"Catherine Cumberworth"
Q101404581	Len	"Catherine Cumberworth"
Q101404581	Lnl	"Catherine Cumberworth"
Q101404581	Amul	"Katherine Cumberworth"

# Q101404588  Joan|Jane Pickering  ->  Joan Pickering   + Jane Pickering
Q101404588	Lmul	"Joan Pickering"
Q101404588	Len	"Joan Pickering"
Q101404588	Lnl	"Joan Pickering"
Q101404588	Amul	"Jane Pickering"

# Q101404601  Ellen|Alianore de Montagu  ->  Ellen de Montagu   + Alianore de Montagu
Q101404601	Lmul	"Ellen de Montagu"
Q101404601	Len	"Ellen de Montagu"
Q101404601	Lnl	"Ellen de Montagu"
Q101404601	Amul	"Alianore de Montagu"

# Q101404846  Maud|Matilda de Bokill (Bokell)  ->  Maud de Bokill (Bokell)   + Matilda de Bokill (Bokell)
Q101404846	Len	"Maud de Bokill (Bokell)"
Q101404846	Amul	"Matilda de Bokill (Bokell)"

# Q101404851  Jane|Joan Leyston  ->  Jane Leyston   + Joan Leyston
Q101404851	Lmul	"Jane Leyston"
Q101404851	Len	"Jane Leyston"
Q101404851	Lnl	"Jane Leyston"
Q101404851	Amul	"Joan Leyston"

# Q101518816  Mecella|Metze z Rožmberka  ->  Mecella z Rožmberka   + Metze z Rožmberka
Q101518816	Len	"Mecella z Rožmberka"
Q101518816	Amul	"Metze z Rožmberka"

# Q101518967  Elisabeth|Elsa von Runkel  ->  Elisabeth von Runkel   + Elsa von Runkel
Q101518967	Len	"Elisabeth von Runkel"
Q101518967	Amul	"Elsa von Runkel"

# Q101523517  Anne|Mary Apulderfield  ->  Anne Apulderfield   + Mary Apulderfield
Q101523517	Lmul	"Anne Apulderfield"
Q101523517	Len	"Anne Apulderfield"
Q101523517	Lnl	"Anne Apulderfield"
Q101523517	Amul	"Mary Apulderfield"

# Q101523537  Jane|Elizabeth Elryngton  ->  Jane Elryngton   + Elizabeth Elryngton
Q101523537	Lmul	"Jane Elryngton"
Q101523537	Len	"Jane Elryngton"
Q101523537	Lnl	"Jane Elryngton"
Q101523537	Amul	"Elizabeth Elryngton"

# Q102147120  Margaret|Marion Fleming  ->  Margaret Fleming   + Marion Fleming
Q102147120	Lmul	"Margaret Fleming"
Q102147120	Len	"Margaret Fleming"
Q102147120	Lnl	"Margaret Fleming"
Q102147120	Amul	"Marion Fleming"

# Q102151346  Maud|Matilda Quatermain (Quatremain)  ->  Maud Quatermain (Quatremain)   + Matilda Quatermain (Quatremain)
Q102151346	Lmul	"Maud Quatermain (Quatremain)"
Q102151346	Len	"Maud Quatermain (Quatremain)"
Q102151346	Amul	"Matilda Quatermain (Quatremain)"

# Q102151382  Alice|Amice Pembrugge (Pembridge)  ->  Alice Pembrugge (Pembridge)   + Amice Pembrugge (Pembridge)
Q102151382	Len	"Alice Pembrugge (Pembridge)"
Q102151382	Amul	"Amice Pembrugge (Pembridge)"

# Q102151391  John Grendon, of Gayton|Grendon  ->  John Grendon, of Gayton   + John Grendon, of Grendon
Q102151391	Lmul	"John Grendon, of Gayton"
Q102151391	Len	"John Grendon, of Gayton"
Q102151391	Amul	"John Grendon, of Grendon"

# Q102158483  Maud|Matilda Oldcastle  ->  Maud Oldcastle   + Matilda Oldcastle
Q102158483	Lmul	"Maud Oldcastle"
Q102158483	Len	"Maud Oldcastle"
Q102158483	Lnl	"Maud Oldcastle"
Q102158483	Amul	"Matilda Oldcastle"

# Q102352274  John|Roger Busard, of Ditchingham  ->  John Busard, of Ditchingham   + Roger Busard, of Ditchingham
Q102352274	Lmul	"John Busard, of Ditchingham"
Q102352274	Len	"John Busard, of Ditchingham"
Q102352274	Lnl	"John Busard, of Ditchingham"
Q102352274	Amul	"Roger Busard, of Ditchingham"

# Q102516306  Albrecht|Auberlin Volland  ->  Albrecht Volland   + Auberlin Volland
Q102516306	Lmul	"Albrecht Volland"
Q102516306	Len	"Albrecht Volland"
Q102516306	Lnl	"Albrecht Volland"
Q102516306	Amul	"Auberlin Volland"

# Q102516540  Utz|Ulrich Schwelcher von Tachenhausen, Edelknecht  ->  Utz Schwelcher von Tachenhausen, Edelknecht   + Ulrich Schwelcher von Tachenhausen, Edelknecht
Q102516540	Lmul	"Utz Schwelcher von Tachenhausen, Edelknecht"
Q102516540	Len	"Utz Schwelcher von Tachenhausen, Edelknecht"
Q102516540	Lnl	"Utz Schwelcher von Tachenhausen, Edelknecht"
Q102516540	Amul	"Ulrich Schwelcher von Tachenhausen, Edelknecht"

# Q102819638  Catherine|Louise Haye-Jousselin, dame de Fougeray  ->  Catherine Haye-Jousselin, dame de Fougeray   + Louise Haye-Jousselin, dame de Fougeray
Q102819638	Lmul	"Catherine Haye-Jousselin, dame de Fougeray"
Q102819638	Len	"Catherine Haye-Jousselin, dame de Fougeray"
Q102819638	Lnl	"Catherine Haye-Jousselin, dame de Fougeray"
Q102819638	Amul	"Louise Haye-Jousselin, dame de Fougeray"

# Q102824060  Tegaine|Tiephaine de Greguen, Heiress de Foretic  ->  Tegaine de Greguen, Heiress de Foretic   + Tiephaine de Greguen, Heiress de Foretic
Q102824060	Lmul	"Tegaine de Greguen, Heiress de Foretic"
Q102824060	Len	"Tegaine de Greguen, Heiress de Foretic"
Q102824060	Lnl	"Tegaine de Greguen, Heiress de Foretic"
Q102824060	Amul	"Tiephaine de Greguen, Heiress de Foretic"

# Q102832024  Olive|Olbric de L'Isle-Jourdain  ->  Olive de L'Isle-Jourdain   + Olbric de L'Isle-Jourdain
Q102832024	Len	"Olive de L'Isle-Jourdain"
Q102832024	Lnl	"Olive de L'Isle-Jourdain"
Q102832024	Amul	"Olbric de L'Isle-Jourdain"

# Q102836339  Grimoard|Guy Bouchard, Seigneur d'Aubeterre  ->  Grimoard Bouchard, Seigneur d'Aubeterre   + Guy Bouchard, Seigneur d'Aubeterre
Q102836339	Lmul	"Grimoard Bouchard, Seigneur d'Aubeterre"
Q102836339	Len	"Grimoard Bouchard, Seigneur d'Aubeterre"
Q102836339	Lnl	"Grimoard Bouchard, Seigneur d'Aubeterre"
Q102836339	Amul	"Guy Bouchard, Seigneur d'Aubeterre"

# Q102836376  Jeanne|Urbaine Chenin  ->  Jeanne Chenin   + Urbaine Chenin
Q102836376	Lmul	"Jeanne Chenin"
Q102836376	Len	"Jeanne Chenin"
Q102836376	Lnl	"Jeanne Chenin"
Q102836376	Amul	"Urbaine Chenin"

# Q102836588  Payen|Paen III de Maillé, Seigneur de Brézé  ->  Payen III de Maillé, Seigneur de Brézé   + Paen III de Maillé, Seigneur de Brézé
Q102836588	Len	"Payen III de Maillé, Seigneur de Brézé"
Q102836588	Lnl	"Payen III de Maillé, Seigneur de Brézé"
Q102836588	Amul	"Paen III de Maillé, Seigneur de Brézé"

# Q102837376  Pleso|Jeanne de Launay  ->  Pleso de Launay   + Jeanne de Launay
Q102837376	Lmul	"Pleso de Launay"
Q102837376	Len	"Pleso de Launay"
Q102837376	Lnl	"Pleso de Launay"
Q102837376	Amul	"Jeanne de Launay"

# Q102837454  Perrinelle|Petronelle d'Amboise, Dame de Fontenay et Rochecorban  ->  Perrinelle d'Amboise, Dame de Fontenay et Rochecorban   + Petronelle d'Amboise, Dame de Fontenay et Rochecorban
Q102837454	Len	"Perrinelle d'Amboise, Dame de Fontenay et Rochecorban"
Q102837454	Lnl	"Perrinelle d'Amboise, Dame de Fontenay et Rochecorban"
Q102837454	Amul	"Petronelle d'Amboise, Dame de Fontenay et Rochecorban"

# Q102837820  Geoffroy|Geoffrey de Mareuil  ->  Geoffroy de Mareuil   + Geoffrey de Mareuil
Q102837820	Lmul	"Geoffroy de Mareuil"
Q102837820	Len	"Geoffroy de Mareuil"
Q102837820	Lnl	"Geoffroy de Mareuil"
Q102837820	Amul	"Geoffrey de Mareuil"

# Q102838056  Anne|Agnès de Bauffremont  ->  Anne de Bauffremont   + Agnès de Bauffremont
Q102838056	Lmul	"Anne de Bauffremont"
Q102838056	Len	"Anne de Bauffremont"
Q102838056	Lnl	"Anne de Bauffremont"
Q102838056	Amul	"Agnès de Bauffremont"

# Q102838072  Edmé|Aimé de Baudoncourt, seigneur de beire  ->  Edmé de Baudoncourt, seigneur de beire   + Aimé de Baudoncourt, seigneur de beire
Q102838072	Lmul	"Edmé de Baudoncourt, seigneur de beire"
Q102838072	Len	"Edmé de Baudoncourt, seigneur de beire"
Q102838072	Lnl	"Edmé de Baudoncourt, seigneur de beire"
Q102838072	Amul	"Aimé de Baudoncourt, seigneur de beire"

# Q102857028  Murza Vaqqas|Aqaz beg, Khan of Nogai horde  ->  Murza Vaqqas beg, Khan of Nogai horde   + Murza Aqaz beg, Khan of Nogai horde
Q102857028	Lmul	"Murza Vaqqas beg, Khan of Nogai horde"
Q102857028	Len	"Murza Vaqqas beg, Khan of Nogai horde"
Q102857028	Lnl	"Murza Vaqqas beg, Khan of Nogai horde"
Q102857028	Amul	"Murza Aqaz beg, Khan of Nogai horde"

# Q102859022  Dmitry Jurijevitch| (Georgijevitch), Prince of Cholm  ->  Dmitry Jurijevitch (Georgijevitch), Prince of Cholm   + Dmitry (Georgijevitch), Prince of Cholm
Q102859022	Len	"Dmitry Jurijevitch (Georgijevitch), Prince of Cholm"
Q102859022	Lnl	"Dmitry Jurijevitch (Georgijevitch), Prince of Cholm"
Q102859022	Amul	"Dmitry (Georgijevitch), Prince of Cholm"

# Q103220335  Jane|Joan Empson  ->  Jane Empson   + Joan Empson
Q103220335	Lmul	"Jane Empson"
Q103220335	Len	"Jane Empson"
Q103220335	Lnl	"Jane Empson"
Q103220335	Amul	"Joan Empson"

# Q103220432  Sybil|Anne Fettiplace, of Stokenchurch  ->  Sybil Fettiplace, of Stokenchurch   + Anne Fettiplace, of Stokenchurch
Q103220432	Lmul	"Sybil Fettiplace, of Stokenchurch"
Q103220432	Len	"Sybil Fettiplace, of Stokenchurch"
Q103220432	Lnl	"Sybil Fettiplace, of Stokenchurch"
Q103220432	Amul	"Anne Fettiplace, of Stokenchurch"

# Q103220505  Agnes|Anne Lovingcott (Lovingott)  ->  Agnes Lovingcott (Lovingott)   + Anne Lovingcott (Lovingott)
Q103220505	Len	"Agnes Lovingcott (Lovingott)"
Q103220505	Amul	"Anne Lovingcott (Lovingott)"

# Q103774892  Winrich|Henrik von Fahrensbach  ->  Winrich von Fahrensbach   + Henrik von Fahrensbach
Q103774892	Lmul	"Winrich von Fahrensbach"
Q103774892	Len	"Winrich von Fahrensbach"
Q103774892	Lnl	"Winrich von Fahrensbach"
Q103774892	Amul	"Henrik von Fahrensbach"

# Q103782013  ridder Joachim|Jakob Hermansen Flemming, lord of Knudstrup  ->  ridder Joachim Hermansen Flemming, lord of Knudstrup   + ridder Jakob Hermansen Flemming, lord of Knudstrup
Q103782013	Lmul	"ridder Joachim Hermansen Flemming, lord of Knudstrup"
Q103782013	Len	"ridder Joachim Hermansen Flemming, lord of Knudstrup"
Q103782013	Lnl	"ridder Joachim Hermansen Flemming, lord of Knudstrup"
Q103782013	Amul	"ridder Jakob Hermansen Flemming, lord of Knudstrup"

# Q103783977  squire Niels Iversen|Ingvordsen til (Hevringholm)  ->  squire Niels Iversen til (Hevringholm)   + squire Niels Ingvordsen til (Hevringholm)
Q103783977	Len	"squire Niels Iversen til (Hevringholm)"
Q103783977	Amul	"squire Niels Ingvordsen til (Hevringholm)"

# Q103784270  Merete|Madelene Jensdatter af Hallkved  ->  Merete Jensdatter af Hallkved   + Madelene Jensdatter af Hallkved
Q103784270	Lmul	"Merete Jensdatter af Hallkved"
Q103784270	Len	"Merete Jensdatter af Hallkved"
Q103784270	Lnl	"Merete Jensdatter af Hallkved"
Q103784270	Amul	"Madelene Jensdatter af Hallkved"

# Q103945885  Lionel|Lyon Claxton  ->  Lionel Claxton   + Lyon Claxton
Q103945885	Lmul	"Lionel Claxton"
Q103945885	Len	"Lionel Claxton"
Q103945885	Lnl	"Lionel Claxton"
Q103945885	Amul	"Lyon Claxton"

# Q103947259  Joan|Jean  ->  Joan   + Jean
Q103947259	Lmul	"Joan"
Q103947259	Len	"Joan"
Q103947259	Lnl	"Joan"
Q103947259	Amul	"Jean"

# Q103947515  Margaret|Maude Lound  ->  Margaret Lound   + Maude Lound
Q103947515	Lmul	"Margaret Lound"
Q103947515	Len	"Margaret Lound"
Q103947515	Lnl	"Margaret Lound"
Q103947515	Amul	"Maude Lound"

# Q103947545  Joan|Jennet Burgh  ->  Joan Burgh   + Jennet Burgh
Q103947545	Lmul	"Joan Burgh"
Q103947545	Len	"Joan Burgh"
Q103947545	Lnl	"Joan Burgh"
Q103947545	Amul	"Jennet Burgh"

# Q104012203  Anna|Anne de Charlton (Cherlton), of Apley, Salop  ->  Anna de Charlton (Cherlton), of Apley, Salop   + Anne de Charlton (Cherlton), of Apley, Salop
Q104012203	Lmul	"Anna de Charlton (Cherlton), of Apley, Salop"
Q104012203	Len	"Anna de Charlton (Cherlton), of Apley, Salop"
Q104012203	Lnl	"Anna de Charlton (Cherlton), of Apley, Salop"
Q104012203	Amul	"Anne de Charlton (Cherlton), of Apley, Salop"

# Q104033728  Margaret|Maud Preston (?)  ->  Margaret Preston (?)   + Maud Preston (?)
Q104033728	Len	"Margaret Preston (?)"
Q104033728	Amul	"Maud Preston (?)"

# Q104037952  Catherine|Katherine Mylde (Milde)  ->  Catherine Mylde (Milde)   + Katherine Mylde (Milde)
Q104037952	Len	"Catherine Mylde (Milde)"
Q104037952	Amul	"Katherine Mylde (Milde)"

# Q104038162  Jane|Alice Croft  ->  Jane Croft   + Alice Croft
Q104038162	Lmul	"Jane Croft"
Q104038162	Len	"Jane Croft"
Q104038162	Lnl	"Jane Croft"
Q104038162	Amul	"Alice Croft"

# Q104038267  Alienore|Aline|Alianore Le Strange  ->  Alienore Le Strange   + Aline Le Strange | Alianore Le Strange
Q104038267	Lmul	"Alienore Le Strange"
Q104038267	Len	"Alienore Le Strange"
Q104038267	Lnl	"Alienore Le Strange"
Q104038267	Amul	"Aline Le Strange"
Q104038267	Amul	"Alianore Le Strange"

# Q104038274  Sir Edmund|John Blount, of Mangotsfield  ->  Sir Edmund Blount, of Mangotsfield   + Sir John Blount, of Mangotsfield
Q104038274	Lmul	"Sir Edmund Blount, of Mangotsfield"
Q104038274	Len	"Sir Edmund Blount, of Mangotsfield"
Q104038274	Lnl	"Sir Edmund Blount, of Mangotsfield"
Q104038274	Amul	"Sir John Blount, of Mangotsfield"

# Q104038325  Joan|Jane Hawte (Haute)  ->  Joan Hawte (Haute)   + Jane Hawte (Haute)
Q104038325	Len	"Joan Hawte (Haute)"
Q104038325	Amul	"Jane Hawte (Haute)"

# Q104038328  Benedicta|Bennet Shelving  ->  Benedicta Shelving   + Bennet Shelving
Q104038328	Lmul	"Benedicta Shelving"
Q104038328	Len	"Benedicta Shelving"
Q104038328	Lnl	"Benedicta Shelving"
Q104038328	Amul	"Bennet Shelving"

# Q104038621  Catrin|Catherine ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam  ->  Catrin ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam   + Catherine ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam
Q104038621	Len	"Catrin ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam"
Q104038621	Lnl	"Catrin ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam"
Q104038621	Amul	"Catherine ferch Morgan ap Llewelyn ab Ieuan of Radyr, Glam"

# Q104038758  Anne|Agnes Roper  ->  Anne Roper   + Agnes Roper
Q104038758	Lmul	"Anne Roper"
Q104038758	Len	"Anne Roper"
Q104038758	Lnl	"Anne Roper"
Q104038758	Amul	"Agnes Roper"

# Q104038768  Harry|Henry Aucher, of Lossenham, Kent  ->  Harry Aucher, of Lossenham, Kent   + Henry Aucher, of Lossenham, Kent
Q104038768	Lmul	"Harry Aucher, of Lossenham, Kent"
Q104038768	Len	"Harry Aucher, of Lossenham, Kent"
Q104038768	Lnl	"Harry Aucher, of Lossenham, Kent"
Q104038768	Amul	"Henry Aucher, of Lossenham, Kent"

# Q104038876  William|Robert Warham, of Malshanger  ->  William Warham, of Malshanger   + Robert Warham, of Malshanger
Q104038876	Lmul	"William Warham, of Malshanger"
Q104038876	Len	"William Warham, of Malshanger"
Q104038876	Lnl	"William Warham, of Malshanger"
Q104038876	Amul	"Robert Warham, of Malshanger"

# Q104038918  Sir Roger|Robert Kempe  ->  Sir Roger Kempe   + Sir Robert Kempe
Q104038918	Lmul	"Sir Roger Kempe"
Q104038918	Len	"Sir Roger Kempe"
Q104038918	Lnl	"Sir Roger Kempe"
Q104038918	Amul	"Sir Robert Kempe"

# Q104038920  Anne|Alice Scott  ->  Anne Scott   + Alice Scott
Q104038920	Lmul	"Anne Scott"
Q104038920	Len	"Anne Scott"
Q104038920	Lnl	"Anne Scott"
Q104038920	Amul	"Alice Scott"

# Q104038933  Elianor|Alice Bellers (Beler)  ->  Elianor Bellers (Beler)   + Alice Bellers (Beler)
Q104038933	Len	"Elianor Bellers (Beler)"
Q104038933	Amul	"Alice Bellers (Beler)"

# Q104074594  Magdalen|Janet Leslie, of Balquhain  ->  Magdalen Leslie, of Balquhain   + Janet Leslie, of Balquhain
Q104074594	Lmul	"Magdalen Leslie, of Balquhain"
Q104074594	Len	"Magdalen Leslie, of Balquhain"
Q104074594	Lnl	"Magdalen Leslie, of Balquhain"
Q104074594	Amul	"Janet Leslie, of Balquhain"

# Q104471578  Matilda|Maud Brereton  ->  Matilda Brereton   + Maud Brereton
Q104471578	Lmul	"Matilda Brereton"
Q104471578	Len	"Matilda Brereton"
Q104471578	Lnl	"Matilda Brereton"
Q104471578	Amul	"Maud Brereton"

# Q104471664  Mary|Elizabeth Port, of Etwall  ->  Mary Port, of Etwall   + Elizabeth Port, of Etwall
Q104471664	Lmul	"Mary Port, of Etwall"
Q104471664	Len	"Mary Port, of Etwall"
Q104471664	Lnl	"Mary Port, of Etwall"
Q104471664	Amul	"Elizabeth Port, of Etwall"

# Q104471987  Joan|Jane Bawde  ->  Joan Bawde   + Jane Bawde
Q104471987	Lmul	"Joan Bawde"
Q104471987	Len	"Joan Bawde"
Q104471987	Lnl	"Joan Bawde"
Q104471987	Amul	"Jane Bawde"

# Q104471993  Margaret|Katherine Welby  ->  Margaret Welby   + Katherine Welby
Q104471993	Lmul	"Margaret Welby"
Q104471993	Len	"Margaret Welby"
Q104471993	Lnl	"Margaret Welby"
Q104471993	Amul	"Katherine Welby"

# Q104471997  Roger|Richard de Welby, of Moulton and Welby  ->  Roger de Welby, of Moulton and Welby   + Richard de Welby, of Moulton and Welby
Q104471997	Lmul	"Roger de Welby, of Moulton and Welby"
Q104471997	Len	"Roger de Welby, of Moulton and Welby"
Q104471997	Lnl	"Roger de Welby, of Moulton and Welby"
Q104471997	Amul	"Richard de Welby, of Moulton and Welby"

# Q104472021  Maud|Margery Mablethorpe  ->  Maud Mablethorpe   + Margery Mablethorpe
Q104472021	Lmul	"Maud Mablethorpe"
Q104472021	Len	"Maud Mablethorpe"
Q104472021	Lnl	"Maud Mablethorpe"
Q104472021	Amul	"Margery Mablethorpe"

# Q104472091  Eleanor|Ellen Limbury  ->  Eleanor Limbury   + Ellen Limbury
Q104472091	Lmul	"Eleanor Limbury"
Q104472091	Len	"Eleanor Limbury"
Q104472091	Lnl	"Eleanor Limbury"
Q104472091	Amul	"Ellen Limbury"

# Q104472165  Emma|Emeline  ->  Emma   + Emeline
Q104472165	Lmul	"Emma"
Q104472165	Len	"Emma"
Q104472165	Lnl	"Emma"
Q104472165	Amul	"Emeline"

# Q104472175  Katherine|Catherine le Brett  ->  Katherine le Brett   + Catherine le Brett
Q104472175	Lmul	"Katherine le Brett"
Q104472175	Len	"Katherine le Brett"
Q104472175	Lnl	"Katherine le Brett"
Q104472175	Amul	"Catherine le Brett"

# Q104472345  Agnes|Joan Aston  ->  Agnes Aston   + Joan Aston
Q104472345	Lmul	"Agnes Aston"
Q104472345	Len	"Agnes Aston"
Q104472345	Lnl	"Agnes Aston"
Q104472345	Amul	"Joan Aston"

# Q104472594  Anne|Agnes Knyvett  ->  Anne Knyvett   + Agnes Knyvett
Q104472594	Lmul	"Anne Knyvett"
Q104472594	Len	"Anne Knyvett"
Q104472594	Lnl	"Anne Knyvett"
Q104472594	Amul	"Agnes Knyvett"

# Q104472984  Helen|Ellen Longford  ->  Helen Longford   + Ellen Longford
Q104472984	Lmul	"Helen Longford"
Q104472984	Len	"Helen Longford"
Q104472984	Lnl	"Helen Longford"
Q104472984	Amul	"Ellen Longford"

# Q104473002  Alice|Margaret Deincourt  ->  Alice Deincourt   + Margaret Deincourt
Q104473002	Lmul	"Alice Deincourt"
Q104473002	Len	"Alice Deincourt"
Q104473002	Lnl	"Alice Deincourt"
Q104473002	Amul	"Margaret Deincourt"

# Q104473012  Margery|Margaret Sulney  ->  Margery Sulney   + Margaret Sulney
Q104473012	Lmul	"Margery Sulney"
Q104473012	Len	"Margery Sulney"
Q104473012	Lnl	"Margery Sulney"
Q104473012	Amul	"Margaret Sulney"

# Q104473135  William|John|Roger Dethick, of Newhall, Derbs  ->  William Dethick, of Newhall, Derbs   + John Dethick, of Newhall, Derbs | Roger Dethick, of Newhall, Derbs
Q104473135	Lmul	"William Dethick, of Newhall, Derbs"
Q104473135	Len	"William Dethick, of Newhall, Derbs"
Q104473135	Lnl	"William Dethick, of Newhall, Derbs"
Q104473135	Amul	"John Dethick, of Newhall, Derbs"
Q104473135	Amul	"Roger Dethick, of Newhall, Derbs"

# Q104473158  William Kynardsley, of Loxton|Loxley  ->  William Kynardsley, of Loxton   + William Kynardsley, of Loxley
Q104473158	Lmul	"William Kynardsley, of Loxton"
Q104473158	Len	"William Kynardsley, of Loxton"
Q104473158	Lnl	"William Kynardsley, of Loxton"
Q104473158	Amul	"William Kynardsley, of Loxley"

# Q104473541  Agnes|Anne Stanhope  ->  Agnes Stanhope   + Anne Stanhope
Q104473541	Lmul	"Agnes Stanhope"
Q104473541	Len	"Agnes Stanhope"
Q104473541	Lnl	"Agnes Stanhope"
Q104473541	Amul	"Anne Stanhope"

# Q104473559  Maud|Matilda  ->  Maud   + Matilda
Q104473559	Lmul	"Maud"
Q104473559	Len	"Maud"
Q104473559	Lnl	"Maud"
Q104473559	Amul	"Matilda"

# Q104473578  Elizabeth|Beatrice Lewknor  ->  Elizabeth Lewknor   + Beatrice Lewknor
Q104473578	Lmul	"Elizabeth Lewknor"
Q104473578	Len	"Elizabeth Lewknor"
Q104473578	Lnl	"Elizabeth Lewknor"
Q104473578	Amul	"Beatrice Lewknor"

# Q104473674  Sir Roger|Robert Leche, of Chatsworth  ->  Sir Roger Leche, of Chatsworth   + Sir Robert Leche, of Chatsworth
Q104473674	Lmul	"Sir Roger Leche, of Chatsworth"
Q104473674	Len	"Sir Roger Leche, of Chatsworth"
Q104473674	Lnl	"Sir Roger Leche, of Chatsworth"
Q104473674	Amul	"Sir Robert Leche, of Chatsworth"

# Q104484426  Joan|Julian Hovel  ->  Joan Hovel   + Julian Hovel
Q104484426	Lmul	"Joan Hovel"
Q104484426	Len	"Joan Hovel"
Q104484426	Lnl	"Joan Hovel"
Q104484426	Amul	"Julian Hovel"

# Q104503644  Marion|Margery Mitford  ->  Marion Mitford   + Margery Mitford
Q104503644	Lmul	"Marion Mitford"
Q104503644	Len	"Marion Mitford"
Q104503644	Lnl	"Marion Mitford"
Q104503644	Amul	"Margery Mitford"

# Q104550087  Kerstin|Karin  ->  Kerstin   + Karin
Q104550087	Len	"Kerstin"
Q104550087	Lnl	"Kerstin"
Q104550087	Amul	"Karin"

# Q104550851  Elisabeth|Else von Maydell, Heiress of Joesse  ->  Elisabeth von Maydell, Heiress of Joesse   + Else von Maydell, Heiress of Joesse
Q104550851	Lmul	"Elisabeth von Maydell, Heiress of Joesse"
Q104550851	Len	"Elisabeth von Maydell, Heiress of Joesse"
Q104550851	Lnl	"Elisabeth von Maydell, Heiress of Joesse"
Q104550851	Amul	"Else von Maydell, Heiress of Joesse"

# Q104603612  Simon|Stephen de Peplesham  ->  Simon de Peplesham   + Stephen de Peplesham
Q104603612	Lmul	"Simon de Peplesham"
Q104603612	Len	"Simon de Peplesham"
Q104603612	Lnl	"Simon de Peplesham"
Q104603612	Amul	"Stephen de Peplesham"

# Q104773019  Freiin Anna|Johanna von Wolharticz  ->  Freiin Anna von Wolharticz   + Freiin Johanna von Wolharticz
Q104773019	Len	"Freiin Anna von Wolharticz"
Q104773019	Lnl	"Freiin Anna von Wolharticz"
Q104773019	Amul	"Freiin Johanna von Wolharticz"

# Q104773029  Wenzel|Wentsch von Dohna zu Radmeritz, herr von Grafenstein  ->  Wenzel von Dohna zu Radmeritz, herr von Grafenstein   + Wentsch von Dohna zu Radmeritz, herr von Grafenstein
Q104773029	Len	"Wenzel von Dohna zu Radmeritz, herr von Grafenstein"
Q104773029	Lnl	"Wenzel von Dohna zu Radmeritz, herr von Grafenstein"
Q104773029	Amul	"Wentsch von Dohna zu Radmeritz, herr von Grafenstein"

# Q104773030  Wenzel|Wentsch IV von Dohna zu Herwigsdorf und Wittgendorf  ->  Wenzel IV von Dohna zu Herwigsdorf und Wittgendorf   + Wentsch IV von Dohna zu Herwigsdorf und Wittgendorf
Q104773030	Len	"Wenzel IV von Dohna zu Herwigsdorf und Wittgendorf"
Q104773030	Lnl	"Wenzel IV von Dohna zu Herwigsdorf und Wittgendorf"
Q104773030	Amul	"Wentsch IV von Dohna zu Herwigsdorf und Wittgendorf"

# Q104785128  Roger|John|Thomas Heritage, of Burton Dasset  ->  Roger Heritage, of Burton Dasset   + John Heritage, of Burton Dasset | Thomas Heritage, of Burton Dasset
Q104785128	Lmul	"Roger Heritage, of Burton Dasset"
Q104785128	Len	"Roger Heritage, of Burton Dasset"
Q104785128	Lnl	"Roger Heritage, of Burton Dasset"
Q104785128	Amul	"John Heritage, of Burton Dasset"
Q104785128	Amul	"Thomas Heritage, of Burton Dasset"

# Q104799486  Joan|Jane Threlkeld (Thirkeld)  ->  Joan Threlkeld (Thirkeld)   + Jane Threlkeld (Thirkeld)
Q104799486	Len	"Joan Threlkeld (Thirkeld)"
Q104799486	Amul	"Jane Threlkeld (Thirkeld)"

# Q105554455  Esther Griner|Crider  ->  Esther Griner   + Esther Crider
Q105554455	Lmul	"Esther Griner"
Q105554455	Len	"Esther Griner"
Q105554455	Lnl	"Esther Griner"
Q105554455	Amul	"Esther Crider"

# Q105767160  Eden|Idonea Hunt  ->  Eden Hunt   + Idonea Hunt
Q105767160	Lmul	"Eden Hunt"
Q105767160	Len	"Eden Hunt"
Q105767160	Lnl	"Eden Hunt"
Q105767160	Amul	"Idonea Hunt"

# Q105768306  Jane|Elizabeth|Joan Beaumont  ->  Jane Beaumont   + Elizabeth Beaumont | Joan Beaumont
Q105768306	Lmul	"Jane Beaumont"
Q105768306	Len	"Jane Beaumont"
Q105768306	Lnl	"Jane Beaumont"
Q105768306	Amul	"Elizabeth Beaumont"
Q105768306	Amul	"Joan Beaumont"

# Q105768384  Agnes|Alice de Grey  ->  Agnes de Grey   + Alice de Grey
Q105768384	Lmul	"Agnes de Grey"
Q105768384	Len	"Agnes de Grey"
Q105768384	Lnl	"Agnes de Grey"
Q105768384	Amul	"Alice de Grey"

# Q105768731  Hawise|Helwise de Lancaster, Baroness Kendal  ->  Hawise de Lancaster, Baroness Kendal   + Helwise de Lancaster, Baroness Kendal
Q105768731	Lmul	"Hawise de Lancaster, Baroness Kendal"
Q105768731	Len	"Hawise de Lancaster, Baroness Kendal"
Q105768731	Lnl	"Hawise de Lancaster, Baroness Kendal"
Q105768731	Amul	"Helwise de Lancaster, Baroness Kendal"

# Q105768735  Hawise|Helwise de Stuteville  ->  Hawise de Stuteville   + Helwise de Stuteville
Q105768735	Len	"Hawise de Stuteville"
Q105768735	Lnl	"Hawise de Stuteville"
Q105768735	Amul	"Helwise de Stuteville"

# Q105770364  Joan|Jane Cheney (or Cheyne)  ->  Joan Cheney (or Cheyne)   + Jane Cheney (or Cheyne)
Q105770364	Len	"Joan Cheney (or Cheyne)"
Q105770364	Amul	"Jane Cheney (or Cheyne)"

# Q105770454  Joan|Margaret Cloford (Clawford)  ->  Joan Cloford (Clawford)   + Margaret Cloford (Clawford)
Q105770454	Len	"Joan Cloford (Clawford)"
Q105770454	Amul	"Margaret Cloford (Clawford)"

# Q105770456  John|Richard Floyer  ->  John Floyer   + Richard Floyer
Q105770456	Lmul	"John Floyer"
Q105770456	Len	"John Floyer"
Q105770456	Lnl	"John Floyer"
Q105770456	Amul	"Richard Floyer"

# Q105770518  Ellen|Ele Mallett (Malet)  ->  Ellen Mallett (Malet)   + Ele Mallett (Malet)
Q105770518	Len	"Ellen Mallett (Malet)"
Q105770518	Amul	"Ele Mallett (Malet)"

# Q105770525  Joane|Joan de la More (Delamere)  ->  Joane de la More (Delamere)   + Joan de la More (Delamere)
Q105770525	Len	"Joane de la More (Delamere)"
Q105770525	Amul	"Joan de la More (Delamere)"

# Q105771252  Anne|Agnes Plumpton (or Plompton)  ->  Anne Plumpton (or Plompton)   + Agnes Plumpton (or Plompton)
Q105771252	Len	"Anne Plumpton (or Plompton)"
Q105771252	Amul	"Agnes Plumpton (or Plompton)"

# Q105771289  Grisell|Julian Rivett, of Rowsden  ->  Grisell Rivett, of Rowsden   + Julian Rivett, of Rowsden
Q105771289	Lmul	"Grisell Rivett, of Rowsden"
Q105771289	Len	"Grisell Rivett, of Rowsden"
Q105771289	Lnl	"Grisell Rivett, of Rowsden"
Q105771289	Amul	"Julian Rivett, of Rowsden"

# Q105776871  Rose|Roesia Lucy, of Charlecote  ->  Rose Lucy, of Charlecote   + Roesia Lucy, of Charlecote
Q105776871	Lmul	"Rose Lucy, of Charlecote"
Q105776871	Len	"Rose Lucy, of Charlecote"
Q105776871	Lnl	"Rose Lucy, of Charlecote"
Q105776871	Amul	"Roesia Lucy, of Charlecote"

# Q105776889  Margery|Margaret Throckmorton  ->  Margery Throckmorton   + Margaret Throckmorton
Q105776889	Lmul	"Margery Throckmorton"
Q105776889	Len	"Margery Throckmorton"
Q105776889	Lnl	"Margery Throckmorton"
Q105776889	Amul	"Margaret Throckmorton"

# Q105787972  Avery|Alured Rawson  ->  Avery Rawson   + Alured Rawson
Q105787972	Lmul	"Avery Rawson"
Q105787972	Len	"Avery Rawson"
Q105787972	Lnl	"Avery Rawson"
Q105787972	Amul	"Alured Rawson"

# Q105788077  Agnes|Anne Daundy  ->  Agnes Daundy   + Anne Daundy
Q105788077	Lmul	"Agnes Daundy"
Q105788077	Len	"Agnes Daundy"
Q105788077	Lnl	"Agnes Daundy"
Q105788077	Amul	"Anne Daundy"

# Q105791239  Margaret|Mary Green (Greene)  ->  Margaret Green (Greene)   + Mary Green (Greene)
Q105791239	Len	"Margaret Green (Greene)"
Q105791239	Amul	"Mary Green (Greene)"

# Q105793143  Agnes|Jane Darell, of Cale Hill, Kent  ->  Agnes Darell, of Cale Hill, Kent   + Jane Darell, of Cale Hill, Kent
Q105793143	Lmul	"Agnes Darell, of Cale Hill, Kent"
Q105793143	Len	"Agnes Darell, of Cale Hill, Kent"
Q105793143	Lnl	"Agnes Darell, of Cale Hill, Kent"
Q105793143	Amul	"Jane Darell, of Cale Hill, Kent"

# Q105793176  Stephen|Henry Spilman (Spelman), of Spelman's Place  ->  Stephen Spilman (Spelman), of Spelman's Place   + Henry Spilman (Spelman), of Spelman's Place
Q105793176	Lmul	"Stephen Spilman (Spelman), of Spelman's Place"
Q105793176	Len	"Stephen Spilman (Spelman), of Spelman's Place"
Q105793176	Lnl	"Stephen Spilman (Spelman), of Spelman's Place"
Q105793176	Amul	"Henry Spilman (Spelman), of Spelman's Place"

# Q105793189  Adam|Hamond Narborough (Narborow)  ->  Adam Narborough (Narborow)   + Hamond Narborough (Narborow)
Q105793189	Len	"Adam Narborough (Narborow)"
Q105793189	Amul	"Hamond Narborough (Narborow)"

# Q105794039  Anne|Mary Twyneho (Twinyho)  ->  Anne Twyneho (Twinyho)   + Mary Twyneho (Twinyho)
Q105794039	Len	"Anne Twyneho (Twinyho)"
Q105794039	Amul	"Mary Twyneho (Twinyho)"

# Q105794198  Elizabeth|Alice Watno  ->  Elizabeth Watno   + Alice Watno
Q105794198	Lmul	"Elizabeth Watno"
Q105794198	Len	"Elizabeth Watno"
Q105794198	Lnl	"Elizabeth Watno"
Q105794198	Amul	"Alice Watno"

# Q105794202  Joanna|Joan Fineux (Fyneux)  ->  Joanna Fineux (Fyneux)   + Joan Fineux (Fyneux)
Q105794202	Len	"Joanna Fineux (Fyneux)"
Q105794202	Amul	"Joan Fineux (Fyneux)"

# Q105794803  Alice|Anne Belknap  ->  Alice Belknap   + Anne Belknap
Q105794803	Lmul	"Alice Belknap"
Q105794803	Len	"Alice Belknap"
Q105794803	Lnl	"Alice Belknap"
Q105794803	Amul	"Anne Belknap"

# Q105794928  Alice|Eleanor de Coggeshall  ->  Alice de Coggeshall   + Eleanor de Coggeshall
Q105794928	Lmul	"Alice de Coggeshall"
Q105794928	Len	"Alice de Coggeshall"
Q105794928	Lnl	"Alice de Coggeshall"
Q105794928	Amul	"Eleanor de Coggeshall"

# Q105796701  Mariot|Marion Dunbar, of Mochrum  ->  Mariot Dunbar, of Mochrum   + Marion Dunbar, of Mochrum
Q105796701	Lmul	"Mariot Dunbar, of Mochrum"
Q105796701	Len	"Mariot Dunbar, of Mochrum"
Q105796701	Lnl	"Mariot Dunbar, of Mochrum"
Q105796701	Amul	"Marion Dunbar, of Mochrum"

# Q105797673  Cynwrig|Kendrik Eyton, of Eyton  ->  Cynwrig Eyton, of Eyton   + Kendrik Eyton, of Eyton
Q105797673	Lmul	"Cynwrig Eyton, of Eyton"
Q105797673	Len	"Cynwrig Eyton, of Eyton"
Q105797673	Lnl	"Cynwrig Eyton, of Eyton"
Q105797673	Amul	"Kendrik Eyton, of Eyton"

# Q105797749  Gwenhwyfar|Gwenllian ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin  ->  Gwenhwyfar ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin   + Gwenllian ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin
Q105797749	Lmul	"Gwenhwyfar ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin"
Q105797749	Len	"Gwenhwyfar ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin"
Q105797749	Lnl	"Gwenhwyfar ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin"
Q105797749	Amul	"Gwenllian ferch Richard ap Rhys ap Morus Gethin ab Ieuan Gethin ap Magod Cyffin"

# Q105798946  Jane|Maud Petit, of Ardevera  ->  Jane Petit, of Ardevera   + Maud Petit, of Ardevera
Q105798946	Lmul	"Jane Petit, of Ardevera"
Q105798946	Len	"Jane Petit, of Ardevera"
Q105798946	Lnl	"Jane Petit, of Ardevera"
Q105798946	Amul	"Maud Petit, of Ardevera"

# Q105800017  James|John Hay, Provost of Dundee  ->  James Hay, Provost of Dundee   + John Hay, Provost of Dundee
Q105800017	Lmul	"James Hay, Provost of Dundee"
Q105800017	Len	"James Hay, Provost of Dundee"
Q105800017	Lnl	"James Hay, Provost of Dundee"
Q105800017	Amul	"John Hay, Provost of Dundee"

# Q105800402  Mary|May Wadham  ->  Mary Wadham   + May Wadham
Q105800402	Lmul	"Mary Wadham"
Q105800402	Len	"Mary Wadham"
Q105800402	Lnl	"Mary Wadham"
Q105800402	Amul	"May Wadham"

# Q105800447  Joan|Jane Fowell  ->  Joan Fowell   + Jane Fowell
Q105800447	Lmul	"Joan Fowell"
Q105800447	Len	"Joan Fowell"
Q105800447	Lnl	"Joan Fowell"
Q105800447	Amul	"Jane Fowell"

# Q105800518  Anne|Agnes Chichester  ->  Anne Chichester   + Agnes Chichester
Q105800518	Lmul	"Anne Chichester"
Q105800518	Len	"Anne Chichester"
Q105800518	Lnl	"Anne Chichester"
Q105800518	Amul	"Agnes Chichester"

# Q105800720  Agnes|Anne Baker  ->  Agnes Baker   + Anne Baker
Q105800720	Lmul	"Agnes Baker"
Q105800720	Len	"Agnes Baker"
Q105800720	Lnl	"Agnes Baker"
Q105800720	Amul	"Anne Baker"

# Q105801167  Margery|Margaret Wentworth  ->  Margery Wentworth   + Margaret Wentworth
Q105801167	Lmul	"Margery Wentworth"
Q105801167	Len	"Margery Wentworth"
Q105801167	Lnl	"Margery Wentworth"
Q105801167	Amul	"Margaret Wentworth"

# Q105801192  Rose|Anne Bennett, of Rushall, Norfolk  ->  Rose Bennett, of Rushall, Norfolk   + Anne Bennett, of Rushall, Norfolk
Q105801192	Lmul	"Rose Bennett, of Rushall, Norfolk"
Q105801192	Len	"Rose Bennett, of Rushall, Norfolk"
Q105801192	Lnl	"Rose Bennett, of Rushall, Norfolk"
Q105801192	Amul	"Anne Bennett, of Rushall, Norfolk"

# Q105801251  Elizabeth|Eva Clipsby  ->  Elizabeth Clipsby   + Eva Clipsby
Q105801251	Lmul	"Elizabeth Clipsby"
Q105801251	Len	"Elizabeth Clipsby"
Q105801251	Lnl	"Elizabeth Clipsby"
Q105801251	Amul	"Eva Clipsby"

# Q105801340  Egidius|Giles Arden, of Drayton  ->  Egidius Arden, of Drayton   + Giles Arden, of Drayton
Q105801340	Lmul	"Egidius Arden, of Drayton"
Q105801340	Len	"Egidius Arden, of Drayton"
Q105801340	Lnl	"Egidius Arden, of Drayton"
Q105801340	Amul	"Giles Arden, of Drayton"

# Q105801355  Katherine|Margred Gwrgan (Wogan)  ->  Katherine Gwrgan (Wogan)   + Margred Gwrgan (Wogan)
Q105801355	Len	"Katherine Gwrgan (Wogan)"
Q105801355	Amul	"Margred Gwrgan (Wogan)"

# Q105802202  Elizabeth|Anne Beaumont, of Lascelles Hall  ->  Elizabeth Beaumont, of Lascelles Hall   + Anne Beaumont, of Lascelles Hall
Q105802202	Lmul	"Elizabeth Beaumont, of Lascelles Hall"
Q105802202	Len	"Elizabeth Beaumont, of Lascelles Hall"
Q105802202	Lnl	"Elizabeth Beaumont, of Lascelles Hall"
Q105802202	Amul	"Anne Beaumont, of Lascelles Hall"

# Q105802203  John|William|Edmund Beaumont, of Lascelles Hall  ->  John Beaumont, of Lascelles Hall   + William Beaumont, of Lascelles Hall | Edmund Beaumont, of Lascelles Hall
Q105802203	Lmul	"John Beaumont, of Lascelles Hall"
Q105802203	Len	"John Beaumont, of Lascelles Hall"
Q105802203	Lnl	"John Beaumont, of Lascelles Hall"
Q105802203	Amul	"William Beaumont, of Lascelles Hall"
Q105802203	Amul	"Edmund Beaumont, of Lascelles Hall"

# Q105802982  William|Robert Brouncker, of Melksham  ->  William Brouncker, of Melksham   + Robert Brouncker, of Melksham
Q105802982	Lmul	"William Brouncker, of Melksham"
Q105802982	Len	"William Brouncker, of Melksham"
Q105802982	Lnl	"William Brouncker, of Melksham"
Q105802982	Amul	"Robert Brouncker, of Melksham"

# Q105805053  Katherine|Catherine Mobberley  ->  Katherine Mobberley   + Catherine Mobberley
Q105805053	Lmul	"Katherine Mobberley"
Q105805053	Len	"Katherine Mobberley"
Q105805053	Lnl	"Katherine Mobberley"
Q105805053	Amul	"Catherine Mobberley"

# Q105805091  Janet|Jonet Bradshaw  ->  Janet Bradshaw   + Jonet Bradshaw
Q105805091	Lmul	"Janet Bradshaw"
Q105805091	Len	"Janet Bradshaw"
Q105805091	Lnl	"Janet Bradshaw"
Q105805091	Amul	"Jonet Bradshaw"

# Q105805263  Agnes|Alice Farby (or Foreby)  ->  Agnes Farby (or Foreby)   + Alice Farby (or Foreby)
Q105805263	Len	"Agnes Farby (or Foreby)"
Q105805263	Amul	"Alice Farby (or Foreby)"

# Q105806069  Isabella|Sabrina Jaquett  ->  Isabella Jaquett   + Sabrina Jaquett
Q105806069	Lmul	"Isabella Jaquett"
Q105806069	Len	"Isabella Jaquett"
Q105806069	Lnl	"Isabella Jaquett"
Q105806069	Amul	"Sabrina Jaquett"

# Q105814419  Sionet|Jonet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan  ->  Sionet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan   + Jonet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan
Q105814419	Lmul	"Sionet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan"
Q105814419	Len	"Sionet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan"
Q105814419	Lnl	"Sionet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan"
Q105814419	Amul	"Jonet ferch Dafydd ab Ieuan ap Hywel ap Cynwrig Iorwerth Fychan"

# Q105814464  Elizabeth|Isabel Barley  ->  Elizabeth Barley   + Isabel Barley
Q105814464	Lmul	"Elizabeth Barley"
Q105814464	Len	"Elizabeth Barley"
Q105814464	Lnl	"Elizabeth Barley"
Q105814464	Amul	"Isabel Barley"

# Q105815062  Gerard|Gerald de Furnival  ->  Gerard de Furnival   + Gerald de Furnival
Q105815062	Lmul	"Gerard de Furnival"
Q105815062	Len	"Gerard de Furnival"
Q105815062	Lnl	"Gerard de Furnival"
Q105815062	Amul	"Gerald de Furnival"

# Q105815098  Cicely|Cecily Pelham, of Laughton  ->  Cicely Pelham, of Laughton   + Cecily Pelham, of Laughton
Q105815098	Lmul	"Cicely Pelham, of Laughton"
Q105815098	Len	"Cicely Pelham, of Laughton"
Q105815098	Lnl	"Cicely Pelham, of Laughton"
Q105815098	Amul	"Cecily Pelham, of Laughton"

# Q105815184  Frideswide|Frisewide Norton  ->  Frideswide Norton   + Frisewide Norton
Q105815184	Lmul	"Frideswide Norton"
Q105815184	Len	"Frideswide Norton"
Q105815184	Lnl	"Frideswide Norton"
Q105815184	Amul	"Frisewide Norton"

# Q105815186  Joan|Jane Northwood (Norwood)  ->  Joan Northwood (Norwood)   + Jane Northwood (Norwood)
Q105815186	Len	"Joan Northwood (Norwood)"
Q105815186	Amul	"Jane Northwood (Norwood)"

# Q105815260  Agnes|Anne Pigott  ->  Agnes Pigott   + Anne Pigott
Q105815260	Lmul	"Agnes Pigott"
Q105815260	Len	"Agnes Pigott"
Q105815260	Lnl	"Agnes Pigott"
Q105815260	Amul	"Anne Pigott"

# Q105815264  William|John Sewarby (Sywardby), of Yorks  ->  William Sewarby (Sywardby), of Yorks   + John Sewarby (Sywardby), of Yorks
Q105815264	Lmul	"William Sewarby (Sywardby), of Yorks"
Q105815264	Len	"William Sewarby (Sywardby), of Yorks"
Q105815264	Lnl	"William Sewarby (Sywardby), of Yorks"
Q105815264	Amul	"John Sewarby (Sywardby), of Yorks"

# Q105815314  Emota|Emma Middleton  ->  Emota Middleton   + Emma Middleton
Q105815314	Lmul	"Emota Middleton"
Q105815314	Len	"Emota Middleton"
Q105815314	Lnl	"Emota Middleton"
Q105815314	Amul	"Emma Middleton"

# Q105815471  Hew Wallace, of Carnell|Cairnhill  ->  Hew Wallace, of Carnell   + Hew Wallace, of Cairnhill
Q105815471	Lmul	"Hew Wallace, of Carnell"
Q105815471	Len	"Hew Wallace, of Carnell"
Q105815471	Lnl	"Hew Wallace, of Carnell"
Q105815471	Amul	"Hew Wallace, of Cairnhill"

# Q105816711  Hugh|Hugo Hull (Hill), of Hill, Salop  ->  Hugh Hull (Hill), of Hill, Salop   + Hugo Hull (Hill), of Hill, Salop
Q105816711	Len	"Hugh Hull (Hill), of Hill, Salop"
Q105816711	Lnl	"Hugh Hull (Hill), of Hill, Salop"
Q105816711	Amul	"Hugo Hull (Hill), of Hill, Salop"

# Q105816720  Alice|Katherine de Malpas  ->  Alice de Malpas   + Katherine de Malpas
Q105816720	Lmul	"Alice de Malpas"
Q105816720	Len	"Alice de Malpas"
Q105816720	Lnl	"Alice de Malpas"
Q105816720	Amul	"Katherine de Malpas"

# Q105816734  Jenkin|John Hollis (Hooks), of Flint  ->  Jenkin Hollis (Hooks), of Flint   + John Hollis (Hooks), of Flint
Q105816734	Lmul	"Jenkin Hollis (Hooks), of Flint"
Q105816734	Len	"Jenkin Hollis (Hooks), of Flint"
Q105816734	Lnl	"Jenkin Hollis (Hooks), of Flint"
Q105816734	Amul	"John Hollis (Hooks), of Flint"

# Q105816746  Elizabeth|Perceval Harington, of Westby  ->  Elizabeth Harington, of Westby   + Perceval Harington, of Westby
Q105816746	Lmul	"Elizabeth Harington, of Westby"
Q105816746	Len	"Elizabeth Harington, of Westby"
Q105816746	Lnl	"Elizabeth Harington, of Westby"
Q105816746	Amul	"Perceval Harington, of Westby"

# Q105816787  Avice|Alice Wallop, of Nether Wallop, Hants  ->  Avice Wallop, of Nether Wallop, Hants   + Alice Wallop, of Nether Wallop, Hants
Q105816787	Lmul	"Avice Wallop, of Nether Wallop, Hants"
Q105816787	Len	"Avice Wallop, of Nether Wallop, Hants"
Q105816787	Lnl	"Avice Wallop, of Nether Wallop, Hants"
Q105816787	Amul	"Alice Wallop, of Nether Wallop, Hants"

# Q105816792  Margery|Margaret Danvers  ->  Margery Danvers   + Margaret Danvers
Q105816792	Lmul	"Margery Danvers"
Q105816792	Len	"Margery Danvers"
Q105816792	Lnl	"Margery Danvers"
Q105816792	Amul	"Margaret Danvers"

# Q105817851  Anne|Alice Hyde, of South Denchworth  ->  Anne Hyde, of South Denchworth   + Alice Hyde, of South Denchworth
Q105817851	Lmul	"Anne Hyde, of South Denchworth"
Q105817851	Len	"Anne Hyde, of South Denchworth"
Q105817851	Lnl	"Anne Hyde, of South Denchworth"
Q105817851	Amul	"Alice Hyde, of South Denchworth"

# Q105817860  Jane|Joan Wandesford  ->  Jane Wandesford   + Joan Wandesford
Q105817860	Lmul	"Jane Wandesford"
Q105817860	Len	"Jane Wandesford"
Q105817860	Lnl	"Jane Wandesford"
Q105817860	Amul	"Joan Wandesford"

# Q105817881  Alice|Agnes Lidiard (Ledyard)  ->  Alice Lidiard (Ledyard)   + Agnes Lidiard (Ledyard)
Q105817881	Len	"Alice Lidiard (Ledyard)"
Q105817881	Amul	"Agnes Lidiard (Ledyard)"

# Q105817888  William|Walter Wallis, of Cowden  ->  William Wallis, of Cowden   + Walter Wallis, of Cowden
Q105817888	Lmul	"William Wallis, of Cowden"
Q105817888	Len	"William Wallis, of Cowden"
Q105817888	Lnl	"William Wallis, of Cowden"
Q105817888	Amul	"Walter Wallis, of Cowden"

# Q105819189  Elizabeth|Frances Malone, of Litter  ->  Elizabeth Malone, of Litter   + Frances Malone, of Litter
Q105819189	Lmul	"Elizabeth Malone, of Litter"
Q105819189	Len	"Elizabeth Malone, of Litter"
Q105819189	Lnl	"Elizabeth Malone, of Litter"
Q105819189	Amul	"Frances Malone, of Litter"

# Q105819302  Lucy|Lucia Warren  ->  Lucy Warren   + Lucia Warren
Q105819302	Lmul	"Lucy Warren"
Q105819302	Len	"Lucy Warren"
Q105819302	Lnl	"Lucy Warren"
Q105819302	Amul	"Lucia Warren"

# Q105819473  Sir Richard|John Rugge, of Rugge, Salop  ->  Sir Richard Rugge, of Rugge, Salop   + Sir John Rugge, of Rugge, Salop
Q105819473	Len	"Sir Richard Rugge, of Rugge, Salop"
Q105819473	Lnl	"Sir Richard Rugge, of Rugge, Salop"
Q105819473	Amul	"Sir John Rugge, of Rugge, Salop"

# Q105819485  Sir John|William Booth, of Barton, Lancs  ->  Sir John Booth, of Barton, Lancs   + Sir William Booth, of Barton, Lancs
Q105819485	Lmul	"Sir John Booth, of Barton, Lancs"
Q105819485	Len	"Sir John Booth, of Barton, Lancs"
Q105819485	Lnl	"Sir John Booth, of Barton, Lancs"
Q105819485	Amul	"Sir William Booth, of Barton, Lancs"

# Q105819546  Elsbeth|Alis ferch Thomas ap Hywel ap Llywelyn  ->  Elsbeth ferch Thomas ap Hywel ap Llywelyn   + Alis ferch Thomas ap Hywel ap Llywelyn
Q105819546	Lmul	"Elsbeth ferch Thomas ap Hywel ap Llywelyn"
Q105819546	Len	"Elsbeth ferch Thomas ap Hywel ap Llywelyn"
Q105819546	Lnl	"Elsbeth ferch Thomas ap Hywel ap Llywelyn"
Q105819546	Amul	"Alis ferch Thomas ap Hywel ap Llywelyn"

# Q105819578  Annes|Nest ferch Gwilym ap Gruffudd ap Trahaearn Llwyd  ->  Annes ferch Gwilym ap Gruffudd ap Trahaearn Llwyd   + Nest ferch Gwilym ap Gruffudd ap Trahaearn Llwyd
Q105819578	Lmul	"Annes ferch Gwilym ap Gruffudd ap Trahaearn Llwyd"
Q105819578	Len	"Annes ferch Gwilym ap Gruffudd ap Trahaearn Llwyd"
Q105819578	Lnl	"Annes ferch Gwilym ap Gruffudd ap Trahaearn Llwyd"
Q105819578	Amul	"Nest ferch Gwilym ap Gruffudd ap Trahaearn Llwyd"

# Q105820788  Sir John|Thomas Murdack, of Compton Murdack  ->  Sir John Murdack, of Compton Murdack   + Sir Thomas Murdack, of Compton Murdack
Q105820788	Lmul	"Sir John Murdack, of Compton Murdack"
Q105820788	Len	"Sir John Murdack, of Compton Murdack"
Q105820788	Lnl	"Sir John Murdack, of Compton Murdack"
Q105820788	Amul	"Sir Thomas Murdack, of Compton Murdack"

# Q105820869  Richard|Robert Abrahall  ->  Richard Abrahall   + Robert Abrahall
Q105820869	Lmul	"Richard Abrahall"
Q105820869	Len	"Richard Abrahall"
Q105820869	Lnl	"Richard Abrahall"
Q105820869	Amul	"Robert Abrahall"

# Q105820871  William|Thomas Walwyn, of Bickerton, Heref  ->  William Walwyn, of Bickerton, Heref   + Thomas Walwyn, of Bickerton, Heref
Q105820871	Lmul	"William Walwyn, of Bickerton, Heref"
Q105820871	Len	"William Walwyn, of Bickerton, Heref"
Q105820871	Lnl	"William Walwyn, of Bickerton, Heref"
Q105820871	Amul	"Thomas Walwyn, of Bickerton, Heref"

# Q105820872  Johanna|Elizabeth Greyndour  ->  Johanna Greyndour   + Elizabeth Greyndour
Q105820872	Lmul	"Johanna Greyndour"
Q105820872	Len	"Johanna Greyndour"
Q105820872	Lnl	"Johanna Greyndour"
Q105820872	Amul	"Elizabeth Greyndour"

# Q105821023  Elizabeth|Joan Sanders  ->  Elizabeth Sanders   + Joan Sanders
Q105821023	Lmul	"Elizabeth Sanders"
Q105821023	Len	"Elizabeth Sanders"
Q105821023	Lnl	"Elizabeth Sanders"
Q105821023	Amul	"Joan Sanders"

# Q105821248  Alice|Eleanor|Anne Cornewall  ->  Alice Cornewall   + Eleanor Cornewall | Anne Cornewall
Q105821248	Lmul	"Alice Cornewall"
Q105821248	Len	"Alice Cornewall"
Q105821248	Lnl	"Alice Cornewall"
Q105821248	Amul	"Eleanor Cornewall"
Q105821248	Amul	"Anne Cornewall"

# Q105826045  Anne|Alice Hoorde  ->  Anne Hoorde   + Alice Hoorde
Q105826045	Lmul	"Anne Hoorde"
Q105826045	Len	"Anne Hoorde"
Q105826045	Lnl	"Anne Hoorde"
Q105826045	Amul	"Alice Hoorde"

# Q105826149  Margery|Margaret Harewdon (Harrowden)  ->  Margery Harewdon (Harrowden)   + Margaret Harewdon (Harrowden)
Q105826149	Len	"Margery Harewdon (Harrowden)"
Q105826149	Amul	"Margaret Harewdon (Harrowden)"

# Q105826270  Sir Thomas|Robert Rokes, of Ascortt  ->  Sir Thomas Rokes, of Ascortt   + Sir Robert Rokes, of Ascortt
Q105826270	Lmul	"Sir Thomas Rokes, of Ascortt"
Q105826270	Len	"Sir Thomas Rokes, of Ascortt"
Q105826270	Lnl	"Sir Thomas Rokes, of Ascortt"
Q105826270	Amul	"Sir Robert Rokes, of Ascortt"

# Q105826278  Margaret|Isabel Browne, of Walcot, Northants  ->  Margaret Browne, of Walcot, Northants   + Isabel Browne, of Walcot, Northants
Q105826278	Lmul	"Margaret Browne, of Walcot, Northants"
Q105826278	Len	"Margaret Browne, of Walcot, Northants"
Q105826278	Lnl	"Margaret Browne, of Walcot, Northants"
Q105826278	Amul	"Isabel Browne, of Walcot, Northants"

# Q105826526  Lyonell|Lionel Tollemache  ->  Lyonell Tollemache   + Lionel Tollemache
Q105826526	Lmul	"Lyonell Tollemache"
Q105826526	Len	"Lyonell Tollemache"
Q105826526	Lnl	"Lyonell Tollemache"
Q105826526	Amul	"Lionel Tollemache"

# Q105826551  Agnes|Anne Morley  ->  Agnes Morley   + Anne Morley
Q105826551	Lmul	"Agnes Morley"
Q105826551	Len	"Agnes Morley"
Q105826551	Lnl	"Agnes Morley"
Q105826551	Amul	"Anne Morley"

# Q105853236  Geoffrey|John Boydell, of Pulcroft  ->  Geoffrey Boydell, of Pulcroft   + John Boydell, of Pulcroft
Q105853236	Lmul	"Geoffrey Boydell, of Pulcroft"
Q105853236	Len	"Geoffrey Boydell, of Pulcroft"
Q105853236	Lnl	"Geoffrey Boydell, of Pulcroft"
Q105853236	Amul	"John Boydell, of Pulcroft"

# Q105853668  Margaret|Mary Whitfield  ->  Margaret Whitfield   + Mary Whitfield
Q105853668	Lmul	"Margaret Whitfield"
Q105853668	Len	"Margaret Whitfield"
Q105853668	Lnl	"Margaret Whitfield"
Q105853668	Amul	"Mary Whitfield"

# Q105856648  Elizabeth|Alice Ansley (Apsley)  ->  Elizabeth Ansley (Apsley)   + Alice Ansley (Apsley)
Q105856648	Len	"Elizabeth Ansley (Apsley)"
Q105856648	Amul	"Alice Ansley (Apsley)"

# Q105871948  Elen|Jonette ferch Thomas ap Rhys ap Cynwrig  ->  Elen ferch Thomas ap Rhys ap Cynwrig   + Jonette ferch Thomas ap Rhys ap Cynwrig
Q105871948	Lmul	"Elen ferch Thomas ap Rhys ap Cynwrig"
Q105871948	Len	"Elen ferch Thomas ap Rhys ap Cynwrig"
Q105871948	Lnl	"Elen ferch Thomas ap Rhys ap Cynwrig"
Q105871948	Amul	"Jonette ferch Thomas ap Rhys ap Cynwrig"

# Q105871961  Margred|Margred Talbot  ->  Margred Talbot
Q105871961	Lmul	"Margred Talbot"
Q105871961	Len	"Margred Talbot"
Q105871961	Lnl	"Margred Talbot"

# Q105871975  Anne|Thomasine Sothill  ->  Anne Sothill   + Thomasine Sothill
Q105871975	Lmul	"Anne Sothill"
Q105871975	Len	"Anne Sothill"
Q105871975	Lnl	"Anne Sothill"
Q105871975	Amul	"Thomasine Sothill"

# Q105872053  Eleanor|Elizabeth Ramsey  ->  Eleanor Ramsey   + Elizabeth Ramsey
Q105872053	Lmul	"Eleanor Ramsey"
Q105872053	Len	"Eleanor Ramsey"
Q105872053	Lnl	"Eleanor Ramsey"
Q105872053	Amul	"Elizabeth Ramsey"

# Q105872261  Elizabeth|Dorothy Wolriche  ->  Elizabeth Wolriche   + Dorothy Wolriche
Q105872261	Lmul	"Elizabeth Wolriche"
Q105872261	Len	"Elizabeth Wolriche"
Q105872261	Lnl	"Elizabeth Wolriche"
Q105872261	Amul	"Dorothy Wolriche"

# Q105872266  Eleanor|Joyce Peshale (Peshall)  ->  Eleanor Peshale (Peshall)   + Joyce Peshale (Peshall)
Q105872266	Len	"Eleanor Peshale (Peshall)"
Q105872266	Amul	"Joyce Peshale (Peshall)"

# Q105872306  Andrew|Edward Wolriche, of Dudmaston, Salop  ->  Andrew Wolriche, of Dudmaston, Salop   + Edward Wolriche, of Dudmaston, Salop
Q105872306	Lmul	"Andrew Wolriche, of Dudmaston, Salop"
Q105872306	Len	"Andrew Wolriche, of Dudmaston, Salop"
Q105872306	Lnl	"Andrew Wolriche, of Dudmaston, Salop"
Q105872306	Amul	"Edward Wolriche, of Dudmaston, Salop"

# Q105872420  Juliana|Katherine Burley  ->  Juliana Burley   + Katherine Burley
Q105872420	Lmul	"Juliana Burley"
Q105872420	Len	"Juliana Burley"
Q105872420	Lnl	"Juliana Burley"
Q105872420	Amul	"Katherine Burley"

# Q105872471  Elizabeth|Eleanor Winter, of Maynorgayng  ->  Elizabeth Winter, of Maynorgayng   + Eleanor Winter, of Maynorgayng
Q105872471	Lmul	"Elizabeth Winter, of Maynorgayng"
Q105872471	Len	"Elizabeth Winter, of Maynorgayng"
Q105872471	Lnl	"Elizabeth Winter, of Maynorgayng"
Q105872471	Amul	"Eleanor Winter, of Maynorgayng"

# Q105873235  Elizabeth|Eleanor Flambard  ->  Elizabeth Flambard   + Eleanor Flambard
Q105873235	Lmul	"Elizabeth Flambard"
Q105873235	Len	"Elizabeth Flambard"
Q105873235	Lnl	"Elizabeth Flambard"
Q105873235	Amul	"Eleanor Flambard"

# Q105873237  Antiocha|Mary Hawkwood  ->  Antiocha Hawkwood   + Mary Hawkwood
Q105873237	Lmul	"Antiocha Hawkwood"
Q105873237	Len	"Antiocha Hawkwood"
Q105873237	Lnl	"Antiocha Hawkwood"
Q105873237	Amul	"Mary Hawkwood"

# Q105873243  Elizabeth|Eleanor Popham  ->  Elizabeth Popham   + Eleanor Popham
Q105873243	Lmul	"Elizabeth Popham"
Q105873243	Len	"Elizabeth Popham"
Q105873243	Lnl	"Elizabeth Popham"
Q105873243	Amul	"Eleanor Popham"

# Q105873289  Dorothy|Elizabeth Read (or Rede)  ->  Dorothy Read (or Rede)   + Elizabeth Read (or Rede)
Q105873289	Len	"Dorothy Read (or Rede)"
Q105873289	Amul	"Elizabeth Read (or Rede)"

# Q105873410  Ursula Angels|Engele von Wrede zu Reigern  ->  Ursula Angels von Wrede zu Reigern   + Ursula Engele von Wrede zu Reigern
Q105873410	Lmul	"Ursula Angels von Wrede zu Reigern"
Q105873410	Len	"Ursula Angels von Wrede zu Reigern"
Q105873410	Lnl	"Ursula Angels von Wrede zu Reigern"
Q105873410	Amul	"Ursula Engele von Wrede zu Reigern"

# Q105873542  Agnes|Alice  ->  Agnes   + Alice
Q105873542	Lmul	"Agnes"
Q105873542	Len	"Agnes"
Q105873542	Lnl	"Agnes"
Q105873542	Amul	"Alice"

# Q105878032  Anne|Agnes  ->  Anne   + Agnes
Q105878032	Lmul	"Anne"
Q105878032	Len	"Anne"
Q105878032	Lnl	"Anne"
Q105878032	Amul	"Agnes"

# Q105878035  Annis|Agnes Bayford  ->  Annis Bayford   + Agnes Bayford
Q105878035	Lmul	"Annis Bayford"
Q105878035	Len	"Annis Bayford"
Q105878035	Lnl	"Annis Bayford"
Q105878035	Amul	"Agnes Bayford"

# Q105905320  Duyff|Duijff Boelendr.  ->  Duyff Boelendr.   + Duijff Boelendr.
Q105905320	Lmul	"Duyff Boelendr."
Q105905320	Len	"Duyff Boelendr."
Q105905320	Lnl	"Duyff Boelendr."
Q105905320	Amul	"Duijff Boelendr."

# Q105905763  Henrica|Hendersken Kaldenbach  ->  Henrica Kaldenbach   + Hendersken Kaldenbach
Q105905763	Lmul	"Henrica Kaldenbach"
Q105905763	Len	"Henrica Kaldenbach"
Q105905763	Lnl	"Henrica Kaldenbach"
Q105905763	Amul	"Hendersken Kaldenbach"

# Q105983384  Margaretha|Alijt Hollen or van der Hell  ->  Margaretha Hollen or van der Hell   + Alijt Hollen or van der Hell
Q105983384	Lmul	"Margaretha Hollen or van der Hell"
Q105983384	Len	"Margaretha Hollen or van der Hell"
Q105983384	Lnl	"Margaretha Hollen or van der Hell"
Q105983384	Amul	"Alijt Hollen or van der Hell"

# Q105983925  Jan|Johan van Lynden, 3.Heer van Hemmen  ->  Jan van Lynden, 3.Heer van Hemmen   + Johan van Lynden, 3.Heer van Hemmen
Q105983925	Lmul	"Jan van Lynden, 3.Heer van Hemmen"
Q105983925	Len	"Jan van Lynden, 3.Heer van Hemmen"
Q105983925	Lnl	"Jan van Lynden, 3.Heer van Hemmen"
Q105983925	Amul	"Johan van Lynden, 3.Heer van Hemmen"

# Q105983962  Fulkwine|Fulckwina|Folswijn van Randwijck  ->  Fulkwine van Randwijck   + Fulckwina van Randwijck | Folswijn van Randwijck
Q105983962	Lmul	"Fulkwine van Randwijck"
Q105983962	Len	"Fulkwine van Randwijck"
Q105983962	Lnl	"Fulkwine van Randwijck"
Q105983962	Amul	"Fulckwina van Randwijck"
Q105983962	Amul	"Folswijn van Randwijck"

# Q106503213  Elizabeth|Cicely Mitchell (Michell)  ->  Elizabeth Mitchell (Michell)   + Cicely Mitchell (Michell)
Q106503213	Len	"Elizabeth Mitchell (Michell)"
Q106503213	Amul	"Cicely Mitchell (Michell)"

# Q106503248  Isabel|Eleanor (Thomasine) Totham (Tatton)  ->  Isabel (Thomasine) Totham (Tatton)   + Eleanor (Thomasine) Totham (Tatton)
Q106503248	Len	"Isabel (Thomasine) Totham (Tatton)"
Q106503248	Amul	"Eleanor (Thomasine) Totham (Tatton)"

# Q106503748  Ralph|John Roscarrock  ->  Ralph Roscarrock   + John Roscarrock
Q106503748	Lmul	"Ralph Roscarrock"
Q106503748	Len	"Ralph Roscarrock"
Q106503748	Lnl	"Ralph Roscarrock"
Q106503748	Amul	"John Roscarrock"

# Q106503764  Sir Renfry|Reinfrid de Arundell  ->  Sir Renfry de Arundell   + Sir Reinfrid de Arundell
Q106503764	Lmul	"Sir Renfry de Arundell"
Q106503764	Len	"Sir Renfry de Arundell"
Q106503764	Lnl	"Sir Renfry de Arundell"
Q106503764	Amul	"Sir Reinfrid de Arundell"

# Q106503776  Ralph|John Trenowith  ->  Ralph Trenowith   + John Trenowith
Q106503776	Lmul	"Ralph Trenowith"
Q106503776	Len	"Ralph Trenowith"
Q106503776	Lnl	"Ralph Trenowith"
Q106503776	Amul	"John Trenowith"

# Q106504492  Margaret|Margery Danby  ->  Margaret Danby   + Margery Danby
Q106504492	Lmul	"Margaret Danby"
Q106504492	Len	"Margaret Danby"
Q106504492	Lnl	"Margaret Danby"
Q106504492	Amul	"Margery Danby"

# Q106504493  Ralph|Robert Danby, of Yafforth  ->  Ralph Danby, of Yafforth   + Robert Danby, of Yafforth
Q106504493	Lmul	"Ralph Danby, of Yafforth"
Q106504493	Len	"Ralph Danby, of Yafforth"
Q106504493	Lnl	"Ralph Danby, of Yafforth"
Q106504493	Amul	"Robert Danby, of Yafforth"

# Q106506175  John|Ion Chalkhill, of Kingsbury  ->  John Chalkhill, of Kingsbury   + Ion Chalkhill, of Kingsbury
Q106506175	Lmul	"John Chalkhill, of Kingsbury"
Q106506175	Len	"John Chalkhill, of Kingsbury"
Q106506175	Lnl	"John Chalkhill, of Kingsbury"
Q106506175	Amul	"Ion Chalkhill, of Kingsbury"

# Q106508128  Thomas|John Sandford, of Askham, Westm  ->  Thomas Sandford, of Askham, Westm   + John Sandford, of Askham, Westm
Q106508128	Lmul	"Thomas Sandford, of Askham, Westm"
Q106508128	Len	"Thomas Sandford, of Askham, Westm"
Q106508128	Lnl	"Thomas Sandford, of Askham, Westm"
Q106508128	Amul	"John Sandford, of Askham, Westm"

# Q106508150  Maud|Mabel Middleton, of Middleton  ->  Maud Middleton, of Middleton   + Mabel Middleton, of Middleton
Q106508150	Lmul	"Maud Middleton, of Middleton"
Q106508150	Len	"Maud Middleton, of Middleton"
Q106508150	Lnl	"Maud Middleton, of Middleton"
Q106508150	Amul	"Mabel Middleton, of Middleton"

# Q106509507  Agnes|Anne Yewings  ->  Agnes Yewings   + Anne Yewings
Q106509507	Lmul	"Agnes Yewings"
Q106509507	Len	"Agnes Yewings"
Q106509507	Lnl	"Agnes Yewings"
Q106509507	Amul	"Anne Yewings"

# Q106509702  Thomas Hayton, of Botayles|Batailles  ->  Thomas Hayton, of Botayles   + Thomas Hayton, of Batailles
Q106509702	Lmul	"Thomas Hayton, of Botayles"
Q106509702	Len	"Thomas Hayton, of Botayles"
Q106509702	Lnl	"Thomas Hayton, of Botayles"
Q106509702	Amul	"Thomas Hayton, of Batailles"

# Q106509740  Margaret|Eleanor Beaumont  ->  Margaret Beaumont   + Eleanor Beaumont
Q106509740	Len	"Margaret Beaumont"
Q106509740	Lnl	"Margaret Beaumont"
Q106509740	Amul	"Eleanor Beaumont"

# Q106509779  Maude|Eleanor Deincourt (Daucote)  ->  Maude Deincourt (Daucote)   + Eleanor Deincourt (Daucote)
Q106509779	Len	"Maude Deincourt (Daucote)"
Q106509779	Amul	"Eleanor Deincourt (Daucote)"

# Q106637451  Elizabeth|Agnes Aske  ->  Elizabeth Aske   + Agnes Aske
Q106637451	Lmul	"Elizabeth Aske"
Q106637451	Len	"Elizabeth Aske"
Q106637451	Lnl	"Elizabeth Aske"
Q106637451	Amul	"Agnes Aske"

# Q106637473  Mary|Margaret St.John  ->  Mary St.John   + Margaret St.John
Q106637473	Lmul	"Mary St.John"
Q106637473	Len	"Mary St.John"
Q106637473	Lnl	"Mary St.John"
Q106637473	Amul	"Margaret St.John"

# Q106686149  Maud|Matilda Lascelles, of Scourby  ->  Maud Lascelles, of Scourby   + Matilda Lascelles, of Scourby
Q106686149	Lmul	"Maud Lascelles, of Scourby"
Q106686149	Len	"Maud Lascelles, of Scourby"
Q106686149	Lnl	"Maud Lascelles, of Scourby"
Q106686149	Amul	"Matilda Lascelles, of Scourby"

# Q106686152  Eleanor|Ellen Harrington  ->  Eleanor Harrington   + Ellen Harrington
Q106686152	Lmul	"Eleanor Harrington"
Q106686152	Len	"Eleanor Harrington"
Q106686152	Lnl	"Eleanor Harrington"
Q106686152	Amul	"Ellen Harrington"

# Q106686236  Margaret|Matilda Vavasour  ->  Margaret Vavasour   + Matilda Vavasour
Q106686236	Lmul	"Margaret Vavasour"
Q106686236	Len	"Margaret Vavasour"
Q106686236	Lnl	"Margaret Vavasour"
Q106686236	Amul	"Matilda Vavasour"

# Q106703056  Ales|Alswn|Alice ferch Gruffudd ap Jenkin Broughton  ->  Ales ferch Gruffudd ap Jenkin Broughton   + Alswn ferch Gruffudd ap Jenkin Broughton | Alice ferch Gruffudd ap Jenkin Broughton
Q106703056	Lmul	"Ales ferch Gruffudd ap Jenkin Broughton"
Q106703056	Len	"Ales ferch Gruffudd ap Jenkin Broughton"
Q106703056	Lnl	"Ales ferch Gruffudd ap Jenkin Broughton"
Q106703056	Amul	"Alswn ferch Gruffudd ap Jenkin Broughton"
Q106703056	Amul	"Alice ferch Gruffudd ap Jenkin Broughton"

# Q106703064  Elsbeth|Elizabeth Conwy  ->  Elsbeth Conwy   + Elizabeth Conwy
Q106703064	Lmul	"Elsbeth Conwy"
Q106703064	Len	"Elsbeth Conwy"
Q106703064	Lnl	"Elsbeth Conwy"
Q106703064	Amul	"Elizabeth Conwy"

# Q106703090  Dafydd ap Dafydd|Rhirid y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn  ->  Dafydd ap Dafydd y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn   + Dafydd ap Rhirid y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn
Q106703090	Len	"Dafydd ap Dafydd y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn"
Q106703090	Lnl	"Dafydd ap Dafydd y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn"
Q106703090	Amul	"Dafydd ap Rhirid y Pothan Flaidd ap Rhirid Fychan ap Madog of Penllyn"

# Q106703146  Edward|Edmund Catesby, of Seaton, Rutland  ->  Edward Catesby, of Seaton, Rutland   + Edmund Catesby, of Seaton, Rutland
Q106703146	Lmul	"Edward Catesby, of Seaton, Rutland"
Q106703146	Len	"Edward Catesby, of Seaton, Rutland"
Q106703146	Lnl	"Edward Catesby, of Seaton, Rutland"
Q106703146	Amul	"Edmund Catesby, of Seaton, Rutland"

# Q106703170  Isabel|Elizabeth Brocket  ->  Isabel Brocket   + Elizabeth Brocket
Q106703170	Lmul	"Isabel Brocket"
Q106703170	Len	"Isabel Brocket"
Q106703170	Lnl	"Isabel Brocket"
Q106703170	Amul	"Elizabeth Brocket"

# Q106703189  Amice|Amicia de Arden (Arderne)  ->  Amice de Arden (Arderne)   + Amicia de Arden (Arderne)
Q106703189	Len	"Amice de Arden (Arderne)"
Q106703189	Amul	"Amicia de Arden (Arderne)"

# Q106703521  Elizabeth|Katherine Corbet  ->  Elizabeth Corbet   + Katherine Corbet
Q106703521	Lmul	"Elizabeth Corbet"
Q106703521	Len	"Elizabeth Corbet"
Q106703521	Lnl	"Elizabeth Corbet"
Q106703521	Amul	"Katherine Corbet"

# Q106703528  Joan|Alice Besford  ->  Joan Besford   + Alice Besford
Q106703528	Lmul	"Joan Besford"
Q106703528	Len	"Joan Besford"
Q106703528	Lnl	"Joan Besford"
Q106703528	Amul	"Alice Besford"

# Q106703657  Anthony|Antoise Larbalestier, seigneur d'Augres  ->  Anthony Larbalestier, seigneur d'Augres   + Antoise Larbalestier, seigneur d'Augres
Q106703657	Lmul	"Anthony Larbalestier, seigneur d'Augres"
Q106703657	Len	"Anthony Larbalestier, seigneur d'Augres"
Q106703657	Lnl	"Anthony Larbalestier, seigneur d'Augres"
Q106703657	Amul	"Antoise Larbalestier, seigneur d'Augres"

# Q106703744  John|Jean Aumont  ->  John Aumont   + Jean Aumont
Q106703744	Lmul	"John Aumont"
Q106703744	Len	"John Aumont"
Q106703744	Lnl	"John Aumont"
Q106703744	Amul	"Jean Aumont"

# Q106703787  Margaret Mudge|Mugge  ->  Margaret Mudge   + Margaret Mugge
Q106703787	Lmul	"Margaret Mudge"
Q106703787	Len	"Margaret Mudge"
Q106703787	Lnl	"Margaret Mudge"
Q106703787	Amul	"Margaret Mugge"

# Q106703811  John|Jean Messervy, of St.Martin  ->  John Messervy, of St.Martin   + Jean Messervy, of St.Martin
Q106703811	Lmul	"John Messervy, of St.Martin"
Q106703811	Len	"John Messervy, of St.Martin"
Q106703811	Lnl	"John Messervy, of St.Martin"
Q106703811	Amul	"Jean Messervy, of St.Martin"

# Q106703813  Jean|John Lempriere, seigneur de Rozel  ->  Jean Lempriere, seigneur de Rozel   + John Lempriere, seigneur de Rozel
Q106703813	Lmul	"Jean Lempriere, seigneur de Rozel"
Q106703813	Len	"Jean Lempriere, seigneur de Rozel"
Q106703813	Lnl	"Jean Lempriere, seigneur de Rozel"
Q106703813	Amul	"John Lempriere, seigneur de Rozel"

# Q106703974  Joan|Elizabeth Corbet  ->  Joan Corbet   + Elizabeth Corbet
Q106703974	Lmul	"Joan Corbet"
Q106703974	Len	"Joan Corbet"
Q106703974	Lnl	"Joan Corbet"
Q106703974	Amul	"Elizabeth Corbet"

# Q106703977  William|Thomas Corbet, of Wollaston  ->  William Corbet, of Wollaston   + Thomas Corbet, of Wollaston
Q106703977	Lmul	"William Corbet, of Wollaston"
Q106703977	Len	"William Corbet, of Wollaston"
Q106703977	Lnl	"William Corbet, of Wollaston"
Q106703977	Amul	"Thomas Corbet, of Wollaston"

# Q106704199  William|Watkin Garraway (or Garway), of Welby  ->  William Garraway (or Garway), of Welby   + Watkin Garraway (or Garway), of Welby
Q106704199	Lmul	"William Garraway (or Garway), of Welby"
Q106704199	Len	"William Garraway (or Garway), of Welby"
Q106704199	Lnl	"William Garraway (or Garway), of Welby"
Q106704199	Amul	"Watkin Garraway (or Garway), of Welby"

# Q106704202  Elizabeth|Ursula Brydges  ->  Elizabeth Brydges   + Ursula Brydges
Q106704202	Lmul	"Elizabeth Brydges"
Q106704202	Len	"Elizabeth Brydges"
Q106704202	Lnl	"Elizabeth Brydges"
Q106704202	Amul	"Ursula Brydges"

# Q106704208  Sarah|Sarra  ->  Sarah   + Sarra
Q106704208	Lmul	"Sarah"
Q106704208	Len	"Sarah"
Q106704208	Lnl	"Sarah"
Q106704208	Amul	"Sarra"

# Q106704220  William|Thomas Birch  ->  William Birch   + Thomas Birch
Q106704220	Lmul	"William Birch"
Q106704220	Len	"William Birch"
Q106704220	Lnl	"William Birch"
Q106704220	Amul	"Thomas Birch"

# Q106704535  Elizabeth|Alice Boteler, of Bewsey  ->  Elizabeth Boteler, of Bewsey   + Alice Boteler, of Bewsey
Q106704535	Lmul	"Elizabeth Boteler, of Bewsey"
Q106704535	Len	"Elizabeth Boteler, of Bewsey"
Q106704535	Lnl	"Elizabeth Boteler, of Bewsey"
Q106704535	Amul	"Alice Boteler, of Bewsey"

# Q106704540  Alice|Ellen Harington, of Wolfage  ->  Alice Harington, of Wolfage   + Ellen Harington, of Wolfage
Q106704540	Lmul	"Alice Harington, of Wolfage"
Q106704540	Len	"Alice Harington, of Wolfage"
Q106704540	Lnl	"Alice Harington, of Wolfage"
Q106704540	Amul	"Ellen Harington, of Wolfage"

# Q106704547  Alice|Dulcia Savage  ->  Alice Savage   + Dulcia Savage
Q106704547	Lmul	"Alice Savage"
Q106704547	Len	"Alice Savage"
Q106704547	Lnl	"Alice Savage"
Q106704547	Amul	"Dulcia Savage"

# Q106704701  Maud|Margaret Dethick  ->  Maud Dethick   + Margaret Dethick
Q106704701	Lmul	"Maud Dethick"
Q106704701	Len	"Maud Dethick"
Q106704701	Lnl	"Maud Dethick"
Q106704701	Amul	"Margaret Dethick"

# Q107146443  Seince|Sanche Draper  ->  Seince Draper   + Sanche Draper
Q107146443	Lmul	"Seince Draper"
Q107146443	Len	"Seince Draper"
Q107146443	Lnl	"Seince Draper"
Q107146443	Amul	"Sanche Draper"

# Q107146499  Sibyl|Sibbell  ->  Sibyl   + Sibbell
Q107146499	Lmul	"Sibyl"
Q107146499	Len	"Sibyl"
Q107146499	Lnl	"Sibyl"
Q107146499	Amul	"Sibbell"

# Q107211527  Richardis|Maria von Alfter  ->  Richardis von Alfter   + Maria von Alfter
Q107211527	Lmul	"Richardis von Alfter"
Q107211527	Len	"Richardis von Alfter"
Q107211527	Lnl	"Richardis von Alfter"
Q107211527	Amul	"Maria von Alfter"

# Q107211558  Gilles|Egidius van Hamale (Hamal), Heer van Elderen  ->  Gilles van Hamale (Hamal), Heer van Elderen   + Egidius van Hamale (Hamal), Heer van Elderen
Q107211558	Lmul	"Gilles van Hamale (Hamal), Heer van Elderen"
Q107211558	Len	"Gilles van Hamale (Hamal), Heer van Elderen"
Q107211558	Lnl	"Gilles van Hamale (Hamal), Heer van Elderen"
Q107211558	Amul	"Egidius van Hamale (Hamal), Heer van Elderen"

# Q107211596  Godard|Gottfried II van Flodrop, Voogd van Roermond 1369-1405  ->  Godard II van Flodrop, Voogd van Roermond 1369-1405   + Gottfried II van Flodrop, Voogd van Roermond 1369-1405
Q107211596	Lmul	"Godard II van Flodrop, Voogd van Roermond 1369-1405"
Q107211596	Len	"Godard II van Flodrop, Voogd van Roermond 1369-1405"
Q107211596	Lnl	"Godard II van Flodrop, Voogd van Roermond 1369-1405"
Q107211596	Amul	"Gottfried II van Flodrop, Voogd van Roermond 1369-1405"

# Q107211783  Richza|Rixa von Querfurt zu Schraplau  ->  Richza von Querfurt zu Schraplau   + Rixa von Querfurt zu Schraplau
Q107211783	Lmul	"Richza von Querfurt zu Schraplau"
Q107211783	Len	"Richza von Querfurt zu Schraplau"
Q107211783	Lnl	"Richza von Querfurt zu Schraplau"
Q107211783	Amul	"Rixa von Querfurt zu Schraplau"

# Q107211784  Umarg|Amarg, Herr van Waldenburg  ->  Umarg Herr van Waldenburg   + Amarg, Herr van Waldenburg
Q107211784	Len	"Umarg Herr van Waldenburg"
Q107211784	Lnl	"Umarg Herr van Waldenburg"
Q107211784	Amul	"Amarg, Herr van Waldenburg"

# Q107211806  Willeburgis|Wilibirg von Querfurt, Burggräfin von Magdeburg  ->  Willeburgis von Querfurt, Burggräfin von Magdeburg   + Wilibirg von Querfurt, Burggräfin von Magdeburg
Q107211806	Len	"Willeburgis von Querfurt, Burggräfin von Magdeburg"
Q107211806	Lnl	"Willeburgis von Querfurt, Burggräfin von Magdeburg"
Q107211806	Amul	"Wilibirg von Querfurt, Burggräfin von Magdeburg"

# Q107212014  Aechte|Petronella van Steenhuys Pieter Nevendr.  ->  Aechte van Steenhuys Pieter Nevendr.   + Petronella van Steenhuys Pieter Nevendr.
Q107212014	Lmul	"Aechte van Steenhuys Pieter Nevendr."
Q107212014	Len	"Aechte van Steenhuys Pieter Nevendr."
Q107212014	Lnl	"Aechte van Steenhuys Pieter Nevendr."
Q107212014	Amul	"Petronella van Steenhuys Pieter Nevendr."

# Q107212020  Willem|Jan van der Burch  ->  Willem van der Burch   + Jan van der Burch
Q107212020	Lmul	"Willem van der Burch"
Q107212020	Len	"Willem van der Burch"
Q107212020	Lnl	"Willem van der Burch"
Q107212020	Amul	"Jan van der Burch"

# Q107275154  Cecily|Cicely Bussey (Bussy)  ->  Cecily Bussey (Bussy)   + Cicely Bussey (Bussy)
Q107275154	Len	"Cecily Bussey (Bussy)"
Q107275154	Amul	"Cicely Bussey (Bussy)"

# Q107275174  Ann|Katherine Vavasour, of Hazlewood  ->  Ann Vavasour, of Hazlewood   + Katherine Vavasour, of Hazlewood
Q107275174	Lmul	"Ann Vavasour, of Hazlewood"
Q107275174	Len	"Ann Vavasour, of Hazlewood"
Q107275174	Lnl	"Ann Vavasour, of Hazlewood"
Q107275174	Amul	"Katherine Vavasour, of Hazlewood"

# Q107275715  Alice|Sibil Wasteneys  ->  Alice Wasteneys   + Sibil Wasteneys
Q107275715	Lmul	"Alice Wasteneys"
Q107275715	Len	"Alice Wasteneys"
Q107275715	Lnl	"Alice Wasteneys"
Q107275715	Amul	"Sibil Wasteneys"

# Q107275841  Hugh|Thomas de Corona  ->  Hugh de Corona   + Thomas de Corona
Q107275841	Lmul	"Hugh de Corona"
Q107275841	Len	"Hugh de Corona"
Q107275841	Lnl	"Hugh de Corona"
Q107275841	Amul	"Thomas de Corona"

# Q107275933  Isabel|Sibyl Bellew  ->  Isabel Bellew   + Sibyl Bellew
Q107275933	Lmul	"Isabel Bellew"
Q107275933	Len	"Isabel Bellew"
Q107275933	Lnl	"Isabel Bellew"
Q107275933	Amul	"Sibyl Bellew"

# Q107276673  Margaret|Alianor Cheyne (Cheney), of Pinhoe  ->  Margaret Cheyne (Cheney), of Pinhoe   + Alianor Cheyne (Cheney), of Pinhoe
Q107276673	Lmul	"Margaret Cheyne (Cheney), of Pinhoe"
Q107276673	Len	"Margaret Cheyne (Cheney), of Pinhoe"
Q107276673	Lnl	"Margaret Cheyne (Cheney), of Pinhoe"
Q107276673	Amul	"Alianor Cheyne (Cheney), of Pinhoe"

# Q107276761  William|Thomas Baskett, of Dewlish  ->  William Baskett, of Dewlish   + Thomas Baskett, of Dewlish
Q107276761	Lmul	"William Baskett, of Dewlish"
Q107276761	Len	"William Baskett, of Dewlish"
Q107276761	Lnl	"William Baskett, of Dewlish"
Q107276761	Amul	"Thomas Baskett, of Dewlish"

# Q107276770  Margaret|Mary Fitzjames, of Redlynch  ->  Margaret Fitzjames, of Redlynch   + Mary Fitzjames, of Redlynch
Q107276770	Lmul	"Margaret Fitzjames, of Redlynch"
Q107276770	Len	"Margaret Fitzjames, of Redlynch"
Q107276770	Lnl	"Margaret Fitzjames, of Redlynch"
Q107276770	Amul	"Mary Fitzjames, of Redlynch"

# Q107276777  Margaret|Margery Brockman  ->  Margaret Brockman   + Margery Brockman
Q107276777	Lmul	"Margaret Brockman"
Q107276777	Len	"Margaret Brockman"
Q107276777	Lnl	"Margaret Brockman"
Q107276777	Amul	"Margery Brockman"

# Q107276944  Thomas|John Hody (Huddy), of Kington Magna  ->  Thomas Hody (Huddy), of Kington Magna   + John Hody (Huddy), of Kington Magna
Q107276944	Lmul	"Thomas Hody (Huddy), of Kington Magna"
Q107276944	Len	"Thomas Hody (Huddy), of Kington Magna"
Q107276944	Lnl	"Thomas Hody (Huddy), of Kington Magna"
Q107276944	Amul	"John Hody (Huddy), of Kington Magna"

# Q107277197  Godfrey|Geoffrey Lyffe, of Currypool (Corypole)  ->  Godfrey Lyffe, of Currypool (Corypole)   + Geoffrey Lyffe, of Currypool (Corypole)
Q107277197	Lmul	"Godfrey Lyffe, of Currypool (Corypole)"
Q107277197	Len	"Godfrey Lyffe, of Currypool (Corypole)"
Q107277197	Lnl	"Godfrey Lyffe, of Currypool (Corypole)"
Q107277197	Amul	"Geoffrey Lyffe, of Currypool (Corypole)"

# Q107278685  Margery|Margaret Cralle  ->  Margery Cralle   + Margaret Cralle
Q107278685	Lmul	"Margery Cralle"
Q107278685	Len	"Margery Cralle"
Q107278685	Lnl	"Margery Cralle"
Q107278685	Amul	"Margaret Cralle"

# Q107278784  Beatrix|Bridget Wesse (West)  ->  Beatrix Wesse (West)   + Bridget Wesse (West)
Q107278784	Len	"Beatrix Wesse (West)"
Q107278784	Amul	"Bridget Wesse (West)"

# Q107278888  Margaret|Bridget Kene (Kyme)  ->  Margaret Kene (Kyme)   + Bridget Kene (Kyme)
Q107278888	Len	"Margaret Kene (Kyme)"
Q107278888	Amul	"Bridget Kene (Kyme)"

# Q107278907  Isabel|Katherine Bellingham  ->  Isabel Bellingham   + Katherine Bellingham
Q107278907	Lmul	"Isabel Bellingham"
Q107278907	Len	"Isabel Bellingham"
Q107278907	Lnl	"Isabel Bellingham"
Q107278907	Amul	"Katherine Bellingham"

# Q107278915  Margaret|Elizabeth Redmayne (Redman), of Harewood  ->  Margaret Redmayne (Redman), of Harewood   + Elizabeth Redmayne (Redman), of Harewood
Q107278915	Lmul	"Margaret Redmayne (Redman), of Harewood"
Q107278915	Len	"Margaret Redmayne (Redman), of Harewood"
Q107278915	Lnl	"Margaret Redmayne (Redman), of Harewood"
Q107278915	Amul	"Elizabeth Redmayne (Redman), of Harewood"

# Q107278956  Anne|Alice Fincham  ->  Anne Fincham   + Alice Fincham
Q107278956	Lmul	"Anne Fincham"
Q107278956	Len	"Anne Fincham"
Q107278956	Lnl	"Anne Fincham"
Q107278956	Amul	"Alice Fincham"

# Q107279030  Anne|Mary Sidney  ->  Anne Sidney   + Mary Sidney
Q107279030	Lmul	"Anne Sidney"
Q107279030	Len	"Anne Sidney"
Q107279030	Lnl	"Anne Sidney"
Q107279030	Amul	"Mary Sidney"

# Q107279089  John|Thomas Metcalfe  ->  John Metcalfe   + Thomas Metcalfe
Q107279089	Lmul	"John Metcalfe"
Q107279089	Len	"John Metcalfe"
Q107279089	Lnl	"John Metcalfe"
Q107279089	Amul	"Thomas Metcalfe"

# Q107305290  Maret|Maarja Molkenbur  ->  Maret Molkenbur   + Maarja Molkenbur
Q107305290	Lmul	"Maret Molkenbur"
Q107305290	Len	"Maret Molkenbur"
Q107305290	Lnl	"Maret Molkenbur"
Q107305290	Amul	"Maarja Molkenbur"

# Q108180006  Joan|Jane Oteley (Ottley), of Pitchford  ->  Joan Oteley (Ottley), of Pitchford   + Jane Oteley (Ottley), of Pitchford
Q108180006	Lmul	"Joan Oteley (Ottley), of Pitchford"
Q108180006	Len	"Joan Oteley (Ottley), of Pitchford"
Q108180006	Lnl	"Joan Oteley (Ottley), of Pitchford"
Q108180006	Amul	"Jane Oteley (Ottley), of Pitchford"

# Q108180013  Alice|Elizabeth Corbet, of Lee (Leigh)  ->  Alice Corbet, of Lee (Leigh)   + Elizabeth Corbet, of Lee (Leigh)
Q108180013	Lmul	"Alice Corbet, of Lee (Leigh)"
Q108180013	Len	"Alice Corbet, of Lee (Leigh)"
Q108180013	Lnl	"Alice Corbet, of Lee (Leigh)"
Q108180013	Amul	"Elizabeth Corbet, of Lee (Leigh)"

# Q108187134  Mary|Margery Monson  ->  Mary Monson   + Margery Monson
Q108187134	Lmul	"Mary Monson"
Q108187134	Len	"Mary Monson"
Q108187134	Lnl	"Mary Monson"
Q108187134	Amul	"Margery Monson"

# Q108306212  Susan|Elizabeth Rogers (or Rodgers)  ->  Susan Rogers (or Rodgers)   + Elizabeth Rogers (or Rodgers)
Q108306212	Len	"Susan Rogers (or Rodgers)"
Q108306212	Amul	"Elizabeth Rogers (or Rodgers)"

# Q108306320  Joanna|Joan|Juliana Cokrel (Cockrell)  ->  Joanna Cokrel (Cockrell)   + Joan Cokrel (Cockrell) | Juliana Cokrel (Cockrell)
Q108306320	Len	"Joanna Cokrel (Cockrell)"
Q108306320	Amul	"Joan Cokrel (Cockrell)"
Q108306320	Amul	"Juliana Cokrel (Cockrell)"

# Q108306323  John|William Cusse, of Broughton Gifford  ->  John Cusse, of Broughton Gifford   + William Cusse, of Broughton Gifford
Q108306323	Lmul	"John Cusse, of Broughton Gifford"
Q108306323	Len	"John Cusse, of Broughton Gifford"
Q108306323	Lnl	"John Cusse, of Broughton Gifford"
Q108306323	Amul	"William Cusse, of Broughton Gifford"

# Q108306344  Eleanor|Helen Crooke  ->  Eleanor Crooke   + Helen Crooke
Q108306344	Lmul	"Eleanor Crooke"
Q108306344	Len	"Eleanor Crooke"
Q108306344	Lnl	"Eleanor Crooke"
Q108306344	Amul	"Helen Crooke"

# Q108409338  Caroline|Charlotte Levy  ->  Caroline Levy   + Charlotte Levy
Q108409338	Lmul	"Caroline Levy"
Q108409338	Len	"Caroline Levy"
Q108409338	Lnl	"Caroline Levy"
Q108409338	Amul	"Charlotte Levy"

# Q108409369  Merry|Mery Botellho  ->  Merry Botellho   + Mery Botellho
Q108409369	Lmul	"Merry Botellho"
Q108409369	Len	"Merry Botellho"
Q108409369	Lnl	"Merry Botellho"
Q108409369	Amul	"Mery Botellho"

# Q108409370  Pedro|Pieter Botellho  ->  Pedro Botellho   + Pieter Botellho
Q108409370	Lmul	"Pedro Botellho"
Q108409370	Len	"Pedro Botellho"
Q108409370	Lnl	"Pedro Botellho"
Q108409370	Amul	"Pieter Botellho"

# Q108409413  Per|Pehr Persson  ->  Per Persson   + Pehr Persson
Q108409413	Lmul	"Per Persson"
Q108409413	Len	"Per Persson"
Q108409413	Lnl	"Per Persson"
Q108409413	Amul	"Pehr Persson"

# Q108409417  Louisa|Lovisa Olofsdotter  ->  Louisa Olofsdotter   + Lovisa Olofsdotter
Q108409417	Lmul	"Louisa Olofsdotter"
Q108409417	Len	"Louisa Olofsdotter"
Q108409417	Lnl	"Louisa Olofsdotter"
Q108409417	Amul	"Lovisa Olofsdotter"

# Q108409559  Agatha|Agien Burghuysen  ->  Agatha Burghuysen   + Agien Burghuysen
Q108409559	Lmul	"Agatha Burghuysen"
Q108409559	Len	"Agatha Burghuysen"
Q108409559	Lnl	"Agatha Burghuysen"
Q108409559	Amul	"Agien Burghuysen"

# Q108409628  Jose|Joze Botellho  ->  Jose Botellho   + Joze Botellho
Q108409628	Lmul	"Jose Botellho"
Q108409628	Len	"Jose Botellho"
Q108409628	Lnl	"Jose Botellho"
Q108409628	Amul	"Joze Botellho"

# Q108409630  Magretha|Margretha Jones  ->  Magretha Jones   + Margretha Jones
Q108409630	Lmul	"Magretha Jones"
Q108409630	Len	"Magretha Jones"
Q108409630	Lnl	"Magretha Jones"
Q108409630	Amul	"Margretha Jones"

# Q108409792  Anne|Jeanne Françoise Galmiche  ->  Anne Françoise Galmiche   + Jeanne Françoise Galmiche
Q108409792	Lmul	"Anne Françoise Galmiche"
Q108409792	Len	"Anne Françoise Galmiche"
Q108409792	Lnl	"Anne Françoise Galmiche"
Q108409792	Amul	"Jeanne Françoise Galmiche"

# Q108409801  Dominique|Demenge Richard  ->  Dominique Richard   + Demenge Richard
Q108409801	Lmul	"Dominique Richard"
Q108409801	Len	"Dominique Richard"
Q108409801	Lnl	"Dominique Richard"
Q108409801	Amul	"Demenge Richard"

# Q108431724  Giovanna|Caterina de Lannoy  ->  Giovanna de Lannoy   + Caterina de Lannoy
Q108431724	Lmul	"Giovanna de Lannoy"
Q108431724	Len	"Giovanna de Lannoy"
Q108431724	Lnl	"Giovanna de Lannoy"
Q108431724	Amul	"Caterina de Lannoy"

# Q108432327  Jolande|Yolande de Barbancon, Dame de Montigny-le-Christophe  ->  Jolande de Barbancon, Dame de Montigny-le-Christophe   + Yolande de Barbancon, Dame de Montigny-le-Christophe
Q108432327	Len	"Jolande de Barbancon, Dame de Montigny-le-Christophe"
Q108432327	Lnl	"Jolande de Barbancon, Dame de Montigny-le-Christophe"
Q108432327	Amul	"Yolande de Barbancon, Dame de Montigny-le-Christophe"

# Q108654755  noble Domna|Daria Iakovlevna Toloshanova  ->  noble Domna Iakovlevna Toloshanova   + noble Daria Iakovlevna Toloshanova
Q108654755	Len	"noble Domna Iakovlevna Toloshanova"
Q108654755	Lnl	"noble Domna Iakovlevna Toloshanova"
Q108654755	Amul	"noble Daria Iakovlevna Toloshanova"

# Q108683868  John|Jenkin Bowles (Bowlay), of Penhow  ->  John Bowles (Bowlay), of Penhow   + Jenkin Bowles (Bowlay), of Penhow
Q108683868	Lmul	"John Bowles (Bowlay), of Penhow"
Q108683868	Len	"John Bowles (Bowlay), of Penhow"
Q108683868	Lnl	"John Bowles (Bowlay), of Penhow"
Q108683868	Amul	"Jenkin Bowles (Bowlay), of Penhow"

# Q108734092  Milles|Gui, Baron de Chandieu, Seigneur de Poules  ->  Milles Baron de Chandieu, Seigneur de Poules   + Gui, Baron de Chandieu, Seigneur de Poules
Q108734092	Lmul	"Milles Baron de Chandieu, Seigneur de Poules"
Q108734092	Len	"Milles Baron de Chandieu, Seigneur de Poules"
Q108734092	Lnl	"Milles Baron de Chandieu, Seigneur de Poules"
Q108734092	Amul	"Gui, Baron de Chandieu, Seigneur de Poules"

# Q108734168  Anne|Claudinee de Goumoëns  ->  Anne de Goumoëns   + Claudinee de Goumoëns
Q108734168	Lmul	"Anne de Goumoëns"
Q108734168	Len	"Anne de Goumoëns"
Q108734168	Lnl	"Anne de Goumoëns"
Q108734168	Amul	"Claudinee de Goumoëns"

# Q108742386  Hugues|Himbert de Bertonde  ->  Hugues de Bertonde   + Himbert de Bertonde
Q108742386	Lmul	"Hugues de Bertonde"
Q108742386	Len	"Hugues de Bertonde"
Q108742386	Lnl	"Hugues de Bertonde"
Q108742386	Amul	"Himbert de Bertonde"

# Q108743240  Léger|Lezer Mestrezat  ->  Léger Mestrezat   + Lezer Mestrezat
Q108743240	Lmul	"Léger Mestrezat"
Q108743240	Len	"Léger Mestrezat"
Q108743240	Lnl	"Léger Mestrezat"
Q108743240	Amul	"Lezer Mestrezat"

# Q108840453  Sir Adrian|Richard Molines (Molyns)  ->  Sir Adrian Molines (Molyns)   + Sir Richard Molines (Molyns)
Q108840453	Len	"Sir Adrian Molines (Molyns)"
Q108840453	Amul	"Sir Richard Molines (Molyns)"

# Q108840457  Anne|Jane Colpeper, of Bedsbury (Bedgebury)  ->  Anne Colpeper, of Bedsbury (Bedgebury)   + Jane Colpeper, of Bedsbury (Bedgebury)
Q108840457	Lmul	"Anne Colpeper, of Bedsbury (Bedgebury)"
Q108840457	Len	"Anne Colpeper, of Bedsbury (Bedgebury)"
Q108840457	Lnl	"Anne Colpeper, of Bedsbury (Bedgebury)"
Q108840457	Amul	"Jane Colpeper, of Bedsbury (Bedgebury)"

# Q108840659  Guntram|Güntheram Schenk zu Schweinsberg  ->  Guntram Schenk zu Schweinsberg   + Güntheram Schenk zu Schweinsberg
Q108840659	Lmul	"Guntram Schenk zu Schweinsberg"
Q108840659	Len	"Guntram Schenk zu Schweinsberg"
Q108840659	Lnl	"Guntram Schenk zu Schweinsberg"
Q108840659	Amul	"Güntheram Schenk zu Schweinsberg"

# Q108840662  Hermann|Mengot Schenck von Schweinsberg  ->  Hermann Schenck von Schweinsberg   + Mengot Schenck von Schweinsberg
Q108840662	Lmul	"Hermann Schenck von Schweinsberg"
Q108840662	Len	"Hermann Schenck von Schweinsberg"
Q108840662	Lnl	"Hermann Schenck von Schweinsberg"
Q108840662	Amul	"Mengot Schenck von Schweinsberg"

# Q108840664  Luckard|Lucia von Merlau gen. Böhm  ->  Luckard von Merlau gen. Böhm   + Lucia von Merlau gen. Böhm
Q108840664	Lmul	"Luckard von Merlau gen. Böhm"
Q108840664	Len	"Luckard von Merlau gen. Böhm"
Q108840664	Lnl	"Luckard von Merlau gen. Böhm"
Q108840664	Amul	"Lucia von Merlau gen. Böhm"

# Q108840666  Agnes|Nese von Virmond  ->  Agnes von Virmond   + Nese von Virmond
Q108840666	Lmul	"Agnes von Virmond"
Q108840666	Len	"Agnes von Virmond"
Q108840666	Lnl	"Agnes von Virmond"
Q108840666	Amul	"Nese von Virmond"

# Q108840667  Ambrosius|Brosecke von Viermynne (Virmond)  ->  Ambrosius von Viermynne (Virmond)   + Brosecke von Viermynne (Virmond)
Q108840667	Len	"Ambrosius von Viermynne (Virmond)"
Q108840667	Amul	"Brosecke von Viermynne (Virmond)"

# Q108840671  Else|Ilse Wais von Fauerbach  ->  Else Wais von Fauerbach   + Ilse Wais von Fauerbach
Q108840671	Lmul	"Else Wais von Fauerbach"
Q108840671	Len	"Else Wais von Fauerbach"
Q108840671	Lnl	"Else Wais von Fauerbach"
Q108840671	Amul	"Ilse Wais von Fauerbach"

# Q108840690  Weiprecht|Eberhard von Wolfskehl  ->  Weiprecht von Wolfskehl   + Eberhard von Wolfskehl
Q108840690	Lmul	"Weiprecht von Wolfskehl"
Q108840690	Len	"Weiprecht von Wolfskehl"
Q108840690	Lnl	"Weiprecht von Wolfskehl"
Q108840690	Amul	"Eberhard von Wolfskehl"

# Q108840708  Reinhard|Reiner von Schönrade  ->  Reinhard von Schönrade   + Reiner von Schönrade
Q108840708	Lmul	"Reinhard von Schönrade"
Q108840708	Len	"Reinhard von Schönrade"
Q108840708	Lnl	"Reinhard von Schönrade"
Q108840708	Amul	"Reiner von Schönrade"

# Q108840716  Johannes|Hans gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen  ->  Johannes gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen   + Hans gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen
Q108840716	Lmul	"Johannes gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen"
Q108840716	Len	"Johannes gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen"
Q108840716	Lnl	"Johannes gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen"
Q108840716	Amul	"Hans gen. Junghans von Dörnberg (Döringenberg), auf Frankenhausen"

# Q108841404  Ida A. Nordstrom|Peterson  ->  Ida A. Nordstrom   + Ida A. Peterson
Q108841404	Lmul	"Ida A. Nordstrom"
Q108841404	Len	"Ida A. Nordstrom"
Q108841404	Lnl	"Ida A. Nordstrom"
Q108841404	Amul	"Ida A. Peterson"

# Q108844603  Ellen|Eleanor Vincent  ->  Ellen Vincent   + Eleanor Vincent
Q108844603	Lmul	"Ellen Vincent"
Q108844603	Len	"Ellen Vincent"
Q108844603	Lnl	"Ellen Vincent"
Q108844603	Amul	"Eleanor Vincent"

# Q108912561  Helen|Eleanor Conyers  ->  Helen Conyers   + Eleanor Conyers
Q108912561	Lmul	"Helen Conyers"
Q108912561	Len	"Helen Conyers"
Q108912561	Lnl	"Helen Conyers"
Q108912561	Amul	"Eleanor Conyers"

# Q108912855  Joan|Cecily Sharpe  ->  Joan Sharpe   + Cecily Sharpe
Q108912855	Lmul	"Joan Sharpe"
Q108912855	Len	"Joan Sharpe"
Q108912855	Lnl	"Joan Sharpe"
Q108912855	Amul	"Cecily Sharpe"

# Q108912859  Joan|Janet Ffarington  ->  Joan Ffarington   + Janet Ffarington
Q108912859	Lmul	"Joan Ffarington"
Q108912859	Len	"Joan Ffarington"
Q108912859	Lnl	"Joan Ffarington"
Q108912859	Amul	"Janet Ffarington"

# Q108912865  Isabel|Elizabeth Langton, of Newton  ->  Isabel Langton, of Newton   + Elizabeth Langton, of Newton
Q108912865	Lmul	"Isabel Langton, of Newton"
Q108912865	Len	"Isabel Langton, of Newton"
Q108912865	Lnl	"Isabel Langton, of Newton"
Q108912865	Amul	"Elizabeth Langton, of Newton"

# Q108912911  Anne|Mary Scarisbrick  ->  Anne Scarisbrick   + Mary Scarisbrick
Q108912911	Lmul	"Anne Scarisbrick"
Q108912911	Len	"Anne Scarisbrick"
Q108912911	Lnl	"Anne Scarisbrick"
Q108912911	Amul	"Mary Scarisbrick"

# Q108912950  Maria Lanston|Langton  ->  Maria Lanston   + Maria Langton
Q108912950	Lmul	"Maria Lanston"
Q108912950	Len	"Maria Lanston"
Q108912950	Lnl	"Maria Lanston"
Q108912950	Amul	"Maria Langton"

# Q109010964  Madeleine|Jeanne de Vendôme, Dame d'Illiers  ->  Madeleine de Vendôme, Dame d'Illiers   + Jeanne de Vendôme, Dame d'Illiers
Q109010964	Len	"Madeleine de Vendôme, Dame d'Illiers"
Q109010964	Lnl	"Madeleine de Vendôme, Dame d'Illiers"
Q109010964	Amul	"Jeanne de Vendôme, Dame d'Illiers"

# Q109533594  Elisabeth|Elspeth|Jelna von Walsee  ->  Elisabeth von Walsee   + Elspeth von Walsee | Jelna von Walsee
Q109533594	Len	"Elisabeth von Walsee"
Q109533594	Lnl	"Elisabeth von Walsee"
Q109533594	Amul	"Elspeth von Walsee"
Q109533594	Amul	"Jelna von Walsee"

# Q109533826  Hans|Johann von Rammingen  ->  Hans von Rammingen   + Johann von Rammingen
Q109533826	Lmul	"Hans von Rammingen"
Q109533826	Len	"Hans von Rammingen"
Q109533826	Lnl	"Hans von Rammingen"
Q109533826	Amul	"Johann von Rammingen"

# Q109807804  Gast|Just von Polenz  ->  Gast von Polenz   + Just von Polenz
Q109807804	Len	"Gast von Polenz"
Q109807804	Lnl	"Gast von Polenz"
Q109807804	Amul	"Just von Polenz"

# Q109807834  Anna|Jutta von Hirschfeld (Hirsfelt) a.d.H. Otterwisch  ->  Anna von Hirschfeld (Hirsfelt) a.d.H. Otterwisch   + Jutta von Hirschfeld (Hirsfelt) a.d.H. Otterwisch
Q109807834	Len	"Anna von Hirschfeld (Hirsfelt) a.d.H. Otterwisch"
Q109807834	Amul	"Jutta von Hirschfeld (Hirsfelt) a.d.H. Otterwisch"

# Q109808001  Beatrijs|Béatrice van Duffel  ->  Beatrijs van Duffel   + Béatrice van Duffel
Q109808001	Lmul	"Beatrijs van Duffel"
Q109808001	Len	"Beatrijs van Duffel"
Q109808001	Lnl	"Beatrijs van Duffel"
Q109808001	Amul	"Béatrice van Duffel"

# Q109808012  Théodora|Thierrette de Cocq (Cock van Opynen) de Brueckom  ->  Théodora de Cocq (Cock van Opynen) de Brueckom   + Thierrette de Cocq (Cock van Opynen) de Brueckom
Q109808012	Len	"Théodora de Cocq (Cock van Opynen) de Brueckom"
Q109808012	Amul	"Thierrette de Cocq (Cock van Opynen) de Brueckom"

# Q109808168  Hildegond|Hildegarde von Hessen zu Diersfordt, Vrouwe van Diersfort  ->  Hildegond von Hessen zu Diersfordt, Vrouwe van Diersfort   + Hildegarde von Hessen zu Diersfordt, Vrouwe van Diersfort
Q109808168	Lmul	"Hildegond von Hessen zu Diersfordt, Vrouwe van Diersfort"
Q109808168	Len	"Hildegond von Hessen zu Diersfordt, Vrouwe van Diersfort"
Q109808168	Lnl	"Hildegond von Hessen zu Diersfordt, Vrouwe van Diersfort"
Q109808168	Amul	"Hildegarde von Hessen zu Diersfordt, Vrouwe van Diersfort"

# Q109808223  Maria|Anna von Oer zu Geist  ->  Maria von Oer zu Geist   + Anna von Oer zu Geist
Q109808223	Lmul	"Maria von Oer zu Geist"
Q109808223	Len	"Maria von Oer zu Geist"
Q109808223	Lnl	"Maria von Oer zu Geist"
Q109808223	Amul	"Anna von Oer zu Geist"

# Q109808400  Cunegonde|Kunigunde de Juppleu (Zuppleau), Heiress of Herlemont  ->  Cunegonde de Juppleu (Zuppleau), Heiress of Herlemont   + Kunigunde de Juppleu (Zuppleau), Heiress of Herlemont
Q109808400	Lmul	"Cunegonde de Juppleu (Zuppleau), Heiress of Herlemont"
Q109808400	Len	"Cunegonde de Juppleu (Zuppleau), Heiress of Herlemont"
Q109808400	Lnl	"Cunegonde de Juppleu (Zuppleau), Heiress of Herlemont"
Q109808400	Amul	"Kunigunde de Juppleu (Zuppleau), Heiress of Herlemont"

# Q109835751  Andreas 'Berneck' Holter|Holtte  ->  Andreas 'Berneck' Holter   + Andreas 'Berneck' Holtte
Q109835751	Len	"Andreas 'Berneck' Holter"
Q109835751	Lnl	"Andreas 'Berneck' Holter"
Q109835751	Amul	"Andreas 'Berneck' Holtte"

# Q109835762  Ellen|Lene Jorgensdatter Daa  ->  Ellen Jorgensdatter Daa   + Lene Jorgensdatter Daa
Q109835762	Len	"Ellen Jorgensdatter Daa"
Q109835762	Lnl	"Ellen Jorgensdatter Daa"
Q109835762	Amul	"Lene Jorgensdatter Daa"

# Q109835998  Arsle|Ursula  ->  Arsle   + Ursula
Q109835998	Lmul	"Arsle"
Q109835998	Len	"Arsle"
Q109835998	Lnl	"Arsle"
Q109835998	Amul	"Ursula"

# Q109852878  Margaret|Alice Bradfield  ->  Margaret Bradfield   + Alice Bradfield
Q109852878	Lmul	"Margaret Bradfield"
Q109852878	Len	"Margaret Bradfield"
Q109852878	Lnl	"Margaret Bradfield"
Q109852878	Amul	"Alice Bradfield"

# Q109852882  John|James Newport, of Pelham, Herts  ->  John Newport, of Pelham, Herts   + James Newport, of Pelham, Herts
Q109852882	Lmul	"John Newport, of Pelham, Herts"
Q109852882	Len	"John Newport, of Pelham, Herts"
Q109852882	Lnl	"John Newport, of Pelham, Herts"
Q109852882	Amul	"James Newport, of Pelham, Herts"

# Q109852883  Margaret|Margery Crawley  ->  Margaret Crawley   + Margery Crawley
Q109852883	Lmul	"Margaret Crawley"
Q109852883	Len	"Margaret Crawley"
Q109852883	Lnl	"Margaret Crawley"
Q109852883	Amul	"Margery Crawley"

# Q109852954  Katherine|Catherine de Drayton  ->  Katherine de Drayton   + Catherine de Drayton
Q109852954	Lmul	"Katherine de Drayton"
Q109852954	Len	"Katherine de Drayton"
Q109852954	Lnl	"Katherine de Drayton"
Q109852954	Amul	"Catherine de Drayton"

# Q109852969  Julian|Juliana de Bockland  ->  Julian de Bockland   + Juliana de Bockland
Q109852969	Lmul	"Julian de Bockland"
Q109852969	Len	"Julian de Bockland"
Q109852969	Lnl	"Julian de Bockland"
Q109852969	Amul	"Juliana de Bockland"

# Q110066771  Arnold|Ralph St.Leger, of Ulcombe  ->  Arnold St.Leger, of Ulcombe   + Ralph St.Leger, of Ulcombe
Q110066771	Len	"Arnold St.Leger, of Ulcombe"
Q110066771	Lnl	"Arnold St.Leger, of Ulcombe"
Q110066771	Amul	"Ralph St.Leger, of Ulcombe"

# Q110067007  Nicholas|Francis Waring  ->  Nicholas Waring   + Francis Waring
Q110067007	Lmul	"Nicholas Waring"
Q110067007	Len	"Nicholas Waring"
Q110067007	Lnl	"Nicholas Waring"
Q110067007	Amul	"Francis Waring"

# Q110067036  Jane|Joanna Dale  ->  Jane Dale   + Joanna Dale
Q110067036	Lmul	"Jane Dale"
Q110067036	Len	"Jane Dale"
Q110067036	Lnl	"Jane Dale"
Q110067036	Amul	"Joanna Dale"

# Q110067314  John|Thomas Dale  ->  John Dale   + Thomas Dale
Q110067314	Lmul	"John Dale"
Q110067314	Len	"John Dale"
Q110067314	Lnl	"John Dale"
Q110067314	Amul	"Thomas Dale"

# Q110067354  Jane|Joan Hill, of Buntingdale, Salop  ->  Jane Hill, of Buntingdale, Salop   + Joan Hill, of Buntingdale, Salop
Q110067354	Lmul	"Jane Hill, of Buntingdale, Salop"
Q110067354	Len	"Jane Hill, of Buntingdale, Salop"
Q110067354	Lnl	"Jane Hill, of Buntingdale, Salop"
Q110067354	Amul	"Joan Hill, of Buntingdale, Salop"

# Q110067497  Margaret|Mary Bromley  ->  Margaret Bromley   + Mary Bromley
Q110067497	Lmul	"Margaret Bromley"
Q110067497	Len	"Margaret Bromley"
Q110067497	Lnl	"Margaret Bromley"
Q110067497	Amul	"Mary Bromley"

# Q110067684  Randle|Raff ap Iorwerth Gôch ab Ednyfed ap Madog Broughton  ->  Randle ap Iorwerth Gôch ab Ednyfed ap Madog Broughton   + Raff ap Iorwerth Gôch ab Ednyfed ap Madog Broughton
Q110067684	Lmul	"Randle ap Iorwerth Gôch ab Ednyfed ap Madog Broughton"
Q110067684	Len	"Randle ap Iorwerth Gôch ab Ednyfed ap Madog Broughton"
Q110067684	Lnl	"Randle ap Iorwerth Gôch ab Ednyfed ap Madog Broughton"
Q110067684	Amul	"Raff ap Iorwerth Gôch ab Ednyfed ap Madog Broughton"

# Q110067686  Alice|Alswn Brereton, of Malpas  ->  Alice Brereton, of Malpas   + Alswn Brereton, of Malpas
Q110067686	Lmul	"Alice Brereton, of Malpas"
Q110067686	Len	"Alice Brereton, of Malpas"
Q110067686	Lnl	"Alice Brereton, of Malpas"
Q110067686	Amul	"Alswn Brereton, of Malpas"

# Q110067764  Teili|Deilu ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch  ->  Teili ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch   + Deilu ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch
Q110067764	Lmul	"Teili ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch"
Q110067764	Len	"Teili ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch"
Q110067764	Lnl	"Teili ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch"
Q110067764	Amul	"Deilu ferch Ieuan ap Madog Cyffin ap Madog Gôch of Meol Iwrch"

# Q110067821  Margred|Angharad ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig  ->  Margred ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig   + Angharad ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig
Q110067821	Lmul	"Margred ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig"
Q110067821	Len	"Margred ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig"
Q110067821	Lnl	"Margred ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig"
Q110067821	Amul	"Angharad ferch Robin ap Gruffudd ap Madog Pado ab Ednyfed Gôch ap Cynwrig"

# Q110103734  Bitter|Ritter II von Raesfeld, Herr zu Ostendorf  ->  Bitter II von Raesfeld, Herr zu Ostendorf   + Ritter II von Raesfeld, Herr zu Ostendorf
Q110103734	Lmul	"Bitter II von Raesfeld, Herr zu Ostendorf"
Q110103734	Len	"Bitter II von Raesfeld, Herr zu Ostendorf"
Q110103734	Lnl	"Bitter II von Raesfeld, Herr zu Ostendorf"
Q110103734	Amul	"Ritter II von Raesfeld, Herr zu Ostendorf"

# Q110110520  Benedicta|Ponzetta zu Solms-Burgsolms  ->  Benedicta zu Solms-Burgsolms   + Ponzetta zu Solms-Burgsolms
Q110110520	Len	"Benedicta zu Solms-Burgsolms"
Q110110520	Amul	"Ponzetta zu Solms-Burgsolms"

# Q110151258  Freiin Katharina|Helena von Sowinecz  ->  Freiin Katharina von Sowinecz   + Freiin Helena von Sowinecz
Q110151258	Len	"Freiin Katharina von Sowinecz"
Q110151258	Lnl	"Freiin Katharina von Sowinecz"
Q110151258	Amul	"Freiin Helena von Sowinecz"

# Q110152321  Ludolph|Ludolphus von Münchhausen  ->  Ludolph von Münchhausen   + Ludolphus von Münchhausen
Q110152321	Lmul	"Ludolph von Münchhausen"
Q110152321	Len	"Ludolph von Münchhausen"
Q110152321	Lnl	"Ludolph von Münchhausen"
Q110152321	Amul	"Ludolphus von Münchhausen"

# Q110152324  Johannes|Ioannes von Münchhausen  ->  Johannes von Münchhausen   + Ioannes von Münchhausen
Q110152324	Lmul	"Johannes von Münchhausen"
Q110152324	Len	"Johannes von Münchhausen"
Q110152324	Lnl	"Johannes von Münchhausen"
Q110152324	Amul	"Ioannes von Münchhausen"

# Q110152375  Eberhard|Jobst von Brandenstein auf Oppurg  ->  Eberhard von Brandenstein auf Oppurg   + Jobst von Brandenstein auf Oppurg
Q110152375	Lmul	"Eberhard von Brandenstein auf Oppurg"
Q110152375	Len	"Eberhard von Brandenstein auf Oppurg"
Q110152375	Lnl	"Eberhard von Brandenstein auf Oppurg"
Q110152375	Amul	"Jobst von Brandenstein auf Oppurg"

# Q110152399  Berta|Bertha  ->  Berta   + Bertha
Q110152399	Lmul	"Berta"
Q110152399	Len	"Berta"
Q110152399	Lnl	"Berta"
Q110152399	Amul	"Bertha"

# Q110152441  Wolf|Volf II Pogwisch  ->  Wolf II Pogwisch   + Volf II Pogwisch
Q110152441	Lmul	"Wolf II Pogwisch"
Q110152441	Len	"Wolf II Pogwisch"
Q110152441	Lnl	"Wolf II Pogwisch"
Q110152441	Amul	"Volf II Pogwisch"

# Q110152447  Heinrich|Henrik von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk  ->  Heinrich von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk   + Henrik von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk
Q110152447	Lmul	"Heinrich von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk"
Q110152447	Len	"Heinrich von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk"
Q110152447	Lnl	"Heinrich von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk"
Q110152447	Amul	"Henrik von Rantzau in Dame, Herr von Salzau, Neuhaus & Bülk"

# Q110152483  Anna|Ilsabe von der Lühe  ->  Anna von der Lühe   + Ilsabe von der Lühe
Q110152483	Lmul	"Anna von der Lühe"
Q110152483	Len	"Anna von der Lühe"
Q110152483	Lnl	"Anna von der Lühe"
Q110152483	Amul	"Ilsabe von der Lühe"

# Q110152597  Bartholomeus|Kaspar von Apfaltern  ->  Bartholomeus von Apfaltern   + Kaspar von Apfaltern
Q110152597	Len	"Bartholomeus von Apfaltern"
Q110152597	Lnl	"Bartholomeus von Apfaltern"
Q110152597	Amul	"Kaspar von Apfaltern"

# Q110152661  Dorothea|Johanna von Waldburg  ->  Dorothea von Waldburg   + Johanna von Waldburg
Q110152661	Len	"Dorothea von Waldburg"
Q110152661	Lnl	"Dorothea von Waldburg"
Q110152661	Amul	"Johanna von Waldburg"

# Q110152808  Helena|Helene von Albersdorf (Altersdorff)  ->  Helena von Albersdorf (Altersdorff)   + Helene von Albersdorf (Altersdorff)
Q110152808	Len	"Helena von Albersdorf (Altersdorff)"
Q110152808	Amul	"Helene von Albersdorf (Altersdorff)"

# Q110153421  Vilém|Wilhelm z Zierotin  ->  Vilém z Zierotin   + Wilhelm z Zierotin
Q110153421	Len	"Vilém z Zierotin"
Q110153421	Lnl	"Vilém z Zierotin"
Q110153421	Amul	"Wilhelm z Zierotin"

# Q110153465  Jeanne|Agnes de Halewyn  ->  Jeanne de Halewyn   + Agnes de Halewyn
Q110153465	Lmul	"Jeanne de Halewyn"
Q110153465	Len	"Jeanne de Halewyn"
Q110153465	Lnl	"Jeanne de Halewyn"
Q110153465	Amul	"Agnes de Halewyn"

# Q110153494  Caspar|Kaspar I von Promnitz in Lessendorf  ->  Caspar I von Promnitz in Lessendorf   + Kaspar I von Promnitz in Lessendorf
Q110153494	Lmul	"Caspar I von Promnitz in Lessendorf"
Q110153494	Len	"Caspar I von Promnitz in Lessendorf"
Q110153494	Lnl	"Caspar I von Promnitz in Lessendorf"
Q110153494	Amul	"Kaspar I von Promnitz in Lessendorf"

# Q110153560  Anseau|André de Joinville, Seigneur de Bonney  ->  Anseau de Joinville, Seigneur de Bonney   + André de Joinville, Seigneur de Bonney
Q110153560	Lmul	"Anseau de Joinville, Seigneur de Bonney"
Q110153560	Len	"Anseau de Joinville, Seigneur de Bonney"
Q110153560	Lnl	"Anseau de Joinville, Seigneur de Bonney"
Q110153560	Amul	"André de Joinville, Seigneur de Bonney"

# Q110153946  Graf Johann|Hans von Lupfen, Landgraf von Stühlingen  ->  Graf Johann von Lupfen, Landgraf von Stühlingen   + Graf Hans von Lupfen, Landgraf von Stühlingen
Q110153946	Len	"Graf Johann von Lupfen, Landgraf von Stühlingen"
Q110153946	Lnl	"Graf Johann von Lupfen, Landgraf von Stühlingen"
Q110153946	Amul	"Graf Hans von Lupfen, Landgraf von Stühlingen"

# Q110154000  Johann IV|Hanns von Eberstorf  ->  Johann IV von Eberstorf   + Johann Hanns von Eberstorf
Q110154000	Len	"Johann IV von Eberstorf"
Q110154000	Lnl	"Johann IV von Eberstorf"
Q110154000	Amul	"Johann Hanns von Eberstorf"

# Q110154005  Ehrentraub|Ehrentrudis von Puchheim  ->  Ehrentraub von Puchheim   + Ehrentrudis von Puchheim
Q110154005	Len	"Ehrentraub von Puchheim"
Q110154005	Lnl	"Ehrentraub von Puchheim"
Q110154005	Amul	"Ehrentrudis von Puchheim"

# Q110154028  Hinko|Heinrich, Herr von Wrbna auf Maidelberg  ->  Hinko Herr von Wrbna auf Maidelberg   + Heinrich, Herr von Wrbna auf Maidelberg
Q110154028	Len	"Hinko Herr von Wrbna auf Maidelberg"
Q110154028	Lnl	"Hinko Herr von Wrbna auf Maidelberg"
Q110154028	Amul	"Heinrich, Herr von Wrbna auf Maidelberg"

# Q110154082  Margery|Heyda von Detsch-Neukirch  ->  Margery von Detsch-Neukirch   + Heyda von Detsch-Neukirch
Q110154082	Len	"Margery von Detsch-Neukirch"
Q110154082	Lnl	"Margery von Detsch-Neukirch"
Q110154082	Amul	"Heyda von Detsch-Neukirch"

# Q110154112  Hans|Johann von Pottendorf, Herr zu Feistritz  ->  Hans von Pottendorf, Herr zu Feistritz   + Johann von Pottendorf, Herr zu Feistritz
Q110154112	Len	"Hans von Pottendorf, Herr zu Feistritz"
Q110154112	Lnl	"Hans von Pottendorf, Herr zu Feistritz"
Q110154112	Amul	"Johann von Pottendorf, Herr zu Feistritz"

# Q110154117  Elisabeth|Elsbeth von Walsee  ->  Elisabeth von Walsee   + Elsbeth von Walsee
Q110154117	Len	"Elisabeth von Walsee"
Q110154117	Lnl	"Elisabeth von Walsee"
Q110154117	Amul	"Elsbeth von Walsee"

# Q110154466  Heinrich|Albrecht von Brandenstein auf Oppurg, Herr auf Oppurg  ->  Heinrich von Brandenstein auf Oppurg, Herr auf Oppurg   + Albrecht von Brandenstein auf Oppurg, Herr auf Oppurg
Q110154466	Lmul	"Heinrich von Brandenstein auf Oppurg, Herr auf Oppurg"
Q110154466	Len	"Heinrich von Brandenstein auf Oppurg, Herr auf Oppurg"
Q110154466	Lnl	"Heinrich von Brandenstein auf Oppurg, Herr auf Oppurg"
Q110154466	Amul	"Albrecht von Brandenstein auf Oppurg, Herr auf Oppurg"

# Q110154472  Margarethe|Marta|Martha von Kauffungen  ->  Margarethe von Kauffungen   + Marta von Kauffungen | Martha von Kauffungen
Q110154472	Lmul	"Margarethe von Kauffungen"
Q110154472	Len	"Margarethe von Kauffungen"
Q110154472	Lnl	"Margarethe von Kauffungen"
Q110154472	Amul	"Marta von Kauffungen"
Q110154472	Amul	"Martha von Kauffungen"

# Q110154484  Dietrich|Ditericus von Münchhausen  ->  Dietrich von Münchhausen   + Ditericus von Münchhausen
Q110154484	Lmul	"Dietrich von Münchhausen"
Q110154484	Len	"Dietrich von Münchhausen"
Q110154484	Lnl	"Dietrich von Münchhausen"
Q110154484	Amul	"Ditericus von Münchhausen"

# Q110154602  Ludwig|Lutz VI von Wangenheim  ->  Ludwig VI von Wangenheim   + Lutz VI von Wangenheim
Q110154602	Lmul	"Ludwig VI von Wangenheim"
Q110154602	Len	"Ludwig VI von Wangenheim"
Q110154602	Lnl	"Ludwig VI von Wangenheim"
Q110154602	Amul	"Lutz VI von Wangenheim"

# Q110154604  Margarethe|Elisabeth von Schönberg  ->  Margarethe von Schönberg   + Elisabeth von Schönberg
Q110154604	Len	"Margarethe von Schönberg"
Q110154604	Lnl	"Margarethe von Schönberg"
Q110154604	Amul	"Elisabeth von Schönberg"

# Q110154760  Gräfin Valpurga|Walpurgis Slikova z Pasoun (von Schlick)  ->  Gräfin Valpurga Slikova z Pasoun (von Schlick)   + Gräfin Walpurgis Slikova z Pasoun (von Schlick)
Q110154760	Len	"Gräfin Valpurga Slikova z Pasoun (von Schlick)"
Q110154760	Amul	"Gräfin Walpurgis Slikova z Pasoun (von Schlick)"

# Q110248869  Jane|Joan Norton  ->  Jane Norton   + Joan Norton
Q110248869	Lmul	"Jane Norton"
Q110248869	Len	"Jane Norton"
Q110248869	Lnl	"Jane Norton"
Q110248869	Amul	"Joan Norton"

# Q110261762  Richard|Rikart XII (XIII) von Daun  ->  Richard XII (XIII) von Daun   + Rikart XII (XIII) von Daun
Q110261762	Len	"Richard XII (XIII) von Daun"
Q110261762	Amul	"Rikart XII (XIII) von Daun"

# Q110268777  Catherine|Mary Goodwin, of Winchendon  ->  Catherine Goodwin, of Winchendon   + Mary Goodwin, of Winchendon
Q110268777	Lmul	"Catherine Goodwin, of Winchendon"
Q110268777	Len	"Catherine Goodwin, of Winchendon"
Q110268777	Lnl	"Catherine Goodwin, of Winchendon"
Q110268777	Amul	"Mary Goodwin, of Winchendon"

# Q110278698  Anne|Amy Fermor (Farmer)  ->  Anne Fermor (Farmer)   + Amy Fermor (Farmer)
Q110278698	Lmul	"Anne Fermor (Farmer)"
Q110278698	Len	"Anne Fermor (Farmer)"
Q110278698	Amul	"Amy Fermor (Farmer)"

# Q110278713  Jane|Joan Raleigh  ->  Jane Raleigh   + Joan Raleigh
Q110278713	Lmul	"Jane Raleigh"
Q110278713	Len	"Jane Raleigh"
Q110278713	Amul	"Joan Raleigh"

# Q110290088  Agnes|Anne Curzon  ->  Agnes Curzon   + Anne Curzon
Q110290088	Lmul	"Agnes Curzon"
Q110290088	Len	"Agnes Curzon"
Q110290088	Amul	"Anne Curzon"

# Q110290406  Roger|Robin Holland  ->  Roger Holland   + Robin Holland
Q110290406	Lmul	"Roger Holland"
Q110290406	Len	"Roger Holland"
Q110290406	Amul	"Robin Holland"

# Q110302825  Trond Sigundson|Elgenbriktson  ->  Trond Sigundson   + Trond Elgenbriktson
Q110302825	Lmul	"Trond Sigundson"
Q110302825	Len	"Trond Sigundson"
Q110302825	Lnl	"Trond Sigundson"
Q110302825	Amul	"Trond Elgenbriktson"

# Q110303496  Else|Elisabeth|Gerdruta|Kerttu von Fersen  ->  Else von Fersen   + Elisabeth von Fersen | Gerdruta von Fersen | Kerttu von Fersen
Q110303496	Lmul	"Else von Fersen"
Q110303496	Len	"Else von Fersen"
Q110303496	Lnl	"Else von Fersen"
Q110303496	Amul	"Elisabeth von Fersen"
Q110303496	Amul	"Gerdruta von Fersen"
Q110303496	Amul	"Kerttu von Fersen"

# Q110313619  Gyrild|Gyrith Bengtsdotter, heiress of Heggetorp  ->  Gyrild Bengtsdotter, heiress of Heggetorp   + Gyrith Bengtsdotter, heiress of Heggetorp
Q110313619	Lmul	"Gyrild Bengtsdotter, heiress of Heggetorp"
Q110313619	Len	"Gyrild Bengtsdotter, heiress of Heggetorp"
Q110313619	Lnl	"Gyrild Bengtsdotter, heiress of Heggetorp"
Q110313619	Amul	"Gyrith Bengtsdotter, heiress of Heggetorp"

# Q110313930  Adriane|Anne de Halewyn  ->  Adriane de Halewyn   + Anne de Halewyn
Q110313930	Len	"Adriane de Halewyn"
Q110313930	Lnl	"Adriane de Halewyn"
Q110313930	Amul	"Anne de Halewyn"

# Q110314401  Katherine|Catherine Leeke  ->  Katherine Leeke   + Catherine Leeke
Q110314401	Lmul	"Katherine Leeke"
Q110314401	Len	"Katherine Leeke"
Q110314401	Lnl	"Katherine Leeke"
Q110314401	Amul	"Catherine Leeke"

# Q110315105  Marguerite|Béatrix de Bruyères  ->  Marguerite de Bruyères   + Béatrix de Bruyères
Q110315105	Len	"Marguerite de Bruyères"
Q110315105	Lnl	"Marguerite de Bruyères"
Q110315105	Amul	"Béatrix de Bruyères"

# Q110315246  Sébille|Clémence d'Aulnays  ->  Sébille d'Aulnays   + Clémence d'Aulnays
Q110315246	Lmul	"Sébille d'Aulnays"
Q110315246	Len	"Sébille d'Aulnays"
Q110315246	Lnl	"Sébille d'Aulnays"
Q110315246	Amul	"Clémence d'Aulnays"

# Q110315413  Sir Hamon|Hammon Whichcote, of Harpswell  ->  Sir Hamon Whichcote, of Harpswell   + Sir Hammon Whichcote, of Harpswell
Q110315413	Lmul	"Sir Hamon Whichcote, of Harpswell"
Q110315413	Len	"Sir Hamon Whichcote, of Harpswell"
Q110315413	Lnl	"Sir Hamon Whichcote, of Harpswell"
Q110315413	Amul	"Sir Hammon Whichcote, of Harpswell"

# Q110315489  Alice|Isabel Snawsell  ->  Alice Snawsell   + Isabel Snawsell
Q110315489	Lmul	"Alice Snawsell"
Q110315489	Len	"Alice Snawsell"
Q110315489	Lnl	"Alice Snawsell"
Q110315489	Amul	"Isabel Snawsell"

# Q110315534  Robert|William Hingeston (Hyndeston), of Wonwell, Devon  ->  Robert Hingeston (Hyndeston), of Wonwell, Devon   + William Hingeston (Hyndeston), of Wonwell, Devon
Q110315534	Lmul	"Robert Hingeston (Hyndeston), of Wonwell, Devon"
Q110315534	Len	"Robert Hingeston (Hyndeston), of Wonwell, Devon"
Q110315534	Lnl	"Robert Hingeston (Hyndeston), of Wonwell, Devon"
Q110315534	Amul	"William Hingeston (Hyndeston), of Wonwell, Devon"

# Q110315679  Sir Adam|Alan Esse, of Thewborough  ->  Sir Adam Esse, of Thewborough   + Sir Alan Esse, of Thewborough
Q110315679	Lmul	"Sir Adam Esse, of Thewborough"
Q110315679	Len	"Sir Adam Esse, of Thewborough"
Q110315679	Lnl	"Sir Adam Esse, of Thewborough"
Q110315679	Amul	"Sir Alan Esse, of Thewborough"

# Q110315689  Reginold|Reginald FitzNichol  ->  Reginold FitzNichol   + Reginald FitzNichol
Q110315689	Lmul	"Reginold FitzNichol"
Q110315689	Len	"Reginold FitzNichol"
Q110315689	Lnl	"Reginold FitzNichol"
Q110315689	Amul	"Reginald FitzNichol"

# Q110315691  Jone|Joanna  ->  Jone   + Joanna
Q110315691	Lmul	"Jone"
Q110315691	Len	"Jone"
Q110315691	Lnl	"Jone"
Q110315691	Amul	"Joanna"

# Q110315692  Margaret|Margery  ->  Margaret   + Margery
Q110315692	Lmul	"Margaret"
Q110315692	Len	"Margaret"
Q110315692	Lnl	"Margaret"
Q110315692	Amul	"Margery"

# Q110315706  Thomasin|Thomasine Cruse (Cruuwys)  ->  Thomasin Cruse (Cruuwys)   + Thomasine Cruse (Cruuwys)
Q110315706	Len	"Thomasin Cruse (Cruuwys)"
Q110315706	Amul	"Thomasine Cruse (Cruuwys)"

# Q110315763  Anne|Joanna Holway  ->  Anne Holway   + Joanna Holway
Q110315763	Lmul	"Anne Holway"
Q110315763	Len	"Anne Holway"
Q110315763	Lnl	"Anne Holway"
Q110315763	Amul	"Joanna Holway"

# Q110315775  Elinor|Joan|Jane Reynell  ->  Elinor Reynell   + Joan Reynell | Jane Reynell
Q110315775	Lmul	"Elinor Reynell"
Q110315775	Len	"Elinor Reynell"
Q110315775	Lnl	"Elinor Reynell"
Q110315775	Amul	"Joan Reynell"
Q110315775	Amul	"Jane Reynell"

# Q110324663  Conrad Hofmeister|Kornmann  ->  Conrad Hofmeister   + Conrad Kornmann
Q110324663	Lmul	"Conrad Hofmeister"
Q110324663	Len	"Conrad Hofmeister"
Q110324663	Lnl	"Conrad Hofmeister"
Q110324663	Amul	"Conrad Kornmann"

# Q110324807  Börries|Liborius von Münchhausen, Herr von Apelern  ->  Börries von Münchhausen, Herr von Apelern   + Liborius von Münchhausen, Herr von Apelern
Q110324807	Lmul	"Börries von Münchhausen, Herr von Apelern"
Q110324807	Len	"Börries von Münchhausen, Herr von Apelern"
Q110324807	Lnl	"Börries von Münchhausen, Herr von Apelern"
Q110324807	Amul	"Liborius von Münchhausen, Herr von Apelern"

# Q110324873  Statius|Iustatius III von Münchhausen  ->  Statius III von Münchhausen   + Iustatius III von Münchhausen
Q110324873	Lmul	"Statius III von Münchhausen"
Q110324873	Len	"Statius III von Münchhausen"
Q110324873	Lnl	"Statius III von Münchhausen"
Q110324873	Amul	"Iustatius III von Münchhausen"

# Q110324994  Kurt|Konrad von Viermynne (Virmond), Pfandherr zu Medebach  ->  Kurt von Viermynne (Virmond), Pfandherr zu Medebach   + Konrad von Viermynne (Virmond), Pfandherr zu Medebach
Q110324994	Lmul	"Kurt von Viermynne (Virmond), Pfandherr zu Medebach"
Q110324994	Len	"Kurt von Viermynne (Virmond), Pfandherr zu Medebach"
Q110324994	Lnl	"Kurt von Viermynne (Virmond), Pfandherr zu Medebach"
Q110324994	Amul	"Konrad von Viermynne (Virmond), Pfandherr zu Medebach"

# Q110325426  Mechtild|Elisabeth von Mandelsloh  ->  Mechtild von Mandelsloh   + Elisabeth von Mandelsloh
Q110325426	Lmul	"Mechtild von Mandelsloh"
Q110325426	Len	"Mechtild von Mandelsloh"
Q110325426	Lnl	"Mechtild von Mandelsloh"
Q110325426	Amul	"Elisabeth von Mandelsloh"

# Q110325528  Beate|Agnes von Löser a.d.H. Pretzsch  ->  Beate von Löser a.d.H. Pretzsch   + Agnes von Löser a.d.H. Pretzsch
Q110325528	Lmul	"Beate von Löser a.d.H. Pretzsch"
Q110325528	Len	"Beate von Löser a.d.H. Pretzsch"
Q110325528	Lnl	"Beate von Löser a.d.H. Pretzsch"
Q110325528	Amul	"Agnes von Löser a.d.H. Pretzsch"

# Q110325544  Elisabeth|Anna Pflug  ->  Elisabeth Pflug   + Anna Pflug
Q110325544	Lmul	"Elisabeth Pflug"
Q110325544	Len	"Elisabeth Pflug"
Q110325544	Lnl	"Elisabeth Pflug"
Q110325544	Amul	"Anna Pflug"

# Q110325552  Elisabeth|Ilse von Schleinitz  ->  Elisabeth von Schleinitz   + Ilse von Schleinitz
Q110325552	Len	"Elisabeth von Schleinitz"
Q110325552	Lnl	"Elisabeth von Schleinitz"
Q110325552	Amul	"Ilse von Schleinitz"

# Q110325704  Burchard|Busso von Querfurt  ->  Burchard von Querfurt   + Busso von Querfurt
Q110325704	Lmul	"Burchard von Querfurt"
Q110325704	Len	"Burchard von Querfurt"
Q110325704	Lnl	"Burchard von Querfurt"
Q110325704	Amul	"Busso von Querfurt"

# Q110325895  Lencke|Elseke von Münchhausen  ->  Lencke von Münchhausen   + Elseke von Münchhausen
Q110325895	Lmul	"Lencke von Münchhausen"
Q110325895	Len	"Lencke von Münchhausen"
Q110325895	Lnl	"Lencke von Münchhausen"
Q110325895	Amul	"Elseke von Münchhausen"

# Q110326028  Elisabeth|Lutrud von Plesse  ->  Elisabeth von Plesse   + Lutrud von Plesse
Q110326028	Lmul	"Elisabeth von Plesse"
Q110326028	Len	"Elisabeth von Plesse"
Q110326028	Lnl	"Elisabeth von Plesse"
Q110326028	Amul	"Lutrud von Plesse"

# Q110326393  Steben|Stephan II von der Malsburg  ->  Steben II von der Malsburg   + Stephan II von der Malsburg
Q110326393	Lmul	"Steben II von der Malsburg"
Q110326393	Len	"Steben II von der Malsburg"
Q110326393	Lnl	"Steben II von der Malsburg"
Q110326393	Amul	"Stephan II von der Malsburg"

# Q110326556  Elisabeth|Bele von Bartensleben  ->  Elisabeth von Bartensleben   + Bele von Bartensleben
Q110326556	Lmul	"Elisabeth von Bartensleben"
Q110326556	Len	"Elisabeth von Bartensleben"
Q110326556	Lnl	"Elisabeth von Bartensleben"
Q110326556	Amul	"Bele von Bartensleben"

# Q110328200  Marie|Marguerite de Boiselve  ->  Marie de Boiselve   + Marguerite de Boiselve
Q110328200	Lmul	"Marie de Boiselve"
Q110328200	Len	"Marie de Boiselve"
Q110328200	Lnl	"Marie de Boiselve"
Q110328200	Amul	"Marguerite de Boiselve"

# Q110332061  Agnes|Annes Playford  ->  Agnes Playford   + Annes Playford
Q110332061	Lmul	"Agnes Playford"
Q110332061	Len	"Agnes Playford"
Q110332061	Lnl	"Agnes Playford"
Q110332061	Amul	"Annes Playford"

# Q110332098  Francis|Alanus Calibut (Calybutt), of Castle Acre, Norfolk  ->  Francis Calibut (Calybutt), of Castle Acre, Norfolk   + Alanus Calibut (Calybutt), of Castle Acre, Norfolk
Q110332098	Lmul	"Francis Calibut (Calybutt), of Castle Acre, Norfolk"
Q110332098	Len	"Francis Calibut (Calybutt), of Castle Acre, Norfolk"
Q110332098	Lnl	"Francis Calibut (Calybutt), of Castle Acre, Norfolk"
Q110332098	Amul	"Alanus Calibut (Calybutt), of Castle Acre, Norfolk"

# Q110332162  Audrey|Ethelreda Hare, of Bruisyard  ->  Audrey Hare, of Bruisyard   + Ethelreda Hare, of Bruisyard
Q110332162	Lmul	"Audrey Hare, of Bruisyard"
Q110332162	Len	"Audrey Hare, of Bruisyard"
Q110332162	Lnl	"Audrey Hare, of Bruisyard"
Q110332162	Amul	"Ethelreda Hare, of Bruisyard"

# Q110332307  Margaret|Margery Sackville, of Fawley  ->  Margaret Sackville, of Fawley   + Margery Sackville, of Fawley
Q110332307	Lmul	"Margaret Sackville, of Fawley"
Q110332307	Len	"Margaret Sackville, of Fawley"
Q110332307	Lnl	"Margaret Sackville, of Fawley"
Q110332307	Amul	"Margery Sackville, of Fawley"

# Q110332336  John|Jenkin Walbyf (Walbeoffe), of Llanhamlech  ->  John Walbyf (Walbeoffe), of Llanhamlech   + Jenkin Walbyf (Walbeoffe), of Llanhamlech
Q110332336	Lmul	"John Walbyf (Walbeoffe), of Llanhamlech"
Q110332336	Len	"John Walbyf (Walbeoffe), of Llanhamlech"
Q110332336	Lnl	"John Walbyf (Walbeoffe), of Llanhamlech"
Q110332336	Amul	"Jenkin Walbyf (Walbeoffe), of Llanhamlech"

# Q110332337  Jane|Jonet Gunter  ->  Jane Gunter   + Jonet Gunter
Q110332337	Lmul	"Jane Gunter"
Q110332337	Len	"Jane Gunter"
Q110332337	Lnl	"Jane Gunter"
Q110332337	Amul	"Jonet Gunter"

# Q110332353  Stephen|Lawrence Guybon  ->  Stephen Guybon   + Lawrence Guybon
Q110332353	Lmul	"Stephen Guybon"
Q110332353	Len	"Stephen Guybon"
Q110332353	Lnl	"Stephen Guybon"
Q110332353	Amul	"Lawrence Guybon"

# Q110332388  Helene|Ella|Elizabeth Audley  ->  Helene Audley   + Ella Audley | Elizabeth Audley
Q110332388	Lmul	"Helene Audley"
Q110332388	Len	"Helene Audley"
Q110332388	Lnl	"Helene Audley"
Q110332388	Amul	"Ella Audley"
Q110332388	Amul	"Elizabeth Audley"

# Q110332898  Margaret|Margery Upton  ->  Margaret Upton   + Margery Upton
Q110332898	Lmul	"Margaret Upton"
Q110332898	Len	"Margaret Upton"
Q110332898	Lnl	"Margaret Upton"
Q110332898	Amul	"Margery Upton"

# Q110332910  Jennet|Janet Dawe  ->  Jennet Dawe   + Janet Dawe
Q110332910	Lmul	"Jennet Dawe"
Q110332910	Len	"Jennet Dawe"
Q110332910	Lnl	"Jennet Dawe"
Q110332910	Amul	"Janet Dawe"

# Q110332912  Johanna|Jane Reskymer  ->  Johanna Reskymer   + Jane Reskymer
Q110332912	Lmul	"Johanna Reskymer"
Q110332912	Len	"Johanna Reskymer"
Q110332912	Lnl	"Johanna Reskymer"
Q110332912	Amul	"Jane Reskymer"

# Q110332962  Margaret|Agnes Yonge  ->  Margaret Yonge   + Agnes Yonge
Q110332962	Len	"Margaret Yonge"
Q110332962	Lnl	"Margaret Yonge"
Q110332962	Amul	"Agnes Yonge"

# Q110333014  Wenllyan|Joan Osborne, of London  ->  Wenllyan Osborne, of London   + Joan Osborne, of London
Q110333014	Lmul	"Wenllyan Osborne, of London"
Q110333014	Len	"Wenllyan Osborne, of London"
Q110333014	Lnl	"Wenllyan Osborne, of London"
Q110333014	Amul	"Joan Osborne, of London"

# Q110347026  Robert|Roger Breynton  ->  Robert Breynton   + Roger Breynton
Q110347026	Lmul	"Robert Breynton"
Q110347026	Len	"Robert Breynton"
Q110347026	Lnl	"Robert Breynton"
Q110347026	Amul	"Roger Breynton"

# Q110347323  Henriette|Marguerite du Chastel  ->  Henriette du Chastel   + Marguerite du Chastel
Q110347323	Lmul	"Henriette du Chastel"
Q110347323	Len	"Henriette du Chastel"
Q110347323	Lnl	"Henriette du Chastel"
Q110347323	Amul	"Marguerite du Chastel"

# Q110347435  Aliette|Alix de Launay, dame de Coëtquenan  ->  Aliette de Launay, dame de Coëtquenan   + Alix de Launay, dame de Coëtquenan
Q110347435	Lmul	"Aliette de Launay, dame de Coëtquenan"
Q110347435	Len	"Aliette de Launay, dame de Coëtquenan"
Q110347435	Lnl	"Aliette de Launay, dame de Coëtquenan"
Q110347435	Amul	"Alix de Launay, dame de Coëtquenan"

# Q110352771  Clara Ottolina|Johanna van der Hoop  ->  Clara Ottolina van der Hoop   + Clara Johanna van der Hoop
Q110352771	Lmul	"Clara Ottolina van der Hoop"
Q110352771	Len	"Clara Ottolina van der Hoop"
Q110352771	Lnl	"Clara Ottolina van der Hoop"
Q110352771	Amul	"Clara Johanna van der Hoop"

# Q110352836  Willemina|Wilhelmina Crouwel  ->  Willemina Crouwel   + Wilhelmina Crouwel
Q110352836	Lmul	"Willemina Crouwel"
Q110352836	Len	"Willemina Crouwel"
Q110352836	Lnl	"Willemina Crouwel"
Q110352836	Amul	"Wilhelmina Crouwel"

# Q110353062  Arend|Arij van den Berg  ->  Arend van den Berg   + Arij van den Berg
Q110353062	Lmul	"Arend van den Berg"
Q110353062	Len	"Arend van den Berg"
Q110353062	Lnl	"Arend van den Berg"
Q110353062	Amul	"Arij van den Berg"

# Q110354353  Elsebe|Elizabeth Hagens  ->  Elsebe Hagens   + Elizabeth Hagens
Q110354353	Lmul	"Elsebe Hagens"
Q110354353	Len	"Elsebe Hagens"
Q110354353	Lnl	"Elsebe Hagens"
Q110354353	Amul	"Elizabeth Hagens"

# Q110354375  Ame|Aam|Arne Pieters Borgman  ->  Ame Pieters Borgman   + Aam Pieters Borgman | Arne Pieters Borgman
Q110354375	Lmul	"Ame Pieters Borgman"
Q110354375	Len	"Ame Pieters Borgman"
Q110354375	Lnl	"Ame Pieters Borgman"
Q110354375	Amul	"Aam Pieters Borgman"
Q110354375	Amul	"Arne Pieters Borgman"

# Q110354495  Aise|Eisso Muntinga  ->  Aise Muntinga   + Eisso Muntinga
Q110354495	Len	"Aise Muntinga"
Q110354495	Amul	"Eisso Muntinga"

# Q110354507  Ida|Alida de Boer  ->  Ida de Boer   + Alida de Boer
Q110354507	Lmul	"Ida de Boer"
Q110354507	Len	"Ida de Boer"
Q110354507	Lnl	"Ida de Boer"
Q110354507	Amul	"Alida de Boer"

# Q110354569  Johanna|Anna|Anneke van Hoften  ->  Johanna van Hoften   + Anna van Hoften | Anneke van Hoften
Q110354569	Lmul	"Johanna van Hoften"
Q110354569	Len	"Johanna van Hoften"
Q110354569	Lnl	"Johanna van Hoften"
Q110354569	Amul	"Anna van Hoften"
Q110354569	Amul	"Anneke van Hoften"

# Q110354805  Vaes|Servaes Panhuys, of van Limbourg  ->  Vaes Panhuys, of van Limbourg   + Servaes Panhuys, of van Limbourg
Q110354805	Lmul	"Vaes Panhuys, of van Limbourg"
Q110354805	Len	"Vaes Panhuys, of van Limbourg"
Q110354805	Lnl	"Vaes Panhuys, of van Limbourg"
Q110354805	Amul	"Servaes Panhuys, of van Limbourg"

# Q110354806  Johan|Jehan Vaes Panhuys  ->  Johan Vaes Panhuys   + Jehan Vaes Panhuys
Q110354806	Lmul	"Johan Vaes Panhuys"
Q110354806	Len	"Johan Vaes Panhuys"
Q110354806	Lnl	"Johan Vaes Panhuys"
Q110354806	Amul	"Jehan Vaes Panhuys"

# Q110354815  Jehenne|Johanna du Bois  ->  Jehenne du Bois   + Johanna du Bois
Q110354815	Lmul	"Jehenne du Bois"
Q110354815	Len	"Jehenne du Bois"
Q110354815	Lnl	"Jehenne du Bois"
Q110354815	Amul	"Johanna du Bois"

# Q110362967  István|Stephen Sulyok de Leksce  ->  István Sulyok de Leksce   + Stephen Sulyok de Leksce
Q110362967	Lmul	"István Sulyok de Leksce"
Q110362967	Len	"István Sulyok de Leksce"
Q110362967	Lnl	"István Sulyok de Leksce"
Q110362967	Amul	"Stephen Sulyok de Leksce"

# Q110362970  Klara|Clara Kende de Kölcse  ->  Klara Kende de Kölcse   + Clara Kende de Kölcse
Q110362970	Lmul	"Klara Kende de Kölcse"
Q110362970	Len	"Klara Kende de Kölcse"
Q110362970	Lnl	"Klara Kende de Kölcse"
Q110362970	Amul	"Clara Kende de Kölcse"

# Q110363095  noble Ladislau|Vlad Dracula de Sintesti, (Lászlá Drakulya de Semtheest)  ->  noble Ladislau Dracula de Sintesti, (Lászlá Drakulya de Semtheest)   + noble Vlad Dracula de Sintesti, (Lászlá Drakulya de Semtheest)
Q110363095	Lmul	"noble Ladislau Dracula de Sintesti, (Lászlá Drakulya de Semtheest)"
Q110363095	Len	"noble Ladislau Dracula de Sintesti, (Lászlá Drakulya de Semtheest)"
Q110363095	Lnl	"noble Ladislau Dracula de Sintesti, (Lászlá Drakulya de Semtheest)"
Q110363095	Amul	"noble Vlad Dracula de Sintesti, (Lászlá Drakulya de Semtheest)"

# Q110363211  Stefan|István Bagdy de Basarág  ->  Stefan Bagdy de Basarág   + István Bagdy de Basarág
Q110363211	Lmul	"Stefan Bagdy de Basarág"
Q110363211	Len	"Stefan Bagdy de Basarág"
Q110363211	Lnl	"Stefan Bagdy de Basarág"
Q110363211	Amul	"István Bagdy de Basarág"

# Q110363333  Helene|Ilona Haranglábi  ->  Helene Haranglábi   + Ilona Haranglábi
Q110363333	Lmul	"Helene Haranglábi"
Q110363333	Len	"Helene Haranglábi"
Q110363333	Lnl	"Helene Haranglábi"
Q110363333	Amul	"Ilona Haranglábi"

# Q110366823  Jitka|Brigitta von Landstein  ->  Jitka von Landstein   + Brigitta von Landstein
Q110366823	Len	"Jitka von Landstein"
Q110366823	Lnl	"Jitka von Landstein"
Q110366823	Amul	"Brigitta von Landstein"

# Q110366899  Hartnid|Hartold V von Pettau zu Friedau, Marschall von Steiermark  ->  Hartnid V von Pettau zu Friedau, Marschall von Steiermark   + Hartold V von Pettau zu Friedau, Marschall von Steiermark
Q110366899	Len	"Hartnid V von Pettau zu Friedau, Marschall von Steiermark"
Q110366899	Lnl	"Hartnid V von Pettau zu Friedau, Marschall von Steiermark"
Q110366899	Amul	"Hartold V von Pettau zu Friedau, Marschall von Steiermark"

# Q110366916  Antonio|Anton II, Conte d'Arco  ->  Antonio II, Conte d'Arco   + Anton II, Conte d'Arco
Q110366916	Len	"Antonio II, Conte d'Arco"
Q110366916	Lnl	"Antonio II, Conte d'Arco"
Q110366916	Amul	"Anton II, Conte d'Arco"

# Q110366961  Peter|Petrein von Eberstorf  ->  Peter von Eberstorf   + Petrein von Eberstorf
Q110366961	Len	"Peter von Eberstorf"
Q110366961	Lnl	"Peter von Eberstorf"
Q110366961	Amul	"Petrein von Eberstorf"

# Q110367234  Kata|Katalin  ->  Kata   + Katalin
Q110367234	Len	"Kata"
Q110367234	Lnl	"Kata"
Q110367234	Amul	"Katalin"

# Q110369185  Yolande|Violante de Bueil  ->  Yolande de Bueil   + Violante de Bueil
Q110369185	Lmul	"Yolande de Bueil"
Q110369185	Len	"Yolande de Bueil"
Q110369185	Lnl	"Yolande de Bueil"
Q110369185	Amul	"Violante de Bueil"

# Q110369420  Helena|Ilona Thoroczkay de Thoroczkó-, Szent-György  ->  Helena Thoroczkay de Thoroczkó-, Szent-György   + Ilona Thoroczkay de Thoroczkó-, Szent-György
Q110369420	Len	"Helena Thoroczkay de Thoroczkó-, Szent-György"
Q110369420	Lnl	"Helena Thoroczkay de Thoroczkó-, Szent-György"
Q110369420	Amul	"Ilona Thoroczkay de Thoroczkó-, Szent-György"

# Q110370342  Jeanne|Antoinette de La Baume, Comtesse de Montrevel  ->  Jeanne de La Baume, Comtesse de Montrevel   + Antoinette de La Baume, Comtesse de Montrevel
Q110370342	Len	"Jeanne de La Baume, Comtesse de Montrevel"
Q110370342	Lnl	"Jeanne de La Baume, Comtesse de Montrevel"
Q110370342	Amul	"Antoinette de La Baume, Comtesse de Montrevel"

# Q110378161  Luitgarde|Leukard, Gräfin von Zollern, Burgräfin von Nürnberg  ->  Luitgarde Gräfin von Zollern, Burgräfin von Nürnberg   + Leukard, Gräfin von Zollern, Burgräfin von Nürnberg
Q110378161	Lmul	"Luitgarde Gräfin von Zollern, Burgräfin von Nürnberg"
Q110378161	Len	"Luitgarde Gräfin von Zollern, Burgräfin von Nürnberg"
Q110378161	Lnl	"Luitgarde Gräfin von Zollern, Burgräfin von Nürnberg"
Q110378161	Amul	"Leukard, Gräfin von Zollern, Burgräfin von Nürnberg"

# Q110378504  Archibald|Andrew Sibbald, of Rankeilour  ->  Archibald Sibbald, of Rankeilour   + Andrew Sibbald, of Rankeilour
Q110378504	Lmul	"Archibald Sibbald, of Rankeilour"
Q110378504	Len	"Archibald Sibbald, of Rankeilour"
Q110378504	Lnl	"Archibald Sibbald, of Rankeilour"
Q110378504	Amul	"Andrew Sibbald, of Rankeilour"

# Q110378546  Margaret|Marjory Stewart, of Innermeath  ->  Margaret Stewart, of Innermeath   + Marjory Stewart, of Innermeath
Q110378546	Lmul	"Margaret Stewart, of Innermeath"
Q110378546	Len	"Margaret Stewart, of Innermeath"
Q110378546	Lnl	"Margaret Stewart, of Innermeath"
Q110378546	Amul	"Marjory Stewart, of Innermeath"

# Q110378859  Hanault|Hamiltone McLeod, of Harris  ->  Hanault McLeod, of Harris   + Hamiltone McLeod, of Harris
Q110378859	Lmul	"Hanault McLeod, of Harris"
Q110378859	Len	"Hanault McLeod, of Harris"
Q110378859	Lnl	"Hanault McLeod, of Harris"
Q110378859	Amul	"Hamiltone McLeod, of Harris"

# Q110379158  Andrew|Alexander Jardine (Jardyne)  ->  Andrew Jardine (Jardyne)   + Alexander Jardine (Jardyne)
Q110379158	Len	"Andrew Jardine (Jardyne)"
Q110379158	Amul	"Alexander Jardine (Jardyne)"

# Q110381117  Hüe|Hugues du Moulin  ->  Hüe du Moulin   + Hugues du Moulin
Q110381117	Lmul	"Hüe du Moulin"
Q110381117	Len	"Hüe du Moulin"
Q110381117	Lnl	"Hüe du Moulin"
Q110381117	Amul	"Hugues du Moulin"

# Q110381272  Marguerite|Isabeau Boursette  ->  Marguerite Boursette   + Isabeau Boursette
Q110381272	Lmul	"Marguerite Boursette"
Q110381272	Len	"Marguerite Boursette"
Q110381272	Lnl	"Marguerite Boursette"
Q110381272	Amul	"Isabeau Boursette"

# Q110381295  Renaud|Antoine de Haveskerke, Seigneur de Basse  ->  Renaud de Haveskerke, Seigneur de Basse   + Antoine de Haveskerke, Seigneur de Basse
Q110381295	Lmul	"Renaud de Haveskerke, Seigneur de Basse"
Q110381295	Len	"Renaud de Haveskerke, Seigneur de Basse"
Q110381295	Lnl	"Renaud de Haveskerke, Seigneur de Basse"
Q110381295	Amul	"Antoine de Haveskerke, Seigneur de Basse"

# Q110381301  Maria|Marguerite van Beveren, Vrouwe van Diksmuide, Watou, Jumelles  ->  Maria van Beveren, Vrouwe van Diksmuide, Watou, Jumelles   + Marguerite van Beveren, Vrouwe van Diksmuide, Watou, Jumelles
Q110381301	Lmul	"Maria van Beveren, Vrouwe van Diksmuide, Watou, Jumelles"
Q110381301	Len	"Maria van Beveren, Vrouwe van Diksmuide, Watou, Jumelles"
Q110381301	Lnl	"Maria van Beveren, Vrouwe van Diksmuide, Watou, Jumelles"
Q110381301	Amul	"Marguerite van Beveren, Vrouwe van Diksmuide, Watou, Jumelles"

# Q110381302  Jan|Jean van Beveren  ->  Jan van Beveren   + Jean van Beveren
Q110381302	Lmul	"Jan van Beveren"
Q110381302	Len	"Jan van Beveren"
Q110381302	Lnl	"Jan van Beveren"
Q110381302	Amul	"Jean van Beveren"

# Q110383575  Metza|Motza Boos von Waldeck  ->  Metza Boos von Waldeck   + Motza Boos von Waldeck
Q110383575	Len	"Metza Boos von Waldeck"
Q110383575	Lnl	"Metza Boos von Waldeck"
Q110383575	Amul	"Motza Boos von Waldeck"

# Q110383576  Johann|Philipp Boos von Waldeck  ->  Johann Boos von Waldeck   + Philipp Boos von Waldeck
Q110383576	Lmul	"Johann Boos von Waldeck"
Q110383576	Len	"Johann Boos von Waldeck"
Q110383576	Lnl	"Johann Boos von Waldeck"
Q110383576	Amul	"Philipp Boos von Waldeck"

# Q110383585  Margarethe|Guta Knebel|Kenblin von Katzenelbogen  ->  Margarethe Knebel von Katzenelbogen   + Guta Kenblin von Katzenelbogen
Q110383585	Lmul	"Margarethe Knebel von Katzenelbogen"
Q110383585	Len	"Margarethe Knebel von Katzenelbogen"
Q110383585	Lnl	"Margarethe Knebel von Katzenelbogen"
Q110383585	Amul	"Guta Kenblin von Katzenelbogen"

# Q110386085  Hadewich|Haze van Culemborg  ->  Hadewich van Culemborg   + Haze van Culemborg
Q110386085	Lmul	"Hadewich van Culemborg"
Q110386085	Len	"Hadewich van Culemborg"
Q110386085	Lnl	"Hadewich van Culemborg"
Q110386085	Amul	"Haze van Culemborg"

# Q110387744  Maud|Matilda Bold  ->  Maud Bold   + Matilda Bold
Q110387744	Lmul	"Maud Bold"
Q110387744	Len	"Maud Bold"
Q110387744	Lnl	"Maud Bold"
Q110387744	Amul	"Matilda Bold"

# Q110388839  Margaret|Anne Brereton, of Malpas  ->  Margaret Brereton, of Malpas   + Anne Brereton, of Malpas
Q110388839	Lmul	"Margaret Brereton, of Malpas"
Q110388839	Len	"Margaret Brereton, of Malpas"
Q110388839	Lnl	"Margaret Brereton, of Malpas"
Q110388839	Amul	"Anne Brereton, of Malpas"

# Q110389654  Maud|Maude Massy (Massey), of Horton  ->  Maud Massy (Massey), of Horton   + Maude Massy (Massey), of Horton
Q110389654	Lmul	"Maud Massy (Massey), of Horton"
Q110389654	Len	"Maud Massy (Massey), of Horton"
Q110389654	Lnl	"Maud Massy (Massey), of Horton"
Q110389654	Amul	"Maude Massy (Massey), of Horton"

# Q110389717  Douce|Dowse Warburton  ->  Douce Warburton   + Dowse Warburton
Q110389717	Lmul	"Douce Warburton"
Q110389717	Len	"Douce Warburton"
Q110389717	Lnl	"Douce Warburton"
Q110389717	Amul	"Dowse Warburton"

# Q110390408  Katherine|Alice Holland  ->  Katherine Holland   + Alice Holland
Q110390408	Lmul	"Katherine Holland"
Q110390408	Len	"Katherine Holland"
Q110390408	Lnl	"Katherine Holland"
Q110390408	Amul	"Alice Holland"

# Q110390631  Gwladus|Margaret|Jane ferch Gwilym ab Ieuan ap Morgan  ->  Gwladus ferch Gwilym ab Ieuan ap Morgan   + Margaret ferch Gwilym ab Ieuan ap Morgan | Jane ferch Gwilym ab Ieuan ap Morgan
Q110390631	Lmul	"Gwladus ferch Gwilym ab Ieuan ap Morgan"
Q110390631	Len	"Gwladus ferch Gwilym ab Ieuan ap Morgan"
Q110390631	Lnl	"Gwladus ferch Gwilym ab Ieuan ap Morgan"
Q110390631	Amul	"Margaret ferch Gwilym ab Ieuan ap Morgan"
Q110390631	Amul	"Jane ferch Gwilym ab Ieuan ap Morgan"

# Q110390643  Jonet|Cecily ferch Ieuan ap Trahaearn ap Meurig  ->  Jonet ferch Ieuan ap Trahaearn ap Meurig   + Cecily ferch Ieuan ap Trahaearn ap Meurig
Q110390643	Lmul	"Jonet ferch Ieuan ap Trahaearn ap Meurig"
Q110390643	Len	"Jonet ferch Ieuan ap Trahaearn ap Meurig"
Q110390643	Lnl	"Jonet ferch Ieuan ap Trahaearn ap Meurig"
Q110390643	Amul	"Cecily ferch Ieuan ap Trahaearn ap Meurig"

# Q110394408  Thomas Bulteau|Bulteel  ->  Thomas Bulteau   + Thomas Bulteel
Q110394408	Lmul	"Thomas Bulteau"
Q110394408	Len	"Thomas Bulteau"
Q110394408	Lnl	"Thomas Bulteau"
Q110394408	Amul	"Thomas Bulteel"

# Q110394593  Anna|Marguerite van Hooghvorst van Grymbergen  ->  Anna van Hooghvorst van Grymbergen   + Marguerite van Hooghvorst van Grymbergen
Q110394593	Lmul	"Anna van Hooghvorst van Grymbergen"
Q110394593	Len	"Anna van Hooghvorst van Grymbergen"
Q110394593	Lnl	"Anna van Hooghvorst van Grymbergen"
Q110394593	Amul	"Marguerite van Hooghvorst van Grymbergen"

# Q110394733  Mahaut|Isabelle, Dame de Francières  ->  Mahaut Dame de Francières   + Isabelle, Dame de Francières
Q110394733	Len	"Mahaut Dame de Francières"
Q110394733	Lnl	"Mahaut Dame de Francières"
Q110394733	Amul	"Isabelle, Dame de Francières"

# Q110395414  Ellen|Helena Mountford (Montford)  ->  Ellen Mountford (Montford)   + Helena Mountford (Montford)
Q110395414	Len	"Ellen Mountford (Montford)"
Q110395414	Amul	"Helena Mountford (Montford)"

# Q110395449  Sybil|Sibilla de Lorty (L'Orti)  ->  Sybil de Lorty (L'Orti)   + Sibilla de Lorty (L'Orti)
Q110395449	Len	"Sybil de Lorty (L'Orti)"
Q110395449	Amul	"Sibilla de Lorty (L'Orti)"

# Q110395933  Isabella|Isobel Holt (Holte)  ->  Isabella Holt (Holte)   + Isobel Holt (Holte)
Q110395933	Len	"Isabella Holt (Holte)"
Q110395933	Amul	"Isobel Holt (Holte)"

# Q110396438  Mary|Margaret Bromley  ->  Mary Bromley   + Margaret Bromley
Q110396438	Lmul	"Mary Bromley"
Q110396438	Len	"Mary Bromley"
Q110396438	Lnl	"Mary Bromley"
Q110396438	Amul	"Margaret Bromley"

# Q110396550  Isabella|Sibilla de Halton  ->  Isabella de Halton   + Sibilla de Halton
Q110396550	Lmul	"Isabella de Halton"
Q110396550	Len	"Isabella de Halton"
Q110396550	Lnl	"Isabella de Halton"
Q110396550	Amul	"Sibilla de Halton"

# Q110396874  Laurence|Lawrence Standish, of Standish  ->  Laurence Standish, of Standish   + Lawrence Standish, of Standish
Q110396874	Lmul	"Laurence Standish, of Standish"
Q110396874	Len	"Laurence Standish, of Standish"
Q110396874	Lnl	"Laurence Standish, of Standish"
Q110396874	Amul	"Lawrence Standish, of Standish"

# Q110396878  Laura|Lora Pilkington  ->  Laura Pilkington   + Lora Pilkington
Q110396878	Lmul	"Laura Pilkington"
Q110396878	Len	"Laura Pilkington"
Q110396878	Lnl	"Laura Pilkington"
Q110396878	Amul	"Lora Pilkington"

# Q110398002  Hamon|Hamnet Massey (Mascy), of Rixton  ->  Hamon Massey (Mascy), of Rixton   + Hamnet Massey (Mascy), of Rixton
Q110398002	Lmul	"Hamon Massey (Mascy), of Rixton"
Q110398002	Len	"Hamon Massey (Mascy), of Rixton"
Q110398002	Lnl	"Hamon Massey (Mascy), of Rixton"
Q110398002	Amul	"Hamnet Massey (Mascy), of Rixton"

# Q110398007  Joanna|Janet Booth, of Dunham Massey  ->  Joanna Booth, of Dunham Massey   + Janet Booth, of Dunham Massey
Q110398007	Lmul	"Joanna Booth, of Dunham Massey"
Q110398007	Len	"Joanna Booth, of Dunham Massey"
Q110398007	Lnl	"Joanna Booth, of Dunham Massey"
Q110398007	Amul	"Janet Booth, of Dunham Massey"

# Q110398671  Alice|Agnes Fitton  ->  Alice Fitton   + Agnes Fitton
Q110398671	Lmul	"Alice Fitton"
Q110398671	Len	"Alice Fitton"
Q110398671	Lnl	"Alice Fitton"
Q110398671	Amul	"Agnes Fitton"

# Q110399510  Sevastia|Elisabeta 'Safta' Palladi  ->  Sevastia 'Safta' Palladi   + Elisabeta 'Safta' Palladi
Q110399510	Len	"Sevastia 'Safta' Palladi"
Q110399510	Lnl	"Sevastia 'Safta' Palladi"
Q110399510	Amul	"Elisabeta 'Safta' Palladi"

# Q110399520  Elisabeta|Sevastia 'Safta' Ursachi  ->  Elisabeta 'Safta' Ursachi   + Sevastia 'Safta' Ursachi
Q110399520	Lmul	"Elisabeta 'Safta' Ursachi"
Q110399520	Len	"Elisabeta 'Safta' Ursachi"
Q110399520	Lnl	"Elisabeta 'Safta' Ursachi"
Q110399520	Amul	"Sevastia 'Safta' Ursachi"

# Q110399576  Nicolae|Neculai Catargiul  ->  Nicolae Catargiul   + Neculai Catargiul
Q110399576	Lmul	"Nicolae Catargiul"
Q110399576	Len	"Nicolae Catargiul"
Q110399576	Lnl	"Nicolae Catargiul"
Q110399576	Amul	"Neculai Catargiul"

# Q110399683  Sarbica|Siruca Barnovscha  ->  Sarbica Barnovscha   + Siruca Barnovscha
Q110399683	Lmul	"Sarbica Barnovscha"
Q110399683	Len	"Sarbica Barnovscha"
Q110399683	Lnl	"Sarbica Barnovscha"
Q110399683	Amul	"Siruca Barnovscha"

# Q110399775  Elisabeta|Sevastie 'Safta' Balsh  ->  Elisabeta 'Safta' Balsh   + Sevastie 'Safta' Balsh
Q110399775	Lmul	"Elisabeta 'Safta' Balsh"
Q110399775	Len	"Elisabeta 'Safta' Balsh"
Q110399775	Lnl	"Elisabeta 'Safta' Balsh"
Q110399775	Amul	"Sevastie 'Safta' Balsh"

# Q110399860  Safta|Sanda Jora  ->  Safta Jora   + Sanda Jora
Q110399860	Lmul	"Safta Jora"
Q110399860	Len	"Safta Jora"
Q110399860	Lnl	"Safta Jora"
Q110399860	Amul	"Sanda Jora"

# Q110409812  Johann Orth 'the Elder|the Blind'  ->  Johann Orth 'the Elder Blind'   + Johann Orth 'the the Blind'
Q110409812	Lmul	"Johann Orth 'the Elder Blind'"
Q110409812	Len	"Johann Orth 'the Elder Blind'"
Q110409812	Lnl	"Johann Orth 'the Elder Blind'"
Q110409812	Amul	"Johann Orth 'the the Blind'"

# Q110409996  Catharina|Marga von Hövell  ->  Catharina von Hövell   + Marga von Hövell
Q110409996	Lmul	"Catharina von Hövell"
Q110409996	Len	"Catharina von Hövell"
Q110409996	Lnl	"Catharina von Hövell"
Q110409996	Amul	"Marga von Hövell"

# Q110410070  Dries|Andreas von Eller zu Luxheim  ->  Dries von Eller zu Luxheim   + Andreas von Eller zu Luxheim
Q110410070	Lmul	"Dries von Eller zu Luxheim"
Q110410070	Len	"Dries von Eller zu Luxheim"
Q110410070	Lnl	"Dries von Eller zu Luxheim"
Q110410070	Amul	"Andreas von Eller zu Luxheim"

# Q110410119  Fulsgin|Fulcona van Swalmen, Heiress of St.Laurensberg  ->  Fulsgin van Swalmen, Heiress of St.Laurensberg   + Fulcona van Swalmen, Heiress of St.Laurensberg
Q110410119	Lmul	"Fulsgin van Swalmen, Heiress of St.Laurensberg"
Q110410119	Len	"Fulsgin van Swalmen, Heiress of St.Laurensberg"
Q110410119	Lnl	"Fulsgin van Swalmen, Heiress of St.Laurensberg"
Q110410119	Amul	"Fulcona van Swalmen, Heiress of St.Laurensberg"

# Q110410348  Amiel|Amé II de La Trémoille, seigneur de Fontmorand  ->  Amiel II de La Trémoille, seigneur de Fontmorand   + Amé II de La Trémoille, seigneur de Fontmorand
Q110410348	Lmul	"Amiel II de La Trémoille, seigneur de Fontmorand"
Q110410348	Len	"Amiel II de La Trémoille, seigneur de Fontmorand"
Q110410348	Lnl	"Amiel II de La Trémoille, seigneur de Fontmorand"
Q110410348	Amul	"Amé II de La Trémoille, seigneur de Fontmorand"

# Q110410456  William|Guillaume Daubeney (d'Aubigné), Seigneur de Landal  ->  William Daubeney (d'Aubigné), Seigneur de Landal   + Guillaume Daubeney (d'Aubigné), Seigneur de Landal
Q110410456	Lmul	"William Daubeney (d'Aubigné), Seigneur de Landal"
Q110410456	Len	"William Daubeney (d'Aubigné), Seigneur de Landal"
Q110410456	Lnl	"William Daubeney (d'Aubigné), Seigneur de Landal"
Q110410456	Amul	"Guillaume Daubeney (d'Aubigné), Seigneur de Landal"

# Q110412817  Emma|Emmotta Perrott  ->  Emma Perrott   + Emmotta Perrott
Q110412817	Lmul	"Emma Perrott"
Q110412817	Len	"Emma Perrott"
Q110412817	Lnl	"Emma Perrott"
Q110412817	Amul	"Emmotta Perrott"

# Q110412847  Gwenllian|Jonet ferch Hywel ap Maredudd Fychan ap Maredudd  ->  Gwenllian ferch Hywel ap Maredudd Fychan ap Maredudd   + Jonet ferch Hywel ap Maredudd Fychan ap Maredudd
Q110412847	Lmul	"Gwenllian ferch Hywel ap Maredudd Fychan ap Maredudd"
Q110412847	Len	"Gwenllian ferch Hywel ap Maredudd Fychan ap Maredudd"
Q110412847	Lnl	"Gwenllian ferch Hywel ap Maredudd Fychan ap Maredudd"
Q110412847	Amul	"Jonet ferch Hywel ap Maredudd Fychan ap Maredudd"

# Q110412862  William (Herle) of Stoke Bishop|Bliss  ->  William (Herle) of Stoke Bishop   + William (Herle) of Stoke Bliss
Q110412862	Len	"William (Herle) of Stoke Bishop"
Q110412862	Amul	"William (Herle) of Stoke Bliss"

# Q110412954  Jenkin|John Kynaston, of Stocks  ->  Jenkin Kynaston, of Stocks   + John Kynaston, of Stocks
Q110412954	Lmul	"Jenkin Kynaston, of Stocks"
Q110412954	Len	"Jenkin Kynaston, of Stocks"
Q110412954	Lnl	"Jenkin Kynaston, of Stocks"
Q110412954	Amul	"John Kynaston, of Stocks"

# Q110413095  Agnes|Nest Russell  ->  Agnes Russell   + Nest Russell
Q110413095	Lmul	"Agnes Russell"
Q110413095	Len	"Agnes Russell"
Q110413095	Lnl	"Agnes Russell"
Q110413095	Amul	"Nest Russell"

# Q110413123  Eleanor|Alice|Elizabeth Corbet, of Moreton Corbet  ->  Eleanor Corbet, of Moreton Corbet   + Alice Corbet, of Moreton Corbet | Elizabeth Corbet, of Moreton Corbet
Q110413123	Lmul	"Eleanor Corbet, of Moreton Corbet"
Q110413123	Len	"Eleanor Corbet, of Moreton Corbet"
Q110413123	Lnl	"Eleanor Corbet, of Moreton Corbet"
Q110413123	Amul	"Alice Corbet, of Moreton Corbet"
Q110413123	Amul	"Elizabeth Corbet, of Moreton Corbet"

# Q110414047  Gwenhwyfar|Angharad ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel  ->  Gwenhwyfar ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel   + Angharad ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel
Q110414047	Lmul	"Gwenhwyfar ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel"
Q110414047	Len	"Gwenhwyfar ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel"
Q110414047	Lnl	"Gwenhwyfar ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel"
Q110414047	Amul	"Angharad ferch Dafydd ab Ieuan ap Rhirid Foel of Blodwel"

# Q110414722  Johan|Giovanni von der Leiter (della Scala), Herr von Bern  ->  Johan von der Leiter (della Scala), Herr von Bern   + Giovanni von der Leiter (della Scala), Herr von Bern
Q110414722	Len	"Johan von der Leiter (della Scala), Herr von Bern"
Q110414722	Lnl	"Johan von der Leiter (della Scala), Herr von Bern"
Q110414722	Amul	"Giovanni von der Leiter (della Scala), Herr von Bern"

# Q110414898  Gräfin Anna|Agnes von Honstein  ->  Gräfin Anna von Honstein   + Gräfin Agnes von Honstein
Q110414898	Len	"Gräfin Anna von Honstein"
Q110414898	Lnl	"Gräfin Anna von Honstein"
Q110414898	Amul	"Gräfin Agnes von Honstein"

# Q110415835  Johann|Hans, Freiherr von Aichberg zu Laberweinting  ->  Johann Freiherr von Aichberg zu Laberweinting   + Hans, Freiherr von Aichberg zu Laberweinting
Q110415835	Lmul	"Johann Freiherr von Aichberg zu Laberweinting"
Q110415835	Len	"Johann Freiherr von Aichberg zu Laberweinting"
Q110415835	Lnl	"Johann Freiherr von Aichberg zu Laberweinting"
Q110415835	Amul	"Hans, Freiherr von Aichberg zu Laberweinting"

# Q110422691  Eleonora|Caterina Cirino  ->  Eleonora Cirino   + Caterina Cirino
Q110422691	Lmul	"Eleonora Cirino"
Q110422691	Len	"Eleonora Cirino"
Q110422691	Lnl	"Eleonora Cirino"
Q110422691	Amul	"Caterina Cirino"

# Q110423586  Vincente Calvaert|Caluwaert  ->  Vincente Calvaert   + Vincente Caluwaert
Q110423586	Lmul	"Vincente Calvaert"
Q110423586	Len	"Vincente Calvaert"
Q110423586	Lnl	"Vincente Calvaert"
Q110423586	Amul	"Vincente Caluwaert"

# Q110423587  Jan Calvaert|Caluwaert  ->  Jan Calvaert   + Jan Caluwaert
Q110423587	Lmul	"Jan Calvaert"
Q110423587	Len	"Jan Calvaert"
Q110423587	Lnl	"Jan Calvaert"
Q110423587	Amul	"Jan Caluwaert"

# Q110423641  Louis|Raoul de Presles  ->  Louis de Presles   + Raoul de Presles
Q110423641	Len	"Louis de Presles"
Q110423641	Lnl	"Louis de Presles"
Q110423641	Amul	"Raoul de Presles"

# Q110425353  Jan|Hans Sweerts de Weert  ->  Jan Sweerts de Weert   + Hans Sweerts de Weert
Q110425353	Lmul	"Jan Sweerts de Weert"
Q110425353	Len	"Jan Sweerts de Weert"
Q110425353	Lnl	"Jan Sweerts de Weert"
Q110425353	Amul	"Hans Sweerts de Weert"

# Q110425430  Katharina|Anna von Wylich  ->  Katharina von Wylich   + Anna von Wylich
Q110425430	Lmul	"Katharina von Wylich"
Q110425430	Len	"Katharina von Wylich"
Q110425430	Lnl	"Katharina von Wylich"
Q110425430	Amul	"Anna von Wylich"

# Q110425470  Barthold|Bertold van Gendt, Heer van Loenen, Wolferen  ->  Barthold van Gendt, Heer van Loenen, Wolferen   + Bertold van Gendt, Heer van Loenen, Wolferen
Q110425470	Lmul	"Barthold van Gendt, Heer van Loenen, Wolferen"
Q110425470	Len	"Barthold van Gendt, Heer van Loenen, Wolferen"
Q110425470	Lnl	"Barthold van Gendt, Heer van Loenen, Wolferen"
Q110425470	Amul	"Bertold van Gendt, Heer van Loenen, Wolferen"

# Q110427960  Cecily|Sibyl Kemeys  ->  Cecily Kemeys   + Sibyl Kemeys
Q110427960	Lmul	"Cecily Kemeys"
Q110427960	Len	"Cecily Kemeys"
Q110427960	Lnl	"Cecily Kemeys"
Q110427960	Amul	"Sibyl Kemeys"

# Q110427972  Jenet|Joan ferch Ieuan ap Llesion ap Rhys (of Baglan) ap Morgan Fychan  ->  Jenet ferch Ieuan ap Llesion ap Rhys (of Baglan) ap Morgan Fychan   + Joan ferch Ieuan ap Llesion ap Rhys (of Baglan) ap Morgan Fychan
Q110427972	Len	"Jenet ferch Ieuan ap Llesion ap Rhys (of Baglan) ap Morgan Fychan"
Q110427972	Amul	"Joan ferch Ieuan ap Llesion ap Rhys (of Baglan) ap Morgan Fychan"

# Q110427976  Elizabeth|Isabel de la Mare (?Bere)  ->  Elizabeth de la Mare (?Bere)   + Isabel de la Mare (?Bere)
Q110427976	Len	"Elizabeth de la Mare (?Bere)"
Q110427976	Amul	"Isabel de la Mare (?Bere)"

# Q110428779  Thomas|John Hanley  ->  Thomas Hanley   + John Hanley
Q110428779	Lmul	"Thomas Hanley"
Q110428779	Len	"Thomas Hanley"
Q110428779	Lnl	"Thomas Hanley"
Q110428779	Amul	"John Hanley"

# Q110438516  Joan|Jane Busby  ->  Joan Busby   + Jane Busby
Q110438516	Lmul	"Joan Busby"
Q110438516	Len	"Joan Busby"
Q110438516	Lnl	"Joan Busby"
Q110438516	Amul	"Jane Busby"

# Q110438758  Robert|William Brandling, of Spytton  ->  Robert Brandling, of Spytton   + William Brandling, of Spytton
Q110438758	Lmul	"Robert Brandling, of Spytton"
Q110438758	Len	"Robert Brandling, of Spytton"
Q110438758	Lnl	"Robert Brandling, of Spytton"
Q110438758	Amul	"William Brandling, of Spytton"

# Q110438928  Thomas|James Livesey, of Livesey, Lancs  ->  Thomas Livesey, of Livesey, Lancs   + James Livesey, of Livesey, Lancs
Q110438928	Lmul	"Thomas Livesey, of Livesey, Lancs"
Q110438928	Len	"Thomas Livesey, of Livesey, Lancs"
Q110438928	Lnl	"Thomas Livesey, of Livesey, Lancs"
Q110438928	Amul	"James Livesey, of Livesey, Lancs"

# Q110438953  Edith|Eden Grey  ->  Edith Grey   + Eden Grey
Q110438953	Lmul	"Edith Grey"
Q110438953	Len	"Edith Grey"
Q110438953	Lnl	"Edith Grey"
Q110438953	Amul	"Eden Grey"

# Q110439205  Sir Roger|Robert Whittingham, of Pendley  ->  Sir Roger Whittingham, of Pendley   + Sir Robert Whittingham, of Pendley
Q110439205	Lmul	"Sir Roger Whittingham, of Pendley"
Q110439205	Len	"Sir Roger Whittingham, of Pendley"
Q110439205	Lnl	"Sir Roger Whittingham, of Pendley"
Q110439205	Amul	"Sir Robert Whittingham, of Pendley"

# Q110439230  Isabel|Emmote Wilcotes  ->  Isabel Wilcotes   + Emmote Wilcotes
Q110439230	Lmul	"Isabel Wilcotes"
Q110439230	Len	"Isabel Wilcotes"
Q110439230	Lnl	"Isabel Wilcotes"
Q110439230	Amul	"Emmote Wilcotes"

# Q110440305  Galfred|Geoffrey de Coryton  ->  Galfred de Coryton   + Geoffrey de Coryton
Q110440305	Lmul	"Galfred de Coryton"
Q110440305	Len	"Galfred de Coryton"
Q110440305	Lnl	"Galfred de Coryton"
Q110440305	Amul	"Geoffrey de Coryton"

# Q110440338  Elisabeth|Isabell Mathaderva (Mathadarda)  ->  Elisabeth Mathaderva (Mathadarda)   + Isabell Mathaderva (Mathadarda)
Q110440338	Len	"Elisabeth Mathaderva (Mathadarda)"
Q110440338	Amul	"Isabell Mathaderva (Mathadarda)"

# Q110440365  Johane|Johanna Pengelley  ->  Johane Pengelley   + Johanna Pengelley
Q110440365	Lmul	"Johane Pengelley"
Q110440365	Len	"Johane Pengelley"
Q110440365	Lnl	"Johane Pengelley"
Q110440365	Amul	"Johanna Pengelley"

# Q110440385  Joan|Joanne Lanhergy (Lannerey)  ->  Joan Lanhergy (Lannerey)   + Joanne Lanhergy (Lannerey)
Q110440385	Len	"Joan Lanhergy (Lannerey)"
Q110440385	Amul	"Joanne Lanhergy (Lannerey)"

# Q110440632  Ellen|Eleanor Rocliffe (Roucliffe)  ->  Ellen Rocliffe (Roucliffe)   + Eleanor Rocliffe (Roucliffe)
Q110440632	Len	"Ellen Rocliffe (Roucliffe)"
Q110440632	Amul	"Eleanor Rocliffe (Roucliffe)"

# Q110440662  Dulcia|Dowsabel Ashley  ->  Dulcia Ashley   + Dowsabel Ashley
Q110440662	Lmul	"Dulcia Ashley"
Q110440662	Len	"Dulcia Ashley"
Q110440662	Lnl	"Dulcia Ashley"
Q110440662	Amul	"Dowsabel Ashley"

# Q110440752  Margery|Margaret Drury  ->  Margery Drury   + Margaret Drury
Q110440752	Lmul	"Margery Drury"
Q110440752	Len	"Margery Drury"
Q110440752	Lnl	"Margery Drury"
Q110440752	Amul	"Margaret Drury"

# Q110440757  Margaret|Margery Naunton  ->  Margaret Naunton   + Margery Naunton
Q110440757	Lmul	"Margaret Naunton"
Q110440757	Len	"Margaret Naunton"
Q110440757	Lnl	"Margaret Naunton"
Q110440757	Amul	"Margery Naunton"

# Q110440920  Joan|Joanna Dene (Deane)  ->  Joan Dene (Deane)   + Joanna Dene (Deane)
Q110440920	Len	"Joan Dene (Deane)"
Q110440920	Amul	"Joanna Dene (Deane)"

# Q110440944  Maud|Matilda Prestwood  ->  Maud Prestwood   + Matilda Prestwood
Q110440944	Lmul	"Maud Prestwood"
Q110440944	Len	"Maud Prestwood"
Q110440944	Lnl	"Maud Prestwood"
Q110440944	Amul	"Matilda Prestwood"

# Q110441617  Iorwerth|Iocyn ap Cynwrig ap Rhys ap Robert  ->  Iorwerth ap Cynwrig ap Rhys ap Robert   + Iocyn ap Cynwrig ap Rhys ap Robert
Q110441617	Lmul	"Iorwerth ap Cynwrig ap Rhys ap Robert"
Q110441617	Len	"Iorwerth ap Cynwrig ap Rhys ap Robert"
Q110441617	Lnl	"Iorwerth ap Cynwrig ap Rhys ap Robert"
Q110441617	Amul	"Iocyn ap Cynwrig ap Rhys ap Robert"

# Q110441660  Elliw|Gwenllian ferch Gruffudd Derwas  ->  Elliw ferch Gruffudd Derwas   + Gwenllian ferch Gruffudd Derwas
Q110441660	Lmul	"Elliw ferch Gruffudd Derwas"
Q110441660	Len	"Elliw ferch Gruffudd Derwas"
Q110441660	Lnl	"Elliw ferch Gruffudd Derwas"
Q110441660	Amul	"Gwenllian ferch Gruffudd Derwas"

# Q110458671  Agnes|Kunigunde von Westerburg  ->  Agnes von Westerburg   + Kunigunde von Westerburg
Q110458671	Lmul	"Agnes von Westerburg"
Q110458671	Len	"Agnes von Westerburg"
Q110458671	Lnl	"Agnes von Westerburg"
Q110458671	Amul	"Kunigunde von Westerburg"

# Q110458688  Brigitte|Jutta von Leisnig  ->  Brigitte von Leisnig   + Jutta von Leisnig
Q110458688	Len	"Brigitte von Leisnig"
Q110458688	Lnl	"Brigitte von Leisnig"
Q110458688	Amul	"Jutta von Leisnig"

# Q110459026  Bernhard|Bouchard de Guise  ->  Bernhard de Guise   + Bouchard de Guise
Q110459026	Len	"Bernhard de Guise"
Q110459026	Lnl	"Bernhard de Guise"
Q110459026	Amul	"Bouchard de Guise"

# Q110504200  Honora|Norin O'More, of Leix  ->  Honora O'More, of Leix   + Norin O'More, of Leix
Q110504200	Lmul	"Honora O'More, of Leix"
Q110504200	Len	"Honora O'More, of Leix"
Q110504200	Amul	"Norin O'More, of Leix"

# Q110504473  Lucy|Lleucu ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon  ->  Lucy ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon   + Lleucu ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon
Q110504473	Lmul	"Lucy ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon"
Q110504473	Len	"Lucy ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon"
Q110504473	Amul	"Lleucu ferch Morgan ap Llywelyn ap Hywel Fychan of Brecon"

# Q110504582  Sean|John|Shane Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory  ->  Sean Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory   + John Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory | Shane Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory
Q110504582	Lmul	"Sean Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory"
Q110504582	Len	"Sean Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory"
Q110504582	Amul	"John Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory"
Q110504582	Amul	"Shane Mac-Gill-Patrick (Fitzpatrick), of Upper Ossory"

# Q110504637  Mahon|Mathghamhain O'Brien, of Killclanoy  ->  Mahon O'Brien, of Killclanoy   + Mathghamhain O'Brien, of Killclanoy
Q110504637	Lmul	"Mahon O'Brien, of Killclanoy"
Q110504637	Len	"Mahon O'Brien, of Killclanoy"
Q110504637	Amul	"Mathghamhain O'Brien, of Killclanoy"

# Q110504642  Margaret|Joanna FitzMaurice  ->  Margaret FitzMaurice   + Joanna FitzMaurice
Q110504642	Lmul	"Margaret FitzMaurice"
Q110504642	Len	"Margaret FitzMaurice"
Q110504642	Amul	"Joanna FitzMaurice"

# Q110505149  Barbara|Anna von Niebelschütz  ->  Barbara von Niebelschütz   + Anna von Niebelschütz
Q110505149	Lmul	"Barbara von Niebelschütz"
Q110505149	Len	"Barbara von Niebelschütz"
Q110505149	Amul	"Anna von Niebelschütz"

# Q110505197  Mathilde|Mahaut de Confignon  ->  Mathilde de Confignon   + Mahaut de Confignon
Q110505197	Lmul	"Mathilde de Confignon"
Q110505197	Len	"Mathilde de Confignon"
Q110505197	Amul	"Mahaut de Confignon"

# Q110505753  Jaus Leins|Luenss  ->  Jaus Leins   + Jaus Luenss
Q110505753	Lmul	"Jaus Leins"
Q110505753	Len	"Jaus Leins"
Q110505753	Amul	"Jaus Luenss"

# Q110506078  Anna Henninger|Hennicke  ->  Anna Henninger   + Anna Hennicke
Q110506078	Lmul	"Anna Henninger"
Q110506078	Len	"Anna Henninger"
Q110506078	Amul	"Anna Hennicke"

# Q110506281  Mr. Jan|Johan van Ittersum  ->  Mr. Jan van Ittersum   + Mr. Johan van Ittersum
Q110506281	Lmul	"Mr. Jan van Ittersum"
Q110506281	Len	"Mr. Jan van Ittersum"
Q110506281	Amul	"Mr. Johan van Ittersum"

# Q110506502  Alard Fleck|Vlecke van Caldenbroeck  ->  Alard Fleck van Caldenbroeck   + Alard Vlecke van Caldenbroeck
Q110506502	Lmul	"Alard Fleck van Caldenbroeck"
Q110506502	Len	"Alard Fleck van Caldenbroeck"
Q110506502	Amul	"Alard Vlecke van Caldenbroeck"

# Q110506504  Lijsbeth|Elisabeth van Tegelen  ->  Lijsbeth van Tegelen   + Elisabeth van Tegelen
Q110506504	Lmul	"Lijsbeth van Tegelen"
Q110506504	Len	"Lijsbeth van Tegelen"
Q110506504	Amul	"Elisabeth van Tegelen"

# Q110506970  NN van Rosande|van Rosaw  ->  NN van Rosande Rosaw   + NN van van Rosaw
Q110506970	Lmul	"NN van Rosande Rosaw"
Q110506970	Len	"NN van Rosande Rosaw"
Q110506970	Amul	"NN van van Rosaw"

# Q110507038  Fije|Sophia van Sinderen  ->  Fije van Sinderen   + Sophia van Sinderen
Q110507038	Lmul	"Fije van Sinderen"
Q110507038	Len	"Fije van Sinderen"
Q110507038	Amul	"Sophia van Sinderen"

# Q110507592  Jutte|Judith Mulert  ->  Jutte Mulert   + Judith Mulert
Q110507592	Lmul	"Jutte Mulert"
Q110507592	Len	"Jutte Mulert"
Q110507592	Amul	"Judith Mulert"

# Q110507596  Engelbert|Egbert Mulert  ->  Engelbert Mulert   + Egbert Mulert
Q110507596	Lmul	"Engelbert Mulert"
Q110507596	Len	"Engelbert Mulert"
Q110507596	Amul	"Egbert Mulert"

# Q110509176  Aysinus|Arsieu III de Montesquiou, Chevalier  ->  Aysinus III de Montesquiou, Chevalier   + Arsieu III de Montesquiou, Chevalier
Q110509176	Lmul	"Aysinus III de Montesquiou, Chevalier"
Q110509176	Len	"Aysinus III de Montesquiou, Chevalier"
Q110509176	Amul	"Arsieu III de Montesquiou, Chevalier"

# Q110509203  Aysinus|Arsieu II de Montesquiou, Chevalier  ->  Aysinus II de Montesquiou, Chevalier   + Arsieu II de Montesquiou, Chevalier
Q110509203	Lmul	"Aysinus II de Montesquiou, Chevalier"
Q110509203	Len	"Aysinus II de Montesquiou, Chevalier"
Q110509203	Amul	"Arsieu II de Montesquiou, Chevalier"

# Q110509209  Aysinus|Arsieu I 'le Vieux' de Montesquiou, Baron de Montesquiou  ->  Aysinus I 'le Vieux' de Montesquiou, Baron de Montesquiou   + Arsieu I 'le Vieux' de Montesquiou, Baron de Montesquiou
Q110509209	Len	"Aysinus I 'le Vieux' de Montesquiou, Baron de Montesquiou"
Q110509209	Amul	"Arsieu I 'le Vieux' de Montesquiou, Baron de Montesquiou"

# Q110520145  Reynold|Reginald Trethurffe  ->  Reynold Trethurffe   + Reginald Trethurffe
Q110520145	Lmul	"Reynold Trethurffe"
Q110520145	Len	"Reynold Trethurffe"
Q110520145	Amul	"Reginald Trethurffe"

# Q110520693  John|Edward Upton, of Upton  ->  John Upton, of Upton   + Edward Upton, of Upton
Q110520693	Lmul	"John Upton, of Upton"
Q110520693	Len	"John Upton, of Upton"
Q110520693	Amul	"Edward Upton, of Upton"

# Q110520725  Joan|Johanna Trelawny  ->  Joan Trelawny   + Johanna Trelawny
Q110520725	Lmul	"Joan Trelawny"
Q110520725	Len	"Joan Trelawny"
Q110520725	Amul	"Johanna Trelawny"

# Q110520788  Thomas|John Uppeton  ->  Thomas Uppeton   + John Uppeton
Q110520788	Lmul	"Thomas Uppeton"
Q110520788	Len	"Thomas Uppeton"
Q110520788	Amul	"John Uppeton"

# Q110520795  Radigond|Radigund  ->  Radigond   + Radigund
Q110520795	Lmul	"Radigond"
Q110520795	Len	"Radigond"
Q110520795	Amul	"Radigund"

# Q110520969  Maud|Mathilda de Kederston  ->  Maud de Kederston   + Mathilda de Kederston
Q110520969	Lmul	"Maud de Kederston"
Q110520969	Len	"Maud de Kederston"
Q110520969	Amul	"Mathilda de Kederston"

# Q110537076  Elisabeth|Elsa von Galen  ->  Elisabeth von Galen   + Elsa von Galen
Q110537076	Lmul	"Elisabeth von Galen"
Q110537076	Len	"Elisabeth von Galen"
Q110537076	Amul	"Elsa von Galen"

# Q110537456  Adelheid|Alix Berthout, Heiress of Grimberghe  ->  Adelheid Berthout, Heiress of Grimberghe   + Alix Berthout, Heiress of Grimberghe
Q110537456	Len	"Adelheid Berthout, Heiress of Grimberghe"
Q110537456	Amul	"Alix Berthout, Heiress of Grimberghe"

# Q110537898  Catherine|Claude de Monchy (Mouchy)  ->  Catherine de Monchy (Mouchy)   + Claude de Monchy (Mouchy)
Q110537898	Len	"Catherine de Monchy (Mouchy)"
Q110537898	Amul	"Claude de Monchy (Mouchy)"

# Q110538936  Wulfing|Wolfgang Ungnad von Weissenwolf  ->  Wulfing Ungnad von Weissenwolf   + Wolfgang Ungnad von Weissenwolf
Q110538936	Lmul	"Wulfing Ungnad von Weissenwolf"
Q110538936	Len	"Wulfing Ungnad von Weissenwolf"
Q110538936	Amul	"Wolfgang Ungnad von Weissenwolf"

# Q110539125  Theodor|Getrzych (?Dietrich) von Kolowrat-Bezdruziczky  ->  Theodor (?Dietrich) von Kolowrat-Bezdruziczky   + Getrzych (?Dietrich) von Kolowrat-Bezdruziczky
Q110539125	Len	"Theodor (?Dietrich) von Kolowrat-Bezdruziczky"
Q110539125	Amul	"Getrzych (?Dietrich) von Kolowrat-Bezdruziczky"

# Q110548301  riddare Simon Pedersen Körning|Kyrning, bailiff of Kastelholma, lord of Lundås manor  ->  riddare Simon Pedersen Körning bailiff of Kastelholma, lord of Lundås manor   + riddare Simon Pedersen Kyrning, bailiff of Kastelholma, lord of Lundås manor
Q110548301	Len	"riddare Simon Pedersen Körning bailiff of Kastelholma, lord of Lundås manor"
Q110548301	Amul	"riddare Simon Pedersen Kyrning, bailiff of Kastelholma, lord of Lundås manor"

# Q110548771  Ermegaard|Armgard Bylow, Grevinna i Gripsholm  ->  Ermegaard Bylow, Grevinna i Gripsholm   + Armgard Bylow, Grevinna i Gripsholm
Q110548771	Lmul	"Ermegaard Bylow, Grevinna i Gripsholm"
Q110548771	Len	"Ermegaard Bylow, Grevinna i Gripsholm"
Q110548771	Amul	"Armgard Bylow, Grevinna i Gripsholm"

# Q110548776  Alhed|Aleda  ->  Alhed   + Aleda
Q110548776	Len	"Alhed"
Q110548776	Amul	"Aleda"

# Q110549014  Dina|Mariotta Ogilvie  ->  Dina Ogilvie   + Mariotta Ogilvie
Q110549014	Lmul	"Dina Ogilvie"
Q110549014	Len	"Dina Ogilvie"
Q110549014	Amul	"Mariotta Ogilvie"

# Q110549352  Kristofer|Krister Stackelberg  ->  Kristofer Stackelberg   + Krister Stackelberg
Q110549352	Lmul	"Kristofer Stackelberg"
Q110549352	Len	"Kristofer Stackelberg"
Q110549352	Amul	"Krister Stackelberg"

# Q110549531  Kristen|Christiern Skram zu Urup  ->  Kristen Skram zu Urup   + Christiern Skram zu Urup
Q110549531	Len	"Kristen Skram zu Urup"
Q110549531	Amul	"Christiern Skram zu Urup"

# Q110549747  Sigmund|Simon III Thun, Herr von Thun in Castel-Brughier  ->  Sigmund III Thun, Herr von Thun in Castel-Brughier   + Simon III Thun, Herr von Thun in Castel-Brughier
Q110549747	Len	"Sigmund III Thun, Herr von Thun in Castel-Brughier"
Q110549747	Amul	"Simon III Thun, Herr von Thun in Castel-Brughier"

# Q110556468  Jan|Jean de Villegas  ->  Jan de Villegas   + Jean de Villegas
Q110556468	Lmul	"Jan de Villegas"
Q110556468	Len	"Jan de Villegas"
Q110556468	Amul	"Jean de Villegas"

# Q110557065  Jakob|Jacob van der Ehze (Heeckeren)  ->  Jakob van der Ehze (Heeckeren)   + Jacob van der Ehze (Heeckeren)
Q110557065	Lmul	"Jakob van der Ehze (Heeckeren)"
Q110557065	Len	"Jakob van der Ehze (Heeckeren)"
Q110557065	Amul	"Jacob van der Ehze (Heeckeren)"

# Q110558671  Matthias|Albert Finck, Herr von Finckenstein auf Roggenhausen  ->  Matthias Finck, Herr von Finckenstein auf Roggenhausen   + Albert Finck, Herr von Finckenstein auf Roggenhausen
Q110558671	Lmul	"Matthias Finck, Herr von Finckenstein auf Roggenhausen"
Q110558671	Len	"Matthias Finck, Herr von Finckenstein auf Roggenhausen"
Q110558671	Amul	"Albert Finck, Herr von Finckenstein auf Roggenhausen"

# Q110558676  Dorothea|Barbara von Seewalde  ->  Dorothea von Seewalde   + Barbara von Seewalde
Q110558676	Lmul	"Dorothea von Seewalde"
Q110558676	Len	"Dorothea von Seewalde"
Q110558676	Amul	"Barbara von Seewalde"

# Q110558999  Iain|John Campbell, of Craignish  ->  Iain Campbell, of Craignish   + John Campbell, of Craignish
Q110558999	Lmul	"Iain Campbell, of Craignish"
Q110558999	Len	"Iain Campbell, of Craignish"
Q110558999	Amul	"John Campbell, of Craignish"

# Q110559555  Humfrey|Humphrey Tyrrell, of Thornton  ->  Humfrey Tyrrell, of Thornton   + Humphrey Tyrrell, of Thornton
Q110559555	Lmul	"Humfrey Tyrrell, of Thornton"
Q110559555	Len	"Humfrey Tyrrell, of Thornton"
Q110559555	Amul	"Humphrey Tyrrell, of Thornton"

# Q110559640  Anne|Matilda Huntley, of Treowen  ->  Anne Huntley, of Treowen   + Matilda Huntley, of Treowen
Q110559640	Lmul	"Anne Huntley, of Treowen"
Q110559640	Len	"Anne Huntley, of Treowen"
Q110559640	Amul	"Matilda Huntley, of Treowen"

# Q110559649  Margred|Elsbeth ferch John ap Thomas ab Adam  ->  Margred ferch John ap Thomas ab Adam   + Elsbeth ferch John ap Thomas ab Adam
Q110559649	Lmul	"Margred ferch John ap Thomas ab Adam"
Q110559649	Len	"Margred ferch John ap Thomas ab Adam"
Q110559649	Amul	"Elsbeth ferch John ap Thomas ab Adam"

# Q110559927  Sibill|Sybbell Fitzelles (Fitzellis)  ->  Sibill Fitzelles (Fitzellis)   + Sybbell Fitzelles (Fitzellis)
Q110559927	Lmul	"Sibill Fitzelles (Fitzellis)"
Q110559927	Len	"Sibill Fitzelles (Fitzellis)"
Q110559927	Amul	"Sybbell Fitzelles (Fitzellis)"

# Q110561456  Ellen|Elbert|Elizabeth Allen  ->  Ellen Allen   + Elbert Allen | Elizabeth Allen
Q110561456	Lmul	"Ellen Allen"
Q110561456	Len	"Ellen Allen"
Q110561456	Amul	"Elbert Allen"
Q110561456	Amul	"Elizabeth Allen"

# Q110561477  Richard|Ralph Chamberlayne  ->  Richard Chamberlayne   + Ralph Chamberlayne
Q110561477	Lmul	"Richard Chamberlayne"
Q110561477	Len	"Richard Chamberlayne"
Q110561477	Amul	"Ralph Chamberlayne"

# Q110572003  Clara|Anna von Freyberg  ->  Clara von Freyberg   + Anna von Freyberg
Q110572003	Lmul	"Clara von Freyberg"
Q110572003	Len	"Clara von Freyberg"
Q110572003	Amul	"Anna von Freyberg"

# Q110572007  Chunrat|Konrad von Freyberg  ->  Chunrat von Freyberg   + Konrad von Freyberg
Q110572007	Lmul	"Chunrat von Freyberg"
Q110572007	Len	"Chunrat von Freyberg"
Q110572007	Amul	"Konrad von Freyberg"

# Q110574594  Clinet|Claude de Lanes (Lannes), Seigneur de Bellade et de Rochebalade  ->  Clinet de Lanes (Lannes), Seigneur de Bellade et de Rochebalade   + Claude de Lanes (Lannes), Seigneur de Bellade et de Rochebalade
Q110574594	Len	"Clinet de Lanes (Lannes), Seigneur de Bellade et de Rochebalade"
Q110574594	Amul	"Claude de Lanes (Lannes), Seigneur de Bellade et de Rochebalade"

# Q110574618  Clinet|Clignet de Perigord de Talleyrand  ->  Clinet de Perigord de Talleyrand   + Clignet de Perigord de Talleyrand
Q110574618	Len	"Clinet de Perigord de Talleyrand"
Q110574618	Amul	"Clignet de Perigord de Talleyrand"

# Q110578155  Etiennette|Tiphaine de Chantocé  ->  Etiennette de Chantocé   + Tiphaine de Chantocé
Q110578155	Lmul	"Etiennette de Chantocé"
Q110578155	Len	"Etiennette de Chantocé"
Q110578155	Amul	"Tiphaine de Chantocé"

# Q110578184  Origone|Orguen  ->  Origone   + Orguen
Q110578184	Lmul	"Origone"
Q110578184	Len	"Origone"
Q110578184	Amul	"Orguen"

# Q110578358  Pierre|Jean Raymond  ->  Pierre Raymond   + Jean Raymond
Q110578358	Lmul	"Pierre Raymond"
Q110578358	Len	"Pierre Raymond"
Q110578358	Amul	"Jean Raymond"

# Q110580647  Joane|Joan de Bromflete (Brounflete)  ->  Joane de Bromflete (Brounflete)   + Joan de Bromflete (Brounflete)
Q110580647	Lmul	"Joane de Bromflete (Brounflete)"
Q110580647	Len	"Joane de Bromflete (Brounflete)"
Q110580647	Amul	"Joan de Bromflete (Brounflete)"

# Q110582239  Elsbeth|Elizabeth Conwy  ->  Elsbeth Conwy   + Elizabeth Conwy
Q110582239	Lmul	"Elsbeth Conwy"
Q110582239	Len	"Elsbeth Conwy"
Q110582239	Amul	"Elizabeth Conwy"

# Q110582255  Richard|Ralph Brereton, of Cheshire  ->  Richard Brereton, of Cheshire   + Ralph Brereton, of Cheshire
Q110582255	Lmul	"Richard Brereton, of Cheshire"
Q110582255	Len	"Richard Brereton, of Cheshire"
Q110582255	Amul	"Ralph Brereton, of Cheshire"

# Q110582418  Gruffudd|Griffi ap Llywelyn ap Robert ap Llywarch  ->  Gruffudd ap Llywelyn ap Robert ap Llywarch   + Griffi ap Llywelyn ap Robert ap Llywarch
Q110582418	Lmul	"Gruffudd ap Llywelyn ap Robert ap Llywarch"
Q110582418	Len	"Gruffudd ap Llywelyn ap Robert ap Llywarch"
Q110582418	Amul	"Griffi ap Llywelyn ap Robert ap Llywarch"

# Q110582440  Gwladys|Gwenllian ferch Gruffudd ap Meilir Eutun ab Elidir  ->  Gwladys ferch Gruffudd ap Meilir Eutun ab Elidir   + Gwenllian ferch Gruffudd ap Meilir Eutun ab Elidir
Q110582440	Lmul	"Gwladys ferch Gruffudd ap Meilir Eutun ab Elidir"
Q110582440	Len	"Gwladys ferch Gruffudd ap Meilir Eutun ab Elidir"
Q110582440	Amul	"Gwenllian ferch Gruffudd ap Meilir Eutun ab Elidir"

# Q110582810  Lleuki|Nest ferch Gwerstan ap Gwaithfoed  ->  Lleuki ferch Gwerstan ap Gwaithfoed   + Nest ferch Gwerstan ap Gwaithfoed
Q110582810	Lmul	"Lleuki ferch Gwerstan ap Gwaithfoed"
Q110582810	Len	"Lleuki ferch Gwerstan ap Gwaithfoed"
Q110582810	Amul	"Nest ferch Gwerstan ap Gwaithfoed"

# Q110583387  Joice|Jocosa Burley  ->  Joice Burley   + Jocosa Burley
Q110583387	Lmul	"Joice Burley"
Q110583387	Len	"Joice Burley"
Q110583387	Amul	"Jocosa Burley"

# Q110583502  Dyddgu|Gwerful ferch Aron ap Pen Hen ab Iorwerth  ->  Dyddgu ferch Aron ap Pen Hen ab Iorwerth   + Gwerful ferch Aron ap Pen Hen ab Iorwerth
Q110583502	Lmul	"Dyddgu ferch Aron ap Pen Hen ab Iorwerth"
Q110583502	Len	"Dyddgu ferch Aron ap Pen Hen ab Iorwerth"
Q110583502	Amul	"Gwerful ferch Aron ap Pen Hen ab Iorwerth"

# Q110585521  Angharad|Hunydd ferch Gruffudd ap Cadwgan  ->  Angharad ferch Gruffudd ap Cadwgan   + Hunydd ferch Gruffudd ap Cadwgan
Q110585521	Lmul	"Angharad ferch Gruffudd ap Cadwgan"
Q110585521	Len	"Angharad ferch Gruffudd ap Cadwgan"
Q110585521	Amul	"Hunydd ferch Gruffudd ap Cadwgan"

# Q110585751  Gladousa|Wladousa  ->  Gladousa   + Wladousa
Q110585751	Lmul	"Gladousa"
Q110585751	Len	"Gladousa"
Q110585751	Amul	"Wladousa"

# Q110585877  Anne|Agnes Taylor  ->  Anne Taylor   + Agnes Taylor
Q110585877	Lmul	"Anne Taylor"
Q110585877	Len	"Anne Taylor"
Q110585877	Amul	"Agnes Taylor"

# Q110585903  Philip|Thomas Knottesford  ->  Philip Knottesford   + Thomas Knottesford
Q110585903	Lmul	"Philip Knottesford"
Q110585903	Len	"Philip Knottesford"
Q110585903	Amul	"Thomas Knottesford"

# Q110602300  Estevanhinha|Estafania Garcia  ->  Estevanhinha Garcia   + Estafania Garcia
Q110602300	Lmul	"Estevanhinha Garcia"
Q110602300	Len	"Estevanhinha Garcia"
Q110602300	Amul	"Estafania Garcia"

# Q110612463  Jane|Joan Jewe  ->  Jane Jewe   + Joan Jewe
Q110612463	Lmul	"Jane Jewe"
Q110612463	Len	"Jane Jewe"
Q110612463	Amul	"Joan Jewe"

# Q110612785  Margaret|Margeria de Trewargen (Trevanyon)  ->  Margaret de Trewargen (Trevanyon)   + Margeria de Trewargen (Trevanyon)
Q110612785	Lmul	"Margaret de Trewargen (Trevanyon)"
Q110612785	Len	"Margaret de Trewargen (Trevanyon)"
Q110612785	Amul	"Margeria de Trewargen (Trevanyon)"

# Q110612792  Riej|Richard Bloyet (Bluet)  ->  Riej Bloyet (Bluet)   + Richard Bloyet (Bluet)
Q110612792	Lmul	"Riej Bloyet (Bluet)"
Q110612792	Len	"Riej Bloyet (Bluet)"
Q110612792	Amul	"Richard Bloyet (Bluet)"

# Q110612796  Sir Theobald|Tibbot Gorges alias Russell, of Wraxall  ->  Sir Theobald Gorges alias Russell, of Wraxall   + Sir Tibbot Gorges alias Russell, of Wraxall
Q110612796	Lmul	"Sir Theobald Gorges alias Russell, of Wraxall"
Q110612796	Len	"Sir Theobald Gorges alias Russell, of Wraxall"
Q110612796	Amul	"Sir Tibbot Gorges alias Russell, of Wraxall"

# Q110613212  Letitia|Alicia L'Estrange  ->  Letitia L'Estrange   + Alicia L'Estrange
Q110613212	Lmul	"Letitia L'Estrange"
Q110613212	Len	"Letitia L'Estrange"
Q110613212	Amul	"Alicia L'Estrange"

# Q110613606  Stevina|Stevania van Wisch  ->  Stevina van Wisch   + Stevania van Wisch
Q110613606	Lmul	"Stevina van Wisch"
Q110613606	Len	"Stevina van Wisch"
Q110613606	Amul	"Stevania van Wisch"

# Q110615895  Anne|Agnes Mauleverer  ->  Anne Mauleverer   + Agnes Mauleverer
Q110615895	Lmul	"Anne Mauleverer"
Q110615895	Len	"Anne Mauleverer"
Q110615895	Amul	"Agnes Mauleverer"

# Q110616340  Ruffin Bourell|Bourel|Boureel  ->  Ruffin Bourell   + Ruffin Bourel | Ruffin Boureel
Q110616340	Lmul	"Ruffin Bourell"
Q110616340	Len	"Ruffin Bourell"
Q110616340	Amul	"Ruffin Bourel"
Q110616340	Amul	"Ruffin Boureel"

# Q110616705  Maria|Mayor Rodriguez Pecha  ->  Maria Rodriguez Pecha   + Mayor Rodriguez Pecha
Q110616705	Lmul	"Maria Rodriguez Pecha"
Q110616705	Len	"Maria Rodriguez Pecha"
Q110616705	Amul	"Mayor Rodriguez Pecha"

# Q110618305  Etheldred|Audrey Poyntz  ->  Etheldred Poyntz   + Audrey Poyntz
Q110618305	Lmul	"Etheldred Poyntz"
Q110618305	Len	"Etheldred Poyntz"
Q110618305	Amul	"Audrey Poyntz"

# Q110618374  Geoffrey|Gregory Radcliffe, of Farmesden  ->  Geoffrey Radcliffe, of Farmesden   + Gregory Radcliffe, of Farmesden
Q110618374	Lmul	"Geoffrey Radcliffe, of Farmesden"
Q110618374	Len	"Geoffrey Radcliffe, of Farmesden"
Q110618374	Amul	"Gregory Radcliffe, of Farmesden"

# Q110618420  Sir Robert|John Segrave, of Norfolk  ->  Sir Robert Segrave, of Norfolk   + Sir John Segrave, of Norfolk
Q110618420	Lmul	"Sir Robert Segrave, of Norfolk"
Q110618420	Len	"Sir Robert Segrave, of Norfolk"
Q110618420	Amul	"Sir John Segrave, of Norfolk"

# Q110618461  Gerald|Gerard Meynell, of Willington  ->  Gerald Meynell, of Willington   + Gerard Meynell, of Willington
Q110618461	Lmul	"Gerald Meynell, of Willington"
Q110618461	Len	"Gerald Meynell, of Willington"
Q110618461	Amul	"Gerard Meynell, of Willington"

# Q110618483  Joan|Johanna  ->  Joan   + Johanna
Q110618483	Lmul	"Joan"
Q110618483	Len	"Joan"
Q110618483	Amul	"Johanna"

# Q110618684  Margaret|Magdalen Bray  ->  Margaret Bray   + Magdalen Bray
Q110618684	Lmul	"Margaret Bray"
Q110618684	Len	"Margaret Bray"
Q110618684	Amul	"Magdalen Bray"

# Q110618866  Reginald|Richard Warcup, of Smerdale  ->  Reginald Warcup, of Smerdale   + Richard Warcup, of Smerdale
Q110618866	Lmul	"Reginald Warcup, of Smerdale"
Q110618866	Len	"Reginald Warcup, of Smerdale"
Q110618866	Amul	"Richard Warcup, of Smerdale"

# Q110619225  Sir Robert|Thomas Newport  ->  Sir Robert Newport   + Sir Thomas Newport
Q110619225	Lmul	"Sir Robert Newport"
Q110619225	Len	"Sir Robert Newport"
Q110619225	Amul	"Sir Thomas Newport"

# Q110621289  Leena|Madleena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi  ->  Leena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi   + Madleena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi
Q110621289	Lmul	"Leena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi"
Q110621289	Len	"Leena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi"
Q110621289	Amul	"Madleena Deken, heiress of Rooküla, co-heiress of Paunküla & Harmi"

# Q110621296  Maikki|Maret Tuve  ->  Maikki Tuve   + Maret Tuve
Q110621296	Lmul	"Maikki Tuve"
Q110621296	Len	"Maikki Tuve"
Q110621296	Amul	"Maret Tuve"

# Q110621529  Jörg|Georg von Arberg  ->  Jörg von Arberg   + Georg von Arberg
Q110621529	Lmul	"Jörg von Arberg"
Q110621529	Len	"Jörg von Arberg"
Q110621529	Amul	"Georg von Arberg"

# Q110621543  Christoph|Christopher von Obritschau  ->  Christoph von Obritschau   + Christopher von Obritschau
Q110621543	Lmul	"Christoph von Obritschau"
Q110621543	Len	"Christoph von Obritschau"
Q110621543	Amul	"Christopher von Obritschau"

# Q110621880  Jane|Joan  ->  Jane   + Joan
Q110621880	Lmul	"Jane"
Q110621880	Len	"Jane"
Q110621880	Amul	"Joan"

# Q110621955  Gwenllian|Lucy Norris  ->  Gwenllian Norris   + Lucy Norris
Q110621955	Lmul	"Gwenllian Norris"
Q110621955	Len	"Gwenllian Norris"
Q110621955	Amul	"Lucy Norris"

# Q110621969  Joan|Crisly ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch  ->  Joan ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch   + Crisly ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch
Q110621969	Lmul	"Joan ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch"
Q110621969	Len	"Joan ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch"
Q110621969	Amul	"Crisly ferch Rhûn ap Gronwy Fychan ap Gronwy ap Llywarch"

# Q110621995  Agnes|Elizabeth Chicheley  ->  Agnes Chicheley   + Elizabeth Chicheley
Q110621995	Lmul	"Agnes Chicheley"
Q110621995	Len	"Agnes Chicheley"
Q110621995	Amul	"Elizabeth Chicheley"

# Q110622076  Morgan|Meurig ab Iestyn, lord of Glamorgan  ->  Morgan ab Iestyn, lord of Glamorgan   + Meurig ab Iestyn, lord of Glamorgan
Q110622076	Lmul	"Morgan ab Iestyn, lord of Glamorgan"
Q110622076	Len	"Morgan ab Iestyn, lord of Glamorgan"
Q110622076	Amul	"Meurig ab Iestyn, lord of Glamorgan"

# Q110622122  Jenkin|John de Turberville  ->  Jenkin de Turberville   + John de Turberville
Q110622122	Lmul	"Jenkin de Turberville"
Q110622122	Len	"Jenkin de Turberville"
Q110622122	Amul	"John de Turberville"

# Q110622416  Elsbeth|Elizabeth Eliot  ->  Elsbeth Eliot   + Elizabeth Eliot
Q110622416	Lmul	"Elsbeth Eliot"
Q110622416	Len	"Elsbeth Eliot"
Q110622416	Amul	"Elizabeth Eliot"

# Q110622430  Jonet|Joan Perott  ->  Jonet Perott   + Joan Perott
Q110622430	Lmul	"Jonet Perott"
Q110622430	Len	"Jonet Perott"
Q110622430	Amul	"Joan Perott"

# Q110622435  Sir John|Gwilyn ap John ap Robert ap Jenkin Clement  ->  Sir John ap John ap Robert ap Jenkin Clement   + Sir Gwilyn ap John ap Robert ap Jenkin Clement
Q110622435	Lmul	"Sir John ap John ap Robert ap Jenkin Clement"
Q110622435	Len	"Sir John ap John ap Robert ap Jenkin Clement"
Q110622435	Amul	"Sir Gwilyn ap John ap Robert ap Jenkin Clement"

# Q110622453  Margred|Jane Welsh  ->  Margred Welsh   + Jane Welsh
Q110622453	Lmul	"Margred Welsh"
Q110622453	Len	"Margred Welsh"
Q110622453	Amul	"Jane Welsh"

# Q110622492  Sir Walter|Gwilym ap Walter Malephant  ->  Sir Walter ap Walter Malephant   + Sir Gwilym ap Walter Malephant
Q110622492	Lmul	"Sir Walter ap Walter Malephant"
Q110622492	Len	"Sir Walter ap Walter Malephant"
Q110622492	Amul	"Sir Gwilym ap Walter Malephant"

# Q110622583  Sir Thomas|John Hampton  ->  Sir Thomas Hampton   + Sir John Hampton
Q110622583	Lmul	"Sir Thomas Hampton"
Q110622583	Len	"Sir Thomas Hampton"
Q110622583	Amul	"Sir John Hampton"

# Q110622936  Eleanor|Ellen Rigges (Brigges)  ->  Eleanor Rigges (Brigges)   + Ellen Rigges (Brigges)
Q110622936	Lmul	"Eleanor Rigges (Brigges)"
Q110622936	Len	"Eleanor Rigges (Brigges)"
Q110622936	Amul	"Ellen Rigges (Brigges)"

# Q110623118  John|Thomas Bird, of Middlesex  ->  John Bird, of Middlesex   + Thomas Bird, of Middlesex
Q110623118	Lmul	"John Bird, of Middlesex"
Q110623118	Len	"John Bird, of Middlesex"
Q110623118	Amul	"Thomas Bird, of Middlesex"

# Q110623207  Janet Robertson, of Strowan|Struan  ->  Janet Robertson, of Strowan   + Janet Robertson, of Struan
Q110623207	Lmul	"Janet Robertson, of Strowan"
Q110623207	Len	"Janet Robertson, of Strowan"
Q110623207	Amul	"Janet Robertson, of Struan"

# Q110623212  Jean|Janet Somerville  ->  Jean Somerville   + Janet Somerville
Q110623212	Lmul	"Jean Somerville"
Q110623212	Len	"Jean Somerville"
Q110623212	Amul	"Janet Somerville"

# Q110623341  Alianore|Eleanor Chandos  ->  Alianore Chandos   + Eleanor Chandos
Q110623341	Lmul	"Alianore Chandos"
Q110623341	Len	"Alianore Chandos"
Q110623341	Amul	"Eleanor Chandos"

# Q110623449  Anne|Innocentia|Senecha|Sarah Gresley  ->  Anne Gresley   + Innocentia Gresley | Senecha Gresley | Sarah Gresley
Q110623449	Lmul	"Anne Gresley"
Q110623449	Len	"Anne Gresley"
Q110623449	Amul	"Innocentia Gresley"
Q110623449	Amul	"Senecha Gresley"
Q110623449	Amul	"Sarah Gresley"

# Q110623477  Pernele|Petronelle de Camville  ->  Pernele de Camville   + Petronelle de Camville
Q110623477	Lmul	"Pernele de Camville"
Q110623477	Len	"Pernele de Camville"
Q110623477	Amul	"Petronelle de Camville"

# Q110623887  Margred|Elizabeth Lewis  ->  Margred Lewis   + Elizabeth Lewis
Q110623887	Lmul	"Margred Lewis"
Q110623887	Len	"Margred Lewis"
Q110623887	Amul	"Elizabeth Lewis"

# Q110635485  Angharad|Gwerful ferch Ieuan ap Hywel ap Tegwared Bais Wen  ->  Angharad ferch Ieuan ap Hywel ap Tegwared Bais Wen   + Gwerful ferch Ieuan ap Hywel ap Tegwared Bais Wen
Q110635485	Lmul	"Angharad ferch Ieuan ap Hywel ap Tegwared Bais Wen"
Q110635485	Len	"Angharad ferch Ieuan ap Hywel ap Tegwared Bais Wen"
Q110635485	Amul	"Gwerful ferch Ieuan ap Hywel ap Tegwared Bais Wen"

# Q110635521  Awdrey|Ethelrede  ->  Awdrey   + Ethelrede
Q110635521	Lmul	"Awdrey"
Q110635521	Len	"Awdrey"
Q110635521	Amul	"Ethelrede"

# Q110635652  Agnes|Jane ferch Dafydd  ->  Agnes ferch Dafydd   + Jane ferch Dafydd
Q110635652	Lmul	"Agnes ferch Dafydd"
Q110635652	Len	"Agnes ferch Dafydd"
Q110635652	Amul	"Jane ferch Dafydd"

# Q110637009  Efa|Gwenllian ferch Gruffudd Llwyd  ->  Efa ferch Gruffudd Llwyd   + Gwenllian ferch Gruffudd Llwyd
Q110637009	Lmul	"Efa ferch Gruffudd Llwyd"
Q110637009	Len	"Efa ferch Gruffudd Llwyd"
Q110637009	Amul	"Gwenllian ferch Gruffudd Llwyd"

# Q110637365  Anne|Isolda Salwey  ->  Anne Salwey   + Isolda Salwey
Q110637365	Lmul	"Anne Salwey"
Q110637365	Len	"Anne Salwey"
Q110637365	Amul	"Isolda Salwey"

# Q110637387  Mary Breaux|Bressy  ->  Mary Breaux   + Mary Bressy
Q110637387	Lmul	"Mary Breaux"
Q110637387	Len	"Mary Breaux"
Q110637387	Amul	"Mary Bressy"

# Q110637477  Reginald|Reynold Barantyne  ->  Reginald Barantyne   + Reynold Barantyne
Q110637477	Lmul	"Reginald Barantyne"
Q110637477	Len	"Reginald Barantyne"
Q110637477	Amul	"Reynold Barantyne"

# Q110637490  Joan|Jane Goddard  ->  Joan Goddard   + Jane Goddard
Q110637490	Lmul	"Joan Goddard"
Q110637490	Len	"Joan Goddard"
Q110637490	Amul	"Jane Goddard"

# Q110637510  Gonar|Gonnora (or Grace) Thurgood (or Thorowgood)  ->  Gonar (or Grace) Thurgood (or Thorowgood)   + Gonnora (or Grace) Thurgood (or Thorowgood)
Q110637510	Lmul	"Gonar (or Grace) Thurgood (or Thorowgood)"
Q110637510	Len	"Gonar (or Grace) Thurgood (or Thorowgood)"
Q110637510	Amul	"Gonnora (or Grace) Thurgood (or Thorowgood)"

# Q110637529  Crysogona|Grisogena Smith  ->  Crysogona Smith   + Grisogena Smith
Q110637529	Lmul	"Crysogona Smith"
Q110637529	Len	"Crysogona Smith"
Q110637529	Amul	"Grisogena Smith"

# Q110638109  Jane|Isabel Anderson  ->  Jane Anderson   + Isabel Anderson
Q110638109	Lmul	"Jane Anderson"
Q110638109	Len	"Jane Anderson"
Q110638109	Amul	"Isabel Anderson"

# Q110638131  Elisabeth|Eleanor Markenfield  ->  Elisabeth Markenfield   + Eleanor Markenfield
Q110638131	Lmul	"Elisabeth Markenfield"
Q110638131	Len	"Elisabeth Markenfield"
Q110638131	Amul	"Eleanor Markenfield"

# Q110638184  Anne|Agnes Crake (Creyke)  ->  Anne Crake (Creyke)   + Agnes Crake (Creyke)
Q110638184	Lmul	"Anne Crake (Creyke)"
Q110638184	Len	"Anne Crake (Creyke)"
Q110638184	Amul	"Agnes Crake (Creyke)"

# Q110638736  Mary|Joan de Heton  ->  Mary de Heton   + Joan de Heton
Q110638736	Lmul	"Mary de Heton"
Q110638736	Len	"Mary de Heton"
Q110638736	Amul	"Joan de Heton"

# Q110640245  Anne|Louise d'Enghien de Havrech  ->  Anne d'Enghien de Havrech   + Louise d'Enghien de Havrech
Q110640245	Lmul	"Anne d'Enghien de Havrech"
Q110640245	Len	"Anne d'Enghien de Havrech"
Q110640245	Amul	"Louise d'Enghien de Havrech"

# Q110640427  Egidius|Gilles de Bouchout  ->  Egidius de Bouchout   + Gilles de Bouchout
Q110640427	Lmul	"Egidius de Bouchout"
Q110640427	Len	"Egidius de Bouchout"
Q110640427	Amul	"Gilles de Bouchout"

# Q110640434  Alard|Eylard de Poucques, Vicomte d'Ypres  ->  Alard de Poucques, Vicomte d'Ypres   + Eylard de Poucques, Vicomte d'Ypres
Q110640434	Lmul	"Alard de Poucques, Vicomte d'Ypres"
Q110640434	Len	"Alard de Poucques, Vicomte d'Ypres"
Q110640434	Amul	"Eylard de Poucques, Vicomte d'Ypres"

# Q110640440  Catharina|Katharina van Borselen  ->  Catharina van Borselen   + Katharina van Borselen
Q110640440	Lmul	"Catharina van Borselen"
Q110640440	Len	"Catharina van Borselen"
Q110640440	Amul	"Katharina van Borselen"

# Q110640441  Claas|Nikolaus van Borselen Rasenzoon  ->  Claas van Borselen Rasenzoon   + Nikolaus van Borselen Rasenzoon
Q110640441	Lmul	"Claas van Borselen Rasenzoon"
Q110640441	Len	"Claas van Borselen Rasenzoon"
Q110640441	Amul	"Nikolaus van Borselen Rasenzoon"

# Q110640889  Jacques|Josse van Calendries  ->  Jacques van Calendries   + Josse van Calendries
Q110640889	Lmul	"Jacques van Calendries"
Q110640889	Len	"Jacques van Calendries"
Q110640889	Amul	"Josse van Calendries"

# Q110640959  Elisabeth|Marie van Rotselaer (Rotzelaer)  ->  Elisabeth van Rotselaer (Rotzelaer)   + Marie van Rotselaer (Rotzelaer)
Q110640959	Len	"Elisabeth van Rotselaer (Rotzelaer)"
Q110640959	Amul	"Marie van Rotselaer (Rotzelaer)"

# Q110688264  Eleanor|Helen Waldeive  ->  Eleanor Waldeive   + Helen Waldeive
Q110688264	Lmul	"Eleanor Waldeive"
Q110688264	Len	"Eleanor Waldeive"
Q110688264	Amul	"Helen Waldeive"

# Q110715309  Béatrice|Cecile de Réthel  ->  Béatrice de Réthel   + Cecile de Réthel
Q110715309	Lmul	"Béatrice de Réthel"
Q110715309	Len	"Béatrice de Réthel"
Q110715309	Amul	"Cecile de Réthel"

# Q110729293  Jyrki|Yrjänä Matinpoika of Vilkki  ->  Jyrki Matinpoika of Vilkki   + Yrjänä Matinpoika of Vilkki
Q110729293	Lmul	"Jyrki Matinpoika of Vilkki"
Q110729293	Len	"Jyrki Matinpoika of Vilkki"
Q110729293	Amul	"Yrjänä Matinpoika of Vilkki"

# Q110729337  Jyrki|Yrjänä Simonpoika of Vilkki  ->  Jyrki Simonpoika of Vilkki   + Yrjänä Simonpoika of Vilkki
Q110729337	Lmul	"Jyrki Simonpoika of Vilkki"
Q110729337	Len	"Jyrki Simonpoika of Vilkki"
Q110729337	Amul	"Yrjänä Simonpoika of Vilkki"

# Q110730678  Anne|Ann Isaac  ->  Anne Isaac   + Ann Isaac
Q110730678	Lmul	"Anne Isaac"
Q110730678	Len	"Anne Isaac"
Q110730678	Amul	"Ann Isaac"

# Q110730725  Cecily|Cecilia Deincourt  ->  Cecily Deincourt   + Cecilia Deincourt
Q110730725	Lmul	"Cecily Deincourt"
Q110730725	Len	"Cecily Deincourt"
Q110730725	Amul	"Cecilia Deincourt"

# Q110730740  Margaret|Margery Calthorpe  ->  Margaret Calthorpe   + Margery Calthorpe
Q110730740	Lmul	"Margaret Calthorpe"
Q110730740	Len	"Margaret Calthorpe"
Q110730740	Amul	"Margery Calthorpe"

# Q110730994  Ailine|Elen  ->  Ailine   + Elen
Q110730994	Lmul	"Ailine"
Q110730994	Len	"Ailine"
Q110730994	Amul	"Elen"

# Q110731010  Henry|Gilbert de Clifton  ->  Henry de Clifton   + Gilbert de Clifton
Q110731010	Lmul	"Henry de Clifton"
Q110731010	Len	"Henry de Clifton"
Q110731010	Amul	"Gilbert de Clifton"

# Q110731138  Iannaki|Jorgos Mavros  ->  Iannaki Mavros   + Jorgos Mavros
Q110731138	Len	"Iannaki Mavros"
Q110731138	Amul	"Jorgos Mavros"

# Q110731142  noble Nike|Victoria Soutzaina  ->  noble Nike Soutzaina   + noble Victoria Soutzaina
Q110731142	Lmul	"noble Nike Soutzaina"
Q110731142	Len	"noble Nike Soutzaina"
Q110731142	Amul	"noble Victoria Soutzaina"

# Q110731154  Constantin|Apostol Catargiu, steward of Moldavia  ->  Constantin Catargiu, steward of Moldavia   + Apostol Catargiu, steward of Moldavia
Q110731154	Len	"Constantin Catargiu, steward of Moldavia"
Q110731154	Amul	"Apostol Catargiu, steward of Moldavia"

# Q110731625  Gottfried|Gothard V, Herr zu Drachenfels und Fronenbruch  ->  Gottfried V, Herr zu Drachenfels und Fronenbruch   + Gothard V, Herr zu Drachenfels und Fronenbruch
Q110731625	Len	"Gottfried V, Herr zu Drachenfels und Fronenbruch"
Q110731625	Amul	"Gothard V, Herr zu Drachenfels und Fronenbruch"

# Q110731701  John Gashis|Gashes|Gaches  ->  John Gashis   + John Gashes | John Gaches
Q110731701	Lmul	"John Gashis"
Q110731701	Len	"John Gashis"
Q110731701	Amul	"John Gashes"
Q110731701	Amul	"John Gaches"

# Q110737710  Bahadur|Baindur|Baadur Sidamoni  ->  Bahadur Sidamoni   + Baindur Sidamoni | Baadur Sidamoni
Q110737710	Lmul	"Bahadur Sidamoni"
Q110737710	Len	"Bahadur Sidamoni"
Q110737710	Amul	"Baindur Sidamoni"
Q110737710	Amul	"Baadur Sidamoni"

# Q110737861  Rusa|Rusudan Mkheidze  ->  Rusa Mkheidze   + Rusudan Mkheidze
Q110737861	Lmul	"Rusa Mkheidze"
Q110737861	Len	"Rusa Mkheidze"
Q110737861	Amul	"Rusudan Mkheidze"

# Q111424098  George|Jyrgi Leslie, lord of Saka manor  ->  George Leslie, lord of Saka manor   + Jyrgi Leslie, lord of Saka manor
Q111424098	Lmul	"George Leslie, lord of Saka manor"
Q111424098	Len	"George Leslie, lord of Saka manor"
Q111424098	Amul	"Jyrgi Leslie, lord of Saka manor"

# Q111424100  John|Johannes Watson  ->  John Watson   + Johannes Watson
Q111424100	Lmul	"John Watson"
Q111424100	Len	"John Watson"
Q111424100	Amul	"Johannes Watson"

# Q111444002  Agnes|Joan|Jane Gross  ->  Agnes Gross   + Joan Gross | Jane Gross
Q111444002	Lmul	"Agnes Gross"
Q111444002	Len	"Agnes Gross"
Q111444002	Amul	"Joan Gross"
Q111444002	Amul	"Jane Gross"

# Q111444231  Sir Richard|George Lane, of Tulske, 1st Baronet  ->  Sir Richard Lane, of Tulske, 1st Baronet   + Sir George Lane, of Tulske, 1st Baronet
Q111444231	Lmul	"Sir Richard Lane, of Tulske, 1st Baronet"
Q111444231	Len	"Sir Richard Lane, of Tulske, 1st Baronet"
Q111444231	Amul	"Sir George Lane, of Tulske, 1st Baronet"

# Q111451883  Joan|Jennet Thweng (Thwynge)  ->  Joan Thweng (Thwynge)   + Jennet Thweng (Thwynge)
Q111451883	Lmul	"Joan Thweng (Thwynge)"
Q111451883	Len	"Joan Thweng (Thwynge)"
Q111451883	Amul	"Jennet Thweng (Thwynge)"

# Q111452296  Marie|Mary Lane  ->  Marie Lane   + Mary Lane
Q111452296	Lmul	"Marie Lane"
Q111452296	Len	"Marie Lane"
Q111452296	Amul	"Mary Lane"

# Q111452444  Robert|Robinet Twyford, of Sponden  ->  Robert Twyford, of Sponden   + Robinet Twyford, of Sponden
Q111452444	Lmul	"Robert Twyford, of Sponden"
Q111452444	Len	"Robert Twyford, of Sponden"
Q111452444	Amul	"Robinet Twyford, of Sponden"

# Q111452557  John|George Pigott, of Abingdon Hall  ->  John Pigott, of Abingdon Hall   + George Pigott, of Abingdon Hall
Q111452557	Lmul	"John Pigott, of Abingdon Hall"
Q111452557	Len	"John Pigott, of Abingdon Hall"
Q111452557	Amul	"George Pigott, of Abingdon Hall"

# Q111452839  Elizabeth|Maud|Margaret Savage  ->  Elizabeth Savage   + Maud Savage | Margaret Savage
Q111452839	Lmul	"Elizabeth Savage"
Q111452839	Len	"Elizabeth Savage"
Q111452839	Amul	"Maud Savage"
Q111452839	Amul	"Margaret Savage"

# Q111453018  Radulf|Ralph de Clayton  ->  Radulf de Clayton   + Ralph de Clayton
Q111453018	Lmul	"Radulf de Clayton"
Q111453018	Len	"Radulf de Clayton"
Q111453018	Amul	"Ralph de Clayton"

# Q111454495  Margaret|Margery Eyton  ->  Margaret Eyton   + Margery Eyton
Q111454495	Lmul	"Margaret Eyton"
Q111454495	Len	"Margaret Eyton"
Q111454495	Amul	"Margery Eyton"

# Q111456769  Jane|Joan Egan  ->  Jane Egan   + Joan Egan
Q111456769	Lmul	"Jane Egan"
Q111456769	Len	"Jane Egan"
Q111456769	Amul	"Joan Egan"

# Q111456846  William|John Winter, of Winter Barningham  ->  William Winter, of Winter Barningham   + John Winter, of Winter Barningham
Q111456846	Lmul	"William Winter, of Winter Barningham"
Q111456846	Len	"William Winter, of Winter Barningham"
Q111456846	Amul	"John Winter, of Winter Barningham"

# Q111456851  Elizabeth|Joan Newenham  ->  Elizabeth Newenham   + Joan Newenham
Q111456851	Lmul	"Elizabeth Newenham"
Q111456851	Len	"Elizabeth Newenham"
Q111456851	Amul	"Joan Newenham"

# Q111456924  Nerio|Rainerio I Acciaioli (Acciaiuoli), Duke of Athens  ->  Nerio I Acciaioli (Acciaiuoli), Duke of Athens   + Rainerio I Acciaioli (Acciaiuoli), Duke of Athens
Q111456924	Lmul	"Nerio I Acciaioli (Acciaiuoli), Duke of Athens"
Q111456924	Len	"Nerio I Acciaioli (Acciaiuoli), Duke of Athens"
Q111456924	Amul	"Rainerio I Acciaioli (Acciaiuoli), Duke of Athens"

# Q111464838  Humphrey|William Titley, of Titley  ->  Humphrey Titley, of Titley   + William Titley, of Titley
Q111464838	Lmul	"Humphrey Titley, of Titley"
Q111464838	Len	"Humphrey Titley, of Titley"
Q111464838	Amul	"William Titley, of Titley"

# Q111466118  Sir John|Hugh Bussy, of Haugham, Lincs  ->  Sir John Bussy, of Haugham, Lincs   + Sir Hugh Bussy, of Haugham, Lincs
Q111466118	Lmul	"Sir John Bussy, of Haugham, Lincs"
Q111466118	Len	"Sir John Bussy, of Haugham, Lincs"
Q111466118	Amul	"Sir Hugh Bussy, of Haugham, Lincs"

# Q111466125  Margaret|Katherine Cumberworth  ->  Margaret Cumberworth   + Katherine Cumberworth
Q111466125	Lmul	"Margaret Cumberworth"
Q111466125	Len	"Margaret Cumberworth"
Q111466125	Amul	"Katherine Cumberworth"

# Q111466138  Maud|Mabel Folville, of Ashley Folville  ->  Maud Folville, of Ashley Folville   + Mabel Folville, of Ashley Folville
Q111466138	Lmul	"Maud Folville, of Ashley Folville"
Q111466138	Len	"Maud Folville, of Ashley Folville"
Q111466138	Amul	"Mabel Folville, of Ashley Folville"

# Q111466158  Sybil|Sibilla Corbuson (Corticon)  ->  Sybil Corbuson (Corticon)   + Sibilla Corbuson (Corticon)
Q111466158	Lmul	"Sybil Corbuson (Corticon)"
Q111466158	Len	"Sybil Corbuson (Corticon)"
Q111466158	Amul	"Sibilla Corbuson (Corticon)"

# Q111466212  William|Walter Prest, of Melton Mowbray  ->  William Prest, of Melton Mowbray   + Walter Prest, of Melton Mowbray
Q111466212	Lmul	"William Prest, of Melton Mowbray"
Q111466212	Len	"William Prest, of Melton Mowbray"
Q111466212	Amul	"Walter Prest, of Melton Mowbray"

# Q111466256  Elizabeth|Isabel Auderley (Audley)  ->  Elizabeth Auderley (Audley)   + Isabel Auderley (Audley)
Q111466256	Lmul	"Elizabeth Auderley (Audley)"
Q111466256	Len	"Elizabeth Auderley (Audley)"
Q111466256	Amul	"Isabel Auderley (Audley)"

# Q111466689  Matilda|Elizabeth  ->  Matilda   + Elizabeth
Q111466689	Lmul	"Matilda"
Q111466689	Len	"Matilda"
Q111466689	Amul	"Elizabeth"

# Q111506488  Lodovik|Lewis Meux, of Lymington & Kingston  ->  Lodovik Meux, of Lymington & Kingston   + Lewis Meux, of Lymington & Kingston
Q111506488	Lmul	"Lodovik Meux, of Lymington & Kingston"
Q111506488	Len	"Lodovik Meux, of Lymington & Kingston"
Q111506488	Amul	"Lewis Meux, of Lymington & Kingston"

# Q111506574  Johanna|Joan Cavell  ->  Johanna Cavell   + Joan Cavell
Q111506574	Lmul	"Johanna Cavell"
Q111506574	Len	"Johanna Cavell"
Q111506574	Amul	"Joan Cavell"

# Q111506582  Anne|Amicia Coode (Code)  ->  Anne Coode (Code)   + Amicia Coode (Code)
Q111506582	Lmul	"Anne Coode (Code)"
Q111506582	Len	"Anne Coode (Code)"
Q111506582	Amul	"Amicia Coode (Code)"

# Q111506593  Alianor|Helen FitzJames  ->  Alianor FitzJames   + Helen FitzJames
Q111506593	Lmul	"Alianor FitzJames"
Q111506593	Len	"Alianor FitzJames"
Q111506593	Amul	"Helen FitzJames"

# Q111506638  Mary|Margaret Chudleigh  ->  Mary Chudleigh   + Margaret Chudleigh
Q111506638	Lmul	"Mary Chudleigh"
Q111506638	Len	"Mary Chudleigh"
Q111506638	Amul	"Margaret Chudleigh"

# Q111506746  Isabella|Joan Drewe  ->  Isabella Drewe   + Joan Drewe
Q111506746	Lmul	"Isabella Drewe"
Q111506746	Len	"Isabella Drewe"
Q111506746	Amul	"Joan Drewe"

# Q111506752  Emeline Crewes|Cruwys  ->  Emeline Crewes   + Emeline Cruwys
Q111506752	Lmul	"Emeline Crewes"
Q111506752	Len	"Emeline Crewes"
Q111506752	Amul	"Emeline Cruwys"

# Q111506765  Thomasine|Mary Lovelace, of Kingsdowne  ->  Thomasine Lovelace, of Kingsdowne   + Mary Lovelace, of Kingsdowne
Q111506765	Lmul	"Thomasine Lovelace, of Kingsdowne"
Q111506765	Len	"Thomasine Lovelace, of Kingsdowne"
Q111506765	Amul	"Mary Lovelace, of Kingsdowne"

# Q111506774  Stephen|Thomas Harry  ->  Stephen Harry   + Thomas Harry
Q111506774	Lmul	"Stephen Harry"
Q111506774	Len	"Stephen Harry"
Q111506774	Amul	"Thomas Harry"

# Q111506785  Maude|Agnes|Amy French  ->  Maude French   + Agnes French | Amy French
Q111506785	Lmul	"Maude French"
Q111506785	Len	"Maude French"
Q111506785	Amul	"Agnes French"
Q111506785	Amul	"Amy French"

# Q111506811  Thomas|John Bastard  ->  Thomas Bastard   + John Bastard
Q111506811	Lmul	"Thomas Bastard"
Q111506811	Len	"Thomas Bastard"
Q111506811	Amul	"John Bastard"

# Q111506843  William Heale|Hele, of Soputh Hele  ->  William Heale of Soputh Hele   + William Hele, of Soputh Hele
Q111506843	Lmul	"William Heale of Soputh Hele"
Q111506843	Len	"William Heale of Soputh Hele"
Q111506843	Amul	"William Hele, of Soputh Hele"

# Q111506847  Alice Lewre|Lure  ->  Alice Lewre   + Alice Lure
Q111506847	Lmul	"Alice Lewre"
Q111506847	Len	"Alice Lewre"
Q111506847	Amul	"Alice Lure"

# Q111506883  Sir Thomas|John Reynes, of Marston  ->  Sir Thomas Reynes, of Marston   + Sir John Reynes, of Marston
Q111506883	Lmul	"Sir Thomas Reynes, of Marston"
Q111506883	Len	"Sir Thomas Reynes, of Marston"
Q111506883	Amul	"Sir John Reynes, of Marston"

# Q111506953  Robert Meryott|Meriot  ->  Robert Meryott   + Robert Meriot
Q111506953	Lmul	"Robert Meryott"
Q111506953	Len	"Robert Meryott"
Q111506953	Amul	"Robert Meriot"

# Q111523829  Jeanne|Suzanne d'Haranges  ->  Jeanne d'Haranges   + Suzanne d'Haranges
Q111523829	Lmul	"Jeanne d'Haranges"
Q111523829	Len	"Jeanne d'Haranges"
Q111523829	Amul	"Suzanne d'Haranges"

# Q111525065  Gwilym|Wilcock ap Watkin Gunter  ->  Gwilym ap Watkin Gunter   + Wilcock ap Watkin Gunter
Q111525065	Lmul	"Gwilym ap Watkin Gunter"
Q111525065	Len	"Gwilym ap Watkin Gunter"
Q111525065	Amul	"Wilcock ap Watkin Gunter"

# Q111525129  Jane|Joan Eton (Eyton)  ->  Jane Eton (Eyton)   + Joan Eton (Eyton)
Q111525129	Lmul	"Jane Eton (Eyton)"
Q111525129	Len	"Jane Eton (Eyton)"
Q111525129	Amul	"Joan Eton (Eyton)"

# Q111907904  Margarethe|Maria von Landsberg  ->  Margarethe von Landsberg   + Maria von Landsberg
Q111907904	Lmul	"Margarethe von Landsberg"
Q111907904	Len	"Margarethe von Landsberg"
Q111907904	Amul	"Maria von Landsberg"

# Q111907998  Imagina|Adelheid von Werd, Heiress of Landgrafschaft im Elsass  ->  Imagina von Werd, Heiress of Landgrafschaft im Elsass   + Adelheid von Werd, Heiress of Landgrafschaft im Elsass
Q111907998	Lmul	"Imagina von Werd, Heiress of Landgrafschaft im Elsass"
Q111907998	Len	"Imagina von Werd, Heiress of Landgrafschaft im Elsass"
Q111907998	Amul	"Adelheid von Werd, Heiress of Landgrafschaft im Elsass"

# Q111908000  Jolanthe|Yland von Hirschhorn  ->  Jolanthe von Hirschhorn   + Yland von Hirschhorn
Q111908000	Lmul	"Jolanthe von Hirschhorn"
Q111908000	Len	"Jolanthe von Hirschhorn"
Q111908000	Amul	"Yland von Hirschhorn"

# Q111948083  Hodierne|Helvise de Mondoubleau  ->  Hodierne de Mondoubleau   + Helvise de Mondoubleau
Q111948083	Lmul	"Hodierne de Mondoubleau"
Q111948083	Len	"Hodierne de Mondoubleau"
Q111948083	Amul	"Helvise de Mondoubleau"

# Q111954793  Karin|Birgitta Andersdotter av Venngarn  ->  Karin Andersdotter av Venngarn   + Birgitta Andersdotter av Venngarn
Q111954793	Lmul	"Karin Andersdotter av Venngarn"
Q111954793	Len	"Karin Andersdotter av Venngarn"
Q111954793	Amul	"Birgitta Andersdotter av Venngarn"

# Q111954852  Elisif|Elseby Pedersdatter af Ollinge, heiress of ¥llinge manor  ->  Elisif Pedersdatter af Ollinge, heiress of ¥llinge manor   + Elseby Pedersdatter af Ollinge, heiress of ¥llinge manor
Q111954852	Len	"Elisif Pedersdatter af Ollinge, heiress of ¥llinge manor"
Q111954852	Amul	"Elseby Pedersdatter af Ollinge, heiress of ¥llinge manor"

# Q111971823  Joan|Anne Thimbleby  ->  Joan Thimbleby   + Anne Thimbleby
Q111971823	Lmul	"Joan Thimbleby"
Q111971823	Len	"Joan Thimbleby"
Q111971823	Amul	"Anne Thimbleby"

# Q111971833  Mary|Elizabeth Donham (Dunham)  ->  Mary Donham (Dunham)   + Elizabeth Donham (Dunham)
Q111971833	Lmul	"Mary Donham (Dunham)"
Q111971833	Len	"Mary Donham (Dunham)"
Q111971833	Amul	"Elizabeth Donham (Dunham)"

# Q111971835  Bennet|Benedicta|Jane Foljambe  ->  Bennet Foljambe   + Benedicta Foljambe | Jane Foljambe
Q111971835	Lmul	"Bennet Foljambe"
Q111971835	Len	"Bennet Foljambe"
Q111971835	Amul	"Benedicta Foljambe"
Q111971835	Amul	"Jane Foljambe"

# Q111971965  James|John Rudston, of Hayton  ->  James Rudston, of Hayton   + John Rudston, of Hayton
Q111971965	Lmul	"James Rudston, of Hayton"
Q111971965	Len	"James Rudston, of Hayton"
Q111971965	Amul	"John Rudston, of Hayton"

# Q111971977  George|Gregory Heaton (Haton)  ->  George Heaton (Haton)   + Gregory Heaton (Haton)
Q111971977	Lmul	"George Heaton (Haton)"
Q111971977	Len	"George Heaton (Haton)"
Q111971977	Amul	"Gregory Heaton (Haton)"

# Q111989282  Wolf|Volf von Rantzau in Wittenberg  ->  Wolf von Rantzau in Wittenberg   + Volf von Rantzau in Wittenberg
Q111989282	Lmul	"Wolf von Rantzau in Wittenberg"
Q111989282	Len	"Wolf von Rantzau in Wittenberg"
Q111989282	Amul	"Volf von Rantzau in Wittenberg"

# Q111989314  Volf|Wolf Bentsen af Anfeldt (von Ahlefeldt), Lord of Noer  ->  Volf Bentsen af Anfeldt (von Ahlefeldt), Lord of Noer   + Wolf Bentsen af Anfeldt (von Ahlefeldt), Lord of Noer
Q111989314	Len	"Volf Bentsen af Anfeldt (von Ahlefeldt), Lord of Noer"
Q111989314	Amul	"Wolf Bentsen af Anfeldt (von Ahlefeldt), Lord of Noer"

# Q111989342  Wolf|Volf I Pogwisch  ->  Wolf I Pogwisch   + Volf I Pogwisch
Q111989342	Lmul	"Wolf I Pogwisch"
Q111989342	Len	"Wolf I Pogwisch"
Q111989342	Amul	"Volf I Pogwisch"

# Q111989552  noble NN of Pyöli|Salmenkylä  ->  noble NN of Pyöli   + noble NN of Salmenkylä
Q111989552	Lmul	"noble NN of Pyöli"
Q111989552	Len	"noble NN of Pyöli"
Q111989552	Amul	"noble NN of Salmenkylä"

# Q111989560  Yrjänä|Jyrki Siffredinpoika  ->  Yrjänä Siffredinpoika   + Jyrki Siffredinpoika
Q111989560	Lmul	"Yrjänä Siffredinpoika"
Q111989560	Len	"Yrjänä Siffredinpoika"
Q111989560	Amul	"Jyrki Siffredinpoika"

# Q111989806  squire Johannes|Jovan (Filpunpoika)  ->  squire Johannes (Filpunpoika)   + squire Jovan (Filpunpoika)
Q111989806	Lmul	"squire Johannes (Filpunpoika)"
Q111989806	Len	"squire Johannes (Filpunpoika)"
Q111989806	Amul	"squire Jovan (Filpunpoika)"

# Q112379933  Otes|Oates Nicholls, of the Isle of Guernsey  ->  Otes Nicholls, of the Isle of Guernsey   + Oates Nicholls, of the Isle of Guernsey
Q112379933	Lmul	"Otes Nicholls, of the Isle of Guernsey"
Q112379933	Len	"Otes Nicholls, of the Isle of Guernsey"
Q112379933	Amul	"Oates Nicholls, of the Isle of Guernsey"

# Q112379946  Robert|Henry Cavell  ->  Robert Cavell   + Henry Cavell
Q112379946	Lmul	"Robert Cavell"
Q112379946	Len	"Robert Cavell"
Q112379946	Amul	"Henry Cavell"

# Q112382774  Elizabeth|Margaret Babthorpe  ->  Elizabeth Babthorpe   + Margaret Babthorpe
Q112382774	Lmul	"Elizabeth Babthorpe"
Q112382774	Len	"Elizabeth Babthorpe"
Q112382774	Amul	"Margaret Babthorpe"

# Q112382797  Elizabeth|Margaret Rydness (de Redenis)  ->  Elizabeth Rydness (de Redenis)   + Margaret Rydness (de Redenis)
Q112382797	Lmul	"Elizabeth Rydness (de Redenis)"
Q112382797	Len	"Elizabeth Rydness (de Redenis)"
Q112382797	Amul	"Margaret Rydness (de Redenis)"

# Q112382824  John|Ralph Acclam  ->  John Acclam   + Ralph Acclam
Q112382824	Lmul	"John Acclam"
Q112382824	Len	"John Acclam"
Q112382824	Amul	"Ralph Acclam"

# Q112383256  Elizabeth|Margaret Etton  ->  Elizabeth Etton   + Margaret Etton
Q112383256	Lmul	"Elizabeth Etton"
Q112383256	Len	"Elizabeth Etton"
Q112383256	Amul	"Margaret Etton"

# Q112482869  Elizabeth Harries | Harriss  ->  Elizabeth Harries Harriss
Q112482869	Lmul	"Elizabeth Harries Harriss"
Q112482869	Len	"Elizabeth Harries Harriss"

# Q112484733  Elsbeth|Ffelis ferch Thomas ap Richard  ->  Elsbeth ferch Thomas ap Richard   + Ffelis ferch Thomas ap Richard
Q112484733	Lmul	"Elsbeth ferch Thomas ap Richard"
Q112484733	Len	"Elsbeth ferch Thomas ap Richard"
Q112484733	Amul	"Ffelis ferch Thomas ap Richard"

# Q112484749  Simkin|Symkin Hervey, of Herefordshire  ->  Simkin Hervey, of Herefordshire   + Symkin Hervey, of Herefordshire
Q112484749	Lmul	"Simkin Hervey, of Herefordshire"
Q112484749	Len	"Simkin Hervey, of Herefordshire"
Q112484749	Amul	"Symkin Hervey, of Herefordshire"

# Q112527461  burgher Hermanni van Börger|Borgen, town councillor of Viipuri  ->  burgher Hermanni van Börger town councillor of Viipuri   + burgher Hermanni van Borgen, town councillor of Viipuri
Q112527461	Lmul	"burgher Hermanni van Börger town councillor of Viipuri"
Q112527461	Len	"burgher Hermanni van Börger town councillor of Viipuri"
Q112527461	Amul	"burgher Hermanni van Borgen, town councillor of Viipuri"

# Q112528801  Margred|Marsli Salusbury  ->  Margred Salusbury   + Marsli Salusbury
Q112528801	Lmul	"Margred Salusbury"
Q112528801	Len	"Margred Salusbury"
Q112528801	Amul	"Marsli Salusbury"

# Q112530707  Elizabeth|Catherine Stanley, of Ewloe  ->  Elizabeth Stanley, of Ewloe   + Catherine Stanley, of Ewloe
Q112530707	Lmul	"Elizabeth Stanley, of Ewloe"
Q112530707	Len	"Elizabeth Stanley, of Ewloe"
Q112530707	Amul	"Catherine Stanley, of Ewloe"

# Q112533627  Mawd Wen|Margred ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth  ->  Mawd Wen ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth   + Mawd Margred ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth
Q112533627	Lmul	"Mawd Wen ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth"
Q112533627	Len	"Mawd Wen ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth"
Q112533627	Amul	"Mawd Margred ferch Dafydd Llwyd ab Ieuan ap Gruffudd of Broniarth"

# Q112533684  Elis ferch John|Robert Grey  ->  Elis ferch John Grey   + Elis ferch Robert Grey
Q112533684	Lmul	"Elis ferch John Grey"
Q112533684	Len	"Elis ferch John Grey"
Q112533684	Amul	"Elis ferch Robert Grey"

# Q112533686  John|Robert Grey  ->  John Grey   + Robert Grey
Q112533686	Lmul	"John Grey"
Q112533686	Len	"John Grey"
Q112533686	Amul	"Robert Grey"

# Q112573821  Gilles|Gille|Egidia Mauduit  ->  Gilles Mauduit   + Gille Mauduit | Egidia Mauduit
Q112573821	Lmul	"Gilles Mauduit"
Q112573821	Len	"Gilles Mauduit"
Q112573821	Amul	"Gille Mauduit"
Q112573821	Amul	"Egidia Mauduit"

# Q112610807  Hari|Harry ap Thomas ap Philip of Cwmtudu  ->  Hari ap Thomas ap Philip of Cwmtudu   + Harry ap Thomas ap Philip of Cwmtudu
Q112610807	Lmul	"Hari ap Thomas ap Philip of Cwmtudu"
Q112610807	Len	"Hari ap Thomas ap Philip of Cwmtudu"
Q112610807	Amul	"Harry ap Thomas ap Philip of Cwmtudu"

# Q112610890  Margred|Mawd ferch Jenkin ab Owain ab Einion  ->  Margred ferch Jenkin ab Owain ab Einion   + Mawd ferch Jenkin ab Owain ab Einion
Q112610890	Lmul	"Margred ferch Jenkin ab Owain ab Einion"
Q112610890	Len	"Margred ferch Jenkin ab Owain ab Einion"
Q112610890	Amul	"Mawd ferch Jenkin ab Owain ab Einion"

# Q112611044  Sir John|Shane Fitzgerald, of Cloncurry, Co. Kildare  ->  Sir John Fitzgerald, of Cloncurry, Co. Kildare   + Sir Shane Fitzgerald, of Cloncurry, Co. Kildare
Q112611044	Lmul	"Sir John Fitzgerald, of Cloncurry, Co. Kildare"
Q112611044	Len	"Sir John Fitzgerald, of Cloncurry, Co. Kildare"
Q112611044	Amul	"Sir Shane Fitzgerald, of Cloncurry, Co. Kildare"

# Q112643765  Hywel Clun|Colunwy ap Meurig ap Maredudd ap Madog of Clun  ->  Hywel Clun ap Meurig ap Maredudd ap Madog of Clun   + Hywel Colunwy ap Meurig ap Maredudd ap Madog of Clun
Q112643765	Lmul	"Hywel Clun ap Meurig ap Maredudd ap Madog of Clun"
Q112643765	Len	"Hywel Clun ap Meurig ap Maredudd ap Madog of Clun"
Q112643765	Amul	"Hywel Colunwy ap Meurig ap Maredudd ap Madog of Clun"

# Q112644947  Aert|Aernout van Erp  ->  Aert van Erp   + Aernout van Erp
Q112644947	Lmul	"Aert van Erp"
Q112644947	Len	"Aert van Erp"
Q112644947	Amul	"Aernout van Erp"

# Q112943053  William|John Barrett, of Stanford Dingley  ->  William Barrett, of Stanford Dingley   + John Barrett, of Stanford Dingley
Q112943053	Lmul	"William Barrett, of Stanford Dingley"
Q112943053	Len	"William Barrett, of Stanford Dingley"
Q112943053	Amul	"John Barrett, of Stanford Dingley"

# Q112961995  Honor|Honora O'Brien  ->  Honor O'Brien   + Honora O'Brien
Q112961995	Lmul	"Honor O'Brien"
Q112961995	Len	"Honor O'Brien"
Q112961995	Amul	"Honora O'Brien"

# Q112962027  Julia|Sile O'Mulryan (or O'Ryan), of Sulloghode  ->  Julia O'Mulryan (or O'Ryan), of Sulloghode   + Sile O'Mulryan (or O'Ryan), of Sulloghode
Q112962027	Len	"Julia O'Mulryan (or O'Ryan), of Sulloghode"
Q112962027	Amul	"Sile O'Mulryan (or O'Ryan), of Sulloghode"

# Q112962352  Orlath|Aurnia MacCarthy  ->  Orlath MacCarthy   + Aurnia MacCarthy
Q112962352	Lmul	"Orlath MacCarthy"
Q112962352	Len	"Orlath MacCarthy"
Q112962352	Amul	"Aurnia MacCarthy"

# Q112962354  Edaoin|Edina  ->  Edaoin   + Edina
Q112962354	Lmul	"Edaoin"
Q112962354	Len	"Edaoin"
Q112962354	Amul	"Edina"

# Q112962362  Saiv|Sadhbh (MacCarthy)  ->  Saiv (MacCarthy)   + Sadhbh (MacCarthy)
Q112962362	Len	"Saiv (MacCarthy)"
Q112962362	Amul	"Sadhbh (MacCarthy)"

# Q112964249  Marcia|Maria Nesbitt  ->  Marcia Nesbitt   + Maria Nesbitt
Q112964249	Lmul	"Marcia Nesbitt"
Q112964249	Len	"Marcia Nesbitt"
Q112964249	Amul	"Maria Nesbitt"

# Q112968447  Birgitte|Barbara of Lehtse  ->  Birgitte of Lehtse   + Barbara of Lehtse
Q112968447	Lmul	"Birgitte of Lehtse"
Q112968447	Len	"Birgitte of Lehtse"
Q112968447	Amul	"Barbara of Lehtse"

# Q112968501  noble Aleit|Hel Brakel  ->  noble Aleit Brakel   + noble Hel Brakel
Q112968501	Lmul	"noble Aleit Brakel"
Q112968501	Len	"noble Aleit Brakel"
Q112968501	Amul	"noble Hel Brakel"

# Q112968651  magnate Vinrik|Indrek Live, lord of Parmila  ->  magnate Vinrik Live, lord of Parmila   + magnate Indrek Live, lord of Parmila
Q112968651	Lmul	"magnate Vinrik Live, lord of Parmila"
Q112968651	Len	"magnate Vinrik Live, lord of Parmila"
Q112968651	Amul	"magnate Indrek Live, lord of Parmila"

# Q112968808  Lasse|Lauri Matinpoika of Teitomi, Lord of Kuuskoski  ->  Lasse Matinpoika of Teitomi, Lord of Kuuskoski   + Lauri Matinpoika of Teitomi, Lord of Kuuskoski
Q112968808	Lmul	"Lasse Matinpoika of Teitomi, Lord of Kuuskoski"
Q112968808	Len	"Lasse Matinpoika of Teitomi, Lord of Kuuskoski"
Q112968808	Amul	"Lauri Matinpoika of Teitomi, Lord of Kuuskoski"

# Q112968832  Sir Alexandair|Alexander Moray (a Moireabh), Laird of Abercairny  ->  Sir Alexandair Moray (a Moireabh), Laird of Abercairny   + Sir Alexander Moray (a Moireabh), Laird of Abercairny
Q112968832	Lmul	"Sir Alexandair Moray (a Moireabh), Laird of Abercairny"
Q112968832	Len	"Sir Alexandair Moray (a Moireabh), Laird of Abercairny"
Q112968832	Amul	"Sir Alexander Moray (a Moireabh), Laird of Abercairny"

# Q112969030  Ada|Ela  ->  Ada   + Ela
Q112969030	Lmul	"Ada"
Q112969030	Len	"Ada"
Q112969030	Amul	"Ela"

# Q112970968  Metta|Martta Rekontytär of Kyynämäki, lady of Lemu manor  ->  Metta Rekontytär of Kyynämäki, lady of Lemu manor   + Martta Rekontytär of Kyynämäki, lady of Lemu manor
Q112970968	Lmul	"Metta Rekontytär of Kyynämäki, lady of Lemu manor"
Q112970968	Len	"Metta Rekontytär of Kyynämäki, lady of Lemu manor"
Q112970968	Amul	"Martta Rekontytär of Kyynämäki, lady of Lemu manor"

# Q112974561  Borante|Brant Paykull  ->  Borante Paykull   + Brant Paykull
Q112974561	Lmul	"Borante Paykull"
Q112974561	Len	"Borante Paykull"
Q112974561	Amul	"Brant Paykull"

# Q113040349  Asser|Asscher  ->  Asser   + Asscher
Q113040349	Lmul	"Asser"
Q113040349	Len	"Asser"
Q113040349	Amul	"Asscher"

# Q113295283  Magdalena|Jacomina van Sloten  ->  Magdalena van Sloten   + Jacomina van Sloten
Q113295283	Lmul	"Magdalena van Sloten"
Q113295283	Len	"Magdalena van Sloten"
Q113295283	Amul	"Jacomina van Sloten"

# Q113296293  Maria|Agatha van Loon  ->  Maria van Loon   + Agatha van Loon
Q113296293	Lmul	"Maria van Loon"
Q113296293	Len	"Maria van Loon"
Q113296293	Amul	"Agatha van Loon"

# Q113503660  Bertold|Frantz Kempe  ->  Bertold Kempe   + Frantz Kempe
Q113503660	Lmul	"Bertold Kempe"
Q113503660	Len	"Bertold Kempe"
Q113503660	Amul	"Frantz Kempe"

# Q113503862  Adelheit|Alheit von Bardewick  ->  Adelheit von Bardewick   + Alheit von Bardewick
Q113503862	Lmul	"Adelheit von Bardewick"
Q113503862	Len	"Adelheit von Bardewick"
Q113503862	Amul	"Alheit von Bardewick"

# Q113503954  Taleke|Thalia Thürkow  ->  Taleke Thürkow   + Thalia Thürkow
Q113503954	Lmul	"Taleke Thürkow"
Q113503954	Len	"Taleke Thürkow"
Q113503954	Amul	"Thalia Thürkow"

# Q113883089  Gabriel Pallestreli|Pallastrelli  ->  Gabriel Pallestreli   + Gabriel Pallastrelli
Q113883089	Lmul	"Gabriel Pallestreli"
Q113883089	Len	"Gabriel Pallestreli"
Q113883089	Amul	"Gabriel Pallastrelli"

# Q113883090  Bertolina Banfortes|Bracciforte  ->  Bertolina Banfortes   + Bertolina Bracciforte
Q113883090	Lmul	"Bertolina Banfortes"
Q113883090	Len	"Bertolina Banfortes"
Q113883090	Amul	"Bertolina Bracciforte"

# Q113933173  Elizabeth Strangways, of Skelton|Ketton  ->  Elizabeth Strangways, of Skelton   + Elizabeth Strangways, of Ketton
Q113933173	Lmul	"Elizabeth Strangways, of Skelton"
Q113933173	Len	"Elizabeth Strangways, of Skelton"
Q113933173	Amul	"Elizabeth Strangways, of Ketton"

# Q113933199  Matilda|Maud  ->  Matilda   + Maud
Q113933199	Lmul	"Matilda"
Q113933199	Len	"Matilda"
Q113933199	Amul	"Maud"

# Q113958021  John|Thomas Chelmington, of Chelmington  ->  John Chelmington, of Chelmington   + Thomas Chelmington, of Chelmington
Q113958021	Lmul	"John Chelmington, of Chelmington"
Q113958021	Len	"John Chelmington, of Chelmington"
Q113958021	Amul	"Thomas Chelmington, of Chelmington"

# Q115538516  Alice|Agnes Fiscare  ->  Alice Fiscare   + Agnes Fiscare
Q115538516	Lmul	"Alice Fiscare"
Q115538516	Len	"Alice Fiscare"
Q115538516	Amul	"Agnes Fiscare"

# Q115627005  Sidney|Sydney Horace Truss  ->  Sidney Horace Truss   + Sydney Horace Truss
Q115627005	Lmul	"Sidney Horace Truss"
Q115627005	Len	"Sidney Horace Truss"
Q115627005	Amul	"Sydney Horace Truss"

# Q115633768  Marie Madeleine|Michelle de Jauche de Mastaing  ->  Marie Madeleine de Jauche de Mastaing   + Marie Michelle de Jauche de Mastaing
Q115633768	Lmul	"Marie Madeleine de Jauche de Mastaing"
Q115633768	Len	"Marie Madeleine de Jauche de Mastaing"
Q115633768	Amul	"Marie Michelle de Jauche de Mastaing"

# Q115634021  Jeanne|Elisabeth de Haveskerke, Dame de Fléchin  ->  Jeanne de Haveskerke, Dame de Fléchin   + Elisabeth de Haveskerke, Dame de Fléchin
Q115634021	Len	"Jeanne de Haveskerke, Dame de Fléchin"
Q115634021	Amul	"Elisabeth de Haveskerke, Dame de Fléchin"

# Q115634088  Alix|Aleidis de Hainault  ->  Alix de Hainault   + Aleidis de Hainault
Q115634088	Lmul	"Alix de Hainault"
Q115634088	Len	"Alix de Hainault"
Q115634088	Amul	"Aleidis de Hainault"

# Q115634423  Jeanne|Colette Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte  ->  Jeanne Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte   + Colette Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte
Q115634423	Lmul	"Jeanne Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte"
Q115634423	Len	"Jeanne Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte"
Q115634423	Amul	"Colette Catelaine, Chastellain dit de Bosquuiel, Dame de Quiercy-la-Motte"

# Q115714652  Anne|Amicia  ->  Anne   + Amicia
Q115714652	Lmul	"Anne"
Q115714652	Len	"Anne"
Q115714652	Amul	"Amicia"

# Q115714685  Mary|Sarah Clare  ->  Mary Clare   + Sarah Clare
Q115714685	Lmul	"Mary Clare"
Q115714685	Len	"Mary Clare"
Q115714685	Amul	"Sarah Clare"

# Q115714699  Sir Thomas|John Gerbridge  ->  Sir Thomas Gerbridge   + Sir John Gerbridge
Q115714699	Lmul	"Sir Thomas Gerbridge"
Q115714699	Len	"Sir Thomas Gerbridge"
Q115714699	Amul	"Sir John Gerbridge"

# Q115714719  Walter|Richard Paston  ->  Walter Paston   + Richard Paston
Q115714719	Lmul	"Walter Paston"
Q115714719	Len	"Walter Paston"
Q115714719	Amul	"Richard Paston"

# Q115714721  Robert|Rafe Paston  ->  Robert Paston   + Rafe Paston
Q115714721	Lmul	"Robert Paston"
Q115714721	Len	"Robert Paston"
Q115714721	Amul	"Rafe Paston"

# Q115714722  Wolstanus|William Paston  ->  Wolstanus Paston   + William Paston
Q115714722	Lmul	"Wolstanus Paston"
Q115714722	Len	"Wolstanus Paston"
Q115714722	Amul	"William Paston"

# Q115714723  Wolstane|William Paston, of Paston, Norfolk  ->  Wolstane Paston, of Paston, Norfolk   + William Paston, of Paston, Norfolk
Q115714723	Lmul	"Wolstane Paston, of Paston, Norfolk"
Q115714723	Len	"Wolstane Paston, of Paston, Norfolk"
Q115714723	Amul	"William Paston, of Paston, Norfolk"

# Q115870545  Klas|Niklas Hansson Prytz  ->  Klas Hansson Prytz   + Niklas Hansson Prytz
Q115870545	Lmul	"Klas Hansson Prytz"
Q115870545	Len	"Klas Hansson Prytz"
Q115870545	Amul	"Niklas Hansson Prytz"

# Q115871027  Berent|Päärni Steen von Steenhuse  ->  Berent Steen von Steenhuse   + Päärni Steen von Steenhuse
Q115871027	Len	"Berent Steen von Steenhuse"
Q115871027	Amul	"Päärni Steen von Steenhuse"

# Q115958776  Anne|Amy Sapcotts  ->  Anne Sapcotts   + Amy Sapcotts
Q115958776	Lmul	"Anne Sapcotts"
Q115958776	Len	"Anne Sapcotts"
Q115958776	Amul	"Amy Sapcotts"

# Q115974127  burgher Jasperi|Kasperi Aarni Poeg Reiheri  ->  burgher Jasperi Aarni Poeg Reiheri   + burgher Kasperi Aarni Poeg Reiheri
Q115974127	Lmul	"burgher Jasperi Aarni Poeg Reiheri"
Q115974127	Len	"burgher Jasperi Aarni Poeg Reiheri"
Q115974127	Amul	"burgher Kasperi Aarni Poeg Reiheri"

# Q116004200  Aimée|Agnès de Corgenon, dame de Meillonas-en-Bresse  ->  Aimée de Corgenon, dame de Meillonas-en-Bresse   + Agnès de Corgenon, dame de Meillonas-en-Bresse
Q116004200	Lmul	"Aimée de Corgenon, dame de Meillonas-en-Bresse"
Q116004200	Len	"Aimée de Corgenon, dame de Meillonas-en-Bresse"
Q116004200	Amul	"Agnès de Corgenon, dame de Meillonas-en-Bresse"

# Q116004711  Ida|Ita, Gräfin von Toggenburg  ->  Ida Gräfin von Toggenburg   + Ita, Gräfin von Toggenburg
Q116004711	Lmul	"Ida Gräfin von Toggenburg"
Q116004711	Len	"Ida Gräfin von Toggenburg"
Q116004711	Amul	"Ita, Gräfin von Toggenburg"

# Q116004877  Mena|Imagina, Gräfin von Leiningen  ->  Mena Gräfin von Leiningen   + Imagina, Gräfin von Leiningen
Q116004877	Lmul	"Mena Gräfin von Leiningen"
Q116004877	Len	"Mena Gräfin von Leiningen"
Q116004877	Amul	"Imagina, Gräfin von Leiningen"

# Q116005200  Brita|Bretonne  ->  Brita   + Bretonne
Q116005200	Lmul	"Brita"
Q116005200	Len	"Brita"
Q116005200	Amul	"Bretonne"

# Q116005322  Servus Dei|Sluga Bozhji izh Nevna  ->  Servus Dei Bozhji izh Nevna   + Servus Sluga Bozhji izh Nevna
Q116005322	Lmul	"Servus Dei Bozhji izh Nevna"
Q116005322	Len	"Servus Dei Bozhji izh Nevna"
Q116005322	Amul	"Servus Sluga Bozhji izh Nevna"

# Q116005399  Elisabeth|Isabelle d'Arquennes, Dame d'Arquennes et du Petit-Roeulx  ->  Elisabeth d'Arquennes, Dame d'Arquennes et du Petit-Roeulx   + Isabelle d'Arquennes, Dame d'Arquennes et du Petit-Roeulx
Q116005399	Lmul	"Elisabeth d'Arquennes, Dame d'Arquennes et du Petit-Roeulx"
Q116005399	Len	"Elisabeth d'Arquennes, Dame d'Arquennes et du Petit-Roeulx"
Q116005399	Amul	"Isabelle d'Arquennes, Dame d'Arquennes et du Petit-Roeulx"

# Q116005562  Agnes|Jeanne du Plessis  ->  Agnes du Plessis   + Jeanne du Plessis
Q116005562	Lmul	"Agnes du Plessis"
Q116005562	Len	"Agnes du Plessis"
Q116005562	Amul	"Jeanne du Plessis"

# Q116005597  Isabella|Elisabeth von Rappoltstein, Dame de Port-sur-Saone et de Vignory  ->  Isabella von Rappoltstein, Dame de Port-sur-Saone et de Vignory   + Elisabeth von Rappoltstein, Dame de Port-sur-Saone et de Vignory
Q116005597	Lmul	"Isabella von Rappoltstein, Dame de Port-sur-Saone et de Vignory"
Q116005597	Len	"Isabella von Rappoltstein, Dame de Port-sur-Saone et de Vignory"
Q116005597	Amul	"Elisabeth von Rappoltstein, Dame de Port-sur-Saone et de Vignory"

# Q116005726  Mahaut|Michaulde de Sampy  ->  Mahaut de Sampy   + Michaulde de Sampy
Q116005726	Lmul	"Mahaut de Sampy"
Q116005726	Len	"Mahaut de Sampy"
Q116005726	Amul	"Michaulde de Sampy"

# Q116006099  Peter|Pierre Odart, Seigneur de Verrières  ->  Peter Odart, Seigneur de Verrières   + Pierre Odart, Seigneur de Verrières
Q116006099	Len	"Peter Odart, Seigneur de Verrières"
Q116006099	Amul	"Pierre Odart, Seigneur de Verrières"

# Q116006478  Cuno|Kuno von Laiming  ->  Cuno von Laiming   + Kuno von Laiming
Q116006478	Lmul	"Cuno von Laiming"
Q116006478	Len	"Cuno von Laiming"
Q116006478	Amul	"Kuno von Laiming"

# Q116006508  Anna|Agnes von Wunstorf  ->  Anna von Wunstorf   + Agnes von Wunstorf
Q116006508	Len	"Anna von Wunstorf"
Q116006508	Amul	"Agnes von Wunstorf"

# Q116006755  Gottfried|Gotzmann von Staufen  ->  Gottfried von Staufen   + Gotzmann von Staufen
Q116006755	Len	"Gottfried von Staufen"
Q116006755	Amul	"Gotzmann von Staufen"

# Q116006759  Elisabeth|Elsine Münch von Landskron  ->  Elisabeth Münch von Landskron   + Elsine Münch von Landskron
Q116006759	Lmul	"Elisabeth Münch von Landskron"
Q116006759	Len	"Elisabeth Münch von Landskron"
Q116006759	Amul	"Elsine Münch von Landskron"

# Q116006773  Benedikta|Agnes von Rötteln  ->  Benedikta von Rötteln   + Agnes von Rötteln
Q116006773	Lmul	"Benedikta von Rötteln"
Q116006773	Len	"Benedikta von Rötteln"
Q116006773	Amul	"Agnes von Rötteln"

# Q116007409  Orsina|Ursula d'Este  ->  Orsina d'Este   + Ursula d'Este
Q116007409	Lmul	"Orsina d'Este"
Q116007409	Len	"Orsina d'Este"
Q116007409	Amul	"Ursula d'Este"

# Q116007417  György|Georg, Graf Frangepan de Cetinje  ->  György Graf Frangepan de Cetinje   + Georg, Graf Frangepan de Cetinje
Q116007417	Len	"György Graf Frangepan de Cetinje"
Q116007417	Amul	"Georg, Graf Frangepan de Cetinje"

# Q116007669  Clara|Walpurga von Stadion  ->  Clara von Stadion   + Walpurga von Stadion
Q116007669	Lmul	"Clara von Stadion"
Q116007669	Len	"Clara von Stadion"
Q116007669	Amul	"Walpurga von Stadion"

# Q116007677  Conrad|Konrad von Rietheim (Riedheim)  ->  Conrad von Rietheim (Riedheim)   + Konrad von Rietheim (Riedheim)
Q116007677	Lmul	"Conrad von Rietheim (Riedheim)"
Q116007677	Len	"Conrad von Rietheim (Riedheim)"
Q116007677	Amul	"Konrad von Rietheim (Riedheim)"

# Q116007690  Stephen|Stephan 'der Aeltere' Volkra von Dornach und Greillenstein  ->  Stephen 'der Aeltere' Volkra von Dornach und Greillenstein   + Stephan 'der Aeltere' Volkra von Dornach und Greillenstein
Q116007690	Lmul	"Stephen 'der Aeltere' Volkra von Dornach und Greillenstein"
Q116007690	Len	"Stephen 'der Aeltere' Volkra von Dornach und Greillenstein"
Q116007690	Amul	"Stephan 'der Aeltere' Volkra von Dornach und Greillenstein"

# Q116025838  Katherine|Catherine|Dorothy Bullock  ->  Katherine Bullock   + Catherine Bullock | Dorothy Bullock
Q116025838	Lmul	"Katherine Bullock"
Q116025838	Len	"Katherine Bullock"
Q116025838	Amul	"Catherine Bullock"
Q116025838	Amul	"Dorothy Bullock"

# Q116026132  Amy|Agnes Tresithney  ->  Amy Tresithney   + Agnes Tresithney
Q116026132	Lmul	"Amy Tresithney"
Q116026132	Len	"Amy Tresithney"
Q116026132	Amul	"Agnes Tresithney"

# Q116026137  Anne|Jane|Joan Tregonnan (Tregennow)  ->  Anne Tregonnan (Tregennow)   + Jane Tregonnan (Tregennow) | Joan Tregonnan (Tregennow)
Q116026137	Lmul	"Anne Tregonnan (Tregennow)"
Q116026137	Len	"Anne Tregonnan (Tregennow)"
Q116026137	Amul	"Jane Tregonnan (Tregennow)"
Q116026137	Amul	"Joan Tregonnan (Tregennow)"

# Q116026425  John|Jenkin Berry, of Berryarbor  ->  John Berry, of Berryarbor   + Jenkin Berry, of Berryarbor
Q116026425	Lmul	"John Berry, of Berryarbor"
Q116026425	Len	"John Berry, of Berryarbor"
Q116026425	Amul	"Jenkin Berry, of Berryarbor"

# Q116026434  Joan|Jane  ->  Joan   + Jane
Q116026434	Lmul	"Joan"
Q116026434	Len	"Joan"
Q116026434	Amul	"Jane"

# Q116026514  Petrenelle|Parnell Cheney, of Warbleton  ->  Petrenelle Cheney, of Warbleton   + Parnell Cheney, of Warbleton
Q116026514	Lmul	"Petrenelle Cheney, of Warbleton"
Q116026514	Len	"Petrenelle Cheney, of Warbleton"
Q116026514	Amul	"Parnell Cheney, of Warbleton"

# Q116026701  Felicia|Phillis Milward  ->  Felicia Milward   + Phillis Milward
Q116026701	Lmul	"Felicia Milward"
Q116026701	Len	"Felicia Milward"
Q116026701	Amul	"Phillis Milward"

# Q116026714  Ellen|Eleanor Clayton  ->  Ellen Clayton   + Eleanor Clayton
Q116026714	Lmul	"Ellen Clayton"
Q116026714	Len	"Ellen Clayton"
Q116026714	Amul	"Eleanor Clayton"

# Q116026761  Ann|Alice Kniveton  ->  Ann Kniveton   + Alice Kniveton
Q116026761	Lmul	"Ann Kniveton"
Q116026761	Len	"Ann Kniveton"
Q116026761	Amul	"Alice Kniveton"

# Q116026762  Felicia|Alicia Savage  ->  Felicia Savage   + Alicia Savage
Q116026762	Lmul	"Felicia Savage"
Q116026762	Len	"Felicia Savage"
Q116026762	Amul	"Alicia Savage"

# Q116026945  Sir John|William Creedy, of Creedy, Devon  ->  Sir John Creedy, of Creedy, Devon   + Sir William Creedy, of Creedy, Devon
Q116026945	Lmul	"Sir John Creedy, of Creedy, Devon"
Q116026945	Len	"Sir John Creedy, of Creedy, Devon"
Q116026945	Amul	"Sir William Creedy, of Creedy, Devon"

# Q116027272  Margery|Margaret Games, of Aberbrân  ->  Margery Games, of Aberbrân   + Margaret Games, of Aberbrân
Q116027272	Lmul	"Margery Games, of Aberbrân"
Q116027272	Len	"Margery Games, of Aberbrân"
Q116027272	Amul	"Margaret Games, of Aberbrân"

# Q116028868  Sir Robert|John Mauteby, of Mauteby  ->  Sir Robert Mauteby, of Mauteby   + Sir John Mauteby, of Mauteby
Q116028868	Lmul	"Sir Robert Mauteby, of Mauteby"
Q116028868	Len	"Sir Robert Mauteby, of Mauteby"
Q116028868	Amul	"Sir John Mauteby, of Mauteby"

# Q116028966  Anne|Agnes Cranmer  ->  Anne Cranmer   + Agnes Cranmer
Q116028966	Lmul	"Anne Cranmer"
Q116028966	Len	"Anne Cranmer"
Q116028966	Amul	"Agnes Cranmer"

# Q116029103  Robert|John Arthington  ->  Robert Arthington   + John Arthington
Q116029103	Lmul	"Robert Arthington"
Q116029103	Len	"Robert Arthington"
Q116029103	Amul	"John Arthington"

# Q116029114  Sir Edmund|Edward Neville, of Liversedge  ->  Sir Edmund Neville, of Liversedge   + Sir Edward Neville, of Liversedge
Q116029114	Lmul	"Sir Edmund Neville, of Liversedge"
Q116029114	Len	"Sir Edmund Neville, of Liversedge"
Q116029114	Amul	"Sir Edward Neville, of Liversedge"

# Q116029122  Ellen|Anne Molyneux  ->  Ellen Molyneux   + Anne Molyneux
Q116029122	Lmul	"Ellen Molyneux"
Q116029122	Len	"Ellen Molyneux"
Q116029122	Amul	"Anne Molyneux"

# Q116029157  Sir Edward|Edmund Molyneux, of Hawton & Teversall  ->  Sir Edward Molyneux, of Hawton & Teversall   + Sir Edmund Molyneux, of Hawton & Teversall
Q116029157	Lmul	"Sir Edward Molyneux, of Hawton & Teversall"
Q116029157	Len	"Sir Edward Molyneux, of Hawton & Teversall"
Q116029157	Amul	"Sir Edmund Molyneux, of Hawton & Teversall"

# Q116029866  Mena|Imagina von Bickenbach  ->  Mena von Bickenbach   + Imagina von Bickenbach
Q116029866	Lmul	"Mena von Bickenbach"
Q116029866	Len	"Mena von Bickenbach"
Q116029866	Amul	"Imagina von Bickenbach"

# Q116031035  Jeanne|Jeannette de Pesmes, Dame de Pesmes  ->  Jeanne de Pesmes, Dame de Pesmes   + Jeannette de Pesmes, Dame de Pesmes
Q116031035	Len	"Jeanne de Pesmes, Dame de Pesmes"
Q116031035	Amul	"Jeannette de Pesmes, Dame de Pesmes"

# Q116031091  Elisabeth|Ermengarde  ->  Elisabeth   + Ermengarde
Q116031091	Lmul	"Elisabeth"
Q116031091	Len	"Elisabeth"
Q116031091	Amul	"Ermengarde"

# Q116031316  Roger de Barclay|Berkeley  ->  Roger de Barclay   + Roger de Berkeley
Q116031316	Lmul	"Roger de Barclay"
Q116031316	Len	"Roger de Barclay"
Q116031316	Amul	"Roger de Berkeley"

# Q116032803  Georg|Jürgen von Ketteler  ->  Georg von Ketteler   + Jürgen von Ketteler
Q116032803	Lmul	"Georg von Ketteler"
Q116032803	Len	"Georg von Ketteler"
Q116032803	Amul	"Jürgen von Ketteler"

# Q116033442  Richard|Richer Gordon  ->  Richard Gordon   + Richer Gordon
Q116033442	Lmul	"Richard Gordon"
Q116033442	Len	"Richard Gordon"
Q116033442	Amul	"Richer Gordon"

# Q116039897  Irmgard|Isengard von Fleisch von Cleeberg  ->  Irmgard von Fleisch von Cleeberg   + Isengard von Fleisch von Cleeberg
Q116039897	Lmul	"Irmgard von Fleisch von Cleeberg"
Q116039897	Len	"Irmgard von Fleisch von Cleeberg"
Q116039897	Amul	"Isengard von Fleisch von Cleeberg"

# Q116040991  Ricold|Rijcout de Borchgrave  ->  Ricold de Borchgrave   + Rijcout de Borchgrave
Q116040991	Lmul	"Ricold de Borchgrave"
Q116040991	Len	"Ricold de Borchgrave"
Q116040991	Amul	"Rijcout de Borchgrave"

# Q116041838  Walter|Gauthier de Mortagne, Castellan of Tournai, Sire de Mortagne  ->  Walter de Mortagne, Castellan of Tournai, Sire de Mortagne   + Gauthier de Mortagne, Castellan of Tournai, Sire de Mortagne
Q116041838	Lmul	"Walter de Mortagne, Castellan of Tournai, Sire de Mortagne"
Q116041838	Len	"Walter de Mortagne, Castellan of Tournai, Sire de Mortagne"
Q116041838	Amul	"Gauthier de Mortagne, Castellan of Tournai, Sire de Mortagne"

# Q116046454  Hans|Jan van der Merct  ->  Hans van der Merct   + Jan van der Merct
Q116046454	Lmul	"Hans van der Merct"
Q116046454	Len	"Hans van der Merct"
Q116046454	Amul	"Jan van der Merct"

# Q116046898  Maria|Mayken Helena Lievensdr. de Huybert van Zuidlant  ->  Maria Helena Lievensdr. de Huybert van Zuidlant   + Mayken Helena Lievensdr. de Huybert van Zuidlant
Q116046898	Lmul	"Maria Helena Lievensdr. de Huybert van Zuidlant"
Q116046898	Len	"Maria Helena Lievensdr. de Huybert van Zuidlant"
Q116046898	Amul	"Mayken Helena Lievensdr. de Huybert van Zuidlant"

# Q116046900  Aefgen|Eva van Zwaanswijck  ->  Aefgen van Zwaanswijck   + Eva van Zwaanswijck
Q116046900	Lmul	"Aefgen van Zwaanswijck"
Q116046900	Len	"Aefgen van Zwaanswijck"
Q116046900	Amul	"Eva van Zwaanswijck"

# Q116052765  Ffrwdwr ap Gwrfawr|Morfawr ap Gadeon ab Eudaf Hên  ->  Ffrwdwr ap Gwrfawr ap Gadeon ab Eudaf Hên   + Ffrwdwr ap Morfawr ap Gadeon ab Eudaf Hên
Q116052765	Len	"Ffrwdwr ap Gwrfawr ap Gadeon ab Eudaf Hên"
Q116052765	Amul	"Ffrwdwr ap Morfawr ap Gadeon ab Eudaf Hên"

# Q116052955  Bleiddig|Bledri  ->  Bleiddig   + Bledri
Q116052955	Lmul	"Bleiddig"
Q116052955	Len	"Bleiddig"
Q116052955	Amul	"Bledri"

# Q116052980  Tegwas ap Gwyn ab Aelan|Aelaw ab Alser of Abergwaun  ->  Tegwas ap Gwyn ab Aelan ab Alser of Abergwaun   + Tegwas ap Gwyn ab Aelaw ab Alser of Abergwaun
Q116052980	Lmul	"Tegwas ap Gwyn ab Aelan ab Alser of Abergwaun"
Q116052980	Len	"Tegwas ap Gwyn ab Aelan ab Alser of Abergwaun"
Q116052980	Amul	"Tegwas ap Gwyn ab Aelaw ab Alser of Abergwaun"

# Q116052981  Gwyn ab Aelan|Aelaw ab Alser ap Tudwal Gloff  ->  Gwyn ab Aelan ab Alser ap Tudwal Gloff   + Gwyn ab Aelaw ab Alser ap Tudwal Gloff
Q116052981	Lmul	"Gwyn ab Aelan ab Alser ap Tudwal Gloff"
Q116052981	Len	"Gwyn ab Aelan ab Alser ap Tudwal Gloff"
Q116052981	Amul	"Gwyn ab Aelaw ab Alser ap Tudwal Gloff"

# Q116053135  Thomas|John Groves  ->  Thomas Groves   + John Groves
Q116053135	Lmul	"Thomas Groves"
Q116053135	Len	"Thomas Groves"
Q116053135	Amul	"John Groves"

# Q116053146  Sybilla|Sibella  ->  Sybilla   + Sibella
Q116053146	Lmul	"Sybilla"
Q116053146	Len	"Sybilla"
Q116053146	Amul	"Sibella"

# Q116053651  Maria|Costanza de Valcarcel  ->  Maria de Valcarcel   + Costanza de Valcarcel
Q116053651	Lmul	"Maria de Valcarcel"
Q116053651	Len	"Maria de Valcarcel"
Q116053651	Amul	"Costanza de Valcarcel"

# Q116053988  Zeno|Zeyno|Seyno Mulert  ->  Zeno Mulert   + Zeyno Mulert | Seyno Mulert
Q116053988	Lmul	"Zeno Mulert"
Q116053988	Len	"Zeno Mulert"
Q116053988	Amul	"Zeyno Mulert"
Q116053988	Amul	"Seyno Mulert"

# Q116054221  Anne|Agnes Lawe, of Wigston Magna  ->  Anne Lawe, of Wigston Magna   + Agnes Lawe, of Wigston Magna
Q116054221	Lmul	"Anne Lawe, of Wigston Magna"
Q116054221	Len	"Anne Lawe, of Wigston Magna"
Q116054221	Amul	"Agnes Lawe, of Wigston Magna"

# Q116054225  Mabel|Isabel Croftes  ->  Mabel Croftes   + Isabel Croftes
Q116054225	Lmul	"Mabel Croftes"
Q116054225	Len	"Mabel Croftes"
Q116054225	Amul	"Isabel Croftes"

# Q116054227  Elizabeth|Joanna Villiers  ->  Elizabeth Villiers   + Joanna Villiers
Q116054227	Lmul	"Elizabeth Villiers"
Q116054227	Len	"Elizabeth Villiers"
Q116054227	Amul	"Joanna Villiers"

# Q116054325  Anne|Joan Cumberworth  ->  Anne Cumberworth   + Joan Cumberworth
Q116054325	Lmul	"Anne Cumberworth"
Q116054325	Len	"Anne Cumberworth"
Q116054325	Amul	"Joan Cumberworth"

# Q116054327  Margery|Margaret Braytofte  ->  Margery Braytofte   + Margaret Braytofte
Q116054327	Lmul	"Margery Braytofte"
Q116054327	Len	"Margery Braytofte"
Q116054327	Amul	"Margaret Braytofte"

# Q116054366  Agnes|Alice|Anne Clopton  ->  Agnes Clopton   + Alice Clopton | Anne Clopton
Q116054366	Lmul	"Agnes Clopton"
Q116054366	Len	"Agnes Clopton"
Q116054366	Amul	"Alice Clopton"
Q116054366	Amul	"Anne Clopton"

# Q116054427  Jonet|Janet Bulkeley, of Eaton  ->  Jonet Bulkeley, of Eaton   + Janet Bulkeley, of Eaton
Q116054427	Lmul	"Jonet Bulkeley, of Eaton"
Q116054427	Len	"Jonet Bulkeley, of Eaton"
Q116054427	Amul	"Janet Bulkeley, of Eaton"

# Q116054593  Sir Piers|Peter de Dutton aka Warburton  ->  Sir Piers de Dutton aka Warburton   + Sir Peter de Dutton aka Warburton
Q116054593	Lmul	"Sir Piers de Dutton aka Warburton"
Q116054593	Len	"Sir Piers de Dutton aka Warburton"
Q116054593	Amul	"Sir Peter de Dutton aka Warburton"

# Q116054623  Margaret|Margery Bruyn  ->  Margaret Bruyn   + Margery Bruyn
Q116054623	Lmul	"Margaret Bruyn"
Q116054623	Len	"Margaret Bruyn"
Q116054623	Amul	"Margery Bruyn"

# Q116054654  Elsbeth|Elizabeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go  ->  Elsbeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go   + Elizabeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go
Q116054654	Lmul	"Elsbeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go"
Q116054654	Len	"Elsbeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go"
Q116054654	Amul	"Elizabeth ferch John Llwyd ab Ieuan ap Maredudd of Gwern-y-go"

# Q116054661  Elen|Elsbeth ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel  ->  Elen ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel   + Elsbeth ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel
Q116054661	Lmul	"Elen ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel"
Q116054661	Len	"Elen ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel"
Q116054661	Amul	"Elsbeth ferch Dafydd Llwyd ap Dafydd ab Einion ap Hywel"

# Q116054664  Mallt|Mawd ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn  ->  Mallt ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn   + Mawd ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn
Q116054664	Lmul	"Mallt ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn"
Q116054664	Len	"Mallt ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn"
Q116054664	Amul	"Mawd ferch Jenkin ab Iorwerth ab Einion of Ynys-y-Maen-Gwyn"

# Q116054722  John|Reginald Scriven  ->  John Scriven   + Reginald Scriven
Q116054722	Lmul	"John Scriven"
Q116054722	Len	"John Scriven"
Q116054722	Amul	"Reginald Scriven"

# Q116054725  Marion|Mary Anne Salter  ->  Marion Anne Salter   + Mary Anne Salter
Q116054725	Lmul	"Marion Anne Salter"
Q116054725	Len	"Marion Anne Salter"
Q116054725	Amul	"Mary Anne Salter"

# Q116054760  Alswn|Alice ferch Maredudd ap Hywel ab Adda ap Madog  ->  Alswn ferch Maredudd ap Hywel ab Adda ap Madog   + Alice ferch Maredudd ap Hywel ab Adda ap Madog
Q116054760	Lmul	"Alswn ferch Maredudd ap Hywel ab Adda ap Madog"
Q116054760	Len	"Alswn ferch Maredudd ap Hywel ab Adda ap Madog"
Q116054760	Amul	"Alice ferch Maredudd ap Hywel ab Adda ap Madog"

# Q116054807  Peter|Perkin ap Roger Corbet  ->  Peter ap Roger Corbet   + Perkin ap Roger Corbet
Q116054807	Lmul	"Peter ap Roger Corbet"
Q116054807	Len	"Peter ap Roger Corbet"
Q116054807	Amul	"Perkin ap Roger Corbet"

# Q116054826  Lleici|Lleucu ferch Gruffudd ap Beli  ->  Lleici ferch Gruffudd ap Beli   + Lleucu ferch Gruffudd ap Beli
Q116054826	Lmul	"Lleici ferch Gruffudd ap Beli"
Q116054826	Len	"Lleici ferch Gruffudd ap Beli"
Q116054826	Amul	"Lleucu ferch Gruffudd ap Beli"

# Q116054975  Madog|Cadwgan ap Thomas ap Rhodri ab Owain Gwynedd  ->  Madog ap Thomas ap Rhodri ab Owain Gwynedd   + Cadwgan ap Thomas ap Rhodri ab Owain Gwynedd
Q116054975	Lmul	"Madog ap Thomas ap Rhodri ab Owain Gwynedd"
Q116054975	Len	"Madog ap Thomas ap Rhodri ab Owain Gwynedd"
Q116054975	Amul	"Cadwgan ap Thomas ap Rhodri ab Owain Gwynedd"

# Q116055450  Ednowain|Owain ap Trahaearn ap Caradog  ->  Ednowain ap Trahaearn ap Caradog   + Owain ap Trahaearn ap Caradog
Q116055450	Len	"Ednowain ap Trahaearn ap Caradog"
Q116055450	Amul	"Owain ap Trahaearn ap Caradog"

# Q116057660  Diebold|Theobald von Erlach, Herr zu Blimplitz  ->  Diebold von Erlach, Herr zu Blimplitz   + Theobald von Erlach, Herr zu Blimplitz
Q116057660	Len	"Diebold von Erlach, Herr zu Blimplitz"
Q116057660	Amul	"Theobald von Erlach, Herr zu Blimplitz"

# Q116057672  Johann|Hans von Erlach, Herr von Bümplitz  ->  Johann von Erlach, Herr von Bümplitz   + Hans von Erlach, Herr von Bümplitz
Q116057672	Len	"Johann von Erlach, Herr von Bümplitz"
Q116057672	Amul	"Hans von Erlach, Herr von Bümplitz"

# Q116057687  Adeheid|Isabelle Haller von Gurtlarin (Courtelary)  ->  Adeheid Haller von Gurtlarin (Courtelary)   + Isabelle Haller von Gurtlarin (Courtelary)
Q116057687	Lmul	"Adeheid Haller von Gurtlarin (Courtelary)"
Q116057687	Len	"Adeheid Haller von Gurtlarin (Courtelary)"
Q116057687	Amul	"Isabelle Haller von Gurtlarin (Courtelary)"

# Q116057709  Johanna Franziska|Francisquina von Raron  ->  Johanna Franziska von Raron   + Johanna Francisquina von Raron
Q116057709	Lmul	"Johanna Franziska von Raron"
Q116057709	Len	"Johanna Franziska von Raron"
Q116057709	Amul	"Johanna Francisquina von Raron"

# Q116057724  Heinrich|Heinzmann von Bubenberg, herr zu Spiez  ->  Heinrich von Bubenberg, herr zu Spiez   + Heinzmann von Bubenberg, herr zu Spiez
Q116057724	Lmul	"Heinrich von Bubenberg, herr zu Spiez"
Q116057724	Len	"Heinrich von Bubenberg, herr zu Spiez"
Q116057724	Amul	"Heinzmann von Bubenberg, herr zu Spiez"

# Q116057745  Nicolas|Nicod, sire de La Sarraz  ->  Nicolas sire de La Sarraz   + Nicod, sire de La Sarraz
Q116057745	Lmul	"Nicolas sire de La Sarraz"
Q116057745	Len	"Nicolas sire de La Sarraz"
Q116057745	Amul	"Nicod, sire de La Sarraz"

# Q116058213  Bernard|Barnard Samways, of Toller Tratrum  ->  Bernard Samways, of Toller Tratrum   + Barnard Samways, of Toller Tratrum
Q116058213	Lmul	"Bernard Samways, of Toller Tratrum"
Q116058213	Len	"Bernard Samways, of Toller Tratrum"
Q116058213	Amul	"Barnard Samways, of Toller Tratrum"

# Q116058427  Drugo|Drew Brudenell  ->  Drugo Brudenell   + Drew Brudenell
Q116058427	Lmul	"Drugo Brudenell"
Q116058427	Len	"Drugo Brudenell"
Q116058427	Amul	"Drew Brudenell"

# Q116058432  Anne|Agnes Bourman (or Boorman), of Brooke  ->  Anne Bourman (or Boorman), of Brooke   + Agnes Bourman (or Boorman), of Brooke
Q116058432	Lmul	"Anne Bourman (or Boorman), of Brooke"
Q116058432	Len	"Anne Bourman (or Boorman), of Brooke"
Q116058432	Amul	"Agnes Bourman (or Boorman), of Brooke"

# Q116058469  Robert|Roger Kempe, of Weston  ->  Robert Kempe, of Weston   + Roger Kempe, of Weston
Q116058469	Lmul	"Robert Kempe, of Weston"
Q116058469	Len	"Robert Kempe, of Weston"
Q116058469	Amul	"Roger Kempe, of Weston"

# Q116058779  Margaret|Maud Stonor  ->  Margaret Stonor   + Maud Stonor
Q116058779	Lmul	"Margaret Stonor"
Q116058779	Len	"Margaret Stonor"
Q116058779	Amul	"Maud Stonor"

# Q116058782  Anne|Catherine? Lovell  ->  Anne Lovell   + Catherine? Lovell
Q116058782	Lmul	"Anne Lovell"
Q116058782	Len	"Anne Lovell"
Q116058782	Amul	"Catherine? Lovell"

# Q116073165  Ellen|Hélène FitzGerald  ->  Ellen FitzGerald   + Hélène FitzGerald
Q116073165	Lmul	"Ellen FitzGerald"
Q116073165	Len	"Ellen FitzGerald"
Q116073165	Amul	"Hélène FitzGerald"

# Q116073167  Ellen|Hélène MacSeehy  ->  Ellen MacSeehy   + Hélène MacSeehy
Q116073167	Lmul	"Ellen MacSeehy"
Q116073167	Len	"Ellen MacSeehy"
Q116073167	Amul	"Hélène MacSeehy"

# Q116073187  Edmond|Emmanuel MacSeehy  ->  Edmond MacSeehy   + Emmanuel MacSeehy
Q116073187	Lmul	"Edmond MacSeehy"
Q116073187	Len	"Edmond MacSeehy"
Q116073187	Amul	"Emmanuel MacSeehy"

# Q116073293  Jean|Joan MacNamara  ->  Jean MacNamara   + Joan MacNamara
Q116073293	Lmul	"Jean MacNamara"
Q116073293	Len	"Jean MacNamara"
Q116073293	Amul	"Joan MacNamara"

# Q116084800  John|Januarius|Janvier Dunstanville, of Ecland, Wilts, alias Castlecombe  ->  John Dunstanville, of Ecland, Wilts, alias Castlecombe   + Januarius Dunstanville, of Ecland, Wilts, alias Castlecombe | Janvier Dunstanville, of Ecland, Wilts, alias Castlecombe
Q116084800	Lmul	"John Dunstanville, of Ecland, Wilts, alias Castlecombe"
Q116084800	Len	"John Dunstanville, of Ecland, Wilts, alias Castlecombe"
Q116084800	Amul	"Januarius Dunstanville, of Ecland, Wilts, alias Castlecombe"
Q116084800	Amul	"Janvier Dunstanville, of Ecland, Wilts, alias Castlecombe"

# Q116084819  Robert|James Drayton, of London  ->  Robert Drayton, of London   + James Drayton, of London
Q116084819	Lmul	"Robert Drayton, of London"
Q116084819	Len	"Robert Drayton, of London"
Q116084819	Amul	"James Drayton, of London"

# Q116085217  Sophie|Anna von Trümbach zu Wehrda  ->  Sophie von Trümbach zu Wehrda   + Anna von Trümbach zu Wehrda
Q116085217	Lmul	"Sophie von Trümbach zu Wehrda"
Q116085217	Len	"Sophie von Trümbach zu Wehrda"
Q116085217	Amul	"Anna von Trümbach zu Wehrda"

# Q116085324  Benedict|Benedikt von Ahlefeldt, in Lehmkulen  ->  Benedict von Ahlefeldt, in Lehmkulen   + Benedikt von Ahlefeldt, in Lehmkulen
Q116085324	Lmul	"Benedict von Ahlefeldt, in Lehmkulen"
Q116085324	Len	"Benedict von Ahlefeldt, in Lehmkulen"
Q116085324	Amul	"Benedikt von Ahlefeldt, in Lehmkulen"

# Q116085580  Anna|Elsa von Fleckenstein  ->  Anna von Fleckenstein   + Elsa von Fleckenstein
Q116085580	Lmul	"Anna von Fleckenstein"
Q116085580	Len	"Anna von Fleckenstein"
Q116085580	Amul	"Elsa von Fleckenstein"

# Q116085870  Elsa|Esel von Büdesheim  ->  Elsa von Büdesheim   + Esel von Büdesheim
Q116085870	Lmul	"Elsa von Büdesheim"
Q116085870	Len	"Elsa von Büdesheim"
Q116085870	Amul	"Esel von Büdesheim"

# Q116085934  Johan|Johann von Ahlefeldt af Lehmkulen og Wittmold  ->  Johan von Ahlefeldt af Lehmkulen og Wittmold   + Johann von Ahlefeldt af Lehmkulen og Wittmold
Q116085934	Len	"Johan von Ahlefeldt af Lehmkulen og Wittmold"
Q116085934	Amul	"Johann von Ahlefeldt af Lehmkulen og Wittmold"

# Q116086202  Döll|Tolde Wais von Fauerbach  ->  Döll Wais von Fauerbach   + Tolde Wais von Fauerbach
Q116086202	Lmul	"Döll Wais von Fauerbach"
Q116086202	Len	"Döll Wais von Fauerbach"
Q116086202	Amul	"Tolde Wais von Fauerbach"

# Q116087330  Johann|Jakob von Helmstorff, Her auf Eppishausen  ->  Johann von Helmstorff, Her auf Eppishausen   + Jakob von Helmstorff, Her auf Eppishausen
Q116087330	Lmul	"Johann von Helmstorff, Her auf Eppishausen"
Q116087330	Len	"Johann von Helmstorff, Her auf Eppishausen"
Q116087330	Amul	"Jakob von Helmstorff, Her auf Eppishausen"

# Q116087518  Jakob|Jacques Mayor de Lutry, seigneur de Maisery  ->  Jakob Mayor de Lutry, seigneur de Maisery   + Jacques Mayor de Lutry, seigneur de Maisery
Q116087518	Lmul	"Jakob Mayor de Lutry, seigneur de Maisery"
Q116087518	Len	"Jakob Mayor de Lutry, seigneur de Maisery"
Q116087518	Amul	"Jacques Mayor de Lutry, seigneur de Maisery"

# Q116087615  Brigitte|Brida von Schlierbach  ->  Brigitte von Schlierbach   + Brida von Schlierbach
Q116087615	Lmul	"Brigitte von Schlierbach"
Q116087615	Len	"Brigitte von Schlierbach"
Q116087615	Amul	"Brida von Schlierbach"

# Q116088573  Joan|Mary Strother  ->  Joan Strother   + Mary Strother
Q116088573	Lmul	"Joan Strother"
Q116088573	Len	"Joan Strother"
Q116088573	Amul	"Mary Strother"

# Q116088623  Robert|Nicholas (IV) Raynes, of Shortflatt  ->  Robert (IV) Raynes, of Shortflatt   + Nicholas (IV) Raynes, of Shortflatt
Q116088623	Lmul	"Robert (IV) Raynes, of Shortflatt"
Q116088623	Len	"Robert (IV) Raynes, of Shortflatt"
Q116088623	Amul	"Nicholas (IV) Raynes, of Shortflatt"

# Q116090513  Jane|Jone Widdrington  ->  Jane Widdrington   + Jone Widdrington
Q116090513	Lmul	"Jane Widdrington"
Q116090513	Len	"Jane Widdrington"
Q116090513	Amul	"Jone Widdrington"

# Q116093418  Margaret|Margery  ->  Margaret   + Margery
Q116093418	Lmul	"Margaret"
Q116093418	Len	"Margaret"
Q116093418	Amul	"Margery"

# Q116093614  Agnes|Alice Greene, of Gressingham  ->  Agnes Greene, of Gressingham   + Alice Greene, of Gressingham
Q116093614	Lmul	"Agnes Greene, of Gressingham"
Q116093614	Len	"Agnes Greene, of Gressingham"
Q116093614	Amul	"Alice Greene, of Gressingham"

# Q116094793  Françoise|Catherine d'Aiguières  ->  Françoise d'Aiguières   + Catherine d'Aiguières
Q116094793	Lmul	"Françoise d'Aiguières"
Q116094793	Len	"Françoise d'Aiguières"
Q116094793	Amul	"Catherine d'Aiguières"

# Q116094942  Irlandé|Yoland de Genebrières  ->  Irlandé de Genebrières   + Yoland de Genebrières
Q116094942	Len	"Irlandé de Genebrières"
Q116094942	Amul	"Yoland de Genebrières"

# Q116095768  Jane|Joan Warren, of Poynton  ->  Jane Warren, of Poynton   + Joan Warren, of Poynton
Q116095768	Lmul	"Jane Warren, of Poynton"
Q116095768	Len	"Jane Warren, of Poynton"
Q116095768	Amul	"Joan Warren, of Poynton"

# Q116096187  Catherine|Euphemia von Ebersbach  ->  Catherine von Ebersbach   + Euphemia von Ebersbach
Q116096187	Lmul	"Catherine von Ebersbach"
Q116096187	Len	"Catherine von Ebersbach"
Q116096187	Amul	"Euphemia von Ebersbach"

# Q116101877  Hans|Kunz von Schlieben, Lord of Kavertitz and Mühlberg  ->  Hans von Schlieben, Lord of Kavertitz and Mühlberg   + Kunz von Schlieben, Lord of Kavertitz and Mühlberg
Q116101877	Lmul	"Hans von Schlieben, Lord of Kavertitz and Mühlberg"
Q116101877	Len	"Hans von Schlieben, Lord of Kavertitz and Mühlberg"
Q116101877	Amul	"Kunz von Schlieben, Lord of Kavertitz and Mühlberg"

# Q116101950  Caspar|Sigismund von Knobelsdorff  ->  Caspar von Knobelsdorff   + Sigismund von Knobelsdorff
Q116101950	Lmul	"Caspar von Knobelsdorff"
Q116101950	Len	"Caspar von Knobelsdorff"
Q116101950	Amul	"Sigismund von Knobelsdorff"

# Q116102434  Nikolaus|Claus von Lützow  ->  Nikolaus von Lützow   + Claus von Lützow
Q116102434	Lmul	"Nikolaus von Lützow"
Q116102434	Len	"Nikolaus von Lützow"
Q116102434	Amul	"Claus von Lützow"

# Q116106020  Piers|Peter de Hatton, of Kirstybirches  ->  Piers de Hatton, of Kirstybirches   + Peter de Hatton, of Kirstybirches
Q116106020	Lmul	"Piers de Hatton, of Kirstybirches"
Q116106020	Len	"Piers de Hatton, of Kirstybirches"
Q116106020	Amul	"Peter de Hatton, of Kirstybirches"

# Q116106026  Hawisa|Anne Dalby  ->  Hawisa Dalby   + Anne Dalby
Q116106026	Lmul	"Hawisa Dalby"
Q116106026	Len	"Hawisa Dalby"
Q116106026	Amul	"Anne Dalby"

# Q116106051  Thomas|John Westby, of Kent  ->  Thomas Westby, of Kent   + John Westby, of Kent
Q116106051	Lmul	"Thomas Westby, of Kent"
Q116106051	Len	"Thomas Westby, of Kent"
Q116106051	Amul	"John Westby, of Kent"

# Q116106208  Thomas|Oliver Shires  ->  Thomas Shires   + Oliver Shires
Q116106208	Lmul	"Thomas Shires"
Q116106208	Len	"Thomas Shires"
Q116106208	Amul	"Oliver Shires"

# Q116108294  Alice|Alicia  ->  Alice   + Alicia
Q116108294	Lmul	"Alice"
Q116108294	Len	"Alice"
Q116108294	Amul	"Alicia"

# Q116108813  John|Jenkin ab Ieuan ap Madog ab Iorwerth of Stansty  ->  John ab Ieuan ap Madog ab Iorwerth of Stansty   + Jenkin ab Ieuan ap Madog ab Iorwerth of Stansty
Q116108813	Lmul	"John ab Ieuan ap Madog ab Iorwerth of Stansty"
Q116108813	Len	"John ab Ieuan ap Madog ab Iorwerth of Stansty"
Q116108813	Amul	"Jenkin ab Ieuan ap Madog ab Iorwerth of Stansty"

# Q116108901  Gwenllian|Margred ferch Madog ab Ednyfed Gôch ap Cynwrig  ->  Gwenllian ferch Madog ab Ednyfed Gôch ap Cynwrig   + Margred ferch Madog ab Ednyfed Gôch ap Cynwrig
Q116108901	Lmul	"Gwenllian ferch Madog ab Ednyfed Gôch ap Cynwrig"
Q116108901	Len	"Gwenllian ferch Madog ab Ednyfed Gôch ap Cynwrig"
Q116108901	Amul	"Margred ferch Madog ab Ednyfed Gôch ap Cynwrig"

# Q116110773  Roger Fychan|Estwick ap Roger  ->  Roger Fychan ap Roger   + Roger Estwick ap Roger
Q116110773	Lmul	"Roger Fychan ap Roger"
Q116110773	Len	"Roger Fychan ap Roger"
Q116110773	Amul	"Roger Estwick ap Roger"

# Q116111575  Mawd ferch Richard|Roger Manley  ->  Mawd ferch Richard Manley   + Mawd ferch Roger Manley
Q116111575	Lmul	"Mawd ferch Richard Manley"
Q116111575	Len	"Mawd ferch Richard Manley"
Q116111575	Amul	"Mawd ferch Roger Manley"

# Q116113716  Alswn|Alice ferch Maredudd Ddû ap Gronwy ap Maredudd  ->  Alswn ferch Maredudd Ddû ap Gronwy ap Maredudd   + Alice ferch Maredudd Ddû ap Gronwy ap Maredudd
Q116113716	Lmul	"Alswn ferch Maredudd Ddû ap Gronwy ap Maredudd"
Q116113716	Len	"Alswn ferch Maredudd Ddû ap Gronwy ap Maredudd"
Q116113716	Amul	"Alice ferch Maredudd Ddû ap Gronwy ap Maredudd"

# Q116114703  Alice|Margred Kynaston  ->  Alice Kynaston   + Margred Kynaston
Q116114703	Lmul	"Alice Kynaston"
Q116114703	Len	"Alice Kynaston"
Q116114703	Amul	"Margred Kynaston"

# Q116115056  Margred|Catrin ferch Thomas ap Llywelyn ap Madog  ->  Margred ferch Thomas ap Llywelyn ap Madog   + Catrin ferch Thomas ap Llywelyn ap Madog
Q116115056	Lmul	"Margred ferch Thomas ap Llywelyn ap Madog"
Q116115056	Len	"Margred ferch Thomas ap Llywelyn ap Madog"
Q116115056	Amul	"Catrin ferch Thomas ap Llywelyn ap Madog"

# Q116115848  Llywarch|Llywelyn  ->  Llywarch   + Llywelyn
Q116115848	Lmul	"Llywarch"
Q116115848	Len	"Llywarch"
Q116115848	Amul	"Llywelyn"

# Q116117100  Mahaut|Marie de la Douve dite de Nieukercke (Nieuwkerke)  ->  Mahaut de la Douve dite de Nieukercke (Nieuwkerke)   + Marie de la Douve dite de Nieukercke (Nieuwkerke)
Q116117100	Lmul	"Mahaut de la Douve dite de Nieukercke (Nieuwkerke)"
Q116117100	Len	"Mahaut de la Douve dite de Nieukercke (Nieuwkerke)"
Q116117100	Amul	"Marie de la Douve dite de Nieukercke (Nieuwkerke)"

# Q116118912  Johann|Hans, Herr von Biberstein in Beeskaw und Storkow  ->  Johann Herr von Biberstein in Beeskaw und Storkow   + Hans, Herr von Biberstein in Beeskaw und Storkow
Q116118912	Len	"Johann Herr von Biberstein in Beeskaw und Storkow"
Q116118912	Amul	"Hans, Herr von Biberstein in Beeskaw und Storkow"

# Q116119468  Dignamenta|Margareta von Morsleben  ->  Dignamenta von Morsleben   + Margareta von Morsleben
Q116119468	Lmul	"Dignamenta von Morsleben"
Q116119468	Len	"Dignamenta von Morsleben"
Q116119468	Amul	"Margareta von Morsleben"

# Q116125245  Helena|Elena  ->  Helena   + Elena
Q116125245	Lmul	"Helena"
Q116125245	Len	"Helena"
Q116125245	Amul	"Elena"

# Q116125764  Eleanor|Joan de Oulton  ->  Eleanor de Oulton   + Joan de Oulton
Q116125764	Lmul	"Eleanor de Oulton"
Q116125764	Len	"Eleanor de Oulton"
Q116125764	Amul	"Joan de Oulton"

# Q116126151  Mathurine|Matheline Herbert  ->  Mathurine Herbert   + Matheline Herbert
Q116126151	Lmul	"Mathurine Herbert"
Q116126151	Len	"Mathurine Herbert"
Q116126151	Amul	"Matheline Herbert"

# Q116126290  Philippe Burelle|Bureau  ->  Philippe Burelle   + Philippe Bureau
Q116126290	Lmul	"Philippe Burelle"
Q116126290	Len	"Philippe Burelle"
Q116126290	Amul	"Philippe Bureau"

# Q116126506  Marie Péron|Peyron  ->  Marie Péron   + Marie Peyron
Q116126506	Lmul	"Marie Péron"
Q116126506	Len	"Marie Péron"
Q116126506	Amul	"Marie Peyron"

# Q116126798  Isabelle|Jeanne de Chartres  ->  Isabelle de Chartres   + Jeanne de Chartres
Q116126798	Lmul	"Isabelle de Chartres"
Q116126798	Len	"Isabelle de Chartres"
Q116126798	Amul	"Jeanne de Chartres"

# Q116126931  Pierre|Jean Bessoneau, seigneur de Germignon  ->  Pierre Bessoneau, seigneur de Germignon   + Jean Bessoneau, seigneur de Germignon
Q116126931	Lmul	"Pierre Bessoneau, seigneur de Germignon"
Q116126931	Len	"Pierre Bessoneau, seigneur de Germignon"
Q116126931	Amul	"Jean Bessoneau, seigneur de Germignon"

# Q116128837  Arndt|Arnold von Wülffen  ->  Arndt von Wülffen   + Arnold von Wülffen
Q116128837	Lmul	"Arndt von Wülffen"
Q116128837	Len	"Arndt von Wülffen"
Q116128837	Amul	"Arnold von Wülffen"

# Q116128838  Arndt|Arnold von Wülffen  ->  Arndt von Wülffen   + Arnold von Wülffen
Q116128838	Lmul	"Arndt von Wülffen"
Q116128838	Len	"Arndt von Wülffen"
Q116128838	Amul	"Arnold von Wülffen"

# Q116130057  Johann|Hans Zeller von Zell auf Riedau  ->  Johann Zeller von Zell auf Riedau   + Hans Zeller von Zell auf Riedau
Q116130057	Lmul	"Johann Zeller von Zell auf Riedau"
Q116130057	Len	"Johann Zeller von Zell auf Riedau"
Q116130057	Amul	"Hans Zeller von Zell auf Riedau"

# Q116130555  Isabelle|Marguerite de Flandre (Flandren zu Praet)  ->  Isabelle de Flandre (Flandren zu Praet)   + Marguerite de Flandre (Flandren zu Praet)
Q116130555	Lmul	"Isabelle de Flandre (Flandren zu Praet)"
Q116130555	Len	"Isabelle de Flandre (Flandren zu Praet)"
Q116130555	Amul	"Marguerite de Flandre (Flandren zu Praet)"

# Q116130558  Jean|Johann I de Flandre et Praet, Seigneur de Praet et de La Woestine  ->  Jean I de Flandre et Praet, Seigneur de Praet et de La Woestine   + Johann I de Flandre et Praet, Seigneur de Praet et de La Woestine
Q116130558	Lmul	"Jean I de Flandre et Praet, Seigneur de Praet et de La Woestine"
Q116130558	Len	"Jean I de Flandre et Praet, Seigneur de Praet et de La Woestine"
Q116130558	Amul	"Johann I de Flandre et Praet, Seigneur de Praet et de La Woestine"

# Q116130730  Christine|Chrétienne de Belle  ->  Christine de Belle   + Chrétienne de Belle
Q116130730	Lmul	"Christine de Belle"
Q116130730	Len	"Christine de Belle"
Q116130730	Amul	"Chrétienne de Belle"

# Q116130744  Philippine|Philippotte du Quesnoy  ->  Philippine du Quesnoy   + Philippotte du Quesnoy
Q116130744	Lmul	"Philippine du Quesnoy"
Q116130744	Len	"Philippine du Quesnoy"
Q116130744	Amul	"Philippotte du Quesnoy"

# Q116130752  Gauvain|Gonin de La Viéville, Seigneur de La Prée  ->  Gauvain de La Viéville, Seigneur de La Prée   + Gonin de La Viéville, Seigneur de La Prée
Q116130752	Lmul	"Gauvain de La Viéville, Seigneur de La Prée"
Q116130752	Len	"Gauvain de La Viéville, Seigneur de La Prée"
Q116130752	Amul	"Gonin de La Viéville, Seigneur de La Prée"

# Q116136365  Rafe|Ralph Vernon, of Haslington  ->  Rafe Vernon, of Haslington   + Ralph Vernon, of Haslington
Q116136365	Lmul	"Rafe Vernon, of Haslington"
Q116136365	Len	"Rafe Vernon, of Haslington"
Q116136365	Amul	"Ralph Vernon, of Haslington"

# Q116136369  Joan|Jane Molyneux  ->  Joan Molyneux   + Jane Molyneux
Q116136369	Lmul	"Joan Molyneux"
Q116136369	Len	"Joan Molyneux"
Q116136369	Amul	"Jane Molyneux"

# Q116136391  Alice|Elizabeth Charleton  ->  Alice Charleton   + Elizabeth Charleton
Q116136391	Lmul	"Alice Charleton"
Q116136391	Len	"Alice Charleton"
Q116136391	Amul	"Elizabeth Charleton"

# Q116136593  Helena|Ilona Rozgönyi  ->  Helena Rozgönyi   + Ilona Rozgönyi
Q116136593	Lmul	"Helena Rozgönyi"
Q116136593	Len	"Helena Rozgönyi"
Q116136593	Amul	"Ilona Rozgönyi"

# Q116136594  Catherine|Katalin Balassa de Gyarmat  ->  Catherine Balassa de Gyarmat   + Katalin Balassa de Gyarmat
Q116136594	Lmul	"Catherine Balassa de Gyarmat"
Q116136594	Len	"Catherine Balassa de Gyarmat"
Q116136594	Amul	"Katalin Balassa de Gyarmat"

# Q116136641  Benedict|Benedikt Schifer auf Freiling  ->  Benedict Schifer auf Freiling   + Benedikt Schifer auf Freiling
Q116136641	Lmul	"Benedict Schifer auf Freiling"
Q116136641	Len	"Benedict Schifer auf Freiling"
Q116136641	Amul	"Benedikt Schifer auf Freiling"

# Q116136728  Konstancie|Constanza, Contessa di Collalto e San Salvatore  ->  Konstancie Contessa di Collalto e San Salvatore   + Constanza, Contessa di Collalto e San Salvatore
Q116136728	Len	"Konstancie Contessa di Collalto e San Salvatore"
Q116136728	Amul	"Constanza, Contessa di Collalto e San Salvatore"

# Q116143290  John|Thomas Heslerton (Haslerton)  ->  John Heslerton (Haslerton)   + Thomas Heslerton (Haslerton)
Q116143290	Lmul	"John Heslerton (Haslerton)"
Q116143290	Len	"John Heslerton (Haslerton)"
Q116143290	Amul	"Thomas Heslerton (Haslerton)"

# Q116144001  George|Thomas|John Scopham, of Scopham  ->  George Scopham, of Scopham   + Thomas Scopham, of Scopham | John Scopham, of Scopham
Q116144001	Lmul	"George Scopham, of Scopham"
Q116144001	Len	"George Scopham, of Scopham"
Q116144001	Amul	"Thomas Scopham, of Scopham"
Q116144001	Amul	"John Scopham, of Scopham"

# Q116144966  Maud|Matilda Molton  ->  Maud Molton   + Matilda Molton
Q116144966	Lmul	"Maud Molton"
Q116144966	Len	"Maud Molton"
Q116144966	Amul	"Matilda Molton"

# Q116145367  Matilda|Maud Lane  ->  Matilda Lane   + Maud Lane
Q116145367	Lmul	"Matilda Lane"
Q116145367	Len	"Matilda Lane"
Q116145367	Amul	"Maud Lane"

# Q116145392  John|James Livesey  ->  John Livesey   + James Livesey
Q116145392	Lmul	"John Livesey"
Q116145392	Len	"John Livesey"
Q116145392	Amul	"James Livesey"

# Q116145402  Joan|Anne Radcliffe, of Ordsall  ->  Joan Radcliffe, of Ordsall   + Anne Radcliffe, of Ordsall
Q116145402	Lmul	"Joan Radcliffe, of Ordsall"
Q116145402	Len	"Joan Radcliffe, of Ordsall"
Q116145402	Amul	"Anne Radcliffe, of Ordsall"

# Q116145415  Jane|Joan Headlam  ->  Jane Headlam   + Joan Headlam
Q116145415	Lmul	"Jane Headlam"
Q116145415	Len	"Jane Headlam"
Q116145415	Amul	"Joan Headlam"

# Q116145423  Lettice|Letitia  ->  Lettice   + Letitia
Q116145423	Lmul	"Lettice"
Q116145423	Len	"Lettice"
Q116145423	Amul	"Letitia"

# Q116145437  Anne|Amy Toke (or Tooke)  ->  Anne Toke (or Tooke)   + Amy Toke (or Tooke)
Q116145437	Len	"Anne Toke (or Tooke)"
Q116145437	Amul	"Amy Toke (or Tooke)"

# Q116145445  Avelina|Anabella Rigmaden  ->  Avelina Rigmaden   + Anabella Rigmaden
Q116145445	Lmul	"Avelina Rigmaden"
Q116145445	Len	"Avelina Rigmaden"
Q116145445	Amul	"Anabella Rigmaden"

# Q116145453  Sibyl|Sibilla|Isabella Hudleston  ->  Sibyl Hudleston   + Sibilla Hudleston | Isabella Hudleston
Q116145453	Lmul	"Sibyl Hudleston"
Q116145453	Len	"Sibyl Hudleston"
Q116145453	Amul	"Sibilla Hudleston"
Q116145453	Amul	"Isabella Hudleston"

# Q116145535  Rowland|Richard Jay, of Jay, Salop  ->  Rowland Jay, of Jay, Salop   + Richard Jay, of Jay, Salop
Q116145535	Lmul	"Rowland Jay, of Jay, Salop"
Q116145535	Len	"Rowland Jay, of Jay, Salop"
Q116145535	Amul	"Richard Jay, of Jay, Salop"

# Q116145561  George|Thomas Onslow, of Rodington, Salop  ->  George Onslow, of Rodington, Salop   + Thomas Onslow, of Rodington, Salop
Q116145561	Lmul	"George Onslow, of Rodington, Salop"
Q116145561	Len	"George Onslow, of Rodington, Salop"
Q116145561	Amul	"Thomas Onslow, of Rodington, Salop"

# Q116145604  Wilgiford|Wiliford Williams  ->  Wilgiford Williams   + Wiliford Williams
Q116145604	Lmul	"Wilgiford Williams"
Q116145604	Len	"Wilgiford Williams"
Q116145604	Amul	"Wiliford Williams"

# Q116145635  Gwenllian|Ann ferch John ap Gruffudd ap Hywel Melyn  ->  Gwenllian ferch John ap Gruffudd ap Hywel Melyn   + Ann ferch John ap Gruffudd ap Hywel Melyn
Q116145635	Lmul	"Gwenllian ferch John ap Gruffudd ap Hywel Melyn"
Q116145635	Len	"Gwenllian ferch John ap Gruffudd ap Hywel Melyn"
Q116145635	Amul	"Ann ferch John ap Gruffudd ap Hywel Melyn"

# Q116146007  Joan|Jane ferch Lewis Marcross  ->  Joan ferch Lewis Marcross   + Jane ferch Lewis Marcross
Q116146007	Lmul	"Joan ferch Lewis Marcross"
Q116146007	Len	"Joan ferch Lewis Marcross"
Q116146007	Amul	"Jane ferch Lewis Marcross"

# Q116146111  Thomas|Richard Basset, of St.Hilary  ->  Thomas Basset, of St.Hilary   + Richard Basset, of St.Hilary
Q116146111	Lmul	"Thomas Basset, of St.Hilary"
Q116146111	Len	"Thomas Basset, of St.Hilary"
Q116146111	Amul	"Richard Basset, of St.Hilary"

# Q116146112  Susan|Margaret de la Bere  ->  Susan de la Bere   + Margaret de la Bere
Q116146112	Lmul	"Susan de la Bere"
Q116146112	Len	"Susan de la Bere"
Q116146112	Amul	"Margaret de la Bere"

# Q116146114  Ann|Agnes  ->  Ann   + Agnes
Q116146114	Lmul	"Ann"
Q116146114	Len	"Ann"
Q116146114	Amul	"Agnes"

# Q116146141  Sir Tryw|Andryw of Valence  ->  Sir Tryw of Valence   + Sir Andryw of Valence
Q116146141	Lmul	"Sir Tryw of Valence"
Q116146141	Len	"Sir Tryw of Valence"
Q116146141	Amul	"Sir Andryw of Valence"

# Q116146210  John|Nicholas Beaumont  ->  John Beaumont   + Nicholas Beaumont
Q116146210	Lmul	"John Beaumont"
Q116146210	Len	"John Beaumont"
Q116146210	Amul	"Nicholas Beaumont"

# Q116146288  John|Thomas Soame, of Bestley (Betley)  ->  John Soame, of Bestley (Betley)   + Thomas Soame, of Bestley (Betley)
Q116146288	Lmul	"John Soame, of Bestley (Betley)"
Q116146288	Len	"John Soame, of Bestley (Betley)"
Q116146288	Amul	"Thomas Soame, of Bestley (Betley)"

# Q116146456  Sir Richard|Robert Radcliffe (Ratcliffe)  ->  Sir Richard Radcliffe (Ratcliffe)   + Sir Robert Radcliffe (Ratcliffe)
Q116146456	Lmul	"Sir Richard Radcliffe (Ratcliffe)"
Q116146456	Len	"Sir Richard Radcliffe (Ratcliffe)"
Q116146456	Amul	"Sir Robert Radcliffe (Ratcliffe)"

# Q116146620  Tangwystl|Angharad ferch Jenkin Gôch ab Ieuan ap Gruffudd  ->  Tangwystl ferch Jenkin Gôch ab Ieuan ap Gruffudd   + Angharad ferch Jenkin Gôch ab Ieuan ap Gruffudd
Q116146620	Lmul	"Tangwystl ferch Jenkin Gôch ab Ieuan ap Gruffudd"
Q116146620	Len	"Tangwystl ferch Jenkin Gôch ab Ieuan ap Gruffudd"
Q116146620	Amul	"Angharad ferch Jenkin Gôch ab Ieuan ap Gruffudd"

# Q116146799  Iorwerth ab Y Gwion|Gwgon ap Trahaearn ab Iorwerth  ->  Iorwerth ab Y Gwion ap Trahaearn ab Iorwerth   + Iorwerth ab Y Gwgon ap Trahaearn ab Iorwerth
Q116146799	Lmul	"Iorwerth ab Y Gwion ap Trahaearn ab Iorwerth"
Q116146799	Len	"Iorwerth ab Y Gwion ap Trahaearn ab Iorwerth"
Q116146799	Amul	"Iorwerth ab Y Gwgon ap Trahaearn ab Iorwerth"

# Q116146801  Efa|Elen ferch Adda  ->  Efa ferch Adda   + Elen ferch Adda
Q116146801	Lmul	"Efa ferch Adda"
Q116146801	Len	"Efa ferch Adda"
Q116146801	Amul	"Elen ferch Adda"

# Q116146829  Y Gwion|Gwgon ap Trahaearn ab Iorwerth ab Einion  ->  Y Gwion ap Trahaearn ab Iorwerth ab Einion   + Y Gwgon ap Trahaearn ab Iorwerth ab Einion
Q116146829	Lmul	"Y Gwion ap Trahaearn ab Iorwerth ab Einion"
Q116146829	Len	"Y Gwion ap Trahaearn ab Iorwerth ab Einion"
Q116146829	Amul	"Y Gwgon ap Trahaearn ab Iorwerth ab Einion"

# Q116147386  Maud|Margred|Mallt ferch Madog ab Idnerth ap Cadwgan  ->  Maud ferch Madog ab Idnerth ap Cadwgan   + Margred ferch Madog ab Idnerth ap Cadwgan | Mallt ferch Madog ab Idnerth ap Cadwgan
Q116147386	Lmul	"Maud ferch Madog ab Idnerth ap Cadwgan"
Q116147386	Len	"Maud ferch Madog ab Idnerth ap Cadwgan"
Q116147386	Amul	"Margred ferch Madog ab Idnerth ap Cadwgan"
Q116147386	Amul	"Mallt ferch Madog ab Idnerth ap Cadwgan"

# Q116147485  Robin|Rotpert Llwyd ap Rhys ap Robert ap Gruffudd  ->  Robin Llwyd ap Rhys ap Robert ap Gruffudd   + Rotpert Llwyd ap Rhys ap Robert ap Gruffudd
Q116147485	Lmul	"Robin Llwyd ap Rhys ap Robert ap Gruffudd"
Q116147485	Len	"Robin Llwyd ap Rhys ap Robert ap Gruffudd"
Q116147485	Amul	"Rotpert Llwyd ap Rhys ap Robert ap Gruffudd"

# Q116147595  Meuter Fawr|Fwr ap Hedd ab Alunog ap Greddyf  ->  Meuter Fawr ap Hedd ab Alunog ap Greddyf   + Meuter Fwr ap Hedd ab Alunog ap Greddyf
Q116147595	Lmul	"Meuter Fawr ap Hedd ab Alunog ap Greddyf"
Q116147595	Len	"Meuter Fawr ap Hedd ab Alunog ap Greddyf"
Q116147595	Amul	"Meuter Fwr ap Hedd ab Alunog ap Greddyf"

# Q116147632  Mallt|Jonet ferch Llywelyn ap Bleddyn  ->  Mallt ferch Llywelyn ap Bleddyn   + Jonet ferch Llywelyn ap Bleddyn
Q116147632	Lmul	"Mallt ferch Llywelyn ap Bleddyn"
Q116147632	Len	"Mallt ferch Llywelyn ap Bleddyn"
Q116147632	Amul	"Jonet ferch Llywelyn ap Bleddyn"

# Q116147987  Patrick de Chaworth|Chaorces  ->  Patrick de Chaworth   + Patrick de Chaorces
Q116147987	Lmul	"Patrick de Chaworth"
Q116147987	Len	"Patrick de Chaworth"
Q116147987	Amul	"Patrick de Chaorces"

# Q116147998  Alice|Mallt ferch Gruffudd ap Rhys  ->  Alice ferch Gruffudd ap Rhys   + Mallt ferch Gruffudd ap Rhys
Q116147998	Lmul	"Alice ferch Gruffudd ap Rhys"
Q116147998	Len	"Alice ferch Gruffudd ap Rhys"
Q116147998	Amul	"Mallt ferch Gruffudd ap Rhys"

# Q116148399  Magdalena|Elisabeth von Röder  ->  Magdalena von Röder   + Elisabeth von Röder
Q116148399	Lmul	"Magdalena von Röder"
Q116148399	Len	"Magdalena von Röder"
Q116148399	Amul	"Elisabeth von Röder"

# Q116148429  Arnould|Arnaud V de La Hamaide, Seigneur de Condé  ->  Arnould V de La Hamaide, Seigneur de Condé   + Arnaud V de La Hamaide, Seigneur de Condé
Q116148429	Lmul	"Arnould V de La Hamaide, Seigneur de Condé"
Q116148429	Len	"Arnould V de La Hamaide, Seigneur de Condé"
Q116148429	Amul	"Arnaud V de La Hamaide, Seigneur de Condé"

# Q116149839  Georg|Jiri z Kravar (Krawarz)  ->  Georg z Kravar (Krawarz)   + Jiri z Kravar (Krawarz)
Q116149839	Len	"Georg z Kravar (Krawarz)"
Q116149839	Amul	"Jiri z Kravar (Krawarz)"

# Q116150164  Albrecht|Andreas, Herr von Zelking  ->  Albrecht Herr von Zelking   + Andreas, Herr von Zelking
Q116150164	Len	"Albrecht Herr von Zelking"
Q116150164	Amul	"Andreas, Herr von Zelking"

# Q116150167  Anna|Margaretha|Maria von Nussdorf  ->  Anna von Nussdorf   + Margaretha von Nussdorf | Maria von Nussdorf
Q116150167	Len	"Anna von Nussdorf"
Q116150167	Amul	"Margaretha von Nussdorf"
Q116150167	Amul	"Maria von Nussdorf"

# Q116150186  Jutta|Gutta von Ellerbach  ->  Jutta von Ellerbach   + Gutta von Ellerbach
Q116150186	Lmul	"Jutta von Ellerbach"
Q116150186	Len	"Jutta von Ellerbach"
Q116150186	Amul	"Gutta von Ellerbach"

# Q116150293  Mats|Mathais Gustafsson 'den Gamle' [Sparre av Vik]  ->  Mats Gustafsson 'den Gamle' [Sparre av Vik]   + Mathais Gustafsson 'den Gamle' [Sparre av Vik]
Q116150293	Lmul	"Mats Gustafsson 'den Gamle' [Sparre av Vik]"
Q116150293	Len	"Mats Gustafsson 'den Gamle' [Sparre av Vik]"
Q116150293	Amul	"Mathais Gustafsson 'den Gamle' [Sparre av Vik]"

# Q116150297  Lave|Lage Pedersen [Bielke]  ->  Lave Pedersen [Bielke]   + Lage Pedersen [Bielke]
Q116150297	Lmul	"Lave Pedersen [Bielke]"
Q116150297	Len	"Lave Pedersen [Bielke]"
Q116150297	Amul	"Lage Pedersen [Bielke]"

# Q116150304  Bengt|Benedict Ebbesen [Pik], Lord of Rossared  ->  Bengt Ebbesen [Pik], Lord of Rossared   + Benedict Ebbesen [Pik], Lord of Rossared
Q116150304	Lmul	"Bengt Ebbesen [Pik], Lord of Rossared"
Q116150304	Len	"Bengt Ebbesen [Pik], Lord of Rossared"
Q116150304	Amul	"Benedict Ebbesen [Pik], Lord of Rossared"

# Q116150307  Jens|Jon [Ulf]  ->  Jens [Ulf]   + Jon [Ulf]
Q116150307	Lmul	"Jens [Ulf]"
Q116150307	Len	"Jens [Ulf]"
Q116150307	Amul	"Jon [Ulf]"

# Q116150684  Farkas|Domokos Szeszármai  ->  Farkas Szeszármai   + Domokos Szeszármai
Q116150684	Len	"Farkas Szeszármai"
Q116150684	Amul	"Domokos Szeszármai"

# Q116150950  Mircea|Marcu Becleanu, 'Bethlen de Bethlen'  ->  Mircea Becleanu, 'Bethlen de Bethlen'   + Marcu Becleanu, 'Bethlen de Bethlen'
Q116150950	Lmul	"Mircea Becleanu, 'Bethlen de Bethlen'"
Q116150950	Len	"Mircea Becleanu, 'Bethlen de Bethlen'"
Q116150950	Amul	"Marcu Becleanu, 'Bethlen de Bethlen'"

# Q116150957  noble Judit|Judith Becleanu, 'Bethlen de Bethlen'  ->  noble Judit Becleanu, 'Bethlen de Bethlen'   + noble Judith Becleanu, 'Bethlen de Bethlen'
Q116150957	Len	"noble Judit Becleanu, 'Bethlen de Bethlen'"
Q116150957	Amul	"noble Judith Becleanu, 'Bethlen de Bethlen'"

# Q116151212  Menze|Mechtild von Militz  ->  Menze von Militz   + Mechtild von Militz
Q116151212	Len	"Menze von Militz"
Q116151212	Amul	"Mechtild von Militz"

# Q116151447  Margarete|Margareta von Mecklenburg (von Rostock)  ->  Margarete von Mecklenburg (von Rostock)   + Margareta von Mecklenburg (von Rostock)
Q116151447	Len	"Margarete von Mecklenburg (von Rostock)"
Q116151447	Amul	"Margareta von Mecklenburg (von Rostock)"

# Q116155513  Alice|Joan ferch Gwilym ap Thomas ap Llywelyn  ->  Alice ferch Gwilym ap Thomas ap Llywelyn   + Joan ferch Gwilym ap Thomas ap Llywelyn
Q116155513	Lmul	"Alice ferch Gwilym ap Thomas ap Llywelyn"
Q116155513	Len	"Alice ferch Gwilym ap Thomas ap Llywelyn"
Q116155513	Amul	"Joan ferch Gwilym ap Thomas ap Llywelyn"

# Q116156568  Catrin|Gwenllian ferch Gruffudd Derwas  ->  Catrin ferch Gruffudd Derwas   + Gwenllian ferch Gruffudd Derwas
Q116156568	Lmul	"Catrin ferch Gruffudd Derwas"
Q116156568	Len	"Catrin ferch Gruffudd Derwas"
Q116156568	Amul	"Gwenllian ferch Gruffudd Derwas"

# Q116159111  Dorothy|Thomasine Dene  ->  Dorothy Dene   + Thomasine Dene
Q116159111	Lmul	"Dorothy Dene"
Q116159111	Len	"Dorothy Dene"
Q116159111	Amul	"Thomasine Dene"

# Q116159112  James|Thomas Dene, of Barrowby  ->  James Dene, of Barrowby   + Thomas Dene, of Barrowby
Q116159112	Lmul	"James Dene, of Barrowby"
Q116159112	Len	"James Dene, of Barrowby"
Q116159112	Amul	"Thomas Dene, of Barrowby"

# Q116159113  John|James Dene, of Barrowby  ->  John Dene, of Barrowby   + James Dene, of Barrowby
Q116159113	Lmul	"John Dene, of Barrowby"
Q116159113	Len	"John Dene, of Barrowby"
Q116159113	Amul	"James Dene, of Barrowby"

# Q116159116  Catherine|Katherine Pedwardine  ->  Catherine Pedwardine   + Katherine Pedwardine
Q116159116	Lmul	"Catherine Pedwardine"
Q116159116	Len	"Catherine Pedwardine"
Q116159116	Amul	"Katherine Pedwardine"

# Q116159775  Eleanor|Elen Davison (Davies)  ->  Eleanor Davison (Davies)   + Elen Davison (Davies)
Q116159775	Len	"Eleanor Davison (Davies)"
Q116159775	Amul	"Elen Davison (Davies)"

# Q116159871  Richard|Robert Carnesew  ->  Richard Carnesew   + Robert Carnesew
Q116159871	Lmul	"Richard Carnesew"
Q116159871	Len	"Richard Carnesew"
Q116159871	Amul	"Robert Carnesew"

# Q116159881  Jane|Joan Sherston  ->  Jane Sherston   + Joan Sherston
Q116159881	Lmul	"Jane Sherston"
Q116159881	Len	"Jane Sherston"
Q116159881	Amul	"Joan Sherston"

# Q116159960  Patrick Barclay, of Gartley|Garntully  ->  Patrick Barclay, of Gartley   + Patrick Barclay, of Garntully
Q116159960	Lmul	"Patrick Barclay, of Gartley"
Q116159960	Len	"Patrick Barclay, of Gartley"
Q116159960	Amul	"Patrick Barclay, of Garntully"

# Q116160044  Sir Giles|Gyles Bray, of Great Barrington  ->  Sir Giles Bray, of Great Barrington   + Sir Gyles Bray, of Great Barrington
Q116160044	Lmul	"Sir Giles Bray, of Great Barrington"
Q116160044	Len	"Sir Giles Bray, of Great Barrington"
Q116160044	Amul	"Sir Gyles Bray, of Great Barrington"

# Q116160489  Jane|Margaret Drury  ->  Jane Drury   + Margaret Drury
Q116160489	Lmul	"Jane Drury"
Q116160489	Len	"Jane Drury"
Q116160489	Amul	"Margaret Drury"

# Q116160556  William|Henry de Kingscote, of Kingscote  ->  William de Kingscote, of Kingscote   + Henry de Kingscote, of Kingscote
Q116160556	Lmul	"William de Kingscote, of Kingscote"
Q116160556	Len	"William de Kingscote, of Kingscote"
Q116160556	Amul	"Henry de Kingscote, of Kingscote"

# Q116168675  Jacob de Rho|Rota  ->  Jacob de Rho   + Jacob de Rota
Q116168675	Lmul	"Jacob de Rho"
Q116168675	Len	"Jacob de Rho"
Q116168675	Amul	"Jacob de Rota"

# Q116168884  Eleanor|Elizabeth Veale  ->  Eleanor Veale   + Elizabeth Veale
Q116168884	Lmul	"Eleanor Veale"
Q116168884	Len	"Eleanor Veale"
Q116168884	Amul	"Elizabeth Veale"

# Q116168892  Richard|Robert Turgis, of Melcombe, Dorset  ->  Richard Turgis, of Melcombe, Dorset   + Robert Turgis, of Melcombe, Dorset
Q116168892	Lmul	"Richard Turgis, of Melcombe, Dorset"
Q116168892	Len	"Richard Turgis, of Melcombe, Dorset"
Q116168892	Amul	"Robert Turgis, of Melcombe, Dorset"

# Q116168923  Jean|Joneta Barclay  ->  Jean Barclay   + Joneta Barclay
Q116168923	Lmul	"Jean Barclay"
Q116168923	Len	"Jean Barclay"
Q116168923	Amul	"Joneta Barclay"

# Q116169014  Geoffrey|Galfridus de Staunton  ->  Geoffrey de Staunton   + Galfridus de Staunton
Q116169014	Lmul	"Geoffrey de Staunton"
Q116169014	Len	"Geoffrey de Staunton"
Q116169014	Amul	"Galfridus de Staunton"

# Q116169015  Malgerus|Mauger  ->  Malgerus   + Mauger
Q116169015	Lmul	"Malgerus"
Q116169015	Len	"Malgerus"
Q116169015	Amul	"Mauger"

# Q116169036  Emoine|Edmunda le Boteler  ->  Emoine le Boteler   + Edmunda le Boteler
Q116169036	Lmul	"Emoine le Boteler"
Q116169036	Len	"Emoine le Boteler"
Q116169036	Amul	"Edmunda le Boteler"

# Q116169737  Alexandra|Alice Lugg  ->  Alexandra Lugg   + Alice Lugg
Q116169737	Lmul	"Alexandra Lugg"
Q116169737	Len	"Alexandra Lugg"
Q116169737	Amul	"Alice Lugg"

# Q116169746  Edward|Walter Fowler, of Stonehouse  ->  Edward Fowler, of Stonehouse   + Walter Fowler, of Stonehouse
Q116169746	Lmul	"Edward Fowler, of Stonehouse"
Q116169746	Len	"Edward Fowler, of Stonehouse"
Q116169746	Amul	"Walter Fowler, of Stonehouse"

# Q116169749  Judith|Margery Bennet, of Stonehouse  ->  Judith Bennet, of Stonehouse   + Margery Bennet, of Stonehouse
Q116169749	Lmul	"Judith Bennet, of Stonehouse"
Q116169749	Len	"Judith Bennet, of Stonehouse"
Q116169749	Amul	"Margery Bennet, of Stonehouse"

# Q116169815  Thomas|William Jennyns  ->  Thomas Jennyns   + William Jennyns
Q116169815	Lmul	"Thomas Jennyns"
Q116169815	Len	"Thomas Jennyns"
Q116169815	Amul	"William Jennyns"

# Q116171556  Alison|Alice Neville, of Liversedge  ->  Alison Neville, of Liversedge   + Alice Neville, of Liversedge
Q116171556	Lmul	"Alison Neville, of Liversedge"
Q116171556	Len	"Alison Neville, of Liversedge"
Q116171556	Amul	"Alice Neville, of Liversedge"

# Q116171577  Margaret|Anne Laxham  ->  Margaret Laxham   + Anne Laxham
Q116171577	Lmul	"Margaret Laxham"
Q116171577	Len	"Margaret Laxham"
Q116171577	Amul	"Anne Laxham"

# Q116172147  Ann|Joan Broughton  ->  Ann Broughton   + Joan Broughton
Q116172147	Lmul	"Ann Broughton"
Q116172147	Len	"Ann Broughton"
Q116172147	Amul	"Joan Broughton"

# Q116173950  Irmgard|Irmesind von Daun zu Wolkringen  ->  Irmgard von Daun zu Wolkringen   + Irmesind von Daun zu Wolkringen
Q116173950	Lmul	"Irmgard von Daun zu Wolkringen"
Q116173950	Len	"Irmgard von Daun zu Wolkringen"
Q116173950	Amul	"Irmesind von Daun zu Wolkringen"

# Q116174056  Adelheid|Aleide von Wildenberg  ->  Adelheid von Wildenberg   + Aleide von Wildenberg
Q116174056	Lmul	"Adelheid von Wildenberg"
Q116174056	Len	"Adelheid von Wildenberg"
Q116174056	Amul	"Aleide von Wildenberg"

# Q116174227  Joan|Agnes|Eleanor Milbourn (Milborne)  ->  Joan Milbourn (Milborne)   + Agnes Milbourn (Milborne) | Eleanor Milbourn (Milborne)
Q116174227	Lmul	"Joan Milbourn (Milborne)"
Q116174227	Len	"Joan Milbourn (Milborne)"
Q116174227	Amul	"Agnes Milbourn (Milborne)"
Q116174227	Amul	"Eleanor Milbourn (Milborne)"

# Q116177435  Kater|Katerina ze Hedcan  ->  Kater ze Hedcan   + Katerina ze Hedcan
Q116177435	Len	"Kater ze Hedcan"
Q116177435	Amul	"Katerina ze Hedcan"

# Q116177560  Nikolaus|Niklaus von Wattenwyl (Watteville)  ->  Nikolaus von Wattenwyl (Watteville)   + Niklaus von Wattenwyl (Watteville)
Q116177560	Lmul	"Nikolaus von Wattenwyl (Watteville)"
Q116177560	Len	"Nikolaus von Wattenwyl (Watteville)"
Q116177560	Amul	"Niklaus von Wattenwyl (Watteville)"

# Q116177565  Urban|Ulrich von Mühleren, Herr von Burgistein  ->  Urban von Mühleren, Herr von Burgistein   + Ulrich von Mühleren, Herr von Burgistein
Q116177565	Lmul	"Urban von Mühleren, Herr von Burgistein"
Q116177565	Len	"Urban von Mühleren, Herr von Burgistein"
Q116177565	Amul	"Ulrich von Mühleren, Herr von Burgistein"

# Q116177576  Adelheid|Elisabeth Meiss  ->  Adelheid Meiss   + Elisabeth Meiss
Q116177576	Lmul	"Adelheid Meiss"
Q116177576	Len	"Adelheid Meiss"
Q116177576	Amul	"Elisabeth Meiss"

# Q116177680  Catherine|Marguerite de Vuillens  ->  Catherine de Vuillens   + Marguerite de Vuillens
Q116177680	Lmul	"Catherine de Vuillens"
Q116177680	Len	"Catherine de Vuillens"
Q116177680	Amul	"Marguerite de Vuillens"

# Q116177685  Ancelis|Amphélise  ->  Ancelis   + Amphélise
Q116177685	Lmul	"Ancelis"
Q116177685	Len	"Ancelis"
Q116177685	Amul	"Amphélise"

# Q116177694  Jacqueline|Jakobea de Duyns  ->  Jacqueline de Duyns   + Jakobea de Duyns
Q116177694	Lmul	"Jacqueline de Duyns"
Q116177694	Len	"Jacqueline de Duyns"
Q116177694	Amul	"Jakobea de Duyns"

# Q116177713  Jeannette|Jordane de Cossonay  ->  Jeannette de Cossonay   + Jordane de Cossonay
Q116177713	Lmul	"Jeannette de Cossonay"
Q116177713	Len	"Jeannette de Cossonay"
Q116177713	Amul	"Jordane de Cossonay"

# Q116177726  Jean|Guillaume de Saint-Armour, seigneur de Vincelles  ->  Jean de Saint-Armour, seigneur de Vincelles   + Guillaume de Saint-Armour, seigneur de Vincelles
Q116177726	Lmul	"Jean de Saint-Armour, seigneur de Vincelles"
Q116177726	Len	"Jean de Saint-Armour, seigneur de Vincelles"
Q116177726	Amul	"Guillaume de Saint-Armour, seigneur de Vincelles"

# Q116177733  Marguerite|Mathilde de Thoyre (Thoire-Villars)  ->  Marguerite de Thoyre (Thoire-Villars)   + Mathilde de Thoyre (Thoire-Villars)
Q116177733	Lmul	"Marguerite de Thoyre (Thoire-Villars)"
Q116177733	Len	"Marguerite de Thoyre (Thoire-Villars)"
Q116177733	Amul	"Mathilde de Thoyre (Thoire-Villars)"

# Q116177750  Elizabeth|Anne Balderston  ->  Elizabeth Balderston   + Anne Balderston
Q116177750	Lmul	"Elizabeth Balderston"
Q116177750	Len	"Elizabeth Balderston"
Q116177750	Amul	"Anne Balderston"

# Q116177754  Alan|William Singleton, of the Tower  ->  Alan Singleton, of the Tower   + William Singleton, of the Tower
Q116177754	Lmul	"Alan Singleton, of the Tower"
Q116177754	Len	"Alan Singleton, of the Tower"
Q116177754	Amul	"William Singleton, of the Tower"

# Q116177782  William|Thomas Carus, of Ashworth  ->  William Carus, of Ashworth   + Thomas Carus, of Ashworth
Q116177782	Lmul	"William Carus, of Ashworth"
Q116177782	Len	"William Carus, of Ashworth"
Q116177782	Amul	"Thomas Carus, of Ashworth"

# Q116177783  William|Richard Carus, of Ashworth  ->  William Carus, of Ashworth   + Richard Carus, of Ashworth
Q116177783	Lmul	"William Carus, of Ashworth"
Q116177783	Len	"William Carus, of Ashworth"
Q116177783	Amul	"Richard Carus, of Ashworth"

# Q116177813  Margaret|Elizabeth Cobham  ->  Margaret Cobham   + Elizabeth Cobham
Q116177813	Lmul	"Margaret Cobham"
Q116177813	Len	"Margaret Cobham"
Q116177813	Amul	"Elizabeth Cobham"

# Q116178153  Watkin|Walter ap Richard Gunter  ->  Watkin ap Richard Gunter   + Walter ap Richard Gunter
Q116178153	Lmul	"Watkin ap Richard Gunter"
Q116178153	Len	"Watkin ap Richard Gunter"
Q116178153	Amul	"Walter ap Richard Gunter"

# Q116180032  Elizabeth|Edith Twinihoe (Twinyho), of Keyford  ->  Elizabeth Twinihoe (Twinyho), of Keyford   + Edith Twinihoe (Twinyho), of Keyford
Q116180032	Lmul	"Elizabeth Twinihoe (Twinyho), of Keyford"
Q116180032	Len	"Elizabeth Twinihoe (Twinyho), of Keyford"
Q116180032	Amul	"Edith Twinihoe (Twinyho), of Keyford"

# Q116182874  Kunz Osiander|Osanner  ->  Kunz Osiander   + Kunz Osanner
Q116182874	Lmul	"Kunz Osiander"
Q116182874	Len	"Kunz Osiander"
Q116182874	Amul	"Kunz Osanner"

# Q116183109  Eva|Ella Lösch  ->  Eva Lösch   + Ella Lösch
Q116183109	Lmul	"Eva Lösch"
Q116183109	Len	"Eva Lösch"
Q116183109	Amul	"Ella Lösch"

# Q116183134  Nikolaus|Klaus Märklin  ->  Nikolaus Märklin   + Klaus Märklin
Q116183134	Lmul	"Nikolaus Märklin"
Q116183134	Len	"Nikolaus Märklin"
Q116183134	Amul	"Klaus Märklin"

# Q116183868  Albrecht|Aberlin Volland, Vogt  ->  Albrecht Volland, Vogt   + Aberlin Volland, Vogt
Q116183868	Lmul	"Albrecht Volland, Vogt"
Q116183868	Len	"Albrecht Volland, Vogt"
Q116183868	Amul	"Aberlin Volland, Vogt"

# Q116454884  Edmund|Edward Warneford, of Sevenhampton  ->  Edmund Warneford, of Sevenhampton   + Edward Warneford, of Sevenhampton
Q116454884	Lmul	"Edmund Warneford, of Sevenhampton"
Q116454884	Len	"Edmund Warneford, of Sevenhampton"
Q116454884	Amul	"Edward Warneford, of Sevenhampton"

# Q116454919  Richard|Raphe Flyer, of Uttoxeter, Staffs  ->  Richard Flyer, of Uttoxeter, Staffs   + Raphe Flyer, of Uttoxeter, Staffs
Q116454919	Lmul	"Richard Flyer, of Uttoxeter, Staffs"
Q116454919	Len	"Richard Flyer, of Uttoxeter, Staffs"
Q116454919	Amul	"Raphe Flyer, of Uttoxeter, Staffs"

# Q116469808  Wilcock|William Lewrch alias Clerke, of Knoyles Place, Llantwit  ->  Wilcock Lewrch alias Clerke, of Knoyles Place, Llantwit   + William Lewrch alias Clerke, of Knoyles Place, Llantwit
Q116469808	Lmul	"Wilcock Lewrch alias Clerke, of Knoyles Place, Llantwit"
Q116469808	Len	"Wilcock Lewrch alias Clerke, of Knoyles Place, Llantwit"
Q116469808	Amul	"William Lewrch alias Clerke, of Knoyles Place, Llantwit"

# Q116470885  Rossor|Roger ap John|Jenkin ap Hywel ab Ieuan of Llanhenog  ->  Rossor ap John ap Hywel ab Ieuan of Llanhenog   + Roger ap Jenkin ap Hywel ab Ieuan of Llanhenog
Q116470885	Lmul	"Rossor ap John ap Hywel ab Ieuan of Llanhenog"
Q116470885	Len	"Rossor ap John ap Hywel ab Ieuan of Llanhenog"
Q116470885	Amul	"Roger ap Jenkin ap Hywel ab Ieuan of Llanhenog"

# Q116470886  John|Jenkin ap Hywel ab Ieuan ap Meurig pf Llanover  ->  John ap Hywel ab Ieuan ap Meurig pf Llanover   + Jenkin ap Hywel ab Ieuan ap Meurig pf Llanover
Q116470886	Lmul	"John ap Hywel ab Ieuan ap Meurig pf Llanover"
Q116470886	Len	"John ap Hywel ab Ieuan ap Meurig pf Llanover"
Q116470886	Amul	"Jenkin ap Hywel ab Ieuan ap Meurig pf Llanover"

# Q116470910  Reynold|Rheinallt ap Gwilym Powell, of Perth-hir  ->  Reynold ap Gwilym Powell, of Perth-hir   + Rheinallt ap Gwilym Powell, of Perth-hir
Q116470910	Lmul	"Reynold ap Gwilym Powell, of Perth-hir"
Q116470910	Len	"Reynold ap Gwilym Powell, of Perth-hir"
Q116470910	Amul	"Rheinallt ap Gwilym Powell, of Perth-hir"

# Q116477674  Llywelyn Moel|Foel ap Hywel ap Tegwared Fychan ap Tegwared  ->  Llywelyn Moel ap Hywel ap Tegwared Fychan ap Tegwared   + Llywelyn Foel ap Hywel ap Tegwared Fychan ap Tegwared
Q116477674	Lmul	"Llywelyn Moel ap Hywel ap Tegwared Fychan ap Tegwared"
Q116477674	Len	"Llywelyn Moel ap Hywel ap Tegwared Fychan ap Tegwared"
Q116477674	Amul	"Llywelyn Foel ap Hywel ap Tegwared Fychan ap Tegwared"

# Q116478238  Gronwy Sais ap Richard|Rhys ap Gruffudd Ddwn ab Iorwerth  ->  Gronwy Sais ap Richard ap Gruffudd Ddwn ab Iorwerth   + Gronwy Sais ap Rhys ap Gruffudd Ddwn ab Iorwerth
Q116478238	Lmul	"Gronwy Sais ap Richard ap Gruffudd Ddwn ab Iorwerth"
Q116478238	Len	"Gronwy Sais ap Richard ap Gruffudd Ddwn ab Iorwerth"
Q116478238	Amul	"Gronwy Sais ap Rhys ap Gruffudd Ddwn ab Iorwerth"

# Q116478248  Sir John|Jenkin Donne, of Utkinton  ->  Sir John Donne, of Utkinton   + Sir Jenkin Donne, of Utkinton
Q116478248	Lmul	"Sir John Donne, of Utkinton"
Q116478248	Len	"Sir John Donne, of Utkinton"
Q116478248	Amul	"Sir Jenkin Donne, of Utkinton"

# Q116478542  John ap Robin|Robert Fychan ap Gruffudd ap Hywel Wynn alias Whyte  ->  John ap Robin Fychan ap Gruffudd ap Hywel Wynn alias Whyte   + John ap Robert Fychan ap Gruffudd ap Hywel Wynn alias Whyte
Q116478542	Lmul	"John ap Robin Fychan ap Gruffudd ap Hywel Wynn alias Whyte"
Q116478542	Len	"John ap Robin Fychan ap Gruffudd ap Hywel Wynn alias Whyte"
Q116478542	Amul	"John ap Robert Fychan ap Gruffudd ap Hywel Wynn alias Whyte"

# Q116478704  Nest|Annes ferch Gruffudd ap John ap Gruffudd  ->  Nest ferch Gruffudd ap John ap Gruffudd   + Annes ferch Gruffudd ap John ap Gruffudd
Q116478704	Lmul	"Nest ferch Gruffudd ap John ap Gruffudd"
Q116478704	Len	"Nest ferch Gruffudd ap John ap Gruffudd"
Q116478704	Amul	"Annes ferch Gruffudd ap John ap Gruffudd"

# Q116478775  Jonet|Elliw ferch Ieuan ap Llywelyn ap Gruffudd Llwyd  ->  Jonet ferch Ieuan ap Llywelyn ap Gruffudd Llwyd   + Elliw ferch Ieuan ap Llywelyn ap Gruffudd Llwyd
Q116478775	Lmul	"Jonet ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"
Q116478775	Len	"Jonet ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"
Q116478775	Amul	"Elliw ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"

# Q116478989  Mali|Gwladus ferch Ieuan ap Llywelyn ap Gruffudd Llwyd  ->  Mali ferch Ieuan ap Llywelyn ap Gruffudd Llwyd   + Gwladus ferch Ieuan ap Llywelyn ap Gruffudd Llwyd
Q116478989	Lmul	"Mali ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"
Q116478989	Len	"Mali ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"
Q116478989	Amul	"Gwladus ferch Ieuan ap Llywelyn ap Gruffudd Llwyd"

# Q116480345  Anne|Alice de Botreaux  ->  Anne de Botreaux   + Alice de Botreaux
Q116480345	Lmul	"Anne de Botreaux"
Q116480345	Len	"Anne de Botreaux"
Q116480345	Amul	"Alice de Botreaux"

# Q116812065  Jennet|Sionet ferch Lewys Raglan, of Vorganwg  ->  Jennet ferch Lewys Raglan, of Vorganwg   + Sionet ferch Lewys Raglan, of Vorganwg
Q116812065	Lmul	"Jennet ferch Lewys Raglan, of Vorganwg"
Q116812065	Len	"Jennet ferch Lewys Raglan, of Vorganwg"
Q116812065	Amul	"Sionet ferch Lewys Raglan, of Vorganwg"

# Q116812185  Julian|Joan Hawey, of St.Donat's  ->  Julian Hawey, of St.Donat's   + Joan Hawey, of St.Donat's
Q116812185	Lmul	"Julian Hawey, of St.Donat's"
Q116812185	Len	"Julian Hawey, of St.Donat's"
Q116812185	Amul	"Joan Hawey, of St.Donat's"

# Q116812456  Richard|Rhys ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan  ->  Richard ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan   + Rhys ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan
Q116812456	Lmul	"Richard ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan"
Q116812456	Len	"Richard ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan"
Q116812456	Amul	"Rhys ap Gruffudd Ddwn ab Iorwerth ap Maredudd of Mertyn Uwch Glan"

# Q116812564  Margred ferch Thomas|Gwilym Bawdrip  ->  Margred ferch Thomas Bawdrip   + Margred ferch Gwilym Bawdrip
Q116812564	Lmul	"Margred ferch Thomas Bawdrip"
Q116812564	Len	"Margred ferch Thomas Bawdrip"
Q116812564	Amul	"Margred ferch Gwilym Bawdrip"

# Q116812565  Thomas|Gwilym Bawdrip, of Penmark  ->  Thomas Bawdrip, of Penmark   + Gwilym Bawdrip, of Penmark
Q116812565	Lmul	"Thomas Bawdrip, of Penmark"
Q116812565	Len	"Thomas Bawdrip, of Penmark"
Q116812565	Amul	"Gwilym Bawdrip, of Penmark"

# Q116854564  Lady Mairi|Marjory Sinclair  ->  Lady Mairi Sinclair   + Lady Marjory Sinclair
Q116854564	Lmul	"Lady Mairi Sinclair"
Q116854564	Len	"Lady Mairi Sinclair"
Q116854564	Amul	"Lady Marjory Sinclair"

# Q117024927  Anne|Agnes Huntington  ->  Anne Huntington   + Agnes Huntington
Q117024927	Lmul	"Anne Huntington"
Q117024927	Len	"Anne Huntington"
Q117024927	Amul	"Agnes Huntington"

# Q117243145  Johann|Hans Swellengrebel  ->  Johann Swellengrebel   + Hans Swellengrebel
Q117243145	Lmul	"Johann Swellengrebel"
Q117243145	Len	"Johann Swellengrebel"
Q117243145	Amul	"Hans Swellengrebel"

# Q117243157  Balthasar|Filerectus Fademrecht  ->  Balthasar Fademrecht   + Filerectus Fademrecht
Q117243157	Lmul	"Balthasar Fademrecht"
Q117243157	Len	"Balthasar Fademrecht"
Q117243157	Amul	"Filerectus Fademrecht"

# Q117243361  Hans|Johann Schwellengrebel  ->  Hans Schwellengrebel   + Johann Schwellengrebel
Q117243361	Lmul	"Hans Schwellengrebel"
Q117243361	Len	"Hans Schwellengrebel"
Q117243361	Amul	"Johann Schwellengrebel"

# Q117245776  Philip Philipszoon Kuvel|Quivel|Quiveel  ->  Philip Philipszoon Kuvel   + Philip Philipszoon Quivel | Philip Philipszoon Quiveel
Q117245776	Lmul	"Philip Philipszoon Kuvel"
Q117245776	Len	"Philip Philipszoon Kuvel"
Q117245776	Amul	"Philip Philipszoon Quivel"
Q117245776	Amul	"Philip Philipszoon Quiveel"

# Q117302656  Eleanor|Elinor Warren  ->  Eleanor Warren   + Elinor Warren
Q117302656	Lmul	"Eleanor Warren"
Q117302656	Len	"Eleanor Warren"
Q117302656	Amul	"Elinor Warren"

# Q117302950  Margaret|Margery Bostock  ->  Margaret Bostock   + Margery Bostock
Q117302950	Lmul	"Margaret Bostock"
Q117302950	Len	"Margaret Bostock"
Q117302950	Amul	"Margery Bostock"

# Q117306706  Dafydd|Deicws ap Madog ap Dafydd Gôch ap Dafydd Hên  ->  Dafydd ap Madog ap Dafydd Gôch ap Dafydd Hên   + Deicws ap Madog ap Dafydd Gôch ap Dafydd Hên
Q117306706	Lmul	"Dafydd ap Madog ap Dafydd Gôch ap Dafydd Hên"
Q117306706	Len	"Dafydd ap Madog ap Dafydd Gôch ap Dafydd Hên"
Q117306706	Amul	"Deicws ap Madog ap Dafydd Gôch ap Dafydd Hên"

# Q117306988  Elsbeth|Elizabeth ferch John ap Humphrey Grey  ->  Elsbeth ferch John ap Humphrey Grey   + Elizabeth ferch John ap Humphrey Grey
Q117306988	Lmul	"Elsbeth ferch John ap Humphrey Grey"
Q117306988	Len	"Elsbeth ferch John ap Humphrey Grey"
Q117306988	Amul	"Elizabeth ferch John ap Humphrey Grey"

# Q117378853  Margred|Jane Dyer, of Boulston  ->  Margred Dyer, of Boulston   + Jane Dyer, of Boulston
Q117378853	Lmul	"Margred Dyer, of Boulston"
Q117378853	Len	"Margred Dyer, of Boulston"
Q117378853	Amul	"Jane Dyer, of Boulston"

# Q118173835  Margaret|Mary Chute  ->  Margaret Chute   + Mary Chute
Q118173835	Lmul	"Margaret Chute"
Q118173835	Len	"Margaret Chute"
Q118173835	Amul	"Mary Chute"

# Q121340516  Lewis|Ludowick Walker, of Bramshall  ->  Lewis Walker, of Bramshall   + Ludowick Walker, of Bramshall
Q121340516	Lmul	"Lewis Walker, of Bramshall"
Q121340516	Len	"Lewis Walker, of Bramshall"
Q121340516	Amul	"Ludowick Walker, of Bramshall"

# Q121344808  Isabel|Elizabeth de Harcourt  ->  Isabel de Harcourt   + Elizabeth de Harcourt
Q121344808	Lmul	"Isabel de Harcourt"
Q121344808	Len	"Isabel de Harcourt"
Q121344808	Amul	"Elizabeth de Harcourt"

# Q122260514  Margaret|Mary Herbert  ->  Margaret Herbert   + Mary Herbert
Q122260514	Lmul	"Margaret Herbert"
Q122260514	Len	"Margaret Herbert"
Q122260514	Amul	"Mary Herbert"

# Q122260550  Dydvil|Maud ferch Thomas ap Gwilym ap Jenkin  ->  Dydvil ferch Thomas ap Gwilym ap Jenkin   + Maud ferch Thomas ap Gwilym ap Jenkin
Q122260550	Lmul	"Dydvil ferch Thomas ap Gwilym ap Jenkin"
Q122260550	Len	"Dydvil ferch Thomas ap Gwilym ap Jenkin"
Q122260550	Amul	"Maud ferch Thomas ap Gwilym ap Jenkin"

# Q122360620  Egidia|Giles Moray (Murray), of Culbin  ->  Egidia Moray (Murray), of Culbin   + Giles Moray (Murray), of Culbin
Q122360620	Lmul	"Egidia Moray (Murray), of Culbin"
Q122360620	Len	"Egidia Moray (Murray), of Culbin"
Q122360620	Amul	"Giles Moray (Murray), of Culbin"

# Q122360623  Cristina|Christian Mercer  ->  Cristina Mercer   + Christian Mercer
Q122360623	Lmul	"Cristina Mercer"
Q122360623	Len	"Cristina Mercer"
Q122360623	Amul	"Christian Mercer"

# Q122361169  Joanna|Joan Hoord  ->  Joanna Hoord   + Joan Hoord
Q122361169	Lmul	"Joanna Hoord"
Q122361169	Len	"Joanna Hoord"
Q122361169	Amul	"Joan Hoord"

# Q122361173  Eleanor|Helen Mytton  ->  Eleanor Mytton   + Helen Mytton
Q122361173	Lmul	"Eleanor Mytton"
Q122361173	Len	"Eleanor Mytton"
Q122361173	Amul	"Helen Mytton"

# Q122361403  Joan|Jane Yonge  ->  Joan Yonge   + Jane Yonge
Q122361403	Lmul	"Joan Yonge"
Q122361403	Len	"Joan Yonge"
Q122361403	Amul	"Jane Yonge"

# Q122361620  Gwylawg|Gwallawe|Gwallog ab Eginyn ap Llesab Idnerth Benfras  ->  Gwylawg ab Eginyn ap Llesab Idnerth Benfras   + Gwallawe ab Eginyn ap Llesab Idnerth Benfras | Gwallog ab Eginyn ap Llesab Idnerth Benfras
Q122361620	Lmul	"Gwylawg ab Eginyn ap Llesab Idnerth Benfras"
Q122361620	Len	"Gwylawg ab Eginyn ap Llesab Idnerth Benfras"
Q122361620	Amul	"Gwallawe ab Eginyn ap Llesab Idnerth Benfras"
Q122361620	Amul	"Gwallog ab Eginyn ap Llesab Idnerth Benfras"

# Q122361761  Jean|Euphemia Lumsden  ->  Jean Lumsden   + Euphemia Lumsden
Q122361761	Lmul	"Jean Lumsden"
Q122361761	Len	"Jean Lumsden"
Q122361761	Amul	"Euphemia Lumsden"

# Q122362409  Marike|Magdalena Anthonisse  ->  Marike Anthonisse   + Magdalena Anthonisse
Q122362409	Lmul	"Marike Anthonisse"
Q122362409	Len	"Marike Anthonisse"
Q122362409	Amul	"Magdalena Anthonisse"

# Q122362846  Joan|Margaret Tempest, of Bracewell  ->  Joan Tempest, of Bracewell   + Margaret Tempest, of Bracewell
Q122362846	Lmul	"Joan Tempest, of Bracewell"
Q122362846	Len	"Joan Tempest, of Bracewell"
Q122362846	Amul	"Margaret Tempest, of Bracewell"

# Q122364354  Robert|Francis Gale, of Akeham Grange  ->  Robert Gale, of Akeham Grange   + Francis Gale, of Akeham Grange
Q122364354	Lmul	"Robert Gale, of Akeham Grange"
Q122364354	Len	"Robert Gale, of Akeham Grange"
Q122364354	Amul	"Francis Gale, of Akeham Grange"

# Q122364561  James|Robert Danby, of Thorpe, Yorks  ->  James Danby, of Thorpe, Yorks   + Robert Danby, of Thorpe, Yorks
Q122364561	Lmul	"James Danby, of Thorpe, Yorks"
Q122364561	Len	"James Danby, of Thorpe, Yorks"
Q122364561	Amul	"Robert Danby, of Thorpe, Yorks"

# Q122364575  Margery|Margaret|Marian Constable  ->  Margery Constable   + Margaret Constable | Marian Constable
Q122364575	Lmul	"Margery Constable"
Q122364575	Len	"Margery Constable"
Q122364575	Amul	"Margaret Constable"
Q122364575	Amul	"Marian Constable"

# Q122677838  Roger|Ralph de Wynfield, of Edelstowe Hall  ->  Roger de Wynfield, of Edelstowe Hall   + Ralph de Wynfield, of Edelstowe Hall
Q122677838	Lmul	"Roger de Wynfield, of Edelstowe Hall"
Q122677838	Len	"Roger de Wynfield, of Edelstowe Hall"
Q122677838	Amul	"Ralph de Wynfield, of Edelstowe Hall"

# Q123207015  Sir Edmund|Edward Molineux  ->  Sir Edmund Molineux   + Sir Edward Molineux
Q123207015	Lmul	"Sir Edmund Molineux"
Q123207015	Len	"Sir Edmund Molineux"
Q123207015	Amul	"Sir Edward Molineux"

# Q123207019  Dorothy|Dorathey Paynell  ->  Dorothy Paynell   + Dorathey Paynell
Q123207019	Lmul	"Dorothy Paynell"
Q123207019	Len	"Dorothy Paynell"
Q123207019	Amul	"Dorathey Paynell"

# Q123207204  Richard|George Lascelles, of Stourton  ->  Richard Lascelles, of Stourton   + George Lascelles, of Stourton
Q123207204	Lmul	"Richard Lascelles, of Stourton"
Q123207204	Len	"Richard Lascelles, of Stourton"
Q123207204	Amul	"George Lascelles, of Stourton"

# Q123585207  Johannes|Hannu Nissenpoika Pose, land commissioner  ->  Johannes Nissenpoika Pose, land commissioner   + Hannu Nissenpoika Pose, land commissioner
Q123585207	Lmul	"Johannes Nissenpoika Pose, land commissioner"
Q123585207	Len	"Johannes Nissenpoika Pose, land commissioner"
Q123585207	Amul	"Hannu Nissenpoika Pose, land commissioner"

# Q123651999  Rensie Feddans|Fedders  ->  Rensie Feddans   + Rensie Fedders
Q123651999	Lmul	"Rensie Feddans"
Q123651999	Len	"Rensie Feddans"
Q123651999	Amul	"Rensie Fedders"

# Q125524447  Margaret|Marion Cathcart  ->  Margaret Cathcart   + Marion Cathcart
Q125524447	Lmul	"Margaret Cathcart"
Q125524447	Len	"Margaret Cathcart"
Q125524447	Amul	"Marion Cathcart"

# Q125569134  Robert Cowton, of Burgh|Brough  ->  Robert Cowton, of Burgh   + Robert Cowton, of Brough
Q125569134	Lmul	"Robert Cowton, of Burgh"
Q125569134	Len	"Robert Cowton, of Burgh"
Q125569134	Amul	"Robert Cowton, of Brough"

# Q125569183  Jane|Joan Muswell  ->  Jane Muswell   + Joan Muswell
Q125569183	Lmul	"Jane Muswell"
Q125569183	Len	"Jane Muswell"
Q125569183	Amul	"Joan Muswell"

# Q126902898  Ida|Odette du Chastelet (Châtelet)  ->  Ida du Chastelet (Châtelet)   + Odette du Chastelet (Châtelet)
Q126902898	Lmul	"Ida du Chastelet (Châtelet)"
Q126902898	Len	"Ida du Chastelet (Châtelet)"
Q126902898	Amul	"Odette du Chastelet (Châtelet)"

# Q126938430  Hugh|Hew Wallace, of Cairnhill|Carnell  ->  Hugh Wallace, of Cairnhill   + Hew Wallace, of Carnell
Q126938430	Lmul	"Hugh Wallace, of Cairnhill"
Q126938430	Len	"Hugh Wallace, of Cairnhill"
Q126938430	Amul	"Hew Wallace, of Carnell"

# Q126938448  Margaret Fresale|Fraser  ->  Margaret Fresale   + Margaret Fraser
Q126938448	Lmul	"Margaret Fresale"
Q126938448	Len	"Margaret Fresale"
Q126938448	Amul	"Margaret Fraser"

# Q127225204  Ann|Amy Williams  ->  Ann Williams   + Amy Williams
Q127225204	Lmul	"Ann Williams"
Q127225204	Len	"Ann Williams"
Q127225204	Amul	"Amy Williams"

# Q127225219  Augustine|Austin Porter, of Belton, Lincs  ->  Augustine Porter, of Belton, Lincs   + Austin Porter, of Belton, Lincs
Q127225219	Lmul	"Augustine Porter, of Belton, Lincs"
Q127225219	Len	"Augustine Porter, of Belton, Lincs"
Q127225219	Amul	"Austin Porter, of Belton, Lincs"

# Q127225232  Rowland|Roger Wigmore, of Shobdon, Heref  ->  Rowland Wigmore, of Shobdon, Heref   + Roger Wigmore, of Shobdon, Heref
Q127225232	Lmul	"Rowland Wigmore, of Shobdon, Heref"
Q127225232	Len	"Rowland Wigmore, of Shobdon, Heref"
Q127225232	Amul	"Roger Wigmore, of Shobdon, Heref"

# Q127225239  Gwenffryd|Winifred Hacluyt (Hackluyt), of Tegeingl cantref  ->  Gwenffryd Hacluyt (Hackluyt), of Tegeingl cantref   + Winifred Hacluyt (Hackluyt), of Tegeingl cantref
Q127225239	Lmul	"Gwenffryd Hacluyt (Hackluyt), of Tegeingl cantref"
Q127225239	Len	"Gwenffryd Hacluyt (Hackluyt), of Tegeingl cantref"
Q127225239	Amul	"Winifred Hacluyt (Hackluyt), of Tegeingl cantref"

# Q127225314  Roger|William de la Zouche, of Lubbesthorpe  ->  Roger de la Zouche, of Lubbesthorpe   + William de la Zouche, of Lubbesthorpe
Q127225314	Lmul	"Roger de la Zouche, of Lubbesthorpe"
Q127225314	Len	"Roger de la Zouche, of Lubbesthorpe"
Q127225314	Amul	"William de la Zouche, of Lubbesthorpe"

# Q127227264  Agnes|Anne Cowper  ->  Agnes Cowper   + Anne Cowper
Q127227264	Lmul	"Agnes Cowper"
Q127227264	Len	"Agnes Cowper"
Q127227264	Amul	"Anne Cowper"

# Q127270212  Miikkula|Nigulis Jaenisch  ->  Miikkula Jaenisch   + Nigulis Jaenisch
Q127270212	Len	"Miikkula Jaenisch"
Q127270212	Amul	"Nigulis Jaenisch"

# Q127270449  'old'|'gamle' Olof i Bureå  ->  'old' Olof i Bureå   + 'gamle' Olof i Bureå
Q127270449	Lmul	"'old' Olof i Bureå"
Q127270449	Len	"'old' Olof i Bureå"
Q127270449	Amul	"'gamle' Olof i Bureå"

# Q127270487  Lorentz|Lars Hoyer  ->  Lorentz Hoyer   + Lars Hoyer
Q127270487	Lmul	"Lorentz Hoyer"
Q127270487	Len	"Lorentz Hoyer"
Q127270487	Amul	"Lars Hoyer"

# Q127270727  squire Peder Pederson Körning|Kyrning, , av (Kvissberg)  ->  squire Peder Pederson Körning , av (Kvissberg)   + squire Peder Pederson Kyrning, , av (Kvissberg)
Q127270727	Lmul	"squire Peder Pederson Körning , av (Kvissberg)"
Q127270727	Len	"squire Peder Pederson Körning , av (Kvissberg)"
Q127270727	Amul	"squire Peder Pederson Kyrning, , av (Kvissberg)"

# Q127270788  Erine|Irene  ->  Erine   + Irene
Q127270788	Lmul	"Erine"
Q127270788	Len	"Erine"
Q127270788	Amul	"Irene"

# Q127270880  Cecilie|Sidsel Gyntersdatter  ->  Cecilie Gyntersdatter   + Sidsel Gyntersdatter
Q127270880	Lmul	"Cecilie Gyntersdatter"
Q127270880	Len	"Cecilie Gyntersdatter"
Q127270880	Amul	"Sidsel Gyntersdatter"

# Q127270881  Sidsel|Cecilie  ->  Sidsel   + Cecilie
Q127270881	Lmul	"Sidsel"
Q127270881	Len	"Sidsel"
Q127270881	Amul	"Cecilie"

# Q127414037  Elizabeth|Elspeth Gray  ->  Elizabeth Gray   + Elspeth Gray
Q127414037	Lmul	"Elizabeth Gray"
Q127414037	Len	"Elizabeth Gray"
Q127414037	Amul	"Elspeth Gray"

# Q127687135  Ralph|Raufe Ayre, of Offerton  ->  Ralph Ayre, of Offerton   + Raufe Ayre, of Offerton
Q127687135	Lmul	"Ralph Ayre, of Offerton"
Q127687135	Len	"Ralph Ayre, of Offerton"
Q127687135	Amul	"Raufe Ayre, of Offerton"

# Q128804021  Catherine|Claude de Cardaillac  ->  Catherine de Cardaillac   + Claude de Cardaillac
Q128804021	Lmul	"Catherine de Cardaillac"
Q128804021	Len	"Catherine de Cardaillac"
Q128804021	Amul	"Claude de Cardaillac"

# Q128849381  Cecilia|Cecily Walker, of Cambridge  ->  Cecilia Walker, of Cambridge   + Cecily Walker, of Cambridge
Q128849381	Lmul	"Cecilia Walker, of Cambridge"
Q128849381	Len	"Cecilia Walker, of Cambridge"
Q128849381	Amul	"Cecily Walker, of Cambridge"

# Q128852643  Charles|Cormac McCarthy, of Carrignavar  ->  Charles McCarthy, of Carrignavar   + Cormac McCarthy, of Carrignavar
Q128852643	Lmul	"Charles McCarthy, of Carrignavar"
Q128852643	Len	"Charles McCarthy, of Carrignavar"
Q128852643	Amul	"Cormac McCarthy, of Carrignavar"

# Q128852646  Donald|Daniel McCarthy  ->  Donald McCarthy   + Daniel McCarthy
Q128852646	Lmul	"Donald McCarthy"
Q128852646	Len	"Donald McCarthy"
Q128852646	Amul	"Daniel McCarthy"

# Q128854440  Catherine|Julia Reagh  ->  Catherine Reagh   + Julia Reagh
Q128854440	Lmul	"Catherine Reagh"
Q128854440	Len	"Catherine Reagh"
Q128854440	Amul	"Julia Reagh"

# Q128854456  Ellen|Elana FitzGerald  ->  Ellen FitzGerald   + Elana FitzGerald
Q128854456	Lmul	"Ellen FitzGerald"
Q128854456	Len	"Ellen FitzGerald"
Q128854456	Amul	"Elana FitzGerald"

# Q129094761  Aimery|Amaury de Beth'san, Bailli of Cyprus, Signore di Tricarico  ->  Aimery de Beth'san, Bailli of Cyprus, Signore di Tricarico   + Amaury de Beth'san, Bailli of Cyprus, Signore di Tricarico
Q129094761	Lmul	"Aimery de Beth'san, Bailli of Cyprus, Signore di Tricarico"
Q129094761	Len	"Aimery de Beth'san, Bailli of Cyprus, Signore di Tricarico"
Q129094761	Amul	"Amaury de Beth'san, Bailli of Cyprus, Signore di Tricarico"

# Q129168340  Adam ap Robert|Roger ab Emerod Turberville, of Gwernvale  ->  Adam ap Robert ab Emerod Turberville, of Gwernvale   + Adam ap Roger ab Emerod Turberville, of Gwernvale
Q129168340	Lmul	"Adam ap Robert ab Emerod Turberville, of Gwernvale"
Q129168340	Len	"Adam ap Robert ab Emerod Turberville, of Gwernvale"
Q129168340	Amul	"Adam ap Roger ab Emerod Turberville, of Gwernvale"

# Q129168464  Isode|Isabel Farrington  ->  Isode Farrington   + Isabel Farrington
Q129168464	Lmul	"Isode Farrington"
Q129168464	Len	"Isode Farrington"
Q129168464	Amul	"Isabel Farrington"

# Q129168469  William|John Cheverell, of Chauntemarell  ->  William Cheverell, of Chauntemarell   + John Cheverell, of Chauntemarell
Q129168469	Lmul	"William Cheverell, of Chauntemarell"
Q129168469	Len	"William Cheverell, of Chauntemarell"
Q129168469	Amul	"John Cheverell, of Chauntemarell"

# Q129168770  Margery|Margred Wogan, of Prendergast  ->  Margery Wogan, of Prendergast   + Margred Wogan, of Prendergast
Q129168770	Lmul	"Margery Wogan, of Prendergast"
Q129168770	Len	"Margery Wogan, of Prendergast"
Q129168770	Amul	"Margred Wogan, of Prendergast"

# Q129169049  Mariot|Marion Drummond  ->  Mariot Drummond   + Marion Drummond
Q129169049	Lmul	"Mariot Drummond"
Q129169049	Len	"Mariot Drummond"
Q129169049	Amul	"Marion Drummond"

# Q129257001  Sidonia von Fictum|Vitzthum  ->  Sidonia von Fictum   + Sidonia von Vitzthum
Q129257001	Len	"Sidonia von Fictum"
Q129257001	Amul	"Sidonia von Vitzthum"

# Q129257376  Hester|Esther Sayer  ->  Hester Sayer   + Esther Sayer
Q129257376	Lmul	"Hester Sayer"
Q129257376	Len	"Hester Sayer"
Q129257376	Amul	"Esther Sayer"

# Q129730634  Elizabeth|Isabel Cuningham  ->  Elizabeth Cuningham   + Isabel Cuningham
Q129730634	Lmul	"Elizabeth Cuningham"
Q129730634	Len	"Elizabeth Cuningham"
Q129730634	Amul	"Isabel Cuningham"

# Q130332809  Idony|Idoine Cotesford  ->  Idony Cotesford   + Idoine Cotesford
Q130332809	Lmul	"Idony Cotesford"
Q130332809	Len	"Idony Cotesford"
Q130332809	Amul	"Idoine Cotesford"

# Q130334138  Margaretha|Margarethe von Marenholtz  ->  Margaretha von Marenholtz   + Margarethe von Marenholtz
Q130334138	Lmul	"Margaretha von Marenholtz"
Q130334138	Len	"Margaretha von Marenholtz"
Q130334138	Amul	"Margarethe von Marenholtz"

# Q130334293  Agnes|Anna von Hagen  ->  Agnes von Hagen   + Anna von Hagen
Q130334293	Len	"Agnes von Hagen"
Q130334293	Amul	"Anna von Hagen"

# Q130334431  Anna Juncker|de Joncker  ->  Anna Juncker Joncker   + Anna de Joncker
Q130334431	Lmul	"Anna Juncker Joncker"
Q130334431	Len	"Anna Juncker Joncker"
Q130334431	Amul	"Anna de Joncker"

# Q130334536  Toke|Tage|Thyge  ->  Toke   + Tage | Thyge
Q130334536	Lmul	"Toke"
Q130334536	Len	"Toke"
Q130334536	Amul	"Tage"
Q130334536	Amul	"Thyge"

# Q130334563  noble Sidsel|Cecilie Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup  ->  noble Sidsel Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup   + noble Cecilie Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup
Q130334563	Lmul	"noble Sidsel Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup"
Q130334563	Len	"noble Sidsel Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup"
Q130334563	Amul	"noble Cecilie Jonsdatter af Tommerup, heiress of Hyringsholm castle & Vedby & Knardrup"

# Q130334576  Peter Juncker|de Joncker  ->  Peter Juncker Joncker   + Peter de Joncker
Q130334576	Lmul	"Peter Juncker Joncker"
Q130334576	Len	"Peter Juncker Joncker"
Q130334576	Amul	"Peter de Joncker"

# Q130334775  Hedwig|Hese  ->  Hedwig   + Hese
Q130334775	Lmul	"Hedwig"
Q130334775	Len	"Hedwig"
Q130334775	Amul	"Hese"

# Q130335079  Agnes|Anne  ->  Agnes   + Anne
Q130335079	Lmul	"Agnes"
Q130335079	Len	"Agnes"
Q130335079	Amul	"Anne"

# Q130335373  Alice|Christiana Radcliffe  ->  Alice Radcliffe   + Christiana Radcliffe
Q130335373	Lmul	"Alice Radcliffe"
Q130335373	Len	"Alice Radcliffe"
Q130335373	Amul	"Christiana Radcliffe"

# Q130335378  Helen|Anne Parker  ->  Helen Parker   + Anne Parker
Q130335378	Lmul	"Helen Parker"
Q130335378	Len	"Helen Parker"
Q130335378	Amul	"Anne Parker"

# Q130335455  Lettice|Leticia Talbot  ->  Lettice Talbot   + Leticia Talbot
Q130335455	Lmul	"Lettice Talbot"
Q130335455	Len	"Lettice Talbot"
Q130335455	Amul	"Leticia Talbot"

# Q130335456  William|Parkin Talbot, of Shuttleworth Hall  ->  William Talbot, of Shuttleworth Hall   + Parkin Talbot, of Shuttleworth Hall
Q130335456	Lmul	"William Talbot, of Shuttleworth Hall"
Q130335456	Len	"William Talbot, of Shuttleworth Hall"
Q130335456	Amul	"Parkin Talbot, of Shuttleworth Hall"

# Q130335466  Agnes|Elizabeth  ->  Agnes   + Elizabeth
Q130335466	Lmul	"Agnes"
Q130335466	Len	"Agnes"
Q130335466	Amul	"Elizabeth"

# Q130335481  Isabella|Elizabeth Atherton  ->  Isabella Atherton   + Elizabeth Atherton
Q130335481	Lmul	"Isabella Atherton"
Q130335481	Len	"Isabella Atherton"
Q130335481	Amul	"Elizabeth Atherton"

# Q130335548  Jorveth|Yarwit de Hulton  ->  Jorveth de Hulton   + Yarwit de Hulton
Q130335548	Lmul	"Jorveth de Hulton"
Q130335548	Len	"Jorveth de Hulton"
Q130335548	Amul	"Yarwit de Hulton"

# Q130335568  Henry|John Gurney (Gourney), of Lymington, Suffolk  ->  Henry Gurney (Gourney), of Lymington, Suffolk   + John Gurney (Gourney), of Lymington, Suffolk
Q130335568	Lmul	"Henry Gurney (Gourney), of Lymington, Suffolk"
Q130335568	Len	"Henry Gurney (Gourney), of Lymington, Suffolk"
Q130335568	Amul	"John Gurney (Gourney), of Lymington, Suffolk"

# Q130335600  William|Richard Stanley, of Pipe, Lancs  ->  William Stanley, of Pipe, Lancs   + Richard Stanley, of Pipe, Lancs
Q130335600	Lmul	"William Stanley, of Pipe, Lancs"
Q130335600	Len	"William Stanley, of Pipe, Lancs"
Q130335600	Amul	"Richard Stanley, of Pipe, Lancs"

# Q130335604  Richard|Thomas D'Oyley, of Ewden, Bucks  ->  Richard D'Oyley, of Ewden, Bucks   + Thomas D'Oyley, of Ewden, Bucks
Q130335604	Lmul	"Richard D'Oyley, of Ewden, Bucks"
Q130335604	Len	"Richard D'Oyley, of Ewden, Bucks"
Q130335604	Amul	"Thomas D'Oyley, of Ewden, Bucks"

# Q130335650  Sir Robert|John|Thomas Waterton, of Waterton Hall  ->  Sir Robert Waterton, of Waterton Hall   + Sir John Waterton, of Waterton Hall | Sir Thomas Waterton, of Waterton Hall
Q130335650	Lmul	"Sir Robert Waterton, of Waterton Hall"
Q130335650	Len	"Sir Robert Waterton, of Waterton Hall"
Q130335650	Amul	"Sir John Waterton, of Waterton Hall"
Q130335650	Amul	"Sir Thomas Waterton, of Waterton Hall"

# Q130335654  Maud|Agnes Fairfax  ->  Maud Fairfax   + Agnes Fairfax
Q130335654	Lmul	"Maud Fairfax"
Q130335654	Len	"Maud Fairfax"
Q130335654	Amul	"Agnes Fairfax"

# Q130336737  Julian Smyth|Smith  ->  Julian Smyth   + Julian Smith
Q130336737	Lmul	"Julian Smyth"
Q130336737	Len	"Julian Smyth"
Q130336737	Amul	"Julian Smith"

# Q130338029  Thomasine|Catherine Tuite, of Ballinsallagh  ->  Thomasine Tuite, of Ballinsallagh   + Catherine Tuite, of Ballinsallagh
Q130338029	Lmul	"Thomasine Tuite, of Ballinsallagh"
Q130338029	Len	"Thomasine Tuite, of Ballinsallagh"
Q130338029	Amul	"Catherine Tuite, of Ballinsallagh"

# Q130338036  Cahir|Charles O'Dempsey, of Ballybrittas  ->  Cahir O'Dempsey, of Ballybrittas   + Charles O'Dempsey, of Ballybrittas
Q130338036	Lmul	"Cahir O'Dempsey, of Ballybrittas"
Q130338036	Len	"Cahir O'Dempsey, of Ballybrittas"
Q130338036	Amul	"Charles O'Dempsey, of Ballybrittas"

# Q130338086  Richard|Robert Tuite, of Ballinsallagh  ->  Richard Tuite, of Ballinsallagh   + Robert Tuite, of Ballinsallagh
Q130338086	Lmul	"Richard Tuite, of Ballinsallagh"
Q130338086	Len	"Richard Tuite, of Ballinsallagh"
Q130338086	Amul	"Robert Tuite, of Ballinsallagh"

# Q130338954  Gwenllian|Alice ferch Bleddyn ab Einion Fychan ab Einion  ->  Gwenllian ferch Bleddyn ab Einion Fychan ab Einion   + Alice ferch Bleddyn ab Einion Fychan ab Einion
Q130338954	Lmul	"Gwenllian ferch Bleddyn ab Einion Fychan ab Einion"
Q130338954	Len	"Gwenllian ferch Bleddyn ab Einion Fychan ab Einion"
Q130338954	Amul	"Alice ferch Bleddyn ab Einion Fychan ab Einion"

# Q130339420  Joan|Margery Russell  ->  Joan Russell   + Margery Russell
Q130339420	Lmul	"Joan Russell"
Q130339420	Len	"Joan Russell"
Q130339420	Amul	"Margery Russell"

# Q130340259  Madog of Llanferis|Llanferres  ->  Madog of Llanferis   + Madog of Llanferres
Q130340259	Lmul	"Madog of Llanferis"
Q130340259	Len	"Madog of Llanferis"
Q130340259	Amul	"Madog of Llanferres"

# Q130340645  Jane|Joan Moreton  ->  Jane Moreton   + Joan Moreton
Q130340645	Lmul	"Jane Moreton"
Q130340645	Len	"Jane Moreton"
Q130340645	Amul	"Joan Moreton"

# Q130340660  Robert|Roger de Manlegh  ->  Robert de Manlegh   + Roger de Manlegh
Q130340660	Lmul	"Robert de Manlegh"
Q130340660	Len	"Robert de Manlegh"
Q130340660	Amul	"Roger de Manlegh"

# Q130340784  Henry|Hari ap Piers Scourfield, of New Moat  ->  Henry ap Piers Scourfield, of New Moat   + Hari ap Piers Scourfield, of New Moat
Q130340784	Lmul	"Henry ap Piers Scourfield, of New Moat"
Q130340784	Len	"Henry ap Piers Scourfield, of New Moat"
Q130340784	Amul	"Hari ap Piers Scourfield, of New Moat"

# Q130340882  Mawd|Jane Broughton (Brochdyn)  ->  Mawd Broughton (Brochdyn)   + Jane Broughton (Brochdyn)
Q130340882	Lmul	"Mawd Broughton (Brochdyn)"
Q130340882	Len	"Mawd Broughton (Brochdyn)"
Q130340882	Amul	"Jane Broughton (Brochdyn)"

# Q130340885  John|Jenkin Butler, of Dunraven  ->  John Butler, of Dunraven   + Jenkin Butler, of Dunraven
Q130340885	Lmul	"John Butler, of Dunraven"
Q130340885	Len	"John Butler, of Dunraven"
Q130340885	Amul	"Jenkin Butler, of Dunraven"

# Q130340910  Isabel|Sybil ferch Robert Cantelupe  ->  Isabel ferch Robert Cantelupe   + Sybil ferch Robert Cantelupe
Q130340910	Lmul	"Isabel ferch Robert Cantelupe"
Q130340910	Len	"Isabel ferch Robert Cantelupe"
Q130340910	Amul	"Sybil ferch Robert Cantelupe"

# Q130341462  Anne|Angharad Vaughan  ->  Anne Vaughan   + Angharad Vaughan
Q130341462	Lmul	"Anne Vaughan"
Q130341462	Len	"Anne Vaughan"
Q130341462	Amul	"Angharad Vaughan"

# Q130341574  Rhyangen|Arianwen ferch Iorwerth ap Trahearn  ->  Rhyangen ferch Iorwerth ap Trahearn   + Arianwen ferch Iorwerth ap Trahearn
Q130341574	Lmul	"Rhyangen ferch Iorwerth ap Trahearn"
Q130341574	Len	"Rhyangen ferch Iorwerth ap Trahearn"
Q130341574	Amul	"Arianwen ferch Iorwerth ap Trahearn"

# Q130344139  Julian|Juliana Erpingham  ->  Julian Erpingham   + Juliana Erpingham
Q130344139	Lmul	"Julian Erpingham"
Q130344139	Len	"Julian Erpingham"
Q130344139	Amul	"Juliana Erpingham"

# Q130352957  Dorothy|Alice Everingham  ->  Dorothy Everingham   + Alice Everingham
Q130352957	Len	"Dorothy Everingham"
Q130352957	Amul	"Alice Everingham"

# Q130353041  Margery|Eleanor  ->  Margery   + Eleanor
Q130353041	Lmul	"Margery"
Q130353041	Len	"Margery"
Q130353041	Amul	"Eleanor"

# Q130353105  Alured|Alvery|Alfred Barwick (Beswick), of Bulcotes  ->  Alured Barwick (Beswick), of Bulcotes   + Alvery Barwick (Beswick), of Bulcotes | Alfred Barwick (Beswick), of Bulcotes
Q130353105	Len	"Alured Barwick (Beswick), of Bulcotes"
Q130353105	Amul	"Alvery Barwick (Beswick), of Bulcotes"
Q130353105	Amul	"Alfred Barwick (Beswick), of Bulcotes"

# Q130354044  Joane|Joan Hedworth  ->  Joane Hedworth   + Joan Hedworth
Q130354044	Len	"Joane Hedworth"
Q130354044	Amul	"Joan Hedworth"

# Q130358353  Mary|Margaret ferch John Stedman  ->  Mary ferch John Stedman   + Margaret ferch John Stedman
Q130358353	Lmul	"Mary ferch John Stedman"
Q130358353	Len	"Mary ferch John Stedman"
Q130358353	Amul	"Margaret ferch John Stedman"

# Q130358519  Cydifor|Cadwgan ap Gwaithfoed  ->  Cydifor ap Gwaithfoed   + Cadwgan ap Gwaithfoed
Q130358519	Lmul	"Cydifor ap Gwaithfoed"
Q130358519	Len	"Cydifor ap Gwaithfoed"
Q130358519	Amul	"Cadwgan ap Gwaithfoed"

# Q130359032  Eleanor|Elizabeth Cornewall, of Burford  ->  Eleanor Cornewall, of Burford   + Elizabeth Cornewall, of Burford
Q130359032	Lmul	"Eleanor Cornewall, of Burford"
Q130359032	Len	"Eleanor Cornewall, of Burford"
Q130359032	Amul	"Elizabeth Cornewall, of Burford"

# Q130634857  squire Frederik|Vikke Düker, lord of Pala (/&Atla)  ->  squire Frederik Düker, lord of Pala (/&Atla)   + squire Vikke Düker, lord of Pala (/&Atla)
Q130634857	Lmul	"squire Frederik Düker, lord of Pala (/&Atla)"
Q130634857	Len	"squire Frederik Düker, lord of Pala (/&Atla)"
Q130634857	Amul	"squire Vikke Düker, lord of Pala (/&Atla)"

# Q130648019  Agnes|Anne Bowyer  ->  Agnes Bowyer   + Anne Bowyer
Q130648019	Lmul	"Agnes Bowyer"
Q130648019	Len	"Agnes Bowyer"
Q130648019	Amul	"Anne Bowyer"

# Q130648072  Elizabeth|Isabel Oldcastle  ->  Elizabeth Oldcastle   + Isabel Oldcastle
Q130648072	Lmul	"Elizabeth Oldcastle"
Q130648072	Len	"Elizabeth Oldcastle"
Q130648072	Amul	"Isabel Oldcastle"

# Q130648183  Cicely|Cecilia Hopkins  ->  Cicely Hopkins   + Cecilia Hopkins
Q130648183	Lmul	"Cicely Hopkins"
Q130648183	Len	"Cicely Hopkins"
Q130648183	Amul	"Cecilia Hopkins"

# Q130682209  noble Dordi of Fersam|Borsem  ->  noble Dordi of Fersam   + noble Dordi of Borsem
Q130682209	Lmul	"noble Dordi of Fersam"
Q130682209	Len	"noble Dordi of Fersam"
Q130682209	Amul	"noble Dordi of Borsem"

# Q130718035  Julia|Julian Martin  ->  Julia Martin   + Julian Martin
Q130718035	Lmul	"Julia Martin"
Q130718035	Len	"Julia Martin"
Q130718035	Amul	"Julian Martin"

# Q130718046  Ann|Joane Burlegh, of Clanacombe (Chaucombe), Devon  ->  Ann Burlegh, of Clanacombe (Chaucombe), Devon   + Joane Burlegh, of Clanacombe (Chaucombe), Devon
Q130718046	Lmul	"Ann Burlegh, of Clanacombe (Chaucombe), Devon"
Q130718046	Len	"Ann Burlegh, of Clanacombe (Chaucombe), Devon"
Q130718046	Amul	"Joane Burlegh, of Clanacombe (Chaucombe), Devon"

# Q131137948  Johanna|Jane Whitworth  ->  Johanna Whitworth   + Jane Whitworth
Q131137948	Lmul	"Johanna Whitworth"
Q131137948	Len	"Johanna Whitworth"
Q131137948	Amul	"Jane Whitworth"

# Q131138002  Marke|Mark Flamoke, Lord of Flaemoke  ->  Marke Flamoke, Lord of Flaemoke   + Mark Flamoke, Lord of Flaemoke
Q131138002	Lmul	"Marke Flamoke, Lord of Flaemoke"
Q131138002	Len	"Marke Flamoke, Lord of Flaemoke"
Q131138002	Amul	"Mark Flamoke, Lord of Flaemoke"

# Q131138770  Elery|Clara Goodere  ->  Elery Goodere   + Clara Goodere
Q131138770	Lmul	"Elery Goodere"
Q131138770	Len	"Elery Goodere"
Q131138770	Amul	"Clara Goodere"

# Q131138772  Sir Richard|William Goodere, of London  ->  Sir Richard Goodere, of London   + Sir William Goodere, of London
Q131138772	Lmul	"Sir Richard Goodere, of London"
Q131138772	Len	"Sir Richard Goodere, of London"
Q131138772	Amul	"Sir William Goodere, of London"

# Q131233922  Maud|Maude Tresithney  ->  Maud Tresithney   + Maude Tresithney
Q131233922	Lmul	"Maud Tresithney"
Q131233922	Len	"Maud Tresithney"
Q131233922	Amul	"Maude Tresithney"

# Q131332281  Johann V|Kraft von Mirlaer  ->  Johann V von Mirlaer   + Johann Kraft von Mirlaer
Q131332281	Lmul	"Johann V von Mirlaer"
Q131332281	Len	"Johann V von Mirlaer"
Q131332281	Amul	"Johann Kraft von Mirlaer"

# Q131342591  Elizabeth|Rose Wayte  ->  Elizabeth Wayte   + Rose Wayte
Q131342591	Lmul	"Elizabeth Wayte"
Q131342591	Len	"Elizabeth Wayte"
Q131342591	Amul	"Rose Wayte"

# Q131342794  Cecilia|Cecil ferch Edward Carne  ->  Cecilia ferch Edward Carne   + Cecil ferch Edward Carne
Q131342794	Lmul	"Cecilia ferch Edward Carne"
Q131342794	Len	"Cecilia ferch Edward Carne"
Q131342794	Amul	"Cecil ferch Edward Carne"

# Q131346922  Fromand|Fermand Brown  ->  Fromand Brown   + Fermand Brown
Q131346922	Lmul	"Fromand Brown"
Q131346922	Len	"Fromand Brown"
Q131346922	Amul	"Fermand Brown"

# Q131347084  William|Henry Martin, of Trericet  ->  William Martin, of Trericet   + Henry Martin, of Trericet
Q131347084	Lmul	"William Martin, of Trericet"
Q131347084	Len	"William Martin, of Trericet"
Q131347084	Amul	"Henry Martin, of Trericet"

# Q131355534  Hamon|Hamo|Heimond le Gras (FitzRaymond)  ->  Hamon le Gras (FitzRaymond)   + Hamo le Gras (FitzRaymond) | Heimond le Gras (FitzRaymond)
Q131355534	Lmul	"Hamon le Gras (FitzRaymond)"
Q131355534	Len	"Hamon le Gras (FitzRaymond)"
Q131355534	Amul	"Hamo le Gras (FitzRaymond)"
Q131355534	Amul	"Heimond le Gras (FitzRaymond)"

# Q131369895  Oswin|Oswald Cresswell, of Cresswell  ->  Oswin Cresswell, of Cresswell   + Oswald Cresswell, of Cresswell
Q131369895	Lmul	"Oswin Cresswell, of Cresswell"
Q131369895	Len	"Oswin Cresswell, of Cresswell"
Q131369895	Amul	"Oswald Cresswell, of Cresswell"

# Q131447187  Vittoria|Violante Caetani dell'Aquila d'Aragona  ->  Vittoria Caetani dell'Aquila d'Aragona   + Violante Caetani dell'Aquila d'Aragona
Q131447187	Lmul	"Vittoria Caetani dell'Aquila d'Aragona"
Q131447187	Len	"Vittoria Caetani dell'Aquila d'Aragona"
Q131447187	Amul	"Violante Caetani dell'Aquila d'Aragona"

# Q131522293  Katharina von Weilzogen|Wolzogen  ->  Katharina von Weilzogen   + Katharina von Wolzogen
Q131522293	Lmul	"Katharina von Weilzogen"
Q131522293	Len	"Katharina von Weilzogen"
Q131522293	Amul	"Katharina von Wolzogen"

# Q131554079  Karlis Ceege|Zoeges, bailiff of Piltene  ->  Karlis Ceege bailiff of Piltene   + Karlis Zoeges, bailiff of Piltene
Q131554079	Lmul	"Karlis Ceege bailiff of Piltene"
Q131554079	Len	"Karlis Ceege bailiff of Piltene"
Q131554079	Amul	"Karlis Zoeges, bailiff of Piltene"

# Q131726556  Hanns|Johann II von Degenfeld  ->  Hanns II von Degenfeld   + Johann II von Degenfeld
Q131726556	Len	"Hanns II von Degenfeld"
Q131726556	Amul	"Johann II von Degenfeld"

# Q131726563  Gertrud|Gertraud von Neuhausen a.d.H Hofen  ->  Gertrud von Neuhausen a.d.H Hofen   + Gertraud von Neuhausen a.d.H Hofen
Q131726563	Lmul	"Gertrud von Neuhausen a.d.H Hofen"
Q131726563	Len	"Gertrud von Neuhausen a.d.H Hofen"
Q131726563	Amul	"Gertraud von Neuhausen a.d.H Hofen"

# Q131730876  Captain Pavel|Pál de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'  ->  Captain Pavel de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'   + Captain Pál de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'
Q131730876	Lmul	"Captain Pavel de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'"
Q131730876	Len	"Captain Pavel de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'"
Q131730876	Amul	"Captain Pál de Bornemisa, de Petrelin & 'Bornemisza de Boros-Jenö'"

# Q131731269  Margaret|Marian McGillivray  ->  Margaret McGillivray   + Marian McGillivray
Q131731269	Lmul	"Margaret McGillivray"
Q131731269	Len	"Margaret McGillivray"
Q131731269	Amul	"Marian McGillivray"

# Q131731322  Enno Sytzena|Cirksena, Burgrave in Norden  ->  Enno Sytzena Burgrave in Norden   + Enno Cirksena, Burgrave in Norden
Q131731322	Lmul	"Enno Sytzena Burgrave in Norden"
Q131731322	Len	"Enno Sytzena Burgrave in Norden"
Q131731322	Amul	"Enno Cirksena, Burgrave in Norden"

# Q131731337  boier Marcea|Mircea  ->  boier Marcea   + boier Mircea
Q131731337	Lmul	"boier Marcea"
Q131731337	Len	"boier Marcea"
Q131731337	Amul	"boier Mircea"

# Q131732625  Karl Friedrich|Hans Heinrich? von Gregorsdorff  ->  Karl Friedrich Heinrich? von Gregorsdorff   + Karl Hans Heinrich? von Gregorsdorff
Q131732625	Lmul	"Karl Friedrich Heinrich? von Gregorsdorff"
Q131732625	Len	"Karl Friedrich Heinrich? von Gregorsdorff"
Q131732625	Amul	"Karl Hans Heinrich? von Gregorsdorff"

# Q131732860  Thady|Terence O'Conor, of Knockleg  ->  Thady O'Conor, of Knockleg   + Terence O'Conor, of Knockleg
Q131732860	Lmul	"Thady O'Conor, of Knockleg"
Q131732860	Len	"Thady O'Conor, of Knockleg"
Q131732860	Amul	"Terence O'Conor, of Knockleg"

# Q131741074  Joan|Jane ferch Hugh Huntley  ->  Joan ferch Hugh Huntley   + Jane ferch Hugh Huntley
Q131741074	Lmul	"Joan ferch Hugh Huntley"
Q131741074	Len	"Joan ferch Hugh Huntley"
Q131741074	Amul	"Jane ferch Hugh Huntley"

# Q131741171  Margaret|Elizabeth Tamworth (Thomworth)  ->  Margaret Tamworth (Thomworth)   + Elizabeth Tamworth (Thomworth)
Q131741171	Lmul	"Margaret Tamworth (Thomworth)"
Q131741171	Len	"Margaret Tamworth (Thomworth)"
Q131741171	Amul	"Elizabeth Tamworth (Thomworth)"

# Q131784445  Edmund|Thomas Thimblethorpe, of Foulsham  ->  Edmund Thimblethorpe, of Foulsham   + Thomas Thimblethorpe, of Foulsham
Q131784445	Lmul	"Edmund Thimblethorpe, of Foulsham"
Q131784445	Len	"Edmund Thimblethorpe, of Foulsham"
Q131784445	Amul	"Thomas Thimblethorpe, of Foulsham"

# Q131784501  Sir Saier|Saher Rochford, of Fenne, Boston, Lincs  ->  Sir Saier Rochford, of Fenne, Boston, Lincs   + Sir Saher Rochford, of Fenne, Boston, Lincs
Q131784501	Lmul	"Sir Saier Rochford, of Fenne, Boston, Lincs"
Q131784501	Len	"Sir Saier Rochford, of Fenne, Boston, Lincs"
Q131784501	Amul	"Sir Saher Rochford, of Fenne, Boston, Lincs"

# Q132174909  Susan|Susanna Howe  ->  Susan Howe   + Susanna Howe
Q132174909	Lmul	"Susan Howe"
Q132174909	Len	"Susan Howe"
Q132174909	Amul	"Susanna Howe"

# Q133461036  Elis|Mallt ferch Dafydd Llwyd Blaeney  ->  Elis ferch Dafydd Llwyd Blaeney   + Mallt ferch Dafydd Llwyd Blaeney
Q133461036	Len	"Elis ferch Dafydd Llwyd Blaeney"
Q133461036	Amul	"Mallt ferch Dafydd Llwyd Blaeney"

# Q133461548  Dafydd Ddû of Aber|Aberriw  ->  Dafydd Ddû of Aber   + Dafydd Ddû of Aberriw
Q133461548	Len	"Dafydd Ddû of Aber"
Q133461548	Amul	"Dafydd Ddû of Aberriw"

# Q133461559  Madog ap Gwylawg|Gwallawe ab Eginir ap Llywelyn  ->  Madog ap Gwylawg ab Eginir ap Llywelyn   + Madog ap Gwallawe ab Eginir ap Llywelyn
Q133461559	Len	"Madog ap Gwylawg ab Eginir ap Llywelyn"
Q133461559	Amul	"Madog ap Gwallawe ab Eginir ap Llywelyn"

# Q133860939  Frans de Pottere|Potters  ->  Frans de Pottere   + Frans de Potters
Q133860939	Len	"Frans de Pottere"
Q133860939	Amul	"Frans de Potters"

# Q133864558  Elisabeth Semsdr. van Breene|van Brienen  ->  Elisabeth Semsdr. van Breene Brienen   + Elisabeth Semsdr. van van Brienen
Q133864558	Len	"Elisabeth Semsdr. van Breene Brienen"
Q133864558	Amul	"Elisabeth Semsdr. van van Brienen"

# Q133864560  Sem IJsbrantsz. van Breene|van Brienen  ->  Sem IJsbrantsz. van Breene Brienen   + Sem IJsbrantsz. van van Brienen
Q133864560	Len	"Sem IJsbrantsz. van Breene Brienen"
Q133864560	Amul	"Sem IJsbrantsz. van van Brienen"

# Q134269493  noble Anna Tvisel|Zweifel, heiress of Ellivere manor  ->  noble Anna Tvisel heiress of Ellivere manor   + noble Anna Zweifel, heiress of Ellivere manor
Q134269493	Len	"noble Anna Tvisel heiress of Ellivere manor"
Q134269493	Amul	"noble Anna Zweifel, heiress of Ellivere manor"

# Q134269546  Beren|Bernard Tweiseln|Zweifeln  ->  Beren Tweiseln   + Bernard Zweifeln
Q134269546	Len	"Beren Tweiseln"
Q134269546	Amul	"Bernard Zweifeln"

# Q134287275  Maycken|Makye Boulijn  ->  Maycken Boulijn   + Makye Boulijn
Q134287275	Len	"Maycken Boulijn"
Q134287275	Amul	"Makye Boulijn"

# Q134287405  Pieter Halling|Hallinc  ->  Pieter Halling   + Pieter Hallinc
Q134287405	Len	"Pieter Halling"
Q134287405	Amul	"Pieter Hallinc"

# Q135445414  Laurens ther Poirten|Poirtman  ->  Laurens ther Poirten   + Laurens ther Poirtman
Q135445414	Len	"Laurens ther Poirten"
Q135445414	Amul	"Laurens ther Poirtman"

# Q135480198  Colonel Indrek|Henrikki Robert Burt, commandant of Stralsund, lord of Tohisoo & Noistvere  ->  Colonel Indrek Robert Burt, commandant of Stralsund, lord of Tohisoo & Noistvere   + Colonel Henrikki Robert Burt, commandant of Stralsund, lord of Tohisoo & Noistvere
Q135480198	Len	"Colonel Indrek Robert Burt, commandant of Stralsund, lord of Tohisoo & Noistvere"
Q135480198	Amul	"Colonel Henrikki Robert Burt, commandant of Stralsund, lord of Tohisoo & Noistvere"

# Q135525179  Jonathan|George Oakley, of Carmarthen  ->  Jonathan Oakley, of Carmarthen   + George Oakley, of Carmarthen
Q135525179	Len	"Jonathan Oakley, of Carmarthen"
Q135525179	Amul	"George Oakley, of Carmarthen"

# Q135663094  Katrine Magdalene|Maleene Kaass  ->  Katrine Magdalene Kaass   + Katrine Maleene Kaass
Q135663094	Len	"Katrine Magdalene Kaass"
Q135663094	Amul	"Katrine Maleene Kaass"

# Q135669004  Persephone|Proserpina Manarys  ->  Persephone Manarys   + Proserpina Manarys
Q135669004	Len	"Persephone Manarys"
Q135669004	Amul	"Proserpina Manarys"

# Q135672123  John|Thomas Hatcher, of Careby  ->  John Hatcher, of Careby   + Thomas Hatcher, of Careby
Q135672123	Len	"John Hatcher, of Careby"
Q135672123	Amul	"Thomas Hatcher, of Careby"

# Q135681066  Sanabait|Senebeit of Arademma & Metz  ->  Sanabait of Arademma & Metz   + Senebeit of Arademma & Metz
Q135681066	Len	"Sanabait of Arademma & Metz"
Q135681066	Amul	"Senebeit of Arademma & Metz"

# Q135681510  Sahlitu|Sahalu Inqu  ->  Sahlitu Inqu   + Sahalu Inqu
Q135681510	Len	"Sahlitu Inqu"
Q135681510	Amul	"Sahalu Inqu"

# Q135683817  Nechit|Nachit  ->  Nechit   + Nachit
Q135683817	Len	"Nechit"
Q135683817	Amul	"Nachit"

# Q135855377  Indrek IndrekiPoeg Raute|Ruth, lord of Jogisuu and Alliku  ->  Indrek IndrekiPoeg Raute lord of Jogisuu and Alliku   + Indrek IndrekiPoeg Ruth, lord of Jogisuu and Alliku
Q135855377	Len	"Indrek IndrekiPoeg Raute lord of Jogisuu and Alliku"
Q135855377	Amul	"Indrek IndrekiPoeg Ruth, lord of Jogisuu and Alliku"

# Q136005549  Jeanne Kautz|Kantoz  ->  Jeanne Kautz   + Jeanne Kantoz
Q136005549	Len	"Jeanne Kautz"
Q136005549	Amul	"Jeanne Kantoz"

# Q136006105  Agnes|Helen Walkinshaw  ->  Agnes Walkinshaw   + Helen Walkinshaw
Q136006105	Len	"Agnes Walkinshaw"
Q136006105	Amul	"Helen Walkinshaw"

# Q136010152  Margareta|Grete zu Wiltz  ->  Margareta zu Wiltz   + Grete zu Wiltz
Q136010152	Len	"Margareta zu Wiltz"
Q136010152	Amul	"Grete zu Wiltz"

# Q136010154  Gottfried|Godart, Herr zu Wiltz und Hartelstein  ->  Gottfried Herr zu Wiltz und Hartelstein   + Godart, Herr zu Wiltz und Hartelstein
Q136010154	Len	"Gottfried Herr zu Wiltz und Hartelstein"
Q136010154	Amul	"Godart, Herr zu Wiltz und Hartelstein"

# Q136027179  Hélène|Jeanne de Marbré  ->  Hélène de Marbré   + Jeanne de Marbré
Q136027179	Len	"Hélène de Marbré"
Q136027179	Amul	"Jeanne de Marbré"

# Q136027184  Anne|Agnès Green de Saint-Marsault  ->  Anne Green de Saint-Marsault   + Agnès Green de Saint-Marsault
Q136027184	Len	"Anne Green de Saint-Marsault"
Q136027184	Amul	"Agnès Green de Saint-Marsault"

# Q136028340  Johanna Zeiler|Zailler  ->  Johanna Zeiler   + Johanna Zailler
Q136028340	Len	"Johanna Zeiler"
Q136028340	Amul	"Johanna Zailler"

# Q136028960  Margery|Margaret Conyers, of Thormanby, Yorks  ->  Margery Conyers, of Thormanby, Yorks   + Margaret Conyers, of Thormanby, Yorks
Q136028960	Len	"Margery Conyers, of Thormanby, Yorks"
Q136028960	Amul	"Margaret Conyers, of Thormanby, Yorks"

# Q136030919  Michelle|Albertine Imbert, Dame de Warenghien, de Grimaretz, de Martinsart  ->  Michelle Imbert, Dame de Warenghien, de Grimaretz, de Martinsart   + Albertine Imbert, Dame de Warenghien, de Grimaretz, de Martinsart
Q136030919	Len	"Michelle Imbert, Dame de Warenghien, de Grimaretz, de Martinsart"
Q136030919	Amul	"Albertine Imbert, Dame de Warenghien, de Grimaretz, de Martinsart"

# Q136140805  Judith|Juliana Brudenell  ->  Judith Brudenell   + Juliana Brudenell
Q136140805	Len	"Judith Brudenell"
Q136140805	Amul	"Juliana Brudenell"

# Q136207659  Margaret|Ann Cunningham  ->  Margaret Cunningham   + Ann Cunningham
Q136207659	Len	"Margaret Cunningham"
Q136207659	Amul	"Ann Cunningham"

# Q136247458  Hans Oeheim|Ehem, der Jüngere  ->  Hans Oeheim der Jüngere   + Hans Ehem, der Jüngere
Q136247458	Len	"Hans Oeheim der Jüngere"
Q136247458	Amul	"Hans Ehem, der Jüngere"

# Q136289775  squire Laavus|Niiles Lassenpoika of Ahtinen  ->  squire Laavus Lassenpoika of Ahtinen   + squire Niiles Lassenpoika of Ahtinen
Q136289775	Len	"squire Laavus Lassenpoika of Ahtinen"
Q136289775	Amul	"squire Niiles Lassenpoika of Ahtinen"

# Q136311063  Maria|Marijcke van Teylingen  ->  Maria van Teylingen   + Marijcke van Teylingen
Q136311063	Len	"Maria van Teylingen"
Q136311063	Amul	"Marijcke van Teylingen"

# Q136336174  Jane|Anne Stokeham  ->  Jane Stokeham   + Anne Stokeham
Q136336174	Len	"Jane Stokeham"
Q136336174	Amul	"Anne Stokeham"

# Q136336422  Margaret|Helen Mayne  ->  Margaret Mayne   + Helen Mayne
Q136336422	Len	"Margaret Mayne"
Q136336422	Amul	"Helen Mayne"

# Q136336618  Angus|Aindalis O'Docherty  ->  Angus O'Docherty   + Aindalis O'Docherty
Q136336618	Len	"Angus O'Docherty"
Q136336618	Amul	"Aindalis O'Docherty"

# Q136341075  Beste|Hessel van Brienen  ->  Beste van Brienen   + Hessel van Brienen
Q136341075	Len	"Beste van Brienen"
Q136341075	Amul	"Hessel van Brienen"

# Q136376259  Baron Villem Gillis|Vilhelm Julius Coyet, 1.Friherre till Ljungby, lord of Årup  ->  Baron Villem Gillis Julius Coyet, 1.Friherre till Ljungby, lord of Årup   + Baron Villem Vilhelm Julius Coyet, 1.Friherre till Ljungby, lord of Årup
Q136376259	Len	"Baron Villem Gillis Julius Coyet, 1.Friherre till Ljungby, lord of Årup"
Q136376259	Amul	"Baron Villem Vilhelm Julius Coyet, 1.Friherre till Ljungby, lord of Årup"

# Q136376261  Julius|Gillis Coyet  ->  Julius Coyet   + Gillis Coyet
Q136376261	Len	"Julius Coyet"
Q136376261	Amul	"Gillis Coyet"

# Q136376266  Reiner|Reinholt Lehusen  ->  Reiner Lehusen   + Reinholt Lehusen
Q136376266	Len	"Reiner Lehusen"
Q136376266	Amul	"Reinholt Lehusen"

# Q136376438  Elisabeth of Kula|Lod  ->  Elisabeth of Kula   + Elisabeth of Lod
Q136376438	Len	"Elisabeth of Kula"
Q136376438	Amul	"Elisabeth of Lod"

# Q136383973  Aleta|Adelheid Wrangell  ->  Aleta Wrangell   + Adelheid Wrangell
Q136383973	Len	"Aleta Wrangell"
Q136383973	Amul	"Adelheid Wrangell"

# Q136481689  Ellen|Eleanor Chator (Chaytor)  ->  Ellen Chator (Chaytor)   + Eleanor Chator (Chaytor)
Q136481689	Len	"Ellen Chator (Chaytor)"
Q136481689	Amul	"Eleanor Chator (Chaytor)"

# Q136688654  Mary Stkison|Stikson  ->  Mary Stkison   + Mary Stikson
Q136688654	Len	"Mary Stkison"
Q136688654	Amul	"Mary Stikson"
