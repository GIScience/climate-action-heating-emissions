# <img src="resources/heating-radiator.jpeg" width="5%"> Space heating emissions

Space heating is the main driver of energy consumption in buildings, and therefore of greenhouse emissions.
This plugin estimates annual building space heating emissions by combining open data from various sources.
In its current, first version, the plugin relies primarily on gridded data (100-m resolution) from the German 2022 census, and includes only _residential_ buildings.

We also provide *simulated* daily emission estimates for a self-defined year.
This estimate is simulated based on the [demand_ninja](https://doi.org/10.1038/s41560-023-01341-5) model and our emission factors.
(This function is not available to the public yet limited by slow computation speed, but will be in the future after optimization)
The code for this function can be found [here](heating_emissions/components/temporal_downscale).

## Data sources
Data sources are documented in our [methodology](resources/methodology.md?ref_type=heads#data-sources).

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

### Translations

We use [GNU gettext](https://www.gnu.org/software/gettext/) with support
of [pybabel](https://babel.pocoo.org/en/latest/) for translations.
In case a string or Markdown file was updated, the translation needs to be adapted.
To do so run

1. Extract .pot templates
   ```shell
   # If changes to the .md files were made run
   poetry run md2po -P -S resources/locales/en/*.md resources/locales
   # If changes to strings in the source code were made run
   poetry run pybabel extract heating_emissions/ \
       -w 120 \
       -o resources/locales/messages.pot \
       --keyword=tr \
       --copyright-holder="HeiGIT gGmbH" \
       --project=heating-emissions
   ```
2. Update .po files
   ```shell
   poetry run pybabel update \
       -w 120 \
       -i resources/locales/<the-changed-file>.pot \
       -D <the-changed-file> \
       -d resources/locales/
   ```
3. Now update the fresh .po files with the new translations
4. If changes were made to the .md files, for each available language run
   ```shell
   poetry run po2md \
     -m 120 \
     -i resources/locales/<target-lang>/LC_MESSAGES/ \
     -t resources/locales/en/ \
     -o resources/locales/<target-lang>
   ```

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

