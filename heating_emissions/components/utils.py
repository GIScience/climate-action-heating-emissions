import logging
from enum import StrEnum

import geopandas as gpd
from climatoology.base.aoi import AoiConstraintSets, AoiProperties, CoveredByGeomConstraint
from climatoology.base.exception import ClimatoologyUserError, InputValidationError
from climatoology.base.i18n import N_
from shapely import MultiPolygon

log = logging.getLogger(__name__)

# Define dictionary with emission factors
EMISSION_FACTORS_DIRECT = {  # in kg of CO2 per kWh of heating
    'gas': 0.20029,
    'heating_oil': 0.26739,
    'wood': 0.34,
    'biomass_biogas': 0.20029,
    'solar_geothermal_heat_pumps': 0.0,
    'electricity': 0.0,
    'coal': 0.33661,
    'district_heating': 0.0,
}

EMISSION_FACTORS_LIFE_CYCLE = {  # in kg of CO2eq per kWh of heating
    'gas': 0.232,
    'heating_oil': 0.318,
    'wood': 0.017,
    'biomass_biogas': 0.017,
    'solar_geothermal_heat_pumps': 0.130,
    'electricity': 0.417,
    'coal': 0.646,
    'district_heating': 0.154,
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
}

# Category orders for building ages and energy sources
BUILDING_AGES = {
    'pre_1919': N_('pre-1919'),
    '1919_1948': '1919-1948',
    '1949_1978': '1949-1978',
    '1979_1990': '1979-1990',
    '1991_2000': '1991-2000',
    '2001_2010': '2001-2010',
    '2011_2019': '2011-2019',
    'post_2020': N_('post-2020'),
    'unknown': N_('Unknown'),
}

ENERGY_SOURCES = {
    'wood': N_('Wood'),
    'coal': N_('Coal'),
    'heating_oil': N_('Heating oil'),
    'gas': N_('Gas'),
    'biomass_biogas': N_('Biomass / Biogas'),
    'solar_geothermal_heat_pumps': N_('Solar / Geothermal / Heat pumps'),
    'electricity': N_('Electricity'),
    'district_heating': N_('District heating'),
    'unknown': N_('Unknown'),
}


class Topics(StrEnum):
    DIRECT_EMISSIONS = N_('direct_emissions')
    LIFE_CYCLE_EMISSIONS = N_('life_cycle_emissions')
    PARAMETERS = N_('parameters')
    TEMPORAL = N_('temporally flexible simulation')


def calculate_heating_emissions(census_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    census_data['average_sqm_per_person'] = census_data['average_sqm_per_person'].fillna(
        census_data['average_sqm_per_person'].mean()
    )
    census_data['heat_consumption'] = census_data['heat_consumption'].fillna(census_data['heat_consumption'].mean())
    for mode in ['direct', 'life_cycle']:
        census_data[f'{mode}_emission_factor'] = census_data[mode].fillna(census_data[mode].mean())

        census_data[f'{mode}_heated_area'] = census_data['population'] * census_data['average_sqm_per_person']
        census_data[f'{mode}_co2_emissions'] = (
            census_data[f'{mode}_heated_area']
            * census_data['heat_consumption']
            * census_data[f'{mode}_emission_factor']
        ).round()  # result in kg of CO2 per year
        census_data[f'{mode}_co2_emissions_per_capita'] = (
            census_data['average_sqm_per_person']
            * census_data['heat_consumption']
            * census_data[f'{mode}_emission_factor']
        ).round()  # result in kg of CO2 per year

    return census_data


def postprocess_uncalculated_census_data(uncalculated_census_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    uncalculated_census_data[['dominant_age', 'dominant_energy']] = uncalculated_census_data[
        ['dominant_age', 'dominant_energy']
    ].fillna(N_('Unknown'))
    return uncalculated_census_data


def check_aoi(aoi: MultiPolygon, aoi_properties: AoiProperties, aoi_constraints: AoiConstraintSets) -> bool:
    if len(aoi_constraints) > 1:
        raise NotImplementedError('Only one tier of AOI Constraints is currently supported')

    constraints = aoi_constraints[0]

    valid = True
    for con in constraints:
        valid = valid and con.check(aoi_geometry=aoi, aoi_properties=aoi_properties)

        if not valid:
            log.error(f'{aoi=} failed constraint check: {con}')
            # We intentionally raise a ClimatoologyUserError for the CoveredByGeomConstraint because this error type
            # will not be cached. We don't want to cache this error because the HEAL data may spontaneously be expanded
            # to cover new regions, in which case we should immediately be able to run for those regions.
            if isinstance(con, CoveredByGeomConstraint):
                raise ClimatoologyUserError(
                    'The selected area is outside of the valid regions. '
                    'Please contact us to add new areas to this assessment tool.'
                )
            else:
                raise InputValidationError("The selected area doesn't meet the area constraint limits")

    return valid
