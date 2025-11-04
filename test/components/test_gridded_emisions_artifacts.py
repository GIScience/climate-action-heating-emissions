from pathlib import Path

import geopandas as gpd
import pytest
from climatoology.base.artifact import ArtifactModality

from heating_emissions.components.gridded_emissions_artifact import (
    build_gridded_artifact,
    build_gridded_artifact_classdata,
)

ROOT_DIR = Path(__file__).parent.parent.parent


@pytest.mark.parametrize(
    'per_capita,output,expected_name',
    [
        (True, 'co2', 'Per capita CO₂ emissions (kg/year)'),
        (False, 'co2', 'Absolute CO₂ emissions (kg/year)'),
        (True, 'heat_consumption', 'Energy consumption (kWh/m²/year)'),
        (True, 'average_sqm_per_person', 'Living space (m² per person)'),
        (True, 'emission_factor', 'Emission factor (kg of CO₂ per kWh)'),
    ],
)
def test_build_gridded_artifact(per_capita, output, expected_name, compute_resources):
    test_df = gpd.GeoDataFrame(
        {
            'x_mp_100m': [4500000, 4500100, 4500200],
            'y_mp_100m': [3500000, 3500100, 3500200],
            'co2_emissions_per_capita': [100.0, 200.0, 250.0],
            'co2_emissions': [1000.0, 2000.0, 2500.0],
            'heat_consumption': [80.0, 90.0, 100.0],
            'average_sqm_per_person': [20.0, 30.0, 40.0],
            'emission_factor': [0.1, 0.2, 0.25],
        }
    )

    artifact = build_gridded_artifact(test_df, compute_resources, output=output, per_capita=per_capita)
    assert artifact.name == expected_name
    assert artifact.modality == ArtifactModality.MAP_LAYER_GEOJSON


@pytest.mark.parametrize(
    'output,expected_name',
    [
        ('dominant_age', 'Dominant building construction year'),
        ('dominant_energy', 'Dominant building energy carrier'),
    ],
)
def test_build_gridded_artifact_classdata(compute_resources, output, expected_name):
    test_df = gpd.GeoDataFrame(
        {
            'x_mp_100m': [4500000, 4500100, 4500200],
            'y_mp_100m': [3500000, 3500100, 3500200],
            'dominant_age': ['1949-1978', '1979-1990', 'Unknown'],
            'dominant_energy': ['Gas', 'District heating', 'Unknown'],
        }
    )

    artifact = build_gridded_artifact_classdata(test_df, compute_resources, output=output)
    assert artifact.name == expected_name
    assert artifact.modality == ArtifactModality.MAP_LAYER_GEOJSON
