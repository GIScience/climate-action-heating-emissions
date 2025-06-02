import geopandas as gpd
import numpy as np
import plotly.graph_objects as go
from climatoology.base.artifact import _Artifact, create_plotly_chart_artifact
from climatoology.base.computation import ComputationResources
from plotly.graph_objs import Figure


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
    hist_plot = Figure(
        data=go.Histogram(
            x=census_data['co2_emissions_per_capita'] / 1e3,  # result in tonnes,
            hovertemplate='%{y:.1f} % of cells emit %{x} tonnes of carbon dioxide per person per year <extra></extra>',
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
    hist_plot.add_vline(
        x=2.2,
        line_width=1.5,
        line_dash='dot',
        annotation_text='German average',
        annotation_position='top left',
        annotation_textangle=-90,
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
    hist_plot.add_vline(
        x=127.1,
        line_width=1.5,
        line_dash='dot',
        annotation_text='German average',
        annotation_position='top left',
        annotation_textangle=-90,
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
