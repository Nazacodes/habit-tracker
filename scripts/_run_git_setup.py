"""One-off: init git repo and first commit; writes git_setup_result.txt in repo root."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "git_setup_result.txt"


def run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    msg = (p.stdout or "") + (p.stderr or "")
    return p.returncode, msg


def main() -> int:
    lines: list[str] = []
    # Local identity only for this repo (safe if you have no global git config yet).
    setup_cmds = [
        ["git", "--version"],
        ["git", "init"],
        ["git", "config", "user.name", "Chinaza Ogwudiegwu"],
        ["git", "config", "user.email", "ogwudiegwuc@gmail.com"],
        ["git", "add", "-A"],
        ["git", "status", "-sb"],
        [
            "git",
            "commit",
            "-m",
            "Initial commit: Habit Studio (COMP8066 coursework)",
        ],
    ]
    for cmd in setup_cmds:
        code, msg = run(cmd)
        lines.append(f"$ {' '.join(cmd)}\nexit={code}\n{msg}\n")
        if code != 0 and cmd[1] != "status":
            OUT.write_text("\n".join(lines), encoding="utf-8")
            return code
    OUT.write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
