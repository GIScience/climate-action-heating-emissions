import logging.config

from climatoology.app.plugin import start_plugin
from ecmwf.datastores import Client as cds_Client

from heating_emissions.core.operator_worker import Operator
from heating_emissions.core.settings import FeatureFlags, Settings

log = logging.getLogger(__name__)


def init_plugin() -> int:
    feature_flags = FeatureFlags()
    log.debug(f'Running plugin with feature flags {feature_flags}')

    settings = Settings()
    cdsapi_client = cds_Client(url=settings.cdsapi_url, key=settings.cdsapi_key)
    operator = Operator(ca_database_url=settings.ca_database_url, cdsapi_client=cdsapi_client)

    log.info('Starting Plugin')
    return start_plugin(operator=operator)


if __name__ == '__main__':
    exit_code = init_plugin()
    log.info(f'Plugin exited with code {exit_code}')
