import logging

import geopandas as gpd
import matplotlib
import numpy as np
import pandas as pd
from climatoology.base.artifact import (
    Artifact,
    ArtifactMetadata,
    ContinuousLegendData,
    Legend,
)
from climatoology.base.artifact_creators import create_vector_artifact
from climatoology.base.computation import ComputationResources
from matplotlib.colors import Normalize, to_hex
from pydantic_extra_types.color import Color

from heating_emissions.components.utils import BUILDING_AGES, ENERGY_SOURCES, Topics

log = logging.getLogger(__name__)


def build_gridded_artifact(
    result: gpd.GeoDataFrame, resources: ComputationResources, output: str, per_capita: bool = True
) -> Artifact:
    legend_lower_cap = 0
    if output == 'direct_co2_emissions':
        output_column = 'direct_co2_emissions_per_capita'
        file_name = 'direct_heating_emissions_per_capita'
        emission_type = 'Per capita'
        legend_upper_cap = 3000
        if not per_capita:
            output_column = 'direct_co2_emissions'
            file_name = 'direct_heating_emissions_absolute'
            emission_type = 'Absolute'
            legend_upper_cap = 150000

        layer_name = f'{emission_type} direct CO₂ emissions (kg/year)'
        caption = f'{emission_type} direct CO₂ emissions from residential heating per year per 100-m pixel'
        description = '**Estimated** direct CO₂ emissions from heating residential buildings.'
        tags = {Topics.DIRECT_EMISSIONS}

    if output == 'life_cycle_co2_emissions':
        output_column = 'life_cycle_co2_emissions_per_capita'
        file_name = 'life_cycle_heating_emissions_per_capita'
        emission_type = 'Per capita'
        legend_upper_cap = 3000
        if not per_capita:
            output_column = 'life_cycle_co2_emissions'
            file_name = 'life_cycle_heating_emissions_absolute'
            emission_type = 'Absolute'
            legend_upper_cap = 150000

        layer_name = f'{emission_type} life cycle GHG emissions (kg CO₂eq/year)'
        caption = f'{emission_type} life cycle GHG emissions from residential heating per 100-m pixel (kg CO₂eq/year)'
        description = '**Estimated** life cycle GHG emissions from heating residential buildings.'
        tags = {Topics.LIFE_CYCLE_EMISSIONS}

    if output == 'heat_consumption':
        output_column = output
        file_name = output
        legend_upper_cap = 135
        legend_lower_cap = 70
        layer_name = 'Energy consumption (kWh/m²/year)'
        caption = 'Average heating energy consumption rate in residential buildings (Estimated)'
        description = (
            '**Estimated** energy consumption rate for heating residential buildings based on building age data.'
        )
        tags = {Topics.PARAMETERS}

    low_bound_tick_label = f'{legend_lower_cap}'

    if output == 'average_sqm_per_person':
        output_column = output
        file_name = output
        legend_upper_cap = 100
        legend_lower_cap = 10
        low_bound_tick_label = f'< {legend_lower_cap}'
        layer_name = 'Living space (m² per person)'
        caption = 'Average living space per capita'
        description = 'Average living space per capita (m²) in 100-m grid cells (data from 2022 German census)'
        tags = {Topics.PARAMETERS}

    if output == 'direct_emission_factor':
        output_column = 'direct_emission_factor'
        file_name = 'direct_emission_factor'
        legend_upper_cap = 0.3
        layer_name = 'Direct emission factor (kg of CO₂ per kWh)'
        caption = 'Average direct emission factor from heating (Estimated)'
        description = (
            '**Estimated** average direct emission factor (kg of CO₂ per kWh) from heating residential buildings.'
        )
        tags = {Topics.DIRECT_EMISSIONS}

    if output == 'life_cycle_emission_factor':
        output_column = 'life_cycle_emission_factor'
        file_name = 'life_cycle_emission_factor'
        legend_upper_cap = 0.3
        layer_name = 'Life cycle emission factor (kg of CO₂eq per kWh)'
        caption = 'Average life cycle emission factor from heating (Estimated)'
        description = (
            '**Estimated** average life cycle emission factor (kg of CO₂eq per kWh) from heating residential buildings.'
        )
        tags = {Topics.LIFE_CYCLE_EMISSIONS}

    if 'yearly_emissions' in output:
        output_column, output_year = output.split(':')
        file_name = output_column
        emission_type = 'Per capita'
        legend_upper_cap = 3000
        if not per_capita:
            emission_type = 'Absolute'
            legend_upper_cap = 150000

        layer_name = f'{emission_type} CO₂ emissions (Simulated, {output_year}) (kg/year)'
        caption = f'{emission_type} CO₂ emissions from residential heating per 100-m pixel (Simulated, {output_year})'
        description = (
            f'Direct (scope 1) CO₂ emissions from heating residential buildings (Simulated, {output_year}). '
            f'This result is computed based on simulated heating demand by demand_ninja model.'
        )
        tags = {Topics.TEMPORAL}

    # Buffer centroids
    grid_cell_centroids = gpd.points_from_xy(x=result['x_mp_100m'], y=result['y_mp_100m'], crs='EPSG:3035')
    artifact_data = gpd.GeoDataFrame(data=result[output_column], geometry=grid_cell_centroids)
    artifact_data.geometry = artifact_data.buffer(50, cap_style=3)
    artifact_data_4326 = artifact_data.to_crs('EPSG:4326')

    # Define colors and legend
    norm = Normalize(vmin=legend_lower_cap, vmax=legend_upper_cap)
    cmap = matplotlib.colormaps.get('YlOrRd')
    cmap.set_under('#808080')
    artifact_data_4326['color'] = artifact_data[output_column].apply(lambda v: Color(to_hex(cmap(norm(v)))))
    legend_data = ContinuousLegendData(
        cmap_name='YlOrRd',
        ticks={f'> {legend_upper_cap}': 1, low_bound_tick_label: 0},
    )
    gridded_artifact_metadata = ArtifactMetadata(
        name=layer_name,
        summary=caption,
        description=description,
        filename=file_name,
        tags=tags,
    )
    return create_vector_artifact(
        data=artifact_data_4326,
        metadata=gridded_artifact_metadata,
        label=output_column,
        legend=Legend(
            legend_data=legend_data,
        ),
        resources=resources,
    )


