import json
import os
from pathlib import Path
from geojson_pydantic.features import FeatureCollection
from pydantic import ValidationError
from .Exceptions import raise_422_exception


def validate_file(path, extension):
    if Validator.SUPPORTED_FORMAT[extension] == SupportedFormat.GEOJSON:
        validator = Validator(path, extension)
        if not validator.validate():
            raise_422_exception()
        return True
    print("WARNING: validator not implemented yet")
    return True


class SupportedFormat():
    SHP = "SHP"
    DWG = "DWG"
    GEOJSON = "GEOJSON"
    CSV = "CSV"


class Validator():
    SUPPORTED_FORMAT = {".shp": SupportedFormat.SHP, ".dwg": SupportedFormat.DWG, ".json": SupportedFormat.GEOJSON,
                        ".csv": SupportedFormat.CSV}

    def __init__(self, file_path: str, file_type: str):
        self.file_path = Path(file_path)
        self.file_type = self.SUPPORTED_FORMAT[file_type]

    def validate(self) -> bool:
        if self.file_type == SupportedFormat.SHP:
            raise NotImplementedError("SHP Validator Not implemented")
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
