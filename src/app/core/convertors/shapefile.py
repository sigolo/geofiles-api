import os
from ..convertors.Convertor import Convertor
from zipfile import ZipFile
from pathlib import Path
from ...db import files as files_repository
import subprocess
import shutil


class ShapeFileConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        pass

    async def to_dwg(self):
        json_dxf = os.path.join("app/uploads", "temp.dxf")
        file_id = os.path.basename(self.path)
        file_record = await files_repository.get_one(file_id)
        if not file_record:
            return False
        # command = subprocess.run(["ogr2ogr", "-f", "GeoJSON" - ])
        pass

    def to_geojson(self):
        source_dir, file_ext = os.path.splitext(self.path)
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        json_tmp = os.path.join(source_dir, f"{file_name}.json")
        try:
            with ZipFile(self.path, "r") as zip_ref:
                zip_ref.extractall(source_dir)
            for file in os.listdir(source_dir):
                if file.endswith(".shp"):
                    shape_file_path = os.path.join(source_dir, file)
                    return_code = subprocess.run(["ogr2ogr", "-f", "GeoJSON", json_tmp, shape_file_path])
                    if not return_code.returncode == 0 or not Path(json_tmp).exists():
                        return False
                    return json_tmp
        except Exception as e:
            print(e)
            return

    def to_csv(self):
        pass
