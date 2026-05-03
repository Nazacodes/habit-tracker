from datetime import date, timedelta

import pytest

from habit_tracker.streak import (
    best_streak,
    completions_in_week,
    current_streak,
    format_iso_week_range,
    iso_week_bounds,
)


def test_current_streak_empty():
    assert current_streak([], date(2026, 5, 2)) == 0


def test_current_streak_single_today():
    d = date(2026, 5, 2)
    assert current_streak([d], d) == 1


def test_current_streak_consecutive_from_today():
    today = date(2026, 5, 2)
    days = [today - timedelta(i) for i in range(5)]
    assert current_streak(days, today) == 5


def test_current_streak_uses_yesterday_anchor_if_today_missing():
    today = date(2026, 5, 2)
    assert current_streak([today - timedelta(1), today - timedelta(2)], today) == 2


def test_current_streak_zero_if_gap_before_anchor():
    today = date(2026, 5, 2)
    # completed two days ago only — not today or yesterday
    assert current_streak([today - timedelta(2)], today) == 0


def test_current_streak_duplicate_dates_idempotent():
    today = date(2026, 5, 2)
    assert current_streak([today, today, today], today) == 1


def test_best_streak_sparse():
    d0 = date(2026, 5, 1)
    assert best_streak([d0, d0 + timedelta(1), d0 + timedelta(3)]) == 2


def test_best_streak_full_run():
    d0 = date(2026, 4, 10)
    assert best_streak([d0 + timedelta(i) for i in range(10)]) == 10


def test_iso_week_bounds_monday_sunday():
    today = date(2026, 5, 2)  # Saturday
    mon, sun = iso_week_bounds(today)
    assert mon.weekday() == 0
    assert sun.weekday() == 6
    assert sun - mon == timedelta(days=6)


def test_completions_in_week_filters_outside():
    today = date(2026, 5, 2)
    mon, _ = iso_week_bounds(today)
    inside = {mon, mon + timedelta(2)}
    outside = {mon - timedelta(days=1)}
    assert completions_in_week(inside | outside, today) == 2


def test_completions_in_week_counts_unique_days_only():
    today = date(2026, 5, 2)
    mon, _ = iso_week_bounds(today)
    assert completions_in_week([mon, mon], today) == 1


def test_format_iso_week_range_separators():
    text = format_iso_week_range(date(2026, 5, 2))
    assert "–" in text
    assert "2026" in text


def test_format_iso_week_range_not_empty_near_year_roll():
    sample = date(2025, 12, 31)
    formatted = format_iso_week_range(sample)
    assert "–" in formatted
    assert len(formatted.strip()) >= 12

