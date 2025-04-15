from typing import Tuple
import matplotlib as mpl
import numpy as np
import pandas as pd
from rasterio import CRS, Affine
from rasterio.warp import reproject
import xarray
from pydantic_extra_types.color import Color
import logging

log = logging.getLogger(__name__)

# Define dictionary with emission factors
EMISSION_FACTORS = {
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
