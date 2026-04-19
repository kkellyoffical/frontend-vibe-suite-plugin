#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    plugin_manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    publisher = load_json(PLUGIN_ROOT / "data" / "publisher-metadata.json")
    component_catalog = load_json(PLUGIN_ROOT / "data" / "component-libraries.json")
    prompt_scenarios = load_json(PLUGIN_ROOT / "data" / "prompt-scenarios.json")
    runtime_contract = load_json(PLUGIN_ROOT / "data" / "runtime-contract.json")
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    plugin_readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    hero_svg = (REPO_ROOT / "assets" / "frontend-vibe-suite-hero.svg").read_text(encoding="utf-8")
    env_example = (PLUGIN_ROOT / ".env.example").read_text(encoding="utf-8")
    requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
    runtime_scripts = [
        (PLUGIN_ROOT / "scripts" / "video_to_ui_brief.py").read_text(encoding="utf-8"),
        (PLUGIN_ROOT / "scripts" / "run_visual_loop.py").read_text(encoding="utf-8"),
    ]
    runtime_script_text = "\n".join(runtime_scripts)

    version = plugin_manifest.get("version", "")
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "plugin version is not semver", errors)
    require(plugin_manifest.get("name") == publisher.get("packageName"), "package name mismatch between plugin manifest and publisher metadata", errors)
    require(plugin_manifest.get("interface", {}).get("displayName") == publisher.get("displayName"), "display name mismatch between plugin manifest and publisher metadata", errors)
    require(f"## {version} -" in changelog, f"CHANGELOG.md is missing entry for {version}", errors)
    require(version in root_readme, "root README does not mention current version", errors)
    require(version in hero_svg, "hero SVG does not show current version", errors)

    keywords = plugin_manifest.get("keywords", [])
    require(len(keywords) == len(set(keywords)), "plugin keywords contain duplicates", errors)
    require("frontend" in keywords, "plugin keywords should include 'frontend'", errors)
    require("web-components" in keywords, "plugin keywords should include 'web-components'", errors)

    tag_taxonomy = publisher.get("tagTaxonomy", {})
    require(all(tag_taxonomy.get(bucket) for bucket in ["capability", "frameworks", "modality", "delivery", "libraries"]),
            "publisher metadata is missing one or more tag buckets", errors)
    flattened_tags = {tag for values in tag_taxonomy.values() for tag in values}
    require("react" in flattened_tags and "vue" in flattened_tags and "angular" in flattened_tags,
            "publisher tags should cover multiple framework families", errors)

    require(len(component_catalog.get("libraries", [])) >= 20, "component catalog is smaller than expected", errors)
    require(len(prompt_scenarios.get("scenarios", [])) >= 20, "prompt scenario catalog is smaller than expected", errors)
    require(publisher.get("hostTargets") == ["codex", "openclaw"], "hostTargets should stay ['codex', 'openclaw']", errors)
    require(publisher.get("family") == "bundle-plugin", "publisher family should remain bundle-plugin", errors)
    require(publisher.get("bundleFormat") == "codex", "bundleFormat should remain codex", errors)
    require(runtime_contract.get("pythonDependencies") == [], "runtime contract should declare no third-party Python dependencies", errors)
    require("DASHSCOPE_API_KEY" in env_example, ".env.example must list DASHSCOPE_API_KEY", errors)
    require("DASHSCOPE_API_KEY" in plugin_readme, "plugin README must mention DASHSCOPE_API_KEY", errors)
    require("standard library" in requirements.lower(), "requirements.txt should explicitly document stdlib-only Python usage", errors)
    require(".codex/skills/wan27" not in runtime_script_text, "runtime scripts should not reference home-directory Wan skill paths", errors)
    require(".claude/skills/wan27" not in runtime_script_text, "runtime scripts should not reference Claude-side Wan skill paths", errors)

    tracked = subprocess.check_output(["git", "-C", str(REPO_ROOT), "ls-files"], text=True).splitlines()
    tracked_pyc = [path for path in tracked if path.endswith(".pyc") or "__pycache__/" in path]
    require(not tracked_pyc, f"release tree tracks Python bytecode artifacts: {tracked_pyc[:5]}", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "version": version,
                "packageName": publisher.get("packageName"),
                "hostTargets": publisher.get("hostTargets"),
                "libraryCount": len(component_catalog.get("libraries", [])),
                "scenarioCount": len(prompt_scenarios.get("scenarios", [])),
                "requiredEnv": [item["name"] for item in runtime_contract.get("requiredEnv", [])]
            },
            ensure_ascii=False,
            indent=2
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
