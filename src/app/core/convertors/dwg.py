import os
from ..convertors.Convertor import Convertor
import json
from pathlib import Path
import subprocess
import shutil


class DwgConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        pass

    def to_dwg(self):
        pass

    def to_geojson(self):
        json_tmp = os.path.join("app/uploads", "temp.json")
        try:
            return_code = subprocess.call(["dwgread", "-f", self.path, "-O", "GeoJSON", "-o", json_tmp])
            if return_code == 0 and Path(json_tmp).exists():
                with open(json_tmp, 'r') as fp:
                    json_dict = json.loads(fp.read())
                    if "features" in json_dict:
                        json_dict["features"] = [feature for feature in json_dict["features"] if feature["geometry"] is not None]
                    return json.dumps(json_dict)
        except Exception as e:
            print(e)
            return
        finally:
            if Path(json_tmp).exists():
                print("ok")
                # Path(json_tmp).unlink()

    def to_csv(self):
        pass
