import uuid

from climatoology.base.baseoperator import AoiProperties
from climatoology.base.computation import ComputationScope
import pytest
import shapely

from plugin_blueprint.core.operator_worker import Operator
from plugin_blueprint.core.input import ComputeInput


@pytest.fixture
def default_compute_input() -> ComputeInput:
    return ComputeInput()


@pytest.fixture
def default_aoi() -> shapely.MultiPolygon:
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
def default_aoi_properties() -> AoiProperties:
    return AoiProperties(name='Heidelberg', id='heidelberg')


# The following fixtures can be ignored on plugin setup
@pytest.fixture
def compute_resources():
    with ComputationScope(uuid.uuid4()) as resources:
        yield resources


@pytest.fixture
def operator():
    return Operator()
