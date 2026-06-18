Wie viel Kohlendioxid verursachen wir beim Heizen unserer Wohnungen? Dies hängt von drei Hauptfaktoren ab:

1. Beheizte Fläche: Wie groß ist unsere Wohnstätte und wie viel davon heizen wir? Wohnen wir allein in einem großen Haus
   oder teilen wir uns eine kleine Wohnung? Heizen wir während der kalten Jahreszeit den gesamten Wohnraum oder nur
   Räume, während wir sie nutzen?

2. Energieeffizienz: Wie viel Energie benötigen wir, um einen Quadratmeter zu heizen? Das hängt davon ab, wie gut
   Gebäude gedämmt sind, aber auch davon, wie wir unsere Wohnungen im Winter lüften.

3. Energiequelle: Wie heizen wir? Nutzen wir einen Gaskessel, einen Ölofen, einen Kamin oder eine Wärmepumpe? Die
   Energiequelle bzw. der Energieträger bestimmt, wie viel CO₂ pro kWh Heizenergie, die wir verbrauchen, ausgestoßen
   wird (und wo).

Der deutsche Zensus von 2022 liefert räumliche Daten, anhand derer wir all diese Schlüsselvariablen für jede
100-Meter-Gitterzelle in ganz Deutschland schätzen können.

1. Multiplikation der Einwohnerzahl mit der durchschnittlichen Wohnfläche pro Kopf, um die Gesamtwohnfläche zu erhalten
   (d. h. die Fläche, die vermutlich beheizt wird).

2. Berechnung des durchschnittlichen flächenbezogenen Heizenergieverbrauchs (kWh pro m²) von Wohngebäuden auf der
   Grundlage des Baujahres der Gebäude.

3. Berechnung der durchschnittlichen Kohlendioxidemissionen pro Einheit Heizenergie (kg pro kWh) auf der Grundlage des
   Anteils der Gebäude mit unterschiedlichen Heizenergieträgern (z. B. Gas, Öl, Holz, Fernwärme usw.).

Die Emissionsschätzungen sind das Produkt aus Gesamtwohnfläche, durchschnittlichem flächenbezogenen Energieverbrauch und
durchschnittlichem Emissionsfaktor.

## Datenquellen

