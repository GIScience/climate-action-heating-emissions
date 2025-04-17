import pandas as pd
import geopandas as gpd
import numpy as np
from heating_emissions.components.gridded_emissions_artifact import calculate_heating_emissions


def test_calculate_heating_emissions():
    example_dataframe = pd.DataFrame(
        {
            'population': [31],
            'average_sqm_per_person': [40],
            'heat_consumption': [65],
            'emission_factor': [0.2],
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

    expected_per_capita = (
        example_dataframe['average_sqm_per_person']
        * example_dataframe['heat_consumption']
        * example_dataframe['emission_factor']
    ) / 10

    expected_absolute = expected_per_capita * example_dataframe['population']

    assert result['co2_emissions'][0] == expected_absolute[0]
    assert result['co2_emissions_per_capita'][0] == expected_per_capita[0]


def test_calculate_heating_emissions_missing_data():
    example_dataframe = pd.DataFrame(
        {
            'population': [31, 85, 15],
            'average_sqm_per_person': [np.nan, 80, 75],
            'heat_consumption': [65, 125.3, 145.2],
            'emission_factor': [0.2, 0.15, 0.3],
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

    expected_absolute = (31 * ((80 + 75) / 2) * 65 * 0.2) / 10

    assert result['co2_emissions'][0] == expected_absolute
