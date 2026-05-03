from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path

from habit_tracker.models import Habit, StoreData
from habit_tracker.storage import load_store, save_store


def default_store_path() -> Path:
    env = os.environ.get("HABIT_STORE_PATH")
    if env:
        return Path(env)
    return Path(__file__).resolve().parent.parent / "data" / "store.json"


def get_habit(data: StoreData, habit_id: str) -> Habit | None:
    for h in data.habits:
        if h.id == habit_id:
            return h
    return None


def parse_completion_date(s: str | None, default: date) -> date:
    if not s or not str(s).strip():
        return default
    try:
        return datetime.strptime(str(s).strip(), "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("date must be YYYY-MM-DD") from exc


def add_or_load(path: Path) -> StoreData:
    if not path.exists():
        return StoreData(habits=[])
    return load_store(path)


def delete_habit(data: StoreData, habit_id: str) -> bool:
    before = len(data.habits)
    data.habits = [h for h in data.habits if h.id != habit_id]
    return len(data.habits) < before
