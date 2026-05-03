from __future__ import annotations

from collections.abc import Iterable
from collections import Counter
from datetime import date, timedelta


DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def weekly_counts(completion_dates: Iterable[date], today: date) -> list[tuple[str, int]]:
    """
    For the ISO week containing `today`, return (weekday_label, count) Monday→Sunday.

    Only completions falling in that calendar week are counted.
    """
    monday = today - timedelta(days=today.weekday())
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    dset = set(completion_dates)

    ctr: Counter[int] = Counter()
    for d in dset:
        if week_dates[0] <= d <= week_dates[6]:
            ctr[d.weekday()] += 1

    return [(DAY_NAMES[i], ctr.get(i, 0)) for i in range(7)]


def weekly_chart_bars(
    chart: list[tuple[str, int]],
    chart_max: int,
    *,
    bar_max_px: int = 132,
    zero_stub_px: int = 8,
    nonzero_floor_px: int = 12,
) -> list[dict[str, object]]:
    """
    Turn (label, count) rows into pixel heights for the habit detail bar chart.

    Percentage heights were misleading inside a stretched flex/grid (bars looked
    equal). Pixel heights inside a fixed track make 0 vs 1 vs scaled counts obvious.
    """
    if chart_max < 1:
        chart_max = 1
    out: list[dict[str, object]] = []
    for label, count in chart:
        if count <= 0:
            height_px = zero_stub_px
            filled = False
        else:
            frac = min(1.0, count / chart_max)
            raw = int(round(frac * bar_max_px))
            height_px = max(nonzero_floor_px, raw)
            filled = True
        out.append({"label": label, "count": count, "height_px": height_px, "filled": filled})
    return out


def total_last_n_days(completion_dates: Iterable[date], today: date, n: int) -> int:
    """Count completions in the inclusive window [today - (n-1), today]."""
    if n < 1:
        return 0
    start = today - timedelta(days=n - 1)
    dset = set(completion_dates)
    return sum(1 for d in dset if start <= d <= today)
