from typing import Generator

import pytest
from starlette.testclient import TestClient

from ..app.main import app


@pytest.fixture(scope="module")
def test_app() -> Generator:
    with TestClient(app) as c:
        yield c
