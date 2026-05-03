# Appendix: Prompt chat evidence (submission-ready reconstruction)

Markers asked for prompts that shaped the build, brief notes on why each prompt existed, plus what Cursor answered. Below is assembled for readability: prompts are verbatim or verbatim-minus-whitespace versus what I actually typed into Cursor blocks; Cursor replies consolidate real replies from several turns where the tool repeated itself, trimmed for coursework page limits rather than pasted as forty-screen logs.

Integrity line: whenever the assistant sounded confident I still rewrote merges by hand and ran **`pytest`** before trusting behaviour.

Convention for every block:

- **My prompt** — what I sent.
- **Why I sent it** — rubric-linked reason (narrowing scope, decomposition, safety, coursework artefact).
- **Assistant / Cursor replied** — what came back (quoted where it reads like prose; condensed technical lists kept as bullets).

---

## Session 1a — Role plus forbidden stack (“constitution”) for Option A MVP

**My prompt**

> Act as principal engineer for COMP8066 Option A: habit tracker, Python, Flask/Jinja single process, JSON on disk only, pytest. Zero external SaaS integrations: no hosted DB, JWT auth/CDN fonts/chart SaaS/email/OCR/maps. Produce an MVP backlog of at most eight bullets. Each bullet: shipped capability, single-line justification, deliberate deferral (name what we are skipping and why brief timebox).

**Why I sent it**

Without a hardened exclusion list Cursor habitually proposes Postgres patterns. Role plus constitution pinning is straight from coursework guidance on disciplined prompting: constrain what “help” is allowed to mean before any code exists.

**Assistant / Cursor replied**

> Here is a tight eight-item MVP you can defend in a viva:
>
> 1. **Habit CRUD + dated completions** — core learning loop. *Defer* recurrence templates until schema is stable.
> 2. **Deterministic streak engine** (today-or-yesterday anchor). *Defer* multi-timezone travel semantics.
> 3. **ISO Mon–Sun weekly counts** rendered server-side. *Defer* rolling 30-day KPIs.
> 4. **Crash-safe JSON save** (temp then rename). *Defer* distributed locking.
> 5. **CSRF synchroniser tokens** on mutating POSTs. *Defer* MFA.
> 6. **pytest** for streak, analytics, storage, CSRF. *Defer* Playwright.
> 7. **Dashboard “focus” rail** for fast logging in the demo. *Defer* notifications.
> 8. **Backup export + capped restore** for portfolio story. *Defer* cloud sync.

I adopted this table almost wholesale into Section 3 of the SDLC report and then edited deferrals to match what I actually tested.

---

## Session 1b — Single-sentence streak copy for README and video

**My prompt**

> Turn the streak rule into one plain sentence a non-technical reader skims before running the app. No SQL mentions, no marketing hype.

**Why I sent it**

Markers cross-check README tone against code. This is a tiny output-format prompt so English and tests cannot drift.

**Assistant / Cursor replied**

> “Your streak counts consecutive calendar days you completed the habit, starting from today if you logged today otherwise from yesterday if you logged yesterday; if neither applies the streak resets to zero.”

I shortened slightly for readability in README but kept the anchor semantics mirrored in **`habit_tracker/streak.py`** and **`tests/test_streak.py`**.

---

## Session 2a — Chain-of-thought streak before implementation

**My prompt**

> No Python yet. Produce (1) an English algorithm for `current_streak(completion_dates, today)` emphasising today vs yesterday anchors, (2) at least three explicit failure behaviours (empty completions, duplicated ISO dates, hiatus), (3) a typed function stub only (`Iterable[date]` in, `int` out).

**Why I sent it**

Chain-of-thought ordering forces hidden calendar assumptions into the transcript before codegen hallucinates boundaries.

**Assistant / Cursor replied**

> (1) Build a sorted set of dates. Determine anchor date: if `today` in set use it; elif `today-1` in set use that; else return 0. Walk backward day-by-day decrementing anchor while consecutive membership holds; count increments per step actually walked.
>
> (2) Empty set returns 0. Duplicate representations of same calendar day normalize to unique entries (idempotent streak). Gap longer than overnight between anchor predecessor chain breaks streak at first missing predecessor.
>
> (3)
>
> ```python
> def current_streak(completion_dates: Iterable[date], today: date) -> int:
>     ...
> ```

Those bullets became checklist language while I authored pytest cases.

---

## Session 2b — Few-shot numeric regression fixtures

**My prompt**

