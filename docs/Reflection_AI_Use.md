# Reflection on AI use (aiming near the handbook 500–700 word band — verify printed brief)

Generative assistants were used early for scaffolding and late for polish, never as a substitute for running the app yourself. They sped up drafting tables and Flask route outlines, but each time the model reached for libraries or renamed concepts between sessions it created cleanup work I had to unwind with tests instead of trust.

Two failure-to-fix loops are the ones I would show a marker if asked for proof of human control.

First, the heatmap grid (`habit_tracker/heatmap.py`): a nested loop refactor produced an IndexError because Monday stepping drifted. I pasted the traceback and the rule “no new dependencies,” rejected the assistant’s large redesign, and only accepted a smaller loop rewrite that `tests/test_heatmap.py` could pin. The lesson was that the bug was coordinate logic, not syntax, and only geometry-style tests exposed it.

Second, CSRF synchroniser tokens (`habit_tracker/security.py`) broke naive integration posts in `tests/test_integration.py` with HTTP 403. Turning CSRF off in TESTING would have faked security for the rubric, so instead I extended `tests/support.py` to scrape the hidden field the way a browser would. The assistant suggested brittle HTML matchers; I kept rejecting them until the regex matched the real `_csrf_field` partial. The lesson is that “disable CSRF in tests” is an expedient hallucination and I vetoed it.

What worked was shrinking prompts into verifiable slices. Streak maths lived in pure functions keyed by `HABIT_TODAY`, so English arguments stopped once pytest encoded today-or-yesterday anchors. Prompts moved from “build the whole app” to “Pass A is maths only” and “Pass B is template guardrails,” which is explicit decomposition. Catching mistakes used two habits: never install packages the brief forbids, and never ship a story the test suite does not exercise.

What failed was nostalgic Flask advice and calendar folklore that looked fine on toy dates but broke near real week edges. I treated every patch like an unreviewed PR: smallest diff, full suite, no cherry-picked single-test green.

Ethically, faster drafting raises plagiarism-adjacent risk if you paste external guides without synthesis, and it raises overconfidence if polished prose replaces evidence. I kept prompt logs and appendices so the submission shows adjustment, not pure pasting. Batching questions also felt more responsible than spamming micro-prompts with small environmental cost each time.

Prompt evidence for markers is staged deliberately: **`Prompt_Decision_Log.md`** summarises tactic names versus intent, while **`Prompt_Chats_Appendix.md`** walks each substantive exchange as “what I typed, why I bothered, what Cursor spat back.” I treat that triple format as coursework discipline, not creative writing—the replies are tightened from real sessions so page limits stay humane, yet every story still points to filenames and tests rather than unsubstantiated claims. When Cursor proposed CSRF-shortcuts or database layers I rejected them synchronously rather than retrospectively rewriting history inside the appendix, because academic integrity clauses care about truthful process description as much as they care about originality of prose.

If I repeated the module I would snapshot diagrams before long UI prompt sessions, keep a one-page glossary of words like “streak” and “week,” and paste one failing pytest line per appendix footnote so the tone stays grounded.

On limitations, models do not own production outcomes. They suggest cache layers or background workers that fight the “small stdlib surface” goal. I learned to state invariants up front (“JSON reader never silently drops keys”) so later prompts cannot smuggle behaviour changes.

Net: AI sped mechanical work. Disciplined scepticism plus pytest turned that speed into something I could defend in a viva. The voice I want to own is “I rejected disabling CSRF in tests” and “I made heatmap tests fail before I believed the prose.”
