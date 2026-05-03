from tests.support import scrape_csrf


def test_quick_today_marks_reference_day(client, csrf_token_for_forms):
    create = client.post(
        "/habits",
        data={"name": "Sprint", "description": "", "csrf_token": csrf_token_for_forms},
        follow_redirects=False,
    )
    habit_id = create.headers["Location"].rsplit("/", 1)[-1]

    page = client.get("/?sort=streak")
    assert page.status_code == 200
    token = scrape_csrf(client, "/habits/new")
    resp = client.post(
        f"/habits/{habit_id}/today",
        data={"csrf_token": token, "sort": "streak"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert "sort=streak" in resp.headers["Location"]

    detail = client.get(f"/habits/{habit_id}")
    assert "2026-05-02" in detail.get_data(as_text=True)
