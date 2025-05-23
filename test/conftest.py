from unittest.mock import patch
import uuid

import pandas as pd
from climatoology.base.baseoperator import AoiProperties
from climatoology.base.computation import ComputationScope
import pytest
import shapely
import geopandas as gpd

from heating_emissions.core.operator_worker import Operator
from heating_emissions.core.input import ComputeInput


@pytest.fixture
def default_compute_input() -> ComputeInput:
    return ComputeInput()


@pytest.fixture
def default_german_aoi() -> shapely.MultiPolygon:
    return shapely.MultiPolygon(
        polygons=[
            [
                [
                    [12.3, 48.22],
                    [12.3, 48.34],
                    [12.48, 48.34],
                    [12.48, 48.22],
                    [12.3, 48.22],
                ]
            ]
        ]
    )


@pytest.fixture
def default_non_german_aoi() -> shapely.MultiPolygon:
    return shapely.MultiPolygon(
        polygons=[
            [
                [
                    [0.3, 48.22],
                    [0.3, 48.34],
                    [0.48, 48.34],
                    [0.48, 48.22],
                    [0.3, 48.22],
                ]
            ]
        ]
    )


@pytest.fixture
def default_aoi_properties() -> AoiProperties:
    return AoiProperties(name='Heidelberg', id='heidelberg')


@pytest.fixture
def default_non_german_aoi_properties() -> AoiProperties:
    return AoiProperties(name='Abenteuerland', id='abenteuerland')


# The following fixtures can be ignored on plugin setup
@pytest.fixture
def compute_resources():
    with ComputationScope(uuid.uuid4()) as resources:
        yield resources


@pytest.fixture
def operator():
    with patch('heating_emissions.core.operator_worker.MetaData.reflect', side_effect=None):
        operator = Operator(ca_database_url='sqlite:///:memory:')
        yield operator


@pytest.fixture
def mock_query_census_tables():
    default_census_grid = gpd.read_file('resources/test/census_grid.geojson').set_index('raster_id_100m')

    def return_default_table(db_connection, raster_ids, table_name):
        return pd.read_csv(f'resources/test/{table_name}.csv').set_index('raster_id_100m')

    with (
        patch('heating_emissions.components.census_data.get_clipped_census_grid', return_value=default_census_grid),
        patch('heating_emissions.components.census_data.query_table_from_db', side_effect=return_default_table),
    ):
        yield
