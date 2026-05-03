#!/usr/bin/env python3
"""
Export Markdown reports under docs/ to Word (.docx) via Pandoc.

Usage (from repo root):
  pip install -r requirements-docx.txt
  python scripts/export_reports_to_docx.py

First run may download a Pandoc binary through pypandoc if none is on PATH.
Mermaid diagrams remain as code blocks in Word unless you paste rendered images.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from md_docx_utils import ensure_pandoc, repo_root

REPORTS: list[tuple[str, str | None]] = [
    ("docs/Mini_SDLC_Report.md", None),
    ("docs/Prompt_Decision_Log.md", None),
    ("docs/Prompt_Chats_Appendix.md", None),
    ("docs/Reflection_AI_Use.md", None),
    ("docs/UI_Design_Rationale.md", None),
    ("docs/Submission_Guide.md", None),
    ("docs/INTEGRITY_EXEMPLARS_README.md", None),
    ("docs/report-figures/README.md", "report-figures_README.docx"),
]


def main() -> None:
    import pypandoc

    ensure_pandoc()
    root = repo_root()
    out_dir = root / "docs" / "docx"
    out_dir.mkdir(parents=True, exist_ok=True)

    for rel_src, rename in REPORTS:
        src = root / Path(rel_src)
        if not src.is_file():
            print(f"[skip] Missing: {src.relative_to(root)}", flush=True)
            continue
        out_name = rename or (src.stem + ".docx")
        dst = out_dir / out_name
        print(f"[docx] {src.relative_to(root)} -> docs/docx/{out_name}", flush=True)
        pypandoc.convert_file(
            str(src),
            "docx",
            format="markdown",
            outputfile=str(dst),
            extra_args=[
                "--standalone",
                "--resource-path",
                str(root / "docs"),
            ],
        )
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
