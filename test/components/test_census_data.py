import geopandas as gpd

from heating_emissions.components.census_data import get_census_tables_from_db


def test_get_census_tables_from_db(operator, default_german_aoi, mock_query_census_tables):
    raster_grid = gpd.read_file('resources/test/census_grid.geojson').set_index('raster_id_100m')
    census_data, uncalc_census_data = get_census_tables_from_db(
        db_connection=operator.ca_database_connection, raster_grid=raster_grid
    )

    expected_columns = ['population', 'average_sqm_per_person', 'heat_consumption', 'emission_factor']
    expected_columns_uncalc = ['dominant_age', 'dominant_energy']

    assert all([c in census_data.columns for c in expected_columns])
    assert all([c in uncalc_census_data.columns for c in expected_columns_uncalc])
