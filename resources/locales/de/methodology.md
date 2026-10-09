Wie viel Kohlendioxid stoßen wir beim Heizen unserer Wohnungen aus? Dies hängt von drei Hauptfaktoren ab:

1. Beheizte Fläche: Wie groß ist unsere Wohnstätte und wie viel davon heizen wir? Wohnen wir allein in einem großen Haus
   oder teilen wir uns eine kleine Wohnung? Heizen wir während der kalten Jahreszeit das ganze Haus oder nur Räume,
   während wir sie nutzen?

2. Energieeffizienz: Wie viel Energie benötigen wir, um einen Quadratmeter Wohnfläche zu heizen? Das hängt davon ab, wie
   gut Gebäude gedämmt sind, aber auch davon, wie wir unsere Wohnungen im Winter lüften.

3. Energiequelle: Woher kommt die Wärme? Nutzen wir einen Gaskessel, einen Ölofen, einen Kamin oder eine Wärmepumpe? Die
   Energiequelle bzw. der Energieträger bestimmt, wie viel CO₂ pro kWh Heizenergie, die wir verbrauchen, ausgestoßen
   wird (und wo).

Der deutsche Zensus von 2022 liefert räumliche Daten, anhand derer wir all diese Schlüsselvariablen für jede
100-Meter-Gitterzelle in ganz Deutschland schätzen können.

1. Multiplikation der Einwohnerzahl mit der durchschnittlichen Wohnfläche pro Kopf, um die Gesamtwohnfläche zu erhalten
   (d. h. die Fläche, die vermutlich beheizt wird).

2. Berechnung des durchschnittlichen Heizenergieverbrauchs pro Flächeneinheit (kWh pro m²) anhand des Anteils der in
   verschiedenen Zeiträumen errichteten Gebäude, da sich die Baustandards im Laufe der Zeit verändert haben und neuere
   Gebäude in der Regel besser gedämmt sind.

3. Berechnung der durchschnittlichen Kohlendioxidemissionen pro Einheit Heizenergie (sog. "Emissionsfaktor", gemessen in
   kg pro kWh) auf der Grundlage des Anteils der Gebäude mit unterschiedlichen Heizenergieträgern (z. B. Gas, Öl, Holz,
   Fernwärme usw.).

Die Emissionsschätzungen sind das Produkt aus Gesamtwohnfläche, durchschnittlichem Energieverbrauch pro Quadratmeter und
durchschnittlichem Emissionsfaktor.

## Datenquellen

