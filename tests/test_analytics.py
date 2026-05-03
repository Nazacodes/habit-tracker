from datetime import date, timedelta

from habit_tracker.analytics import total_last_n_days, weekly_counts


def test_weekly_counts_only_current_iso_week():
    today = date(2026, 5, 2)  # Saturday
    monday = today - timedelta(days=today.weekday())
    prev_sunday = monday - timedelta(days=1)
    chart = weekly_counts({monday, prev_sunday, today}, today)
    labels = [label for label, _ in chart]
    assert labels == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    counts = {label: c for label, c in chart}
    assert counts["Mon"] == 1
    assert counts["Sat"] == 1
    # previous Sunday is outside this ISO week
    assert counts["Sun"] == 0


def test_total_last_n_days_inclusive():
    today = date(2026, 5, 2)
    days = {today - timedelta(i) for i in (0, 1, 3, 10)}
    assert total_last_n_days(days, today, 7) == 3
