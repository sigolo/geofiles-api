# Geo files API

#### A REST API for converting between most popular geographic files type

---

#### Summary

---

This product aims to make conversions between differents geographic files format easier.
It consumes two very popular open source libraries behind the scenes :

- GDAL / ogr2ogr
- LibreDWG

It makes use also of FastAPI as the REST framwork (I used it with pydantic models - such as geojson-pydantic)
It has a token validation built in. For this validation you can use the users-api and the oauth-api of micro-gis organisation.

#### Installation

---

After installing Docker and docker-compose, download this repository and simply runs the command `docker-compose up`

Since this API uploads files and save them (with a path reference on PostgreSQL) you can define a lifetime for those files : simply update the `FILE_EOL` environment variable in the _docker-compose.yml_ file.
