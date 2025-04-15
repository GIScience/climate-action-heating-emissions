# <img src="resources/icon.jpeg" width="5%"> Space heating emissions

Space heating is the main driver of energy consumption in buildings, and therefore of greenhouse emissions. This plugin estimates annual building space heating emissions by combining open data from various sources. In its current, first version, the plugin relies primarily on gridded data (100-m resolution) from the German 2022 census, and includes only _residential_ buildings.

## Data sources

### Spatial data
Gridded data from the German 2022 census can be downloaded from: https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/_inhalt.html#Gitterdaten2022

The current version of the plugin uses the following gridded census data:
- Population counts ("Bevölkerungszahlen in Gitterzellen")
- Living space per capita ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
- Building year of construction ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
- Heating energy carriers in residential buildings ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Energy consumption rates
We use energy consumption values for buildings of different age classes from (co2online)[https://www.wohngebaeude.info/daten/#/heizen/bundesweit], which are based on measurements from over 300 thousand buildings across Germany, and are adjusted by temperature differences.

| Age class    | Energy consumption (kWh/m2) | Notes      |
|--------------|-----------------------------|------------|
| Before 1919  | 134.6                       | Pre-war    |
| 1919 to 1948 | 134.6                       | Pre-war    |
| 1949 to 1978 | 135.7                       | Post-war   |
| 1979 to 1990 | 126.2                       | WSchVO 1   |
| 1991 to 2000 | 93.3                        | WSchVO 3   |
| 2001 to 2010 | 78.5                        | EnEV 2002  |
| 2011 to 2019 | 74.1                        | EnEV 2007* |
| Since 2019   | 74.1                        | EnEV 2007* |


When the age of a building is unknown, we assign them the mean energy consumption rate (126.7 kWh).

### Emission factors
We use carbon dioxide emission factors for each energy carrier (from unit processes) from the Probas database.


## Development setup

To run your plugin locally requires the following setup:

1. Set up the [infrastructure](https://gitlab.heigit.org/climate-action/infrastructure) locally in `devel` mode
2. Copy your [.env.base_template](.env.base_template) to `.env.base` and update it
3. Run `poetry run python {plugin-name}/plugin.py`

If you want to run your plugin through Docker, refer to
the [Plugin Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).

## Releasing a new plugin version

To release a new plugin version

1. Update the [CHANGELOG.md](CHANGELOG.md).
   It should already be up to date but give it one last read and update the heading above this upcoming release
2. Decide on the new version number.
   Once your plugin outgrew the 'special versions' `dummy` and `mvp`, we suggest you adhere to
   the [Semantic Versioning](https://semver.org/) scheme,
   based on the changes since the last release.
   You can think of your plugin methods (info method, input parameters and artifacts) as the public API of your plugin.
3. Update the version attribute in the [pyproject.toml](pyproject.toml) (e.g. by running
   `poetry version {patch|minor|major}`)
4. Create a [release]((https://docs.gitlab.com/ee/user/project/releases/#create-a-release-in-the-releases-page)) on
   GitLab, including a changelog

