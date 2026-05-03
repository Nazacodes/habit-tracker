"""HTTP hardening probes and trivial operational endpoints."""


def test_healthz_json(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload is not None
    assert payload["status"] == "ok"


def test_post_without_csrf_is_forbidden(client):
    resp = client.post("/habits", data={"name": "X", "description": ""})
    assert resp.status_code == 403


def test_post_with_wrong_csrf_is_forbidden(client):
    client.get("/habits/new")  # establish session-backed token expectation
    resp = client.post(
        "/habits",
        data={"name": "X", "description": "", "csrf_token": "not-the-token"},
    )
    assert resp.status_code == 403


def test_mark_done_requires_csrf(client, csrf_token_for_forms):
    create = client.post(
        "/habits",
        data={"name": "Run", "description": "", "csrf_token": csrf_token_for_forms},
        follow_redirects=False,
    )
    assert create.status_code == 302
    habit_id = create.headers["Location"].rsplit("/", 1)[-1]

    bad = client.post(
        f"/habits/{habit_id}/complete",
        data={"completion_date": "2026-05-02", "csrf_token": "bogus"},
        follow_redirects=False,
    )
    assert bad.status_code == 403
