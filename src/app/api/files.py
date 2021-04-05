from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, Header
from ..db import files as files_repository

from ..utils.Exceptions import raise_422_exception, raise_401_exception, raise_404_exception
from ..utils import token
from ..utils.validator import Validator
from fastapi.responses import FileResponse
from pathlib import Path

import os

router = APIRouter()


@router.post("/upload/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(file: UploadFile = File(...), access_token: Optional[str] = Header(None)):
    if not access_token:
        raise_401_exception()
    filename, file_extension = os.path.splitext(file.filename)
    if file_extension not in Validator.SUPPORTED_FORMAT:
        raise_422_exception()
    user = await token.check_user_credentials(access_token)
    if not user:
        raise_401_exception()
    file_uuid = await files_repository.create(file, file_extension, user)
    return file_uuid


@router.get("/{file_uuid}", status_code=status.HTTP_201_CREATED)
async def download_file(file_uuid: str, access_token: Optional[str] = Header(None)):
    if not access_token:
        raise_401_exception()
    user = await token.check_user_credentials(access_token)
    if not user:
        raise_401_exception()
    file_record = await files_repository.get_one(file_uuid)
    if not file_record:
        raise_404_exception()
    if file_record.get("user_id") != user["user_id"]:
        raise_401_exception()
    if not Path(file_record.get("path")).exists():
        raise_404_exception()
    return FileResponse(
        file_record.get("path"), media_type='application/octet-stream', filename=file_record.get("file_name"))
