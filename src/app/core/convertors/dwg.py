import os
from ..convertors.Convertor import Convertor
import json
from pathlib import Path
import subprocess

class DwgConvertor(Convertor):

    def __init__(self, path):
        if not Path(path).exists():
            print("path error")
            raise FileNotFoundError(f"the provided path {self.path} was not found")
        self.path = path

    def to_shp(self):
        pass

    def to_dwg(self):
        pass

    def to_geojson(self):
        source_dir, file_ext = os.path.splitext(self.path)
        json_tmp = os.path.join(source_dir, "temp.json")
        try:
            return_code = subprocess.call(["dwgread", self.path, "-O", "GeoJSON", "-o", json_tmp])
            print("DWG after")
            if not return_code == 0 :
                print("Return dwgread error")
                return False
            if not Path(json_tmp).exists():
                print("Return path error : ", json_tmp)
                print("list dir : ", os.listdir("app/uploads"))
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
                        return json.dumps(json_dict)
                    except KeyError as e:
                        print(e)
                        return False
            except Exception as e:
                print(e)
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            if Path(json_tmp).exists():
                Path(json_tmp).unlink()

    def to_csv(self):
        pass
