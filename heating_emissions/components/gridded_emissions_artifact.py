from climatoology.base.artifact import (
    ContinuousLegendData,
    RasterInfo,
    _Artifact,
    create_geotiff_artifact,
    create_plotly_chart_artifact,
)
from climatoology.base.computation import ComputationResources
import geopandas as gpd
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from rasterio import Affine, CRS
import logging
from itertools import product


from heating_emissions.components.utils import generate_colors, reproject_data_to_4326

log = logging.getLogger(__name__)


def build_emissions_artifact(
    result: gpd.GeoDataFrame, resources: ComputationResources, per_capita: bool = True
) -> _Artifact:
    output_emissions = 'co2_emissions_per_capita'
    file_name = 'heating_emissions_per_capita'
    emission_type = 'Per capita'
    if not per_capita:
        output_emissions = 'co2_emissions'
        file_name = 'heating_emissions_absolute'
        emission_type = 'Absolute'
    cmap = 'YlOrRd'
    cap = 0.95
    raster_info = create_emissions_raster_data(result, cmap=cmap, output_emissions=output_emissions, cap=cap)

    emissions_max = int(result[output_emissions].quantile(cap).round())

    labels = ContinuousLegendData(cmap_name=cmap, ticks={f'> {emissions_max}0 kg of CO2': 1, '0 kg of CO2': 0})

    return create_geotiff_artifact(
        raster_info=raster_info,
        layer_name=f'{emission_type} heating emissions',
        caption=f'{emission_type} heating carbon dioxide emissions per 100-m grid cell',
        description='Territorial (scope 1) carbon dioxide emissions from residential space heating. Based on data from 2022 German census.',
        legend_data=labels,
        primary=per_capita,
        resources=resources,
        filename=file_name,
    )


def calculate_heating_emissions(census_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    census_data['average_sqm_per_person'] = census_data['average_sqm_per_person'].fillna(
        census_data['average_sqm_per_person'].mean()
    )
    census_data['heat_consumption'] = census_data['heat_consumption'].fillna(census_data['heat_consumption'].mean())
    census_data['emission_factor'] = census_data['emission_factor'].fillna(census_data['emission_factor'].mean())

    census_data['heated_area'] = census_data['population'] * census_data['average_sqm_per_person']
    census_data['co2_emissions'] = (
        census_data['heated_area'] * census_data['heat_consumption'] * census_data['emission_factor'] / 10
    )  # result in 10s of kg
    census_data['co2_emissions_per_capita'] = (
        census_data['average_sqm_per_person'] * census_data['heat_consumption'] * census_data['emission_factor'] / 10
    )  # result in 10s of kg

    return census_data


def create_emissions_raster_data(
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


def build_per_capita_co2_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> _Artifact:
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        title='Histogram per capita emissions',
        caption=f'Average carbon dioxide emissions from heating residential buildings '
        f'are {round(np.mean(aoi_aggregate["data"][0].x), 2)} tonnes per person per year, '
        f'but range from {round(np.min(aoi_aggregate["data"][0].x), 2)} to '
        f' {round(np.max(aoi_aggregate["data"][0].x), 2)} tonnes.',
        resources=resources,
        filename='aoi_C02pc_histogram',
        primary=True,
    )


def build_energy_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> _Artifact:
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        title='Histogram energy consumption',
        caption=f'Average heating energy consumption in residential buildings '
        f'is {round(np.mean(aoi_aggregate["data"][0].x), 2)} kWh per square meter per year, '
        f'but range from {round(np.min(aoi_aggregate["data"][0].x), 2)} to '
        f' {round(np.max(aoi_aggregate["data"][0].x), 2)} .',
        resources=resources,
        filename='aoi_energy_histogram',
        primary=False,
    )


def build_emission_factor_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> _Artifact:
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        title='Histogram emission factor',
        caption=f'Average emission factor from heating residential buildings '
        f'is {round(np.mean(aoi_aggregate["data"][0].x), 2)} kg of carbon dioxide per kWh, '
        f'but range from {round(np.min(aoi_aggregate["data"][0].x), 2)} to '
        f' {round(np.max(aoi_aggregate["data"][0].x), 2)}.',
        resources=resources,
        filename='aoi_ef_histogram',
        primary=False,
    )


def plot_per_capita_co2_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    census_data['co2_emissions_per_capita'] = (
        census_data['average_sqm_per_person']
        * census_data['heat_consumption']
        * census_data['emission_factor']
        / 1e3  # result in tonnes
    )
    hist_plot = Figure(
        data=go.Histogram(
            x=census_data['co2_emissions_per_capita'],
            hovertemplate='%{y:.1f} % of cells emit %{x} tonnes of carbon'
            ' dioxide per person per year <extra></extra>',
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text='Per capita carbon dioxide emissions from residential heating',
                subtitle=dict(text='% of 100-m grid cells in area of interest', font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text='annual tonnes of carbon dioxide per person')),
        ),
    )
    return hist_plot


def plot_energy_consumption_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=census_data['heat_consumption'],
            hovertemplate='Buildings in %{y:.1f} % of cells consume %{x} kWh of heating energy'
            ' per square meter per year <extra></extra>',
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text='Average heating energy consumption rate in residential buildings',
                subtitle=dict(text='% of 100-m grid cells in area of interest', font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text='kWh per square meter per year')),
        ),
    )
    return hist_plot


def plot_emission_factor_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=census_data['emission_factor'],
            hovertemplate='Buildings in %{y:.1f} % of cells emit %{x} kg of carbon dioxide'
            ' per kWh of heating energy used <extra></extra>',
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text='Average emission factor from heating in residential buildings',
                subtitle=dict(text='% of 100-m grid cells in area of interest', font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text='kg of carbon dioxide per kWh of heating')),
        ),
    )
    return hist_plot
