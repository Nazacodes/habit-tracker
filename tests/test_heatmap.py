from datetime import date, timedelta

from habit_tracker.heatmap import build_heatmap_columns, month_tick_labels


def test_heatmap_future_cells_after_reference_today():
    today = date(2026, 5, 2)  # Saturday
    grid, weeks, _, _ = build_heatmap_columns([], today, num_weeks=3)
    assert len(weeks) == 3
    # Saturday row index 5 (Mon=0)
    sat_row = 5
    # last column is week containing today -> Saturday should be done/empty not future
    assert grid[sat_row][-1] in ("empty", "done")
    # Sunday row (6) same week may be future relative to Saturday today
    assert grid[6][-1] == "future"


def test_heatmap_marks_completion():
    today = date(2026, 5, 2)
    grid, weeks, _, _ = build_heatmap_columns([today], today, num_weeks=2)
    sat_row = 5
    assert grid[sat_row][-1] == "done"


def test_month_tick_labels_changes_on_boundary():
    mondays = [date(2026, 4, 27), date(2026, 5, 4)]
    labels = month_tick_labels(mondays)
    assert labels[0] == "Apr"
    assert labels[1] == "May"
