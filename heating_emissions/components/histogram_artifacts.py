import geopandas as gpd
import numpy as np
import plotly.graph_objects as go
from climatoology.base.artifact import Artifact, ArtifactMetadata
from climatoology.base.artifact_creators import create_plotly_chart_artifact
from climatoology.base.computation import ComputationResources
from climatoology.base.i18n import tr
from plotly.graph_objs import Figure

from heating_emissions.components.utils import Topics


def format_summary(summary: str, figure: Figure) -> str:
    return summary.format(
        mean_data=round(np.mean(figure['data'][0].x), 2),
        min_data=round(np.min(figure['data'][0].x), 2),
        max_data=round(np.max(figure['data'][0].x), 2),
    )


def build_per_capita_direct_co2_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> Artifact:
    summary = tr(
        'Average direct per capita CO₂ emissions from heating residential buildings (estimated) '
        'are {mean_data} tonnes per person per year, '
        'but range from {min_data} to '
        ' {max_data} tonnes.'
    )
    summary = format_summary(summary, aoi_aggregate)
    per_capita_direct_co2_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of per capita direct emissions'),
        summary=summary,
        filename='aoi_direct_C02pc_histogram',
        tags={tr(Topics.DIRECT_EMISSIONS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=per_capita_direct_co2_histogram_artifact_metadata,
        resources=resources,
    )


def build_per_capita_life_cycle_co2_histogram_artifact(
    aoi_aggregate: Figure, resources: ComputationResources
) -> Artifact:
    summary = tr(
        'Average life-cycle GHG per capita emissions from heating residential buildings (estimated) '
        'are {mean_data} tonnes of CO₂-eq. per person per year, '
        'but range from {min_data} to '
        ' {max_data} tonnes.'
    )
    summary = format_summary(summary, aoi_aggregate)
    per_capita_life_cycle_co2_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of per capita life-cycle emissions'),
        summary=summary,
        filename='aoi_life_cycle_C02pc_histogram',
        tags={tr(Topics.LIFE_CYCLE_EMISSIONS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=per_capita_life_cycle_co2_histogram_artifact_metadata,
        resources=resources,
    )


def build_energy_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> Artifact:
    summary = tr(
        'Average estimated heating energy consumption in residential buildings '
        'is {mean_data} kWh per square meter per year, '
        'but ranges from {min_data} to '
        ' {max_data} .'
    )
    summary = format_summary(summary, aoi_aggregate)
    energy_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of energy consumption'),
        summary=summary,
        filename='aoi_energy_histogram',
        tags={tr(Topics.PARAMETERS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=energy_histogram_artifact_metadata,
        resources=resources,
    )


def build_direct_emission_factor_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> Artifact:
    summary = tr(
        'The average estimated (direct) emission factor across grid cells '
        'is {mean_data} kg of carbon dioxide per kWh, '
        'but ranges from {min_data} to '
        ' {max_data}.'
    )
    summary = format_summary(summary, aoi_aggregate)
    direct_emission_factor_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of direct emission factor'),
        summary=summary,
        filename='aoi_direct_ef_histogram',
        tags={tr(Topics.PARAMETERS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=direct_emission_factor_histogram_artifact_metadata,
        resources=resources,
    )


def build_life_cycle_emission_factor_histogram_artifact(
    aoi_aggregate: Figure, resources: ComputationResources
) -> Artifact:
    summary = tr(
        'The average estimated (life-cycle) emission factor across grid cells '
        'is {mean_data} kg of carbon dioxide per kWh, '
        'but ranges from {min_data} to '
        ' {max_data}.'
    )
    summary = format_summary(summary, aoi_aggregate)
    life_cycle_emission_factor_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of life-cycle emission factor'),
        summary=summary,
        filename='aoi_life_cycle_ef_histogram',
        tags={tr(Topics.PARAMETERS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=life_cycle_emission_factor_histogram_artifact_metadata,
        resources=resources,
    )


def build_living_space_histogram_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> Artifact:
    summary = tr(
        'The average living space across all grid cells '
        'is {mean_data} square meters per person, '
        'but ranges from {min_data} to '
        ' {max_data}.'
    )
    summary = format_summary(summary, aoi_aggregate)
    living_space_histogram_artifact_metadata = ArtifactMetadata(
        name=tr('Histogram of living space per person'),
        summary=summary,
        filename='aoi_living_space_histogram',
        tags={tr(Topics.PARAMETERS)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=living_space_histogram_artifact_metadata,
        resources=resources,
    )


def plot_per_capita_direct_co2_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['direct_co2_emissions_per_capita'] / 1e3).round(2),  # result in tonnes,
            hovertemplate=tr(
                '%{y:.1f} % of cells emit %{x} tonnes of carbon dioxide per person per year <extra></extra>'
            ),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Per capita direct carbon dioxide emissions from residential heating (estimated)'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('annual tonnes of carbon dioxide per person'))),
        ),
    )
    hist_plot.add_vline(
        x=1.27,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot


def plot_per_capita_life_cycle_co2_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['life_cycle_co2_emissions_per_capita'] / 1e3).round(2),  # result in tonnes,
            hovertemplate=tr('%{y:.1f} % of cells emit %{x} tonnes of CO₂-eq. per person per year <extra></extra>'),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Per capita life-cycle GHG emissions from residential heating (estimated)'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('annual tonnes of CO₂-eq. per person'))),
        ),
    )
    hist_plot.add_vline(
        x=1.59,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot


def plot_energy_consumption_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['heat_consumption']).round(1),
            hovertemplate=tr(
                'Buildings in %{y:.1f} % of cells consume %{x} kWh of heating energy'
                ' per square meter per year <extra></extra>'
            ),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Average heating energy consumption per square meter of residential space (estimated)'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('kWh per square meter per year'))),
        ),
    )
    hist_plot.add_vline(
        x=127.1,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot


def plot_direct_emission_factor_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['direct_emission_factor']).round(2),
            hovertemplate=tr(
                'Buildings in %{y:.1f} % of cells emit %{x} kg of carbon dioxide'
                ' per kWh of heating energy used <extra></extra>'
            ),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Average direct emission factor of space heating in residential buildings (estimated)'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('kg of carbon dioxide per kWh of heating'))),
        ),
    )
    hist_plot.add_vline(
        x=0.194,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot


def plot_life_cycle_emission_factor_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['life_cycle_emission_factor']).round(2),
            hovertemplate=tr(
                'Buildings in %{y:.1f} % of cells emit %{x} kg of carbon dioxide'
                ' per kWh of heating energy used <extra></extra>'
            ),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Average life-cycle emission factor of space heating in residential buildings (estimated)'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('kg of carbon dioxide per kWh of heating'))),
        ),
    )
    hist_plot.add_vline(
        x=0.238,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot


def plot_living_space_per_capita_histogram(
    census_data: gpd.GeoDataFrame,
) -> Figure:
    hist_plot = Figure(
        data=go.Histogram(
            x=(census_data['average_sqm_per_person']).round(1),
            hovertemplate=tr('%{y:.1f} % of cells have %{x} square meters of living space per person.<extra></extra>'),
            histnorm='percent',
        ),
        layout=go.Layout(
            title=dict(
                text=tr('Average living space per capita'),
                subtitle=dict(text=tr('% of 100-m grid cells in area of interest'), font=dict(color='gray', size=10)),
            ),
            font=dict(size=12),
            xaxis=dict(title=dict(text=tr('square meters per person'))),
        ),
    )
    hist_plot.add_vline(
        x=46.3,
        line_width=1.5,
        line_dash='dot',
        annotation_text=tr('German average'),
        annotation_position='top left',
        annotation_textangle=-90,
    )
    return hist_plot
