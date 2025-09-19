How much carbon dioxide do we emit when heating our homes? This depends on three main factors:

1. Heated area: how large is our home and how much of it do we heat? Do we live alone in a large house or do we share a small apartment? Do we heat the entire house throughout the cold season or only the rooms we use while we use them?

2. Energy efficiency: how much energy do we need to heat one square meter? This depends on how well insulated buildings are, but also on how we ventilate our homes during winter.

3. Energy source: how do we heat? Do we use a gas boiler, an oil furnace, a fireplace, or a heat pump? The source (or "carrier") of energy determines how much CO2 is emitted (and where) for each kWh of heating energy we use.

The 2022 German national census provides spatial information (on a 100-m grid) that allows us to calculate (or estimate) each of these key variables in any 100-m grid cell across Germany. The calculation involves only three steps:

1. multiply population by the average living space per capita to obtain total living space (i.e., the space that is presumably heated).

2. calculate the average heating energy consumption rate (kWh per m2) of residential buildings based on buildings' year of construction.

3. calculate average carbon dioxide emissions per unit of heating energy (kg per kWh) based on the proportion of different heating energy carriers (e.g., gas, oil, wood, district heating, etc.).

Emission estimates are the product of total living space, average energy consumption rate, and average emission factor.

## Data sources

### Spatial data
Gridded data from the German 2022 census can be downloaded [here](https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/_inhalt.html#Gitterdaten2022). We use the four following datasets:

1. Population counts ("Bevölkerungszahlen in Gitterzellen")
2. Living space per capita ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Building year of construction ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heating energy carriers in residential buildings ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Energy consumption rates
We use energy consumption values for buildings of different age classes from [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit), which are based on measurements from over 300 thousand buildings across Germany, and are adjusted by temperature differences.

| Age class    | Energy consumption (kWh/m²) | Building standard |
|--------------|-----------------------------|-------------------|
| Before 1919  | 134.6                       |                   |
| 1919 to 1948 | 134.6                       |                   |
| 1949 to 1978 | 135.7                       |                   |
| 1979 to 1990 | 126.2                       | WSchVO 1          |
| 1991 to 2000 | 93.3                        | WSchVO 3          |
| 2001 to 2010 | 78.5                        | EnEV 2002         |
| 2011 to 2019 | 74.1                        | EnEV 2007*        |
| Since 2019   | 74.1                        | EnEV 2007*        |

When the age of a building is unknown, we assign it the mean energy consumption rate of buildings recorded in co2online (126.7 kWh).

### Emission factors
We use carbon dioxide emission factors from the Probas database for [gas](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=4c06c7a1-cdec-46cd-9929-0df2a70b8897&version=02.44.152&stock=PUBLIC&lang=de), [oil](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=26f4942c-889a-4b07-a2e7-3c6d8e74227e&version=02.44.152&stock=PUBLIC&lang=de), and [coal](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=cb66d367-05d9-485e-b301-24f7b88b4320&version=02.44.152&stock=PUBLIC&lang=de). Note that we use emission factors for "unit processes", meaning that they include emissions related to burning the fuels for heat, but do not include other upstream and downstream emissions in the lifecycle of the fuels.

| Energy carrier                      | Emission factor (kg of CO₂/kWh) | Source / Notes |
|-------------------------------------|---------------------------------|----------------|
| Gas                                 | 0.20029                         | Probas         |
| Oil                                 | 0.26793                         | Probas         |
| Coal                                | 0.33661                         | Probas         |
| Wood pellets                        | 0.34000                         | Note 1         |
| Biomass/Biogas                      | 0.20029                         | Note 1         |
| District heating                    | 0.00000                         | Note 2         |
| Electricity                         | 0.00000                         | Note 2         |
| Solar/Geothermal/Environmental Heat | 0.00000                         | Note 2         |
| Unknown                             | 0.19534                         | Note 3         |

- **Note 1**: The model estimates emissions associated with heating without accounting for the full lifecycle of the energy carriers. This means that we estimate the CO2 released while burning biomass without considering that carbon was only recently captured through photosynthesis. Hence, we used emission factors similar to gas and coal for biogas/biomass and wood pellets, respectively.

- **Note 2**: The model estimates territorial (scope 1) emissions. Since no emissions are generated directly at buildings heated with electricity, heat pumps, and district heating, these emission factors are 0. Heating these buildings likely still generates emissions (for example, for electricity generation), but these happen elsewhere (e.g., at power or district heating plants).

- **Note 3**: For buildings with unknown energy carrier, we use the average emission factor across the 8 categories above, weighting by the number of buildings with each carrier across all of Germany.

### Other data sources
German average heating energy consumption rate in residential buildings (127.1 kWh/m² per year, plotted in the respective histogram): [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit)
German average per capita carbon dioxide emissions from residential heating (2.2 t per year, plotted in the respective histogram): [UBA](https://www.umweltbundesamt.de/bild/durchschnittlicher-co2-fussabdruck-pro-kopf-in)