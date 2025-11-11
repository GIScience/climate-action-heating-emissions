import numpy as np
import xarray

VARIABLES_NAMES = {
    '2m_temperature': 't2m',  # unit: K(elvin)
    '2m_dewpoint_temperature': 'd2m',  # unit: K(elvin)
    'surface_pressure': 'sp',  # unit: Pa (Pascal)
    '10m_u_component_of_wind': 'u10',  # unit: m/s
    '10m_v_component_of_wind': 'v10',  # unit: m/s
    'surface_solar_radiation_downwards': 'ssrd',  # ssrd (J m-2 accumulation)
}

VARIABLES_demand_ninja = {
    'q2m': 'humidity',
    'ssrd': 'radiation_global_horizontal',
    't2m': 'temperature',
    'wind2m': 'wind_speed_2m',
}

# source: Supplementary Table 4
# https://static-content.springer.com/esm/art%3A10.1038%2Fs41560-023-01341-5/MediaObjects/41560_2023_1341_MOESM1_ESM.pdf
DEMAND_NINJA_THRESHOLD = {
    'heating_threshold': 15,  # 14.7, # Celsius degree # might be 15 in Germany based on https://proceedings.ises.org/citation?doi=swc.2023.06.05&mode=list
    'heating_power': 107 / 1000,  # mean + 0.5 std (monthly gas in EU), # kW per Celsius degree per capita
    'smoothing': 0.42,  # 0.62 (daily electricity, avg EU), 0.42 (daily gas, avg UK).
    'solar_gains': 0.019,  # daily electricity in EU
    'wind_chill': -0.13,  # daily electricity in EU
    'humidity_discomfort': 0.032,  # daily electricity in EU
}


def calc_2m_specific_humidity(dew_temp_2m: np.ndarray, surf_pressure: np.ndarray) -> np.ndarray:
    """
    Calculate 2m specific humidity from dew point temperature and surface pressure.
    reference:
        1. ECMWF forum: https://forum.ecmwf.int/t/how-to-calculate-hus-at-2m-huss/1254
        2. ECMWF IFS doc (chapter 7, section 7.2.1(b) - Saturation specific humidity):
            https://www.ecmwf.int/en/elibrary/81626-ifs-documentation-cy49r1-part-iv-physical-processes

    Parameters:
    dew_temp_2m (np.ndarray): Dew point temperature at 2 meters in Kelvin.
    surf_pressure (np.ndarray): Surface pressure in Pascals.

    Returns:
    np.ndarray: Specific humidity at 2 meters (dimensionless, kg/kg).
    """
    # Constants from Buck (1981) for saturation over water, to calculate saturation vapour pressure
    a1 = 611.21  # in Pa
    a3 = 17.502
    a4 = 32.19  # in Kelvin
    t0 = 273.16  # in Kelvin
    # Constants to calculate specific humidity
    eps = 0.621981  # Rdry /Rvap,  the ratio of the molar masses of water and dry air

    # Calculate saturation water vapour pressure by Teten's formula (in Pa)
    e_s = a1 * np.exp((a3 * (dew_temp_2m - t0)) / (dew_temp_2m - a4))

    # Calculate specific humidity (dimensionless, kg/kg)
    q_2m = (eps * e_s) / (surf_pressure - (1 - eps) * e_s)

    return q_2m


def era5_data_preprocess(dataset: xarray.Dataset) -> xarray.Dataset:
    # 1. preprocess ssrd - surface_solar_radiation_downwards
    dataset['ssrd'] = dataset['ssrd'] / 3600.0  # Convert from J/m2 to W/m2

    # 2. preprocess d2m & sp - calculate specific humidity at 2m
    q2m = calc_2m_specific_humidity(dataset['d2m'], dataset['sp'])
    q2m.name = 'q2m'
    dataset = dataset.assign(q2m=q2m)
    # drop dew point temperature and surface pressure after calculating specific humidity
    dataset = dataset.drop_vars(['d2m', 'sp'])

    # 3. preprocess u10 & v10 - calculate wind speed at 10m, but rename it to wind at 2m for demand ninja
    wind_speed_2m = np.sqrt(dataset['u10'] ** 2 + dataset['v10'] ** 2)
    wind_speed_2m.name = 'wind2m'
    dataset = dataset.assign(wind2m=wind_speed_2m)
    # drop u10 and v10 after calculating wind speed
    dataset = dataset.drop_vars(['u10', 'v10'])

    # 4. align units used in demand ninja
    ## t2m: from K to Celsius
    ## q2m: from kg/kg to g/kg
    ## wind2m: already in m/s
    ## ssrd: already in W/m2
    dataset['t2m'] = dataset['t2m'] - 273.15  # Convert from Kelvin to Celsius
    dataset['q2m'] = dataset['q2m'] * 1000.0  # Convert from kg/kg to g/kg

    # global setting: set CRS (4326) and geolocation info
    dataset.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude', inplace=True)
    dataset.rio.write_crs('epsg:4326', inplace=True)

    return dataset
