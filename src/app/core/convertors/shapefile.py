import os
from ..convertors.Convertor import Convertor
from zipfile import ZipFile
from pathlib import Path
import subprocess
import shutil


class ShapeFileConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        pass

    def to_dwg(self):
        pass

    def to_geojson(self):
        source_dir, file_ext = os.path.splitext(self.path)
        json_tmp = os.path.join(source_dir, "temp.json")
        try:
            with ZipFile(self.path, "r") as zip_ref:
                zip_ref.extractall(source_dir)
            for file in os.listdir(source_dir):
                if file.endswith(".shp"):
                    shape_file_path = os.path.join(source_dir, file)
                    return_code = subprocess.call(["ogr2ogr", "-f", "GeoJSON", json_tmp, shape_file_path])
                    if not return_code == 0 or not Path(json_tmp).exists():
                        return False
                    try:
                        with open(json_tmp, 'r') as geojson:
                            return geojson.read()
                    except FileNotFoundError as e:
                        print(e)
                        return False
        except Exception as e:
            print(e)
            return
        finally:
            if Path(source_dir).is_dir():
                shutil.rmtree(source_dir)

    def to_csv(self):
        pass
