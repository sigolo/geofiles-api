import os
import shutil

from ..convertors.Convertor import Convertor
import json
from pathlib import Path
import subprocess
from ...utils.command import CALL_ogr2_geojson, CALL_ogr2_shp, CALL_ldwg_read_to_dxf
from ...utils.zip import make_zip


class DwgConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        source_dir, shp_tmp_folder = self.get_output_path("")
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        candidate = self.path
        if ext == ".dwg":
            candidate = os.path.join(source_dir, f"{file_name}.dxf")
            CALL_ldwg_read_to_dxf(candidate, self.path)
        CALL_ogr2_shp(shp_tmp_folder, candidate)
        if not Path(shp_tmp_folder).is_dir():
            return False
        zip_path = make_zip(source_dir, source_dir + ".zip")
        if not Path(zip_path).exists():
            return False
        try:
            shutil.rmtree(shp_tmp_folder)
        except Exception as e:
            print(f"unable to remove source folder of shapefile {self.path}")
        return zip_path

    def get_output_path(self, file_output_ext: str):
        source_dir, file_ext = os.path.splitext(self.path)
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        tmp_file_path = os.path.join(os.path.dirname(source_dir), f"{file_name}{file_output_ext}")
        return [source_dir, tmp_file_path]

    def to_cad(self):
        return self.path

    def to_geojson(self):
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        source_dir = os.path.dirname(self.path)
        json_tmp = os.path.join(source_dir, f"{file_name}.json")
        candidate = self.path
        try:
            if ext == ".dwg":
                candidate = os.path.join(source_dir, f"{file_name}.dxf")
                CALL_ldwg_read_to_dxf(candidate, self.path)
            command = CALL_ogr2_geojson(json_tmp, candidate)
            if not command.returncode == 0 or not Path(json_tmp).exists():
                return False
            try:
                with open(json_tmp, 'r') as fp:
                    json_dict = json.loads(fp.read())
                    if "features" not in json_dict:
                        print("invalid GeoJSON")
                        return False
                    try:
                        json_dict["features"] = [feature for feature in json_dict["features"]
                                                 if feature["geometry"] is not None]
                    except KeyError as e:
                        print(e)
                        return False
                with open(json_tmp, 'w') as fp:
                    json.dump(json_dict, fp=fp)
                return json_tmp
            except Exception as e:
                print(e)
                return False
        except Exception as e:
            print(e)
            return False

    def to_csv(self):
        pass
