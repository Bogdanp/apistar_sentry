import pytest

from apistar import TestClient
from .app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)
