# Geo files API

#### A REST API for converting between most popular geographic files type

---

#### Summary

---

This product aims to make conversions between differents geographic files format easier.
It consumes two very popular open source libraries behind the scenes :

- [GDAL / ogr2ogr][1]
- [LibreDWG][2]

It also makes use of [FastAPI][3] as the REST framwork (I used it with pydantic models - such as [geojson-pydantic][4])
It has a token validation built in. For this validation you can use the users-api and the oauth-api of micro-gis organisation.

#### Installation

---

After installing Docker and docker-compose, download this repository and simply runs the command `docker-compose up`

Since this API uploads files and save them (with a path reference on PostgreSQL) you can define a lifetime for those files : simply update the `FILE_EOL` environment variable in the _docker-compose.yml_ file.


[1]: https://gdal.org/programs/ogr2ogr.html
[2]: https://github.com/LibreDWG/libredwg
[3]: https://fastapi.tiangolo.com/
[4]: https://github.com/developmentseed/geojson-pydantic
