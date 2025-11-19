# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project mostly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/compare/1.1.1...main)

### Fixed
- rename results' index from 'raster_id_100m' to 'index' to support the grid value visualization in dashboard ([41](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/41))

### Changed
- Introduced artifact tags ([40](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/40))
- Changed the database connection to read tables from the `census_de` schema ([#32](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/32))
- Ignore total_buildings column from census when computing emission factors and heating consumption ([#39](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/39))
- Changed colormap of construction year and energy carrier artifacts to coolwarm_r ([#48](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/48))

### Added
- Maps of dominant building ages and energy carriers ([28](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/28))
- Tests for gridded artifact functions, several functions in utils, and get_clipped_census_grid ([24](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/24), [38](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/38))
- Paragraph on uncertainty sources to methodology description ([#44](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/44))
- Temporal flexible emission simulation: Provide yearly emission maps with daily emission line chart (Deactivated in production due to long runtime) ([#6](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/6))
- Line with mean emission factor in emission factor histogram ([#45](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/45))

## [1.1.1](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/releases/1.1.1) - 2025-06-04

### Fixed

- use a `NullPool` connection with our database engine to avoid intermittent database connection failures

### Changed

- Updated climatoology to 6.4.2

### Added

- Information about emission factors and their source to the methodology ([29](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/29))

## [1.1.0](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/releases/1.1.0) - 2025-06-03

### Changed

- Mapped emissions are now in vector (geoJSON) format, allowing better display and downloading of actual emissions data ([18](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/18))
- Expanded methodology with more context for non-technical users ([19](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/19))
- Simplified legend annotation to avoid capitalization typos ([15](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/15))
- Capped maximum values for color maps of per capita and absolute emissions ([25](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/25))

### Added

- Gridded maps of emission drivers: emission factor, energy consumption, and living space per capita ([26](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/26))
- Reference lines for histograms of per capita emissions and energy consumption ([10](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/10))
- Safety check and error message for AOIs without residential buildings

- Test for check_aoi() to see if it correctly catches AOIs outside of Germany ([16](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/issues/16))


## [1.0.1](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/releases/1.0.1) - 2025-05-14

### Changed

- New icon matching style of other assessment tools in the Climate Action Navigator

## [1.0.0](https://gitlab.heigit.org/climate-action/plugins/heating-emissions/-/releases/1.0.0)

### Added

- Absolute Heating Emissions Artifact
- Per Capita Heating Emissions Artifact
- Histograms of:
  - per capita CO2 emissions
  - energy consumption
  - emission factors
