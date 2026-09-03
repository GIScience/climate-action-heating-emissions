from datetime import timedelta
from pathlib import Path

import geopandas as gpd
from climatoology.base.aoi import AreaConstraint, CoveredByGeomConstraint
from climatoology.base.i18n import N_
from climatoology.base.plugin_info import PluginAuthor, PluginInfo, generate_plugin_info
from pydantic import HttpUrl
from shapely.geometry import mapping

from heating_emissions.core.input import ComputeInput


def get_info() -> PluginInfo:
    germany = gpd.read_file('resources/germany_buffered_boundaries.geojson').buffer(2500).to_crs(4326)
    aoi_constraints = [
        [
            AreaConstraint(max_area=30_000),
            CoveredByGeomConstraint(
                description='Germany',
                geom=mapping(germany.union_all()),
            ),
        ]
    ]

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
        aoi_constraints=aoi_constraints,
    )
    return info
