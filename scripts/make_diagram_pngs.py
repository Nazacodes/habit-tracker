#!/usr/bin/env python3
"""Emit docs/diagrams/fig*.png using Pillow — high-level figures only."""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_OUT = _ROOT / "docs" / "diagrams"


def fonts():
    from PIL import ImageFont

    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20),
            ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15),
            ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13),
            ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11),
        )
    except Exception:
        d = ImageFont.load_default()
        return d, d, d, d


def architecture() -> None:
    from PIL import Image, ImageDraw

    _OUT.mkdir(parents=True, exist_ok=True)
    tfont, nb, sm, xs = fonts()
    w, h = 1520, 540
    im = Image.new("RGB", (w, h), "#fafbfc")
    dr = ImageDraw.Draw(im)

    def rrect(xy, outline, fill_, rad=12, width_=2):
        dr.rounded_rectangle(xy, radius=rad, outline=outline, fill=fill_, width=width_)

    dr.text((w // 2, 22), "Figure A - High-level architecture (prototype)", fill="#1a202c", font=tfont, anchor="mm")

    rrect((44, 70, 400, 420), "#6b9280", "#f2faf5")
    dr.text((222, 94), "Client (your browser)", fill="#143021", font=nb, anchor="mm")
    dr.text((222, 138), "- Renders dashboards, forms, streak views", fill="#374151", font=sm, anchor="mm")
    dr.text((222, 168), "- Normal clicks and form submits", fill="#374151", font=sm, anchor="mm")
    dr.text((222, 210), "Runs against localhost only for coursework.", fill="#6b7280", font=xs, anchor="mm")

    mid_y = 248
    dr.line((400, mid_y, 518, mid_y), fill="#2f6b4f", width=4)
    dr.polygon(((522, mid_y), (512, mid_y - 7), (512, mid_y + 7)), fill="#2f6b4f")
    dr.text((461, mid_y - 42), "page requests / HTML back", fill="#374151", font=xs, anchor="mm")

    rrect((528, 70, 1004, 420), "#6b8299", "#f3f7fb")
    dr.text((766, 94), "Application tier (Python web app)", fill="#15202e", font=nb, anchor="mm")
    dr.text((766, 138), "- Receives browsing and submits", fill="#374151", font=sm, anchor="mm")
    dr.text((766, 168), "- Validates habit text + guarded forms", fill="#374151", font=sm, anchor="mm")
    dr.text((766, 198), "- CRUD + streak maths + charts + snapshots", fill="#374151", font=sm, anchor="mm")
    dr.text((766, 228), "- Sends updated HTML screens", fill="#374151", font=sm, anchor="mm")
    dr.text((766, 275), "Single user, runs on one laptop.", fill="#6b7280", font=xs, anchor="mm")

    dr.line((1004, mid_y, 1122, mid_y), fill="#475569", width=4)
    dr.polygon(((1126, mid_y), (1116, mid_y - 7), (1116, mid_y + 7)), fill="#475569")
    dr.text((1063, mid_y - 42), "load/save structured records", fill="#374151", font=xs, anchor="mm")

    rrect((1132, 70, 1476, 420), "#4b5568", "#1f2937")
    dr.text((1304, 100), "Persistence (file acts like a tiny database)", fill="#f9fafb", font=nb, anchor="mm")
    dr.text((1304, 140), "- One JSON file with habits + dates", fill="#e5e7eb", font=sm, anchor="mm")
    dr.text((1304, 170), "- A real rollout might swap this for SQLite", fill="#e5e7eb", font=sm, anchor="mm")
    dr.text((1304, 210), "- Backup/export is your manual portability path", fill="#e5e7eb", font=sm, anchor="mm")

    dr.text((w // 2, 478), "Section 4 links this sketch to concrete code files.", fill="#6b7280", font=xs, anchor="mm")

    im.save(_OUT / "fig01-architecture.png", dpi=(144, 144))
    print("[ok]", (_OUT / "fig01-architecture.png").relative_to(_ROOT))


def sequence_create() -> None:
    from PIL import Image, ImageDraw

    tfont, _, lf, xf = fonts()
    w, h = 1280, 500
    im = Image.new("RGB", (w, h), "#ffffff")
    dr = ImageDraw.Draw(im)
    dr.text((w // 2, 22), "Figure B - Creating a habit (happy path)", fill="#1a202c", font=tfont, anchor="mm")

    cols = [(110, "Browser"), (470, "App server"), (900, "Stored data")]
    y0 = 62
    y1 = 430
    xs = []
    for x, name in cols:
        xs.append(x)
        dr.line((x, y0, x, y1), fill="#cbd5e0", width=2)
        dr.text((x, y0 - 6), name, fill="#1a202c", font=lf, anchor="md")
    B_, A_, D_ = xs

    def fwd(y, xl, xr, lab):
        dr.line((xl + 12, y, xr - 12, y), fill="#1f2937", width=2)
        dr.polygon(((xr - 12, y), (xr - 22, y - 5), (xr - 22, y + 5)), fill="#1f2937")
        dr.text(((xl + xr) / 2, y - 14), lab, fill="#4b5563", font=xf, anchor="md")

    def back(y, xl, xr, lab):
        dr.line((xr - 12, y, xl + 12, y), fill="#78716c", width=2)
        dr.polygon(((xl + 12, y), (xl + 22, y - 5), (xl + 22, y + 5)), fill="#78716c")
        dr.text(((xl + xr) / 2, y - 14), lab, fill="#78716c", font=xf, anchor="md")

    y = 100
    fwd(y, B_, A_, "Post new habit form")
    y += 44
    dr.text(((B_ + A_) / 2, y), "checks token + validates text", fill="#4b5563", font=xf, anchor="md")
    y += 38
    fwd(y, A_, D_, "Write habit row into snapshot")
    y += 44
    back(y, A_, D_, "Confirm save completed")
    y += 44
    back(y, B_, A_, "Redirect browser to habit page")

    dr.text((w // 2, 460), "Mirrors integration test create-then-fetch flow.", fill="#9ca3af", font=xf, anchor="mm")
    im.save(_OUT / "fig02-sequence-create.png", dpi=(144, 144))
    print("[ok]", (_OUT / "fig02-sequence-create.png").relative_to(_ROOT))


def sequence_mark_complete() -> None:
    from PIL import Image, ImageDraw

    tfont, _, lf, xf = fonts()
    w, h = 1280, 460
    im = Image.new("RGB", (w, h), "#ffffff")
    dr = ImageDraw.Draw(im)
    dr.text((w // 2, 22), "Figure C - Marking a habit done for one date", fill="#1a202c", font=tfont, anchor="mm")

    cols = [(110, "Browser"), (470, "App server"), (900, "Stored data")]
    y0 = 62
    y1 = 380
    xs = []
    for x, name in cols:
        xs.append(x)
        dr.line((x, y0, x, y1), fill="#cbd5e0", width=2)
        dr.text((x, y0 - 6), name, fill="#1a202c", font=lf, anchor="md")
    B_, A_, D_ = xs

    def fwd(y, xl, xr, lab):
        dr.line((xl + 12, y, xr - 12, y), fill="#1f2937", width=2)
        dr.polygon(((xr - 12, y), (xr - 22, y - 5), (xr - 22, y + 5)), fill="#1f2937")
        dr.text(((xl + xr) / 2, y - 14), lab, fill="#4b5563", font=xf, anchor="md")

    def back(y, xl, xr, lab):
        dr.line((xr - 12, y, xl + 12, y), fill="#78716c", width=2)
        dr.polygon(((xl + 12, y), (xl + 22, y - 5), (xl + 22, y + 5)), fill="#78716c")
        dr.text(((xl + xr) / 2, y - 14), lab, fill="#78716c", font=xf, anchor="md")

    y = 100
    fwd(y, B_, A_, "Post completion for chosen ISO date")
    y += 42
    dr.text(((B_ + A_) / 2, y), "validate token then merge date into habit", fill="#4b5563", font=xf, anchor="md")
    y += 36
    fwd(y, A_, D_, "Persist updated completions list")
    y += 42
    back(y, B_, A_, "Reload page showing new streak tally")

    dr.text((w // 2, 410), "Same pattern for quick-done from dashboard rail.", fill="#9ca3af", font=xf, anchor="mm")

    im.save(_OUT / "fig03-sequence-mark.png", dpi=(144, 144))
    print("[ok]", (_OUT / "fig03-sequence-mark.png").relative_to(_ROOT))


def main() -> None:
    architecture()
    sequence_create()
    sequence_mark_complete()


if __name__ == "__main__":
    main()
