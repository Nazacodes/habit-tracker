from __future__ import annotations

import json
import os
from datetime import date
from io import BytesIO
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, url_for

from habit_tracker.analytics import weekly_counts
from habit_tracker.dashboard import gather_today_focus, portfolio_best, sort_rows
from habit_tracker.models import Habit, StoreData
from habit_tracker.security import csrf_token, validate_csrf
from habit_tracker.service import (
    add_or_load,
    default_store_path,
    delete_habit,
    get_habit,
    parse_completion_date,
)
from habit_tracker.heatmap import build_heatmap_columns, month_tick_labels
from habit_tracker.storage import save_store
from habit_tracker.streak import best_streak, current_streak, format_iso_week_range
from habit_tracker.validation import validate_habit_fields

_ROOT = Path(__file__).resolve().parent.parent
app = Flask(
    __name__,
    template_folder=str(_ROOT / "templates"),
    static_folder=str(_ROOT / "static"),
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024


@app.context_processor
def inject_helpers() -> dict[str, object]:
    return {"csrf_token": csrf_token}


def _store_path() -> Path:
    return default_store_path()


def _today() -> date:
    """Bound for tests via HABIT_TODAY ISO date."""
    raw = os.environ.get("HABIT_TODAY")
    if raw:
        from datetime import datetime

        return datetime.strptime(raw, "%Y-%m-%d").date()
    return date.today()


def _persist(data: StoreData) -> None:
    save_store(_store_path(), data)


@app.errorhandler(403)
def forbidden(_exc):
    """CSRF misuse or deliberate tampering."""
    return (
        render_template(
            "errors/error.html",
            title="Forbidden",
            message=(
                "This action could not be verified (missing or invalid security token). "
                "Reload the page and try again."
            ),
        ),
        403,
    )


@app.errorhandler(404)
def not_found(_exc):
    return (
        render_template(
            "errors/error.html",
            title="Page not found",
            message="The page you requested does not exist.",
        ),
        404,
    )


@app.get("/healthz")
def healthz():
    """Lightweight liveness probe for demos / CI smoke (no secrets)."""
    return {"status": "ok", "storage": _store_path().name}


@app.route("/")
def index():
    data = add_or_load(_store_path())
    today = _today()
    habits = sorted(data.habits, key=lambda h: h.name.casefold())
    rows: list[dict] = []
    for h in habits:
        cset = h.completion_set()
        rows.append(
            {
                "habit": h,
                "current": current_streak(cset, today),
                "best": best_streak(cset),
            }
        )

    sort_mode = (request.args.get("sort") or "name").strip()
    sorted_rows = sort_rows(rows, sort_mode, today)
    pending_focus, today_done_ct, habits_total = gather_today_focus(sorted_rows, today)
    aggregate_best = portfolio_best(sorted_rows)

    completion_rate = (
        round((today_done_ct / habits_total) * 100) if habits_total else None
    )

    return render_template(
        "index.html",
        rows=sorted_rows,
        today=today,
        sort_mode=sort_mode,
        pending_focus=pending_focus,
        today_done_ct=today_done_ct,
        habits_total=habits_total,
        completion_rate=completion_rate,
        aggregate_best=aggregate_best,
    )


@app.post("/habits/<habit_id>/today")
def habit_mark_today_quick(habit_id: str):
    validate_csrf(request)
    sort_mode = request.form.get("sort", "name")
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index", sort=sort_mode))

    td = _today()
    if td not in habit.completions:
        habit.completions.append(td)
    _persist(data)
    flash(f"Marked “{habit.name}” complete for today.", "success")
    return redirect(url_for("index", sort=sort_mode))


@app.get("/backup/export")
def backup_export():
    path = _store_path()
    download_name = "habit-tracker-backup.json"
    if path.exists():
        return send_file(
            path,
            mimetype="application/json",
            as_attachment=True,
            download_name=download_name,
            max_age=0,
        )
    payload = BytesIO(json.dumps({"habits": []}, indent=2).encode("utf-8"))
    payload.seek(0)
    return send_file(
        payload,
        mimetype="application/json",
        as_attachment=True,
        download_name=download_name,
        max_age=0,
    )


@app.get("/backup")
def backup_page():
    exists = _store_path().exists()
    return render_template("backup.html", store_exists=exists)


@app.post("/backup/restore")
def backup_restore():
    validate_csrf(request)
    if request.form.get("confirm_restore") != "yes":
        flash("Please confirm restoring a backup.", "error")
        return redirect(url_for("backup_page"))

    upload = request.files.get("backup_file")
    if upload is None or upload.filename == "":
        flash("Choose a `.json` backup file first.", "error")
        return redirect(url_for("backup_page"))

    try:
        raw = upload.stream.read().decode("utf-8")
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        flash("That file is not valid JSON.", "error")
        return redirect(url_for("backup_page"))

    if not isinstance(payload, dict) or not isinstance(payload.get("habits", []), list):
        flash('Backup must contain a top-level object with key "habits" (array).', "error")
        return redirect(url_for("backup_page"))

    try:
        rebuilt = StoreData.from_dict(payload)
    except (ValueError, KeyError, TypeError):
        flash("Backup JSON does not match the expected habit schema.", "error")
        return redirect(url_for("backup_page"))

    save_store(_store_path(), rebuilt)
    flash("Backup restored successfully.", "success")
    return redirect(url_for("index"))


@app.route("/habits/new")
def habit_new():
    return render_template("habit_form.html", habit=None, title="New habit")


@app.post("/habits")
def habit_create():
    validate_csrf(request)
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    ok, err = validate_habit_fields(name, description)
    if not ok:
        flash(err or "Validation failed.", "error")
        return render_template("habit_form.html", habit=None, title="New habit"), 400
    data = add_or_load(_store_path())
    habit = Habit.new(name=name, description=description)
    data.habits.append(habit)
    _persist(data)
    flash("Habit created.", "success")
    return redirect(url_for("habit_detail", habit_id=habit.id))


@app.get("/habits/<habit_id>")
def habit_detail(habit_id: str):
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    today = _today()
    cset = habit.completion_set()
    chart = weekly_counts(cset, today)
    chart_max = max((c for _, c in chart), default=0)
    if chart_max < 1:
        chart_max = 1
    heatmap_grid, heat_weeks, _hm_lo, _hm_hi = build_heatmap_columns(cset, today, num_weeks=14)
    heat_ticks = month_tick_labels(heat_weeks)
    return render_template(
        "habit_detail.html",
        habit=habit,
        today=today,
        week_heading=format_iso_week_range(today),
        current=current_streak(cset, today),
        best=best_streak(cset),
        week_total=sum(c for _, c in chart),
        chart=chart,
        chart_max=chart_max,
        heatmap_grid=heatmap_grid,
        heat_ticks=heat_ticks,
    )


@app.post("/habits/<habit_id>/complete")
def habit_complete(habit_id: str):
    validate_csrf(request)
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    try:
        d = parse_completion_date(request.form.get("completion_date"), _today())
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("habit_detail", habit_id=habit_id))
    if d not in habit.completions:
        habit.completions.append(d)
    _persist(data)
    flash(f"Marked done for {d.isoformat()}.", "success")
    return redirect(url_for("habit_detail", habit_id=habit_id))


