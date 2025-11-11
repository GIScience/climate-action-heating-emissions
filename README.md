# <img src="resources/heating-radiator.jpeg" width="5%"> Space heating emissions

Space heating is the main driver of energy consumption in buildings, and therefore of greenhouse emissions. This plugin estimates annual building space heating emissions by combining open data from various sources. In its current, first version, the plugin relies primarily on gridded data (100-m resolution) from the German 2022 census, and includes only _residential_ buildings.

We also provide the *simulated* daily emission estimates for a self-defined year. This estimate is simulated based on the [demand_ninja](https://doi.org/10.1038/s41560-023-01341-5) model and our emission factors.

## Data sources

### Spatial data
Gridded data from the German 2022 census can be downloaded [here](https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/_inhalt.html#Gitterdaten2022). We use the four following datasets:

1. Population counts ("Bevölkerungszahlen in Gitterzellen")
2. Living space per capita ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Building year of construction ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heating energy carriers in residential buildings ("Gebäude mit Wohnraum nach Energieträger der Heizung in Gitterzellen")

### Energy consumption rates
We use energy consumption values for buildings of different age classes from [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit), which are based on measurements from over 300 thousand buildings across Germany, and are adjusted by temperature differences.
Co2online gave us permission to use their data in this plugin.

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

- **Note 1**: The model estimates emissions associated with heating without accounting for the full lifecycle of the energy carriers. This means that we estimate the CO2 released while burning biomass without considering that carbon was only recently captured through photosynthesis. Hence, we used emission factors similar to gas and coal for biogas/biomass and wood pellets, respectively.

- **Note 2**: The model estimates territorial (scope 1) emissions. Since no emissions are generated directly at buildings heated with electricity, heat pumps, and district heating, these emission factors are 0. Heating these buildings likely still generates emissions (for example, for electricity generation), but these happen elsewhere (e.g., at power or district heating plants).

- **Note 3**: For buildings with unknown energy carrier, we use the average emission factor across the 8 categories above, weighting by the number of buildings with each carrier across all of Germany.

### Weather data
We use [ERA5 reanalysis weather data](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) for the heating demand simulation by `demand_ninja` model.
The weather data-based heating demand estimates are further used for the daily emission estimation.
- 2m_temperature
- specific humidity calculated by *2m_dewpoint_temperature* and *surface_pressure* ([reference: 7.2.1(b)](https://www.ecmwf.int/en/elibrary/81626-ifs-documentation-cy49r1-part-iv-physical-processes))
- wind speed calculated by *10m_u_component_of_wind* and *10m_v_component_of_wind*
- surface_solar_radiation_downwards

## Development setup

To run your plugin locally requires the following setup:

1. Set up the [infrastructure](https://gitlab.heigit.org/climate-action/infrastructure) locally in `devel` mode
2. Copy your [.env.base_template](.env.base_template) to `.env.base` and update it
3. Run `poetry run python {plugin-name}/plugin.py`

If you want to run your plugin through Docker, refer to
the [Plugin Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).

### Further requirements

Make sure you have the following installed on your machine:
- psql (PostgreSQL) v16.10 or higher
- postgis v3.4.2 or higher

### Testing

We use [pytest](https://pytest.org) as a testing engine.
Ensure all tests are passing by running `poetry run pytest`.

#### Coverage

To get a coverage report of how much of your code is run during testing, execute
`poetry run pytest --ignore test/core/ --cov`.
We ignore the `test/core/` folder when assessing coverage because the core tests run the whole plugin to be sure
everything successfully runs with a very basic configuration.
Yet, they don't actually test functionality and therefore artificially inflate the test coverage results.

To get a more detailed report including which lines in each file are **not** tested,
run `poetry run pytest --ignore test/core/ --cov --cov-report term-missing`

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

## Docker

To build docker images, you need to give the engine access to the climatoology repository.
Create a file `CI_JOB_TOKEN` that contains your personal access token to the climatoology repository.

### Build

The tool is also [Dockerised](Dockerfile).
Images are automatically built and deployed in the [CI-pipeline](.gitlab-ci.yml).

In case you want to manually build and run locally (e.g. to test a new feature in development), execute

```shell
docker build --secret id=CI_JOB_TOKEN . --tag repo.heigit.org/climate-action/heating-emissions:devel
```

Note that this will overwrite any existing image with the same tag (i.e. the one you previously pulled from the Climate
Action docker registry).

To mimic the build behaviour of the CI you have to add `--build-arg CI_COMMIT_SHORT_SHA=$(git rev-parse --short HEAD)`
to the above command.

### Run

If you have the Climate Infrastructure running (see [Development Setup](#development-setup)) you can now run the
container via

```shell
docker run --rm --network=host --env-file .env.base --env-file .env repo.heigit.org/climate-action/heating-emissions:devel
```

### Deploy

Deployment is handled by the GitLab CI automatically.
If for any reason you want to deploy manually (and have the required rights), after building the image, run

```shell
docker image push repo.heigit.org/climate-action/heating-emissions:devel
```