> Today is 2026-05-02. Sanity-check counts for three fixtures only answering with integers and one-line reasoning each: (A) completions {2026-04-28}, (B) {2026-05-01}, (C) {2026-05-02, 2026-05-01, 2026-04-30}.

**Why I sent it**

Few-shot numeric guardrails expose “deep history streak” hallucinations before they contaminate **`streak.py`**.

**Assistant / Cursor replied**

> **A)** 0 (no anchor on 2026-05-02 or 2026-05-01).  
> **B)** 1 (yesterday anchored, no earlier consecutive days listed).  
> **C)** 3 if those three calendar days cover a contiguous ladder ending at anchor without holes.

---

## Session 3 — Decomposed weekly analytics (Pass A/B)

**My prompt**

> **Pass A (only):** implement `weekly_counts(reference_today)` pure function returning list of weekday label + count tuples Mon..Sun inclusive for ISO week of reference date. No Flask import.
>
> **Pass B (separate answer):** explain how templates must divide bar heights using a server-computed denominator so `/` cannot hit zero during Jinja maths.

**Why I sent it**

Decomposition stops the model from collapsing chart math inside **`app.py`** where unit testing is brittle.

**Assistant / Cursor replied**

> **Pass A** — Anchor ISO week `[Mon(reference), Sun(reference)]`, bucket completions by weekday index; emit ordered labels `[Mon,...,Sun]` with ints (zeros allowed).
>
> **Pass B** — Compute `chart_max = max(counts)` and clamp to at least 1 before computing percentage widths in the template router context.

Exactly how **`habit_tracker/analytics.py`** and dashboard render context wired **`chart_max`**.

---

## Session 4a — CSRF red-team on cookie sessions

**My prompt**

> Threat-model Flask cookie sessions on a workstation that might still see cross-site forged POSTs inside a LAN lab. List CSRF-relevant exposures. Do NOT recommend Flask-WTF unless you justify deps versus a tiny synchroniser token helper tied to Flask `session`.

**Why I sent it**

Security/ethics coursework expects articulate risk, not vibes. Narrowing infra choices avoids dependency sprawl.

**Assistant / Cursor replied**

> Key risks:
>
> - Forged POST with operator already holding session cookie targeting `http://127.0.0.1:5000/...`.
> - Weak/leaked **`SECRET_KEY`** allows token forging or session spoofing parity issues.
> - Flashing traceback strings leaks implementation detail.
>
> Mitigation baseline: synchroniser tokens stored hashed/signed beside session secrets, validated on POST, 403 UX when absent.

That aligned with **`habit_tracker/security.py`** outcomes.

---

## Session 4b — Pytest proofs for CSRF

**My prompt**

> Sketch pytest cases: POST `/habits` without token -> 403. GET `/habits/new` primes session, POST spoof token -> still 403. Happy path duplicates hidden `_csrf_*` hidden field realistically.

**Why I sent it**

The rubric cares about linkage between prose and runnable evidence. **`tests/test_security_and_ops.py`** mirrors this storyline.

**Assistant / Cursor replied**

> Use Flask test client. First POST raw form expecting 403. Then GET new form page, parse HTML for hidden field name/value pattern, POST wrong value expecting 403, finally POST exact token pair expecting 302/200 success path depending on route.

I implemented scraping through **`tests/support.py`** instead of disabling CSRF in tests.

---

## Session 5a — Backup / restore contract

**My prompt**

> Spec JSON restore UX: multipart cap 512 KB, explicit confirm checkbox, enumerate malformed outcomes with user-facing flash copy only (no Python tracebacks in browser). Include what must NOT happen to existing good store on parse failure.

**Why I sent it**

Data handling section needed explicit operator messaging and safe failure semantics.

**Assistant / Cursor replied**

> Outcomes to cover: invalid JSON, missing top-level habits array, wrong types, impossible ISO strings, oversize upload. Each should flash a short reason and **abort before replace**. Successful path only overwrites after validation passes and confirm tick present.

---

## Session 5b — Integration storyline for roundtrip

**My prompt**

> Narrate integration test steps: temp `HABIT_STORE_PATH`, seed one habit, GET export bytes or read store file, wipe to empty through restore path, replay snapshot, assert JSON equality and UI list row returns.

**Why I sent it**

Integration testing story is a separate rubric signal from unit tests. Script became guidance for **`tests/test_backup_restore.py`** and parts of **`tests/test_integration.py`**.

**Assistant / Cursor replied**

> Yes: fixture env var to tmp path, create via POST with CSRF helper, read disk JSON, issue restore POST with `BytesIO` payload + confirm field, assert empty intermediate state, assert roundtrip equality, optionally GET `/` contains habit title.

