import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parent.parent


class RepoFileTests(unittest.TestCase):
    def test_prompt_scenarios_count(self):
        data = json.loads(
            (REPO_ROOT / "plugins" / "frontend-vibe-suite" / "data" / "prompt-scenarios.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(len(data.get("scenarios", [])), 20)

    def test_component_library_catalog_has_multiframe_entries(self):
        data = json.loads(
            (REPO_ROOT / "plugins" / "frontend-vibe-suite" / "data" / "component-libraries.json").read_text(
                encoding="utf-8"
            )
        )
        names = {item["name"] for item in data.get("libraries", [])}
        expected = {"React Aria", "Radix UI", "shadcn/ui", "PrimeVue", "PrimeNG", "Bits UI", "Lit", "DaisyUI"}
        self.assertTrue(expected.issubset(names))

    def test_readme_mentions_routing_and_scenarios(self):
        root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        plugin_readme = (REPO_ROOT / "plugins" / "frontend-vibe-suite" / "README.md").read_text(encoding="utf-8")
        self.assertIn("component-library-routing.md", root_readme)
        self.assertIn("prompt-scenarios.json", plugin_readme)
        self.assertIn("DASHSCOPE_API_KEY", plugin_readme)
        self.assertIn("0.0.4", root_readme)
        self.assertIn("0.0.4", plugin_readme)

    def test_runtime_contract_declares_required_env(self):
        data = json.loads(
            (REPO_ROOT / "plugins" / "frontend-vibe-suite" / "data" / "runtime-contract.json").read_text(
                encoding="utf-8"
            )
        )
        required = {item["name"] for item in data.get("requiredEnv", [])}
        self.assertIn("DASHSCOPE_API_KEY", required)

    def test_runtime_scripts_do_not_read_other_skill_env_files(self):
        scripts = [
            REPO_ROOT / "plugins" / "frontend-vibe-suite" / "scripts" / "video_to_ui_brief.py",
            REPO_ROOT / "plugins" / "frontend-vibe-suite" / "scripts" / "run_visual_loop.py",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in scripts)
        self.assertNotIn(".codex/skills/wan27", combined)
        self.assertNotIn(".claude/skills/wan27", combined)

    def test_release_tree_has_no_pyc(self):
        tracked = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "ls-files"],
            text=True,
        ).splitlines()
        tracked_pyc = [path for path in tracked if path.endswith(".pyc") or "__pycache__/" in path]
        self.assertEqual(tracked_pyc, [])


if __name__ == "__main__":
    unittest.main()
