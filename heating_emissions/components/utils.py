import logging
from enum import StrEnum

import geopandas as gpd

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

# Category orders for building ages and energy sources
BUILDING_AGES = {
    'pre_1919': 'pre-1919',
    '1919_1948': '1919-1948',
    '1949_1978': '1949-1978',
    '1979_1990': '1979-1990',
    '1991_2000': '1991-2000',
    '2001_2010': '2001-2010',
    '2011_2019': '2011-2019',
    'post_2020': 'post-2020',
    'unknown': 'Unknown',
}

ENERGY_SOURCES = {
    'wood': 'Wood',
    'coal': 'Coal',
    'heating_oil': 'Heating oil',
    'gas': 'Gas',
    'biomass_biogas': 'Biomass / Biogas',
    'solar_geothermal_heat_pumps': 'Solar / Geothermal / Heat pumps',
    'electricity': 'Electricity',
    'district_heating': 'District heating',
    'unknown': 'Unknown',
}


class Topics(StrEnum):
    EMISSIONS = 'emissions'
    PARAMETERS = 'parameters'


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


def postprocess_uncalculate_census_data(uncalculated_census_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    uncalculated_census_data[['dominant_age', 'dominant_energy']] = uncalculated_census_data[
        ['dominant_age', 'dominant_energy']
    ].fillna('Unknown')
    return uncalculated_census_data
