# Habit Studio

Local web habit tracker: **CRUD habits**, **daily completions**, **streak engine**, **weekly analytics**, **heatmap**, **backup/restore**, light/dark theme. Data is a **JSON file** on disk. **No external APIs** (no CDN fonts or hosted chart services).

**Repository:** https://github.com/Nazacodes/habit-tracker

## Requirements

- Python **3.11+** (3.12 recommended)

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
.\.venv\Scripts\activate
python -m habit_tracker
```

Open **http://127.0.0.1:5000**.

## Sample data

Bundled dataset: **`data/seed_demo.json`**. To load it as your live store, **stop the app**, copy that file over **`data/store.json`**, then start again.

Optional: set **`HABIT_TODAY=YYYY-MM-DD`** so the app treats a fixed calendar day as “today” (useful for screenshots or automated checks).

## Tests

```bash
pytest -q
```

CI runs the same suite on Python 3.11 and 3.12 (see `.github/workflows/ci.yml`).

## Layout

| Path | Role |
|------|------|
| `habit_tracker/` | Flask app, models, JSON storage, streak, analytics, heatmap, CSRF helpers |
| `templates/`, `static/` | UI |
| `data/` | Default `store.json` location (created on first save) |
| `tests/` | `pytest` |

## Environment

| Variable | Purpose |
|----------|---------|
| `HABIT_STORE_PATH` | Path to JSON store (default: `data/store.json` under repo root) |
| `HABIT_TODAY` | ISO date used as “today” for demos/tests (omit in normal use) |
| `FLASK_SECRET_KEY` | Session / CSRF signing (set something strong if others can reach your LAN) |

## Licence

Educational project; check your institution before reusing.
