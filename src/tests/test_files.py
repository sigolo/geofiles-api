import pytest
from fastapi import status
from starlette.testclient import TestClient
from pathlib import Path

from ..app.utils import token

JSON_VALID_FILE = "test.json"
NOT_SUPPORTED_FILE = "test.png"


@pytest.mark.parametrize(
    "path_to_file, access_token, token_data, expected_status_code",
    [
        [JSON_VALID_FILE, "some-valid-token", {"username": "john", "user_id": 1}, status.HTTP_201_CREATED],
        [JSON_VALID_FILE, None, None, status.HTTP_401_UNAUTHORIZED],
        [NOT_SUPPORTED_FILE, "some-valid-token", {"username": "john", "user_id": 1},
         status.HTTP_422_UNPROCESSABLE_ENTITY],
    ]
)
def test_retrieve_layer(test_app: TestClient, monkeypatch, path_to_file: str, access_token: str, token_data,
                        expected_status_code: int):
    path_to_file = Path('tests/resources', path_to_file)
    assert path_to_file.exists()
    files_payload = {'file': path_to_file.open('rb')}

    async def mock_check_credentials(token: str):
        return token_data

    test_app.headers["access-token"] = access_token
    monkeypatch.setattr(token, "check_user_credentials", mock_check_credentials)
    response = test_app.post('/files/upload/', files=files_payload)
    assert response.status_code == expected_status_code
