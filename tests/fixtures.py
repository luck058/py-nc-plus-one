import pytest
from fastapi.testclient import TestClient

from routes import events
from main import app
from db.seed import seed

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def reset_db():
    seed()