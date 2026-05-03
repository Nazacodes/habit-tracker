import json
from pathlib import Path

import pytest

from habit_tracker.models import Habit, StoreData
from habit_tracker.storage import load_store, save_store


def test_habit_round_trip_dict():
    h = Habit.new("Read", "Books")
    h.completions.append(__import__("datetime").date(2026, 5, 1))
    d = h.to_dict()
    h2 = Habit.from_dict(d)
    assert h2.id == h.id
    assert h2.name == "Read"
    assert h2.completion_set() == h.completion_set()


def test_load_missing_file_empty(tmp_path):
    p = tmp_path / "missing.json"
    data = load_store(p)
    assert data.habits == []


def test_save_load_round_trip(tmp_path):
    p = tmp_path / "store.json"
    h = Habit.new("X", "")
    save_store(p, StoreData(habits=[h]))
    data = load_store(p)
    assert len(data.habits) == 1
    assert data.habits[0].name == "X"


def test_load_invalid_json_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        load_store(p)


def test_load_not_object_raises(tmp_path):
    p = tmp_path / "bad2.json"
    p.write_text(json.dumps(["x"]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_store(p)


def test_save_deduplicates_sorted_completions(tmp_path):
    from datetime import date

    p = tmp_path / "store.json"
    d = date(2026, 5, 1)
    habit = Habit.new("Dup day", "")
    habit.completions = [d, d]
    save_store(p, StoreData(habits=[habit]))

    restored = load_store(p)
    assert restored.habits[0].completions == [d]