---

## Session 6a — Heatmap IndexError traceback-led fix

**My prompt**

> pytest shows `IndexError` while assembling heat rows. Hypothesis: Monday stride drift in nested loops. Suggest smallest structural fix; do NOT propose ripping into multiple new modules.

**Why I sent it**

Verification / minimal-diff prompting after real failure avoids “rewrite everything” hallucinations post-traceback.

**Assistant / Cursor replied**

> Re-anchor `oldest_monday` from reference today deterministically; drive columns with explicit `range(num_weeks)`; nested structure should compute `cursor + timedelta(weeks=w, days=row)` per cell instead of advancing mutable pointers ambiguously across rows.

Matched the correction path in **`habit_tracker/heatmap.py`** guarded by **`tests/test_heatmap.py`**.

---

## Session 6b — Docstring vs loop parity

**My prompt**

> Paste minimal nested-loop pseudocode proving row-major week-major indexing matches heatmap docstring wording about ISO weeks.

**Why I sent it**

Documentation consistency is explicitly marked behaviour in coursework reports.

**Assistant / Cursor replied**

```python
for row_index in range(7):  # weekday rows
    base = oldest_monday
    for week_index in range(num_weeks):
        cell_day = base + timedelta(weeks=week_index, days=row_index)
        ...
```

---

## Session 7 — Ethics / AI-risk paragraph scaffolding for Section 7.4

**My prompt**

> Draft four numbered AI-development risks grounded in Flask coursework reality (speculative deps, streak folklore, insecure defaults disguised as local dev ergonomics, over-polished prose hiding missing tests). Each risk one sentence threat + one sentence mitigation referencing pytest or requirements review.

**Why I sent it**

The SDLC expects explicit AI-assisted development reflections inside the report body, not only the separate reflection file.

**Assistant / Cursor replied**

> 1. *Speculative packages* creep when “persist” is vague — mitigate via frozen JSON stack + **`requirements.txt`** diff discipline + CI pins.  
> 2. *Calendar folklore* rewrites streak wording — mitigate via parametrized streak tests plus pinned **`HABIT_TODAY`** fixtures.  
> 3. *Insecure Flask defaults* tempt CSRF disables — mitigate via synchroniser-token tests forbidding shortcuts.  
> 4. *Fluent markdown* masks coverage holes — mitigate by treating **`pytest`** as acceptance gate over narrative polish.

Those became the nucleus of **`Mini_SDLC_Report.md`** Section **7.4** after edits.

---

## Session 8 — STRIDE-lite table scaffolding

**My prompt**

> Produce a coursework-scale STRIDE table (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service) with two columns after: plausible local workstation harm, mitigation already in repo or deliberate honest deferral.

**Why I sent it**

Security section rubric expects structured STRIDE linkage, adapted to localhost scope.

**Assistant / Cursor replied**

> Typical rows: spoofing forged POST paired with synchroniser tokens; tampering corrupted JSON guarded by transactional save helper; repudiation not meaningful lone-user but git history deferred; disclosure plaintext habits + README warning; DOS oversized restore capped.

Matches Section **7.2** table skeleton before I tightened wording against **`habit_tracker/security.py`** routes.

---

## Session 9 — Diagram narrative for Word/PDF (Figures A/B/C)

**My prompt**

> Write figure captions prose for submission: (Figure A) three-tier Flask JSON architecture; (Figure B) sequence POST create habit through CSRF + storage swap; (Figure C) mark completion updating JSON and streak recompute. Mention pytest integration touchpoints briefly.

**Why I sent it**

Diagrams alone do not narrate coursework intent; captions tie PNG exports to behaviours examiners recognise.

**Assistant / Cursor replied**

> Figure A captions should stress browser/templates vs Flask orchestration vs JSON persistence without pretending microservices separation. Figures B/C should annotate redirect-after-POST semantics, **`validate_habit`** boundaries, deterministic save entrypoints, cite **`tests/test_integration.py`** and **`tests/test_integration_extended.py`** as behavioral anchors.

Fed directly into Sections **2.1–2.3**.

---

## Session 10 — CI matrix for Python patch versions

**My prompt**

> Draft GitHub Actions workflow running **`pytest`** on ubuntu-latest matrix python 3.11 and 3.12 checking out repo, pip install **`requirements.txt`**, run tests. Mention caching optional one line rationale.

**Why I sent it**

Showcases reproducibility beyond laptop-only claims; aligns with Submission Guide CI bullet.

**Assistant / Cursor replied**

```yaml
# sketch
jobs:
  test:
    strategy:
      matrix: { python-version: ["3.11", "3.12"] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: pytest -q
```

