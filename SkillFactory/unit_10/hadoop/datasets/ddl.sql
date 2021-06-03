-------------------------------------------------------countries_of_the_world-------------------------------------------------------------
--Index(['Country', 'Region', 'Population', 'Area (sq. mi.)',
--       'Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)',
--       'Net migration', 'Infant mortality (per 1000 births)',
--       'GDP ($ per capita)', 'Literacy (%)', 'Phones (per 1000)', 'Arable (%)',
--       'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate',
--       'Agriculture', 'Industry', 'Service'],
--      dtype='object')

-- DROP TABLE dwh_polygon.countries_of_the_world;

CREATE TABLE dwh_polygon.countries_of_the_world (
	coutry varchar(1024) NULL,
	region varchar(1024) NULL,
	population int4 NULL,
	area int4 NULL,
	pop_density numeric(10,3) NULL,
	coastline numeric(10,3) NULL,
	net_migration numeric(10,3) NULL,
	infant_mortality numeric(10,3) NULL,
	gdp numeric(10,1) NULL,
	literacy numeric(10,3) NULL,
	phones numeric(10,3) NULL,
	arable numeric(10,3) NULL,
	crops numeric(10,3) NULL,
	other numeric(10,3) NULL,
	climate numeric(5,1) NULL,
	birthrate numeric(10,3) NULL,
	deathrate numeric(10,3) NULL,
	agriculture numeric(10,3) NULL,
	industry numeric(10,3) NULL,
	service numeric(10,3) NULL
);

-------------------------------------------------------Country_Data-------------------------------------------------------------
------------------------------------------continent----------------------------------------
-- DROP TABLE dwh_polygon.continent;

CREATE TABLE dwh_polygon.continent (
	country varchar(1024) NULL,
	continent varchar(1024) NULL
);

------------------------------------------currency----------------------------------------
-- DROP TABLE dwh_polygon.currency;

CREATE TABLE dwh_polygon.currency (
	country varchar(1024) NULL,
	currency varchar(1024) NULL
);

------------------------------------------iso3----------------------------------------
-- DROP TABLE dwh_polygon.iso3;

CREATE TABLE dwh_polygon.iso3 (
	country varchar(1024) NULL,
	iso3 varchar(1024) NULL
);

------------------------------------------country_name----------------------------------------
-- DROP TABLE dwh_polygon.country_name;

CREATE TABLE dwh_polygon.country_name (
	country varchar(1024) NULL,
	country_name varchar(1024) NULL
);

------------------------------------------country_phone_code----------------------------------------
-- DROP TABLE dwh_polygon.country_phone_code;

CREATE TABLE dwh_polygon.country_phone_code (
	country varchar(1024) NULL,
	phone_code varchar(1024) NULL
);

-------------------------------------------------------worldcitiespop-----------------------------------------------------------
-- DROP TABLE dwh_polygon.worldcitiespop;

CREATE TABLE dwh_polygon.worldcitiespop (
	country varchar(1024) NULL,
	city varchar(1024) NULL,
	accentcity varchar(1024) NULL,
	region varchar(100) NULL,
	latitude float8 NULL,
	longitude float8 NULL
);

-------------------------------------------------------nobel-----------------------------------------------------------
-- DROP TABLE dwh_polygon.nobel;

CREATE TABLE dwh_polygon.nobel (
	iyear int4 NULL,
	category varchar(100) NULL,
	prize varchar(100) NULL,
	motivation varchar(1024) NULL,
	prize_share varchar(100) NULL,
	laureate_id int4 NULL,
	laureate_type varchar(100) NULL,
	full_name varchar(100) NULL,
	birth_date varchar(100) NULL,
	birth_city varchar(100) NULL,
	birth_country varchar(100) NULL,
	sex varchar(100) NULL,
	organization_name varchar(300) NULL,
	organization_city varchar(100) NULL,
	organization_country varchar(100) NULL,
	death_date varchar(100) NULL,
	death_city varchar(100) NULL,
	death_country varchar(100) NULL
);
