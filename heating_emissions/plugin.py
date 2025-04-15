import logging.config

from climatoology.app.plugin import start_plugin

from heating_emissions.core.operator_worker import Operator
from heating_emissions.core.settings import Settings

log = logging.getLogger(__name__)


def init_plugin() -> int:
    settings = Settings()
    operator = Operator(ca_database_url=settings.ca_database_url)

    log.info('Starting Plugin')
    return start_plugin(operator=operator)


if __name__ == '__main__':
    exit_code = init_plugin()
    log.info(f'Plugin exited with code {exit_code}')
