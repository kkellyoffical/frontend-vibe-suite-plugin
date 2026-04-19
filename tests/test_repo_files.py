import json
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
