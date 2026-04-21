import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import shapely
from climatoology.base.exception import ClimatoologyUserError
from pandas._testing import assert_series_equal

from heating_emissions.components.census_data import (
    clean_building_age_data,
    extract_dominant_characteristics,
    get_census_tables_from_db,
    get_clipped_census_grid,
)


def test_get_census_tables_from_db(operator):
    with operator.ca_database_connection.engine.connect() as connection:
        raster_grid = gpd.read_postgis(
            'select * from census_de.raster_grid_100m', con=connection, geom_col='geometry', index_col='raster_id_100m'
        )
    census_data, uncalc_census_data = get_census_tables_from_db(
        db_connection=operator.ca_database_connection, raster_grid=raster_grid
    )

    expected_columns = ['population', 'average_sqm_per_person', 'heat_consumption', 'direct', 'life_cycle']
    expected_columns_uncalc = ['dominant_age', 'dominant_energy']

    assert all([c in census_data.columns for c in expected_columns])
    assert all([c in uncalc_census_data.columns for c in expected_columns_uncalc])


def test_get_clipped_census_grid(default_german_aoi, operator):
    result_gdf = get_clipped_census_grid(operator.ca_database_connection, default_german_aoi)

    inside_aoi = [
        'CRS3035RES100mN2923000E4224200',
        'CRS3035RES100mN2923000E4224300',
        'CRS3035RES100mN2923000E4224400',
        'CRS3035RES100mN2923100E4224100',
        'CRS3035RES100mN2923100E4224200',
        'CRS3035RES100mN2923100E4224300',
    ]

    outside_aoi = ['CRS3035RES100mN2922800E4223800', 'CRS3035RES100mN2922800E4223900']

    assert isinstance(result_gdf, gpd.GeoDataFrame)
    assert all([index in result_gdf.index for index in inside_aoi])
    assert not any([index in result_gdf.index for index in outside_aoi])


def test_get_clipped_census_grid_no_data(operator):
    empty_aoi = shapely.MultiPolygon(
        polygons=[
            [
                [
                    [9.664, 49.410],
                    [9.664, 49.419],
                    [9.670, 49.419],
                    [9.670, 49.410],
                    [9.664, 49.410],
                ]
            ]
        ]
    )
    with pytest.raises(ClimatoologyUserError, match='no data for residential buildings'):
        get_clipped_census_grid(operator.ca_database_connection, empty_aoi)


@pytest.mark.parametrize(
    'dominant_character, data, expected',
    [
        ('dominant_age', {'pre_1919': [5], 'post_2000': [3]}, 'pre-1919'),
        ('dominant_energy', {'wood': [4], 'gas': [2]}, 'Wood'),
    ],
)
def test_extract_dominant_characteristics(dominant_character, data, expected):
    census_dominant_data = gpd.GeoDataFrame(data)
    received = extract_dominant_characteristics(census_dominant_data, dominant_character)

    assert received.iloc[0] == expected


def test_extract_dominant_characteristics_error():
    census_dominant_data = gpd.GeoDataFrame({'col1': [1]})

    with pytest.raises(ValueError, match='Unknown dominant_character: invalid_type'):
        extract_dominant_characteristics(census_dominant_data, 'invalid_type')


def test_clean_building_age_data_remove_uninhabited_areas():
    inhabited_cell_id = 'CRS3035RES100mN2923000E4224300'
    cell_id_wo_buildings = 'CRS3035RES100mN2923000E4224400'

    expected_heat_consumption = pd.Series({inhabited_cell_id: 134.6}, name='heat_consumption')
    expected_dominant_age = pd.Series({inhabited_cell_id: 'pre-1919'}, name='dominant_age')

    census_data = pd.DataFrame(
        {
            'total_buildings': {inhabited_cell_id: 3, cell_id_wo_buildings: 3},
            'pre_1919': {inhabited_cell_id: 3.0, cell_id_wo_buildings: np.nan},
            '1919_1948': {inhabited_cell_id: 3.0, cell_id_wo_buildings: np.nan},
            '1949_1978': {inhabited_cell_id: None, cell_id_wo_buildings: None},
            '1979_1990': {inhabited_cell_id: None, cell_id_wo_buildings: None},
            '1991_2000': {inhabited_cell_id: None, cell_id_wo_buildings: None},
            '2001_2010': {inhabited_cell_id: None, cell_id_wo_buildings: None},
            '2011_2019': {inhabited_cell_id: None, cell_id_wo_buildings: None},
            'post_2020': {inhabited_cell_id: None, cell_id_wo_buildings: None},
        }
    )

    computed_heat_consumption, computed_dominant_age = clean_building_age_data(census_data=census_data)

    assert_series_equal(left=expected_heat_consumption, right=computed_heat_consumption, check_dtype=False)
    assert_series_equal(left=expected_dominant_age, right=computed_dominant_age)
