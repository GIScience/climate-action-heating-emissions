# You may ask yourself why this file has such a strange name.
# Well ... python imports: https://discuss.python.org/t/warning-when-importing-a-local-module-with-the-same-name-as-a-2nd-or-3rd-party-module/27799
import logging
import time
from typing import List, Optional

import geopandas as gpd
import shapely
from climatoology.base.baseoperator import AoiProperties, Artifact, BaseOperator, ComputationResources
from climatoology.base.exception import ClimatoologyUserError
from climatoology.base.plugin_info import PluginInfo
from ecmwf.datastores import Client

# import is required for table reflection: https://geoalchemy-2.readthedocs.io/en/latest/core_tutorial.html#reflecting-tables
from geoalchemy2 import Geometry  # noqa: F401
from pydantic_extra_types.language_code import LanguageAlpha2
from sqlalchemy import MetaData, NullPool, create_engine

from heating_emissions.components.census_data import DatabaseConnection, collect_census_data
from heating_emissions.components.gridded_emissions_artifact import (
    build_gridded_artifact,
    build_gridded_artifact_classdata,
)
from heating_emissions.components.histogram_artifacts import (
    build_direct_emission_factor_histogram_artifact,
    build_energy_histogram_artifact,
    build_life_cycle_emission_factor_histogram_artifact,
    build_per_capita_direct_co2_histogram_artifact,
    build_per_capita_life_cycle_co2_histogram_artifact,
    plot_direct_emission_factor_histogram,
    plot_energy_consumption_histogram,
    plot_life_cycle_emission_factor_histogram,
    plot_per_capita_direct_co2_histogram,
    plot_per_capita_life_cycle_co2_histogram,
)
from heating_emissions.components.line_artifacts import (
    build_daily_emission_lineplot_artifact,
    plot_daily_emission_lineplot,
)
from heating_emissions.components.temporal_downscale.temporal_estimation import calculate_time_downscale_emissions
from heating_emissions.components.utils import (
    calculate_heating_emissions,
    get_aoi_area,
)
from heating_emissions.core.info import get_info
from heating_emissions.core.input import ComputeInput

log = logging.getLogger(__name__)


