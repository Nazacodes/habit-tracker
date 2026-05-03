"""Shared helpers for Markdown → Pandoc → Word workflows."""

from __future__ import annotations

import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_pandoc() -> None:
    try:
        import pypandoc

        try:
            pypandoc.get_pandoc_path()
        except OSError:
            print("Downloading Pandoc (one-time)...", flush=True)
            pypandoc.download_pandoc(delete_trash=True)
    except ImportError as e:
        print(
            "Missing pypandoc. Install: pip install -r requirements-docx.txt",
            file=sys.stderr,
        )
        raise SystemExit(1) from e


# Hard page break for DOCX via Pandoc raw OpenXML
DOCX_PAGE_BREAK_MD = """

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

"""
