import numpy as np
import pandas as pd
import plotly.graph_objects as go
from climatoology.base.artifact import Artifact, ArtifactMetadata
from climatoology.base.artifact_creators import create_plotly_chart_artifact
from climatoology.base.computation import ComputationResources
from climatoology.base.i18n import tr
from plotly.graph_objs import Figure

from heating_emissions.components.utils import Topics


def build_daily_emission_lineplot_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> Artifact:
    summary = tr(
        'Daily CO₂ emissions from heating residential buildings. '
        'Simulated yearly emissions are {data_sum} tonnes of CO₂.'
    ).format(data_sum=round(np.sum(aoi_aggregate['data'][0].y) / 1000, 2))
    daily_emission_lineplot_artifact_metadata = ArtifactMetadata(
        name=tr('Line plot of regional daily heating emissions'),
        summary=summary,
        filename='aoi_dailyCO2_line',
        tags={tr(Topics.TEMPORAL)},
    )
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        metadata=daily_emission_lineplot_artifact_metadata,
        resources=resources,
    )


def plot_daily_emission_lineplot(daily_emissions: pd.DataFrame, y_column: str = 'regional_daily_emissions') -> Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_emissions['valid_time'],
            y=daily_emissions[y_column],  # result in tonnes
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(0, 123, 255, 0.25)',
            line=dict(width=2),
            hovertemplate=tr('Heating: %{y:.2f} kg CO₂<extra></extra>'),
            name=tr('Daily Emissions (full year)'),
        ),
    )

    fig.update_layout(
        xaxis_title=tr('Date'),
        yaxis_title=tr('Heating emissions (kg of CO₂)'),
        template='simple_white',
        hovermode='x unified',
        margin=dict(l=60, r=20, t=40, b=60),
        showlegend=True,
        legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='center', x=0.5),
    )

    return fig
