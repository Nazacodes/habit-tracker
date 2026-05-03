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


def total_last_n_days(completion_dates: Iterable[date], today: date, n: int) -> int:
    """Count completions in the inclusive window [today - (n-1), today]."""
    if n < 1:
        return 0
    start = today - timedelta(days=n - 1)
    dset = set(completion_dates)
    return sum(1 for d in dset if start <= d <= today)
