#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCENARIO_PATH = SCRIPT_DIR.parent / "data" / "prompt-scenarios.json"


def load_brief(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_or_empty(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def bullet_list(values) -> str:
    if not values:
        return "- none provided"
    return "\n".join(f"- {value}" for value in values)


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
        "id": top.get("id", "general-product-app"),
        "label": top.get("label", "General Product App"),
        "deliveryShape": top.get("deliveryShape", "web app"),
        "imageDirectives": top.get("imageDirectives", []),
        "videoDirectives": top.get("videoDirectives", []),
        "omniDirectives": top.get("omniDirectives", []),
        "buildDirectives": top.get("buildDirectives", []),
        "fallbackCandidates": [item.get("id") for item in ranked[1:4]],
    }


def score_scenario(scenario: dict, brief: dict, scenario_hint: str) -> int:
    score = 0
    if scenario_hint:
        hint = scenario_hint.strip().lower()
        if hint == str(scenario.get("id", "")).lower() or hint == str(scenario.get("label", "")).lower():
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

    delivery_shape = str(brief.get("deliveryShape", "")).lower()
    if delivery_shape and delivery_shape == str(scenario.get("deliveryShape", "")).lower():
        score += 6
    if not haystack and scenario.get("id") == "general-product-app":
        score += 1
    return score


def render_prompt_pack(brief: dict, scenario_hint: str = "") -> dict:
    product = brief.get("product", "product")
    surface = brief.get("surface", "web application")
    goal = brief.get("primaryGoal", "deliver a clear primary user task")
    users = ", ".join(brief.get("users", [])) or "general users"
    mood = ", ".join(brief.get("brandMood", [])) or "clear, modern, high-signal"
    layout = brief.get("layoutDirection", "structured and readable")
    density = brief.get("density", "balanced")
    color = brief.get("colorDirection", "brand-aligned, readable contrast")
    typography = brief.get("typographyDirection", "clean sans-serif system")
    motion = brief.get("motionDirection", "restrained, meaningful transitions")
    content_tone = brief.get("contentTone", "product-facing, concise, useful")
    visual_refs = ", ".join(brief.get("visualReferences", [])) or "no explicit references"
    stack_targets = ", ".join(list_or_empty(brief.get("stackTargets"))) or "not specified"
    component_prefs = ", ".join(list_or_empty(brief.get("componentPreferences"))) or "not specified"
    library_route = brief.get("libraryRoute") if isinstance(brief.get("libraryRoute"), dict) else None
    library_route_text = ""
    if library_route:
        primary = library_route.get("primary")
        fallback = ", ".join(list_or_empty(library_route.get("fallback")))
        frameworks = ", ".join(list_or_empty(library_route.get("frameworks")))
        mode = library_route.get("mode", "not specified")
        reason = library_route.get("reason", "not specified")
        caveats = ", ".join(list_or_empty(library_route.get("caveats")))
        library_route_text = (
            f"Preferred library route: {primary or 'not specified'}\n"
            f"Fallbacks: {fallback or 'not specified'}\n"
            f"Frameworks covered: {frameworks or 'not specified'}\n"
            f"Mode: {mode}\n"
            f"Reason: {reason}\n"
            f"Caveats: {caveats or 'none'}\n"
        )

    must_have = bullet_list(brief.get("mustHave", []))
    anti_goals = bullet_list(brief.get("antiGoals", []))
    constraints = bullet_list(brief.get("technicalConstraints", []))
    acceptance = bullet_list(brief.get("acceptanceCriteria", []))
    scenario_profile = choose_scenario(load_brief(SCENARIO_PATH), brief, scenario_hint or str(brief.get("promptScenario", "")))
    image_directives = bullet_list(scenario_profile.get("imageDirectives", []))
    video_directives = bullet_list(scenario_profile.get("videoDirectives", []))
    omni_directives = bullet_list(scenario_profile.get("omniDirectives", []))
    build_directives = bullet_list(scenario_profile.get("buildDirectives", []))

    common_context = (
        f"Product: {product}\n"
        f"Primary surface: {surface}\n"
        f"Primary goal: {goal}\n"
        f"Prompt scenario: {scenario_profile.get('label')} ({scenario_profile.get('id')})\n"
        f"Delivery shape: {scenario_profile.get('deliveryShape')}\n"
        f"Target users: {users}\n"
        f"Brand mood: {mood}\n"
        f"Layout direction: {layout}\n"
        f"Density: {density}\n"
        f"Color direction: {color}\n"
        f"Typography direction: {typography}\n"
        f"Motion direction: {motion}\n"
        f"Content tone: {content_tone}\n"
        f"Visual references: {visual_refs}\n"
        f"Target stacks: {stack_targets}\n"
        f"Component preferences: {component_prefs}\n"
        f"{library_route_text}"
        f"Must-have elements:\n{must_have}\n"
        f"Anti-goals:\n{anti_goals}\n"
        f"Technical constraints:\n{constraints}\n"
        f"Acceptance criteria:\n{acceptance}"
    )

    wan_image_prompt = (
        "Create a polished UI concept frame for a modern digital product.\n"
        f"{common_context}\n"
        f"Scenario-specific image directives:\n{image_directives}\n"
        "Show a realistic product interface, not a moodboard. Preserve readable hierarchy, "
        "clear spacing, and believable product chrome. No watermark. No explanatory labels."
    )

    wan_video_prompt = (
        "Create a short showcase video of a frontend product experience.\n"
        f"{common_context}\n"
        f"Scenario-specific video directives:\n{video_directives}\n"
        "The video should reveal the page hierarchy, navigation, content rhythm, and motion language. "
        "Favor one concrete product flow over abstract camera movement. Keep the scene grounded in real UI."
    )

    omni_translation_prompt = (
        "Analyze this UI design video as a frontend lead. Return a structured brief that names layout regions, "
        "design tokens, interaction patterns, motion cues, content structure, component types, likely stack fit, "
        "and open ambiguities. Prefer concrete frontend language over cinematic commentary.\n"
        f"{common_context}\n"
        f"Scenario-specific translation directives:\n{omni_directives}"
    )

    build_handoff_prompt = (
        "Implement this frontend strictly from the translated UI brief and the original style brief.\n"
        f"{common_context}\n"
        f"Scenario-specific implementation directives:\n{build_directives}\n"
        "Preserve the hierarchy, visual tone, motion attitude, and anti-goals. "
        "Do not improvise new product directions. Call out any ambiguity that remains after the video translation."
    )

    return {
        "style_brief": brief,
        "scenario_profile": scenario_profile,
        "stack_profile": {
            "targets": list_or_empty(brief.get("stackTargets")),
            "component_preferences": list_or_empty(brief.get("componentPreferences")),
            "library_route": library_route,
        },
        "wan_image_prompt": wan_image_prompt,
        "wan_video_prompt": wan_video_prompt,
        "omni_translation_prompt": omni_translation_prompt,
        "build_handoff_prompt": build_handoff_prompt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a multimodal prompt pack from a frontend style brief JSON file."
    )
    parser.add_argument("--brief", required=True, help="Path to the input style brief JSON.")
    parser.add_argument("--scenario", default="", help="Optional explicit prompt scenario id or label.")
    parser.add_argument("--output", required=True, help="Path to write the prompt pack JSON.")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    output_path = Path(args.output)

    prompt_pack = render_prompt_pack(load_brief(brief_path), scenario_hint=args.scenario)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(prompt_pack, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
