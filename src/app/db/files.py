import os

from sqlalchemy import and_

from .db_models import Files as UploadTable
from .db_engine import database
from ..api.schemas import TokenData
from fastapi import UploadFile
import aiofiles
import uuid
import datetime
from pathlib import Path
from ..core.validator import Validator, validate_file
from pydantic.types import UUID
from ..utils.logs import RestLogger

def get_expiration_time():
    expiration_time: int = int(os.getenv("FILE_EOL")) if os.getenv("FILE_EOL") else 15
    return datetime.datetime.now() + datetime.timedelta(minutes=expiration_time)


async def insert(file_uuid, file_type, user_id, path, file_name, source_id=None):
    query = UploadTable.insert().values(id=file_uuid, type=file_type,
                                        user_id=user_id,
                                        path=path,
                                        file_name=file_name,
                                        source_id=source_id,
                                        eol=get_expiration_time())
    RestLogger.instance.log_sql_query(sql_query=query)
    return await database.execute(query=query)


async def create_from_request(file: UploadFile, file_extension: str, user: TokenData):
    # Write the file
    file_uuid = uuid.uuid4()
    upload_path = os.path.join("app/uploads", str(file_uuid) + file_extension)
    async with aiofiles.open(upload_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    # If file successfully written

    if Path(upload_path).exists() and validate_file(upload_path, file_extension):
        # Insert new row
        await insert(file_uuid, Validator.SUPPORTED_FORMAT[file_extension], user["user_id"], upload_path, file.filename)
        await refresh_expired()
        return file_uuid
    # Else return False
    return False


async def get_one(file_uuid: str):
    await refresh_expired()
    query = UploadTable.select().where(UploadTable.c.id == file_uuid)
    file_found = await database.fetch_all(query=query)
    RestLogger.instance.log_sql_query(sql_query=query, record_num=len(file_found))
    return file_found[0]


async def get_one_by_source_id(source_uuid: UUID, file_type):
    await refresh_expired()
    query = UploadTable.select().where(and_(UploadTable.c.source_id == source_uuid, UploadTable.c.type == file_type))
    file_found = await database.fetch_one(query=query)
    RestLogger.instance.log_sql_query(sql_query=query, record_num=len(file_found))
    return file_found


async def refresh_expired():
    query = UploadTable.select().where(UploadTable.c.eol < datetime.datetime.now())
    expired_files = await database.fetch_all(query=query)
    RestLogger.instance.log_sql_query(sql_query=query, record_num=len(expired_files))
    for f in expired_files:
        file_path = Path(f.get("path"))
        try:
            file_path.unlink()
        except FileNotFoundError as e:
            print(e)
        finally:
            await delete(f.get("id"))


async def delete(file_uid: str):
    query = UploadTable.delete().where(UploadTable.c.id == file_uid)
    return await database.execute(query=query)
