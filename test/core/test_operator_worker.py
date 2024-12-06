from climatoology.base.artifact import _Artifact
from climatoology.base.info import _Info


def test_operator_info_request(operator):
    assert isinstance(operator.info(), _Info)


def test_operator_compute_request(
    operator,
    default_compute_input,
    default_aoi,
    default_aoi_properties,
    compute_resources,
):
    computed_artifacts = operator.compute(
        resources=compute_resources,
        aoi=default_aoi,
        aoi_properties=default_aoi_properties,
        params=default_compute_input,
    )

    assert len(computed_artifacts) == 1
    for artifact in computed_artifacts:
        assert isinstance(artifact, _Artifact)
