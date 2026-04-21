import logging
from pathlib import Path
from typing import NoReturn

import click
from click import Context
from climatoology.app.plugin import run_standalone_computation, start_plugin
from climatoology.base.logging import get_climatoology_logger
from climatoology.base.plugin_info import DEFAULT_LANGUAGE
from ecmwf.datastores import Client as cds_Client

from heating_emissions.core.info import get_info
from heating_emissions.core.input import ComputeInput
from heating_emissions.core.operator_worker import Operator
from heating_emissions.core.settings import FeatureFlags, Settings

log = get_climatoology_logger(__name__)


@click.group(context_settings={'show_default': True})
@click.pass_context
def plugin(ctx: Context) -> None:
    feature_flags = FeatureFlags()
    log.debug(f'Running plugin with feature flags {feature_flags}')

    settings = Settings()
    logging.basicConfig(level=settings.log_level)

    cdsapi_client = None
    if settings.cdsapi_key is not None:
        cdsapi_client = cds_Client(url=settings.cdsapi_url, key=settings.cdsapi_key)

    operator = Operator(ca_database_url=settings.ca_database_url, cdsapi_client=cdsapi_client)

    ctx.ensure_object(dict)
    ctx.obj['operator'] = operator


@plugin.command()
@click.pass_context
def start(ctx: Context) -> NoReturn:  # dead: disable
    log.info('Starting Plugin')
    start_plugin(operator=ctx.obj['operator'])


@plugin.command()
@click.option(
    '--aoi-file',
    default=Path('resources/aoi.geojson'),
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help='The GeoJSON file containing the AOI geometry. It needs to contain a single geojson Feature with a '
    'MultiPolygon geometry and at least properties "name" and "id"',
)
@click.option(
    '--lang',
    default=DEFAULT_LANGUAGE,
    type=click.Choice(get_info().purpose.keys()),
    help='The language the computation results should be generated in',
)
@click.option(
    '--downscale-year',
    default=None,
    type=int,
    help='Calculate a specific year with high temporal resolution. Will not apply temporal-downscaling by default.',
)
@click.option(
    '--output-dir',
    default=None,
    type=click.Path(exists=False, file_okay=False, writable=True, path_type=Path),
    help='The directory where the output should be written. Defaults to results/<now-timestamp>-<aoi-name>-<random_id>',
)
@click.pass_context
def compute(  # dead: disable
    ctx: Context, aoi_file: Path, lang: str, output_dir: Path, downscale_year: int = None
) -> None:
    log.info('Running plugin in stand-alone mode')

    params = ComputeInput(temporal_emission_year=downscale_year)

    computation_info = run_standalone_computation(
        operator=ctx.obj['operator'],
        aoi_file=aoi_file,
        params=params,
        lang=lang,
        output_dir=output_dir,
    )

    print(f'Wrote {len(computation_info.artifacts)} artifacts to {computation_info.output_dir.absolute()}')
