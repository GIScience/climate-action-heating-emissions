import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from climatoology.base.aoi import AreaConstraint
from climatoology.base.exception import ClimatoologyUserError, InputValidationError
from shapely import MultiPolygon

from heating_emissions.components.utils import (
    calculate_heating_emissions,
    check_aoi,
    postprocess_uncalculated_census_data,
)


def test_calculate_heating_emissions():
    example_dataframe = pd.DataFrame(
        {
            'population': [31],
            'average_sqm_per_person': [40],
            'heat_consumption': [65],
            'direct': [0.2],
            'life_cycle': [0.4],
            'latitude': [45.15],
            'longitude': [5.15],
        }
    )

    example_geo_dataframe = gpd.GeoDataFrame(
        example_dataframe,
        geometry=gpd.points_from_xy(example_dataframe.longitude, example_dataframe.latitude),
        crs='EPSG:4326',
    )

    result = calculate_heating_emissions(census_data=example_geo_dataframe)

    expected_per_capita_direct = (
        example_dataframe['average_sqm_per_person']
        * example_dataframe['heat_consumption']
        * example_dataframe['direct']
    )

    expected_absolute_direct = expected_per_capita_direct * example_dataframe['population']

    expected_per_capita_life_cycle = (
        example_dataframe['average_sqm_per_person']
        * example_dataframe['heat_consumption']
        * example_dataframe['life_cycle']
    )

    expected_absolute_life_cycle = expected_per_capita_life_cycle * example_dataframe['population']

    assert result['direct_co2_emissions'][0] == expected_absolute_direct[0]
    assert result['direct_co2_emissions_per_capita'][0] == expected_per_capita_direct[0]
    assert result['life_cycle_co2_emissions'][0] == expected_absolute_life_cycle[0]
    assert result['life_cycle_co2_emissions_per_capita'][0] == expected_per_capita_life_cycle[0]


def test_calculate_heating_emissions_missing_data():
    example_dataframe = pd.DataFrame(
        {
            'population': [31, 85, 15],
            'average_sqm_per_person': [np.nan, 80, 75],
            'heat_consumption': [65, 125.3, 145.2],
            'direct': [0.2, 0.15, 0.3],
            'life_cycle': [0.4, 0.15, 0.3],
            'latitude': [45.15, 45.16, 45.15],
            'longitude': [5.15, 5.16, 5.16],
        }
    )

    example_geo_dataframe = gpd.GeoDataFrame(
        example_dataframe,
        geometry=gpd.points_from_xy(example_dataframe.longitude, example_dataframe.latitude),
        crs='EPSG:4326',
    )

    result = calculate_heating_emissions(census_data=example_geo_dataframe)

    expected_absolute_direct = round(31 * ((80 + 75) / 2) * 65 * 0.2)
    expected_absolute_life_cycle = round(31 * ((80 + 75) / 2) * 65 * 0.4)

    assert result['direct_co2_emissions'][0] == expected_absolute_direct
    assert result['life_cycle_co2_emissions'][0] == expected_absolute_life_cycle


def test_postprocess_uncalculate_census_data():
    df = gpd.GeoDataFrame(
        {
            'dominant_age': [None, '1949-1978', None],
            'dominant_energy': [None, 'Gas', None],
            'geometry': [None, None, None],
        }
    )
    result = postprocess_uncalculated_census_data(df)
    assert all(result['dominant_age'] == ['Unknown', '1949-1978', 'Unknown'])
    assert all(result['dominant_energy'] == ['Unknown', 'Gas', 'Unknown'])


def test_check_aoi_valid(operator, default_german_aoi, default_aoi_properties):
    aoi_constraints = operator.info().aoi_constraints

    assert check_aoi(aoi=default_german_aoi, aoi_properties=default_aoi_properties, aoi_constraints=aoi_constraints)


def test_check_aoi_invalid_geom(operator, default_aoi_properties):
    aoi_constraints = operator.info().aoi_constraints

    aoi_outside_supported_regions = MultiPolygon(
        polygons=[
            [
                [
                    [6.0, 49.0],
                    [6.0, 49.1],
                    [6.1, 49.1],
                    [6.1, 49.0],
                    [6.0, 49.0],
                ]
            ]
        ]
    )

    with pytest.raises(ClimatoologyUserError, match=r'The selected area is outside of the valid regions'):
        check_aoi(
            aoi=aoi_outside_supported_regions, aoi_properties=default_aoi_properties, aoi_constraints=aoi_constraints
        )


def test_check_aoi_invalid_area_size(default_german_aoi, default_aoi_properties):
    aoi_constraints = [[AreaConstraint(max_area=0.4)]]

    with pytest.raises(InputValidationError, match=r"The selected area doesn't meet the area constraint limits"):
        check_aoi(aoi=default_german_aoi, aoi_properties=default_aoi_properties, aoi_constraints=aoi_constraints)