### Räumliche Daten
Rasterdaten des deutschen Zensus 2022 können
[hier](https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/_inhalt.html#Gitterdaten2022) heruntergeladen werden. Wir
verwenden die folgenden vier Datensätze:

1. Bevölkerung ("Bevölkerungszahlen in Gitterzellen")
2. Wohnfläche pro Kopf ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Baujahr der Gebäude ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heizenergieträger in Wohngebäuden ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Flächenbezogenene Energieverbräuche
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
Wir verwenden Emissionsfaktoren aus der ProBas-Datenbank des Umweltbundesamtes. Zur Schätzung sowohl der direkten
Emissionen als auch der Lebenszyklus-Emissionen nutzen wir zwei unterschiedliche Sätze von Emissionsfaktoren.

**Direkte Emissionen (Scope 1)** basieren auf Emissionsfaktoren für „Einzelprozesse“, was bedeutet, dass sie die
Emissionen aus der Verbrennung von Brennstoffen zur Wärmeerzeugung umfassen, jedoch keine anderen vor- und
nachgelagerten Emissionen im Lebenszyklus der Brennstoffe.

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
und die tatsächlichen Emissionen je nach Energiequelle des Fernwärmekraftwerks, z.B. Kohle, Gas, Holz oder eine
Wärmepumpe, stark variieren können. Ebenso gehen wir bei
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
- Durchschnittlicher flächenbezogener Heizenergieverbrauch in Wohngebäuden in Deutschland (127,1 kWh/m² pro Jahr):
  [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit)
- Durchschnittliche Pro-Kopf-Kohlendioxidemissionen durch das Heizen von Wohnraum in Deutschland (2,2 t pro Jahr):
  [Umweltbundesamt](https://www.umweltbundesamt.de/bild/durchschnittlicher-co2-fussabdruck-pro-kopf-in)
- Deutscher durchschnittlicher Emissionsfaktor (0,199 kg Kohlendioxid pro kWh verbrauchter Heizenergie): Berechnet auf
  der Grundlage des Anteils der Gebäude mit verschiedenen Energieträgern im gesamten Bundesgebiet unter Verwendung der
  oben aufgeführten Emissionsfaktoren.

## Unsicherheit

### Unsicherheit der Eingabedaten

1. Räumliche Daten aus dem deutschen Zensus: Da es sich um offizielle amtliche Daten handelt, gehen wir von einer sehr
   geringen (vernachlässigbaren) Unsicherheit aus
2. Flächenbezogene Energieverbrauchswerte von co2online: 9 % Unsicherheit ([co2online, UBA,
   2019](https://www.umweltbundesamt.de/publikationen/hintergrundbericht-wohnen-sanieren))
3. Emissionsfaktoren vom Umweltbundesamt: nicht angegeben

### Unsicherheit durch die Gewichtung nach Anzahl der Gebäude statt nach Gebäudefläche

Um den durchschnittlichen flächenbezogenen Energieverbrauch in jeder Gitterzelle zu schätzen, gewichten wir die
empirischen Heizenergieverbrauchswerte der einzelnen Gebäudealtersklassen mit dem Anteil der Gebäude in der jeweiligen
Altersklasse, basierend auf Zensusdaten. Für jede Gitterzelle wissen wir, wie viele Gebäude zu jeder Altersklasse
gehören, doch fehlen uns Informationen über ihre Größe oder beheizte Fläche. Daher nehmen wir für alle Gebäude die
gleiche beheizte Fläche an.

Diese Annahme kann jedoch zu Unsicherheiten innerhalb einer Gitterzelle führen, da sich Gebäude unterschiedlichen Alters
in ihrer Größe erheblich unterscheiden können. Stelle Dir beispielsweise eine Gitterzelle mit drei Gebäuden vor: ein
älteres Gebäude aus der Altersklasse 1949–1978 mit einer beheizten Fläche von 1.000 m² und zwei neuere Gebäude aus der
Altersklasse 2011–2019 mit jeweils 150 m².

Unsere Methode berücksichtigt nur die Anzahl der Gebäude, aber nicht deren Größe. Bei der Berechnung des
durchschnittlichen Energieverbrauchs werden daher dem älteren Gebäude ein Drittel der Gewichtung und den neueren
Gebäuden zwei Drittel der Gewichtung zugewiesen. Tatsächlich macht das ältere Gebäude den größten Teil der beheizten
Fläche in der Gitterzelle aus. Da ältere Gebäude aufgrund ihrer schlechteren Dämmung tendenziell mehr Energie
verbrauchen, würde dieser Ansatz den tatsächlichen Heizenergieverbrauch in diesem Beispiel unterschätzen, da das Gebäude
mit hohem Energiebedarf bei der Berechnung zu gering gewichtet wird.

Eine ähnliche Unsicherheit ergibt sich bei der Gewichtung mit dem Anteil der Gebäude mit den jeweiligen
Heizenergieträgern (basierend auf Zensusdaten) zur Ermittlung des durchschnittlichen Emissionsfaktors in jeder
Gitterzelle.

Zudem berücksichtigen wir keine möglichen Zusammenhänge zwischen dem Alter der Gebäude und ihrem Energieträger. Ältere
Gebäude verfügen eher über klimaschädliche Energiequellen wie Ölheizungen, während neuere Gebäude eher mit Wärmepumpen
ausgestattet sind. Die Nichtbeachtung dieser möglichen Zusammenhänge führt zu einer Unterschätzung der Emissionen.

## Grundwissen

### Was sind Sope 1, 2 und 3 Emissionen?
1. **Scope 1** Emissionen sind direkte Emissionen, die in den Gebäuden selbst entstehen, z.B. durch die Verbrennung von
   Brennstoffen in einer Hausheizung. Emissionen aus Kraftwerken oder Fernwärmeanlagen sind hier nicht enthalten.
2. **Scope 2** Emissionen sind indirekte Emissionen, die bei der Erzeugung der Energie entstehen, die von der
   berichtenden Einheit verbraucht wird. Wird ein Gebäude mit Strom oder Fernwärme beheizt, gelten die Emissionen aus
   der Erzeugung dieses Stroms oder dieser Wärme als Scope-2-Emissionen.
3. **Scope 3** Emissionen sind alle anderen anfallenden indirekten Emissionen