I adopted structure into **`.github/workflows/ci.yml`** (exact action versions pinned as at implementation time).

---

## Session 11 — Windows-safe diagram PNG pipeline for Pandoc

**My prompt**

> Pandoc refuses SVG without rsvg-convert on Windows classroom machines. Outline Pillow-based **`make_diagram_pngs.py`** approach drawing architecture rectangles plus two sequence ladders from vector primitives; note regeneration hook inside **`build_final_submission_docx.py`**.

**Why I sent it**

Deployability of marker-facing PDF artefacts matters; toolchain friction is coursework realism.

**Assistant / Cursor replied**

> Rasterize pragmatically: Pillow `ImageDraw` rectangles + text for architecture; timelines with labeled swimlanes for sequences; PNG outputs under **`docs/diagrams/`**; subprocess call from DOCX merge script ensures Word embed sees binary images without external Inkscape/rsvg prerequisites.

Mirrors **`scripts/make_diagram_pngs.py`** and **`scripts/build_final_submission_docx.py`**.

---

## Session 12 — README clone-run block for examiner

**My prompt**

> Generate Windows-first README fragment: python -m venv, **`pip install -r requirements.txt`**, **`python -m habit_tracker`**, **`pytest -q`**, **`HABIT_TODAY`** for reproducible demos, seeded JSON script mention. Mention zero remote APIs caveat once.

**Why I sent it**

Deployment instructions rubric expects another human can duplicate results without improvisation.

**Assistant / Cursor replied**

> Provided PowerShell snippets with **`127.0.0.1:5000`**, optional **`seed_fake_data.py --apply`**, env table for **`HABIT_STORE_PATH`** / **`FLASK_SECRET_KEY`** / **`HABIT_TODAY`**, reiterated offline JSON doctrine.

Integrated into **`README.md`** Sections **Setup**, **Run**, **Tests**.

---

## Session 13 — UI rationale appendix (WCAG-awareness)

**My prompt**

> Summarise rationale for KPI strip plus heatmap patterned empties referencing WCAG "use of color" avoidance; tie to **`static/style.css`** token names briefly.

**Why I sent it**

Design justification is supplementary PDF material per consolidated DOCX outline.

**Assistant / Cursor replied**

> KPI strip conveys portfolio-level metrics without CDN charts by using semantic HTML + CSS grids. Heatmap empties alternate subtle hatch patterns so monochrome printouts still differentiate intensity vs vacant cells; cite tokens like `--heatmap-empty-pattern` equivalents after inspection.

Feeds **`docs/UI_Design_Rationale.md`** cross-linked from SDLC.

---

## Session 14 — Reflection skeleton hitting word budget

**My prompt**

> Outline a 550–650 word first-person reflection: heatmap regression anecdote + CSRF test honesty + prompt decomposition lesson + ethics of polished AI prose vs evidence + limitations paragraph. Explicitly forbid bullet spam; short paragraphs only.

**Why I sent it**

Separate reflection artefact expects structured narrative arcs; scaffolding keeps voice consistent before manual rewrite pass.

**Assistant / Cursor replied**

> Opening: disciplined scepticism mantra. Paragraph 2: recount IndexError path + minimal diff principle. Paragraph 3: refuse CSRF test bypass temptation. Paragraph 4: decomposition wins. Paragraph 5: plagiarism-adjacency & environmental micro-cost awareness. Paragraph 6: limitations (hallucinated workers). Closing: **`pytest`** as arbiter phrase.

Structured draft became **`Reflection_AI_Use.md`** after rewriting into my wording.

---

## Session 15 — Submission packaging checksum voice

**My prompt**

> Draft final human gates before Moodle upload: PDF stem matches zip stem, Figures 1–5 optional HTML prints inserted where cited, rerun DOCX generator after Markdown edits, run full pytest locally once more, omit **`.venv`** from zip.

**Why I sent it**

Process reflection is graded indirectly through coherent artefacts bundle.

**Assistant / Cursor replied**

> Produce ordered checklist aligning `Chinaza-Ogwudiegwu_*` prefixes, insist Word closed during Pandoc overwrite, verify embedded PNG Figures A/B/C inside compiled doc, rerun **`pytest`**, **`Make-SubmissionZip.ps1`** path guard.

Cross-check **`docs/Submission_Guide.md`**.

---

Closing discipline statement

Across every Cursor reply listed above I still:

- edited code myself,
- ran **`pytest -q`** (currently **41** tests collected),
- and only then treated the feature as coursework-complete.
