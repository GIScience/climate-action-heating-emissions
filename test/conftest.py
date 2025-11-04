import os
import uuid
from pathlib import Path

import pytest
import shapely
from climatoology.base.baseoperator import AoiProperties
from climatoology.base.computation import ComputationScope
from pytest_postgresql import factories

from heating_emissions.core.input import ComputeInput
from heating_emissions.core.operator_worker import Operator


@pytest.fixture
def default_compute_input() -> ComputeInput:
    return ComputeInput()


@pytest.fixture
def default_german_aoi() -> shapely.MultiPolygon:
    return shapely.MultiPolygon(
        polygons=[
            [
                [
                    [8.664, 49.410],
                    [8.664, 49.419],
                    [8.670, 49.419],
                    [8.670, 49.410],
                    [8.664, 49.410],
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
def operator(test_database_url):
    operator = Operator(ca_database_url=test_database_url)
    yield operator


# Configure test database fixtures
if os.getenv('CI', 'False').lower() == 'true':
    connection_params = dict(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        dbname='test_db',
    )
    db_test_schema = factories.postgresql_noproc(
        load=[Path(__file__).parent / 'resources/create_db_tables.sql'], **connection_params
    )
else:
    db_test_schema = factories.postgresql_proc(load=[Path(__file__).parent / 'resources/create_db_tables.sql'])
db_test_engine = factories.postgresql('db_test_schema')


@pytest.fixture
def test_database_url(db_test_engine):
    return f'postgresql+psycopg2://{db_test_engine.info.user}:{db_test_engine.info.password}@{db_test_engine.info.host}:{db_test_engine.info.port}/{db_test_engine.info.dbname}'
