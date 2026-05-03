# Habit Studio — Habit Tracker Pro (COMP8066 Project 2)

Local web habit tracker (**“Habit Studio”** in the UI) delivering **CRUD**, **daily completion**, a **documented streak engine**, **weekly analytics**, and new **product-grade MVP affordances** below. All persistence is a **JSON file** on disk — **no external APIs** (no CDN fonts, no hosted analytics).

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

Open **http://127.0.0.1:5000** in your browser.

### Fake/demo data *(UI + manual testing)*

Prebuilt file: **`data/seed_demo.json`** — six habits with ~90 days of mixed completions (streaks, heatmap texture, Focus rail quirks).

Regenerate / apply:

```powershell
# Regenerate demo file (reference day = real clock, or set HABIT_TODAY below)
python scripts/seed_fake_data.py

# Copy demo data into your live store (overwrite)
python scripts/seed_fake_data.py --apply

# Match coursework screenshots with a fixed clock
$env:HABIT_TODAY="2026-05-02"
python scripts/seed_fake_data.py --apply
```

### Product MVP highlights (beyond baseline Option A)

- **Dashboard KPIs:** today completion coverage + portfolio “best streak” benchmark.
- **Today’s focus rail:** one-click “Done today” (CSRF-backed) for habits missing the reference day.
- **Roster sorting:** name / current streak / best streak / recent activity (bookmarkable query string for demos).
- **Consistency heatmap:** 14-week GitHub-style grid per habit (`habit_tracker/heatmap.py`).
- **Backup / restore:** download JSON snapshot + guarded upload replace (`/backup`).
- **Theme system:** light/dark with `prefers-color-scheme` default + persisted toggle (`localStorage`, `static/theme.js`).
- **Design narrative:** WCAG-aligned green tokens documented in [`docs/UI_Design_Rationale.md`](docs/UI_Design_Rationale.md).

### Quality bar (“exceptional-tier” checkpoints)

- **CSRF synchroniser tokens** on every state-changing POST (`habit_tracker/security.py`).
- **Strict server-side validation** (`habit_tracker/validation.py`) + deterministic JSON normalization on save.
- **Accessibility polish:** skip link, `aria-live` flashes, focus-visible outlines, semantic tables/figures, patterned heatmap empties (not hue-only cues).
- **CI:** GitHub Actions runs **`pytest`** on Python 3.11 + 3.12 ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)).
- **`GET /healthz`** JSON smoke probe for narration during video recordings.

### Optional environment variables

| Variable | Purpose |
|----------|---------|
| `HABIT_STORE_PATH` | Absolute path to the JSON store (default: `data/store.json` under the project root). |
| `HABIT_TODAY` | ISO date (`YYYY-MM-DD`) used as “today” for demos and automated tests (omit for real use). |
| `FLASK_SECRET_KEY` | Secret for session/flash signing **and** CSRF token storage (defaults to a dev value — change if multiple users share a LAN). |

## Tests

```bash
pytest -q
```

## Project layout

- `habit_tracker/` — Flask app, models, JSON storage, streak/analytics/dashboard/heatmap/security helpers
- `templates/`, `static/` — UI
- `data/` — default location for `store.json` (created on first save)
- `tests/` — unit + integration tests
- `docs/` — SDLC report, prompt log & chat appendix, reflection (Markdown sources + **[`docs/docx/COMP8066_Final_Submission.docx`](docs/docx/COMP8066_Final_Submission.docx)** bundle via [`scripts/build_final_submission_docx.py`](scripts/build_final_submission_docx.py); per-file Word via [`requirements-docx.txt`](requirements-docx.txt))
- [`docs/Prompt_Chats_Appendix.md`](docs/Prompt_Chats_Appendix.md) — full prompt-engineering transcript blocks
- [`docs/Submission_Guide.md`](docs/Submission_Guide.md) — PDF/video/zip checklist and PowerShell helper
- [`docs/diagrams/`](docs/diagrams/) — SVG architecture + sequence figures embedded via SDLC Markdown / Word bundle
- [`docs/report-figures/`](docs/report-figures/) — Figures 1–5 as HTML (print/snip into PDF)
- [`docs/mockups/CHAT_MOCKUPS_INDEX.html`](docs/mockups/CHAT_MOCKUPS_INDEX.html) — Cursor / ChatGPT / Copilot–style static “screenshot” pages for the report

## Non-trivial logic (assignment)

The **streak engine** (`habit_tracker/streak.py`) defines how *current streak* is derived from completion dates relative to a reference day, plus **best-ever** streak and **ISO week** helpers used by analytics.

## Publish to GitHub (public repo)

Keep the repo **source-first**: Markdown docs, `habit_tracker/`, `tests/`, `templates/`, `static/`, `scripts/`, `data/seed_demo.json`, CI workflow. Your `.gitignore` already drops **`.venv/`**, **local `data/store.json`**, pytest caches, and **timestamped Word fallbacks** under `docs/docx/`.

1. Install [Git for Windows](https://git-scm.com/download/win) or use **GitHub Desktop**.
2. On GitHub: **New repository** → name it (e.g. `habit-studio`) → **Public** → create **without** adding a README (avoids merge friction), or add README and use pull/rebase on first push.
3. In the project folder (with Git in `PATH`):

```powershell
cd c:\Users\rituh\Desktop\aisdlc
git init
git add .
git status   # confirm no .venv, no store.json, no .env
git commit -m "Initial public import: Habit Studio coursework"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

Do **not** commit Moodle **PDF**, personal **video**, or **graded zip** unless you intend to; markers care about your submission copy, not the public repo. After the repo exists, set the real URL in `docs/Mini_SDLC_Report.md` (repository line) and rebuild the Word/PDF if needed.

## Licence

Educational submission — check with your institution for reuse.
