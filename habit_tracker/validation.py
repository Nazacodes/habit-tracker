from __future__ import annotations

MAX_NAME_LEN = 120
MAX_DESCRIPTION_LEN = 2000


def validate_habit_fields(name: str, description: str) -> tuple[bool, str | None]:
    if not name.strip():
        return False, "Name is required."
    if len(name) > MAX_NAME_LEN:
        return False, f"Name must be at most {MAX_NAME_LEN} characters."
    if len(description) > MAX_DESCRIPTION_LEN:
        return False, f"Description must be at most {MAX_DESCRIPTION_LEN} characters."
    return True, None
