from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from heating_emissions.core.settings import FeatureFlags

feature_flags = FeatureFlags()


class ComputeInput(BaseModel):
    temporal_emission_year: Annotated[
        Optional[int],
        Field(
            title='Temporal Downscaling',
            description='Specify the year to be used for temporal flexible simulation of heating emissions. '
            'If `None` (the default) then do not apply temporal downscaling. '
            'The emissions are calculated based on '
            'simulated heating demand profiles derived from ERA5 weather data. '
            'Warning: The download of the ERA5 weather data may take a long time. '
            'If data download is not complete after 30 minutes, '
            'the temporally-downscaled simulation will be aborted. ',
            ge=2017,
            le=datetime.now().year - 1,
            examples=[2022],
            default=None,
            json_schema_extra={'x-mark-important': True},
        ),
        None if feature_flags.temporal_downscaling else SkipJsonSchema(),
    ]
