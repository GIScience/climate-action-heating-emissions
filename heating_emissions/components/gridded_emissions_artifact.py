import matplotlib
from climatoology.base.artifact import (
    ContinuousLegendData,
    _Artifact,
    create_geojson_artifact,
)
from climatoology.base.computation import ComputationResources
import geopandas as gpd
from matplotlib.colors import to_hex, Normalize
import logging
from pydantic_extra_types.color import Color

log = logging.getLogger(__name__)


def build_gridded_artifact(
    result: gpd.GeoDataFrame, resources: ComputationResources, output: str = 'co2', per_capita: bool = True
) -> _Artifact:
    output_column = 'co2_emissions_per_capita'
    file_name = 'heating_emissions_per_capita'
    emission_type = 'Per capita'
    legend_upper_cap = 3000
    legend_lower_cap = 0
    is_primary = True
    if not per_capita:
        output_column = 'co2_emissions'
        file_name = 'heating_emissions_absolute'
        emission_type = 'Absolute'
        legend_upper_cap = 150000
        is_primary = False

    layer_name = f'{emission_type} CO₂ emissions (kg/year)'
    caption = f'{emission_type} CO₂ emissions from residential heating per year per 100-m pixel'
    description = 'Territorial (scope 1) CO₂ emissions from heating residential buildings.'

    if output == 'heat_consumption':
        output_column = output
        file_name = output
        legend_upper_cap = 135
        legend_lower_cap = 70
        layer_name = 'Energy consumption (kWh/m²/year)'
        caption = 'Average heating energy consumption rate in residential buildings'
        description = 'Estimated energy consumption rate for heating residential buildings based on building age data.'
        is_primary = False

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
        is_primary = False

    if output == 'emission_factor':
        output_column = output
        file_name = output
        legend_upper_cap = 0.3
        layer_name = 'Emission factor (kg of CO₂ per kWh)'
        caption = 'Average (scope 1) emission factor from heating'
        description = (
            'Estimated level of in situ (scope 1) emissions (kg of CO₂ per kWh) from heating residential buildings.'
        )
        is_primary = False

    # Buffer centroids
    grid_cell_centroids = gpd.points_from_xy(x=result['x_mp_100m'], y=result['y_mp_100m'], crs='EPSG:3035')
    artifact_data = gpd.GeoDataFrame(data=result[output_column], geometry=grid_cell_centroids)
    artifact_data.geometry = artifact_data.buffer(50, cap_style=3)
    artifact_data_4326 = artifact_data.to_crs('EPSG:4326')

    # Define colors and legend
    norm = Normalize(vmin=legend_lower_cap, vmax=legend_upper_cap)
    cmap = matplotlib.colormaps.get('YlOrRd')
    cmap.set_under('#808080')
    color = artifact_data[output_column].apply(lambda v: Color(to_hex(cmap(norm(v)))))
    legend = ContinuousLegendData(
        cmap_name='YlOrRd',
        ticks={f'> {legend_upper_cap}': 1, low_bound_tick_label: 0},
    )

    return create_geojson_artifact(
        features=artifact_data_4326.geometry,
        layer_name=layer_name,
        caption=caption,
        description=description,
        color=color,
        label=artifact_data[output_column].to_list(),
        legend_data=legend,
        primary=is_primary,
        resources=resources,
        filename=file_name,
    )
