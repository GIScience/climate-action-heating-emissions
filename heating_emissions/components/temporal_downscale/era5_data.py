import asyncio
import glob
import logging.config
import os
import time
import zipfile

import numpy as np
import shapely
import xarray
from climatoology.utility.exception import ClimatoologyUserError
from ecmwf.datastores import Client, Remote

from heating_emissions.components.temporal_downscale.temporal_utils import VARIABLES_NAMES, era5_data_preprocess

log = logging.getLogger(__name__)


def open_era5_data(file_path: str) -> xarray.Dataset:
    """
    Open ERA5 data from a NetCDF file using xarray.
    """
    import xarray as xr

    log.debug(f'Loading ERA5 data from {file_path}...')
    with zipfile.ZipFile(file_path) as zip_ds:
        zip_ds.extractall(os.path.join(file_path.split('.zip')[0]))
        extracted_files = glob.glob(os.path.join(file_path.split('.zip')[0], '*.nc'))

    dataset = [xr.open_dataset(extracted_file) for extracted_file in extracted_files]
    dataset = xr.merge(dataset, compat='no_conflicts')

    dataset = era5_data_preprocess(dataset)

    log.debug('ERA5 data loaded.')

    return dataset


# async def download_era5_data(
def submit_era5_request(
    cdsapi_client: Client, year: int, month: int, variables: list[str], area: list, output_file: str
) -> Remote:
    """
    Download ERA5 data for a specific year, month, and variable over a defined area.
    https://cds.climate.copernicus.eu/how-to-api
    """
    log.debug(f'Starting ERA5 data download for {year}-{month:02d}...')

    request = {
        'product_type': ['reanalysis'],
        'data_format': 'netcdf',  # netCDF is convenient for xarray
        'download_format': 'zip',  # always download as zip, as the required variables might be from multi files.
        'variable': variables,
        'year': [year],
        'month': [month],
        'day': [
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '20',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
        ],
        'time': [
            '00:00',
            '01:00',
            '02:00',
            '03:00',
            '04:00',
            '05:00',
            '06:00',
            '07:00',
            '08:00',
            '09:00',
            '10:00',
            '11:00',
            '12:00',
            '13:00',
            '14:00',
            '15:00',
            '16:00',
            '17:00',
            '18:00',
            '19:00',
            '20:00',
            '21:00',
            '22:00',
            '23:00',
        ],
        'area': area,  # area = [North, West, South, East]  - replace with your bbox or remove for global
    }

    remote = cdsapi_client.submit('reanalysis-era5-single-levels', request)
    return remote


async def async_download_era5_data(remote: Remote, target: str, time_timeout: float):
    is_result_ready = False
    while (time_timeout - time.time() > 0) and (not is_result_ready):
        is_result_ready = await asyncio.to_thread(lambda: remote.results_ready)
        if is_result_ready:
            await asyncio.to_thread(remote.download, target)

        await asyncio.sleep(1)

    if not os.path.exists(target):
        raise asyncio.TimeoutError(f'download {target} timed out.')


async def async_get_yearly_era5_data(
    cdsapi_client: Client,
    year: int,
    aoiname: str,
    area: list,
    savedir: str,
    estimate_months: list,
    time_timeout: float,
):
    tasks = []

    for month in range(estimate_months[0], estimate_months[1] + 1):
        output_file = os.path.join(savedir, f'era5_data_{aoiname.lower()}_{year}_{month}.zip')
        if os.path.exists(output_file):  # if already downloaded, skip download and directly return file path
            log.debug(f'{output_file} already exists, skipping.')
            continue
        else:
            log.debug(f"{output_file} doesn't exist, downloading...")
            remote_request = submit_era5_request(
                cdsapi_client, year, month, list(VARIABLES_NAMES.keys()), area, output_file
            )
            tasks.append(asyncio.create_task(async_download_era5_data(remote_request, output_file, time_timeout)))

    log.debug('all tasks submitted.')

    return await asyncio.gather(*tasks)


def get_era5_data_4_energy_estimation(
    cdsapi_client: Client,
    year: int,
    aoiname: str,
    aoi: shapely.MultiPolygon,
    savedir: str,
    estimate_months: list = [1, 12],
    runtime_limit: float = 20 * 60,  # seconds
):
    # Define output directory
    os.makedirs(savedir, exist_ok=True)

    # Define area from AOI bounding box
    minx, miny, maxx, maxy = aoi.buffer(0.000001).bounds  # do a small buffer to avoid issues with degenerate boxes
    area = [maxy, minx, miny, maxx]  # North, West, South, East

    ###############
    # Download ERA5 Data
    ###############
    log.debug('downloading era5 data...')
    max_num_month = 4
    # if the request monthes too many, split it into several sub-tasks to avoid depriority
    # and raise error when out time limitation
    sub_estimate_months = np.arange(estimate_months[0], estimate_months[1], max_num_month)
    sub_estimate_months = np.hstack([sub_estimate_months, estimate_months[1] + 1])
    sub_estimate_months = np.vstack([sub_estimate_months[:-1], sub_estimate_months[1:] - 1]).astype('int').T
    time_timeout = time.time() + runtime_limit
    try:
        for sub_estimate_month in sub_estimate_months:
            log.debug(f'Downloading data in {sub_estimate_month} months...')
            asyncio.run(
                async_get_yearly_era5_data(
                    cdsapi_client,
                    year,
                    aoiname,
                    area,
                    savedir,
                    estimate_months=sub_estimate_month,
                    time_timeout=time_timeout,
                )
            )
    except asyncio.TimeoutError:
        raise ClimatoologyUserError(
            f'Era5 data download exceeded the time limit of {runtime_limit / 60:.2f} minutes. Temporal flexible simulation will not be computed.'
        )
    except Exception as e:
        raise ClimatoologyUserError(f'Era5 data download failed by the following exception:\n{e}')
