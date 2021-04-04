import os

from .db_models import Files as UploadTable
from .db_engine import database
from ..api.schemas import TokenData
from fastapi import UploadFile
import aiofiles
import uuid
import datetime
from pathlib import Path
from ..utils.validator import Validator, validate_file



async def create(file: UploadFile, file_extension: str, user: TokenData):
    # Write the file
    file_uuid = uuid.uuid4()
    upload_path = os.path.join("app/uploads", str(file_uuid) + file_extension)
    async with aiofiles.open(upload_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    # If file successfully written
    if Path(upload_path).exists() and validate_file(upload_path, file_extension):
        expiration_time: int = int(os.getenv("FILE_EOL")) if os.getenv("FILE_EOL") else 15
        eol = datetime.datetime.now() + datetime.timedelta(minutes=expiration_time)

        query = UploadTable.insert().values(id=file_uuid, type=Validator.SUPPORTED_FORMAT[file_extension],
                                            user_id=user["user_id"],
                                            path=upload_path, eol=eol)
        await database.execute(query=query)
        await refresh_expired()
        return file_uuid
    # Else return False
    return False


async def refresh_expired():
    query = UploadTable.select().where(UploadTable.c.eol < datetime.datetime.now())
    expired_files = await database.fetch_all(query=query)
    for f in expired_files:
        file_path = Path(f.get("path"))
        if not file_path.exists():
            print("file not found")
        file_path.unlink()
        await delete(f.get("id"))


async def delete(file_uid: str):
    query = UploadTable.delete().where(UploadTable.c.id == file_uid)
    return await database.execute(query=query)

