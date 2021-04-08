import os
from ..convertors.Convertor import Convertor
from zipfile import ZipFile
from pathlib import Path
from ...utils.command import CALL_ogr2_dxf, CALL_ogr2_geojson
import shutil


class ShapeFileConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        return self.path

    def get_output_path(self, file_output_ext: str):
        source_dir, file_ext = os.path.splitext(self.path)
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        tmp_file_path = os.path.join(os.path.dirname(source_dir), f"{file_name}.{file_output_ext}")
        return [source_dir, tmp_file_path]

    def extract_and_convert(self, target_output, source_dir, helper_function):
        if Path(target_output).exists():
            return target_output
        try:
            with ZipFile(self.path, "r") as zip_ref:
                zip_ref.extractall(source_dir)
            for file in os.listdir(source_dir):
                if file.endswith(".shp"):
                    shape_file_path = os.path.join(source_dir, file)
                    return_code = helper_function(target_output, shape_file_path)
                    if not return_code.returncode == 0 or not Path(target_output).exists():
                        return False
                    return target_output
        except Exception as e:
            print(e)
            return
        finally:
            if Path(source_dir).is_dir():
                shutil.rmtree(source_dir)

    def to_cad(self):
        source_dir, dxf_tmp = self.get_output_path("dxf")
        return self.extract_and_convert(dxf_tmp, source_dir, CALL_ogr2_dxf)

    def to_geojson(self):
        source_dir, json_tmp = self.get_output_path("json")
        return self.extract_and_convert(json_tmp, source_dir, CALL_ogr2_geojson)

    def to_csv(self):
        pass
