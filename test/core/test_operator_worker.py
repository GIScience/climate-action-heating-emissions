import pytest
from climatoology.base.artifact import _Artifact
from climatoology.base.info import _Info
from climatoology.utility.exception import ClimatoologyUserError


def test_operator_info_request(operator):
    assert isinstance(operator.info(), _Info)


def test_operator_compute_german_request(
    operator,
    default_compute_input,
    default_german_aoi,
    default_aoi_properties,
    compute_resources,
    mock_query_census_tables,
):
    computed_artifacts = operator.compute(
        resources=compute_resources,
        aoi=default_german_aoi,
        aoi_properties=default_aoi_properties,
        params=default_compute_input,
    )

    assert len(computed_artifacts) == 5
    for artifact in computed_artifacts:
        assert isinstance(artifact, _Artifact)


def test_check_aoi_outside_germany(
    operator,
    default_compute_input,
    default_non_german_aoi,
    default_non_german_aoi_properties,
    compute_resources,
    mock_query_census_tables,
):
    with pytest.raises(ClimatoologyUserError):
        operator.compute(
            resources=compute_resources,
            aoi=default_non_german_aoi,
            aoi_properties=default_non_german_aoi_properties,
            params=default_compute_input,
        )
