# Habit Studio — COMP8066 video script (under 5 minutes)

**Target:** about 4:30 spoken (leave ~30s under the Moodle cap).

**Before recording**

1. Optional fixed clock: `$env:HABIT_TODAY="2026-05-02"` then `python -m habit_tracker`.
2. If the dashboard is empty: stop the app, copy `data/seed_demo.json` over `data/store.json`, start again (see `README.md`).
3. Open editor tabs: `habit_tracker/streak.py`, `habit_tracker/heatmap.py`, `tests/test_backup_restore.py`.
4. Browser zoom ~110% if text looks small on camera.

---

## Part A — Read this straight through (teleprompter)

Hi, I am Chinaza Ogwudiegwu, student ID r002316262. This video is my COMP8066 Project 2 submission, Option A: a local habit tracker called **Habit Studio**.

It is built with Python and Flask, Jinja templates, and a JSON file on disk. There are no external APIs, no hosted databases, and no chart CDNs. Quality is enforced with **pytest** and GitHub Actions on Python three eleven and three twelve.

I will start the app with `python -m habit_tracker` and open the dashboard at port five thousand.

The header line on the product is: your habits, one steady rhythm, on your device, under your control. The home screen shows **today’s date**, how many habits are already done today, and the best streak across the roster.

**Today’s focus** lists habits that still need a log for today. I can hit **Done today** on one of them. Form posts are protected with synchroniser tokens tied to the session, so random cross-site posts cannot change data.

Opening a habit gives an overview: current streak, best streak, and completions for **this week** Monday through Sunday. I can mark a date done or clear a date. The copy on the page explains the streak rule in plain language.

Below that is **this week by weekday**, a simple bar chart built in the template from counts the server computed. The chart uses a safe denominator so we never divide by zero.

The **consistency map** is a multi-week grid. Colour and pattern work together so you can read it in greyscale, not colour alone.

On **backup**, I can export a JSON snapshot or restore from a file I trust, with a confirmation step and an upload size cap so a bad upload cannot wipe data silently.

There is a light and dark theme that respects system settings, with a manual toggle.

For the written SDLC I froze requirements, mapped them to files, and split what ships now from what is deferred, for example recurrence engines and cloud sync are out of scope. Diagrams show the browser, Flask layer, and JSON store, plus create and complete flows.

For AI-assisted development I kept a prompt log: what I typed, why I sent it, and what Cursor answered. I did not treat pytest as optional. When tooling suggested turning CSRF off in tests, I refused and scraped hidden fields the way a browser would.

In code, **`habit_tracker/streak.py`** implements the anchor rule: today if logged, else yesterday, else zero, then walk backwards through consecutive calendar days.

**`habit_tracker/heatmap.py`** builds week columns from a stable Monday anchor. That is where a bad loop once raised IndexError; tests caught it before shipping.

**`tests/test_backup_restore.py`** and related tests cover backup roundtrips and CSRF failures. Locally I have forty one tests passing, and CI runs the same suite on Ubuntu.

The runnable source is public at **github.com slash Nazacodes slash habit-tracker**. My full module write-up, prompt appendix, and reflection live in the submission pack I upload to Moodle, not only in that repo.

Thank you for watching.

---

## Part B — Cue sheet (time / screen / line)

| Time | On screen | Say (short cue) |
|------|-----------|-----------------|
| 0:00 | Title or face | Name, ID, COMP8066 Project 2, Option A, **Habit Studio**. |
| 0:18 | Terminal + browser | Stack: Flask, JSON, no external APIs, pytest + Actions 3.11/3.12. |
| 0:28 | `python -m habit_tracker` → localhost | “Starting the app.” |
| 0:38 | Dashboard | Tagline + **today** + KPI “done today”. |
| 0:52 | **Today’s focus** | Habits still open; **Done today** one tap. |
| 1:02 | After click or habit open | Session-bound tokens on POSTs. |
| 1:12 | Habit detail | Streaks, mark date, streak rule text on page. |
| 1:28 | **This week by weekday** chart | Server counts; safe bar scaling. |
| 1:42 | **Consistency map** | Multi-week grid; pattern + colour. |
| 1:56 | **Backup** | Export JSON; restore with confirm + cap. |
| 2:06 | Theme toggle (optional) | System + manual theme. |
| 2:16 | SDLC PDF / TOC | Requirements, map to files, shipped vs deferred. |
| 2:36 | Diagram page | Browser, Flask, JSON; sequences. |
| 2:52 | Prompt log / appendix | Typed prompts + why + replies; pytest as gate; no CSRF-off in tests. |
| 3:08 | `streak.py` | Anchor walk logic in code. |
| 3:32 | `heatmap.py` | Monday anchor columns; IndexError story if you want it. |
| 3:56 | `test_backup_restore.py` or `pytest -q` | Integration + forty one tests; CI same suite. |
| 4:18 | GitHub **Nazacodes/habit-tracker** | Public app source; full Moodle pack separate. |
| 4:32 | Face or title | Thank you. |

---

## Tongue-twister swaps

- Say “Monday to Sunday week” instead of spelling “ISO” if you trip.
- Say “security token on forms” once if “CSRF synchroniser” is awkward on camera.

---

## After one dry run

Re-time Part B; cut any sentence in Part A that you naturally shorten when speaking.
