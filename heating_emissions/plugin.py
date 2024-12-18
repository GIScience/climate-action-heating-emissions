import logging.config

from climatoology.app.plugin import start_plugin

from heating_emissions.core.operator_worker import Operator

log = logging.getLogger(__name__)


def init_plugin() -> int:
    operator = Operator()

    log.info('Starting Plugin')
    return start_plugin(operator=operator)


if __name__ == '__main__':
    exit_code = init_plugin()
    log.info(f'Plugin exited with code {exit_code}')
