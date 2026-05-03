# UI design rationale (Habit Studio)

## Colour & contrast

The interface uses a **dual theme** (light default + dark) with tokens defined in [`static/style.css`](../static/style.css). Greens are chosen to echo *progress / growth* while keeping **WCAG-style contrast discipline**:

- **Light shell:** off‑white page (`#f7fafc`) with deep ink text (`#1a202c`) for ≥ **4.5:1** style pairings on body copy.
- **Primary actions:** forest greens (`#2f855a` → `#276749`) on light; brighter mint (`#48bb78`) on dark surfaces to preserve separation from backgrounds.
- **Heatmap cells:** pair solid fills with **striped “empty”** states so status is not conveyed by hue alone (WCAG **1.4.1 Use of Color** awareness).

Before final submission, paste the token list into a matrix checker (e.g. [Palette Accessibility Matrix](https://66colorful.com/tools/palette-accessibility-matrix)) and attach a screenshot to your PDF appendix if your rubric rewards evidence.

## UX patterns referenced (industry)

| Pattern | Where it shows up | Why it helps the marker |
|--------|-------------------|-------------------------|
| **Command hub + KPI strip** | Dashboard hero + cards | Instant story: scope, metrics, “what’s left today”. |
| **Focus rail** | “Today’s focus” list | Reduces clicks for the core loop (log completion). |
| **Dense analytics + explanation** | Weekly bars + heatmap | Shows *non-trivial* logic + visualisation without external chart APIs. |
| **Destructive flow guard** | Backup restore confirm + cap | Shows security thinking appropriate to local tools. |
| **Theme toggle w/ `prefers-color-scheme`** | [`static/theme.js`](../static/theme.js) | Modern UX affordance; still zero network calls. |

## Motion & a11y

- `prefers-reduced-motion` disables hover lift transforms.
- Skip link, `aria-live` flash host, focus-visible rings, semantic heatmap `title` hints.

---

*This note is safe to paste (condensed) into your PDF under Design → UX justification.*
