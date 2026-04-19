#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCENARIO_PATH = SCRIPT_DIR.parent / "data" / "prompt-scenarios.json"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_or_empty(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def normalize(text: str) -> str:
    return text.strip().lower()


def score_scenario(scenario: dict, brief: dict, scenario_hint: str) -> int:
    score = 0
    if scenario_hint:
        hint = normalize(scenario_hint)
        if hint == normalize(scenario.get("id", "")) or hint == normalize(scenario.get("label", "")):
            score += 20

    text_parts = []
    for key in ["product", "surface", "primaryGoal", "layoutDirection", "contentTone", "deliveryShape", "promptScenario"]:
        value = brief.get(key)
        if isinstance(value, str):
            text_parts.append(value.lower())
    for key in ["users", "brandMood", "visualReferences", "stackTargets", "componentPreferences", "mustHave", "antiGoals", "technicalConstraints"]:
        text_parts.extend(item.lower() for item in list_or_empty(brief.get(key)))
    haystack = " ".join(text_parts)

    for signal in scenario.get("signals", []):
        if signal.lower() in haystack:
            score += 4

    delivery_shape = normalize(str(brief.get("deliveryShape", "")))
    if delivery_shape and delivery_shape == normalize(str(scenario.get("deliveryShape", ""))):
        score += 6

    if not haystack and scenario.get("id") == "general-product-app":
        score += 1
    return score


def choose_scenario(catalog: dict, brief: dict, scenario_hint: str) -> dict:
    if not scenario_hint:
        scenario_hint = str(brief.get("promptScenario", ""))
    scenarios = catalog.get("scenarios", [])
    ranked = sorted(
        scenarios,
        key=lambda item: score_scenario(item, brief, scenario_hint),
        reverse=True,
    )
    top = ranked[0] if ranked else {}
    return {
        "scenarioProfile": {
            "id": top.get("id", "general-product-app"),
            "label": top.get("label", "General Product App"),
            "deliveryShape": top.get("deliveryShape", "web app"),
            "imageDirectives": top.get("imageDirectives", []),
            "videoDirectives": top.get("videoDirectives", []),
            "omniDirectives": top.get("omniDirectives", []),
            "buildDirectives": top.get("buildDirectives", []),
            "fallbackCandidates": [item.get("id") for item in ranked[1:4]]
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Choose a frontend prompt scenario from a style brief."
    )
    parser.add_argument("--brief", required=True, help="Path to the style brief JSON.")
    parser.add_argument("--scenario", default="", help="Optional explicit scenario id or label override.")
    parser.add_argument("--output", help="Optional output JSON path.")
    args = parser.parse_args()

    brief = load_json(Path(args.brief))
    result = choose_scenario(load_json(SCENARIO_PATH), brief, args.scenario or str(brief.get("promptScenario", "")))

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
