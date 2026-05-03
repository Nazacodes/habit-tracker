from __future__ import annotations

from datetime import date
from typing import Any

from habit_tracker.models import Habit
from habit_tracker.streak import best_streak


def habit_last_completed(habit: Habit) -> date:
    return max(habit.completions) if habit.completion_set() else date.min


def sort_rows(
    rows: list[dict[str, Any]],
    sort_mode: str,
    today: date,
) -> list[dict[str, Any]]:
    mode = sort_mode.casefold().strip() or "name"
    clone = list(rows)
    if mode == "streak":
        clone.sort(key=lambda r: (-r["current"], r["habit"].name.casefold()))
    elif mode == "best":
        clone.sort(key=lambda r: (-r["best"], r["habit"].name.casefold()))
    elif mode == "recent":
        clone.sort(key=lambda r: (-habit_last_completed(r["habit"]).toordinal(), r["habit"].name.casefold()))
    else:
        clone.sort(key=lambda r: r["habit"].name.casefold())
    return clone


def gather_today_focus(rows: list[dict[str, Any]], today: date) -> tuple[list[dict[str, Any]], int, int]:
    """Pending = habits without a completion stamped on ``today``."""
    pending = [r for r in rows if today not in r["habit"].completion_set()]
    done_today_count = len(rows) - len(pending)
    return pending, done_today_count, len(rows)


def portfolio_best(rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    return max(best_streak(r["habit"].completion_set()) for r in rows)
