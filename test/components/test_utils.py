import pandas as pd

from heating_emissions.components.utils import generate_colors


def test_generate_colors():
    test_data = pd.Series(data=[1, 2, 4])

    expected_color_map = {0: (59, 76, 192), 1: (141, 176, 254), 2: (221, 220, 220), 3: (244, 152, 122), 4: (180, 4, 38)}

    resulting_color_map = generate_colors(test_data, cmap_name='coolwarm')

    assert isinstance(resulting_color_map[0], tuple)
    assert isinstance(resulting_color_map[3], tuple)
    assert isinstance(resulting_color_map[4], tuple)

    assert resulting_color_map == expected_color_map
