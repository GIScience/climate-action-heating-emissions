FROM python:3.11.5-bookworm
SHELL ["/bin/bash", "-c"]

ENV PACKAGE_NAME='heating_emissions'

RUN pip install --no-cache-dir poetry==2.1.3

COPY pyproject.toml poetry.lock ./


RUN --mount=type=secret,id=CI_JOB_TOKEN,env=CI_JOB_TOKEN \
    git config --global url."https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.heigit.org".insteadOf "ssh://git@gitlab.heigit.org:2022" && \
    poetry install --no-ansi --no-interaction --all-extras --without dev,test --no-root

COPY $PACKAGE_NAME $PACKAGE_NAME
COPY resources resources
COPY README.md ./README.md

ARG CI_COMMIT_SHORT_SHA
RUN if [[ -n "${CI_COMMIT_SHORT_SHA}" ]]; then sed -E -i "s/^(version *= *\"[^+]*)\"/\\1+${CI_COMMIT_SHORT_SHA}\"/" pyproject.toml; fi;

RUN poetry install --no-ansi --no-interaction --all-extras --without dev,test

SHELL ["/bin/bash", "-c"]
ENTRYPOINT exec poetry run python ${PACKAGE_NAME}/plugin.py
