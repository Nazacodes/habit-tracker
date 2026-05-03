from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta


def current_streak(completion_dates: Iterable[date], today: date) -> int:
    """
    Current streak counts consecutive calendar days backwards from an anchor day.

    Anchor rules (habit-tracking style):
    - If `today` is completed, streak runs backward from today.
    - Else if `today - 1 day` is completed, streak runs backward from yesterday
      (still active before missing two days).
    - Otherwise streak is 0.

    Duplicate dates in the iterable are ignored (treated as a set).
    """
    dates = set(completion_dates)
    if not dates:
        return 0

    if today in dates:
        anchor = today
    elif today - timedelta(days=1) in dates:
        anchor = today - timedelta(days=1)
    else:
        return 0

    count = 0
    cursor = anchor
    while cursor in dates:
        count += 1
        cursor -= timedelta(days=1)
    return count


def best_streak(completion_dates: Iterable[date]) -> int:
    """Longest run of consecutive calendar days in the history (0 if empty)."""
    dates = sorted(set(completion_dates))
    if not dates:
        return 0
    best = 1
    run = 1
    for prev, cur in zip(dates, dates[1:]):
        if cur == prev + timedelta(days=1):
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


def iso_week_bounds(today: date) -> tuple[date, date]:
    """Monday–Sunday inclusive for the ISO week containing `today`."""
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def format_iso_week_range(today: date) -> str:
    """Human-readable Mon–Sun range for the ISO week containing `today`."""
    mon, sun = iso_week_bounds(today)
    if mon.year == sun.year:
        left = mon.strftime("%a %d %b")
        right = sun.strftime("%a %d %b %Y")
    else:
        left = mon.strftime("%a %d %b %Y")
        right = sun.strftime("%a %d %b %Y")
    return f"{left} – {right}"


def completions_in_week(completion_dates: Iterable[date], today: date) -> int:
    mon, sun = iso_week_bounds(today)
    dset = set(completion_dates)
    return sum(1 for d in dset if mon <= d <= sun)
