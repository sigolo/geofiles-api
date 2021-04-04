from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, Header
from ..db import files as files_repository

from ..utils.Exceptions import raise_422_exception, raise_401_exception
from ..utils import token
from ..utils.validator import Validator

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
    fileUUID = await files_repository.create(file, file_extension, user)
    return fileUUID
