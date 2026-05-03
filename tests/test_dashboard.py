from datetime import date, timedelta

from habit_tracker.dashboard import gather_today_focus, portfolio_best, sort_rows
from habit_tracker.models import Habit


def _row(hname: str, completions: list[date], cur: int, best: int) -> dict:
    h = Habit.new(hname, "")
    h.completions.extend(completions)
    return {"habit": h, "current": cur, "best": best}


def test_sort_by_streak_desc():
    today = date(2026, 5, 2)
    rows = [
        _row("a", [today], 1, 1),
        _row("b", [today, today - timedelta(1)], 2, 2),
    ]
    out = sort_rows(rows, "streak", today)
    assert out[0]["habit"].name == "b"


def test_gather_today_focus():
    today = date(2026, 5, 2)
    rows = [
        _row("done", [today], 1, 1),
        _row("pending", [], 0, 0),
    ]
    pending, done_ct, total = gather_today_focus(rows, today)
    assert total == 2
    assert done_ct == 1
    assert len(pending) == 1
    assert pending[0]["habit"].name == "pending"


def test_portfolio_best():
    today = date(2026, 5, 2)
    streak5 = [today - timedelta(days=i) for i in range(5)]
    rows = [
        _row("x", [today, today - timedelta(days=1)], 2, 2),
        _row("y", streak5, 5, 5),
    ]
    assert portfolio_best(rows) == 5
