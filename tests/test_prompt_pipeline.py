import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = REPO_ROOT / "plugins" / "frontend-vibe-suite" / "scripts"
EXAMPLES_DIR = REPO_ROOT / "plugins" / "frontend-vibe-suite" / "examples"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def load_script_module(name: str, filename: str):
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PromptPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render_prompt_pack = load_script_module("render_prompt_pack", "render_prompt_pack.py")
        cls.select_prompt_template = load_script_module("select_prompt_template", "select_prompt_template.py")
        cls.choose_library = load_script_module("choose_library", "choose_library.py")
        cls.build_handoff = load_script_module("build_handoff", "build_handoff.py")
        cls.run_visual_loop = load_script_module("run_visual_loop", "run_visual_loop.py")

    def load_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_select_prompt_template_matches_examples(self):
        cases = [
            ("frontend-style-brief.example.json", "operations-console"),
            ("frontend-style-brief.vue.example.json", "admin-crud"),
            ("frontend-style-brief.web-components.example.json", "design-system-docs"),
        ]
        catalog = self.select_prompt_template.load_json(
            SCRIPT_DIR.parent / "data" / "prompt-scenarios.json"
        )
        for filename, expected in cases:
            brief = self.load_json(EXAMPLES_DIR / filename)
            result = self.select_prompt_template.choose_scenario(catalog, brief, "")
            self.assertEqual(result["scenarioProfile"]["id"], expected)

    def test_choose_library_matches_examples(self):
        catalog = self.choose_library.load_json(
            SCRIPT_DIR.parent / "data" / "component-libraries.json"
        )
        react_brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.example.json")
        vue_brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.vue.example.json")
        webc_brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.web-components.example.json")

        react = self.choose_library.choose_route(
            catalog,
            self.choose_library.infer_frameworks(react_brief, []),
            "source-first",
            "dashboard",
            True,
            False,
        )
        vue = self.choose_library.choose_route(
            catalog,
            self.choose_library.infer_frameworks(vue_brief, []),
            "full-suite",
            "dashboard",
            False,
            False,
        )
        webc = self.choose_library.choose_route(
            catalog,
            self.choose_library.infer_frameworks(webc_brief, []),
            "portable",
            "design-system",
            False,
            True,
        )

        self.assertEqual(react["libraryRoute"]["primary"], "shadcn/ui")
        self.assertEqual(vue["libraryRoute"]["primary"], "PrimeVue")
        self.assertEqual(webc["libraryRoute"]["primary"], "Lit")

    def test_render_prompt_pack_includes_stack_and_scenario(self):
        brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.example.json")
        prompt_pack = self.render_prompt_pack.render_prompt_pack(brief)
        self.assertIn("scenario_profile", prompt_pack)
        self.assertIn("stack_profile", prompt_pack)
        self.assertIn("Operations Console", prompt_pack["wan_video_prompt"])
        self.assertIn("shadcn/ui", prompt_pack["build_handoff_prompt"])

    def test_build_handoff_contains_library_and_scenario(self):
        brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.example.json")
        translated = self.load_json(EXAMPLES_DIR / "video-ui-brief.example.json")
        prompt_pack = self.render_prompt_pack.render_prompt_pack(brief)
        handoff = self.build_handoff.merge_handoff(brief, translated, prompt_pack)
        self.assertEqual(handoff["scenario_context"]["id"], "operations-console")
        self.assertEqual(handoff["library_route"]["primary"], "shadcn/ui")
        self.assertIn("Library route:", handoff["coding_prompt"])

    def test_scripts_can_roundtrip_outputs(self):
        brief = self.load_json(EXAMPLES_DIR / "frontend-style-brief.vue.example.json")
        translated = self.load_json(EXAMPLES_DIR / "video-ui-brief.example.json")
        prompt_pack = self.render_prompt_pack.render_prompt_pack(brief)
        handoff = self.build_handoff.merge_handoff(brief, translated, prompt_pack)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            prompt_path = tmp / "prompt-pack.json"
            handoff_path = tmp / "handoff.json"
            markdown_path = tmp / "handoff.md"
            prompt_path.write_text(json.dumps(prompt_pack, ensure_ascii=False, indent=2), encoding="utf-8")
            handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
            markdown_path.write_text(self.build_handoff.to_markdown(handoff), encoding="utf-8")
            self.assertTrue(prompt_path.exists())
            self.assertTrue(handoff_path.exists())
            self.assertTrue(markdown_path.exists())

    def test_i2v_command_uses_explicit_flags(self):
        prompt_pack = self.load_json(EXAMPLES_DIR / "frontend-prompt-pack.example.json")
        args = type(
            "Args",
            (),
            {
                "video_mode": "i2v",
                "video_region": "beijing",
                "video_resolution": "720P",
                "video_duration": 5,
                "video_output": "artifacts/concept.mp4",
                "video_ratio": "16:9",
                "first_frame_url": "https://example.com/first.png",
                "last_frame_url": "https://example.com/last.png",
                "driving_audio_url": "https://example.com/audio.mp3"
            },
        )()
        command = self.run_visual_loop.build_video_command(prompt_pack, args)
        self.assertIn("--first-frame-url", command)
        self.assertIn("--last-frame-url", command)
        self.assertIn("--driving-audio-url", command)
        self.assertNotIn("--media", command)


if __name__ == "__main__":
    unittest.main()
