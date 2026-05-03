"""Integration: create habit via HTTP → persist → reload from JSON."""

import json
from pathlib import Path

from tests.support import scrape_csrf


def test_create_habit_persists_to_store(client, isolated_app_env, csrf_token_for_forms):
    store_path = isolated_app_env
    resp = client.post(
        "/habits",
        data={
            "name": "Stretch",
            "description": "Morning",
            "csrf_token": csrf_token_for_forms,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302
    habit_id = resp.headers["Location"].rsplit("/", 1)[-1]

    raw = json.loads(Path(store_path).read_text(encoding="utf-8"))
    assert len(raw["habits"]) == 1
    assert raw["habits"][0]["id"] == habit_id
    assert raw["habits"][0]["name"] == "Stretch"

    get_resp = client.get(f"/habits/{habit_id}")
    assert get_resp.status_code == 200
    body = get_resp.data.decode("utf-8")
    assert "Stretch" in body


def test_dashboard_lists_created_habit(client, isolated_app_env, csrf_token_for_forms):
    client.post(
        "/habits",
        data={
            "name": "Read",
            "description": "10 pages",
            "csrf_token": csrf_token_for_forms,
        },
        follow_redirects=False,
    )
    dash = client.get("/")
    assert dash.status_code == 200
    html = dash.data.decode("utf-8")
    assert "Read" in html


def test_delete_habit_removes_from_store(client, isolated_app_env, csrf_token_for_forms):
    create = client.post(
        "/habits",
        data={"name": "Temp", "description": "", "csrf_token": csrf_token_for_forms},
        follow_redirects=False,
    )
    habit_id = create.headers["Location"].rsplit("/", 1)[-1]
    csrf_detail = scrape_csrf(client, f"/habits/{habit_id}")
    del_resp = client.post(
        f"/habits/{habit_id}/delete",
        data={"csrf_token": csrf_detail},
        follow_redirects=False,
    )
    assert del_resp.status_code == 302
    raw = json.loads(Path(isolated_app_env).read_text(encoding="utf-8"))
    assert raw["habits"] == []
    gone = client.get(f"/habits/{habit_id}")
    assert gone.status_code == 302
