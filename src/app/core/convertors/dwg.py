import os
from ..convertors.Convertor import Convertor
import json
from pathlib import Path
import subprocess

class DwgConvertor(Convertor):

    def __init__(self, path):
        self.path = path

    def to_shp(self):
        pass

    def to_dwg(self):


        pass

    def to_geojson(self):
        file_name, ext = os.path.splitext(os.path.basename(self.path))
        source_dir = os.path.dirname(self.path)
        json_tmp = os.path.join(source_dir, f"{file_name}.json")
        try:
            command = subprocess.run(["dwgread", self.path, "-O", "GeoJSON", "-o", json_tmp])
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
