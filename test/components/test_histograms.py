from plotly.graph_objects import Figure
from heating_emissions.components.histogram_artifacts import (
    plot_per_capita_co2_histogram,
    plot_energy_consumption_histogram,
    plot_emission_factor_histogram,
)
from heating_emissions.components.utils import calculate_heating_emissions


def test_plot_histograms(compute_resources, default_census_table):
    default_census_data = default_census_table
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
