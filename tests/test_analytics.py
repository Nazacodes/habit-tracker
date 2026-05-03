from datetime import date, timedelta

from habit_tracker.analytics import total_last_n_days, weekly_chart_bars, weekly_counts


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


def test_weekly_chart_bars_zero_days_are_short_stubs():
    chart = [("Mon", 1), ("Tue", 1), ("Wed", 0), ("Thu", 0), ("Fri", 0), ("Sat", 0), ("Sun", 0)]
    rows = weekly_chart_bars(chart, chart_max=1, bar_max_px=100, zero_stub_px=8, nonzero_floor_px=10)
    by_label = {r["label"]: r for r in rows}
    assert by_label["Mon"]["filled"] is True
    assert by_label["Mon"]["height_px"] == 100
    assert by_label["Wed"]["filled"] is False
    assert by_label["Wed"]["height_px"] == 8


def test_weekly_chart_bars_scales_partial_week():
    chart = [("Mon", 0), ("Tue", 1), ("Wed", 0), ("Thu", 0), ("Fri", 0), ("Sat", 0), ("Sun", 0)]
    rows = weekly_chart_bars(chart, chart_max=2, bar_max_px=80, zero_stub_px=6, nonzero_floor_px=8)
    tue = next(r for r in rows if r["label"] == "Tue")
    assert tue["filled"] is True
    assert tue["height_px"] == 40  # half of 80


def test_total_last_n_days_inclusive():
    today = date(2026, 5, 2)
    days = {today - timedelta(i) for i in (0, 1, 3, 10)}
    assert total_last_n_days(days, today, 7) == 3
