import geopandas as gpd
import numpy as np
import pandas as pd
from climatoology.base.artifact import RasterInfo
from shapely import box
from shapely.geometry import Point

from heating_emissions.components.utils import (
    calculate_heating_emissions,
    create_emissions_raster_data,
    generate_colors,
    get_aoi_area,
    postprocess_uncalculate_census_data,
)


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
    )

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

    expected_absolute = round(31 * ((80 + 75) / 2) * 65 * 0.2)

    assert result['co2_emissions'][0] == expected_absolute


def test_generate_colors():
    test_data = pd.Series(data=[1, 2, 4])

    expected_color_map = {0: (59, 76, 192), 1: (141, 176, 254), 2: (221, 220, 220), 3: (244, 152, 122), 4: (180, 4, 38)}

    resulting_color_map = generate_colors(test_data, cmap_name='coolwarm')

    assert isinstance(resulting_color_map[0], tuple)
    assert isinstance(resulting_color_map[3], tuple)
    assert isinstance(resulting_color_map[4], tuple)

    assert resulting_color_map == expected_color_map


def test_generate_colors_triggers_max_branch():
    color_by = pd.Series([1, 2, 10])
    expected_color_map = {
        0: (59, 76, 192),
        1: (111, 146, 243),
        2: (170, 199, 253),
        3: (221, 220, 220),
        4: (247, 184, 156),
        5: (231, 116, 91),
        6: (180, 4, 38),
        7: (180, 4, 38),
        8: (180, 4, 38),
        9: (180, 4, 38),
        10: (180, 4, 38),
    }
    resulting_color_map = generate_colors(color_by, cmap_name='coolwarm', cap=0.75)

    assert resulting_color_map == expected_color_map


def test_get_aoi_area():
    aoi = gpd.GeoSeries(box(0, 0, 1000, 1000), crs='EPSG:3857')
    area = get_aoi_area(aoi)
    assert area == 1.0


def test_postprocess_uncalculate_census_data():
    df = gpd.GeoDataFrame(
        {
            'dominant_age': [None, '1949-1978', None],
            'dominant_energy': [None, 'Gas', None],
            'geometry': [None, None, None],
        }
    )
    result = postprocess_uncalculate_census_data(df)
    assert all(result['dominant_age'] == ['Unknown', '1949-1978', 'Unknown'])
    assert all(result['dominant_energy'] == ['Unknown', 'Gas', 'Unknown'])


def test_create_emissions_raster_data():
    # Create a minimal GeoDataFrame with two points and emissions
    df = gpd.GeoDataFrame(
        {'geometry': [Point(10, 50), Point(10.001, 50.001)], 'emissions': [100, 200]}, crs='EPSG:4326'
    )
    raster_info = create_emissions_raster_data(df, cmap='viridis', output_emissions='emissions', cap=1.0)
    assert isinstance(raster_info, RasterInfo)
    assert raster_info.data is not None
    assert raster_info.data.dtype == np.uint16
    assert raster_info.colormap is not None
    assert raster_info.crs.to_epsg() == 4326
