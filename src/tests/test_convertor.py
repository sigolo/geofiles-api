import os

import pytest
from starlette.testclient import TestClient
from ..app.core.convertors.helper_functions import convert_to_geojson
from ..app.core.validator import SupportedFormat

VALID_SHP = "valid_shp.zip"
INVALID_SHP = "invalid_shp.zip"
VALID_DWG = "valid.dwg"
INVALID_DWG = "invalid.dwg"

GEOJSON_INVALID_FILE = "test_invalid.json"


@pytest.mark.parametrize(
    "path_to_file, file_format, success",
    [
        [VALID_SHP, SupportedFormat.SHP, True],
        [INVALID_SHP, SupportedFormat.SHP, False],
        # [VALID_DWG, SupportedFormat.DWG, True],
        [INVALID_DWG, SupportedFormat.CAD, False],
    ]
)
def test_convert_to_json(test_app: TestClient, monkeypatch, path_to_file, file_format, success):
    path = os.path.join('tests/resources', path_to_file)

    # geojson = convert_to_geojson()
    # assert bool(geojson) == success
