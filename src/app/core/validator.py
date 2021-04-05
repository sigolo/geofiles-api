import json
import os
from pathlib import Path
from geojson_pydantic.features import FeatureCollection
from pydantic import ValidationError
from ..utils.Exceptions import raise_422_exception
from zipfile import ZipFile


def validate_file(path, extension):
    validator = Validator(path, extension)
    if not validator.validate():
        raise_422_exception()
        return False
    return True


class SupportedFormat:
    SHP = "SHP"
    DWG = "DWG"
    GEOJSON = "GEOJSON"
    CSV = "CSV"

    @classmethod
    def get_available_format(cls, input_format: str):
        all_format = [SupportedFormat.SHP, SupportedFormat.DWG, SupportedFormat.GEOJSON, SupportedFormat.CSV]
        all_format.remove(input_format)
        all_format.sort()
        return all_format


class Validator:
    SUPPORTED_FORMAT = {".zip": SupportedFormat.SHP, ".dwg": SupportedFormat.DWG, ".json": SupportedFormat.GEOJSON,
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
        if self.file_type == SupportedFormat.DWG:
            raise NotImplementedError("DWG Validator Not implemented")
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
