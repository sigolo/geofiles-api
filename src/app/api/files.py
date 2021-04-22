from typing import Optional, List

from fastapi import APIRouter, status, UploadFile, File, Header, Request
from ..db import files as files_repository

from ..utils.Exceptions import raise_422_exception, raise_401_exception, raise_404_exception, raise_410_exception
from ..utils.http import HTTPFactory
from ..core.validator import Validator, SupportedFormat
from ..core.convertors.helper_functions import convert_to_geojson as to_geojson, convert_to_cad as to_cad, \
    convert_to_shp as to_shp
from fastapi.responses import FileResponse
from pathlib import Path
from geojson_pydantic.features import FeatureCollection

from .schemas import FileRecord, PublicFile
import os

router = APIRouter()


async def file_request_handler(file_uuid: str, request: Request, token: Optional[str] = Header(None)):
    if not request.state.user:
        raise_401_exception()
    file_record = await files_repository.get_one(file_uuid)
    if not file_record:
        raise_410_exception()
    if file_record.get("user_id") != request.state.user["user_id"]:
        raise_401_exception()
    if not Path(file_record.get("path")).exists():
        raise_410_exception()
    return FileRecord.parse_obj(dict(file_record))


@router.post("/upload/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(request: Request, file: UploadFile = File(...),
                             token: Optional[str] = Header(None)):
    filename, file_extension = os.path.splitext(file.filename)
    if file_extension not in Validator.SUPPORTED_FORMAT:
        raise_422_exception()
    if not request.state.user:
        raise_401_exception()
    file_uuid = await files_repository.create_from_request(file, file_extension, request.state.user)
    return file_uuid


@router.get("/{file_uuid}", status_code=status.HTTP_200_OK)
async def download_file(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    return FileResponse(
        file_record.path, media_type=SupportedFormat.get_mime_type(file_record.type), filename=file_record.file_name)


@router.get("/{file_uuid}/format", status_code=status.HTTP_200_OK)
async def get_allowed_formats(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    available_format = SupportedFormat.get_available_format(file_record.type)
    urls = [f"/{file_uuid}/to{export_format}" for export_format in available_format]
    return urls


@router.get("/{file_uuid}/toGEOJSON", response_model=FeatureCollection, status_code=status.HTTP_200_OK)
async def convert_to_geojson(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    geojson_response = await to_geojson(file_record, stream=False)
    if not geojson_response:
        raise_422_exception()
    file_name = f"{os.path.splitext(file_record.file_name)[0]}.json"
    return FileResponse(
        geojson_response, media_type='application/json', filename=file_name)


@router.get("/{file_uuid}/toCAD", status_code=status.HTTP_200_OK)
async def convert_to_dwg(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    dwg_response = await to_cad(file_record)
    if not dwg_response:
        raise_422_exception()
    file_name = f"{os.path.splitext(file_record.file_name)[0]}.dxf"
    return FileResponse(
        dwg_response, media_type='application/dxf', filename=file_name)


@router.get("/{file_uuid}/toSHP", status_code=status.HTTP_200_OK)
async def convert_to_shp(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    shp_response = await to_shp(file_record)

    if not shp_response:
        raise_422_exception()
    file_name = f"{os.path.splitext(file_record.file_name)[0]}.zip"
    return FileResponse(
        shp_response, media_type='application/zip', filename=file_name)


@router.get("/{file_uuid}/stream/geojson", response_model=FeatureCollection, status_code=status.HTTP_200_OK)
async def convert_to_geojson(request: Request, file_uuid: str, token: Optional[str] = Header(None)):
    file_record = await file_request_handler(file_uuid, request)
    geojson_response = await to_geojson(file_record, stream=True)
    if not geojson_response:
        raise_422_exception()
    return FeatureCollection.parse_raw(geojson_response)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PublicFile])
async def retrieve_users_files(request: Request, token: Optional[str] = Header(None)):
    if not request.state.user:
        raise_401_exception()
    users_files = await files_repository.retrieve_users_files(request.state.user["user_id"])
    return users_files
