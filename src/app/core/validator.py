import json
import os
import subprocess
from pathlib import Path
from geojson_pydantic.features import FeatureCollection
from pydantic import ValidationError
from ..utils.Exceptions import raise_422_exception
from ..utils.command import CALL_ldwg_read_geojson, CALL_ogr2_geojson
from ..utils.logs import log_function
from zipfile import ZipFile


def validate_file(path, extension):
    validator = Validator(path, extension)
    if not validator.validate():
        raise_422_exception()
        return False
    return True


class SupportedFormat:
    SHP = "SHP"
    CAD = "CAD"
    GEOJSON = "GEOJSON"
    CSV = "CSV"

    @classmethod
    def get_available_format(cls, input_format: str):
        all_format = [SupportedFormat.SHP, SupportedFormat.CAD, SupportedFormat.GEOJSON]
        all_format.remove(input_format)
        all_format.sort()
        return all_format


class Validator:
    SUPPORTED_FORMAT = {".zip": SupportedFormat.SHP, ".dxf": SupportedFormat.CAD, ".dwg":SupportedFormat.CAD,".json": SupportedFormat.GEOJSON,
                        ".csv": SupportedFormat.CSV}

    SHAPE_FILE_MANDATORY = [".dbf", ".shp", ".shx"]

    def __init__(self, file_path: str, file_type: str):
        self.file_path = Path(file_path)
        self.file_type = self.SUPPORTED_FORMAT[file_type]

    def validate(self) -> bool:
        if self.file_type == SupportedFormat.SHP:
            return self.validate_shapefile()
        if self.file_type == SupportedFormat.CSV:
            raise NotImplementedError("CSV Validator Not implemented")
        if self.file_type == SupportedFormat.CAD:
            return self.validate_dwg()
        if self.file_type == SupportedFormat.GEOJSON:
            return self.validate_geojson()

    def validate_geojson(self):
        if not self.file_path.exists():
            return False
        try:
            with open(self.file_path, 'r') as fp:
                candidate = json.loads(fp.read())
                try:
                    model = FeatureCollection.parse_raw(json.dumps(candidate))
                    return True
                except ValidationError as e:
                    print(json.dumps(candidate))
                    print(e)
                    return False
        except ValueError as err:
            return False

    def validate_dwg(self):
        json_tmp = os.path.join("app/uploads", "temp.json")
        try:
            select_command = CALL_ldwg_read_geojson if self.file_path.suffix == ".dwg" else CALL_ogr2_geojson
            command = select_command(json_tmp, self.file_path)
            if command.returncode == 0 and Path(json_tmp).exists():

                return True
            return False
        except Exception as e:
            print(e)
            return
        finally:
            if Path(json_tmp).exists():
                Path(json_tmp).unlink()

    def validate_shapefile(self):
        with ZipFile(self.file_path, 'r') as zipObject:
            list_of_file_names = zipObject.namelist()
            contained_files = []
            for file in list_of_file_names:
                file_name, file_ext = os.path.splitext(file)
                if file_ext in self.SHAPE_FILE_MANDATORY:
                    contained_files.append(file_ext)
            contained_files.sort()
            if contained_files == self.SHAPE_FILE_MANDATORY:
                return True
            return False
