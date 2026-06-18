import logging
from enum import StrEnum

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
from climatoology.base.i18n import N_, tr, translate_dataframe
from matplotlib.colors import Normalize, to_hex
from pydantic_extra_types.color import Color

from heating_emissions.components.utils import BUILDING_AGES, ENERGY_SOURCES, Topics

log = logging.getLogger(__name__)


class Output(StrEnum):
    life_cycle_emission_factor = 'life_cycle_emission_factor'
    direct_emission_factor = 'direct_emission_factor'
    average_sqm_per_person = 'average_sqm_per_person'
    direct_co2_emissions = 'direct_co2_emissions'
    life_cycle_co2_emissions = 'life_cycle_co2_emissions'
    heat_consumption = 'heat_consumption'


class EmissionType(StrEnum):
    per_capita = N_('Per capita')
    absolute = N_('Absolute')


def build_gridded_artifact(
    result: gpd.GeoDataFrame, resources: ComputationResources, output: Output | str, is_per_capita: bool = True
) -> Artifact:
    legend_lower_cap = 0
    low_bound_tick_label = f'{legend_lower_cap}'

    emission_type = tr(EmissionType.per_capita) if is_per_capita else tr(EmissionType.absolute)

    match output:
        case Output.direct_co2_emissions:
            if is_per_capita:
                output_column = 'direct_co2_emissions_per_capita'
                file_name = 'direct_heating_emissions_per_capita'
                legend_upper_cap = 3000
            else:
                output_column = 'direct_co2_emissions'
                file_name = 'direct_heating_emissions_absolute'
                legend_upper_cap = 150000

            layer_name = tr('{emission_type} direct CO₂ emissions (kg/year)').format(emission_type=emission_type)
            caption = tr(
                '{emission_type} direct CO₂ emissions from residential heating per year per 100-m pixel'
            ).format(emission_type=emission_type)
            description = tr('**Estimated** direct CO₂ emissions from heating residential buildings.')
            tags = {tr(Topics.DIRECT_EMISSIONS)}

        case Output.life_cycle_co2_emissions:
            if is_per_capita:
                output_column = 'life_cycle_co2_emissions_per_capita'
                file_name = 'life_cycle_heating_emissions_per_capita'
                legend_upper_cap = 3000
            else:
                output_column = 'life_cycle_co2_emissions'
                file_name = 'life_cycle_heating_emissions_absolute'
                legend_upper_cap = 150000

            layer_name = tr('{emission_type} life cycle GHG emissions (kg CO₂eq/year)').format(
                emission_type=emission_type
            )
            caption = tr(
                '{emission_type} life cycle GHG emissions from residential heating per 100-m pixel (kg CO₂eq/year)'
            ).format(emission_type=emission_type)
            description = tr('**Estimated** life cycle GHG emissions from heating residential buildings.')
            tags = {tr(Topics.LIFE_CYCLE_EMISSIONS)}

        case Output.heat_consumption:
            output_column = output
            file_name = output
            legend_upper_cap = 135
            legend_lower_cap = 70
            layer_name = tr('Energy consumption (kWh/m²/year)')
            caption = tr('Average area-specific heating energy consumption in residential buildings (estimated)')
            description = tr(
                '**Estimated** area-specific energy consumption for heating residential buildings based on building age data.'
            )
            tags = {tr(Topics.PARAMETERS)}

        case Output.average_sqm_per_person:
            output_column = output
            file_name = output
            legend_upper_cap = 100
            legend_lower_cap = 10
            low_bound_tick_label = f'< {legend_lower_cap}'
            layer_name = tr('Living space (m² per person)')
            caption = tr('Average living space per capita')
            description = tr('Average living space per capita (m²) in 100-m grid cells (data from 2022 German census)')
            tags = {tr(Topics.PARAMETERS)}

        case Output.direct_emission_factor:
            output_column = 'direct_emission_factor'
            file_name = 'direct_emission_factor'
            legend_upper_cap = 0.3
            layer_name = tr('Direct emission factor (kg of CO₂ per kWh)')
            caption = tr('Average direct emission factor from heating (estimated)')
            description = tr(
                '**Estimated** average direct emission factor (kg of CO₂ per kWh) from heating residential buildings.'
            )
            tags = {tr(Topics.DIRECT_EMISSIONS)}

        case Output.life_cycle_emission_factor:
            output_column = 'life_cycle_emission_factor'
            file_name = 'life_cycle_emission_factor'
            legend_upper_cap = 0.3
            layer_name = tr('Life cycle emission factor (kg of CO₂eq per kWh)')
            caption = tr('Average life cycle emission factor from heating (estimated)')
            description = tr(
                '**Estimated** average life cycle emission factor (kg of CO₂eq per kWh) from heating residential buildings.'
            )
            tags = {tr(Topics.LIFE_CYCLE_EMISSIONS)}
        case _:
            # TODO: this if statement should be redundant?
            if 'yearly_emissions' in output:
                output_column, output_year = output.split(':')
                file_name = output_column
                if is_per_capita:
                    legend_upper_cap = 3000
                else:
                    legend_upper_cap = 150000

                layer_name = tr('{emission_type} CO₂ emissions (simulated, {output_year}) (kg/year)').format(
                    emission_type=emission_type, output_year=output_year
                )
                caption = tr(
                    '{emission_type} CO₂ emissions from residential heating per 100-m pixel (simulated, {output_year})'
                ).format(emission_type=emission_type, output_year=output_year)
                description = tr(
                    'Direct (scope 1) CO₂ emissions from heating residential buildings (simulated, {output_year}). '
                    'This result is computed based on simulated heating demand by demand_ninja model.'
                ).format(output_year=output_year)
                tags = {tr(Topics.TEMPORAL)}

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


class ClassdataOutput(StrEnum):
    dominant_age = 'dominant_age'
    dominant_energy = 'dominant_energy'


def build_gridded_artifact_classdata(
    uncalculated_census_data: gpd.GeoDataFrame | pd.DataFrame, resources: ComputationResources, output: ClassdataOutput
) -> Artifact:
    # maps of building age and dominant energy source
    output_column = output
    file_name = output

    match output:
        case ClassdataOutput.dominant_age:
            layer_name = tr('Dominant building construction year')
            caption = tr('Dominant building construction year')
            description = tr('Dominant building construction year in 100-m grid cells (data from 2022 German census)')
            color_categories = BUILDING_AGES

        case ClassdataOutput.dominant_energy:
            layer_name = tr('Dominant building energy carrier')
            caption = tr('Dominant building energy carrier')
            description = tr('Dominant building energy carrier in 100-m grid cells (data from 2022 German census)')
            color_categories = ENERGY_SOURCES
        case _:
            raise NotImplementedError(f'{output} not implemented')

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

    tr_color_map = {tr(k): v for k, v in color_map.items()}
    tr_artifact_data = translate_dataframe(artifact_data_4326)

    # pass legend and use the default setting -> read 'create_vector_artifact' explanation.
    gridded_artifact_classdata_metadata = ArtifactMetadata(
        name=layer_name,
        summary=caption,
        description=description,
        filename=file_name,
        tags={tr(Topics.PARAMETERS)},
    )
    return create_vector_artifact(
        data=tr_artifact_data,
        metadata=gridded_artifact_classdata_metadata,
        label=output_column,
        legend=Legend(legend_data=tr_color_map),
        resources=resources,
    )
