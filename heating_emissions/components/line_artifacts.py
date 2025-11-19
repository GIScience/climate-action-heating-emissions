import numpy as np
import pandas as pd
import plotly.graph_objects as go
from climatoology.base.artifact import _Artifact, create_plotly_chart_artifact
from climatoology.base.computation import ComputationResources
from plotly.graph_objs import Figure

from heating_emissions.components.utils import Topics


def build_daily_emission_lineplot_artifact(aoi_aggregate: Figure, resources: ComputationResources) -> _Artifact:
    return create_plotly_chart_artifact(
        figure=aoi_aggregate,
        title='Line plot of regional daily heating emissions',
        caption=f'Daily CO₂ emissions from heating residential buildings. '
        f'Simulated yearly emissions are {round(np.sum(aoi_aggregate["data"][0].y) / 1000, 2)} tonnes of CO₂.',
        resources=resources,
        filename='aoi_dailyCO2_line',
        tags={Topics.TEMPORAL},
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
            hovertemplate='Heating: %{y:.2f} kg CO₂<extra></extra>',
            name='Daily Emissions (Full Year)',
        ),
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Heating emissions (kg of CO₂)',
        template='simple_white',
        hovermode='x unified',
        margin=dict(l=60, r=20, t=40, b=60),
        showlegend=True,
        legend=dict(orientation='h', yanchor='top', y=1.02, xanchor='center', x=0.5),
    )

    return fig
