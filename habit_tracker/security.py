from __future__ import annotations

import secrets

from flask import Request, abort, session

_CSRF_KEY = "_csrf_token"


def csrf_token() -> str:
    """Return stable per-session token for form posts (synchroniser token pattern)."""
    token = session.get(_CSRF_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[_CSRF_KEY] = token
    return token


def validate_csrf(request: Request) -> None:
    expected = session.get(_CSRF_KEY)
    supplied = request.form.get("csrf_token")
    if not expected or supplied != expected:
        abort(403)
