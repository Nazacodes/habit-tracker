from __future__ import annotations

import re


def scrape_csrf(client, path: str = "/habits/new") -> str:
    r = client.get(path)
    assert r.status_code == 200
    text = r.get_data(as_text=True)
    match = re.search(r'name="csrf_token"\s+value="([^"]+)"', text)
    assert match is not None, text[:600]
    return match.group(1)
