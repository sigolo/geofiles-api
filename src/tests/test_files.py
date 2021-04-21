import datetime

import pytest
import os
from fastapi import status, UploadFile
from starlette.testclient import TestClient
from pathlib import Path

from ..app.api.schemas import TokenData
from ..app.utils import Exceptions
from ..app.utils.http import HTTPFactory
from ..app.core import validator
from ..app.db import files as files_repository
from ..app.utils.env import ACCESS_TOKEN_KEY

import uuid

JSON_VALID_FILE = "test.json"
JSON_INVALID_FILE = "test_invalid.json"
NOT_SUPPORTED_FILE = "test.png"


@pytest.mark.parametrize(
    "path_to_file, access_token, token_data, expected_status_code",
    [
        [JSON_VALID_FILE, "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_201_CREATED],
        [JSON_VALID_FILE, None, None, status.HTTP_401_UNAUTHORIZED],
        [JSON_INVALID_FILE, "some-valid-token", {"username": "john", "user_id": 1},
         status.HTTP_422_UNPROCESSABLE_ENTITY],
        [NOT_SUPPORTED_FILE, "some-valid-token", {"username": "john", "user_id": 1},
         status.HTTP_422_UNPROCESSABLE_ENTITY],
    ]
)
def test_upload_file(test_app: TestClient, monkeypatch, path_to_file: str, access_token: str, token_data,
                     expected_status_code: int):
    path_to_file = Path('tests/resources', path_to_file)
    assert path_to_file.exists()
    files_payload = {'file': path_to_file.open('rb')}

    async def mock_check_credentials(token_string: str):
        if access_token:
            return token_data, access_token
        return None, None

    async def mock_create(file: UploadFile, file_extension: str, user: TokenData):
        if validator.validate_file(path_to_file, path_to_file.suffix):
            return uuid.uuid4()
        raise Exceptions.raise_422_exception()

    test_app.headers[ACCESS_TOKEN_KEY] = access_token
    monkeypatch.setattr(HTTPFactory.instance, "check_user_credentials", mock_check_credentials)
    monkeypatch.setattr(files_repository, "create_from_request", mock_create)
    response = test_app.post('/files/upload/', files=files_payload)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "file_uuid, file_record, access_token,token_data, expected_status_code",
    [
        ["some_valid_uuid",
         {"id": uuid.uuid4(), "user_id": 1, "path": os.path.join('tests/resources', JSON_VALID_FILE),
          "file_name": JSON_VALID_FILE,
          "type": "GEOJSON", "source_id": None, "eol": datetime.datetime.now()},
         "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_200_OK],
        ["some_expired_uuid",
         None,
         "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_410_GONE],
        ["some_valid_uuid",
         {"user_id": 1, "path": os.path.join('tests/resources', JSON_VALID_FILE), "file_name": JSON_VALID_FILE},
         "some-valid-token-from-other-user", {"username": "not_john", "user_id": 2}, status.HTTP_401_UNAUTHORIZED],
        [None, None, "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_410_GONE],
    ]
)
def test_download_file(test_app: TestClient, monkeypatch, file_uuid, file_record, access_token, token_data,
                       expected_status_code: int):
    async def mock_check_credentials(token_string: str):
        if access_token:
            return token_data, access_token
        return None, None

    async def mock_get_one(file_uuid: str):
        return file_record

    test_app.headers[ACCESS_TOKEN_KEY] = access_token
    monkeypatch.setattr(HTTPFactory.instance, "check_user_credentials", mock_check_credentials)
    monkeypatch.setattr(files_repository, "get_one", mock_get_one)
    response = test_app.get(f"/files/{file_uuid}")
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "file_uuid, file_record, expected_download_types, access_token,token_data, expected_status_code",
    [
        ["some_valid_uuid",
         {"id": uuid.uuid4(), "user_id": 1, "path": os.path.join('tests/resources', JSON_VALID_FILE),
          "file_name": JSON_VALID_FILE,
          "type": "GEOJSON", "source_id": None, "eol": datetime.datetime.now()}, ['CAD', 'SHP'],
         "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_200_OK],
        ["some_valid_uuid",
         {"id": uuid.uuid4(), "user_id": 1, "path": os.path.join('tests/resources', JSON_VALID_FILE),
          "file_name": JSON_VALID_FILE,
          "type": "SHP", "source_id": None, "eol": datetime.datetime.now()}, ['CAD', 'GEOJSON'],
         "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_200_OK],
        ["some_valid_uuid",
         {"id": uuid.uuid4(), "user_id": 1, "path": os.path.join('tests/resources', JSON_VALID_FILE),
          "file_name": JSON_VALID_FILE,
          "type": "CAD", "source_id": None, "eol": datetime.datetime.now()}, ['GEOJSON', 'SHP'],
         "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_200_OK],
    ]
)
def test_retrieve_download_format(test_app: TestClient, monkeypatch, file_uuid, file_record, expected_download_types,
                                  access_token, token_data,
                                  expected_status_code: int):
    async def mock_check_credentials(token_string: str):
        if access_token:
            return token_data, access_token
        return None, None

    async def mock_get_one(file_uuid: str):
        return file_record

    test_app.headers[ACCESS_TOKEN_KEY] = access_token
    monkeypatch.setattr(HTTPFactory.instance, "check_user_credentials", mock_check_credentials)
    monkeypatch.setattr(files_repository, "get_one", mock_get_one)
    response = test_app.get(f"/files/{file_uuid}/format")
    expected_download_types = [f"/{file_uuid}/to{export_format}" for export_format in expected_download_types]
    assert response.status_code == expected_status_code
    assert response.json() == expected_download_types


@pytest.mark.parametrize(
    "access_token, token_data, retrieved_files, expected_status_code",
    [["some_valid_token", {"username": "john", "user_id": 1}, [{
        "id": "944abf17-c113-4583-bcca-2ac1269b435e",
        "eol": "2021-04-19T14:01:12.287151",
        "type": "SHP",
        "file_name": "valid_shp (3).zip"
    }], status.HTTP_200_OK],
     [None, {"username": "john", "user_id": 1}, [], status.HTTP_401_UNAUTHORIZED]]
)
def test_retrieve_files(test_app: TestClient, monkeypatch, access_token, token_data, retrieved_files,
                        expected_status_code):
    async def mock_check_credentials(token_string: str):
        if access_token:
            return token_data, access_token
        return None, None

    async def mock_retrieve_users_files(token: str):
        return retrieved_files

    test_app.headers[ACCESS_TOKEN_KEY] = access_token
    monkeypatch.setattr(HTTPFactory.instance, "check_user_credentials", mock_check_credentials)
    monkeypatch.setattr(files_repository, "retrieve_users_files", mock_retrieve_users_files)
    response = test_app.get(f"/files/")
    assert response.status_code == expected_status_code