def build_gridded_artifact_classdata(
    uncalculated_census_data: gpd.GeoDataFrame | pd.DataFrame, resources: ComputationResources, output: str
) -> Artifact:
    # maps of building age and dominant energy source
    output_column = output
    file_name = output

    if output == 'dominant_age':
        layer_name = 'Dominant building construction year'
        caption = 'Dominant building construction year'
        description = 'Dominant building construction year in 100-m grid cells (data from 2022 German census)'
        color_categories = BUILDING_AGES

    if output == 'dominant_energy':
        layer_name = 'Dominant building energy carrier'
        caption = 'Dominant building energy carrier'
        description = 'Dominant building energy carrier in 100-m grid cells (data from 2022 German census)'
        color_categories = ENERGY_SOURCES

    # Buffer centroids
    grid_cell_centroids = gpd.points_from_xy(
        x=uncalculated_census_data['x_mp_100m'], y=uncalculated_census_data['y_mp_100m'], crs='EPSG:3035'
    )
    artifact_data = gpd.GeoDataFrame(data=uncalculated_census_data[output_column], geometry=grid_cell_centroids)
    artifact_data.geometry = artifact_data.buffer(50, cap_style=3)
    artifact_data_4326 = artifact_data.to_crs('EPSG:4326')

    # Define colors and legend
    cmap = matplotlib.colormaps.get('coolwarm_r')
    color_list = cmap(np.linspace(0, 0.9, len(color_categories) - 1))
    color_list = [Color(to_hex(_)) for _ in color_list]
    color_list.append(Color('#808080'))  # the last category: unknown
    color_map = dict(zip(color_categories.values(), color_list))
    artifact_data_4326['color'] = artifact_data[output_column].map(color_map)

    # pass legend and use the default setting -> read 'create_vector_artifact' explanation.
    gridded_artifact_classdata_metadata = ArtifactMetadata(
        name=layer_name,
        summary=caption,
        description=description,
        filename=file_name,
        tags={Topics.PARAMETERS},
    )
    return create_vector_artifact(
        data=artifact_data_4326,
        metadata=gridded_artifact_classdata_metadata,
        label=output_column,
        legend=Legend(legend_data=color_map),
        resources=resources,
    )
