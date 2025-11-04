CREATE EXTENSION postgis;

CREATE SCHEMA census_de;


-- Create table census_de.raster_grid_100m
CREATE TABLE
    census_de.raster_grid_100m (
        raster_id_100m varchar NOT NULL,
        x_mp_100m int4 NULL,
        y_mp_100m int4 NULL,
        geometry public.geometry (point, 4326) NULL,
        CONSTRAINT raster_grid_100m_pk PRIMARY KEY (raster_id_100m)
    );

CREATE INDEX idx_raster_grid_100m_geometry ON census_de.raster_grid_100m USING gist (geometry);

CREATE INDEX ix_census_de_raster_grid_100m_raster_id_100m ON census_de.raster_grid_100m USING btree (raster_id_100m);

INSERT INTO
    census_de.raster_grid_100m (raster_id_100m, x_mp_100m, y_mp_100m, geometry)
VALUES
    ('CRS3035RES100mN2922800E4223800', 4223850, 2922850, 'POINT (8.661454554966516 49.41060039206927)'),
    ('CRS3035RES100mN2922800E4223900', 4223950, 2922850, 'POINT (8.662832094477682 49.410616750377287)'),
    ('CRS3035RES100mN2923000E4224200', 4224250, 2923050, 'POINT (8.66691558699795 49.412464029916087)'),
    ('CRS3035RES100mN2923000E4224300', 4224350, 2923050, 'POINT (8.668293180627245 49.412480321549467)'),
    ('CRS3035RES100mN2923000E4224400', 4224450, 2923050, 'POINT (8.669670775098256 49.412496596340624)'),
    ('CRS3035RES100mN2923100E4224100', 4224150, 2923150, 'POINT (8.665513401589685 49.413346873487946)'),
    ('CRS3035RES100mN2923100E4224200', 4224250, 2923150, 'POINT (8.66689101974962 49.413363182309659)'),
    ('CRS3035RES100mN2923100E4224300', 4224350, 2923150, 'POINT (8.668268638752203 49.41337947428876)');


-- Create table census_de.population

CREATE TABLE census_de.population (
	raster_id_100m varchar NOT NULL,
	population int4 NULL,
	CONSTRAINT population_pk PRIMARY KEY (raster_id_100m),
	CONSTRAINT population_raster_grid_100m_fk FOREIGN KEY (raster_id_100m) REFERENCES census_de.raster_grid_100m(raster_id_100m)
);
CREATE INDEX ix_census_de_population_raster_id_100m ON census_de.population USING btree (raster_id_100m);

INSERT INTO
    census_de.population (raster_id_100m, population)
VALUES
    ('CRS3035RES100mN2922800E4223800', 6),
    ('CRS3035RES100mN2922800E4223900', 5),
    ('CRS3035RES100mN2923000E4224200', 41),
    ('CRS3035RES100mN2923000E4224300', 39),
    ('CRS3035RES100mN2923000E4224400', 387),
    ('CRS3035RES100mN2923100E4224100', 44),
    ('CRS3035RES100mN2923100E4224200', 208),
    ('CRS3035RES100mN2923100E4224300', 274);


-- Create table census_de.residential_living_space

CREATE TABLE
    census_de.residential_living_space (
        raster_id_100m varchar NOT NULL,
        average_sqm_per_person float8 NULL,
        CONSTRAINT residential_living_space_pk PRIMARY KEY (raster_id_100m)
    );

CREATE INDEX ix_census_de_residential_living_space_raster_id_100m ON census_de.residential_living_space USING btree (raster_id_100m);

INSERT INTO
    census_de.residential_living_space (raster_id_100m, average_sqm_per_person)
VALUES
    ('CRS3035RES100mN2922800E4223800', 56.3),
    ('CRS3035RES100mN2922800E4223900', 104.87),
    ('CRS3035RES100mN2923000E4224200', 17.84),
    ('CRS3035RES100mN2923000E4224300', 17.48),
    ('CRS3035RES100mN2923000E4224400', 21.39),
    ('CRS3035RES100mN2923100E4224100', 15.75),
    ('CRS3035RES100mN2923100E4224200', 19.81),
    ('CRS3035RES100mN2923100E4224300', 24.05);


-- Create table census_de.residential_buildings_by_year

CREATE TABLE census_de.residential_buildings_by_year (
	raster_id_100m varchar NOT NULL,
	total_buildings int4 NULL,
	pre_1919 int4 NULL,
	"1919_1948" int4 NULL,
	"1949_1978" int4 NULL,
	"1979_1990" int4 NULL,
	"1991_2000" int4 NULL,
	"2001_2010" int4 NULL,
	"2011_2019" int4 NULL,
	post_2020 int4 NULL,
	CONSTRAINT residential_buildings_by_year_pk PRIMARY KEY (raster_id_100m)
);
CREATE INDEX ix_census_de_residential_buildings_by_year_raster_id_100m ON census_de.residential_buildings_by_year USING btree (raster_id_100m);

INSERT INTO
    census_de.residential_buildings_by_year (raster_id_100m, total_buildings, pre_1919, "1919_1948", "1949_1978", "1979_1990", "1991_2000", "2001_2010", "2011_2019", post_2020)
VALUES
    ('CRS3035RES100mN2923100E4224300',3,NULL,NULL,NULL,NULL,NULL,3.0,NULL,NULL),
    ('CRS3035RES100mN2923000E4224400',3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
    ('CRS3035RES100mN2923100E4224200',3,NULL,NULL,NULL,NULL,NULL,3.0,NULL,NULL);


-- Create table census_de.residential_heating_sources

CREATE TABLE
    census_de.residential_heating_sources (
        raster_id_100m varchar NOT NULL,
        total_buildings int4 NULL,
        gas int4 NULL,
        heating_oil int4 NULL,
        wood int4 NULL,
        biomass_biogas int4 NULL,
        solar_geothermal_heat_pumps int4 NULL,
        electricity int4 NULL,
        coal int4 NULL,
        district_heating int4 NULL,
        "none" int4 NULL,
        CONSTRAINT residential_heating_sources_pk PRIMARY KEY (raster_id_100m)
    );

CREATE INDEX ix_census_de_residential_heating_sources_raster_id_100m ON census_de.residential_heating_sources USING btree (raster_id_100m);

INSERT INTO
    census_de.residential_heating_sources (raster_id_100m, total_buildings, gas, heating_oil, wood, biomass_biogas, solar_geothermal_heat_pumps, electricity, coal, district_heating, "none")
VALUES
    ('CRS3035RES100mN2922800E4223800', 3, null, 3.0, null, null, null, null, null, null, null),
    ('CRS3035RES100mN2922800E4223900', 3, 3.0, null, null, null, null, null, null, null, null),
    ('CRS3035RES100mN2923000E4224200', 63, null, null, null, null, null, null, 63.0, null, null),
    ('CRS3035RES100mN2923000E4224300', 16, null, null, null, null, null, null, 16.0, null, null),
    ('CRS3035RES100mN2923000E4224400', 350, 207.0, null, null, null, null, null, 146.0, null, null),
    ('CRS3035RES100mN2923100E4224100', 54, null, null, null, null, null, null, null, 54.0, null),
    ('CRS3035RES100mN2923100E4224200', 238, null, null, null, null, null, null, 238.0, null, null),
    ('CRS3035RES100mN2923100E4224300', 180, null, null, null, null, null, null, 158.0, 26.0, null);