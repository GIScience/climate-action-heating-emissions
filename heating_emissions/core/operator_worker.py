# You may ask yourself why this file has such a strange name.
# Well ... python imports: https://discuss.python.org/t/warning-when-importing-a-local-module-with-the-same-name-as-a-2nd-or-3rd-party-module/27799
import logging
from typing import List

from climatoology.base.baseoperator import ComputationResources, BaseOperator, _Artifact, AoiProperties
from climatoology.base.info import _Info
import shapely
import geopandas as gpd
from geoalchemy2 import Geometry  # noqa: F401 (Geometry import is required for table reflection: https://geoalchemy-2.readthedocs.io/en/latest/core_tutorial.html#reflecting-tables)
from sqlalchemy import MetaData, create_engine

from heating_emissions.components.census_data import DatabaseConnection, collect_census_data
from heating_emissions.components.gridded_emissions_artifact import (
    build_emissions_artifact,
    calculate_heating_emissions,
    plot_per_capita_co2_histogram,
    build_per_capita_co2_histogram_artifact,
    plot_energy_consumption_histogram,
    build_energy_histogram_artifact,
    plot_emission_factor_histogram,
    build_emission_factor_histogram_artifact,
)
from heating_emissions.core.info import get_info
from heating_emissions.core.input import ComputeInput

log = logging.getLogger(__name__)


class Operator(BaseOperator[ComputeInput]):
    def __init__(self, ca_database_url: str):
        super().__init__()

        engine = create_engine(ca_database_url, echo=False, plugins=['geoalchemy2'])
        metadata = MetaData()
        metadata.reflect(bind=engine)
        self.ca_database_connection = DatabaseConnection(engine=engine, metadata=metadata)

    def info(self) -> _Info:
        return get_info()

    def compute(
        self,
        resources: ComputationResources,
        aoi: shapely.MultiPolygon,
        aoi_properties: AoiProperties,
        params: ComputeInput,
    ) -> List[_Artifact]:
        # Check we are within bounds of census data coverage
        self.check_aoi(aoi, aoi_properties)

        census_data = collect_census_data(db_connection=self.ca_database_connection, aoi=aoi)
        result = calculate_heating_emissions(census_data)

        per_capita_histogram = plot_per_capita_co2_histogram(census_data=census_data)
        energy_histogram = plot_energy_consumption_histogram(census_data=census_data)
        emission_factor_histogram = plot_emission_factor_histogram(census_data=census_data)

        heating_per_capita_emissions_artifact = build_emissions_artifact(result=result, resources=resources)
        heating_absolute_emissions_artifact = build_emissions_artifact(
            result=result, resources=resources, per_capita=False
        )

        per_capita_histogram_artifact = build_per_capita_co2_histogram_artifact(
            aoi_aggregate=per_capita_histogram, resources=resources
        )
        energy_consumption_histogram_artifact = build_energy_histogram_artifact(
            aoi_aggregate=energy_histogram, resources=resources
        )
        emission_factor_histogram_artifact = build_emission_factor_histogram_artifact(
            aoi_aggregate=emission_factor_histogram, resources=resources
        )

        return [
            heating_per_capita_emissions_artifact,
            per_capita_histogram_artifact,
            energy_consumption_histogram_artifact,
            emission_factor_histogram_artifact,
            heating_absolute_emissions_artifact,
        ]

    def check_aoi(self, aoi: shapely.MultiPolygon, aoi_properties: AoiProperties) -> None:
        aoi_gpd = gpd.GeoSeries(data=[aoi], crs='EPSG:4326')
        germany = gpd.read_file('resources/germany_bkg_boundaries.json')
        intersections = aoi_gpd.intersects(germany.geometry)
        if intersections[0]:
            return None
        else:
            log.error(
                f'Currently the Heating Emissions Plugin is only available for Germany. {aoi_properties.name} does not intersect Boundaries for Germany'
            )
            raise ValueError()
