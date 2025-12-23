from datetime import timedelta
from pathlib import Path
from typing import Type

from climatoology.base.plugin_info import PluginAuthor, PluginInfo, generate_plugin_info
from pydantic import BaseModel, HttpUrl

from heating_emissions.core.input import ComputeInput


def get_info(params: Type[BaseModel]) -> PluginInfo:
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
        teaser='Estimate carbon dioxide emissions from residential heating in Germany.',
        purpose=Path('resources/purpose.md'),
        methodology=Path('resources/methodology.md'),
        demo_input_parameters=ComputeInput(temporal_emission_year=2022),
        computation_shelf_life=timedelta(weeks=52),
    )
    return info
