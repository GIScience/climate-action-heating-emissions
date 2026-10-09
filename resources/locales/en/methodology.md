How much carbon dioxide do we emit when heating our homes? This depends on three main factors:

1. Heated area: How large is our home and how much of it do we heat? Do we live alone in a large house or do we share a small apartment? Do we heat the entire house throughout the cold season or only the rooms we use while we use them?

2. Energy efficiency: How much energy do we need to heat one square meter of living space? This depends on how well insulated buildings are, but also on how we ventilate our homes during winter.

3. Energy source: Where does the heat come from? Do we use a gas boiler, an oil furnace, a fireplace, or a heat pump? The source (or "carrier") of energy determines how much CO₂ is emitted (and where) for each kWh of heating energy we use.

The 2022 German national census provides spatial information that allows us to estimate each of these key variables in any 100-m grid cell across Germany.

1. Multiply population by the average living space per capita to obtain total living space (i.e., the space that is presumably heated).

2. Calculate the average heating energy consumption per unit area (kWh per m²) based on the proportion of buildings constructed in different periods, since building standards have changed through time and newer buildings are typically better insulated.

3. Calculate the average carbon dioxide emissions per unit of heating energy (known as "emission factor", measured in kg of CO₂ per kWh) based on the proportion of buildings with different heating energy carriers (e.g., gas, oil, wood, district heating, etc.).

Emission estimates are the product of total living space, average energy consumption per square meter, and average emission factor.

## Data sources