@app.post("/habits/<habit_id>/uncomplete")
def habit_uncomplete(habit_id: str):
    validate_csrf(request)
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    try:
        d = parse_completion_date(request.form.get("completion_date"), _today())
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("habit_detail", habit_id=habit_id))
    habit.completions = [x for x in habit.completions if x != d]
    _persist(data)
    flash(f"Cleared {d.isoformat()}.", "success")
    return redirect(url_for("habit_detail", habit_id=habit_id))


@app.get("/habits/<habit_id>/edit")
def habit_edit(habit_id: str):
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    return render_template("habit_form.html", habit=habit, title="Edit habit")


@app.post("/habits/<habit_id>")
def habit_update(habit_id: str):
    validate_csrf(request)
    data = add_or_load(_store_path())
    habit = get_habit(data, habit_id)
    if not habit:
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    ok, err = validate_habit_fields(name, description)
    if not ok:
        flash(err or "Validation failed.", "error")
        return render_template("habit_form.html", habit=habit, title="Edit habit"), 400
    habit.name = name
    habit.description = description
    _persist(data)
    flash("Habit updated.", "success")
    return redirect(url_for("habit_detail", habit_id=habit_id))


@app.post("/habits/<habit_id>/delete")
def habit_delete(habit_id: str):
    validate_csrf(request)
    data = add_or_load(_store_path())
    if not delete_habit(data, habit_id):
        flash("Habit not found.", "error")
        return redirect(url_for("index"))
    _persist(data)
    flash("Habit deleted.", "success")
    return redirect(url_for("index"))
