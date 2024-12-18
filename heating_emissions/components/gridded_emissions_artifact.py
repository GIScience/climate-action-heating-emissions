from typing import Dict

from climatoology.base.artifact import RasterInfo, _Artifact, create_geotiff_artifact
from climatoology.base.computation import ComputationResources
from climatoology.utility.api import LabelDescriptor
from pydantic_extra_types.color import Color


def build_lulc_artifact(
    raster_info: RasterInfo, labels: Dict[str, LabelDescriptor], resources: ComputationResources
) -> _Artifact:
    return create_geotiff_artifact(
        raster_info=raster_info,
        layer_name='LULC Classification',
        caption='A land-use and land-cover classification of a user defined area.',
        description='The classification is created using a deep learning model.',
        legend_data={v.name: Color(v.color) for _, v in labels.items()},
        resources=resources,
        filename='raster',
    )
