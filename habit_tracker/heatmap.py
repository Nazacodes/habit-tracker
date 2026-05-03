from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta

from typing import Literal

HeatState = Literal["future", "done", "empty"]


def monday_containing(day: date) -> date:
    return day - timedelta(days=day.weekday())


def build_heatmap_columns(
    completion_dates: Iterable[date],
    today: date,
    num_weeks: int = 12,
) -> tuple[list[list[HeatState]], list[date], date, date]:
    """
    Contribution-style chart: **7 rows** (Mon→Sun top→bottom) × **num_weeks** columns
    left = oldest column, right = week containing ``today``.
    Each cell ``state`` distinguishes future days, completions, misses.
    """
    if num_weeks < 1:
        return [], [], today, today
    comps = set(completion_dates)
    newest_monday = monday_containing(today)
    oldest_monday = newest_monday - timedelta(weeks=num_weeks - 1)

    grid: list[list[HeatState]] = []
    week_start_dates: list[date] = []
    mon = oldest_monday
    while mon <= newest_monday:
        week_start_dates.append(mon)
        mon += timedelta(weeks=1)

    for row in range(7):
        row_cells: list[HeatState] = []
        cursor_monday = oldest_monday
        for _ in range(num_weeks):
            d = cursor_monday + timedelta(days=row)
            if d > today:
                row_cells.append("future")
            elif d in comps:
                row_cells.append("done")
            else:
                row_cells.append("empty")
            cursor_monday += timedelta(weeks=1)
        grid.append(row_cells)

    return grid, week_start_dates, oldest_monday, newest_monday


def month_tick_labels(week_mondays: list[date]) -> list[str]:
    """Short month labels for column headers (only on first week of a month)."""
    prev: int | None = None
    labels: list[str] = []
    for d in week_mondays:
        if d.month != prev:
            labels.append(d.strftime("%b"))
        else:
            labels.append("")
        prev = d.month
    return labels
