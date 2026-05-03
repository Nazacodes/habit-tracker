import json
from io import BytesIO

from tests.support import scrape_csrf


def test_export_returns_json(client, isolated_app_env):
    r = client.get("/backup/export")
    assert r.status_code == 200
    assert r.mimetype == "application/json"
    body = json.loads(r.data.decode("utf-8"))
    assert body == {"habits": []}


def test_restore_replaces_store(client, isolated_app_env, csrf_token_for_forms):
    create = client.post(
        "/habits",
        data={"name": "Alpha", "description": "", "csrf_token": csrf_token_for_forms},
        follow_redirects=False,
    )
    assert create.status_code == 302

    raw = isolated_app_env.read_bytes()
    token = scrape_csrf(client, "/backup")
    payload = {"habits": []}
    empty_blob = BytesIO(json.dumps(payload).encode("utf-8"))
    resp = client.post(
        "/backup/restore",
        data={
            "csrf_token": token,
            "confirm_restore": "yes",
            "backup_file": (empty_blob, "clear.json"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert json.loads(isolated_app_env.read_text(encoding="utf-8"))["habits"] == []

    token2 = scrape_csrf(client, "/backup")
    resp2 = client.post(
        "/backup/restore",
        data={
            "csrf_token": token2,
            "confirm_restore": "yes",
            "backup_file": (BytesIO(raw), "restore.json"),
        },
        content_type="multipart/form-data",
    )
    assert resp2.status_code == 302
    revived = json.loads(isolated_app_env.read_text(encoding="utf-8"))
    assert len(revived["habits"]) == 1
    assert revived["habits"][0]["name"] == "Alpha"
