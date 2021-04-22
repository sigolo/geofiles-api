import os
import uuid
from ..validator import SupportedFormat
from ..convertors.shapefile import ShapeFileConvertor
from ..convertors.geojson import GeoJSONConvertor
from ..convertors.cad import DwgConvertor
from ...api.schemas import FileRecord
from ...db import files as files_repository


async def convert_to_geojson(file: FileRecord, stream: bool = True):
    file_exists = await files_repository.get_one_by_source_id(file.id, SupportedFormat.GEOJSON)
    if file_exists:
        if stream:
            with open(file_exists.get("path"), 'r') as geojson:
                return geojson.read()
        return file_exists.get("path")
    json_path = None
    if file.type == SupportedFormat.SHP:
        json_path = ShapeFileConvertor(file.path).to_geojson()
    if file.type == SupportedFormat.GEOJSON:
        json_path = file.path
    if file.type == SupportedFormat.CAD:
        json_path = DwgConvertor(file.path).to_geojson()
    try:
        if not json_path:
            return False
        await persist_converted_file(file, json_path, "json", SupportedFormat.GEOJSON)
        if stream:
            with open(json_path, 'r') as geojson:
                return geojson.read()
        return json_path
    except FileNotFoundError as e:
        print(e)
        return False


async def convert_to_cad(file: FileRecord):
    file_exists = await files_repository.get_one_by_source_id(file.id, SupportedFormat.CAD)
    if file_exists:
        return file_exists.get("path")
    dxf_path = None
    if file.type == SupportedFormat.SHP:
        dxf_path = ShapeFileConvertor(file.path).to_cad()
    if file.type == SupportedFormat.GEOJSON:
        dxf_path = GeoJSONConvertor(file.path).to_cad()
    if file.type == SupportedFormat.CAD:
        dxf_path = file.path
    if not dxf_path:
        return False
    await persist_converted_file(file, dxf_path, "dxf", SupportedFormat.CAD)
    return dxf_path


async def convert_to_shp(file: FileRecord):
    file_exists = await files_repository.get_one_by_source_id(file.id, SupportedFormat.CAD)
    if file_exists:
        return file_exists.get("path")
    shp_path = None
    if file.type == SupportedFormat.SHP:
        shp_path = file.path
    if file.type == SupportedFormat.GEOJSON:
        shp_path = GeoJSONConvertor(file.path).to_shp()
    if file.type == SupportedFormat.CAD:
        shp_path = DwgConvertor(file.path).to_shp()
    if not shp_path:
        return False
    await persist_converted_file(file, shp_path, "zip", SupportedFormat.SHP)
    return shp_path


async def persist_converted_file(file: FileRecord, file_path, file_ext, file_type):
    file_uuid = uuid.uuid4()
    file_name = os.path.splitext(file.file_name)[0]
    await files_repository.insert(file_uuid=file_uuid,
                                  file_type=file_type,
                                  user_id=file.user_id,
                                  path=file_path,
                                  file_name=f"{file_name}.{file_ext}",
                                  source_id=file.id)
