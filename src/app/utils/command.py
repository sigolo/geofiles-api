import subprocess


def CALL_ogr2_geojson(output_json_path, source_path):
    return subprocess.run(["ogr2ogr", "-f", "GeoJSON", output_json_path, source_path])


def CALL_ogr2_dxf(output_dxf_path, source_path):
    return subprocess.run(["ogr2ogr", "-f", "DXF", output_dxf_path, source_path])


def CALL_ogr2_shp(output_shp_path, source_path):
    return subprocess.run(["ogr2ogr", "-f", "ESRI Shapefile", output_shp_path, source_path, "-lco", "ENCODING=UTF-8"])


def CALL_ldwg_read_geojson(output_json_tmp, dwg_path):
    return subprocess.run(["dwgread", dwg_path, "-O", "GeoJSON", "-o", output_json_tmp])

def CALL_ldwg_read_to_dxf(output_dxf_tmp, dwg_path):
    return subprocess.run(["dwgread", dwg_path, "-O", "DXF", "-o", output_dxf_tmp])