#!/usr/bin/env python3
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    removed = []
    for directory in REPO_ROOT.rglob("__pycache__"):
        if directory.is_dir():
            shutil.rmtree(directory)
            removed.append(str(directory))
    for pyc in REPO_ROOT.rglob("*.pyc"):
        if pyc.is_file():
            pyc.unlink()
            removed.append(str(pyc))
    if removed:
        print("\n".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
