from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from habit_tracker.models import StoreData


def load_store(path: Path) -> StoreData:
    """Load JSON store; missing file yields empty habits."""
    if not path.exists():
        return StoreData(habits=[])
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("store root must be an object")
    return StoreData.from_dict(raw)


def save_store(path: Path, data: StoreData) -> None:
    """Persist atomically: write temp in same dir then replace."""
    data.normalize_for_save()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = data.to_dict()
    fd, tmp_path = tempfile.mkstemp(
        prefix=".habit_store_",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=False)
            fh.write("\n")
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
