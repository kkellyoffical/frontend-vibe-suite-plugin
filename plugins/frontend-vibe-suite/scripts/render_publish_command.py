#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO_ROOT), *args], text=True).strip()


def shell_join(parts: list[str]) -> str:
    def quote(part: str) -> str:
        if all(ch.isalnum() or ch in "-_./:@," for ch in part):
            return part
        return "'" + part.replace("'", "'\"'\"'") + "'"

    return " ".join(quote(part) for part in parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a reproducible ClawHub publish command from repository metadata."
    )
    parser.add_argument("--version", help="Release version. Defaults to plugin manifest version.")
    parser.add_argument("--source-ref", help="Release ref or tag. Defaults to v<version> if that tag exists, else current branch.")
    parser.add_argument("--changelog", default="", help="Optional changelog override.")
    args = parser.parse_args()

    plugin = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    publisher = load_json(PLUGIN_ROOT / "data" / "publisher-metadata.json")

    version = args.version or plugin["version"]
    tag_name = f"v{version}"
    known_tags = git_output("tag", "--list", tag_name)
    source_ref = args.source_ref or (tag_name if known_tags == tag_name else git_output("branch", "--show-current"))
    source_commit = git_output("rev-parse", "HEAD")
    changelog_text = args.changelog or f"Release {version}"

    command = [
        "npx", "-y", "clawhub@latest",
        "package", "publish",
        str(PLUGIN_ROOT),
        "--family", publisher["family"],
        "--name", publisher["packageName"],
        "--display-name", publisher["displayName"],
        "--version", version,
        "--changelog", changelog_text,
        "--tags", "latest",
        "--bundle-format", publisher["bundleFormat"],
        "--host-targets", ",".join(publisher["hostTargets"]),
        "--source-repo", publisher["sourceRepo"],
        "--source-commit", source_commit,
        "--source-ref", source_ref,
        "--source-path", publisher["sourcePath"],
    ]

    print(shell_join(command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
