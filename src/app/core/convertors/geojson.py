import os
from inspect import getframeinfo, currentframe
from ..convertors.Convertor import Convertor
from pathlib import Path
from ...utils.command import CALL_ogr2_dxf, CALL_ogr2_shp
from ...utils.zip import make_zip
from ...utils.logs import log_function, LogLevel
import shutil


class GeoJSONConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        source_dir, shp_tmp = self.get_output_path("")
        CALL_ogr2_shp(shp_tmp, self.path)
        if not Path(shp_tmp).is_dir():
            log_function(GeoJSONConvertor.__name__,
                         GeoJSONConvertor.to_shp.__name__,
                         f"file : {self.path} conversion to {shp_tmp} failed",
                         getframeinfo(currentframe()).lineno, LogLevel.ERROR)
            return False
        zip_path = make_zip(source_dir, source_dir + ".zip")
        if not Path(zip_path).exists():
            log_function(GeoJSONConvertor.__name__,
                         GeoJSONConvertor.to_shp.__name__,
                         f"file : {self.path} conversion to zipfile failed",
                         getframeinfo(currentframe()).lineno, LogLevel.ERROR)
            return False
        try:
            shutil.rmtree(source_dir)
        except OSError as e:
            log_function(GeoJSONConvertor.__name__,
                         GeoJSONConvertor.to_shp.__name__,
                         str(e), getframeinfo(currentframe()).lineno, LogLevel.ERROR)
        return zip_path

    def get_output_path(self, file_output_ext: str):
        source_dir, file_ext = os.path.splitext(self.path)
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        tmp_file_path = os.path.join(os.path.dirname(source_dir), f"{file_name}{file_output_ext}")
        return [source_dir, tmp_file_path]

    def to_cad(self):
        source_dir, dxf_tmp = self.get_output_path(".dxf")
        CALL_ogr2_dxf(dxf_tmp, self.path)
        if not Path(dxf_tmp).exists():
            log_function(GeoJSONConvertor.__name__,
                         GeoJSONConvertor.to_shp.__name__,
                         f"file : {self.path} conversion to {dxf_tmp} failed",
                         getframeinfo(currentframe()).lineno, LogLevel.ERROR)
            return False
        return dxf_tmp

    def to_geojson(self):
        if not Path(self.path).exists():
            log_function(GeoJSONConvertor.__name__,
                         GeoJSONConvertor.to_shp.__name__,
                         f"file : {self.path} does not exists anymore",
                         getframeinfo(currentframe()).lineno, LogLevel.ERROR)
            return False
        return self.path

    def to_csv(self):
        pass
