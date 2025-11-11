from unittest.mock import patch

import pytest
from climatoology.base.artifact import _Artifact
from climatoology.base.info import _Info
from climatoology.utility.exception import ClimatoologyUserError

from heating_emissions.core.input import TemporalEmissionsInput
from heating_emissions.core.operator_worker import calculate_time_downscale_emissions


def test_operator_info_request(operator):
    assert isinstance(operator.info(), _Info)


def test_operator_compute_german_request(
    operator, default_compute_input, default_german_aoi, default_aoi_properties, compute_resources
):
    computed_artifacts = operator.compute(
        resources=compute_resources,
        aoi=default_german_aoi,
        aoi_properties=default_aoi_properties,
        params=default_compute_input,
    )

    assert len(computed_artifacts) == 10
    for artifact in computed_artifacts:
        assert isinstance(artifact, _Artifact)


def test_operator_compute_german_request_all_optionals(
    operator,
    default_compute_input,
    default_german_aoi,
    default_aoi_properties,
    compute_resources,
    mock_read_era5_data,
    default_era5_data_dir,
):
    compute_input = default_compute_input.model_copy(deep=True)
    compute_input.optional_temporal_emission = TemporalEmissionsInput(
        is_active=True,
        year=2022,
    )

    def fake_estimate_months(*args, **kwargs):
        kwargs['estimate_months'] = [1, 2]
        return calculate_time_downscale_emissions(**kwargs)

    def fake_download_target(remote, target, time_timeout):
        fake_target = str(default_era5_data_dir / 'era5_data_heidelberg_2022_1.zip')
        return fake_target

    with (
        patch(
            'heating_emissions.core.operator_worker.calculate_time_downscale_emissions',
            side_effect=fake_estimate_months,
        ),
        patch(
            'heating_emissions.components.temporal_downscale.era5_data.async_download_era5_data',
            side_effect=fake_download_target,
        ),
    ):
        computed_artifacts = operator.compute(
            resources=compute_resources,
            aoi=default_german_aoi,
            aoi_properties=default_aoi_properties,
            params=compute_input,
        )

    assert len(computed_artifacts) == 12
    for artifact in computed_artifacts:
        assert isinstance(artifact, _Artifact)


def test_check_aoi_outside_germany(
    operator,
    default_compute_input,
    default_non_german_aoi,
    default_non_german_aoi_properties,
    compute_resources,
):
    with pytest.raises(ClimatoologyUserError):
        operator.compute(
            resources=compute_resources,
            aoi=default_non_german_aoi,
            aoi_properties=default_non_german_aoi_properties,
            params=default_compute_input,
        )