### Räumliche Daten
Rasterdaten des deutschen Zensus 2022 können
[hier](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/_inhalt.html#sprg1403932)
heruntergeladen werden. Wir verwenden die folgenden vier Datensätze:

1. Bevölkerung ("Bevölkerungszahlen in Gitterzellen")
2. Wohnfläche pro Kopf ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Baujahr der Gebäude ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heizenergieträger in Wohngebäuden ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Energieverbrauch
Wir verwenden Energieverbrauchswerte für Gebäude verschiedener Altersklassen aus
[co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit), die auf Messungen in über 300.000 Gebäuden in ganz
Deutschland basieren und um Temperaturunterschiede bereinigt sind.

| Altersklasse  | Energieverbrauch (kWh/m²) | Gebäudestandard |
| ------------- | ------------------------- | --------------- |
| Vor 1919      | 134,6                     |                 |
| 1919 bis 1948 | 134,6                     |                 |
| 1949 bis 1978 | 135,7                     |                 |
| 1979 bis 1990 | 126,2                     | WSchVO 1        |
| 1991 bis 2000 | 93,3                      | WSchVO 3        |
| 2001 bis 2010 | 78,5                      | EnEV 2002       |
| 2011 bis 2019 | 74,1                      | EnEV 2007*      |
| Seit 2019     | 74,1                      | EnEV 2007*      |


### Emissionsfaktoren
Wir verwenden Emissionsfaktoren aus der ProBas-Datenbank des Umweltbundesamtes. Zur Schätzung der direkten Emissionen
und der Lebenszyklus-Emissionen nutzen wir zwei unterschiedliche Sätze von Emissionsfaktoren.

**Direkte Emissionen** basieren auf Emissionsfaktoren für „Einzelprozesse“, was bedeutet, dass sie die Emissionen aus
der Verbrennung von Brennstoffen zur Wärmeerzeugung umfassen, jedoch keine anderen vor- und nachgelagerten Emissionen im
Lebenszyklus der Brennstoffe.

Wir verwenden CO₂-Emissionsfaktoren aus der ProBas-Datenbank für
[Gas](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=4c06c7a1-cdec-46cd-9929-0df2a70b8897&version=02.44.152&stock=PUBLIC&lang=de),
[Öl](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=26f4942c-889a-4b07-a2e7-3c6d8e74227e&version=02.44.152&stock=PUBLIC&lang=de)
und
[Kohle](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=cb66d367-05d9-485e-b301-24f7b88b4320&version=02.44.152&stock=PUBLIC&lang=de).

| Energieträger                   | Emissionsfaktor (kg CO₂/kWh) | Quelle / Anmerkungen |
| ------------------------------- | ---------------------------- | -------------------- |
| Gas                             | 0,20029                      | ProBas               |
| Öl                              | 0,26793                      | ProBas               |
| Kohle                           | 0,33661                      | ProBas               |
| Holzpellets                     | 0,34000                      | Anmerkung 1          |
| Biomasse/Biogas                 | 0,20029                      | Anmerkung 1          |
| Fernwärme                       | 0,00000                      | Anmerkung 2          |
| Strom                           | 0,00000                      | Anmerkung 2          |
| Solar/Geothermie/Umgebungswärme | 0,00000                      | Anmerkung 2          |

- **Anmerkung 1**: Die direkten Emissionen berücksichtigen nicht den gesamten Lebenszyklus der Energieträger. Das heißt,
  wir schätzen die bei der Verbrennung von Biomasse freigesetzten CO₂-Emissionen, ohne zu berücksichtigen, dass diese
  Kohlenstoffatome erst kürzlich durch Photosynthese gebunden wurden. Daher haben wir für Biogas/Biomasse bzw.
  Holzpellets Emissionsfaktoren verwendet, die denen von Gas und Kohle ähneln.

- **Anmerkung 2**: Bei der Beheizung von Gebäuden mit Strom, Wärmepumpen und Fernwärme entsteht kein direkter
  CO₂-Ausstoß, daher betragen diese Emissionsfaktoren 0. Die Beheizung solcher Gebäude kann jedoch an anderer Stelle
  Emissionen verursachen (beispielsweise in Kraftwerken oder Fernwärmeanlagen), die in Schätzungen der
  Lebenszyklus-Emissionen berücksichtigt werden.

- **Anmerkung 3**: Bei Gebäuden mit unbekanntem Energieträger verwenden wir den durchschnittlichen Emissionsfaktor der
  oben genannten acht Kategorien, gewichtet nach der Anzahl der Gebäude mit dem jeweiligen Energieträger in ganz
  Deutschland.

**Lebenszyklus-Emissionen** umfassen darüber hinaus vor- und nachgelagerte Emissionen (z. B. Energieerzeugung,
Verarbeitung und Vertrieb) und basieren somit auf den Emissionsfaktoren aus den Lebenszyklus-Inventaren von ProBas.

Im Gegensatz zu direkten Emissionen, die ausschließlich Kohlendioxid umfassen, beinhalten Lebenszyklus-Emissionen auch
andere Treibhausgase und werden daher in CO₂-Äquivalenten angegeben, indem die Emissionen der verschiedenen Gase mit
ihrem jeweiligen Treibhauspotenzial (GWP) über einen Zeitraum von 100 Jahren multipliziert werden (ProBas verwendet
GWP-Werte aus dem IPCC-AR5-Bericht).

Wir verwenden Emissionsfaktoren für THG (CO₂-Äquivalente) aus der ProBas-Datenbank. Für
[Gas](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=c6fb47f4-dafa-4aea-b009-1dbf9ca1d8ca&lang=de)
und
[Öl](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=0593c706-4ee5-44ae-85ef-bd60eac7c9c8&lang=de)
nehmen wir an, dass in den Gebäuden Brennwertkessel genutzt werden. Für
[Kohle](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=127daa60-ce89-4ad3-9fc2-dd9932481d41&version=02.44.152&stock=PUBLIC)
gehen wir von Braunkohlebriketts aus. Für
[Holz](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=74cfbbc8-96d4-49ae-8052-6ec8d8ece18f&version=02.44.152&stock=PUBLIC&lang=en)
nehmen wir an, dass Holzstücke in einer Zentralheizungsanlage verbrannt werden. Für
[Fernwärme](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=6dc315d7-c017-46ed-99f8-05ff57de1702&lang=de)
gehen wir vom deutschen Energiemix im Jahr 2020 aus. Beachte, dass es sich hierbei um einen Durchschnittswert handelt
und die tatsächlichen Emissionen je nach Energiequelle des Fernwärmenetzes stark variieren können. Ebenso gehen wir bei
[Strom](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=6abaf6e8-ad5f-434d-bd0d-9d4682bba924&version=02.44.152&stock=PUBLIC&lang=en)
vom durchschnittlichen deutschen Energiemix im Jahr 2020 aus. Bei
[Wärmepumpen](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=0d3ea28c-3efa-449f-897c-8dfaa291c4e7&version=02.44.152&stock=PUBLIC&lang=en)
gehen wir von Luftwärmepumpen aus, die mit dem durchschnittlichen deutschen Strommix im Jahr 2020 betrieben werden.

| Energieträger                   | Emissionsfaktor (kg CO₂-äq./kWh) | Quelle / Anmerkungen |
| ------------------------------- | -------------------------------- | -------------------- |
| Gas                             | 0,232                            | ProBas               |
| Öl                              | 0,318                            | ProBas               |
| Kohle                           | 0,646                            | ProBas               |
| Holzpellets                     | 0,017                            | ProBas               |
| Biomasse/Biogas                 | 0,017                            | Anmerkung 4          |
| Fernwärme                       | 0,154                            | ProBas               |
| Strom                           | 0,417                            | ProBas               |
| Solar/Geothermie/Umgebungswärme | 0,130                            | ProBas               |

- **Anmerkung 4**: Die Kategorie „Biomasse/Biogas“ umfasst verschiedene biogene Brennstoffe, für die ProBas keine
  Emissionsfaktoren bereitstellt. Wir verwenden daher denselben Emissionsfaktor wie für Holz. Diese Annahme dürfte auf
  der Ebene ganzer Stadtteile und darüber hinaus kaum Auswirkungen auf die Ergebnisse haben, da weniger als 0,1 % der
  Haushalte in Deutschland mit diesem Energieträger beheizt werden.

### Andere Datenquellen
- Durchschnittlicher witterungsbereinigter Heizenergieverbrauch pro Quadratmeter in Wohngebäuden in Deutschland (127,1
  kWh/m² pro Jahr): [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit)
- Durchschnittliche Pro-Kopf-Kohlendioxidemissionen durch das Heizen von Wohnraum in Deutschland (2,2 t pro Jahr):
  [Umweltbundesamt](https://www.umweltbundesamt.de/bild/durchschnittlicher-co2-fussabdruck-pro-kopf-in)
- Deutscher durchschnittlicher Emissionsfaktor (0,199 kg Kohlendioxid pro kWh verbrauchter Heizenergie): Berechnet auf
  der Grundlage des Anteils der Gebäude mit verschiedenen Energieträgern im gesamten Bundesgebiet unter Verwendung der
  oben aufgeführten Emissionsfaktoren.

## Unsicherheit

### Unsicherheit der Eingabedaten

1. Räumliche Daten des Zensus 2022: Aus Datenschutzgründen verwendet der Zensus die Cell-Key-Methode, bei der die
   Gebäudezahlen in jeder Gitterzelle durch zufällige Überlagerungen leicht verändert werden. Dadurch sind die
   durchschnittlichen Heizenergieverbräuche und die durchschnittlichen Emissionsfaktoren wahrscheinlich verzerrt,
   insbesondere in Gitterzellen mit nur wenigen Gebäuden. Das Ausmaß dieser Unsicherheit lässt sich leider
   methodenbedingt nicht quantifizieren.
2. Flächenbezogene Energieverbrauchswerte von co2online: 9 % Unsicherheit ([co2online, UBA,
   2019](https://www.umweltbundesamt.de/publikationen/hintergrundbericht-wohnen-sanieren))
3. Emissionsfaktoren vom Umweltbundesamt: nicht angegeben

### Unsicherheit durch die Gewichtung nach Anzahl der Gebäude statt nach beheizter Fläche

Um den durchschnittlichen flächenbezogenen Energieverbrauch in jeder Gitterzelle zu schätzen, gewichten wir die
empirischen Heizenergieverbrauchswerte der einzelnen Gebäudealtersklassen mit dem Anteil der Gebäude in der jeweiligen
Altersklasse, basierend auf Zensusdaten. Der Zensus gibt für jede Gitterzelle nur an, wie viele Gebäude zu jeder
Baualtersklasse gehören, nicht jedoch deren beheizte Fläche. Unsere Berechnungen gehen daher davon aus, dass alle
Gebäude dieselbe beheizte Fläche haben.

Diese Annahme führt zu Unsicherheiten, da sich Gebäude unterschiedlichen Alters in ihrer Größe unterscheiden können.
Angenommen, eine Gitterzelle enthält drei Gebäude: ein älteres Gebäude mit 1.000 m² und zwei neuere Gebäude mit jeweils
150 m². Da unsere Methode nur die Anzahl der Gebäude berücksichtigt, gewichtet sie bei der Berechnung des
durchschnittlichen Energieverbrauchs das ältere Gebäude mit einem Drittel und die neueren Gebäude mit zwei Dritteln.
Tatsächlich entfällt jedoch der Großteil der beheizten Fläche in der Gitterzelle auf das ältere Gebäude. Da ältere
Gebäude aufgrund schlechterer Dämmung tendenziell mehr Energie verbrauchen, würde unser Ansatz den tatsächlichen
Heizenergieverbrauch in diesem Beispiel unterschätzen, weil das Gebäude mit hohem Energiebedarf in der Berechnung zu
wenig Gewicht erhält.

Dasselbe Problem tritt bei der Schätzung des durchschnittlichen Emissionsfaktors in jeder Gitterzelle auf, die auf der
Anzahl der Gebäude mit unterschiedlichen Energieträgern beruht.

Zudem berücksichtigen wir keine möglichen Zusammenhänge zwischen dem Alter der Gebäude und ihrem Energieträger. Ältere
Gebäude verfügen eher über klimaschädliche Energiequellen wie Ölheizungen, während neuere Gebäude eher mit Wärmepumpen
ausgestattet sind. Die Nichtbeachtung dieser möglichen Zusammenhänge führt zu einer Unterschätzung der Emissionen.

## Literatur

Eine ausführlichere Beschreibung der Methodik und der Datenquellen des Tools sowie Informationen zur Validierung der
Ergebnisse und zur Anwendung des Tools in der kommunalen Wärmeplanung finden Sie hier:

* Kong G., Ulrich V., Knoblauch S., Martin M., Schott M., von Elverfeldt K., Zipf A., Block S. 2027. Residential heating
  emissions tool in the Climate Action Navigator: High-resolution estimation based on open data. Computers, Environment
  and Urban Systems, 131, https://doi.org/10.1016/j.compenvurbsys.2026.102525.
