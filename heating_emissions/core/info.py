from datetime import timedelta
from pathlib import Path

from climatoology.base.i18n import N_
from climatoology.base.plugin_info import PluginAuthor, PluginInfo, generate_plugin_info
from pydantic import HttpUrl

from heating_emissions.core.input import ComputeInput


def get_info() -> PluginInfo:
    info = generate_plugin_info(
        name='Heating Emissions',
        icon=Path('resources/heating-radiator.jpeg'),
        authors=[
            PluginAuthor(
                name='Climate Action Team',
                affiliation='HeiGIT gGmbH',
                website=HttpUrl('https://heigit.org/heigit-team/'),
            ),
        ],
        concerns=set(),
        teaser=N_('Estimate carbon dioxide emissions from residential heating in Germany.'),
        demo_input_parameters=ComputeInput(temporal_emission_year=None),
        computation_shelf_life=timedelta(weeks=52),
    )
    return info