class Operator(BaseOperator[ComputeInput]):
    def __init__(self, ca_database_url: str, cdsapi_client: Optional[Client]):
        super().__init__()

        engine = create_engine(ca_database_url, echo=False, plugins=['geoalchemy2'], poolclass=NullPool)
        metadata = MetaData(schema='census_de')
        metadata.reflect(bind=engine)
        self.ca_database_connection = DatabaseConnection(engine=engine, metadata=metadata)
        self.cdsapi_client = cdsapi_client

    def info(self) -> PluginInfo:
        return get_info()

    def compute(  # dead: disable
        self,
        resources: ComputationResources,
        aoi: shapely.MultiPolygon,
        aoi_properties: AoiProperties,
        params: ComputeInput,
        language: LanguageAlpha2,
        **kwargs,
    ) -> List[Artifact]:
        # record start time to monitor the running time and raise an error when the temporal estimation timeout.
        plugin_start_time = time.time()

        # Check we are within bounds of census data coverage
        self.check_aoi(aoi, aoi_properties)

        census_data, uncalculated_census_data = collect_census_data(db_connection=self.ca_database_connection, aoi=aoi)
        result = calculate_heating_emissions(census_data)

        # Gridded artifacts
        result.index.names = ['index']
        heating_per_capita_direct_emissions_artifact = build_gridded_artifact(
            result=result, resources=resources, output='direct_co2_emissions'
        )
        heating_per_capita_life_cycle_emissions_artifact = build_gridded_artifact(
            result=result, resources=resources, output='life_cycle_co2_emissions'
        )
        heating_absolute_direct_emissions_artifact = build_gridded_artifact(
            result=result, resources=resources, output='direct_co2_emissions', per_capita=False
        )
        heating_absolute_life_cycle_emissions_artifact = build_gridded_artifact(
            result=result, resources=resources, output='life_cycle_co2_emissions', per_capita=False
        )
        energy_consumption_artifact = build_gridded_artifact(
            result=result, resources=resources, output='heat_consumption'
        )
        living_space_artifact = build_gridded_artifact(
            result=result, resources=resources, output='average_sqm_per_person'
        )
        direct_emission_factor_artifact = build_gridded_artifact(
            result=result, resources=resources, output='direct_emission_factor'
        )
        life_cycle_emission_factor_artifact = build_gridded_artifact(
            result=result, resources=resources, output='life_cycle_emission_factor'
        )

        # Gridded artifacts -- original (uncalculated) census data
        uncalculated_census_data.index.names = ['index']
        building_age_artifact = build_gridded_artifact_classdata(
            uncalculated_census_data=uncalculated_census_data, resources=resources, output='dominant_age'
        )
        building_energy_source_artifact = build_gridded_artifact_classdata(
            uncalculated_census_data=uncalculated_census_data, resources=resources, output='dominant_energy'
        )

        # Histograms
        direct_per_capita_histogram = plot_per_capita_direct_co2_histogram(census_data=census_data)
        direct_per_capita_histogram_artifact = build_per_capita_direct_co2_histogram_artifact(
            aoi_aggregate=direct_per_capita_histogram, resources=resources
        )
        life_cycle_per_capita_histogram = plot_per_capita_life_cycle_co2_histogram(census_data=census_data)
        life_cycle_per_capita_histogram_artifact = build_per_capita_life_cycle_co2_histogram_artifact(
            aoi_aggregate=life_cycle_per_capita_histogram, resources=resources
        )
        energy_histogram = plot_energy_consumption_histogram(census_data=census_data)
        energy_consumption_histogram_artifact = build_energy_histogram_artifact(
            aoi_aggregate=energy_histogram, resources=resources
        )

        direct_emission_factor_histogram = plot_direct_emission_factor_histogram(census_data=census_data)
        direct_emission_factor_histogram_artifact = build_direct_emission_factor_histogram_artifact(
            aoi_aggregate=direct_emission_factor_histogram, resources=resources
        )
        life_cycle_emission_factor_histogram = plot_life_cycle_emission_factor_histogram(census_data=census_data)
        life_cycle_emission_factor_histogram_artifact = build_life_cycle_emission_factor_histogram_artifact(
            aoi_aggregate=life_cycle_emission_factor_histogram, resources=resources
        )

        return_artifacts = [
            heating_per_capita_direct_emissions_artifact,
            heating_per_capita_life_cycle_emissions_artifact,
            direct_per_capita_histogram_artifact,
            life_cycle_per_capita_histogram_artifact,
            energy_consumption_histogram_artifact,
            direct_emission_factor_histogram_artifact,
            life_cycle_emission_factor_histogram_artifact,
            heating_absolute_direct_emissions_artifact,
            heating_absolute_life_cycle_emissions_artifact,
            energy_consumption_artifact,
            living_space_artifact,
            direct_emission_factor_artifact,
            life_cycle_emission_factor_artifact,
            building_age_artifact,
            building_energy_source_artifact,
        ]

        # temporal downscaling emissions
        if params.temporal_emission_year is not None:
            optional_func_start_time = time.time() - plugin_start_time  # unit: seconds
            runtime_limit = 121 * 60 - optional_func_start_time
            with self.catch_exceptions(indicator_name='Temporal_emissions', resources=resources):
                assert self.cdsapi_client is not None, 'CDS API client must be configured to run temporal downscaling'

                year = params.temporal_emission_year
                census_data.index.names = ['raster_id_100m']
                census_yearly_emi_user, region_daily_emissions = calculate_time_downscale_emissions(
                    cdsapi_client=self.cdsapi_client,
                    year=year,
                    city_name=aoi_properties.name,
                    aoi=aoi,
                    census_data=census_data,
                    savedir=resources.computation_dir / 'weather_data',
                    runtime_limit=runtime_limit,  # 'resources/weather_data'
                )

                census_yearly_emi_user.index.names = ['index']
                yearly_emissions_artifact = build_gridded_artifact(
                    result=census_yearly_emi_user,
                    resources=resources,
                    per_capita=False,
                    output=f'yearly_emissions:{year}',
                )
                daily_emission_line = plot_daily_emission_lineplot(
                    daily_emissions=region_daily_emissions, y_column='regional_daily_emissions'
                )
                daily_emission_line_artifact = build_daily_emission_lineplot_artifact(
                    aoi_aggregate=daily_emission_line, resources=resources
                )
                return_artifacts.extend([yearly_emissions_artifact, daily_emission_line_artifact])

        return return_artifacts

    def check_aoi(self, aoi: shapely.MultiPolygon, aoi_properties: AoiProperties) -> None:
        aoi_as_series = gpd.GeoSeries(data=[aoi], crs='EPSG:4326')

        germany = gpd.read_file('resources/germany_buffered_boundaries.json').buffer(2e-2)
        inside_germany = aoi_as_series.within(germany.geometry)
        if not inside_germany[0]:
            raise ClimatoologyUserError(
                f'For now, estimates of heating emissions are only available for Germany. {aoi_properties.name} is '
                'outside Germany. We are working on expanding the tool to other countries'
            )

        aoi_utm32n_area_km2 = get_aoi_area(aoi_as_series)
        if aoi_utm32n_area_km2 > 30000:
            raise ClimatoologyUserError(
                f'The selected area is too large: {aoi_utm32n_area_km2} km². Currently, the maximum allowed area is 30000 km². Please select a smaller area or a sub-region of your selected area.'
            )
