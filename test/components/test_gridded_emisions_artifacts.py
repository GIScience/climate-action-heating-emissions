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
        (True, 'direct_co2_emissions', 'Per capita direct CO₂ emissions (kg/year)'),
        (False, 'direct_co2_emissions', 'Absolute direct CO₂ emissions (kg/year)'),
        (True, 'life_cycle_co2_emissions', 'Per capita life cycle GHG emissions (kg CO₂eq/year)'),
        (False, 'life_cycle_co2_emissions', 'Absolute life cycle GHG emissions (kg CO₂eq/year)'),
        (True, 'heat_consumption', 'Energy consumption (kWh/m²/year)'),
        (True, 'average_sqm_per_person', 'Living space (m² per person)'),
        (True, 'direct_emission_factor', 'Direct emission factor (kg of CO₂ per kWh)'),
        (True, 'life_cycle_emission_factor', 'Life cycle emission factor (kg of CO₂eq per kWh)'),
    ],
)
def test_build_gridded_artifact(per_capita, output, expected_name, compute_resources):
    test_df = gpd.GeoDataFrame(
        {
            'x_mp_100m': [4500000, 4500100, 4500200],
            'y_mp_100m': [3500000, 3500100, 3500200],
            'direct_co2_emissions_per_capita': [100.0, 200.0, 250.0],
            'life_cycle_co2_emissions_per_capita': [300.0, 400.0, 450.0],
            'direct_co2_emissions': [1000.0, 2000.0, 2500.0],
            'life_cycle_co2_emissions': [2000.0, 4000.0, 5500.0],
            'heat_consumption': [80.0, 90.0, 100.0],
            'average_sqm_per_person': [20.0, 30.0, 40.0],
            'direct_emission_factor': [0.1, 0.2, 0.25],
            'life_cycle_emission_factor': [0.4, 0.2, 0.25],
        }
    )

    artifact = build_gridded_artifact(test_df, compute_resources, output=output, per_capita=per_capita)
    assert artifact.name == expected_name
    assert artifact.modality == ArtifactModality.VECTOR_MAP_LAYER


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
    assert artifact.modality == ArtifactModality.VECTOR_MAP_LAYER
