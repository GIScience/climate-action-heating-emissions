import logging
import os

import geopandas as gpd
import pandas as pd
import shapely
import xarray
from ecmwf.datastores import Client

from heating_emissions.components.temporal_downscale import demand_ninja
from heating_emissions.components.temporal_downscale.era5_data import get_era5_data_4_energy_estimation, open_era5_data
from heating_emissions.components.temporal_downscale.temporal_utils import (
    DEMAND_NINJA_THRESHOLD,
    VARIABLES_demand_ninja,
)

log = logging.getLogger(__name__)

pd.options.mode.copy_on_write = True


def estimate_hourly_energy_demand(weather_dataset: xarray.Dataset) -> pd.DataFrame:
    """
    Estimate temporal heating energy demand using DemandNinja: https://doi.org/10.1038/s41560-023-01341-5

    return:
        ds_w_hourly_demand: building-level energy deman
            energy demand unit: should be kWh based on DemandNinja's paper & website (https://www.renewables.ninja/)
                                where the unit of heating power threshold is kW/Celsius.
    """
    # Convert xarray Dataset variable to pandas DataFrame for demand_ninja calculation.
    #   # whose `inputs` has to be a pandas.DataFrame with four columns,
    #   # humidity, radiation_global_horizontal, temperature, and wind_speed_2m
    weather_data = weather_dataset.to_dataframe().reset_index().reset_index()

    ds_w_hourly_demand = weather_data[['index', 'valid_time', 'latitude', 'longitude']].set_index('index')
    ds_w_hourly_demand['heating_demand'] = 0.0
    for grpi, (grp_idx, weather_grid) in enumerate(weather_data.groupby(by=['latitude', 'longitude'])):
        weather_grid = weather_grid.set_index('valid_time').sort_index()
        demand_ninja_input_grid = weather_grid[VARIABLES_demand_ninja.keys()]
        demand_ninja_input_grid.rename(columns=VARIABLES_demand_ninja, inplace=True)
        hourly_demand = demand_ninja.demand(demand_ninja_input_grid.copy(), raw=True, **DEMAND_NINJA_THRESHOLD)
        hourly_demand['index'] = weather_grid['index']
        hourly_demand = hourly_demand.reset_index().set_index('index')
        ds_w_hourly_demand.loc[hourly_demand.index, 'heating_demand'] = hourly_demand['heating_demand']

    return ds_w_hourly_demand


def collect_building_hourly_energy_demand_permonth(
    year: int,
    month: int,
    aoiname: str,
    savedir: str,
) -> pd.DataFrame:
    """Collect monthly energy demand results."""
    # Open & preprocess the downloaded ERA5 data
    era5_file = os.path.join(savedir, f'era5_data_{aoiname.lower()}_{year}_{month}.zip')
    dataset = open_era5_data(era5_file)

    # Estimate energy demand using DemandNinja
    ds_w_hourly_demand = estimate_hourly_energy_demand(dataset)  # valid_time, latitude, longitude, heating_demand

    return ds_w_hourly_demand


