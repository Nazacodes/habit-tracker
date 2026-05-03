# Habit Studio — video demonstration script (max 5 minutes)

Aligns with the module brief:

| Block | Content | Time budget |
|-------|---------|-------------|
| **1** | **Your app running** — key features | **~1–2 minutes** |
| **2** | **SDLC process** — what you want to highlight | **~1–2 minutes** |
| **3** | **Main parts of your code** | **~1–2 minutes** |

**Total:** stay under **5:00**. Aim **~4:30** so you are not cut off mid-sentence.

---

## Before you record

1. Optional fixed “today”: `$env:HABIT_TODAY="2026-05-02"` then `python -m habit_tracker`.
2. If the dashboard is empty: stop the app, copy `data/seed_demo.json` over `data/store.json`, start again (`README.md`).
3. For block 3, open tabs: `habit_tracker/streak.py`, `habit_tracker/heatmap.py`, `tests/test_backup_restore.py` (or `tests/test_security_and_ops.py`).
4. Have your **SDLC PDF** (or Word) open on: **requirements / MVP table**, **one diagram page**, **prompt decision log or appendix** (pick what you will actually show).
5. Browser zoom ~110% if UI text is small on camera.

---

## Block 1 — App running (~1–2 min) — key features

**Show:** terminal start → browser `http://127.0.0.1:5000` → habit detail → backup → (optional) theme.

**Say (teleprompter — tighten after one rehearsal):**

Hi, I am Chinaza Ogwudiegwu, student ID r002316262. This is my COMP8066 Project 2 video demonstration for **Habit Studio**, a local habit tracker: Python, Flask, JSON on disk, no external APIs.

I start the app with `python -m habit_tracker`.

On the **dashboard** you see today’s date, how many habits are done today, portfolio best streak, **Today’s focus** for anything still open, and **Done today** to log with one tap. Sorting is in the URL so you can bookmark a view.

Opening a **habit** shows current and best streak, mark or clear a date, plain-language **streak rules**, **this week by weekday** bars from server counts, and a **consistency map** over several weeks using colour and pattern so it still reads in greyscale.

**Backup** exports JSON or restores with confirmation and an upload cap so a bad file cannot silently wipe data.

Optional: **theme** follows the system with a manual toggle.

---

## Block 2 — SDLC process (~1–2 min) — your highlights

**Show:** PDF or Word — TOC, **requirements or FR table**, **MVP designed vs implemented vs deferred**, **one architecture or sequence diagram**, **prompt log / decision matrix** (whatever you actually submit).

**Say:**

In the SDLC write-up I froze **functional and non-functional** requirements and mapped them to modules under `habit_tracker/` and `tests/`.

The **MVP table** splits what shipped in this build from what is **deferred** on purpose, for example recurrence engines and cloud sync are out of scope so the JSON model stays honest.

**Diagrams** show the browser, Flask layer, and JSON persistence, plus create-habit and mark-complete flows.

For **AI-assisted development** I logged prompts with **why** I sent them and what the assistant returned, then merged code by hand and ran **pytest** before trusting behaviour. I rejected shortcuts such as turning CSRF off in tests and instead scraped hidden form fields like a browser.

---

## Block 3 — Main parts of your code (~1–2 min)

**Show:** editor — `streak.py`, `heatmap.py`, one test file; optional **two-second** flash of `.github/workflows/ci.yml`; terminal `pytest -q`.

**Say:**

**`habit_tracker/streak.py`** implements the streak anchor: today if logged, else yesterday, else zero, then walk backwards through consecutive calendar days.

**`habit_tracker/heatmap.py`** lays out week columns from a stable Monday anchor so the grid does not drift at month edges.

**Tests:** integration coverage for backup restore and CSRF; **`pytest -q`** shows **43** tests passing locally, and **GitHub Actions** runs the same suite on Ubuntu for Python **3.11** and **3.12**.

The public application repo is **github.com / Nazacodes / habit-tracker**. The full Moodle submission includes the written SDLC, prompt evidence, and reflection.

Thank you for watching.

---

## Minute-by-minute cue sheet (optional)

| Clock | Block | On screen | One-line cue |
|-------|-------|-----------|--------------|
| 0:00 | 1 | Face or title | Name, ID, project, Habit Studio, stack. |
| 0:25 | 1 | Terminal + browser | `python -m habit_tracker`, open localhost. |
| 0:40 | 1 | Dashboard | Today, KPI, Today’s focus, Done today. |
| 1:00 | 1 | Habit detail | Streaks, week bars, consistency map. |
| 1:25 | 1 | Backup (+ theme optional) | Export / restore / cap / confirm. |
| 1:45 | 2 | SDLC doc | Requirements, MVP deferrals. |
| 2:15 | 2 | Diagram | Architecture or sequence. |
| 2:35 | 2 | Prompt log | Techniques + pytest as gate. |
| 2:55 | 3 | `streak.py` | Anchor + walk in code. |
| 3:25 | 3 | `heatmap.py` | Monday anchor / grid. |
| 3:50 | 3 | Tests + pytest + CI | 43 tests; Actions matrix. |
| 4:20 | 3 | GitHub + outro | Repo URL; thank you. |

If block 1 runs long, cut theme toggle and shorten dashboard narration. If block 2 runs long, show one diagram only.

---

## Phrasing fallbacks

- “Monday through Sunday week” instead of spelling **ISO** if you stumble.
- “Security token on forms” once instead of repeating **CSRF**.

---

After one full run, adjust Part B clocks so **block 1 ends by ~2:00**, **block 2 by ~4:00**, **block 3 ends before 5:00**.
