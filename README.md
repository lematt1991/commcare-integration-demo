Commcare Integration Demo
-------------------------

This file contains the necessary instructions to reproduce the Commcare integration demo.

## Setup 

There are a few dependencies that will need to be installed

- [Python](https://www.python.org/downloads/) (2.7) and pip
- [PostgreSQL](https://www.postgresql.org/download)
- [PostGIS](http://postgis.net/)

To install python dependencies:

```
pip install -r requirements.txt
``` 

## Database setup

- Create a database

```
createdb commcare-demo
```

- Create the PostGIS extension

```
psql commcare-demo -c "CREATE EXTENSION postgis;"
```


## Initialize the database

Create the `gps_case_data` table 

- Export the `GPS Case Data` repot as an Excel file from [Commcare HQ](https://www.commcarehq.org/a/atlas-api-demo/dashboard/project/)
- Save it in `commcare-integration-demo/data`
- Create the table in PostgreSQL

```
./mk_tables.py
```

## Save the schema for later (optional)

```
pg_dump commcare-demo --schema-only -f init.sql
```

## Update the database

```
./demo.py --update
```

## Adding support for spatial queries
Run the following commands in `psql`

- Create the geometry column 

```SQL
ALTER TABLE gps_case_data ADD COLUMN geom geometry('POINT', 4326);
```
- Fill in the `geom` column

```SQL
UPDATE gps_case_data SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
```

- Create an index on the `geom` column

```SQL
CREATE INDEX ON gps_case_data USING GIST(geom);
```

- Add the Guatemalan administrative areas (from terminal)

```
psql -f gtm_admin_areas.sql
```

- Run some spatial queries

```SQL
SELECT name_2 as muni, COUNT(name) FROM admin_areas
LEFT JOIN gps_case_data ON ST_Contains(admin_areas.geom, gps_case_data.geom)
GROUP BY muni ORDER BY COUNT(*) DESC;
```



















