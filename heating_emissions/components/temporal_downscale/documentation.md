### Weather data
(This data and its related function are not available to the public yet limited by slow computation speed, but will be in the future after optimization)

We use [ERA5 reanalysis weather data](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) for the heating demand simulation by `demand_ninja` model.
The weather data-based heating demand estimates are further used for the daily emission estimation.

- 2m_temperature
- specific humidity calculated by *2m_dewpoint_temperature* and *surface_pressure* ([reference: 7.2.1(b)](https://www.ecmwf.int/en/elibrary/81626-ifs-documentation-cy49r1-part-iv-physical-processes))
- wind speed calculated by *10m_u_component_of_wind* and *10m_v_component_of_wind*
- surface_solar_radiation_downwards