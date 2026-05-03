from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any
from uuid import uuid4


def _parse_date(s: str) -> date:
    y, m, d = (int(p) for p in s.split("-"))
    return date(y, m, d)


@dataclass
class Habit:
    id: str
    name: str
    description: str
    completions: list[date] = field(default_factory=list)

    @classmethod
    def new(cls, name: str, description: str = "") -> Habit:
        return cls(id=str(uuid4()), name=name.strip(), description=description.strip(), completions=[])

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "completions": sorted({d.isoformat() for d in self.completions}),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Habit:
        raw = d.get("completions") or []
        completions = []
        for item in raw:
            if isinstance(item, str):
                completions.append(_parse_date(item))
            else:
                raise ValueError("completion must be ISO date string")
        return cls(
            id=str(d["id"]),
            name=str(d.get("name", "")),
            description=str(d.get("description", "")),
            completions=completions,
        )

    def completion_set(self) -> set[date]:
        return set(self.completions)


@dataclass
class StoreData:
    habits: list[Habit]

    def normalize_for_save(self) -> None:
        """Dedupe completion dates and keep deterministic ordering on disk."""
        for h in self.habits:
            h.completions = sorted(set(h.completions))

    def to_dict(self) -> dict[str, Any]:
        return {"habits": [h.to_dict() for h in self.habits]}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StoreData:
        habits = [Habit.from_dict(h) for h in d.get("habits", [])]
        return cls(habits=habits)
