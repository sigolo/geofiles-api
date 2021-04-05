import json
import os

import shapefile
from ..convertors.Convertor import Convertor
from zipfile import ZipFile
from pathlib import Path
from bs4 import UnicodeDammit
import subprocess


class ShapeFileConvertor(Convertor):



    def __init__(self, path):
        self.path = path

    def to_shp(self):
        pass

    def to_dwg(self):
        pass

    def to_geojson(self):
        TMP_FILE= "app/uploads/temp.json"
        try:
            filename, file_ext = os.path.splitext(self.path)
            with ZipFile(self.path, "r") as zip_ref:
                zip_ref.extractall(filename)
            for file in os.listdir(filename):
                if file.endswith(".shp"):
                    shape_file_path = os.path.join(filename, file)
                    return_code = subprocess.call(["ogr2ogr", "-f", "GeoJSON", TMP_FILE, shape_file_path])
                    if return_code == 0:
                        with open(TMP_FILE, 'r') as geojson:
                            return geojson.read()
        except Exception as e:
            print(e)
            return

    def to_csv(self):
        pass
