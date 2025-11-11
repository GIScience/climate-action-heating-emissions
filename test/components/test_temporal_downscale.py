from pathlib import Path

import geopandas as gpd
import pandas as pd

from heating_emissions.components.temporal_downscale.era5_data import open_era5_data
from heating_emissions.components.temporal_downscale.temporal_estimation import (
    calculate_hourly_emissions_permonth,
    collect_building_hourly_energy_demand_permonth,
)


def test_open_era5_data(default_era5_data_dir: Path):
    era5_filepath = str(default_era5_data_dir / 'era5_data_heidelberg_2022_1.zip')

    era5_dataset = open_era5_data(era5_filepath)
    era5_data_layers = era5_dataset.variables.keys()

    expected_data_layers = ['longitude', 'latitude', 't2m', 'q2m', 'ssrd', 'wind2m']

    assert all([c in era5_data_layers for c in expected_data_layers])
    assert era5_dataset.rio.crs.to_epsg() == 4326


def test_collect_building_hourly_energy_demand(
    operator, default_german_aoi, default_aoi_properties, default_era5_data_dir, mock_cdsapi_client
):
    year = 2022
    month = 1

    hourly_demand = collect_building_hourly_energy_demand_permonth(
        year=year, month=month, aoiname=default_aoi_properties.name, savedir=default_era5_data_dir
    )

    expected_columns = ['valid_time', 'latitude', 'longitude', 'heating_demand']

    assert all([c in hourly_demand.columns for c in expected_columns])
    assert len(hourly_demand) == 744


def test_calculate_hourly_emissions_permonth():
    calculated_census_data = gpd.read_file('resources/test/temporal_downscale/census_data_heidelberg.gpkg').set_index(
        'raster_id_100m'
    )
    hourly_demand = pd.read_csv('resources/test/temporal_downscale/hourly_demand_2022-1_heidelberg.csv')

    emission_map, emission_hourly_regional = calculate_hourly_emissions_permonth(hourly_demand, calculated_census_data)

    expected_index_map = ['raster_id_100m']
    expected_columns_map = ['monthly_emissions']
    expected_columns_hourly_line = ['valid_time', 'regional_hourly_emissions']

    assert emission_map.index.names == expected_index_map
    assert all([c in emission_map.columns for c in expected_columns_map])
    assert all([c in emission_hourly_regional.columns for c in expected_columns_hourly_line])
