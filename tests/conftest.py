import pytest

from habit_tracker.app import app
from tests.support import scrape_csrf


@pytest.fixture()
def isolated_app_env(tmp_path, monkeypatch):
    store = tmp_path / "store.json"
    monkeypatch.setenv("HABIT_STORE_PATH", str(store))
    monkeypatch.setenv("HABIT_TODAY", "2026-05-02")
    return store


@pytest.fixture()
def client(isolated_app_env):
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture()
def csrf_token_for_forms(client):
    return scrape_csrf(client)
