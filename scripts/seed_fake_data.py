#!/usr/bin/env python3
"""
Generate or apply realistic fake habit data for UI / manual testing.

Examples:
  python scripts/seed_fake_data.py              # writes data/seed_demo.json
  python scripts/seed_fake_data.py --apply      # copy to data/store.json (overwrite)
  set HABIT_TODAY=2026-05-02 & python scripts/seed_fake_data.py --apply
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import date, timedelta
from pathlib import Path

# Fixed UUIDs so diffs stay stable across runs.
HABITS_SPEC: list[tuple[str, str, str, str]] = [
    (
        "11111111-1111-4111-8111-111111111111",
        "Morning mobility",
        "Stretch + lumbar · 10 min",
        "everyday_anchor",
    ),
    (
        "22222222-2222-4222-8222-222222222222",
        "Deep work block",
        "90 min focus — phone in drawer",
        "weekday_bias",
    ),
    (
        "33333333-3333-4333-8333-333333333333",
        "Hydration",
        "3× refill bottle",
        "sparse",
    ),
    (
        "44444444-4444-4444-8444-444444444444",
        "Read · 25 min",
        "Non-fiction or course text",
        "streaky",
    ),
    (
        "55555555-5555-4555-8555-555555555555",
        "Lights out by 23:00",
        "Wind-down: no doomscroll",
        "sleep_rhythm",
    ),
    (
        "66666666-6666-4666-8666-666666666666",
        "Walk outside",
        "20+ minutes daylight",
        "weekend_heavy",
    ),
]


def _ref_today() -> date:
    raw = os.environ.get("HABIT_TODAY")
    if raw:
        y, m, d = (int(x) for x in raw.split("-"))
        return date(y, m, d)
    return date.today()


def _range_inclusive(start: date, end: date) -> list[date]:
    out: list[date] = []
    cur = start
    while cur <= end:
        out.append(cur)
        cur += timedelta(days=1)
    return out


def _weekdays_between(start: date, end: date) -> list[date]:
    return [d for d in _range_inclusive(start, end) if d.weekday() < 5]


def build_completions(pattern: str, today: date) -> list[str]:
    """Return sorted unique ISO dates for the last ~90 days (density varies by pattern)."""
    lo = today - timedelta(days=88)
    dates: set[date] = set()

    if pattern == "everyday_anchor":
        dates.update(_range_inclusive(today - timedelta(days=34), today))
    elif pattern == "weekday_bias":
        dates.update(_weekdays_between(today - timedelta(days=45), today))
        # Remove one recent Friday so the heatmap shows a deliberate gap.
        for off in range(21):
            d = today - timedelta(days=off)
            if d.weekday() == 4:
                dates.discard(d)
                break
    elif pattern == "sparse":
        for i in (0, 1, 3, 7, 12, 18, 25, 40, 55, 70):
            if today - timedelta(days=i) >= lo:
                dates.add(today - timedelta(days=i))
        # Deliberately skip *today* so “Focus rail” often lists this habit
    elif pattern == "streaky":
        # two separate runs for heatmap texture
        dates.update(_range_inclusive(today - timedelta(days=8), today))
        dates.update(_range_inclusive(today - timedelta(days=40), today - timedelta(days=30)))
        dates.update({today - timedelta(days=15), today - timedelta(days=17)})
    elif pattern == "sleep_rhythm":
        dates.update(_range_inclusive(today - timedelta(days=21), today))
        for d in list(dates):
            if d.weekday() == 6:  # skip some Sundays
                dates.discard(d)
    elif pattern == "weekend_heavy":
        for d in _range_inclusive(lo, today):
            if d.weekday() >= 5:
                dates.add(d)
        dates.update(_range_inclusive(today - timedelta(days=9), today - timedelta(days=7)))

    dates = {d for d in dates if d >= lo and d <= today}
    return sorted({d.isoformat() for d in dates})


def build_payload(today: date) -> dict:
    habits = []
    for hid, name, desc, pattern in HABITS_SPEC:
        habits.append(
            {
                "id": hid,
                "name": name,
                "description": desc,
                "completions": build_completions(pattern, today),
            }
        )
    return {"habits": habits}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate fake habit JSON for demos.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Copy generated JSON to the live store (data/store.json or HABIT_STORE_PATH).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "seed_demo.json",
        help="Output path for the demo seed file.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    ref = _ref_today()
    payload = build_payload(ref)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.out} (reference day: {ref.isoformat()})")

    if args.apply:
        env_path = os.environ.get("HABIT_STORE_PATH")
        target = Path(env_path) if env_path else root / "data" / "store.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.out, target)
        print(f"Applied → {target} (overwritten)")


if __name__ == "__main__":
    main()
