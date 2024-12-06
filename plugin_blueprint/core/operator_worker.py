# You may ask yourself why this file has such a strange name.
# Well ... python imports: https://discuss.python.org/t/warning-when-importing-a-local-module-with-the-same-name-as-a-2nd-or-3rd-party-module/27799
import logging
from typing import List

from climatoology.base.artifact import create_markdown_artifact
from climatoology.base.baseoperator import ComputationResources, BaseOperator, _Artifact, AoiProperties
from climatoology.base.info import _Info
import shapely

from plugin_blueprint.core.info import get_info
from plugin_blueprint.core.input import ComputeInput


log = logging.getLogger(__name__)


class Operator(BaseOperator[ComputeInput]):
    def info(self) -> _Info:
        return get_info()

    def compute(
        self,
        resources: ComputationResources,
        aoi: shapely.MultiPolygon,
        aoi_properties: AoiProperties,
        params: ComputeInput,
    ) -> List[_Artifact]:
        # Create a placeholder markdown artifact
        markdown_artifact = create_markdown_artifact(
            text='A placeholder artifact showing some text results.',
            name='Placeholder Result',
            tl_dr='Some placeholder text',
            resources=resources,
            filename='markdown',
        )

        # When building your own plugin, refactor the logic for creating results by moving it to a submodule
        # See the Plugin Showcase for a full example

        return [markdown_artifact]
