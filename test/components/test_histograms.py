import geopandas as gpd
from plotly.graph_objects import Figure

from heating_emissions.components.histogram_artifacts import (
    plot_emission_factor_histogram,
    plot_energy_consumption_histogram,
    plot_per_capita_co2_histogram,
)
from heating_emissions.components.utils import calculate_heating_emissions


def test_plot_histograms():
    default_census_data = gpd.GeoDataFrame(
        data={
            'population': [31, 85, 15],
            'average_sqm_per_person': [40, 80, 75],
            'heat_consumption': [65, 125.3, 145.2],
            'emission_factor': [0.2, 0.15, 0.3],
        },
        geometry=gpd.points_from_xy([5.15, 5.16, 5.16], [45.15, 45.16, 45.15]),
        crs='EPSG:4326',
    )

    result = calculate_heating_emissions(default_census_data)

    per_capita_histogram = plot_per_capita_co2_histogram(result)
    energy_consumption_histogram = plot_energy_consumption_histogram(result)
    emission_factor_histogram = plot_emission_factor_histogram(result)

    assert isinstance(per_capita_histogram, Figure)
    assert isinstance(energy_consumption_histogram, Figure)
    assert isinstance(emission_factor_histogram, Figure)

    assert per_capita_histogram['data'][0]['x'][0] == 0.52
    assert energy_consumption_histogram['data'][0]['x'][0] == 65
    assert emission_factor_histogram['data'][0]['x'][0] == 0.2
