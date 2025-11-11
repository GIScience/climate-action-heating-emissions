from datetime import datetime

from pydantic import BaseModel, Field


class TemporalEmissionsInput(BaseModel):
    is_active: bool = Field(
        title='Activate temporal flexible simulation of heating emissions for a specific year',
        description='If activated, daily heating emissions will be computed for the specified year.',
        examples=[False],
    )


class ComputeInput(BaseModel):
    # I used a group paramters here to show the 'title' and description. or they will disappear.
    optional_temporal_emission: TemporalEmissionsInput = Field(
        title='Temporal flexible simulation',
        description='Compute heating emissions for a specific year at high temporal resolution: yearly and daily emissions. '
        'The emissions are calculated based on '
        'simulated heating demand profiles derived from ERA5 weather data. '
        'Warning: The download of the ERA5 weather data may take a long time. '
        'If data download is not complete after 30 minutes, '
        'the temporal flexible simulation will be aborted.',
        examples=[TemporalEmissionsInput(is_active=False)],
        default=TemporalEmissionsInput(is_active=False),
    )

    temporal_emission_year: int = Field(
        title='Year for simulation',
        description='Year to be used for temporal flexible simulation of heating emissions.',
        ge=2017,
        le=datetime.now().year - 1,
        examples=[2022],
        default=2022,
    )