def calculate_hourly_emissions_permonth(
    hourly_demand_era5: pd.DataFrame,
    census_data: gpd.GeoDataFrame,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Calculate hourly emissions based on energy demand and emission factor.
    :param hourly_demand: DataFrame with columns ['valid_time', 'latitude', 'longitude', 'heating_demand']
    :param census_data: GeoDataFrame with columns
                            ['fid', 'raster_id_100m', 'x_mp_100m', 'y_mp_100m',
                             'population', 'average_sqm_per_person', 'heat_consumption', 'emission_factor']
    :return
        census_data: return census data with 'monthly_emissions' estimates
        emission_hourly_regional: return ['valid_time', 'regional_hourly_emissions']
    """
    census_data = census_data.reset_index()  # keep raster_id_100m as a column for later join

    # spatial join hourly demand with census data
    gdf_hourly_demand = gpd.GeoDataFrame(
        hourly_demand_era5,
        geometry=gpd.points_from_xy(hourly_demand_era5.longitude, hourly_demand_era5.latitude),
        crs='EPSG:4326',
    )

    ## convert to projected CRS for spatial join
    census_data = census_data.to_crs(census_data.estimate_utm_crs())
    gdf_hourly_demand = gdf_hourly_demand.to_crs(census_data.estimate_utm_crs())

    nearest = census_data.sjoin_nearest(
        gdf_hourly_demand.drop_duplicates(subset=['longitude', 'latitude'])[['longitude', 'latitude', 'geometry']],
        how='left',
    )
    census_data[['lon_era5', 'lat_era5']] = nearest[['longitude', 'latitude']]
    del nearest

    # calculate hourly emissions for each grid cell in census data
    census_data['monthly_emissions'] = 0.0
    census_monthly_emission = census_data[['raster_id_100m', 'monthly_emissions']].set_index('raster_id_100m')
    hourly_emission_regional = []
    for hr, hr_demand in gdf_hourly_demand.groupby('valid_time'):
        hr_demand = hr_demand[['latitude', 'longitude', 'heating_demand']]
        census_data_w_hourly_demand = pd.merge(
            census_data[['raster_id_100m', 'lon_era5', 'lat_era5', 'emission_factor', 'population', 'geometry']],
            hr_demand,
            left_on=['lat_era5', 'lon_era5'],
            right_on=['latitude', 'longitude'],
            how='left',
        )

        census_data_w_hourly_demand['hourly_emissions'] = (
            census_data_w_hourly_demand['heating_demand']
            * census_data_w_hourly_demand['population']
            * census_data_w_hourly_demand['emission_factor']
        )
        census_data_w_hourly_demand.set_index('raster_id_100m', inplace=True)

        census_monthly_emission['monthly_emissions'] += census_data_w_hourly_demand['hourly_emissions']
        hourly_emission_regional.append([hr, census_data_w_hourly_demand['hourly_emissions'].sum()])

    census_data = census_data.set_index('raster_id_100m').to_crs(epsg=4326)
    census_data['monthly_emissions'] = census_monthly_emission['monthly_emissions']

    emission_hourly_regional = pd.DataFrame(
        hourly_emission_regional, columns=['valid_time', 'regional_hourly_emissions']
    )

    return census_data, emission_hourly_regional


def calculate_time_downscale_emissions(
    cdsapi_client: Client,
    year: int,
    city_name: str,
    aoi: shapely.MultiPolygon,
    census_data: gpd.GeoDataFrame,
    savedir: str,
    estimate_months: list = [1, 12],
    runtime_limit: float = 28 * 60,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """Calculate daily emissions for a year based on hourly energy demand estimation.
    return:
        1. the emissions for the user specified year for map
        2. the daily emissions for plot
    """
    # download yearly era5 data
    get_era5_data_4_energy_estimation(cdsapi_client, year, city_name, aoi, savedir, estimate_months, runtime_limit)

    # data pre-processing: fillna in census data
    census_data['emission_factor'] = census_data['emission_factor'].fillna(census_data['emission_factor'].mean())

    # calculate the emissions for each month in a year
    region_hourly_emissions = []
    census_yearly_emission = census_data[['x_mp_100m', 'y_mp_100m']]
    census_yearly_emission['yearly_emissions'] = 0.0
    for month in range(estimate_months[0], estimate_months[1] + 1):
        log.info(f'Calculating emissions for month: {year}-{month} ...')
        hourly_demand = collect_building_hourly_energy_demand_permonth(year, month, city_name, savedir)
        census_monthly_emi, region_hourly_emi = calculate_hourly_emissions_permonth(hourly_demand, census_data)

        census_yearly_emission['yearly_emissions'] += census_monthly_emi['monthly_emissions']

        region_hourly_emissions.append(region_hourly_emi)

    # concat along rows
    region_hourly_emissions = pd.concat(region_hourly_emissions, axis=0, ignore_index=True)
    region_daily_emissions = (
        region_hourly_emissions.resample('D', on='valid_time')['regional_hourly_emissions']
        .sum()
        .rename('regional_daily_emissions')
        .reset_index()
    )

    return census_yearly_emission, region_daily_emissions
