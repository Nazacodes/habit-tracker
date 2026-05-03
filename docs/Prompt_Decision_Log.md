# Prompt engineering: decision log (COMP8066 Project 2)

The chat evidence is typed for markers in Prompt_Chats_Appendix.md. Every excerpt there follows the same submission layout on purpose:

1. My prompt (quoted as I typed it).
2. Reason I sent it (linked to coursework technique or risk).
3. What Cursor or the assistant answered.

Below is an executive overview plus one matrix that maps technique names to the appendix sessions so reviewers can skim first, then read the verbatim triples later.

## What the workflow aimed for

Requirements were nailed down before any serious code generation so the assistant could not “helpfully” add databases or SaaS integrations. Competitive apps were skimmed only for interaction ideas (heatmap, streak copy, speed of logging a day); nothing pulls data from outside the laptop because the coursework forbids outbound APIs.

After that loop the pattern stayed the same until hand-in:

1. Write a bite-sized brief (often with a persona or forbidden list).
2. Take the suggestion, reshape it manually, integrate in small edits.
3. Run pytest locally; push only when CI is green again.
4. Keep a dated mental note whenever the model hallucinated modules or rewrote Flask APIs wrong so the appendix does not pretend everything was effortless.

## Technique matrix

| Technique | Context you gave | Hard limits | Input (short) | What the model usually returned | What I changed by hand | Why bother using it |
|-----------|--------------------|-------------|---------------|----------------------------------|------------------------|----------------------|
| Role plus constitution | Option A, Flask, JSON, pytest | No SQL, no JWT, no hosted chart CDNs | Cap backlog to eight bullets with deferrals each | Auth and Postgres ideas | Cut back to local JSON and named files | Stops stack sprawl at the first prompt |
| Chain-of-thought | Vague “streak” language | English steps before code | Anchor rule plus three calendar sets | Missed dormant streak days | Locked README sentence and added tests | Surfaces hidden calendar rules |
| Decomposition / chaining | Risk of tangling chart math and routes | Pass A then Pass B, no merge | Pure weekly_counts first, then chart_max story | Almost inlined everything in views | Kept chart_max on server for safe division | Makes pure unit tests possible |
| Few-shot calendar checks | Needed exact integers from ISO strings | Store only normalised dates | Three date sets with expected streak outputs | Failed the gap case once | Added failing test, tightened prompt | Catches confident wrong maths |
| Red-team (CSRF) | Shared lab trust model | No new security libraries | List cookie session CSRF risks | Slight overclaim on clickjacking | Implemented synchroniser tokens and 403 UX | Matches the ethics write-up |
| Verification / minimal diff | pytest IndexError in heatmap | Avoid huge refactors | Paste traceback, ask for minimal fix | Offered full rewrite | Restructured only the row loop | Keeps review readable |
| Competitive / desk research | How big apps feel | Still no external calls | Compare habits apps to our scope | Suggested cloud auth | Took UI patterns only, rejected infra | Grounds the product without cheating constraints |
| Report drafting / ethics scaffolding | Needed numbered AI-risk section | Facts must cite tests/requirements review | Outline four AI dev risks plus mitigations | Over-wrote fluff | Compressed into Mini SDLC 7.4 voice | Bridges rubric wording to codebase |
| Repro diagrams + DOCX toolchain | Marker PDF embed failures on SVG | Pillow-only raster path | Explain PNG generator + pandoc bundle hook | Recommended external Inkscape installs | Locked `make_diagram_pngs.py` + build script integration | Classroom Windows reliability |

## How prompts got shorter over time

Early on I pasted whole sections. Once models.py and storage.py stabilised I switched to one failing test line plus the invariant it should enforce.

HABIT_TODAY stayed pinned so “today” matched between browser demos, appendix screenshots, and CI.

## Hallucinations caught (honest slice)

Phantom database layer suggested after I said “persist” loosely. Blocked by the frozen requirements row that says JSON only.

Streak counted from deepest history once. Neutralised after Session 2 calendar fixtures contradicted it.

Stale Flask decorators recommended from old forum posts. Checked Flask 3.x notes before trusting.

Heatmap row builder threw IndexError on nested Monday math. pytest caught it early; refused a flashy multi-file refactor in favour of a tight loop correction.

## Debugging pattern that worked

Format I kept using: observed behaviour plus suspected folder plus constraint “no extra pip packages unless justified.” The model spat patch sketches, I applied the smallest change, ran the full suite, repeated. Usually three turns per bug.

## Timeline in four beats

1. Freeze MVP table (Sessions 1a–b in appendix).
2. Core calendar logic with tests (Sessions 2–3 plus heatmap Sessions 6a–b).
3. Safety and data portability (Sessions 4–5) plus ethics/STRIDE/diagram scaffolding (Sessions 7–9).
4. Repo hardening / packaging narratives (Sessions 10–15: CI, Windows PNG toolchain, README, UI rationale prose, reflection outline, Moodle gates).

Sessions 10–15 were added explicitly so appendix evidence stretches across report writing, reproducibility tooling, deployment instructions, supplementary design narrative, reflection word-band drafting, and pre-upload discipline—not only CRUD scaffolding.

## Checklist before calling the branch done

- [x] MVP table matched what tests cover
- [x] No surprise external integrations in requirements.txt
- [x] Feature slice not merged without pytest
- [x] Backup path described next to the security section