### Spatial data
Gridded data from the German 2022 census can be downloaded [here](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/_inhalt.html#sprg1403932). We use the four following datasets:

1. Population counts ("Bevölkerungszahlen in Gitterzellen")
2. Living space per capita ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Building year of construction ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heating energy carriers in residential buildings ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Energy consumption
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


### Emission factors
We use emission factors from the ProBas database of Germany's Federal Environment Agency. We use two distinct sets of emission factors to estimate direct and life cycle emissions.

**Direct emissions** are based on emission factors for "unit processes", meaning that they include emissions related to burning fuels for heat, but do not include other upstream and downstream emissions in the lifecycle of the fuels.

We use carbon dioxide emission factors from the ProBas database for [gas](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=4c06c7a1-cdec-46cd-9929-0df2a70b8897&version=02.44.152&stock=PUBLIC&lang=de), [oil](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=26f4942c-889a-4b07-a2e7-3c6d8e74227e&version=02.44.152&stock=PUBLIC&lang=de), and [coal](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=cb66d367-05d9-485e-b301-24f7b88b4320&version=02.44.152&stock=PUBLIC&lang=de).

| Energy carrier                      | Emission factor (kg of CO₂/kWh) | Source / Notes |
|-------------------------------------|---------------------------------|----------------|
| Gas                                 | 0.20029                         | ProBas         |
| Oil                                 | 0.26793                         | ProBas         |
| Coal                                | 0.33661                         | ProBas         |
| Wood pellets                        | 0.34000                         | Note 1         |
| Biomass/Biogas                      | 0.20029                         | Note 1         |
| District heating                    | 0.00000                         | Note 2         |
| Electricity                         | 0.00000                         | Note 2         |
| Solar/Geothermal/Environmental Heat | 0.00000                         | Note 2         |

- **Note 1**: direct emissions do not include the full lifecycle of the energy carriers. That is, we estimate the CO₂ released while burning biomass without considering that those carbon atoms were only recently captured through photosynthesis. Hence, we used emission factors similar to gas and coal for biogas/biomass and wood pellets, respectively.

- **Note 2**: No CO₂ is emitted directly from heating buildings with electricity, heat pumps, and district heating, so these emission factors are 0. Heating such buildings can nonetheless generate emissions elsewhere (for example, at power or district heating plants), which are captured by the life-cycle emission estimates.

- **Note 3**: For buildings with unknown energy carrier, we use the average emission factor across the 8 categories above, weighting by the number of buildings with each carrier across all of Germany.


**Life cycle emissions** additionally include upstream and downstream emissions (e.g., energy production, processing, and distribution), and thus are based on Life Cycle Inventory emission factors from ProBas.

In contrast to direct emissions, which include only carbon dioxide, life cycle emissions include other greenhouse gases and are thus reported in units of CO₂-equivalents by multiplying the emissions of different gases by their respective global warming potential (GWP) over 100 years (ProBas uses GWP values from the IPCC AR5 report).

We use GHG (carbon dioxide equivalents) emission factors from the ProBas database. For [gas](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=c6fb47f4-dafa-4aea-b009-1dbf9ca1d8ca&lang=de) and [oil](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=0593c706-4ee5-44ae-85ef-bd60eac7c9c8&lang=de) we assume buildings use condensing boilers. For [coal](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=127daa60-ce89-4ad3-9fc2-dd9932481d41&version=02.44.152&stock=PUBLIC) we assume lignite briquettes. For [wood](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=74cfbbc8-96d4-49ae-8052-6ec8d8ece18f&version=02.44.152&stock=PUBLIC&lang=en) we assume wood pieces are burned in a central heating system. For [district heating](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=6dc315d7-c017-46ed-99f8-05ff57de1702&lang=de), we assume the German mix in 2020. Note that this is an average value, and the actual emissions can vary widely depending on the heat sources feeding into the district heating network. Similarly, for [electricity](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=6abaf6e8-ad5f-434d-bd0d-9d4682bba924&version=02.44.152&stock=PUBLIC&lang=en) we assume the average German mix in 2020. For [heat pumps](https://data.probas.umweltbundesamt.de/datasetdetail/process.xhtml?uuid=0d3ea28c-3efa-449f-897c-8dfaa291c4e7&version=02.44.152&stock=PUBLIC&lang=en) we assume air heat pumps powered with the average German electricity mix in 2020.

| Energy carrier                      | Emission factor (kg of CO₂-eq./kWh) | Source / Notes  |
|-------------------------------------|-------------------------------------|-----------------|
| Gas                                 | 0.232                               | ProBas          |
| Oil                                 | 0.318                               | ProBas          |
| Coal                                | 0.646                               | ProBas          |
| Wood pellets                        | 0.017                               | ProBas          |
| Biomass/Biogas                      | 0.017                               | Note 4          |
| District heating                    | 0.154                               | ProBas          |
| Electricity                         | 0.417                               | ProBas          |
| Solar/Geothermal/Environmental Heat | 0.130                               | ProBas          |

- **Note 4**: The Biomass/Biogas category includes different biogenic fuels for which ProBas does not provide emission factors. We thus use the same emission factor as for wood. This assumption is unlikely to have a large effect on the results at scales of whole neighborhoods and above, since less than 0.1% of residences in Germany are heated with this energy carrier.

### Other data sources
- Average German, weather-adjusted space heating energy consumption per square meter in residential buildings (127.1 kWh/m² per year): [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit)
- German average per capita carbon dioxide emissions from residential heating (2.2 t per year): [German Federal Environment Agency](https://www.umweltbundesamt.de/bild/durchschnittlicher-co2-fussabdruck-pro-kopf-in)
- German average emission factor (0.199 kg of carbon dioxide per kWh of heating energy used): calculated based on the proportion of buildings with different energy carriers across the entire country using the emission factors listed above.

## Uncertainty

### Uncertainty of the input data

1. Spatial data from the German 2022 census: to protect data privacy, the census uses the cell-key method to introduce random noise into the building counts at each grid cell. This means the average heating energy consumption rates and average emission factors are likely distorted, particularly in grid cells with only a few buildings. Unfortunately, the magnitude of this uncertainty is, by design, impossible to quantify.
2. Area-specific energy consumptions from co2online: 9 % uncertainty ([co2online, UBA, 2019](https://www.umweltbundesamt.de/publikationen/hintergrundbericht-wohnen-sanieren))
3. Emission factors from the German Environment Agency: not given

### Uncertainty from weighting by building count instead of heated area

To estimate the average area-specific energy consumption in each grid cell, we weight empirical heating energy consumption values for each building age class by the fraction of buildings in each age class, based on census data. For each grid cell, the census only reports how many buildings belong to each age class, but not their heated floor areas. Therefore, our calculations assumes that all buildings have the same heated area.

This assumption introduces uncertainty because buildings of different ages can differ in size. Imagine a grid cell with three buildings: one older building of 1,000 m² and two newer buildings of 150 m² each. Since our method only accounts for the number of buildings, it assigns one-third of the weight to the older building and two-thirds to the newer ones when calculating the average energy consumption. In reality, however, the older building represents most of the heated area in the grid cell. Since older buildings tend to consume more energy due to poorer insulation, our approach would underestimate the true heating energy consumption in this example, since the high-energy-demand building receives too little weight in the calculation.

The same problem emerges in the estimation of the average emission factor in each grid cell, which is based on the number of buildings with different energy carriers.

Moreover, we do not account for potential correlations between the age of the buildings and their energy carrier. Older buildings are more likely to have dirty energy carriers, such as oil heaters, while newer buildings are more likely to have heat pumps. Ignoring the potential correlations results in an underestimation of emissions.

## References

For a more detailed description of the methodology and data sources behind the tool, as well as on the validation of the results and application of the tool for municipal heating planning, see:

* Kong G., Ulrich V., Knoblauch S., Martin M., Schott M., von Elverfeldt K., Zipf A., Block S. 2027. Residential heating emissions tool in the Climate Action Navigator: High-resolution estimation based on open data. Computers, Environment and Urban Systems, 131, https://doi.org/10.1016/j.compenvurbsys.2026.102525.