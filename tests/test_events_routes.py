from fastapi.testclient import TestClient

from routes import events
import tests.fixtures as my_fixtures 


def test_get_events_returns_correct_ids(client: TestClient, dependencies=[my_fixtures.reset_db]):
    