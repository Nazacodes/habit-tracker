#!/usr/bin/env python3
"""
Build ONE consolidated submission Word document for COMP8066 Project 2:

  Cover sheet → Mini SDLC report → Prompt & decision log → Prompt chats appendix
  → Reflection on AI use → Supporting UI rationale (supporting appendix)

Outputs: docs/docx/COMP8066_Final_Submission.docx

Prereqs: pip install -r requirements-docx.txt
Also: `pip install pillow` (included via `requirements-docx.txt`). This script runs `make_diagram_pngs.py` so Pandoc receives embedded PNG diagrams on Windows without `rsvg-convert`.

Uses temporary concat Markdown at docs/.submission_compile.tmp.md (overwritten).
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from md_docx_utils import DOCX_PAGE_BREAK_MD, ensure_pandoc, repo_root

BODY_FILES: tuple[tuple[str, str | None], ...] = (
    ("docs/Mini_SDLC_Report.md", None),
    ("docs/Prompt_Decision_Log.md", "# Part II - Prompt engineering and curated evidence"),
    ("docs/Prompt_Chats_Appendix.md", "# Part III - Prompt chat appendix"),
    ("docs/Reflection_AI_Use.md", "# Part IV - Reflection on AI use"),
    ("docs/UI_Design_Rationale.md", "# Appendix A - Supporting UI design rationale"),
)

COVER_MD = """---
title: COMP8066 - AI-powered Mini SDLC (Project 2)
author: 'Chinaza Ogwudiegwu, r002316262'
---

# Consolidated submission (Word master)

Use this `.docx` as the printable spine for `Chinaza-Ogwudiegwu_COMP8066_Assignment_1.pdf` (order: SDLC report, prompt log and appendix excerpts, reflection, UI rationale appendix). Check Moodle hyphen and capitalisation rules before uploading. Aim near the handbook page ceiling for the report body alone. Paste Figures 1-5 screenshots from docs/report-figures or from a running app wherever the prose references them.

Diagrams Figures A/B/C regenerate as PNG inside docs/diagrams when you run scripts/build_final_submission_docx.py (Pillow renders so Windows Word/Pandoc behave).

---


"""


def load_utf8(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    return text


def strip_leading_document_h1(md: str) -> str:
    raw = md.splitlines()
    i = 0
    while i < len(raw) and raw[i].strip() == "":
        i += 1
    if i >= len(raw):
        return ""
    cand = raw[i].lstrip()
    if cand.startswith("# ") and not cand.startswith("##"):
        return "\n".join(raw[i + 1 :]).lstrip("\n") + "\n"
    return md.rstrip() + "\n"


def main() -> None:
    import pypandoc

    ensure_pandoc()
    root = repo_root()

    mp = Path(__file__).resolve().parent / "make_diagram_pngs.py"
    print("[diagrams] PNG export (Pillow) for Pandoc", flush=True)
    proc = subprocess.run(
        [sys.executable, str(mp)],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stdout + proc.stderr, flush=True)
        print("[warn] make_diagram_pngs failed — pip install pillow", flush=True)
    else:
        print(proc.stdout.strip(), flush=True)

    chunks: list[str] = [COVER_MD]

    first = True
    for rel, part_heading in BODY_FILES:
        src = root / Path(rel)
        if not src.is_file():
            print(f"[fatal] Missing source: {src.relative_to(root)}")
            raise SystemExit(2)
        body = load_utf8(src)
        if not first:
            chunks.append(DOCX_PAGE_BREAK_MD)
        first = False
        if part_heading:
            chunks.append("\n")
            chunks.append(part_heading.rstrip())
            chunks.append("\n\n")
            chunks.append(strip_leading_document_h1(body))
        else:
            chunks.append(body.rstrip() + "\n")

    concat_path = root / "docs" / ".submission_compile.tmp.md"
    concat_path.write_text("".join(chunks), encoding="utf-8")

    out_dir = root / "docs" / "docx"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = "COMP8066_Final_Submission"
    candidates: list[Path] = [
        out_dir / f"{stem}.docx",
        out_dir / f"{stem}-generated.docx",
        out_dir / f"{stem}-build-{datetime.now().strftime('%Y%m%d-%H%M%S')}.docx",
    ]

    print("[concat]", concat_path.relative_to(root))
    out_docx: Path | None = None
    pandoc_extra = [
        "--standalone",
        "--resource-path",
        str(root / "docs"),
    ]

    def write_docx(destination: Path) -> None:
        pypandoc.convert_file(
            str(concat_path),
            "docx",
            format="markdown",
            outputfile=str(destination),
            extra_args=pandoc_extra,
        )

    for cand in candidates:
        try:
            if cand.is_file():
                cand.unlink()
        except OSError as exc:
            print(
                f"[warn] could not clear {cand.name} ({exc}); trying next output name",
                flush=True,
            )
            continue
        try:
            print("[docx]", cand.relative_to(root), flush=True)
            write_docx(cand)
            out_docx = cand
            break
        except RuntimeError as exc:
            print(f"[warn] pandoc failed on {cand.name}: {exc}", flush=True)

    if out_docx is None:
        fresh = (
            out_dir / f"{stem}-build-{datetime.now().strftime('%Y%m%d-%H%M%S')}.docx"
        )
        print("[docx]", fresh.relative_to(root), "(fresh timestamp path)", flush=True)
        write_docx(fresh)
        out_docx = fresh

    if out_docx.name != f"{stem}.docx":
        print(
            "[warn] output is not the default filename - close Word and re-run "
            "to overwrite COMP8066_Final_Submission.docx",
            flush=True,
        )

    print("Done ->", out_docx.relative_to(root), flush=True)


if __name__ == "__main__":
    main()
