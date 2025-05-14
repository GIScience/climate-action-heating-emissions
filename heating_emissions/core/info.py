import importlib
import importlib.metadata
from pathlib import Path

from climatoology.base.info import _Info, generate_plugin_info, PluginAuthor
from semver import Version
from datetime import timedelta


def get_info(params) -> _Info:
    info = generate_plugin_info(
        name='Heating Emissions',
        icon=Path('resources/heating-radiator.jpeg'),
        authors=[
            PluginAuthor(
                name='Sebastian Block',
                affiliation='HeiGIT gGmbH',
                website='https://heigit.org/heigit-team/',
            ),
            PluginAuthor(
                name='Veit Ulrich',
                affiliation='HeiGIT gGmbH',
                website='https://heigit.org/heigit-team/',
            ),
            PluginAuthor(
                name='Rizwan Khan',
                affiliation='HeiGIT gGmbH',
                website='https://heigit.org/heigit-team/',
            ),
        ],
        version=Version.parse(importlib.metadata.version('heating-emissions')),
        concerns=set(),
        purpose=Path('resources/purpose.md'),
        methodology=Path('resources/methodology.md'),
        demo_input_parameters=params(),
        computation_shelf_life=timedelta(weeks=52),
    )
    return info
