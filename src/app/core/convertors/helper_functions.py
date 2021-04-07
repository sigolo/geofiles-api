from ..validator import SupportedFormat
from ..convertors.shapefile import ShapeFileConvertor
from ..convertors.dwg import DwgConvertor


def convert_to_geojson(file_type, file_path):
    geojson_response = None

    if file_type == SupportedFormat.SHP:
        geojson_response = ShapeFileConvertor(file_path).to_geojson()
    if file_type == SupportedFormat.GEOJSON:
        with open(file_path) as fp:
            geojson_response = fp.read()
    if file_type == SupportedFormat.DWG:
        print("DWG before")
        geojson_response = DwgConvertor(file_path).to_geojson()
    return geojson_response
