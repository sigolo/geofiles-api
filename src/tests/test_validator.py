import os

import pytest
from starlette.testclient import TestClient
from ..app.core.validator import Validator

GEOJSON_VALID_FILE = "test.json"
GEOJSON_INVALID_FILE = "test_invalid.json"


@pytest.mark.parametrize(
    "path_to_file, file_type, expected_output",
    [
        [GEOJSON_VALID_FILE, ".json", True],
        [GEOJSON_INVALID_FILE, ".json", False],
    ]
)
def test_upload_file(test_app: TestClient, monkeypatch, path_to_file, file_type, expected_output):
    path = os.path.join('tests/resources', path_to_file)
    is_valid = Validator(path, file_type)
    assert is_valid.validate() == expected_output
