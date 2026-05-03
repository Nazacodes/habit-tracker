"""Extra integration scenarios building on authenticated form posts."""

from tests.support import scrape_csrf


def test_completion_mark_writes_json(client, isolated_app_env, csrf_token_for_forms):
    store = isolated_app_env
    create = client.post(
        "/habits",
        data={"name": "Yoga", "description": "", "csrf_token": csrf_token_for_forms},
        follow_redirects=False,
    )
    habit_id = create.headers["Location"].rsplit("/", 1)[-1]

    csrf_detail = scrape_csrf(client, f"/habits/{habit_id}")
    post_complete = client.post(
        f"/habits/{habit_id}/complete",
        data={"completion_date": "2026-05-02", "csrf_token": csrf_detail},
        follow_redirects=False,
    )
    assert post_complete.status_code == 302

    txt = store.read_text(encoding="utf-8")
    assert "2026-05-02" in txt
