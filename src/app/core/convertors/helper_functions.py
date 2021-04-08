import uuid
from typing import Mapping

from ..validator import SupportedFormat
from ..convertors.shapefile import ShapeFileConvertor
from ..convertors.dwg import DwgConvertor
from ...api.schemas import FileRecord
from ...db import files as files_repository


async def convert_to_geojson(file: FileRecord):
    file_exists = await files_repository.get_one_by_source_id(file.id, SupportedFormat.GEOJSON)
    if file_exists:
        with open(file_exists.get("path"), 'r') as geojson:
            return geojson.read()
    json_path = None
    if file.type == SupportedFormat.SHP:
        json_path = ShapeFileConvertor(file.path).to_geojson()
    if file.type == SupportedFormat.GEOJSON:
        json_path = file.path
    if file.type == SupportedFormat.DWG:
        json_path = DwgConvertor(file.path).to_geojson()
    try:
        if not json_path:
            return False
        file_uuid = uuid.uuid4()
        await files_repository.insert(file_uuid=file_uuid,
                                      file_type=SupportedFormat.GEOJSON,
                                      user_id=file.user_id,
                                      path=json_path,
                                      file_name=f"{file.file_name}.json",
                                      source_id=file.id)
        with open(json_path, 'r') as geojson:
            return geojson.read()

    except FileNotFoundError as e:
        print(e)
        return False
