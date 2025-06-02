import logging
from itertools import product
from typing import Tuple

import geopandas as gpd
import matplotlib as mpl
import numpy as np
import pandas as pd
import xarray
from climatoology.base.artifact import RasterInfo
from pydantic_extra_types.color import Color
from rasterio import CRS
from rasterio._base import Affine
from rasterio.warp import reproject

log = logging.getLogger(__name__)

# Define dictionary with emission factors
EMISSION_FACTORS = {  # in kg of CO2 per kWh og heating
    'gas': 0.20029,
    'heating_oil': 0.26739,
    'wood': 0.34,
    'biomass_biogas': 0.20029,
    'solar_geothermal_heat_pumps': 0.0,
    'electricity': 0.0,
    'coal': 0.33661,
    'district_heating': 0.0,
    'unknown': 0.19534,
}

## Based on data from https://www.wohngebaeude.info/daten/#/heizen/bundesweit
HEAT_CONSUMPTION = {  # in kWh/m2
    'pre_1919': 134.6,
    '1919_1948': 134.6,
    '1949_1978': 135.7,
    '1979_1990': 126.2,
    '1991_2000': 93.3,
    '2001_2010': 78.5,
    '2011_2019': 74.1,
    'post_2020': 74.1,
    'unknown': 126.7,
}


def generate_colors(color_by: pd.Series, cmap_name: str, cap: float = 1.0) -> dict[int : tuple[int, int, int]]:
    norm = mpl.colors.Normalize(vmin=0, vmax=color_by.quantile(cap))
    cmap = mpl.colormaps[cmap_name]
    mapped_colors = {}
    for value in range(0, int(color_by.quantile(cap)) + 1):
        mapped_colors[value] = Color(mpl.colors.to_hex(cmap(norm(value)))).as_rgb_tuple()

    for value in range(int(color_by.quantile(cap)) + 1, int(color_by.max()) + 1):
        mapped_colors[value] = Color(mpl.colors.to_hex(cmap(norm(int(color_by.quantile(cap)) + 1)))).as_rgb_tuple()

    return mapped_colors


def get_aoi_area(aoi_as_geoseries: gpd.GeoSeries) -> float:
    reprojected_aoi_df = aoi_as_geoseries.to_crs(aoi_as_geoseries.estimate_utm_crs())
    area_km2 = round(reprojected_aoi_df.geometry.area.sum() / 1e6, 2)
    return area_km2


def calculate_heating_emissions(census_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    census_data['average_sqm_per_person'] = census_data['average_sqm_per_person'].fillna(
        census_data['average_sqm_per_person'].mean()
    )
    census_data['heat_consumption'] = census_data['heat_consumption'].fillna(census_data['heat_consumption'].mean())
    census_data['emission_factor'] = census_data['emission_factor'].fillna(census_data['emission_factor'].mean())

    census_data['heated_area'] = census_data['population'] * census_data['average_sqm_per_person']
    census_data['co2_emissions'] = (
        census_data['heated_area'] * census_data['heat_consumption'] * census_data['emission_factor']
    ).round()  # result in kg of CO2 per year
    census_data['co2_emissions_per_capita'] = (
        census_data['average_sqm_per_person'] * census_data['heat_consumption'] * census_data['emission_factor']
    ).round()  # result in kg of CO2 per year

    return census_data


def create_emissions_raster_data(  # dead: disable
    result: gpd.GeoDataFrame, cmap: str, output_emissions: str, cap: float = 1.0
) -> RasterInfo:
    grid_size = 100  # m as of EPSG:3035
    geom_in_3035 = result.geometry.to_crs(3035)
    result = result.assign(x_mp_100m=geom_in_3035.x.astype(int), y_mp_100m=geom_in_3035.y.astype(int))
    raster_df = result.set_index(['y_mp_100m', 'x_mp_100m'])
    raster_df = raster_df[[output_emissions]].round()

    # pad dataframe by missing grid cells
    all_x = [x for x in range(result['x_mp_100m'].min(), result['x_mp_100m'].max() + grid_size, grid_size)]
    all_y = [y for y in range(result['y_mp_100m'].min(), result['y_mp_100m'].max() + grid_size, grid_size)]
    missing_x = set(all_x).difference(set(result['x_mp_100m']))
    missing_y = set(all_y).difference(set(result['y_mp_100m']))
    missing_pairs = list(product(missing_y, missing_x))

    if len(missing_pairs) != 0:
        for index in missing_pairs:
            raster_df.loc[index, output_emissions] = 0
    elif len(missing_y) == 0:
        for x in missing_x:
            raster_df.loc[(all_y[0], x), output_emissions] = 0
    elif len(missing_x) == 0:
        for y in missing_y:
            raster_df.loc[(y, all_x[0]), output_emissions] = 0

    raster_df.sort_index(level=[1, 0], inplace=True)

    raster_data = raster_df[output_emissions].to_xarray()

    transform = Affine(
        grid_size,
        0.0,
        result['x_mp_100m'].min() - (grid_size / 2),
        0.0,
        grid_size,
        result['y_mp_100m'].min() - (grid_size / 2),
    )

    projected_raster_data, projected_transform = reproject_data_to_4326(raster_data, transform, CRS.from_epsg(3035))
    color_map = generate_colors(color_by=result[output_emissions], cmap_name=cmap, cap=cap)

    raster_info = RasterInfo(
        data=projected_raster_data.astype(np.uint16),
        crs=CRS.from_epsg(4326),
        transformation=projected_transform,
        colormap=color_map,
    )

    return raster_info


def reproject_data_to_4326(
    source_data: xarray.DataArray, source_transform: Affine, source_crs: CRS
) -> Tuple[
    np.ndarray,
    Affine,
]:
    destination = np.zeros(source_data.shape, np.int16)
    geographic_raster_data, geographic_transform = reproject(
        source=source_data.to_numpy(),
        destination=destination,
        src_transform=source_transform,
        src_crs=source_crs,
        dst_crs=CRS.from_epsg(4326),
    )
    log.debug(f'projected transform: {geographic_transform}')
    return geographic_raster_data, geographic_transform
