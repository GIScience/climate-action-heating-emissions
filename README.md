# <img src="resources/heating-radiator.jpeg" width="5%"> Space heating emissions

Space heating is the main driver of energy consumption in buildings, and therefore of greenhouse emissions.
This plugin estimates annual building space heating emissions by combining open data from various sources.
In its current, first version, the plugin relies primarily on gridded data (100-m resolution) from the German 2022
census, and includes only _residential_ buildings.

We also provide the *simulated* daily emission estimates for a self-defined year.
This estimate is simulated based on the [demand_ninja](https://doi.org/10.1038/s41560-023-01341-5) model and our
emission factors.

## Data sources

### Spatial data

Gridded data from the German 2022 census can be
downloaded [here](https://www.zensus2022.de/DE/Ergebnisse-des-Zensus/_inhalt.html#Gitterdaten2022).
We use the four following datasets:

1. Population counts ("Bevölkerungszahlen in Gitterzellen")
2. Living space per capita ("Durchschnittliche Wohnfläche je Bewohner in Gitterzellen")
3. Building year of construction ("Gebäude nach Baujahr in Mikrozensus-Klassen in Gitterzellen")
4. Heating energy carriers in residential buildings ("Gebäude mit Wohnraum nach Energieträger der Heizung in
   Gitterzellen")

### Energy consumption rates

We use energy consumption values for buildings of different age classes
from [co2online](https://www.wohngebaeude.info/daten/#/heizen/bundesweit), which are based on measurements from over 300
thousand buildings across Germany, and are adjusted by temperature differences.
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

We use two types of emission factors: Direct (scope 1) and life cycle (scope 1, 2 and 3).
Details are documented in our [methodology](https://gitlab.heigit.org/climate-action/plugins/heating-emissions#emission-factors).

### Weather data
(This data and its related function is not available to the public yet limited by slow computation speed, but will be in the future after optimization)

We
use [ERA5 reanalysis weather data](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview)
for the heating demand simulation by `demand_ninja` model.
The weather data-based heating demand estimates are further used for the daily emission estimation.

- 2m_temperature
- specific humidity calculated by *2m_dewpoint_temperature* and
  *surface_pressure* ([reference: 7.2.1(b)](https://www.ecmwf.int/en/elibrary/81626-ifs-documentation-cy49r1-part-iv-physical-processes))
- wind speed calculated by *10m_u_component_of_wind* and *10m_v_component_of_wind*
- surface_solar_radiation_downwards

## Future roadmap
### Ongoing
- Downscaling to hourly emission estimates by linking energy consumption to local weather, including the map of yearly simulated results and line charts showing daily emissions
- Explanatory analysis of heating emissions
  - Adding histograms for living space per capita
  - Adding proportional bar plots of energy carriers and building age to compare the specific AOI with Germany.

### Short-term (around next 6 months)
- Assessing and propagating uncertainty in the spatial allocation of energy carriers at the building level
- Simulating the effects of interventions and behavioral changes on emissions

### Long-term
- Adding estimates of water heating emissions
- Extend to other countries

If you have any suggestions for other features or improvements, please feel free to reach out to us through `climateactionnavigator@heigit.org`.

## Starting the plugin

### Preparation

To prepare running the plugin you have to have access or set up a database containing the required data.
See the [CA data repository](https://gitlab.heigit.org/climate-action/dev-ops/data-etl) for an explanation of how to
achieve that.

Optionally, you will need a CDASPI key if you want to run the temporal downscaling model.
Acquire one from [ECMWF](https://cds.climate.copernicus.eu/how-to-api).

Now copy the `.env_template` with `cp .env_template .env` and fill it with the above acquired information.

### Execute

There are two ways how to start the plugin.
To run a single computation run `poetry run plugin compute --aoi-file resources/aoi-template.geojson`.
See `poetry run plugin compute --help` for more info on customisation.
To run the plugin as an entity connected to the CA platform, see [below](#development-setup).

### Docker

The tool is also [Dockerised](Dockerfile).

To build and run the docker image execute

```shell
docker build . --tag heating-emissions
docker run \
  --env-file .env \
  -v ./resources/aoi-template.geojson:/resources/aoi.geojson  \
  -v ./results:/results \
  --rm \
  heating-emissions compute
```

To change the target AOI mount a different AOI file with `-v`.

## Development setup

To run your plugin locally as an entity of the CA platform requires the following setup:

1. Set up the [infrastructure](https://gitlab.heigit.org/climate-action/infrastructure) locally in `devel` mode
2. Copy your [.env.base_template](.env.base_template) to `.env.base` and update it
3. Run `poetry run plugin start`

If you want to run your plugin through Docker, refer to
the [Plugin Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).

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

