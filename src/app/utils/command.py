import subprocess


def CALL_ogr2_geojson(output_json_path, source_path):
    return subprocess.run(["ogr2ogr", "-f", "GeoJSON", output_json_path, source_path])


def CALL_ogr2_dxf(output_dxf_path, source_path):
    print("SHP output", output_dxf_path)
    print("source path", source_path)
    return subprocess.run(["ogr2ogr", "-f", "DXF", output_dxf_path, source_path])


def CALL_ogr2_shp(output_shp_path, source_path):

    return subprocess.run(["ogr2ogr", "-f", "ESRI Shapefile", output_shp_path, source_path])


def CALL_ldwg_read_geojson(dwg_path, json_tmp):
    return subprocess.run(["dwgread", dwg_path, "-O", "GeoJSON", "-o", json_tmp])
