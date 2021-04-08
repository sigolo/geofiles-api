import os
from ..convertors.Convertor import Convertor
from pathlib import Path
from ...utils.command import CALL_ogr2_dxf, CALL_ogr2_shp
from ...utils.zip import make_zip
import shutil

class GeoJSONConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        source_dir, shp_tmp = self.get_output_path("")
        CALL_ogr2_shp(shp_tmp, self.path)
        if not Path(shp_tmp).is_dir():
            return False
        zip_path = make_zip(source_dir, source_dir + ".zip")
        if not Path(zip_path).exists():
            return False
        try:
            shutil.rmtree(shp_tmp)
        except Exception as e:
            print(f"unable to remove source folder of shapefile {self.path}")
        return zip_path

    def get_output_path(self, file_output_ext: str):
        source_dir, file_ext = os.path.splitext(self.path)
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        tmp_file_path = os.path.join(os.path.dirname(source_dir), f"{file_name}{file_output_ext}")
        return [source_dir, tmp_file_path]

    def to_cad(self):
        source_dir, dxf_tmp = self.get_output_path(".dxf")
        return CALL_ogr2_dxf(dxf_tmp, source_dir)

    def to_geojson(self):
        return self.path

    def to_csv(self):
        pass
