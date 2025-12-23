import logging
from dataclasses import dataclass

import geopandas as gpd
import pandas as pd
import shapely
from climatoology.base.exception import ClimatoologyUserError
from geoalchemy2 import WKTElement
from sqlalchemy import Engine, MetaData, select

from heating_emissions.components.utils import (
    BUILDING_AGES,
    EMISSION_FACTORS,
    ENERGY_SOURCES,
    HEAT_CONSUMPTION,
    postprocess_uncalculate_census_data,
)

log = logging.getLogger(__name__)


@dataclass
class DatabaseConnection:
    engine: Engine
    metadata: MetaData


def collect_census_data(
    db_connection: DatabaseConnection, aoi: shapely.MultiPolygon
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Read all required census data and return it as a single geodataframe."""
    raster_grid = get_clipped_census_grid(db_connection=db_connection, aoi=aoi)
    census_data, uncalculated_census_data = get_census_tables_from_db(db_connection, raster_grid)
    uncalculated_census_data = postprocess_uncalculate_census_data(uncalculated_census_data)
    return census_data, uncalculated_census_data


def get_clipped_census_grid(db_connection: DatabaseConnection, aoi: shapely.MultiPolygon) -> gpd.GeoDataFrame:
    """Query the census grid cells within the AOI from the database."""
    log.info('Querying database for census grid points within the AOI')

    db_table = db_connection.metadata.tables['census_de.raster_grid_100m']
    aoi_geom = WKTElement(aoi.wkt, srid=4326)
    query = select(db_table).where(db_table.c.geometry.op('&&')(aoi_geom) & db_table.c.geometry.ST_Within(aoi_geom))
    with db_connection.engine.connect() as conn:
        result = conn.execute(query).mappings().all()

    if not result:
        raise ClimatoologyUserError(
            'There are no data for residential buildings in the area you selected. Please select an area '
            'with residential buildings'
        )

    result_gdf = pd.DataFrame(result)
    result_gdf['geometry'] = gpd.GeoSeries.from_wkb(result_gdf['geometry'].astype(str))
    result_gdf = gpd.GeoDataFrame(result_gdf, crs='4326').set_index('raster_id_100m')

    log.debug(f'Found {len(result_gdf)} points within the AOI')
    return result_gdf


def get_census_tables_from_db(
    db_connection: DatabaseConnection, raster_grid: gpd.GeoDataFrame
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Query all other tables from the database for the grid points in `raster_grid`, clean them, and return a
    GeoDataFrame with all tables joined.
    Return:
        1. the census data after calculation, e.g., the heat_consumption is already calculated based on building ages.
        2. the census data before calculation, e.g., the dominant/original building ages information.
    """

    tables_and_cleaning_fns = {
        'census_de.population': clean_population_data,
        'census_de.residential_living_space': clean_living_space_data,
        'census_de.residential_buildings_by_year': clean_building_age_data,
        'census_de.residential_heating_sources': clean_energy_source_data,
    }

    census_data = []
    uncalculated_census_data = []
    for table, cleaning_fn in tables_and_cleaning_fns.items():
        log.debug(f'Querying database table {table}')
        result = query_table_from_db(db_connection, raster_grid.index, table)
        result, uncalculated_data = cleaning_fn(result)
        census_data.append(result)

        if uncalculated_data is not None:
            uncalculated_census_data.append(uncalculated_data)
        else:
            uncalculated_census_data.append(result)

    return raster_grid.join(census_data), raster_grid.join(uncalculated_census_data)


def query_table_from_db(db_connection: DatabaseConnection, raster_ids: pd.Series, table: str) -> pd.DataFrame:
    db_table = db_connection.metadata.tables[table]
    query = select(db_table).where(db_table.c.raster_id_100m.in_(raster_ids))
    with db_connection.engine.connect() as conn:
        result = conn.execute(query).mappings().all()
    return pd.DataFrame(result).set_index('raster_id_100m')


def clean_population_data(census_data: pd.DataFrame) -> tuple[pd.DataFrame, None]:
    return census_data['population'].fillna(0), None


def clean_living_space_data(census_data: gpd.GeoDataFrame) -> tuple[pd.Series, None]:
    return census_data['average_sqm_per_person'].fillna(0), None


def clean_building_age_data(census_data: gpd.GeoDataFrame) -> tuple[pd.Series, pd.Series]:
    building_counts = census_data.fillna(0)

    building_ages_columns = list(BUILDING_AGES.keys())
    building_ages_columns.remove('unknown')
    log.debug(f'Current building age columns will be considered: {building_ages_columns}')
    building_ages = building_counts[building_ages_columns]

    building_counts['computed_total_buildings'] = building_ages.sum(axis='columns')

    building_counts['heat_consumption'] = 0.0
    for age, heat_consumption_factor in HEAT_CONSUMPTION.items():
        building_counts['heat_consumption'] = building_counts['heat_consumption'] + (
            heat_consumption_factor * (building_counts[age] / (building_counts['computed_total_buildings']))
        )

    # For grid cells with no building age data, assign average heating consumption in AOI
    building_counts['heat_consumption'] = building_counts['heat_consumption'].fillna(
        building_counts['heat_consumption'].mean()
    )

    building_counts['dominant_age'] = extract_dominant_characteristics(building_ages, 'dominant_age')

    return building_counts['heat_consumption'], building_counts['dominant_age']


def clean_energy_source_data(census_data: gpd.GeoDataFrame) -> tuple[pd.Series, pd.Series]:
    with pd.option_context('future.no_silent_downcasting', True):
        cropped_energy_data = census_data.fillna(0).infer_objects(copy=False)

    building_energy_columns = list(ENERGY_SOURCES.keys())
    building_energy_columns.remove('unknown')
    log.debug(f'Current building energy carrier columns will be considered: {building_energy_columns}')
    cropped_energy_data_energysource = cropped_energy_data[building_energy_columns]
    cropped_energy_data['computed_total_buildings'] = cropped_energy_data_energysource.sum(axis='columns')

    # Average emission factor in grid cell given heat mix (in kg of CO2 per kWh)
    cropped_energy_data['emission_factor'] = 0.0
    for fuel, emissions in EMISSION_FACTORS.items():
        cropped_energy_data['emission_factor'] = cropped_energy_data['emission_factor'] + (
            emissions * (cropped_energy_data[fuel] / (cropped_energy_data['computed_total_buildings']))
        )

    # For grid cells with no Energy Carrier data, assign average emission factor in AOI
    cropped_energy_data['emission_factor'] = cropped_energy_data['emission_factor'].fillna(
        cropped_energy_data['emission_factor'].mean()
    )

    cropped_energy_data['dominant_energy'] = extract_dominant_characteristics(
        cropped_energy_data_energysource, 'dominant_energy'
    )

    return cropped_energy_data['emission_factor'], cropped_energy_data['dominant_energy']


def extract_dominant_characteristics(census_dominant_data: gpd.GeoDataFrame, dominant_character: str) -> pd.Series:
    ## rename for label
    match dominant_character:
        case 'dominant_age':
            new_columns_names = BUILDING_AGES
        case 'dominant_energy':
            new_columns_names = ENERGY_SOURCES
        case _:
            raise ValueError(f'Unknown dominant_character: {dominant_character}')

    census_dominant_data = census_dominant_data.rename(columns=new_columns_names)
    census_dominant_data = census_dominant_data.replace({0: None}).idxmax(axis=1)
    census_dominant_data = census_dominant_data.fillna('Unknown')

    return census_dominant_data
