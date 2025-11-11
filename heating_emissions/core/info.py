import importlib
import importlib.metadata
from datetime import timedelta
from pathlib import Path

from climatoology.base.info import PluginAuthor, _Info, generate_plugin_info
from semver import Version


def get_info(params) -> _Info:
    info = generate_plugin_info(
        name='Heating Emissions',
        icon=Path('resources/heating-radiator.jpeg'),
        authors=[
            PluginAuthor(
                name='Climate Action Team',
                affiliation='HeiGIT gGmbH',
                website='https://heigit.org/heigit-team/',
            ),
        ],
        version=Version.parse(importlib.metadata.version('heating-emissions')),
        concerns=set(),
        teaser='Estimate carbon dioxide emissions from residential heating in Germany.',
        purpose=Path('resources/purpose.md'),
        methodology=Path('resources/methodology.md'),
        demo_input_parameters=params(temporal_emission_year=2022),
        computation_shelf_life=timedelta(weeks=52),
    )
    return info
